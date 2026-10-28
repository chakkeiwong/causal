"""Create explicit successors for a reviewed causal-modeling argument."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tools'
def repl(t,m):return re.sub('|'.join(re.escape(k) for k in sorted(m,key=len,reverse=True)),lambda a:m[a.group()],t)
def save(n,t):
 p=T/n;assert not p.exists();compile(t,str(p),'exec');p.write_text(t)
def main():
 t=repl((T/'build_linguistic_measurement_reader_20261028.py').read_text(),{
 'linguistic_measurement_reference_20261028':'causal_modeling_reference_20261028',
 '2026-10-28/linguistic-measurement-reader-v1':'2026-10-28/causal-modeling-reader-v1',
 '2026-10-28/linguistic-measurement-v1':'2026-10-28/causal-modeling-lead-v1',
 '2026-10-25/benchmark-oracles-reader-v1':'2026-10-28/linguistic-measurement-reader-v1',
 'causal_proposal_benchmark_oracles_reviewed_v1_2026-10-25':'causal_proposal_linguistic_measurement_reviewed_v1_2026-10-28',
 'causal_proposal_linguistic_measurement_reviewed_v1_2026-10-28':'causal_proposal_causal_modeling_reviewed_v1_2026-10-28',
 '1392':'1395','added==3':'added==2','expected_scholarly_pdfs=268':'expected_scholarly_pdfs=269',
 'sec:exec28-lm':'sec:exec28-cm','Linguistic measurement and executable interventions':'From business phrases to causal variables'})
 t=t.replace('Add the inspected Pryzant preprint, exact heterogeneous measurement witness and component-specific runtime findings;','Add the inspected Razouk preprint, variable/value contract, generated-label limits and exact compound-interaction/path-cancellation witnesses;')
 save('build_causal_modeling_reader_20261028.py',t)
 t=repl((T/'publish_linguistic_measurement_reader_20261028.py').read_text(),{'build_linguistic_measurement_reader_20261028':'build_causal_modeling_reader_20261028','1395':'1397','1392':'1395','268':'269','added_citation_records=3':'added_citation_records=2','linguistic_measurement':'causal_modeling','linguistic measurement and adoption':'causal variable modeling'})
 t=t.replace("{'exec28_lm_'+k for k in ['pryzant','artifacts','reference']}","{'exec28_cm_'+k for k in ['razouk','reference']}")
 t=t.replace('A language-assisted banking decision begins with an intervention that a bank can actually implement.','A useful causal assistant must decide what the variables mean before it can reason about arrows.')
 t=t.replace('The proposed product must preserve the distinction between a meaningful scientific question, a justified answer and an executable method.','The result is a traceable scientific specification whose ambiguity remains visible, rather than a diagram that merely looks complete.')
 t=t.replace("['CFPB','TextCause','77.5','50,000','LCM']","['560','559','105','payment','partition']")
 t=t.replace('three additional primary-paper, component-source and independent-project records','two additional primary-paper and independent-project records')
 t=t.replace('Exact conditional-mean enumeration and separate algebra reproduce heterogeneous effects,proxy sign reversal and stipulated USD consequences;','Exact finite examples reproduce compound interaction0or5,mediated/direct cancellation and inconsistent semantic pair grouping;')
 t=t.replace('Preprint conditions and component inventories are inspected; the stochastic-proxy witness remains distinct from source theorem assumptions and native results.','Preprint tasks and generated evaluation labels are inspected; authored semantic and causal witnesses remain distinct from native results.')
 t=t.replace('linguistic measurement, sequential policy and component adoption comparison; all previous content preserved.','variable/value mapping, generated-label evaluation and exact compound interaction/path-cancellation examples; all previous content preserved.')
 t=t.replace('Proposed semantic and sequential policy contracts preserve intervention meaning, clocks, measurement, support and explicit runtime artifact failures; no native capability.','Proposed semantic artifacts preserve variables,values,units,clocks,provenance,ambiguity and intervention meaning; no native capability.')
 save('publish_causal_modeling_reader_20261028.py',t)
 t=repl((T/'build_linguistic_measurement_sponsor_20261028.py').read_text(),{
 'build_linguistic_measurement_reader_20261028':'build_causal_modeling_reader_20261028',
 '2026-10-28/sponsor-linguistic-measurement-v1':'2026-10-28/sponsor-causal-modeling-v1',
 '2026-10-25/sponsor-benchmark-oracles-v1':'2026-10-28/sponsor-linguistic-measurement-v1',
 '2026-10-25/benchmark-oracles-reader-v1':'2026-10-28/linguistic-measurement-reader-v1',
 '2026-10-28/linguistic-measurement-v1':'2026-10-28/causal-modeling-lead-v1',
 'sponsor_proposal_linguistic_measurement_reviewed_2026-10-28':'sponsor_proposal_causal_modeling_reviewed_2026-10-28',
 '1392':'1395','1395':'1397','1035':'1040','1040':'1044','267':'268','268':'269',
 'sp25bor_reader,sp25bor_progress':'sp28lm_reader,sp28lm_progress','sp28lm_reader':'sp28cm_reader','sp28lm_progress':'sp28cm_progress',
 'linguistic measurement and component adoption':'causal variable modeling'})
 save('build_causal_modeling_sponsor_20261028.py',t)
 t=repl((T/'publish_linguistic_measurement_sponsor_20261028.py').read_text(),{
 'build_linguistic_measurement_sponsor_20261028':'build_causal_modeling_sponsor_20261028','1040':'1044','1035':'1040','1395':'1397','268':'269','sp28lm_reader':'sp28cm_reader','sp28lm_progress':'sp28cm_progress','Measure the intervention before funding the language workflow':'Validate variable meaning before accepting the diagram','linguistic measurement and component adoption':'causal variable modeling','publish_linguistic_measurement_sponsor':'publish_causal_modeling_sponsor'})
 t=t.replace("{'exec28_lm_'+k for k in ['pryzant','artifacts','reference']}","{'exec28_cm_'+k for k in ['razouk','reference']}")
 save('publish_causal_modeling_sponsor_20261028.py',t)
 print('Four explicit preserving successors created.')
if __name__=='__main__':main()
