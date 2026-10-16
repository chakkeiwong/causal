#!/usr/bin/env python3
"""Review and publish a preserving reporting/monitoring proposal successor."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_reporting_reader_v2_20261017 as build
import review_reporting_sources_20261016 as work
import reporting_reference_20261016 as examples
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT, BASE, OUT, WORK = build.ROOT, build.BASE, build.OUT, build.WORK


def read(path):
    return json.loads(path.read_text())


def review():
    report, audit, prior = read(OUT/'build-report.json'), read(OUT/'source-audit.json'), read(build.PRIOR)
    index = read(BASE/'traceability-review.json')
    for obj in [report,audit,prior,index,read(BASE/'prepared-inputs.json'),read(WORK/'author-review.json')]:
        verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==179
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==670 and len(new)==677 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=read(build.PRIOR.parent.parent/'traceability-review.json')
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x,sort_keys=True) for x in row['citation_contexts'])-contexts[row['citation_key']]
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Reporting causal results and monitoring their continued applicability',
        '71.3%', '87.9%', '12.8%', '28/30', '48/60', '.459640',
        'not even a member', 'schema-only', 'fifteen models', 'An LLM’s severity label']:
        assert phrase in text, phrase
    assert examples.calculate()==read(WORK/'exact-results.json')
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Preserving reporting reader'),(OUT/'source-audit.json','677 source records'),
        (BASE/'traceability-review.json','179 genuine PDFs and preserved citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds'),(OUT/'reader.txt','Inspected integrated text'),
        (WORK/'source-review.json','Nine papers and inspected package/local source paths'),
        (WORK/'candidate-reassessment.json','Seven concrete candidate outcomes'),
        (WORK/'omissions-register.json','Three unresolved original routes and implementation limits'),
        (WORK/'exact-results.json','Five exact authored reference families'),
        (WORK/'arithmetic-review.json','Alternative mathematical checks'),
        (WORK/'proposed-contract.json','Proposed report, applicability, monitoring and public comparison'),
        (WORK/'author-review.json','Criterion-specific review'),
        (WORK/'authoring-recovery.json','Preserved authoring error and repair'),
        (work.OUTPUT,'Contracted task synthesis'),(Path(__file__),'Exact-reader review and transitions')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author primary, exact-mathematical and extracted-text proposal review',
        'preserved_records':670,'new_records':7,'preserved_compiled_sources':len(kept),
        'original_contexts_retained':True,'evidence':evidence,
        'findings':read(WORK/'author-review.json')['findings']+[
            'Four genuine new primary PDFs retained under title/first-author/year filenames.',
            'All inherited source records, citation contexts and compiled content remain.',
            'No new live model, upstream execution, monitor implementation or bank claim.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'sections':report['reporting_sections']}))


def record():
    verify_bindings(read(BASE/'release-source-review.json'))
    author=read(WORK/'author-review.json')
    state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,work.OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',
        scope='Bounded reporting and monitoring proposal synthesis; no census or capability qualification',
        reviewer=work.REVIEWER,limitations=work.LIMITS,capabilities=[],
        outputs=[ref(work.OUTPUT,'Reviewed reporting and monitoring synthesis')],nonexecution_reason='',
        revisit_trigger='Accessible originals for candidates259/273/282; complete permissible package paths; registered fresh public/generated comparisons and valid selective/sequential inference.',
        criteria=[{'index':i,'verdict':'pass','finding':f,
                   'evidence':[ref(WORK/'author-review.json','Criterion review'),ref(BASE/'release-source-review.json','Preserving integration')]}
                  for i,f in enumerate(author['findings'])])
    write(BASE/'operation-receipt.json',receipt);transition('record',work.OP,BASE/'operation-receipt.json')


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None and work.OP in state['execution_program']['results']
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    status=state['reader']['status'];assert status=='Working monograph; not I02 acceptance'
    report,audit,reviewed=read(OUT/'build-report.json'),read(OUT/'source-audit.json'),read(BASE/'release-source-review.json')
    verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving reporting reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Integrate nine primary-paper comparisons, static package findings and a banking reporting argument.',
                   'Develop five exact reference families, version applicability, explicit monitoring ownership and a public/generated prototype contract.'],
        'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed reporting working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status=status);state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_reporting_monitoring_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader']}))


def renew():
    report=read(OUT/'build-report.json');verify_bindings(read(BASE/'release-source-review.json'))
    findings={
        'Q2':'All670 inherited records, citation contexts and compiled content remain. Seven additions include four genuine primary PDFs, nine paper rereads, pinned package/local source findings and explicit candidate gaps. The677 records and179 genuine PDFs pass traceability; broader census remains open.',
        'Q3':'Five exact authored families and alternative checks reproduce set-valued money, complete denominators, selective interval coverage, repeated-look alarms and dependency invalidation. Literature, static code, exact arithmetic and proposed model comparison remain separate; no live model or bank execution is claimed.',
        'Q4':'The preserved investment argument gains a deterministic-report baseline and staged public/generated comparison before expensive authentic trials. Conditional48/60 versus all-request48/100 success and stipulated net{-40,60} show why completion and midpoint gains misstate value. Review, retrieval, retries, storage and maintenance costs are explicit; no actual bank ROI is claimed.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
            ref(BASE/'release-source-review.json','Inspected reporting delta'),ref(work.OUTPUT,'Task synthesis'),
            ref(WORK/'proposed-contract.json','Public/generated comparison and full costs'),ref(Path(__file__),'Review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor author review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record reviewed reporting delta with preserved evidence and limits.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader proposal delta review'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
            'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','record','publish','renew']);a=p.parse_args()
    {'review':review,'record':record,'publish':publish,'renew':renew}[a.command]()
