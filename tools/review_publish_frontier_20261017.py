#!/usr/bin/env python3
"""Review and publish a preserving frontier delta without awarding census closure."""
import argparse
import json
import re
from pathlib import Path

import build_integrated_monograph_v12 as shared
import master_control as core
import prepare_frontier_successor_20261017 as build
import review_s3_20261017 as preservation
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
TRANCHE=build.previous.BASE
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=[
    'The inherited113-candidate corpus has35 inspected originals and78 unread; neither census closure nor search saturation is established.',
    'No exclusive chapter-depth credit or L1 acceptance is awarded; physical pages do not establish substantive depth.',
    'Chang Table4 is binary; three selected rows were checked against reported rounding. The separate L1 denominator inconsistency remains unresolved.',
    'OrcheCause adverse SHD and EpiCausalX heuristic, small-usability, future-validation and rights limits remain explicit.',
    'Exact examples are project constructions; no live model, upstream package, banking experiment or measured ROI was produced.',
    'Public observational data do not supply gold causal effects merely by being public.',
    'Visual acceptance remains false under the exhausted inherited image allowance.',
    'Overall proposal acceptance, Q1/Q5 and all three mandatory manuscript repairs remain open.']


def read(path):return json.loads(path.read_text())


def verify():
    for p in [BASE/'prepared-inputs.json',OUT/'build-report.json',OUT/'source-audit.json',
              BASE/'traceability-review.json',TRANCHE/'prepared-inputs.json',TRANCHE/'primary-review.json',
              TRANCHE/'census-register.json',TRANCHE/'task-map.json',BASE/'candidate-review.json']:
        verify_bindings(read(p))
    report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
    layout=read(OUT/'text-layout-review.json')
    assert report['pages']==1019 and report['cited_records']==735
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==191
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.EXTENSION.read_text()==build.corrected_extension()
    kept=preservation.preserve(audit,index,build.previous.PREDECESSOR,731,
                              [str(build.previous.OLD.relative_to(ROOT))])
    old=read(build.previous.OUT/'source-audit.json')
    assert {s['integrated_citation_key']:s for s in old['sources']}=={s['integrated_citation_key']:s for s in audit['sources']}
    changed={str(build.previous.DRIVER.relative_to(ROOT)),str(build.previous.EXTENSION.relative_to(ROOT))}
    files={r['path']:r for r in audit['tex_files']}
    assert all(files[r['path']]['sha256']==r['sha256'] for r in old['tex_files'] if r['path'] not in changed)
    # Only the explicitly repaired extension changes citation windows/path.
    old_contexts=preservation.contexts(read(build.previous.BASE/'traceability-review.json'),str(build.previous.EXTENSION.relative_to(ROOT)))
    current=preservation.contexts(index)
    assert all(not ctx-current[key] for key,ctx in old_contexts.items())
    tex=build.EXTENSION.read_text();expected={}
    for match in re.finditer(shared.CITE,tex):
        for key in match.group(1).split(','):
            expected.setdefault(key.strip(),[]).append(dict(path=str(build.EXTENSION.relative_to(ROOT)),
                line=tex.count('\n',0,match.start())+1,context=tex[max(0,match.start()-550):match.end()+220]))
    actual={r['citation_key']:[c for c in r['citation_contexts'] if c['path']==str(build.EXTENSION.relative_to(ROOT))] for r in index['records']}
    assert {k:v for k,v in actual.items() if v}==expected
    assert build.previous.exact.serial(build.previous.exact.calculate())==read(TRANCHE/'exact-results.json')
    aux=(OUT/(build.NAME+'.aux')).read_text();labels={}
    for label,number in [('transition','40.9'),('multiclass','40.10'),('scm','40.11'),('observed','40.12')]:
        match=re.search(re.escape('\\newlabel{exec17:frontier-'+label+'}{{')+r'([^}]+)',aux)
        assert match and match.group(1)==number
        labels[label]=number
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    assert all(re.search(r'\b'+str(physical-22)+r'\b',pages[physical-1]) for physical in range(554,560))
    assert 'three selected rounded rows' in pages[554]
    assert 'minusUSD' not in ''.join(pages[553:559])
    counts=read(TRANCHE/'census-register.json')['counts']
    assert counts['inspected_primary_retained_with_limits']==35 and counts['open_original_not_inspected']==78
    tasks=read(TRANCHE/'task-map.json')['task_families'];assert len(tasks)==14
    return report,dict(unchanged_canonical_tex_files=kept,preserved_canonical_records=731,
        preserved_candidate_records=735,canonical_citation_contexts='unchanged multisets',
        candidate_context_changes='Exactly corrected extension path and deterministic two-phrase repair',
        equations=labels,new_section_printed_pages=[532,537],new_section_physical_pages=[554,559],
        physical_span=6,exclusive_depth_credit=None,visual_acceptance=False)


def review():
    report,checks=verify()
    evidence=[ref(p,'Reviewed frontier evidence') for p in [OUT/'build-report.json',OUT/'source-audit.json',
        OUT/'text-layout-review.json',BASE/'traceability-review.json',BASE/'prepared-inputs.json',
        BASE/'candidate-review.json',TRANCHE/'primary-review.json',TRANCHE/'exact-results.json',
        TRANCHE/'census-register.json',TRANCHE/'task-map.json',TRANCHE/'citation-chains.json',
        TRANCHE/'search-observations.json',Path(__file__)]]
    write(BASE/'release-source-review.json',dict(status='pass',scope='Author source and mathematical delta review; no census/depth or final acceptance',
        reviewer=REVIEWER,reviewed_reader=report['pdf'],checks=checks,evidence=evidence,
        findings=[
            'All731 predecessor source records and citation-context multisets survive. The735-record first candidate remains preserved; its two wording defects are repaired deterministically.',
            'Three genuine inspected originals are integrated with explicit scientific, evaluation and rights boundaries.',
            'Four rendered equation numbers, both tables, six extracted pages, rational calculations and separate threshold enumeration agree.',
            'Complete observed-law equality coexists with positive, zero and negative intervention effects. Internal consistency and favorable observed fit do not establish causal identification.',
            'Public/generated prototype comparisons are proposals with predeclared requirements; none is described as an executed experiment.'],
        provenance_clarifications=[dict(record=ref(OUT/'build-report.json','Frozen builder output'),
            field='predecessor_pdf.anchor',original='Frozen683-page working reader',
            clarification='Inherited generic label only. Bound predecessor is the1014-page S9 PDF, exactly hash-verified; it is not a683-page reader.'),
            dict(field='pdf.anchor',clarification='Inherited native-software label; this exact successor adds frontier research discussion, not a new software execution.')],
        limitations=LIMITS,whole_census_closed=False,depth_acceptance=False,final_acceptance=False,visual_acceptance=False))
    write(BASE/'census-yield.json',dict(
        finding='Recovered build and genuine originals;35 inspected/78 unread across14 task families. Corrected first-reader wording in a preserving successor; census remains incomplete.',
        next_action='Continue candidate27 primary acquisition and the saved complementary longitudinal/off-policy and negative-result search. Inspect genuine originals and citation leads; do not claim census closure or L1 acceptance.',
        yield_reason='Publish the reviewed integrated delta and renew Q2–Q4 on its exact identity, then resume the independent census task.',
        evidence=evidence+[ref(BASE/'release-source-review.json','Reviewed source/math delta')]))
    print(json.dumps(dict(review='pass',pages=report['pages'],records=735,papers=191,census_closed=False,visual_acceptance=False)))


def publish():
    report,_=verify();verify_bindings(read(BASE/'release-source-review.json'))
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.previous.OLD.with_suffix('.pdf').relative_to(ROOT))
    audit=read(OUT/'source-audit.json');reviewed=read(BASE/'release-source-review.json')
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving frontier reader'),
        source_review=ref(BASE/'release-source-review.json','Source/math delta and explicit provenance clarifications'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=audit['tex_files']+reviewed['evidence']+[
            ref(TRANCHE/'source-audit.json','Three primary originals and an authored reference')],
        changes=['Integrate RCA, OrcheCause and EpiCausalX with scoped adverse results and limits.',
                 'Develop exact answer-transition and observational-equivalence banking examples.',
                 'Reconcile35 inspected/78 unread originals without awarding census or chapter acceptance.'],
        visual_acceptance=False,mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor baseline; Q5 reconciliation remains open.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed frontier working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_frontier_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,_=verify();verify_bindings(read(BASE/'working-release.json'))
    findings={
        'Q2':'All731 canonical records and citation-context multisets survive.735 audited records retain191 genuine scholarly PDFs; three newly inspected originals have identity, version/date, hash, primary anchors and bounded claims. All735 initial-candidate records are unchanged; corrected extension citation windows are exactly verified.35 inspected/78 unread originals do not establish complete literature or rights closure.',
        'Q3':'The four added equations, exact rational laws and independent threshold enumeration reproduce. Binary Table4 is correctly scoped; three selected rounding checks do not reconstruct its experiment. The L1 denominator conflict remains unresolved. All-page text bounds pass with no material compiler warnings; no exclusive depth or visual acceptance is awarded.',
        'Q4':'Identical positive observed joint cells permit effects+1/10,0,-1/10. At stipulated USD100 outcome value and USD5 offer cost, incremental values are USD5,-5,-15. The example proves an information distinction under its constructed law, not measured bank returns; public prototype and matched-cost evaluation remain proposed.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        if run.same_reader(old.get('reviewed_reader',{}),report['pdf']):
            assert old['outcome']=='pass';continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
            ref(BASE/'release-source-review.json','Preserving source/math delta'),
            ref(TRANCHE/'primary-review.json','Three inspected originals'),
            ref(TRANCHE/'exact-results.json','Exact authored laws and selected rounding checks'),
            ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires a preserving author delta review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,next_action='Record scoped frontier source, mathematical and economic delta.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author exact-reader delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
            findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Exact-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt)
        transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2–Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review','publish','renew'])
    args=parser.parse_args();{'review':review,'publish':publish,'renew':renew}[args.command]()
