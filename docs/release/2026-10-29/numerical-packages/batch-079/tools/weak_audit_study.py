#!/usr/bin/env python3
"""Registered fresh paired weak-audit study with durable per-request records."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import numpy as np
from scipy.stats import beta
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import DECLARATIONS, simulate_rows
from causalbank.linkage_sets import decode_set
from causalbank.streaming_pilot import fit_streaming_pilot
from causalbank.weak_audit_projection import fit_weak_audit_projection

SPEC = 'docs/studies/weak-audit-projection-spec.json'
JOURNAL = 'docs/studies/weak-audit-projection-final.jsonl'
RESULT = 'docs/studies/weak-audit-projection-results.json'
INPUTS = [SPEC, 'tools/weak_audit_study.py', 'tools/weak_audit_checks.py',
          'docs/reviews/weak-audit-projection-checks.json',
          'docs/program/weak-audit-projection-plan-2026-10-11.md',
          'docs/reviews/weak-audit-projection-plan-review-2026-10-11.md',
          'src/causalbank/weak_audit_projection.py', 'src/causalbank/streaming_pilot.py',
          'src/causalbank/funding_calibration.py', 'src/causalbank/dynamic_funding.py',
          'src/causalbank/linkage_sets.py', 'src/causalbank/dynamic_validation.py',
          'src/causalbank/responses.py', 'docs/studies/dynamic-funding-spec.json',
          'docs/studies/dynamic-observation-spec.json']


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def interval(k, n, alpha=.05):
    return [0. if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1)),
            1. if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))]


def properties(result, truth):
    if result['status'] == 'computed':
        pieces = [result['interval']]
    elif result['status'] in ('computed_set', 'empty_projection'):
        pieces = decode_set(result['financial_set'])
    else:
        pieces = []
    computed = result['status'] in ('computed', 'computed_set', 'empty_projection')
    covered = any(lo <= truth <= hi for lo, hi in pieces)
    finite = bool(pieces) and all(math.isfinite(lo) and math.isfinite(hi) for lo, hi in pieces)
    whole = pieces == [(-math.inf, math.inf)]
    return dict(covered=covered, computed=computed, finite=finite, whole=whole,
                disconnected=len(pieces) > 1, empty=computed and not pieces,
                unbounded=bool(pieces) and not finite,
                width=sum(hi - lo for lo, hi in pieces) if finite else None)


def summarize(rows, truth, spec):
    summaries, values = {}, {}
    for method in spec['methods']:
        values[method] = [properties(row['methods'][method], truth) for row in rows]
        items = values[method]
        n = len(items)
        k = sum(item['covered'] for item in items)
        finite_items = [item for item in items if item['finite']]
        widths = [item['width'] for item in finite_items]
        statuses = {}
        for row in rows:
            status = row['methods'][method]['status']
            statuses[status] = statuses.get(status, 0) + 1
        summaries[method] = dict(
            requests=n, covered=k, coverage_all=k / n,
            mc95=interval(k, n), simultaneous_mc95=interval(k, n, .05 / len(spec['designs'])),
            computed=sum(item['computed'] for item in items),
            finite=sum(item['finite'] for item in items),
            whole_line=sum(item['whole'] for item in items),
            disconnected=sum(item['disconnected'] for item in items),
            empty=sum(item['empty'] for item in items),
            unbounded=sum(item['unbounded'] for item in items),
            coverage_among_finite=(sum(item['covered'] for item in finite_items) / len(finite_items)
                                   if finite_items else None),
            finite_width_quantiles=np.quantile(widths, [.1, .5, .9]).tolist() if widths else None,
            statuses=statuses)
    left, right = (values[name] for name in spec['methods'])
    gains = sum(b['covered'] and not a['covered'] for a, b in zip(left, right))
    losses = sum(a['covered'] and not b['covered'] for a, b in zip(left, right))
    return dict(methods=summaries, paired=dict(gained=gains, lost=losses,
                                              coverage_difference=(gains - losses) / len(rows)))


def load_journal(identity):
    path = ROOT / JOURNAL
    records = {}
    if path.exists():
        with path.open() as stream:
            if json.loads(next(stream)) != {'input_sha256': identity}:
                raise ValueError('Changed registered study inputs; no hash replacement is allowed')
            for line in stream:
                row = json.loads(line)
                if row['key'] in records:
                    raise ValueError('Duplicate final request')
                records[row['key']] = row['result']
    return records


def main(verify):
    spec, base, observation = read(SPEC), read('docs/studies/dynamic-funding-spec.json'), read('docs/studies/dynamic-observation-spec.json')
    checks = read('docs/reviews/weak-audit-projection-checks.json')
    if checks['status'] != 'pass' or any(digest(path) != value for path, value in checks['input_sha256'].items()):
        raise ValueError('Missing or stale independent numerical checks')
    identity = {path: digest(path) for path in sorted(INPUTS)}
    records = load_journal(identity)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    if not verify and not (ROOT / JOURNAL).exists():
        (ROOT / JOURNAL).write_text(json.dumps(dict(input_sha256=identity)) + '\n')
    results = []
    for cell, design in enumerate(spec['designs']):
        law = dict(base, rho=design.get('rho', base['rho']))
        obs = dict(observation, correct_pair_probability=design['probability'])
        correlation = design.get('innovation_correlation', 0.)
        truth = float(target.weights() @ (base['beta'] * law['rho'] ** np.arange(target.horizon + 1)) - target.direct_cost())
        rows = []
        for i in range(spec['repetitions']):
            key = f'{design["name"]}/{i}'
            if key not in records:
                if verify:
                    raise ValueError('Missing request: ' + key)
                data = simulate_rows(law, obs, design['dates'], [spec['seed'], cell, i, 1], correlation)
                prior = simulate_rows(law, obs, spec['pilot_multiple'] * design['dates'], [spec['seed'], cell, i, 2], correlation)
                counts = np.random.default_rng([spec['seed'], cell, i, 3]).binomial(design['audit'], design['probability']).tolist()
                methods = {}
                for method, function in [('pilot4_horizon', fit_streaming_pilot),
                                         ('weak_audit_projection', fit_weak_audit_projection)]:
                    try:
                        extra = dict(response_error=spec['response_error_total'], audit_error=spec['audit_error_total']) if method == 'weak_audit_projection' else {}
                        result = function(prior, data, target, counts, [design['audit']] * 2,
                                          base['penalties'], chunk_size=spec['pilot_chunk_size'],
                                          declarations=DECLARATIONS, **extra)
                        result.pop('coefficient', None)
                    except (ValueError, np.linalg.LinAlgError) as error:
                        result = dict(status='failed_request', error=str(error))
                    methods[method] = result
                record = dict(methods=methods, audit_successes=counts)
                encoded = json.dumps(dict(key=key, result=record), allow_nan=False)
                with (ROOT / JOURNAL).open('a') as stream:
                    stream.write(encoded + '\n')
                    stream.flush()
                    os.fsync(stream.fileno())
                records[key] = record
                if len(records) % 100 == 0:
                    print(f'Saved {len(records)}/3000 requests', flush=True)
            rows.append(records[key])
        results.append(dict(design=design, truth=truth, summary=summarize(rows, truth, spec)))
        print(json.dumps(dict(design=design['name'], coverage={name: result['coverage_all'] for name, result in results[-1]['summary']['methods'].items()})), flush=True)
    if len(records) != len(spec['designs']) * spec['repetitions']:
        raise ValueError('Unexpected extra final requests')
    result = dict(status='pass', date='2026-10-11', requests=len(records), results=results,
                  scope='Fixed selected synthetic laws; numerical completion is distinct from calibration and finite bank precision.',
                  input_sha256=dict(identity, **{JOURNAL: digest(JOURNAL)}))
    if verify:
        if read(RESULT) != result:
            raise ValueError('Saved summary differs from reconstructed requests')
        print('Journal reconstruction and registered input identities: pass')
    else:
        (ROOT / RESULT).write_text(json.dumps(result, indent=2) + '\n')
        print(f'Completed {len(records)} fresh paired requests.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    with threadpool_limits(limits=1):
        main(parser.parse_args().verify)
