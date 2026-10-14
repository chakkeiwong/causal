#!/usr/bin/env python3
"""Complete fresh-process dense/chunked funding workloads and request recovery."""
import argparse
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits, threadpool_info
from calibration_common import ROOT, SPEC, Journal, save, digest
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import simulate_rows, fit_funding, fit_dense, DECLARATIONS

INPUTS = [SPEC, 'tools/calibration_workloads.py', 'src/causalbank/funding_calibration.py',
    'src/causalbank/dynamic_funding.py', 'docs/studies/dynamic-funding-spec.json',
    'docs/studies/dynamic-observation-spec.json']
FOLDER = ROOT / 'docs/studies/calibration-workload-runs'


def input_paths(n):
    return FOLDER/f'input-{n}.npy', FOLDER/f'input-{n}.json'


def output_path(n, algorithm, repeat):
    return FOLDER/f'{algorithm}-{n}-{repeat}.json'


def prepare(n):
    FOLDER.mkdir(exist_ok=True)
    path, metadata = input_paths(n)
    expected = {p:digest(p) for p in INPUTS}
    if path.exists() or metadata.exists():
        record = json.loads(metadata.read_text())
        assert record['input_sha256'] == expected and digest(path) == record['sha256']
        return
    spec = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/spec['base']).read_text())
    obs = json.loads((ROOT/spec['observation']).read_text())
    obs['correct_pair_probability'] = [.9, .85]
    rows = simulate_rows(base, obs, n, [spec['workload_seed'], n])
    with path.open('xb') as stream:
        np.save(stream, rows)
    metadata.write_text(json.dumps(dict(path=str(path.relative_to(ROOT)), sha256=digest(path),
        shape=list(rows.shape), input_sha256=expected), indent=2)+'\n')
    print(json.dumps({'prepared_origins': n, 'input_bytes': path.stat().st_size}), flush=True)


def worker(args):
    spec = json.loads((ROOT/SPEC).read_text())
    base = json.loads((ROOT/spec['base']).read_text())
    path, metadata = input_paths(args.n)
    expected = json.loads(metadata.read_text())
    assert all(digest(p) == sha for p, sha in expected['input_sha256'].items())
    assert digest(path) == expected['sha256']
    rows = np.load(path, mmap_mode='r' if args.algorithm == 'chunked' else None)
    rows.flags.writeable = False
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    with threadpool_limits(limits=1):
        pools = threadpool_info()
        assert all(p['num_threads'] == 1 for p in pools)
        operation = fit_funding if args.algorithm == 'chunked' else fit_dense
        kwargs = dict(declarations=DECLARATIONS)
        if args.algorithm == 'chunked':
            kwargs['chunk_size'] = spec['workloads']['chunk_size']
        result = operation(rows, target, [9000, 8500], [10000, 10000], **kwargs)
    if args.interrupt_before_output:
        raise SystemExit(75)
    assert digest(path) == expected['sha256']
    output = output_path(args.n, args.algorithm, args.repeat)
    value = dict(result=result, input_sha256=expected['sha256'], numeric_threadpools=pools,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime)
    temporary = output.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
    temporary.replace(output)
    assert json.loads(output.read_text()) == value


def invoke(n, algorithm, repeat, interrupted=False):
    command = [sys.executable, str(Path(__file__).resolve()), '--worker', '--n', str(n),
        '--algorithm', algorithm, '--repeat', str(repeat)]
    if interrupted:
        command.append('--interrupt-before-output')
    environment = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    start = time.perf_counter()
    process = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=600)
    elapsed = time.perf_counter()-start
    if interrupted:
        assert process.returncode == 75, process.stderr
        return elapsed
    assert process.returncode == 0, process.stderr
    path = output_path(n, algorithm, repeat)
    value = json.loads(path.read_text())
    value.update(algorithm=algorithm, dates=n, repeat=repeat, complete_process_seconds=elapsed,
        output_path=str(path.relative_to(ROOT)), output_sha256=digest(path))
    return value


def difference(left, right):
    if isinstance(left, dict):
        assert set(left) == set(right)
        return max((difference(left[k], right[k]) for k in left if k != 'algorithm'), default=0.)
    if isinstance(left, list):
        assert len(left) == len(right)
        return max((difference(a, b) for a, b in zip(left, right)), default=0.)
    if isinstance(left, (float, int)):
        return abs(left-right)/max(1., abs(left), abs(right))
    assert left == right
    return 0.


def rehearsal():
    n = 431
    prepare(n)
    path = output_path(n, 'chunked', -1)
    before = digest(path) if path.exists() else None
    invoke(n, 'chunked', -1, True)
    after = digest(path) if path.exists() else None
    assert before == after
    first = invoke(n, 'chunked', -1)
    second = invoke(n, 'chunked', -1)
    assert first['result'] == second['result']
    result = dict(status='pass', deliberate_worker_exit=75, interrupted_write_preserved_previous_artifact=True,
        repeated_completed_request_same_result=True,
        scope='Interruption before output is retried from immutable input; no claim of partial-fit checkpoint or distributed recovery.')
    save('docs/reviews/calibration-recovery-rehearsal.json', result, INPUTS+
        [str(p.relative_to(ROOT)) for p in (*input_paths(n), path)])
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))


def main():
    spec = json.loads((ROOT/SPEC).read_text())
    for n in spec['workloads']['dates']:
        prepare(n)
    inputs = INPUTS+[str(p.relative_to(ROOT)) for n in spec['workloads']['dates'] for p in input_paths(n)]
    journal = Journal('workloads', inputs)
    rows = []
    for n in spec['workloads']['dates']:
        for repeat in range(spec['workloads']['repeats']):
            pair = []
            # Alternate order across repeats; every operation has a fresh process.
            algorithms = ['dense', 'chunked'] if repeat == 0 else ['chunked', 'dense']
            for algorithm in algorithms:
                value = journal.run(f'{n}/{repeat}/{algorithm}', lambda: invoke(n, algorithm, repeat))
                pair.append(value)
            keyed = {r['algorithm']:r for r in pair}
            error = difference(keyed['dense']['result'], keyed['chunked']['result'])
            assert error < 1e-9
            rows.append(dict(dates=n, repeat=repeat, maximum_relative_difference=error,
                chunked_to_dense_peak_rss=keyed['chunked']['peak_rss_bytes']/keyed['dense']['peak_rss_bytes'],
                chunked_to_dense_complete_seconds=keyed['chunked']['complete_process_seconds']/keyed['dense']['complete_process_seconds']))
            print(json.dumps(rows[-1]), flush=True)
    journal.finish(dict(status='pass', comparisons=rows, runs=list(journal.rows.values()),
        platform=dict(system=platform.system(), machine=platform.machine(), python=platform.python_version()),
        scope='Complete local joint-OLS route, including imports, input checks, fitting, scalar inference, persistence/read-back. Acquisition excluded equally; mapped input pages included in peak RSS. Does not qualify growing-pilot streaming, multi-host service levels or analyst savings.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--rehearsal', action='store_true')
    parser.add_argument('--interrupt-before-output', action='store_true')
    parser.add_argument('--n', type=int)
    parser.add_argument('--algorithm', choices=['dense', 'chunked'])
    parser.add_argument('--repeat', type=int)
    args = parser.parse_args()
    worker(args) if args.worker else rehearsal() if args.rehearsal else main()
