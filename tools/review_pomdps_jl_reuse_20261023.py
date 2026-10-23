#!/usr/bin/env python3
"""Audit a concrete Julia interface; no solver or native qualification implied."""
import argparse, hashlib, json
from pathlib import Path
import pomdps_jl_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/pomdps-jl-reuse-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=['Sixteen selected immutable source/doc files and independently authored finite examples only; no upstream Julia executed.',
 'Root POMDPs interface review does not approve POMDPTools, any solver/updater/simulator, or all organization packages.',
 'Supplied-model generation is not causal identification, posterior correctness, policy confidence or measured bank benefit.',
 'Complete Julia/dependency custody, separate package rights, native conformance and visual/final acceptance remain open.']
SPANS={
 'LICENSE.md':[([1,24],'MIT root license and explicit separate-license warning for organization packages.')],
 'Project.toml':[([1,26],'Root version 1.0.0, UUID, dependencies and Julia/dependency compatibility ranges.')],
 'src/POMDPs.jl':[([1,14],'Root interface and imports.'),([16,90],'Exports and concrete source includes; solver/updater/simulator are distinct interfaces.')],
 'src/pomdp.jl':[([1,65],'MDP/POMDP types, distribution functions and observation arity fallbacks.'),([67,119],'Reward signature consistency, terminal-zero continuation/default false, initial state and initial observation distinction.'),([122,193],'Index and representation conversion interfaces.')],
 'src/generative.jl':[([1,39],'Joint generator contract with named fields and optional partial outputs.'),([41,69],'Caller macro, requested output tuple, explicit or default random generator.')],
 'src/gen_impl.jl':[([1,54],'One gen invocation per genout; NamedTuple assertion and supplied-field preference.'),([56,109],'Dependency graph and explicit transition/observation/reward fallbacks.')],
 'src/belief.jl':[([7,39],'Generalized belief/update, lossy initialization contract and identity fallback.'),([41,59],'Partial history permitted; current observation uses last history item.')],
 'src/distribution.jl':[([5,40],'Distribution sampling, density/mass, mode, mean and support interface declarations.')],
 'src/space.jl':[([5,48],'Complete spaces, state/belief-dependent actions and fallbacks.')],
 'src/policy.jl':[([7,36],'Policy information state, action, default updater and utility interface.')],
 'src/solver.jl':[([2,12],'Abstract solver and solve declaration, not a concrete numerical algorithm.')],
 'src/simulator.jl':[([1,14],'Abstract simulator, flexible return and external simulation-standard reference.')],
 'docs/src/interfaces.md':[([1,28],'Flexible space/distribution types and required operations; third-party implementations separate.')],
 'docs/src/concepts.md':[([3,18],'Problem/solver/experiment separation.'),([49,91],'Generalized, possibly lossy belief representation and separate updater.'),([95,124],'Offline solve versus online action and simulator roles.')],
 'docs/src/def_pomdp.md':[([129,184],'Stable state identity, action dependence, distribution sampling and old-state observation compatibility.'),([350,398],'Joint/partial generation and limits for explicit-distribution solvers.'),([400,434],'Declared tabular indexing orientation.')],
 'docs/src/def_updater.md':[([7,27],'Belief information requirements, partial history and updater contract.'),([29,53],'Illustrative history updater copies and appends; no generic posterior inference.')]
}
FINDINGS=['A concrete root interface is distinguished from organization-wide, solver and tools adoption.',
 'Joint generation preserves dependence only if the adapter preserves the event; the split-call witness is an adapter counterexample, not an upstream defect.',
 'Observation arity, expected reward, terminal-entry clock and indexing require solver-specific conformance.',
 'Generalized belief and lossy/pass-through initialization do not certify posterior sufficiency, normalization or isolation.',
 'Reference disposition retains a conditional Julia worker route, with exact target, costs, owners and native prerequisites.']

def audit():
 assert not (BASE/'source-audit.json').exists()
 sel=read(BASE/'source-selection.json');commit=read(RAW/'exec23_pomdpsjl_cutoff.json')[0];tree=read(RAW/'exec23_pomdpsjl_tree.json')
 assert sel['commit']==commit['sha']=='d970a36d6e41b7d6baa8377ce0426c7282bc5025'
 assert tree['sha']==commit['commit']['tree']['sha']==sel['tree'] and not tree['truncated']
 assert sel['date']==commit['commit']['committer']['date']=='2026-06-08T01:47:11Z'
 entries={e['path']:e for e in tree['tree']};records=[]
 for e in sel['selected']:
  p=RAW/(e['id']+'.txt');data=p.read_bytes();receipt=read(RAW/(e['id']+'.receipt.json'));path=e['path']
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  url='https://raw.githubusercontent.com/JuliaPOMDP/POMDPs.jl/'+commit['sha']+'/'+path
  assert blob==entries[path]['sha'] and len(data)==entries[path]['size'] and receipt['sha256']==core.sha(p) and receipt['url']==url
  assert all(1<=a<=b<=len(data.decode().splitlines()) for (a,b),_ in SPANS[path]),path
  records.append(dict(upstream_path=path,source_identity=url,version_date=sel['date'],local_copy=ref(p,'Inspected primary contract'),receipt=ref(RAW/(e['id']+'.receipt.json'),'Acquisition custody'),git_blob_sha1=blob,inspected_anchors=[dict(lines=span,finding=c) for span,c in SPANS[path]],supported_claims=[c for _,c in SPANS[path]],executed=False))
 assert len(records)==16 and 'version = "1.0.0"' in (RAW/'exec23_pomdpsjl_01.txt').read_text()
 assert exact.calculate()==read(BASE/'exact-results.json')
 identity=dict(repository='JuliaPOMDP/POMDPs.jl',package='POMDPs',version='1.0.0',commit=commit['sha'],tree=tree['sha'],date=sel['date'],source_blobs=16,evidence=[ref(RAW/'exec23_pomdpsjl_cutoff.json','Cutoff revision'),ref(RAW/'exec23_pomdpsjl_tree.json','Canonical tree')],maintenance='Selected repository activity and compatibility metadata; no service/support or entire release-history claim.')
 write(BASE/'identity.json',identity)
 write(BASE/'static-contract-check.json',dict(native_execution=False,findings=FINDINGS,evidence=[ref(Path(exact.__file__),'Independent algebra and source assertions')],limits=['No executed API, Julia timing or conformance claim.','Authored conversion counterexamples are not claimed upstream defects.']))
 source=dict(integrated_citation_key='exec23_pomdpsjl_sources',kind='software_primary_sources',title='POMDPs.jl 1.0.0 root model, generation, belief and solver interfaces',author='JuliaPOMDP contributors',year=2026,source_identity='https://github.com/JuliaPOMDP/POMDPs.jl/tree/'+commit['sha'],version_date='1.0.0; '+sel['date'],local_copy=records[3]['local_copy'],identity=identity,records=records,inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],supported_claims=[c for spans in SPANS.values() for _,c in spans],license_text=ref(RAW/'exec23_pomdpsjl_00.txt','Pinned root license'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_pomdpsjl_reference',kind='project_derivation_and_exact_reference',title='Exact joint-generation and model-conversion witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/pomdps_jl_reference_20261023.py',version_date='23 October 2026; independent finite-law arithmetic',local_copy=ref(Path(exact.__file__),'calculate'),inspected_anchors=['calculate'],supported_claims=['Coherent versus split generation gives state-alert agreement 1 versus 5/8 and alert-loss probability 1/4 versus 1/16.', 'Stipulated rescue values are 35/4 versus -5/8; expected reward -4 differs from uniform state average -16.', 'Terminal entry reward 12 survives zero continuation; a destination mask wrongly gives zero.', 'An old-state-dependent alert cannot always be represented by action and next state alone.', 'Supplied-model target and proposed conversion safeguards are project arguments, not observed package/bank results.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 omissions=dict(items=[dict(gap='Concrete solver/updater/simulator and tools packages',next_action='Choose explicit candidates, acquire their source/licenses and audit requirements; root interface approval cannot transfer.'),dict(gap='Complete native environment and rights',next_action='Bind Julia version, exact dependency artifacts, model code, notices and reproducible worker environment.'),dict(gap='Native conversion and accuracy',next_action='Register joint-generation, old-state sensor, reward expectation, terminal entry, indexing, mutation, history and RNG conformance against finite oracles; measure offline/online cost and recovery.'),dict(gap='Scientific model and uncertainty',next_action='Justify intervention/observation law and latent state, then separately assess numerical, model and policy-selection uncertainty.')],limitations=LIMITS)
 write(BASE/'omissions-register.json',omissions)
 write(BASE/'plan-review.json',dict(status='pass_for_reference_disposition',evidence=[ref(BASE/n,'Reviewed argument') for n in ['plan.md','exact-results.json','static-contract-check.json','development.tex']],findings=FINDINGS,native_execution=False))
 evidence=[ref(BASE/n,'Reviewed source or exact witness') for n in ['source-audit.json','identity.json','static-contract-check.json','exact-results.json','omissions-register.json','plan-review.json','development.tex']]+[ref(Path(__file__),'Audit logic'),ref(Path(exact.__file__),'Independent examples')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=FINDINGS,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(source_blobs=16,source_records=2,decision='reference',native_execution=False)))

def receipt():
 op='SW.DECISION.inherited_pomdps';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op;verify_bindings(read(BASE/'review.json'))
 evidence=[ref(BASE/n,'Reviewed root-interface reference decision') for n in ['source-audit.json','identity.json','review.json','plan-review.json','exact-results.json','static-contract-check.json','omissions-register.json','development.tex']]+[ref(Path(__file__),'Receipt construction')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified root Julia planning-interface reference; no native solver or adapter approval',identity=read(BASE/'identity.json'),reason='Retain explicit model/solver/updater/simulator separation and joint-generation semantics, subject to concrete solver and native qualification.',target_and_uncertainty='Declared supplied-model finite or justified discounted policy value; interface availability does not identify latent mechanisms or calibrate learned-policy confidence.',
  license=dict(declaration='MIT root package only',text=ref(RAW/'exec23_pomdpsjl_00.txt','Pinned root license and separate-package warning'),transitive_clearance=False),dependencies=dict(runtime=['Julia compatible with 1.6','Distributions','Graphs','NamedTupleTools','POMDPLinter','Pkg','Random','Statistics'],environment_locked=False),
  conversion_contract=['Bind model/state/action/observation identity, information clock, target horizon, reward units and discount.', 'Preserve one joint event and declared random stream; do not split coupled generator output into independent calls.', 'Match solver observation/reward arity, probability-weighted expectation, terminal-entry reward and index orientation.', 'Identify generalized belief representation, lossy transformations, history sufficiency, mutation/isolation and supported operations.', 'Library/CLI/MCP carry identical target, diagnostics and refusal; online action and offline solve budgets are separately measured.'],
  alternatives=[dict(route='Full organization adoption',decision='reject',reason='Root interface cannot confer solver, tools, rights or numerical acceptance.'),dict(route='Concrete native Julia worker',decision='conditional future prototype',reason='Preserves ecosystem dispatch after selected solver/updater/simulator review and registered conformance.'),dict(route='R/Python/Java/C++ port',decision='reject for current scope',reason='No demonstrated benefit warrants duplicating stochastic-event and dispatch semantics.'),dict(route='Independent finite-state oracle',decision='retain',reason='Separately checks target law and conversion.'),dict(route='Latent identification or calibrated policy-confidence engine',decision='reject',reason='The root planning interface does not establish these scientific guarantees.')],
  costs_to_measure=['Julia artifact custody and compilation','Concrete package audit and rights','Model/event serialization','Offline solve and online action latency','Accuracy-dependent time/memory','Isolation, timeout and recovery','Version maintenance'],owner_obligations=dict(scientific='Intervention and observation meaning; numerical/model/selection uncertainty',maintainer='Pinned Julia package set and conversion conformance',operator='Rights, budgets, persistence and recovery'),revisit_trigger='Complete concrete solver/updater/simulator review, locked Julia environment and registered native finite-oracle evidence; changed model/clock requires new review.',evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);r=run.ledger.receipt_template(node)
 findings=['Concrete root identity, source, license and compatibility boundaries inspected.', 'Target, conversion contracts, alternatives, costs, owners and revisit triggers explicit.', 'Reference-only result separates interface design, exact examples and native/scientific qualification.']
 r.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted interface reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
