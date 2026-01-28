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