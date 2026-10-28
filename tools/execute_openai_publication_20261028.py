"""Serialize exact publication and unchanged full controller checks."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/openai-contract-review-v1'


def step(name, command):
    log = BASE / (name + '.log')
    assert not log.exists(), log
    with log.open('x') as out:
        result = subprocess.run(command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT)
    event = dict(step=name, exit_code=result.returncode, log=str(log.relative_to(ROOT)))
    with (BASE / 'publication-sequence.jsonl').open('a') as out:
        out.write(json.dumps(event) + chr(10))
    print(json.dumps(event), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main():
    prior = BASE.parent / 'followup-causal-review-v1'
    consumed = json.loads((prior / 'delivery-consumed.json').read_text())
    assert consumed['actual_exit_code'] == 0
    for revision in ['HEAD', 'origin/main']:
        assert subprocess.check_output(['git', 'rev-parse', revision], cwd=ROOT, text=True).strip() == consumed['commit']
    assert json.loads((BASE / 'reader-build-consumed.json').read_text())['actual_exit_code'] == 0
    for name, script, verb in [
        ('reader-publish', 'publish_openai_contract_reader_20261028', 'publish'),
        ('census-record', 'review_openai_program_20261028', 'census'),
        ('sponsor-prepare', 'build_openai_contract_sponsor_20261028', 'prepare'),
        ('sponsor-build', 'build_openai_contract_sponsor_20261028', 'build'),
        ('renew', 'publish_openai_contract_reader_20261028', 'renew'),
        ('sponsor-review', 'publish_openai_contract_sponsor_20261028', 'review'),
        ('sponsor-publish', 'publish_openai_contract_sponsor_20261028', 'publish'),
        ('chapter-review', 'review_openai_program_20261028', 'chapter'),
        ('program-refresh', 'refresh_openai_program_20261028', None),
    ]:
        command = ['python3', 'tools/run_with_review_context_cache_20261025.py', 'tools/' + script + '.py']
        if verb:
            command.append(verb)
        step(name, command)
    for name, script in [('program-check', 'run_program_checkpoint_v3'), ('legacy-check', 'causal_program')]:
        step(name, ['python3', 'tools/' + script + '.py', 'check'])
    state = json.loads((ROOT / 'docs/program/state.json').read_text())
    (BASE / 'publication-checkpoint.json').write_text(json.dumps(dict(status='published_checked', reader=state['reader'],
        sponsor='docs/sponsor_proposal_openai_contract_reviewed_2026-10-28.pdf', recorded=351, nonpassing=150,
        visual_acceptance=False, final_acceptance=False), indent=2) + chr(10))
    print('Publication and both unchanged full checks completed.', flush=True)


if __name__ == '__main__':
    main()
