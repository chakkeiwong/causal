#!/usr/bin/env python3
"""Review and publish six evidence-backed L1 author-field corrections."""
import argparse
import json
from pathlib import Path
import re
import build_integration_depth_reader_20261017 as build
import integration_review_reference_20261017 as exact
from collections import Counter
import build_integrated_monograph_v12 as shared
import master_control as core
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write
ROOT,WORK,BASE,OUT=build.ROOT,build.WORK,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
CANONICAL=build.PREDECESSOR
CANONICAL_DRIVER=build.OLD
LIMITS=[
 'Author source, mathematical and extracted-page review; no independent or rendered visual acceptance.',
 'Proposed consumer reference uses preserved response fixtures; no fresh MCP, actual deployed client or bank trial.',
 'Publication, retention and capacity examples are finite authored constructions, not measured service levels.',
 'Original census remains37 inspected/76 unread of113; software coverage and sponsor reconciliation remain open.',
 'I2 and I4 have separate coverage/depth outcomes; no automatic MR03 or whole-proposal acceptance.',
 'Q1/Q5 and all mandatory manuscript repair gates remain open.']
NEXT='Record actual I2/I4 chapter reviews, then continue original literature/software coverage and sponsor reconciliation; commit and push recovery.'


def read(path):
 return json.loads(path.read_text())


def filtered_contexts(index, excluded):
 return {r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'] if x['path'] not in excluded) for r in index['records']}


def verify():
 for path in [BASE/'prepared-inputs.json',BASE/'plan-review.json',BASE/'mathematical-review.json',BASE/'evidence-review.json',BASE/'source-audit.json',OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json']:
  verify_bindings(read(path))
 report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
 assert report['cited_records']==748 and index['scholarly_pdfs']==196
 assert index['status']=='pass' and not index['issues']
 bounds=read(OUT/'text-layout-review.json');assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
 assert not [w for w in report['warnings'] if 'Underfull' not in w]
 assert build.DRIVER.read_text()==build.expected_driver()
 assert exact.calculate()==read(BASE/'exact-results.json')
 previous=read(CANONICAL/'reader/source-audit.json');old={x['integrated_citation_key']:x for x in previous['sources']};new={x['integrated_citation_key']:x for x in audit['sources']}
 assert len(old)==747 and all(new[k]==v for k,v in old.items())
 replaced={'docs/program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex','docs/program/execution/2026-10-13/operational-adoption/integration-preserving.tex',str(CANONICAL_DRIVER.relative_to(ROOT))}
 files={r['path']:r for r in audit['tex_files']};kept=[r for r in previous['tex_files'] if r['path'] not in replaced]
 assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
 current=filtered_contexts(index,set());prior=filtered_contexts(read(CANONICAL/'traceability-review.json'),replaced)
 assert all(not c-current[k] for k,c in prior.items())
 oldtex=(ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.I4/chapter.tex').read_text()
 corrected=re.sub(r'(?<=[A-Za-z0-9.])\\cite\{',r'~\\citep{',oldtex)
 assert (BASE/'operations-preserving.tex').read_text()==corrected
 assert Counter(re.findall(shared.CITE,oldtex))==Counter(re.findall(shared.CITE,corrected))
 for path in [BASE/'client.tex',BASE/'operations.tex',BASE/'operations-preserving.tex']:
  tex=path.read_text();expected={}
  for match in re.finditer(shared.CITE,tex):
   for k in match.group(1).split(','):
    expected.setdefault(k.strip(),[]).append(dict(path=str(path.relative_to(ROOT)),line=tex.count('\n',0,match.start())+1,context=tex[max(0,match.start()-550):match.end()+220]))
  actual={r['citation_key']:[c for c in r['citation_contexts'] if c['path']==str(path.relative_to(ROOT))] for r in index['records']}
  assert {k:v for k,v in actual.items() if v}==expected
 aux=(OUT/(build.NAME+'.aux')).read_text();equations={}
 for suffix in ['reachability','memory']:
  label='exec17:i4-'+suffix;m=re.search(re.escape('\\newlabel{'+label+'}{{')+r'([^}]+)',aux)
  assert m and re.fullmatch(r'56\.\d+',m.group(1)),label
  equations[label]=m.group(1)
 pages=(OUT/'reader.txt').read_text().split(chr(12));sections=report['added_section_printed_pages'];text=' '.join(' '.join(pages[sections['in:surfaces']+21:sections['exec17:integration-continuity-end']+22]).split())
 assert all('('+n+')' in text for n in equations.values())
 for term in ['Twelve','five','three','running','duplicate','retention']:
  assert term.lower() in text.lower(),term
 return report,dict(preserved_records=747,new_project_records=1,unchanged_compiled_inputs=len(kept),unrelated_citation_contexts_preserved=True,changed_contexts_recomputed=True,recorded_responses=11,adverse_cases=12,exact_reference_pass=True,equations=equations,sections=sections,visual_acceptance=False)


def review():
 report,checks=verify()
 evidence=[ref(p,'Reviewed integration source, mathematical and preservation evidence') for p in [BASE/'plan-review.json',BASE/'mathematical-review.json',BASE/'evidence-review.json',BASE/'initial-findings.json',BASE/'prepared-inputs.json',BASE/'traceability-review.json',OUT/'build-report.json',OUT/'source-audit.json',OUT/'reader.txt',OUT/'text-layout-review.json',Path(__file__)]]
 write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope='Preserving I2 client and I4 operations development',reviewer=REVIEWER,reviewed_reader=report['pdf'],checks=checks,evidence=evidence,findings=['All747 prior sources and unrelated manuscript/citation contexts preserved; one exact project reference added.','Proposed client reference distinguishes malformed replies, scientific dispositions, representation conflicts and job states.','Publication/cancellation, stable-root retention, additive memory admission and deterministic deadlines have bounded exact examples.','Historical trials are not misreported as fresh MCP or bank execution; source and all-page text checks pass.','I2/I4 depth has separate review; visual and whole-proposal acceptance remain open.'],limitations=LIMITS,final_acceptance=False,visual_acceptance=False))
 write(BASE/'chapter-yield.json',dict(finding='Integration successor passes source, exact-reference and extracted-text checks.',next_action=NEXT,yield_reason='Publish reviewed working successor and renew exact-reader Q2-Q4 before chapter outcomes.',evidence=evidence+[ref(BASE/'release-source-review.json','Reviewed working successor')]))
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
        build_report=ref(OUT/'build-report.json', 'Preserving integration depth repair reader'),
        source_review=ref(BASE/'release-source-review.json', 'Bounded source and mathematical review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=audit['tex_files']+review['evidence']+[
            ref(BASE/'exact-results.json', 'Executed finite consumer and operating references')],
        changes=['Develop I2 client admission and I4 crash publication, retention and capacity analysis; correct I4 citation spacing through preserving source copy.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed integration depth repair working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_integration_depth_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    run.ledger.validate_working_release(ROOT, ref(BASE/'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All747 predecessor records and196 scholarly PDFs survive; one finite project reference adds inspected code, outputs and source checks. All unaffected citation contexts remain unchanged.',
        'Q3': 'Eleven preserved response fixtures and twelve adverse consumer cases reproduce; publication, reachability, memory and deterministic queue examples pass. Two new equations and all-page text bounds pass; no full client or visual acceptance inferred.',
        'Q4': 'No actual prices or bank value added. Capacity and deadline figures are stipulated planning references; complete attempted-request and cost denominators remain explicit. Earlier L2 monetary repairs and examples remain unchanged.'}
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
            ref(BASE/'evidence-review.json','Preserved source and trial evidence'),ref(BASE/'mathematical-review.json','Finite consumer and operating constructions'), ref(Path(__file__), 'Exact-reader review findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded integration depth repair source, mathematical and economic delta.'))
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
