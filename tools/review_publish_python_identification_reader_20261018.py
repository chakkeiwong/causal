#!/usr/bin/env python3
"""Review and publish the preserving Python identification manuscript successor."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_python_identification_reader_20261018 as build
import master_control as core
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author primary-source, mathematical and extracted-page review; rendered visual and independent acceptance remain open.',
    'The Python coverage result is inconclusive: GCM counterfactual paths, general counterfactual identification and partial-identification optimizers remain omissions.',
    'Ananke0.5.0 is a selected historical release, not a latest-release or current-support claim; only authenticated inert source was inspected.',
    'No external package was installed, imported or executed; environment separation, typed conversion and engine admission remain proposed.',
    'The response-type calculation is a deterministic authored construction, not a sampling interval, prospective policy value or bank ROI.',
    'Dependency and distribution conflicts, Q1/Q5, mandatory repairs, L1/L6 coverage and final proposal acceptance remain open.'
]


def read(path):
    return json.loads(path.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    for path in [BASE/n for n in ['prepared-inputs.json', 'source-audit.json',
        'manuscript-plan-review.json', 'mathematical-review.json', 'copyedit-review.json',
        'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']]:
        verify_bindings(read(path))
    report = read(OUT/'build-report.json')
    audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    assert report['cited_records'] == 781 and index['scholarly_pdfs'] == 201
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.calculate() == read(BASE/'exact-results.json')
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR)['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 772 and all(new[k] == v for k, v in old.items())
    added = set(new)-set(old)
    assert added == set(build.NEW_KEYS)
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in read(build.PRIOR)['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if 'A lending analyst may ask' in p]
    assert len(starts) == 1, starts
    start = starts[0]
    ends = [i for i in range(start, min(start+20, len(pages))) if 'qualified banking decisions.' in pages[i]]
    assert len(ends) == 1, ends
    end = ends[0]
    text = ' '.join(pages[start:end+1])
    for phrase in ['DoWhy', 'pgmpy', 'Ananke', 'y0', 'OneLineID', 'NotIdentifiedError',
                   '5 December 2023', 'identification is not considered', 'within-person coupling',
                   'attainability', 'monotonicity', 'USD350', 'USD50', 'retrospective',
                   'below0.14', 'Sympy', 'Other/Proprietary', 'partial-identification']:
        assert phrase.lower() in text.lower(), phrase
    equations = {}
    for label in ['exec18:pyid-equal-laws', 'exec18:pyid-conditional',
                  'exec18:pyid-sharp', 'exec18:pyid-bounds']:
        number = report['added_anchors'][label]['number']
        assert '('+number+')' in text, label
        equations[label] = number
    return report, dict(preserved_records=772, added_records=sorted(added),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        context_rule='Exclude only the new Python identification development path from predecessor context multisets.',
        physical_pages=[start+1, end+1], equations=equations,
        added_anchors=report['added_anchors'], visual_acceptance=False)


def review():
    report, checks = verify()
    paths = [BASE/n for n in ['plan.md', 'prepared-inputs.json', 'manuscript-plan-review.json',
        'source-audit.json', 'mathematical-review.json', 'copyedit-review.json',
        'traceability-review.json', 'exact-results.json', 'development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json',
        'review-attempt-1/failure-review.json']]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving four-family Python identification source/math/text delta',
        checks=checks, evidence=[ref(p, 'Reviewed delta and preservation evidence') for p in paths]+[
            ref(Path(__file__), 'Exact preservation and manuscript review')],
        findings=['All772 predecessor source records,201 scholarly PDFs, citation contexts and unchanged compiled inputs survive.',
            'The four inspected source boundaries distinguish adjustment, intervention ID, conditional intervention and cross-world queries.',
            'Invalid experimental preconditions do not become scientific nonidentification merely because an exception has that name.',
            'Both structural models have the same randomized observed/intervention laws, but conditional recovery differs0 versus1.',
            'The response-type family proves sharp benefit-share[0,1/2] and conditional[0,1] bounds; monotonicity is an additional restriction.',
            'The stipulated retrospective net range[-50,350]USD is not an actionable preassignment policy value.',
            'Source-specific environment incompatibilities, distribution declarations and omitted families remain visible.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def publish():
    report, _ = verify()
    review_record = read(BASE/'release-source-review.json')
    verify_bindings(review_record)
    assert review_record['status'] == 'pass' and not review_record['issues']
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest = dict(kind='working_monograph', final_acceptance=False,
        pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving Python identification build'),
        source_review=ref(BASE/'release-source-review.json', 'Author source/math/preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate four-family Python identification source boundaries and proposed component-specific reuse.',
                 'Derive exact randomized response-type ambiguity, sharp bounds and retrospective monetary interpretation.',
                 'Retain dependency/license conflicts, failed-precondition semantics and specific source omissions.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Predecessor sponsor stays paired to its original reader; a preserving exact-reader successor follows.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed Python identification working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_python_identification_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': 'All772 predecessor citation records and contexts survive with201 genuine scholarly PDFs. Seven authentic selected-release Ananke source records and two authored project records bring the total to781. Wider Python counterfactual and optimizer coverage remains unresolved.',
        'Q3': 'Fresh exact rational enumeration reproduces identical randomized observed/intervention laws, ATE0, retrospective recovery0 versus1 and sharp response-type bounds. This is an authored construction; four-family native execution and adapters remain unqualified.',
        'Q4': 'The stipulated USD400 recovery value and USD50 cost yield a sharp retrospective conditional net range[-50,350]USD. The factual failure was unavailable at original assignment, so this does not establish prospective policy value or bank ROI. All prior monetary examples remain unchanged.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = core.read(ROOT, previous['path'])
        if old.get('reviewed_reader', {}).get('sha256') == report['pdf']['sha256']:
            continue
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, binding, ref(BASE/'release-source-review.json', 'Preserving author delta'),
                    ref(BASE/'source-audit.json', 'Authentic primary identities and project references'),
                    ref(BASE/'mathematical-review.json', 'Exact coupling, bounds and monetary interpretation')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded Python source, mathematics and monetary interpretation.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader preserving delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0],
            reviewer=REVIEWER, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', scope=scope, findings=[finding], evidence=evidence,
            limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact-reader '+q+' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = dict(review=review, publish=publish, renew=renew)
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
