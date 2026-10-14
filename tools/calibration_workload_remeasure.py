#!/usr/bin/env python3
"""Remeasure unchanged funding workloads after detecting inherited RSS peaks."""
import json
import os
import subprocess
import sys
import time
from calibration_common import ROOT, SPEC, Journal, digest
from calibration_workloads import INPUTS, input_paths, output_path, difference


def main():
    spec = json.loads((ROOT/SPEC).read_text())
    inputs = INPUTS+['tools/calibration_worker_launcher.py', 'tools/calibration_workload_remeasure.py',
        'docs/studies/calibration-workloads-results.json']
    inputs += [str(p.relative_to(ROOT)) for n in spec['workloads']['dates'] for p in input_paths(n)]
    journal = Journal('workload-remeasurement', inputs)
    def run(n, algorithm, repeat):
        identifier = repeat+100
        command = [sys.executable, str(ROOT/'tools/calibration_worker_launcher.py'), '--n', str(n),
            '--algorithm', algorithm, '--repeat', str(identifier)]
        environment = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        start = time.perf_counter()
        process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=660)
        elapsed = time.perf_counter()-start
        assert process.returncode == 0, process.stderr
        launcher = json.loads(process.stdout)
        path = output_path(n, algorithm, identifier)
        value = json.loads(path.read_text())
        assert launcher['launcher_rss_before_worker_bytes'] < 40*1024**2
        assert abs(launcher['child_peak_rss_bytes']-value['peak_rss_bytes']) < 2*1024**2
        value.update(algorithm=algorithm, dates=n, repeat=repeat, complete_process_seconds=elapsed,
            launcher=launcher, output_path=str(path.relative_to(ROOT)), output_sha256=digest(path))
        return value
    comparisons = []
    for n in spec['workloads']['dates']:
        for repeat in range(spec['workloads']['repeats']):
            pair = {}
            for algorithm in (['dense', 'chunked'] if repeat == 0 else ['chunked', 'dense']):
                pair[algorithm] = journal.run(f'{n}/{repeat}/{algorithm}', lambda: run(n, algorithm, repeat))
            error = difference(pair['dense']['result'], pair['chunked']['result'])
            assert error < 1e-9
            row = dict(dates=n, repeat=repeat, maximum_relative_difference=error,
                chunked_to_dense_peak_rss=pair['chunked']['peak_rss_bytes']/pair['dense']['peak_rss_bytes'],
                chunked_to_dense_complete_seconds=pair['chunked']['complete_process_seconds']/pair['dense']['complete_process_seconds'])
            comparisons.append(row)
            print(json.dumps(row), flush=True)
    journal.finish(dict(status='pass', comparisons=comparisons, runs=list(journal.rows.values()),
        scope='Unchanged inputs and scientific worker, through a standard-library launcher below 40 MiB RSS. Child and worker peak RSS agree. Complete times include the extra launcher equally. Original contaminated memory measurements remain preserved. Local joint-OLS route only; no growing-pilot streaming or bank-platform claim.'))


if __name__ == '__main__':
    main()
