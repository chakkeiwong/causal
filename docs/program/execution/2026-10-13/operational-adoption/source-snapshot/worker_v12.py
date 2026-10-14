"""Fixed internal subprocess entry; no user-selectable code or shell."""
import argparse
import json
import os
from pathlib import Path
import resource
import signal
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-bytes", type=int, required=True)
    parser.add_argument("--wall-seconds", type=float, required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--job")
    args = parser.parse_args()
    if args.memory_bytes < 64 * 1024 * 1024 or not 0 < args.wall_seconds <= 300:
        raise ValueError("Worker resource budget outside local bounds")
    resource.setrlimit(resource.RLIMIT_AS, (args.memory_bytes, args.memory_bytes))
    signal.signal(signal.SIGALRM, lambda signum, frame: (_ for _ in ()).throw(TimeoutError("wall budget")))
    signal.setitimer(signal.ITIMER_REAL, args.wall_seconds)
    try:
        if args.job:
            from .runtime_v12 import Runtime
            Runtime(args.root).run_report_job(args.job)
        else:
            from .operation_service_v12 import OperationService, envelope
            data = sys.stdin.buffer.read(1_000_001)
            if len(data) > 1_000_000:
                raise ValueError("Worker request exceeds bound")
            request = json.loads(data)
            try:
                response = OperationService(args.root).invoke(request)
            except Exception as exc:
                response = envelope(request, status="failed", disposition="unavailable",
                    qualification="none", error={"code": "invalid_or_unavailable_input" if isinstance(exc, (ValueError, KeyError, TypeError, FileNotFoundError)) else "worker_failure",
                    "message": type(exc).__name__ + ": " + str(exc)[:180], "retryable": False})
            sys.stdout.write(json.dumps(response, allow_nan=False, sort_keys=True) + "\n")
            sys.stdout.flush()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    main()
