#!/usr/bin/env python3
"""Rerun inspected historical verifiers, redirecting only their known outputs."""
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

PROGRAMS = {
    'revision': ('verify_revision', ['docs/reviews/revision-verification.json']),
    'completion': ('verify_completion', ['docs/reviews/scientific-completion-verification.json']),
    'scope': ('verify_scope', ['docs/studies/scope-workload-summary.json', 'docs/reviews/scope-verification.json']),
    'dynamic': ('verify_dynamic', ['docs/reviews/dynamic-verification.json']),
    'linkage': ('verify_linkage', ['docs/reviews/linkage-verification.json']),
    'reliability': ('reliability_verify', ['docs/reviews/reliability-verification.json']),
    'calibration': ('calibration_verify', ['docs/reviews/calibration-verification.json']),
    'precision': ('precision_verify', ['docs/reviews/precision-verification.json']),
    'weak-audit': ('weak_audit_verify', ['docs/reviews/weak-audit-verification.json']),
    'weak-sharpening': ('weak_audit_sharpening_verify', ['docs/reviews/weak-audit-sharpening-verification.json']),
    'linked-funding': ('linked_funding_verify', ['docs/reviews/linked-funding-verification.json']),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', choices=PROGRAMS)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    module_name, outputs = PROGRAMS[args.program]
    module = importlib.import_module(module_name)
    from threadpoolctl import threadpool_limits
    mappings = {(ROOT / name).resolve(): out / Path(name).name for name in outputs}
    originals = {p: ref(p) for p in mappings}
    writes = []
    original_write = Path.write_text
    result = {'status': 'running', 'replay_executed_at': datetime.now(timezone.utc).isoformat(),
              'harness': ref(Path(__file__)), 'verifier': ref(Path(module.__file__)),
              'scope': 'Execute unchanged historical calculations and checks. Redirect known result writes only; original evidence remains read-only. Historical dates inside reproduced receipts are not this replay date.',
              'limits': ['Each historical verifier retains its stated scope; summary reconstruction is not full simulator or workload reexecution.'],
              'outputs': []}

    def redirected(path, data, *positional, **keywords):
        frozen = path.resolve()
        if frozen not in mappings:
            raise ValueError('Uninspected write_text target: ' + str(frozen))
        target = mappings[frozen]
        if target.exists():
            raise ValueError('Repeated verifier output: ' + str(target))
        count = original_write(target, data, *positional, **keywords)
        writes.append(frozen)
        return count

    try:
        with (out / 'execution.log').open('w') as log, contextlib.redirect_stdout(log), threadpool_limits(limits=1):
            Path.write_text = redirected
            try:
                code = module.main()
            except SystemExit as exit_status:
                code = exit_status.code
            finally:
                Path.write_text = original_write
            assert code in (None, 0), 'Verifier exit: ' + str(code)
        assert set(writes) == set(mappings), 'Not all expected outputs were reproduced'
        for original, computed in mappings.items():
            fresh = json.loads(computed.read_text())
            if 'status' in fresh:
                assert fresh['status'] == 'pass' and not fresh.get('issues'), str(fresh.get('issues'))[:1200]
            compare(fresh, json.loads(original.read_text()))
            result['outputs'].append({'frozen': originals[original], 'recomputed': ref(computed), 'comparison': 'pass'})
        result['status'] = 'pass'
    except Exception as exc:
        result.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
        (out / 'failure.txt').write_text(traceback.format_exc())
    finally:
        Path.write_text = original_write
    result['originals_unchanged'] = all(ref(p) == identity for p, identity in originals.items())
    if not result['originals_unchanged']:
        result['status'] = 'fail'
    (out / 'replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'program': args.program, 'status': result['status'],
                      'originals_unchanged': result['originals_unchanged'], 'error': result.get('error')}))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
