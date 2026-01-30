import pytest


def test_request_timeout_export() -> None:
    from farsounder import RequestTimeoutError

    assert issubclass(RequestTimeoutError, TimeoutError)


def test_history_type_export() -> None:
    from farsounder import HistoryData

    assert HistoryData.__name__ == "HistoryData"


def test_nav_api_pb2_export() -> None:
    try:
        from farsounder import nav_api_pb2
    except ModuleNotFoundError:
        pytest.skip("Generated protobuf modules not available.")
    assert hasattr(nav_api_pb2, "GetProcessorSettingsRequest")
