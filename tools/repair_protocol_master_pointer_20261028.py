"""Restore the frozen master and publish a separate current execution pointer."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'program-refresh-attention-protocol-repair-v1'
PRIOR = DAY / 'program-refresh-attention-protocol-v1'


def main():
    assert not BASE.exists()
    failed = DAY / 'attention-protocol-validation-v1/legacy-check-exit.json'
    receipt = json.loads(failed.read_text())
    verify_bindings(receipt)
    assert receipt['actual_exit_code'] == 1
    log = ROOT / receipt['evidence'][0]['path']
    assert 'Missing or changed evidence: docs/program/master-program.md' in log.read_text()
    BASE.mkdir()
    master = ROOT / 'docs/program/master-program.md'
    (BASE / 'failed-master-pointer.md').write_bytes(master.read_bytes())
    master.write_bytes((PRIOR / 'prior-master-program.md').read_bytes())
    current = ROOT / 'docs/program/master-current.md'
    assert not current.exists()
    current.write_text('''# Current master program: causal banking proposal

Updated 28 October 2026. The executable contracts, current documents, gap routes
and continuation actions are in the [current program](execution/current-program.md).
The [V11 master](master-program.md) is a frozen historical source whose exact
bytes remain bound by earlier evidence. It is retained as historical scope,
not a current progress dashboard.

The current program governs the research and product proposal for four banking
journeys, including the software survey and reuse decisions, LLM and agent
methods, CLI/MCP integration, public-data prototype designs and sponsor case.
Public and synthetic evidence justify later expensive bank experiments.
Proposal completion does not establish an implemented or accepted bank product.

The paired reader has 1,751 pages, 1,433 audited citation records and 274 genuine
scholarly PDFs; the sponsor has 166 pages and 1,094 audited citation records.
There are 351 recorded outcomes among 376 original operations. All 150
nonpassing obligations remain: 121 inconclusive, 25 open and four negative.
The original scheduler's zero-ready count requires reviewed successors.

The independent stronger local fixture passed 48 adversarial cases. Seven
pinned Java delegates have verified originals and a completed bounded source
review. Both packets await preserving paired-document integration; their
completion does not award broad software or product acceptance.

Use `python3 tools/run_followup_program_v2_20261028.py status`, `next` and
`check` for active-agent work. Both original controllers continue to govern
acceptance and full integrity. Checkpoints and phase boundaries are recovery
records. A local blocker leaves independent eligible work available.
''')
    mission = ROOT / 'docs/mission-control.md'
    m = mission.read_text().replace('[Current program and execution rules]', '[Current program and execution rules]')
    marker = '# Mission control: causal banking proposal\n'
    assert m.startswith(marker)
    mission.write_text(m.replace(marker, marker + '\n[Current master program](program/master-current.md).\n', 1))
    execution = ROOT / 'docs/program/execution/current-program.md'
    text = execution.read_text()
    text += '''
## Frozen-master integrity repair

The first post-publication legacy check exited 1 because the refresh prepended
a pointer to the frozen V11 master file. Its original bytes are restored.
The [current master](../master-current.md) now supplies the live entrypoint;
historical source bindings remain unchanged. The failed exit and repair are
preserved in `program-refresh-attention-protocol-repair-v1`.
'''
    execution.write_text(text)
    write(BASE / 'repair-review.json', dict(
        status='repaired_pending_unchanged_checks',
        issue='A current-pointer edit invalidated the hash-bound historical master file.',
        repair='Restored exact prior master bytes and published a separate current-master document.',
        evidence=[ref(failed, 'Actual failed unchanged check'),
                  ref(log, 'Observed missing/changed-evidence diagnostic'),
                  ref(BASE / 'failed-master-pointer.md', 'Preserved failed pointer edit'),
                  ref(PRIOR / 'prior-master-program.md', 'Exact restoration source'),
                  ref(master, 'Restored historical master'),
                  ref(current, 'Separate live master entrypoint'),
                  ref(Path(__file__), 'Narrow evidence-preserving repair')],
        next_action='Consume any already-running full check; rerun unchanged controllers after this repair and retain all actual exits.',
        final_acceptance=False, visual_acceptance=False))
    print(json.dumps(dict(restored='docs/program/master-program.md',
                          current_master='docs/program/master-current.md', failed_exit_preserved=True)))


if __name__ == '__main__':
    main()
