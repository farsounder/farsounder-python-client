# farsounder-python

Python client SDK for the Farsounder APIs.

## Protobuf stubs

Protobuf sources live in `proto/`. Generate Python stubs with:

```
uv run --group dev gen-protos
```

Or:

```
python tools/gen_protos.py
```

## Usage (async)

```python
import asyncio

from farsounder import build_config, get_processor_settings, subscribe
from farsounder.proto.proto import nav_api_pb2 as nav_api


async def main() -> None:
    config = build_config(
        host="127.0.0.1",
        subscribe=["TargetData"],
    )

    sub = subscribe(config)

    def on_targets(message: nav_api.TargetData) -> None:
        print("Targets:", len(message.groups))

    # Pub/Sub
    sub.on("TargetData", on_targets)
    await sub.start()

    # Req/rep
    settings = await get_processor_settings(config)
    print(settings)

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