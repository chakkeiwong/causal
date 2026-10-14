#!/usr/bin/env python3
"""Review and register the preserving local-failure evidence reader."""
import argparse
import json
from pathlib import Path
import build_failure_recovery_reader_20261014 as build
import review_failure_trials_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT

def review():
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text());index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass'and not index['issues']and index['scholarly_pdfs']==160
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not[w for w in report['warnings']if 'Underfull'not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==565 and len(new)==568 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']};kept=[r for r in prior['tex_files']if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256']for r in kept)
    prev=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
    assert all(contexts[r['citation_key']]==r['citation_contexts']for r in prev['records'])
    work.verify_observations()
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Recovery that preserves a causal request','invalid_request','before publishing its descriptor',
        'same report handle','production spawn counter excludes','not outage frequencies']:
        assert phrase.lower()in text.lower(),phrase
    evidence=[ref(p,a)for p,a in [
        (OUT/'build-report.json','Exact successor identity and warnings'),(OUT/'source-audit.json','568 citation records'),
        (BASE/'traceability-review.json','All inherited contexts and originals preserved'),(OUT/'text-layout-review.json','All-page text bounds'),
        (OUT/'reader.txt','Inspected integrated recovery development'),(work.BASE/'author-review.json','Reviewed proposal requirement'),
        (work.BASE/'local-observations.json','12 actual/instrumented cases'),(work.BASE/'cli-observations-v2.json','Three actual CLI cases'),
        (work.BASE/'primary-review.json','Five source records and inherited scope'),(work.BASE/'design-review.json','Proposed repairs, acceptance and owner inputs'),
        (work.BASE/'cli-probe-repair.json','Preserved post-save logging failure'),(Path(__file__),'Exact-reader preservation checks')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
        'scope':'Exact-reader author review; generated local proposal evidence','evidence':evidence,
        'preserved_records':565,'new_records':3,'preserved_compiled_sources':len(kept),'original_contexts_retained':True,
        'findings':['All original citations and contexts remain unchanged; three new project records bind observations and proposed repairs.',
            'Actual runtime, instrumented interruption and ordinary recovery are explicitly distinguished.',
            'Local orphan, checkpoint and acknowledgement cases preserve artifact and scientific identities.',
            'Corrupt-cache library exception and CLI misclassification are retained with concrete proposed repairs.',
            'No implementation, reliability-rate, monetary benefit or external acceptance is inferred.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':3,'prior_contexts':'unchanged'}))

def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k]for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving failure-recovery reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Develop semantic and operational failure distinctions with actual generated runtime and CLI evidence.',
            'Explain three publication windows, exact recovery identities and checkpoint refusal.',
            'Retain corrupt-cache classification gap and propose scoped acceptance cases.'],
        'sponsor_binding':'Preserved sponsor baseline; exact Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed failure-recovery successor')
    run.ledger.validate_working_release(ROOT,binding);state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k]for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_failure_recovery_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))

def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={'Q2':'All565 inherited citation records and contexts retained; three new project records produce568, with160 genuine cited scholarly PDFs unchanged. Current code, exact generated requests/results and proposed repairs are hash-bound.',
        'Q3':'Twelve actual/instrumented runtime cases and three actual CLI cases support the exact stated behaviors. First CLI run and summary-print failure are preserved without duplicate case credit. No reliability-rate, bank or live-MCP claim is added.',
        'Q4':'Recovery failure cases identify a bounded prototype repair and acceptance program before bank/platform trials. No new monetary, throughput or ROI estimate is asserted; prior exact-reader investment conclusions remain scoped.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact working reader'),ref(BASE/'release-source-review.json','Source/text/observation author review'),
            ref(work.SYN,'Proposal failure requirement'),ref(work.BASE/'local-observations.json','Actual/instrumented cases'),
            ref(work.BASE/'cli-observations-v2.json','CLI cases'),ref(work.BASE/'design-review.json','Unimplemented repair route'),
            ref(Path(__file__),'Exact-reader review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.','prior_result':previous,'reviewed_reader':report['pdf'],
            'evidence':evidence,'next_action':'Record exact-reader source/demo/economics review of failure evidence.'})
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
