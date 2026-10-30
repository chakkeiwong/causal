"""Primary-source audit for random recovery of incomplete servicing histories."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'docs/twelve-hour-closure/2026-10-29'
def save(name,x):(O/name).write_text(json.dumps(x,indent=2)+chr(10))
def ident(path):
 p=R/path
 return dict(path=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
sources=[dict(id='levis2023double',title='Double sampling for informatively missing data in electronic health record-based comparative effectiveness research',
 authors=['Alexander W. Levis','Rajarshi Mukherjee','Rui Wang','Heidi Fischer','Sebastien Haneuse'],
 version='arXiv:2204.02432v2,10 July2023; technical support refers to this inspected preprint',
 published_identity='Statistics in Medicine,online5 December2024,DOI10.1002/sim.10298; published text not substituted for inspected version',
 artifact=ident('docs/papers/Double sampling for informatively missing data in electronic health record-based comparative effectiveness research Levis(2023).pdf'),
 classification='DIRECT_METHOD',status='retained with limits',
 inspected=['PDF7–8,Sections3.1–3.3:successful completion,Assumptions2–3,Proposition1 and proof',
 'PDF9–12,Section3.4:Theorems1–2,independent nuisance training,product bias and rate conditions',
 'PDF22–23,Discussion:informative second-stage nonresponse,recall error,cost and unresolved design questions',
 'PDF29–34,AppendixA.1–A.2:general coarsening,Assumptions4–5,Propositions2–3 and proof construction'],
 allowed=['Successful noninformative second-stage recovery can identify the full data law despite informative original missingness.',
 'Published research includes efficient augmented mean estimators and a general coarsening transformation under stated assumptions.',
 'Random invitation is insufficient when completed recovery remains outcome-selective.'],
 forbidden=['Our sequential score is semiparametrically efficient by citation alone.','Bank histories can in fact be recovered truthfully.','A random invitation guarantees the design assumptions.']),
 dict(id='sun2025double',title='Estimating weighted quantile treatment effects with missing outcome data by double sampling',
 authors=['Shuo Sun','Sebastien Haneuse','Alexander W. Levis','Catherine Lee','David E. Arterburn','Heidi Fischer','Susan Shortreed','Rajarshi Mukherjee'],
 version='arXiv:2310.09239v3,14 March2025; technical support refers to this inspected preprint',
 published_identity='Biometrics,2 April2025,DOI10.1093/biomtc/ujaf038',
 artifact=ident('docs/papers/Estimating weighted quantile treatment effects with missing outcome data by double sampling Sun(2025).pdf'),
 classification='DIRECT_METHOD',status='retained with version warning',
 inspected=['PDF6–8,Sections3.1–3.2:observed data,noninformative successful recovery,positivity,regularity and correct nuisance specification',
 'PDF8–11,Sections3.3–3.4:equations4–7 and Theorem1;IPW quantile estimating equations and pointwise asymptotic inference',
 'PDF12–13,Sections3.5–3.6:uniform quantile results,bootstrap conditions',
 'PDF19–21,Discussion:quantile vs mean targets,original MNAR and second-stage assumptions'],
 allowed=['The same two-phase principle has a quantile-treatment-effect formulation with target-specific conditions.',
 'A quantile effect is not obtained by averaging conditional quantile effects.'],
 forbidden=['A mean-reward experiment qualifies tail-risk or quantile effects.','The stale Biometrics64 December2008 template header identifies this source.'],
 version_warning='Authentic preprint contains a stale journal-template header and unrelated template DOI. Identity uses arXiv version/title/authors and separate publisher metadata. Published-PMC PDF route failed and remains recorded.'),
 dict(id='jiang2016',title='Doubly Robust Off-policy Value Evaluation for Reinforcement Learning',authors=['Nan Jiang','Lihong Li'],
 version='ICML2016 proceedings,PMLR48',artifact=ident('docs/papers/Doubly Robust Off-policy Value Evaluation for Reinforcement Learning Jiang(2016).pdf'),
 classification='FOUNDATIONAL',status='retained with limits',
 inspected=['PDF2–4,Sections3–4.3:finite-horizon setting,independent nuisance training,equation10,Theorem1 and variance decomposition',
 'PDF8,AppendixA:recursive proof of unbiasedness and variance'],
 allowed=['A separately fitted sequential outcome model can reduce action-weighting variance while known importance ratios preserve unbiasedness.',
 'Zero outcome regression reduces the construction to step-wise importance sampling.'],
 forbidden=['Normal intervals have exact finite-sample coverage.','Correct outcome regression removes all transition or reward noise.','The paper alone proves our additional missing-history recovery design.'])]
save('outcome-source-support.json',dict(cutoff='2026-10-07',sources=sources,scope='Focused support for a new servicing derivation; not expansion of the original113-candidate language-model census'))
metadata=[]
for label,work,raw in [('levis','W4405041730','closure30_levis_openalex.json'),('sun','W4409233979','closure30_quantile_missing_openalex.json')]:
 data=json.loads((R/'docs/literature/raw'/raw).read_text());w=next(x for x in data['results'] if x['id'].endswith(work))
 crpath='docs/literature/raw/closure30_'+label+'_crossref.json';cr=json.loads((R/crpath).read_text())['message']
 metadata.append(dict(source=label,access_date='2026-10-30 Asia/Shanghai',openalex=ident('docs/literature/raw/'+raw),
   cited_by_count=w.get('cited_by_count'),is_retracted=w.get('is_retracted'),venue=(w.get('primary_location')or{}).get('source',{}).get('display_name'),
   venue_ranking='not independently audited; not used as correctness evidence',crossref=ident(crpath),
   update_to=cr.get('update-to'),updated_by=cr.get('updated-by'),relation=cr.get('relation'),
   limit='No update/retraction flag found in these records. This is not an exhaustive absence certificate;metadata retrieved after cutoff,works filtered by publication date.'))
metadata.append(dict(source='jiang2016',access_date='2026-10-30 Asia/Shanghai',citation_count='not refreshed',venue='ICML2016,PMLR48',retraction_check='Inherited original source record plus inspected original;no new exhaustive correction search',venue_ranking='not used'))
save('outcome-citation-metadata.json',metadata)
back=[('Frangakis and Rubin2001','Addressing an idiosyncrasy in estimating survival curves using double sampling in the presence of self-selected right censoring','FOUNDATIONAL','Historical antecedent;candidate only,no theorem imported;Levis supplies inspected direct proof.'),
 ('Robins,Rotnitzky and Zhao1994','Estimation of regression coefficients when some regressors are not always observed','FOUNDATIONAL','General missing-data influence-function antecedent;candidate only;Levis AppendixA proof inspected.'),
 ('An etal2009','Double-sampling with missing longitudinal follow-up','DIRECT_METHOD','Candidate longitudinal antecedent;not cited as support until exact original obtained.'),
 ('Coppock etal2017','Combining double sampling and bounds to address nonignorable missing outcomes in randomized experiments','COMPETITOR','Important partial-identification alternative when second-stage recovery fails;inspect next before making numerical bounds claims.'),
 ('Qian,Frangakis and Yiannoutsos2020','Deductive semiparametric estimation in double-sampling designs','DIRECT_METHOD','Candidate efficient-method alternative;not claimed to be implemented.'),
 ('Haneuse etal2016;Koffman etal2021','Patient follow-up and bariatric outcome missingness studies','EMPIRICAL_EXAMPLE','Applications motivate recovery and recall concerns;not bank evidence or our quantitative input.'),
 ('Rothenhaeusler2020','Adaptive model selection for missingness assumptions','COMPETITOR','Levis compares adaptive MAR/non-MAR estimators;our fixed design does not choose a missingness assumption from evaluation outcomes.'),
 ('Jiang and Li2016','Doubly robust off-policy value evaluation','FOUNDATIONAL','Original inspected;cite equation10/Theorem1;derive recovery composition directly.'),
 ('Levis etal2023;Sun etal2025','Mean and quantile effects under double sampling','DIRECT_METHOD','Both genuine originals inspected and cited;different targets distinguished.')]
save('outcome-backward-snowball.json',[dict(candidate=a,title=b,classification=c,disposition=d) for a,b,c,d in back])
forward=[]
for label in ['levis','sun']:
 for sort in ['cited','recent']:
  path='docs/literature/raw/closure30_'+label+'_'+sort+'.json';d=json.loads((R/path).read_text())
  forward.append(dict(seed=label,order=sort,query_artifact=ident(path),cutoff='2026-10-07',access_date='2026-10-30 Asia/Shanghai',count=d['meta']['count'],
    results=[dict(title=w['title'],date=w['publication_date'],doi=w.get('doi'),citations=w['cited_by_count'],
      disposition='Inspected original in this study' if 'quantile treatment' in w['title'] else 'Peripheral mortality-prediction application;not scientific support for this causal design') for w in d['results']],
    limit='Bounded OpenAlex coverage;absence of indexed citations is not absence of follow-up work.'))
save('outcome-forward-snowball.json',forward)
claims=[('Recovery estimator','PROJECT_DERIVATION','outcome-audit.tex,conditional expectation and variance derivation;runner mask and enumeration checks'),
 ('Sequential augmentation','PRIMARY_TECHNICAL_SUPPORT and PROJECT_DERIVATION','Jiang2016 equation10/Theorem1;explicit telescoping derivation in our notation and independently trained model'),
 ('Two-phase identification','PRIMARY_TECHNICAL_SUPPORT','Levis2023 Proposition1,AppendixA Propositions2–3;Sun2025 equations4–7 for quantile distinction'),
 ('Finite-sample findings','IMPLEMENTATION_EVIDENCE','Frozen500-replication scenario files and independent raw-CSV reconstruction;conditional generated evidence only'),
 ('Cost and allocation','PROJECT_DERIVATION','Conditional variance and constrained expected-cost differentiation;unpriced design implications,not ROI or optimal bank design')]
save('outcome-claim-support.json',[dict(claim=a,support_class=b,anchor=c)for a,b,c in claims])
save('outcome-omissions-risk.json',dict(omissions=[
 dict(source='Schomaker etal2013,Non-ignorable loss to follow-up',status='SOURCE_BLOCKED',reason='Authentic PMC text saved;exact PDF endpoint returned non-PDF. Not cited as technical support under local PDF rule.',next='Acquire genuine institutional accepted manuscript;do not relabel an HTML printout as original PDF.'),
 dict(source='Coppock etal2017',status='candidate,not yet inspected',reason='Useful bounds alternative for incomplete second-stage recovery;no numeric bounds imported.',next='Retrieve original and compare assumptions.'),
 dict(source='Published Levis and Sun versions',status='version-limited',reason='Primary claims audited against authentic specified preprints;publisher metadata establishes publication identity only.',next='Compare published versions when accessible.')],
 reviewer_risks=['Our augmentation is not proved semiparametrically efficient for the combined sequential/coarsened model.',
 'IID customer simulation does not qualify calendar dependence,estimated treatment propensities or selected policy inference.',
 'Recovery needs whole missing histories and accurate measurement;terminal balances alone may not suffice.',
 'Pilot cost is additional and observed-historical records are not free by declaration.',
 'No finite-grid minimum-coverage qualification is claimed from nominal-compatible Monte Carlo estimates.']))
print(json.dumps(dict(sources=len(sources),ledgers=6,original_census_changed=False)))
