#!/usr/bin/env python3
"""Reconstruct V10 saved requests and bind unchanged V9 receipts to its archive."""
import hashlib
import json
import zipfile

import numpy as np
from scipy.stats import binomtest

from precision_common import ROOT, SCIENCE_INPUTS, SPEC, digest, save, summary
from precision_interval_review import exact
from precision_workload_launcher import difference
from causalbank.dynamic_funding import FundingTarget


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads((ROOT / path).read_text())


def bound(path):
    receipt = read(path)
    require(receipt.get('status') == 'pass' and bool(receipt.get('input_sha256')),
            'Missing passing receipt: ' + path)
    for name, expected in receipt['input_sha256'].items():
        require(digest(name) == expected, 'Stale receipt input: ' + path + '/' + name)
    return receipt


def journal(path, expected_inputs):
    with (ROOT / path).open() as stream:
        header = json.loads(next(stream))
        require(header == {'input_sha256': {p: digest(p) for p in sorted(set(expected_inputs))}},
                'Journal code/input identity changed: ' + path)
        rows = {}
        for line in stream:
            row = json.loads(line)
            require(set(row) == {'key', 'result'} and row['key'] not in rows,
                    'Duplicate or malformed journal request: ' + path)
            rows[row['key']] = row['result']
    return rows


def study(name, spec, base):
    result_path = f'docs/studies/precision-{name}-results.json'
    receipt = bound(result_path)
    require(receipt['mode'] == name and receipt['status'] == 'pass', 'Wrong study mode')
    reps = spec['pilot_repetitions'] if name == 'pilot' else spec['repetitions']
    require(receipt['repetitions'] == reps and len(receipt['results']) == len(spec['designs']),
            'Incomplete study summary: ' + name)
    rows = journal(f'docs/studies/precision-{name}.jsonl', SCIENCE_INPUTS + ['tools/precision_study.py'])
    expected = {f'{design["name"]}/{i}' for design in spec['designs'] for i in range(reps)}
    require(set(rows) == expected, 'Missing, extra or duplicate study requests: ' + name)
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    for design, case in zip(spec['designs'], receipt['results']):
        require(case['design'] == design, 'Study design/order changed: ' + name)
        law = dict(base, rho=design.get('rho', base['rho']))
        truth = float(target.weights() @ (base['beta'] * law['rho'] ** np.arange(target.horizon + 1)) - target.direct_cost())
        require(case['truth'] == truth, 'Financial truth changed: ' + design['name'])
        subset = []
        for i in range(reps):
            row = rows[f'{design["name"]}/{i}']
            require(set(row['methods']) == set(spec['methods']), 'Study methods changed')
            require(row['pilot_dates'] == [m * design['dates'] for m in spec['pilot_multipliers']],
                    'Pilot history changed')
            require(len(row['audit_successes']) == 2 and
                    all(isinstance(x, int) and 0 <= x <= design['audit'] for x in row['audit_successes']),
                    'Invalid audit counts')
            subset.append(row)
        require(case['summary'] == summary(subset, truth), 'Study summary cannot be reconstructed: ' + design['name'])
    return len(rows)


def intervals(report):
    review = bound('docs/reviews/precision-interval-review.json')
    require(len(review['results']) == len(report['results']), 'Incomplete interval review')
    n = report['repetitions']
    for case, row in zip(report['results'], review['results']):
        require(row['design'] == case['design']['name'], 'Interval design changed')
        for method, values in case['summary']['methods'].items():
            observed = row['methods'][method]
            require(observed['exact_mc95'] == exact(values['covered'], n, .05), 'Ordinary exact bound changed')
            require(observed['exact_simultaneous_mc95'] == exact(values['covered'], n, .05/24),
                    'Simultaneous exact bound changed')
        for name, values in case['summary']['paired'].items():
            observed = row['paired'][name]
            g, l = values['gained'], values['lost']
            gain, loss = exact(g, n, .025), exact(l, n, .025)
            sg, sl = exact(g, n, .05/48), exact(l, n, .05/48)
            p = float(binomtest(g, g+l, .5).pvalue) if g+l else 1.
            require(observed == dict(
                coverage_difference=values['coverage_difference'],
                conservative_mc95=[gain[0]-loss[1], gain[1]-loss[0]],
                conservative_simultaneous_mc95=[sg[0]-sl[1], sg[1]-sl[0]],
                exact_equal_coverage_p=p, bonferroni_equal_coverage_p=min(1., 24*p),
                gained=g, lost=l), 'Paired interval cannot be reconstructed: ' + name)
    return 24


def workloads(spec):
    receipt = bound('docs/studies/precision-workloads-results.json')
    folder = 'docs/studies/precision-workload-runs'
    inputs = [SPEC, 'tools/precision_workload_launcher.py', 'tools/precision_workloads.py']
    metadata = {}
    for n in spec['workloads']['dates']:
        name = f'{folder}/input-{n}.json'
        item = read(name)
        require(item['dates'] == n and item['pilot_dates'] == n * spec['workloads']['pilot_multiple'],
                'Workload input dimensions changed')
        require(item['input_sha256'] == {p: digest(p) for p in item['input_sha256']},
                'Workload generation input changed')
        require(item['files'] == {p: digest(p) for p in item['files']}, 'Workload array changed')
        inputs.extend([name] + list(item['files']))
        metadata[n] = item
    rows = journal('docs/studies/precision-workloads.jsonl', inputs)
    expected_keys = {f'{n}/{i}/{a}' for n in spec['workloads']['dates']
                     for i in range(spec['workloads']['repeats']) for a in ('dense', 'streaming')}
    require(set(rows) == expected_keys and len(receipt['runs']) == len(rows), 'Incomplete workload journal')
    with (ROOT / 'docs/studies/precision-workloads.jsonl').open() as stream:
        next(stream)
        ordered = [json.loads(line)['result'] for line in stream]
    require(receipt['runs'] == ordered, 'Workload runs differ from journal')
    comparisons = []
    for n in spec['workloads']['dates']:
        for repeat in range(spec['workloads']['repeats']):
            pair = {a: rows[f'{n}/{repeat}/{a}'] for a in ('dense', 'streaming')}
            for algorithm, row in pair.items():
                path = f'{folder}/{algorithm}-{n}-{repeat}.json'
                require(row['output_path'] == path and digest(path) == row['output_sha256'],
                        'Workload output identity changed')
                saved = read(path)
                require(all(row[k] == value for k, value in saved.items()) and
                        row['input_files'] == metadata[n]['files'] and
                        row['algorithm'] == algorithm and row['dates'] == n and row['repeat'] == repeat,
                        'Workload output or routing changed')
                launcher = row['launcher']
                require(launcher['launcher_rss_bytes'] < 40*1024**2 and
                        abs(launcher['child_peak_rss_bytes'] - row['peak_rss_bytes']) < 2*1024**2 and
                        row['complete_seconds'] > 0 and row['peak_rss_bytes'] > 0 and
                        all(pool['num_threads'] == 1 for pool in row['numeric_threadpools']),
                        'Workload measurement qualification failed')
            error = difference(pair['dense']['result'], pair['streaming']['result'])
            require(error < 1e-9 and pair['dense']['result']['pilot_penalty'] ==
                    pair['streaming']['result']['pilot_penalty'], 'Workload outputs differ')
            comparisons.append(dict(dates=n, pilot_dates=n*spec['workloads']['pilot_multiple'],
                repeat=repeat, maximum_scaled_difference=error,
                memory_ratio=pair['streaming']['peak_rss_bytes']/pair['dense']['peak_rss_bytes'],
                time_ratio=pair['streaming']['complete_seconds']/pair['dense']['complete_seconds']))
    require(receipt['comparisons'] == comparisons, 'Workload ratios cannot be reconstructed')
    return len(rows), len(comparisons)


def historical_v9():
    preservation = read('docs/program/history/v9-preservation-receipt.json')
    require(preservation['status'] == 'pass' and preservation['version'] == '9.0', 'V9 preservation failed')
    archive_name = preservation['archive']
    require(digest(archive_name) == preservation['sha256'], 'V9 archive identity changed')
    names = ('docs/reviews/calibration-verification.json',
             'docs/reviews/calibration-exact-replay.json')
    with zipfile.ZipFile(ROOT / archive_name) as archive:
        raw = archive.read('docs/program/reconstruction-delivery-manifest.json')
        require(hashlib.sha256(raw).hexdigest() == preservation['manifest_sha256'], 'V9 manifest changed')
        manifest = json.loads(raw)
        artifacts = {row['path']: row['sha256'] for row in manifest['artifacts']}
        require(manifest['version'] == '9.0' and len(artifacts) == preservation['preserved_artifacts'],
                'V9 artifact count changed')
        members = set(archive.namelist())
        require(len(members) == preservation['archived_artifacts'] + 1,
                'V9 archived member count changed')
        for name in names:
            require(digest(name) == artifacts[name], 'Historical V9 receipt changed: ' + name)
            require(hashlib.sha256(archive.read(name)).hexdigest() == artifacts[name],
                    'Historical V9 receipt not preserved: ' + name)
            receipt = read(name)
            require(receipt['status'] == 'pass', 'Historical V9 check failed: ' + name)
            for path, expected in receipt['input_sha256'].items():
                require(artifacts.get(path) == expected, 'V9 input absent or differs from manifest: ' + path)
                if path in members and (not (ROOT / path).is_file() or digest(path) != expected):
                    require(hashlib.sha256(archive.read(path)).hexdigest() == expected,
                            'Historical V9 input differs in archive: ' + path)
                else:
                    require(digest(path) == expected, 'Historical V9 input unavailable: ' + path)
    return dict(archive=archive_name, sha256=preservation['sha256'], artifacts=len(artifacts),
                historical_receipts=list(names))


def main():
    spec = read(SPEC)
    base = read(spec['base'])
    counts = {name: study(name, spec, base) for name in ('pilot', 'final')}
    interval_cells = intervals(read('docs/studies/precision-final-results.json'))
    workload_requests, comparisons = workloads(spec)
    historical = historical_v9()
    bound('docs/reviews/precision-streaming-checks.json')
    bound('docs/reviews/precision-table-generation.json')
    inputs = [SPEC, 'tools/precision_verify.py', 'tools/precision_common.py',
              'tools/precision_study.py', 'tools/precision_workloads.py',
              'src/causalbank/streaming_pilot.py',
              'tools/precision_interval_review.py', 'tools/precision_workload_launcher.py',
              'docs/studies/precision-pilot.jsonl', 'docs/studies/precision-final.jsonl',
              'docs/studies/precision-workloads.jsonl',
              'docs/studies/precision-pilot-results.json', 'docs/studies/precision-final-results.json',
              'docs/studies/precision-workloads-results.json', 'docs/reviews/precision-interval-review.json',
              'docs/reviews/precision-streaming-checks.json', 'docs/reviews/precision-table-generation.json',
              'docs/program/history/v9-preservation-receipt.json', historical['archive']]
    inputs += historical['historical_receipts']
    # Historical receipt identity alone does not bind the live artifacts used
    # by inherited manuscript claims. Reuse only byte-identical V9 evidence;
    # a changed artifact must receive a new V10 qualification explicitly.
    claims_path = 'docs/literature/reconstruction-claims.json'
    claimed = {path for claim in read(claims_path) for path in claim.get('artifacts', [])}
    inherited_claims = sorted(claimed - set(inputs) - {'docs/reviews/precision-verification.json'})
    inherited_inputs = read('docs/reviews/calibration-verification.json')['input_sha256']
    for path in inherited_claims:
        require(path in inherited_inputs and digest(path) == inherited_inputs[path],
                'Inherited claim evidence changed or lacks V9 qualification: ' + path)
    inputs += inherited_claims + [claims_path]
    save('docs/reviews/precision-verification.json', dict(status='pass', issues=[],
         study_requests=counts, workload_requests=workload_requests,
         workload_comparisons=comparisons, exact_interval_cells=interval_cells,
         historical_v9=historical,
         unchanged_inherited_claim_artifacts=inherited_claims,
         scope='Saved V10 request, summary, interval and workload identity reconstruction; V9 historical receipts bound to preserved bytes. Does not rerun all Monte Carlo requests, establish bank validity or independently review the science.'), inputs)
    print(json.dumps(dict(status='pass', study_requests=counts,
                          workload_requests=workload_requests, historical_v9_artifacts=historical['artifacts'])))


if __name__ == '__main__':
    main()
