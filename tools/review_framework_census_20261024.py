#!/usr/bin/env python3
"""Review pinned framework contracts without executing downloaded software."""
import argparse,hashlib,json
from pathlib import Path
import framework_census_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/framework-census-v1'
PRIOR=ROOT/'docs/program/execution/2026-10-24/sas-reuse-reader-v1/reader/source-audit.json'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static selected-source review and authored finite examples; no downloaded code, model, provider service or native benchmark executes.',
 'Source version declarations and pre-cutoff commit identities are not installed distributions, a resolved environment or current-release claims.',
 'Framework state, messages, stop reasons and source notices do not establish causal identification, calibrated uncertainty or complete rights.',
 'Provider/backend census, further runtime delegates, public native fixtures and measured costs remain open.',
 'No visual, independent, bank or final acceptance; no exhaustive framework market census.']
PROFILES={
 'langchain':('LangChain and its LangGraph dependency','LangChain1.4.3/core1.6.7;classic1.0.8 separately scoped;inherited LangGraph1.2.14','SW.DECISION.seed_097'),
 'autogen':('AutoGen AgentChat','AgentChat0.7.5 and matching declared core;retained maintenance notice','SW.DECISION.seed_098'),
 'semantic_kernel':('Semantic Kernel Python','Python1.45.0;other language parity unverified','SW.DECISION.seed_099'),
 'dspy':('DSPy','Source declaration3.4.0','SW.DECISION.seed_100'),
 'llama_index':('LlamaIndex with delegated workflows','Core0.14.25 and separately scoped workflows2.25.0','SW.DECISION.seed_101'),
 'haystack':('Haystack','Source declaration3.4.0-rc0 retained as prerelease','SW.DECISION.seed_102')}
SPANS={
 'exec24_framework_langchain_source_0':[(1,21)],
 'exec24_framework_langchain_source_4':[(6,37)],
 'exec24_framework_langchain_source_6':[(6,34)],
 'exec24_framework_langchain_v1_0':[(6,31)],
 'exec24_framework_langchain_v1_1':[(1237,1244),(1897,1925)],
 'exec24_framework_langchain_v1_2':[(119,161),(197,269)],
 'exec24_framework_langchain_v1_3':[(136,188),(264,353)],
 'exec24_framework_semantic_kernel_source_0':[(1,21)],
 'exec24_framework_semantic_kernel_source_2':[(1,40)],
 'exec24_framework_semantic_kernel_delegate_0':[(1,9)],
 'exec24_framework_semantic_kernel_delegate_1':[(1,21)],
 'exec24_framework_semantic_kernel_source_4':[(26,107)],
 'exec24_framework_semantic_kernel_source_6':[(370,484)],
 'exec24_framework_dspy_source_0':[(1,21)],
 'exec24_framework_dspy_source_7':[(1,34)],
 'exec24_framework_dspy_source_4':[(19,147)],
 'exec24_framework_dspy_source_3':[(75,109),(155,185)],
 'exec24_framework_dspy_source_6':[(21,106),(108,136),(163,238)],
 'exec24_framework_llama_index_source_0':[(1,21)],
 'exec24_framework_llama_index_source_7':[(36,42),(75,86)],
 'exec24_framework_llama_index_source_2':[(492,552),(554,593)],
 'exec24_framework_llama_index_source_3':[(150,187)],
 'exec24_framework_llama_index_source_5':[(1,1)],
 'exec24_framework_llama_index_source_6':[(1,1)],
 'exec24_framework_haystack_source_0':[(1,17),(88,119)],
 'exec24_framework_haystack_source_6':[(6,16),(162,173)],
 'exec24_framework_haystack_delegate_0':[(1,1)],
 'exec24_framework_haystack_source_2':[(390,455),(898,921),(1157,1193)],
 'exec24_framework_haystack_source_5':[(200,265)],
 'exec24_framework_workflows_source_0':[(1,21)],
 'exec24_framework_workflows_source_1':[(24,41)],
 'exec24_framework_workflows_source_2':[(100,124)],
 'exec24_framework_workflows_source_3':[(812,895)],
 'exec24_framework_workflows_source_4':[(202,226)]}
CLAIMS={
 'langchain':['Modern,core and classic package declarations are distinct;modern LangChain declares a LangGraph range.',
  'The modern factory constructs a StateGraph and passes checkpointer/store/interrupt settings;recursion limit is not a monetary or wall-time budget.',
  'Retry middleware counts initial plus retry attempts;GraphBubbleUp propagates and nonmatching exceptions re-raise.',
  'Exhausted tool retries can return status=error ToolMessage;exhausted model retries can return assistant error text;error-raising routes also exist.'],
 'semantic_kernel':['Python version is1.45.0;no cross-language parity claim.',
  'Function-choice filters and auto-invoke settings control exposed functions;kernel checks required/unexpected arguments and invokes filters.',
  'Selected automatic function handler converts ordinary exceptions to function-result error text;termination is a separate context flag.'],
 'dspy':['Source declares3.4.0;selected root notice is MIT.',
  'ReAct records tool exceptions in the trajectory and performs extraction after loop exit;returned prediction is not proof all scientific tools succeeded.',
  'Returned evaluations fill missing results with failure_score and use full devset denominator;error-threshold cancellation can raise before an aggregate.',
  'Parallel straggler resubmission is tracked by Future identity while results are indexed by input;per-item retry cap is not proved by the nearby comment alone.'],
 'llama_index':['Core declares0.14.25 and workflows>=2.14.0,<3;workflow modules re-export separate runtime.',
  'Iteration limit can raise or trigger final generation;returned summaries require separate scientific status.',
  'Function-agent source distinguishes return_direct and handoff;selected typed/structured paths do not establish scientific semantics.'],
 'haystack':['Selected declaration is3.4.0-rc0 with Apache2.0 root notice;not promoted to stable release.',
  'Agent exposes ordered hooks,state mappings,concurrency and max steps;max-step exit returns current state with a distinct exit reason.',
  'Selected tool exit logic rejects an errored exit-condition tool;tool failure can be returned as a chat message.',
  'General function tools have no formal output-name schema by default;specialized component tools can override it.'],
 'workflows':['Repository redirect resolves to run-llama/llama-agents;selected package declares workflows2.25.0 and MIT.',
  'Constructor documentation defines timeout as known-alive processed-journal time excluding specified downtime;not an external wall deadline.',
  'cancel_run signals its external adapter and catches timeout/cancellation/other exceptions;return alone is not verified remote side-effect termination.',
  'Retry policy separates predicates,delay and stop;selected default is three attempts with five-second delays.']}

def prepare():
    assert not (BASE/'review.json').exists()
    inventories=[read(BASE/n) for n in ['acquisition-review.json','supplementary-acquisition-review.json','workflow-acquisition-review.json']]
    rows=[r for d in inventories for r in d['records']];assert len(rows)==50
    records={};uninspected=[]
    for r in rows:
        verify_bindings(r);p=ROOT/r['local_copy']['path'];data=p.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['git_blob_sha1']
        key=r['request']['id'];ranges=SPANS.get(key,[])
        if not ranges:uninspected.append(dict(id=key,path=r['upstream_path'],reason='Acquired inventory only;no new technical claim from uninspected file'));continue
        lines=data.decode().split('\n');anchors=[]
        for lo,hi in ranges:
            assert 1<=lo<=hi<=len(lines),(key,lo,hi,len(lines))
            text='\n'.join(lines[lo-1:hi]);anchors.append(dict(upstream_path=r['upstream_path'],lines=[lo,hi],excerpt_sha256=hashlib.sha256(text.encode()).hexdigest(),inspection='Author substantive source inspection;no execution'))
        record=dict(source_identity=r['request']['url'],version_date=r['commit_date']+'; '+r['revision'],local_copy=ref(p,'Authenticated original selected source'),git_blob_sha1=r['git_blob_sha1'],inspected_anchors=anchors,technical_inspected=True,executed=False)
        records.setdefault(r['candidate'],[]).append(record)
    prior=read(PRIOR);inherited=[s for s in prior['sources'] if s['integrated_citation_key'] in ['v12_la04_autogen','v12_la04_langgraph']];assert len(inherited)==2
    for s in inherited:verify_bindings(s)
    inherited_spans=[]
    for name,spans in [('v12_la04_langgraph_source_2.txt',[(893,915)]),('v12_la04_autogen_readme.txt',[(18,25)]),('v12_la04_autogen_source_1.txt',[(109,146),(1630,1639)]),('v12_la04_autogen_source_2.txt',[(5,19)])]:
        p=ROOT/'docs/literature/raw'/name;lines=p.read_text().split('\n')
        inherited_spans.append(dict(local_copy=ref(p,'Reinspected preserved original'),anchors=[dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()) for lo,hi in spans]))
    write(BASE/'inherited-review-bindings.json',dict(prior_audit=ref(PRIOR,'Predecessor audit'),sources=inherited,reinspected=inherited_spans))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_static_contracts',records=records,claims=CLAIMS,uninspected_acquired_files=uninspected,evidence=[ref(BASE/n,'Identity and acquisition') for n in ['identities.json','workflow-identity.json','acquisition-review.json','supplementary-acquisition-review.json','workflow-acquisition-review.json','inherited-review-bindings.json']],limits=LIMITS))
    assert exact.calculate()==read(BASE/'exact-results.json')
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_examples',evidence=[ref(Path(exact.__file__),'Independent code'),ref(BASE/'exact-results.json','Exact outputs'),ref(BASE/'development.tex','Derivations and assumptions')],findings=['Returned-qualified fractions3/4versus3/5 use distinct denominators.','Specified repeated actions1500versus500USD;non-atomic reservations overspend40USD.','Active40seconds plus downtime3600seconds gives wall3640seconds.','Different uncertainty sets share midpoint0;scalar cannot uniquely invert projection.','Two Future retry identities can share one logical input;this is not a native liveness result.','24000USD over1000/800/600 gives24/30/40USD.'],native_execution=False))
    choices=[]
    for key,(name,version,op) in PROFILES.items():
        constraints={
         'langchain':'Preserve graph/checkpointer identity,interrupt replay,logical action and attempt keys,tool-error status and model-error text;separate classic and modern.',
         'autogen':'Isolate stateful agent instances,preserve model-context versus scientific state,tool concurrency and reflection costs;inspect migration target independently.',
         'semantic_kernel':'Name Python artifact and connector;preserve filter choice,argument errors,function result status and termination;do not infer other-language parity.',
         'dspy':'Fix task/scorer/splits and failure score;retain full devset and all submissions;test extraction after partial work and Future-versus-input retry identity.',
         'llama_index':'Pin core and delegated workflow runtime;preserve iteration exit,scientific status,clock definition,cancellation and external-job reconciliation.',
         'haystack':'Retain prerelease identity,ordered hooks,state mappings,output schemas,tool errors,step exit reasons and complete work counts.'}[key]
        next_action='Retain bounded reference; '+constraints+' Resolve exact native environment,dependency/provider rights and prices;run shared public scientific/refusal/replay/fault fixtures before native admission.'
        c=dict(operation=op,candidate=name,canonical_candidate=name,decision='reference',selected_version=version,selected_revision='Exact original identities in primary-review and inherited bindings',reason='Concrete selected contracts support comparison;scientific and native qualifications remain separate.',alternatives=[dict(route='adopt',decision='defer',reason='Orchestration does not qualify the causal product or full environment'),dict(route='integrate',decision='conditional',reason=constraints),dict(route='port',decision='selective_conditional',reason='Inspect actual component notices/dependencies and compare maintenance with direct reuse'),dict(route='reference',decision='retain',reason='Authenticated original technical contracts'),dict(route='reject',decision='restricted',reason='Reject unsupported causal,success,replay,deadline and parity claims')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Business question,graph,intervention,target and assumptions'),('Statistical','Scorer,split,uncertainty,dependence and loss'),('Adapter','Types,refusals,logical IDs,replay and partial results'),('Platform','Environment,rights,deadlines,budgets and recovery')]],costs=dict(prices='Unmeasured;24000USD authored example',categories=['model calls','tools','retries','duplicates','partial work','human review','maintenance']),maintenance='Exact pinned source;current support and solved environment separate',conversion_contract=constraints,revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
        write(BASE/(key+'-choice.json'),c);choices.append(c)
    write(BASE/'omissions-register.json',dict(global_blocker=False,remaining=['Named hosted/local backend comparison','Remaining runtime/provider/connector delegates','Resolved and tested distributions','Full dependency and provider terms','Native public task/fault fixtures and measured costs','Visual and final acceptance'],acquired_uninspected=uninspected,known_routes=['Bounded primary-source acquisition and exact component comparison','Shared public scientific and refusal oracles','Fault/replay/deadline and complete-cost experiments'],unknown_without_information=['Business assignment truth or omitted confounding','Lost uncertainty or ambiguous graph direction','Universal dependent/adaptive inference guarantees'],next_action='Integrate this preserving comparison and six reference dispositions;continue independent backend and frontier original review;do not close L6 on framework sources alone.'))
    sources=[]
    for key,rs in records.items():
        first=rs[0];sources.append(dict(integrated_citation_key='exec24_framework_'+key,kind='software_primary_sources',title={'langchain':'LangChain modern,core and classic execution and retry contracts','semantic_kernel':'Semantic Kernel Python filters,arguments and function-result contracts','dspy':'DSPy trajectory,evaluation and parallel submission contracts','llama_index':'LlamaIndex iteration,output and delegated workflow contracts','haystack':'Haystack prerelease hook,state,tool and stop contracts','workflows':'LlamaIndex workflows delegated timing,cancellation and retry contracts'}[key],author=key+' project contributors',year=2026,source_identity=first['source_identity'],version_date=first['version_date'],local_copy=first['local_copy'],records=rs,inspected_anchors=[a for r in rs for a in r['inspected_anchors']],supported_claims=CLAIMS[key],limitations=LIMITS))
    assert len(sources)==6
    sources.append(dict(integrated_citation_key='exec24_framework_contracts',kind='project_evidence_not_scholarly_paper',title='Agent-framework scientific state,replay,clock,budget and evaluation contracts',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;static selected sources and exact authored examples',local_copy=ref(BASE/'mathematical-review.json','Exact authored reference'),inspected_anchors=[ref(BASE/n,'Reviewed claim') for n in ['primary-review.json','inherited-review-bindings.json','omissions-register.json']]+[ref(BASE/(k+'-choice.json'),'Candidate-specific disposition') for k in PROFILES],supported_claims=['Connected source-specific comparisons and six bounded reference choices','Exact replay,budget,clock,uncertainty and denominator witnesses','Shared public qualification and component-specific integration proposal'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=0,inherited_records_preserved=2,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_source_wave',evidence=[ref(BASE/n,'Reviewed plan/evidence') for n in ['plan.md','integration-outline.md','primary-review.json','mathematical-review.json','omissions-register.json']],findings=['Actual dependencies and repository redirect traced;modern/classic and prerelease profiles remain distinct.','References and conditional integrations separated from native qualification.','Provider and remaining delegate coverage remain open;no exhaustive L6 claim.','Independent source work proceeds while canonical publication remains sequential.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_comparison',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Investment implications')],findings=['Business-to-causal question,graphs,tools,uncertainty and recovery connected for each candidate.','Default behaviors scoped to inspected paths;not all provider/language profiles.','Finite witnesses not labeled native findings or bank value.'],visual_acceptance=False))
    review=dict(status='pass_for_bounded_framework_reference_wave',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['primary-review.json','inherited-review-bindings.json','source-audit.json','mathematical-review.json','exact-results.json','omissions-register.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(BASE/(k+'-choice.json'),'Candidate choice') for k in PROFILES]+[ref(Path(__file__),'Review procedure')],findings=['Six new primary audit records and one authored record;two inherited records preserved.','Six reference dispositions with precise ownership,costs,conversion and revisit conditions.','No native,whole-L6,visual or final acceptance.'],limitations=LIMITS)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(primary_profiles=6,new_records=7,reference_decisions=6,uninspected_files=len(uninspected),native_execution=False)))

def receipt(key):
    name,_,op=PROFILES[key];state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==op
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,op)
    value=read(BASE/(key+'-choice.json'));value.update(status='pass',scope='Bounded '+name+' proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    out=ROOT/node['outputs'][0];write(out,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','primary-review.json',key+'-choice.json','mathematical-review.json','omissions-register.json']]
    findings=['Concrete component/revision,dependency and notice identities reviewed.','Adopt/integrate/port/reference/reject alternatives,owners,costs and conversion explicit.','Bounded reference choice;native and scientific qualification remain separately gated.']
    r=run.ledger.receipt_template(node);r.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger']);run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/(key+'-operation-receipt.json'),r);print(name+' receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare']+list(PROFILES));a=p.parse_args();prepare() if a.command=='prepare' else receipt(a.command)
