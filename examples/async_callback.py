import asyncio
import sys

from farsounder import config, exceptions, requests, subscriber
from farsounder.proto import nav_api_pb2


async def on_targets(message: nav_api_pb2.TargetData) -> None:
    print("Got TargetData message!")
    print("Targets this ping:", len(message.groups))
    print()


async def on_processor_settings(message: nav_api_pb2.ProcessorSettings) -> None:
    print("Got ProcessorSettings message!")
    print("Processor settings:", message)
    print()


async def main() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    cfg = config.build_config(
        host="127.0.0.1",
        subscribe=["TargetData", "ProcessorSettings"],
        timeout_seconds=10.0,
    )

    sub = subscriber.subscribe(cfg)
    sub.on("TargetData", on_targets)
    sub.on("ProcessorSettings", on_processor_settings)

    await sub.start()
    try:
        settings = await requests.get_processor_settings(cfg)
    except exceptions.RequestTimeoutError as exc:
        print("Timeout waiting for processor settings:", exc)
        return

    try:
        vessel = await requests.get_vessel_info(cfg)
    except exceptions.RequestTimeoutError as exc:
        print("Timeout waiting for vessel info:", exc)
        return

    try:
        history = await requests.get_history_data(
            cfg,
            latitude=41.6538,
            longitude=-71.3712,
            radius_meters=500,
        )
        print("Got history data!")
        print("Bottom detections:", len(history.gridded_bottom_detections))
        print("Inwater detections:", len(history.gridded_inwater_detections))
    except Exception as exc:
        print("Error getting history data!")
        print(exc)

    print(
        "Processor settings:",
        settings.result.code if settings.HasField("result") else None,
    )
    print("Vessel info:", vessel.info if vessel.HasField("info") else None)

    print("Listening for messages. Press Ctrl+C to stop.")
    try:
        while True:
            await asyncio.sleep(1.0)
    finally:
        await sub.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
