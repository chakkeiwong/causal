#!/usr/bin/env python3
"""Small standard-library launcher isolates worker RSS from data preparation."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--algorithm', choices=['dense', 'chunked'], required=True)
    parser.add_argument('--repeat', type=int, required=True)
    args = parser.parse_args()
    status = Path('/proc/self/status').read_text().splitlines()
    before = int(next(line for line in status if line.startswith('VmRSS:')).split()[1])*1024
    command = [sys.executable, str(ROOT/'tools/calibration_workloads.py'), '--worker', '--n', str(args.n),
        '--algorithm', args.algorithm, '--repeat', str(args.repeat)]
    start = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=600)
    elapsed = time.perf_counter()-start
    assert result.returncode == 0, result.stderr
    print(json.dumps(dict(launcher_rss_before_worker_bytes=before,
        complete_worker_seconds=elapsed,
        child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024)))
