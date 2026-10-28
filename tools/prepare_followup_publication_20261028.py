"""Prepare preserving reader/sponsor successors with explicit reviewed delta."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tools'
def repl(t,m):return re.sub('|'.join(re.escape(k) for k in sorted(m,key=len,reverse=True)),lambda x:m[x.group()],t)
def save(n,t):
 p=T/n;assert not p.exists();compile(t,str(p),'exec');p.write_text(t)
def main():
 common={'causal_modeling':'followup_causal','causal-modeling-reader-v1':'followup-causal-reader-v1','causal-modeling-lead-v1':'followup-causal-review-v1','sponsor-causal-modeling-v1':'sponsor-followup-causal-v1','linguistic-measurement-reader-v1':'causal-modeling-reader-v1','sponsor-linguistic-measurement-v1':'sponsor-causal-modeling-v1','causal_proposal_linguistic_measurement_reviewed_v1_2026-10-28':'causal_proposal_causal_modeling_reviewed_v1_2026-10-28','sponsor_proposal_linguistic_measurement_reviewed_2026-10-28':'sponsor_proposal_causal_modeling_reviewed_2026-10-28','1397':'1400','1395':'1397','269':'271','268':'269','1044':'1049','1040':'1044','exec28_cm_':'exec28_fr_','sec:exec28-cm':'sec:exec28-fr','sp28cm_':'sp28fr_','sp28lm_':'sp28cm_'}
 t=repl((T/'build_causal_modeling_reader_20261028.py').read_text(),common)
 t=t.replace('import followup_causal_reference_20261028 as exact','import followup_causal_reference_20261028 as exact').replace('added==2','added==3')
 t=t.replace('From business phrases to causal variables','Causal tasks and representation interventions')
 t=t.replace('Add the inspected Razouk preprint, variable/value contract, generated-label limits and exact compound-interaction/path-cancellation witnesses','Add the inspected Ma survey and Hu representation preprint,source-specific evaluation limits,and exact arithmetic/geometric and joint-confounder witnesses')
 save('build_followup_causal_reader_20261028.py',t)
 t=repl((T/'publish_causal_modeling_reader_20261028.py').read_text(),common)
 t=t.replace("['razouk','reference']","['ma','hu','reference']").replace('added_citation_records=2','added_citation_records=3')
 t=t.replace('A useful causal assistant must decide what the variables mean before it can reason about arrows.','A causal assistant must preserve the distinction between answering a causal question and changing a language model.')
 t=t.replace('The result is a traceable scientific specification whose ambiguity remains visible, rather than a diagram that merely looks complete.','For the banking analyst, the useful output is an auditable answer whose scientific target survives every translation and approximation.')
 t=t.replace("['560','559','105','payment','partition']","['1,000','740','geometric','reminder','CHAIR']")
 t=t.replace('two additional primary-paper and independent-project records','three additional primary-paper and independent-project records')
 t=t.replace('Exact finite examples reproduce compound interaction0or5,mediated/direct cancellation and inconsistent semantic pair grouping','Exact finite examples distinguish arithmetic3/10,geometric1/4,uniform1/2,conditional37/50andjoint1/2versusproduct1/4')
 t=t.replace('Proposed semantic artifacts preserve variables,values,units,clocks,provenance,ambiguity and intervention meaning','Proposed request contracts distinguish measurement,model-internal intervention and banking-policy effects,with explicit weights,approximations and assumptions')
 t=t.replace('variable/value mapping, generated-label evaluation and exact compound interaction/path-cancellation examples','Task-specific survey evaluation,representation interventions and exact approximation/joint-confounder witnesses')
 t=t.replace('Preprint tasks and generated evaluation labels are inspected; authored semantic and causal witnesses remain distinct from native results.','Survey comparability limits and representation methods/results are inspected; authored mathematical witnesses remain distinct from native results.')
 t=t.replace('causal variable modeling','task-specific survey and representation')
 save('publish_followup_causal_reader_20261028.py',t)
 t=repl((T/'build_causal_modeling_sponsor_20261028.py').read_text(),common)
 t=t.replace('causal variable modeling comparison','task-specific survey and representation comparison')
 save('build_followup_causal_sponsor_20261028.py',t)
 t=repl((T/'publish_causal_modeling_sponsor_20261028.py').read_text(),common)
 t=t.replace("['razouk','reference']","['ma','hu','reference']").replace('Validate variable meaning before accepting the diagram','Separate causal reasoning from model repair')
 t=t.replace('causal variable modeling','task-specific survey and representation')
 save('publish_followup_causal_sponsor_20261028.py',t)
 print('Prepared four explicit preserving publication successors.')
if __name__=='__main__':main()
