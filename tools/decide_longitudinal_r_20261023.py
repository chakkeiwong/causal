#!/usr/bin/env python3
"""Close proposal reuse choices without granting native integration."""
import argparse,json,re
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT;DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'longitudinal-r-decisions-v1';SOURCE=DAY/'longitudinal-r-reconciliation-v2';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
def fields(p):
 out={};key=None
 for line in p.read_text().splitlines():
  if line.startswith((' ','\t')) and key:out[key]+=' '+line.strip()
  elif re.match(r'^[A-Za-z][^:]*:',line):key,value=line.split(':',1);out[key]=value.strip()
 return out

def prepare():
 assert not (BASE/'review.json').exists();verify_bindings(read(SOURCE/'review.json'))
 licenses=[]
 for name,spans in [('exec22_riv_gpl2',[(60,104),(130,173)]),('exec23_longr_mit_standard',None)]:
  p=RAW/(name+'.txt');r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];lines=p.read_text().splitlines();spans=spans or [(1,len(lines))]
  licenses.append(dict(source_url=r['url'],version_date='GPL2 June1991' if 'gpl2' in name else 'CRAN standard MIT template;acquired24October2026 Asia/Shanghai',local_copy=ref(p,'Authentic license text'),acquisition=ref(p.with_suffix('.receipt.json'),'Source/date/hash'),inspected_anchors=[dict(lines=[a,b],text=chr(10).join(lines[a-1:b])) for a,b in spans],finding='Review actual source/distribution/notices obligations; no transitive clearance or native admission.'))
 write(BASE/'license-review.json',dict(status='pass_for_reference_choice',sources=licenses,limitations=['MIT template supplies standard terms with package year/holder fields; no blanket dependency rights clearance.','GPL>=2 selection and distribution arrangement need owner review; process isolation is not an automatic exemption.']))
 choices=[]
 for key,name,version,stem in [('060','stremr','0.4','exec23_longr_stremr_00'),('062','survtmle','1.1.1','exec23_longr_survtmle_00')]:
  desc=fields(RAW/(stem+'.txt'));assert desc['Version']==version
  source=next(x for x in read(SOURCE/'source-audit.json')['sources'] if x['integrated_citation_key']=='exec23_longr_'+name)
  choice=dict(operation='SW.DECISION.seed_'+key,decision='reference',name=name,version=version,identity=source,license=dict(declaration=desc['License'],review=ref(BASE/'license-review.json','Authentic selected standard terms'),package_holder=ref(RAW/'exec23_longr_survtmle_01.txt','Package year/holder') if name=='survtmle' else None,transitive_clearance=False),dependencies={k:desc.get(k,'') for k in ['Depends','Imports','LinkingTo','Suggests','NeedsCompilation']},maintenance='Selected cutoff CRAN mirror commit and declared package date only; age does not establish abandonment or SLA.',integration_allowed=False,capabilities=[])
  if name=='stremr':
   choice.update(target='Sequential treatment/monitoring regimes with typed histories and subject-level contributions; no arbitrary bank dependence qualification.',reason='Retain original R source as a prospective worker/reference. Monitoring and supplied/internal-weight paths are substantive; loop/residual and Qstratify tension require qualified tests.',failure_contract=['Reject simultaneous TMLE and iterative TMLE.','Return effective supplied/generated weights and actual truncation path.','Retain initial/iterative status separately and recompute final score before reporting convergence.','Qualify cap+1 updates, monitoring histories, positivity and ID/clock cases; do not claim observed failures from source.'])
  else:
   choice.update(target='Baseline-treatment cumulative incidence with declared event/censoring/horizon conventions; no automatic repeated-action policy interface.',reason='Retain original R hazard/mean implementations as bounded references. Method forwarding, source guard, scalar shape, sentinel and clock paths require explicit worker contracts.',failure_contract=['Preserve hazard Gcomp warning and effective TMLE method.','Validate requested events and one/multiple output shape before native admission.','Retain inner optimizer warnings, outer cap, final meanIC and covariance.','Detect character sentinels before list extraction; qualify irregular clocks and missing endpoints.'])
  choice.update(alternatives=[dict(route='Original pinned R worker',decision='preferred conditional prototype',reason='Preserves algorithm and audited semantics after native conformance.'),dict(route='Python/Java/C++ port',decision='reject for current proposal scope',reason='Duplicates learner, event, weight and uncertainty obligations without measured benefit.'),dict(route='Other longitudinal engine',decision='retain comparator',reason='lmtp,ltmle,gfoRmula and grf have different qualified regimes; match targets before costs or precision.'),dict(route='Exact authored reference',decision='retain semantic oracle',reason='Event, variance and stopping laws expose conversion errors without claiming upstream execution.')],costs=read(SOURCE/'conversion-contract.json')['costs'],owners=read(SOURCE/'conversion-contract.json')['owners'],revisit_trigger='Locked distribution/dependencies/rights, registered native conformance/failure cases, declared sampling-law uncertainty and matched complete costs.',limitations=read(SOURCE/'review.json')['limitations'])
  choices.append(choice)
 write(BASE/'choices.json',dict(choices=choices,evidence=[ref(SOURCE/'review.json','Reviewed integrated source comparison'),ref(BASE/'license-review.json','Additional terms inspection')]))
 evidence=[ref(BASE/n,'Reviewed prospective reference choice') for n in ['choices.json','license-review.json']]+[ref(SOURCE/n,'Existing verified source and semantics') for n in ['source-audit.json','review.json','conversion-contract.json','exact-results.json','development.tex']]+[ref(Path(__file__),'Decision logic')]
 review=dict(status='pass_for_two_reference_only_decisions',evidence=evidence,findings=['Two named engines and aliases bound to pinned authentic sources.','Targets, variance/failure contracts, alternatives, costs, owners and triggers explicit.','No integration allowed, native capability, complete rights clearance or survey closure.']);verify_bindings(review);write(BASE/'review.json',review);print('Two reference choices prepared.')
def receipt(key):
 op='SW.DECISION.seed_'+key;state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op;verify_bindings(read(BASE/'review.json'))
 value=next(x for x in read(BASE/'choices.json')['choices'] if x['operation']==op);evidence=[ref(BASE/'review.json','Reviewed choice'),ref(BASE/'choices.json','Target/rights/alternatives'),ref(BASE/'license-review.json','Authentic standard terms')]
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);out=ROOT/node['outputs'][0];value=dict(value,status='pass',scope='Completed proposal reference disposition; no native integration',evidence=evidence);write(out,value)
 r=run.ledger.receipt_template(node);findings=['Pinned source/version, standard license terms, direct dependencies and maintenance limits bound.','Target/uncertainty, alternatives, costs, owners and revisit trigger reviewed.','Reference-only choice; integration_allowed=false and capabilities empty; native conversion/failure qualification remains explicit.']
 r.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Reference-only decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=value['limitations'],capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger']);run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/(key+'-receipt.json'),r);print(op,'reference pass; no integration')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);p.add_argument('key',nargs='?');a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.key)
