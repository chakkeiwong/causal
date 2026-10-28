"""Prepare reviewed serial orchestration and a scope-correct master refresh."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tools'
def repl(t,m):return re.sub('|'.join(re.escape(k) for k in sorted(m,key=len,reverse=True)),lambda a:m[a.group()],t)
def save(n,t):
 p=T/n;assert not p.exists();compile(t,str(p),'exec');p.write_text(t)
def main():
 t=(T/'refresh_linguistic_measurement_program_20261028.py').read_text()
 t=repl(t,{'program-refresh-linguistic-measurement-v1':'program-refresh-causal-modeling-v1',"PRIOR=DAY/'recovered-followups-v1'":"PRIOR=DAY/'program-refresh-linguistic-measurement-v1'",'linguistic-measurement-reader-v1':'causal-modeling-reader-v1','sponsor-linguistic-measurement-v1':'sponsor-causal-modeling-v1',"SOURCE=DAY/'linguistic-measurement-v1'":"SOURCE=DAY/'causal-modeling-lead-v1'",'1395':'1397','1040':'1044','1392':'1395','1035':'1040','410':'411','268':'269','1,395':'1,397','1,392':'1,395','1,040':'1,044','causal_proposal_linguistic_measurement_reviewed_v1_2026-10-28':'causal_proposal_causal_modeling_reviewed_v1_2026-10-28','sponsor_proposal_linguistic_measurement_reviewed_2026-10-28':'sponsor_proposal_causal_modeling_reviewed_2026-10-28','adds5':'adds4'})
 t=t.replace("'2026-10-25/program-refresh-benchmark-oracles-v1/'+name","'2026-10-28/program-refresh-linguistic-measurement-v1/'+name")
 t=t.replace('One adjacent original adds scholarly depth without closing an unrelated census row.','One later search original is integrated without changing the inherited census denominator.')
 t=t.replace('Completed runtime inventories and bounded backward-chain work replace stale continuation instructions.','Actual census acceptance criteria and95later search rows are explicit;2rows now bind the reviewed original.')
 start=t.index('Pages 296-300 connect');end=t.index("\n'''",start)
 block='''The new section distinguishes business phrases, variable values, compound entities and causal interventions.
The inspected Razouk preprint reports seven models evaluated on generated data; independent bank truth is not inferred.
Exact authored examples distinguish compound wording from additive causal interaction and graph paths from nonzero total mean effects.
All source-reported scores remain tied to historical task definitions, model labels and generated-label denominators.

The [census contract audit](2026-10-28/census-acceptance-scope-v1/review.json) identifies an execution-scope problem:
LL.CENSUS requires evidence-backed dispositions, task mapping, complementary bounded searches and citation chaining.
It permits recorded source unavailability with affected claims restricted. Native installation and bank validation are separate gates.
No unread paper becomes inspected, and no coverage or final acceptance is granted by this diagnosis.

The [followup register](2026-10-28/causal-modeling-lead-v1/followup-lead-register.json) preserves 60 earlier and 35 specialist search rows.
Two rows now bind the inspected causal-modeling preprint. The remaining 93 need explicit identity/version and source-disposition reconciliation.
This queue is separate from the 113 inherited candidate census and prevents untracked later discoveries from being overlooked.

The prior linguistic intervention and component-adoption section remains intact. Its exact proxy example and LLM-CD/LLM-and-SCD/LCM limits
remain qualified. Public/generated prototype evidence, source coverage, native qualification and bank acceptance retain distinct outcomes.
'''
 t=t[:start]+block+t[end:]
 t=t.replace("text=text.replace('2026-10-28/recovered-followups-v1/remaining-operations.json','2026-10-28/program-refresh-causal-modeling-v1/remaining-operations.json')","text=text.replace('2026-10-28/program-refresh-linguistic-measurement-v1/remaining-operations.json','2026-10-28/program-refresh-causal-modeling-v1/remaining-operations.json')")
 save('refresh_causal_modeling_program_20261028.py',t)
 t=repl((T/'execute_linguistic_publication_20261028.py').read_text(),{'linguistic-measurement-v1':'causal-modeling-lead-v1',"RECOVERY=BASE.parent/'recovered-followups-v1'":"RECOVERY=BASE.parent/'linguistic-measurement-v1'",'linguistic_measurement':'causal_modeling','sponsor_proposal_linguistic_measurement_reviewed_2026-10-28':'sponsor_proposal_causal_modeling_reviewed_2026-10-28'})
 save('execute_causal_modeling_publication_20261028.py',t)
 t=repl((T/'deliver_linguistic_publication_v2_20261028.py').read_text(),{'execute_linguistic_publication_20261028':'execute_causal_modeling_publication_20261028','Causal Effects of Linguistic Properties Pryzant(2020).pdf':'Evaluating Large Language Models for Causal Modeling Razouk(2024).pdf','tools/*linguistic*20261028.py':'tools/*causal_modeling*20261028.py','docs/program/execution/2026-10-28/*linguistic*':'docs/program/execution/2026-10-28/*causal-modeling*','docs/program/execution/2026-10-28/longitudinal-backward-chain-v1':'docs/program/execution/2026-10-28/census-acceptance-scope-v1','docs/literature/raw/exec28_lbc*':'docs/literature/raw/exec28_modeling*',"BASE.parent/'recovered-followups-v1'":"BASE.parent/'linguistic-measurement-v1'",'Integrate linguistic intervention assumptions and component-specific adoption evidence':'Integrate causal variable modeling and repair census continuation scope'})
 t=t.replace("'tools/audit_recovery_staging_v3_20261028.py',","'tools/audit_recovery_staging_v3_20261028.py','tools/audit_census_acceptance_scope_20261028.py',",1)
 save('deliver_causal_modeling_publication_20261028.py',t)
 print('Prepared refresh,execution and delivery successors.')
if __name__=='__main__':main()
