#!/usr/bin/env python3
"""Authenticate recovered NOTEARS originals and prepare its reviewed disposition."""
from pathlib import Path
import hashlib,json
import run_program_checkpoint_v3 as controller
import notears_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=controller.base; ROOT=run.core.ROOT; RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-23/notears-reuse-v1'
OP='SW.DECISION.inherited_notears'; PIN='4a9ab19fe502e392503da331773c5223d82d3666'
OUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=['Thirteen selected original blobs are statically inspected; no downloaded module, CLI, demo or test executed.',
'Cutoff-filtered default-branch commit and setup version 3.0 do not establish a release artifact, support commitment or native qualification.',
'Root Apache-2.0 text and wrapper attribution are preserved; full distribution and transitive dependency rights remain unreviewed.',
'Authored rational and functional examples are proposal references, not observed algorithm failures, empirical accuracy or bank returns.',
'No latent, temporal, intervention-identification, graph confidence, effect interval or bank-deployment capability is granted.',
'DAGrad is an upstream README lead only; this decision does not review its code or claim superiority.',
'Complete software census, Q1/Q5, rendered visual acceptance and final proposal acceptance remain open.']

def main():
 state=run.core.read(ROOT,run.core.STATE)
 assert state['execution_runtime']['active']['operation']==OP
 assert not OUT.exists()
 commit=read(RAW/'exec23_notears_commits.json')[0]; tree=read(RAW/'exec23_notears_pinned_tree.json')
 assert commit['sha']==PIN and commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 assert tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
 entries={r['path']:r for r in tree['tree']}; records=[]
 maps=[]
 for mf in ['pinned-source-manifest.json','delegate-manifest.json']:
  maps.extend(r for r in read(BASE/mf)['requests'] if r.get('source_path'))
 assert len(maps)==13
 findings={
 'README.md':'Requirements and contents; update points to DAGrad without proving support or performance; original implementation identity.',
 'LICENSE':'Apache 2.0 sections 2-4 and 7-9: grant, notices, modifications, warranty and liability text.',
 'notears/linear.py':'notears_linear: X@W source-row convention, three losses, exponential trace constraint, centering by new array, sol.x without success check, stopping and strict-less-than removal; DAG assertion only in demo.',
 'notears/nonlinear.py':'NotearsMLP/NotearsSobolev return first-layer norms; dual_ascent_step mutates supplied model; no optimizer result surfaced; CPU NumPy and PyTorch bridge.',
 'notears/utils.py':'Simulation is stipulated data; set_random_seed sets Python/NumPy only; graph-metric CPDAG encoding gives undirected hits favorable credit and is not effect calibration.',
 'setup.py':'Declares notears 3.0, alpha classifier, Apache 2.0, two CLI scripts; numpy/scipy/python-igraph unpinned; torch omitted from required dependencies.',
 'notears/lbfgsb_scipy.py':'SciPy wrapper attributes Arthur Mensch gist; casts through default torch dtype, distributes sol.x, discards optimizer status; native device behavior untested.',
 'notears/locally_connected.py':'Initialization uses torch random uniform; local layers preserve output mapping; extra_repr names attributes different from constructor assignments (static observation).',
 'notears/trace_expm.py':'SciPy expm through input.detach().numpy(); transpose derivative; standalone gradcheck exists but not run.',
 'bin/notears_linear':'Loads numeric CSV, runs loss/penalty defaults, asserts DAG, saves matrix; labels and diagnostics are not serialized.',
 'bin/notears_nonlinear':'Sets double dtype, creates randomly initialized MLP without explicit seed, asserts DAG then saves only norm matrix.',
 'Dockerfile':'Ubuntu 18.04 with floating apt/pip installs; no locked environment or torch installation in this file.',
 'experiments/expt_twovars.py':'Legacy notears.notears_linear_l1 import/call differs from selected tree API; 1000-graph loop is experimental code, not evidence of execution.'}
 extracts=[]
 for row in maps:
  path=RAW/(row['id']+'.txt'); data=path.read_bytes(); receipt_path=path.with_suffix('.receipt.json'); receipt=read(receipt_path)
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(); upstream=row['source_path']
  assert blob==entries[upstream]['sha'] and len(data)==entries[upstream]['size']
  assert receipt['status']=='saved' and receipt['url']==row['url'] and receipt['sha256']==run.core.sha(path)
  anchor=f'lines 1-{len(data.decode().splitlines())}; '+findings[upstream]
  records.append(dict(source_identity=row['url'],version_date=commit['commit']['committer']['date']+'; '+PIN,
   local_copy=ref(path,anchor),receipt=ref(receipt_path,'Successful bounded acquisition'),git_blob_sha1=blob,
   inspected_anchors=[anchor],supported_claims=[findings[upstream]],executed=False))
  extracts.append(dict(upstream=upstream,local_copy=ref(path,anchor)))
 for name in ['exec23_notears_commits','exec23_notears_pinned_tree']:
  assert read(RAW/(name+'.receipt.json'))['sha256']==run.core.sha(RAW/(name+'.json'))
 identity=dict(repository='xunzheng/notears',selected_commit=PIN,commit_date=commit['commit']['committer']['date'],
  tree_sha=tree['sha'],source_blobs=13,declared_version='3.0',cutoff='2026-10-07',
  version_limit='Setup declaration only; no fetched release or supported build.',
  maintenance='Selected commit message is update README; redirect to DAGrad is a lead, not deprecation or comparative evidence.',
  canonical_boundary='Original xunzheng implementation is distinct from gCastle, DAGMA, CausalNex and other ports.',
  evidence=[ref(RAW/(n+'.json'),'Pinned repository identity') for n in ['exec23_notears_commits','exec23_notears_pinned_tree']])
 write(BASE/'identity-review.json',identity)
 write(BASE/'inspected-extracts.json',dict(originals=extracts,native_execution=False))
 write(BASE/'exact-results.json',exact.calculate())
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_proposal_decision',reviewer=REVIEWER,
  evidence=[ref(BASE/'plan.md','Reviewed scope')],findings=['Inspect CLI and nonlinear delegates before dependency claims.',
  'Compare actual threshold operators and exponential/polynomial constraints; avoid treating algorithms as aliases.',
  'Keep static source observations, exact authored examples and native behavior distinct.',
  'Retain predecessor artifacts and source-specific omissions; no blanket integration approval.']))
 contract=dict(status='proposed_not_implemented',selected_path='Pinned original linear Python worker first; nonlinear requires separate fitted-function contract.',
  scientific_requirements=['Specify independent units, measured variable meaning and units, causal sufficiency and identifiable SEM restrictions.',
   'Do not certify causal directions from acyclicity or optimizer success alone.'],
  conversion=['Own a finite floating copy with ordered variable IDs and recorded centering/scales.',
   'Validate data shape, sample count, loss-specific domains, penalties, threshold, h_tol, positive iteration budget and rho_max>1.',
   'Keep source-row/target-column matrix, raw weights and exact removal rule abs(w)<threshold.',
   'Nonlinear norms are unsigned connectivity measures; retain structural functions, scales and noise law for separate effect queries.',
   'Never export a norm as a signed coefficient or use it as an intervention derivative.'],
  failure=['Expose solver termination/status, residual and elapsed budget rather than infer convergence from a returned matrix.',
   'Check final support acyclicity separately; reject rather than silently delete cycles.',
   'Handle nonfinite/overflow/shape/dtype/device errors explicitly; isolate CPU bridge and mutable model ownership.',
   'Seed each relevant random generator, bind dependency versions and preserve input/output hashes.',
   'CLI/MCP must use the same typed contract; assertion-only native CLI and CSV graph alone are insufficient.'],
  trial=['Replay threshold equality, unit changes and cyclic residual examples with independent reference targets.',
   'Use the registered language-specific public/synthetic designs before any empirical qualification claim.',
   'Measure installation, optimization, serialization, graph checks, retries and upgrade effort on matched tasks.'],
  integration_allowed=False)
 write(BASE/'conversion-contract.json',contract)
 omissions=[dict(gap='Native execution and numerical conformance',next_action='Resolve environment and use prospective public/synthetic protocol; no bank data prerequisite.'),
  dict(gap='Distribution and dependency custody',next_action='Pin actual artifacts, transitive dependencies, license notices and attributed wrapper origin before shipping.'),
  dict(gap='Nonlinear output semantics',next_action='Preserve fitted functions and noise law; separately establish intervention identification and diagnostics.'),
  dict(gap='DAGrad lead',next_action='Separate cutoff pin, technical inspection and reuse disposition; do not transfer upstream marketing to this review.'),
  dict(gap='Legacy experiment compatibility',next_action='Resolve legacy import/API against selected original revision before attempting experiment reproduction.'),
  dict(gap='Statistical/bank utility',next_action='Match sample-law and identifiability assumptions, assess uncertainty and public prototype merit; later obtain authentic bank truth and costs.')]
 write(BASE/'omissions-register.json',dict(items=omissions,limits=LIMITS))
 source=dict(integrated_citation_key='exec23_notears_source',kind='software_primary_sources',
  title='Original NOTEARS pinned source, numerical and interface contracts',author='Xun Zheng and NOTEARS contributors',year=2026,
  source_identity='https://github.com/xunzheng/notears/tree/'+PIN,version_date=identity['commit_date']+'; '+PIN,
  local_copy=records[0]['local_copy'],records=records,inspected_anchors=list(findings.values()),supported_claims=list(findings.values()),limitations=LIMITS)
 reference=dict(integrated_citation_key='exec23_notears_reference',kind='project_derivation_and_exact_reference',
  title='NOTEARS threshold, matrix, cycle and nonlinear intervention references',author='Causal banking proposal project',year=2026,
  source_identity='tools/notears_contract_reference_20261023.py',version_date='2026-10-23',
  local_copy=ref(ROOT/'tools/notears_contract_reference_20261023.py','calculate() independent rational identities'),
  inspected_anchors=['calculate(); rational series bounds, path transformation and assumed local derivatives'],
  supported_claims=['Exact threshold equality gives retained/deleted supports; assumed margins 10 and -20 USD.',
   'Two-cycle residual can lie below tolerance; exponential and polynomial residuals differ on the same matrix.',
   'Units transform path coefficients; equal nonnegative first-layer norms allow opposite signed derivatives.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,reference],cutoff='2026-10-07',native_execution=False))
 gcastle=ROOT/'docs/program/execution/2026-10-20/gcastle-reuse-v1/source-audit.json'
 dagma=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_dagma/decision.json'
 verify_bindings(read(gcastle)); verify_bindings(read(dagma))
 evidence=[ref(BASE/n,'Reviewed NOTEARS evidence') for n in ['plan.md','plan-review.json','identity-review.json','inspected-extracts.json','source-audit.json','exact-results.json','conversion-contract.json','omissions-register.json','recovered-acquisition.json']]
 evidence.extend([ref(gcastle,'Previously authenticated comparator'),ref(dagma,'Distinct previous DAGMA decision'),ref(Path(__file__),'Reviewed source-authentication and receipt construction')])
 decision=dict(operation_id=OP,decision='reference',status='pass',decision_scope='Original NOTEARS method-specific proposal reference choice with a prospective isolated-worker route.',
  identity=identity,license=dict(declaration='Apache License 2.0',evidence=records[1]['local_copy'],transitive_clearance=False),
  dependencies=dict(core=['numpy','scipy'],utilities=['python-igraph'],nonlinear=['torch','SciPy/PyTorch bridge'],
   conditional_simulation=['scikit-learn GaussianProcessRegressor'],setup_versions_locked=False),
  target_and_uncertainty='Weighted or norm-valued candidate DAG under selected model restrictions; neither is an effect confidence region.',
  reason='The original implementation provides a transparent separately pinned comparator. Its numerical/API differences require explicit contracts before adoption; no measured advantage justifies a port.',
  alternatives=[dict(route='Pinned original linear worker',disposition='conditional future prototype',reason='Preserves source semantics while wrapper validates diagnostics, units, topology and errors.'),
   dict(route='Whole-package direct adoption',disposition='defer',reason='Unpinned environment, hidden optimizer status and distinct nonlinear meaning remain unresolved.'),
   dict(route='Port into another language/core',disposition='reject for current proposal',reason='No demonstrated platform/cost benefit offsets numerical and maintenance divergence.'),
   dict(route='gCastle or DAGMA',disposition='separate comparators',reason='Threshold/constraint/output contracts differ; shared family naming does not transfer evidence.'),
   dict(route='Infer signed nonlinear effects from adjacency',disposition='reject',reason='Identical norms can hide opposite effect signs.'),
   dict(route='PC/FCI or temporal method',disposition='question-dependent alternative',reason='Different sample-law/latent/equivalence-class requirements need their own justification.')],
  costs_to_measure=['Build/dependency maintenance','Optimization and complete failures','Serialization and custody','Diagnostics and topology','Upgrade regression and human scientific review'],
  owner_obligations=dict(scientific='Model restrictions, intervention target and sampling law',maintainer='Environment, conversions, diagnostics and failure denominator',operator='Distribution notices, custody and future deployment constraints'),
  revisit_trigger='A complete permissible environment, observable diagnostics and matched prospective public/native results justify reconsidering integration; reopen on source, model or platform change.',
  contract=ref(BASE/'conversion-contract.json','Proposed typed conversion and failure semantics'),
  integration_allowed=False,capabilities=[],runtime_qualification=False,original_gap_qualification=False,
  reviewer=REVIEWER,evidence=evidence,limitations=LIMITS)
 write(OUT,decision)
 findings_review=['Thirteen original blobs match the selected tree; version, license, delegates and maintenance limits are explicit.',
 'Method-specific targets, threshold/constraint differences, independent references, alternatives, costs, owners and reopening triggers are documented.',
 'Reference disposition grants no native/integration capability; prospective contract does not claim implemented behavior.']
 write(BASE/'review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,findings=findings_review,evidence=evidence,reviewed_output=ref(OUT,'Original NOTEARS disposition'),limitations=LIMITS))
 graph,merged,_=run.combined(ROOT,state); node=run.ledger.operation(graph,OP)
 receipt=run.ledger.receipt_template(node)
 receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,limitations=LIMITS,
  original_gap_qualification=False,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],outputs=[ref(OUT,'Contracted decision')],
  criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Individual author review')]) for i,f in enumerate(findings_review)])
 verify_bindings(receipt); run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']))
 write(BASE/'operation-receipt.json',receipt)
 print(json.dumps(dict(operation=OP,source_blobs=len(records),decision='reference',native_execution=False,integration_allowed=False)))

if __name__=='__main__':main()
