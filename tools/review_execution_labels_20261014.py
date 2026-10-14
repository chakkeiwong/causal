#!/usr/bin/env python3
"""Audit execution evidence classes without rerunning or relabeling frozen trials."""
from collections import Counter
import hashlib,json,sys
from pathlib import Path
import run_program as control
import master_control as core
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.runtime_v12 import execution_identity
BASE=ROOT/'docs/program/execution/2026-10-14/execution-labels'
OUTPUT=ROOT/'docs/program/comprehensive-v14/work/IN.REQ.actual_vs_mocked_execution/requirement-review.json'
def ref(p,a):
 p=Path(p);return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':a}
def write(p,d):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 servicing=ROOT/'docs/program/execution/2026-10-14/servicing-journey'
 journal=json.loads((servicing/'local-journal.json').read_text());local=json.loads((servicing/'local-review.json').read_text())
 manifest=ROOT/'docs/program/repair-v12/work/IN04/implementation-manifest.json'
 manifest_data=json.loads(manifest.read_text());env=json.loads((servicing/'environment.json').read_text())
 current=execution_identity();assert current==env==manifest_data['execution_identity']
 transport_path=ROOT/'docs/program/repair-v12/work/IN04/transport-checks.json';transport=json.loads(transport_path.read_text())
 assert transport['status']=='pass' and transport['scientific_cases']==11 and len(transport['tool_names'])==9
 assert transport['protocol']=='2025-11-25'
 attempts=journal['attempts'];assert len(attempts)==98 and sum(x['passed'] for x in attempts)==94
 assert {x['route'] for x in attempts}=={'library','cli'}
 assert local['status']=='negative' and local['matched_frozen_expectations']==94
 unsupported=refused=failures=0
 examples=[]
 for a in attempts:
  r=a['response']
  if r['disposition'] in ('unsupported','refused'):
   assert r['result'] is None and r['qualification']['level']=='none'
   unsupported+=r['disposition']=='unsupported';refused+=r['disposition']=='refused'
  if r['status'] in ('failed','rejected'):failures+=1
  if a['phase']=='initial' and a['route']=='library':
   examples.append({'case':a['case'],'request_id':a['request']['request_id'],'operation':r['operation'],
      'execution_class':'actual_local_engine','input_origin':'project_generated','status':r['status'],
      'scientific_disposition':r['disposition'],'qualification':r['qualification']['level'],
      'numerical_result_returned':r['result'] is not None,'journal_anchor':a['id']})
 controller=ROOT/'docs/program/repair-v12/work/LA05/verification.json';agent=json.loads(controller.read_text())
 assert agent['combined_tests']==80 and agent['live_model_calls']==0
 classes=[
  {'label':'proposed','meaning':'An intended interface, workflow or engine admission not yet implemented','admissible_claim':'Design exists; no runtime availability','example':ref(ROOT/'docs/program/comprehensive-v14/work/IN.DESIGN.Java/adapter-contract.json','Java adapter design; selected engine admission deferred')},
  {'label':'static_source_inspection','meaning':'Original versioned source or technical documentation inspected','admissible_claim':'The named code path or documented contract says this; no package execution','example':ref(ROOT/'docs/program/execution/2026-10-14/java-latent/primary-review.json','Pinned FCI/RFCI and endpoint source; Java 21 environment unresolved')},
  {'label':'exact_project_reference','meaning':'An independently authored finite/rational/population calculation','admissible_claim':'The declared mathematical fixture reproduces; no third-party engine validation','example':ref(ROOT/'docs/program/execution/2026-10-14/estimation-validation/exact-oracle.json','Three population targets and score reversal')},
  {'label':'mock_or_consumer_double','meaning':'A substitute for an external backend or consumer','admissible_claim':'Contract behavior against the substitute only; external component never marked executed','example':ref(ROOT/'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.servicing/workflow-protocol.json','evidence_classes separates consumer doubles from actual dispatcher')},
  {'label':'actual_local_engine','meaning':'Actual named process/library and versioned code received bound requests and emitted recorded outcomes','admissible_claim':'Only the executed method/input/platform/result scope','example':ref(servicing/'local-journal.json','98 actual library/CLI invocations; no native servicing estimator')},
  {'label':'actual_local_transport','meaning':'Real protocol negotiation and calls against a named local server/client','admissible_claim':'Only the tested protocol/SDK/transport in the qualified environment','example':ref(transport_path,'11 library/CLI/MCP scientific parity cases; MCP 2025-11-25 local stdio')},
  {'label':'owner_run_external_consumer','meaning':'Named external owner actually executes the integration and attests the scoped result','admissible_claim':'Only the accepted consumer/configuration; distinct from bank causal truth','example':None,'status':'No such acceptance is established by this review'}]
 contract={'required_for_actual_execution':['Engine/source and schema hash','Runtime and dependency versions','Bound input identities and scientific context','Real route, request, result and failure journal','All-request denominator including cancellations/refusals','Execution time, resource scope and stopping rule','Distinct input origin and execution class','Qualification limited to claimed operation and environment'],
    'forbidden_promotions':['A static inspection cannot become a runtime result','A computed graph syntax check cannot become causal discovery','A project formula cannot become an engine estimate','A live numerical call with generated input cannot become bank data validation','A mock or replay cannot become an external owner run','A completed response with disposition unsupported/refused cannot become a returned estimate'],
    'later_cases':{'local':['Resolve full engine environments before third-party adapter admission','Test graph classes and endpoint roundtrips, unsupported methods, timeout and numerical failures','Record modern MCP/HTTP separately if implemented','Benchmark actual consumers with fixed protocol and complete cost denominator'],
                   'external_conditional':['Owner-run consumer conformance and actual custody/configuration','Independent scientific review of consequential assumptions','Bank assignment/measurement/transport validation only after prototype merit supports the expense']}}
 write(BASE/'evidence-labels.json',{'classes':classes,'contract':contract,'identity_current_matches_servicing_and_IN04':True,
  'execution_identity':current,'identity_sources':[ref(manifest,'Saved IN04 executed source/environment'),ref(servicing/'environment.json','Servicing source/environment')],
  'review_kind':'Evidence reinspection, no new runtime/transport study','limitations':['Transport trial retains sandbox anyio limitation; no new MCP run','Local runtime qualification is not bank causal validity']})
 write(BASE/'journal-review.json',{'review_kind':'Reinspection of immutable execution journal','journal':ref(servicing/'local-journal.json','All 98 frozen invocations'),
   'all_requests':98,'matched_expectations':94,'status':'negative','route_counts':dict(Counter(x['route'] for x in attempts)),
   'unsupported':unsupported,'refused':refused,'failed_or_rejected':failures,'initial_library_examples':examples,
   'expectation_correction':ref(servicing/'expectation-correction.json','Authored expected-error mismatch; actual corrupt bytes failed safely'),
   'runtime_claims':['Nine supported local operations only','No servicing policy estimator, graph discovery or live model backend'],
   'agent_controller':{'checks':80,'live_calls':0,'evidence':ref(controller,'Offline local synthetic conformance')},
   'qualification':'none beyond each original receipt'})
 review={'operation_id':'IN.REQ.actual_vs_mocked_execution','outcome':'pass','scope':'Proposal requirement and bound evidence labels; no new execution qualification',
   'classification':ref(BASE/'evidence-labels.json','Seven evidence classes and concrete promotion/acceptance contract'),
   'journal_review':ref(BASE/'journal-review.json','Actual local examples, unsupported/refused/failure states and preserved negative trial'),
   'source_identity':ref(ROOT/'src/causalbank/runtime_v12.py','execution_identity, invoke and dispatch failure paths'),
   'remaining_local_acceptance':contract['later_cases']['local'],'remaining_external_acceptance':contract['later_cases']['external_conditional'],
   'external_inputs_block_current_proposal':False,'original_gap_qualification':False,'capabilities':[],
   'limitations':['No third-party package or external consumer newly executed','No live agent, modern MCP, production or bank causal claim']}
 write(OUTPUT,review)
 graph,_,_=control.combined(ROOT,core.read(ROOT,core.STATE));node=control.ledger.operation(graph,review['operation_id']);receipt=control.ledger.receipt_template(node)
 ev=[ref(OUTPUT,'Reviewed integration requirement'),review['classification'],review['journal_review'],review['source_identity']]
 receipt.update(outcome='pass',execution='performed',scope=review['scope'],reviewer={'name':'Codex author/coordinator','kind':'author'},limitations=review['limitations'],capabilities=[],outputs=[ev[0]])
 for i,f in enumerate(['Current runtime identity matches two original executed evidence sets; design/static/reference/mock/local/transport/owner-run classes and exact remaining cases are bound.',
                       '98-slot local journal retains all semantic refusals and four frozen expectation mismatches; actual transport and offline controller scopes are separated, with no new external acceptance.']):receipt['criteria'][i].update(verdict='pass',finding=f,evidence=ev)
 write(BASE/'operation-receipt.json',receipt)
 print(json.dumps({'outcome':'pass','classes':7,'journal_slots':98,'preserved_negative':True,'identity_match':True,'new_engine_calls':0}))
if __name__=='__main__':main()
