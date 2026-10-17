#!/usr/bin/env python3
"""Review and publish the preserving Copilot delta with exact-reader receipts."""
import argparse
import json
from pathlib import Path
import re

import build_copilot_reader_v2_20261017 as build
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, WORK, BASE, OUT = build.ROOT, build.WORK, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Original census remains37 inspected/76 unread among113 candidates, with4 cross-cutting records; Copilot is a separate citation-chain lead.',
    'Paper arXiv2504.13263v2 is dated2025-04-21. The source snapshot dated2026-05-15 is not bound to the paper experiments.',
    'Paper Table3 n5000 Copilot .668 versus prose .649, and very-large p100 versus prose p1000, remain unresolved.',
    'Truth-assisted conversion concerns inspected benchmark scoring paths, not live-discovery truth leakage or a reproduced2025 experiment.',
    'The conditional edit witness stipulates bootstrap frequencies and accepted C, stops after the LLM mutation and does not reproduce a full upstream run.',
    'Bootstrap covariance stability is not an upstream graph frequency, causal correctness probability or confidence interval.',
    'Two structural worlds and USD100/30 payoffs are authored examples, not general sharp bounds, sampled bank evidence or ROI.',
    'Root MIT and one vendored MIT notice do not close transitive, provider, asset, data or deployment rights; runtime qualification remains open.',
    'No exclusive chapter-depth, census closure or mandatory-repair acceptance is awarded. Q1/Q5 and final proposal acceptance remain open.',
    'Visual acceptance remains false under the exhausted inherited image allowance.']
NEXT = ('Continue complementary longitudinal/off-policy and negative-result originals; retain candidate27 as a scoped acquisition omission, '
        'and preserve the separate Copilot citation-chain denominator. Review outstanding L1/L2/I2/I4 chapter depth and sponsor reconciliation independently.')


def read(path):
    return json.loads(path.read_text())


def verify():
    for path in [BASE/'prepared-inputs.json', OUT/'build-report.json', OUT/'source-audit.json',
                 BASE/'traceability-review.json', WORK/'primary-review.json', WORK/'source-audit.json',
                 WORK/'citation-chain-register.json', WORK/'git-byte-validation.json', WORK/'recovery-review.json']:
        verify_bindings(read(path))
    report, audit = read(OUT/'build-report.json'), read(OUT/'source-audit.json')
    index, bounds = read(BASE/'traceability-review.json'), read(OUT/'text-layout-review.json')
    assert report['pages'] > 1025 and report['cited_records'] == 742
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 194
    assert bounds['status'] == 'pass' and not bounds['out_of_bounds'] and not bounds['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    kept = preservation.preserve(audit, index, build.PREDECESSOR, 738,
                                [str(build.OLD.relative_to(ROOT))])
    candidate_kept = preservation.preserve(audit, index, WORK, 742,
        [str((build.DOCS/'causal_proposal_copilot_reviewed_2026-10-17.tex').relative_to(ROOT))])
    bibliography = (BASE/'refs.bib').read_text()
    paper = next(s for s in read(WORK/'source-audit.json')['sources']
                 if s['integrated_citation_key'] == 'exec17_copilot_paper')
    expected_author = 'author={'+build.shared.escape(paper['author'])+'}'
    assert expected_author in bibliography and 'author={{Xinyue Wang' not in bibliography
    bbl = (OUT/(build.NAME+'.bbl')).read_text()
    paper_start = bbl.index(']{exec17_copilot_paper}')
    paper_entry = ' '.join(bbl[paper_start:bbl.find('\\bibitem', paper_start+1)].split())
    assert 'Xinyue Wang' in paper_entry and 'Biwei Huang' in paper_entry
    assert 'Wang et~al.' in bbl
    assert all(name in paper_entry for name in ['Kun Zhou', 'Wenyi Wu', 'Har~Simrat Singh',
        'Fang Nan', 'Songyao Jin', 'Aryan Philip', 'Saloni Patnaik', 'Hou Zhu',
        'Shivam Singh', 'Parjanya Prashant', 'Qian Shen'])
    oldkeys = {s['integrated_citation_key'] for s in read(build.PRIOR)['sources']}
    added = sorted({s['integrated_citation_key'] for s in audit['sources']}-oldkeys)
    assert added == ['exec17_copilot_code', 'exec17_copilot_exact', 'exec17_copilot_paper', 'exec17_copilot_rights']
    assert build.exact.serial(build.exact.calculate()) == read(WORK/'exact-results.json')
    aux = (OUT/(build.NAME+'.aux')).read_text()
    equations = {}
    for suffix in ['worlds', 'observed', 'stability', 'value', 'score', 'edit-input', 'guard']:
        label = 'exec17:copilot-'+suffix
        match = re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)', aux)
        assert match and re.fullmatch(r'\d+\.\d+', match.group(1)), label
        equations[suffix] = match.group(1)
    assert len(set(equations.values())) == 7
    pages = (OUT/'reader.txt').read_text().split(chr(12))
    physical_start = next(i for i, text in enumerate(pages, 1)
                          if 'An analyst who can run a discovery algorithm' in text)
    start = report['added_section_printed_pages']['development']
    end = report['added_section_printed_pages']['development-end']
    offset = physical_start-start
    selected = pages[physical_start-1:end+offset]
    for physical, text in enumerate(selected, physical_start):
        assert re.search(r'\b'+str(physical-offset)+r'\b', text)
    extracted = ' '.join(' '.join(selected).split())
    for phrase in ['0.96875', '46,656', '45,198', '531441/3200000', '0.668', '0.649',
                   '0.95', '0.05', 'without replacement', 'twenty bootstrap results',
                   'truth-assisted', 'MIT', 'CLI or MCP', 'USD 30']:
        assert phrase in extracted, phrase
    assert all('('+number+')' in extracted for number in equations.values())
    assert 'Wang et al., 2025' in extracted
    assert 'Xinyue Wang and Kun Zhou and' not in extracted
    return report, dict(preserved_records=738, preserved_first_candidate_records=742,
        first_candidate_unchanged_tex_files=candidate_kept, shortened_scholarly_citations=True,
        unchanged_compiled_tex_files=kept,
        canonical_citation_contexts='Unchanged predecessor multisets', added_sources=added,
        new_section_printed_pages=[start, end], new_section_physical_pages=[physical_start, end+offset],
        equations=equations, exclusive_depth_credit=None, census_closed=False, visual_acceptance=False)


def review():
    report, checks = verify()
    evidence = [ref(p, 'Reviewed Copilot evidence') for p in [OUT/'build-report.json',
        OUT/'source-audit.json', OUT/'text-layout-review.json', OUT/'reader.txt',
        BASE/'traceability-review.json', BASE/'prepared-inputs.json', WORK/'primary-review.json',
        WORK/'exact-results.json', WORK/'citation-chain-register.json', WORK/'git-byte-validation.json',
        WORK/'recovery-review.json', WORK/'omissions.json', build.EXTENSION,
        ROOT/'tools/copilot_reference_20261017.py', BASE/'repair-plan.json', Path(__file__)]]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[],
        scope='Author primary-source, static-path, preservation, mathematical and extracted-page delta review',
        reviewer=REVIEWER, reviewed_reader=report['pdf'], checks=checks, evidence=evidence,
        findings=[
            'All738 predecessor source records, compiled sources and citation-context multisets survive. Four added audited records include one genuine scholarly PDF, exact historical source, two bounded MIT notices and authored references.',
            'The manuscript develops business translation, method-selection authority, stable observational ambiguity, source-specific experimental limits, scoring information and a conditional graph-edit witness.',
            'Seven equation numbers, extracted new pages and independently enumerated observed/interventional laws, bootstrap sequences, scoring and conditional guard values agree.',
            'Temporal summary, lag storage, reachable ts=False call, without-replacement branch, runtime boundary, test exclusions and incomplete environment/rights are explicitly scoped.',
            'The adoption assessment names useful components, required repairs and the proposal own missing integrated experience and qualification. No upstream run or automatic depth acceptance is claimed.',
            'The first candidate remains preserved after a scholarly author-serialization failure. This successor retains all742 candidate records and citation contexts, parses thirteen scholarly authors and uses shortened in-text citations.',
            'All-page text bounds and source traceability pass without material compilation warnings; rendered visual acceptance remains pending.'],
        unresolved_source_issues=read(WORK/'primary-review.json')['source_limits'],
        limitations=LIMITS, whole_census_closed=False, depth_acceptance=False,
        final_acceptance=False, visual_acceptance=False))
    write(BASE/'census-yield.json', dict(
        finding='Copilot paper and separate2026 static snapshot integrated with exact examples and bounded adoption decisions; original census remains37 inspected/76 unread.',
        next_action=NEXT, yield_reason='Publish the preserving reviewed working PDF and renew Q2-Q4 on that exact identity; eligible work continues afterward.',
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
        build_report=ref(OUT/'build-report.json', 'Preserving Copilot reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(WORK/'source-audit.json', 'Copilot primary-source and exact-reference audit')],
        changes=['Integrate an autonomous-discovery workflow and component adoption assessment into the L4 development.',
            'Develop exact stable-association, truth-assisted scoring and conditional graph-edit examples.',
            'Preserve paper/code version separation, unresolved source discrepancies, proposal deficits and incomplete original census.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed Copilot working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_copilot_source_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All738 predecessor source records and citation-context multisets survive.742 audited records retain194 genuine scholarly PDFs. Copilot paper and separate historical code have exact identities, hashes and inspected anchors. Both paper discrepancies, bounded rights and separate census denominator remain explicit.',
        'Q3': 'Seven equations, independent finite observed/interventional and bootstrap enumerations, two-node scoring and conditional graph-edit guard reproduce. All-page text bounds and extracted-page review pass without material warnings. Static paths are not upstream execution; no exclusive depth or visual acceptance is awarded.',
        'Q4': 'Two stipulated worlds share the observed law but have offer effects.8 and0; hypothetical USD100 contribution/30 cost yield USD50/-30 incremental values. Conditional bootstrap stability31/32 does not identify the effect or bank ROI. Actual complete workflow value and prices remain unmeasured.'}
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
            ref(WORK/'primary-review.json', 'Inspected paper and historical code'),
            ref(WORK/'exact-results.json', 'Authored exact examples'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded Copilot source, mathematical and economic delta.'))
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
