#!/usr/bin/env python3
"""Bounded cutoff Julia/Rust IV/RD source audit; no native qualification."""
from pathlib import Path
import hashlib,json
import run_program_checkpoint_v3 as c
import other_iv_rd_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=c.base;ROOT=run.core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-23/other-iv-rd-v1';OP='SW.CELL.iv_rd_design.other_relevant'
OUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
REPOS=['FixedEffects/FixedEffectModels.jl','nignatiadis/RegressionDiscontinuity.jl','gragusa/InstrumentalVariables.jl','xiangao/RDRobust.jl','suenot/127-regression-discontinuity']
LIMITS=['Bounded current repository discovery with created-date filter is not a historical complete index; technical claims use authenticated pre-cutoff commits.',
 'Eight further returned Julia repository leads and other languages remain uninspected; zero Rust IV hits is not evidence of absence.',
 'Selected source inspection and independent reference calculations only; no downloaded code, upstream tests or native packages executed.',
 'Scientific originals named in software comments are not newly cited or admitted without genuine PDFs and inspected technical anchors.',
 'RDRobust.jl is reviewed as the distinct xiangao repository; its metadata author string does not establish official RD Packages endorsement or parity.',
 'Dependency rights, numerical conformance, statistical calibration and bank economics remain unqualified.',
 'No integration capability, full coverage closure, or final proposal acceptance is granted.']

def main():
 state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP and not OUT.exists()
 specs={
 (0,0):('3-38','Julia high-dimensional FE/IV package and declared comparison targets; unexecuted speed claims are not adopted.'),
 (0,1):('1-22','MIT Expat notice and warranty terms; dependency clearance separate.'),
 (0,2):('1-53','Version 2.1.0; Julia1.10; FixedEffects2.6/3, Vcov0.8 and explicit dependencies; no resolved artifact.'),
 (0,3):('116-138;158-197;235-286;327-375','Formula and finite checks; positive-weight sample filtering; HC2/HC3 FE refusal; FE nonconvergence logged but fitting continues; first-stage rank-test exception leaves NaN; degrees floored at1.'),
 (0,4):('8-38','Lightweight object stores sample mask, coefficients, covariance and schema, not original data; separate data custody required.'),
 (0,5):('15-32','Formula IV parsing, malformed and no-endogenous guards and instrument-count guard; syntax does not establish exclusion.'),
 (0,6):('7-55;144-235;244-265','Relative sweep rank tolerance; removes collinear terms, can recategorize endogenous columns as exogenous; 2SLS projection and first-stage residuals; omitted coefficients reinserted0 with NaN covariance.'),
 (1,0):('19-55','Explicit experimental warning; naive sharp RD without bias correction; separate optimized-estimator lead.'),
 (1,1):('1-21','MIT license text; no solver/dependency rights cleared.'),
 (1,2):('1-57','Version0.4.0, Julia1.9, GLM/JuMP/Empirikos and numerical dependencies; unlocked environment.'),
 (1,3):('1-38','Module delegates to running-variable, bandwidth, local-linear, minmax, density and noise-induced randomization sources.'),
 (1,4):('22-80;87-93','Weighted local-linear contrast and EHW variance; table marks bias unaccounted; p-value uses one upper normal tail at absolute z while CI uses two-sided alpha/2.'),
 (1,5):('112-167','Density method fits local linear binned densities, logs their ratio, and uses two-sided normal tail; positive local density/support requirements need explicit guards.'),
 (1,6):('1-12;26-83','IK-named bandwidth uses pilot density, cubic derivative, side quadratic curvature and regularization; sparse-support/zero-curvature cases require native replay.'),
 (1,7):('5-35;84-110;124-144','Explicit threshold inclusivity and treatment direction; discretized binning/weights and numeric cutoff retained.'),
 (1,8):('1-19;33-47;66-131','Curvature bound B and external solver required; homoskedastic variance estimate; optimize! followed by value extraction without local status guard; bias-aware normal radius is a separate contract.'),
 (1,9):('54-85;273-300','Noise-induced randomization exposes outcome bounds, target, convex class, solver, skip_bias and optimization budget; selected optimization extracts values without local termination guard; full theory/delegates unreviewed.'),
 (2,0):('7-38','Legacy Julia IV interface and covariance claims; README default HC0 wording differs from inspected no-argument covariance implementation.'),
 (2,1):('1-22','MIT Expat notice.'),
 (2,2):('1-5','Legacy REQUIRE declares Julia0.3 and unbounded Reexport/GLM/StatsBase/CovarianceMatrices dependencies.'),
 (2,3):('54-75;107-127;179-195;224-254','Legacy Cholesky 2SLS; DimensionMismatch values constructed without throw and instrument-count expression checks rows; displayed p uses normal upper tail at squared statistic; weighted default covariance mutates residual vector in place.'),
 (3,0):('1-27','Distinct Julia rdrobust implementation with declared workflow and tolerance claim; neither official provenance nor observed parity established.'),
 (3,1):('1-21','MIT notice credits Xiang Ao; metadata authorship and official support remain distinct.'),
 (3,2):('1-28','Version0.1.1 and Julia1.6 compatibility; DataFrames/Distributions/Missings dependencies; author field alone is not affiliation evidence.'),
 (3,3):('90-207;270-295;335-490','Missing conversion and filtering, numeric cluster conversion, polynomial/bias bandwidths, sharp/fuzzy ratio gradient, warning plus pseudoinverse under covariate collinearity, separate conventional/bias-corrected/robust interval rows.'),
 (3,4):('108-146;200-233;298-322','Scale standardization, mass-point counts and bandwidth enlargement, side pilots and regularization, CER multiplier; these do not establish identification for discrete scores.'),
 (3,5):('19-29;146-191','Helper named qrXXinv directly inverts cross-product; complete_cases excludes NaN but not infinity; cluster correction uses g/(g-1) and (n-1)/(n-k).'),
 (4,0):('1-38','Trading-oriented RD repository; introductory near-threshold randomization claim requires scientific assumptions and is not adopted as evidence.'),
 (4,1):('1-21','MIT notice credits Eugen Soloviov.'),
 (4,2):('1-38','rdd_trading0.1.0 Rust2021; trading examples, async and HTTP dependencies; no trading/network execution allowed or performed.'),
 (4,3):('141-242;245-433;434-483','Sharp intercept contrast and normal CI; zero-SE statistic fallback0; fuzzy first-stage threshold0.01 and RF-only SE divided by first stage, omitting denominator variance/covariance; determinant ridge and denominator floors; heuristic IK-named bandwidth.'),
 (4,4):('102-167','Density diagnostic uses near-cutoff counts after computing unused binned counts; nonpositive local density falls back to theta0,se1 and thus p1; this is not accepted no-manipulation evidence.')
 }
 allrecords=[];sources=[];identities=[]
 manifests=[read(BASE/n)['requests'] for n in ['source-manifest.json','additional-source-manifest.json']]
 maps=[r for rows in manifests for r in rows if r.get('source_path')]
 for i,repo in enumerate(REPOS):
  cp=RAW/f'exec23_otheriv_cutoff_{i}.json';tp=RAW/f'exec23_otheriv_tree_{i}.json';commit=read(cp)[0];tree=read(tp);pin=commit['sha'];date=commit['commit']['committer']['date']
  assert date<'2026-10-07T15:59:59Z' and tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
  entries={x['path']:x for x in tree['tree']};records=[]
  for row in maps:
   if row['repository']!=repo:continue
   j=int(row['id'].split('_')[-1]);p=RAW/(row['id']+'.txt');rp=p.with_suffix('.receipt.json');data=p.read_bytes();rec=read(rp);up=row['source_path']
   url=f'https://raw.githubusercontent.com/{repo}/{pin}/{up}';blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   assert rec['status']=='saved' and rec['url']==url and rec['sha256']==run.core.sha(p) and blob==entries[up]['sha'] and len(data)==entries[up]['size']
   span,claim=specs[i,j];record=dict(source_identity=url,version_date=date+'; '+pin,upstream_path=up,local_copy=ref(p,span),receipt=ref(rp,'Acquisition identity'),
    git_blob_sha1=blob,inspected_anchors=[span],supported_claims=[claim],executed=False)
   records.append(record)
  assert len(records)==[7,10,4,6,5][i]
  identity=dict(repository=repo,commit=pin,date=date,tree_sha=tree['sha'],records=len(records),evidence=[ref(cp,'Cutoff-selected commit'),ref(tp,'Canonical tree')]);identities.append(identity)
  sources.append(dict(integrated_citation_key=f'exec23_otheriv_source_{i}',kind='software_primary_sources',title=repo+' selected IV/RD implementation contracts',author=repo+' contributors',year=int(date[:4]),source_identity='https://github.com/'+repo+'/tree/'+pin,version_date=date+'; '+pin,local_copy=records[0]['local_copy'],identity=identity,records=records,inspected_anchors=[x['inspected_anchors'][0] for x in records],supported_claims=[x['supported_claims'][0] for x in records],limitations=LIMITS))
  allrecords+=records
 assert len(allrecords)==32
 write(BASE/'identity-review.json',dict(identities=identities,cutoff='2026-10-07'))
 write(BASE/'exact-results.json',exact.calculate())
 sources.append(dict(integrated_citation_key='exec23_otheriv_reference',kind='project_authored_exact_reference',title='Fuzzy-ratio uncertainty and IV/RD implementation witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/other_iv_rd_reference_20261023.py',version_date='2026-10-23',local_copy=ref(Path(exact.__file__),'calculate() independent exact and normal-tail calculations'),inspected_anchors=['calculate()'],supported_claims=['Reduced form2 and first stage1/5 yield effect10 and stipulated net4; full regular delta variance24 versus frozen-denominator variance1.',
  'At z2 normal tails distinguish usual two-sided .04550026, one-tail .02275013 and squared-z .00003167.',
  'Repeated score points leave local-linear design rank deficient; repeated weighted residual mutation changes squared norm4 to16.'],limitations=LIMITS))
 write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',native_execution=False))
 searches=[];discovered=set()
 for i in range(4):
  p=RAW/f'exec23_otheriv_search_{i}.json';rp=p.with_suffix('.receipt.json');d=read(p);rc=read(rp);assert run.core.sha(p)==rc['sha256'] and rc['status']=='saved'
  names=[x['full_name'] for x in d['items']];discovered.update(names)
  searches.append(dict(query=rc['url'],total_count=d['total_count'],returned=len(names),candidates=names,evidence=[ref(p,'Repository discovery only'),ref(rp,'Query receipt')]))
 uninspected=sorted(discovered-set(REPOS));assert len(uninspected)==8
 write(BASE/'search-review.json',dict(status='bounded_discovery_repaired_not_complete',cutoff='2026-10-07',queries=searches,
  inherited=ref(RAW/'v12_sw_cell_iv_rd_design_other.json','Compound fulltext query returned unrelated literature; no absence inference'),
  stopping_rule='Four separate language/topic repository searches, top10 each; five selected concrete source profiles; all other returned leads retained.',
  uninspected_candidates=uninspected,limits=LIMITS,web_discovery=ref(BASE/'discovery-review.json','Discovery leads, not technical evidence')))
 omissions=[dict(item=x,status='uninspected_candidate',next_action='Pin cutoff identity, inspect original estimator/inference and license, determine alias/replication relationship, then write a scoped disposition.') for x in uninspected]
 omissions += [dict(item='FixedEffects/Vcov solver and rank-test delegates',status='selected_surface_only',next_action='Resolve exact dependency artifacts and inspect rank/covariance numerical delegates; source API statistics do not establish weak-IV confidence sets.'),
  dict(item='RegressionDiscontinuity optimized/NIR proofs and delegates',status='partial_source_only',next_action='Inspect genuine theoretical originals and all needed numerical delegates, curvature/noise assumptions and solver-status/discretization contracts before claims.'),
  dict(item='RDRobust Julia upstream equivalence and artifact origin',status='unexecuted_unendorsed',next_action='Check repository provenance and use independent matched sharp/fuzzy, mass-point, rank, zero-denominator and covariance trials; do not borrow R qualification.'),
  dict(item='Other language/platform coverage',status='open',next_action='Continue separately targeted languages and registries; zero-result query is not a negative capability finding.'),
  dict(item='Native execution and economics',status='not_performed',next_action='Use authorized installed profiles for predeclared public/synthetic trials; preserve failures, all costs and controls.') ]
 write(BASE/'omissions-register.json',dict(items=omissions,global_blocker=None))
 contract=dict(status='proposed_not_implemented',integration_allowed=False,requirements=[
  'Declare threshold rule/inclusivity, eligibility and receipt treatment, outcome clock, locality, exclusion and monotonicity when interpreting a fuzzy ratio.',
  'Do not substitute fixed effects, high first-stage statistics or a failed density rejection for causal assumptions.',
  'Require finite inputs, valid weights, side support and independent score counts; preserve sample selection and rank/column reclassification.',
  'Separate reduced-form, first-stage and structural targets; preserve their joint covariance and refuse unqualified near-zero denominators.',
  'Retain partial-out convergence flags, actual covariance method, degrees of freedom, missing first-stage tests and dropped coefficients.',
  'Distinguish conventional, bias-corrected and robust-bias-corrected intervals and method-specific curvature/discretization assumptions.',
  'Check solver termination, numerical error, input scaling and repeated accessor purity with independent oracles.',
  'Report density unavailable when local cells are empty; no default zero statistic or p1 may count as assumption validation.',
  'Do not run trading/network code; selected worker profiles must exclude unrelated operational functionality.'])
 write(BASE/'conversion-contract.json',contract)
 write(BASE/'plan-review.json',dict(status='pass_for_bounded_execution',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Recovery continuation plan')],findings=['Separate discovery, cutoff authentication and actual technical claims.',
  'Five profiles and all eight remaining returned leads are represented; coverage stays inconclusive.',
  'Inspect numerical/inference delegates and compare explicit variance and refusal behavior before considering integration.']))
 choices=[dict(repository=REPOS[0],route='conditional Julia worker/reference',reason='Substantive FE/2SLS profile; convergence, rank, Vcov delegates and weak-IV inference need separate qualification.'),
  dict(repository=REPOS[1],route='research reference; defer integration',reason='Explicit experimental warning, naive p-value mismatch and optimized/noise-based routes need scoped proof and solver review.'),
  dict(repository=REPOS[2],route='historical reference; reject current native adoption',reason='Legacy Julia0.3 dependencies, ineffective dimension guards, displayed probability and mutable-covariance hazards; prefer a maintained evaluated route.'),
  dict(repository=REPOS[3],route='conditional comparator; defer adoption',reason='Useful local-polynomial/bias and ratio covariance surfaces; distinct repository provenance, inverse/rank/cluster controls and native equivalence unresolved.'),
  dict(repository=REPOS[4],route='reject for proposed scientific engine at this pin',reason='Fuzzy denominator uncertainty omitted, fixed weak threshold and misleading empty-density fallback; trading examples do not establish a causal design.')]
 write(BASE/'reuse-routes.json',dict(routes=choices,porting='No new port until a measured requirement justifies duplicate numerical/inference maintenance.',costs=['Cutoff/version/dependency maintenance','Data and score conversion','Fit and uncertainty including failures','Solver/worker/recovery cost','Scientific and rights review'],owners=dict(scientific='Target/assumptions/uncertainty',maintainer='Exact numerical and failure profile',operator='Artifacts, budgets and custody'),integration_allowed=False))
 evidence=[ref(BASE/n,'Reviewed source and contract evidence') for n in ['plan.md','plan-review.json','identity-review.json','source-audit.json','search-review.json','exact-results.json','conversion-contract.json','reuse-routes.json','omissions-register.json']]+[ref(Path(__file__),'Audit implementation'),ref(Path(exact.__file__),'Independent reference')]
 criteria=[dict(index=0,verdict='inconclusive',finding='Five source profiles reviewed, with eight returned candidates and broader language/algorithm coverage still open.'),
  dict(index=1,verdict='pass',finding='Thirty-two original files match cutoff canonical trees and acquisition SHA; selected technical anchors and independent references support bounded claims.'),
  dict(index=2,verdict='pass',finding='Candidate-specific adoption/refusal alternatives and source/proof/runtime omissions are explicit; no unavailable original is waived.')]
 trigger='Inspect the eight remaining returned candidates and actual numerical/theory delegates; qualify permitted installed profiles with independent weak-IV, discrete-score, covariance and failure oracles.'
 output=dict(operation_id=OP,status='inconclusive',scope='Selected Julia and Rust IV/RD implementation, inference and refusal contracts',reviewer=REVIEWER,cutoff='2026-10-07',candidate_ids=REPOS,documented_findings=[c for s in sources for c in s['supported_claims']],alternatives=choices,evidence=evidence,limitations=LIMITS,criteria=criteria,revisit_trigger=trigger,integration_allowed=False,capabilities=[],coverage_complete=False,bank_inputs_required=False)
 write(OUT,output);write(BASE/'review.json',dict(status='inconclusive_for_coverage',reviewer=REVIEWER,reviewed_output=ref(OUT,'Bounded coverage disposition'),findings=criteria,evidence=evidence,limitations=LIMITS))
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
 receipt.update(outcome='inconclusive',execution='performed',scope=output['scope'],reviewer=REVIEWER,capabilities=[],outputs=[ref(OUT,'Contracted coverage review')],limitations=LIMITS,nonexecution_reason='',revisit_trigger=trigger,criteria=[dict(x,evidence=evidence+[ref(BASE/'review.json','Author review')]) for x in criteria])
 verify_bindings(receipt);run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']));write(BASE/'operation-receipt.json',receipt)
 print(json.dumps(dict(operation=OP,outcome='inconclusive',files=32,profiles=5,uninspected_candidates=8,native_execution=False)))

if __name__=='__main__':main()
