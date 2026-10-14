#!/usr/bin/env python3
"""Review and register the exact CausalPy proposal-reader successor."""
import argparse
import json
from pathlib import Path

import build_causalpy_reader_20261014 as build
import review_causalpy_reuse_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT

def review():
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text());index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in[report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),json.loads((work.BASE/'author-review-v2.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass'and not index['issues']and index['scholarly_pdfs']==156
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not[w for w in report['warnings']if 'Underfull'not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==549 and len(new)==552 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']};kept=[r for r in prior['tex_files']if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256']for r in kept)
    prev=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
    assert all(all(c in contexts[r['citation_key']]for c in r['citation_contexts'])for r in prev['records'])
    changed=[r['citation_key']for r in prev['records']if contexts[r['citation_key']]!=r['citation_contexts']]
    assert set(changed)<={'v12_sw_rdrobust'}
    assert work.exact()==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in['CausalPy at a lending threshold','5.05','5.0005','singleton chain and draw dimensions',
        'minus USD 3','Integration remains disabled','Python 3.12']:
        assert phrase.lower()in text.lower(),phrase
    evidence=[ref(p,anchor)for p,anchor in[
        (OUT/'build-report.json','Exact successor PDF identity and counts'),(OUT/'source-audit.json','552 bound citation records'),
        (BASE/'traceability-review.json','Retained original citation contexts'),(OUT/'text-layout-review.json','All-page text bounds'),
        (OUT/'reader.txt','Inspected integrated development'),(work.BASE/'author-review-v2.json','Corrected author source review'),
        (work.BASE/'primary-review-v2.json','Twelve tree-matched original files'),(work.BASE/'exact-results.json','Replayed rational examples'),
        (work.BASE/'conversion-contract.json','Explicit proposed contract'),(Path(__file__),'Exact preservation and review procedure')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
        'scope':'Exact-reader author review; selected RD reference only','evidence':evidence,'preserved_records':549,'new_records':3,
        'preserved_compiled_sources':len(kept),'original_contexts_retained':True,'changed_existing_context_keys':changed,
        'findings':['Pinned source version1.0.0rc1 distinguished from prior metadata0.9.0.',
            'Finite5.05 versus cutoff5 and score-unit transformation reproduce exactly; identical observed laws do not settle continuity.',
            'Point, expected-outcome posterior and predictive semantics are explicitly separated.',
            'Design support, data lifecycle, licensing/environment boundaries and concrete reuse alternatives are developed.',
            'Public/generated prototype tasks are appropriate before bank experiments; integration remains disabled.',
            'All inherited manuscript source bytes and citation contexts retained. Two inaccurate source labels corrected in preserved successor review.'],
        'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':3,'changed_contexts':changed}))

def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active']is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k]for k in['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving CausalPy reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader author review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page text bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Develop sharp-RD local target and exact unit/identification examples.',
            'Distinguish posterior, predictive and singleton point outputs.',
            'Specify reference/deferred integration decision and public-prototype obligations.'],
        'sponsor_binding':'Preserved sponsor baseline; exact Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed CausalPy working successor')
    run.ledger.validate_working_release(ROOT,binding);state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k]for k in['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_causalpy_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))

def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={'Q2':'All549 original records and contexts retained; three new source/project records produce552.156 genuine scholarly PDFs. Twelve pinned CausalPy files and corrected source labels are auditable.',
        'Q3':'Preserved demonstrations plus exact cutoff5 versus finite5.05 and unit transformation5.0005 reproduce. Two identical observed laws have effects5 and0. Upstream CausalPy is not represented as executed.',
        'Q4':'Stipulated local net2 versus minus3 USD establishes dependence on design, not bank ROI. Full environment/sampling/review costs are proposed for public/generated prototype measurement before expensive bank studies.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE);assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact working reader'),ref(BASE/'release-source-review.json','Source/math/text author review'),
            ref(work.OUTPUT,'Reference decision; no enabled adapter'),ref(work.BASE/'primary-review-v2.json','Corrected authoritative source review'),ref(Path(__file__),'Exact-reader review findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.','prior_result':previous,'reviewed_reader':report['pdf'],
            'evidence':evidence,'next_action':'Record exact-reader scoped CausalPy source/demo/economics review.'})
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
