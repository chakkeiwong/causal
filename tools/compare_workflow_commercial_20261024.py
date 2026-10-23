#!/usr/bin/env python3
"""Eight-family documentary comparison; no new native or edition acceptance."""
import argparse,json
from pathlib import Path
import run_program_checkpoint_v3 as controller
import workflow_contract_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/workflow-commercial-comparison-v1'
READER=ROOT/'docs/program/execution/2026-10-24/openlineage-reader-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/workflow-contracts-v3'
OP='SW.COMM.computation_workflow';read=lambda p:json.loads(p.read_text())
REVIEWER=dict(name='Codex author/coordinator',kind='author')

PROFILES=[
 ('Databricks',['exec22_workflow_databricks_repair','exec22_workflow_databricks_monitor'],
  'Public repair and monitoring manuals; exact cutoff deployment edition remains unauthenticated.',
  'Documents partial repair and run monitoring, including explicit warnings about non-idempotent tasks and current repair settings.',
  'A funding batch repair must retain original target, data snapshot and code/settings; a changed repair can be a new scientific experiment.',
  'Retain as execution-platform comparator; use a narrow request/artifact adapter after edition qualification.',
  'Authenticate cutoff manual/API and supported workspace/runtime profile; bind task repair, run-history retention, configuration and append/idempotency behavior.'),
 ('Snowflake',['exec22_workflow_snowflake_graphs'],
  'Public task-graph manual; exact cutoff account/edition/API profile unresolved.',
  'Documents dependency graphs, finalizers, retries and overlap; task-graph versioning does not automatically bind called procedure bodies.',
  'Scheduled portfolio estimates need procedure/code and data versions beyond orchestration DAG identity; skipped root/finalizer cases retain explicit denominators.',
  'Retain task execution as conditional backend; causal graph and execution DAG remain separate.',
  'Acquire cutoff edition/version originals; bind stored-procedure snapshots, suspended/skipped tasks, overlap, retry and retention contracts.'),
 ('Microsoft Azure Machine Learning',['exec22_workflow_azure_reuse'],
  'Public pipeline reuse troubleshooting text; exact cutoff workspace/API/SDK version unresolved.',
  'Documents reuse comparisons over code, environments, inputs, parameters and run settings; determinism is declared.',
  'Repeated collections-policy evaluation must include causal context, split, logger and observation-clock identity in reuse keys; declared determinism alone does not prove it.',
  'Retain reuse machinery as conditional comparator; validate causal semantics at artifact boundary.',
  'Pin cutoff component/SDK/API/environment and inspect reuse/cancellation/export semantics, identity, entitlement and failure outcomes.'),
 ('AWS Step Functions',['exec22_workflow_aws_errors'],
  'Public error-handling manual; exact cutoff state-language/service profile unresolved.',
  'Documents ordered retries/catches, redrive and failure-class distinctions; retries have billing implications but no price is inferred.',
  'A discovery-to-effect workflow must retain unsupported/refused scientific states independently from caught task errors and execution failures.',
  'Retain orchestration as conditional backend; causal acceptance remains an explicit downstream decision.',
  'Authenticate cutoff service/schema and Standard/Express profile, execution limits, redrive/error classes, idempotency and applicable pricing units.'),
 ('Dataiku DSS',['exec24_workflow_contracts_dataiku','exec23_dss_latest_flow','exec23_dss_latest_triggers','exec23_dss_latest_steps','exec23_dss_latest_releases','exec23_dss_dss14_flow','exec23_dss_dss14_releases'],
  'Pinned Python client14.7.3; separately inspected mutable DSS14/15 manuals do not authenticate cutoff server15.0.2 technical bytes.',
  'Scenario control, trigger/run distinction and explicit outcome handling; client source exposes cancellation-before-run and strict success behavior.',
  'Four requested policy comparisons can create only three runs and one accepted artifact; trigger cancellation, WARNING and failed output stay in request-level accounting.',
  'Prefer conditional original Python client with guarded cancelled-trigger handling and explicit transport/observation deadlines.',
  'Bind immutable supported DSS server/client matrix, trigger precedence, full variable/clock and error contracts; qualify no_fail cancellation path and rights.'),
 ('SAS Viya',['exec24_workflow_contracts_sas','exec23_workflow_sasctl','exec23_workflow_delegates_sasctl'],
  'Pinned sasctl and preview Job Execution document version5 dated26November2019; neither is a full supported SAS server edition.',
  'Workflow prompt/request machinery and asynchronous job resources, state links, provider-specific results and logs are documented.',
  'Monthly causal batch submission must preserve time/units, immutable sampling membership, remote identity, provider artifact and cleanup; a failed terminal return is not success.',
  'Prefer conditional original service client/worker; do not replace normative server evidence by porting REST code.',
  'Acquire supported normative workflow and Job Execution schemas, complete state/errors and client/server matrix; separate Visual Investigator case-management from analytics workflow.'),
 ('Domino',['exec24_workflow_contracts_domino','exec23_workflow_dominopy','exec23_workflow_delegates_dominopy'],
  'Pinned Python clientc36d3cae32a7b97716dc75cbbfeac1899e113a41; supported v4/jobs server profile unresolved.',
  'Job identity, start/stop/status/restart and revision controls; source review distinguishes transport retries, reauthentication and remote restart.',
  'A restarted servicing estimate needs original target/data/environment custody; a successful mock or client409 interpretation cannot define every server state.',
  'Prefer conditional original client with explicit remote reconciliation and frozen environment; keep a direct request oracle.',
  'Acquire immutable v4/jobs terminal/error/idempotency schemas and supported server matrix; solve the dependency lock and register connection/read/status/restart cases.'),
 ('Posit Workbench and Connect',['exec24_workflow_contracts_posit','exec23_workflow_positgo','exec23_workflow_connectapi','exec23_workflow_delegates_positgo'],
  'Pinned Go Launcher SDK, C++ Local backend and connectapi sources; historical Workbench1.4 prerequisites are not a current support matrix.',
  'Typed scheduler states/exit codes, plugin boundary and Connect task/job/schedule clients; sample Local backend has explicit unsupported cancellation.',
  'A Finished process with exit7 and no bound causal artifact differs from exit0 with accepted output; unknown scheduler states and unsupported Cancel must remain visible.',
  'Prefer conditional original SDK/client plus selected backend; separate Workbench/Launcher execution from Connect publication/scheduling.',
  'Select supported Workbench/Launcher/Connect and SDK builds, backend, privilege/network/output profile; qualify nonzero exits, missing artifacts, kill/cancel races and conformance coverage.')]

def prepare():
    assert not BASE.exists();BASE.mkdir()
    audit=read(READER/'reader/source-audit.json');verify_bindings(audit);sources={s['integrated_citation_key']:s for s in audit['sources']}
    assert exact.calculate()==read(PRIOR/'exact-results.json')
    write(BASE/'exact-replay.json',exact.calculate())
    plan=dict(status='reviewed_for_documentary_comparison',steps=['Resolve eight concrete vendor families, retaining Workbench/Connect subprofiles.','Reuse authenticated integrated originals with exact temporal and edition limitations.','Contrast vendor strengths with actual narrow local runtime, proposed adapters and remaining gaps.','Record incomplete edition comparison as inconclusive; no invented transaction, price or runtime.','Bind existing integrated sections; no new manuscript depth claimed; continue ready work.'],risks=['Do not collapse four recently reviewed client families into the entire shortlist.','Do not promote current mutable manuals or client versions to cutoff server evidence.','A local recovery fixture is not commercial-platform equivalence.'])
    write(BASE/'plan-review.json',plan)
    p=ROOT/'src/causalbank/operation_service_v12.py';lines=p.read_text().splitlines()
    spans=[(1,31),(64,75),(95,137)];current=dict(mode='read_only_current_source_plus_preserved_historical_trial',source=ref(p,'Current dispatcher and explicit unsupported paths'),inspected_anchors=[dict(lines=[a,b],text=chr(10).join(lines[a-1:b])) for a,b in spans],historical_evidence=[ref(ROOT/n,'Preserved scoped local implementation and trials') for n in ['docs/program/master/work/E01-v2/review.md','docs/program/master/work/E01-v2/recovery.json','docs/program/repair-v12/work/IN04/review.md','docs/program/repair-v12/work/IN04/implementation-manifest.json','docs/program/repair-v12/work/IN04/transport-checks.json','docs/program/repair-v12/work/IN04/fault-trials.json']],finding='Current dispatcher exposes declared graph syntax, supplied-DAG back-door expression, supplied-moment Gaussian residual inversion, quadratic sensitivity and clock diagnostics. Preserved IN04 trials establish scoped local library/CLI/MCP parity, durable artifacts and local faults; they do not establish these commercial integrations.',limitations=['No rerun or new platform performance evidence in this comparison.','Single local operator model; no bank, multi-tenant, multi-host or commercial-platform acceptance.'])
    verify_bindings(current);write(BASE/'current-capability-review.json',current)
    vendors=[]
    for family,keys,edition,strength,use,route,gap in PROFILES:
        selected=[sources[k] for k in keys]
        vendors.append(dict(family=family,source_records=selected,edition_version_scope=edition,documented_strength=strength,use_case_comparison=use,proposed_choice=route,current_capability=current['finding'],proposed_capability='Typed original-platform worker preserving request/target/data/clock/artifact identities, full native outcomes and scientific acceptance separately.',remaining_gap=gap,edition_acceptance='inconclusive',runtime_status='not evaluated',absence_claim=False,integration_allowed=False,price_evidence=dict(status='unavailable_in_inspected_evidence',amount=None,currency=None,quote=None),deployment_and_rights='Exact server entitlement, automation/export/redistribution and deployment terms remain unverified; an open client or SDK does not license a paid server.',cost_categories=['Licensed service and infrastructure','Conversion and validation','All requested work including cancellation/refusal/failure','Retries and reconciliation','Artifact storage/retention','Operations, security, maintenance and support'],next_evidence=gap+' Bind public/quoted terms and actual cost units; no vendor contact or purchase in this review.'))
    assert len(vendors)==8 and all(v['source_records'] for v in vendors)
    integration=[]
    for dirname in ['2026-10-22/computation-workflow-reader-v1','2026-10-23/detailed-workflow-reader-v2','2026-10-23/workflow-clients-reader-v2','2026-10-23/workflow-delegates-reader-v1','2026-10-24/workflow-contracts-reader-v3']:
        b=ROOT/'docs/program/execution'/dirname;p=b/'development.tex'
        assert p.exists();entry=next(x for x in audit['tex_files'] if x['path']==str(p.relative_to(ROOT)));core.bound(ROOT,entry);integration.append(dict(manuscript=entry,release=ref(b/'working-release.json','Previously published and preserved comparative treatment')))
    write(BASE/'integration-review.json',dict(status='existing_integrated_treatment_preserved',reader=ref(READER/'working-release.json','Current source-preserving reader'),sections=integration,new_manuscript_depth_claimed=False,scope='This operation consolidates candidate-specific comparisons already developed in the main document.'))
    evidence=[ref(BASE/n,'Reviewed documentary comparison') for n in ['plan-review.json','current-capability-review.json','integration-review.json','exact-replay.json']]+[ref(READER/'reader/source-audit.json','Every reused source record'),ref(PRIOR/'omissions-register.json','Current client/server omissions'),ref(ROOT/'docs/program/execution/2026-10-23/dataiku-workflow-v1/omissions-register.json','Complete inherited shortlist and temporal limits'),ref(Path(__file__),'Comparison logic')]
    trigger='Resolve each named cutoff server/API profile, full state/failure semantics, supported client/runtime matrix, entitlements and actual cost basis. Register public/generated adapter and fault trials after prototype merit; record unavailable sources locally and continue independent work.'
    limits=['All eight families retain incomplete edition/server/rights/runtime comparisons; no exhaustive market or absence finding.','Current mutable manuals and pinned client code are not authenticated historical supported server behavior.','No installation, downloaded-code execution, vendor contact, purchase or trial; no actual prices or ROI.','Preserved local historical engineering trials are narrow author evidence, not platform parity or bank acceptance.','Existing integrated manuscript treatment is bound; this register adds no counted chapter depth.']
    comparison=dict(operation_id=OP,status='inconclusive',scope='Eight-family workflow documentary comparison against narrow local capability and proposed adapters',reviewer=REVIEWER,cutoff='2026-10-07',review_date='2026-10-24',vendors=vendors,current_capability=ref(BASE/'current-capability-review.json','Observed source and historical local trials'),capability_gap='Commercial platforms document broader execution/orchestration/publication contracts. The project has a narrow local reference runtime, not a replacement platform or accepted commercial adapter. A scientific-context/refusal contract is proposed differentiation, not measured competitive advantage.',proposed_contract=ref(PRIOR/'conversion-contract.json','Original-platform typed worker requirements'),evidence=evidence,limitations=limits,revisit_trigger=trigger,capabilities=[],integration_allowed=False,bank_truth_required_for_next_public_research=False)
    verify_bindings(comparison);write(BASE/'comparison.json',comparison)
    criteria=[dict(index=0,verdict='inconclusive',finding='All eight families have traceable source/use-case discussion, but cutoff edition/server evidence is incomplete; no complete competitive qualification.'),dict(index=1,verdict='pass',finding='Missing evidence, unevaluated runtime, unavailable prices and unverified entitlement are distinct from absent capability; no fabricated transaction or native trial.')]
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,criteria=criteria,evidence=evidence+[ref(BASE/'comparison.json','All eight candidate comparisons')],limitations=limits,revisit_trigger=trigger))
    rows=['# Commercial workflow comparison','', 'Eight families; edition/runtime qualification remains inconclusive. All treatment is already integrated in the current monograph.','', '| Family | Documented strength | Main remaining evidence |','|---|---|---|']
    rows += ['| '+v['family']+' | '+v['documented_strength']+' | '+v['remaining_gap']+' |' for v in vendors]
    rows += ['',current['finding'],'','No platform price, native trial or comparative ROI is inferred.']
    (BASE/'comparison.md').write_text(chr(10).join(rows)+chr(10))
    print(json.dumps(dict(prepared=True,families=8,outcome='inconclusive',new_native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    review=read(BASE/'review.json');comparison=read(BASE/'comparison.json');verify_bindings(review);verify_bindings(comparison)
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);out=ROOT/node['outputs'][0];assert not out.exists();write(out,comparison)
    evidence=review['evidence']+[ref(BASE/'review.json','Author comparison review')]
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope=comparison['scope'],reviewer=REVIEWER,outputs=[ref(out,'Eight-family comparison')],criteria=[dict(c,evidence=evidence) for c in review['criteria']],limitations=comparison['limitations'],capabilities=[],nonexecution_reason='',revisit_trigger=comparison['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Commercial workflow receipt prepared: inconclusive')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
