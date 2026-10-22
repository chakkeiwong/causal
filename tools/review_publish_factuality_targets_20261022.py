#!/usr/bin/env python3
"""Review preservation and publish exact-reader factuality/target synthesis."""
import argparse
import json
from pathlib import Path
import build_factuality_targets_reader_v2_20261022 as build
import review_publish_observations_v2_20261022 as common
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run,core=common.run,common.core
ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=[
    'Author primary-text, source-preservation, mathematical and extracted rendered-text review; no independent or visual acceptance.',
    'Factuality survey descriptions of other experiments are not independent reviews of those originals.',
    'Weighted-target inference assumes identified group effects; exact known covariance/fixed classes differ from feasible estimation.',
    'No downloaded software, live model, paper implementation or public empirical dataset was executed.',
    '61/113 originals inspected,52 unread and four crosscutting search obligations remain; no census or software coverage closure.',
    'Q1/Q5, mandatory manuscript repairs, native qualification and bank adoption remain open.']
read=lambda p:json.loads(p.read_text())


def verify():
    for name in ['prepared-inputs.json','source-audit.json','plan-review.json','review.json',
      'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
      'traceability-review.json','reader/source-audit.json','reader/build-report.json']:
        verify_bindings(read(BASE/name))
    prepared,report,audit,index=[read(BASE/n) for n in
      ['prepared-inputs.json','reader/build-report.json','reader/source-audit.json','traceability-review.json']]
    assert report['cited_records']==prepared['expected_cited_records']==925
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==prepared['expected_scholarly_pdfs']==221
    bounds=read(OUT/'text-layout-review.json')
    assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.exact.calculate()==read(BASE/'exact-results.json')
    prior=read(build.PRIOR)
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==prepared['prior_cited_records']==922 and all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={s['integrated_citation_key'] for s in read(BASE/'source-audit.json')['sources']}
    compiled={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256']==r['sha256'] for r in kept)
    before=common.contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after=common.contexts(index,{str(p.relative_to(ROOT)) for p in [build.DEVELOPMENT,build.FACTUALITY_DEVELOPMENT]})
    assert all(v==after[k] for k,v in before.items())
    pages=[' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    sections={}
    for key,first,last,tokens,labels in [
      ('weighted_targets','A banking assistant translating an offer proposal must specify whose outcome',
       'for one target into evidence for another.',
       ['Vilfort','0.0009686482','7/12','90%','85%','U8','MCP'],
       ['exec22:targets-'+s for s in ['definition','experiment','class','value','wrong','geometry','bound','ci','point','set']]),
      ('factuality','A retrieved explanation of a lending policy can be well supported by its cited',
       'remain empirical questions for the bounded public prototype.',
       ['Wang','attribution','autoregressive','MCP','known-law'],[])]:
        starts=[i for i,p in enumerate(pages) if first in p];assert len(starts)==1,(key,starts)
        start=starts[0];ends=[i for i,p in enumerate(pages) if i>=start and last in p]
        assert len(ends)==1,(key,ends)
        end=ends[0];text=' '.join(pages[start:end+1]).replace('- ','-')
        for token in tokens:assert token in text,(key,token)
        equations={k:report['added_anchors'][k]['number'] for k in labels}
        assert all('('+n+')' in text for n in equations.values())
        sections[key]=dict(physical_pages=[start+1,end+1],equations=equations)
    return report,dict(preserved_records=len(old),added_records=sorted(new.keys()-old.keys()),
      unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,sections=sections,
      visual_acceptance=False,native_execution=False)


def review():
    report,checks=verify()
    names=['prepared-inputs.json','source-audit.json','plan-review.json','review.json','mathematical-review.json',
      'copyedit-review.json','manuscript-plan-review.json','traceability-review.json','exact-results.json',
      'targets-development.tex','factuality-development.tex','reader/build-report.json',
      'reader/source-audit.json','reader/reader.txt','reader/text-layout-review.json','text-review-attempt-1.json']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,reviewed_reader=report['pdf'],
      scope='Preserving factuality and weighted-target source, argument and rendered-text review',checks=checks,
      evidence=[ref(BASE/n,'Reviewed preserving integration') for n in names]+[ref(Path(__file__),'Exact delta checks')],
      findings=['All922 earlier citation identities/contexts and earlier compiled content inputs survive.',
        'Two genuine selected pre-cutoff originals and one labeled authored reference add distinct source/target safeguards.',
        'Normalized signed weights, population mixtures, target ambiguity and confounding have different meanings.',
        'Authored target ranges and analytic wrong-target probability reproduce; oracle geometry is distinct from feasible robust inference.',
        'Source coverage budgets protect different fixed-target and simultaneous-set events; estimated classes retain containment conditions.',
        'Source support, external correctness, causal validity, selected-target inference and cost are separate public evaluation outcomes.'],
      limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report,_=verify();record=read(BASE/'release-source-review.json');verify_bindings(record)
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
      supersedes={k:state['reader'][k] for k in ['path','sha256']},
      build_report=ref(OUT/'build-report.json','Preserving factuality/target build'),
      source_review=ref(BASE/'release-source-review.json','Primary-source and preservation review'),
      text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
      source_artifacts=read(OUT/'source-audit.json')['tex_files']+record['evidence'],
      changes=['Integrate weighted business targets, confidence events and source-support limits in the existing chapters.'],
      visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair preserving sponsor to exact current reader.')
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed factuality/target working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_factuality_targets_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,checks=verify();binding=ref(BASE/'working-release.json','Exact current reader')
    run.ledger.validate_working_release(ROOT,binding)
    findings={
      'Q2':f'All{checks["preserved_records"]} earlier source identities and citation contexts survive. Two genuine arXiv originals with printed-edition/date/author qualifications and one labeled authored reference add evidence. Survey descriptions are not independently reviewed experiments;61/52 census remains partial.',
      'Q3':'The normalized-weight definition, exact known-normal experiment, class sensitivity, attained Cauchy-Schwarz witness, minimax geometry and analytic wrong-target probability reproduce. Source fixed-target and simultaneous confidence budgets differ; feasible covariance/class containment conditions and noncentrality parameterization remain explicit. No robust solver or native package equivalence is claimed.',
      'Q4':'Stipulated group effects6/-2 and cost1 give baseline/alternative net3/-1; truncated-simplex worst-case net3-6epsilon crosses zero at1/2. This motivates target elicitation and matched public known-law/corpus comparisons before expensive bank experiments. No bank return, live-agent superiority or measured software integration value is asserted.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][identifier];old=core.read(ROOT,previous['path'])
        if old.get('reviewed_reader',{}).get('sha256')==report['pdf']['sha256']:continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,binding,ref(BASE/'release-source-review.json','Preserving author review'),
          ref(BASE/'source-audit.json','Audited primary sources'),ref(BASE/'mathematical-review.json','Exact scoped derivations'),
          ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserving delta review.',prior_result=previous,
          reviewed_reader=report['pdf'],evidence=evidence,next_action='Record source, mathematical and value delta for this reader.'))
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+LIMITS));scope='Author exact-reader preserving delta review; proposal evidence only'
        write(output,dict(operation=identifier,status='pass',criterion=node['criteria'][0],reviewer=REVIEWER,
          reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',scope=scope,
          findings=[finding],evidence=evidence,limitations=limits,visual_acceptance=False))
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
          reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
          outputs=[ref(output,'Exact-reader '+q+' review')],nonexecution_reason='',revisit_trigger='',
          criteria=[dict(index=0,verdict='pass',finding=finding,evidence=evidence)])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass',Q1_Q5='open',proposal_accepted=False)))


if __name__=='__main__':
    commands=dict(review=review,publish=publish,renew=renew)
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=commands)
    commands[parser.parse_args().command]()
