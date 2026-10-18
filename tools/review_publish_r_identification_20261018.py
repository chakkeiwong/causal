#!/usr/bin/env python3
"""Preserve, review and publish the recovered R-identification proposal delta."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import build_r_identification_reader_20261018 as build
import master_control as core
import r_identification_reference_20261018 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
SOURCES = ROOT/'docs/program/execution/2026-10-18/r-identification'
PRIOR = build.PREDECESSOR
OP = 'SW.CELL.identification_counterfactual.R'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author source, mathematical and extracted-page review; no independent or rendered visual acceptance.',
    'Ten named R families are compared; broader census, historical task-view coverage and additional leads remain unresolved.',
    'Original acquisition-plan wording said two rounds; five saved manifest batches were actually used and are explicitly disclosed.',
    'Pinned source inspection is not native R execution, numerical qualification or complete dependency/rights clearance.',
    'The exact response-type, confounding and accounting examples are project constructions, not observed bank results.',
    'Q1/Q5, all three mandatory manuscript repairs and final proposal acceptance remain open.'
]


def read(path):
    return json.loads(path.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
            for c in r['citation_contexts'] if c['path'] not in excluded)
            for r in index['records']}


def verify():
    inputs = [BASE/'prepared-inputs.json', BASE/'plan-review.json',
              BASE/'mathematical-review.json', BASE/'source-audit.json',
              BASE/'primary-review.json', BASE/'copyedit-review.json',
              OUT/'build-report.json', OUT/'source-audit.json',
              BASE/'traceability-review.json', SOURCES/'candidate-omissions-register.json']
    for p in inputs:
        verify_bindings(read(p))
    report = read(OUT/'build-report.json')
    audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    assert report['cited_records'] == 760 and index['scholarly_pdfs'] == 199
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    prior = read(PRIOR/'reader/source-audit.json')
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 751 and all(new[k] == v for k, v in old.items())
    added = sorted(new.keys()-old.keys())
    assert len(added) == 9
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    addition = str((SOURCES/'development.tex').relative_to(ROOT))
    before = contexts(read(PRIOR/'traceability-review.json'))
    after = contexts(index, {addition})
    assert all(c == after[k] for k, c in before.items())
    aux = (OUT/(build.NAME+'.aux')).read_text()
    equations = {}
    for label in ['exec18:r-fiber', 'exec18:r-ate', 'exec18:r-pn']:
        m = re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)', aux)
        assert m and all(x.isdigit() for x in m.group(1).split('.')), label
        equations[label] = m.group(1)
    pages = (OUT/'reader.txt').read_text().split(chr(12))
    normalized = [' '.join(p.split()) for p in pages]
    title = 'Identification software must preserve what is and is not identified'
    starts = [i for i, p in enumerate(normalized) if title in p and
              'Suppose a bank is considering' in p]
    assert len(starts) == 1
    start = starts[0]
    ends = [i for i in range(start, min(start+12, len(pages))) if
            'the wider R ecosystem remains incomplete' in normalized[i]]
    assert len(ends) == 1
    end = ends[0]
    text = ' '.join(normalized[start:end+1])
    for phrase in ['causaleffect', 'dosearch', 'cfid', 'causaloptim', 'bpbounds',
                   'CausalQueries', '729/65536', '729/4096', '5/6', '7/9',
                   'not an executed package trial', 'Disabling a time limit']:
        assert phrase in text, phrase
    assert all('('+n+')' in text for n in equations.values())
    checks = dict(preserved_records=751, added_records=added, new_scholarly_records=2,
                  new_software_records=6, new_project_records=1,
                  unchanged_compiled_inputs=len(kept),
                  all_prior_citation_contexts_preserved=True,
                  context_rule='Compare every predecessor context after excluding only the new development.tex path.',
                  equations=equations, physical_pages=[start+1, end+1],
                  printed_pages=report['added_section_printed_pages'],
                  exact_ATE='1/2', sharp_PN=['2/3', '1'],
                  posterior_PN_means=['5/6', '7/9'],
                  financial_values=['-400/3', '200', '100/3', '-200/9'],
                  visual_acceptance=False)
    return report, checks


def review():
    report, checks = verify()
    paths = [BASE/'plan-review.json', BASE/'mathematical-review.json',
             BASE/'primary-review.json', BASE/'copyedit-review.json',
             BASE/'source-audit.json', BASE/'prepared-inputs.json',
             BASE/'traceability-review.json', OUT/'build-report.json',
             OUT/'source-audit.json', OUT/'reader.txt', OUT/'text-layout-review.json',
             BASE/'exact-results.json', SOURCES/'candidate-omissions-register.json', Path(__file__)]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[],
        scope='Preserving R-identification source, mathematical and extracted-page delta',
        reviewer=REVIEWER, reviewed_reader=report['pdf'], checks=checks,
        evidence=[ref(p, 'Reviewed R-identification delta and preservation evidence') for p in paths],
        findings=[
            'All751 predecessor source records, unchanged compiled inputs and original citation contexts survive.',
            'Selected package output semantics distinguish valid negative certificates, incomplete searches, undefined queries and invalid input.',
            'Exact examples separate a point-identified average effect, a sharp counterfactual interval, prior sensitivity and stipulated accounting.',
            'Six software originals and two genuine scholarly manuscripts support the added technical claims; omissions and actual acquisition bounds remain explicit.'
        ], limitations=LIMITS, final_acceptance=False, visual_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def yield_for_publication():
    report, _ = verify()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    path = BASE/'publication-progress.json'
    write(path, dict(finding='Source, exact-reference, compilation, text-bound and preserving citation reviews passed for the recovered R-identification successor.',
        next_action='Publish the reviewed successor, renew exact-reader Q2-Q4, then record the R cell as inconclusive and continue independent work.',
        evidence=[ref(BASE/'release-source-review.json', 'Bounded author release review'),
                  ref(OUT/'build-report.json', 'Completed preserving build'),
                  report['pdf']],
        yield_reason='Publishing and exact-reader reviews require an idle active-operation slot; this is a scheduling transition, not a completion or permission checkpoint.'))
    transition('yield', OP, path)


def publish():
    report, _ = verify()
    review_record = read(BASE/'release-source-review.json')
    verify_bindings(review_record)
    assert review_record['status'] == 'pass' and not review_record['issues']
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    audit = read(OUT/'source-audit.json')
    manifest = dict(kind='working_monograph', final_acceptance=False,
        pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving R-identification build'),
        source_review=ref(BASE/'release-source-review.json', 'Source/math/preservation delta'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review_record['evidence'],
        changes=['Integrate comparison of R adjustment, ID/IDC, counterfactual, restricted bounds and Bayesian query tools; exact repayment example and conditional reuse boundaries.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved October18 sponsor; retain exact baseline pairing and record successor delta before Q5.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed R-identification working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_r_identification_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All751 predecessor records and197 scholarly PDFs are preserved; six authentic software sources, two genuine scholarly PDFs and one exact project reference yield760 records and199 scholarly PDFs. Every original citation context remains unchanged; added citations have separate contexts.',
        'Q3': 'Exact response-type probabilities, sharp PN interval, equal likelihoods, two posterior means and observationally equivalent confounded models reproduce. Complete-algorithm negative results, timeout/incomplete unknowns and undefined queries are distinct. No native package or rendered visual acceptance inferred.',
        'Q4': 'The stipulated retrospective attribution rule yields sharp net range[-400/3,200]USD and posterior means100/3 and-200/9USD. These are illustrative exact calculations, not prospective assignment, observed bank benefit or ROI. Prior financial examples remain unchanged.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader', {}), report['pdf']):
            assert old['outcome'] == 'pass'
            continue
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE/'working-release.json', 'Exact current reader'),
            ref(BASE/'release-source-review.json', 'Preserving source/math delta'),
            ref(BASE/'source-audit.json', 'Authentic R primary sources'),
            ref(BASE/'mathematical-review.json', 'Exact response-type examples'),
            ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded R-identification source, mathematical and economic delta.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
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


def record_cell():
    report, checks = verify()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['pdf'])
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    evidence = [ref(SOURCES/'candidate-omissions-register.json', 'Ten named families, source/census omissions and actual stopping rule'),
                ref(BASE/'source-audit.json', 'Authentic primary identity/version/hash/anchor/claim bindings'),
                ref(BASE/'release-source-review.json', 'Inspected author delta and exact preservation'),
                ref(BASE/'working-release.json', 'Integrated working reader')]
    criteria = [
        dict(index=0, verdict='inconclusive', finding='Five inherited families and five complementary families are identified and compared at the cutoff. Historical CRAN coverage, repository403, SEMID, Counterfactual/WhatIf/R6causal and IV/mediation taxonomy boundaries prevent an exhaustive census. Five batches were used despite the original ambiguous two-round wording; this deviation is retained.', evidence=evidence),
        dict(index=1, verdict='pass', finding='All added technical claims have authentic pinned source bytes, acquisition/hash/blob checks, versions, precise inspected anchors and supported claims. The two cited scholarly originals are genuine correctly named PDFs. Inherited source records and citation contexts are preserved; exact examples reproduce.', evidence=evidence),
        dict(index=2, verdict='pass', finding='Adjustment, ID/IDC, counterfactual, restricted sharp bounds, IV confidence sets and Bayesian queries have distinct roles and conditional reuse decisions. Uninspected leads and unavailable originals remain explicit; no essential-source or absence waiver is awarded.', evidence=evidence)]
    output = ROOT/node['outputs'][0]
    scope = 'Bounded author R-identification coverage review; broader source census unresolved'
    write(output, dict(operation=OP, status='inconclusive', reviewer=REVIEWER,
        scope=scope, reviewed_reader=report['pdf'], criteria=criteria, checks=checks,
        evidence=evidence, limitations=LIMITS, proposal_only=True,
        followup_actions=[
            'Resolve pre-cutoff SEMID, Counterfactual, WhatIf and R6causal identities and primary scope under a newly explicit acquisition budget.',
            'Reconcile wider IV/mediation candidates and aliases and obtain a historical CRAN task-view snapshot; rerun repository discovery when available.',
            'Obtain authentic CausalQueries article if its scholarly claims are needed; current package-doc claims do not substitute for that article.',
            'Keep native R execution and dependency/rights qualification as separate prototype admission work.'
        ], visual_acceptance=False))
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope=scope,
        reviewer=REVIEWER, limitations=LIMITS, reviewed_reader=report['pdf'],
        acceptance_scope='proposal_only', criteria=criteria,
        outputs=[ref(output, 'Contracted R-identification coverage outcome')],
        revisit_trigger='A preserving coverage successor must inspect remaining leads, historical snapshot and taxonomy boundaries under a reviewed fixed budget.',
        nonexecution_reason='')
    write(BASE/'operation-receipt.json', receipt)
    transition('record', OP, BASE/'operation-receipt.json')
    print(json.dumps(dict(operation=OP, outcome='inconclusive', next='Continue independent ready operation.')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = dict(review=review, yield_for_publication=yield_for_publication,
                    publish=publish, renew=renew, record_cell=record_cell)
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
