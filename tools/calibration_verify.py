#!/usr/bin/env python3
"""Verify V9 saved evidence, summaries and preserved scientific bytes."""
import hashlib
import json
import zipfile
from importlib.metadata import version
import numpy as np
from calibration_common import ROOT, SPEC, summarize, save, digest
from calibration_workloads import difference
from causalbank.dynamic_funding import FundingTarget


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    issues = []
    inputs = {__file__.removeprefix(str(ROOT)+'/'), 'tools/calibration_common.py',
        'tools/closure_common.py', 'tools/reliability_common.py', SPEC,
        'docs/studies/calibration-followup-spec.json'}
    hashes = {}
    counts = {'final': {}, 'pilot': {}}
    spec = read(SPEC)
    follow_spec = read('docs/studies/calibration-followup-spec.json')

    def require(condition, message):
        if not condition:
            issues.append(message)

    def identity(path, expected, context):
        inputs.add(path)
        if path not in hashes:
            hashes[path] = digest(path)
        require(hashes[path] == expected, context+': changed '+path)

    def bind(path, passing=False):
        record = read(path)
        inputs.add(path)
        require(bool(record.get('input_sha256')), 'Unbound receipt: '+path)
        for name, expected in record.get('input_sha256', {}).items():
            identity(name, expected, path)
        if passing:
            require(record.get('status') == 'pass' and not record.get('issues'), 'Failed receipt: '+path)
            require(all(record.get('checks', {}).values()), 'Failed checks: '+path)
        return record

    def journal(name, expected, pilot=False):
        mode = 'pilot' if pilot else 'final'
        path = f'docs/studies/calibration-{name}-{mode}.jsonl'
        inputs.add(path)
        rows = {}
        with (ROOT/path).open() as stream:
            header = json.loads(next(stream))
            for name_in, value in header['input_sha256'].items():
                identity(name_in, value, path)
            for line in stream:
                row = json.loads(line)
                require(row['key'] not in rows, 'Duplicate journal key: '+path+'/'+row['key'])
                rows[row['key']] = row['result']
        require(len(rows) == expected, 'Wrong request count: '+path)
        counts[mode][name] = len(rows)
        report = f'docs/studies/calibration-{name}-'+('pilot' if pilot else 'results')+'.json'
        return rows, bind(report)

    base = read(spec['base'])
    inputs.add(spec['base'])
    target = FundingTarget(horizon=base['horizon'], branches=base['branches'])
    def truth(rho):
        return float(target.weights()@(base['beta']*rho**np.arange(target.horizon+1))-target.direct_cost())

    def replay(rows, prefix, reps, financial_truth, expected):
        subset = [rows[f'{prefix}/{i}'] for i in range(reps)]
        require(summarize(subset, financial_truth) == expected, 'Summary mismatch: '+prefix)
        return subset

    for pilot in (False, True):
        reps = spec['pilot_repetitions'] if pilot else spec['diagnostic_repetitions']
        rows, result = journal('diagnostics', reps*len(spec['diagnostics']['dates']), pilot)
        require(result['financial_truth'] == truth(base['rho']), 'Diagnostic truth mismatch')
        require([r['dates'] for r in result['results']] == spec['diagnostics']['dates'], 'Diagnostic designs changed')
        for case in result['results']:
            subset = replay(rows, 'T'+str(case['dates']), reps, result['financial_truth'], case['summary'])
            bias = {k: dict(mean=float(np.mean([r['conditional_pilot_bias'][k] for r in subset])),
                rms=float(np.sqrt(np.mean([r['conditional_pilot_bias'][k]**2 for r in subset]))))
                for k in subset[0]['conditional_pilot_bias']}
            require(bias == case['conditional_bias'], 'Conditional bias summary mismatch')

        reps = spec['pilot_repetitions'] if pilot else spec['validation_repetitions']
        rows, result = journal('validation', reps*len(spec['validation']), pilot)
        require([r['case'] for r in result['results']] == spec['validation'], 'Validation designs changed')
        for case in result['results']:
            law = case['case']
            require(case['financial_truth'] == truth(law.get('rho', base['rho'])), 'Validation truth mismatch')
            subset = replay(rows, law['name'], reps, case['financial_truth'], case['summary'])
            require(all(r['dense_comparison_error'] is None or r['dense_comparison_error'] < 1e-6
                        for r in subset), 'Dense witness failed: '+law['name'])

        reps = follow_spec['pilot_repetitions'] if pilot else follow_spec['repetitions']
        rows, result = journal('followup', reps*len(follow_spec['designs']), pilot)
        require([r['design'] for r in result['results']] == follow_spec['designs'], 'Follow-up designs changed')
        for case in result['results']:
            require(case['financial_truth'] == truth(base['rho']), 'Follow-up truth mismatch')
            subset = replay(rows, case['design']['name'], reps, case['financial_truth'], case['summary'])
            timing = {k: float(np.mean([r['fit_inference_seconds'][k] for r in subset]))
                      for k in subset[0]['fit_inference_seconds']}
            require(timing == case['mean_fit_inference_seconds'], 'Follow-up time summary mismatch')
            require(case['pilot_history_multiplier'] == 4*case['design']['dates']/case['design']['old_pilot_dates'],
                    'Follow-up information cost changed')
        if not pilot:
            follow_rows, follow_result = rows, result

    # These are two sets of the same workload, not independent statistical draws.
    for name in ('workloads', 'workload-remeasurement'):
        rows, result = journal(name, 8)
        require(result['status'] == 'pass', 'Incomplete workload receipt')
        require(result['runs'] == list(rows.values()), 'Workload runs differ from journal')
        comparisons = []
        for n in spec['workloads']['dates']:
            metadata_path = f'docs/studies/calibration-workload-runs/input-{n}.json'
            metadata = bind(metadata_path)
            identity(metadata['path'], metadata['sha256'], 'Workload data')
            for repeat in range(spec['workloads']['repeats']):
                pair = {a: rows[f'{n}/{repeat}/{a}'] for a in ('dense', 'chunked')}
                for algorithm, row in pair.items():
                    identity(row['output_path'], row['output_sha256'], 'Workload output')
                    persisted = read(row['output_path'])
                    require(all(row[k] == v for k, v in persisted.items()), 'Output fields changed')
                    require(row['input_sha256'] == metadata['sha256'], 'Different workload input')
                    require(row['algorithm'] == algorithm and row['dates'] == n and row['repeat'] == repeat,
                            'Workload routing mismatch')
                    require(row['complete_process_seconds'] > 0 and row['peak_rss_bytes'] > 0 and
                        all(p['num_threads'] == 1 for p in row['numeric_threadpools']), 'Workload cost/thread check')
                    if name == 'workload-remeasurement':
                        launcher = row['launcher']
                        require(launcher['launcher_rss_before_worker_bytes'] < 40*1024**2 and
                            abs(launcher['child_peak_rss_bytes']-row['peak_rss_bytes']) < 2*1024**2,
                            'Unqualified RSS measurement')
                error = difference(pair['dense']['result'], pair['chunked']['result'])
                require(error < 1e-9, 'Workload numerical mismatch')
                comparisons.append(dict(dates=n, repeat=repeat, maximum_relative_difference=error,
                    chunked_to_dense_peak_rss=pair['chunked']['peak_rss_bytes']/pair['dense']['peak_rss_bytes'],
                    chunked_to_dense_complete_seconds=pair['chunked']['complete_process_seconds']/pair['dense']['complete_process_seconds']))
        require(comparisons == result['comparisons'], 'Workload summary mismatch: '+name)

    receipts = ['docs/reviews/calibration-independent-checks.json',
        'docs/reviews/calibration-followup-checks.json', 'docs/reviews/calibration-local-rehearsal.json',
        'docs/reviews/calibration-recovery-rehearsal.json', 'docs/reviews/calibration-table-generation.json',
        'docs/literature/calibration-source-review.json', 'docs/reviews/calibration-exact-replay.json']
    bound = {p: bind(p, True) for p in receipts}
    pairs = []
    for case in follow_result['results']:
        subset = [follow_rows[f'{case["design"]["name"]}/{i}'] for i in range(follow_spec['repetitions'])]
        for method in ('fourfold_pilot_bartlett', 'fourfold_pilot_innovation_horizon'):
            def covers(row, name):
                value = row['methods'][name]
                return int(value['status'] == 'computed' and value['interval'][0] <= case['financial_truth'] <= value['interval'][1])
            changes = np.array([covers(row, method)-covers(row, 'inherited_pilot_bartlett') for row in subset])
            error = changes.std(ddof=1)/np.sqrt(len(changes))
            pairs.append(dict(design=case['design']['name'], method=method,
                paired_coverage_difference=float(changes.mean()), new_only=int(np.sum(changes == 1)),
                old_only=int(np.sum(changes == -1)),
                approximate_mc95=[float(changes.mean()-1.96*error), float(changes.mean()+1.96*error)]))
    require(pairs == bound['docs/reviews/calibration-table-generation.json']['paired_followup'], 'Paired comparison mismatch')

    preservation_path = 'docs/program/history/v8-preservation-receipt.json'
    preserved = read(preservation_path)
    inputs.add(preservation_path)
    identity(preserved['archive'], preserved['sha256'], 'V8 archive')
    with zipfile.ZipFile(ROOT/preserved['archive']) as archive:
        manifest_bytes = archive.read('docs/program/reconstruction-delivery-manifest.json')
    require(hashlib.sha256(manifest_bytes).hexdigest() == preserved['manifest_sha256'], 'V8 manifest changed')
    manifest = json.loads(manifest_bytes)
    require(manifest['version'] == '8.0' and len(manifest['artifacts']) == preserved['preserved_artifacts'], 'Wrong V8 preservation')
    originals = {r['path']: r['sha256'] for r in manifest['artifacts']}
    inherited = []
    claims = read('docs/literature/reconstruction-claims.json')
    for claim in claims:
        for path in claim.get('artifacts', []):
            inputs.add(path)
            if not claim['id'].startswith('F-R'):
                require(path in originals, 'Inherited artifact absent from V8: '+path)
                if path in originals:
                    identity(path, originals[path], 'Inherited scientific evidence')
                    inherited.append(dict(claim=claim['id'], path=path, unchanged_v8=hashes[path] == originals[path]))
    old_path = 'docs/reviews/reliability-verification.json'
    identity(old_path, originals[old_path], 'Historical V8 verification')
    editorial = {'docs/causal_foundations.tex', 'docs/sponsor_reconstruction.tex', 'docs/literature/reconstruction-claims.json'}
    for path, expected in read(old_path)['input_sha256'].items():
        if path not in editorial:
            identity(path, expected, 'Inherited V8 verification input')
    inputs.update(['docs/literature/reconstruction-claims.json', 'docs/literature/sources.json',
        'docs/reconstruction/23_calibration.tex', 'contracts/calibrated-funding.md',
        'docs/program/external-validation-v9.md'])
    result = dict(status='pass' if not issues else 'fail', issues=issues,
        verified_journal_requests=sum(counts['final'].values()), pilot_requests=sum(counts['pilot'].values()),
        journal_counts=counts, inherited_artifacts=inherited,
        runtime_versions_observed={name: version(name) for name in ('numpy','scipy','jax','jaxlib','scikit-learn','threadpoolctl')},
        workload_disposition='Original eight requests retain inherited-RSS contamination; corrected eight requests alone support the new RSS comparison.',
        scope='Current code/input identities, saved journal reconstruction, paired summaries, workload outputs and inherited scientific bytes; not independent review, bank validity, universal calibration or 7016 independent method replications.')
    save('docs/reviews/calibration-verification.json', result, sorted(inputs))
    print(json.dumps({k: result[k] for k in ('status','issues','verified_journal_requests','pilot_requests','journal_counts')}))
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
