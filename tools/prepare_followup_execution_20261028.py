"""Prepare serial integration,complete program reconciliation and scoped delivery."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tools'
def repl(t,m):return re.sub('|'.join(re.escape(k) for k in sorted(m,key=len,reverse=True)),lambda x:m[x.group()],t)
def save(n,t):
 p=T/n;assert not p.exists();compile(t,str(p),'exec');p.write_text(t)
def main():
 m={'program-refresh-causal-modeling-v1':'program-refresh-followup-causal-v1','program-refresh-linguistic-measurement-v1':'program-refresh-causal-modeling-v1','causal-modeling-reader-v1':'followup-causal-reader-v1','sponsor-causal-modeling-v1':'sponsor-followup-causal-v1','causal-modeling-lead-v1':'followup-causal-review-v1','causal_modeling':'followup_causal','1397':'1400','1395':'1397','1044':'1049','1040':'1044','269':'271','411':'412','1,397':'1,400','1,395':'1,397','1,044':'1,049','1,040':'1,044'}
 t=repl((T/'refresh_causal_modeling_program_20261028.py').read_text(),m)
 t=t.replace('One later search original is integrated without changing the inherited census denominator.','Two selected originals integrated;all95later search rows explicitly dispositioned without changing inherited113candidates.')
 t=t.replace('Actual census acceptance criteria and95later search rows are explicit;2rows now bind the reviewed original.','All95rows map to79metadata identities;16duplicates,13selected-source rows and66unique acquisition/edition obligations retained.')
 t=t.replace('adds4','adds5')
 start=t.index('The new section distinguishes business phrases');end=t.index("\n'''",start)
 block='''The new section distinguishes causal tasks from causal interventions inside a language model.
The selected Ma survey supports a task taxonomy and warns about differing evaluation settings.
The selected Hu preprint supplies source-reported image-language architecture and results,including small benchmark regressions.
Exact authored witnesses distinguish arithmetic adjustment from normalized geometric approximation,changed weights and joint-confounder factorization.
Source findings,authored mathematics,proposed interfaces,native qualification and bank truth remain separate.

The [finite followup register](2026-10-28/followup-causal-review-v1/followup-lead-register.json)
now preserves explicit dispositions for all95later search rows:79metadata identities,16duplicates,
13rows linked to10retained selected originals,and66unique acquisition or edition obligations.
The additional Ma selected preprint is linked to,but not equated with,the indexed2025conference edition.
No source is admitted by title similarity alone;unversioned index entries do not establish byte equality.

Eleven exact-DOI lookups supply recorded routes and date limits. One returned metadata cluster links distinct SSRN/journal identifiers.
The [metadata review](2026-10-28/followup-causal-review-v1/metadata-review.json) retains that distinction and year-only date uncertainty.
The actual literature criteria require bounded searches,primary evidence or explicit omissions,and task-specific impacts.
They do not require native installation or bank validation;coverage and final acceptance nevertheless remain open.
'''
 t=t[:start]+block+t[end:]
 save('refresh_followup_causal_program_20261028.py',t)
 t=repl((T/'execute_causal_modeling_publication_20261028.py').read_text(),m)
 t=t.replace("RECOVERY=BASE.parent/'linguistic-measurement-v1'","RECOVERY=BASE.parent/'causal-modeling-lead-v1'").replace('new_scholarly_originals=1','new_scholarly_originals=2')
 save('execute_followup_causal_publication_20261028.py',t)
 t=repl((T/'deliver_causal_modeling_publication_20261028.py').read_text(),m)
 t=t.replace("'docs/papers/Evaluating Large Language Models for Causal Modeling Razouk(2024).pdf'","'docs/papers/Causal Inference with Large Language Model A Survey Ma(2024).pdf','docs/papers/Causal-LLaVA Causal Disentanglement for Mitigating Hallucination in Multimodal Large Language Models Hu(2025).pdf','tools/reconcile_followup_identities_20261028.py','tools/prepare_followup_publication_20261028.py','tools/prepare_followup_execution_20261028.py'")
 t=t.replace("'tools/*followup_causal*20261028.py'","'tools/*followup_causal*20261028.py'")
 t=t.replace("'docs/program/execution/2026-10-28/*causal-modeling*'","'docs/program/execution/2026-10-28/*followup-causal*','docs/program/execution/2026-10-28/followup-identity-reconciliation-v1'")
 t=t.replace("'docs/literature/raw/exec28_modeling*'","'docs/literature/raw/exec28_followup*'")
 t=t.replace("BASE.parent/'linguistic-measurement-v1'","BASE.parent/'causal-modeling-lead-v1'")
 t=t.replace('Integrate causal variable modeling and repair census continuation scope','Integrate causal task survey and representation assumptions with reconciled source queue')
 save('deliver_followup_causal_publication_20261028.py',t)
 print('Prepared serial execution,refresh and delivery successors.')
if __name__=='__main__':main()
