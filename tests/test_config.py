import pytest

from farsounder import config


def test_build_config_defaults() -> None:
    cfg = config.build_config()
    assert cfg.host == "127.0.0.1"
    assert set(cfg.subscribe) == {
        "HydrophoneData",
        "TargetData",
        "RawTargetData",
        "ProcessorSettings",
        "VesselInfo",
    }
    assert cfg.callback_executor == "threadpool"
    assert cfg.pubsub_ports["RawTargetData"] == 61505


def test_build_config_overrides() -> None:
    cfg = config.build_config(
        subscribe=["TargetData"],
        port_overrides={
            "TargetData": 62000,
            "GetVesselInfo": 60001,
            "GetHistoryData": 3001,
        },
    )
    assert cfg.subscribe == ("TargetData",)
    assert cfg.pubsub_ports["TargetData"] == 62000
    assert cfg.reqrep_ports["GetVesselInfo"] == 60001
    assert cfg.rest_ports["GetHistoryData"] == 3001


def test_build_config_unknown_override() -> None:
    with pytest.raises(ValueError, match="Unknown port override key"):
        config.build_config(port_overrides={"UnknownMessage": 12345})
