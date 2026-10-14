#!/usr/bin/env python3
"""Prepare a preserving, source-bound integrated proposal successor."""
import argparse,hashlib,json,re,subprocess
from fractions import Fraction as F
from pathlib import Path
import build_integrated_monograph_v12 as shared
import master_control as core
ROOT=core.ROOT;DOCS=ROOT/'docs';BASE=DOCS/'program/execution/2026-10-14/reader-repair'
OLD=DOCS/'causal_proposal_l2_v4_2026-10-13.tex'
NAME='causal_proposal_integrated_2026-10-14';DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
PRIOR_AUDIT=DOCS/'program/execution/2026-10-13/l2/final-v4/reader/source-audit.json'
ref=shared.ref

def write(path,obj):
 assert not path.exists(),path
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def exact():
 # Same covariance from latent and direct SCMs; residual coefficient checked
 # both through conditional variance and the independent 2x2 normal equation.
 rows=[]
 for s in [F(0),F(1,4),F(1,2),F(1),F(4)]:
  v=s/(1+2*s);coefficient=v/(F(1,2)+v)
  varw=F(1,2)+s;aw=yw=F(1,2);ay=F(1,2)
  normal=(varw*ay-aw*yw)/(varw-aw*aw)
  assert coefficient==normal==2*s/(1+4*s)
  rows.append({'score_noise_variance':str(s),'residual_variance':str(v),'coefficient':str(coefficient),'normal_equation':str(normal)})
 assert rows[2]['coefficient']=='1/3'
 lhs=[]
 for p in [F(1,4),F(1,2),F(3,4)]:
  for e in [F(1,5),F(2,5),F(4,5)]:
   for m0,m1 in [(F(0),F(2)),(F(1),F(3)),(F(2),F(6))]:
    mu0,mu1=F(1),F(3)
    expectation=m1-m0+p/e*(mu1-m1)-(1-p)/(1-e)*(mu0-m0)
    remainder=(e-p)*((m1-mu1)/e+(m0-mu0)/(1-e))
    assert expectation-(mu1-mu0)==remainder
    lhs.append({'p':str(p),'e':str(e),'m0':str(m0),'m1':str(m1),'bias':str(remainder)})
 assert 6*5//2*2**4==240
 return {'kind':'exact_project_derivations','package_or_live_execution':False,'random_draws':0,
  'observational_equivalence':{'latent_model_variances':['1/2','1/2','1/2'],'direct_model_variances':['1','3/4'],
     'observed_covariance':[['1','1/2'],['1/2','1']],'effects':['0','1/2'],'no_selection':True},
  'proxy_rows':rows,'two_world_interval_bound':{'assumptions':'Identical observed records and admissible text laws; internal randomness same in both worlds; both marginal coverages >=1-alpha',
     'derivation':'Under the common report law P(E0 and E1)>=1-P(not E0)-P(not E1)>=1-2alpha; the set must then have diameter >= Delta',
     'alpha':'1/20','diameter_event_lower_bound':'9/10','example_delta':'2/5'},
  'decision_example':{'gross_values':['0','8'],'offer_cost':'3','net_values':['-3','5'],'prior_threshold':'3/8',
     'q':'1/2','current_expected_optimum':'1','perfect_information_value':'5/2','EVPI':'3/2',
     'all_values_stipulated':True},
  'ci_family':{'p':6,'fixed_queries':240,'alpha':'1/5000','union_bound':'6/125','graph_coverage_claim':False},
  'aipw_population_remainder':{'formula':'(e-p)*((m1-mu1)/e+(m0-mu0)/(1-e))','rational_identity_cases':lhs,
     'interpretation':'Algebra only; causal identification and statistical asymptotics need separate assumptions'}}

def source(key,title,author,kind,identity,version,local,anchor,claims,records):
 return {'integrated_citation_key':key,'kind':kind,'title':title,'author':author,'year':2026,'source_identity':identity,
   'version_date':version,'local_copy':ref(ROOT/local,anchor),'records':records,'inspected_anchors':[anchor],
   'claims':claims,'limitations':['Only the explicitly stated inspected or project scope; no bank or independent acceptance.']}

def prepare():
 assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
 # Correct two overcompressed draft statements without changing recorded outputs.
 correction={'kind':'successor_manuscript_corrections','preserved_drafts':[ref(ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L4/chapter.tex','Initial short draft; superseded for reader integration'),
   ref(ROOT/'docs/program/comprehensive-v14/work/LL.TASK.estimation_validation/task-synthesis.md','Recorded task synthesis; historical omissions sentence corrected below')],
  'findings':['The initial L4 draft repeats earlier text and cannot independently meet the 20-22 substantive-page allocation; the preserving chapter joins original discovery, temporal evidence and new nonduplicate derivations.',
    'The initial phrase score measured without sampling error confused population arithmetic with measurement error; the successor states explicit noisy-score laws and population moments.',
    'Candidate 269, Text and Causal Inference, already has an inspected original in the later census under exec13_census_text_review_arxiv; it is not still uninspected. Candidates 175 and 241 likewise have later inspected originals.',
    'CausalDS has both uncapped and capped means; preserve both and distinguish dashboard capping from missing package functionality.',
    'First L4 receipt draft lacked the task contract; rejected draft preserved and corrected receipt recorded.'],
  'corrected_omissions':{'resolved_later':['LA01-candidate-175','LA01-candidate-241','LA01-candidate-269'],
     'still_uninspected_selected':['LA01-candidate-31','LA01-candidate-256','LA01-candidate-266']},
  'evidence':[ref(ROOT/'docs/program/execution/2026-10-13/llm-census/source-audit.json','Later original-source custody and anchors'),
              ref(BASE/'l4-development.tex','Corrected expanded discovery argument'),ref(BASE/'estimation-development.tex','Correct target and scorer interpretation')]}
 write(BASE/'draft-repair-review.json',correction)
 write(BASE/'exact-results.json',exact())
 comp=ROOT/'docs/program/execution/2026-10-14/commercial-latent-comparison/comparison.md'
 subprocess.run(['pandoc','--from=markdown+raw_tex+tex_math_single_backslash','--to=latex','--wrap=auto',str(comp),'-o',str(BASE/'commercial-latent.tex')],check=True,timeout=20)
 # Convert top-level markdown heading to section within existing commercial chapter.
 c=(BASE/'commercial-latent.tex').read_text();c=c.replace('\\section{Choosing a commercial latent-model component}', '\\section{Choosing a commercial latent-model component}')
 (BASE/'commercial-latent.tex').write_text(c)
 base14='docs/program/execution/2026-10-14/'
 est=json.loads((ROOT/(base14+'estimation-validation/primary-review.json')).read_text())
 java=json.loads((ROOT/(base14+'java-latent/primary-review.json')).read_text())
 reuse=json.loads((ROOT/(base14+'causallearn-reuse/primary-review.json')).read_text())
 records=[]
 for item in est['packages']:
  records.extend({'local_copy':r,'source_identity':item['identity'],'version_date':item['commit_date']+'; '+item['commit'],'inspected_anchors':item['inspected_anchors']} for r in item['originals'])
 sources=[source('exec14_estimation_sources','OCI and CausalDS pinned estimation and scoring source review','Netflix-Skunkworks/oci-agent; andleb/causalds','software_primary_sources',
  'https://github.com/Netflix-Skunkworks/oci-agent ; https://github.com/andleb/causalds','OCI a978030e; CausalDS c74671d; inspected 2026-10-14',base14+'estimation-validation/primary-review.json','Notebook cells 42-43; scorer lines 152-174, 1507-1568, 3529-3546',
  ['Uniform retained AIPW is a trimmed target, not conventional overlap weighting','Scorer publishes both uncapped and capped interval means','Missing-ID defaults and nonfinite endpoint checks require guarded adaptation','Notebook timeout is unbounded; selected paths statically inspected, not executed'],records),
 source('exec14_estimation_oracles','Exact target and interval-score comparison','Causal banking proposal','project_derivation', 'Project authored finite reference','2026-10-14',base14+'estimation-validation/exact-oracle.json','Three strata, target rules, cap reversal and selected denominator',
 ['Full effect 18/5, trimmed 4, overlap 1656/433','Capping at ten reverses the illustrated score-pair ranking','No package execution or bank effect'],[{'local_copy':ref(ROOT/'tools/review_estimation_validation_20261014.py','Fraction calculations')}]),
 source('exec14_discovery_oracles','Discovery information, decision and CI-family derivations','Causal banking proposal','project_derivation','Project authored derivations','2026-10-14',str((BASE/'exact-results.json').relative_to(ROOT)),'Identical Gaussian observation laws, proxy residual, two-world coverage, EVPI and AIPW algebra',
 ['Hidden and direct Gaussian models share covariance but effects differ','Union-bound interval diameter condition under identical inputs','Exact costs and prior threshold, no bank ROI','CI-family false-rejection bound is not graph coverage'],[{'local_copy':ref(Path(__file__),'Exact Fraction calculations and proof assumptions')}]),
 source('exec14_java_latent_sources','Tetrad FCI, RFCI and endpoint path inspection','cmu-phil/tetrad','software_primary_sources','https://github.com/cmu-phil/tetrad','b89afaf952a4fd647df0d85b08102250106c6764; 2026-09-22; acquired 2026-10-14',base14+'java-latent/primary-review.json','Six original sources matched to tree; selected search, endpoint and orientation branches',
 ['FCI source whole-candidate tests and final-orientation branch require executable qualification','RFCI is a distinct path','Edge constructor may reverse node order; marks bind to proximal nodes','No Java FCI/RFCI engine executed'],[{'local_copy':x['original'],'source_identity':x['source_identity'],'inspected_anchors':x['inspected_anchors']} for x in java['sources']]),
 source('exec14_causallearn_reuse','causal-learn source and scoped PC reuse decision','cmu-phil/causal-learn; Causal banking proposal','software_primary_sources','https://github.com/cmu-phil/causal-learn','0dacacf36390e3084704636bc3c36e82e35ee0cc; 2026-09-04; inspected 2026-10-14',base14+'causallearn-reuse/primary-review.json','Six pinned source files, twelve dependency declarations, endpoint/CI semantics and explicit deferred admission',
 ['Scoped PC direct integration preferred; FCI separate','MIT root license does not close full dependencies','No engine execution or adapter admitted'],[{'local_copy':x['local_copy'],'source_identity':x['source_identity'],'inspected_anchors':x['inspected_anchors']} for x in reuse['sources']]+[{'local_copy':ref(ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_causallearn/decision.json','Explicit selection and integration_allowed=false')}]),
 source('exec14_execution_evidence','Local interface execution identities and evidence labels','Causal banking proposal','project_implementation','Project runtime and immutable local journals','local-runtime/1; audited 2026-10-14',base14+'execution-labels/evidence-labels.json','Execution classes; source identity equals IN04 and servicing runtime',
 ['Nine actual narrow runtime operations','Eleven prior library/CLI/MCP scientific parity cases at protocol 2025-11-25','80 local controller conformance checks, zero live calls','Mock, static, exact, runtime and owner-run evidence remain distinct'],[{'local_copy':ref(ROOT/p,a)} for p,a in [
 ('docs/program/repair-v12/work/IN04/implementation-manifest.json','Source/runtime identities'),('docs/program/repair-v12/work/IN04/transport-checks.json','Actual 11-case local transport transcript'),('docs/program/repair-v12/work/LA05/verification.json','80 local checks and no live calls'),('src/causalbank/runtime_v12.py','Bounded dispatch and idempotency')]]),
 source('exec14_servicing_evidence','Servicing local interface screen and exact policy reference','Causal banking proposal','project_empirical_and_derivation','Project preregistered local screen; generated finite law','2026-10-14; preserved negative outcome',base14+'servicing-journey/local-review.json','98 requests, 94 matches, 24 parity cases, 964 rational checks and negative expectation diagnosis',
 ['Corrupt bytes failed safely; frozen expected-name mismatch retained','Only supported operations execute; no servicing estimator','Exact policy values and adverse precision/missing-information results reproduced','Timing and stipulated currency scenario have explicit scope'],[{'local_copy':ref(ROOT/p,a)} for p,a in [
 (base14+'servicing-journey/local-journal.json','All 98 slots and resource observations'),(base14+'servicing-journey/exact-reproduction.json','Exact finite policy results and radii'),(base14+'servicing-journey/expectation-correction.json','No runtime integrity breach; negative trial retained'),('docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.servicing/local-results.json','Bound results and planning cost scenario')]])]
 write(BASE/'source-audit.json',{'sources':sources,'cutoff':'2026-10-07','new_content_date':'2026-10-14','prior':ref(PRIOR_AUDIT,'Unchanged whole-reader citations'),'correction':ref(BASE/'draft-repair-review.json','Explicit successor corrections')})
 bib=[]
 for x in sources:bib.append('@misc{'+x['integrated_citation_key']+',\n author={{'+shared.escape(x['author'])+'}},\n title={'+shared.escape(x['title'])+'},\n year={2026},\n note={'+shared.escape(x['version_date'])+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib))
 text=OLD.read_text()
 oldl4='\\input{program/repair-v12/work/LA03/chapter-draft.tex}\n\\input{program/execution/2026-10-13/llm-census/temporal.tex}'
 assert text.count(oldl4)==1
 text=text.replace(oldl4,'\\input{program/comprehensive-v14/work/TEXT.DRAFT.L4/chapter-reviewed.tex}')
 insertions=[('program/execution/2026-10-13/pgmpy-reuse/decision.tex','causallearn-decision.tex'),
 ('program/execution/2026-10-13/commercial-latent/comparison.tex','commercial-latent.tex'),
 ('program/execution/2026-10-13/data-code/chapter.tex','estimation-development.tex'),
 ('program/execution/2026-10-13/observations-journey/section.tex','execution-meaning.tex')]
 for anchor,filename in insertions:
  marker='\\input{'+anchor+'}';assert text.count(marker)==1
  text=text.replace(marker,marker+'\n\\input{program/execution/2026-10-14/reader-repair/'+filename+'}')
 pattern=re.compile(r'\\bibliography\{([^}]+)\}');assert len(pattern.findall(text))==1
 text=pattern.sub(lambda m:'\\bibliography{'+m.group(1)+',program/execution/2026-10-14/reader-repair/refs}',text)
 DRIVER.write_text(text)
 files=shared.scan(DRIVER);cited={k.strip() for _,t in files for group in re.findall(shared.CITE,t) for k in group.split(',')}
 prior=json.loads(PRIOR_AUDIT.read_text());known={x['integrated_citation_key'] for x in prior['sources']}|{x['integrated_citation_key'] for x in sources}
 assert cited<=known,cited-known
 write(BASE/'prepared-inputs.json',{'inputs':[ref(OLD,'Immutable predecessor driver'),ref(PRIOR_AUDIT,'Prior source identities'),ref(comp,'Reviewed vendor comparison'),ref(Path(__file__),'Preparation and exact arithmetic')],
 'generated':[ref(p,'Prepared successor input') for p in [DRIVER,BASE/'source-audit.json',BASE/'refs.bib',BASE/'exact-results.json',BASE/'draft-repair-review.json']+list(BASE.glob('*.tex'))+[ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L4/chapter-reviewed.tex']]})
 print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_citations':len(sources),'all_citations':len(cited),'prior_reader_preserved':True}))

if __name__=='__main__':prepare()
