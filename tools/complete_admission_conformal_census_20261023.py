#!/usr/bin/env python3
"""Preserving census successor from inspected originals and exact authored witnesses."""
import copy,hashlib,json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import admission_conformal_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23'
BASE=DAY/'census-admission-conformal-v1';PRIOR=DAY/'census-geometric-hierarchical-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Author primary-text review, not independent review or empirical reproduction.',
 'No new pixel review; six-image allowance exhausted. Pseudocode has alternate text extraction.',
 'No downloaded code or live model executed. Underlying papers, repositories and model claims need separate originals before new technical reliance.',
 'Public/authored benchmarks do not establish bank truth, identification, native capability, deployment prevalence or ROI.',
 'Claim-dependency graph is not intervention DAG; inspection does not endorse every claim or close coverage.']
SPECS=[dict(id='LA01-candidate-0',short='admission',key='exec23_epistemic_admission',
 title='A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory',
 author='Xiaoyang Li and Yiqi Wang and Chencheng Zhu and Ke Xu and Wencheng Yang and Zequn Sun and Pingan Song and Yiqun Duan and Taotao Cai',surname='Li',version='2609.30813v1',date='2026-09-25',
 filename='A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory Li(2026).pdf',
 anchors={1:'Identity and summary.',3:'Earlier admissions change later candidate streams.',4:'Authored input lineage versus declared generated provenance; Static rule agreement and simulated exposure.',5:'Static600/200/400 split; six agents/six rounds;100 configurations plus separate pools.',6:'Shared judge/agent families; Live descriptive, Static clustered tests.',7:'Own-stream denominators and source-type dependence.',8:'553 constrained memory-only probes; not deployment rates.',9:'Paraphrase and authoritative-type failures.',10:'Oracle lineage cannot certify independent truth.',11:'Share-all ablation does not test support-counting policies.',16:'Adapters and corrected/refrozen assembly.',17:'Shared collapse predicate and merged rows.',18:'Specific Mem0/A-MemGuard components.',21:'Different policy-stream denominators.',22:'Pooled versus extra cross cells.',26:'Retraction available but untested; declarations incomplete.',27:'Gold-using grader; blind versus reviewed labels.',28:'Probe paraphrase misses; category-balanced validation.',29:'Assertion versus citation/provenance.',30:'Judge/agent entanglement and sampling.',31:'No equal-coverage comparison.',32:'Selected confirmatory tests; transcripts promised on acceptance.',33:'Author-reported freezes and scoring-only gold.',34:'Authored fiction and explicit limits.'},
 claims=['Admission, lineage, simulated exposure and assertion adoption are distinct from bank loss.',
 'Policy-dependent candidate streams require separate fixed-candidate and closed-loop comparisons.',
 'Perfect copy lineage removes duplication without proving independent claims true.',
 'Imported verdicts, authored truth, scoring gold and declared provenance are distinct.',
 'Source-type gating fails in specified false-authoritative scenarios; correction/equal-coverage performance open.',
 'Blind validation, paraphrase misses, selected pools and shared model roles limit interpretation.']),
 dict(id='LA01-candidate-276',short='conformal',key='exec23_scientific_conformal',
 title='Though Language Models Err While They Strive: Conformal Prediction for Self-Correcting Scientific Generation',
 author='Mingqiao Mo and Yunlong Tan and Hao Zhang',surname='Mo',version='2607.16704v1',date='2026-07-18',
 filename='Though Language Models Err While They Strive Conformal Prediction for Self-Correcting Scientific Generation Mo(2026).pdf',
 anchors={1:'Identity/headlines.',3:'Fact splitting and pipeline; figure text only.',4:'Truth/splitter assumed; incomplete extracted score definitions.',5:'Correctness and justified order; relevance excluded.',6:'Semantic approximate-graph requirements beyond acyclicity.',7:'Low-risk acceptance and unproved semantic template assertion.',8:'Broad theorem; MATH71.2 versus48.9 contradicts universal superiority; table discrepancies.',9:'Exchangeable pairs/fixed mapping assumed; branch-score direction reverses.',10:'Table/prose discrepancies; selected branching not randomized benefit.',14:'Cascade proof assumes accepted prefixes truly valid.',15:'Failed final attempt has no increment/exit; fallible LLM validator.',16:'Proof additionally needs truth of safe subgraphs, nesting and semantic graph properties.',17:'Domain improvement/fallback require conditions.',18:'Dimensional consistency heuristic is not entailment.',19:'Fitted scores/weights need independent calibration.',20:'Fixed measurable transformation proof; measured determinism below1; bounded-template complexity assumptions.',21:'Unproved edge-error to whole-chain bound; causal wording is linguistic.',22:'Minimum quantile needs correct event/direction; lexical classification is not statistical independence.',23:'Model/run roles and cost protocol unresolved.',24:'Linear fallback for cyclic graph does not prove semantic properties.',25:'Re-prompted output requires its own validation scope.'},
 claims=['Exchangeability preservation presupposes exchangeable complete examples and fixed measurable mapping; neither truth nor exchangeability is created.',
 'Semantic graph properties exceed acyclicity or low validation scores.',
 'Conflicting tables do not support superiority across all benchmarks.',
 'Printed Algorithm3 has no bounded exit on persistent last-attempt failure; not a native runtime observation.',
 'Score direction, target, run identity and calibration access need clarification before certification.',
 'Progressive validation and bounded retries are prototype candidates; universal correctness/calibration/bank benefit unqualified.'])]
class Meta(HTMLParser):
 def __init__(self):super().__init__();self.data={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' and 'content' in a:self.data.setdefault(a.get('name',a.get('property','')),[]).append(a['content'])

def main():
 assert not (BASE/'source-audit.json').exists(),'Preserve bound artifacts'
 sources=[]
 for s in SPECS:
  short=s['short'];pdf=RAW/('exec23_census_'+short+'_pdf.pdf');html=RAW/('exec23_census_'+short+'_abstract.html')
  receipt=read(pdf.with_suffix('.receipt.json'));hr=read(html.with_suffix('.receipt.json'))
  assert receipt['status']==hr['status']=='saved'
  for p,r in [(pdf,receipt),(html,hr)]:assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
  assert pdf.read_bytes().startswith(b'%PDF-');m=Meta();m.feed(html.read_text())
  assert m.data['citation_title']==[s['title']] and m.data['citation_date']==[s['date'].replace('-','/')]
  assert s['date']<='2026-10-07' and m.data['og:url'][0].endswith(s['version'])
  first=(BASE/(short+'-page-001.txt')).read_text();assert s['version'] in first and s['surname'] in first
  dest=ROOT/'docs/papers'/s['filename']
  if dest.exists():assert dest.read_bytes()==pdf.read_bytes()
  else:dest.write_bytes(pdf.read_bytes())
  anchors=[dict(anchor=f'PDF physical page {n}',finding=f,extracted_text=ref(BASE/(short+f'-page-{n:03}.txt'),'Inspected primary text; no new pixel review')) for n,f in s['anchors'].items()]
  sources.append(dict(integrated_citation_key=s['key'],kind='paper',title=s['title'],author=s['author'],authors=s['author'],first_author=s['surname'],year=2026,source_identity=receipt['url'],version_date='arXiv:'+s['version']+'; '+s['date']+'; acquired2026-10-23',local_path=str(dest.relative_to(ROOT)),sha256=receipt['sha256'],bytes=dest.stat().st_size,local_copy=ref(dest,'Authentic cutoff original'),inspected_anchors=anchors,supported_claims=s['claims'],limitations=LIMITS,identity_evidence=[ref(html,'Archive identity'),ref(html.with_suffix('.receipt.json'),'Identity receipt'),ref(pdf.with_suffix('.receipt.json'),'PDF receipt')]))
 code=Path(exact.__file__)
 reference=dict(integrated_citation_key='exec23_admission_conformal_reference',kind='project_derivation_and_exact_reference',title='Exact references for copied support, conditional streams and scientific-validation contracts',author='Causal banking proposal project',year=2026,source_identity=str(code.relative_to(ROOT)),version_date='2026-10-23',local_copy=ref(code,'calculate(): rational arithmetic and bounded control flow'),inspected_anchors=['calculate()'],supported_claims=['Independent80%-accurate majority112/125; perfect copies4/5.', 'Stipulated net0 and1 USD per request.', 'Five independent90%-valid outputs yield family error40951/100000.', 'n5,alpha0.1 needs rank6/infinity sentinel.', 'Minimum quantiles can lose ordinary score-coverage, distinct from hereditary filtering.', 'Always-failing literal Algorithm3 repeats maximum attempt count.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=sources+[reference],cutoff='2026-10-07',visual_acceptance=False,native_execution=False))
 write(BASE/'exact-results.json',exact.calculate())
 write(BASE/'primary-review.json',dict(status='pass_for_primary_review_not_claim_endorsement',evidence=[ref(BASE/'source-audit.json','Primary findings'),ref(BASE/'exact-results.json','Independent references'),ref(BASE/'conformal-algorithms-raw.txt','Alternate extraction')],findings=[c for s in sources for c in s['supported_claims']],limitations=LIMITS,coverage_acceptance=False,visual_acceptance=False))
 old=read(PRIOR/'census-register-v2.json');new=copy.deepcopy(old);changed={s['id']:x for s,x in zip(SPECS,sources)}
 for row in new['items']:
  if row['id'] not in changed:continue
  source=changed[row['id']];assert row['disposition']=='open_original_not_inspected'
  row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=source['integrated_citation_key'],primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Bounded original review'),mapping_basis='Inspected methods, assumptions, denominators and limits.',availability='Genuine cutoff original saved/inspected; code/data/proof dependencies separate.',effect_on_claims='Design/critical evidence; no universal guarantee or capability.',next_action='Integrate qualified argument; inspect code, manifests, labels and proof originals before certification/performance claims.')
 assert len(new['items'])==len(old['items'])==117
 assert all(a==b for a,b in zip(old['items'],new['items']) if a['id'] not in changed)
 counts=Counter(x['disposition'] for x in new['items']);assert counts['inspected_primary_retained_with_limits']==67 and counts['open_original_not_inspected']==46
 new.update(counts=dict(counts),status='successor_bounded_primary_review',supersedes=ref(PRIOR/'census-register-v2.json','Preserved65/48'),changes=['Only candidate0 and276 updated;115 other rows unchanged.'],evidence=[ref(BASE/'primary-review.json','Two reviews')],closure=False,interpretation='67/113 inspected;46 unread;four searches remain.')
 write(BASE/'census-register.json',new)
 task=copy.deepcopy(read(PRIOR/'task-map-v2.json'))
 for f in task['task_families']:
  f['coverage_acceptance']=False
  for key,source in changed.items():
   if key in f.get('uninspected_candidate_ids',[]):
    f['uninspected_candidate_ids'].remove(key)
    if key not in f.setdefault('inspected_candidate_ids',[]):f['inspected_candidate_ids'].append(key)
    if source['integrated_citation_key'] not in f.setdefault('inspected_source_keys',[]):f['inspected_source_keys'].append(source['integrated_citation_key'])
 task.update(register=ref(BASE/'census-register.json','67 inspected46 unread'),supersedes=ref(PRIOR/'task-map-v2.json','Preserved families'));write(BASE/'task-map.json',task)
 write(BASE/'omissions-register.json',dict(whole_census_complete=False,items=[
 dict(gap='46 unread originals/four searches',action='Continue cutoff acquisition and primary inclusion/exclusion review.'),
 dict(gap='CPB reproduction/rights',action='Inspect cutoff repository, license, freezes and promised transcripts; scope component findings.'),
 dict(gap='Decision-useful memory comparison',action='Register fixed-candidate/closed-loop tracks, blind labels, utility/coverage, lineage and retraction using public/generated truth.'),
 dict(gap='SFC proof/implementation',action='Inspect underlying conformal originals, score/tie definitions, run identity, calibration truth, threshold direction and retries. No certification before agreement.'),
 dict(gap='SFC conflicting tables',action='Acquire run-level results, denominators and paired comparisons before ranking claims.'),
 dict(gap='Adaptive banking queries',action='Freeze pipeline, separate fitting/calibration/testing and define query selection; derive control or abstain.'),
 dict(gap='Visual/external acceptance',action='Fresh visual review and later independent/native/bank work; independent sources remain eligible.')]))
 write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=115,original_candidates=113,inspected=67,unread=46,evidence=[ref(BASE/'census-register.json','Conserved rows'),ref(BASE/'task-map.json','Task coverage')]))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_review',evidence=[ref(BASE/'plan.md','Plan'),ref(BASE/'primary-review.json','Findings')],findings=['No blanket guarantee/ranking endorsement.','Public evidence/authored witnesses/native studies separate.','No phase/global blocker.']))
 write(BASE/'review.json',dict(status='pass_for_scoped_primary_and_authored_argument',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed source/argument') for n in ['primary-review.json','plan-review.json','source-audit.json','exact-results.json','census-register.json','task-map.json','reconciliation-review.json','omissions-register.json','development.tex']],limitations=LIMITS,capabilities=[],native_execution=False,visual_acceptance=False,whole_census_complete=False))
 verify_bindings(read(BASE/'review.json'));print(json.dumps(dict(inspected=67,unread=46,added_genuine_papers=2,coverage_complete=False)))
if __name__=='__main__':main()
