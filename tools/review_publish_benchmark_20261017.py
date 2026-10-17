#!/usr/bin/env python3
"""Review and publish the benchmark delta, preserving open program obligations."""
import argparse
import json
from pathlib import Path
import re

import build_benchmark_reader_20261017 as build
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Inherited census remains incomplete:37 inspected/76 unread among113 original candidates, with4 cross-cutting records. New citation leads are separate.',
    'Published CELLO equal-task/ALL aggregation discrepancy is conditional on the stated equal100/task interpretation; cause and raw results remain unknown.',
    'The all-No robustness task is distinct from the original binary task balance. Question validity and answer polarity do not establish causal truth.',
    'CausalReasonBench public-release and on-request statements conflict; code, gold and raw results have not been executed or independently reproduced.',
    'Token-set example concerns CIR only; no full-composite or actual upstream regex exploit is asserted. Selected pilot correlation is not held-out validation.',
    'Financial payoffs, classifier rates and random-effects variances are project assumptions; no measured bank ROI, live-model calls or upstream engine execution.',
    'No exclusive chapter-depth or census closure is awarded. Q1/Q5, all three mandatory manuscript repairs and final proposal acceptance remain open.',
    'Visual acceptance remains false under the exhausted inherited image allowance.']


def read(path):
    return json.loads(path.read_text())


def verify():
    for path in [BASE/'prepared-inputs.json', OUT/'build-report.json', OUT/'source-audit.json',
                 BASE/'traceability-review.json', BASE/'primary-review.json', BASE/'source-audit.json',
                 BASE/'census-register.json', BASE/'task-map.json']:
        verify_bindings(read(path))
    report = read(OUT/'build-report.json')
    audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    bounds = read(OUT/'text-layout-review.json')
    assert report['pages'] > 1019 and report['cited_records'] == 738
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 193
    assert bounds['status'] == 'pass' and not bounds['out_of_bounds'] and not bounds['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    kept = preservation.preserve(audit, index, build.PREDECESSOR, 735,
                                [str(build.OLD.relative_to(ROOT))])
    previous = read(build.PRIOR)
    prior_keys = {s['integrated_citation_key'] for s in previous['sources']}
    added = sorted({s['integrated_citation_key'] for s in audit['sources']}-prior_keys)
    assert added == ['exec17_benchmark_cello', 'exec17_benchmark_cherif', 'exec17_benchmark_exact']
    assert build.exact.serial(build.exact.calculate()) == read(BASE/'exact-results.json')
    aux = (OUT/(build.NAME+'.aux')).read_text()
    equations = {}
    for suffix in ['rounding', 'score', 'accuracy', 'value', 'cluster-law', 'cluster-variance']:
        label = 'exec17:benchmark-'+suffix
        match = re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)', aux)
        assert match and re.fullmatch(r'\d+\.\d+', match.group(1)), label
        equations[suffix] = match.group(1)
    assert len(set(equations.values())) == 6
    pages = (OUT/'reader.txt').read_text().split(chr(12))
    physical_start = next(i for i, text in enumerate(pages, 1)
                          if 'A causal assistant can improve the wording' in text)
    printed_start = report['added_section_printed_pages']['development']
    printed_end = report['added_section_printed_pages']['development-end']
    offset = physical_start-printed_start
    selected = pages[physical_start-1:printed_end+offset]
    for physical, text in enumerate(selected, physical_start):
        assert re.search(r'\b'+str(physical-offset)+r'\b', text)
    extracted = ' '.join(' '.join(selected).split())
    for phrase in ['0.6875', '0.6825', '0.6925', '0.695', '0.705',
                   'Always withhold', '1.50', '4.00', 'selection set',
                   'reasonable request', '1,152', '4.5']:
        assert phrase in extracted, phrase
    assert all('('+number+')' in extracted for number in equations.values())
    counts = read(BASE/'census-register.json')['counts']
    assert counts['inspected_primary_retained_with_limits'] == 37
    assert counts['open_original_not_inspected'] == 76
    assert len(read(BASE/'task-map.json')['task_families']) == 14
    return report, dict(preserved_records=735, unchanged_compiled_tex_files=kept,
        canonical_citation_contexts='Unchanged multisets', added_sources=added,
        new_section_printed_pages=[printed_start, printed_end],
        new_section_physical_pages=[physical_start, printed_end+offset], equations=equations,
        exclusive_depth_credit=None, census_closed=False, visual_acceptance=False)


def review():
    report, checks = verify()
    evidence = [ref(p, 'Reviewed benchmark evidence') for p in [OUT/'build-report.json',
        OUT/'source-audit.json', OUT/'text-layout-review.json', OUT/'reader.txt',
        BASE/'traceability-review.json', BASE/'prepared-inputs.json', BASE/'primary-review.json',
        BASE/'exact-results.json', BASE/'census-register.json', BASE/'task-map.json',
        build.EXTENSION, ROOT/'tools/benchmark_reference_20261017.py', Path(__file__)]]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[],
        scope='Author primary-source, preservation, mathematical and extracted-page delta review',
        reviewer=REVIEWER, reviewed_reader=report['pdf'], checks=checks, evidence=evidence,
        findings=[
            'All735 predecessor source records, unchanged compiled sources and citation-context multisets survive. The reader adds two genuine exact-version originals and an authored exact reference.',
            'The connected evaluation section distinguishes scene-template labels, original binary balance, all-No refusal, answer reasons, lexical scores, metric selection and causal identification.',
            'CELLO aggregation and CausalReasonBench availability discrepancies are stated as unresolved source limits; neither is concealed or promoted to an experimental reproduction.',
            'Six equation numbers, extracted section pages, the table, exact fractions and separate integer/confusion/covariance enumerations agree.',
            'All-page text bounds and traceability pass without material compiler warnings. Public paired-case studies are proposed, not described as executed.'],
        unresolved_source_issues=read(BASE/'primary-review.json')['unresolved_source_issues'],
        limitations=LIMITS, whole_census_closed=False, depth_acceptance=False,
        final_acceptance=False, visual_acceptance=False))
    write(BASE/'census-yield.json', dict(
        finding='Two benchmark originals integrated with exact source-specific limits and reproducible banking references.37 inspected/76 unread; no census or chapter closure.',
        next_action='Review the acquired Causal-Copilot exact versions and citation-chain lead; continue candidate27 acquisition and complementary longitudinal/off-policy and negative-result originals. Preserve separate denominators for new leads.',
        yield_reason='Publish the reviewed preserving working PDF and renew Q2–Q4 on that exact identity; source work remains eligible afterward.',
        evidence=evidence+[ref(BASE/'release-source-review.json', 'Reviewed connected delta')]))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def publish():
    report, _ = verify()
    review = read(BASE/'release-source-review.json')
    verify_bindings(review)
    assert review['status'] == 'pass' and review['issues'] == []
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    audit = read(OUT/'source-audit.json')
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving benchmark reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(BASE/'source-audit.json', 'Two authentic benchmark originals and exact deductions')],
        changes=['Integrate CELLO and CausalReasonBench primary-text assessment into the evaluation chapter.',
            'Develop exact support-review value and mechanism-clustering examples.',
            'Retain unresolved source discrepancies and incomplete37-inspected/76-unread census.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed benchmark working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_benchmark_source_reader',
                                       manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All735 predecessor source records and citation contexts survive.738 records retain193 genuine scholarly PDFs. The two added benchmark originals have exact versions, identities, hashes and inspected primary anchors. Source discrepancies and the37-inspected/76-unread census remain explicit.',
        'Q3': 'Six added equations, exact rounding envelopes, integer totals, confusion-count values and covariance enumeration reproduce. All-page text bounds and extracted section review pass without material compiler warnings. Token invariance concerns CIR only; no raw source reproduction, exclusive depth or visual acceptance is awarded.',
        'Q4': 'Under a stipulated balanced support-review law and USD20/80 payoffs, rule A has accuracy.85/valueUSD4 and B has accuracy.875/valueUSD1.50. Constant withholding has zero value and perfect accuracy only in an all-unsupported test. These are authored sensitivity examples; actual bank payoffs and comparative model value remain unknown.'}
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
            ref(BASE/'primary-review.json', 'Two inspected originals and bounded claims'),
            ref(BASE/'exact-results.json', 'Exact deductions and banking laws'),
            ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded benchmark-source, mathematical and economic delta.'))
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
    print(json.dumps(dict(exact_reader_reviews='Q2–Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    {'review': review, 'publish': publish, 'renew': renew}[parser.parse_args().command]()
