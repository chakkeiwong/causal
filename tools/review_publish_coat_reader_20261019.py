#!/usr/bin/env python3
"""Preserve prior evidence and publish the reviewed COAT proposal delta."""
import argparse
from collections import Counter
import json

import build_coat_reader_20261019 as build
import coat_reference_20261019 as exact
import master_control as core
import run_program_reviews_v2 as extension
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author source, exact arithmetic and extracted-text review; no rendered visual or independent acceptance.',
    'The census remains incomplete; COAT runtime and general scientific guarantees are not qualified.',
    'Authored noisy-factor and dependence examples are distinct from source-reported results and general source proofs.',
    'Full software/LLM/integration repairs, Q1/Q5 and final acceptance remain open.']
read = lambda p: json.loads(p.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    names = ['prepared-inputs.json', 'source-audit.json', 'primary-review.json', 'review.json',
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
    assert new.keys()-old.keys() == {'exec19_coat', 'exec19_coat_reference'}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if 'Consider a servicing team with customer narratives' in p]
    assert len(starts) == 1
    start = starts[0]
    ends = [i for i, p in enumerate(pages) if i >= start and 'Public or stipulated gold factors' in p
            and 'remain later evidence' in p]
    assert len(ends) == 1
    end = ends[0]
    text = ' '.join(pages[start:end+1])
    for token in ['COAT-MB', 'COAT-PAG', 'COAT-ADJ', '75%', 'Gaussian', '1/16', 'USD 10',
        '1.90', '1.32', 'three times', '200 trading days', '400', 'conditional independence']:
        assert token in text, token
    equations = {k: report['added_anchors'][k]['number'] for k in
        ['exec19:coat-information', 'exec19:coat-noise-law', 'exec19:coat-covariance', 'exec19:coat-proxy-effect']}
    assert all('('+n+')' in text for n in equations.values())
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys()-old.keys()),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        physical_pages=[start+1, end+1], equations=equations, visual_acceptance=False, native_execution=False)


def review():
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'primary-review.json', 'review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
        'traceability-review.json', 'exact-results.json', 'development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving COAT source, mathematical and extracted-page review',
        checks=checks, evidence=[ref(BASE/n, 'Reviewed delta and preservation evidence') for n in names]+
            [ref(Path(__file__), 'Exact preservation and review checks')],
        findings=['All prior citations, contexts and chapter inputs survive.',
            'The2025v3paper is authentic and retained with explicit parsing, graph and sampling premises.',
            'Exact noisy-proxy and dependent-attempt examples reproduce without upstream execution.',
            'Model-specific RMSE and reported trading examples do not establish blanket superiority or bank economics.',
            'Census is49inspected/64unread; the independently blocked ACL candidate remains unread.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def yield_for_publication():
    report, _ = verify()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'LL.CENSUS'
    path = BASE/'publication-progress.json'
    write(path, dict(finding='COAT primary review and preserving reader pass source, exact arithmetic, citation and text checks; census49/64.',
        next_action='Publish COAT reader, renew exact-reader Q2-Q4, pair sponsor and continue independent eligible work.',
        evidence=[ref(BASE/'release-source-review.json','Bounded author review'), report['pdf']],
        yield_reason='Publication requires an idle active-operation slot; this scheduling transition is not a work stop.'))
    transition('yield','LL.CENSUS',path)


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
        build_report=ref(OUT/'build-report.json', 'Preserving COAT build'),
        source_review=ref(BASE/'release-source-review.json', 'Source, mathematical and preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate COAT representation, parsing and convergence assumptions with exact banking consequences and public prototype design.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Create a preserving sponsor successor paired to these exact reader bytes.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed COAT working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_coat_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': f'All {checks["preserved_records"]} prior citation identities and contexts survive. Authentic78page COATv3 dated13October2025 adds one scholarly PDF and an authored reference; two new records. Census49/64 and one independent acquisition-route rejection remain explicit.',
        'Q3': 'A75percent-accurate noisy factor leaves covariance3/64 and spurious standardized contrast1/5 under true effect0. Equal marginal proposal probabilities do not imply binomial useful-round counts. Source convergence uses a Gaussian approximation and is not imported as an exact finite guarantee.',
        'Q4': 'Assumed payoff100/cost10 gives proxy net10 versus true net-10. Source-reported model-specific RMSE and historical trading results are separated from measured project economics; timing, dependence and full costs remain proposed public checks.'}
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
            next_action='Record bounded COAT source, mathematical and economic delta.'))
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
    commands = dict(review=review, yield_for_publication=yield_for_publication, publish=publish, renew=renew)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
