#!/usr/bin/env python3
"""Reproduce inherited proposal witnesses, selected study requests and profiles."""
import argparse
import contextlib
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from replay_proposal_demonstrations_20261013 import compare, ref


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('group', choices=['witnesses', 'studies', 'public-profile', 'agent'])
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    receipt = {'executed_at': datetime.now(timezone.utc).isoformat(), 'harness': ref(Path(__file__)),
               'group': args.group, 'status': 'running', 'evidence': [], 'checks': []}
    originals = {}

    def bind(path):
        binding = ref(path)
        originals[path] = binding
        receipt['evidence'].append(binding)

    def save():
        (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')

    try:
        if args.group == 'witnesses':
            import precision_exact_replay as old
            original = ROOT / 'docs/reconstruction/checks.json'
            bind(original)
            bind(ROOT / 'tools/reconstruction_checks.py')
            result = json.loads(json.dumps({k: f() for k, f in old.FUNCTIONS.items()}))
            compare(result, json.loads(original.read_text())['checks'])
            (out / 'recomputed.json').write_text(json.dumps(result, indent=2) + '\n')
            receipt['checks'] = [{'family': k, 'status': 'pass'} for k in result]
            receipt['scope'] = 'Eighteen finite witness families, not general theorem validation.'
        elif args.group == 'studies':
            from threadpoolctl import threadpool_limits
            import master_release_evidence as previous
            receipt['scope'] = 'First/middle/last requests in each of five frozen studies; not a rerun of every Monte Carlo request.'
            with threadpool_limits(limits=1):
                for folder in ['R01', 'R02', 'R03', 'R04-v3', 'R05-v2']:
                    base = ROOT / 'docs/program/master/work' / folder
                    bind(base / 'protocol.json')
                    bind(base / 'results.json')
                    spec = json.loads((base / 'protocol.json').read_text())
                    module = importlib.import_module(spec['module'])
                    bind(Path(module.__file__))
                    for cell, index in [(0, 0), (len(spec['designs']) // 2, 256), (len(spec['designs']) - 1, 511)]:
                        frozen = base / 'requests' / f'{cell:02d}-{index:05d}.json'
                        bind(frozen)
                        fresh = module.request(spec, cell, index)
                        target = out / f'{folder}-{cell:02d}-{index:05d}.json'
                        target.write_text(json.dumps(fresh, indent=2) + '\n')
                        assert previous.close(json.loads(frozen.read_text())['result'], fresh), (folder, cell, index)
                        receipt['checks'].append({'family': folder, 'cell': cell, 'index': index,
                                                  'status': 'pass', 'recomputed': ref(target)})
                        save()
                    print(json.dumps({'study': folder, 'regenerated': 3, 'status': 'pass'}), flush=True)
            receipt['tolerance'] = {'rtol': 1e-9, 'atol': 1e-7}
        elif args.group == 'public-profile':
            import profile_public_bank_data as profile
            original = ROOT / 'docs/program/public-data-v15/bank-profile.json'
            bind(original)
            bind(profile.ARCHIVE)
            bind(Path(profile.__file__))
            frozen = json.loads(original.read_text())
            for item in frozen['extracted_files']:
                bind(ROOT / item['path'])
            profile.BASE = out
            profile.OUT = out / 'extracted'
            with (out / 'execution.log').open('w') as log, contextlib.redirect_stdout(log):
                profile.main()
            computed = json.loads((out / 'bank-profile.json').read_text())
            # Relocation is the only intentional change in the file bindings.
            for row in computed['datasets']:
                name = Path(row['file']['path']).name
                oldrow = next(r for r in frozen['datasets'] if Path(r['file']['path']).name == name)
                assert row['file']['sha256'] == oldrow['file']['sha256']
                row['file']['path'] = oldrow['file']['path']
            for row in computed['extracted_files']:
                oldrow = next(r for r in frozen['extracted_files'] if Path(r['path']).name == Path(row['path']).name)
                assert row['sha256'] == oldrow['sha256']
                row['path'] = oldrow['path']
            compare(computed, frozen)
            receipt['checks'] = [{'file': Path(r['file']['path']).name, 'rows': r['rows'], 'status': 'pass'} for r in frozen['datasets']]
            receipt['scope'] = 'Fresh extraction and descriptive counts; no fitted causal study.'
        else:
            import run_la05_reference as reference
            original = reference.WORK / 'prototype-evidence.json'
            bind(original)
            bind(Path(reference.__file__))
            bind(ROOT / 'src/causalbank/agent_workflow_v12.py')
            bind(ROOT / 'docs/program/repair-v12/work/LA02/casebook.json')
            reference.WORK = out
            with (out / 'execution.log').open('w') as log, contextlib.redirect_stdout(log):
                reference.run()
            fresh = json.loads((out / 'prototype-evidence.json').read_text())
            frozen = json.loads(original.read_text())
            compare(fresh, frozen)
            receipt['checks'] = [{'case': r['case'], 'status': r['result']['status'], 'reproduced': True} for r in fresh['cases']]
            receipt['scope'] = 'Six authored offline cases with real local tools, replay and set preservation; zero live-model calls.'
        receipt['status'] = 'pass'
    except Exception as exc:
        receipt.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
        (out / 'failure.txt').write_text(traceback.format_exc())
    receipt['originals_unchanged'] = all(ref(p) == identity for p, identity in originals.items())
    if not receipt['originals_unchanged']:
        receipt['status'] = 'fail'
    save()
    print(json.dumps({'group': args.group, 'status': receipt['status'], 'checks': len(receipt['checks']),
                      'error': receipt.get('error'), 'originals_unchanged': receipt['originals_unchanged']}))
    return 0 if receipt['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
