#!/usr/bin/env python3
"""Registered dynamic comparison of regular and projected linkage inference."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget, train_pilot
from causalbank.dynamic_product import Backend, DynamicBrief, fit_linked
from causalbank.linked_observation import linked_response
from causalbank.linkage_sets import decode_set, binomial_interval
from dynamic_observation_study import make_linked


def default(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


def contains(pieces, value):
    return any(lo <= value <= hi for lo, hi in pieces)


def summarize(rows, truth):
    sets = [decode_set(r['projection']['financial_set']) for r in rows]
    bounded = [r for r in sets if r and all(math.isfinite(x) for pair in r for x in pair)]
    valid = [r['regular'] for r in rows if r['regular']['status'] == 'computed']
    regular_count = sum(r['financial_interval'][0] <= truth <= r['financial_interval'][1] for r in valid)
    projected_count = sum(contains(r, truth) for r in sets)
    challengers = [decode_set(r['projection']['candidate_box_challenger']) for r in rows]
    challenger_bounded = [r for r in challengers if r and all(math.isfinite(x) for pair in r for x in pair)]
    return {'requested': len(rows), 'projection_coverage': projected_count / len(rows),
            'projection_coverage_mc_interval': binomial_interval(projected_count, len(rows), .05),
            'bounded_fraction': len(bounded) / len(rows),
            'disconnected_fraction': sum(len(r) > 1 for r in sets) / len(rows),
            'whole_line_fraction': sum(r == [(-math.inf, math.inf)] for r in sets) / len(rows),
            'empty_fraction': sum(not r for r in sets) / len(rows),
            'median_width_given_bounded': float(np.median([sum(hi-lo for lo, hi in r) for r in bounded])) if bounded else None,
            'regular_available': len(valid), 'regular_coverage_all': regular_count / len(rows),
            'candidate_box_coverage': sum(contains(r, truth) for r in challengers) / len(rows),
            'candidate_box_bounded_fraction': len(challenger_bounded) / len(rows),
            'candidate_box_median_width_given_bounded': float(np.median([sum(hi-lo for lo, hi in r) for r in challenger_bounded])) if challenger_bounded else None,
            'regular_coverage_given_available': regular_count / len(valid) if valid else None,
            'regular_median_width_given_available': float(np.median([r['financial_interval'][1]-r['financial_interval'][0] for r in valid])) if valid else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pilot', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'docs/studies/linkage-projection-spec.json'
    spec = json.loads(path.read_text())
    base = json.loads((ROOT / spec['funding_spec']).read_text())
    observation = json.loads((ROOT / spec['observation_spec']).read_text())
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    truth = float(target.weights() @ (base['beta'] * base['rho']**np.arange(target.horizon+1)) - target.direct_cost())
    seed = spec['pilot_seed'] if args.pilot else spec['seed']
    reps = 3 if args.pilot else spec['repetitions']
    cases = []
    start = time.perf_counter()
    with threadpool_limits(limits=1), Backend(1) as backend:
        for case_id, case in enumerate(spec['cases']):
            rows = []
            linked_spec = dict(observation, correct_pair_probability=case['probability'])
            for rep in range(reps):
                pilot = make_linked(base, linked_spec, spec['pilot_dates'], [seed, case_id, rep, 0])
                fitted = train_pilot(pilot, base['penalties'])
                data = make_linked(base, linked_spec, spec['dates'], [seed, case_id, rep, 1])
                rng = np.random.default_rng(np.random.SeedSequence([seed, case_id, rep, 2]))
                n = spec['audit_per_stratum']
                audit = rng.binomial(n, case['probability'])
                brief = DynamicBrief(target, 'registered_candidate_law', 'independent_pilot', 'independent_audit', int(2*spec['dates']**.2))
                projection = fit_linked(data, fitted, audit, [n, n], brief, backend, 'weak_linkage_projection', spec['alpha'])
                regular = linked_response(data, fitted, audit, [n, n], target, brief.bandwidth)
                regular = {key: value for key, value in regular.items() if key in ('status', 'financial_value', 'financial_se', 'financial_interval', 'audit_probability', 'audit_intervals')}
                rows.append({'rep': rep, 'audit_successes': audit, 'projection': projection, 'regular': regular})
                if not args.pilot and (rep+1) % 100 == 0:
                    print(json.dumps({'case': case['name'], 'completed': rep+1}), flush=True)
            summary = summarize(rows, truth)
            cases.append({'case': case, 'summary': summary, 'runs': rows})
            print(json.dumps({'case': case['name'], **summary}), flush=True)
    names = [str(path.relative_to(ROOT)), spec['funding_spec'], spec['observation_spec'],
             'tools/linkage_projection_study.py', 'tools/dynamic_observation_study.py',
             'src/causalbank/dynamic_product.py', 'src/causalbank/dynamic_validation.py',
             'src/causalbank/linkage_sets.py', 'src/causalbank/dynamic_funding.py',
             'src/causalbank/linked_observation.py', 'src/causalbank/responses.py']
    result = {'mode': 'pilot' if args.pilot else 'final', 'spec': spec, 'financial_truth': truth,
              'results': cases, 'seconds': time.perf_counter()-start,
              'input_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}}
    output = ROOT / ('docs/studies/linkage-projection-pilot.json' if args.pilot else 'docs/studies/linkage-projection-results.json')
    output.write_text(json.dumps(result, default=default, allow_nan=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
