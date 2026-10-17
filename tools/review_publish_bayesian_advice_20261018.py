#!/usr/bin/env python3
"""Review and publish the primary-reviewed Bayesian-advice addition."""
import argparse
import json
from pathlib import Path
import re
import build_bayesian_advice_reader_20261018 as build
import bayesian_advice_reference_20261018 as exact
from collections import Counter
import build_integrated_monograph_v12 as shared
import master_control as core
import review_s3_20261017 as preservation
import run_program_reviews_v2 as extension
run=extension.base
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
CANONICAL=ROOT/'docs/program/execution/2026-10-17/integration-review-v1/v3'
CANONICAL_DRIVER=ROOT/'docs/causal_proposal_retention_reviewed_2026-10-17.tex'
LIMITS=[
 'Author source, mathematical and extracted-page review; no independent or rendered visual acceptance.',
 'Thesis experimental results are reported means, not newly reproduced trials or significance tests.',
 'Exact rational examples are project derivations; no DiBS, AGFN, DSPy or model-provider execution.',
 'Original census remains40 inspected/73 unread of113; source coverage and software decisions remain open.',
 'Q1/Q5 and all mandatory manuscript repair gates remain open.']
NEXT='Continue independent software, source coverage, L1/L6 and sponsor reconciliation; preserve omissions and commit/push recovery.'


def read(path):
 return json.loads(path.read_text())


def filtered_contexts(index, excluded):
 return {r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'] if x['path'] not in excluded) for r in index['records']}


def verify():
 for p in [BASE/'prepared-inputs.json',BASE/'plan-review.json',BASE/'mathematical-review.json',BASE/'source-audit.json',BASE/'primary-review.json',BASE/'copyedit-review.json',OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json']:
  verify_bindings(read(p))
 report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
 assert report['cited_records']==751 and index['scholarly_pdfs']==197
 assert index['status']=='pass' and not index['issues']
 bounds=read(OUT/'text-layout-review.json');assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert not [w for w in report['warnings'] if 'Underfull' not in w]
 assert build.DRIVER.read_text()==build.expected_driver()
 assert exact.calculate()==read(BASE/'exact-results.json')
 previous=read(CANONICAL/'reader/source-audit.json');old={x['integrated_citation_key']:x for x in previous['sources']};new={x['integrated_citation_key']:x for x in audit['sources']}
 assert len(old)==749 and all(new[k]==v for k,v in old.items())
 files={r['path']:r for r in audit['tex_files']};kept=[r for r in previous['tex_files'] if r['path']!=str(CANONICAL_DRIVER.relative_to(ROOT))]
 assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
 current=filtered_contexts(index,set());prior=filtered_contexts(read(CANONICAL/'traceability-review.json'),set())
 assert all(c==current[k] for k,c in prior.items())
 aux=(OUT/(build.NAME+'.aux')).read_text();equations={}
 for label in ['exec18:dag-conditioning','exec18:feedback-update']:
  m=re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)',aux)
  assert m and all(x.isdigit() for x in m.group(1).split('.')),label
  equations[label]=m.group(1)
 pages=(OUT/'reader.txt').read_text().split(chr(12));sections=report['added_section_printed_pages']
 matching=[(i+1,s) for i,s in enumerate(pages) if 'What an elicited Bayesian prior actually buys' in s and 'Response frequency is an elicitation quantity' in s]
 assert len(matching)==1
 start=matching[0][0];text=' '.join(' '.join(pages[start-1:start+8]).split())
 assert all('('+n+')' in text for n in equations.values())
 assert all(x in text for x in ['Videira','160.05','26.70','not significance tests','2000 observations','2001','conditional opportunity'])
 return report,dict(preserved_records=749,new_scholarly_records=1,new_project_records=1,unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,equations=equations,sections=sections,physical_start=start,exact_acyclic_edge_marginal='1/3',exact_feedback_posterior=['1/7','3/4','1/14','1/28'],reverse_ranking_auc=0,visual_acceptance=False)


def review():
 report,checks=verify()
 evidence=[ref(p,'Bayesian-advice source, mathematical and preservation evidence') for p in [BASE/'plan-review.json',BASE/'mathematical-review.json',BASE/'primary-review.json',BASE/'copyedit-review.json',BASE/'source-audit.json',BASE/'prepared-inputs.json',BASE/'traceability-review.json',OUT/'build-report.json',OUT/'source-audit.json',OUT/'reader.txt',OUT/'text-layout-review.json',BASE/'exact-results.json',Path(__file__)]]
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope='Preserving Bayesian-advice source-critical development',reviewer=REVIEWER,reviewed_reader=report['pdf'],checks=checks,evidence=evidence,findings=['All749 prior sources, compiled inputs and citation contexts preserved; one authentic thesis and one exact project reference added.','Mixed posterior graph metrics and unreported adverse feedback trials constrain the source conclusions.','The response-frequency/truth distinction, graph-conditioning example and categorical posterior are explicit.','Appendix seed/sample-count gaps and source semantic discrepancies remain visible; no native integration claimed.'],limitations=LIMITS,final_acceptance=False,visual_acceptance=False))

 print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report, _ = verify()
    review = read(BASE/'release-source-review.json')
    verify_bindings(review)
    assert review['status'] == 'pass' and review['issues'] == []
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(CANONICAL_DRIVER.with_suffix('.pdf').relative_to(ROOT))
    audit = read(OUT/'source-audit.json')
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving Bayesian-advice reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(BASE/'exact-results.json', 'Executed finite Bayesian references')],
        changes=['Integrate authentic Bayesian-discovery thesis, mixed results, exact conditional examples, semantic and reproducibility limits, and bounded reuse design.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed Bayesian-advice working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_bayesian_advice_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All749 predecessor records and196 scholarly PDFs survive unchanged; one authentic corrected thesis and one finite project reference yield751 records and197 scholarly PDFs. All prior citation contexts are identical.',
        'Q3': 'Exact acyclic conditioning, categorical feedback, reported-mean differences and reverse-ranking examples agree with numbered equations. Thesis results remain mixed and source-reported; repetition does not validate a truth likelihood. No upstream or visual acceptance inferred.',
        'Q4': 'No new bank price or empirical performance claim. Published E-SHD means are distinguished from new experiments and the numerical examples are conditional constructions; prior financial examples remain unchanged.'}
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
            ref(BASE/'source-audit.json','Thesis and project source evidence'),ref(BASE/'mathematical-review.json','Exact conditional Bayesian examples'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded Bayesian-advice source, mathematical and economic delta.'))
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
