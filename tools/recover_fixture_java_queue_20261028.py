"""Recover completed independent packets into immutable successor contracts."""
import argparse
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
from run_followup_program_20261028 import ROOT, append, load, view
from run_followup_program_v2_20261028 import POINTER, selected

DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'followup-runtime-v7'
PACKETS = {'FIXTURE.V2': DAY / 'public-attention-contract-v2',
           'JAVA.DELEGATES': DAY / 'aitiotita-delegates-v1'}


def dispatch():
    prior = selected()
    assert all(v == 'completed' for v in load(ROOT, prior)['states'].values())
    if BASE.exists():
        assert not (BASE / 'events.jsonl').exists()
        assert (BASE / 'prior-pointer.json').read_bytes() == POINTER.read_bytes()
        verify_bindings(json.loads((BASE / 'plan-review.json').read_text()))
        write(BASE / 'activation-repair.json', dict(status='repaired', actual_prior_exit=1,
              failure='Immutable write helper correctly refused to overwrite the live followup pointer.',
              repair='Preserve predecessor pointer and contracts; replace only the mutable live pointer.',
              evidence=[ref(BASE / n, 'Preserved prior activation state') for n in
                        ('contracts.json', 'plan-review.json', 'prior-pointer.json')]))
        POINTER.write_text(json.dumps(dict(contracts=ref(BASE / 'contracts.json', 'Reviewed current batch'),
              predecessor=ref(BASE / 'plan-review.json', 'Independent successor plan'), awards_acceptance=False), indent=2) + '\n')
        print(json.dumps(view(load(ROOT, BASE))))
        return
    evidence = [ref(prior / n, 'Completed predecessor packet') for n in
                ('contracts.json', 'publication.json', 'publication-receipt.json')]
    for packet in PACKETS.values():
        verify_bindings(json.loads((packet / 'author-review.json').read_text()))
        evidence.append(ref(packet / 'author-review.json', 'Completed independent evidence'))
    tasks = [
        dict(id='FIXTURE.V2', depends=[], action='Recover and register the completed 48-case local contract evidence without repeating its test run.',
             acceptance=['Actual JUnit cases, test exit and repaired wrapper count agree at 48 passed, zero failures/errors/skips.',
                         'Local information boundaries and missing-score denominators remain distinct from native or bank qualification.'],
             outputs=[str((BASE / 'fixture-v2.json').relative_to(ROOT))]),
        dict(id='JAVA.DELEGATES', depends=[], action='Recover and register the completed seven-original pinned Java review without another acquisition or native execution.',
             acceptance=['Pinned originals, hashes, inspected delegates and finite logical witnesses have verified evidence.',
                         'Generic Gaussian counterexample and linguistic oracle stay separate; broad Java coverage and port qualification remain open.'],
             outputs=[str((BASE / 'java-delegates.json').relative_to(ROOT))]),
        dict(id='FIXTURE.JAVA.PUBLICATION', depends=['FIXTURE.V2', 'JAVA.DELEGATES'],
             action='Integrate both reviewed packets into a preserving monograph and sponsor, renew exact-reader reviews and run both unchanged controllers.',
             acceptance=['All 1433 reader and 1094 sponsor predecessor citations, contexts and content inputs are preserved; new source identities and calculations are audited.',
                         'Both paired PDFs pass all-page text/bounds and actual unchanged integrity checks; Q1/Q5, visual, native and final acceptance stay open.'],
             outputs=[str((BASE / 'publication.json').relative_to(ROOT))])]
    for task in tasks:
        task.update(scope='Finite author proposal work; no original acceptance awarded', owner='Current author/coordinator')
    BASE.mkdir()
    write(BASE / 'contracts.json', dict(schema_version=1, awards_acceptance=False,
          canonical_obligations=376, cutoff='2026-10-07T15:59:59Z', tasks=tasks, evidence=evidence))
    write(BASE / 'plan-review.json', dict(status='pass', evidence=evidence + [ref(BASE / 'contracts.json', 'Reviewed contracts')],
          findings=['Fixture and Java evidence packets are independent; only their joint publication requires both.',
                    'Preserve completed executions and failed attempts; do not repeat non-reentrant wrappers.',
                    'Update only live master/current program documents; frozen master bytes remain unchanged.',
                    'Paired publication cannot award original coverage, native, visual or final acceptance.']))
    (BASE / 'prior-pointer.json').write_bytes(POINTER.read_bytes())
    POINTER.write_text(json.dumps(dict(contracts=ref(BASE / 'contracts.json', 'Reviewed current batch'),
          predecessor=ref(BASE / 'plan-review.json', 'Independent successor plan'), awards_acceptance=False), indent=2) + '\n')
    print(json.dumps(view(load(ROOT, BASE))))


def register(task):
    assert selected() == BASE
    packet = PACKETS[task]
    review = json.loads((packet / 'author-review.json').read_text())
    verify_bindings(review)
    data = load(ROOT, BASE)
    assert data['states'][task] == 'ready'
    if task == 'FIXTURE.V2':
        assert review['actual_exit_code'] == 0
        assert review['tests'] == dict(tests=48, failures=0, errors=0, skipped=0)
        names = ('author-review.json', 'test-exit.json', 'pytest-results.xml', 'harness-failure.json', 'exact-example.json')
        findings = ['All 48 previously executed adversarial cases passed and their actual test exit is zero; no rerun.',
                    'Trusted local contracts retain truth-access roles, exact ties and complete request denominators; no native or bank claim.']
    else:
        assert review['status'] == 'pass_for_bounded_static_review'
        names = ('author-review.json', 'source-audit.json', 'exact-results.json', 'remaining-gaps.json')
        findings = ['All seven pinned originals and selected finite logical witnesses retain verified bindings; no native execution.',
                    'Generic Gaussian witness and bundled linguistic oracle are separate; native port and broad Java coverage remain open.']
    evidence = [ref(packet / n, 'Performed predecessor evidence') for n in names]
    evidence.append(ref(Path(__file__), 'Recovery registration logic'))
    start = BASE / (task.lower() + '-start.json')
    write(start, dict(task=task, awards_acceptance=False, evidence=evidence,
          next_action='Register the verified completed packet; do not rerun its acquisition or tests.'))
    append('start', task, str(start.relative_to(ROOT)), ROOT, BASE)
    output = ROOT / data['nodes'][task]['outputs'][0]
    write(output, dict(status='performed_pass', recovered_execution=True, evidence=evidence,
          findings=findings, native_execution=False, visual_acceptance=False, final_acceptance=False))
    receipt = BASE / (task.lower() + '-receipt.json')
    write(receipt, dict(task=task, awards_acceptance=False, execution='performed', outcome='pass',
          outputs=[ref(output, 'Recovered exact packet')], evidence=evidence,
          criteria=[dict(index=i, verdict='pass', finding=f) for i, f in enumerate(findings)],
          next_action='Continue the other independent packet or the preserving paired publication.'))
    append('record', task, str(receipt.relative_to(ROOT)), ROOT, BASE)
    print(json.dumps(view(load(ROOT, BASE))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['dispatch', 'fixture', 'java'])
    command = parser.parse_args().command
    dispatch() if command == 'dispatch' else register('FIXTURE.V2' if command == 'fixture' else 'JAVA.DELEGATES')
