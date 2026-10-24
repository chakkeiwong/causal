#!/usr/bin/env python3
"""Audited reference disposition; never executes downloaded package code."""
import argparse, hashlib, json
from pathlib import Path
import augsynth_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/augsynth-reuse-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.DECISION.seed_067'
PIN='7e70072232fe75057aa8b5d7af08c7e1aef53ae8'
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected single-date ridge and conformal paths, not exhaustive package qualification.',
 'Downloaded R package, upstream tests and solver dependencies were not executed; authored base-R expressions only checked language semantics.',
 'Full staggered, multiple-outcome, gsynth, jackknife and placebo paths remain unqualified.',
 'Complete installed rights, OSQP internals, native diagnostics, empirical uncertainty and full costs remain open.',
 'Static conditional findings and exact authored witnesses are not observed package failures or bank benefits.',
 'Reference-only decision grants no native capabilities, independent review, visual or final acceptance.']
SPECS={
 'DESCRIPTION':[(1,35,'Version, dependencies, MIT declaration and minimum R/OSQP versions')],
 'LICENSE':[(1,2,'Copyright metadata')],
 'LICENSE.md':[(1,21,'Actual MIT permission, notice condition and disclaimer; not dependency clearance')],
 'R/augsynth.R':[(28,80,'Single-date defaults, preparation, donor names and target'),(99,167,'Dispatch, fixed effects, transformation forwarding and retention of fitted lambda'),(177,203,'Equal treated average and donor-weight prediction')],
 'R/fit_synth.R':[(8,28,'Transformation shape helper; broad nrow branch requires caller qualification'),(39,57,'Constrained fit and uniform-imbalance denominator'),(76,108,'Auxiliary QP, OSQP tolerances and primal extraction without local status gate')],
 'R/ridge.R':[(35,70,'Defaults, donor centering and feature transformation'),(75,130,'Covariate residualization/standardization and ridge dispatch'),(225,263,'SCM or uniform start and ridge weight update'),(268,342,'SVD maximum, R index-based grid, one-SE rule and actual loss delegate')],
 'R/cv.R':[(1,104,'Separate generic CV helper; not used to infer the inspected ridge loss path')],
 'R/inference.R':[(134,189,'Pointwise conformal grid, three-element vapply and joint null'),(279,329,'Null adjustment, model refit, IID permutations and circular shifts'),(345,377,'Raw tail proportion, appended zero and extrema of accepted grid')],
 'R/eligible_donors.R':[(29,44,'Donor treatment strictly after cohort plus horizon'),(48,75,'Missing-observation restrictions'),(78,121,'Matching policy; full staggered estimator remains outside scope')],
 'R/donor_control.R':[(22,59,'Donor table can trigger placebo inference and zero tiny display weights')],
 'R/augsynth_pre.R':[(46,95,'Public dispatch by outcome count and distinct treatment times')],
 'R/ridge_lambda.R':[(17,54,'Actual ridge CV excludes final feasible start; loss mean and sd/sqrt(count)')],
 'R/format.R':[(18,47,'Pre/post split and maximum treatment flag'),(249,292,'Pretreatment covariate aggregation and checks')],
}

def prepare():
 assert not (BASE/'review.json').exists()
 tree=read(RAW/'v12_sw2_tree_augsynth.json');assert tree['sha']==PIN and not tree['truncated']
 by={x['path']:x for x in tree['tree']}
 cutoff=read(RAW/'v12_sw2_author_cutoff_augsynth.json')[0]
 assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']<='2026-10-07T15:59:59Z'
 rows=read(BASE/'acquisition-review.json')['records']+read(BASE/'helper-acquisition-review.json')['records'];assert len(rows)==13
 records=[]
 for row in rows:
  p=ROOT/row['raw_path'];data=p.read_bytes();rc=ROOT/row['receipt'];receipt=read(rc)
  assert core.sha(p)==receipt['sha256']==row['sha256']
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
  assert blob==by[row['path']]['sha']==row['blob_sha']
  lines=data.decode().splitlines();anchors=[]
  for lo,hi,finding in SPECS[row['path']]:
   assert 1<=lo<=hi<=len(lines),(row['path'],hi,len(lines))
   anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest(),finding=finding))
  records.append(dict(source_identity=receipt['url'],upstream_path=row['path'],version_date='0.2.0;4 September 2026;'+PIN,local_copy=ref(p,'Authenticated pinned original'),receipt=ref(rc,'Acquisition'),git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'identity-review.json',dict(status='pass_for_selected_identity',authenticated_files=13,records=records,version='0.2.0',commit=PIN,date=cutoff['commit']['committer']['date'],evidence=[ref(RAW/'v12_sw2_tree_augsynth.json','Pinned tree'),ref(RAW/'v12_sw2_author_cutoff_augsynth.json','Cutoff identity')],native_execution=False))
 write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent Fraction arithmetic'),ref(BASE/'exact-results.json','Exact witnesses'),ref(BASE/'r-semantics-correction.json','Rejected grid interpretation corrected before publication'),ref(BASE/'development.tex','Explained argument')],findings=['Centered ridge update preserves sum but admits negative weights; exact example gives -1/4,5/4 and revenue gap20.', 'R sequence indices yield correct nominal lambda endpoints; earlier interpretation rejected.', 'Abstract holdout losses demonstrate possible ranking change without claiming a realized dataset.', 'Raw and plus-one tail proportions differ; no calibration theorem inferred.', '3600USD over180/150/120 yields20/24/30.'],native_execution=False,empirical_coverage=False))
 write(BASE/'dependency-license-review.json',dict(status='source_license_inspected_not_complete_clearance',evidence=[ref(RAW/'exec24_augsynth_src_00.txt','DESCRIPTION'),ref(RAW/'exec24_augsynth_src_02.txt','Actual MIT text')],declared_license='MIT + file LICENSE',dependencies=['OSQP>=1.0.0','Matrix','Formula','dplyr','tidyr','magrittr','ggplot2','MASS','rlang','purrr','FNN','scales'],unresolved=['Installed/transitive rights and distribution','Numerical libraries, termination, covariance and inference qualifications','Support, maintenance, environment and full observed costs'],integration_allowed=False))
 write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Requested/resolved single,multi-outcome or staggered route','Scientific unit, exposure weighting, eligible donors and information clock','Aligned unit-time panel and persistent-treatment contract','Centered matrices, covariates, transformation, lambda grid, holdouts and RNG'],outputs=['Fitted weights including negatives and l1 norm','Numerical status, residuals and zero-denominator states','All tuning/null-refit attempts, full grids, acceptance sets and failures','Inference law, pointwise/simultaneous scope and complete costs'],refusals=['Unsupported staggered or multi-outcome qualification','Unjustified donor extrapolation or dependence law','Missing/misaligned/nonfinite inputs or unqualified solver result','Repeated-zero, empty, truncated or disconnected grid relabeled as ordinary interval'],oracle=ref(BASE/'exact-results.json','Authored finite reference'),integration_allowed=False))
 write(BASE/'omissions-register.json',dict(known_routes=['Inspect full delegates and installed dependency rights.','Preregister matched public operator,calendar,tuning,solver and grid-degeneracy tests.','Evaluate assumptions, failure denominators, coverage and costs against constrained-donor/factor alternatives.'],no_universal_solution=['Counterfactual stability and donor eligibility need scientific assumptions or new information.','Arbitrary serial dependence or post-outcome donor/tuning selection has no automatic calibrated repair.'],global_blocker=False))
 prior=read(ROOT/'docs/program/execution/2026-10-24/synth-reuse-reader-v1/reader/source-audit.json')
 old=next(s for s in prior['sources'] if s['integrated_citation_key']=='v12_sw_augsynth')
 source=dict(integrated_citation_key='exec24_augsynth_source',kind='software_primary_sources',title='augsynth 0.2.0 pinned dispatch, ridge, tuning, donor and inference paths',author='Eli Ben-Michael',year=2026,source_identity='https://github.com/ebenmichael/augsynth/tree/'+PIN,version_date='0.2.0;4 September 2026;'+PIN,local_copy=ref(RAW/'exec24_augsynth_src_05.txt','Selected ridge implementation'),records=records,identity_evidence=[ref(BASE/'identity-review.json','Authenticated identities')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[c for r in records for c in r['supported_claims']],limitations=LIMITS)
 authored=dict(integrated_citation_key='exec24_augsynth_choice',kind='project_evidence_not_scholarly_paper',title='Authored augmented-control extrapolation,tuning,inference and reference decision',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24 October 2026;cutoff7 October2026;no native package execution',local_copy=ref(BASE/'mathematical-review.json','Authored witnesses'),inspected_anchors=[ref(BASE/n,'Reviewed contract') for n in ['conversion-contract.json','omissions-register.json','exact-results.json']],supported_claims=['Exact negative-weight and revenue example','Corrected lambda indexing and abstract holdout counterexample','Bounded inference-grid interpretation','Reference-only proposal decision and illustrative complete-cost denominators'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,authored,old],new_records=2,new_scholarly_pdfs=0,native_execution=False))
 choice=dict(operation=OP,candidate='augsynth',decision='reference',source_review=ref(BASE/'source-audit.json','Thirteen pinned originals'),target='Single-date ridge-augmented donor comparison under justified extrapolation and resampling restrictions',alternatives=[dict(route='Direct R adapter',decision='defer',reason='Complete dependencies,rights,numerical and inference qualification absent'),dict(route='Whole-library port',decision='defer',reason='No demonstrated benefit over reference; must reproduce dispatch,centering,R indexing,refits and failure semantics'),dict(route='Independent finite oracle',decision='use for reference tests',reason='Reproducible bounded equations and denominators,not package or causal qualification'),dict(route='Constrained-donor,factor or staggered alternatives',decision='separate review',reason='Different targets and assumptions; no inherited qualification')],owners=[dict(role=r,obligation=o) for r,o in [('Scientific','Donor eligibility,extrapolation,target and resampling law'),('Adapter','Aligned matrices,weights,clock,tuning,status and refusal'),('Rights/platform','Complete pinned installed distribution'),('Evaluation','Preregistered public oracles,failures and full costs')]],costs=dict(prices='Unmeasured;3600USD illustrative',categories=['engineering','scientific/rights review','tuning and all null refits','failed compute','storage,recovery,maintenance']),maintenance='Named author and September2026commit; future support not qualified.',revisit_trigger='Justified augmented-control prototype demand plus complete dependency/rights resolution and preregistered dispatch,negative-weight,calendar,tuning,solver,grid-degeneracy,resampling and full-cost public trials.',integration_allowed=False,capabilities=[],limitations=LIMITS)
 write(BASE/'choice.json',choice)
 write(BASE/'plan-review-v2.json',dict(status='pass_for_reference_disposition',evidence=[ref(BASE/n,'Reviewed plan/result') for n in ['plan-review.json','choice.json','source-audit.json','mathematical-review.json']],findings=['Actual ridge delegate inspected rather than generic CV inference.','R sequence misinterpretation corrected using authored base-language expressions.','Unqualified full paths retained as limits; reference decision complete.']))
 write(BASE/'copyedit-review.json',dict(status='pass_for_connected_scoped_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Sponsor consequences')],findings=['Notation,banking examples,assumptions,alternatives,owners and costs explicit.','Static findings distinguished from native runs; no uninspected paper theorem used.'],visual_acceptance=False))
 review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed augmented-control unit') for n in ['source-audit.json','identity-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','plan-review-v2.json','mathematical-review.json','copyedit-review.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Decision logic')],findings=['Thirteen originals authenticated to pinned tree with inspected anchors.','Corrected exact witnesses and conditional source findings reviewed.','Reference only;integration false,capabilities empty.'],limitations=LIMITS,integration_allowed=False)
 verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(authenticated=13,new_records=2,new_papers=0,decision='reference')))

def receipt():
 state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
 verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
 value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference decision; no native admission',evidence=[ref(BASE/'review.json','Author review')]);out=ROOT/node['outputs'][0];write(out,value)
 evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
 findings=['Pinned identity,actual license and bounded dependency/maintenance scope inspected.','Target,negative weights,tuning,inference,alternatives,roles,costs and revisit trigger explicit.','Reference only;integration false,capabilities empty; native public qualification conditional.']
 result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Augmented-control reference receipt prepared.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
