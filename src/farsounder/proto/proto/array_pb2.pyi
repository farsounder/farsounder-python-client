from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArrayData(_message.Message):
    __slots__ = ("dims", "type", "order", "data")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BYTE: _ClassVar[ArrayData.Type]
        INT16: _ClassVar[ArrayData.Type]
        UINT16: _ClassVar[ArrayData.Type]
        INT32: _ClassVar[ArrayData.Type]
        UINT32: _ClassVar[ArrayData.Type]
        INT64: _ClassVar[ArrayData.Type]
        UINT64: _ClassVar[ArrayData.Type]
        FLOAT32: _ClassVar[ArrayData.Type]
        FLOAT64: _ClassVar[ArrayData.Type]
        COMPLEX64: _ClassVar[ArrayData.Type]
        COMPLEX128: _ClassVar[ArrayData.Type]
        BOOL: _ClassVar[ArrayData.Type]
    BYTE: ArrayData.Type
    INT16: ArrayData.Type
    UINT16: ArrayData.Type
    INT32: ArrayData.Type
    UINT32: ArrayData.Type
    INT64: ArrayData.Type
    UINT64: ArrayData.Type
    FLOAT32: ArrayData.Type
    FLOAT64: ArrayData.Type
    COMPLEX64: ArrayData.Type
    COMPLEX128: ArrayData.Type
    BOOL: ArrayData.Type
    class Order(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROW_MAJOR: _ClassVar[ArrayData.Order]
        COLUMN_MAJOR: _ClassVar[ArrayData.Order]
    ROW_MAJOR: ArrayData.Order
    COLUMN_MAJOR: ArrayData.Order
    DIMS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    dims: _containers.RepeatedScalarFieldContainer[int]
    type: ArrayData.Type
    order: ArrayData.Order
    data: bytes
    def __init__(self, dims: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[ArrayData.Type, str]] = ..., order: _Optional[_Union[ArrayData.Order, str]] = ..., data: _Optional[bytes] = ...) -> None: ...
