#!/usr/bin/env python3
"""Review and publish an exact preserving commercial-comparison reader."""
import argparse
import json
from pathlib import Path

import build_commercial_contracts_v2_20261014 as build
import review_commercial_identification_choice_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT

def review():
 report=json.loads((OUT/'build-report.json').read_text())
 audit=json.loads((OUT/'source-audit.json').read_text())
 prior=json.loads(build.PRIOR.read_text())
 index=json.loads((BASE/'traceability-review.json').read_text())
 for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
             json.loads((work.BASE/'author-review.json').read_text())]:verify_bindings(obj)
 assert index['status']=='pass'and not index['issues']and index['scholarly_pdfs']==156
 assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
 assert not[w for w in report['warnings']if 'Underfull'not in w]
 old={s['integrated_citation_key']:s for s in prior['sources']}
 new={s['integrated_citation_key']:s for s in audit['sources']}
 assert len(old)==538 and len(new)==549
 assert all(new[k]==s for k,s in old.items())
 files={r['path']:r for r in audit['tex_files']}
 kept=[r for r in prior['tex_files']if r['path']!=str(build.OLD.relative_to(ROOT))]
 assert all(files[r['path']]['sha256']==r['sha256']for r in kept)
 prev=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
 contexts={r['citation_key']:r['citation_contexts']for r in index['records']}
 assert all(all(c in contexts[r['citation_key']]for c in r['citation_contexts'])for r in prev['records'])
 changed=[r['citation_key']for r in prev['records']if contexts[r['citation_key']]!=r['citation_contexts']]
 selected={s['integrated_citation_key']for s in json.loads((work.BASE/'primary-review.json').read_text())['selected_inherited_records']}
 assert set(changed)<=selected
 assert work.calculate()==json.loads((work.BASE/'exact-results.json').read_text())
 text=' '.join((OUT/'reader.txt').read_text().split())
 for phrase in ['Abduction must preserve uncertainty about the borrower',
                'a back-door association path','an overstatement of USD 500',
                'JMP should now receive a substantive treatment comparison',
                'GBP 550 each','benchmark results to third parties']:
  assert phrase.lower()in text.lower(),phrase
 evidence=[ref(p,anchor)for p,anchor in[
  (OUT/'build-report.json','Exact compiled successor'),(OUT/'source-audit.json','549 bound citation records'),
  (BASE/'traceability-review.json','All original contexts preserved; new contexts inspected'),
  (OUT/'text-layout-review.json','All-page text and physical bounds'),
  (OUT/'reader.txt','Extracted commercial sections inspected'),
  (work.BASE/'author-review.json','Substantive claim/source/example review'),
  (work.BASE/'primary-review.json','Fourteen inherited and nine new official records'),
  (work.BASE/'exact-results.json','Replayed exact three-state structural example'),
  (work.BASE/'price-observation.json','Raw HTML confirms Commercial/GBP selection'),
  (work.BASE/'omissions-register.json','Incomplete edition/runtime/rights coverage'),
  (Path(__file__).resolve(),'Exact preservation and review procedure')]]
 write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,
  'scope':'Claim-limited exact-reader author review; full commercial coverage inconclusive',
  'reviewed_reader':report['pdf'],'evidence':evidence,'preserved_records':538,'new_records':11,
  'preserved_compiled_sources':len(kept),'original_contexts_retained':True,'changed_existing_context_keys':changed,
  'findings':['New technical text distinguishes criterion identification, estimation and individual structural counterfactuals.',
   'Replayed exact posterior1/2 versus point-substitution1; payoff480 versus980 USD under stipulated amounts.',
   'Official semantic ambiguity and API/uncertainty limitations explicitly prevent overclaiming.',
   'Release dates, source acquisition, actual edition entitlement and runtime execution remain distinct.',
   'JMP technical omission repaired from preserved primary prose; uninspected image equations remain excluded.',
   'Public Commercial/GBP prices and the linked agreement disclosure restriction are source-bound, with no assumed accepted rights.',
   'All earlier manuscript source bytes and citation contexts retained. No chapter-depth or mandatory-repair completion awarded.'],
  'limitations':work.LIMITS,'visual_acceptance':False})
 print(json.dumps({'review':'pass','pages':report['pages'],'new_records':11,'changed_contexts':changed,'coverage':'inconclusive'}))

def publish():
 state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
 assert state['execution_runtime']['active']is None
 assert state['reader']['path']==str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
 assert work.OP in state['execution_program']['results']
 report=json.loads((OUT/'build-report.json').read_text());audit=json.loads((OUT/'source-audit.json').read_text())
 source_review=json.loads((BASE/'release-source-review.json').read_text());verify_bindings(source_review)
 manifest={'kind':'working_monograph','final_acceptance':False,'pdf':report['pdf'],'pages':report['pages'],
  'supersedes':{k:state['reader'][k]for k in['path','sha256']},
  'build_report':ref(OUT/'build-report.json','Preserving commercial contract development'),
  'source_review':ref(BASE/'release-source-review.json','Exact-reader author source and mathematics review'),
  'text_layout':ref(OUT/'text-layout-review.json','All-page extraction and bounds'),
  'source_artifacts':audit['tex_files']+source_review['evidence'],
  'visual_acceptance':False,'mandatory_repairs_closed':[],
  'changes':['Add documented identification/abduction API and release/edition comparison.',
   'Develop exact posterior-preservation banking example and intervention-output interpretation.',
   'Reconcile public pricing/rights sources and cross-lane JMP treatment evidence, retaining unresolved families.'],
  'sponsor_binding':'Preserved sponsor baseline; exact Q5 reconciliation remains open.'}
 write(BASE/'working-release.json',manifest);binding=ref(BASE/'working-release.json','Reviewed commercial working successor')
 run.ledger.validate_working_release(ROOT,binding)
 state['execution_program']['working_releases'].append(binding)
 state['reader']={k:report['pdf'][k]for k in['path','sha256']}
 state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
 state['deliveries'].append(dict(state['reader']))
 run.commit(ROOT,before,state,{'action':'publish_commercial_contracts_reader','manifest':binding,'final_acceptance':False})
 print(json.dumps({'published':state['reader'],'proposal_accepted':False}))

def renew():
 report=json.loads((OUT/'build-report.json').read_text())
 findings={'Q2':'All538 earlier records and original contexts preserved; nine new original documentation records and two project records produce549.156 genuine scholarly PDFs. Four scoped commercial comparisons; other families and exact rights remain unresolved.',
  'Q3':'Prior demonstrations unchanged. Exact three-state counterfactual example reproduces prior1/3, posterior1/2 and mean-substitution1. No vendor binary or interface is represented as executed.',
  'Q4':'Stipulated alternative payoff480 versus980 USD is not incremental profit. Public version11 Commercial/GBP individual price and benchmark-disclosure conditions are source-bound; full deployment costs and actual rights remain unresolved. A narrow public/generated prototype precedes justified expensive trials.'}
 verify_bindings(json.loads((BASE/'release-source-review.json').read_text()))
 for q,finding in findings.items():
  identifier='PROPOSAL.'+q;state=core.read(ROOT,core.STATE)
  assert state['reader']['sha256']==report['pdf']['sha256']
  previous=state['execution_runtime']['results'][identifier]
  old=json.loads((ROOT/previous['path']).read_text());folder=BASE/q;folder.mkdir(exist_ok=False)
  evidence=[previous,ref(BASE/'working-release.json','Exact working reader'),
   ref(BASE/'release-source-review.json','Source/math/text review'),ref(work.OUTPUT,'Inconclusive complete commercial coverage'),
   ref(Path(__file__).resolve(),'Exact-reader review findings')]
  write(folder/'reopen.json',{'reason':'Changed reader requires preserved successor review.','prior_result':previous,
   'reviewed_reader':report['pdf'],'evidence':evidence,'next_action':'Record exact-reader scoped commercial source/demo/economics review.'})
  transition('reopen',identifier,folder/'reopen.json')
  state=core.read(ROOT,core.STATE);graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
  attempt=len(state['execution_runtime']['review_history'][identifier]);output=ROOT/run.review_output_paths(node,state['reader'],attempt)[0]
  limits=list(dict.fromkeys(old['limitations']+work.LIMITS));scope='Author exact-reader delta review; proposal evidence only'
  write(output,{'operation':identifier,'status':'pass','criterion':node['criteria'][0],'reviewer':work.REVIEWER,
   'reviewed_reader':report['pdf'],'review_attempt':attempt,'acceptance_scope':'proposal_only','scope':scope,
   'findings':[finding],'evidence':evidence,'limitations':limits,'visual_acceptance':False})
  receipt=run.ledger.receipt_template(node);receipt.update(outcome='pass',execution='performed',scope=scope,
   reviewer=work.REVIEWER,limitations=limits,reviewed_reader=report['pdf'],review_attempt=attempt,
   acceptance_scope='proposal_only',outputs=[ref(output,'Current-reader'+q+'author review')],
   nonexecution_reason='',revisit_trigger='',criteria=[{'index':0,'verdict':'pass','finding':finding,'evidence':evidence}])
  write(folder/'operation-receipt.json',receipt);transition('record',identifier,folder/'operation-receipt.json')
 print(json.dumps({'exact_reader_reviews':'Q2-Q4 pass','Q1_Q5':'open','proposal_accepted':False}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['review','publish','renew']);a=p.parse_args()
 {'review':review,'publish':publish,'renew':renew}[a.command]()
