#!/usr/bin/env python3
"""Integrate the reviewed observation design, exact argument and registered outcomes."""
import json
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/observations-journey'
OLD = ROOT / 'docs/causal_proposal_latent_r_v2_2026-10-13.tex'
DRIVER = ROOT / 'docs/causal_proposal_observations_2026-10-13.tex'
ref = shared.ref


def write(path, data):
    assert not path.exists(), 'Preserve existing evidence: ' + str(path)
    core.write(path, data)


def main():
    assert not DRIVER.exists()
    result_path = ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.observations/local-results.json'
    result = json.loads(result_path.read_text())
    review = json.loads((BASE / 'local-review.json').read_text())
    assert result['status'] == review['status'] == 'pass'
    assert result['all_request_count'] == result['passed_request_count'] == 106
    results = r'''All 106 registered requests matched the frozen boundary expectations, and
all 26 cases preserved semantic responses across the two routes and restart.
The denominator contains 52 computed outputs, 20 unsupported requests,
four scientific refusals, 28 failed/unavailable results and two rejected
changed-horizon requests. A computed output includes diagnostics and generic
sets; this count is not the number of identified or useful causal estimates.
All negative dispositions remain in the comparison. Independent rational
evaluation checked 1,446 points against the supplied inequalities
\citep{exec13_observation_run}.

Total invocation wall time, including failed requests, replay and worker or
CLI launch, was INVOCATION_SECONDS seconds in this local run. Active runner
time was RUNNER_SECONDS seconds, including fixture import and journaling.
These measurements exclude idle gaps between bounded segments, initial
runner startup, author review and all unimplemented work. Parent and child
memory records are separate process high-water readings, not simultaneous
process-tree memory. They do not establish a bank service level, a full
workflow price or a performance advantage over another product.

The journal preserved every earlier request across four execution segments
and a final aggregation-only resume. Restart reused the saved artifact
references and idempotency identities. It did not test process termination
at every possible publication point or multi-host recovery. No native
foreign-language engine, sibling repository, live model or authentic bank
owner participated in this screen~\citep{exec13_observation_run}.
'''
    results = results.replace('INVOCATION_SECONDS', f"{result['full_invocation_wall_seconds']:.3f}")
    results = results.replace('RUNNER_SECONDS', f"{result['active_runner_wall_seconds']:.3f}")
    assert result['segment_count'] == 5
    (BASE / 'results.tex').write_text(results)
    specs = [
        ('exec13_observation_design', 'project_design', 'Trustworthy-observations workflow and reviewed fixed-case protocol',
         ROOT / 'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.observations/workflow-protocol.json',
         'Full decision chain, 26 cases, 106 slots, immutable inputs, prospective stopping and separate evidence classes',
         ['Observation manifest and consumer admission are proposed capabilities.',
          'Feature and outcome clocks, identity, selection, label truth and all workflow costs remain separate.',
          'Local design does not require bank data or sibling execution.']),
        ('exec13_observation_exact', 'project_derivation_and_exact_examples', 'Exact inclusion, linkage, noisy-label and conditional decision examples',
         BASE / 'exact-examples.json', 'Complete exact finite laws; score covariance; factored sensitivity interval and stipulated values',
         ['Identical marginal inclusion probabilities permit variances 1700 and 2500.',
          'Two bijections preserve totals while reversing origin contrasts.',
          'Reported prevalence 17/50 is compatible with true prevalences 3/10 and 3/5 under different positive label laws.',
          'Joint score, projection logic and conditional economics are project derivations with explicit assumptions.']),
        ('exec13_observation_primary', 'project_implementation', 'Inspected local observation, artifact and estimation boundaries',
         ROOT / 'src/causalbank/operation_service_v12.py', 'SUPPORTED, invoke, _estimate and _audit (lines 22–28, 90–120, 180–216, 241–265)',
         ['Observation runtime checks only declared strict feature clocks; other checks are unsupported.',
          'Empty rows and timing-valid false-label or duplicate-origin rows do not establish scientific validity.',
          'Estimation refuses contradicted assumptions and otherwise uses supplied summaries conditionally.']),
        ('exec13_observation_run', 'project_study', 'Prospectively registered local observation workflow comparison',
         BASE / 'local-review.json', 'All 106 requests, 26 parity comparisons, 1446 rational membership checks and retained limits',
         ['All 106 immutable slots matched their declared scoped expectations.',
          '52 computed, 20 unsupported, 4 refused, 28 failed/unavailable and 2 rejected outcomes remain in the denominator.',
          '42.398 seconds is measured invocation time for this run only; no bank-scale or total monetary cost claim.',
          'Replay preserves journal prefixes; no process-kill, native engine, live model or sibling qualification.'])]
    sources = []
    for key, kind, title, path, anchor, claims in specs:
        sources.append({'integrated_citation_key': key, 'kind': kind, 'title': title,
                        'author': 'Causal banking research proposal project', 'year': 2026,
                        'source_identity': str(path.relative_to(ROOT)),
                        'version_date': 'Authored/inspected 2026-10-13; no new external literature claim after cutoff 2026-10-07',
                        'local_copy': ref(path, anchor), 'anchors': [anchor], 'claims': claims,
                        'limits': 'Project design, generated reference or scoped local execution only; no independent, bank, general calibration or adoption acceptance.'})
    sources[1]['additional_sources'] = [ref(ROOT / 'tools/observations_examples_20261013.py', 'Exact law enumeration independent of service code')]
    sources[2]['additional_sources'] = [ref(ROOT / 'src/causalbank/artifacts_v12.py', 'ArtifactStore.put/get content and custody binding'),
        ref(ROOT / 'src/causalbank/operation_contract_v12.py', 'Context and uncertainty meaning preservation')]
    sources[3]['additional_sources'] = [ref(result_path, 'Registered result and every disposition'),
        ref(BASE / 'local-journal.json', 'All actual requests, responses, durations and prefix hashes')]
    write(BASE / 'source-audit.json', {'cutoff': '2026-10-07', 'sources': sources})
    entries = []
    for s in sources:
        entries.append('@misc{' + s['integrated_citation_key'] + ',\n author={{' + shared.escape(s['author']) +
                       '}},\n title={' + shared.escape(s['title']) + '},\n year={2026},\n note={' + shared.escape(s['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(entries))
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-13/funding-journey/section.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker + '\n' + r'\input{program/execution/2026-10-13/observations-journey/section.tex}', 1)
    marker = 'program/execution/2026-10-13/latent-r/reader-input/refs}'
    assert text.count(marker) == 1
    DRIVER.write_text(text.replace(marker, 'program/execution/2026-10-13/latent-r/reader-input/refs,program/execution/2026-10-13/observations-journey/refs}', 1))
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
             'scope': 'Added observation manuscript, exact derivations and registered execution interpretation',
             'findings': ['Feature admission and outcome ascertainment have separate clocks and roles.',
                 'Double-sum inclusion variance and label-score derivatives follow explicit expansions; their statistical premises remain conditional.',
                 'The projection coverage implication is one-way conditional on a valid joint region; neither sharpness nor arbitrary-learner validity is claimed.',
                 'Misclassification prevalence is separated from intervention efficacy; all prices and efficacy assumptions are stipulated.',
                 'Observation conformance passes retain empty-audit and audit-to-estimator admission gaps.',
                 'Measured timing and restart are scoped to this local screen, including excluded costs and failure dispositions.'],
             'evidence': [ref(BASE / n, 'Reviewed argument, source or execution') for n in
                          ['section.tex', 'results.tex', 'source-audit.json', 'plan-review.md', 'local-review.json', 'exact-examples.json']],
             'visual_acceptance': False, 'independent_review': False}
    write(BASE / 'manuscript-review.json', review)
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(OLD, 'Preserved 630-page predecessor driver'), ref(BASE / 'source-audit.json', 'Reviewed added sources'),
                   ref(BASE / 'manuscript-review.json', 'Substantive author review'), ref(Path(__file__), 'Preserving integration code')],
        'generated': [ref(p, 'Prepared manuscript or bibliography') for p in
                      [DRIVER, BASE / 'section.tex', BASE / 'results.tex', BASE / 'refs.bib']]})
    print(json.dumps({'driver': str(DRIVER.relative_to(ROOT)), 'added_citation_records': 4, 'registered_requests': 106}))


if __name__ == '__main__':
    main()
