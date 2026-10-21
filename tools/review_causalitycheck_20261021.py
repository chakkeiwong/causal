"""Bounded original-text review and conservative census reconciliation."""
from collections import Counter
import copy,json,hashlib,re,shutil
from pathlib import Path
import causalitycheck_reference_20261021 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-21/census-causalitycheck-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1'
read=lambda p:json.loads(p.read_text())
LIMITS=['Bounded author primary-text review; no complete frontier search or independent reproduction.',
 'Publisher July2026 proceedings and June2026 PDF metadata precede cutoff; post-cutoff acquisition does not prove unchanged historical bytes.',
 'Public code/data link is a lead; repository,raw item judgments,model snapshots and reuse rights are not qualified.',
 'Textual benchmark accuracy and annotation agreement do not identify banking intervention effects.',
 'No live model,downloaded code or upstream experiment executed; no rendered visual acceptance.']

def main():
 assert not (BASE/'source-audit.json').exists()
 pages=(BASE/'original.txt').read_text().split(chr(12))
 assert len([p for p in pages if p.strip()])==27
 assert 'Jiang Li' in pages[0] and 'July 2-7, 2026' in pages[0]
 acq=BASE/'acquisition/network'
 for name,suffix in [('original','pdf'),('identity','html')]:
  r=read(acq/(name+'.receipt.json'));assert r['returncode']==0 and r['sha256']==hashlib.sha256((acq/(name+'.'+suffix)).read_bytes()).hexdigest()
 assert '2026/7' in (acq/'identity.html').read_text()
 title='CausalityCheck: A Framework for Evaluating Causal Reasoning in Large Language Models'
 filename=title.replace(':','');paper=ROOT/'docs/papers'/f'{filename} Li(2026).pdf'
 assert not paper.exists();shutil.copyfile(acq/'original.pdf',paper)
 write(BASE/'exact-results.json',exact.calculate())
 anchors={1:'Title,authors,ACL2026 pages16403-16429,July2-7;18-model benchmark and code/data lead.',
  3:'Four tasks and four robustness variants; answerability,process and causal-validity concepts are textual labels.',
  4:'GPT5 generation,36 variants per seed,two manual rounds and entity substitution.',
  5:'1200 seeds,43200 generated,10800 selected,8920 retained; unequal cell counts and ten annotators.',
  6:'Table1 cell/task averages,near-ceiling OP and lower PJ/CVA; reported model scores are historical results.',
  8:'AJ-PJ and VCR contrast diagnostics; negative challenge score for Grok4; task differences interpreted as causal-chain errors.',
  9:'Explicit limitations on graph construction,structural rigor and counterfactual reasoning.',
  14:'Few-shot and generation settings; Table3 Kappa values AJ.72/.78 and CVA.59-.65 contradict blanket excellent-agreement language.',
  15:'Annotation category examples,reasoning prompt controls and filtering transition.',
  16:'Remove incomplete,ambiguous and sensitive items; author claim competitor win discounts generator bias requires stronger evidence.',
  17:'Entity-specific negative-response example and dual-prompt pass rates; qualitative mechanism explanation is not an identified causal diagnosis.',
  18:'Checklist construction diagram maps four tasks and four robustness variants.',
  19:'Example seed and altered contexts; textual context/answer requirements.',
  27:'Final virtual-vocabulary causal-validity examples; supplied labels are adjudicated text tasks,not causal-effect estimates.'}
 inspected=[]
 for n,finding in anchors.items():
  p=BASE/f'page-{n}.txt';p.write_text(pages[n-1]);inspected.append(dict(anchor=f'Physical PDF page{n};printed{16402+n}',finding=finding,extracted_text=ref(p,'Inspected primary text')))
 write(BASE/'version-selection.json',dict(candidate='LA01-candidate-109',title=title,filename_title=filename,
  selected='ACL Anthology2026.findings-acl.808',publication='July2026;printedJuly2-7',pdf_metadata='9June2026',
  discovery_metadata='OpenAlex date2026-01-01 is coarse and does not replace publisher publication month',
  cutoff='2026-10-07',pages=27,evidence=[ref(acq/'identity.html','Publisher identity and month'),ref(acq/'original.pdf','Genuine original'),ref(BASE/'pdfinfo.txt','PDF metadata')]))
 claims=['Framework crosses four task types with four robustness variants,using GPT5 transformations of CausalProbe seeds and manual checks.',
  'Paper reports1200 seeds,43200 generated,10800 sampled and8920 retained; printed group counts sum to8920.',
  'Table1 reports near-ceiling original-question accuracy with substantially lower process and causal-validity accuracy for selected models.',
  'Challenge1 subtracts AJ and PJ marginal accuracies; challenge2 contrasts virtual-entity and real-entity task performance.',
  'Table3 reports variable annotation agreement,including AJ.72/.78 and CVA.59-.65.',
  'Authors acknowledge limited structural-graph and counterfactual evaluation; code/data and linked methodological references are separate leads.']
 source=dict(integrated_citation_key='exec21_causalitycheck',kind='paper',title=title,filename_title=filename,
  first_author='Li',author='Li, Jiang and Duo, Zehua and Gao, Guanglai and Su, Xiangdong',year=2026,
  source_identity='https://aclanthology.org/2026.findings-acl.808/; DOI10.18653/v1/2026.findings-acl.808',
  version_date='July2026 ACL proceedings;27pages;acquired21October2026',cutoff='2026-10-07',
  local_copy=ref(paper,'Genuine publisher PDF'),local_path=str(paper.relative_to(ROOT)),sha256=hashlib.sha256(paper.read_bytes()).hexdigest(),
  inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS,
  identity_evidence=[ref(BASE/'version-selection.json','Identity/version reconciliation'),ref(acq/'original.receipt.json','Acquisition receipt')])
 authored=dict(integrated_citation_key='exec21_causalitycheck_reference',kind='project_derivation',
  title='Checklist denominators,paired-error bounds and selection economics',author='Causal banking proposal project',year=2026,
  source_identity='tools/causalitycheck_reference_20261021.py',version_date='21October2026',
  local_copy=ref(ROOT/'tools/causalitycheck_reference_20261021.py','Exact finite constructions'),
  inspected_anchors=[ref(BASE/'exact-results.json','Printed counts and authored matched-design witnesses')],
  supported_claims=['Task totals482,2052,2190,4196 sum8920;1880 of10800 selected instances are excluded.',
    'Same marginal accuracies82.27%/59.46% permit paired A-correct/B-wrong rates22.81%..40.54% under a shared population.',
    'Negative marginal difference-5.12points permits paired error0..23.2%; it does not establish no error.',
    'Retaining50 of100 requests with45 correct gives90% selected accuracy but full accuracy45%..95%;assumed margins5 versus[-13,7].'],limitations=exact.calculate()['limits'])
 write(BASE/'source-audit.json',dict(sources=[source,authored],cutoff='2026-10-07',limitations=LIMITS))
 critical=['Accuracy differences are marginal contrasts,not the frequency of joint errors; unequal task counts make matched interpretation still less direct.',
  'Negative AJ-PJ does not establish absence of causal-chain errors. Paired judgments and accepted gold structure are required.',
  'Entity renaming may change semantics,tokenization,difficulty or response policy; a score change is not uniquely identified memory contamination.',
  'A competitor beating the generator does not establish absence of generator-specific bias or label leakage.',
  'Removing ambiguous or sensitive items changes the target evaluation population; report removals and production-like refusals separately.',
  'Table3 includes sub-.8 AJ agreement; do not repeat blanket excellent-agreement prose without qualification.',
  'Macro cell averages and micro item accuracy differ when cell sizes differ; recover raw seeds,draws and weights before comparing rates.',
  'Known SCM mechanism labels,paired seed splits,blind adjudication and held-out bankspecific tasks are proposed additions,not properties established here.']
 write(BASE/'omissions-register.json',dict(global_blocker=False,remaining=['Pinned code/data and licenses','Raw seed-level predictions,labels,filters and joint outcomes','Model snapshot,prompt and full-cost records','Complementary search/citation chaining','Independent benchmark reproduction and banking transfer'],no_source_waivers=True))
 write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Reviewed recovery plan')],
  checks=['Use genuine original and inspect adverse evidence.','Separate marginal score differences from paired causal-error diagnoses.','Keep census/task conservation and exact source identity.']))
 write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),
  findings=claims,source_critical_qualifications=critical,limitations=LIMITS,
  evidence=[ref(BASE/n,'Primary review evidence') for n in ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],native_execution=False,visual_acceptance=False,coverage_acceptance=False))
 old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
 item=next(x for x in new['items'] if x['id']=='LA01-candidate-109');assert item['disposition']=='open_original_not_inspected'
 item.update(prior_disposition=item['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
  source_key='exec21_causalitycheck',primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Bounded technical review'),
  availability='Genuine27-page July2026 publisher original acquired; sandbox DNS failures retained.',
  effect_on_claims='Supports checklist/evaluation design with marginal-error,selection and label limits; no bank causal qualification.',
  next_action='Integrate bounded review; recover pinned data/code and joint seed-level judgments before runtime reuse.')
 assert len(new['items'])==117 and all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-109')
 counts=Counter(x['disposition'] for x in new['items']);assert counts['inspected_primary_retained_with_limits']==55 and counts['open_original_not_inspected']==58
 new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved54/59 census'),changes=['Candidate109 reviewed;116 other records unchanged.'],
  evidence=[ref(BASE/'primary-review.json','Primary review')],closure=False,interpretation='55/113 originals inspected;58 unread;four separate obligations remain.')
 write(BASE/'census-register.json',new)
 tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
 for task in tasks['task_families']:
  if 'LA01-candidate-109' in task['inherited_ids']:
   task['uninspected_candidate_ids'].remove('LA01-candidate-109');task['inspected_candidate_ids'].append('LA01-candidate-109');task['inspected_source_keys'].append('exec21_causalitycheck')
  task['coverage_acceptance']=False
 tasks.update(register=ref(BASE/'census-register.json','55/58 census'),supersedes=ref(PRIOR/'task-map.json','Preserved task map'))
 tasks.setdefault('primary_application_notes',{})['evaluation_cost']='Use paired seed-level gold judgments; report filtering,macro/micro weights,refusals and decision economics.'
 write(BASE/'task-map.json',tasks)
 write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-109'],unchanged_other_records=116,original_candidates=113,inspected=55,unread=58,task_families=14,coverage_acceptance=False,
  evidence=[ref(BASE/'census-register.json','Census conservation'),ref(BASE/'task-map.json','Task conservation')]))
 write(BASE/'review.json',dict(status='pass_for_bounded_primary_review',limitations=LIMITS,coverage_acceptance=False,
  evidence=[ref(BASE/'primary-review.json','Source-critical inspection'),ref(BASE/'reconciliation-review.json','Conservation')]))
 write(BASE/'inspection-progress.json',dict(finding='Candidate109 original inspected; score-difference,filtering and label limits retained; census55/58.',
  next_action='Integrate CausalityCheck review and exact evaluation witnesses into paired reader/sponsor; continue58 unread originals and complementary searches.',
  evidence=[ref(BASE/n,'Bounded census review') for n in ['source-audit.json','review.json','census-register.json','task-map.json']]))
 verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
 print(json.dumps(dict(inspected=55,unread=58,sources=2,coverage_acceptance=False)))
if __name__=='__main__':main()
