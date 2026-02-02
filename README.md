# SDK Client for live FarSounder data

Python client to communicate with SonaSoft via API.

## Usage

Clone locally and install (uv add .) or install from pypi like:

```
uv add farsounder
```
(or use pip, etc)

Then - for example to subscribe to `TargetData` messages:

```python
import asyncio

from farsounder import config, requests, subscriber
from farsounder.proto import nav_api_pb2


async def main() -> None:
    cfg = config.build_config(
        host="127.0.0.1",
        subscribe=["TargetData"],
    )

    sub = subscriber.subscribe(config)

    def on_targets(message: nav_api_pb2.TargetData) -> None:
        print("Got a TargetData!")
        print("Targets:", len(message.groups))

    # Pub/Sub
    sub.on("TargetData", on_targets)
    await sub.start()

    # Req/rep
    settings = await requests.get_processor_settings(config)
    print(settings)

    # History data
    history = await requests.get_history_data(
        config,
        latitude=41.7223,
        longitude=-71.35,
        radius_meters=500,
    )
    print(history.gridded_bottom_detections)

    await asyncio.sleep(1.0)
    await sub.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

## Simulated backend

You can run a local simulated backend that publishes dummy messages and responds
to request/reply calls:

```
uv run examples/simulated_backend.py
```

Note: the `examples/` directory is not installed with `uv add farsounder`.
Clone the repo to run the examples locally.

# Development

## Re-generate Protobuf stubs

Protobuf sources live in `proto/`. Generate Python stubs with:

```
uv run --group dev gen-protos
```

Or:

```
uv run tools/gen_protos.py
```

## Tests

Run tests with:

```
uv run --group dev pytest
```
