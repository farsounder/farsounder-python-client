from __future__ import annotations

import logging
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Literal

import zmq
from google.protobuf.message import Message

from farsounder.proto.proto import nav_api_pb2 as nav_api
from farsounder.client.config import (
    ClientConfig,
    PubSubMessage,
    build_config,
    resolve_pubsub_port,
)

logger = logging.getLogger(__name__)

MessageCallback = Callable[[Message], None]

PUBSUB_MESSAGE_CLASSES: dict[PubSubMessage, type[Message]] = {
    "HydrophoneData": nav_api.HydrophoneData,
    "TargetData": nav_api.TargetData,
    "RawTargetData": nav_api.RawTargetData,
    "ProcessorSettings": nav_api.ProcessorSettings,
    "VesselInfo": nav_api.VesselInfo,
}


class Subscription:
    """Subscription to pub-sub messages using background threads."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._callbacks: dict[PubSubMessage, list[MessageCallback]] = {
            message_type: [] for message_type in PUBSUB_MESSAGE_CLASSES
        }
        self._threads: list[threading.Thread] = []
        self._running = False
        self._stop_event = threading.Event()
        self._use_threadpool = config.callback_executor == "threadpool"
        self._executor: ThreadPoolExecutor | None = (
            ThreadPoolExecutor() if self._use_threadpool else None
        )

    def on(self, message_type: PubSubMessage, callback: MessageCallback) -> None:
        """Register a callback for a pub-sub message type.

        Parameters
        ----------
        message_type
            Pub-sub message type to listen for.
        callback
            Callback invoked with the parsed protobuf message. Sync callbacks
            are run in a thread pool by default.
        """

        if message_type not in PUBSUB_MESSAGE_CLASSES:
            raise ValueError(f"Unknown pub-sub message type: {message_type}")
        self._callbacks[message_type].append(callback)

    def start(self) -> None:
        """Start background receive threads for subscribed message types."""

        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        if self._use_threadpool and self._executor is None:
            self._executor = ThreadPoolExecutor()

        for message_type in self._config.subscribe:
            thread = threading.Thread(
                target=self._recv_loop,
                args=(message_type,),
                name=f"farsounder-sub-{message_type}",
                daemon=True,
            )
            thread.start()
            self._threads.append(thread)

    def stop(self) -> None:
        """Stop background receive threads."""

        if not self._running:
            return
        self._running = False
        self._stop_event.set()

        for thread in self._threads:
            thread.join()
        self._threads.clear()

        if self._executor is not None:
            self._executor.shutdown(wait=True)
            self._executor = None

    def __enter__(self) -> "Subscription":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    def _recv_loop(self, message_type: PubSubMessage) -> None:
        port = resolve_pubsub_port(self._config, message_type)
        socket = zmq.Context.instance().socket(zmq.SUB)
        socket.setsockopt(zmq.SUBSCRIBE, b"")
        socket.connect(f"tcp://{self._config.host}:{port}")
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        message_cls = PUBSUB_MESSAGE_CLASSES[message_type]
        try:
            while not self._stop_event.is_set():
                try:
                    events = dict(poller.poll(timeout=1000))
                except Exception:
                    if self._stop_event.is_set():
                        break
                    logger.exception("Failed to poll %s", message_type)
                    continue

                if socket not in events:
                    continue

                try:
                    data = socket.recv()
                except Exception:
                    if self._stop_event.is_set():
                        break
                    logger.exception("Failed to receive %s", message_type)
                    continue

                try:
                    message = message_cls()
                    message.ParseFromString(data)
                except Exception:
                    logger.exception("Failed to parse %s", message_type)
                    continue

                self._dispatch(message_type, message)
        finally:
            socket.close(linger=0)

    def _dispatch(self, message_type: PubSubMessage, message: Message) -> None:
        callbacks = list(self._callbacks.get(message_type, []))
        if not callbacks:
            return

        for callback in callbacks:
            if self._use_threadpool and self._executor is not None:
                future = self._executor.submit(callback, message)
                future.add_done_callback(self._log_task_result)
                continue

            try:
                callback(message)
            except Exception:
                logger.exception("Callback error for %s", message_type)

    @staticmethod
    def _log_task_result(task: Future[object]) -> None:
        try:
            task.result()
        except Exception:
            logger.exception("Callback task failed")


def subscribe(
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    subscribe: Iterable[PubSubMessage] | None = None,
    port_overrides: dict[str, int] | None = None,
    callback_executor: Literal["threadpool", "inline"] = "threadpool",
) -> Subscription:
    """Create a subscription for pub-sub messages.

    Parameters
    ----------
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for all sockets.
    subscribe
        Pub-sub message types to subscribe to.
    port_overrides
        Mapping of message or endpoint name to port number.
    callback_executor
        Whether to run sync callbacks in a thread pool or inline.

    Returns
    -------
    Subscription
        Subscription instance for registering callbacks and starting IO.
    """

    if config is None:
        config = build_config(
            host=host,
            subscribe=subscribe,
            port_overrides=port_overrides,
            callback_executor=callback_executor,
        )
    return Subscription(config)
