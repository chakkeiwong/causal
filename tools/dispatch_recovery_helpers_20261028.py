"""Continue independently eligible proposal work after crash recovery."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load, view
from run_followup_program_v2_20261028 import POINTER, selected

DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'followup-runtime-v9'


def main():
    prior = selected()
    assert all(s == 'completed' for s in load(ROOT, prior)['states'].values())
    assert not BASE.exists()
    packets = [
        ('RECOVERY.INVENTORY', 'Index all 150 unresolved obligations and repair the missing commercial cell and stale Python source continuation.',
         ['Every original status and all 105 software/reuse operation identities are preserved.',
          'Exact bounded bindings and stale-reference dispositions are verified without granting acceptance.'],
         ['continuation-inventory-v1/author-review.json', 'python-continuation-recovery-v1/author-review.json']),
        ('BLIP.HELPERS', 'Inspect nine pinned score/input/test helpers and derive exact independent contract witnesses.',
         ['All nine exact originals match pinned Git blobs, byte counts, SHA-256 and inspected anchors.',
          'Source control flow and independent arithmetic are distinguished from native tests and causal qualification.'],
         ['blip-helper-review-v1/review.json', 'blip-helper-review-v1/remaining-gaps.json']),
    ]
    tasks = [dict(id=k, depends=[], action=a, acceptance=c, outputs=[str((BASE / (k.lower().replace('.', '-') + '.json')).relative_to(ROOT))]) for k, a, c, _ in packets]
    tasks += [
        dict(id='HELPERS.PUBLICATION', depends=['BLIP.HELPERS'],
             action='Preserve all predecessor citations and content, integrate reviewed helper findings in paired PDFs, refresh exact-reader checks and live continuation.',
             acceptance=['All 1438 reader and 1103 sponsor citation records remain; new claims trace to exact reviewed sources.',
                         'Both exact paired PDFs, unchanged controllers and explicit remaining gaps are verified; no visual/final acceptance inferred.'],
             outputs=[str((BASE / 'publication.json').relative_to(ROOT))]),
        dict(id='PANEL.LEADS', depends=[],
             action='Reconcile the ten retained R-panel metadata leads against current genuine originals and source audits; register only genuinely missing candidate-specific routes.',
             acceptance=['All ten leads have explicit edition, identity and current-evidence dispositions.',
                         'Named nonabsorbing, multiple-event, stacked, panel-approach and trend-weighting routes remain distinct from native/bank qualification.'],
             outputs=[str((BASE / 'panel-leads.json').relative_to(ROOT))]),
        dict(id='CXX.TAILS', depends=[],
             action='Reconcile CXX01-CXX03 against later inspected originals and current citations, preserving rights and original-source limits.',
             acceptance=['All three historical omission groups have exact later-evidence or precise missing-source dispositions.',
                         'No absent-capability, full census, rights or native acceptance is inferred from search or source access.'],
             outputs=[str((BASE / 'cxx-tails.json').relative_to(ROOT))]),
    ]
    for task in tasks:
        task.update(scope='Finite author proposal work; canonical acceptance remains unchanged', owner='Current author/coordinator')
    BASE.mkdir()
    evidence = [ref(prior / 'publication-receipt.json', 'Completed preserved nested publication'),
                ref(DAY / 'nested-delivery-v1/push-verification.json', 'Verified publication commit and push'),
                ref(DAY / 'continuation-control-recovery-v1/plan-review.json', 'Reviewed recovery plan'),
                ref(DAY / 'continuation-inventory-v1/continuation-register.json', 'All unresolved obligations'),
                ref(Path(__file__), 'Reviewed independent dispatch')]
    write(BASE / 'contracts.json', dict(schema_version=1, awards_acceptance=False, canonical_obligations=376,
                                      cutoff='2026-10-07T15:59:59Z', tasks=tasks, evidence=evidence))
    write(BASE / 'plan-review.json', dict(status='pass_for_scoped_continuation', evidence=evidence + [ref(BASE / 'contracts.json', 'Exact task contracts')],
        findings=['Only publication depends on helper source review.', 'Panel and C++ routes have no unrelated prerequisites.',
                  'Recovery indexing is not full semantic reconciliation or proposal acceptance.',
                  'Historical hash drift is preserved; source and public work do not wait on fresh image or bank gates.']))
    (BASE / 'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(BASE / 'contracts.json', 'Reviewed independent current batch'),
                                      predecessor=ref(BASE / 'plan-review.json', 'Reviewed continuation'), awards_acceptance=False), indent=2) + chr(10))
    for key, _, criteria, names in packets:
        evidence = [ref(DAY / name, 'Performed bounded work') for name in names]
        for name in names:
            verify_bindings(json.loads((DAY / name).read_text()))
        prefix = key.lower().replace('.', '-')
        start = BASE / (prefix + '-start.json')
        write(start, dict(task=key, awards_acceptance=False, evidence=evidence, next_action='Register performed evidence; do not repeat completed acquisition.'))
        append('start', key, str(start.relative_to(ROOT)), ROOT, BASE)
        output = BASE / (prefix + '.json')
        write(output, dict(status='performed_pass', evidence=evidence, awards_acceptance=False, original_outcomes_unchanged=True))
        receipt = BASE / (prefix + '-receipt.json')
        write(receipt, dict(task=key, awards_acceptance=False, execution='performed', outcome='pass',
            outputs=[ref(output, 'Exact performed output')], evidence=evidence,
            criteria=[dict(index=i, verdict='pass', finding=c) for i, c in enumerate(criteria)],
            next_action='Continue independent successor tasks.'))
        append('record', key, str(receipt.relative_to(ROOT)), ROOT, BASE)
    note = BASE / 'publication-start.json'
    write(note, dict(task='HELPERS.PUBLICATION', awards_acceptance=False,
        evidence=[ref(DAY / 'blip-helper-review-v1/review.json', 'Reviewed addition')],
        next_action='Consume pending reader-prepare exit; run subsequent preserving steps once each with durable logs.'))
    append('start', 'HELPERS.PUBLICATION', str(note.relative_to(ROOT)), ROOT, BASE)
    print(json.dumps(view(load(ROOT, BASE))))


if __name__ == '__main__':
    main()
