#!/usr/bin/env python3
"""Record the authorized continuation without overwriting completed history."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/program/state.json'
NAMES = ['Preserve and specify', 'Public inference semantics', 'Persistent audited histories',
         'Linkage precision and calibration', 'Nonlinear audited decisions',
         'Latent temporal effect sets', 'Dependent learning and restartable execution',
         'Reusable banking journeys', 'Scholarly review and inspected delivery']
DEPS = [[], ['C00'], ['C00','C01'], ['C00','C01','C02'], ['C00','C01'],
        ['C00','C01'], ['C02','C03','C04','C05'], ['C01','C06'], ['C07']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['activate','record'])
    parser.add_argument('--phase')
    parser.add_argument('--status', choices=['pending','in_progress','complete'])
    parser.add_argument('--evidence', nargs='*', default=[])
    parser.add_argument('--next-action')
    args = parser.parse_args()
    state = json.loads(PATH.read_text())
    if args.command == 'activate':
        if any(p['id'].startswith('C') for p in state['phases']):
            raise SystemExit('Already active')
        preservation = json.loads((ROOT/'docs/program/history/v6.1-preservation-receipt.json').read_text())
        assert preservation['status'] == 'pass'
        for phase in state['phases']:
            phase['status'] = 'historical'
        state['phases'] += [dict(id=f'C{i:02d}', name=name, depends=DEPS[i],
                                  status='in_progress' if i == 0 else 'pending',
                                  deliverable=name, evidence=[]) for i,name in enumerate(NAMES)]
        state.update(revision='7.0-gap-closure', updated='2026-10-10',
                     status='Authorized gap closure in progress; V6.1 preserved',
                     active_work_program='C00–C08; previous editions historical',
                     plan='docs/program/gap-closure-execution-2026-10-10.md',
                     gap_review='docs/reviews/remaining-gaps-v6.1-2026-10-09.md',
                     delivery_status='V6.1 frozen in history/v6.1-assessed-delivery.zip; current revision not yet delivered',
                     completion_scope='In progress. Scholarly completion and useful capability require separate evidence.',
                     next_action='Complete C00 scientific specifications and C01 public qualification repair.')
        state['boundaries'] = ['Current phase completion is distinct from supported useful capability.',
                               'Deferred research and external obligations are recorded in docs/program/deferred-gaps-2026-10-10.md.',
                               'No independent review, bank validation, deployment, accepted integration or user acceptance is claimed.']
    else:
        phase = next(p for p in state['phases'] if p['id'] == args.phase)
        if args.status == 'complete':
            assert args.evidence and all((ROOT/p).is_file() for p in args.evidence)
            assert all(next(p for p in state['phases'] if p['id']==d)['status']=='complete' for d in phase['depends'])
        phase.update(status=args.status, evidence=args.evidence)
        if args.next_action:
            state['next_action'] = args.next_action
    PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'status':state['status'], 'next_action':state['next_action']}))


if __name__ == '__main__':
    main()
