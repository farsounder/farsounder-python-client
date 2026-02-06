# Python API Client for Argos data

Python client to communicate with SonaSoft via API.

>[!NOTE]
> This is still under active development and testing. But may serve as an example for
> integration, beyond the lower level example in [sdk repo](https://github.com/farsounder/SDK-Integration-Examples).
> For now the docs are the interfaces and the examples in examples/

## Usage

Clone locally and install (uv add .) or install from pypi like:

```
uv add farsounder
```
(or use pip, etc)

Then - for example to subscribe to `TargetData` messages:

```python
import time

from farsounder import config, requests, subscriber
from farsounder.proto import nav_api_pb2


def main() -> None:

    # Build the configuration:
    # - where is the api running?
    # - what messages do you care about subscribing to?
    # - if ports are changed, they can overridden here
    cfg = config.build_config(
        host="127.0.0.1",
        subscribe=["TargetData"],
    )


    # Pub/Sub
    sub = subscriber.subscribe(cfg)
    # A callback to run when there are new target data messages
    # - don't do a lot of processing in here it will block (thank GIL - for now...)
    # - use sync mechanism if you're accessing shared data (callbacks
    #   run on thread pool [default] or on the receive thread for the message
    #   type)
    def on_targets(message: nav_api_pb2.TargetData) -> None:
        print("Got a TargetData!")
        print("Targets:", len(message.groups))

    # register the callback(s)
    sub.on("TargetData", on_targets)

    # start the receive loop
    sub.start()

    # Req/rep
    # for each of the request / reply endpoints - there are specific
    # get/set functions
    settings = requests.get_processor_settings(cfg)
    print(settings)

    history = requests.get_history_data(
        cfg,
        latitude=41.7223,
        longitude=-71.35,
        radius_meters=500,
    )
    print(history.gridded_bottom_detections)

    time.sleep(1.0)

    # Stop receive loop
    sub.stop()


if __name__ == "__main__":
    main()
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
