#!/usr/bin/env python3
"""Preserve and publish the commercial dynamic-panel manuscript delta."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_dynamic_commercial_reader_20261019 as build
import dynamic_panel_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run=extension.base
core=run.core
ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Author source, arithmetic and extracted-text review; no rendered or independent acceptance.',
    'Eight-family commercial coverage remains inconclusive; edition, rights, prices and native comparison remain unresolved.',
    'Authored moment and calendar laws are not bank outcomes, commercial tests or calibrated confidence intervals.',
    'Mandatory repairs, Q1/Q5 and final acceptance remain open.']
read=lambda p:json.loads(p.read_text())


def contexts(index,excluded=()):
    return {r['citation_key']:Counter(json.dumps(c,sort_keys=True) for c in r['citation_contexts']
        if c['path'] not in excluded) for r in index['records']}


def verify():
    for name in ['prepared-inputs.json','source-audit-v2.json','anchor-review.json','review.json',
        'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
        'traceability-review.json','reader/source-audit.json','reader/build-report.json']:
        verify_bindings(read(BASE/name))
    prepared,report,audit,index=[read(BASE/n) for n in
        ['prepared-inputs.json','reader/build-report.json','reader/source-audit.json','traceability-review.json']]
    assert report['cited_records']==prepared['expected_cited_records']
    assert index['status']=='pass' and not index['issues']
    assert index['scholarly_pdfs']==prepared['expected_scholarly_pdfs']
    bounds=read(OUT/'text-layout-review.json')
    assert bounds['status']=='pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text()==build.expected_driver()
    assert exact.calculate()==read(BASE/'exact-results.json')
    prior=read(build.PRIOR)
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==prepared['prior_cited_records'] and all(new[k]==v for k,v in old.items())
    assert new.keys()-old.keys()=={'exec19_dynamic_stata_ab','exec19_dynamic_stata_system',
        'exec19_dynamic_stata_lp','exec19_dynamic_eviews_panel','exec19_dynamic_reference'}
    compiled={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256']==r['sha256'] for r in kept)
    before=contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after=contexts(index,{str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c==after[k] for k,c in before.items())
    pages=[' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts=[i for i,p in enumerate(pages) if 'A funding team may observe hundreds of branches' in p]
    assert len(starts)==1
    start=starts[0]
    ends=[i for i,p in enumerate(pages) if i>=start and 'Compare point estimates only when their targets agree' in p]
    assert len(ends)==1
    end=ends[0];text=' '.join(pages[start:end+1])
    for token in ['xtabond','xtdpdsys','lpirf','171','USD 2,010','USD 283','50.5',
        'MathWorks','institutional acceptance','initial-condition']:
        assert token in text,token
    equations={k:report['added_anchors'][k]['number'] for k in
        ['exec19:dynamic-model','exec19:dynamic-invalid','exec19:dynamic-valid',
         'exec19:dynamic-instruments','exec19:dynamic-calendar','exec19:dynamic-variance']}
    assert all('('+n+')' in text for n in equations.values())
    return report,dict(preserved_records=len(old),added_records=sorted(new.keys()-old.keys()),
        unchanged_compiled_inputs=len(kept),all_prior_citation_contexts_preserved=True,
        physical_pages=[start+1,end+1],equations=equations,visual_acceptance=False,native_execution=False)


def review():
    report,checks=verify()
    names=['prepared-inputs.json','source-audit-v2.json','anchor-review.json','review.json',
        'mathematical-review.json','copyedit-review.json','manuscript-plan-review.json',
        'traceability-review.json','exact-results.json','development.tex','reader/build-report.json',
        'reader/source-audit.json','reader/reader.txt','reader/text-layout-review.json']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],reviewer=REVIEWER,
        reviewed_reader=report['pdf'],scope='Preserving commercial dynamic-panel source and exact-example review',
        checks=checks,evidence=[ref(BASE/n,'Reviewed delta and preservation evidence') for n in names]+
            [ref(Path(__file__),'Exact preservation checks')],findings=[
            'Every prior citation identity, context and compiled chapter input survives.',
            'Four new official originals support selected Stata and EViews claims; existing six source identities remain unchanged.',
            'Instrument validity, covariance correction, predictive and structural targets stay distinct.',
            'Exact moment and calendar examples reproduce; no native commercial execution claimed.',
            'Coverage remains inconclusive with explicit omissions and no product-absence finding.'],
        limitations=LIMITS,visual_acceptance=False,final_acceptance=False))
    print(json.dumps(dict(review='pass',pages=report['pages'],checks=checks)))


def publish():
    report,_=verify();review_record=read(BASE/'release-source-review.json');verify_bindings(review_record)
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving dynamic-panel build'),
        source_review=ref(BASE/'release-source-review.json','Source, arithmetic and preservation review'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate dynamic-panel moment conditions, local projections and calendar uncertainty with a bounded commercial comparison.'],
        visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair a preserving sponsor successor to exact reader bytes.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed dynamic-panel working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_dynamic_commercial_reader',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],proposal_accepted=False)))


def renew():
    report,checks=verify();binding=ref(BASE/'working-release.json','Exact current reader')
    run.ledger.validate_working_release(ROOT,binding)
    findings={
        'Q2':f'All {checks["preserved_records"]} prior citation identities and contexts survive. Four authentic official originals and one authored reference add five records. Edition and acquisition limits, eight-family omissions and MathWorks403 remain explicit.',
        'Q3':'The selected system moment is1/2or0under declared initializations; common-calendar variance is1/T+1/(NT), checked with256states. Instrument count is(T-1)(T-2)/2. No general GMM or finite confidence guarantee is inferred.',
        'Q4':'At stipulated10000USDscale with100panels25dates, standard deviations are approximately2010and283USDunder actual and false-row laws. These are not observed losses or confidence intervals; prices and full costs remain open.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert run.same_reader(state['reader'],report['pdf'])
        previous=state['execution_runtime']['results'][identifier];old=core.read(ROOT,previous['path'])
        if old.get('reviewed_reader',{}).get('sha256')==report['pdf']['sha256']:continue
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,binding,ref(BASE/'release-source-review.json','Preserving author review'),
            ref(BASE/'source-audit-v2.json','Authenticated originals'),ref(BASE/'mathematical-review.json','Exact laws'),
            ref(Path(__file__),'Exact-reader author findings')]
        write(folder/'reopen.json',dict(reason='Changed reader requires preserving delta review.',prior_result=previous,
            reviewed_reader=report['pdf'],evidence=evidence,next_action='Record source, mathematical and economic dynamic-panel delta.'))
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
