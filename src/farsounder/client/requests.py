from __future__ import annotations

import asyncio
from typing import Mapping, TypeVar

import zmq
import zmq.asyncio
from google.protobuf.message import Message

from farsounder.proto.proto import nav_api_pb2 as nav_api
from farsounder.client.config import (
    ClientConfig,
    ReqRepEndpoint,
    build_config,
    resolve_reqrep_port,
)

ResponseT = TypeVar("ResponseT", bound=Message)


class RequestTimeoutError(TimeoutError):
    """Request-reply operation timed out."""


def _ensure_config(
    config: ClientConfig | None,
    *,
    host: str,
    port_overrides: Mapping[str, int] | None,
    timeout_s: float,
) -> ClientConfig:
    if config is not None:
        return config
    return build_config(
        host=host,
        subscribe=(),
        port_overrides=port_overrides,
        timeout_s=timeout_s,
    )


async def _request(
    config: ClientConfig,
    endpoint: ReqRepEndpoint,
    request: Message,
    response_cls: type[ResponseT],
) -> ResponseT:
    ctx = zmq.asyncio.Context.instance()
    socket = ctx.socket(zmq.REQ)
    try:
        port = resolve_reqrep_port(config, endpoint)
        socket.connect(f"tcp://{config.host}:{port}")
        await socket.send(request.SerializeToString())
        try:
            data = await asyncio.wait_for(socket.recv(), timeout=config.timeout_s)
        except asyncio.TimeoutError as exc:
            raise RequestTimeoutError(
                f"Timeout waiting for {endpoint} after {config.timeout_s:.1f}s"
            ) from exc
    finally:
        socket.close(linger=0)

    response = response_cls()
    response.ParseFromString(data)
    return response


async def get_processor_settings(
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.GetProcessorSettingsResponse:
    """Request the current processor settings.

    Parameters
    ----------
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.GetProcessorSettingsResponse
        Response containing the current processor settings.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.GetProcessorSettingsRequest()
    return await _request(
        config,
        "GetProcessorSettings",
        request,
        nav_api.GetProcessorSettingsResponse,
    )


async def set_field_of_view(
    fov: nav_api.FieldOfView,
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.SetFieldOfViewResponse:
    """Request a change to the sonar FieldOfView.

    Parameters
    ----------
    fov
        Desired field of view value.
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.SetFieldOfViewResponse
        Response describing the result of the request.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.SetFieldOfViewRequest(fov=fov)
    return await _request(
        config,
        "SetFieldOfView",
        request,
        nav_api.SetFieldOfViewResponse,
    )


async def set_bottom_detection(
    enable: bool,
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.SetBottomDetectionResponse:
    """Enable or disable bottom detection.

    Parameters
    ----------
    enable
        Whether to enable bottom detection.
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.SetBottomDetectionResponse
        Response describing the result of the request.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.SetBottomDetectionRequest(enable_bottom_detection=enable)
    return await _request(
        config,
        "SetBottomDetection",
        request,
        nav_api.SetBottomDetectionResponse,
    )


async def set_inwater_squelch(
    value: float,
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.SetInWaterSquelchResponse:
    """Set the in-water squelch value.

    Parameters
    ----------
    value
        Squelch value to set.
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.SetInWaterSquelchResponse
        Response describing the result of the request.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.SetInWaterSquelchRequest(new_squelch_val=value)
    return await _request(
        config,
        "SetInWaterSquelch",
        request,
        nav_api.SetInWaterSquelchResponse,
    )


async def set_squelchless_inwater_detector(
    enable: bool,
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.SetSquelchlessInWaterDetectorResponse:
    """Enable or disable the squelchless in-water detector.

    Parameters
    ----------
    enable
        Whether to enable squelchless detection.
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.SetSquelchlessInWaterDetectorResponse
        Response describing the result of the request.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.SetSquelchlessInWaterDetectorRequest(
        enable_squelchless_detection=enable
    )
    return await _request(
        config,
        "SetSquelchlessInWaterDetector",
        request,
        nav_api.SetSquelchlessInWaterDetectorResponse,
    )


async def get_vessel_info(
    config: ClientConfig | None = None,
    *,
    host: str = "127.0.0.1",
    port_overrides: Mapping[str, int] | None = None,
    timeout_s: float = 2.0,
) -> nav_api.GetVesselInfoResponse:
    """Request the current vessel info.

    Parameters
    ----------
    config
        Optional pre-built configuration.
    host
        Hostname or IP address for the request socket.
    port_overrides
        Mapping of endpoint name to port number.
    timeout_s
        Timeout for the request-reply exchange, in seconds.

    Returns
    -------
    nav_api.GetVesselInfoResponse
        Response containing the vessel info.
    """

    config = _ensure_config(
        config, host=host, port_overrides=port_overrides, timeout_s=timeout_s
    )
    request = nav_api.GetVesselInfoRequest()
    return await _request(
        config, "GetVesselInfo", request, nav_api.GetVesselInfoResponse
    )
