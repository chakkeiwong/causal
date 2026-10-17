#!/usr/bin/env python3
"""Preserving author review and publication of advice/benchmark validity."""
import argparse
import json
from pathlib import Path
import re
import build_advice_validity_reader_20261017 as build
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write
ROOT, WORK, BASE, OUT = build.ROOT, build.WORK, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Original census remains37 inspected/76 unread of113; three separately inspected citation-chain leads do not close that denominator.',
    'Known true starting MEC and correct adviser likelihood are assumptions; posterior retention is not automatic fixed-truth coverage.',
    'Benchmark findings concern published v1 text, pseudocode and prompt, not uninspected upstream implementation.',
    'Survey69/72, Barley inclusion and bibliometric specificity remain unreconciled; linked manual-check details remain uninspected.',
    'Exact finite and Gaussian constructions are project examples, not sampled model accuracy, bank data or ROI.',
    'Code, rights, adviser calibration, scalable runtime and context alignment need prototype qualification.',
    'No exclusive-depth, census closure or mandatory-repair acceptance is awarded; Q1/Q5 and final proposal acceptance remain open.',
    'Visual acceptance remains false under the exhausted inherited image allowance.']
NEXT = ('Review the outstanding L1/L2/I2/I4 chapter depth independently, then continue the original source census, '
        'longitudinal/off-policy originals and sponsor reconciliation. Keep source omissions local; commit and push recovered work.')


def read(path):
    return json.loads(path.read_text())


def verify():
    for path in [BASE/'prepared-inputs.json', OUT/'build-report.json', OUT/'source-audit.json',
                 BASE/'traceability-review.json', WORK/'primary-review.json', WORK/'source-audit.json',
                 WORK/'citation-chain-register.json', WORK/'plan-review.json']:
        verify_bindings(read(path))
    report, audit = read(OUT/'build-report.json'), read(OUT/'source-audit.json')
    index, bounds = read(BASE/'traceability-review.json'), read(OUT/'text-layout-review.json')
    assert report['pages'] > 1030 and report['cited_records'] == 745
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 196
    assert bounds['status'] == 'pass' and not bounds['out_of_bounds'] and not bounds['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    kept = preservation.preserve(audit, index, build.PREDECESSOR, 742,
                                 [str(build.OLD.relative_to(ROOT))])
    oldkeys = {s['integrated_citation_key'] for s in read(build.PRIOR)['sources']}
    added = sorted({s['integrated_citation_key'] for s in audit['sources']}-oldkeys)
    assert added == ['exec17_advice_validity_exact', 'exec17_benchmark_consistency', 'exec17_imperfect_experts']
    assert build.exact.serial(build.exact.calculate()) == read(WORK/'exact-results.json')
    bibliography = (BASE/'refs.bib').read_text()
    bbl = (OUT/(build.NAME+'.bbl')).read_text()
    for source in read(WORK/'source-audit.json')['sources']:
        if source['kind'] != 'paper':
            continue
        assert 'author={'+build.shared.escape(source['author'])+'}' in bibliography
        start = bbl.index(']{'+source['integrated_citation_key']+'}')
        end = bbl.find('\\bibitem',start+1)
        entry = ' '.join(bbl[start:end if end >= 0 else len(bbl)].split()).replace('~',' ')
        for author in source['author'].split(' and '):
            assert build.shared.escape(author) in entry or author in entry, (author,entry)
    aux = (OUT/(build.NAME+'.aux')).read_text()
    equations = {}
    labels = ['advice-posterior','advice-retention','advice-chain','advice-repetition',
              'advice-coverage-premises','advice-coverage-composition','validity-markov',
              'validity-cancellation','validity-covariance','validity-graph','validity-opened-scm',
              'validity-opened-covariance','validity-binary','validity-balanced','validity-unknown']
    for suffix in labels:
        label = 'exec17:'+suffix
        match = re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)', aux)
        assert match and re.fullmatch(r'\d+\.\d+', match.group(1)), label
        equations[suffix] = match.group(1)
    assert len(set(equations.values())) == len(labels)
    pages = (OUT/'reader.txt').read_text().split(chr(12))
    sections = {}
    for name, opening in [('advice','A banking analyst may know'),('validity','A benchmark graph is a scientific object')]:
        physical_start = next(i for i,text in enumerate(pages,1) if opening in text)
        start = report['added_section_printed_pages']['exec17:'+name+'-development']
        end = report['added_section_printed_pages']['exec17:'+name+'-development-end']
        offset = physical_start-start
        selected = pages[physical_start-1:end+offset]
        for physical,text in enumerate(selected,physical_start):
            assert re.search(r'\b'+str(physical-offset)+r'\b',text)
        extracted = ' '.join(' '.join(selected).split())
        phrases = ['0.8901','0.9890','59049','59050','0.999983','Long et al., 2023'] if name=='advice' else ['38,081','27','512','256','Barley','11,633','USD 20','Zhang et al., 2026']
        for phrase in phrases:
            assert phrase in extracted, (name,phrase)
        assert all('('+v+')' in extracted for k,v in equations.items() if k.startswith(name+'-'))
        sections[name] = dict(printed=[start,end], physical=[physical_start,end+offset])
    return report, dict(preserved_records=742, unchanged_compiled_tex_files=kept,
        canonical_citation_contexts='Unchanged predecessor multisets', added_sources=added,
        sections=sections, equations=equations, exclusive_depth_credit=None,
        census_closed=False, visual_acceptance=False)


def review():
    report, checks = verify()
    evidence = [ref(p, 'Reviewed advice and benchmark evidence') for p in [OUT/'build-report.json',
        OUT/'source-audit.json', OUT/'text-layout-review.json', OUT/'reader.txt',
        BASE/'traceability-review.json', BASE/'prepared-inputs.json', WORK/'primary-review.json',
        WORK/'exact-results.json', WORK/'citation-chain-register.json', WORK/'omissions.json',
        build.EXTENSION, build.VALIDITY, ROOT/'tools/advice_validity_reference_20261017.py',
        WORK/'plan.md', WORK/'plan-review.json', Path(__file__)]]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[],
        scope='Author primary-source, mathematical, preservation and extracted-page delta review',
        reviewer=REVIEWER, reviewed_reader=report['pdf'], checks=checks, evidence=evidence,
        findings=[
            'All742 predecessor source records, compiled sources and citation-context multisets survive. Three added records include two genuine scholarly PDFs and independent exact references.',
            'L3 distinguishes known-MEC and adviser-law assumptions, joint legal-graph posteriors, repeated dependent advice, posterior mass and learned-class coverage premises.',
            'L7 develops positive-density Markov cancellation, conditioning-activated paths, nonsignificant dependent samples and selective unknown-answer targets.',
            'Fifteen numbered equations, independent graph enumeration, coefficient covariances and256 complete finite samples agree with manuscript claims.',
            'Adoption decisions retain retrieval and reviewed evidence triage while rejecting unsupported automatic relabeling; code, rights, runtime and calibration remain open.',
            'Both scholarly author lists serialize as individual people. All-page text bounds and traceability pass without material warnings; visual acceptance is pending.'],
        unresolved_source_issues=[s.get('unresolved_source_issues',[]) for s in read(WORK/'source-audit.json')['sources']],
        limitations=LIMITS, whole_census_closed=False, depth_acceptance=False,
        final_acceptance=False, visual_acceptance=False))
    write(BASE/'census-yield.json', dict(
        finding='Two genuine originals and exact references integrated into L3/L7; original census remains37 inspected/76 unread.',
        next_action=NEXT, yield_reason='Publish preserving working reader and renew exact-reader Q2-Q4; eligible work continues.',
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
        build_report=ref(OUT/'build-report.json', 'Preserving advice and benchmark validity reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(WORK/'source-audit.json', 'advice and benchmark validity primary-source and exact-reference audit')],
        changes=['Integrate joint imperfect-advice and learned-class retention analysis into L3.',
            'Integrate benchmark semantics, collider activation, nonsignificance and selective evidence analysis into L7.',
            'Preserve all predecessor evidence and state source limits, conditional adoption and prototype requirements.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed advice and benchmark validity working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_advice_validity_source_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All742 predecessor records and citation contexts survive;745 audited records retain196 genuine scholarly PDFs. Two exact-version papers have original bytes, hashes and inspected anchors. Original census closure, source discrepancies and code/rights inspection remain open.',
        'Q3': 'Fifteen numbered equations agree with exact graph posteriors, full active-path enumeration, Gaussian coefficient covariance and all256 binary sample sequences. Extracted new pages and all-page bounds pass without material warnings. No upstream, chapter-depth or visual acceptance is awarded.',
        'Q4': 'The stipulated randomized binary SCM has effect1/2; hypothetical USD100 outcome value andUSD30 cost imply incrementalUSD20. A nonsignificant four-row sample does not identify a zero effect or bank ROI. Full workflow prices and value remain unmeasured.'}
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
            ref(WORK/'primary-review.json', 'Inspected exact-version papers'),
            ref(WORK/'exact-results.json', 'Authored exact examples'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded advice and benchmark validity source, mathematical and economic delta.'))
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    {'review': review, 'publish': publish, 'renew': renew}[parser.parse_args().command]()
