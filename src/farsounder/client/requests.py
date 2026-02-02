from __future__ import annotations

import asyncio
from typing import TypeVar

import httpx
import zmq
import zmq.asyncio
from google.protobuf.message import Message

from farsounder.proto.proto import nav_api_pb2 as nav_api
from farsounder.client.config import (
    ClientConfig,
    ReqRepEndpoint,
    resolve_reqrep_port,
    resolve_rest_port,
)
from farsounder.client.exceptions import RequestTimeoutError
from farsounder.client.history_types import HistoryData

ResponseT = TypeVar("ResponseT", bound=Message)


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
            data = await asyncio.wait_for(socket.recv(), timeout=config.timeout_seconds)
        except asyncio.TimeoutError as exc:
            raise RequestTimeoutError(
                f"Timeout waiting for {endpoint} after {config.timeout_seconds:.1f}s"
            ) from exc
    finally:
        socket.close(linger=0)

    response = response_cls()
    response.ParseFromString(data)
    return response


async def get_processor_settings(
    config: ClientConfig,
) -> nav_api.GetProcessorSettingsResponse:
    """Request the current processor settings.

    Parameters
    ----------
    config
        Client configuration.

    Returns
    -------
    nav_api.GetProcessorSettingsResponse
        Response containing the current processor settings.
    """

    request = nav_api.GetProcessorSettingsRequest()
    return await _request(
        config,
        "GetProcessorSettings",
        request,
        nav_api.GetProcessorSettingsResponse,
    )


async def set_field_of_view(
    fov: nav_api.FieldOfView,
    config: ClientConfig,
) -> nav_api.SetFieldOfViewResponse:
    """Request a change to the sonar FieldOfView.

    Parameters
    ----------
    fov
        Desired field of view value.
    config
        Client configuration.

    Returns
    -------
    nav_api.SetFieldOfViewResponse
        Response describing the result of the request.
    """

    request = nav_api.SetFieldOfViewRequest(fov=fov)
    return await _request(
        config,
        "SetFieldOfView",
        request,
        nav_api.SetFieldOfViewResponse,
    )


async def set_bottom_detection(
    enable: bool,
    config: ClientConfig,
) -> nav_api.SetBottomDetectionResponse:
    """Enable or disable bottom detection.

    Parameters
    ----------
    enable
        Whether to enable bottom detection.
    config
        Client configuration.

    Returns
    -------
    nav_api.SetBottomDetectionResponse
        Response describing the result of the request.
    """

    request = nav_api.SetBottomDetectionRequest(enable_bottom_detection=enable)
    return await _request(
        config,
        "SetBottomDetection",
        request,
        nav_api.SetBottomDetectionResponse,
    )


async def set_inwater_squelch(
    value: float,
    config: ClientConfig,
) -> nav_api.SetInWaterSquelchResponse:
    """Set the in-water squelch value.

    Parameters
    ----------
    value
        Squelch value to set.
    config
        Client configuration.

    Returns
    -------
    nav_api.SetInWaterSquelchResponse
        Response describing the result of the request.
    """

    request = nav_api.SetInWaterSquelchRequest(new_squelch_val=value)
    return await _request(
        config,
        "SetInWaterSquelch",
        request,
        nav_api.SetInWaterSquelchResponse,
    )


async def set_squelchless_inwater_detector(
    enable: bool,
    config: ClientConfig,
) -> nav_api.SetSquelchlessInWaterDetectorResponse:
    """Enable or disable the squelchless in-water detector.

    Parameters
    ----------
    enable
        Whether to enable squelchless detection.
    config
        Client configuration.

    Returns
    -------
    nav_api.SetSquelchlessInWaterDetectorResponse
        Response describing the result of the request.
    """

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
    config: ClientConfig,
) -> nav_api.GetVesselInfoResponse:
    """Request the current vessel info.

    Parameters
    ----------
    config
        Client configuration.

    Returns
    -------
    nav_api.GetVesselInfoResponse
        Response containing the vessel info.
    """

    request = nav_api.GetVesselInfoRequest()
    return await _request(
        config, "GetVesselInfo", request, nav_api.GetVesselInfoResponse
    )


def _build_history_params(
    *,
    latitude: float,
    longitude: float,
    radius_meters: float,
    since_timestamp_utc: float | None,
    tide_corrected_only: bool,
    skip: int,
    limit: int,
    include_count: bool,
) -> dict[str, str]:
    params: dict[str, str] = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "radius_meters": str(radius_meters),
        "tide_corrected_only": str(tide_corrected_only).lower(),
        "skip": str(skip),
        "limit": str(limit),
        "include_count": str(include_count).lower(),
    }
    if since_timestamp_utc is not None:
        params["since_timestamp_utc"] = str(since_timestamp_utc)
    return params


async def get_history_data(
    config: ClientConfig,
    *,
    latitude: float,
    longitude: float,
    radius_meters: float = 500,
    since_timestamp_utc: float | None = None,
    tide_corrected_only: bool = False,
    skip: int = 0,
    limit: int = 50000,
    include_count: bool = True,
) -> HistoryData:
    """Request history data from the REST API.

    Parameters
    ----------
    config
        Client configuration.
    latitude
        Latitude in decimal degrees.
    longitude
        Longitude in decimal degrees.
    radius_meters
        Query radius in meters.
    since_timestamp_utc
        Return data collected or updated since this UTC epoch time.
    tide_corrected_only
        Only return tide corrected seafloor detections.
    skip
        Number of records to skip.
    limit
        Maximum number of records to return.
    include_count
        Include the total count in the response header.

    Returns
    -------
    HistoryData
        Parsed history data response.
    """

    port = resolve_rest_port(config, "GetHistoryData")
    params = _build_history_params(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
        since_timestamp_utc=since_timestamp_utc,
        tide_corrected_only=tide_corrected_only,
        skip=skip,
        limit=limit,
        include_count=include_count,
    )
    url = f"http://{config.host}:{port}/api/history_data"
    try:
        async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
            response = await client.get(url, params=params)
        response.raise_for_status()
    except httpx.ConnectError as exc:
        raise httpx.ConnectError(
            f"Failed to connect to {url}, is the server running?"
        ) from exc

    history_count = None
    if include_count:
        header_val = response.headers.get("X-Grids-Count")
        if header_val is not None:
            try:
                history_count = int(header_val)
            except ValueError:
                history_count = None
    payload = response.json()
    return HistoryData.from_dict(payload, history_count=history_count)
