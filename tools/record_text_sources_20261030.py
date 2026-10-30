"""Source-specific receipts for the text-signal comparison, not survey closure."""
from pathlib import Path
import json,hashlib,datetime

R=Path(__file__).resolve().parents[1];O=R/'docs/twelve-hour-closure/2026-10-29';RAW=R/'docs/literature/raw'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifact(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(name,data):(O/name).write_text(json.dumps(data,indent=2)+chr(10))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
specs=[
 ('inferbert','closure30inferbert','InferBERT A Transformer-Based Causal Inference Framework for Enhancing Pharmacovigilance Wang(2021).pdf','10.3389/frai.2021.659622','2021-05-26',
  ['pp3–4: commercial PharmaPendium curation, cohort labels and64:16:20 split;Table1','pp5–6: Algorithm1 and equations2–6 define feature-membership grouping of saved classifier outputs','pp6–10: comparisons, robustness, limitations and relevant references'],
  ['Classification and term-ranking design; reported experimental scope','Observed root term-group score contrast, verified against fixed source code'],
  ['Identified drug or banking intervention effects','Independent numerical reproduction','Public FAERS extract equals the commercially curated cohort']),
 ('deepcausality','closure30deepcausality','DeepCausality A general AI-powered causal inference framework for free text A case study of LiverTox Wang(2022).pdf','10.3389/frai.2022.999289','2022-12-06',
  ['pp4–6: named-entity candidate construction, Algorithm1, group-membership definition','pp5–8: drug-level likelihood labels,14361sentences,90:10split,test-based checkpoint selection,Table1','pp8–11:20terms/18clinical matches,Table2; cannot distinguish confounders/colliders; references inspected'],
  ['Named entity extraction and observational score comparisons','Reported expert relevance and stated scope limits','Published procedure and pinned notebook differ in visible significance filtering'],
  ['Identified intervention effects','Known numerical leakage penalty','Complete multiplicity procedure reproduced by the notebook','Native execution or independent clinical validation']),
 ('pharma','closure30pharma','Bidirectional Encoder Representations from Transformers-like large language models in patient safety and pharmacovigilance A comprehensive assessment of causal inference implications Wang(2023).pdf','10.1177/15353702231215895','2023-12-12',
  ['pp1909–1911: Table1,data construction,classifier tasks,method references,PPR definition','pp1912–1916:Tables2–4,Figures2–5 and expert-relevance interpretation','p1917: references17/18 identify InferBERT/DeepCausality; methods paragraph instead cites9/10;identity mismatch retained'],
  ['Reported model comparisons and expert relevance of enriched terms','PPR formula TP/(TP+FP);Figure5 PPV values.95,.20,.25 visually checked'],
  ['Causal effect magnitude or intervention uncertainty from PPV','Verified live-LLM performance','Independent reproduction of source comparisons']),
 ('veitch','closure30veitch','Adapting Text Embeddings for Causal Inference Veitch(2020).pdf',None,'PMLR2020,volume124,pp919–928',
  ['Section2 equations2.1–2.3: ATT target,initial text sufficiency and treated-population averaging','Section3 Theorems3.1–3.2 and following caveats: preserved outcome/propensity information and estimation assumptions','PDFpage5 visual inspection confirms final Theorem3.1 display omits treated conditioning; earlier definition retained','Sections4–5:semi-synthetic evaluation and limitations; related work and references inspected'],
  ['Conditional constructive route to dimension reduction when text already suffices for adjustment','Original sufficiency and estimation conditions cannot be inferred from predictive accuracy alone'],
  ['Text sufficiency proved for bank case notes','General finite-sample calibration','ATT and ATE silently interchangeable','Appendix proof fully audited; separate appendix not present in this10-page proceedingsPDF'])
]
sources=[]
for name,key,filename,doi,date,anchors,allowed,forbidden in specs:
 p=R/'docs/papers'/filename;assert p.read_bytes().startswith(b'%PDF')
 d=read(RAW/f'closure30_{name}_openalex.json')
 if name=='veitch':d=next(w for w in d['results'] if w['id'].endswith('W3089984751'))
 metadata={'openalex_work':d['id'],'citations':d['cited_by_count'],'is_retracted':d['is_retracted'],'accessed_utc':now,'venue_rank':'not available','caveat':'Live metadata is discovery/identity evidence, not validity or a pre-cutoff citation count.'}
 status={'openalex_retracted':d['is_retracted'],'limit':'Bounded checks, not exhaustive correction clearance.'}
 if name in ['inferbert','deepcausality']:
  status.update(publisher_visible_notices='No retraction/corrigendum/expression-of-concern notice found in inspected visible publisher text',publisher_structured_dates={'retractedDate':'','correctedDate':''},crossref_update_to=read(RAW/f'closure30_{name}_crossref.json')['message'].get('update-to',[]))
 elif name=='pharma':status.update(crossref_update_to=read(RAW/'closure30_pharma_crossref.json')['message'].get('update-to',[]),publisher_limit='Current publisher full route returns the authenticPDF. No distinctHTML notice page inspected; do not claim publisher-status clearance.',date_note='Issue heading November2023;Crossref/OpenAlex publication date12December2023. Both pre-cutoff.')
 else:status.update(publisher_page='Exact PMLR identity and visible page inspected;no correction notice observed',version='PMLR proceedings copy;OpenAlex indexes linked2019preprint, so its count/status is not a separate proceedings-version clearance')
 source={'name':name,'citation_key':key,'candidate_id':'LA01-candidate-48' if name=='pharma' else None,'classification':'DIRECT_METHOD' if name!='pharma' else 'EMPIRICAL_EXAMPLE','version_date':date,'doi':doi,'local_copy':artifact(p),'inspected_anchors':anchors,'allowed_claims':allowed,'forbidden_claims':forbidden,'status_review':status,'metadata':metadata,'audit_inputs':[artifact(x) for x in sorted(RAW.glob(f'closure30_{name}_*')) if x.is_file()]}
 sources.append(source)
code=[]
for name in ['inferbert','deepcausality']:
 c=read(RAW/f'closure30_{name}_commits.json')[0];repo=read(RAW/f'closure30_{name}_repo.json')
 code.append({'citation_key':'closure30'+name+'code','repository':repo['html_url'],'commit':c['sha'],'commit_date':c['commit']['committer']['date'],'retrieval_date':now,'scope':'Static source inspection only;no downloaded code execution','tree_truncated':read(RAW/f'closure30_{name}_tree.json')['truncated'],'files':[artifact(x) for x in sorted(RAW.glob(f'closure30_{name}_code_*.txt'))],'anchors':['README:data/model prerequisites','causal_tree/compute_gap/compute_Z_score: membership partition,group means and variances','InferBERT lines193–195 filter unadjusted one-sidedp<=.05;DeepCausality notebook cell0 filter commented out','Tree licence names and upstream file notices inspected'],'rights_observation':'No repository-wide licence found in InferBERT;DeepCausality has Apache notice in BioBERT subtree,not explicit permission for project notebook. Static observations,not legal determination.','decision':'Use as disclosed diagnostic/hypothesis-ranking comparator;copying permission unresolved;decline direct use as identified intervention estimator.'})
save('text-source-support.json',{'created_utc':now,'cutoff':'2026-10-07','sources':sources,'software':code})
save('text-citation-metadata.json',{'created_utc':now,'sources':[{k:s[k] for k in ['name','version_date','metadata']} for s in sources]})

forward=[]
for name in ['inferbert','deepcausality','pharma','veitch']:
 seen={};queries=[]
 for label in ['top','recent']:
  p=RAW/f'closure30_{name}_citing_{label}.json';d=read(p);queries.append({'order':label,'count':d['meta']['count'],'maximum_returned':10,'source':artifact(p)})
  for w in d['results']:
   title=w['display_name'];lower=title.lower();classification='SURVEY_OR_TUTORIAL' if any(x in lower for x in ['survey','review']) else 'BACKGROUND';action='Record adjacent domain context;not used as technical support in this narrowly scoped comparison.'
   if any(x in lower for x in ['inferbert','deepcausality','bidirectional encoder representations']):classification='DIRECT_METHOD';action='Primary method inspected here.'
   if 'critical role of model selection' in lower:classification='SOURCE_BLOCKED';action='Direct2026follow-up identified. PublisherPDF route rejected by fixed allowlist;no original read,no claim of replication/correction or coverage closure.'
   if any(x in lower for x in ['causal inference in natural language','text and causal inference']):action='Broader survey comparator;existing local primary survey retained;not evidence for the root-method claims here.'
   if any(x in lower for x in ['wage disparities','words that matter','potential confounders','conformal counterfactual','causaterml','patenting disparities','machine learning in causal inference: application']):classification='DIRECT_METHOD';action='Relevant expansion lead;original not inspected in this treatment;no technical claims imported.'
   seen[w['id']]={'id':w['id'],'title':title,'doi':w.get('doi'),'date':w['publication_date'],'citations':w['cited_by_count'],'is_retracted':w['is_retracted'],'classification':classification,'action':action}
 forward.append({'seed':name,'queries':queries,'candidates':list(seen.values()),'limit':'Top10plus recent10,not exhaustive;index/version coverage and date quality limited. Pre-cutoff filter applied;counts retrieved after cutoff.'})
save('text-forward-snowball.json',{'created_utc':now,'cutoff':'2026-10-07','seeds':forward})

backward=[
 ('InferBERT,DeepCausality','Pearl2010;Tucci2013;Pearl and Mackenzie2018','FOUNDATIONAL','Do-calculus references considered. Root-group identity is established directly from inspected equations/code and project derivation;no theorem imported from unread cited edition.'),
 ('InferBERT','Veitch,Sridhar,Blei2020','DIRECT_METHOD','Authentic proceedingsPDF acquired and inspected;conditional constructive alternative included.'),
 ('InferBERT','Feder etal2020 CausaLM','COMPETITOR','Model explanation differs from real intervention estimation;candidate retained;no technical claim imported.'),
 ('InferBERT','Banda etal2016 curated adverse-event resource;Evans2001 PRR;vanPuijenbroek2002 disproportionality;Szarfman2002 screening','COMPETITOR','Public data and signal-detection alternatives considered. Not validated against the specific commercially curated source cohort.'),
 ('InferBERT,DeepCausality,2023assessment','Devlin BERT;Lan ALBERT;Liu RoBERTa;Lee BioBERT;Kim BERN;Huang ClinicalBERT;Beltagy SciBERT','IMPLEMENTATION_OR_SOFTWARE','Upstream component identities considered;source-specific environments inspected. No new architecture theorem or model-quality claim imported.'),
 ('DeepCausality','Chalasani2021 ACG guideline;Hoofnagle2013 LiverTox','BACKGROUND','Clinical relevance and labels are source-reported comparators;not independent causal truth for our banking example.'),
 ('2023assessment','InferBERT2021 andDeepCausality2022,refs17–18','DIRECT_METHOD','Both originals and pinned implementations inspected;methods paragraph references9–10 do not identify these papers.'),
 ('2023assessment','Kiciman etal2023;Kompa2022;Ball and DalPan2022;Cherkas2022;Agbabiaka2008;Rockey2010','SURVEY_OR_TUTORIAL','LLM/causality and clinical assessment leads retained;no medical intervention or bank-performance claim imported.'),
 ('Veitch','Egami2018;Roberts2018 text matching;Wood-Doughty2018 classifier challenges','COMPETITOR','Text measurement and adjustment alternatives considered;Egami authentic local text inspected for scope;not newly cited.'),
 ('Veitch','Rosenbaum andRubin1983;Kennedy2016;van derLaan andRose2011','FOUNDATIONAL','Adjustment/estimation foundations considered;our example proven by explicit finite enumeration,not new claim based on unread edition.'),
 ('Veitch','Johansson2016/2018/2019/2020;Shi2019;D Amour andFranks2019','COMPETITOR','Representation learning and weighting alternatives;outside the bounded source comparison;broader comparative coverage remains separate.'),
 ('Veitch','Kallus2018;Kuroki andPearl2014;Pearl2012;Miao2018','DIRECT_METHOD','Noisy/missing/proxy measurement routes are relevant future alternatives;do not treat one noisy narrative as identified baseline truth.'),
 ('Veitch','Kuroki andMiyakawa1999;Pearl2014 mediation;Veitch2019 network embeddings','DIRECT_METHOD','Alternative targets and dependence regimes;not substituted for the present populationATE.'),
]
save('text-backward-snowball.json',{'created_utc':now,'scope':'Relevant methodological references from introduction/method/comparison/reference sections;clinical examples and generic application illustrations not imported.','records':[dict(seed=s,candidates=c,classification=k,action=a) for s,c,k,a in backward]})
claims=[
 ('Group-score formula','PRIMARY_TECHNICAL_SUPPORT',['InferBERT equations2–4','DeepCausality Algorithm1 and membership paragraph','Pinned compute_gap implementations']),
 ('Perfect conditional prediction still gives observational group contrast','PROJECT_DERIVATION',['Iterated expectation in text-signals.tex,entity-gap and calibration-group']),
 ('Constructed relief effect−.05 versus group gap+.31 and rewrite+.246703','PROJECT_DERIVATION',['text-signal-attempt-1/result.json','run_text_signal_study_20261030.py exact enumeration and independent formulas']),
 ('Reported model scores are expert relevance/classification,not effect estimates','PRIMARY_TECHNICAL_SUPPORT',['2023assessment Tables1–4,Figure5 and metric definitions']),
 ('Constructive embedding route needs initial text sufficiency','PRIMARY_TECHNICAL_SUPPORT',['Veitch Section2,Theorems3.1–3.2 and limitations']),
 ('Copying rights and full reproduction unresolved','IMPLEMENTATION_EVIDENCE',['Pinned source trees,README files and scoped licence notices;static audit only']),
]
save('text-claim-support.json',{'created_utc':now,'claims':[dict(claim=c,support_class=k,anchors=a) for c,k,a in claims]})
risks=[
 {'gap':'Exact2023publisherHTMLnotice review','status':'limited','action':'Current full route givesPDF;Crossref/OpenAlex inspected. Do not claim exhaustive status clearance.'},
 {'gap':'Direct2026InferBERT comparison','status':'SOURCE_BLOCKED','action':'Fixed collector rejected publisher host;original not read. Preserve exact identity/route failure and avoid claims of exhaustive comparative completeness.'},
 {'gap':'Veitchproof appendix/version','status':'limited','action':'Theorem and premises inspected in proceedingsPDF;separate proof appendix not supplied by inspected landing. ATT display inconsistency recorded rather than silently repaired.'},
 {'gap':'Native model reproduction and data/rights','status':'future_prototype','action':'Clarify project-code permissions and cohort/weight access;then reproduce declared splits and multiplicity procedure. No model training in this campaign.'},
 {'gap':'Bank identification and validation','status':'future_evidence','action':'Define intervention and timing;validate sufficient baseline information or use assignment design. Prediction and clinical relevance do not establish bank effects.'},
 {'gap':'Forward-source breadth','status':'expansion','action':'Bounded index queries expose relevant additional candidates;do not claim comprehensive coverage of all domains.'}
]
save('text-omissions-risk.json',{'created_utc':now,'hostile_review':'Fairly retain positive extraction/relevance contributions;separate code inspection from native qualification;avoid alleging leakage or numerical falsity;bounded counterexample does not refute valid identification methods.','risks':risks})
print(json.dumps({'sources':len(sources),'software_revisions':len(code),'forward_candidates':sum(len(x['candidates']) for x in forward),'ledgers':6,'census_change':'Pending publication-bound completion;only candidate48 is a closure of the113-candidate census.'}))
