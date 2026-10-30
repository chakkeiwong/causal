#!/usr/bin/env python3
"""Registered, resumable linked-outcome funding comparison and read-only replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.funding_calibration import DECLARATIONS
from causalbank.linked_funding import LINKED_DECLARATIONS, fit_linked_funding, simulate_linked
from causalbank.weak_audit_sharpening import fit_transformed_projection
from weak_audit_study import properties, interval

SPEC = 'docs/studies/linked-funding-spec.json'
JOURNAL = 'docs/studies/linked-funding-final.jsonl'
RESULT = 'docs/studies/linked-funding-results.json'
CHECKS = 'docs/reviews/linked-funding-checks.json'
INPUTS = [SPEC, CHECKS, 'docs/program/linked-funding-plan-2026-10-11.md',
          'docs/reviews/linked-funding-initial-preservation.json',
          'docs/studies/linked-funding-initial-schema-failure-2026-10-11.zip',
          'tools/linked_funding_study.py', 'tools/weak_audit_study.py',
          'src/causalbank/linked_funding.py', 'src/causalbank/weak_audit_sharpening.py',
          'src/causalbank/weak_audit_projection.py', 'src/causalbank/linkage_sets.py',
          'src/causalbank/streaming_pilot.py', 'src/causalbank/funding_calibration.py',
          'src/causalbank/dynamic_funding.py', 'docs/studies/dynamic-funding-spec.json',
          'docs/studies/dynamic-observation-spec.json']


def read(name):
    return json.loads((ROOT/name).read_text())


def digest(name):
    with (ROOT/name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def generate(spec, cell, index):
    base, observation = read(spec['base']), read(spec['observation'])
    design = spec['designs'][cell]
    law = dict(base, rho=design.get('rho', base['rho']))
    obs = dict(observation, correct_pair_probability=design['probability'])
    settings = dict(inclusion=design['q'], actual_inclusion=design.get('actual_q'),
                    label_error=design.get('label_error', 0.), correlation=design.get('innovation_correlation', 0.))
    rows, audit = simulate_linked(law, obs, spec['dates'], [spec['seed'], cell, index, 1],
                                 [spec['seed'], cell, index, 4], **settings)
    pilot, pa = simulate_linked(law, obs, spec['pilot_multiple']*spec['dates'],
                               [spec['seed'], cell, index, 2], [spec['seed'], cell, index, 5], **settings)
    counts = np.random.default_rng([spec['seed'], cell, index, 3]).binomial(
        spec['count_audit_per_stratum'], design['probability']).tolist()
    return base, law, rows, audit, pilot, pa, counts


def request(spec, cell, index):
    base, law, rows, audit, pilot, pa, counts = generate(spec, cell, index)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    methods = {}
    for name in spec['methods']:
        try:
            if name == 'transformed_counts':
                result = fit_transformed_projection(pilot, rows, target, counts,
                    [spec['count_audit_per_stratum']]*2, base['penalties'],
                    chunk_size=spec['chunk_size'], declarations=DECLARATIONS,
                    response_error=spec['response_error'], audit_error=spec['audit_error'])
            else:
                result = fit_linked_funding(pilot, rows, target, pa, audit, base['penalties'],
                    augmentation=name == 'linked_augmented', chunk_size=spec['chunk_size'],
                    alpha=spec['alpha'], declarations=LINKED_DECLARATIONS)
            methods[name] = result
        except (ValueError, np.linalg.LinAlgError) as error:
            methods[name] = dict(status='failed_request', error=str(error))
    return dict(methods=methods, count_audit_successes=counts,
                evaluation_labels=int(np.sum(audit[0])), pilot_labels=int(np.sum(pa[0])))


def summarize(rows, truth, spec):
    methods, flags = {}, {}
    for name in spec['methods']:
        current = [properties(row['methods'][name], truth) for row in rows]
        flags[name] = current
        n, covered = len(current), sum(x['covered'] for x in current)
        finite = [x['width'] for x in current if x['finite']]
        computed = [row['methods'][name] for row in rows if row['methods'][name]['status'] == 'computed_set']
        estimates = [x['estimate'] for x in computed if 'estimate' in x]
        errors = [x['standard_error'] for x in computed if 'standard_error' in x]
        statuses = {}
        for row in rows:
            key = row['methods'][name]['status']
            statuses[key] = statuses.get(key, 0)+1
        sd = float(np.std(estimates, ddof=1)) if len(estimates) > 1 else None
        methods[name] = dict(requests=n, covered=covered, coverage_all=covered/n,
            mc95=interval(covered, n),
            simultaneous_mc95=interval(covered, n, .05/(len(spec['designs'])*len(spec['methods']))),
            finite=sum(x['finite'] for x in current), whole_line=sum(x['whole'] for x in current),
            unbounded=sum(x['unbounded'] for x in current), empty=sum(x['empty'] for x in current),
            disconnected=sum(x['disconnected'] for x in current), statuses=statuses,
            conditional_finite_median_width=float(np.median(finite)) if finite else None,
            conditional_bias=float(np.mean(estimates)-truth) if estimates else None,
            conditional_empirical_sd=sd,
            mean_se_over_sd=float(np.mean(errors)/sd) if sd and errors else None)
    paired = {}
    for name in ('transformed_counts', 'linked_ipw'):
        a, b = flags[name], flags['linked_augmented']
        both = [(x['width'], y['width']) for x, y in zip(a, b) if x['finite'] and y['finite']]
        paired[name] = dict(both_finite=len(both), augmented_narrower=sum(y < x for x,y in both),
                           augmented_wider=sum(y > x for x,y in both),
                           finite_gained=sum(y['finite'] and not x['finite'] for x,y in zip(a,b)),
                           finite_lost=sum(x['finite'] and not y['finite'] for x,y in zip(a,b)),
                           coverage_gained=sum(y['covered'] and not x['covered'] for x,y in zip(a,b)),
                           coverage_lost=sum(x['covered'] and not y['covered'] for x,y in zip(a,b)),
                           median_width_ratio=float(np.median([y/x for x,y in both])) if both else None)
    return dict(methods=methods, paired_with_augmented=paired,
                mean_evaluation_labels=float(np.mean([x['evaluation_labels'] for x in rows])),
                mean_pilot_labels=float(np.mean([x['pilot_labels'] for x in rows])),
                separate_count_labels=2*spec['count_audit_per_stratum'])


def main(verify=False, max_new=None):
    spec = read(SPEC)
    checks = read(CHECKS)
    if checks['status'] != 'pass' or any(digest(k) != v for k,v in checks['input_sha256'].items()):
        raise ValueError('Numerical qualification is missing or stale')
    identity = {name:digest(name) for name in sorted(INPUTS)}
    records = {}
    journal = ROOT/JOURNAL
    if journal.exists():
        with journal.open() as stream:
            if json.loads(next(stream)) != {'input_sha256': identity}:
                raise ValueError('Registered inputs changed after final draws')
            for line in stream:
                row = json.loads(line)
                if row['key'] in records:
                    raise ValueError('Duplicate request: '+row['key'])
                records[row['key']] = row['result']
    elif not verify:
        journal.write_text(json.dumps(dict(input_sha256=identity))+'\n')
    base = read(spec['base'])
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    results, fresh = [], 0
    total = spec['repetitions']*len(spec['designs'])
    for cell, design in enumerate(spec['designs']):
        rho = design.get('rho', base['rho'])
        truth = float(target.weights()@(base['beta']*rho**np.arange(target.horizon+1))-target.direct_cost())
        rows = []
        for index in range(spec['repetitions']):
            key = f'{design["name"]}/{index}'
            if key not in records:
                if verify:
                    raise ValueError('Missing request '+key)
                if max_new is not None and fresh >= max_new:
                    print(json.dumps(dict(status='checkpoint', saved=len(records), planned=total)), flush=True)
                    return
                result = request(spec, cell, index)
                with journal.open('a') as stream:
                    stream.write(json.dumps(dict(key=key, result=result), allow_nan=False)+'\n')
                    stream.flush()
                    os.fsync(stream.fileno())
                records[key] = result
                fresh += 1
                if fresh % 100 == 0:
                    print(f'Saved {len(records)}/{total}', flush=True)
            rows.append(records[key])
        summary = summarize(rows, truth, spec)
        results.append(dict(design=design, truth=truth, summary=summary))
        print(json.dumps(dict(design=design['name'], covered={m:x['covered'] for m,x in summary['methods'].items()},
                              finite={m:x['finite'] for m,x in summary['methods'].items()})), flush=True)
    if len(records) != total:
        raise ValueError('Unexpected request count')
    result = dict(status='pass', date='2026-10-11', requests=total, results=results,
                  scope='Fresh selected-law synthetic comparison with linked-outcome information; no bank validation or economic qualification.',
                  input_sha256=dict(identity, **{JOURNAL:digest(JOURNAL)}))
    if verify:
        if read(RESULT) != result:
            raise ValueError('Saved summary differs from journal')
        print('Linked funding journal reconstruction passes.')
    else:
        (ROOT/RESULT).write_text(json.dumps(result, indent=2)+'\n')
        print(f'Completed {total} requests.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--max-new', type=int)
    args = parser.parse_args()
    with threadpool_limits(limits=1):
        main(args.verify, args.max_new)
