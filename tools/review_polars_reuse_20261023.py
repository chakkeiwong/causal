#!/usr/bin/env python3
"""Review authenticated Polars sources; never import upstream code."""
import argparse, hashlib, json, tomllib
from pathlib import Path
import polars_reference_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-23/polars-reuse-v1';RAW=ROOT/'docs/literature/raw'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=['Selected authenticated primary spans and project-owned arithmetic only; no downloaded code or tests executed.',
 'Python 2.0.0 and Rust 0.55.1 are source declarations; distributed artifacts and complete dependencies remain unauthenticated.',
 'No native speed, memory, recovery, causal identification, bank ROI, transitive rights clearance or integration is qualified.',
 'Wider coverage, actual environments, native trials, costs, bank and visual/final acceptance remain open.']
SPANS={
0:[(1,20,'Permission is hereby granted','Root MIT terms require notice retention; dependencies and commercial services remain separate.')],
1:[(1,24,'version = "0.55.1"','Rust workspace declares 0.55.1 and edition 2024, separately from Python numbering.'),(25,65,'workspace.dependencies','Selected dependency declarations do not establish a complete locked environment.')],
2:[(1,92,'version = "2.0.0"','Python source declares 2.0.0, Python>=3.10, matching runtime-32 and distinct optional runtime/interop/database/cloud/GPU routes.')],
3:[(1,37,'fall back','Streaming guide permits in-memory fallback and contains an editorial exclusion comment; repository presence is not proof of hosted publication or speed.')],
4:[(5,26,'NaN','Null is missing; NaN is a distinct floating value.'),(62,76,'fill_null','Filling supports literals, expressions, neighbors and interpolation; none proves a missingness model.'),(141,189,'skip the missing values','NaN is excluded from null_count/fill_null; means/sums skip nulls and typically propagate NaN.')],
5:[(1,18,'Predicate pushdown','Optimization includes predicate/projection/slice pushdown, subplan elimination, join ordering and type coercion.')],
6:[(1,9,'non-optimized','Logical and optimized plans are distinct inspection surfaces.'),(40,108,'explain(optimized=False)','Printed and physical plans expose execution choices; predicate pushdown is not causal justification.')],
7:[(1,43,'semi join','Guide separates membership under equi, outer, semi, anti, cross and as-of joins and Python/Rust routes.'),(175,244,'row filter','Coalescing combines key columns; semi/anti membership differs from joining payloads.'),(246,270,'strategy = "backward"','Stock example seeks quotes before a trade but does not authenticate availability time.')],
8:[(12,31,'replace_time_zone','Time-zone conversion and replacement differ; a Datetime column has one zone.')],
9:[(20,59,'They may overlap','Dynamic grouping requires ordered dates; period and spacing can overlap or leave gaps.')],
10:[(2078,2135,'defaults to the streaming engine','collect documents auto affinity, streaming default absent configuration, fallback and unstable GPU/background/optimization surfaces.'),(2215,2228,'engine_.collect','collect delegates the selected engine and flags.'),(5557,5703,'check_sortedness','As-of direction, strictness, tolerance, grouping and engine-specific sortedness checks differ; calendar days can differ from 24 hours.'),(5905,5958,'allow_eq=allow_exact_matches','As-of forwards strictness and sortedness.'),(5968,6098,'Does not result in checks','Join defaults to inner and unchecked m:m; null, coalescing, ordering and build-side choices are explicit.'),(6258,6284,'validate','Join forwards validation and other contracts to the underlying call.')],
11:[(8296,8348,'not supported by the streaming engine','Eager docstring adds a streaming-validation limit absent from the lazy docstring; lower-level inspection is needed.')],
12:[(2225,2269,'nulls_equal=True','Unexecuted tests specify null-key matching with order-dependent assertions; not identity truth or observed native conformance.')],
13:[(1348,1397,'allow_exact_matches=False','Unexecuted as-of test specifies strict matches and finite tolerance.'),(1428,1504,'Deliberately invalid','Unexecuted tests distinguish grouped in-memory warnings, disabled checks and streaming grouped checks.')],
14:[(295,344,'monitoring','Monitoring is explicit/configured and can activate cloud-related behavior; none is enabled here.'),(388,408,'ldf.collect(self.name','Local engine forwards engine name/callbacks; background uses concurrent collection.'),(692,754,'raise_on_fail','Local engine names differ; GPU provides an explicit no-fallback option.')],
15:[(1,44,'pub mod in_memory','Module separates specialized and in-memory join nodes; no execution result follows.')],
16:[(10,38,'InMemorySinkNode','In-memory join has two input sinks and a supplied closure.'),(59,98,'NodeMemoryUsage::Accumulating','It calls the join closure after both inputs finish and labels its sink memory accumulating.')],
17:[(1,38,'polars_defs::join','Selected imports identify JoinArgs location only; no exhaustive equi-join algorithm review.')],
18:[(1,16,'JoinIds','Ops args contains index aliases, not cardinality-validation definitions.')],
19:[(1355,1397,'!args.validation.needs_checks()','Specialized streaming lowering requires supported joins and no cardinality checks; grouped as-of uses sortedness metadata.'),(1570,1598,'PhysNodeKind::InMemoryJoin','Alternate lowering preserves args/options in InMemoryJoin; no discarded-validation claim.')],
20:[(34,46,'validation: JoinValidation','JoinArgs carries validation, null, coalescing, order and build-side choices.'),(384,424,'ManyToMany','Only m:m needs no uniqueness checks; validation supports specified join types and errors otherwise.')]
}
FINDINGS=['Join multiplicity changes the sampling measure; null responses, nonfinite values and missing identities need distinct contracts.',
 'Event-time matching does not guarantee availability; revisions, strictness, groups, zones and sortedness preserve the information clock.',
 'Overlapping windows alter covariance even if aggregation is correct.',
 'Checked joins take an in-memory alternate lowering path; no silent loss of validation is established.',
 'Retain a Python/Rust data-worker reference; actual conformance, costs and recovery remain trial obligations.']

def audit():
 assert not (BASE/'source-audit.json').exists()
 sel=read(BASE/'source-selection-v3.json');commit=read(RAW/'exec23_polars_cutoff.json')[0];tree=read(RAW/'exec23_polars_tree.json')
 assert sel['commit']==commit['sha']=='bf2152618c7123836a825f8566f4d98585b6ff5b'
 assert sel['tree']==tree['sha']==commit['commit']['tree']['sha'] and not tree['truncated']
 assert sel['date']==commit['commit']['committer']['date']=='2026-10-07T14:54:47Z' and sel['date']<='2026-10-07T15:59:59Z'
 for n in ['cutoff','tree']:
  p=RAW/f'exec23_polars_{n}.json';r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and r['sha256']==core.sha(p)
 entries={x['path']:x for x in tree['tree']};records=[]
 for i,e in enumerate(sel['selected']):
  p=RAW/(e['id']+'.txt');rp=p.with_suffix('.receipt.json');data=p.read_bytes();r=read(rp);blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
  url=f'https://raw.githubusercontent.com/pola-rs/polars/{sel["commit"]}/{e["path"]}'
  assert blob==e['blob']==entries[e['path']]['sha'] and len(data)==e['size']==entries[e['path']]['size']
  assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==url
  lines=data.decode().splitlines();anchors=[]
  for a,b,token,finding in SPANS[i]:
   assert 1<=a<=b<=len(lines) and token in '\n'.join(lines[a-1:b]),(i,a,b,token)
   anchors.append(dict(lines=[a,b],finding=finding))
  records.append(dict(upstream_path=e['path'],source_identity=url,version_date=sel['date'],local_copy=ref(p,'Only listed spans inspected'),receipt=ref(rp,'Acquisition custody'),git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
 assert len(records)==21 and exact.calculate()==read(BASE/'exact-results.json')
 py=tomllib.loads((RAW/'exec23_polars_02.txt').read_text())['project'];rust=tomllib.loads((RAW/'exec23_polars_01.txt').read_text())['workspace']['package']
 assert py['version']=='2.0.0' and py['requires-python']=='>=3.10' and py['dependencies']==['polars-runtime-32 == 2.0.0'] and rust['version']=='0.55.1' and rust['edition']=='2024'
 identity=dict(repository='pola-rs/polars',package='polars',python_version=py['version'],rust_version=rust['version'],version_status='Pinned source declarations; no distributed release authenticated',commit=sel['commit'],tree=tree['sha'],date=sel['date'],python=py['requires-python'],direct_dependencies=py['dependencies'],optional_dependencies=py['optional-dependencies'],rust_edition=rust['edition'],source_blobs=21,maintenance='Selected contracts inspected; no service-level or exhaustive maintenance claim.',evidence=[ref(RAW/f'exec23_polars_{n}.json','Cutoff identity') for n in ['cutoff','tree']])
 write(BASE/'qualified-identity.json',identity)
 write(BASE/'static-contract-check.json',dict(status='pass_for_scoped_source_interpretation',findings=FINDINGS,native_execution=False,rejected_overclaims=['Streaming does not demonstrably discard validation.','Backward event matching need not preserve availability.','Null equality is not customer identity.','No speed, memory or causal qualification.'],documentation_tension='Eager validation note versus lazy docstring; Rust lowering selects InMemoryJoin for checked validation. Native behavior untested.'))
 source=dict(integrated_citation_key='exec23_polars_sources',kind='software_primary_sources',title='Polars pinned dataframe, missing-value, temporal-join and execution contracts',author='Polars Contributors',year=2026,source_identity=f'https://github.com/pola-rs/polars/tree/{sel["commit"]}',version_date=f'Source Python2.0.0 / Rust0.55.1; {sel["date"]}; {sel["commit"]}',local_copy=records[10]['local_copy'],identity=identity,records=records,inspected_anchors=[dict(path=r['upstream_path'],anchors=r['inspected_anchors']) for r in records],supported_claims=[a['finding'] for r in records for a in r['inspected_anchors']],license_text=ref(RAW/'exec23_polars_00.txt','Root MIT terms'),limitations=LIMITS)
 project=dict(integrated_citation_key='exec23_polars_reference',kind='project_derivation_and_exact_reference',title='Exact authored dataframe population, information-clock and overlap witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/polars_reference_20261023.py',version_date='23 October2026; supplied populations and costs',local_copy=ref(Path(exact.__file__),'calculate'),inspected_anchors=['calculate: fanout, missing, information_clock, overlapping_windows'],supported_claims=['Customer contrast5 becomes event-weighted15/2; cost6 gives descriptive margins-1 and3/2.','Observed mean3 leaves full means2 and14/3 compatible with hidden0/8.','Event-backward, nearest and availability-aware supplied values are0,10,4.','Overlap covariance1/4 gives mean variance3/8 versus incorrect independence1/4.'],limitations=LIMITS)
 write(BASE/'source-audit.json',dict(sources=[source,project],cutoff='2026-10-07',native_execution=False))
 write(BASE/'omissions-register.json',dict(items=[dict(gap='Actual artifacts and rights',next_action='Freeze Python/Rust runtimes, optional engines, lockfiles and notices.'),dict(gap='Native conversion conformance',next_action='Register duplicate/null/nonfinite, schema/cardinality/order and checked-join fallback cases.'),dict(gap='Historical availability and uncertainty',next_action='Bind event/availability time, revisions, ties, zones and dependence law.'),dict(gap='Costs and recovery',next_action='Measure validation, scans, conversion, fallback/spill, accepted output and durable restart.'),dict(gap='Scientific/bank validity',next_action='Justify identification, missingness and linkage; computation cannot manufacture truth.')],limitations=LIMITS))
 evidence=[ref(BASE/n,'Reviewed Polars argument') for n in ['plan.json','source-audit.json','qualified-identity.json','static-contract-check.json','omissions-register.json','exact-results.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Source/decision logic'),ref(Path(exact.__file__),'Exact reference')]
 write(BASE/'mathematical-review.json',dict(status='pass_for_authored_examples',evidence=evidence,checks=['Join identity follows finite covariance expansion; no causal effect inferred.','Missing-value worlds have identical observations; clock example imposes both event and availability inequalities.','Eight sign triples reproduce overlap covariance and variance.'],native_execution=False))
 write(BASE/'plan-review.json',dict(status='pass_for_reference_disposition',evidence=evidence,findings=FINDINGS,amendments=['Follow validation to Rust lowering before interpreting streaming limitation.','Separate source versions from distributed releases and native acceptance.']))
 evidence += [ref(BASE/'mathematical-review.json','Exact review'),ref(BASE/'plan-review.json','Amended plan')]
 review=dict(status='pass_for_reference_disposition',reviewer=REVIEWER,evidence=evidence,findings=FINDINGS,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
 print(json.dumps(dict(authenticated_blobs=21,source_records=2,decision='reference',native_execution=False)))

def receipt():
 op='SW.DECISION.inherited_polars';state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
 verify_bindings(read(BASE/'review.json'));identity=read(BASE/'qualified-identity.json')
 evidence=[ref(BASE/n,'Reviewed Polars reuse choice') for n in ['review.json','source-audit.json','qualified-identity.json','static-contract-check.json','omissions-register.json','mathematical-review.json','plan-review.json','exact-results.json','development.tex']]+[ref(Path(__file__),'Receipt construction')]
 output=ROOT/f'docs/program/comprehensive-v14/work/{op}/decision.json'
 decision=dict(operation_id=op,status='pass',decision='reference',decision_scope='Source-qualified Polars data-worker reference; no native integration approval',identity=identity,reason='Retain dataframe execution while binding observation units, information clock, missingness and physical plans.',target_and_uncertainty='Declared population/features; causal identification, missingness/linkage assumptions and dependent-window uncertainty remain scientific obligations.',license=dict(declaration='MIT root terms',text=ref(RAW/'exec23_polars_00.txt','Pinned terms'),transitive_clearance=False,commercial_service_entitlement=False),dependencies=dict(python=identity['python'],direct=identity['direct_dependencies'],optional=identity['optional_dependencies'],rust_edition=identity['rust_edition'],environment_locked=False),
 conversion_contract=['Bind sampling units, stable IDs, snapshots and cardinalities before joins.','Preserve null/NaN/unknown identity, schema, precision and unmatched denominators.','Bind event/availability time, revisions, zones, grouping, strictness and tolerances.','Keep overlap covariance and sampling law separate from aggregation.','Bind engine/runtime/plans/validation/fallback; no unsupported memory or speed claims.','Library/CLI/MCP preserve input/request identity, refusal, diagnostics and cancellation state.'],
 alternatives=[dict(route='Pinned Python worker',decision='conditional prototype',reason='Preserves engine contracts after oracle conformance.'),dict(route='Direct Rust integration',decision='separate candidate',reason='Requires feature/artifact and FFI ownership.'),dict(route='Wholesale R/Java/C++ port',decision='reject for current scope',reason='Duplicates optimizer/null/join/runtime obligations without measured benefit.'),dict(route='Database or other dataframe worker',decision='retain alternative',reason='Compare snapshot/key/plan and complete costs on matched workloads; no ranking.'),dict(route='Exact finite oracle',decision='retain',reason='Independent population, clock and covariance checks.')],
 costs_to_measure=['Validation and snapshot binding','Scans/conversion/output checks','Fallback/spilling','Optional runtime/rights','Restart/version maintenance'],owner_obligations=dict(scientific='Population, missingness, assignment, availability and uncertainty',maintainer='Schema/key/time conversion, pinned engines and oracle cases',operator='Actual resources, costs and recovery'),revisit_trigger='Locked artifacts/rights, registered native join/clock/fallback results, matched costs and restart evidence.',evidence=evidence,reviewer=REVIEWER,limitations=LIMITS,integration_allowed=False,runtime_qualification=False,capabilities=[])
 write(output,decision);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op);receipt=run.ledger.receipt_template(node)
 findings=['Pinned source versions, primary contracts, root terms and dependency limits inspected.','Population/uncertainty, conversion, alternatives, costs, owners and revisit trigger are explicit.','Reference-only choice preserves source/authored/native distinctions and grants no capability.']
 receipt.update(outcome='pass',execution='performed',scope=decision['decision_scope'],reviewer=REVIEWER,outputs=[ref(output,'Contracted reference decision')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=decision['revisit_trigger'])
 run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']));verify_bindings(receipt);write(BASE/'operation-receipt.json',receipt)
 print(json.dumps(dict(operation=op,decision='reference',integration_allowed=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()

