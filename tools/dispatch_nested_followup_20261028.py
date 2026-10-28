"""Install an independent successor after completing the recovered publication."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load, view
from run_followup_program_v2_20261028 import POINTER, selected

DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'followup-runtime-v8'


def main():
    prior = selected()
    assert all(v == 'completed' for v in load(ROOT, prior)['states'].values())
    assert not BASE.exists()
    delta = DAY / 'software-tail-java-panel-delta-v1'
    verify_bindings(json.loads((delta / 'author-review.json').read_text()))
    sources = DAY / 'reliableai-nested-v1'
    verify_bindings(json.loads((sources / 'plan-review.json').read_text()))
    tasks = [
        dict(id='SOURCE.TAIL.DELTA', depends=[], action='Register the performed Java and R-panel later-evidence reconciliation without resetting earlier work.',
             acceptance=['All four Java groups and the later R-panel action basis have verified dated evidence.',
                         'Only two of 104 operation rows are reconciled; all 150 original nonpassing outcomes remain.'],
             outputs=[str((BASE / 'tail-delta.json').relative_to(ROOT))]),
        dict(id='RELIABLEAI.NESTED', depends=[], action='Inspect the 20 pinned BLIP and Spot text originals, source boundaries and conditional banking reuse routes.',
             acceptance=['Every acquired file matches declared bytes, SHA-256, Git blob and inspected primary anchors, or has a precise omission.',
                         'Licenses, score/search, graph endpoints and tests are reviewed without executing external code or inferring causal/native acceptance.',
                         'Concrete adopt/integrate/port/reject choices and remaining dependencies are documented.'],
             outputs=[str((BASE / 'nested-review.json').relative_to(ROOT))]),
        dict(id='NESTED.PUBLICATION', depends=['RELIABLEAI.NESTED'], action='Integrate reviewed nested-engine findings into preserving paired PDFs and refresh exact-reader checks and the live master.',
             acceptance=['All 1436 reader and 1099 sponsor predecessor citation records and content inputs remain preserved.',
                         'New technical claims trace to inspected originals; both PDFs and unchanged controllers are checked; broad and visual acceptance remain explicit.'],
             outputs=[str((BASE / 'publication.json').relative_to(ROOT))]),
    ]
    for task in tasks:
        task.update(scope='Finite author proposal work; no original acceptance awarded', owner='Current author/coordinator')
    BASE.mkdir()
    evidence = [ref(prior / 'publication-receipt.json', 'Completed recovered publication'),
                ref(delta / 'author-review.json', 'Performed independent tail delta'),
                ref(sources / 'plan-review.json', 'Reviewed nested source protocol')]
    write(BASE / 'contracts.json', dict(schema_version=1, awards_acceptance=False, canonical_obligations=376, cutoff='2026-10-07T15:59:59Z', tasks=tasks, evidence=evidence))
    write(BASE / 'plan-review.json', dict(status='pass', evidence=evidence + [ref(BASE / 'contracts.json', 'Reviewed successor contracts'), ref(Path(__file__), 'Dispatch logic')],
        findings=['Later-evidence reconciliation and nested source inspection are independent.',
                  'Publication depends only on reviewed source findings; other source tails remain independent.',
                  'No root license is treated as covering nested dependencies; no downloaded code is executed.',
                  'Full Java census, fresh visual review and final proposal acceptance are not granted by this packet.']))
    (BASE / 'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(BASE / 'contracts.json', 'Reviewed current batch'), predecessor=ref(BASE / 'plan-review.json', 'Reviewed continuation'), awards_acceptance=False), indent=2) + chr(10))
    task = 'SOURCE.TAIL.DELTA'
    output = BASE / 'tail-delta.json'
    note = BASE / 'tail-delta-start.json'
    bindings = [ref(delta / 'source-tail-delta.json', 'Performed source delta'), ref(delta / 'author-review.json', 'Verified scope')]
    write(note, dict(task=task, awards_acceptance=False, evidence=bindings, next_action='Register already performed evidence; do not repeat the review.'))
    append('start', task, str(note.relative_to(ROOT)), ROOT, BASE)
    write(output, dict(status='performed_pass', evidence=bindings, original_outcomes_unchanged=True, awards_acceptance=False))
    receipt = BASE / 'tail-delta-receipt.json'
    write(receipt, dict(task=task, awards_acceptance=False, execution='performed', outcome='pass', outputs=[ref(output, 'Completed bounded delta')], evidence=bindings,
        criteria=[dict(index=0, verdict='pass', finding='Four Java groups and the 24 October R-panel action basis reconciled against their exact later receipts.'),
                  dict(index=1, verdict='pass', finding='Two of 104 trace rows reconciled; other 102 and all 150 original nonpassing outcomes retained.')],
        next_action='Continue the independent nested-engine review.'))
    append('record', task, str(receipt.relative_to(ROOT)), ROOT, BASE)
    task = 'RELIABLEAI.NESTED'
    note = BASE / 'nested-start.json'
    write(note, dict(task=task, awards_acceptance=False, evidence=[ref(sources / 'plan-review.json', 'Reviewed exact source scope')], next_action='Run fixed collector, consume actual exit, verify identities and inspect selected original text without execution.'))
    append('start', task, str(note.relative_to(ROOT)), ROOT, BASE)
    print(json.dumps(view(load(ROOT, BASE))))


if __name__ == '__main__':
    main()
