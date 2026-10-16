#!/usr/bin/env python3
"""Review, publish and renew scoped acceptance for the topology reader."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_topology_reader_20261016 as build
import master_control as core
import run_program as run
import review_topology_v2_20261016 as work
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def review():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text());prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==175
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==634 and len(new)==639 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for r in previous['records']:
        assert not Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'])-contexts[r['citation_key']]
    assert work.exact()==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split()).lower()
    for phrase in ['preserving graph classes, coordinates and set geometry','9007199254740993',
                   'resulting singleton excludes','possibility-of-profit','native adapter','canonical encoding']:
        assert phrase in text,phrase
    evidence=[ref(p,a) for p,a in [
      (OUT/'build-report.json','Exact preserving topology successor'),(OUT/'source-audit.json','639 source records'),
      (BASE/'traceability-review.json','175 genuine scholarly PDFs;inherited citation contexts retained'),
      (OUT/'text-layout-review.json','All-page text bounds'),(OUT/'reader.txt','Extracted integrated argument'),
      (work.BASE/'runtime-probes.json','Twelve actual local case families'),(work.BASE/'node-roundtrip.json','Actual Node codec observations'),
      (work.BASE/'exact-results.json','Exact mathematical and banking references'),(work.BASE/'proposed-acceptance-contract.json','Proposed repair and acceptance cases'),
      (work.BASE/'author-review.json','Scoped author review'),(Path(__file__),'Exact-reader review logic')]]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,'reviewed_reader':report['pdf'],
      'scope':'Author source,math and text-layout review;not final or visual acceptance','evidence':evidence,
      'preserved_records':634,'new_records':5,'preserved_compiled_sources':len(kept),'original_contexts_retained':True,
      'findings':['New actual probes distinguish syntax-only admissions,correct refusals,coordinate-order and JSON numeric/digest boundaries.',
        'Exact finite and monetary examples support a proposed contract,with native adapters and scientific research still explicitly outstanding.',
        '634 inherited citation records and every inherited use remain;five additions give639 records and175 genuine scholarly PDFs.'],
      'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'sections':report['topology_sections']}))


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
      'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
      'build_report':ref(OUT/'build-report.json','Preserving topology reader'),
      'source_review':ref(BASE/'release-source-review.json','Exact-reader review'),
      'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
      'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
      'changes':['Integrate actual graph,set and coordinate counterexamples and Python/Node numeric/digest observations.',
        'Derive finite graph,Gaussian,financial and joint-set references.',
        'Propose six versioned contract groups with local prototype acceptance and later owner inputs.'],
      'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed topology working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']};state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_topology_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
      'Q2':'634 inherited records and all prior contexts retained;five traceable project additions yield639 records and175 genuine scholarly PDFs.Eight unchanged source/schema identities and actual local probe sources are bound.',
      'Q3':'Existing62 selected tests pass;12 actual local case families and Node JSON probes retained.Exact finite graph,equal-law Gaussian,coordinate,coverage and set-image references reproduce.No native adapter or general calibration inferred.',
      'Q4':'Stipulated net25 versus misread-5USD,orientation net2/-8USD and exact joint net-2 versus rectangle[-12,8] connect semantic losses to decisions.Public/generated prototype acceptance is specified before costly bank work.No real prices or ROI inferred.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current reader'),ref(BASE/'release-source-review.json','Source,math and text review'),
          ref(work.OUTPUT,'Scoped topology requirement'),ref(work.BASE/'exact-results.json','Exact references'),ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor review.','prior_result':previous,
          'reviewed_reader':report['pdf'],'evidence':evidence,'next_action':'Record scoped topology source,math and economic review.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review;proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
          'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
          'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
          limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
          outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
          criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);args=p.parse_args()
    {'review':review,'publish':publish,'renew':renew}[args.command]()
