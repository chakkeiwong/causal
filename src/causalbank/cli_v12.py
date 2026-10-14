"""Local JSON CLI for the V12 canonical operation service."""
import argparse
import json
import os
from pathlib import Path
import sys

import jsonschema

from .artifacts_v12 import MAX_ARTIFACT, ROOT
from .runtime_v12 import Runtime


def state_root():
    # An operator launch setting, never a field in a scientific/tool request.
    return Path(os.environ.get("CAUSALBANK_STATE_ROOT", ROOT / ".runtime/operation-v12"))


def output(value):
    sys.stdout.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def read_request(path):
    if path == "-":
        data = sys.stdin.buffer.read(1_000_001)
    else:
        file = Path(path)
        if file.is_symlink() or file.stat().st_size > 1_000_000:
            raise ValueError("Request file must be a bounded nonsymlink file")
        data = file.read_bytes()
    if len(data) > 1_000_000:
        raise ValueError("Request exceeds 1 MB CLI input bound")
    return json.loads(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description="CausalBank local reference runtime; scientific dispositions are explicit")
    parser.add_argument("--version", action="version", version="causalbank local-runtime/1; canonical schema 1.0.0; MCP 2025-11-25")
    sub = parser.add_subparsers(dest="command", required=True)
    invoke = sub.add_parser("operation", help="Invoke a canonical operation using JSON input")
    invoke.add_argument("name")
    invoke.add_argument("--input", default="-", help="Explicit JSON file or '-' for stdin")
    art = sub.add_parser("artifact", help="Operator-local artifact import/description")
    art.add_argument("action", choices=["put", "describe"])
    art.add_argument("--schema-version")
    art.add_argument("--role")
    art.add_argument("--id")
    args = parser.parse_args(argv)
    try:
        service = Runtime(state_root())
        if args.command == "artifact":
            if args.action == "describe":
                if not args.id:
                    raise ValueError("Artifact ID required")
                output(service.store.reference(args.id))
                return 0
            if not args.schema_version or not args.role:
                raise ValueError("Artifact schema-version and role required")
            data = sys.stdin.buffer.read(MAX_ARTIFACT + 1)
            if len(data) > MAX_ARTIFACT:
                raise ValueError("Artifact import exceeds local byte limit")
            output(service.store.put(json.loads(data), args.schema_version, args.role))
            return 0
        request = read_request(args.input)
        if request.get("operation") != args.name:
            raise ValueError("CLI operation and canonical request operation disagree")
        response = service.invoke(request)
        output(response)
        return 0 if response["status"] in {"completed", "queued", "running", "cancelled"} else 4
    except (json.JSONDecodeError, jsonschema.ValidationError, ValueError, KeyError, TypeError) as exc:
        output({"error": {"code": "invalid_request", "message": str(exc)[:300]}})
        return 2
    except (FileNotFoundError, PermissionError):
        output({"error": {"code": "unavailable_artifact", "message": "Required local artifact is unavailable"}})
        return 3
    except Exception:
        output({"error": {"code": "internal_failure", "message": "Local operation failed; inspect the operator log"}})
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
