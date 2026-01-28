from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping

PubSubMessage = Literal[
    "HydrophoneData",
    "TargetData",
    "ProcessorSettings",
    "VesselInfo",
]

ReqRepEndpoint = Literal[
    "GetProcessorSettings",
    "SetFieldOfView",
    "SetBottomDetection",
    "SetInWaterSquelch",
    "SetSquelchlessInWaterDetector",
    "GetVesselInfo",
    "SetDraft",
    "SetKeelOffset",
]

PUBSUB_DEFAULT_PORTS: dict[PubSubMessage, int] = {
    "HydrophoneData": 61501,
    "TargetData": 61502,
    "ProcessorSettings": 61503,
    "VesselInfo": 61504,
}

REQREP_DEFAULT_PORTS: dict[ReqRepEndpoint, int] = {
    "GetProcessorSettings": 60501,
    "SetFieldOfView": 60502,
    "SetBottomDetection": 60503,
    "SetInWaterSquelch": 60504,
    "SetSquelchlessInWaterDetector": 60505,
    "GetVesselInfo": 60506,
    "SetDraft": 60507,
    "SetKeelOffset": 60508,
}


@dataclass(frozen=True)
class ClientConfig:
    """Configuration for the ZeroMQ client.

    Parameters
    ----------
    host
        Hostname or IP address for all sockets.
    subscribe
        Pub-sub message types to subscribe to.
    pubsub_ports
        Port mapping for pub-sub message types.
    reqrep_ports
        Port mapping for request-reply endpoints.
    callback_executor
        Whether to run sync callbacks in a thread pool or inline.
    timeout_s
        Request-reply timeout in seconds.
    """

    host: str
    subscribe: tuple[PubSubMessage, ...]
    pubsub_ports: dict[PubSubMessage, int]
    reqrep_ports: dict[ReqRepEndpoint, int]
    callback_executor: Literal["threadpool", "inline"]
    timeout_s: float


def build_config(
    host: str = "127.0.0.1",
    subscribe: Iterable[PubSubMessage] | None = None,
    port_overrides: Mapping[str, int] | None = None,
    callback_executor: Literal["threadpool", "inline"] = "threadpool",
    timeout_s: float = 2.0,
) -> ClientConfig:
    """Build a client configuration.

    Parameters
    ----------
    host
        Hostname or IP address for all sockets.
    subscribe
        Iterable of message types to subscribe to. Defaults to all pub-sub
        messages.
    port_overrides
        Mapping of message or endpoint name to port number. Keys can be any
        pub-sub message name or request-reply endpoint name.
    callback_executor
        Whether to run sync callbacks in a thread pool or inline.
    timeout_s
        Request-reply timeout in seconds.

    Returns
    -------
    ClientConfig
        The constructed configuration.
    """

    pubsub_ports = dict(PUBSUB_DEFAULT_PORTS)
    reqrep_ports = dict(REQREP_DEFAULT_PORTS)

    if port_overrides:
        for key, port in port_overrides.items():
            if key in pubsub_ports:
                pubsub_ports[key] = port
            elif key in reqrep_ports:
                reqrep_ports[key] = port
            else:
                raise ValueError(f"Unknown port override key: {key}")

    subscribe_list = tuple(subscribe) if subscribe is not None else tuple(pubsub_ports)
    for message_type in subscribe_list:
        if message_type not in pubsub_ports:
            raise ValueError(f"Unknown pub-sub message type: {message_type}")

    return ClientConfig(
        host=host,
        subscribe=subscribe_list,
        pubsub_ports=pubsub_ports,
        reqrep_ports=reqrep_ports,
        callback_executor=callback_executor,
        timeout_s=timeout_s,
    )


def resolve_pubsub_port(config: ClientConfig, message_type: PubSubMessage) -> int:
    """Resolve the port for a pub-sub message type."""

    return config.pubsub_ports[message_type]


def resolve_reqrep_port(config: ClientConfig, endpoint: ReqRepEndpoint) -> int:
    """Resolve the port for a request-reply endpoint."""

    return config.reqrep_ports[endpoint]
