#!/usr/bin/env python3
"""Reconstruct and challenge the saved weak-audit request identities and sets."""
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.dynamic_funding import FundingTarget
from causalbank.linkage_sets import decode_set, pair_projection, weighted_sum
from causalbank.weak_audit_projection import audit_interval

SPEC = 'docs/studies/weak-audit-projection-spec.json'
JOURNAL = 'docs/studies/weak-audit-projection-final.jsonl'
RESULT = 'docs/studies/weak-audit-projection-results.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def same_pieces(actual, expected):
    return len(actual) == len(expected) and all(
        (a == b and c == d) or
        (math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-6) and
         math.isclose(c, d, rel_tol=1e-11, abs_tol=1e-6))
        for (a, c), (b, d) in zip(actual, expected))


def main():
    spec, study = read(SPEC), read(RESULT)
    require(study['status'] == 'pass' and study['requests'] == 3000,
            'Incomplete study result')
    for name, expected in study['input_sha256'].items():
        require(digest(name) == expected, 'Changed study input: ' + name)
    prior = read('docs/reviews/weak-audit-projection-checks.json')
    source = read('docs/reviews/weak-audit-source-review.json')
    table = read('docs/reviews/weak-audit-table-generation.json')
    for receipt in (prior, source, table):
        require(receipt['status'] == 'pass' and
                all(digest(name) == expected for name, expected in receipt['input_sha256'].items()),
                'Stale prior receipt')

    base = read(spec['base'])
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    z = norm.ppf(1 - spec['response_error_total'] / 8)
    design_rows = {design['name']: [] for design in spec['designs']}
    seen = set()
    with (ROOT / JOURNAL).open() as stream:
        header = json.loads(next(stream))
        require(header == {'input_sha256': {k: v for k, v in study['input_sha256'].items() if k != JOURNAL}},
                'Changed journal header')
        for line in stream:
            row = json.loads(line)
            key = row['key']
            require(key not in seen, 'Duplicate request: ' + key)
            seen.add(key)
            design, index = key.split('/')
            require(design in design_rows and 0 <= int(index) < spec['repetitions'],
                    'Unregistered request: ' + key)
            design_rows[design].append(row['result'])
    require(len(seen) == 3000 and all(len(rows) == 600 for rows in design_rows.values()),
            'Missing final requests')

    penalties_matched = 0
    whole = 0
    for item in study['results']:
        design = item['design']
        rows = design_rows[design['name']]
        coverage = {'pilot4_horizon': 0, 'weak_audit_projection': 0}
        finite = 0
        for row in rows:
            regular = row['methods']['pilot4_horizon']
            projected = row['methods']['weak_audit_projection']
            require(projected['status'] == 'computed_set',
                    'Unreviewed projection failure')
            require(regular['status'] in ('computed', 'unavailable_mapping_rank'),
                    'Unreviewed regular failure')
            if regular['status'] == 'computed':
                require(regular['pilot_penalty'] == projected['pilot_penalty'],
                        'Compared procedures changed the pilot fit')
                penalties_matched += 1
                if regular['interval'][0] <= item['truth'] <= regular['interval'][1]:
                    coverage['pilot4_horizon'] += 1
            means = np.asarray(projected['candidate_financial_means']).reshape(2, 2)
            variances = np.asarray(projected['candidate_financial_variances']).reshape(2, 2)
            require(np.isfinite(variances).all() and np.all(variances > 0),
                    'Invalid primitive response uncertainty')
            bounds = np.stack((means - z * np.sqrt(variances),
                               means + z * np.sqrt(variances)), axis=-1)
            require(np.allclose(bounds, projected['candidate_bands'], rtol=1e-12, atol=1e-6),
                    'Changed primitive bands')
            audit = [audit_interval(int(k), design['audit'], spec['audit_error_total'] / 2)
                     for k in row['audit_successes']]
            require(np.allclose(audit, projected['audit_intervals'], rtol=0, atol=1e-14),
                    'Changed exact audit intervals')
            parts = [pair_projection(bounds[s, 0], bounds[s, 1], audit[s]) for s in (0, 1)]
            for actual, expected in zip(projected['stratum_sets'], parts):
                require(same_pieces(decode_set(actual), expected), 'Changed stratum projection')
            expected = weighted_sum(parts, [.5, .5], -target.direct_cost())
            actual = decode_set(projected['financial_set'])
            require(same_pieces(actual, expected), 'Changed financial projection')
            require(actual and all(lo <= hi for lo, hi in actual),
                    'Empty or reversed financial set')
            if any(lo <= item['truth'] <= hi for lo, hi in actual):
                coverage['weak_audit_projection'] += 1
            finite += int(all(math.isfinite(lo) and math.isfinite(hi) for lo, hi in actual))
            whole += int(actual == [(-math.inf, math.inf)])
        for name in spec['methods']:
            require(coverage[name] == item['summary']['methods'][name]['covered'],
                    'Coverage count mismatch: ' + design['name'] + '/' + name)
        require(finite == item['summary']['methods']['weak_audit_projection']['finite'],
                'Finite-set count mismatch')

    inputs = [SPEC, JOURNAL, RESULT,
              'tools/weak_audit_verify.py', 'tools/weak_audit_study.py',
              'src/causalbank/weak_audit_projection.py',
              'src/causalbank/linkage_sets.py',
              'docs/reviews/weak-audit-projection-checks.json',
              'docs/reviews/weak-audit-source-review.json',
              'docs/reviews/weak-audit-table-generation.json',
              'docs/supplements/weak-audit-table.tex']
    receipt = dict(status='pass', date='2026-10-11', issues=[],
                   requests=len(seen), compared_pilot_penalties=penalties_matched,
                   whole_line_sets=whole,
                   scope='Exact reconstruction of saved request identities, primitive bands, audit intervals, projections and coverage counts; not external or bank validation.',
                   input_sha256={name: digest(name) for name in sorted(inputs)})
    (ROOT / 'docs/reviews/weak-audit-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Supplement verification: {len(seen)} requests, {penalties_matched} matching available pilot fits, {whole} whole-line sets.')


if __name__ == '__main__':
    main()
