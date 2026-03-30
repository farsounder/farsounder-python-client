from proto import array_pb2 as _array_pb2
from proto import grid_description_pb2 as _grid_description_pb2
from proto import nav_info_pb2 as _nav_info_pb2
from proto import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldOfView(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k120d100m: _ClassVar[FieldOfView]
    k120d200m: _ClassVar[FieldOfView]
    k90d500m: _ClassVar[FieldOfView]
    k60d1000m: _ClassVar[FieldOfView]
    k90d100m: _ClassVar[FieldOfView]
    k90d200m: _ClassVar[FieldOfView]
    k90d350m: _ClassVar[FieldOfView]
    kStandby: _ClassVar[FieldOfView]
    OBSELETE_k90d110m: _ClassVar[FieldOfView]
    OBSELETE_k90d220m: _ClassVar[FieldOfView]
    OBSELETE_k90d330m: _ClassVar[FieldOfView]
    OBSELETE_k60d440m: _ClassVar[FieldOfView]
    OBSELETE_kAlt: _ClassVar[FieldOfView]
k120d100m: FieldOfView
k120d200m: FieldOfView
k90d500m: FieldOfView
k60d1000m: FieldOfView
k90d100m: FieldOfView
k90d200m: FieldOfView
k90d350m: FieldOfView
kStandby: FieldOfView
OBSELETE_k90d110m: FieldOfView
OBSELETE_k90d220m: FieldOfView
OBSELETE_k90d330m: FieldOfView
OBSELETE_k60d440m: FieldOfView
OBSELETE_kAlt: FieldOfView

class RequestResult(_message.Message):
    __slots__ = ("time", "code", "result_detail")
    class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        kSuccess: _ClassVar[RequestResult.ResultCode]
        kUnknownError: _ClassVar[RequestResult.ResultCode]
        kOperationUnavailable: _ClassVar[RequestResult.ResultCode]
        kParameterOutOfRange: _ClassVar[RequestResult.ResultCode]
        kParameterMissing: _ClassVar[RequestResult.ResultCode]
        kInvalidRequest: _ClassVar[RequestResult.ResultCode]
    kSuccess: RequestResult.ResultCode
    kUnknownError: RequestResult.ResultCode
    kOperationUnavailable: RequestResult.ResultCode
    kParameterOutOfRange: RequestResult.ResultCode
    kParameterMissing: RequestResult.ResultCode
    kInvalidRequest: RequestResult.ResultCode
    TIME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    RESULT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    code: RequestResult.ResultCode
    result_detail: str
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., code: _Optional[_Union[RequestResult.ResultCode, str]] = ..., result_detail: _Optional[str] = ...) -> None: ...

class HydrophoneData(_message.Message):
    __slots__ = ("time", "raw_timeseries", "num_hor_phones", "num_ver_phones", "serial", "transmit_id")
    TIME_FIELD_NUMBER: _ClassVar[int]
    RAW_TIMESERIES_FIELD_NUMBER: _ClassVar[int]
    NUM_HOR_PHONES_FIELD_NUMBER: _ClassVar[int]
    NUM_VER_PHONES_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    TRANSMIT_ID_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    raw_timeseries: _array_pb2.ArrayData
    num_hor_phones: int
    num_ver_phones: int
    serial: str
    transmit_id: str
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., raw_timeseries: _Optional[_Union[_array_pb2.ArrayData, _Mapping]] = ..., num_hor_phones: _Optional[int] = ..., num_ver_phones: _Optional[int] = ..., serial: _Optional[str] = ..., transmit_id: _Optional[str] = ...) -> None: ...

class TargetData(_message.Message):
    __slots__ = ("time", "serial", "heading", "position", "bottom", "groups", "grid_description", "max_depth", "max_range_index")
    TIME_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    GRID_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MAX_RANGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    serial: str
    heading: _nav_info_pb2.Heading
    position: _nav_info_pb2.Position
    bottom: _containers.RepeatedCompositeFieldContainer[Bin]
    groups: _containers.RepeatedCompositeFieldContainer[Group]
    grid_description: _grid_description_pb2.GridDescription
    max_depth: float
    max_range_index: int
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., serial: _Optional[str] = ..., heading: _Optional[_Union[_nav_info_pb2.Heading, _Mapping]] = ..., position: _Optional[_Union[_nav_info_pb2.Position, _Mapping]] = ..., bottom: _Optional[_Iterable[_Union[Bin, _Mapping]]] = ..., groups: _Optional[_Iterable[_Union[Group, _Mapping]]] = ..., grid_description: _Optional[_Union[_grid_description_pb2.GridDescription, _Mapping]] = ..., max_depth: _Optional[float] = ..., max_range_index: _Optional[int] = ...) -> None: ...

class RawTargetData(_message.Message):
    __slots__ = ("time", "serial", "heading", "position", "bottom", "target", "grid_description", "max_depth", "max_range_index", "kernel_roll", "rolls", "tilts", "bin_length", "range_to_first_bin")
    TIME_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    GRID_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    MAX_RANGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    KERNEL_ROLL_FIELD_NUMBER: _ClassVar[int]
    ROLLS_FIELD_NUMBER: _ClassVar[int]
    TILTS_FIELD_NUMBER: _ClassVar[int]
    BIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    RANGE_TO_FIRST_BIN_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    serial: str
    heading: _nav_info_pb2.Heading
    position: _nav_info_pb2.Position
    bottom: _containers.RepeatedCompositeFieldContainer[Bin]
    target: _containers.RepeatedCompositeFieldContainer[Bin]
    grid_description: _grid_description_pb2.GridDescription
    max_depth: float
    max_range_index: int
    kernel_roll: float
    rolls: _containers.RepeatedScalarFieldContainer[float]
    tilts: _containers.RepeatedScalarFieldContainer[float]
    bin_length: float
    range_to_first_bin: float
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., serial: _Optional[str] = ..., heading: _Optional[_Union[_nav_info_pb2.Heading, _Mapping]] = ..., position: _Optional[_Union[_nav_info_pb2.Position, _Mapping]] = ..., bottom: _Optional[_Iterable[_Union[Bin, _Mapping]]] = ..., target: _Optional[_Iterable[_Union[Bin, _Mapping]]] = ..., grid_description: _Optional[_Union[_grid_description_pb2.GridDescription, _Mapping]] = ..., max_depth: _Optional[float] = ..., max_range_index: _Optional[int] = ..., kernel_roll: _Optional[float] = ..., rolls: _Optional[_Iterable[float]] = ..., tilts: _Optional[_Iterable[float]] = ..., bin_length: _Optional[float] = ..., range_to_first_bin: _Optional[float] = ...) -> None: ...

class Bin(_message.Message):
    __slots__ = ("hor_index", "ver_index", "range_index", "cross_range", "down_range", "depth", "strength", "confidence")
    HOR_INDEX_FIELD_NUMBER: _ClassVar[int]
    VER_INDEX_FIELD_NUMBER: _ClassVar[int]
    RANGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CROSS_RANGE_FIELD_NUMBER: _ClassVar[int]
    DOWN_RANGE_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    STRENGTH_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    hor_index: int
    ver_index: int
    range_index: int
    cross_range: float
    down_range: float
    depth: float
    strength: float
    confidence: float
    def __init__(self, hor_index: _Optional[int] = ..., ver_index: _Optional[int] = ..., range_index: _Optional[int] = ..., cross_range: _Optional[float] = ..., down_range: _Optional[float] = ..., depth: _Optional[float] = ..., strength: _Optional[float] = ..., confidence: _Optional[float] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("bins",)
    BINS_FIELD_NUMBER: _ClassVar[int]
    bins: _containers.RepeatedCompositeFieldContainer[Bin]
    def __init__(self, bins: _Optional[_Iterable[_Union[Bin, _Mapping]]] = ...) -> None: ...

class ProcessorSettings(_message.Message):
    __slots__ = ("time", "min_inwater_squelch", "max_inwater_squelch", "inwater_squelch", "squelchless_inwater_detector", "detect_bottom", "system_type", "fov")
    class SystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        kFS500: _ClassVar[ProcessorSettings.SystemType]
        kFS1000: _ClassVar[ProcessorSettings.SystemType]
        kFS350: _ClassVar[ProcessorSettings.SystemType]
        OBSELETE_kFS3DT: _ClassVar[ProcessorSettings.SystemType]
    kFS500: ProcessorSettings.SystemType
    kFS1000: ProcessorSettings.SystemType
    kFS350: ProcessorSettings.SystemType
    OBSELETE_kFS3DT: ProcessorSettings.SystemType
    TIME_FIELD_NUMBER: _ClassVar[int]
    MIN_INWATER_SQUELCH_FIELD_NUMBER: _ClassVar[int]
    MAX_INWATER_SQUELCH_FIELD_NUMBER: _ClassVar[int]
    INWATER_SQUELCH_FIELD_NUMBER: _ClassVar[int]
    SQUELCHLESS_INWATER_DETECTOR_FIELD_NUMBER: _ClassVar[int]
    DETECT_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    FOV_FIELD_NUMBER: _ClassVar[int]
    time: _time_pb2.Time
    min_inwater_squelch: float
    max_inwater_squelch: float
    inwater_squelch: float
    squelchless_inwater_detector: bool
    detect_bottom: bool
    system_type: ProcessorSettings.SystemType
    fov: FieldOfView
    def __init__(self, time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., min_inwater_squelch: _Optional[float] = ..., max_inwater_squelch: _Optional[float] = ..., inwater_squelch: _Optional[float] = ..., squelchless_inwater_detector: bool = ..., detect_bottom: bool = ..., system_type: _Optional[_Union[ProcessorSettings.SystemType, str]] = ..., fov: _Optional[_Union[FieldOfView, str]] = ...) -> None: ...

class GetProcessorSettingsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProcessorSettingsResponse(_message.Message):
    __slots__ = ("result", "settings")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    settings: ProcessorSettings
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ..., settings: _Optional[_Union[ProcessorSettings, _Mapping]] = ...) -> None: ...

class SetFieldOfViewRequest(_message.Message):
    __slots__ = ("fov",)
    FOV_FIELD_NUMBER: _ClassVar[int]
    fov: FieldOfView
    def __init__(self, fov: _Optional[_Union[FieldOfView, str]] = ...) -> None: ...

class SetFieldOfViewResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...

class SetBottomDetectionRequest(_message.Message):
    __slots__ = ("enable_bottom_detection",)
    ENABLE_BOTTOM_DETECTION_FIELD_NUMBER: _ClassVar[int]
    enable_bottom_detection: bool
    def __init__(self, enable_bottom_detection: bool = ...) -> None: ...

class SetBottomDetectionResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...

class SetInWaterSquelchRequest(_message.Message):
    __slots__ = ("new_squelch_val",)
    NEW_SQUELCH_VAL_FIELD_NUMBER: _ClassVar[int]
    new_squelch_val: float
    def __init__(self, new_squelch_val: _Optional[float] = ...) -> None: ...

class SetInWaterSquelchResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...

class SetSquelchlessInWaterDetectorRequest(_message.Message):
    __slots__ = ("enable_squelchless_detection",)
    ENABLE_SQUELCHLESS_DETECTION_FIELD_NUMBER: _ClassVar[int]
    enable_squelchless_detection: bool
    def __init__(self, enable_squelchless_detection: bool = ...) -> None: ...

class SetSquelchlessInWaterDetectorResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...

class VesselInfo(_message.Message):
    __slots__ = ("draft", "keel_offset")
    DRAFT_FIELD_NUMBER: _ClassVar[int]
    KEEL_OFFSET_FIELD_NUMBER: _ClassVar[int]
    draft: float
    keel_offset: float
    def __init__(self, draft: _Optional[float] = ..., keel_offset: _Optional[float] = ...) -> None: ...

class GetVesselInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVesselInfoResponse(_message.Message):
    __slots__ = ("result", "info")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    info: VesselInfo
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ..., info: _Optional[_Union[VesselInfo, _Mapping]] = ...) -> None: ...

class SetDraftRequest(_message.Message):
    __slots__ = ("new_draft",)
    NEW_DRAFT_FIELD_NUMBER: _ClassVar[int]
    new_draft: float
    def __init__(self, new_draft: _Optional[float] = ...) -> None: ...

class SetDraftResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...

class SetKeelOffsetRequest(_message.Message):
    __slots__ = ("new_keel_offset",)
    NEW_KEEL_OFFSET_FIELD_NUMBER: _ClassVar[int]
    new_keel_offset: float
    def __init__(self, new_keel_offset: _Optional[float] = ...) -> None: ...

class SetKeelOffsetResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RequestResult
    def __init__(self, result: _Optional[_Union[RequestResult, _Mapping]] = ...) -> None: ...
