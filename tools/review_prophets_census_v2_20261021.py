#!/usr/bin/env python3
"""Inspect ACL Anthology candidate 167 and preserve a one-candidate census successor."""
from collections import Counter
import copy,hashlib,json,subprocess
from pathlib import Path
from html.parser import HTMLParser
import prophets_reference_20261021 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-21/census-prophets-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-21/census-ace-v1'
PAPER=ROOT/'docs/papers/From Causal Parrots to Causal Prophets Towards Sound Causal Reasoning with Large Language Models Shrestha(2025).pdf'
read=lambda p:json.loads(p.read_text())
LIMITS=[
 'Bounded source-critical inspection of one 15-page article; 56 other census originals remain unread.',
 'Publisher paper is dated 2025 and its PDF metadata shows creation in March 2025; 2026-10-21 acquisition does not authenticate historical archive bytes.',
 'Reported model scores use rounded percentages, one sampled CLADDER formal benchmark and no reported confidence intervals in the inspected result tables.',
 'Code/prompt repository, raw responses, exact question IDs, generated data and execution logs were not acquired or run.',
 'Formal synthetic question answering is not free-form business-to-causal translation, causal discovery on bank records, graph identification or authentic financial validation.',
 'Publisher PDF extraction was text-only; no image-based visual acceptance, independent review or live model execution.']

class Metadata(HTMLParser):
 def __init__(self):super().__init__();self.items=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='meta' and d.get('name','').startswith('citation_'):self.items.append(d)

def main():
 assert not (BASE/'source-audit.json').exists()
 acq=BASE/'acquisition/network'
 for n,suffix in [('original','pdf'),('identity','html')]:
  rec=read(acq/(n+'.receipt.json'));p=acq/(n+'.'+suffix)
  assert rec['status']=='complete_public_original' and rec['bytes']==p.stat().st_size
  assert rec['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
 assert hashlib.sha256(PAPER.read_bytes()).hexdigest()==hashlib.sha256((acq/'original.pdf').read_bytes()).hexdigest()
 pages=(BASE/'original.txt').read_text().split('\f')
 assert len([x for x in pages if x.strip()])==15
 assert 'Rahul B. Shrestha' in pages[0] and 'Proceedings of the 5th International Conference on Natural Language Processing for Digital Humanities' in pages[0]
 meta=Metadata();meta.feed((acq/'identity.html').read_text())
 assert any(x.get('name')=='citation_doi' and x['content']=='10.18653/v1/2025.nlp4dh-1.29' for x in meta.items)
 assert any(x.get('name')=='citation_publication_date' and x['content']=='2025/5' for x in meta.items)
 assert len(pages)==16 # 15 pages plus pdftotext terminal form-feed slot
 info=subprocess.check_output(['pdfinfo',str(PAPER)],text=True)
 (BASE/'pdfinfo.txt').write_text(info)
 anchors={
  1:'Printed authors, equal-contribution note, abstract, conference pages319-333 and publication notice.',
  2:'Research questions and Ladder definitions; causal reasoning background and benchmark task context.',
  3:'CLADDER task justification and formal symbolic ground truth; sample construction begins.',
  4:'Backdoor-adjustment exclusion, GPT-4o-generated perturbations, manual checks, 13-model/date/temperature setup and self-consistency.',
  5:'Tree search greedily self-scores alternatives; PoT generates code and delegates arithmetic to a Python interpreter with DoWhy.',
  6:'Generated synthetic data from question facts, base model results, fixed-sample scope and manual error-sample design.',
  7:'Table2 accuracy by model/rung, RQ1/RQ2 interpretation and Table3 sampled error categories.',
  8:'Prompt comparison interpretation; single-dataset limitations, no informal task evaluation and ethical caveats.',
  9:'Table4 prompt results; CausalPoT gains and counterfactual-specific scores; self-authored perturbation concern.',
  10:'References and adjacent original leads; citation listing is discovery only, not primary-source review.',
  11:'Appendix Table5 sample/original counts, query-type count mismatch and rung totals; repository is cited but not inspected.',
  12:'Memorization test prompts and failed reconstruction; distribution figures and first association example.',
  13:'Appendix association, intervention and mediation examples; literal formula/expansion/arithmetic and outcome-label mismatch in D.3.',
  14:'Appendix Tables6-9; SC10 totals995 and SC5 totals999; PoT error-sample prose says50.',
  15:'Table10 error categories total60 versus prose50; Figure6 variable-name perturbations.'}
 inspected=[]
 for n,finding in anchors.items():
  p=BASE/f'page-{n:02}.txt';assert p.exists()
  inspected.append(dict(anchor=f'PDF physical page {n}; conference printed page {318+n}',finding=finding,
    extracted_text=ref(p,'Extracted primary page text; no image review')))
 write(BASE/'version-selection.json',dict(candidate_id='LA01-candidate-167',
  title='From Causal Parrots to Causal Prophets? Towards Sound Causal Reasoning with Large Language Models',
  authors=['Rahul B. Shrestha','Simon Malberg','Georg Groh'],equal_contribution=['Rahul B. Shrestha','Simon Malberg'],
  doi='10.18653/v1/2025.nlp4dh-1.29',publisher='Association for Computational Linguistics',
  venue='Proceedings of the 5th International Conference on Natural Language Processing for Digital Humanities, pages319-333',
  publication='3-4 May 2025',pdf_creation='28 March 2025',acquired='21 October 2026',cutoff='2026-10-07',
  metadata=meta.items,pdfinfo=ref(BASE/'pdfinfo.txt','Observed PDF metadata'),
  evidence=[ref(acq/'identity.html','ACL Anthology identity'),ref(acq/'original.pdf','Publisher PDF'),ref(PAPER,'Required-name scholarly local copy')]))
 (BASE/'exact-results.json').write_text(json.dumps(exact.calculate(),indent=2)+'\n')
 claims=[
  'The study samples formal CLADDER questions across association, intervention and counterfactual query types; it excludes backdoor-adjustment items from its 1000-item sample.',
  'Anti-commonsensical and nonsense variants are generated from sampled questions using GPT-4o and manually checked; one underlying dataset and prompt design constrain generalization.',
  'Causal tree of thoughts expands and self-rates intermediate candidate solutions, then greedily selects a continuation; scores are model self-evaluation, not independent adjudication.',
  'Causal program of thoughts asks an LLM to generate DoWhy code; the execution example synthesizes data from numerical facts in the prompt and returns a calculation for the LLM to interpret.',
  'For GPT-4o, Table4 overall accuracies are82.0%,86.4% and90.8% for baseline/tree/program; commonsensical subset values are84.3%,87.5%,92.5%. Overall gains are4.4/8.8 percentage points.',
  'The reported CausalPoT counterfactual accuracies are92.5%,90.2% and87.4% on commonsensical, anti-commonsensical and nonsense variants; these remain benchmark scores, not identified financial effects.',
  'The authors explicitly limit claims to formal causal reasoning and CLADDER, call for other benchmarks, and caution against machine-only high-stakes decision making.',
  'Appendix Table5 lists sample query-type counts summing999 although rung counts sum1000; preserve this discrepancy until question-level files resolve it.']
 write(BASE/'source-audit.json',dict(sources=[dict(integrated_citation_key='exec21_prophets',kind='paper',title='From Causal Parrots to Causal Prophets? Towards Sound Causal Reasoning with Large Language Models',
  filename_title='From Causal Parrots to Causal Prophets Towards Sound Causal Reasoning with Large Language Models',first_author='Shrestha',
  author='Shrestha, Rahul B. and Malberg, Simon and Groh, Georg',year=2025,
  source_identity='ACL Anthology; DOI 10.18653/v1/2025.nlp4dh-1.29',version_date='May2025 publisher edition; acquired21 October2026',cutoff='2026-10-07',
  local_path=str(PAPER.relative_to(ROOT)),sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),local_copy=ref(PAPER,'Genuine publisher PDF named per proposal standard'),
  inspected_anchors=inspected,supported_claims=claims,limitations=LIMITS,
  identity_evidence=[ref(BASE/'version-selection.json','Publisher metadata/title/authors'),ref(acq/'original.receipt.json','Bounded public PDF receipt')]),
 dict(integrated_citation_key='exec21_prophets_reference',kind='project_derivation',title='Arithmetic and count reconciliation for Shrestha et al. (2025) displayed benchmark tables',
  author='Causal banking proposal project',year=2026,version_date='21 October2026',source_identity='tools/prophets_reference_20261021.py',
  local_copy=ref(ROOT/'tools/prophets_reference_20261021.py','Exact decimal arithmetic over printed rounded scores'),
  inspected_anchors=[ref(BASE/'exact-results.json','Reproduced score differences and count sums')],
  supported_claims=['Causal program versus baseline is8.8 percentage points; causal tree versus baseline is4.4 points.',
   'Counterfactual score differences are22.4,21.4 and23.3 points across the three reported variants.',
   'Appendix sampled query-type totals sum999 while rung totals sum1000; original counts sum8690.'],limitations=LIMITS)],cutoff='2026-10-07'))
 critical=[
  'The study is a narrow formal reasoning benchmark on symbolic probability questions with known answer-generation rules; it is not a field study of business-question translation or causal discovery from banking records.',
  'PoT code is generated for calculations over information encoded in the question and the displayed method synthesizes data; running that code cannot supply missing causal assumptions, graph direction, exchangeability or intervention truth.',
  'A fluent graph proposal and a correct yes/no answer are separate outcomes; source analysis identifies no validated graph recovery or graph-equivalence metric for bank diagrams.',
  'Self-scored ToT, stochastic self-consistency and code execution have different costs, failure modes and security boundaries; voting does not supply independent validation.',
  'Rounded table percentages, absent question-level outputs and unspecified uncertainty prevent reconstruction of significance or paired per-question differences.',
  'Table5 sampled query counts total999 versus1000 rung counts; SC10 Table7 totals995 and SC5 Table8 totals999; Table10 categories total60 despite prose describing50. Recover question-level records before denominators or error rates.',
  'Appendix D.3 step4 evaluated literally gives -14/125, while its different step6 expansion gives49/2000, not the printed0.0173. Outcome death/survival labels and NIE notation also require reconciliation; no corrected benchmark truth is declared.',
  'Failed recall on three questions does not establish absence of training contamination; GPT-4o-generated perturbations and selected error samples constrain conclusions.',
  'The ACL paper citation points to source code and prompts, but current review acquired neither; no code identity, license, reproducibility or execution claim is granted.']
 omissions=[
  dict(item='Public benchmark reconstruction',next_action='Acquire code/prompts/data at a cutoff-filtered commit, validate exact question IDs and resolve the one-item count mismatch.'),
  dict(item='Question-level and statistical evidence',next_action='Recover raw outputs, exact per-item scores, seeds, model API/revision, paired design and uncertainty before comparing small score differences.'),
  dict(item='Business-language translation and graph truth',next_action='Create held-out banking-like public cases with decision clocks, source spans, expert-added versus stated graph edges and blinded review.'),
  dict(item='Safe code/agent execution',next_action='Use an allowlisted, resource-bounded, network-disabled interpreter; preserve generated code, tool inputs, failures, provenance and independent calculation checks.'),
  dict(item='External/model cost',next_action='Measure prompts, tokens, tool calls, active review, latency, invalid outputs and repeatability on frozen public cases; no costs are supplied here.'),
  dict(item='Coverage',next_action='Continue inspecting 56 unread primary originals and independent complementary searches/citation trails; do not treat this one article as census closure.')]
 write(BASE/'critical-review.json',dict(status='pass_for_bounded_primary_review',reviewer=dict(name='Codex author/coordinator',kind='author'),findings=claims,
  source_critical_qualifications=critical,evidence=[ref(BASE/n,'Inspected primary source review') for n in ['source-audit.json','version-selection.json','exact-results.json','omissions-register.json']],
  limitations=LIMITS,model_execution=False,code_execution=False,visual_acceptance=False,coverage_closure=False))
 write(BASE/'omissions-register.json',dict(global_blocker=None,items=omissions,unavailable_originals=[],no_source_waivers=True))
 write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Bounded original review plan'),ref(BASE/'source-audit.json','Authenticated source')],checks=[
  'Verify genuine publisher text against identity page and save the named scholarly PDF.',
  'Inspect methods, benchmark construction, each reported result and limitations across all15 pages.',
  'Separate source-reported scores from exact derived differences and reconcile displayed denominator counts.',
  'Update only candidate167 and its task map; preserve all other census records.',
  'Scope remaining claims to formal CLADDER reasoning and propose bank-relevant public gates before expensive studies.']))
 write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_review',findings=claims,qualifications=critical,limitations=LIMITS,
  evidence=[ref(BASE/n,'Source-critical bounded review') for n in ['source-audit.json','exact-results.json','critical-review.json']],native_execution=False,coverage_acceptance=False))
 old=read(PRIOR/'census-register.json');new=copy.deepcopy(old)
 row=next(x for x in new['items'] if x['id']=='LA01-candidate-167');assert row['disposition']=='open_original_not_inspected'
 row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
  source_key='exec21_prophets',primary_source_record=read(BASE/'source-audit.json')['sources'][0],
  later_primary_review=ref(BASE/'primary-review.json','Bounded source-critical inspection'),
  task_families=['identification','evaluation_cost','business_translation','diagram_construction','agent_architecture'],
  mapping_basis='Inspected formal benchmark, intermediate graph-generation step, generated DoWhy calculation and explicit non-bank limitations.',
  availability='Genuine ACL Anthology original acquired from bounded public endpoint; prior allowlist and sandbox DNS failures preserved.',
  effect_on_claims='Supports formal task-boundary and tool-use arguments; does not qualify banking translation, causal discovery, graph truth or financial effect inference.',
  next_action='Acquire exact repository prompts/data/code and continue unrelated open candidates; no model or generated code execution.')
 counts=Counter(x['disposition'] for x in new['items'])
 assert len(new['items'])==117 and counts['inspected_primary_retained_with_limits']==57 and counts['open_original_not_inspected']==56
 assert all(a==b for a,b in zip(old['items'],new['items']) if a['id']!='LA01-candidate-167')
 new.update(counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved56/57 predecessor'),
   changes=['Candidate167 authenticated and inspected; all116 other records preserved.'],
   evidence=[ref(BASE/'primary-review.json','Full paper inspection')],closure=False,
   interpretation='57/113 originals inspected;56 unread;four crosscutting obligations remain; task mappings do not prove coverage.')
 write(BASE/'census-register.json',new)
 tasks=copy.deepcopy(read(PRIOR/'task-map.json'));assert len(tasks['task_families'])==14
 mapped=set(row['task_families']);updates=[]
 for task in tasks['task_families']:
  name=task['id']
  if name in mapped:
   if 'LA01-candidate-167' in task.get('uninspected_candidate_ids',[]):task['uninspected_candidate_ids'].remove('LA01-candidate-167')
   if 'LA01-candidate-167' not in task.setdefault('inspected_candidate_ids',[]):task['inspected_candidate_ids'].append('LA01-candidate-167')
   if 'exec21_prophets' not in task.setdefault('inspected_source_keys',[]):task['inspected_source_keys'].append('exec21_prophets')
   updates.append(name)
  task['coverage_acceptance']=False
 tasks.update(register=ref(BASE/'census-register.json','57 inspected,56 unread'),supersedes=ref(PRIOR/'task-map.json','Preserved14-family map'))
 tasks.setdefault('primary_application_notes',{})['causal_prophets']='Formal known-probability tasks and generated-data tool use do not test business translation, discovery on bank data or identification from authentic observational records.'
 write(BASE/'task-map.json',tasks)
 write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=['LA01-candidate-167'],unchanged_other_records=116,
  original_candidates=113,inspected=57,unread=56,task_families=14,updated_families=updates,coverage_acceptance=False,
  evidence=[ref(BASE/'census-register.json','Census conservation'),ref(BASE/'task-map.json','14-family map')]))
 write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
  inputs=['Business question with decision owner/time horizon/action/outcome/unit/cost and information available before action.',
   'Source-backed variable definitions and evidence links; user-vetted candidate graph with uncertain edges and provenance.',
   'Explicit statistical target, identification assumptions and selected symbolic or data-backed calculation type.'],
  outputs=['Question/graph/estimand distinction, unresolved assumptions and competing models.',
   'Typed tool request and reproducible calculation only when data, design and conditions are actually supplied.',
   'Generated code, package/runtime hashes, bounded stdout/stderr, tool authorization and failure status; no autonomous policy action.'],
  oracle=ref(BASE/'exact-results.json','Displayed paper arithmetic only'),
  qualification=['Public known-law translation tasks with blinded experts and explicit alternative DAGs.',
   'Separate graph-role/source-span accuracy from identification and numerical-result accuracy.',
   'Compare no-tool, formula checker, constrained library and generated-code agents under identical budgets.',
   'Freeze models/prompts/tool versions and measure invalid code, leakage, uncertainty, cost and repeated-run variance.',
   'Do not justify costly bank studies until public prototype shows reproducible useful merit.']))
 write(BASE/'review.json',dict(status='pass_for_bounded_candidate_inspection',coverage_acceptance=False,limitations=LIMITS,
  evidence=[ref(BASE/'primary-review.json','Source-critical review'),ref(BASE/'reconciliation-review.json','Candidate and task-map preservation'),ref(BASE/'conversion-contract.json','Proposed interface, not executable integration')]))
 write(BASE/'inspection-progress.json',dict(finding='Candidate167 inspected; census57/56; formal CLADDER gains, PoT execution boundary and one-item query-count discrepancy recorded.',
  next_action='Integrate this bounded literature review into the paired monograph/sponsor; continue unread candidate originals and complementary search routes.',
  evidence=[ref(BASE/n,'Census progress') for n in ['source-audit.json','review.json','census-register.json','task-map.json','omissions-register.json']]))
 verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
 print(json.dumps(dict(inspected=57,unread=56,mapped_families=updates,records=2,code_execution=False)))

if __name__=='__main__':main()
