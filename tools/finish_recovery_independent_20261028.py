"""Register performed independent reconciliations after releasing queue ownership."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load, view
from run_followup_program_v2_20261028 import selected


def main():
    base = selected()
    state = load(ROOT, base)
    assert state['active'] is None and state['states']['HELPERS.PUBLICATION'] == 'completed'
    day = ROOT / 'docs/program/execution/2026-10-28'
    tasks = [('PANEL.LEADS', 'panel-leads.json', 'panel-lead-reconciliation-v1/lead-register.json',
              'panel-lead-reconciliation-v1/author-review.json',
              ['All ten leads have explicit identity/date/edition/source-type dispositions; retained originals verify.',
               'Six wholly uninspected leads and related-edition limits have candidate-specific actions; original coverage remains inconclusive.']),
             ('CXX.TAILS', 'cxx-tails.json', 'cxx-tail-reconciliation-v1/reconciliation.json',
              'cxx-tail-reconciliation-v1/author-review.json',
              ['All three omission groups map to retained exact current source records and explicit pinned continuations.',
               'No source-access closure, universal absence, rights grant or native qualification is inferred.'])]
    for key, filename, output_name, review_name, findings in tasks:
        evidence = [ref(day / output_name, 'Performed bounded reconciliation'), ref(day / review_name, 'Reviewed finite result')]
        for p in (output_name, review_name):
            verify_bindings(json.loads((day / p).read_text()))
        stem = filename.removesuffix('.json')
        start = base / (stem + '-start.json')
        write(start, dict(task=key, awards_acceptance=False, evidence=evidence,
                         next_action='Register existing performed evidence; do not rerun its review.'))
        append('start', key, str(start.relative_to(ROOT)), ROOT, base)
        output = base / filename
        write(output, dict(status='performed_pass_for_finite_disposition', evidence=evidence,
                           original_outcome='inconclusive', awards_acceptance=False))
        receipt = base / (stem + '-receipt.json')
        write(receipt, dict(task=key, awards_acceptance=False, execution='performed', outcome='pass',
            outputs=[ref(output, 'Exact bounded output')], evidence=evidence,
            criteria=[dict(index=i, verdict='pass', finding=f) for i, f in enumerate(findings)],
            next_action='Continue exact candidate-specific source acquisition or review; original coverage remains unresolved.'))
        append('record', key, str(receipt.relative_to(ROOT)), ROOT, base)
    print(json.dumps(view(load(ROOT, base))))


if __name__ == '__main__':
    main()
