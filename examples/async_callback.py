import asyncio
import sys

from farsounder import (
    build_config,
    get_processor_settings,
    get_vessel_info,
    nav_api_pb2,
    subscribe,
    RequestTimeoutError,
)


async def on_targets(message: nav_api_pb2.TargetData) -> None:
    print("Got TargetData message!")
    print("Targets ping:", len(message.groups))
    print()


async def on_processor_settings(message: nav_api_pb2.ProcessorSettings) -> None:
    print("Got ProcessorSettings message!")
    print("Processor settings:", message)
    print()


async def main() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    config = build_config(
        host="127.0.0.1",
        subscribe=["TargetData", "ProcessorSettings"],
        timeout_seconds=10.0,
    )

    sub = subscribe(config)
    sub.on("TargetData", on_targets)
    sub.on("ProcessorSettings", on_processor_settings)

    await sub.start()
    try:
        settings = await get_processor_settings(config)
    except RequestTimeoutError as exc:
        print("Timeout waiting for processor settings:", exc)
        return

    try:
        vessel = await get_vessel_info(config)
    except RequestTimeoutError as exc:
        print("Timeout waiting for vessel info:", exc)
        return

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
