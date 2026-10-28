"""Keep unresolved proposal work visible after a finite packet ends."""
import argparse
import json
from pathlib import Path

import run_followup_program_20261028 as engine
from run_followup_program_v2_20261028 import selected

ROOT = engine.ROOT
POINTER = Path('docs/program/execution/continuation-current.json')
CONTROLLER = 'python3 tools/run_followup_program_v3_20261028.py'


def action_for(row):
    return row.get('corrected_continuation') or row.get('resolved_action') or row['action']


def route(batch, rows, holds, preferred=None):
    """Offer preparation without bypassing canonical acceptance prerequisites."""
    unresolved = [r for r in rows if r['status'] != 'pass']
    ids = [r['id'] for r in unresolved]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate continuation obligation')
    if set(holds) - set(ids):
        raise ValueError('Hold refers to an unknown unresolved obligation')
    for key, hold in holds.items():
        if not all(hold.get(k) for k in ('reason', 'revisit_trigger', 'next_action')):
            raise ValueError('Incomplete local hold: ' + key)
    eligible = [r for r in unresolved if r['lane'] not in ('release', 'proposal_acceptance')
                and not r.get('requires_inputs') and r['id'] not in holds]
    eligible.sort(key=lambda r: (r['id'] != preferred, ids.index(r['id'])))
    result = dict(batch)
    result.update(controller=CONTROLLER, unresolved_obligations=len(unresolved),
                  packet_exhausted=batch.get('next') is None,
                  preparation_candidates=len(eligible),
                  proposal_complete=False, final_acceptance=False,
                  local_holds=sorted(holds), background_worker_running=False)
    if batch.get('next') is not None:
        result['next_kind'] = 'registered_packet'
        return result
    result['ready'] = []
    result['preparation_candidate_ids'] = [r['id'] for r in eligible]
    if eligible:
        row = eligible[0]
        result.update(next=row['id'], next_action=action_for(row),
                      next_kind='successor_preparation', continue_work=True,
                      acceptance_prerequisites=row.get('prerequisites', []),
                      instruction='Prepare a bounded reviewed successor using the exact action basis; preserve prior outcomes. Preparation does not bypass acceptance prerequisites or authorize a native trial.')
    else:
        result.update(next=None, next_action=None, next_kind='no_local_preparation',
                      continue_work=False, unresolved_requires_action=bool(unresolved))
    return result


def current(root=ROOT):
    pointer = json.loads((root / POINTER).read_text())
    for key in ('manifest', 'review'):
        engine.bound(root, pointer[key])
    manifest = json.loads((root / pointer['manifest']['path']).read_text())
    for binding in manifest['evidence']:
        engine.bound(root, binding)
    state = json.loads((root / 'docs/program/state.json').read_text())
    if state['reader']['sha256'] != manifest['reader']['sha256']:
        raise ValueError('Continuation reader changed; refresh the reviewed manifest')
    results = dict(state['execution_program']['results'])
    results.update(state['execution_runtime']['results'])
    for row in manifest['operations']:
        if results.get(row['id'], {}).get('outcome', 'open') != row['status']:
            raise ValueError('Continuation outcome changed; refresh: ' + row['id'])
        for key in ('action_basis', 'later_source_delta', 'corrected_action_checkpoint'):
            if row.get(key):
                engine.bound(root, row[key])
    batch = engine.view(engine.load(root, selected()))
    result = route(batch, manifest['operations'], manifest['local_holds'], manifest.get('preferred'))
    result['manifest'] = pointer['manifest']
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('status', 'next', 'check'))
    args = parser.parse_args()
    result = current()
    if args.command == 'check':
        result = {k: result[k] for k in ('controller', 'unresolved_obligations', 'packet_exhausted',
                  'preparation_candidates', 'proposal_complete', 'final_acceptance')} | {'status': 'pass'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
