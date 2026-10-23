#!/usr/bin/env python3
"""Authenticate selected SCOPE-RL sources and record a proposal reference decision."""
import argparse, ast, hashlib, json
from pathlib import Path
import scope_rl_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/scope-rl-reuse-v1';RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Selected immutable sources and independently authored finite examples only; no downloaded code executed.',
 'No full-artifact/dependency rights clearance, native conformance, empirical coverage, measured bank value or integration permission.',
 'Continuous/distributional/marginal estimators and full model delegates are outside this inspected profile.']
SPANS={
 'LICENSE':[([1,201],'Apache2.0 text, conditions and named copyright holders; transitive rights unreviewed.')],
 'setup.py':[([1,50],'Named author, package metadata, dependency reader and Python classifiers.')],
 'requirements.txt':[([1,12],'Twelve declared dependencies, primarily minimum versions; not an environment lock.')],
 'scope_rl/version.py':[([1,4],'Declared version0.2.1.')],
 'scope_rl/ope/discrete/basic_estimators.py':[([375,498],'TIS weight and discount expressions, shape/probability checks and zero lower limits.'),([620,641],'Fixed trajectory-score interval delegation.'),([720,738],'PDIS prefix weights and discounted score.'),([1073,1109],'DR current/previous weight and fitted-value score.'),([1398,1509],'Self-normalized TIS inheritance, sample-mean denominator and1e-10 stabilizer.')],
 'scope_rl/ope/estimators_base.py':[([81,101],'Named interval helpers selected through shared mapping.'),([113,154],'Behavior-policy cumulative weights and terminal repetition.'),([203,249],'Evaluation probabilities aligned to observed actions and cumulative weights.')],
 'scope_rl/utils.py':[([456,502],'Bootstrap signature/prose mismatch, explicit random seed, fixed-score resampling and bootstrap mean.'),([505,543],'Hoeffding-named source multiplies by sample size and uses observed maximum; differs from printed expression.'),([546,587],'Bernstein-named variance expression differs from printed expression and uses sample maximum.'),([590,632],'Student helper uses1-alpha quantile for symmetric endpoints labelled1-alpha.'),([641,720],'Shape/type/range checks and logged-data key-only checks.')],
 'scope_rl/dataset/base.py':[([18,115],'Equal-length episode contract, reward, done and maximum-step terminal meanings.')],
 'scope_rl/ope/input.py':[([357,405],'Logged-array reshape and done passed as fitted-Q terminal flag.'),([407,497],'FQE default one fold, policy-name cache and contiguous whole-trajectory exclusion.'),([2555,2577],'Whole-input default one-fold and explicit fitting/rollout configuration.')],
 'scope_rl/ope/ops.py':[([586,650],'Required on-policy arrays, sorted policy values and independently sorted lower-quartile values/name pairing.'),([1458,1556],'Lower-bound selector calls truth routine, passes unchanged alpha, ranks endpoints and defines safety-error denominators.')],
 'scope_rl/ope/ope.py':[([304,333],'Default reward preprocessing masks the done row itself with cumulative1-done.'),([489,519],'Candidate interval calls use supplied common alpha and shared estimator helpers.')]
}

def audit():
 assert not (BASE/'source-audit.json').exists()
 selection=read(BASE/'source-selection.json');commit=read(RAW/'exec23_scope_cutoff.json')[0];tree=read(RAW/'exec23_scope_tree.json')
 assert selection['commit']==commit['sha']=='b1c9e9fbfddd924362160ec5e9f9f071abc7b7ea'
 assert tree['sha']==commit['commit']['tree']['sha']==selection['tree'] and not tree['truncated']
 assert commit['commit']['committer']['date']=='2023-12-01T03:58:14Z'
 entries={e['path']:e for e in tree['tree']};records=[]
 for e in selection['selected']:
  p=RAW/(e['id']+'.txt');data=p.read_bytes();receipt=read(RAW/(e['id']+'.receipt.json'));path=e['path']
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  url='https://raw.githubusercontent.com/hakuhodo-technologies/scope-rl/'+commit['sha']+'/'+path
  assert blob==entries[path]['sha'] and len(data)==entries[path]['size']
  assert receipt['status']=='saved' and receipt['url']==url and receipt['sha256']==core.sha(p)
  lines=data.decode().splitlines();assert all(1<=a<=b<=len(lines) for (a,b),_ in SPANS[path]),(path,len(lines))
  records.append(dict(upstream_path=path,source_identity=url,version_date=selection['date'],local_copy=ref(p,'Selected inspected spans'),receipt=ref(RAW/(e['id']+'.receipt.json'),'Acquisition custody'),git_blob_sha1=blob,
   inspected_anchors=[dict(lines=span,finding=claim) for span,claim in SPANS[path]],supported_claims=[claim for _,claim in SPANS[path]],executed=False))
 assert len(records)==11
 utils=(RAW/'exec23_scope_06.txt').read_text();ope=(RAW/'exec23_scope_10.txt').read_text();ops=(RAW/'exec23_scope_09.txt').read_text()
 assert 't.ppf(1 - alpha, n - 1)' in utils and 'samples.max() * np.sqrt(np.log(2 / alpha) / 2 * len(samples))' in utils
 assert '(\n                1 - done\n            ).cumprod(axis=1)' in ope
 assert 'ground_truth_dict = self.obtain_true_selection_result(input_dict)' in ops
 write(BASE/'exact-results.json',exact.calculate())
 static=dict(native_execution=False,source_ast_parsed_not_executed=True,findings=['Same-row done mask can remove terminal receipt under a transition-ending convention.',
  'Fixed-score bootstrap differs from self-normalized ratio resampling; learned nuisances are not refitted in selected call.',
  'Hoeffding radius multiplies by n, observed maxima do not supply population bounds, and Student symmetric endpoints use1-alpha.',
  'Lower-bound selection requires on-policy arrays and forwards unadjusted alpha; lower-quartile names/values need pairing repair.'],limitations=LIMITS)
 write(BASE/'static-contract-check.json',static)
 identity=dict(repository='hakuhodo-technologies/scope-rl',version='0.2.1',commit=commit['sha'],tree=tree['sha'],date=selection['date'],source_blobs=11,
  evidence=[ref(RAW/'exec23_scope_cutoff.json','Cutoff-selected commit'),ref(RAW/'exec23_scope_tree.json','Complete canonical tree')],maintenance='Named author and dated selected revision; no current support or complete release-history claim.')
 write(BASE/'identity.json',identity)
 source=dict(integrated_citation_key='exec23_scope_rl_sources',kind='software_primary_sources',title='SCOPE-RL0.2.1 selected episode, score, uncertainty and policy-selection contracts',author='Haruka Kiyohara and SCOPE-RL contributors',year=2023,
  source_identity='https://github.com/hakuhodo-technologies/scope-rl/tree/'+commit['sha'],version_date='0.2.1; '+selection['date'],local_copy=records[4]['local_copy'],identity=identity,records=records,
  inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],supported_claims=[c for spans in SPANS.values() for _,c in spans],license_text=ref(RAW/'exec23_scope_00.txt','Authenticated source license'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_scope_rl_reference',kind='project_derivation_and_exact_reference',title='Independent episode-value, terminal-clock, resampling and selection witnesses',author='Causal banking proposal project',year=2026,
  source_identity='tools/scope_rl_reference_20261023.py',version_date='23 October2026; exact independently authored examples',local_copy=ref(Path(exact.__file__),'calculate and derive'),inspected_anchors=['calculate','derive'],
  supported_claims=['Two-period finite law gives target5 with sample TIS3 and PDIS15/4.', 'Terminal convention gives value2 versus10 and stipulated net-4 versus4.',
   'Fixed normalized scores and recomputed bootstrap ratios have variances9/2 and9/4 in the stated finite example.',
   'All-zero Bernoulli sample has probability(99/100)^20; conditional symmetric Student pivot coverage is1-2alpha.',
   'Twenty independent nominal5% false admissions yield1-0.95^20; lower-tail name/value pairing has an exact adversarial witness.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 omissions=dict(items=[dict(gap='Full release, dependencies, rights and environment',next_action='Acquire complete frozen release and resolve actual dependency/data notices and versions before integration.'),
  dict(gap='Native trajectory/time/uncertainty conformance',next_action='Use known finite laws, terminal conventions, zero/nonfinite propensities, signed/degenerate returns, bootstrap denominator refitting and cache identity fixtures in an approved frozen environment.'),
  dict(gap='Selection, ground-truth dependency and paired output integrity',next_action='Separate benchmark truth from logged-only use; independently review simultaneous/held-out selection and preserve policy IDs in every sorted field.'),
  dict(gap='Broader families and scientific validity',next_action='Inspect continuous/distributional/marginal methods and full delegates separately; justify logging, support, hidden-state and dependence assumptions for each target.')],limitations=LIMITS)
 write(BASE/'omissions-register.json',omissions)
 write(BASE/'plan-review.json',dict(status='pass_for_reference_disposition',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','static-contract-check.json','exact-results.json','development.tex']],findings=static['findings'],native_execution=False))
 evidence=[ref(BASE/n,'Inspected source or authored argument') for n in ['source-audit.json','identity.json','static-contract-check.json','exact-results.json','omissions-register.json','plan-review.json','development.tex']]+[ref(Path(__file__),'Audit construction'),ref(Path(exact.__file__),'Independent witnesses')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=static['findings'],limitations=LIMITS,native_execution=False)
 verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(source_blobs=11,source_records=2,decision='reference',native_execution=False)))

def receipt():
 op='SW.DECISION.inherited_scope_rl';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
 verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed reference decision') for n in ['source-audit.json','identity.json','review.json','plan-review.json','exact-results.json','static-contract-check.json','omissions-register.json','development.tex']]+[ref(Path(__file__),'Receipt construction')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified proposal reference; no native adapter approval',identity=read(BASE/'identity.json'),
  reason='Retain explicit trajectory-score designs and comparison structure while rejecting unqualified uncertainty/safety admission; preserve concrete repair and native-test requirements.',
  target_and_uncertainty='Specified initial population, episode horizon, logging/target policy, discount and reward clock; conditional fixed-score intervals distinct from nuisance refitting and selected-policy coverage.',
  license=dict(declaration='Apache2.0',evidence=ref(RAW/'exec23_scope_01.txt','Package declaration'),text=ref(RAW/'exec23_scope_00.txt','Pinned license bytes'),transitive_clearance=False),
  dependencies=dict(declared=(RAW/'exec23_scope_02.txt').read_text().splitlines(),environment_locked=False),
  conversion_contract=['Preserve episode IDs/order, pre-action information, horizon, reward units, terminal/max-step convention and policy/training identities.',
   'Require finite positive observed logging probabilities, support and valid target distributions; refuse unsupported or ambiguous discount/termination domains.',
   'Bind fitted nuisance scope, resampling unit, denominator refitting and interval definitions; inspect signed/degenerate values and full warnings.',
   'Separate on-policy benchmark truth from offline requests; preserve policy IDs, multiplicity treatment and untouched evaluation histories across library/CLI/MCP.'],
  alternatives=[dict(route='Full adoption',decision='defer',reason='Broader uninspected families, dependencies and uncertainty defects exceed the profile.'),
   dict(route='Isolated Python worker',decision='conditional future prototype',reason='Potentially preserves original semantics after reviewed repairs, frozen environment and native adverse tests.'),
   dict(route='R/Java/C++ port',decision='reject for current scope',reason='No demonstrated benefit justifies replicating the preprocessing/model/uncertainty maintenance burden.'),
   dict(route='Independent reference oracles',decision='retain',reason='Finite known-law tests clarify targets without claiming package conformance.'),
   dict(route='Generic safety or hidden-state identification',decision='reject',reason='Software output and probability normalization cannot establish the scientific premises.')],
  costs_to_measure=['Dependency custody','Clock/identity conversion','Interval and selection repair review','Native oracle and statistical evaluation','Fitting/resampling compute','Version maintenance'],
  owner_obligations=dict(scientific='Identification, sampling law and selected-policy uncertainty',maintainer='Pinned artifact, repairs, conversion and native conformance',operator='Actual rights, data custody, resource and recovery budget'),
  revisit_trigger='Complete source/dependency custody and reviewed interval/time/selection repairs with registered native evidence; any target/source/environment change requires review.',
  evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision)
 graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Concrete cutoff identity, authentic license, dependency and maintenance limits inspected.', 'Target, uncertainty, failure routes, alternatives, costs, owners and revisit trigger documented.', 'Reference-only disposition grants no native capability and preserves scientific qualification requirements.']
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
