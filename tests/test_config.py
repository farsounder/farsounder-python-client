import pytest

from farsounder import build_config


def test_build_config_defaults() -> None:
    config = build_config()
    assert config.host == "127.0.0.1"
    assert set(config.subscribe) == {
        "HydrophoneData",
        "TargetData",
        "ProcessorSettings",
        "VesselInfo",
    }


def test_build_config_overrides() -> None:
    config = build_config(
        subscribe=["TargetData"],
        port_overrides={
            "TargetData": 62000,
            "GetVesselInfo": 60001,
            "GetHistoryData": 3001,
        },
    )
    assert config.subscribe == ("TargetData",)
    assert config.pubsub_ports["TargetData"] == 62000
    assert config.reqrep_ports["GetVesselInfo"] == 60001
    assert config.rest_ports["GetHistoryData"] == 3001


def test_build_config_unknown_override() -> None:
    with pytest.raises(ValueError, match="Unknown port override key"):
        build_config(port_overrides={"UnknownMessage": 12345})
