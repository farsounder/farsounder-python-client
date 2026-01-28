__all__ = [
    "ClientConfig",
    "PubSubMessage",
    "ReqRepEndpoint",
    "Subscription",
    "build_config",
    "subscribe",
    "get_processor_settings",
    "set_field_of_view",
    "set_bottom_detection",
    "set_inwater_squelch",
    "set_squelchless_inwater_detector",
    "get_vessel_info",
]

_CLIENT_EXPORTS = {
    "ClientConfig",
    "PubSubMessage",
    "RequestTimeoutError",
    "ReqRepEndpoint",
    "Subscription",
    "build_config",
    "subscribe",
    "get_processor_settings",
    "set_field_of_view",
    "set_bottom_detection",
    "set_inwater_squelch",
    "set_squelchless_inwater_detector",
    "get_vessel_info",
}

_PROTO_EXPORTS = {
    "nav_api_pb2",
}


def __getattr__(name: str):
    if name in _CLIENT_EXPORTS:
        from farsounder import client
        return getattr(client, name)
    if name in _PROTO_EXPORTS:
        from importlib import import_module
        return import_module(f"farsounder.proto.proto.{name}")
    raise AttributeError(f"module 'farsounder' has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__ + list(_PROTO_EXPORTS))


def main() -> None:
    print("Hello from farsounder!")
