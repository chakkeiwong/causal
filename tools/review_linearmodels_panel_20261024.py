#!/usr/bin/env python3
"""Authenticate selected panel sources and record a preserving proposal comparison."""
import hashlib,json
from pathlib import Path
import linearmodels_panel_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-24/linearmodels-panel-v1'
FOLLOW=ROOT/'docs/program/execution/2026-10-24/panel-followups-v1'
OLD=ROOT/'docs/program/execution/2026-10-24/panels-python-v1'
IV=ROOT/'docs/program/execution/2026-10-22/linearmodels-reuse-v1'
RAW=ROOT/'docs/literature/raw';PIN='13390eee49ea06fc42f831255ff2163f2ad13e8b'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected PanelOLS and helper review;not exhaustive Python panel coverage.',
 'Dynamic repository version;release wheel and installed environment equality unverified.',
 'Top-level NCSA identity retained;complete dependency/binary rights unresolved.',
 'No downloaded package imported,upstream test executed or native trial performed.',
 'Exact arithmetic is authored;abstract indefinite/irregular-clock scores are not claimed fitted package outputs.',
 'Original inconclusive coverage receipt remains unchanged;search,other estimators and native qualification remain open.',
 'Causal assignment truth,arbitrary dependence and unrestricted heterogeneous effects have no universal software guarantee.',
 'No fresh visual,independent or final acceptance.']
SPECS={
 'linearmodels/panel/model.py':[(78,94,'Dense least-squares rank cutoff and gelsy driver'),
  (401,503,'Weight shape,missing rows and positive mean normalization'),(1260,1312,'Singleton true retains;false enters two-core removal'),
  (1480,1551,'Sparse LSMR coefficients extracted without local termination fields'),
  (1777,1840,'Nesting assignment and one/multiple-effect adjustment;fit defaults'),
  (1909,2022,'Fit transformation,absorbed-regressor mutation,covariance and regression degrees of freedom')],
 'linearmodels/panel/covariance.py':[(94,139,'Covariance effective sample and scale'),
  (277,339,'One/two-way group covariance,optional corrections and symmetrization'),
  (430,453,'Time score aggregation,ordinal kernel and default bandwidth')],
 'linearmodels/panel/utility.py':[(400,435,'Repeated singleton-removal reference algorithm'),
  (439,550,'Absorption checks and retained-column construction')],
 'linearmodels/panel/data.py':[(364,397,'Entity/time category codes and missing-index rejection'),
  (437,536,'Weighted iterative demeaning and local tolerance without explicit cap')],
 'linearmodels/shared/covariance.py':[(16,42,'Group finite-sample scale'),(45,105,'Intersection identities and cluster score sums'),
  (108,139,'Ordinal kernel cross-products')],
 'linearmodels/iv/covariance.py':[(45,70,'Bartlett weights by ordinal lag')],
 'linearmodels/shared/linalg.py':[(8,46,'Constant/rank detection helper')],
 'linearmodels/panel/results.py':[(86,106,'Square-root diagonal standard errors and residual-df p-values'),
  (317,344,'Residual-df or normal confidence quantiles')]
}


def main():
 assert not (BASE/'review.json').exists()
 tree=read(RAW/'exec22_pyiv_linearmodels_tree.json');assert tree['sha']==PIN and not tree['truncated']
 by={r['path']:r for r in tree['tree']}
 identity=read(IV/'identity-review.json');verify_bindings(identity)
 assert identity['commit']==PIN and identity['commit_date']<='2026-10-07T15:59:59Z'
 entries=sum([read(FOLLOW/n) for n in ['source-index.json','helper-source-index.json','results-source-index.json']],[])
 records=[]
 for row in entries:
  p=ROOT/row['raw_path'];data=p.read_bytes();receipt=RAW/(row['key']+'.receipt.json');rc=read(receipt)
  digest=hashlib.sha256(data).hexdigest();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
  assert digest==rc['sha256'] and blob==row['blob_sha']==by[row['path']]['sha']
  assert '/'+PIN+'/' in rc['url']
  lines=data.decode().splitlines();anchors=[]
  for lo,hi,f in SPECS[row['path']]:
   assert 1<=lo<=hi<=len(lines),(row['path'],hi,len(lines))
   anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest()))
  records.append(dict(source_identity=rc['url'],repository_path=row['path'],git_blob=blob,
   version_date='7October2026;'+PIN,local_copy=ref(p,'Pinned authenticated original'),
   acquisition=ref(receipt,'Public source receipt'),inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
 assert len(records)==8
 write(BASE/'identity-review.json',dict(status='pass_for_selected_pinned_sources',records=records,
  inherited=ref(IV/'identity-review.json','Version,license,dependencies and source identity'),
  tree=ref(RAW/'exec22_pyiv_linearmodels_tree.json','Pinned full tree'),cutoff='2026-10-07',release_equivalence=False))
 write(BASE/'exact-results.json',exact.calculate())
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_examples',
  evidence=[ref(Path(exact.__file__),'Exact rational regression'),ref(Path(exact.prior.__file__),'Preserved score witnesses'),
   ref(BASE/'exact-results.json','Exact results'),ref(BASE/'development.tex','Connected derivation')],
  findings=['Within beta7/5 and scores reproduce;raw cluster128/625 versus white64/625.',
   'Nested scale4/3 and group scale3/2 yield512/1875 and256/625;residual df1 differs from scale denominator3.',
   'Abstract two-way score givesnegative1;ordinal5/3 differs from calendar7/3.',
   '3600USD divided over180/150/120 gives20/24/30.'],native_execution=False,empirical_coverage=False))
 write(BASE/'dependency-license-review.json',dict(status='inherited_top_level_inspected_not_complete_clearance',
  evidence=[ref(IV/'identity-review.json','Inherited inspected license and build metadata'),
   ref(RAW/'exec22_pyiv_linearmodels_source_3.txt','Original NCSA terms'),
   ref(RAW/'exec22_pyiv_linearmodels_source_4.txt','Original build/runtime declarations')],
  unresolved=['Dynamic version versus installed wheel','Transitive rights and binary notices','SciPy solver and numerical stack lock','Target-platform performance and support'],integration_allowed=False))
 write(BASE/'conversion-contract.json',dict(status='proposed_panel_worker_only',
  inputs=['Causal target,formula,strict-exogeneity and common-effect restrictions','Original entity/calendar indices and gaps',
   'Weight meaning,missingness,singleton and absorbed-regressor policy','Requested/resolved covariance,effect df,cluster groups,group correction,bandwidth',
   'Numerical path,tolerances,resource and termination policy'],
  outputs=['All dropped rows/columns and retained target mapping','Coefficients,transformed residuals,rank and covariance components',
   'Covariance scale,group scale and reference df/distribution separately','Original and ordinal calendars,solver diagnostics,refusals and complete costs'],
  refusals=['Missing treatment variation or absorbed requested coefficient','Unjustified assignment/dependence law',
   'Unsupported rank,nonfinite/non-PSD covariance or unqualified solver exit','Unregistered dropped-row/clock transformation'],integration_allowed=False))
 next_action='Selected linearmodels panel sources are now directly inspected and integrated;do not repeat this inspection. Preserve original inconclusive Python coverage. Screen remaining synthetic-control,reversal and multiple-event candidates, inspect remaining nuisance/dependency paths, and preregister known-law target,unequal-cluster,absorption,singleton,nesting-order,irregular-calendar,solver/failure and full-cost native trials.'
 write(BASE/'omissions-register.json',dict(status='bounded_source_gap_addressed_broader_coverage_open',
  prior=ref(OLD/'operation-receipt.json','Unchanged inconclusive coverage'),
  remaining=['Additional concrete Python panel candidates and search tails','Other linearmodels panel estimators and uninspected methods',
   'Nested-group order and few-cluster qualification','Complete preprocessing/dependency rights and runtime','Native fixtures and independent scientific acceptance'],
  unknown_without_information=['Assignment and counterfactual truth','Arbitrary dependence and unrestricted effect heterogeneity'],next_action=next_action,global_blocker=False))
 write(BASE/'comparison-review.json',dict(status='pass_for_bounded_source_comparison',
  alternatives=[dict(candidate='PanelOLS worker',route='conditional integration',reason='Explicit linear fixed-effects target;requires native and scientific qualification'),
   dict(candidate='PyFixest',route='preserve prior comparison',reason='Different transformation and inference choices must be matched'),
   dict(candidate='differences/csdid',route='preserve prior comparison',reason='Group-time treatment targets differ from a common panel slope'),
   dict(candidate='Full port',route='defer',reason='No measured benefit versus qualified worker;must preserve numerical and covariance semantics'),
   dict(candidate='Rational oracle',route='reference',reason='Small conversion and algebra checks only')],
  owners=['Scientific target/dependence owner','Adapter/schema owner','Rights/platform owner','Independent evaluation owner'],
  costs=['Preprocessing','All solves/retries','Tuning/validation','Rights/scientific review','Storage','Maintenance'],
  prices='3600USD authored example,not measured',next_action=next_action,capabilities=[],integration_allowed=False))
 write(BASE/'plan-review-v2.json',dict(status='pass_for_preserving_source_successor',
  evidence=[ref(BASE/n,'Reviewed plan and evidence') for n in ['plan.md','identity-review.json','comparison-review.json','mathematical-review.json']],
  findings=['Separate linear-IV review from panel implementation.','Separate exact authored regression from abstract score witnesses and native calibration.',
   'Original coverage receipt remains inconclusive;known follow-up recorded.','Combine sponsor and exact-byte renewals after fect successor.']))
 write(BASE/'copyedit-review.json',dict(status='pass_for_connected_scoped_argument',
  evidence=[ref(BASE/'development.tex','Manuscript'),ref(BASE/'sponsor-addition.md','Sponsor implications')],
  findings=['Explained notation,banking units,assumptions,alternatives and refusal states.','No process checkpoint passed off as causal result.'],visual_acceptance=False))
 source=dict(integrated_citation_key='exec24_lmpanel_source',kind='software_primary_sources',
  title='linearmodels pinned PanelOLS transformations,covariance,clocks and numerical paths',author='Kevin Sheppard and contributors',year=2026,
  source_identity='https://github.com/bashtage/linearmodels/tree/'+PIN,version_date='Dynamic repository version;7October2026;'+PIN,
  local_copy=ref(RAW/'exec24_lmpanel_src_00.txt','Pinned panel model'),records=records,
  identity_evidence=[ref(BASE/'identity-review.json','Identity and cutoff')],inspected_anchors=[r['local_copy'] for r in records],
  supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
 authored=dict(integrated_citation_key='exec24_lmpanel_reference',kind='project_evidence_not_scholarly_paper',
  title='Authored panel regression,covariance-clock and conversion-contract examples',author='Causal banking proposal project',year=2026,
  source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no package execution',
  local_copy=ref(BASE/'mathematical-review.json','Exact reference'),
  inspected_anchors=[ref(BASE/n,'Bounded comparison') for n in ['comparison-review.json','conversion-contract.json','omissions-register.json']],
  supported_claims=['Exact within and covariance algebra','Abstract finite covariance and calendar witnesses','Scope,alternatives,owners,costs and future qualification'],limitations=LIMITS)
 inherited=read(ROOT/'docs/program/execution/2026-10-24/fect-reuse-reader-v1/reader/source-audit.json')
 old=next(s for s in inherited['sources'] if s['integrated_citation_key']=='exec22_linearmodels_reuse')
 write(BASE/'source-audit.json',dict(sources=[source,authored,old],new_records=2,new_scholarly_pdfs=0,native_execution=False))
 review=dict(status='pass_for_bounded_source_followup',reviewer=dict(name='Codex author/coordinator',kind='author'),
  original_result=ref(OLD/'operation-receipt.json','Preserved original inconclusive review'),outcome_remains='inconclusive',
  evidence=[ref(BASE/n,'Reviewed panel-specific source followup') for n in ['source-audit.json','identity-review.json','mathematical-review.json',
   'dependency-license-review.json','conversion-contract.json','omissions-register.json','comparison-review.json','plan-review-v2.json',
   'copyedit-review.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Review logic')],
  findings=['Eight selected source files authenticate to cutoff tree.','Panel-specific fit,covariance and numerical meaning directly inspected.',
   'Authored exact examples reproduce;no native capability admission.'],next_action=next_action,limitations=LIMITS,integration_allowed=False)
 verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(authenticated=8,new_records=2,original_coverage='inconclusive',native_execution=False)))


if __name__=='__main__':main()
