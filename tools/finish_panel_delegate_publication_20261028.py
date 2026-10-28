"""Close only the finite source publication after consuming actual full checks."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load
from run_followup_program_v2_20261028 import selected


def main():
    day = ROOT / 'docs/program/execution/2026-10-28'
    queue = selected()
    assert load(ROOT, queue)['active'] == 'PANEL.DELEGATE.PUBLICATION'
    base = day / 'panel-delegate-publication-v1'
    evidence = []
    for name in ('reader-prepare', 'reader-build', 'reader-review', 'reader-publish', 'reader-renew',
                 'sponsor-prepare', 'sponsor-build', 'sponsor-review', 'sponsor-publish',
                 'chapters', 'refresh', 'legacy-check', 'program-check'):
        p = base / (name + '-exit.json')
        v = json.loads(p.read_text())
        verify_bindings(v)
        assert v['actual_exit_code'] == 0
        if name.endswith('-check'):
            assert v['unwrapped']
        evidence.append(ref(p, 'Actual performed step and exit'))
    reader = json.loads((day / 'panel-delegates-reader-v1/working-release.json').read_text())
    sponsor = json.loads((day / 'sponsor-panel-delegates-v1/working-release.json').read_text())
    for v in (reader, sponsor):
        verify_bindings(v)
    assert reader['pdf']['sha256'] == sponsor['paired_monograph']['sha256']
    evidence += [ref(day / p, 'Preserving publication evidence') for p in
                 ('panel-delegates-reader-v1/release-source-review.json', 'sponsor-panel-delegates-v1/author-review.json',
                  'panel-delegates-v1/review.json', 'program-refresh-panel-delegates-v1/program-review.json')]
    evidence.append(ref(Path(__file__), 'Finite packet closure'))
    output = queue / 'publication.json'
    write(output, dict(status='performed_pass', reader=reader['pdf'], reader_pages=reader['pages'],
          sponsor=sponsor['pdf'], sponsor_pages=sponsor['pages'], evidence=evidence,
          native_execution=False, visual_acceptance=False, final_acceptance=False))
    receipt = queue / 'publication-receipt.json'
    write(receipt, dict(task='PANEL.DELEGATE.PUBLICATION', awards_acceptance=False, execution='performed', outcome='pass',
          outputs=[ref(output, 'Exact paired publication')], evidence=evidence,
          criteria=[dict(index=0, verdict='pass', finding='All 1445 reader and 1114 sponsor predecessor citations, reader contexts and compiled inputs preserved.'),
                    dict(index=1, verdict='pass', finding='Anchored source findings, exact witnesses, paired PDFs, all-page text/bounds and both actual unchanged controller exits pass; visual and final acceptance remain open.')],
          next_action='Continue independent unresolved proposal routes from the refreshed master; this finite publication is not original acceptance.'))
    event = append('record', 'PANEL.DELEGATE.PUBLICATION', str(receipt.relative_to(ROOT)), ROOT, queue)
    print(json.dumps(dict(recorded=event['task'], sequence=event['sequence'], completed=sum(v == 'completed' for v in load(ROOT, queue)['states'].values()), final_acceptance=False)))


if __name__ == '__main__':
    main()
