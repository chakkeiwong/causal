#!/usr/bin/env python3
"""Preserve and review the exact R temporal working-reader successor."""
import argparse
import json
from pathlib import Path

import build_r_temporal_reader_v2_20261014 as build
import review_r_temporal_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT

def review():
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text());index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),json.loads((work.BASE/'author-review-v2.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass'and not index['issues']and index['scholarly_pdfs']==160
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not[w for w in report['warnings']if 'Underfull'not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==558 and len(new)==565 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']};kept=[r for r in prior['tex_files']if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256']for r in kept)
    prev=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
    assert all(all(c in contexts[r['citation_key']]for c in r['citation_contexts'])for r in prev['records'])
    changed=[r['citation_key']for r in prev['records']if contexts[r['citation_key']]!=r['citation_contexts']]
    assert set(changed)<={'exec13_pcalg','exec13_latentr_primary'}
    assert json.loads(json.dumps(work.exact()))==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Temporal order, dynamic prediction and intervention regimes in R','a factor of ten',
        'class UNKNOWN','finite default','minus one and plus','all-rejected models','separate tpc']:
        assert phrase.lower()in text.lower(),phrase
    evidence=[ref(p,anchor)for p,anchor in [
        (OUT/'build-report.json','Exact successor identity and compile warnings'),(OUT/'source-audit.json','565 bound citation records'),
        (BASE/'traceability-review.json','All old citation contexts and originals retained'),(OUT/'text-layout-review.json','All-page text bounds'),
        (OUT/'reader.txt','Inspected integrated development'),(work.BASE/'author-review-v2.json','Author source review'),
        (work.BASE/'primary-review.json','17 pinned blobs, original paper and inherited pcalg reread'),
        (work.BASE/'exact-results.json','Replayed rational calendar and aggregation examples'),
        (work.BASE/'reuse-decisions.json','Five proposed reuse routes'),(work.BASE/'omissions-register.json','Open coverage and conversion questions'),
        (work.BASE/'repair-review.json','Preserved metadata failure and successor repair'),(Path(__file__),'Exact preservation and review procedure')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
        'scope':'Exact-reader author review; selected R temporal coverage remains inconclusive','evidence':evidence,
        'preserved_records':558,'new_records':7,'preserved_compiled_sources':len(kept),'original_contexts_retained':True,
        'changed_existing_context_keys':changed,'findings':[
            'Tiered cohort order, lagged prediction, target invariance and known interventions have distinct contracts.',
            'Source/help discrepancies and existing dbnR ID filtering are faithfully retained; no upstream runtime is claimed.',
            'Original theorem assumptions, parent-set subset guarantee, finiteB and post-selection limits are explicit.',
            'Rational examples reproduce equal stationary observations with distinct effects, aggregation timing, boundaries and calendar variance.',
            'All original sources, contexts and records retained; no depth or repair completion awarded.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':7,'changed_contexts':changed}))

def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k]for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving R temporal reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Compare four new R source families and inherited pcalg with an authentic sequential-invariance original.',
            'Develop exact funding/calendar, aggregation and boundaries examples plus proposed semantic adapters.',
            'Keep complete coverage, conversion runtime and broader rights questions open.'],
        'sponsor_binding':'Preserved sponsor baseline; exact Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed R temporal successor')
    run.ledger.validate_working_release(ROOT,binding);state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k]for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_r_temporal_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))

def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={'Q2':'All558 original records and contexts retained; seven new records produce565 and160 genuine cited scholarly PDFs.17 selected blobs match pinned trees; scholarly version-date discrepancy is explicit.',
        'Q3':'Exact calendar laws, aggregation projection/impulses, series boundaries and shared-date variance reproduce. Source inspections and theorem statements are separated from unexecuted upstream R behavior and empirical calibration.',
        'Q4':'Stipulated funding contribution effects0/4 and net-1/3 thousandUSD illustrate missing identification, not ROI. Public/generated prototype cases distinguish semantic qualification from later bank validation.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact working reader'),ref(BASE/'release-source-review.json','Source/math/text author review'),
            ref(work.SYN,'Coverage incomplete; selected review complete'),ref(work.BASE/'primary-review.json','Versions and anchors'),
            ref(work.BASE/'exact-results.json','Exact illustrations'),ref(Path(__file__),'Exact-reader review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.','prior_result':previous,'reviewed_reader':report['pdf'],
            'evidence':evidence,'next_action':'Record exact-reader R temporal source/demo/economics review.'})
        transition('reopen',identifier,folder/'reopen.json');state=core.read(ROOT,core.STATE)
        graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review; proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
            'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
            limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',outputs=[ref(output,'Current-reader '+q+' author review')],
            nonexecution_reason='',revisit_trigger='',criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);a=p.parse_args()
    {'review':review,'publish':publish,'renew':renew}[a.command]()
