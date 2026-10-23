#!/usr/bin/env python3
"""Record one versioned original without turning partial census progress into completion."""
from collections import Counter
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json
import controlled_writes_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];DAY=ROOT/'docs/program/execution/2026-10-23';BASE=DAY/'census-controlled-writes-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
class Meta(HTMLParser):
 def __init__(self):super().__init__();self.tags={}
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='meta' and d.get('name','').startswith('citation_'):self.tags.setdefault(d['name'],[]).append(d.get('content'))
def main():
 assert read(ROOT/'docs/program/state.json')['execution_runtime']['active']['operation']=='LL.CENSUS'
 m=Meta();m.feed((RAW/'exec23_cpun_v1_abs.html').read_text());title='CPUNeSy: Controlling Model Writes for Reliable Neuro-Symbolic Reasoning'
 assert m.tags['citation_title']==[title] and m.tags['citation_date']==['2026/09/28']
 assert m.tags['citation_author']==['Li, Zeyan','Qiu, Siyuan','Zhao, Shuai','Xu, Jianfeng']
 paper=ROOT/'docs/papers/CPUNeSy Controlling Model Writes for Reliable Neuro-Symbolic Reasoning Li(2026).pdf'
 data=paper.read_bytes();receipt=read(RAW/'exec23_cpun_v1_pdf.receipt.json')
 assert data.startswith(b'%PDF-') and data==(RAW/'exec23_cpun_v1_pdf.pdf').read_bytes()
 assert hashlib.sha256(data).hexdigest()==receipt['sha256'] and receipt['url']=='https://arxiv.org/pdf/2609.37490v1'
 anchors={3:('predicate unit','Grounding, source checking and deterministic executor architecture.'),4:('source','Admission interface, kernel, cache and source/derived separation.'),5:('Algorithm 1','Certificate gate and explicit sound-source-checker/fragment assumptions.'),6:('not established','Conditional soundness, no-promotion invariant and independence-qualified voting lemma.'),7:('Table 2','Reported native versus fallback results and main-table historical adapter rows.'),8:('63/252','Uncertified solver ablation and fixed-trace checking tradeoffs; adverse grounder regimes.'),9:('Physical','Unmeasured physical storage and cost tradeoffs; prospective validation.'),21:('independent','Standing assumptions and state-soundness proof.'),22:('Hoeffding','Induction completion and conditional concentration proof; step/channel independence needed.'),28:('preregistration','Internal protocol lacks independent timestamp; failed redundancy target and unmeasured guarantees.'),33:('2091','PLACEHOLDER'),34:('not matched','Model labels and historical comparator limitations.')}
 # Table33 prints split counts rather than their sum; use its visible header as an anchor.
 anchors[33]=('1,100','PLACEHOLDER') if False else ('Table 10','Exact printed selective-policy counts; raw archive and immutable model revision gaps.')
 inspected=[]
 for page,(token,claim) in anchors.items():
  p=BASE/'physical'/f'page-{page:03d}.txt';assert token.lower() in p.read_text().lower(),(page,token)
  inspected.append(dict(physical_page=page,anchor=claim,local_text=ref(p,token)))
 limits=['Versioned arXiv original only; its ICLR2027 running header is not independently established conference acceptance.',
  'Reported outcomes and printed-count arithmetic, not raw-record or live-model replication.',
  'Sound source checking and channel independence are conditional assumptions, not supplied by proof validity or two agreeing calls.',
  'Historical adapter rows are unmatched according to the appendix; no ranking or universal superiority is inferred.',
  'No downloaded code executed; no native product, bank benefit, visual or final acceptance.']
 source=dict(integrated_citation_key='exec23_controlled_writes_paper',kind='paper',title=title,filename_title='CPUNeSy Controlling Model Writes for Reliable Neuro-Symbolic Reasoning',author='Zeyan Li and Siyuan Qiu and Shuai Zhao and Jianfeng Xu',first_author='Li',year=2026,
  source_identity='https://arxiv.org/abs/2609.37490v1',version_date='arXiv2609.37490v1;28 September2026;37 physical pages',local_path=str(paper.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),local_copy=ref(paper,'Authentic versioned original'),
  identity_metadata=ref(RAW/'exec23_cpun_v1_abs.html','Title/authors/submission history; identity only'),pdf_receipt=ref(RAW/'exec23_cpun_v1_pdf.receipt.json','Versioned acquisition'),inspected_anchors=inspected,
  supported_claims=['Source admission and derived proof checking are distinct modes; state soundness assumes both sound source and fragment checkers.',
   'Restricted writable predicates prevent direct promotion of a rule-head conclusion but do not prove allowed leaves true.',
   'Voting concentration requires conditional independence and leaves a shared-error floor; two calls do not identify latent parameters.',
   'Printed DeepSeek source recheck removes63 wrong and51 correct answers from2091 items; fallback is a separate uncertified channel.',
   'Main-table adapter rows recur as unmatched historical summaries in the appendix; common display columns do not establish a matched experiment.',
   'Protocol preregistration, complete certificates, model revisions, physical storage and prospective calibration retain explicit gaps.'],limitations=limits)
 project=dict(integrated_citation_key='exec23_controlled_writes_reference',kind='project_derivation_and_exact_reference',title='Independent controlled-write counterexample, voting and selective-serving arithmetic',author='Causal banking proposal project',year=2026,source_identity='tools/controlled_writes_reference_20261023.py',version_date='23 October2026; project-owned checks',local_copy=ref(Path(exact.__file__),'calculate()'),inspected_anchors=['calculate()'],supported_claims=['A false but allowed leaf yields a formally derivable conclusion despite rejecting direct target writes.',
  'Stipulated bias1/5 and slips1/10 give two-vote wrong26/125, answered risk26/107 and majority limit1/5.',
  'Printed selective counts give63 fewer errors and114 extra abstentions; stipulated net savings302 or-154 with explicit costs.'],limitations=limits)
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 predecessor=DAY/'census-goal-state-v1/census-register-v2.json';register=deepcopy(read(predecessor));baseline=deepcopy(register)
 row=next(x for x in register['items'] if x['id']=='LA01-candidate-130');assert row['disposition']=='open_original_not_inspected'
 row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,source_key=source['integrated_citation_key'],primary_source_record=source,
  task_families=['identification','agent_architecture','evaluation_cost'],publication_keys=[source['integrated_citation_key'],project['integrated_citation_key']],
  mapping_basis='Explicit conditional proof/source boundary; architecture and selective-policy accounting. Identification mapping records a limit, not an identified causal effect.',
  availability='Authentic versioned PDF acquired and physically anchored.',effect_on_claims='Scoped design reference; matched-superiority and unconditional semantic-validity claims rejected.',
  next_action='Obtain the original offline archive with per-row/model/split/certificate custody before independent replay; prospectively calibrate source checking on held-out banking-like public tasks.')
 assert all(x==next(y for y in register['items'] if y['id']==x['id']) for x in baseline['items'] if x['id']!=row['id'])
 counts=dict(Counter(x['disposition'] for x in register['items']));assert counts['inspected_primary_retained_with_limits']==70 and counts['open_original_not_inspected']==43
 register.update(counts=counts,supersedes=ref(predecessor,'69/44 valid predecessor'),changes=['Only candidate130 changed; all others including candidate165 acquisition omission remain preserved.'],closure=False,interpretation='70 of113 candidate originals inspected;43 unread; four crosscutting obligations remain.')
 write(BASE/'census-register.json',register)
 predecessor_map=DAY/'census-goal-state-v1/task-map-v2.json';taskmap=deepcopy(read(predecessor_map))
 for family in taskmap['task_families']:
  if row['id'] in family.get('uninspected_candidate_ids',[]):family['uninspected_candidate_ids'].remove(row['id'])
  if family['id'] in row['task_families']:
   for field,additions in [('inspected_candidate_ids',[row['id']]),('inspected_source_keys',row['publication_keys'])]:
    family.setdefault(field,[]);family[field].extend(k for k in additions if k not in family[field])
  family['coverage_acceptance']=False
 taskmap.update(register=ref(BASE/'census-register.json','70/43 successor'),supersedes=ref(predecessor_map,'Preserved prior mappings'))
 write(BASE/'task-map.json',taskmap)
 omissions=dict(items=limits+['43 unread originals and four crosscutting obligations remain.','Candidate165 identity is known but genuine original remains unavailable through the tested publisher route.'],evidence=[ref(DAY/'census-scientific-method-v1/identity-followup.json','Actual failed acquisition; no global blocker')],coverage_acceptance=False)
 write(BASE/'omissions-register.json',omissions)
 evidence=[ref(BASE/n,'Inspected source and exact argument') for n in ['source-audit.json','exact-results.json','development.tex','plan.md','extraction-correction.json','census-register.json','task-map.json','omissions-register.json']]+[ref(Path(__file__),'Audit construction'),ref(Path(exact.__file__),'Independent checks')]
 review=dict(status='pass_for_scoped_source_review',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=evidence,findings=source['supported_claims']+project['supported_claims'],limitations=limits,coverage_acceptance=False,native_execution=False,visual_acceptance=False)
 verify_bindings(review);write(BASE/'review.json',review)
 write(BASE/'progress.json',dict(finding='Candidate130 authentic37-page v1 reviewed; conditional source/proof boundary, selective counts and unmatched-comparator limitation retained. Census70/43.',next_action='Integrate reviewed controlled-write section into preserving reader/sponsor successors, renew exact-byte reviews, then continue43 unread originals and independent obligations. Resolve candidate165 original through another authentic route; do not repeat GIST or medflex.',yield_reason='Release canonical operation for publication; partial census progress is not completion.',evidence=[ref(BASE/'review.json','Scoped review'),ref(BASE/'census-register.json','70/43 census')]))
 print(json.dumps(dict(inspected=70,unread=43,source_records=2,physical_pages=37,full_census_closed=False)))
if __name__=='__main__':main()
