#!/usr/bin/env python3
"""Primary-byte interference comparison; source inspection only."""
import argparse
import hashlib
import json
from pathlib import Path
import interference_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/interference-reuse-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static inspection of two pinned distributions; no acquired code,package import or native benchmark executed.',
        'Exact examples are stipulated project calculations,not observed software performance or bank value.',
        'Primary copyright notices and dependency declarations do not clear the complete installed distribution.',
        'General contagion,dynamic networks,unobserved relationships,arbitrary group dependence and universal uncertainty remain unqualified.',
        'No fresh visual,independent,bank or final acceptance.']
SPECS={
 'mossspider':{
  0:[(1,21,'MIT notice and warranty limitation; no transitive clearance')],
  1:[(19,47,'Declared maintainer,Python classifiers and dependencies; most dependency versions unpinned')],
  2:[(1,1,'Distribution version0.0.3')],
  3:[(134,179,'Integer IDs,self-loop refusal,binary treatment,relabeling and unweighted adjacency'),(212,234,'Degree-based eligible population and excluded IDs'),(434,482,'Documentation promises endpoint shortcut while selected body rejects uniform deterministic plans; integer input rejected'),(486,568,'Targeting,pooled-policy means and two conditional variance outputs'),(793,851,'Estimated joint exposure/map density ratio and optional truncation'),(876,921,'Excluded nodes keep observed treatment while eligible nodes are resampled; mapping is rebuilt'),(1147,1208,'Direct residual-square variance and adjacency quadratic without PSD enforcement')],
  4:[(60,126,'Explicit ordered adjacency exposure map; matrix/vector identity and direction matter')],
  5:[(61,143,'Selected native test definitions cover node,loop,model,probability and type refusals; not executed')]},
 'inferference':{
  0:[(1,25,'Version1.0.3,dated CRAN publication,maintainer,GPL>=2 declaration and dependencies')],
  1:[(1,22,'Exported API names; no runtime qualification')],
  2:[(102,178,'Default allocation integration,ordered group construction,allocation range and group count checks'),(180,211,'Declared model routes and zero random-effect refusal')],
  3:[(36,93,'Point-weight path,derivative path and score orchestration')],
  4:[(13,43,'Overall estimate averages weighted group means using fixed group denominator and na.rm'),(47,74,'Treatment-level policy normalization and same fixed denominator')],
  5:[(28,86,'Quadrature failure becomes missing;TRUE reciprocal integral versusFALSE policy mass divided by integral'),(100,121,'Derivative helper consumes integrate_allocation formal but does not forward it into constructed gradient arguments'),(191,235,'Derivative array explicitly passesFALSE; helper forwarding must be considered jointly')],
  6:[(29,83,'Default integrand already divides observed allocation mass by proposed policy mass')],
  7:[(21,58,'Group-centered score crossproduct V matrix')],
  8:[(20,40,'Likelihood quadrature failure becomes missing before logarithm')],
  9:[(1,82,'Selected unit test definitions include weights and derivatives; no native execution or exhaustive testing claim')],
 10:[(38,58,'Group means normalize by group size,including treatment-specific subgroup sums')],
 11:[(134,179,'Robust score-matrix inverse and naive fixed-denominator variance; normal intervals without native qualification')]}}

def prepare():
 assert not (BASE/'review.json').exists()
 profiles={p['role']:p for p in read(BASE/'selected-profiles.json')}
 rows=read(BASE/'source-index-v2.json');records=[]
 for row in rows:
  p=ROOT/row['raw_path'];data=p.read_bytes();receipt=read(p.with_suffix('.receipt.json'))
  assert core.sha(p)==receipt['sha256']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['blob_sha']
  lines=data.decode().splitlines();i=int(row['key'].rsplit('_',1)[1]);anchors=[]
  for lo,hi,finding in SPECS[row['role']][i]:
   assert 1<=lo<=hi<=len(lines),(row['path'],lo,hi,len(lines))
   anchors.append(dict(lines=[lo,hi],finding=finding,excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest()))
  records.append(dict(role=row['role'],source_identity=row['url'],version_date=profiles[row['role']]['commit'],upstream_path=row['path'],local_copy=ref(p,'Authentic pinned source'),receipt=ref(p.with_suffix('.receipt.json'),'Acquisition identity'),git_blob_sha1=row['blob_sha'],inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
 assert len(records)==18
 write(BASE/'authenticated-source-review.json',dict(records=records,authenticated=18,inspected=18,source_execution=False))
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',evidence=[ref(Path(exact.__file__),'Independent exact code'),ref(BASE/'exact-results.json','Exact output')],findings=['Equal-group50 and equal-person20 differ for sizes2/8 and means100/0.','Directed row-neighbor sum000 differs from reversed010.','Keeping an excluded treated hub yields10 versus5/2 under all-node allocation1/4.','Default ratio-integrand weight1/4 becomes1/64 if allocation mass is multiplied again; derivatives-1/4 versus-1/64.','Missing-group fixed denominator40/3 differs from conditional20 and stipulated complete100/3.','Algebraic adjacency variance-2/9 contrasts with residual-square2/3; no native or asymptotic validity claim.','Illustrative2400USD/100submitted=24 versus/60usable=40.'],native_execution=False))
 rights={
  'mossspider':dict(version='0.0.3',license='MIT',owner='Paul Zivich',dependencies=['numpy','scipy','pandas','networkx>=2.0.0','matplotlib','statsmodels','patsy'],maintenance='Selected2022commit and named maintainer; no future support guarantee',limits='Most dependency versions unpinned; complete installed transitive rights and API compatibility unresolved'),
  'inferference':dict(version='1.0.3',license='DESCRIPTION declares GPL>=2',owner='Bradley Saul',dependencies=['R>=3.1','numDeriv>=2012.9-1','lme4>=1.1-6','Formula>=1.1-2','methods','spaMM'],maintenance='CRAN publication15May2025 and named maintainer; no support SLA',limits='GPL declaration inspected; exact distribution obligations and every dependency require qualified review before shipping')
 }
 write(BASE/'dependency-license-review.json',dict(candidates=rights,evidence=[ref(BASE/'authenticated-source-review.json','Identity,notice and dependency originals')],distribution_cleared=False))
 contract=dict(input=['Pinned artifact/runtime/dependencies','Bank decision,population,time andcurrency','Scientific graph direction or group membership and own-treatment/exposure map','Explicit eligible population and behavior of excluded nodes','Policy probabilities and full allocation law','Nuisance formulas,weight truncation and quadrature settings','Uncertainty law,confidence level andresampling seed'],output=['Target identity,equal-group/equal-person weights,policy contrast andunits','Node relabeling,group ordering andeligibility map','Point estimate and scientific status distinct from numeric availability','Native intervals with declared conditionality and sampling law','All group weights,missing/nonfinite values,quadrature and matrix diagnostics','Every submitted attempt and complete engineering/compute/review costs'],refusal=['Unknown edge semantics or mismatched group/individual target','Unsupported deterministic or dynamic policy','Missing required groups,zero support,nonfinite weights or negative/undefined variance','Unqualified transitive rights or unsupported dependency combination'],future_public_trials=['Asymmetric three-node direction fixture','Unequal group sizes and explicit target equality test','Endpoint and degree-restriction fixtures','Constant integrand and exact allocation-ratio/derivative oracle','Missing group and singular score-matrix propagation','Coverage evaluation only under an independently justified network/group sampling law'],integration_allowed=False)
 write(BASE/'conversion-contract.json',contract)
 sources=[]
 for role,profile in profiles.items():
  subset=[r for r in records if r['role']==role]
  source=dict(integrated_citation_key='exec24_interference_'+role,kind='software_source',name=role,title=role+' pinned target,allocation and uncertainty implementation review',author=rights[role]['owner'],year=2026,source_identity='https://github.com/'+profile['repo']+'/tree/'+profile['commit'],version_date=rights[role]['version']+';commit'+profile['commit']+';pre-cutoff selection',local_copy=ref(BASE/'authenticated-source-review.json','Pinned original records'),technical_sources=subset,inspected_anchors=[a for r in subset for a in r['inspected_anchors']],supported_claims=[c for r in subset for c in r['supported_claims']],limitations=LIMITS)
  sources.append(source)
  choice=dict(operation=profile['operation'],candidate=role,decision='reference',revision=profile,version=rights[role]['version'],source=source,rights_dependencies=rights[role],rationale=['Useful bounded target and diagnostic reference.','Explicit source discrepancies and numerical failure paths require native public qualification before integration.'],scientific_scope=('Fixed observed network,eligible-node stochastic intervention andconditional uncertainty;not arbitrary contagion' if role=='mossspider' else 'Grouped partial-interference allocation IPW with equal-group target andexplicit score/variance law'),alternatives=[dict(route='Original-language isolated worker',decision='conditional future',reason='Preserve fitted objects and semantics after rights andpublic conformance'),dict(route='Exact finite-policy oracle',decision='reference',reason='Known graph/group target andfailure semantics'),dict(route='Other reviewed package',decision='compare only matched targets',reason='Network andgroup targets differ by default'),dict(route='Whole-library port',decision='reject current scope',reason='No demonstrated benefit justifies new scientific andmaintenance burden')],costs=dict(observed_prices=False,categories=['adapter/dependency work','complete compute attempts','source/scientific/rights review','fault recovery andmaintenance'],illustrative=ref(BASE/'exact-results.json','2400USD example only')),owners=[dict(role=k,obligation=v) for k,v in [('Scientific','Own graph/group,policy,population andsampling law'),('Adapter','Preserve identities,weights,missing states,defaults anduncertainty'),('Platform/rights','Pin runtime andclear installed distribution'),('Evaluation','Independent public oracle,full failure denominators andcost')]],conversion_contract=ref(BASE/'conversion-contract.json','Proposed contract'),revisit_trigger='Named public prototype demand,complete installed rights andpreregistered direction,target,allocation,derivative,missingness,uncertainty,fault andfull-cost criteria.',limitations=LIMITS,integration_allowed=False,capabilities=[],native_execution=False,evidence=[ref(BASE/n,'Decision evidence') for n in ['authenticated-source-review.json','dependency-license-review.json','conversion-contract.json','mathematical-review.json']])
  verify_bindings(choice);write(BASE/(role+'-decision.json'),choice)
 sources.append(dict(integrated_citation_key='exec24_interference_reference',kind='project_evidence_not_scholarly_paper',title='Authored interference target,allocation,missingness andvariance witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;clientcutoff7October2026',local_copy=ref(BASE/'mathematical-review.json','Exact authored review'),inspected_anchors=[ref(BASE/n,'Authored contract') for n in ['exact-results.json','conversion-contract.json']],supported_claims=read(BASE/'mathematical-review.json')['findings'],limitations=LIMITS))
 write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',new_scholarly_pdfs=0,native_execution=False))
 write(BASE/'review.json',dict(status='pass_for_two_reference_decisions',evidence=[ref(BASE/n,'Reviewed unit') for n in ['initial-plan-review.json','authenticated-source-review.json','source-audit.json','dependency-license-review.json','conversion-contract.json','mathematical-review.json','mossspider-decision.json','inferference-decision.json']]+[ref(Path(__file__),'Inspection anddecision logic')],findings=['18authentic files inspected;three new audit records.','Two explicit reference decisions;no native capability or software coverage closure.'],limitations=LIMITS))
 print(json.dumps(dict(authenticated=18,inspected=18,records=3,native_execution=False)))

def receipt(role):
 state=core.read(ROOT,core.STATE);choice=read(BASE/(role+'-decision.json'));op=choice['operation']
 assert state['execution_runtime']['active']['operation']==op
 verify_bindings(read(BASE/'review.json'));verify_bindings(choice)
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
 value=dict(choice,status='pass',scope='Completed bounded proposal reference decision;no native admission')
 output=ROOT/node['outputs'][0];write(output,value)
 evidence=[ref(BASE/n,'Reviewed candidate') for n in ['review.json',role+'-decision.json','conversion-contract.json','dependency-license-review.json','exact-results.json']]
 result=run.ledger.receipt_template(node)
 findings=['Pinned identity,notices,dependencies andmaintenance inspected.','Target,policy,uncertainty,conversion,alternatives,costs,owners andrevisit trigger explicit.','Reference only;native qualification,rights andfull scientific uncertainty remain conditional.']
 result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=choice['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/(role+'-operation-receipt.json'),result)
 print(json.dumps(dict(operation=op,decision='reference',native_execution=False)))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','mossspider','inferference']);a=p.parse_args()
 prepare() if a.command=='prepare' else receipt(a.command)
