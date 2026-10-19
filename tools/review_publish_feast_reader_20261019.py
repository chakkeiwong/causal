#!/usr/bin/env python3
"""Preserve prior evidence and publish the reviewed Feast proposal delta."""
import argparse
from collections import Counter
import json

import build_feast_reader_20261019 as build
import feast_clock_reference_20261019 as exact
import master_control as core
import run_program_reviews_v2 as extension
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author source, exact arithmetic and extracted-text review; no rendered visual or independent acceptance.',
    'The conditional Feast proposal choice grants no executable admission, native conformance or bank qualification.',
    'Authored availability-clock economics are distinct from source tests and observed product value.',
    'Full software/LLM/integration repairs, Q1/Q5 and final acceptance remain open.']
read = lambda p: json.loads(p.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    names = ['prepared-inputs.json', 'source-audit.json', 'identity-review.json', 'review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
        'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']
    for name in names:
        verify_bindings(read(BASE/name))
    prepared, report, audit, index = [read(BASE/n) for n in
        ['prepared-inputs.json', 'reader/build-report.json', 'reader/source-audit.json', 'traceability-review.json']]
    assert report['cited_records'] == prepared['expected_cited_records']
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs']
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == prepared['prior_cited_records'] and all(new[k] == v for k, v in old.items())
    assert new.keys()-old.keys() == {'exec19_feast_source', 'exec19_feast_reference'}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if "Consider a credit team replaying yesterday" in p]
    assert len(starts) == 1
    start = starts[0]
    ends = [i for i, p in enumerate(pages) if i >= start and 'Costs to measure include history retention' in p]
    assert len(ends) == 1
    end = ends[0]
    text = ' '.join(pages[start:end+1])
    for token in ['creation-time cutoff', 'USD 15', 'USD 0', 'thirty direct',
        'BigQuery', 'Dask', 'HTTP error', 'feast mcp', 'institutional acceptance']:
        assert token in text, token
    equations = {k: report['added_anchors'][k]['number'] for k in
        ['exec19:feast-eligible', 'exec19:feast-law', 'exec19:feast-value', 'exec19:feast-feasible']}
    assert all('('+n+')' in text for n in equations.values())
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys()-old.keys()),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        physical_pages=[start+1, end+1], equations=equations, visual_acceptance=False, native_execution=False)


def review():
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'identity-review.json', 'review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
        'traceability-review.json', 'exact-results.json', 'development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving Feast source, mathematical and extracted-page review',
        checks=checks, evidence=[ref(BASE/n, 'Reviewed delta and preservation evidence') for n in names]+
            [ref(Path(__file__), 'Exact preservation and review checks')],
        findings=['All prior citations, contexts and chapter inputs survive.',
            'Twenty original blobs authenticate to the7October2026commit and complete Git tree.',
            'The existing creation filter and provider support check are accurately described.',
            'Exact information-clock examples separate a15USD unavailable-rule value from0USD feasible value.',
            'Historical, latest online and state-changing MCP operations have distinct contracts.'],
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
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving Feast build'),
        source_review=ref(BASE/'release-source-review.json', 'Source, mathematical and preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate Feast historical clocks, provider contracts, exact banking consequences and distinct MCP surfaces.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Create a preserving sponsor successor paired to these exact reader bytes.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed Feast working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_feast_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': f'All {checks["preserved_records"]} prior citation identities and contexts survive. Twenty authenticated Feast originals and one exact authored reference add two citation records, with no new scholarly PDF. Version, rights, provider and native limits remain explicit.',
        'Q3': 'The exact four-state law yields type values30and-30USD, an unavailable-rule value15USD and value0for every rule measurable at the declared decision information. Source-row permutations, TTL edges, missingness and conflicting revisions have checked outcomes. Creation time is not automatically availability time.',
        'Q4': 'Assumed payoff100/cost50 distinguishes feasible value0from unavailable-information value15USD. It is not measured ROI or native software error. Data retention, joins, provider conversion, network and upgrade costs remain to be measured.'}
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
            ref(BASE/'source-audit.json', 'Authenticated originals'), ref(BASE/'mathematical-review.json', 'Exact target and value'),
            ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded Feast source, mathematical and economic delta.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader preserving delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0], reviewer=REVIEWER,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            scope=scope, findings=[finding], evidence=evidence, limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Exact-reader '+q+' author review')], nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    commands = dict(review=review, publish=publish, renew=renew)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
