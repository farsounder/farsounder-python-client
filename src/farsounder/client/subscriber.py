from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Iterable
from typing import Awaitable, Literal

import zmq
import zmq.asyncio
from google.protobuf.message import Message

from farsounder.proto.proto import nav_api_pb2 as nav_api
from farsounder.client.config import (
    ClientConfig,
    PubSubMessage,
    build_config,
    resolve_pubsub_port,
)

logger = logging.getLogger(__name__)

MessageCallback = Callable[[Message], Awaitable[None] | None]

PUBSUB_MESSAGE_CLASSES: dict[PubSubMessage, type[Message]] = {
    "HydrophoneData": nav_api.HydrophoneData,
    "TargetData": nav_api.TargetData,
    "ProcessorSettings": nav_api.ProcessorSettings,
    "VesselInfo": nav_api.VesselInfo,
}


class Subscription:
    """Async subscription to pub-sub messages."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._callbacks: dict[PubSubMessage, list[MessageCallback]] = {
            message_type: [] for message_type in PUBSUB_MESSAGE_CLASSES
        }
        self._ctx = zmq.asyncio.Context.instance()
        self._sockets: dict[PubSubMessage, zmq.asyncio.Socket] = {}
        self._tasks: list[asyncio.Task[None]] = []
        self._running = False
        self._use_threadpool = config.callback_executor == "threadpool"

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

    async def start(self) -> None:
        """Start background receive tasks for subscribed message types."""

        if self._running:
            return
        self._running = True

        for message_type in self._config.subscribe:
            port = resolve_pubsub_port(self._config, message_type)
            socket = self._ctx.socket(zmq.SUB)
            socket.setsockopt(zmq.SUBSCRIBE, b"")
            socket.connect(f"tcp://{self._config.host}:{port}")
            self._sockets[message_type] = socket
            self._tasks.append(
                asyncio.create_task(self._recv_loop(message_type, socket))
            )

    async def stop(self) -> None:
        """Stop background receive tasks and close sockets."""

        if not self._running:
            return
        self._running = False

        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

        for socket in self._sockets.values():
            socket.close(linger=0)
        self._sockets.clear()

    async def __aenter__(self) -> "Subscription":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.stop()

    async def _recv_loop(
        self, message_type: PubSubMessage, socket: zmq.asyncio.Socket
    ) -> None:
        message_cls = PUBSUB_MESSAGE_CLASSES[message_type]
        while True:
            try:
                data = await socket.recv()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Failed to receive %s", message_type)
                continue

            try:
                message = message_cls()
                message.ParseFromString(data)
            except Exception:
                logger.exception("Failed to parse %s", message_type)
                continue

            self._dispatch(message_type, message)

    def _dispatch(self, message_type: PubSubMessage, message: Message) -> None:
        callbacks = list(self._callbacks.get(message_type, []))
        if not callbacks:
            return

        loop = asyncio.get_running_loop()
        for callback in callbacks:
            if self._use_threadpool and not asyncio.iscoroutinefunction(callback):
                future = loop.run_in_executor(None, callback, message)
                future.add_done_callback(self._log_task_result)
                continue

            try:
                result = callback(message)
            except Exception:
                logger.exception("Callback error for %s", message_type)
                continue

            if asyncio.iscoroutine(result):
                task = asyncio.create_task(result)
                task.add_done_callback(self._log_task_result)

    @staticmethod
    def _log_task_result(task: asyncio.Future[object]) -> None:
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
