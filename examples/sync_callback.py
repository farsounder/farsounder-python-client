import asyncio
import sys
import threading
import time

from farsounder import (
    build_config,
    get_processor_settings,
    nav_api_pb2,
    subscribe,
    RequestTimeoutError,
)


def on_hydrophone(message: nav_api_pb2.HydrophoneData) -> None:
    print("Hydrophone serial:", message.serial)
    print()


def on_processor_settings(message: nav_api_pb2.ProcessorSettings) -> None:
    print("Processor settings:", message)
    print()


def on_targets(message: nav_api_pb2.TargetData) -> None:
    print("Targets ping:", len(message.groups))
    print()


async def _run_async(stop_event: threading.Event) -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    config = build_config(
        host="127.0.0.1",
        subscribe=["HydrophoneData", "ProcessorSettings", "TargetData"],
        timeout_seconds=10.0,
    )

    sub = subscribe(config)
    sub.on("HydrophoneData", on_hydrophone)
    sub.on("ProcessorSettings", on_processor_settings)
    sub.on("TargetData", on_targets)
    await sub.start()

    try:
        settings = await get_processor_settings(config)
    except RequestTimeoutError as exc:
        print("Timeout waiting for processor settings:", exc)
        stop_event.set()
        return

    print(
        "Processor settings:",
        settings.result.code if settings.HasField("result") else None,
    )
    print("Listening for messages. Press Ctrl+C to stop.")
    try:
        while not stop_event.is_set():
            await asyncio.sleep(0.5)
    finally:
        await sub.stop()


def main() -> None:
    stop_event = threading.Event()

    thread = threading.Thread(
        target=lambda: asyncio.run(_run_async(stop_event)),
        name="farsounder-subscription",
        daemon=True,
    )
    thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_event.set()
        thread.join(timeout=2.0)


if __name__ == "__main__":
    main()
