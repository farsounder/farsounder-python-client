from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    proto_dir = repo_root / "proto"
    out_dir = repo_root / "src" / "farsounder" / "proto"

    if not proto_dir.exists():
        print(f"Proto directory not found: {proto_dir}")
        return 1

    proto_files = sorted(proto_dir.glob("*.proto"))
    if not proto_files:
        print(f"No .proto files found in {proto_dir}")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "__init__.py").touch(exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{repo_root}",
        f"-I{proto_dir}",
        f"--python_out={out_dir}",
        f"--pyi_out={out_dir}",
        *[str(path) for path in proto_files],
    ]
    subprocess.check_call(cmd)
    print(f"Generated {len(proto_files)} protobuf modules in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
