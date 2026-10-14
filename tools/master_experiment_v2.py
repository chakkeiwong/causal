#!/usr/bin/env python3
"""Bounded, restartable execution of registered master experiments.

Each request is atomically published under its immutable design identity. A
completed summary is reconstructed exclusively from those request records.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
from pathlib import Path
import resource
import sys
import time

import numpy as np
from scipy.stats import beta
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.pending')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    fd = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def exact_interval(k, n, error=.05):
    return [float(beta.ppf(error/2, k, n-k+1)) if k else 0.,
            float(beta.ppf(1-error/2, k+1, n-k)) if k < n else 1.]


def summary(rows, spec):
    cells = []
    family = len(spec['designs']) * len(spec['methods'])
    for cell, design in enumerate(spec['designs']):
        current = [r for r in rows if r['cell'] == cell]
        methods = {}
        indicators = {}
        for name in spec['methods']:
            values = [r['result']['methods'][name] for r in current]
            covers, widths, estimates, errors, statuses = [], [], [], [], {}
            topologies = {'whole_line':0,'unbounded':0,'disconnected':0,'empty':0}
            retention = []
            for row, value in zip(current, values):
                truth = row['result']['truth']
                bounds = value.get('interval')
                if bounds is not None:
                    bounds = [-np.inf if bounds[0] is None else bounds[0], np.inf if bounds[1] is None else bounds[1]]
                cover = bool(bounds is not None and bounds[0] <= truth <= bounds[1])
                # An explicit finite union is allowed in graph/effect packages.
                if 'components' in value:
                    cover = any(a <= truth <= b for a, b in value['components'])
                    bounds = [min(a for a, b in value['components']), max(b for a, b in value['components'])] if value['components'] else None
                if 'effect_set' in value:
                    pieces = [(-np.inf if c['lower'] is None else c['lower'], np.inf if c['upper'] is None else c['upper']) for c in value['effect_set']]
                    cover = any(a <= truth <= b for a,b in pieces)
                    bounds = [min(a for a,b in pieces),max(b for a,b in pieces)] if pieces else None
                    topologies['whole_line'] += int(pieces == [(-np.inf,np.inf)])
                    topologies['unbounded'] += int(any(not np.isfinite([a,b]).all() for a,b in pieces))
                    topologies['disconnected'] += int(len(pieces)>1)
                    topologies['empty'] += int(not pieces)
                if 'true_class_retained' in value: retention.append(value['true_class_retained'])
                covers.append(cover)
                statuses[value['status']] = statuses.get(value['status'], 0) + 1
                if bounds is not None and np.isfinite(bounds).all():
                    widths.append(bounds[1]-bounds[0])
                if 'estimate' in value:
                    estimates.append(value['estimate']-truth)
                if 'standard_error' in value:
                    errors.append(value['standard_error'])
            n, k = len(values), sum(covers)
            sd = float(np.std(estimates, ddof=1)) if len(estimates) > 1 else None
            lower = float(beta.ppf(.05/family, k, n-k+1)) if k else 0.
            methods[name] = dict(requests=n, covered=k, coverage_all=k/n,
                simultaneous_mc95=exact_interval(k, n, .05/family),
                simultaneous_lower95=lower, minimum_95_screen=lower >= .95,
                finite=len(widths), statuses=statuses, topologies=topologies,
                true_class_retained=sum(retention) if retention else None,
                width_quantiles=np.quantile(widths, [.1, .5, .9]).tolist() if widths else None,
                conditional_bias=float(np.mean(estimates)) if estimates else None,
                conditional_sd=sd, mean_se_over_sd=float(np.mean(errors)/sd) if errors and sd else None)
            indicators[name] = np.array(covers, dtype=float)
        primary = spec['methods'][0]
        paired = {}
        for name in spec['methods'][1:]:
            delta = indicators[primary]-indicators[name]
            paired[name] = dict(coverage_difference=float(delta.mean()),
                difference_mc_se=float(delta.std(ddof=1)/np.sqrt(len(delta))),
                gained=int(np.sum(delta == 1)), lost=int(np.sum(delta == -1)))
        cells.append(dict(design=design, methods=methods, paired_primary=paired,
            mean_elapsed_seconds=float(np.mean([r['elapsed_seconds'] for r in current])),
            mean_labels=float(np.mean([r['result'].get('labels', 0) for r in current])),
            mean_history_rows=float(np.mean([r['result'].get('history_rows', 0) for r in current]))))
    return dict(cells=cells, requests=len(rows),
                total_request_seconds=sum(r['elapsed_seconds'] for r in rows),
                max_process_rss_kib=max(r['process_rss_kib'] for r in rows),
                interpretation='Recorded synthetic evidence; finite grid screening does not prove uniform validity or bank utility.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task')
    parser.add_argument('--max-new', type=int, default=100)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    state = json.loads((ROOT / 'docs/program/state.json').read_text())
    reg = state['registrations'][args.task]
    specpath = ROOT / reg['path']
    folder = specpath.parent
    spec = json.loads(specpath.read_text())
    if digest(specpath) != reg['sha256']:
        raise ValueError('Registered protocol changed')
    for path, expected in spec['input_sha256'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('Registered input changed: ' + path)
    launchpath = folder / 'launch.json'
    if launchpath.exists():
        launch = json.loads(launchpath.read_text())
        if launch['registration_sha256'] != reg['sha256']:
            raise ValueError('Launch belongs to another registration')
    elif args.verify:
        raise ValueError('Missing launch')
    else:
        launch = dict(started_at=datetime.now(timezone.utc).isoformat(),
                      registration_sha256=reg['sha256'])
        if launch['started_at'] <= reg['registered_at']:
            raise ValueError('Launch must follow registration')
        atomic(launchpath, launch)
    module = importlib.import_module(spec['module'])
    rows, fresh = [], 0
    for cell, design in enumerate(spec['designs']):
        for index in range(spec['replications']):
            key = f'{cell:02d}-{index:05d}'
            path = folder / 'requests' / (key + '.json')
            if path.exists():
                row = json.loads(path.read_text())
                if (row['key'] != key or row['registration_sha256'] != reg['sha256']
                        or row['cell'] != cell or row['index'] != index):
                    raise ValueError('Request identity mismatch')
            else:
                if args.verify:
                    raise ValueError('Missing request ' + key)
                if fresh >= args.max_new:
                    print(json.dumps(dict(status='checkpoint', saved=len(rows), fresh=fresh)), flush=True)
                    return
                started = time.perf_counter()
                # Expected scientific refusals belong in request methods. Unexpected
                # exceptions are preserved and stop execution for defect review.
                try:
                    result = module.request(spec, cell, index)
                except Exception as error:
                    failure = folder / ('failure-' + key + '.json')
                    atomic(failure, dict(key=key, error=repr(error), launch=launch))
                    raise
                row = dict(key=key, cell=cell, index=index, registration_sha256=reg['sha256'],
                    result=result, elapsed_seconds=time.perf_counter()-started,
                    process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
                try:
                    atomic(path, row)
                except Exception as error:
                    atomic(folder / ('publication-failure-' + key + '.json'), dict(key=key,error=repr(error),launch=launch))
                    raise
                fresh += 1
            rows.append(row)
    result = summary(rows, spec)
    result.update(launch=launch, registration_sha256=reg['sha256'],
        request_sha256={str((folder/'requests'/(r['key']+'.json')).relative_to(ROOT)):
                        digest(folder/'requests'/(r['key']+'.json')) for r in rows})
    path = folder / 'results.json'
    if args.verify:
        if json.loads(path.read_text()) != result:
            raise ValueError('Saved summary does not reconstruct')
        print(json.dumps(dict(status='verified', task=args.task, requests=len(rows))))
    else:
        atomic(path, result)
        print(json.dumps(dict(status='complete', task=args.task, requests=len(rows),
            cells=[dict(name=c['design']['name'], covers={m:v['covered'] for m,v in c['methods'].items()}) for c in result['cells']])), flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=1):
        main()
