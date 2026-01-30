from farsounder.client.history_types import HistoryData
from farsounder.client.requests import _build_history_params


def test_build_history_params() -> None:
    params = _build_history_params(
        latitude=41.7,
        longitude=-71.3,
        radius_meters=500,
        since_timestamp_utc=None,
        tide_corrected_only=False,
        skip=0,
        limit=100,
        include_count=True,
    )
    assert params["latitude"] == "41.7"
    assert params["longitude"] == "-71.3"
    assert params["radius_meters"] == "500"
    assert params["tide_corrected_only"] == "false"
    assert params["skip"] == "0"
    assert params["limit"] == "100"
    assert params["include_count"] == "true"
    assert "since_timestamp_utc" not in params


def test_history_data_parsing() -> None:
    payload = {
        "gridded_bottom_detections": [
            {
                "timestamp_utc": 1.0,
                "latitude_degrees": 41.0,
                "longitude_degrees": -71.0,
                "grid_interval_meters": 1.0,
                "target_strength_db": 10.0,
                "is_tide_corrected": True,
                "uploaded_to_cloud": False,
                "number_of_points": 2,
                "depth_meters": 12.5,
            }
        ],
        "gridded_inwater_detections": [
            {
                "timestamp_utc": 2.0,
                "latitude_degrees": 41.1,
                "longitude_degrees": -71.1,
                "grid_interval_meters": 1.0,
                "target_strength_db": 11.0,
                "is_tide_corrected": False,
                "uploaded_to_cloud": True,
                "number_of_points": 3,
                "deepest_depth_meters": 25.0,
                "shallowest_depth_meters": 5.0,
            }
        ],
    }
    history = HistoryData.from_dict(payload, history_count=5)
    assert history.history_count == 5
    assert len(history.gridded_bottom_detections) == 1
    assert len(history.gridded_inwater_detections) == 1
