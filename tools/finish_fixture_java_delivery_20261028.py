"""Consume passed custody and retain harmless whitespace in frozen builders."""
import json
import subprocess
from pathlib import Path

import recover_fixture_java_delivery_20261028 as delivery
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = delivery.ROOT
DAY = delivery.DAY
PRIOR = DAY / 'fixture-java-delivery-v3'
BASE = DAY / 'fixture-java-delivery-v4'


def main():
    assert not BASE.exists()
    events = [json.loads(x) for x in (PRIOR / 'delivery-sequence.jsonl').read_text().splitlines()]
    assert [(x['step'], x['actual_exit_code']) for x in events] == [('stage-repair', 0), ('staging-audit', 0), ('authored-whitespace-check', 2)]
    audit = json.loads((PRIOR / 'evidence-staging-review.json').read_text())
    assert audit['status'] == 'pass' and not audit['missing']
    names = ['tools/build_attention_protocol_sponsor_v2_20261028.py', 'tools/build_attention_protocol_sponsor_v3_20261028.py', 'tools/build_attention_protocol_sponsor_v4_20261028.py', 'tools/build_fixture_java_sponsor_20261028.py']
    expected = ''.join(p + ':21: trailing whitespace.\n+    \n' for p in names)
    assert (PRIOR / 'authored-whitespace-check.log').read_text() == expected
    for p in names:
        assert (ROOT / p).read_text().splitlines()[20] == '    '
        assert subprocess.check_output(['git', 'show', ':' + p], cwd=ROOT) == (ROOT / p).read_bytes()
    BASE.mkdir()
    write(BASE / 'whitespace-disposition.json', dict(
        status='reviewed_exact_preservation_exception',
        finding='Exactly four four-space blank lines at line 21; no executable or prose change.',
        decision='Preserve previously executed and hash-bound builder bytes. No source identity refresh to conceal drift.',
        evidence=[ref(PRIOR / 'authored-whitespace-check.log', 'Observed four-line whitespace failure'), ref(PRIOR / 'evidence-staging-review.json', 'Completed full transitive custody')] + [ref(ROOT / p, 'Frozen builder bytes') for p in names],
        final_acceptance=False))
    verify_bindings(json.loads((BASE / 'whitespace-disposition.json').read_text()))
    delivery.BASE = BASE
    paths = [delivery.rel(p) for p in PRIOR.iterdir() if p.is_file()]
    paths += [delivery.rel(Path(__file__)), delivery.rel(BASE / 'whitespace-disposition.json')]
    delivery.step('stage-final-recovery', ['git', 'add', '-f', '--', *paths])
    delivery.step('remaining-whitespace-check', ['git', '-c', 'core.whitespace=-blank-at-eol', 'diff', '--cached', '--check', '--', 'tools', 'tests', 'docs/mission-control.md', 'docs/program/master-live.md', 'docs/program/execution/current-program.md'])
    staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split(chr(0))
    write(BASE / 'staged-review.json', dict(status='pass_with_exact_frozen_whitespace_exception', staged_count=sum(bool(p) for p in staged),
        evidence=[ref(PRIOR / 'evidence-staging-review.json', 'Full custody audit performed once'), ref(BASE / 'whitespace-disposition.json', 'Four exact frozen blank-line exceptions')],
        source_and_document_bytes_unchanged=True, visual_acceptance=False, final_acceptance=False))
    delivery.step('stage-delivery-records', ['git', 'add', '-f', '--', delivery.rel(BASE)])
    delivery.step('git-commit', ['git', '-c', 'user.name=Codex', '-c', 'user.email=codex@users.noreply.github.com', 'commit', '-m', 'Recover proposal publication and reconcile fixture and Java evidence'])
    delivery.step('git-push', ['git', 'push'])
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=ROOT, text=True).strip()
    assert head == remote
    write(BASE / 'push-verification.json', dict(status='pass', commit=head, origin_main=remote, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(pushed=head)), flush=True)


if __name__ == '__main__':
    main()
