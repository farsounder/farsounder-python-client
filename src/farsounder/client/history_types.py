from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GriddedBottomDetection:
    timestamp_utc: float
    latitude_degrees: float
    longitude_degrees: float
    grid_interval_meters: float
    target_strength_db: float
    is_tide_corrected: bool
    uploaded_to_cloud: bool
    number_of_points: int
    depth_meters: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GriddedBottomDetection":
        return cls(
            timestamp_utc=float(data["timestamp_utc"]),
            latitude_degrees=float(data["latitude_degrees"]),
            longitude_degrees=float(data["longitude_degrees"]),
            grid_interval_meters=float(data["grid_interval_meters"]),
            target_strength_db=float(data["target_strength_db"]),
            is_tide_corrected=bool(data["is_tide_corrected"]),
            uploaded_to_cloud=bool(data["uploaded_to_cloud"]),
            number_of_points=int(data["number_of_points"]),
            depth_meters=float(data["depth_meters"]),
        )


@dataclass(frozen=True)
class GriddedInwaterDetection:
    timestamp_utc: float
    latitude_degrees: float
    longitude_degrees: float
    grid_interval_meters: float
    target_strength_db: float
    is_tide_corrected: bool
    uploaded_to_cloud: bool
    number_of_points: int
    deepest_depth_meters: float | None
    shallowest_depth_meters: float | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GriddedInwaterDetection":
        return cls(
            timestamp_utc=float(data["timestamp_utc"]),
            latitude_degrees=float(data["latitude_degrees"]),
            longitude_degrees=float(data["longitude_degrees"]),
            grid_interval_meters=float(data["grid_interval_meters"]),
            target_strength_db=float(data["target_strength_db"]),
            is_tide_corrected=bool(data["is_tide_corrected"]),
            uploaded_to_cloud=bool(data["uploaded_to_cloud"]),
            number_of_points=int(data["number_of_points"]),
            deepest_depth_meters=(
                float(data["deepest_depth_meters"])
                if data.get("deepest_depth_meters") is not None
                else None
            ),
            shallowest_depth_meters=(
                float(data["shallowest_depth_meters"])
                if data.get("shallowest_depth_meters") is not None
                else None
            ),
        )


@dataclass(frozen=True)
class HistoryData:
    gridded_bottom_detections: list[GriddedBottomDetection]
    gridded_inwater_detections: list[GriddedInwaterDetection]
    history_count: int | None = None

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], *, history_count: int | None = None
    ) -> "HistoryData":
        bottom_raw = data.get("gridded_bottom_detections", [])
        inwater_raw = data.get("gridded_inwater_detections", [])
        return cls(
            gridded_bottom_detections=[
                GriddedBottomDetection.from_dict(item) for item in bottom_raw
            ],
            gridded_inwater_detections=[
                GriddedInwaterDetection.from_dict(item) for item in inwater_raw
            ],
            history_count=history_count,
        )
