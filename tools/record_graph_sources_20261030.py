"""Authentic-source audit for graph uncertainty; no automatic survey acceptance."""
from pathlib import Path
import datetime,hashlib,json

R=Path(__file__).resolve().parents[1]
O=R/'docs/twelve-hour-closure/2026-10-29'
RAW=R/'docs/literature/raw'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(p):return json.loads(p.read_text())
def artifact(p):return {'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,d):
    p=O/n;assert not p.exists(),'Preserve audit '+n
    p.write_text(json.dumps(d,indent=2)+chr(10))
def meta(name,wid):
    raw=read(RAW/f'closure30_{name}_openalex.json')
    candidates=raw.get('results',[raw])
    d=next(x for x in candidates if x['id'].endswith(wid))
    return {'work_id':d['id'],'citation_count':d.get('cited_by_count','not available'),
            'is_retracted':d.get('is_retracted','not available'),'venue_rank':'not available',
            'accessed_utc':now,'limit':'Live index metadata after cutoff, not technical validity or historical citation count.'}

sources=[
 {'key':'closure30molero','candidate':'LA01-candidate-136','classification':'DIRECT_METHOD',
  'path':'Development and Implementation of an End-to-End Causal Inference Workflow Integrating Large Language and Causal Generative Models MoleroPerez(2026).pdf',
  'version_date':'Institutional thesis February2026;PDF created26February and modified5March2026',
  'url':'https://oa.upm.es/94628/','metadata':meta('upm','W7134150827'),
  'anchors':['PDF52:project repository','PDF55–64:baseline and retrieval methods',
             'PDF65–70:confidence,token probabilities,HallBayes equations14–19 and topology',
             'PDF71–82:datasets,PC chi-square comparator,400models,percentile intervals andIoU',
             'PDF85–91:reported accuracy,calibration limits and graph metrics',
             'PDF97–100:IoU tables,limitations and conclusions','PDF121–125:implementation descriptions',
             'PDF103–109:relevant reference identities'],
  'allowed':['Description of proposed workflow and reported comparison to fitted expert-graph models',
             'Source-specific discrepancy:complement of success upper cap called error upper bound',
             'Independent Bernoulli sampling and percentile definition,with stated source limits'],
  'forbidden':['General graph/effect calibration','Bank or medical intervention truth',
               'Independent numerical replication','Claim the study actually produced cyclic graphs',
               'General superiority over statistical discovery or order-informed flows'],
  'status':'Primary original inspected with explicit methodological limitations;no formal retraction notice observed in inspected institutional/index records.'},
 {'key':'closure30aitlhouss','candidate':'LA01-candidate-202','classification':'RETRACTED_OR_QUARANTINED',
  'path':'Large Language Models for Causal Inference AitLhouss(2025).pdf',
  'version_date':'19September2025,institutional thesis',
  'url':'https://ebuah.uah.es/dspace/bitstream/10017/66240/4/TFM_Ait_Lhouss_2025.pdf',
  'metadata':meta('uah','W7132031801'),
  'anchors':['Abstract;PDF42section4.1;PDF43Tables5/6:inconsistent10/80study counts',
             'PDF48–51Table9 andPDF72AppendixA:ten selected identities',
             'PDF55–60:productivity,accuracy andclaimed independent trials',
             'PDF72references3/5 versus authentic arXiv landings'],
  'allowed':['Source identity and precise exclusion rationale only'],
  'forbidden':['Survey completeness,accuracy,time savings,reproducibility andcausal method validity'],
  'status':'Quantitative andsurvey support quarantined;not an allegation of intent or formal retraction. See quarantine/uah-disposition.json.'},
 {'key':'closure30chlonone','candidate':None,'classification':'DIRECT_METHOD',
  'path':'Predictable Compression Failures Why Language Models Actually Hallucinate Chlon(2025).pdf',
  'version_date':'arXiv2509.11208v1,14September2025',
  'url':'https://arxiv.org/abs/2509.11208v1',
  'metadata':{'shared_work_id':'https://openalex.org/W4415088079','version_specific_count':'not available'},
  'anchors':['PDF5–6:Theorem5,operational planners andexample','AppendixA.4–A.5:KL proof andclipping',
             'Sections4–6:reported experiments andlimitations','Related work andbibliography'],
  'allowed':['KL convexity/data-processing inequality as necessary information requirement',
             'Historical planner design,distinguished from sufficient calibration guarantee'],
  'forbidden':['Minimum information requirement alone ensures achieved correctness',
               'Prompt masking provides valid true-event probability','Independent reproduction of reported model experiments'],
  'status':'Historical original retained;v3 changes title,authors andverification scope;no withdrawal notice found on inspected landing.'},
 {'key':'closure30chlonthree','candidate':None,'classification':'DIRECT_METHOD',
  'path':'Predictable Compression Failures Order Sensitivity and Information Budgeting for Evidence-Grounded Binary Adjudication Chlon(2026).pdf',
  'version_date':'arXiv2509.11208v3,5June2026',
  'url':'https://arxiv.org/abs/2509.11208v3',
  'metadata':{'shared_work_id':'https://openalex.org/W4415088079','version_specific_count':'not available'},
  'anchors':['Sections2/3:reference distribution andBernoulli predicate','PDF5–7:Theorem5,Algorithm1,Table1,Proposition3',
             'PDF9:verifier and audit limitations','PDF12:AppendixA.4–A.6 proof andclipping',
             'PDF10:references;AppendixB:methods andexamples'],
  'allowed':['Explicit verifier-relative deployment conditions and narrow empirical scope',
             'KL inequality and distinction between full/binary information'],
  'forbidden':['Universal causal-arrow calibration','Necessary full-distribution budget sufficient for target success',
               'Binary threshold identifies increasing versus decreasing probability branch without restriction'],
  'status':'Latest pre-cutoff version inspected. PDF has Chlon,Karim,Awada;landing metadata also lists MaggieChlon. Bibliography follows PDF;identity difference retained.'}
]
for s in sources:
    p=R/'docs/papers'/s.pop('path');assert p.read_bytes().startswith(b'%PDF')
    s['local_copy']=artifact(p)
    s['correction_review_limit']='Bounded original/landing/index checks,not exhaustive correction clearance.'

software=[]
for name,key in [('upm','closure30molerocode'),('hallbayes','closure30berry')]:
    c=read(RAW/f'closure30_{name}_commits.json')[0]
    repo=read(RAW/f'closure30_{name}_repo.json')
    software.append({'key':key,'repository':repo['html_url'],'commit':c['sha'],
      'commit_date':c['commit']['committer']['date'],'scope':'Static source inspection;no downloaded code executed',
      'tree_truncated':read(RAW/f'closure30_{name}_tree.json')['truncated'],
      'licence_observation':'MIT notice inspected;dependency,data,model andspecific-use review still separate.',
      'inspected_files':[artifact(p) for p in sorted(RAW.glob(f'closure30_{name}_*')) if p.is_file()],
      'decision':('Integrate selected suggestion/retrieval ideas,prefer maintained upstream. Public tree lacks reported HallBayes/flow experiment pipeline;no full native reproduction.' if name=='upm' else
                  'Potential CLI/MCP evidence-support comparator. Do not use score as causal-arrow probability;June2026Berry is not verified thesis-era dependency.')})
save('graph-source-support.json',{'created_utc':now,'cutoff':'2026-10-07','sources':sources,'software':software,
     'acquisition_receipts':[artifact(p) for p in sorted(RAW.glob('closure30_*')) if any(w in p.name for w in ['upm','uah','chlon','hallbayes']) and p.is_file()]})
save('graph-citation-metadata.json',{'created_utc':now,'sources':[{'key':s['key'],'version_date':s['version_date'],'metadata':s['metadata']} for s in sources],
     'chlon_work_metadata':artifact(RAW/'closure30_hallbayes_openalex_exact.json'),
     'limit':'No venue-rank field invented;version counts unavailable;index flags are not methodological clearance.'})

backward=[
 ('Molero','Chlon2025 information-bound paper;HallBayes repository','DIRECT_METHOD','Originalv1/v2/v3 recovered;v1/v3math inspected;historical/current code distinctions retained.'),
 ('Molero','Long2023 imperfect experts;Long2024 causal graphs;Ban2023/2025;SunLi2024','COMPETITOR','Relevant graph-guidance alternatives considered;existing retained monograph treatments remain,not newly certified here.'),
 ('Molero','KyriacouGreenlandMansournia2023 biomedical diagrams','BACKGROUND','Reference diagram source identified;no claim that expert model is intervention truth;original not used as independent technical support here.'),
 ('Molero','Javaloy2023 causal normalizing flows;Khemakhem2021 autoregressive flows;Almodovar2025DeCaFlow','DIRECT_METHOD','Relevant generative/deconfounding alternatives. No flow identification theorem imported;native/source-specific comparison remains future work.'),
 ('Molero','Mooij2016cause-effect pairs;Guo2017calibration;JinCLadder/Jincorrelation;CauSciBench','COMPETITOR','Benchmark andcalibration alternatives considered;our study uses known structural worlds,not reproduced benchmark/model claims.'),
 ('Molero','PyWhyLLM,pgmpy,DoWhy,Zuko,Joblib,Statsmodels','IMPLEMENTATION_OR_SOFTWARE','Pinned thesis front end inspected;delegated flow/runtime not qualified.'),
 ('Molero','Spirtes2000;Tsamardinos2006;DonnatHolmes2018','FOUNDATIONAL','Graph-method anddistance references considered;no numerical general-PC superiority imported.'),
 ('Molero','GaoRAGsurvey/modularRAG;LiuLostInMiddle;BerglundReversalCurse;HaldarHockenmaierRatingRoulette','BACKGROUND','Retrieval andmodel-evaluation limitations relevant;no new empirical claims taken from unread editions.'),
 ('Chlon','Chow1970;GeifmanElYaniv2017','FOUNDATIONAL','Selective classification alternatives considered. Elementary union probability argument proved here;no theorem imported from unread originals.'),
 ('Chlon','KalaiVempala2024;Farquhar2024semantic entropy;Xu2025self ensemble;Wang2023self consistency;Chang2024cancer staging','COMPETITOR','Alternative uncertainty signals;not equivalent to causal truth or bank calibration. Broader comparison remains separate.'),
 ('Chlon','Falck2024martingale;Bai2023;Xie2022;Zhang2024;Reuter2025','DIRECT_METHOD','In-context learning andorder sensitivity foundations;outside narrow effect-uncertainty theorem,not newly cited.'),
 ('Chlon','Grunwald2007;Deletang2024compression;Su2024RoFormer;Barbero2025;ChenYan2024;Xu2024RoPE','BACKGROUND','Compression andarchitecture context considered;our necessary-versus-sufficient examples do not require imported architecture claims.'),
 ('AitLhouss','AppendixA10selected studies','RETRACTED_OR_QUARANTINED','Two identifiers independently mismatch;full sample reconciliation andtrial reconstruction unavailable. Do not propagate this list as verified literature.'),
 ('AitLhouss','FederNLP;Kiciman2023;Liu2024/2025surveys;Ma2024;Wu2024','SURVEY_OR_TUTORIAL','Recognizable primary-survey leads considered through existing work;quarantined summary does not support their details.'),
 ('AitLhouss','PRISMA2020;PRISMA-S;Marshall2018/2019;OMaraEves2015;Tsafnat2014;vanDeSchoot2021ASReview','COMPETITOR','Review-method alternatives considered;no unsupported productivity numbers imported.'),
]
save('graph-backward-snowball.json',{'created_utc':now,'scope':'Relevant method/comparator references inspected in original introductions,methods,comparison andbibliographies;generic model histories andclinical illustrations are not imported.',
     'records':[dict(seed=s,candidates=c,classification=k,action=a) for s,c,k,a in backward]})
forward=[]
for name in ['upm','uah','chlon']:
    seen={};queries=[]
    for label in ['top','recent']:
        p=RAW/f'closure30_{name}_citing_{label}.json';d=read(p)
        queries.append({'ordering':label,'reported_count':d['meta']['count'],'maximum_results':10,'artifact':artifact(p)})
        for x in d['results']:
            seen[x['id']]={'id':x['id'],'title':x['display_name'],'date':x['publication_date'],
                'doi':x.get('doi'),'cited_by_count':x['cited_by_count'],'is_retracted':x.get('is_retracted'),
                'classification':'BACKGROUND','action':'Relevant epistemic-diagnostic follow-up recorded;original not inspected,no technical claim imported.'}
    forward.append({'seed':name,'queries':queries,'candidates':list(seen.values()),
                    'limit':'Top10andlatest10,pre-cutoff filter. Zero index results does not establish no citing literature.'})
save('graph-forward-snowball.json',{'created_utc':now,'cutoff':'2026-10-07','seeds':forward})
claims=[
 ('Thesis probability andinterval definitions','PRIMARY_TECHNICAL_SUPPORT','Molero equations14–19,23–24;PDF67and69visually checked'),
 ('Complement of success cap iserror lower bound','PROJECT_DERIVATION','graph-confidence.tex error-floor;independently checked Bernoulli-KL root'),
 ('Full KL budget isnot sufficient for event probability','PROJECT_DERIVATION','Four-point construction,exact formula andnumeric check'),
 ('Binary branch ambiguity','PROJECT_DERIVATION','Bernoulli-KL symmetry atq=.5;no general calibration inference'),
 ('Discarding cycles changes marginals','PROJECT_DERIVATION','Eight exact rational graph states;36/61conditional marginals'),
 ('Model interval agreement can coexist withwrong causal coverage','PROJECT_DERIVATION','TwoGaussianSCMs,equalcovariance;2000retainedsamples;QR checks'),
 ('Graph-class union coverage','PROJECT_DERIVATION','Explicit graph/effect error events andunion bound;assumptions stated'),
 ('Illustrative financial decision reversal','PROJECT_DERIVATION','economic-check.json exact40000versus-20000;scenario inputs'),
 ('Thesis public code supports onlypartial reproduction','IMPLEMENTATION_EVIDENCE','Pinned tree,README,selectednotebooks,augmentationfunctions andMITnotice'),
 ('Alcala source excluded for quantitative support','QUARANTINED','Exactstudy-count discrepancy,twoarXividentitymismatches,repository404receipts'),
]
save('graph-claim-support.json',{'created_utc':now,'claims':[dict(claim=c,support_class=k,anchors=a) for c,k,a in claims],
     'study_artifacts':[artifact(O/'graph-confidence-attempt-1/result.json'),artifact(O/'graph-confidence-attempt-1/replications.csv'),artifact(O/'graph-confidence-attempt-1/economic-check.json')]})
save('graph-omissions-risk.json',{'created_utc':now,'review':'Retain positiveworkflowcontribution andsourcesownlimitations. Distinguish thesis fromcitedpaper versions;neverclaim fabricatedexperiments orobservedcycles. Scientificcounterexamples do notdeny usefulevidence assistance.',
     'risks':[
      {'gap':'Complete thesis experiment code','status':'unavailable_in_inspected_tree','action':'Obtain authentic graph/flow implementation anddata transformations before numerical replication.'},
      {'gap':'HallBayesDecember2025revision','status':'unresolved','action':'Currentdefaultbranchhistoricalqueryempty;later tag andJuneBerry do not replace exactdependency.'},
      {'gap':'General source-correction clearance','status':'limited','action':'Primarylanding/indexchecks bounded;v3PDFauthorlist differsmetadata;do notclaim formalclearance.'},
      {'gap':'Joint graph/effect calibration','status':'open_research','action':'Establish declared graph retention andselection-compatible estimation;thetwographsimulation proves no general rule.'},
      {'gap':'Clinical orbank intervention truth','status':'future_evidence','action':'Use known synthetic/public assignment designs before costly bankexperiment;expert-fit agreement isnottruth.'},
      {'gap':'Alcala inconsistencies','status':'quarantined','action':'Require authentic correction,study inventory andunderlying trialrecords beforeusing reported results.'},
      {'gap':'Forward literature breadth','status':'limited','action':'Boundedindexsearch retained;theone new diagnostic follow-up not read,not citedastechnicalsupport.'}]})
print(json.dumps({'sources':len(sources),'software_revisions':len(software),'forward_candidates':sum(len(x['candidates']) for x in forward),'ledgers':6,'census':'Pending publication-bound review;one admitted thesis andone quarantined disposition,not two admitted studies.'}))
