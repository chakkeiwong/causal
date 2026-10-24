#!/usr/bin/env python3
"""Review dated author original and pinned clinical graph sources; no native execution."""
from collections import Counter
from copy import deepcopy
import hashlib,json
from pathlib import Path
import ecmo_graph_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-24/census-ecmo-v1'
PRIOR=BASE.parent/'census-judge-bias-v1/census-register.json'
PAPER=ROOT/'docs/papers/LLM-Guided Causal Bayesian Network Construction for Pediatric Patients on ECMO Mathur(2025).pdf'
read=lambda p:json.loads(p.read_text())
LIMITS=['Five-page author original; final publisher six-page layout not acquired and byte equivalence not claimed.',
 'Single-center71patient retrospective study and expert reference graph;not independent causal truth or bank validation.',
 'No clinical data,downloaded source,model call or native benchmark executed.',
 'Supplementary PDF and archived result contents not inspected; no claim that every prompt,version or runtime result is qualified.',
 'Visual,independent and final acceptance remain open.']
SPECS={
 0:[(1,37,'AIME2025 identity,supplement scope,patient data omitted and runtime instructions')],
 1:[(1,20,'GPLv3 text in root license; no full installed-distribution clearance')],
 2:[(1,175,'Pinned declared environment inventory; no installation or complete compatibility evidence')],
 3:[(14,16,'Ten-bootstrap configuration and explicit filename-parser limit'),(37,53,'Expert-reference SHD,SID,directed spurious edges and zero-initialized arrays'),(71,103,'Selected score variant,one-character sample parsing and slot assignment'),(109,128,'Mean and population-standard-deviation aggregation without a seen-file completeness test')],
 4:[(24,72,'Initial forbidden-edge filtering,deletion-only BIC and structured-score routes')],
 5:[(20,57,'Full refinement loads selected structured variant and parses one-character sample identity')],
 6:[(84,145,'Deletion-only excludes additions and flips; full search checks acyclicity and forbidden edges'),(300,326,'Greedy maximum score increment and stopping threshold')],
 7:[(45,71,'Subtractive flag passed to local hill-climbing implementation'),(165,230,'Structured score compares tabular BIC and fitted tree scores on supplied data; no held-out validation claim')],
 8:[(1,14,'Ten row-bootstrap samples with seeds0to9; private source CSV required')],
 9:[(1,8,'Explicit forbidden directions from NI to early risk factors')]
}

def main():
 assert not (BASE/'review.json').exists()
 data=PAPER.read_bytes();assert data.startswith(b'%PDF-') and data==(RAW/'exec24_ecmo_original.pdf').read_bytes()
 receipt=read(RAW/'exec24_ecmo_original.receipt.json');digest=hashlib.sha256(data).hexdigest();assert digest==receipt['sha256']
 tree=read(RAW/'exec24_ecmo_tree.json');assert not tree['truncated'];blob=next(x for x in tree['tree'] if x['path']=='assets/pdfs/LLM_guided_CBNs.pdf')
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==blob['sha']
 history=read(RAW/'exec24_ecmo_history.json')[0];assert history['sha']=='f1ca8f8f24dd371e861e7fd04230dfcb7c8929d5';assert history['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 pages=(BASE/'original.txt').read_text().split(chr(12));assert len(pages)==6 and not pages[-1].strip()
 write(BASE/'original-identity-review.json',dict(status='pass_for_author_original_identity',paper=ref(PAPER,'Genuine five-page author PDF'),acquisition=ref(RAW/'exec24_ecmo_original.receipt.json','Bounded original acquisition'),metadata=ref(RAW/'exec24_ecmo_crossref.json','Matching title,authors and2025DOI;metadata only'),historical_tree=ref(RAW/'exec24_ecmo_tree.json','Pre-cutoff exact blob'),history=ref(RAW/'exec24_ecmo_history.json','Author repository commit13November2025'),version='Author original in dated repository;publisher final not acquired',pages=5,sha256=digest,publisher_equivalence=False))
 anchors=[dict(pages=[1,2],finding='Hybrid diagram construction from approximate LLM knowledge,expert constraints and sparse data;score search alone cannot distinguish causal from associational relations'),dict(pages=[3,3],finding='71patients,eightBoolean variables,first24hour summaries,four named LLM families,expert reference andthree structural metrics'),dict(pages=[4,4],finding='Ten-bootstrap Table1;full refinement worsens allthree reported union-graph mean scores versus deletion;single-center,causal-sufficiency and temporal limits'),dict(pages=[5,5],finding='Table2 includes LLaMA SHD5to6.1afterdeletion and8.1afterfull refinement;not uniform improvement')]
 original=dict(integrated_citation_key='exec24_ecmo_original',kind='paper',title='LLM-Guided Causal Bayesian Network Construction for Pediatric Patients on ECMO',filename_title='LLM-Guided Causal Bayesian Network Construction for Pediatric Patients on ECMO',first_author='Mathur',author='Mathur, Saurabh and Singh, Ranveer and Skinner, Michael and Sanford, Ethan and Shah, Neel and Reeder, Phillip and Raman, Lakshmi and Natarajan, Sriraam',year=2025,source_identity=receipt['url'],version_date='2025AIME work;five-page author original pinned13November2025;not final six-page publisher layout',local_path=str(PAPER.relative_to(ROOT)),sha256=digest,local_copy=ref(PAPER,'Authentic original'),identity_evidence=[ref(BASE/'original-identity-review.json','Identity andversion limits')],inspected_anchors=anchors,supported_claims=[x['finding'] for x in anchors],limitations=LIMITS)
 records=[]
 for row in read(BASE/'source-index.json'):
  p=ROOT/row['raw_path'];data=p.read_bytes();r=read(p.with_suffix('.receipt.json'));assert core_sha(p)==r['sha256'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['blob_sha']
  ls=data.decode().splitlines();i=int(row['key'].rsplit('_',1)[1]);spans=[]
  for lo,hi,f in SPECS[i]:
   assert 1<=lo<=hi<=len(ls),(i,lo,hi,len(ls));spans.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256(chr(10).join(ls[lo-1:hi]).encode()).hexdigest()))
  records.append(dict(source_identity=row['url'],version_date='17August2025commit97d5b25d965e598bb04ab8fe674bc9d834455a23',upstream_path=row['path'],local_copy=ref(p,'Pinned original'),receipt=ref(p.with_suffix('.receipt.json'),'Acquisition'),git_blob_sha1=row['blob_sha'],inspected_anchors=spans,supported_claims=[x['finding'] for x in spans],executed=False))
 write(BASE/'authenticated-source-review.json',dict(records=records,acquired=10,inspected=10,native_execution=False))
 code=dict(integrated_citation_key='exec24_ecmo_code',kind='software_source',title='LLM-guided-CBNs pinned refinement andevaluation implementation',author='Saurabh Mathur and collaborators',year=2025,source_identity='https://github.com/saurabhmathur96/LLM-guided-CBNs/tree/97d5b25d965e598bb04ab8fe674bc9d834455a23',version_date='17August2025commit97d5b25d965e598bb04ab8fe674bc9d834455a23',local_copy=ref(BASE/'authenticated-source-review.json','Ten authenticated sources'),technical_sources=records,inspected_anchors=[x for r in records for x in r['inspected_anchors']],supported_claims=[x for r in records for x in r['supported_claims']],limitations=LIMITS+['Selected rootGPLv3 text andrequirements do not establish complete distribution rights.'])
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored rational arithmetic'),ref(BASE/'exact-results.json','Exact results')],findings=['Reported union mean changes1.8SE,1.2SHD,1.1SID afterfull versus deletion.','LLaMA deletion raises reportedSHDby1.1.','Conditional six8-score files outoften slots yield4.8withzero placeholders versus8observed-only;no missing files observed.','Single-character parser cannot distinguish sample1from10;outside stated ten-sample profile.','Opposite within24hour temporal orders have identical Boolean summaries.','Illustrative1800USD/100requests=18 versus/60usable=30;not observed costs.'],native_execution=False))
 reference=dict(integrated_citation_key='exec24_ecmo_reference',kind='project_evidence_not_scholarly_paper',title='Authored clinical-diagram evidence,clock,denominator and cost witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026',local_copy=ref(BASE/'mathematical-review.json','Exact authored review'),inspected_anchors=[ref(BASE/'exact-results.json','Arithmetic witnesses')],supported_claims=read(BASE/'mathematical-review.json')['findings'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[original,code,reference],cutoff='2026-10-07',new_scholarly_pdfs=1,native_execution=False))
 prior=read(PRIOR);census=deepcopy(prior);row=next(x for x in census['items'] if x['id']=='LA01-candidate-214');assert row['disposition']=='open_original_not_inspected'
 row.update(disposition='inspected_primary_retained_with_limits',original=ref(PAPER,'Authentic author original'),source_review=ref(BASE/'source-audit.json','Primary argument,adverse result andcode inspection'),next_action='Integrate reviewed author original andcode limits;final publisher bytes,supplementary prompt/version review andpublic native reproduction remain separate. Do not infer causal truth from expert agreement.')
 counts=Counter(x['disposition'] for x in census['items']);assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
 census.update(counts=dict(counts),supersedes=ref(PRIOR,'Preserved81/32predecessor'),changes=['Only candidate214 changes to inspected with explicit author-version,expert-reference,time-aggregation andnative-reproduction limits.'],evidence=prior.get('evidence',[])+[ref(BASE/'source-audit.json','Selected original andsource review')])
 assert all(x==y for x,y in zip(prior['items'],census['items']) if x['id']!='LA01-candidate-214')
 write(BASE/'census-register.json',census)
 write(BASE/'omissions-register.json',dict(remaining=['Final six-page Springer original not acquired;five-page author original is explicitly named.','Supplementary PDF,prompt provenance,exact hosted model versions and archived result contents not inspected.','Patient dataset is not included according to repository README;no private data requested.','Native FCI endpoint conversion,metrics dependencies,complete files,scientific truth andmonetary utility need independent public fixtures.'],next_action='Retain known graph-generating public fixtures and expert-held-out protocol as prototype route;do not make private clinical data a global proposal blocker.'))
 write(BASE/'review.json',dict(status='pass_for_bounded_original_and_code_review',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed unit') for n in ['original-identity-review.json','authenticated-source-review.json','source-audit.json','mathematical-review.json','census-register.json','omissions-register.json']]+[ref(Path(__file__),'Review logic')],findings=['Genuine author original authenticated against dated Git blob andmatching bibliographic metadata.','Adverse reported comparisons,expert-reference limits andtime aggregation retained.','Ten exact source files inspected;conditional denominator andparser witnesses do not assert observed archive failures.','82inspected,31unread andfourcrosscutting;only candidate214changed.'],limitations=LIMITS))
 print(json.dumps(dict(original_pages=5,source_files=10,census_inspected=82,census_unread=31,records=3)))

def core_sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

if __name__=='__main__':main()
