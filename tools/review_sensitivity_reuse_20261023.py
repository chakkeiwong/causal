#!/usr/bin/env python3
"""Audit selected R sensitivity sources and record separate proposal decisions."""
import argparse,hashlib,json,re
from pathlib import Path
import run_program_checkpoint_v3 as controller
import sensitivity_reuse_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/sensitivity-reuse-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Selected authenticated source and independently authored arithmetic only; no downloaded package code executes.',
'CRAN mirror revisions are concrete source snapshots, not a complete release-history or maintenance-service census.',
'Package license declarations and separately identified local GPL texts do not clear transitive dependencies, datasets or a proposed distribution.',
'No native adapter, finite-sample coverage, causal truth, measured bank benefit, visual review or final proposal acceptance is granted.']
META={
'sensemakr':dict(operation='SW.DECISION.seed_057',version='0.1.6',license='GPL-3',title='sensemakr regression sensitivity, covariance, benchmark and boundary contracts',author='Carlos Cinelli and sensemakr contributors',
 target='Omitted-variable coefficient and uncertainty sensitivity for a declared regression and partial-R-squared restrictions; not a universal causal-effect certificate.',
 reason='Retain a transparent regression-sensitivity reference; numerical wrapper, iid covariance and endpoint contracts need explicit native qualification before an adapter.',
 dependencies=['R >= 3.1.0','Suggested fixest, testthat, covr, knitr, rmarkdown, png and stargazer; no frozen environment'],
 contract=['Require model identity, treatment coefficient, adjustment set, row clock, residual degrees of freedom, covariance type and exact effect units.',
 'Preserve both partial R-squared quantities, sign/reduce direction, q, alpha, benchmark groups and multipliers; benchmark plausibility is an explicit scientific assumption.',
 'The inspected fixest extraction forces iid covariance; refuse silently transferring clustered or heteroskedastic standard errors to this profile.',
 'Use a declared finite regular domain and diagnose singular boundaries before computation; retain warnings and raw benchmark caps.',
 'Compare direct numeric helpers, numeric wrapper and model dispatch. The estimate argument is accepted through ellipsis and unused in the SE helper; inspect dof versus dof-1 interval conventions before promising equivalent output.']),
'evalue':dict(operation='SW.DECISION.seed_058',version='4.1.4',license='GPL-2',title='EValue risk-ratio thresholds, effect-scale conversions and refusal contracts',author='Maya Mathur and EValue contributors',
 target='Sensitivity strength for shifting an observed risk ratio to a declared target, with near-target interval-limit reporting; not an estimated confounder, adjusted causal effect or probability of truth.',
 reason='Retain risk-ratio sensitivity as a scoped reference; a selected RR-only worker is conditional on domain, interval and provenance tests. Do not infer general effect-scale equivalence.',
 dependencies=['Imports stats, graphics, ggplot2 >= 2.2.1, metafor, methods, boot, MetaUtility, dplyr','Suggested testthat, knitr, rmarkdown, metadat; no frozen environment'],
 contract=['Require a strictly positive finite ratio, event/treatment coding, effect type, horizon, target and compatible original interval provenance.',
 'Retain point and near-target interval threshold separately; a crossing interval yields threshold one, not proof of no effect.',
 'Carry rare-outcome flags and full conversion history. OR, HR, standardized difference and OLS routes use different approximations and do not preserve arbitrary targets.',
 'For OLS retain delta and the stated outcome standard deviation; the documented interval treatment regards sd as known.',
 'Explicitly handle zero, infinity, missing values and incompatible bounds. Preserve source warnings and do not relabel a nonfinite endpoint as robust evidence.'])}
FINDINGS={
'sensemakr':{
'R/bias_functions.R':([(151,228),(284,314),(434,449),(534,544)],'Signed adjusted coefficients; adjusted variance factor includes dof/(dof-1); fixest iid warning; direct CI uses dof-1; bias and SE functions divide by one minus treatment partial R-squared.'),
'R/sensitivity_stats.R':([(175,214),(593,644),(814,823),(888,910),(946,964)],'Robustness-value branches; group covariance; numeric dof guard permits zero and one; fixest extraction explicitly requests iid covariance and rejects zero residual dof.'),
'R/sensemakr.R':([(431,531)],'Numeric wrapper passes estimate through an SE helper that accepts ellipsis; this is not an unused-argument failure. Its CI uses dof, unlike the direct helper dof-1; native equivalence remains untested.'),
'R/ovb_bounds.R':([(240,241),(286,318)],'Observed-covariate benchmark restrictions are explicit; impossible treatment bounds stop and outcome bounds above one warn then cap at one.'),
'R/ovb_plots.R':([(1408,1432)],'Partial-R-squared guard admits inclusive zero/one endpoints; multiplier checks enforce nonnegative values and equal lengths. Plotting implementation outside these validators is not inspected.'),
'R/other.R':([(1,27)],'Simulation helper constructs random residuals; no executed simulation and no validation delegate here.'),
'DESCRIPTION':([(1,36)],'Source version, CRAN mirror maintenance identity, GPL-3 declaration, R dependency and suggested packages; metadata not a scientific guarantee.'),
'man/sensemakr.Rd':([(95,145)],'Existing documented partial-R-squared sensitivity and observed-covariate benchmark contract retained.')},
'evalue':{
'R/EValue.R':([(27,49),(301,365),(437,460)],'OLS conversions are approximate and sd is treated as known for intervals; RR checks ordered intervals, reports near-target bound and one for crossing; threshold inverts protective ratios and has zero-boundary divisions.'),
'R/effect_measures.R':([(183,245)],'OLS standardization, exp(0.91 MD), rare/nonrare HR and OR routes and history attributes. Missing rare flags stop; nonrare OR uses square root, not a baseline-specific exact identity.'),
'R/utils.R':([(1,49)],'Separate bias-factor and plotting helpers plus message wrapper; no hidden source execution.'),
'DESCRIPTION':([(1,28)],'Concrete version and maintainers, GPL-2 declaration, imports and suggestions; no complete dependency inventory.'),
'man/evalues.RR.Rd':([(1,39)],'RR/rate-ratio interface, target and near-null interval summary; reciprocal example retained.')}}

def audit():
 assert not (BASE/'source-audit.json').exists()
 requests=read(BASE/'source-manifest.json')['requests']+read(BASE/'delegate-manifest.json')['requests']
 sources=[];identities={}
 for key,m in META.items():
  commit=read(RAW/f'v12_sw2_cran_cutoff_{key}.json')[0];tree=read(RAW/f'exec23_sensitivity_tree_{key}.json')
  assert tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
  assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
  entries={x['path']:x for x in tree['tree']};records=[]
  mapping=[(x['id'],x['source_path']) for x in requests if x.get('package')==key]
  mapping += [(f'v12_sw2_description_{key}','DESCRIPTION'),(f'v12_sw2_manual_{key}_1','man/sensemakr.Rd' if key=='sensemakr' else 'man/evalues.RR.Rd')]
  for file_id,path in mapping:
   p=RAW/(file_id+'.txt');data=p.read_bytes();receipt=read(RAW/(file_id+'.receipt.json'))
   url=f'https://raw.githubusercontent.com/cran/{"EValue" if key=="evalue" else key}/{commit["sha"]}/{path}'
   blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   assert blob==entries[path]['sha'] and len(data)==entries[path]['size']
   assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==core.sha(p)
   spans,claim=FINDINGS[key][path];lines=data.decode().splitlines()
   assert all(1<=a<=b<=len(lines) for a,b in spans),(path,len(lines),spans)
   records.append(dict(source_identity=url,upstream_path=path,git_blob_sha1=blob,version_date=commit['commit']['committer']['date'],local_copy=ref(p,str(spans)),receipt=ref(RAW/(file_id+'.receipt.json'),'Acquisition identity'),inspected_anchors=[dict(lines=[a,b],claim=claim) for a,b in spans],supported_claims=[claim],executed=False))
  identities[key]=dict(repository='cran/'+('EValue' if key=='evalue' else key),commit=commit['sha'],tree=tree['sha'],date=commit['commit']['committer']['date'],version=m['version'],source_blobs=len(records),maintenance='Named maintainers and dated CRAN publication; no promised active support or complete release census.',evidence=[ref(RAW/f'v12_sw2_cran_cutoff_{key}.json','Cutoff commit'),ref(RAW/f'exec23_sensitivity_tree_{key}.json','Canonical immutable tree')])
  sources.append(dict(integrated_citation_key='exec23_sensitivity_'+key,kind='software_primary_sources',title=m['title'],author=m['author'],year=2026,source_identity='https://github.com/'+identities[key]['repository']+'/tree/'+commit['sha'],version_date=m['version']+'; '+identities[key]['date'],local_copy=records[0]['local_copy'],records=records,identity=identities[key],license_declaration=ref(RAW/f'v12_sw2_description_{key}.txt',m['license']+' declaration'),license_text=ref(BASE/(m['license']+'.txt'),'Local operating-system copy; GPL2 sections0-2 or GPL3 sections2,4-6; no distribution clearance'),license_custody=ref(BASE/'license-text-custody.json','Origin distinct from package snapshot'),inspected_anchors=[x['inspected_anchors'] for x in records],supported_claims=[x['supported_claims'][0] for x in records],limitations=LIMITS))
 assert [x['identity']['source_blobs'] for x in sources]==[8,5]
 assert exact.calculate()==read(BASE/'exact-results.json')
 a=(RAW/'exec23_sensitivity_sensemakr_1.txt').read_text();b=(RAW/'exec23_sensitivity_sensemakr_3.txt').read_text()
 formals=re.search(r'adjusted_se.numeric\s*=\s*function\(([^)]*)\)',a).group(1)
 assert 'estimate' not in formals and '...' in formals
 assert 'adjusted_se.numeric(estimate = estimate,' in b
 static=dict(native_execution=False,numeric_se_formals=formals,numeric_wrapper_supplies_estimate=True,ellipsis_accepts_extra_argument=True,finding='The estimate argument is accepted by ellipsis; a preliminary argument-mismatch hypothesis is rejected. CI-degree-of-freedom and domain observations remain.',boundary_findings=['Inclusive partial-R-squared guard admits denominator-zero endpoint.','Numeric dof guard admits values at or below one although adjusted variance uses dof-1.','Direct helper and wrapper use different CI degrees of freedom.','RR threshold can divide by zero for zero input/target; stricter proposed profile is explicit.'])
 write(BASE/'static-contract-check.json',static);write(BASE/'identities.json',identities)
 sources.append(dict(integrated_citation_key='exec23_sensitivity_reference',kind='project_derivation_and_exact_reference',title='Exact regression-sensitivity, risk-ratio and banking decision examples',author='Causal banking proposal project',year=2026,version_date='23 October 2026',source_identity='tools/sensitivity_reuse_reference_20261023.py',local_copy=ref(Path(exact.__file__),'Independent rational calculate()'),inspected_anchors=['calculate()'],supported_claims=['Regression coefficient3 shifts to2 with bias1 and adjusted variance5/7; stipulated net5 changes to-5.','Reciprocal ratios9/5 and5/9 have threshold3.','Square-root OR conversion9/5 differs from exact RR405/181 for stipulated baseline1/5 and OR81/25.'],limitations=LIMITS))
 write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',native_execution=False))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Pre-acquisition reviewed plan'),ref(BASE/'static-contract-check.json','Review incorporates discovered delegates and boundaries')],findings=['Inspected canonical tree identities and thirteen blobs, separating technical text from metadata.','Source hazards retained as static findings; no native failure, legal clearance or causal certificate inferred.','Two independent decisions need no common scientific success gate.','No cited new scholarly original is fabricated or substituted.']))
 write(BASE/'omissions-register.json',dict(items=[dict(gap='Complete environments and distribution rights',next_action='Bind complete selected artifacts, resolved dependencies and their original notices for the actual delivery; qualify any chosen worker.'),dict(gap='Native helper/wrapper and endpoint behavior',next_action='Under an approved frozen environment, compare helper/model/numeric dispatch, CI degrees of freedom, invalid endpoints, covariance overrides and full failure envelopes.'),dict(gap='Original methodological derivations beyond inspected software text',next_action='Acquire and inspect authentic Cinelli/Hazlett and VanderWeele/Ding originals before expanding theorem-level coverage; they are candidates, not new citations here.'),dict(gap='General sensitivity and decision quality',next_action='Specify confounding, selection and measurement mechanisms, benchmark plausibility and sampling law; no scalar robustness summary closes unrestricted identification.')],limitations=LIMITS))
 evidence=[ref(BASE/n,'Reviewed source and exact evidence') for n in ['plan.md','plan-review.json','identities.json','source-audit.json','static-contract-check.json','exact-results.json','omissions-register.json']]+[ref(Path(__file__),'Audit implementation'),ref(Path(exact.__file__),'Independent arithmetic')]
 write(BASE/'review.json',dict(status='pass_for_scoped_reference_dispositions',reviewer=REVIEWER,evidence=evidence,findings=['All13 selected blobs authenticate to their cutoff canonical trees.','Covariance, partial-R-squared, benchmark and RR conversion targets remain distinct.','Independent exact examples reproduce; upstream code unexecuted.','Reuse choices retain adverse findings and give no integration permission.'],limitations=LIMITS))
 print(json.dumps(dict(source_blobs=13,audited_records=3,native_execution=False)))

def receipt(key):
 m=META[key];op=m['operation'];state=core.read(ROOT,core.STATE)
 assert state['execution_runtime']['active']['operation']==op
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json';assert not output.exists()
 verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed decision evidence') for n in ['source-audit.json','identities.json','plan-review.json','review.json','exact-results.json','static-contract-check.json','omissions-register.json']]+[ref(Path(__file__),'Decision and criterion construction')]
 alternatives=[dict(route='Direct full-package adoption',decision='defer',reason='Multiple method/conversion families and unresolved environment, rights and native behavior exceed the selected profile.'),dict(route='Selected isolated R worker',decision='conditional future prototype',reason='Retains source semantics if conversion, sampling law, failures and rights are qualified; process separation does not itself clear rights.'),dict(route='Port to Python/Java/C++',decision='reject for current scope',reason='No measured operational advantage justifies reproducing dispatch, uncertainty, approximations and upgrade maintenance.'),dict(route='Independent formula reference',decision='retain for matched oracle only',reason='Transparent arithmetic supports conversion checks without becoming a calibrated inference service.'),dict(route='Substitute for identification or alternative sensitivity families',decision='reject',reason='Targets and assumptions differ; graph ambiguity, trend sensitivity and latent confounding are not interchangeable.')]
 out=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified proposal reference disposition; no adapter approval',identity=read(BASE/'identities.json')[key],license=dict(declaration=m['license'],declaration_evidence=ref(RAW/f'v12_sw2_description_{key}.txt','Package metadata'),original_text=ref(BASE/(m['license']+'.txt'),'Distinct local license-text origin'),transitive_clearance=False),dependencies=dict(declared=m['dependencies'],environment_locked=False),target_and_uncertainty=m['target'],reason=m['reason'],conversion_contract=m['contract'],alternatives=alternatives,costs_to_measure=['Dependency custody and rights review','Data/model conversion and warning capture','Native oracle and sensitivity-grid execution','Scientific benchmark selection and independent review','Upgrade regression and operator maintenance'],owner_obligations=dict(scientific='Target, identification, covariance and plausibility of sensitivity parameters',maintainer='Pinned artifacts, conversion, dispatch tests and complete failure outputs',operator='Actual delivery permissions, custody and resource budget'),revisit_trigger='Complete selected environment and rights evidence plus native helper/model/boundary oracles; changed source, target, sampling law or delivery requires re-review.',integration_allowed=False,capabilities=[],runtime_qualification=False,reviewer=REVIEWER,evidence=evidence,limitations=LIMITS)
 write(output,out)
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Pinned source, version, package license declaration, separately identified license text, dependencies and maintenance limits are bound for this concrete R engine.','Target and uncertainty, conversion/failure boundaries, alternatives, costs, owners and reopening trigger are explicit.','Reference-only disposition grants no integration capability; authored arithmetic and static adverse findings remain distinct from native execution.']
 r.update(outcome='pass',execution='performed',scope=out['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Separate contracted reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=out['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r)
 folder=BASE/key;folder.mkdir();write(folder/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','sensemakr','evalue']);a=p.parse_args();audit() if a.command=='audit' else receipt(a.command)
