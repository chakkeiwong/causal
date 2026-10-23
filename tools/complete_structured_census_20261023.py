#!/usr/bin/env python3
"""Conserve the census while recording two bounded primary-text reviews."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import structured_causal_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-23/census-geometric-hierarchical-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-23/census-context-conflict-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
LIMITS=['Primary PDF text and selected proof/table anchors only; figures have not received a fresh visual review.',
 'No downloaded code, native package, runtime, empirical calibration or bank result has been reproduced.',
 'Primary author-reported results are distinguished from exact project arithmetic and supplied counterexamples.',
 'Referenced foundational works, software repositories and public data require their own originals before new technical claims rely on them.',
 'These papers do not establish LLM-assisted discovery success or solve the proposal unrestricted dependence and uncertainty gaps.']
SPECS=[dict(id='LA01-candidate-171',short='geometric-v2',raw='exec23_census_geometric_v2',identity='exec23_census_geometric_identity',
 key='exec23_geometric_models',title='Geometric Causal Models',authors='Eli N. Weinstein and David M. Blei',surname='Weinstein',
 filename='Geometric Causal Models Weinstein(2026).pdf',version='arXiv:2607.05153v2',archive='2026-07-11',printed='2026-07-14',
 anchors={1:'Title, authors, selected v2 identity and printed date; geometric framework and semisynthetic illustration.',
 6:'Assumption 1 restricts the initial analysis to index transformations; group actions are substantive model restrictions.',
 7:'Equivariant mechanisms and independent exogenous noise generate structured endogenous dependence.',
 8:'Definition 5 specifies DAG, symmetry group, noise and mechanisms; hard intervention replaces a mechanism.',
 11:'Graph and symmetry group are assumed known; observation, identification and finite-data estimation are distinct.',
 16:'Array experiment reports poor absolute uncertainty calibration despite relative improvement; mean-field approximation is suggested as a cause.',
 18:'Assumption 2 uses countably infinite mixing actions; Propositions 3 and 4 separate soundness from index-transform completeness.',
 19:'Orthogonal-group IV identification invokes linear-Gaussian structure, relevance and finite interference; finite interference supports local positivity.',
 20:'Assumption 4 specifies amenability, tempered sequences and locality; Proposition 7 also requires finite state spaces and positivity. Two text extractions preserve an apparent subgroup-intersection typo.',
 24:'Table 1 reports semisynthetic MSEs for five estimators in two scenarios; twenty repetitions and misspecified outcome models.',
 25:'Propensity correction and extra symmetry do not dominate in all examples; large-scale genomic extension and autocorrelation remain open.',
 26:'Limits include infinite domains, finite interference, ergodicity and known graph/symmetry; model discovery is future work.',
 35:'Appendix B.1/B.2 invokes invariant noise and a zero-one theorem; this review does not independently audit all cited proof dependencies.',
 36:'Appendix B.3/B.4 uses the Markov decomposition and embeds the unrestricted conventional-model class for index-transform completeness.',
 37:'Appendix B.5 derives linear mechanisms under orthogonal equivariance and finite interference.',
 38:'IV covariance ratio only requires a nonzero denominator; the extracted concluding positivity sentence is too strong for a negative first stage.',
 39:'Consistency proof uses finite relevant coordinates, positivity and continuous mapping; figure values are not newly visually accepted.'},
 claims=['Known graph and symmetry restrictions enable scoped identification and consistency; symmetry is not a generally learned causal structure.',
 'The stated consistency result requires mixing, locality, amenability, finite states and positivity; it does not establish arbitrary bank dependence or general interval calibration.',
 'The array example explicitly acknowledges poor absolute uncertainty calibration.',
 'Semisynthetic genomic Table 1 shows no uniform dominance of propensity correction or reverse-complement equivariance.',
 'Two extracted proof passages need qualification: finite subgroup translation has intersection size equal to the subgroup, and relevance implies nonzero rather than positive covariance.']),
 dict(id='LA01-candidate-260',short='hierarchical',raw='exec23_census_hierarchical_v1',identity='exec23_census_hierarchical_identity',
 key='exec23_hierarchical_pipeline',title='Scalable and Versatile Identification for Hierarchical Structural Causal Models: A New Look at Project STAR',
 authors='Janis Aiad, Aghiles Drali, Aymen El Ouadrhiri, Anass Ettahiri, Yasser Oufqir, Simon Patry, David Cortes, Marianne Clausel and Emilie Devijver',surname='Aiad',
 filename='Scalable and Versatile Identification for Hierarchical Structural Causal Models A New Look at Project STAR Aiad(2026).pdf',
 version='arXiv:2608.24500v1',archive='2026-08-25',printed='2026-08-26',
 anchors={1:'Title, authors, v1 identity; hierarchy-to-identification-to-estimation pipeline.',
 2:'The paper describes graph transformations, pyAgrum identification, adapted AST and local models; repository is a lead, not inspected software evidence.',
 3:'Unit and subunit variables and conditional mechanisms are distinct; unit contexts are drawn independently in the illustrated model.',
 4:'Equation 1 intervenes on a unit-level treatment distribution; collapse, augmentation and marginalization precede identification.',
 5:'Symbolic identification sees the transformed graph, not the nested table; numerical fitting is a separate stage.',
 6:'AST nodes encode products, marginalization and density keys; per-unit response averaging differs from pooled row weighting.',
 7:'The paper explicitly states factor normalization changes the numerical functional; positivity and missing fitted factors can cause instability.',
 8:'Ideal parallel cost is an author model with assumptions; hardware-specific CUDA throughput is not an independently measured result here.',
 9:'STAR preprocessing reports 5745 records in 322 classes and 79 schools, then 10 sampled students per class; interventions and targets are explicit.',
 10:'Table 3 distinguishes OLS treatment coefficients, IV class-size coefficient and random-intercept regression.',
 11:'ExactBIC is a selected plausible graph, with a substantive orientation and added latent class context, not a uniquely recovered graph.',
 12:'Table 5 uses different outcomes for mathematics and normalized reading diagnostic; reported differences and CPU ratio are checked as arithmetic only.',
 13:'322 classes and ten students per class limit multi-parent factors; wording distinguishes nominal graph from stabilized functional.',
 14:'The conclusion leaves deeper hierarchies, multi-parent estimation, stabilized-functional uncertainty and graph-family analysis open.'},
 claims=['A distributional unit intervention and a row-level coefficient need not be the same estimand.',
 'Symbolic identification and AST evaluation are separately auditable layers; fitted or normalized factors affect the evaluated functional.',
 'The STAR graph is selected and substantively modified; the paper does not establish unique graph recovery.',
 'Mathematics and reading rows in Table 5 are not a matched before/after normalization comparison.',
 'Two-level implementation, factor uncertainty and graph-family analysis remain limitations; no bank or native qualification follows.'])]

def main():
 assert not (BASE/'source-audit.json').exists(), 'Preserve bound artifacts.'
 sources=[]
 for s in SPECS:
  pdf=RAW/(s['raw']+'.pdf');receipt=read(RAW/(s['raw']+'.receipt.json'))
  digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
  assert receipt['status']=='saved' and receipt['sha256']==digest and pdf.read_bytes().startswith(b'%PDF-')
  xml=RAW/(s['identity']+'.xml');xr=read(RAW/(s['identity']+'.receipt.json'))
  assert xr['status']=='saved' and xr['sha256']==hashlib.sha256(xml.read_bytes()).hexdigest()
  ns={'a':'http://www.w3.org/2005/Atom'};entry=ET.fromstring(xml.read_text()).find('a:entry',ns)
  assert ' '.join(entry.findtext('a:title',namespaces=ns).split())==s['title']
  assert entry.findtext('a:updated',namespaces=ns)<'2026-10-07T16:00:00Z'
  text=(BASE/(s['short']+'.txt')).read_text();pages=text.split(chr(12))
  assert s['version'] in pages[0] and s['surname'] in pages[0]
  path=ROOT/'docs/papers'/s['filename']
  if path.exists(): assert path.read_bytes()==pdf.read_bytes()
  else:path.write_bytes(pdf.read_bytes())
  anchors=[]
  for n,finding in s['anchors'].items():
   p=BASE/f'{s["short"]}-page-{n:03}.txt';assert p.read_text()==pages[n-1]
   anchors.append(dict(anchor=f'PDF physical page {n}',finding=finding,extracted_text=ref(p,'Inspected original text; no fresh pixel review')))
  sources.append(dict(integrated_citation_key=s['key'],kind='paper',title=s['title'],authors=s['authors'],author=s['authors'],first_author=s['surname'],year=2026,
   source_identity=receipt['url'],version_date=f'{s["version"]}; archive {s["archive"]}; printed {s["printed"]}; acquired 2026-10-23',
   local_path=str(path.relative_to(ROOT)),sha256=digest,bytes=path.stat().st_size,local_copy=ref(path,'Authentic selected cutoff PDF'),
   inspected_anchors=anchors,supported_claims=s['claims'],limitations=LIMITS,
   identity_evidence=[ref(RAW/(s['raw']+'.receipt.json'),'Acquisition hash and identity'),ref(xml,'Archive identity only'),ref(BASE/(s['short']+'-pdfinfo.txt'),'PDF metadata')],
   version_note='Geometric v1 is preserved as acquired; pre-cutoff v2 is selected. Archive submission and printed manuscript dates are different fields.'))
 code=Path(exact.__file__)
 reference=dict(integrated_citation_key='exec23_structured_reference',kind='project_derivation_and_exact_reference',
  title='Exact structured causal-model, weighting and source-diagnostic references',author='Causal banking proposal project',year=2026,
  source_identity=str(code.relative_to(ROOT)),version_date='2026-10-23',local_copy=ref(code,'calculate(): finite group, covariance and rational weighting checks'),
  inspected_anchors=['calculate() independent arithmetic and finite enumeration'],
  supported_claims=['A finite subgroup is unchanged by left multiplication from within it.', 'A negative nonzero IV covariance still gives a defined effect ratio.',
   'Equal-branch and customer-weighted net values are 6 and -18/5 USD for stipulated sizes/effects.',
   'A nonconstant weight modification changes a stipulated contrast from 2 to 28/5 USD.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=sources+[reference],visual_acceptance=False,native_execution=False))
 write(BASE/'exact-results.json',exact.calculate())
 evidence=[ref(BASE/n,'Reviewed primary text or exact authored reference') for n in ['source-audit.json','exact-results.json','geometric-v2-page-020-alternate.txt','geometric-v2-page-038-alternate.txt','recovery-notes.json']]
 write(BASE/'primary-review.json',dict(status='pass_for_bounded_primary_text_review',evidence=evidence,findings=[c for s in sources for c in s['supported_claims']],limitations=LIMITS,coverage_acceptance=False,visual_acceptance=False,native_execution=False))
 write(BASE/'omissions-register.json',dict(items=[
  dict(gap='GCM foundational proof dependencies and finite-sample inference',action='Inspect independently acquired proof originals and stated rate/CLT conditions before claiming calibration. Do not infer a CLT from ergodicity alone.'),
  dict(gap='Two apparent printed proof slips',action='Retain both text extractions and independent finite witnesses. A fresh permitted visual session can inspect exact symbols; these slips alone do not refute the main theorem.'),
  dict(gap='Hierarchical package implementation',action='Pin AI-vidence/hierarchicalcausalmodels before cutoff, inspect AST, factor fallbacks, normalization, licenses and environment before proposing adoption or execution.'),
  dict(gap='Reproducing reported public-data or synthetic studies',action='Acquire compatible code, public data, licensed dependencies and exact protocols; reported runtime and arithmetic are not local reproduction.'),
  dict(gap='Graph selection and stabilized-functional uncertainty',action='Specify plausible graphs, intervention distribution, unit weighting, positivity and each modified factor; derive or qualify uncertainty for the actual functional.'),
  dict(gap='LLM contribution',action='These are causal-model building blocks; neither paper establishes a general business-to-graph agent or live-model superiority.')],
  whole_census_complete=False))
 old=read(PRIOR/'census-register.json');new=copy.deepcopy(old);changed={s['id']:source for s,source in zip(SPECS,sources)}
 for row in new['items']:
  if row['id'] not in changed:continue
  source=changed[row['id']];assert row['disposition']=='open_original_not_inspected'
  row.update(prior_disposition=row['disposition'],disposition='inspected_primary_retained_with_limits',technical_source_review_open=False,
   source_key=source['integrated_citation_key'],primary_source_record=source,later_primary_review=ref(BASE/'primary-review.json','Selected cutoff primary text'),
   mapping_basis='Inspected identification, estimator semantics and limitations; not an LLM performance claim.',
   availability='Authentic selected pre-cutoff PDF acquired and inspected; code and proof dependencies remain separate.',
   effect_on_claims='Bounded causal-model evidence; no coverage, native, calibration or bank-acceptance closure.',
   next_action='Integrate the qualified argument and independently inspect implementation/proof dependencies before stronger claims.')
 assert len(new['items'])==len(old['items'])==117
 assert all(x==y for x,y in zip(old['items'],new['items']) if x['id'] not in changed)
 counts=Counter(x['disposition'] for x in new['items']);assert counts['inspected_primary_retained_with_limits']==65 and counts['open_original_not_inspected']==48
 new.update(status='successor_bounded_review',counts=dict(counts),supersedes=ref(PRIOR/'census-register.json','Preserved 63 inspected / 50 unread register'),
  changes=['Only LA01-candidate-171 and LA01-candidate-260 changed; 115 other records are preserved.'],
  evidence=[ref(BASE/'primary-review.json','Two selected original reviews')],closure=False,interpretation='65/113 originals inspected; 48 unread; four crosscutting searches remain.')
 write(BASE/'census-register.json',new)
 task=copy.deepcopy(read(PRIOR/'task-map.json'))
 for family in task['task_families']:
  family['coverage_acceptance']=False
  for key,source in changed.items():
   if key in family.get('uninspected_candidate_ids',[]):family['uninspected_candidate_ids'].remove(key)
   if family['id']=='identification':
    if key not in family.setdefault('inspected_candidate_ids',[]):family['inspected_candidate_ids'].append(key)
    if source['integrated_citation_key'] not in family.setdefault('inspected_source_keys',[]):family['inspected_source_keys'].append(source['integrated_citation_key'])
 task.update(register=ref(BASE/'census-register.json','65 inspected / 48 unread'),supersedes=ref(PRIOR/'task-map.json','Preserved fourteen task families'))
 write(BASE/'task-map.json',task)
 write(BASE/'reconciliation-review.json',dict(status='pass',changed_ids=sorted(changed),unchanged_other_records=115,original_candidates=113,inspected=65,unread=48,
  evidence=[ref(BASE/'census-register.json','Conserved 117 rows'),ref(BASE/'task-map.json','Preserved task structure')]))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_source_review',evidence=[ref(BASE/'plan.md','Independent source unit'),ref(BASE/'primary-review.json','Actual inspected findings')],
  findings=['Use pre-cutoff geometric v2 after metadata discovery; preserve the first acquired v1.', 'Separate theorem assumptions, practical normalization, reported experiments and independent exact witnesses.',
            'Preserve uncertainty and coverage limits; continue other source lanes independently.']))
 verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'primary-review.json'))
 print(json.dumps(dict(inspected=65,unread=48,added_genuine_papers=2,coverage_complete=False)))

if __name__=='__main__':main()
