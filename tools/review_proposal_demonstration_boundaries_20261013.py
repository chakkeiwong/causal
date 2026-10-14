#!/usr/bin/env python3
"""Preserving Q3 follow-up: saved summaries, local engineering and boundaries."""
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-13/prototype-review'


def ref(path):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('group', choices=['summaries', 'engineering', 'servicing', 'boundaries'])
    args = parser.parse_args()
    out = BASE / ('followup-' + args.group)
    out.mkdir(exist_ok=False)
    originals = {}
    record = {'group': args.group, 'executed_at': datetime.now(timezone.utc).isoformat(),
              'harness': ref(Path(__file__)), 'evidence': [], 'checks': [], 'status': 'running'}

    def bind(path):
        path = Path(path)
        identity = ref(path)
        originals[path] = identity
        record['evidence'].append(identity)
        return identity

    try:
        from threadpoolctl import threadpool_limits
        from master_release_evidence import close
        if args.group == 'summaries':
            manuscript_path = ROOT / 'docs/program/repair-v12/integrated-reader/chapters/master_execution.tex'
            bind(manuscript_path)
            manuscript = manuscript_path.read_text()
            for folder in ['R01', 'R02', 'R03', 'R04-v3', 'R05-v2']:
                base = ROOT / 'docs/program/master/work' / folder
                specpath = base / 'protocol.json'
                protocol_ref = bind(specpath)
                spec = json.loads(specpath.read_text())
                frozen = json.loads((base / 'results.json').read_text())
                bind(base / 'results.json')
                bind(base / 'launch.json')
                summary_module = importlib.import_module(
                    'master_experiment_v2' if folder.startswith('R04') else 'master_experiment')
                bind(Path(summary_module.__file__))
                for path, expected in spec['input_sha256'].items():
                    assert ref(ROOT / path)['sha256'] == expected, ('registered input', path)
                rows, identities = [], {}
                for cell in range(len(spec['designs'])):
                    for index in range(spec['replications']):
                        key = f'{cell:02d}-{index:05d}'
                        path = base / 'requests' / (key + '.json')
                        identity = ref(path)
                        relative = identity['path']
                        assert frozen['request_sha256'][relative] == identity['sha256']
                        identities[relative] = identity['sha256']
                        row = json.loads(path.read_text())
                        assert (row['key'], row['cell'], row['index'], row['registration_sha256']) == (
                            key, cell, index, protocol_ref['sha256'])
                        rows.append(row)
                with threadpool_limits(limits=1):
                    fresh = summary_module.summary(rows, spec)
                fresh.update(launch=json.loads((base / 'launch.json').read_text()),
                             registration_sha256=protocol_ref['sha256'], request_sha256=identities)
                assert fresh == frozen, folder + ': full summary changed'
                tables = []
                for cell in fresh['cells']:
                    primary = cell['methods'][spec['methods'][0]]
                    challenger = cell['methods'][spec['methods'][1]]
                    median = '--' if primary['width_quantiles'] is None else (
                        f"{primary['width_quantiles'][1]:,.0f}" if folder[:3] in ['R01', 'R02', 'R03']
                        else f"{primary['width_quantiles'][1]:.3f}")
                    row = (f"{cell['design']['name'].replace('_', ' ')} & {primary['covered']}/512 & "
                           f"{primary['simultaneous_lower95']:.3f} & {primary['finite']}/512 & "
                           f"{median} & {challenger['covered']}/512")
                    assert row in manuscript, ('rendered source table row', row)
                    tables.append(row)
                destination = out / (folder + '-summary.json')
                save(destination, fresh)
                record['checks'].append({'study': folder, 'requests': len(rows),
                    'full_summary_exact': True, 'table_rows_verified': len(tables),
                    'recomputed': ref(destination), 'new_simulator_draws': 0})
                print(json.dumps(record['checks'][-1]), flush=True)
            record['limits'] = ['All saved requests and summary fields reconstructed; no new Monte Carlo draws or timing measurements. Fifteen fresh representative requests are recorded separately.']
        elif args.group == 'engineering':
            import master_e01_v2 as engine
            for path in [Path(engine.__file__), ROOT / 'docs/program/master/work/E01-v2/receipt.json']:
                bind(path)
            receipt = json.loads((ROOT / 'docs/program/master/work/E01-v2/receipt.json').read_text())
            for name, expected in receipt['input_sha256'].items():
                assert bind(ROOT / name)['sha256'] == expected
            frozen = {}
            for name in ['checks.json', 'workloads.json', 'recovery.json']:
                p = engine.FOLDER / name
                bind(p)
                frozen[name] = json.loads(p.read_text())
            engine.FOLDER = out
            sys.argv = [str(Path(engine.__file__))]
            with (out / 'execution.log').open('w') as log, contextlib.redirect_stdout(log), threadpool_limits(limits=1):
                engine.main()
            checks = json.loads((out / 'checks.json').read_text())
            assert close(checks, frozen['checks.json'])
            workloads = json.loads((out / 'workloads.json').read_text())
            assert len(workloads['rows']) == len(frozen['workloads.json']['rows']) == 6
            for new, old in zip(workloads['rows'], frozen['workloads.json']['rows']):
                for key in ['mode', 'origins', 'pilot_origins', 'estimate', 'standard_error', 'status']:
                    assert close(new[key], old[key]), ('workload scientific result', key)
            recovery = json.loads((out / 'recovery.json').read_text())
            assert close(recovery, frozen['recovery.json'])
            record['checks'] = [{'equivalence_cases': len(checks['cases']), 'workloads': 6,
                'real_faults': len(recovery['trials']), 'scientific_results_reproduced': True,
                'new_resource_measurements_equal_historical_measurements': False,
                'outputs': [ref(out / name) for name in frozen]}]
            record['limits'] = ['New local measurements are retained separately. Runtime/RSS are environment-specific observations, not deterministic claims or bank service levels.']
        elif args.group == 'servicing':
            import master_r03_postreview as servicing
            original = ROOT / 'docs/program/master/work/R03/postreview-checks.json'
            for path in [Path(servicing.__file__), original,
                         ROOT / 'src/causalbank/audited_policy_v11.py',
                         ROOT / 'docs/program/master/work/R03/protocol.json']:
                bind(path)

            def redirect(path, value):
                assert Path(path) == original.relative_to(ROOT)
                save(out / 'postreview-checks.json', value)

            servicing.atomic = redirect
            with (out / 'execution.log').open('w') as log, contextlib.redirect_stdout(log), threadpool_limits(limits=1):
                servicing.main()
            fresh = json.loads((out / 'postreview-checks.json').read_text())
            assert close(fresh, json.loads(original.read_text()))
            record['checks'] = [{'scenarios': len(fresh['values']), 'reproduced': True,
                'output': ref(out / 'postreview-checks.json')}]
            record['limits'] = ['Replays the explicitly post-evaluation numerical audit. It does not move its date before registration or certify uniform quadrature accuracy.']
        else:
            import build_integrated_monograph_v12 as book
            reader = ROOT / 'docs/causal_proposal_temporal_information_2026-10-13.pdf'
            record['reviewed_reader'] = bind(reader)
            bind(reader.with_suffix('.tex'))
            inventory = BASE / 'demonstration-inventory.json'
            bind(inventory)
            files = book.scan(reader.with_suffix('.tex'))
            labels = {}
            for path, content in files:
                for match in re.finditer(r'\\label\{([^}]+)\}', content):
                    labels.setdefault(match[1], []).append({'path': str(path.relative_to(ROOT)),
                        'line': content.count('\n', 0, match.start()) + 1})
            hints = []
            for row in json.loads(inventory.read_text())['additional_families']:
                for label in row['labels']:
                    hints.append({'family': row['id'], 'hint': label,
                                  'verified_locations': labels.get(label, []),
                                  'valid_hint': label in labels})
            record['label_hint_audit'] = hints
            record['actual_additional_anchors'] = {
                key: locations for key, locations in labels.items()
                if any(term in key for term in ['weak', 'linked', 'la05', 'in:runtime', 'pd15:portfolio'])}
            transport = ROOT / 'docs/program/repair-v12/work/IN04/transport-checks.json'
            bind(transport)
            d = json.loads(transport.read_text())
            for row in d['transcript']:
                structured = row['mcp']['structuredContent']
                texts = [json.loads(c['text']) for c in row['mcp']['content'] if c['type'] == 'text']
                assert row['library'] == row['cli'] == structured
                assert texts and all(t == structured for t in texts)
                assert row['equal'] and row['text_equal']
                record['checks'].append({'case': row['case'], 'stored_three_surface_equality': True,
                                         'fresh_mcp_execution': False})
            record['limits'] = ['Stored MCP payload equality was recomputed. The server was not rerun; the preserved SDK 1.27.0/local stdio/MCP 2025-11-25 and approved-environment limits remain. Label hints are navigation, not scientific evidence.']
        record['status'] = 'pass'
    except Exception as exc:
        record.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
        (out / 'failure.txt').write_text(traceback.format_exc())
    record['originals_unchanged'] = all(ref(path) == identity for path, identity in originals.items())
    if not record['originals_unchanged']:
        record['status'] = 'fail'
    save(out / 'receipt.json', record)
    print(json.dumps({'group': args.group, 'status': record['status'],
                      'checks': len(record['checks']), 'error': record.get('error')}))
    return 0 if record['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
