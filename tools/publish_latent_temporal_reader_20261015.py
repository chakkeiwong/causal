#!/usr/bin/env python3
"""Review and publish the exact temporal-discovery proposal successor."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_latent_temporal_reader_20261015 as build
import review_latent_temporal_20261015 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def review():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==175
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==619 and len(new)==626 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for r in previous['records']:
        inherited=Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'])
        assert not inherited-contexts[r['citation_key']],r['citation_key']
    assert work.exact()==json.loads((work.BASE/'exact-results.json').read_text())
    text=' '.join((OUT/'reader.txt').read_text().split())
    phrases=['Temporal discovery with hidden causes','same observed bivariate Gaussian law',
        'not proportional','4.8%','99.5%','98.73%','406,781','dictionary-result path',
        'nine cells','five hundred','USD 3.2','unproposed model mass','union bound',
        'HTML rather than a genuine technical PDF']
    for phrase in phrases:assert phrase.lower() in text.lower(),phrase
    primary=json.loads((work.BASE/'primary-review.json').read_text())
    assert len(primary['papers'])==11 and len(primary['sources'])==22
    evidence=[ref(p,a) for p,a in [(OUT/'build-report.json','Exact preserving successor'),
        (OUT/'source-audit.json','626 traceable source records'),(BASE/'traceability-review.json','175 genuine scholarly PDFs;inherited citation uses retained'),
        (OUT/'text-layout-review.json','All-page text bounds and extraction'),(OUT/'reader.txt','Integrated temporal discussion'),
        (work.BASE/'primary-review.json','Eleven primary rereads and22 pinned blobs'),(work.BASE/'exact-results.json','Nine exact reference families'),
        (work.BASE/'conversion-and-study-contract.json','Concrete proposed repairs and comparison'),
        (work.BASE/'candidate-reassessment.json','Recovered originals and remaining coverage limits'),
        (work.BASE/'author-review.json','Scoped synthesis'),(Path(__file__),'Exact-reader checks')]]
    findings=[
        'Time order and equal Gaussian observed laws coexist with effects0/1 and stipulated net values-8/12USD.',
        'Direct finite-law cumulants and independent factor calculations verify the scalar-latent and nonzero-cumulant restrictions.',
        'Valid-IV example preserves observed law and complier effect while population effects differ;no universal IV identification claim.',
        'Five frontier roles and adjacent screening,hierarchy,prediction and workflow results retain their distinct targets and assumptions.',
        'Pinned code findings trace the actual caller,including its second cycle check,dict branch,discarded working matrix and prompt mismatch.',
        'The exact-reader successor preserves619 source records and all earlier citation contexts;seven records and three genuine papers are added.',
        'Known adapter/prototype routes and open general graph/effect coverage research are separated;no native/live performance or bank truth is inferred.'
    ]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
        'reviewed_reader':report['pdf'],'scope':'Author primary-source,math and exact-reader review;no independent acceptance',
        'evidence':evidence,'preserved_records':619,'new_records':7,'preserved_compiled_sources':len(kept),
        'original_contexts_retained':True,'findings':findings,'limitations':work.LIMITS,'visual_acceptance':False})
    print(json.dumps({'review':'pass','pages':report['pages'],'new_records':7,'sections':report['latent_temporal_sections']}))


def publish():
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    assert work.OP in state['execution_program']['results']
    report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
    reviewed=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(reviewed)
    manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
        'supersedes':{k:state['reader'][k] for k in ['path','sha256']},
        'build_report':ref(OUT/'build-report.json','Preserving temporal reader'),
        'source_review':ref(BASE/'release-source-review.json','Exact-reader review'),
        'text_layout':ref(OUT/'text-layout-review.json','All-page bounds'),
        'source_artifacts':audit['tex_files']+reviewed['evidence'],'visual_acceptance':False,'mandatory_repairs_closed':[],
        'changes':['Develop frontier temporal/latent roles and three recovered originals.',
            'Trace22 pinned source blobs and derive nine exact semantic,mathematical and banking references.',
            'Specify prototype repairs and comparison while retaining unresolved effect-set calibration and search coverage.'],
        'sponsor_binding':'Preserved sponsor baseline;Q5 reconciliation remains open.'}
    write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed temporal working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,{'action':'publish_latent_temporal_reader','manifest':binding,'final_acceptance':False})
    print(json.dumps({'published':state['reader'],'proposal_accepted':False}))


def renew():
    report=json.loads((OUT/'build-report.json').read_text());verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
    findings={
      'Q2':'619 inherited records and all citation contexts retained;seven additions yield626 records and175 genuine scholarly PDFs. Three new publisher originals have cutoff-compatible identity,hashes and technical anchors;22 source blobs match exact trees. Missing originals and search limits remain explicit.',
      'Q3':'Inherited demonstrations retained. Nine exact references reproduce observational equivalence,cumulants,IV limits,temporal graphs,source conversions,coverage composition and information value. Eleven papers remain author-reported evidence;no upstream/live execution or general calibration claim.',
      'Q4':'Stipulated net outcomes-8/12USD and maximum perfect-information value3.2USD connect ambiguity to a banking decision. Public/generated prototype tests precede costly bank experiments. Actual prior,trial value,prices and ROI are not inferred.'}
    for q,finding in findings.items():
        identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
        assert state['reader']['sha256']==report['pdf']['sha256']
        previous=state['execution_runtime']['results'][identifier];old=json.loads((ROOT/previous['path']).read_text())
        folder=BASE/q;folder.mkdir(exist_ok=False)
        evidence=[previous,ref(BASE/'working-release.json','Exact current working reader'),
            ref(BASE/'release-source-review.json','Source,math and text review'),ref(work.OUTPUT,'Connected task synthesis'),
            ref(work.BASE/'exact-results.json','Exact authored constructions'),ref(Path(__file__),'Exact-reader findings')]
        write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.','prior_result':previous,
            'reviewed_reader':report['pdf'],'evidence':evidence,'next_action':'Record scoped temporal source,mathematical and economic review.'})
        transition('reopen',identifier,folder/'reopen.json')
        state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
        attempt=len(state['execution_runtime']['review_history'][identifier])
        output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
        limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review;proposal evidence only'
        write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
            'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
            'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=limits,
            reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
            outputs=[ref(output,'Current-reader '+q+' author review')],nonexecution_reason='',revisit_trigger='',
            criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
        write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
    print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['review','publish','renew']);args=parser.parse_args()
    {'review':review,'publish':publish,'renew':renew}[args.command]()
