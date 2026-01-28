"""Protobuf package shim for generated modules."""

from __future__ import annotations

from importlib import import_module
from importlib.machinery import ModuleSpec
from pathlib import Path
import sys
import types

_proto_pkg_name = "proto"
_proto_pkg_path = Path(__file__).resolve().parent / "proto"

if _proto_pkg_name not in sys.modules:
    _module = types.ModuleType(_proto_pkg_name)
    _module.__path__ = [str(_proto_pkg_path)]
    _module.__spec__ = ModuleSpec(_proto_pkg_name, loader=None, is_package=True)
    sys.modules[_proto_pkg_name] = _module

time_pb2 = import_module("farsounder.proto.proto.time_pb2")
array_pb2 = import_module("farsounder.proto.proto.array_pb2")
grid_description_pb2 = import_module("farsounder.proto.proto.grid_description_pb2")
nmea_pb2 = import_module("farsounder.proto.proto.nmea_pb2")
nav_info_pb2 = import_module("farsounder.proto.proto.nav_info_pb2")
nav_api_pb2 = import_module("farsounder.proto.proto.nav_api_pb2")

__all__ = [
    "nav_api_pb2",
    "nav_info_pb2",
    "array_pb2",
    "grid_description_pb2",
    "nmea_pb2",
    "time_pb2",
]