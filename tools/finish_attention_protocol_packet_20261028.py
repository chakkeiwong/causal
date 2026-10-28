"""Consume unchanged check exits and close only the bounded followup packet."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import append, load
from run_followup_program_v2_20261028 import selected

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'attention-protocol-validation-v1'


def check(name):
    BASE.mkdir(exist_ok=True)
    script = {'legacy': 'causal_program', 'program': 'run_program_checkpoint_v3'}[name]
    log = BASE / (name + '-check.log')
    receipt = BASE / (name + '-check-exit.json')
    assert not receipt.exists() and not log.exists(), 'Preserve each actual check; inspect its saved exit.'
    command = [sys.executable, 'tools/' + script + '.py', 'check']
    with log.open('x') as output:
        result = subprocess.run(command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
    write(receipt, dict(command=command, actual_exit_code=result.returncode,
                        execution='performed', unwrapped=True,
                        evidence=[ref(log, 'Complete unchanged-controller output'),
                                  ref(ROOT / ('tools/' + script + '.py'), 'Executed controller')]))
    print(json.dumps(dict(check=name, actual_exit_code=result.returncode,
                          receipt=str(receipt.relative_to(ROOT)))), flush=True)
    raise SystemExit(result.returncode)


def record():
    queue = selected()
    data = load(ROOT, queue)
    assert data['active'] == 'ATTENTION.PROTOCOL'
    receipts = [BASE / (name + '-check-exit.json') for name in ('legacy', 'program')]
    for path in receipts:
        item = json.loads(path.read_text())
        verify_bindings(item)
        assert item['actual_exit_code'] == 0 and item['unwrapped']
    reader = DAY / 'attention-protocol-reader-v2'
    sponsor = DAY / 'sponsor-attention-protocol-v2'
    for path in (reader / 'working-release.json', sponsor / 'working-release.json'):
        verify_bindings(json.loads(path.read_text()))
    monograph = json.loads((reader / 'working-release.json').read_text())
    paired = json.loads((sponsor / 'working-release.json').read_text())
    assert paired['paired_monograph']['sha256'] == monograph['pdf']['sha256']
    evidence = [ref(path, 'Observed unchanged check exit') for path in receipts]
    evidence += [ref(reader / 'release-source-review.json', 'Every prior citation/context/input retained'),
                 ref(sponsor / 'author-review.json', 'Paired preserving sponsor review'),
                 ref(DAY / 'attention-protocol-chapters-v2/L1/operation-receipt.json', 'Exact-reader L1 successor'),
                 ref(DAY / 'attention-protocol-chapters-v2/L6/operation-receipt.json', 'Exact-reader L6 successor'),
                 ref(DAY / 'program-refresh-attention-protocol-v1/program-review.json', 'Reconciled original program'),
                 ref(DAY / 'program-refresh-attention-protocol-repair-v1/repair-review.json', 'Frozen master restoration and failed-check custody'),
                 ref(Path(__file__), 'Performed packet completion')]
    output = queue / 'publication.json'
    write(output, dict(status='performed_pass', reader=monograph['pdf'], reader_pages=monograph['pages'],
                       sponsor=paired['pdf'], sponsor_pages=paired['pages'], evidence=evidence,
                       visual_acceptance=False, final_acceptance=False, native_execution=False))
    receipt = queue / 'publication-receipt.json'
    write(receipt, dict(task='ATTENTION.PROTOCOL', awards_acceptance=False,
                        execution='performed', outcome='pass',
                        outputs=[ref(output, 'Exact paired publication and observed full checks')], evidence=evidence,
                        criteria=[dict(index=0, verdict='pass', finding='All 1430 predecessor reader and 1089 sponsor citation records, contexts and compiled content preserved; new records are traceable.'),
                                  dict(index=1, verdict='pass', finding='Exact temporal/evaluation distinctions, all-page text bounds and both unchanged full controllers pass; no native or full-coverage acceptance.')],
                        next_action='Continue with reviewed fixture-v2 and Java-delegate successor packets and preserving integration; scoped delivery remains eligible.'))
    event = append('record', 'ATTENTION.PROTOCOL', str(receipt.relative_to(ROOT)), ROOT, queue)
    print(json.dumps(dict(recorded=event['task'], sequence=event['sequence'],
                          completed=sum(v == 'completed' for v in load(ROOT, queue)['states'].values()),
                          final_acceptance=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['legacy', 'program', 'record'])
    parser.add_argument('--attempt', choices=['v1', 'v2'], default='v1')
    args = parser.parse_args()
    BASE = DAY / ('attention-protocol-validation-' + args.attempt)
    command = args.command
    record() if command == 'record' else check(command)
