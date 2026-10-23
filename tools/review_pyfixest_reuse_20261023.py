#!/usr/bin/env python3
"""Cutoff source authentication and bounded PyFixest reuse disposition."""
from pathlib import Path
import json,hashlib
import run_program_checkpoint_v3 as c
import pyfixest_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=c.base;ROOT=run.core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-23/pyfixest-reuse-v1'
OP='SW.DECISION.inherited_pyfixest';PIN='45d52b6e368cefc7321239921f2547b4e08c8f20'
OUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=['Static inspection of selected pinned source only; no downloaded Python or Rust code, benchmarks or tests executed.',
'PyFixest is a distinct implementation from R fixest; syntax and upstream parity aspirations do not transfer qualification.',
'Cargo version 0.60.0 and dynamic Python build declaration do not authenticate an installed wheel or supported release.',
'Native within/Rust solver internals, full dependency rights, other estimators, randomization/weak-IV procedures and performance remain separately unqualified.',
'Exact synthetic panel calculations and conversion witnesses are not empirical native failures or bank economics.',
'No integration_allowed, native capability, scientific-gap closure, or final proposal acceptance is granted.',
'Mandatory coverage/depth repair rollups, Q1/Q5 and visual acceptance remain open.']

def main():
 state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP
 assert not OUT.exists()
 commit=read(RAW/'exec22_pyiv_pyfixest_cutoff.json')[0];tree=read(RAW/'exec23_pyfixest_canonical_tree.json')
 assert commit['sha']==PIN and tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
 assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 entries={r['path']:r for r in tree['tree']}
 maps=[dict(id=f'exec22_pyiv_pyfixest_source_{i}',source_path=p)for i,p in enumerate(['pyfixest/estimation/models/feiv_.py','LICENSE.md','pyproject.toml'])]
 for n in ['pinned-source-manifest.json','delegate-manifest.json']:
  maps += [r for r in read(BASE/n)['requests'] if r.get('source_path')]
 specs={
 'README.md':('19-38; 128-136','R fixest syntax/default-parity aspiration, stated estimator inventory and hardware-dependent benchmark framing; not observed parity or speed.'),
 'LICENSE.md':('1-21','MIT license declaration and copyright/notice and no-warranty text; transitive artifacts not cleared.'),
 'pyproject.toml':('1-79','Dynamic version; Python>=3.10, Maturin Rust extension, bounded formulaic requirement and minimum numerical/data dependencies; optional torch/numba.'),
 'Cargo.toml':('1-29','Core declares 0.60.0, Rust 2021, PyO3/within and numerical dependencies; release panic abort; not installed-artifact proof.'),
 'pyfixest/estimation/models/feiv_.py':('178-235; 439-480; 484-565','Prior reviewed weighted within/2SLS and first-stage/effective-F diagnostics remain separate from weak-IV confidence-set inversion.'),
 'pyfixest/estimation/api/feols.py':('31-61; parameter documentation','Defaults retain aweights, singleton removal, collinearity tolerance and solver choice; formula output can be Feols/Feiv or multiple fits.'),
 'pyfixest/estimation/internals/demean_.py':('85-116; 169-217','Demeaner success flag checked; failure raises with iteration budget; named cached matrices and preconditioner context matter.'),
 'pyfixest/did/estimation.py':('17-64; 126-206; 340-380','Three event-study branches, id clustering default; DID2S installs GMM covariance and retains second-stage inference degrees while disabling specified post-estimation capabilities.'),
 'pyfixest/did/did2s.py':('157-258; 305-399','Two unique numeric codes converted to bool without explicit zero/one validation; first stage untreated only; absent FE levels raise on NaN prediction; GMM covariance uses both-stage residuals.'),
 'pyfixest/did/saturated_twfe.py':('136-193; 261-341; 386-445; 487-568','Beta warning; saturated helper does not receive xfml; only period/shares accepted despite broader prose; linear-combination inference uses normal cutoff; weights include period zero despite contrary docstring.'),
 'pyfixest/utils/utils.py':('22-76; 130-188','Explicit small-sample switches for k, FE parameter count, G and multiway G rule; defaults and actual inference path must be retained.'),
 'pyfixest/did/did.py':('37-100','Numeric time/cohort accepts formatted calendar integers but relative time uses subtraction; treatment is absorbing from declared cohort, event origin becomes first observed treated period.'),
 'pyfixest/did/twfe.py':('43-85','Inspected TWFE branch forms treatment indicator plus optional covariates and unit/time effects; stored att flag does not create a lead-lag formula here.'),
 'pyfixest/demeaners.py':('21-52; 185-255; 292-370','Backend-specific preconditioner fallback and warnings; MAP/LSMR and torch/within choices have distinct controls and failure boundaries.'),
 'pyfixest/core/demean.py':('18-90; 93-191','Native wrapper dtype conversion and MAP/within delegation; full native solver remains an inspection/replay obligation.')}
 records=[]
 for row in maps:
  p=RAW/(row['id']+'.txt');rp=p.with_suffix('.receipt.json');data=p.read_bytes();receipt=read(rp);up=row['source_path']
  url=f'https://raw.githubusercontent.com/py-econometrics/pyfixest/{PIN}/{up}'
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==run.core.sha(p)
  assert blob==entries[up]['sha'] and len(data)==entries[up]['size']
  span,claim=specs[up];anchor=span+'; '+claim
  records.append(dict(source_identity=url,version_date=commit['commit']['committer']['date']+'; '+PIN,upstream_path=up,
   local_copy=ref(p,anchor),receipt=ref(rp,'Bounded public-source receipt'),git_blob_sha1=blob,inspected_anchors=[anchor],supported_claims=[claim],executed=False))
 assert len(records)==15
 identity=dict(repository='py-econometrics/pyfixest',selected_commit=PIN,commit_date=commit['commit']['committer']['date'],tree_sha=tree['sha'],declared_core_version='0.60.0',
  Python_version_declaration='dynamic via Maturin',source_blobs=15,cutoff='2026-10-07',
  alias_boundary='Distinct implementation from R fixest; Feols/Feiv/DID2S and saturated event study are method surfaces, not interchangeable qualification.',
  maintenance='Cutoff commit fixes formulaic log handling; beta declarations and changing internal interfaces demand regression ownership; no support horizon established.',
  evidence=[ref(RAW/'exec22_pyiv_pyfixest_cutoff.json','Cutoff-selected commit'),ref(RAW/'exec23_pyfixest_canonical_tree.json','Actual canonical tree')])
 write(BASE/'identity-review.json',identity);write(BASE/'exact-results.json',exact.calculate())
 prior=ROOT/'docs/program/execution/2026-10-22/python-iv-kernels-v1/source-audit.json';verify_bindings(read(prior))
 fixest=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_fixest/decision.json';verify_bindings(read(fixest))
 write(BASE/'prior-evidence.json',dict(IV_review=ref(prior,'Prior weighted IV delegates and limitations'),R_fixest=ref(fixest,'Separate implementation decision'),transfer_of_native_qualification=False))
 source=dict(integrated_citation_key='exec23_pyfixest_reuse_source',kind='software_primary_sources',title='PyFixest pinned panel, event-time, aggregation and numerical contracts',author='PyFixest contributors',year=2026,
  source_identity='https://github.com/py-econometrics/pyfixest/tree/'+PIN,version_date=identity['commit_date']+'; '+PIN,local_copy=records[3]['local_copy'],records=records,
  inspected_anchors=[v[0]for v in specs.values()],supported_claims=[v[1]for v in specs.values()],limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_pyfixest_reference',kind='project_derivation_and_exact_reference',title='Panel projection, cohort weighting and event-clock reference examples',author='Causal banking proposal project',year=2026,
  source_identity='tools/pyfixest_contract_reference_20261023.py',version_date='2026-10-23',local_copy=ref(ROOT/'tools/pyfixest_contract_reference_20261023.py','calculate() independent rational panel algebra'),
  inspected_anchors=['calculate()'],supported_claims=['Positive treated-cell effects average 4 while the stated TWFE projection is -7/2; stipulated cost 2 yields net 2 versus -11/2.',
   'Cohort weights 1/4 and 3/4 give aggregate 1 and covariance 91/16 versus diagonal-only 85/16.',
   'Calendar-coded subtraction, nonzero boolean conversion and first-observed event origin alter specified inputs.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 contract=dict(status='proposed_not_implemented',selected_path='Pinned method-specific Python worker with native numerical artifacts, conditionally after oracle replay and rights/environment review.',
 scientific_requirements=['Declare intervention, control eligibility, parallel trends/anticipation assumptions, support and outcome clock; fixed effects are not identification.',
 'Specify dynamic/cohort target, weights, treatment timing, population and uncertainty independently of formula.'],
 conversion=['Use consecutive integer periods with explicit mapping from real calendar; preserve declared and first-observed adoption dates.',
 'Enforce unique unit-period records, fixed cohort per unit, known never-treated sentinel, missing-period policy and absorbing-treatment assumption or refuse.',
 'Validate DID2S treatment codes exactly before boolean conversion; retain first-stage sample/FE coverage and all row removals.',
 'Preserve formula expansion, covariate use, coefficient order, singleton/rank removals, weight type, solver, backend, tolerance, seed and warnings.',
 'Expose actual covariance, cluster counts, degrees of freedom, small-sample switches and pointwise versus simultaneous inference.',
 'Only offer operations allowed by the chosen branch; reject unsupported aggregation or downstream post-estimation.'],
 failure=['Refuse unseen first-stage FE levels, rank loss and nonfinite covariance; preserve full failure denominator.',
 'Expose backend preconditioner fallback and nonconvergence; budget worker termination for native failures.',
 'Replay date gaps, nonzero treatment codes, unused covariate requests, att flag, period-zero weights and normal aggregation cutoffs.',
 'Compare against independent exact projection and aggregation oracles, separately from declared R-default similarity.'],
 oracle=ref(BASE/'exact-results.json','Authored oracle targets, not native replay'),integration_allowed=False)
 write(BASE/'conversion-contract.json',contract)
 omissions=[dict(gap='Native computation and regression parity',next_action='Pin actual wheel/native/within environment; replay selected oracle cases and registered Python/R designs without downloaded-code execution in the current source-review scope.'),
 dict(gap='Complete estimator and inference scope',next_action='Inspect selected model-matrix/covariance/native backends and remaining methods before admitting a specific operation.'),
 dict(gap='Scientific target and support',next_action='State parallel-trend/anticipation/control laws, sample provenance, cohort weights and justified uncertainty; retain negative results.'),
 dict(gap='Distribution and costs',next_action='Review dependency artifacts/notices and matched successful/failed workflow time, maintenance and review costs before adoption.')]
 write(BASE/'omissions-register.json',dict(items=omissions,limits=LIMITS))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Prior plan')],
 findings=['Inspect common DID timing, concrete TWFE formula, two-stage fit/covariance, saturated weights and native wrapper before general claims.',
 'Distinguish docstrings from actual guards and code; static examples require native replay.',
 'Retain earlier IV and separate R fixest evidence without transferring admission.']))
 evidence=[ref(BASE/n,'Reviewed PyFixest evidence')for n in ['plan.md','plan-review.json','identity-review.json','source-audit.json','prior-evidence.json','exact-results.json','conversion-contract.json','omissions-register.json']]
 evidence += [ref(Path(__file__),'Audit implementation'),ref(ROOT/'tools/pyfixest_contract_reference_20261023.py','Independent reference')]
 decision=dict(operation_id=OP,decision='reference',status='pass',decision_scope='Selected fixed-effect/IV/event-study proposal reference with conditional Python worker route.',identity=identity,
 license=dict(declaration='MIT',evidence=next(x['local_copy']for x in records if x['upstream_path']=='LICENSE.md'),transitive_clearance=False),
 dependencies=dict(build=['Maturin','PyO3','Rust within core'],runtime=['formulaic>=1.2.0,<1.3','numpy','pandas','scipy','narwhals','joblib','reporting dependencies'],optional=['numba','torch'],locked_artifact_environment=False),
 target_and_uncertainty='Weighted fixed-effect/IV projections or specified DID/event-study functionals; cluster/GMM/normal aggregation targets and degrees differ; not universal ATT or weak-IV sets.',
 reason='Concrete source contracts make a useful Python comparator, while timing/coding/aggregation and native-backend issues require narrowly qualified profiles before adoption.',
 alternatives=[dict(route='Direct whole-package adoption',disposition='defer',reason='Method-specific support, native environment and controls not qualified as one capability.'),
 dict(route='Selected Python worker',disposition='conditional prototype',reason='Preserves upstream semantics and adds explicit clocks, refusals, diagnostics and provenance.'),
 dict(route='R fixest',disposition='separate comparator',reason='Its reviewed source and wider/different model interfaces do not prove PyFixest parity; compare matched targets.'),
 dict(route='Port to another language',disposition='reject for current proposal',reason='Existing native acceleration and Python interfaces need evaluation before paying duplicate numerical maintenance cost.'),
 dict(route='Cohort-time or two-stage alternative',disposition='question-dependent',reason='Choose identified effect target and control law before algorithm; a TWFE coefficient need not equal ATT.')],
 costs_to_measure=['Install/native build and upgrade','Demeaning/fit/covariance including failures','Dataset/formula conversion','Cluster and aggregation computation','Scientific review and operational recovery'],
 owner_obligations=dict(scientific='Causal target, adoption clock, support, uncertainty and control law',maintainer='Native artifacts, conversions, oracle cases, diagnostics and upgrade regressions',operator='Dependency notices, budgets and failure/custody accounting'),
 revisit_trigger='Reopen on passing permissible pinned-profile oracle and public/synthetic matched trials or changes to clock, sampling law, source or platform.',
 contract=ref(BASE/'conversion-contract.json','Proposed conversion/failure contract'),integration_allowed=False,capabilities=[],runtime_qualification=False,original_gap_qualification=False,reviewer=REVIEWER,evidence=evidence,limitations=LIMITS)
 write(OUT,decision)
 findings=['Fifteen source blobs bind commit/tree, version declarations, MIT text, dependencies, maintenance limits and distinct R implementation identity.',
 'Targets, uncertainty, alternatives, cost/owner obligations and reopening criteria have exact authored examples and source-specific limits.',
 'Reference disposition grants no integration or native capability; conversion/failure contract remains prospective.']
 write(BASE/'review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,findings=findings,evidence=evidence,reviewed_output=ref(OUT,'Bounded decision'),limitations=LIMITS))
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);r=run.ledger.receipt_template(node)
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,limitations=LIMITS,original_gap_qualification=False,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],outputs=[ref(OUT,'Contracted decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')])for i,f in enumerate(findings)])
 verify_bindings(r);run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=OP,sources=len(records),decision='reference',integration_allowed=False)))
if __name__=='__main__':main()
