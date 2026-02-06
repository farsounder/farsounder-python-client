import time

from farsounder import config, exceptions, requests, subscriber
from farsounder.proto import nav_api_pb2


def on_targets(message: nav_api_pb2.TargetData) -> None:
    print("Got TargetData message!")
    print("Targets this ping:", len(message.groups))
    print()


def on_processor_settings(message: nav_api_pb2.ProcessorSettings) -> None:
    print("Got ProcessorSettings message!")
    print("Processor settings:", message)
    print()


def main() -> None:
    cfg = config.build_config(
        host="127.0.0.1",
        subscribe=["TargetData", "ProcessorSettings"],
        timeout_seconds=10.0,
    )

    sub = subscriber.subscribe(cfg)
    sub.on("TargetData", on_targets)
    sub.on("ProcessorSettings", on_processor_settings)

    sub.start()
    try:
        settings = requests.get_processor_settings(cfg)
    except exceptions.RequestTimeoutError as exc:
        print("Timeout waiting for processor settings:", exc)

    try:
        history = requests.get_history_data(
            cfg,
            latitude=41.6538,
            longitude=-71.3712,
            radius_meters=500,
        )
        print("Got history data!")
        print("Bottom detections:", len(history.gridded_bottom_detections))
        print("Inwater detections:", len(history.gridded_inwater_detections))
    except exceptions.RequestTimeoutError as exc:
        print("Timeout waiting for history data:", exc)
    except Exception as exc:
        print("Error getting history data!")
        print(exc)

    print(
        "Processor settings:",
        settings.result.code if settings and settings.HasField("result") else None,
    )

    print("Listening for messages. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1.0)
    finally:
        sub.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
