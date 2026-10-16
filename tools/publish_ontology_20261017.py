#!/usr/bin/env python3
"""Review, record and publish a preserving variable-meaning proposal successor."""
import argparse
from collections import Counter
import json
from pathlib import Path
import build_ontology_reader_20261017 as build
import review_ontology_sources_20261017 as work
import ontology_reference_v2_20261017 as examples
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT,BASE,OUT,WORK=build.ROOT,build.BASE,build.OUT,build.WORK


def read(path):return json.loads(path.read_text())


def review():
    report,audit,prior=read(OUT/'build-report.json'),read(OUT/'source-audit.json'),read(build.PRIOR)
    index=read(BASE/'traceability-review.json')
    for obj in [report,audit,prior,index,read(BASE/'prepared-inputs.json'),read(WORK/'author-review.json')]:
        verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==185
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==677 and len(new)==686 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=read(build.PRIOR.parent.parent/'traceability-review.json')
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x,sort_keys=True) for x in row['citation_contexts'])-contexts[row['citation_key']]
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Variable meaning, ontology and the observation that a causal claim needs',
        'pooled accuracy is 0.89','USD 100','separate semantic scoring','nine-word phrase',
        'same observed','missing population','Triple-F1','another apparent scale']:
        assert phrase in text,phrase
    assert examples.calculate()==read(WORK/'exact-results-v2.json')
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Preserving ontology reader'),(OUT/'source-audit.json','686 source records'),
        (BASE/'traceability-review.json','185 genuine PDFs and preserved citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds'),(OUT/'reader.txt','Inspected integrated text'),
        (WORK/'source-review.json','Ten papers and pinned/local static source findings'),
        (WORK/'candidate-reassessment.json','Eight concrete candidate outcomes'),
        (WORK/'omissions-register.json','Two unresolved originals, score/version/rights and scientific gaps'),
        (WORK/'exact-results-v2.json','Six exact authored families'),(WORK/'arithmetic-review.json','Alternative exact checks'),
        (WORK/'proposed-contract.json','Typed observation, package choices and public/generated prototype'),
        (WORK/'author-review.json','Criterion review'),(WORK/'recovery-review.json','Crash recovery and authoring repair'),
        (work.OUTPUT,'Contracted task synthesis'),(Path(__file__),'Exact-reader review and transitions')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author primary, exact mathematical and extracted-text proposal review',
        'preserved_records':677,'new_records':9,'preserved_compiled_sources':len(kept),'original_contexts_retained':True,
        'evidence':evidence,'findings':read(WORK/'author-review.json')['findings']+[
            'Six genuine primary PDFs retained under title/first-author/year filenames.',
            'All predecessor sources and citation contexts preserved.',
            'Known limitations remain visible; no new upstream/model experiment or bank truth claimed.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'sections':report['ontology_sections']}))


def record():
    verify_bindings(read(BASE/'release-source-review.json'));author=read(WORK/'author-review.json')
    state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,work.OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',
        scope='Bounded variable-meaning and ontology proposal synthesis; no exhaustive census or capability qualification',
        reviewer=work.REVIEWER,limitations=work.LIMITS,capabilities=[],
        outputs=[ref(work.OUTPUT,'Reviewed variable meaning and ontology synthesis')],nonexecution_reason='',
        revisit_trigger='Permitted originals for candidates41/180; exact modified edition and OntoURL raw scales; complete permitted package/data/model paths; registered public/generated comparisons.',
        criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':[
            ref(WORK/'author-review.json','Criterion review'),ref(BASE/'release-source-review.json','Preserving reader integration')]}
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
        'build_report':ref(OUT/'build-report.json','Preserving ontology reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Integrate ten-paper variable-meaning discussion, pinned source findings and six exact authored examples.',
            'Develop typed observation mapping, metric/rights limits and public/generated comparison before expensive bank validation.'],
        'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed ontology successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status=status);state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_variable_ontology_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader']}))


def renew():
    report=read(OUT/'build-report.json');verify_bindings(read(BASE/'release-source-review.json'))
    findings={
        'Q2':'All677 inherited source records, citation contexts and compiled sources remain. Nine additions include six genuine primary PDFs, ten paper comparisons and pinned/local code paths. All686 records and185 genuine PDFs pass traceability; two missing originals, modified-edition and inconsistent-score limits remain explicit.',
        'Q3':'Six exact authored families reproduce differential measurement and equivalent observed laws, household/account weighting, units, availability, selected notes and document-link scoring. Literal counts independently check arithmetic; published findings, static code and proposed model evaluation remain distinct.',
        'Q4':'The investment argument gains a staged dictionary/ontology/constrained-extraction comparison. Pooled accuracy0.89 can coexist with a stipulated spuriousUSD100 per account, so benchmark completion cannot be assigned bank value. Retrieval, correction, adjudication, retries and maintenance are counted; expensive representative validation follows prototype merit.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=read(ROOT/previous['path'])
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),
            ref(BASE/'release-source-review.json','Inspected ontology delta'),ref(work.OUTPUT,'Task synthesis'),
            ref(WORK/'proposed-contract.json','Public/generated design and full cost'),ref(Path(__file__),'Review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor author review.',
            'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
            'next_action':'Record reviewed ontology delta with preserved evidence and limits.'})
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
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review','record','publish','renew']);a=parser.parse_args()
    {'review':review,'record':record,'publish':publish,'renew':renew}[a.command]()
