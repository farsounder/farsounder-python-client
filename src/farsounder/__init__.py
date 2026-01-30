__all__ = [
    "ClientConfig",
    "PubSubMessage",
    "ReqRepEndpoint",
    "Subscription",
    "build_config",
    "subscribe",
    "get_processor_settings",
    "get_history_data",
    "set_field_of_view",
    "set_bottom_detection",
    "set_inwater_squelch",
    "set_squelchless_inwater_detector",
    "get_vessel_info",
    "HistoryData",
    "GriddedBottomDetection",
    "GriddedInwaterDetection",
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
    "get_history_data",
    "set_field_of_view",
    "set_bottom_detection",
    "set_inwater_squelch",
    "set_squelchless_inwater_detector",
    "get_vessel_info",
    "HistoryData",
    "GriddedBottomDetection",
    "GriddedInwaterDetection",
}

_PROTO_EXPORTS = {
    "nav_api_pb2",
}


# This lazy import pattern is so that the gen-protos tools works even if
# there are no proto modules generated yet (it otherwise tries to import
# them and they possibly don't exist yet). I decided to check the generated
# stubs into the repo, instead of generating them on the fly, so it shouldn't
# really matter for the exising protos. If we were to add one though, this
# will make sure gen-protos works.
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
