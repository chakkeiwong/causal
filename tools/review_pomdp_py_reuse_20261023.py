#!/usr/bin/env python3
"""Inspect a supplied-model planner without granting causal or native qualification."""
import argparse,hashlib,json
from pathlib import Path
import pomdp_py_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT;BASE=ROOT/'docs/program/execution/2026-10-23/pomdp-py-reuse-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text());REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Thirteen selected immutable sources and independently authored finite examples only; no upstream code executed.',
 'Supplied-model planning is not hidden-state identification, calibrated policy-value inference, measured bank economics or native product acceptance.',
 'Complete release/compiler/ABI/dependency custody, transitive rights, broader models and native qualification remain open.']
SPANS={
 'LICENSE':[([1,9],'MIT source license text and named copyright holder.')],
 'setup.py':[([1,49],'Cython extension enumeration, selected modules and binary/source package data.')],
 'pyproject.toml':[([1,38],'Version1.3.5.1, author, MIT declaration, build tools, runtime and optional example dependencies.')],
 'pomdp_py/framework/basics.pyx':[([145,209],'Stochastic reward interface and documented black-box three-tuple.'),([344,398],'History append, prior/current belief and belief sampling.'),([642,722],'General sampler four-tuple and default internal discount; zero-duration noninitiable options and explicit reward accumulation.')],
 'pomdp_py/framework/planner.pyx':[([1,35],'Supplied-model planning, update and belief ownership interfaces.')],
 'pomdp_py/representations/belief/histogram.py':[([15,88],'Bayes product, static shortcut, restricted next-state support and normalization only for positive mass.')],
 'pomdp_py/representations/belief/particles.pyx':[([18,43],'Deprivation error, survivor resampling and optional transformation.'),([46,87],'Explicit updater marked untested; exact observation-match filtering and reinvigoration.')],
 'pomdp_py/algorithms/po_uct.pyx':[([89,105],'Current value action choice and order-sensitive ties.'),([185,223],'Time/simulation defaults and measured counters.'),([249,285],'Agent/tree state and update behavior.'),([298,334],'Action expansion and simulations sampled from current belief.'),([344,415],'Simulation-count priority, between-simulation wall clock, depth conditions, zero-step tree guard and unguarded rollout progress.'),([417,433],'Exploration bonus and visit/value updates select tree actions, not confidence regions.')],
 'pomdp_py/algorithms/pomcp.pyx':[([59,125],'Enumerable action/particle restriction, update history contract and particle deprivation.'),([127,146],'Belief accumulation at depth one and tree belief initialization.')],
 'pomdp_py/algorithms/value_iteration.pyx':[([1,55],'Unpruned finite policy tree and depth-powered child discount; sampled reward.'),([64,140],'Enumerable finite horizon, policy-tree construction and best-belief action.')],
 'pomdp_py/algorithms/value_function.py':[([1,95],'Finite-state deterministic-reward value/Q recursion with one-step discount.'),([98,139],'Expected reward and belief formulas; positive-observation guard in caller versus direct denominator division.')],
 'pomdp_py/representations/distribution/histogram.pyx':[([18,24],'Dictionary-only construction without normalization validation.'),([65,91],'Weighted sampling and normalization-check helper.')],
 'pomdp_py/representations/distribution/particles.pyx':[([5,39],'Weighted duplicate-value average convention and initial cache.'),([130,174],'Entry-weighted sampling versus average-per-value normalized histogram.'),([175,236],'Ordinary Particles overrides with count frequencies and uniform entry sampling.')]
}
FINDINGS=['Supplied-model posterior and planning values do not identify latent bank mechanisms or qualify optimal-policy uncertainty.',
 'Zero-mass histogram, restricted support, particle deprivation and weighted-query/sampling conventions need distinct refusal/identity contracts.',
 'Positive simulation count overrides time; zero-duration rollout can fail to advance and the outer budget cannot interrupt a simulation.',
 'Option reward clocks, black-box arity, stochastic reward expectation and policy-tree depth discount need source-specific native fixtures.',
 'Ordinary Particles and the alternative one-step value recurrence must not inherit defects attributed to different implementations.']
def audit():
 assert not (BASE/'source-audit.json').exists()
 sel=read(BASE/'source-selection.json');commit=read(RAW/'exec23_pomdppy_cutoff.json')[0];tree=read(RAW/'exec23_pomdppy_tree.json')
 assert sel['commit']==commit['sha']=='bd0e4392247aebfe9a95b449275237dcc25e7737'
 assert tree['sha']==commit['commit']['tree']['sha']==sel['tree'] and not tree['truncated']
 assert sel['date']==commit['commit']['committer']['date']=='2025-10-28T03:55:09Z'
 entries={e['path']:e for e in tree['tree']};records=[]
 for e in sel['selected']:
  p=RAW/(e['id']+'.txt');data=p.read_bytes();receipt=read(RAW/(e['id']+'.receipt.json'));path=e['path'];blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();url='https://raw.githubusercontent.com/h2r/pomdp-py/'+commit['sha']+'/'+path
  assert blob==entries[path]['sha'] and len(data)==entries[path]['size'] and receipt['sha256']==core.sha(p) and receipt['url']==url
  assert all(1<=a<=b<=len(data.decode().splitlines()) for (a,b),_ in SPANS[path]),path
  records.append(dict(upstream_path=path,source_identity=url,version_date=sel['date'],local_copy=ref(p,'Inspected contract spans'),receipt=ref(RAW/(e['id']+'.receipt.json'),'Acquisition custody'),git_blob_sha1=blob,inspected_anchors=[dict(lines=span,finding=c) for span,c in SPANS[path]],supported_claims=[c for _,c in SPANS[path]],executed=False))
 assert len(records)==13 and 'version = "1.3.5.1"' in (RAW/'exec23_pomdppy_02.txt').read_text()
 assert exact.calculate()==read(BASE/'exact-results.json')
 write(BASE/'static-contract-check.json',dict(native_execution=False,findings=FINDINGS,evidence=[ref(Path(exact.__file__),'Independent algebra and source assertions')],limits=['No executed timeout, native error, API compatibility or empirical coverage claim.','Depth, option and weighted-particle findings apply to the named source paths only.']))
 identity=dict(repository='h2r/pomdp-py',version='1.3.5.1',commit=commit['sha'],tree=tree['sha'],date=sel['date'],source_blobs=13,evidence=[ref(RAW/'exec23_pomdppy_cutoff.json','Cutoff revision'),ref(RAW/'exec23_pomdppy_tree.json','Canonical tree')],maintenance='Named author, beta metadata and selected revision; no support promise or complete release-history claim.')
 write(BASE/'identity.json',identity)
 source=dict(integrated_citation_key='exec23_pomdppy_sources',kind='software_primary_sources',title='POMDP-Py1.3.5.1 selected belief, planner, horizon and reward-clock contracts',author='Kaiyu Zheng and POMDP-Py contributors',year=2025,source_identity='https://github.com/h2r/pomdp-py/tree/'+commit['sha'],version_date='1.3.5.1; '+sel['date'],local_copy=records[3]['local_copy'],identity=identity,records=records,inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],supported_claims=[c for spans in SPANS.values() for _,c in spans],license_text=ref(RAW/'exec23_pomdppy_00.txt','Pinned MIT text'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_pomdppy_reference',kind='project_derivation_and_exact_reference',title='Exact hidden-state, support, option-clock and planning-horizon witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/pomdp_py_reference_20261023.py',version_date='23 October2026; independent rational-arithmetic examples',local_copy=ref(Path(exact.__file__),'calculate'),inspected_anchors=['calculate'],supported_claims=['Prior1/4 and declared sensor give posteriors1/2 and1/10; stipulated signal-policy net7/4 versus-13/4 under an uninformative actual sensor.',
  'Three-stage depth-powered discount gives13/8 versus ordinary7/4; option clock gives15 versus11.',
  'Weighted repeated-state query gives1/2 versus sampling2/3; ordinary unweighted frequency is2/3.',
  'Impossible observation gives zero normalizer; restricted next-state support changes conditional mass.',
  'Zero duration leaves rollout depth unchanged; source checks outer budget between simulations.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 omissions=dict(items=[dict(gap='Complete artifact/compiler/ABI/environment and rights',next_action='Bind release and model code, compiler/native binaries and dependency notices before actual worker integration.'),dict(gap='Belief and planner native contracts',next_action='Register finite oracles and adverse fixtures for impossible signals, omitted support, duplicate particles, deprivation, history/tree coordination, timeout/zero-duration options, arity, horizon and reward clocks.'),dict(gap='Model identification and uncertainty',next_action='Justify latent observation/intervention laws and separately derive parameter/model/selected-policy uncertainty; supplied-model search cannot establish it.'),dict(gap='Broader algorithms and actual cost',next_action='Inspect additional model/planner families and measure full native workflow cost under declared accuracy and recovery requirements.')],limitations=LIMITS)
 write(BASE/'omissions-register.json',omissions)
 write(BASE/'plan-review.json',dict(status='pass_for_reference_disposition',evidence=[ref(BASE/n,'Reviewed argument') for n in ['plan.md','exact-results.json','static-contract-check.json','development.tex']],findings=FINDINGS,native_execution=False))
 evidence=[ref(BASE/n,'Reviewed source or exact witness') for n in ['source-audit.json','identity.json','static-contract-check.json','exact-results.json','omissions-register.json','plan-review.json','development.tex']]+[ref(Path(__file__),'Audit logic'),ref(Path(exact.__file__),'Independent examples')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=FINDINGS,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(source_blobs=13,source_records=2,decision='reference',native_execution=False)))
def receipt():
 op='SW.DECISION.inherited_pomdp_py';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op;verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed planner reference decision') for n in ['source-audit.json','identity.json','review.json','plan-review.json','exact-results.json','static-contract-check.json','omissions-register.json','development.tex']]+[ref(Path(__file__),'Receipt construction')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified supplied-model planning reference; no native adapter approval',identity=read(BASE/'identity.json'),reason='Retain explicit model/belief/planner separation while requiring concrete belief, progress, clock, arity and horizon repairs and native qualification.',target_and_uncertainty='Finite or explicitly scoped supplied-model expected reward under declared belief/history/horizon; approximate search values are separate from latent identification and learned-policy confidence.',
  license=dict(declaration='MIT',evidence=ref(RAW/'exec23_pomdppy_02.txt','Project metadata'),text=ref(RAW/'exec23_pomdppy_00.txt','Pinned license'),transitive_clearance=False),dependencies=dict(build=['setuptools','wheel','Cython>=3.0.8'],runtime=['numpy>=1.18.0','scipy>=1.6.0','tqdm>=4.55.0'],environment_locked=False),
  conversion_contract=['Bind supplied model revision, initial/current belief, history, state/action/observation IDs and decision clock.', 'Reject zero/nonfinite belief mass and undeclared lost support; distinguish weighted/unweighted measures, deprivation and approximation transforms.', 'Preserve primitive/option reward and duration conventions, horizon and black-box arity; ensure progress and an outer execution deadline.', 'Record native build, random sources, action order, simulation budget and completed counters; library/CLI/MCP retain target, refusals and uncertainty limits.'],
  alternatives=[dict(route='Full adoption',decision='defer',reason='Broader uninspected models, source defects and native build/rights exceed this profile.'),dict(route='Original Python/Cython worker',decision='conditional future prototype',reason='Can preserve explicit model semantics after reviewed fixes and finite-oracle native tests.'),dict(route='R/Java/C++ port',decision='reject for current scope',reason='No demonstrated benefit warrants duplicating belief/search/stochastic-state and maintenance contracts.'),dict(route='Independent finite-state oracle',decision='retain',reason='Separately tests intended target and numerical recurrence.'),dict(route='Hidden-state identification or optimal-value confidence engine',decision='reject',reason='Supplied-model planning does not establish those scientific guarantees.')],
  costs_to_measure=['Native build/custody','Model/clock conversion','Belief/planner repair qualification','Search and memory by accuracy target','Timeout/recovery','Version maintenance'],owner_obligations=dict(scientific='Latent observation/intervention meaning and model/selected-policy uncertainty',maintainer='Pinned native environment, repair and conformance',operator='Actual rights, budgets, deadlines and recovery'),revisit_trigger='Complete source/compiler/dependency custody plus reviewed source-contract repairs and registered native evidence; changed model, target or clocks require new review.',evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Concrete immutable version, license text, dependency/native build and maintenance limits inspected.','Target, belief/search conversion, defects, alternatives, costs, owners and revisit triggers explicit.','Reference-only scope separates static findings and exact witnesses from native/scientific qualification.']
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted planner reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
