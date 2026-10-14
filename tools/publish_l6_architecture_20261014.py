#!/usr/bin/env python3
"""Publish scoped L6 development without claiming complete backend coverage."""
import argparse
import json
from pathlib import Path

import build_l6_architecture_v2_20261014 as build
import review_l6_architecture_20261014 as review
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT


def publish():
 state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
 assert state['execution_runtime']['active'] is None
 assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
 assert all(k in state['execution_program']['results']for k in ['TEXT.DRAFT.L6','TEXT.REVIEW.L6'])
 report=json.loads((OUT/'build-report.json').read_text())
 audit=json.loads((OUT/'source-audit.json').read_text())
 source_review=json.loads((BASE/'release-source-review.json').read_text())
 verify_bindings(source_review);verify_bindings(json.loads(review.REVIEW.read_text()))
 manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
   'supersedes':{k:state['reader'][k]for k in ['path','sha256']},
   'build_report':ref(OUT/'build-report.json','Preserving730-page L6 successor'),
   'source_review':ref(BASE/'release-source-review.json','Source/mathematics and text review'),
   'text_layout':ref(OUT/'text-layout-review.json','All-page extraction and bounds'),
   'source_artifacts':audit['tex_files']+source_review['evidence']+[ref(review.REVIEW,'Inconclusive coverage review with10 substantive pages')],
   'visual_acceptance':False,'mandatory_repairs_closed':[],
   'changes':['Develop packages, backend contracts, three framework choices and local prototype baseline.',
              'Prove scoped state, reservation, adapter and comparison properties with exact project examples.',
              'Repair initial seven-page depth finding to ten; broader backend/framework census remains open.'],
   'sponsor_binding':'Preserved sponsor baseline; Q5 reconciliation remains open.'}
 write(BASE/'working-release.json',manifest)
 binding=ref(BASE/'working-release.json','Reviewed scoped L6 working successor')
 run.ledger.validate_working_release(ROOT,binding)
 state['execution_program']['working_releases'].append(binding)
 state['reader']={k:report['pdf'][k]for k in ['path','sha256']}
 state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
 state['deliveries'].append(dict(state['reader']))
 run.commit(ROOT,before,state,{'action':'publish_l6_architecture_reader','manifest':binding,'final_acceptance':False})
 print(json.dumps({'published':state['reader'],'L6_coverage':'inconclusive','proposal_accepted':False}))


def renew():
 report=json.loads((OUT/'build-report.json').read_text())
 findings={
  'Q2':'All534 earlier records are unchanged and original citation contexts retained. Thirteen keys gain reviewed L6 contexts; four project records bind exact derivations and preserved local evidence.538 records and156 scholarly PDFs. Broader backend/provider evidence omissions remain explicit.',
  'Q3':'Prior demonstrations are unchanged. Exact dependency, unknown-outcome, reservation, routing, affine-set, factorial and availability examples reproduce. No framework/provider execution or empirical model superiority is inferred.',
  'Q4':'Prior economic scenarios are retained. Stipulated routing, shared budgets and task-loss comparisons explain what a public/generated prototype should measure before a bank trial. No current model prices, bank benefit or measured ROI claimed.',
 }
 verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
 for q,finding in findings.items():
  identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
  assert state['reader']['sha256']==report['pdf']['sha256']
  previous=state['execution_runtime']['results'][identifier]
  old=json.loads((ROOT/previous['path']).read_text());folder=BASE/q;folder.mkdir(exist_ok=False)
  evidence=[previous,ref(BASE/'working-release.json','Exact current working reader'),
            ref(BASE/'release-source-review.json','Source and derivation review'),
            ref(review.REVIEW,'Explicit incomplete census and depth outcome'),
            ref(Path(__file__).resolve(),'Exact-reader review findings')]
  write(folder/'reopen.json',{'reason':'Changed reader requires a preserved successor review.',
        'prior_result':previous,'reviewed_reader':report['pdf'],'evidence':evidence,
        'next_action':'Record scoped L6 source/demonstration/economic review for exact reader.'})
  transition('reopen',identifier,folder/'reopen.json')
  state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state)
  node=run.ledger.operation(graph,identifier);attempt=len(state['execution_runtime']['review_history'][identifier])
  output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
  limits=list(dict.fromkeys(old['limitations']+review.LIMITS))
  scope='Author exact-reader delta review; proposal evidence only'
  write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],
        'reviewer':review.REVIEWER,'reviewed_reader':report['pdf'],'review_attempt':attempt,
        'acceptance_scope':'proposal_only','scope':scope,'findings':[finding],
        'evidence':evidence,'limitations':limits,'visual_acceptance':False})
  receipt=run.ledger.receipt_template(node)
  receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=review.REVIEWER,
      limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,acceptance_scope='proposal_only',
      outputs=[ref(output,'Current-reader'+q+'author review')],nonexecution_reason='',revisit_trigger='',
      criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
  write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
 print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['publish','renew']);args=parser.parse_args()
 {'publish':publish,'renew':renew}[args.command]()
