#!/usr/bin/env python3
"""Fresh isolated replay of the documented local CLI/library demonstrations."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
BASE = ROOT / 'docs/program/execution/2026-10-13/prototype-review'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'first', 'second', 'lifecycle', 'review', 'faults'])
    args = parser.parse_args()
    import interface_examples_20261013 as interfaces
    interfaces.BASE = BASE / 'runtime-replay'
    interfaces.OUT = interfaces.BASE / 'examples'
    interfaces.STATE = ROOT / '.runtime/q3-interface-replay-20261013'
    if args.stage == 'faults':
        import qualify_in04_v12 as qualification
        from causalbank.runtime_v12 import Runtime, execution_identity
        path = BASE / 'runtime-replay/faults.json'
        if path.exists():
            raise ValueError('Preserve prior fault receipt')
        state = ROOT / '.runtime/q3-fault-replay-20261013'
        if state.exists():
            raise ValueError('Fresh fault runtime required')
        runtime = Runtime(state)
        result = {'executed_at': datetime.now(timezone.utc).isoformat(),
                  'execution_identity': execution_identity(),
                  'source': interfaces.ref(Path(qualification.__file__), 'Preserved nine fault cases'),
                  'harness': interfaces.ref(Path(__file__), 'Isolated replay wrapper'),
                  'fresh_mcp_run': False}
        try:
            result.update(qualification.faults(runtime, qualification.cases(runtime)))
        except BaseException as exc:
            result.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
            path.with_suffix('.failure.txt').write_text(traceback.format_exc())
        interfaces.write(path, result)
        print(json.dumps({'status': result['status'], 'cases': len(result.get('cases', [])),
                          'error': result.get('error')}))
        return 0 if result['status'] == 'pass' else 1
    actions = {'prepare': interfaces.prepare, 'first': lambda: interfaces.run_cases(True),
               'second': lambda: interfaces.run_cases(False), 'lifecycle': interfaces.lifecycle,
               'review': interfaces.review}
    actions[args.stage]()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
