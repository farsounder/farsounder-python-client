from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping

PubSubMessage = Literal[
    "HydrophoneData",
    "TargetData",
    "RawTargetData",
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

RestEndpoint = Literal["GetHistoryData",]

PUBSUB_DEFAULT_PORTS: dict[PubSubMessage, int] = {
    "HydrophoneData": 61501,
    "TargetData": 61502,
    "RawTargetData": 61505,
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

REST_DEFAULT_PORTS: dict[RestEndpoint, int] = {
    "GetHistoryData": 3000,
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
    rest_ports
        Port mapping for REST endpoints.
    callback_executor
        Whether to run sync callbacks in a thread pool or inline.
    timeout_seconds
        Request-reply timeout in seconds.
    """

    host: str
    subscribe: tuple[PubSubMessage, ...]
    pubsub_ports: dict[PubSubMessage, int]
    reqrep_ports: dict[ReqRepEndpoint, int]
    rest_ports: dict[RestEndpoint, int]
    callback_executor: Literal["threadpool", "inline"]
    timeout_seconds: float


def build_config(
    host: str = "127.0.0.1",
    subscribe: Iterable[PubSubMessage] | None = None,
    port_overrides: Mapping[str, int] | None = None,
    callback_executor: Literal["threadpool", "inline"] = "threadpool",
    timeout_seconds: float = 2.0,
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
        pub-sub message name, request-reply endpoint name, or REST endpoint
        name such as GetHistoryData.
    callback_executor
        Whether to run sync callbacks in a thread pool or inline.
    timeout_seconds
        Request-reply timeout in seconds.

    Returns
    -------
    ClientConfig
        The constructed configuration.
    """

    pubsub_ports = dict(PUBSUB_DEFAULT_PORTS)
    reqrep_ports = dict(REQREP_DEFAULT_PORTS)
    rest_ports = dict(REST_DEFAULT_PORTS)

    if port_overrides:
        for key, port in port_overrides.items():
            if key in pubsub_ports:
                pubsub_ports[key] = port
            elif key in reqrep_ports:
                reqrep_ports[key] = port
            elif key in rest_ports:
                rest_ports[key] = port
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
        rest_ports=rest_ports,
        callback_executor=callback_executor,
        timeout_seconds=timeout_seconds,
    )


def resolve_pubsub_port(config: ClientConfig, message_type: PubSubMessage) -> int:
    """Resolve the port for a pub-sub message type."""

    return config.pubsub_ports[message_type]


def resolve_reqrep_port(config: ClientConfig, endpoint: ReqRepEndpoint) -> int:
    """Resolve the port for a request-reply endpoint."""

    return config.reqrep_ports[endpoint]


def resolve_rest_port(config: ClientConfig, endpoint: RestEndpoint) -> int:
    """Resolve the port for a REST endpoint."""

    return config.rest_ports[endpoint]
