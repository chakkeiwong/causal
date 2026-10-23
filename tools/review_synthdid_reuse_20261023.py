#!/usr/bin/env python3
"""Authenticate the selected R synthdid sources and record a bounded reuse review."""
from pathlib import Path
import hashlib,json
import run_program_checkpoint_v3 as c
import synthdid_contract_reference_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=c.base;ROOT=run.core.ROOT;RAW=ROOT/'docs/literature/raw'
BASE=ROOT/'docs/program/execution/2026-10-23/synthdid-reuse-v1'
OP='SW.DECISION.inherited_synthdid';PIN='70c1ce3eac58e28c30b67435ca377bb48baa9b8a'
OUT=ROOT/f'docs/program/comprehensive-v14/work/{OP}/decision.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=['Static inspection of selected pinned sources; downloaded R code and upstream tests were not executed.',
 'Original synthdid simultaneous-adoption block design is distinct from other staggered-adoption implementations.',
 'Fixed-weight examples are independent authored calculations, not fitted native outputs, calibration or bank returns.',
 'Dependency rights, actual installed artifact, numerical and inference qualification remain open.',
 'No integration capability, universal scientific-gap closure or final proposal acceptance is granted.',
 'Q1/Q5, mandatory depth/coverage rollups and fresh visual acceptance remain open.']

def main():
 state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP
 assert not OUT.exists()
 commit=read(RAW/'exec23_synthdid_cutoff.json')[0];tree=read(RAW/'exec23_synthdid_canonical_tree.json')
 assert commit['sha']==PIN and tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
 assert commit['commit']['committer']['date']<'2026-10-07T15:59:59Z'
 entries={x['path']:x for x in tree['tree']}
 maps=[r for n in ['canonical-manifest.json','pinned-source-manifest.json'] for r in read(BASE/n)['requests'] if r.get('source_path')]
 specs={
 'README.md':('5-15; 36-42','Average treated-block target, simultaneous adoption, beta warning and illustrative normal interval; no assurance from illustration.'),
 'DESCRIPTION':('1-26','Version 0.0.9; R>=3.4; imports mvtnorm; optional testthat/ggplot2/CVXR; alternative GPL>=2 or BSD_3_clause with LICENSE declaration.'),
 'LICENSE':('1-14','Stanford 2019 three-clause BSD text, redistribution notice and endorsement conditions, and warranty exclusion; no transitive clearance.'),
 'R/synthdid.R':('38-107; 119-137; 145-170','Bilinear residual contrast and fixed/update weights; only supplied lengths guarded, no simplex guard; noise-scaled penalty and sparsification; covariate residualization; saved opts omit sparsify and pre-sparsify iteration count; SC/DID alternatives differ.'),
 'R/solver.R':('11-51; 57-102','Frank-Wolfe exact line search, simplex initialization, progress/iteration stopping; covariate gradient step 1/t and absolute objective-change stop; returns values without separate convergence certificate.'),
 'R/vcov.R':('25-36; 46-86; 107-129','Bootstrap/jackknife/placebo variance choices; one-treated NA; fixed-weight jackknife rejects one nonzero donor; placebo requires more controls than treated; bootstrap retries NA without attempt limit; stored opts drive refits.'),
 'R/utils.R':('20-104','Balanced complete unique unit-time panel, binary treatment and simultaneous adoption guards; factors/dates converted to strings; covariates not retained by panel converter; treated.last false leaves row-order obligation.'),
 'R/reference-solver.R':('1-34','CVXR/ECOS simplex reference with intercept and ridge; separate weighted contrast; evidence is inspected source, not executed parity.'),
 'R/summary.R':('34-42','Summary defaults to bootstrap, fast summary to jackknife; effective donor/time counts are inverse squared weight sums.'),
 'R/format.R':('6-13','Formatting invokes fast summary and normal 1.96 multiplier; displayed uncertainty can select jackknife rather than the separately requested variance method.'),
 'tests/testthat/test_synthdid.R':('1-13; 27-36; 39-107; 109-170','Smoke workflow, covariate example and algebraic shift/scaling checks; no observed test pass or general calibration inferred.'),
 'tests/testthat/test_against_reference.R':('1-26','California example comparison to CVXR reference with tolerance .03 and different iteration settings; not general numerical qualification.'),
 'vignettes/synthdid.Rmd':('25-37','Upstream single-treated example explicitly warns about placebo uncertainty and explains default NA; demonstration is not acceptance.')
 }
 records=[]
 for row in maps:
  p=RAW/(row['id']+'.txt');rp=p.with_suffix('.receipt.json');b=p.read_bytes();receipt=read(rp);up=row['source_path']
  url=f'https://raw.githubusercontent.com/synth-inference/synthdid/{PIN}/{up}';blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==run.core.sha(p)
  assert entries[up]['sha']==blob and entries[up]['size']==len(b)
  span,claim=specs[up];anchor=span+'; '+claim
  records.append(dict(source_identity=url,version_date=commit['commit']['committer']['date']+'; '+PIN,upstream_path=up,
   local_copy=ref(p,anchor),receipt=ref(rp,'Bounded public-source receipt'),git_blob_sha1=blob,inspected_anchors=[anchor],supported_claims=[claim],executed=False))
 assert len(records)==13
 identity=dict(repository='synth-inference/synthdid',selected_commit=PIN,commit_date=commit['commit']['committer']['date'],tree_sha=tree['sha'],declared_version='0.0.9',source_blobs=13,cutoff='2026-10-07',
  alias_boundary='Original R package for a simultaneous-adoption treated block; no transfer from staggered SDID packages.',
  maintenance='Cutoff selection is January 2024 and README declares beta; this does not establish abandonment or a support horizon.',
  evidence=[ref(RAW/'exec23_synthdid_cutoff.json','Cutoff-selected commit'),ref(RAW/'exec23_synthdid_canonical_tree.json','Canonical tree')])
 write(BASE/'identity-review.json',identity);write(BASE/'exact-results.json',exact.calculate())
 prior=ROOT/'docs/program/execution/2026-10-23/tigramite-reader-v1/reader/source-audit.json'
 paper=next(s for s in read(prior)['sources'] if s['integrated_citation_key']=='synthdid2021')
 assert run.core.sha(ROOT/paper['local_path'])==paper['sha256']
 write(BASE/'prior-evidence.json',dict(paper=paper,evidence=[ref(prior,'Existing genuine paper audit, restricted to inspected block-design anchor')],theorem_scope_extended=False))
 source=dict(integrated_citation_key='exec23_synthdid_reuse_source',kind='software_primary_sources',title='Original R synthdid pinned panel, optimization and inference contracts',author='synthdid contributors',year=2024,
  source_identity='https://github.com/synth-inference/synthdid/tree/'+PIN,version_date=identity['commit_date']+'; '+PIN,local_copy=records[3]['local_copy'],records=records,
  inspected_anchors=[v[0] for v in specs.values()],supported_claims=[v[1] for v in specs.values()],limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_synthdid_reference',kind='project_derivation_and_exact_reference',title='Fixed-weight block contrast, shift invariance and bootstrap composition examples',author='Causal banking proposal project',year=2026,
  source_identity='tools/synthdid_contract_reference_20261023.py',version_date='2026-10-23',local_copy=ref(Path(exact.__file__),'calculate() independent rational examples'),
  inspected_anchors=['calculate()'],supported_claims=['Supplied unit/time weights yield 11/2 dollars and stipulated net 3/2.',
   'Weights summing to 3/4 allow a common 100-dollar post shock to change contrast by 25 dollars; valid unit-sum weights cancel it.',
   'Two controls and two treated units give homogeneous-bootstrap composition probability 1/8 and 8/7 expected draws per admissible composition.',
   'Weights 3/4 and 1/4 give effective donor count 8/5.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 contract=dict(status='proposed_not_implemented',integration_allowed=False,
  selected_path='Pinned R worker for a narrowly declared balanced simultaneous-adoption profile after permissible native replay.',
  scientific_requirements=['Declare potential-outcome target, no-anticipation/interference and justified counterfactual trend/factor/noise restrictions; fitted weights alone do not identify effects.',
   'Use a complete block and declare treated-unit/post-period equal weighting; a branch-period target is not automatically a customer-weighted target.',
   'Justify each inference method under actual donor/treatment and dependence law; placebo variability is not a randomization p-value by itself.'],
  conversion=['Enforce finite numeric outcomes/covariates, nonempty control/treated/pre/post cells, sufficient pre-period differences and explicit zero-noise handling.',
   'Preserve unique unit-time key, actual calendar ordering, complete observed grid and treatment timing; reject arbitrary imputation or staggered adoption under this profile.',
   'Require controls first and treated last even if treated.last false; align covariate array separately with retained unit/time mappings.',
   'Validate supplied omega/lambda lengths, finiteness, nonnegativity and unit sum for SDID; keep SC zero-lambda convention in a distinct profile.',
   'Preserve intercepts, penalties, noise level, update flags, sparsify function identity, both iteration limits and objective trajectory.',
   'Keep original fit options for resampling rather than relying on incomplete opts; record seed, attempted/rejected/accepted draws, deadline and NA/errors.',
   'Return requested variance method, full weights and diagnostics explicitly; do not parse formatted normal intervals as canonical inference.'],
  failure=['Preserve one-treated bootstrap/jackknife NA and one-effective-donor jackknife NA; never turn them into zero uncertainty.',
   'Enforce placebo donor-count and scientific-exchangeability requirements, and reject unsupported covariance claims.',
   'Distinguish small objective progress from certified numerical error; check finite solutions, budget exhaustion and independent optimum where feasible.',
   'Bound resampling attempts and worker time; repeated NA cannot be silently discarded as success.'],
  oracle=ref(BASE/'exact-results.json','Fixed-weight examples; native replay outstanding'))
 write(BASE/'conversion-contract.json',contract)
 omissions=[dict(gap='Native numerical and resampling fidelity',next_action='Use an authorized installed pinned R environment to replay fixed weights, option reconstruction, zero noise, dimensions, row ordering, failed draws and independent objective checks.'),
  dict(gap='Scientific inference and extrapolation',next_action='Inspect appropriate theorem assumptions and qualify a declared public/synthetic law; retain single-treated and common-shock limitations.'),
  dict(gap='Other adoption patterns',next_action='Review a separately identified staggered procedure or justified cohort decomposition; do not relabel this package as staggered SDID.'),
  dict(gap='Distribution, lifecycle and cost',next_action='Review actual artifacts and dependency terms; measure preparation, tuning, inference, rejected requests and maintenance before adoption.')]
 write(BASE/'omissions-register.json',dict(items=omissions,limits=LIMITS))
 write(BASE/'plan-review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,evidence=[ref(BASE/'plan.md','Prior plan')],findings=['Canonical tree and actual estimator/solver/panel/inference delegates inspected before disposition.',
  'Separate direct matrix validation from panel helper, stored opts from actual fit controls, and illustration from accepted inference.',
  'Examples use supplied weights and exact independent algebra; no native or theorem qualification borrowed.']))
 evidence=[ref(BASE/n,'Reviewed synthdid evidence') for n in ['plan.md','plan-review.json','identity-review.json','source-audit.json','prior-evidence.json','exact-results.json','conversion-contract.json','omissions-register.json']]
 evidence += [ref(Path(__file__),'Audit implementation'),ref(Path(exact.__file__),'Independent reference')]
 decision=dict(operation_id=OP,decision='reference',status='pass',decision_scope='Original R simultaneous-adoption SDID proposal reference with conditional worker route.',identity=identity,
  license=dict(declaration='GPL (>=2) OR BSD_3_clause + LICENSE',evidence=next(x['local_copy'] for x in records if x['upstream_path']=='LICENSE'),transitive_clearance=False),
  dependencies=dict(runtime=['R>=3.4','mvtnorm'],optional=['testthat','ggplot2','CVXR/ECOS for reference comparison'],locked_artifact_environment=False),
  target_and_uncertainty='Equal treated-unit/post-period block effect under justified model; separate bootstrap, fixed-weight jackknife and placebo assumptions, diagnostics and refusals.',
  reason='Transparent original estimator and independent objective provide a useful comparator; guards, option reconstruction, numerical certification and inference require a restricted qualified profile.',
  alternatives=[dict(route='Whole-package adoption',disposition='defer',reason='Beta interface and unqualified numerical/inference and lifecycle contracts.'),
   dict(route='Pinned R worker',disposition='conditional prototype',reason='Preserves original estimator while making panel/weight/inference and failure contracts explicit.'),
   dict(route='Port into Python or C++',disposition='reject for current proposal',reason='Maintain original as reference and measure a concrete bottleneck before duplicating optimization and inference.'),
   dict(route='Cohort-time DID or separate staggered SDID',disposition='question-dependent',reason='Different adoption design and assumptions require separate source and target reviews.'),
   dict(route='SC or ordinary DID',disposition='separate comparator',reason='Provided wrappers deliberately change weights/intercepts and inferential validity; names are not interchangeable.')],
  costs_to_measure=['Panel cleaning and eligible-row loss','Weight fitting and tuning','All resampling attempts including failures','R worker/restart and conversion','Upgrade, scientific and rights review'],
  owner_obligations=dict(scientific='Target, trend/factor/noise assumptions and inference',maintainer='Exact options, oracle replay, row identity and bounded retries',operator='Artifacts/notices, budgets and failure accounting'),
  revisit_trigger='Reopen after permissible pinned native oracle replay and target-specific public/synthetic qualification or a source/platform change.',
  contract=ref(BASE/'conversion-contract.json','Proposed contract'),integration_allowed=False,capabilities=[],runtime_qualification=False,original_gap_qualification=False,reviewer=REVIEWER,evidence=evidence,limitations=LIMITS)
 write(OUT,decision)
 findings=['Thirteen source blobs authenticate the original package identity, version, license and dependencies without transferring staggered support.',
  'Target, numerical/inference guards, alternatives, owner/cost obligations and exact independent examples support the bounded reference decision.',
  'No integration capability is granted; proposed conversion and failure contract and reopening conditions retain all material omissions.']
 write(BASE/'review.json',dict(status='pass_for_scoped_proposal_reference',reviewer=REVIEWER,findings=findings,evidence=evidence,reviewed_output=ref(OUT,'Bounded decision'),limitations=LIMITS))
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);r=run.ledger.receipt_template(node)
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,limitations=LIMITS,original_gap_qualification=False,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],outputs=[ref(OUT,'Contracted decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review')]) for i,f in enumerate(findings)])
 verify_bindings(r);run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=OP,sources=len(records),decision='reference',integration_allowed=False)))

if __name__=='__main__':main()
