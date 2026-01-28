from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GridDescription(_message.Message):
    __slots__ = ("mode", "hor_angles", "ver_angles", "max_range")
    class GridMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        kFixed: _ClassVar[GridDescription.GridMode]
        OBSELETE_kAlternating: _ClassVar[GridDescription.GridMode]

    kFixed: GridDescription.GridMode
    OBSELETE_kAlternating: GridDescription.GridMode
    MODE_FIELD_NUMBER: _ClassVar[int]
    HOR_ANGLES_FIELD_NUMBER: _ClassVar[int]
    VER_ANGLES_FIELD_NUMBER: _ClassVar[int]
    MAX_RANGE_FIELD_NUMBER: _ClassVar[int]
    mode: GridDescription.GridMode
    hor_angles: _containers.RepeatedScalarFieldContainer[float]
    ver_angles: _containers.RepeatedScalarFieldContainer[float]
    max_range: float
    def __init__(
        self,
        mode: _Optional[_Union[GridDescription.GridMode, str]] = ...,
        hor_angles: _Optional[_Iterable[float]] = ...,
        ver_angles: _Optional[_Iterable[float]] = ...,
        max_range: _Optional[float] = ...,
    ) -> None: ...
