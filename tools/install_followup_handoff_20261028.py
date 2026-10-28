"""Install reviewed recovery routing without altering frozen acceptance evidence."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import run_followup_program_20261028 as engine
from run_followup_program_v2_20261028 import selected

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'continuation-handoff-v1'


def main():
    assert not BASE.exists()
    old = engine.view(engine.load(ROOT, selected()))
    assert old['completed'] == 3 and old['next'] is None and not old['continue_work']
    original = DAY / 'program-refresh-panel-delegates-v1/remaining-operations.json'
    remaining = json.loads(original.read_text())
    assert len(remaining['operations']) == 150
    state = json.loads((ROOT / 'docs/program/state.json').read_text())
    assert state['execution_runtime']['active'] is None
    protected = [ROOT / p for p in ['docs/program/master-program.md', 'docs/program/master-current.md', 'docs/program/state.json']]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    BASE.mkdir()
    write(BASE / 'before-next.json', old)
    evidence = [ref(original, 'All 150 unresolved obligations'), ref(DAY / 'followup-runtime-v11/publication-receipt.json', 'Finished finite batch'), ref(DAY / 'panel-delegate-delivery-v2/push-verification.json', 'Verified publication delivery')]
    rows = copy.deepcopy(remaining['operations'])
    for row in rows:
        if row.get('corrected_action_checkpoint'):
            engine.bound(ROOT, row['corrected_action_checkpoint'])
            note = json.loads((ROOT / row['corrected_action_checkpoint']['path']).read_text())
            row['resolved_action'] = note['next_action']
    holds = {'TEXT.REVIEW.L1': None}
    holds = {}
    manifest = dict(schema_version=1, reader=state['reader'], operations=rows, local_holds=holds,
                    preferred='SW.CELL.panels_did.R', canonical_obligations=376,
                    status='routing_inventory_not_acceptance', awards_acceptance=False,
                    evidence=evidence, limits=['Preparation candidates require their own bounded reviewed successor before mutation.', 'This controller does not launch unattended workers.', 'Visual image allowance is exhausted; release acceptance is not preparation.', 'An expired batch cannot make unresolved obligations disappear.'])
    write(BASE / 'manifest.json', manifest)
    write(BASE / 'plan-review.json', dict(status='reviewed',
        problem='v2 next returns continue_work=false and next=null after the finite batch despite 150 unresolved canonical obligations.',
        steps=['Preserve the old controllers and event chains.', 'Add a read-only handoff carrying all unresolved IDs, corrected actions and acceptance prerequisites.', 'Prefer active work; local holds affect only their own obligation; exclude final acceptance from preparation.', 'Run behavioral regression tests and the actual 150-row route; then update mutable entrypoints.'],
        evidence=evidence + [ref(BASE / 'before-next.json', 'Observed false terminal signal'), ref(ROOT / 'tools/run_followup_program_v3_20261028.py', 'Successor routing logic')], awards_acceptance=False))
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_followup_handoff_20261028.py', '-v']
    with (BASE / 'tests.log').open('x') as out:
        result = subprocess.run(command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT)
    write(BASE / 'tests-exit.json', dict(command=command, actual_exit_code=result.returncode, execution='performed', evidence=[ref(BASE / 'tests.log', 'Actual regression results')]))
    assert result.returncode == 0
    review = dict(status='pass_for_handoff_not_completion', evidence=[ref(BASE / 'manifest.json', 'Exact continuation actions'), ref(BASE / 'plan-review.json', 'Reviewed constraints'), ref(BASE / 'tests-exit.json', 'Performed behavioral tests'), ref(ROOT / 'tools/run_followup_program_v3_20261028.py', 'Reviewed successor'), ref(ROOT / 'tests/test_followup_handoff_20261028.py', 'Regression cases')], awards_acceptance=False, final_acceptance=False)
    write(BASE / 'author-review.json', review)
    write(ROOT / 'docs/program/execution/continuation-current.json', dict(manifest=ref(BASE / 'manifest.json', 'Current reviewed routing inventory'), review=ref(BASE / 'author-review.json', 'Performed review')))
    from run_followup_program_v3_20261028 import current
    actual = current()
    assert actual['next'] == 'SW.CELL.panels_did.R' and actual['continue_work']
    assert actual['unresolved_obligations'] == 150 and actual['preparation_candidates'] == 146
    write(BASE / 'after-next.json', actual)
    for name in ['docs/program/master-live.md', 'docs/program/execution/current-program.md', 'docs/mission-control.md']:
        p = ROOT / name
        (BASE / ('before-' + p.name)).write_bytes(p.read_bytes())
        text = p.read_text().replace('python3 tools/run_followup_program_v2_20261028.py status, next and check', 'python3 tools/run_followup_program_v3_20261028.py status, next and check').replace('python3 tools/run_followup_program_v2_20261028.py status, next, check', 'python3 tools/run_followup_program_v3_20261028.py status, next, check')
        text += '\nThe v3 handoff preserves all 150 unresolved obligations when a finite batch ends.\nIt offers bounded successor preparation and preserves acceptance prerequisites;\nno batch boundary implies completion. Use v2 start/checkpoint/record for registered\npacket events. The selected next preparation is the remaining R panel delegate\ncontract. No unattended worker runs.\n'.replace('\n', chr(10))
        p.write_text(text.rstrip() + chr(10))
    mission = (ROOT / 'docs/mission-control.md').read_text()
    html = subprocess.run(['pandoc', '--from=gfm', '--to=html'], input=mission, text=True, capture_output=True, check=True).stdout
    (ROOT / 'docs/mission-control.html').write_text('<!doctype html><meta charset="utf-8"><title>Causal proposal execution</title>' + html)
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    write(BASE / 'installation.json', dict(status='pass', protected_hashes=hashes, evidence=[ref(BASE / 'author-review.json', 'Reviewed handoff'), ref(BASE / 'after-next.json', 'Actual live result'), ref(Path(__file__), 'Exact installation')], final_acceptance=False))
    print(json.dumps(dict(installed='v3', unresolved=150, preparation_candidates=146, next=actual['next'], protected_bytes_unchanged=True)))


if __name__ == '__main__':
    main()
