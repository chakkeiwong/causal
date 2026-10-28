"""Close only the finite fixture/Java publication packet after observed checks."""
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load
from run_followup_program_v2_20261028 import selected

DAY = ROOT / 'docs/program/execution/2026-10-28'


def main():
    queue = selected()
    assert load(ROOT, queue)['active'] == 'FIXTURE.JAVA.PUBLICATION'
    steps = DAY / 'fixture-java-publication-v1'
    evidence = []
    for name in ('reader-build', 'reader-review', 'reader-publish', 'reader-renew',
                 'sponsor-prepare', 'sponsor-build', 'sponsor-review', 'sponsor-publish',
                 'chapters', 'refresh', 'legacy-check', 'program-check'):
        path = steps / (name + '-exit.json')
        item = json.loads(path.read_text())
        verify_bindings(item)
        assert item['actual_exit_code'] == 0
        if name.endswith('-check'):
            assert item['unwrapped']
        evidence.append(ref(path, 'Observed performed step and actual exit'))
    rb, sb = DAY / 'fixture-java-reader-v1', DAY / 'sponsor-fixture-java-v1'
    reader = json.loads((rb / 'working-release.json').read_text())
    sponsor = json.loads((sb / 'working-release.json').read_text())
    for release in (reader, sponsor):
        verify_bindings(release)
    assert sponsor['paired_monograph']['sha256'] == reader['pdf']['sha256']
    evidence += [ref(rb / 'release-source-review.json', 'All source records/contexts/content retained'),
                 ref(sb / 'author-review.json', 'Preserving exact paired sponsor'),
                 ref(DAY / 'program-refresh-fixture-java-v1/program-review.json', 'All 150 nonpassing IDs retained'),
                 ref(Path(__file__), 'Performed packet closure')]
    output = queue / 'publication.json'
    write(output, dict(status='performed_pass', reader=reader['pdf'], reader_pages=reader['pages'],
          sponsor=sponsor['pdf'], sponsor_pages=sponsor['pages'], evidence=evidence,
          visual_acceptance=False, final_acceptance=False, native_execution=False))
    receipt = queue / 'publication-receipt.json'
    write(receipt, dict(task='FIXTURE.JAVA.PUBLICATION', awards_acceptance=False,
          execution='performed', outcome='pass', outputs=[ref(output, 'Exact paired publication')], evidence=evidence,
          criteria=[dict(index=0, verdict='pass', finding='All 1433 reader and 1094 sponsor predecessor source records, reader contexts and compiled content inputs preserved; additions audited.'),
                    dict(index=1, verdict='pass', finding='Paired PDFs, all-page text/bounds and both actual unwrapped full controller exits pass. Q1/Q5, visual, native and final acceptance remain open.')],
          next_action='Deliver the scoped commit/push and continue independent unresolved proposal work; queue completion is not original acceptance.'))
    event = append('record', 'FIXTURE.JAVA.PUBLICATION', str(receipt.relative_to(ROOT)), ROOT, queue)
    print(json.dumps(dict(recorded=event['task'], sequence=event['sequence'],
                          completed=sum(v == 'completed' for v in load(ROOT, queue)['states'].values()),
                          final_acceptance=False)))


if __name__ == '__main__':
    main()
