#!/usr/bin/env python3
"""Review and publish the preserving native identification and counterfactual analytical-preparation argument."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_cxx_identification_reader_20261019 as build
import cxx_identification_reference_20261019 as exact
import master_control as core
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author primary-source, exact arithmetic and extracted-page review; no independent or rendered visual acceptance.',
    'Original census remains46 inspected/67 unread of113; L1/L6 and frontier coverage remain open.',
    'Twelve selected aGrUM originals and inherited dosearch evidence do not saturate C++ identification coverage.',
    'ID/IDC proof alignment, graph scope, accumulated kernels and joint abduction remain explicit qualification obligations.',
    'No native engine, Python wrapper or upstream test was run; no transitive-rights or runtime admission.',
    'Authored coupling and posterior examples do not establish bank effects or ROI.',
    'Q1/Q5, mandatory repair rollups and final proposal acceptance remain open.'
]


def read(path):
    return json.loads(path.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    for path in [BASE/'prepared-inputs.json', BASE/'source-audit.json', BASE/'review.json',
                 BASE/'mathematical-review.json', BASE/'copyedit-review.json', BASE/'manuscript-plan-review.json',
                 BASE/'omissions-register.json', BASE/'traceability-review.json',
                 OUT/'source-audit.json', OUT/'build-report.json']:
        verify_bindings(read(path))
    report, audit, index = [read(p) for p in [OUT/'build-report.json', OUT/'source-audit.json', BASE/'traceability-review.json']]
    assert report['cited_records'] == 797 and index['scholarly_pdfs'] == 205
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']:s for s in prior['sources']}
    new = {s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old) == 795 and all(new[k] == v for k,v in old.items())
    added = sorted(new.keys()-old.keys())
    assert set(added) == {'exec19_cxx_identification_source','exec19_cxx_identification_reference'}
    compiled = {r['path']:r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k,c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i,p in enumerate(pages) if 'Native identification engines and the joint meaning' in p and 'A lending analyst may ask' in p]
    assert len(starts) == 1, starts
    start=starts[0]
    ends=[i for i in range(start,min(start+15,len(pages))) if 'this bounded source review does not close them.' in pages[i]]
    assert len(ends)==1,ends
    end=ends[0]; text=' '.join(pages[start:end+1])
    for phrase in ['6 October 2026','C++20','joint posterior','USD 80','USD 30','dosearch','hedge','1/2']:
        assert phrase.lower() in text.lower(),phrase
    equations={k:v['number'] for k,v in report['added_anchors'].items()
               if k in ['exec19:cxxid-coupling','exec19:cxxid-joint']}
    assert len(equations)==2 and all('('+n+')' in text for n in equations.values())
    return report,dict(preserved_records=795,added_records=added,unchanged_compiled_inputs=len(kept),
        all_prior_citation_contexts_preserved=True,physical_pages=[start+1,end+1],equations=equations,
        added_anchors=report['added_anchors'],native_execution=False,visual_acceptance=False)


def review():
    report,checks=verify()
    names=['prepared-inputs.json','manuscript-plan-review.json','source-audit.json','review.json',
        'mathematical-review.json','copyedit-review.json','omissions-register.json','traceability-review.json',
        'exact-results.json','development.tex','reader/build-report.json','reader/source-audit.json',
        'reader/reader.txt','reader/text-layout-review.json']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,
        reviewed_reader=report['pdf'],scope='Preserving native identification and counterfactual source, arithmetic and extracted-page review',
        checks=checks,evidence=[ref(BASE/n,'Reviewed delta and preservation evidence') for n in names]+[
            ref(Path(__file__),'Exact preservation and manuscript review')],
        findings=['All795 predecessor citation records, contexts and compiled inputs survive.',
            'Twelve pinned native originals support bounded recursion, numeric, wrapper and joint-abduction observations; proof alignment and candidate coverage remain open.',
            'Exact enumeration distinguishes observed/intervention marginals from profile counterfactuals1and0 and independent-posterior reconstruction1/2.',
            'Assumed conditional values80,-20and30USD are not incremental ROI; no native or final acceptance.'],
        limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


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
        build_report=ref(OUT/'build-report.json', 'Preserving native identification and counterfactual build'),
        source_review=ref(BASE/'release-source-review.json', 'Source/math/preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Add native identification recursion and joint-abduction critique, exact coupling examples and concrete typed-result/conformance obligations.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor remains paired to its exact predecessor; create a preserving current-reader sponsor successor before Q5.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed native identification and counterfactual working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_cxx_identification_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2':'All795 predecessor identities and citation contexts survive. Twelve pinned aGrUM implementation/wrapper/test originals and authored arithmetic produce797records with205genuine scholarly PDFs. Inherited dosearch evidence remains bound; candidate saturation and proof alignment stay open.',
        'Q3':'Stable/switch structural worlds share observed and intervention marginals but have profile counterfactuals1and0. Joint posterior roots agree with probability1; multiplying their fair marginals gives1/2. Static source concerns are qualification obligations, not claimed native defects.',
        'Q4':'With assumed100USD success payoff and20USD action cost, the profile values are80,-20and30USD under the respective answers. These are conditional authored values, not incremental bank ROI.'}
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
                    ref(BASE/'source-audit.json', 'Twelve pinned native originals'),
                    ref(BASE/'mathematical-review.json', 'Exact coupling and posterior reference'),
                    ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded native identification and counterfactual source, mathematical and economic delta.'))
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
    parser=argparse.ArgumentParser()
    commands=dict(review=review,publish=publish,renew=renew)
    parser.add_argument('command',choices=commands)
    commands[parser.parse_args().command]()
