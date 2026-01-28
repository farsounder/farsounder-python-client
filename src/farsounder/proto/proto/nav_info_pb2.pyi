from proto import nmea_pb2 as _nmea_pb2
from proto import time_pb2 as _time_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Depth(_message.Message):
    __slots__ = ("depth", "nmea")
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    depth: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        depth: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class Heading(_message.Message):
    __slots__ = ("heading", "type", "nmea")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OBSOLETE_kSensor: _ClassVar[Heading.Type]
        OBSOLETE_kMagnetic: _ClassVar[Heading.Type]
        kTrue: _ClassVar[Heading.Type]
        kManufactured: _ClassVar[Heading.Type]

    OBSOLETE_kSensor: Heading.Type
    OBSOLETE_kMagnetic: Heading.Type
    kTrue: Heading.Type
    kManufactured: Heading.Type
    HEADING_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    heading: float
    type: Heading.Type
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        heading: _Optional[float] = ...,
        type: _Optional[_Union[Heading.Type, str]] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class Position(_message.Message):
    __slots__ = ("lat", "lon", "nmea")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        lat: _Optional[float] = ...,
        lon: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class Speed(_message.Message):
    __slots__ = ("speed", "nmea")
    SPEED_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    speed: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        speed: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class DualSpeed(_message.Message):
    __slots__ = ("ground_transversal", "ground_longitudinal", "nmea")
    GROUND_TRANSVERSAL_FIELD_NUMBER: _ClassVar[int]
    GROUND_LONGITUDINAL_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    ground_transversal: float
    ground_longitudinal: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        ground_transversal: _Optional[float] = ...,
        ground_longitudinal: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class RateOfTurn(_message.Message):
    __slots__ = ("rot", "nmea")
    ROT_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    rot: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        rot: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class CourseOverGround(_message.Message):
    __slots__ = ("true_heading", "nmea")
    TRUE_HEADING_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    true_heading: float
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self,
        true_heading: _Optional[float] = ...,
        nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...,
    ) -> None: ...

class AIS(_message.Message):
    __slots__ = ("nmea",)
    NMEA_FIELD_NUMBER: _ClassVar[int]
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self, nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...
    ) -> None: ...

class ARPA(_message.Message):
    __slots__ = ("nmea",)
    NMEA_FIELD_NUMBER: _ClassVar[int]
    nmea: _nmea_pb2.NmeaData
    def __init__(
        self, nmea: _Optional[_Union[_nmea_pb2.NmeaData, _Mapping]] = ...
    ) -> None: ...

class UTCTime(_message.Message):
    __slots__ = ("time",)
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    def __init__(
        self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...
    ) -> None: ...

class LocalTime(_message.Message):
    __slots__ = ("time",)
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    def __init__(
        self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...
    ) -> None: ...

class FilteredState(_message.Message):
    __slots__ = (
        "time",
        "filter_enabled",
        "lat",
        "lon",
        "latlon_is_filtered",
        "heading",
        "heading_is_filtered",
        "speed",
        "course",
        "rot",
    )
    TIME_FIELD_NUMBER: _ClassVar[int]
    FILTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LATLON_IS_FILTERED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    HEADING_IS_FILTERED_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    ROT_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    filter_enabled: bool
    lat: float
    lon: float
    latlon_is_filtered: bool
    heading: float
    heading_is_filtered: bool
    speed: float
    course: float
    rot: float
    def __init__(
        self,
        time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...,
        filter_enabled: bool = ...,
        lat: _Optional[float] = ...,
        lon: _Optional[float] = ...,
        latlon_is_filtered: bool = ...,
        heading: _Optional[float] = ...,
        heading_is_filtered: bool = ...,
        speed: _Optional[float] = ...,
        course: _Optional[float] = ...,
        rot: _Optional[float] = ...,
    ) -> None: ...
