import argparse
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import zmq

from farsounder.proto.proto import nav_api_pb2 as nav_api
from farsounder.proto.proto import time_pb2


PUB_PORTS = {
    "HydrophoneData": 61501,
    "TargetData": 61502,
    "ProcessorSettings": 61503,
    "VesselInfo": 61504,
}

REP_PORTS = {
    "GetProcessorSettings": 60501,
    "SetFieldOfView": 60502,
    "SetBottomDetection": 60503,
    "SetInWaterSquelch": 60504,
    "SetSquelchlessInWaterDetector": 60505,
    "GetVesselInfo": 60506,
}


@dataclass
class BackendState:
    fov: int = nav_api.k90d500m
    detect_bottom: bool = True
    inwater_squelch: float = 0.5
    squelchless_inwater_detector: bool = True
    draft: float = 2.5
    keel_offset: float = -0.3


def _now_time() -> time_pb2.Time:
    now = datetime.now(timezone.utc)
    return time_pb2.Time(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
        millisecond=now.microsecond // 1000,
    )


def _result_ok() -> nav_api.RequestResult:
    return nav_api.RequestResult(time=_now_time(), code=nav_api.RequestResult.kSuccess)


def _build_hydrophone() -> nav_api.HydrophoneData:
    return nav_api.HydrophoneData(
        time=_now_time(),
        serial="SIM-001",
        transmit_id="sim",
        num_hor_phones=8,
        num_ver_phones=8,
    )


def _build_target_data() -> nav_api.TargetData:
    return nav_api.TargetData(
        time=_now_time(),
        serial="SIM-001",
        max_depth=25.0,
        max_range_index=64,
    )


def _build_processor_settings(state: BackendState) -> nav_api.ProcessorSettings:
    return nav_api.ProcessorSettings(
        time=_now_time(),
        detect_bottom=state.detect_bottom,
        inwater_squelch=state.inwater_squelch,
        squelchless_inwater_detector=state.squelchless_inwater_detector,
        fov=state.fov,
    )


def _build_vessel_info(state: BackendState) -> nav_api.VesselInfo:
    return nav_api.VesselInfo(draft=state.draft, keel_offset=state.keel_offset)


def _publish_loop(
    bind_address: str,
    port: int,
    builder,
    interval_s: float,
    stop_event: threading.Event,
) -> None:
    socket = zmq.Context.instance().socket(zmq.PUB)
    socket.bind(f"tcp://{bind_address}:{port}")
    try:
        while not stop_event.is_set():
            message = builder()
            socket.send(message.SerializeToString())
            time.sleep(interval_s)
    finally:
        socket.close(linger=0)


def _rep_loop(
    bind_address: str,
    port: int,
    handler,
    stop_event: threading.Event,
) -> None:
    socket = zmq.Context.instance().socket(zmq.REP)
    socket.bind(f"tcp://{bind_address}:{port}")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    try:
        while not stop_event.is_set():
            events = dict(poller.poll(timeout=500))
            if socket not in events:
                continue
            data = socket.recv()
            response = handler(data)
            socket.send(response.SerializeToString())
    finally:
        socket.close(linger=0)


def _handle_get_processor_settings(
    state: BackendState, _: bytes
) -> nav_api.GetProcessorSettingsResponse:
    return nav_api.GetProcessorSettingsResponse(
        result=_result_ok(),
        settings=_build_processor_settings(state),
    )


def _handle_set_fov(state: BackendState, data: bytes) -> nav_api.SetFieldOfViewResponse:
    request = nav_api.SetFieldOfViewRequest()
    request.ParseFromString(data)
    if request.HasField("fov"):
        state.fov = request.fov
    return nav_api.SetFieldOfViewResponse(result=_result_ok())


def _handle_set_bottom_detection(
    state: BackendState, data: bytes
) -> nav_api.SetBottomDetectionResponse:
    request = nav_api.SetBottomDetectionRequest()
    request.ParseFromString(data)
    if request.HasField("enable_bottom_detection"):
        state.detect_bottom = request.enable_bottom_detection
    return nav_api.SetBottomDetectionResponse(result=_result_ok())


def _handle_set_inwater_squelch(
    state: BackendState, data: bytes
) -> nav_api.SetInWaterSquelchResponse:
    request = nav_api.SetInWaterSquelchRequest()
    request.ParseFromString(data)
    if request.HasField("new_squelch_val"):
        state.inwater_squelch = request.new_squelch_val
    return nav_api.SetInWaterSquelchResponse(result=_result_ok())


def _handle_set_squelchless_detector(
    state: BackendState, data: bytes
) -> nav_api.SetSquelchlessInWaterDetectorResponse:
    request = nav_api.SetSquelchlessInWaterDetectorRequest()
    request.ParseFromString(data)
    if request.HasField("enable_squelchless_detection"):
        state.squelchless_inwater_detector = request.enable_squelchless_detection
    return nav_api.SetSquelchlessInWaterDetectorResponse(result=_result_ok())


def _handle_get_vessel_info(
    state: BackendState, _: bytes
) -> nav_api.GetVesselInfoResponse:
    return nav_api.GetVesselInfoResponse(
        result=_result_ok(), info=_build_vessel_info(state)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulated nav API backend.")
    parser.add_argument("--bind", default="127.0.0.1", help="Bind address.")
    parser.add_argument("--interval", type=float, default=1.0, help="Publish interval.")
    args = parser.parse_args()

    state = BackendState()
    stop_event = threading.Event()
    threads: list[threading.Thread] = []

    pub_map = {
        "HydrophoneData": _build_hydrophone,
        "TargetData": _build_target_data,
        "ProcessorSettings": lambda: _build_processor_settings(state),
        "VesselInfo": lambda: _build_vessel_info(state),
    }

    rep_map = {
        "GetProcessorSettings": lambda data: _handle_get_processor_settings(
            state, data
        ),
        "SetFieldOfView": lambda data: _handle_set_fov(state, data),
        "SetBottomDetection": lambda data: _handle_set_bottom_detection(state, data),
        "SetInWaterSquelch": lambda data: _handle_set_inwater_squelch(state, data),
        "SetSquelchlessInWaterDetector": lambda data: _handle_set_squelchless_detector(
            state, data
        ),
        "GetVesselInfo": lambda data: _handle_get_vessel_info(state, data),
    }

    for name, port in PUB_PORTS.items():
        thread = threading.Thread(
            target=_publish_loop,
            args=(args.bind, port, pub_map[name], args.interval, stop_event),
            name=f"sim-backend-pub-{name}",
            daemon=True,
        )
        thread.start()
        threads.append(thread)

    for name, port in REP_PORTS.items():
        thread = threading.Thread(
            target=_rep_loop,
            args=(args.bind, port, rep_map[name], stop_event),
            name=f"sim-backend-rep-{name}",
            daemon=True,
        )
        thread.start()
        threads.append(thread)

    print("Simulated backend running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.5)
    finally:
        stop_event.set()
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
