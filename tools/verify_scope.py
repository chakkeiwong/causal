#!/usr/bin/env python3
"""Reconstruct scope-study summaries and bind execution evidence without promoting validity."""
import hashlib
import json
import math
from pathlib import Path
import statistics
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text())


def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main():
    issues, inputs, verified, reconstructed = [], {}, [], {}

    def require(condition, message):
        if not condition:
            issues.append(message)

    def close(actual, expected, label, tolerance=1e-10):
        require(math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), label)

    def bind(name):
        path = ROOT / name
        require(path.is_file(), 'Missing artifact: ' + name)
        if path.is_file():
            inputs[name] = sha(name)

    names = ['inference', 'latent', 'discovery', 'organization', 'public',
             'history', 'latent-bootstrap', 'continuous', 'graph-effect', 'workload']
    data = {}
    for name in names:
        path = f'docs/studies/scope-{name}-results.json'
        receipt = read(path)
        data[name] = receipt
        bind(path)
        require(receipt.get('status', 'pass') == 'pass', 'Failed execution receipt: ' + name)
        require(receipt.get('mode', 'final') == 'final', 'Pilot substituted: ' + name)
        require(bool(receipt.get('input_sha256')), 'Missing input identities: ' + name)
        for source, expected in receipt.get('input_sha256', {}).items():
            bind(source)
            require(inputs.get(source) == expected, f'Stale {name} input: {source}')
        runtime = receipt.get('runtime', {})
        artifacts = runtime.get('artifacts', []) if isinstance(runtime, dict) else [a for r in runtime for a in r['artifacts']]
        for artifact in artifacts:
            bind(artifact['path'])
            require(inputs.get(artifact['path']) == artifact['sha256'], 'Changed installed source copy')
        verified.append({'path': path, 'sha256': sha(path), 'scope': receipt['scope']})

    for name in ['scope-scientific-checks', 'scope-workflow-checks']:
        path = f'docs/reviews/{name}.json'
        receipt = read(path)
        bind(path)
        require(receipt['status'] == 'pass', 'Failed scientific check: ' + name)
        for source, expected in receipt['input_sha256'].items():
            bind(source)
            require(inputs.get(source) == expected, f'Stale {name} input: {source}')
        for key, error in receipt.get('errors', {}).items():
            require(error < receipt['tolerances'][key], 'Failed numerical tolerance: ' + key)
        require(all(receipt.get('checks', {}).values()), 'Failed semantic identity: ' + name)
        verified.append({'path': path, 'sha256': sha(path), 'scope': receipt['scope']})

    # Reconstruct all requested-denominator coverages from retained fitted runs.
    latent = []
    for case in data['latent']['results']:
        runs, summary = case['runs'], case['summary']
        n, truth = summary['requested'], summary['truth']
        require(n == data['latent']['spec']['repetitions'] == len(runs), 'Latent repetition count')
        valid = [r['fit']['optimizer_success'] and not r['fit']['on_boundary']
                 and r['information']['available'] for r in runs]
        require(sum(not x for x in valid) == summary['fit_failures'], 'Latent failure denominator')
        close(statistics.mean(r['estimate']-truth for r in runs), summary['bias'], 'Latent bias')
        for key, coverage in summary['coverage'].items():
            count = sum(ok and abs(r['estimate']-truth) <= 1.959963984540054*r['information'].get(key, 0)
                        for r, ok in zip(runs, valid))
            close(count/n, coverage, 'Latent coverage: ' + key)
        close(statistics.mean(r['omitted_logger']['estimate']-truth for r in runs if 'omitted_logger' in r),
              summary['omitted_logger_bias'], 'Omitted logger bias')
        latent.append(summary)
    reconstructed['finite_latent'] = latent

    continuous = data['continuous']
    require(continuous['checks']['joint_gaussian_likelihood'] < 1e-8
            and continuous['checks']['analytic_score'] < 1e-6, 'Gaussian likelihood/score comparison')
    truth, runs, summary = continuous['summary']['truth'], continuous['runs'], continuous['summary']
    require(len(runs) == continuous['spec']['repetitions'], 'Continuous repetition count')
    close(statistics.mean(r['value']-truth for r in runs), summary['bias'], 'Continuous bias')
    close(sum(r['numerically_usable'] and abs(r['value']-truth) <= 1.959963984540054*r['information'].get('se', 0)
              for r in runs)/len(runs), summary['coverage'], 'Continuous coverage')
    close(statistics.mean(r['omitted_value']-truth for r in runs), summary['omitted_logger_bias'], 'Continuous omitted bias')
    require(sum(not r['numerically_usable'] for r in runs) == summary['unusable'], 'Continuous failure count')
    reconstructed['continuous'] = summary

    history = data['history']
    truth = history['truth']['contrast']
    for case in history['results']:
        require(len(case['runs']) == history['spec']['repetitions'], 'History repetition count')
        for key, summary in case['summary'].items():
            fitted = [r[key]['result'] for r in case['runs']]
            close(statistics.mean(r['estimate']-truth for r in fitted), summary['bias'], 'History bias')
            close(math.sqrt(statistics.mean((r['estimate']-truth)**2 for r in fitted)), summary['rmse'], 'History RMSE')
            close(statistics.mean(r['interval'][0] <= truth <= r['interval'][1] for r in fitted), summary['coverage'], 'History coverage')
            close(statistics.mean(math.sqrt(r['variance']) for r in fitted), summary['mean_se'], 'History mean SE')
        reconstructed['history_' + case['case']] = case['summary']

    bootstrap = data['latent-bootstrap']
    values = [r['estimate'] for r in bootstrap['refits'] if r['diagnostics']['optimizer_success']
              and not r['diagnostics']['on_boundary']]
    summary = bootstrap['summary']
    require(len(bootstrap['refits']) == bootstrap['spec']['bootstrap_refits'] == summary['requested_refits'], 'Bootstrap count')
    require(len(values) == summary['usable_refits'], 'Bootstrap usable count')
    require(len(bootstrap['refits'])-len(values) == summary['failures'], 'Bootstrap failure count')
    close(statistics.stdev(values), summary['bootstrap_se'], 'Bootstrap conditional standard deviation')
    if summary['failures']/summary['requested_refits'] >= .05:
        require('percentile_interval' not in summary and 'basic_interval' not in summary
                and summary.get('interval_status', '').startswith('unavailable'), 'Invalid bootstrap interval released')
    reconstructed['bootstrap'] = summary

    # Independent structural adjacency list, including truth beyond a searched window.
    truth_edges = {(i, i, 1) for i in range(6)} | {(1, 2, 1), (3, 4, 1), (4, 5, 1), (2, 5, 2),
                    (0, 1, 0), (1, 0, 0), (2, 3, 0), (3, 2, 0)}
    discovery_summary = []
    for case in data['discovery']['results']:
        require(len(case['runs']) == 2*data['discovery']['spec']['repetitions'], 'Discovery run count')
        for run in case['runs']:
            graph = np.asarray(run['graph'])
            selected = {tuple(int(v) for v in row) for row in np.argwhere(graph != '')}
            found = len(selected & truth_edges)
            close(found/max(len(selected), 1), run['adjacency_precision'], 'Discovery precision')
            close(found/len(truth_edges), run['adjacency_recall'], 'Discovery recall includes omitted lags')
            require(graph.shape == (6, 6, run['lag']+1), 'Discovery endpoint dimensions')
        for method in ['PCMCI+', 'LPCMCI']:
            rows = [r for r in case['runs'] if r['method'] == method]
            discovery_summary.append({'case': case['case'], 'method': method,
                'precision': statistics.mean(r['adjacency_precision'] for r in rows),
                'recall': statistics.mean(r['adjacency_recall'] for r in rows)})
    reconstructed['discovery_descriptive_adjacency'] = discovery_summary

    for case in data['organization']['results']:
        runs = case['runs']
        require(len(runs) == data['organization']['spec']['repetitions'], 'Organization repetition count')
        for field, raw in [('oracle_retention', 'oracle_retained'), ('resolved_fraction', 'resolved'),
                           ('wrong_acceptance', 'wrong_acceptance')]:
            close(statistics.mean(r[raw] for r in runs), case[field], 'Organization ' + field)
        close(statistics.mean(len(r['questions']) for r in runs), case['mean_questions'], 'Question count')
        if case['case'] == 'third_key_required':
            require(all(r['initial_status'] == 'incompatible' and not r['resolved'] for r in runs), 'Unsupported key accepted')

    # These older experiment receipts preserve aggregate counters, not every run.
    # Validate count arithmetic but do not pretend this recomputes simulations.
    inference = data['inference']
    def check_counts(node):
        if isinstance(node, dict):
            if {'coverage', 'requested', 'mc_se'} <= node.keys():
                p, n = node['coverage'], node['requested']
                require(n == inference['spec']['repetitions'] and 0 <= p <= 1, 'Inference coverage/count')
                close(p*n, round(p*n), 'Inference integer counter')
                close(math.sqrt(p*(1-p)/n), node['mc_se'], 'Inference Monte Carlo standard error')
            for value in node.values():
                check_counts(value)
        elif isinstance(node, list):
            for value in node:
                check_counts(value)
    check_counts(inference['results'])
    for result in data['organization']['linkage'].values():
        p, n = result['coverage'], data['organization']['spec']['linkage']['repetitions']
        require(0 <= p <= 1, 'Linkage coverage range')
        close(p*n, round(p*n), 'Linkage integer counter')
    reconstructed['aggregate_receipt_limits'] = (
        'Inference and linkage summaries retain seeds, generators, specifications and aggregate metrics; '
        'this verifier checks their count arithmetic and unchanged inputs, not a full simulation replay.')

    public = data['public']
    require(public['data_rows'] == public['original_rows'] == 9915, 'Public sample changed')
    require(len(public['results']) == 6, 'Public learner/split count')
    for run in public['results']:
        error = run['matched_doubleml_error']
        require(error['coefficient'] < 1e-9 and error['standard_error'] < 1e-9, 'Matched package disagreement')
        close(run['eligibility_ate']['estimate']/run['participation_late']['denominator'],
              run['participation_late']['estimate'], 'Composed public ratio')
    reconstructed['public_ranges'] = {key: [min(r[key]['estimate'] for r in public['results']),
                                          max(r[key]['estimate'] for r in public['results'])]
                                      for key in ['eligibility_ate', 'participation_late']}

    effects = data['graph-effect']
    for query in effects['queries']:
        result = query['result']
        if result['status'] == 'conditional_structural_effect_set':
            curves = np.array(result['curves'])
            require(np.allclose(np.column_stack((curves.min(0), curves.max(0))), result['pointwise_envelope']),
                    'Effect envelope reconstruction')
            require('No confidence claim' in result['inference'], 'Conditional envelope promoted to confidence')
        if query['case'] == 'hidden_common':
            require(result['status'] == 'unsupported_latent_effect_query', 'Hidden case silently promoted')

    workload = data['workload']
    summaries = []
    require(len(workload['runs']) == len(workload['spec']['cases'])*workload['spec']['repeats'], 'Workload process count')
    for case in workload['spec']['cases']:
        rows = [r for r in workload['runs'] if r['case'] == case['id']]
        require(len(rows) == workload['spec']['repeats'] == 2, 'Workload repeats')
        values = []
        for row in rows:
            require(row['exit_code'] == 0 and inputs.get(row['path']) == row['sha256'], 'Workload output identity')
            value = read(row['path'])
            values.append(value)
            require(value['case'] == case, 'Workload dimensions differ')
            require(bool(value['threadpools']) and all(p['num_threads'] == 1 for p in value['threadpools']), 'Thread limit not observed')
            require(sum(value['stages'].values()) < row['process_seconds'] and value['peak_rss_mib'] > 0,
                    'Invalid workload resource accounting')
            if case['kind'] == 'latent':
                require(value['fit']['optimizer_success'] and not value['fit']['on_boundary']
                        and value['information']['available'], 'Main workload latent numerical issue')
                require(len(value['refits']) == case['refits'] == 3, 'Refit workload count')
                require(all(r['diagnostics']['optimizer_success'] and not r['diagnostics']['on_boundary']
                            for r in value['refits']), 'Refit workload numerical issue')
        summaries.append({'case': case, 'process_seconds_range': [min(r['process_seconds'] for r in rows), max(r['process_seconds'] for r in rows)],
            'rss_mib_range': [min(v['peak_rss_mib'] for v in values), max(v['peak_rss_mib'] for v in values)],
            'stage_seconds_ranges': {key: [min(v['stages'][key] for v in values), max(v['stages'][key] for v in values)] for key in values[0]['stages']}})
    summary_path = 'docs/studies/scope-workload-summary.json'
    (ROOT / summary_path).write_text(json.dumps({'host': workload['host'], 'cases': summaries,
        'source_sha256': sha('docs/studies/scope-workload-results.json'),
        'scope': 'Two separately seeded fresh processes per case; one numerical thread. Cost measurement, not coverage, distributed performance or expert labor comparison.'}, indent=2)+'\n')
    bind(summary_path)
    bind(str(Path(__file__).relative_to(ROOT)))
    result = {'status': 'pass' if not issues else 'fail', 'date': '2026-10-09', 'issues': issues,
        'verified_receipts': verified, 'reconstructed': reconstructed, 'input_sha256': inputs,
        'scope': 'Study/input/source-copy identity, reconstructed fitted-run summaries, denominator and workload checks. Adverse findings remain evidence. Not general proof validation, independent review or bank qualification.'}
    (ROOT / 'docs/reviews/scope-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'bound_inputs': len(inputs), 'issues': issues}, indent=2))
    return bool(issues)


if __name__ == '__main__':
    raise SystemExit(main())
