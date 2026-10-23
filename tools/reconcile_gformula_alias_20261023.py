#!/usr/bin/env python3
"""Resolve exactly the already-authenticated gfoRmula seed alias."""
import json
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=controller.base;ROOT=run.core.ROOT;read=lambda p:json.loads(p.read_text())
BASE=ROOT/'docs/program/execution/2026-10-23/gformula-alias-v1'
OP='SW.DECISION.seed_061';CANONICAL='SW.DECISION.inherited_gformula'
SOURCE=ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1'

def main():
 assert not BASE.exists();BASE.mkdir()
 state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
 catalog=ROOT/'docs/program/gap-repair-v13/work/SW01/catalog.json'
 seed=next(x for x in read(catalog)['candidates'] if x['id']=='seed:061')
 assert seed['family_relation']['kind']=='same_project_alias' and seed['family_relation']['to']=='inherited:gformula'
 existing=merged['execution_program']['results'][CANONICAL];assert existing['outcome']=='pass'
 receipt=read(ROOT/existing['path']);verify_bindings(receipt)
 canonical_path=ROOT/receipt['outputs'][0]['path'];canonical=read(canonical_path)
 identity=read(SOURCE/'identity-review.json');verify_bindings(identity)
 assert identity['repository']=='CausalInference/gfoRmula' and identity['commit']=='86653ca1315f24a96a41b0ef590af13228f90ab4'
 assert canonical['canonical_aliases']==['inherited:gformula','seed:061']
 assert canonical['decision']=='reference' and canonical['integration_allowed'] is False
 evidence=[ref(catalog,'candidates[id=seed:061].family_relation'),existing,ref(canonical_path,'Already reviewed canonical gfoRmula disposition')]
 evidence += [ref(SOURCE/n,'Same canonical authenticated evidence') for n in ['identity-review.json','source-audit.json','inspected-extracts.json','conversion-contract.json','exact-results.json','omissions-register.json']]
 (BASE/'plan-review.md').write_text('Resolve only seed:061 using explicit same_project_alias evidence and the already reviewed canonical pinned engine. Preserve its complete limitations, alternatives and refusal of executable admission. Do not count a second implementation, new native run, new scientific result or extra survey depth. No family-level inheritance is permitted for other wrappers or names.\n')
 evidence += [ref(BASE/'plan-review.md','Specific reviewed reconciliation'),ref(Path(__file__),'Exact alias guard')]
 decision=dict(canonical);decision.update(operation=OP,canonical_operation=CANONICAL,canonical_decision=ref(canonical_path,'Same engine decision'),
  scope='Exact gfoRmula seed alias reconciliation; retains canonical reference choice and all unqualified obligations.',
  alias_identity=seed['family_relation'],distinct_implementation_count_added=0,new_technical_claims=False,
  source_identity=identity['repository'],revision=identity['commit'],costs_to_measure=['R environment and dependency maintenance','Separate simulation M and bootstrap B compute budgets','Serialization and typed history validation','Failure recovery, warning review and upgrade conformance'],measured_costs=False,evidence=evidence)
 output=ROOT/node['outputs'][0];write(output,decision)
 findings=['The seed spelling resolves to the same CausalInference/gfoRmula commit, not a separate implementation.',
  'Canonical target, uncertainty, alternatives, costs/owners, proposed conversion/failure semantics and reopening conditions retain their original scope.',
  'Reference-only choice remains integration_allowed=false; no native capability or duplicate coverage credit is added.']
 write(BASE/'review.json',dict(status='pass_for_exact_alias_reconciliation',reviewer=dict(name='Codex author/coordinator',kind='author'),findings=findings,
  evidence=evidence,output=ref(output,'Reconciled seed disposition'),limitations=canonical['limitations']))
 new=run.ledger.receipt_template(node);new.update(outcome='pass',execution='performed',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
  limitations=canonical['limitations'],original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Contracted seed decision')],nonexecution_reason='',revisit_trigger=canonical['revisit_trigger'],
  criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Individual alias review')]) for i,f in enumerate(findings)])
 verify_bindings(new);run.validate_receipt(ROOT,merged,node,new,len(state['execution_program']['turns']));write(BASE/'operation-receipt.json',new)
 print(json.dumps(dict(operation=OP,alias_of=CANONICAL,new_implementations=0,integration_allowed=False)))
if __name__=='__main__':main()
