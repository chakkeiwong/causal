#!/usr/bin/env python3
"""Frozen deterministic local library/CLI/real MCP observations; no network."""
import argparse
import asyncio
import copy
from datetime import timedelta
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.runtime_v12 import Runtime,execution_identity
from causalbank.operation_contract_v12 import context_digest,validate_response
from mcp import ClientSession
from mcp.client.stdio import stdio_client,StdioServerParameters
from mcp.shared.exceptions import McpError
from interface_examples_20261013 import context,request

BASE=ROOT/'docs/program/execution/2026-10-16/semantic-parity'
STATE=ROOT/'.runtime/semantic-parity-20261016'


def ref(p,anchor):
    return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':anchor}


def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')


def environment():
    return {'PATH':os.environ.get('PATH',''),'PYTHONPATH':str(ROOT/'src'),
        'CAUSALBANK_STATE_ROOT':str(STATE),'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1',
        'MKL_NUM_THREADS':'1','PYTHONUNBUFFERED':'1','PYTHONDONTWRITEBYTECODE':'1'}


def cli(q,op=None):
    p=subprocess.run([sys.executable,'-B','-m','causalbank.cli_v12','operation',op or q['operation']],
        input=json.dumps(q,allow_nan=False),text=True,capture_output=True,timeout=18,cwd=ROOT,env=environment())
    return {'exit_code':p.returncode,'response':json.loads(p.stdout),'stderr':p.stderr}


def library(runtime,q):
    try:return {'response':runtime.invoke(q),'exception':None}
    except Exception as e:return {'response':None,'exception':{'type':type(e).__name__,'message':str(e)[:600]}}


def prepare():
    assert not STATE.exists() and not (BASE/'protocol.json').exists()
    rt=Runtime(STATE);ctx=context();cases=[]
    def add(name,op,params,expected,c=ctx,refs=None):
        q=request('parity16-'+name,op,params,c,refs)
        path=BASE/'requests'/(name+'.json');write(path,q)
        cases.append({'name':name,'request':ref(path,'Frozen complete generated request'),'expected':expected})
    def expected(disposition='computed',status='completed',**kw):return dict(status=status,disposition=disposition,**kw)
    add('capabilities','capabilities.describe',{},expected(),c=None)
    add('graph-syntax','graph.review',{'review_kind':'syntax'},expected())
    add('backdoor','identify.effect',{'method_id':'backdoor'},expected(qualification='conditional_inference'))
    c=copy.deepcopy(ctx);c['sampling']['law']='dependent_months'
    add('dependent-sampling','identify.effect',{'method_id':'backdoor'},expected('unsupported'),c=c)
    c=copy.deepcopy(ctx);c['assumptions'][0]['status']='contradicted'
    add('contradicted-premise','identify.effect',{'method_id':'backdoor'},expected('refused'),c=c)
    add('unsupported-method','estimate.effect',{'engine_id':'absent-engine','estimator_id':'none'},expected('unsupported'))
    for name,coeff,topology,intervals in [
        ('finite',[1,0,-4],'finite_interval',[[-2.0,2.0]]),('empty',[1,0,1],'empty',[]),
        ('whole',[-1,0,-1],'whole_line',[[None,None]]),('disconnected',[-1,0,4],'unbounded_union',[[None,-2.0],[2.0,None]])]:
        data={'context_sha256':context_digest(ctx),'quadratics':[coeff]};write(BASE/'inputs'/(name+'.json'),data)
        art=rt.store.put(data,'quadratic-bounds/1','quadratic_bounds')
        add(name,'sensitivity.evaluate',{'family_id':'quadratic-sublevel'},expected(topology=topology,intervals=intervals),refs=[art])
    data={'context_sha256':context_digest(ctx),'mean':[1.,0.],'lrv':[[.01,0.],[0.,1.]],'n':100,'alpha':.05,'simultaneous':True}
    write(BASE/'inputs/moments.json',data);art=rt.store.put(data,'moment-summary/1','moment_summary')
    params={'engine_id':'reference-moment-sets','estimator_id':'gaussian-residual-inversion'}
    add('weak-moments','estimate.effect',params,expected(topology='unbounded_union',qualification='conditional_inference'),refs=[art])
    c=copy.deepcopy(ctx);c['sign_convention']='no-offer-minus-offer'
    add('changed-context','estimate.effect',params,expected('unavailable','failed',error_code='invalid_or_unavailable_input'),c=c,refs=[art])
    data={'context_sha256':context_digest(ctx),'rows':[
        {'event_at':'2026-01-01T00:00:00+00:00','available_at':'2026-01-02T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'},
        {'event_at':'2026-01-01T00:00:00+00:00','available_at':'2026-01-03T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'},
        {'event_at':'2026-01-01T00:00:00+00:00','decision_at':'2026-01-03T00:00:00+00:00'}]}
    write(BASE/'inputs/clocks.json',data);art=rt.store.put(data,'observation-rows/1','observation_rows')
    add('clock','audit.observation',{'checks':['clock']},expected(),refs=[art])
    assert len(cases)==13
    q=request('parity16-unadvertised','graph.discover',{'algorithm_id':'none','algorithm_version':'0'},ctx)
    write(BASE/'requests/unadvertised.json',q)
    invalid=request('parity16-invalid','capabilities.describe',{},None);invalid['extra_unrecognized']=True
    write(BASE/'requests/invalid.json',invalid)
    replay=request('parity16-corrupt-replay','capabilities.describe',{},None);replay['idempotency_key']='parity16-corrupt-replay'
    write(BASE/'requests/corrupt-replay.json',replay)
    write(BASE/'protocol.json',{'status':'frozen_before_execution','scope':'Deterministic generated transport demonstrations;no statistical study or bank claim',
        'script':ref(Path(__file__),'Frozen bounded harness'),'helper':ref(ROOT/'tools/interface_examples_20261013.py','Request/context constructors only;historical preparation/run functions are not called'),
        'execution_identity':execution_identity(),'sdk_versions':{n:importlib.metadata.version(n) for n in ['mcp','anyio','jsonschema']},
        'cases':cases,'batches':{'a':[x['name'] for x in cases[:6]],'b':[x['name'] for x in cases[6:]]},
        'adverse':{name:ref(BASE/'requests'/(name+'.json'),'Frozen adverse request') for name in ['unadvertised','invalid','corrupt-replay']},
        'adverse_expectations':['Unadvertised graph discovery:library/CLI canonical unsupported;MCP unknown-tool -32602',
            'Invalid schema:library exception,CLI invalid_request exit2,MCP isError with no canonical response',
            'Corrupt replay:valid request but malformed saved JSON;record actual attribution without treating it as invalid scientific input'],
        'lifecycle':'Three declared result summaries;idempotent report submission,terminal job.status and cancel-after-completion across all surfaces;bounded8-second poll',
        'stopping':'Each batch runs once with25-second MCP call timeout and80-second outer timeout;any failure persists and requires a successor attempt',
        'environment':'Local stdio in the existing installed environment;documented sandbox wakeup failure reproduced separately',
        'limits':['No network,live models,sibling writes or new implementation','Only selected deterministic cases and9 advertised operations',
            'No HTTP,multi-tenant,remote exactly-once,modern protocol,bank performance or external owner acceptance']})
    print(json.dumps({'prepared_cases':13,'adverse_cases':3,'state':str(STATE.relative_to(ROOT))}))


def protocol():
    p=json.loads((BASE/'protocol.json').read_text())
    assert p['script']['sha256']==ref(Path(__file__),'')['sha256'] and p['execution_identity']==execution_identity()
    for c in p['cases']:assert c['request']['sha256']==ref(ROOT/c['request']['path'],'')['sha256']
    return p


async def scientific(session,rt,p,batch):
    rows=[]
    for c in p['cases']:
        if c['name'] not in p['batches'][batch]:continue
        q=json.loads((ROOT/c['request']['path']).read_text());a=rt.invoke(q);b=cli(q)
        m=await session.call_tool('causal_'+q['operation'].replace('.','_'),arguments=q)
        e=c['expected'];checks={'canonical_equal':a==b['response']==m.structuredContent,
            'mcp_text_equal':bool(m.content) and json.loads(m.content[0].text)==a,
            'status':a['status']==e['status'],'disposition':a['disposition']==e['disposition'],
            'cli_exit':b['exit_code']==(4 if e['status']=='failed' else 0),
            'mcp_is_error':m.isError==(e['status'] in {'failed','rejected'})}
        if 'qualification' in e:checks['qualification']=a['qualification']['level']==e['qualification']
        if 'topology' in e:checks['topology']=a['result']['coordinate_sets'][0]['topology']==e['topology']
        if 'intervals' in e:
            checks['independent_algebra']=a['result']['coordinate_sets'][0]['intervals']==e['intervals']
            checks['nonprobabilistic']=a['result']['uncertainty']['coverage']=='none' and a['result']['uncertainty']['level'] is None
        if 'error_code' in e:checks['error_code']=a['error']['code']==e['error_code']
        if c['name']=='clock':checks['clock_failures']=a['result']['payload']['clock_failures']==[1,2]
        if c['name']=='graph-syntax':checks['graph_preserved']=a['result']['payload']['graph']==q['scientific_context']['graph']
        if c['name']=='capabilities':checks['nine_operations']=len(a['result']['payload']['implemented'])==9
        validate_response(q,a)
        path=BASE/'observed'/(c['name']+'.json');write(path,{'label':'actual_library_cli_and_MCP_stdio','request':c['request'],
            'library':a,'cli':b,'mcp':m.model_dump(mode='json',by_alias=True),'checks':checks})
        rows.append(ref(path,'Actual complete responses'))
        print(json.dumps({'case':c['name'],'checks_pass':all(checks.values()),'disposition':a['disposition']}),flush=True)
        assert all(checks.values()),c['name']
    return {'cases':rows,'status':'pass'}


async def adverse(session,rt,p):
    rows=[]
    for name in ['unadvertised','invalid','corrupt-replay']:
        q=json.loads((ROOT/p['adverse'][name]['path']).read_text());saved=None;slot=None
        if name=='corrupt-replay':
            good=rt.invoke(q);assert good['status']=='completed'
            slot=rt.cache/(hashlib.sha256(q['idempotency_key'].encode()).hexdigest()+'.json')
            saved=slot.read_bytes();(BASE/'replay-before.json').write_bytes(saved);slot.write_text('{')
        try:
            a=library(rt,q);b=cli(q)
            try:
                m=await session.call_tool('causal_'+q['operation'].replace('.','_'),arguments=q)
                observed={'tool_result':m.model_dump(mode='json',by_alias=True),'protocol_error':None}
            except McpError as e:observed={'tool_result':None,'protocol_error':e.error.model_dump(mode='json')}
            if name=='unadvertised':
                checks={'local_unsupported':a['response']==b['response'] and a['response']['disposition']=='unsupported',
                    'cli_exit_zero':b['exit_code']==0,'mcp_unknown_tool':observed['protocol_error']['code']==-32602}
                finding='Capability-set asymmetry is observed;MCP does not advertise the unimplemented operation. Use capability negotiation before dispatch.'
            else:
                checks={'library_exception':a['exception'] is not None,
                    'cli_invalid_request':b['exit_code']==2 and b['response']['error']['code']=='invalid_request',
                    'mcp_tool_error':observed['tool_result']['isError'] and observed['tool_result'].get('structuredContent') is None}
                finding=('Invalid generated schema is correctly rejected at each surface,with different transport wrappers.' if name=='invalid' else
                    'Valid request plus corrupt stored replay is attributed to invalid request by CLI and MCP broad ValueError handlers. This is an error-classification gap,not a scientific refusal or caller-input defect.')
            path=BASE/'observed'/(name+'.json');write(path,{'label':'actual_local_adverse_trial','request':p['adverse'][name],
                'library':a,'cli':b,'mcp':observed,'checks':checks,'finding':finding,'injected_bytes':'{' if saved else None})
            rows.append(ref(path,'Actual adverse observations'));print(json.dumps({'case':name,'checks_match_observed_contract':all(checks.values())}),flush=True)
            assert all(checks.values()),name
        finally:
            if saved is not None:slot.write_bytes(saved)
    return {'status':'observed_with_error_classification_gap','cases':rows}


async def lifecycle(session,rt,p):
    names=['backdoor','unsupported-method','contradicted-premise'];refs=[]
    for name in names:
        result=json.loads((BASE/'observed'/(name+'.json')).read_text())['library']
        refs.append(rt.store.put(result,'causalbank.response/1.0.0','canonical_response'))
    q=request('parity16-report','report.build',{'artifact_ids':[r['artifact_id'] for r in refs]},None,refs)
    q['idempotency_key']='parity16-report-declarations'
    a=rt.invoke(q);b=cli(q);m=await session.call_tool('causal_report_build',arguments=q)
    jid=a['result']['payload']['job_id'];jq=request('parity16-status','job.status',{'job_id':jid},None)
    deadline=time.monotonic()+8;polls=[]
    while time.monotonic()<deadline:
        v=rt.invoke(jq);polls.append(v)
        if v['result']['payload']['state'] in {'completed','failed','cancelled'}:break
        await asyncio.sleep(.05)
    terminal=polls[-1];bc=cli(jq);mc=await session.call_tool('causal_job_status',arguments=jq)
    cq=request('parity16-cancel-completed','job.cancel',{'job_id':jid},None)
    ca=rt.invoke(cq);cb=cli(cq);cm=await session.call_tool('causal_job_cancel',arguments=cq)
    result_ref=terminal['result']['payload']['result_ref'];report=rt.store.get(result_ref) if result_ref else None
    checks={'submission_equal':a==b['response']==m.structuredContent,'submission_queued':a['status']=='queued',
        'status_equal':terminal==bc['response']==mc.structuredContent,
        'terminal_completed':terminal['result']['payload']['state']=='completed',
        'cancel_equal':ca==cb['response']==cm.structuredContent,
        'cancel_not_rollback':ca['result']['payload']['state']=='completed' and ca['result']['payload']['result_ref']==result_ref,
        'declarations_preserved':report is not None and [x['declared_disposition'] for x in report['summaries']]==['computed','unsupported','refused'],
        'schema_only':report is not None and all(x['verification']=='schema_only_not_causal_or_external_review' for x in report['summaries']),
        'transport_flags':all(x['exit_code']==0 for x in [b,bc,cb]) and all(not x.isError for x in [m,mc,cm])}
    path=BASE/'observed/lifecycle.json';write(path,{'label':'actual_library_cli_and_MCP_stdio','request':q,
        'submitted':a,'cli_submission':b,'mcp_submission':m.model_dump(mode='json',by_alias=True),
        'polls':polls,'terminal_cli':bc,'terminal_mcp':mc.model_dump(mode='json',by_alias=True),
        'cancel_library':ca,'cancel_cli':cb,'cancel_mcp':cm.model_dump(mode='json',by_alias=True),
        'report':report,'checks':checks})
    print(json.dumps({'case':'lifecycle','checks_pass':all(checks.values())}),flush=True)
    assert all(checks.values())
    return {'status':'pass','evidence':ref(path,'Actual report/status/cancel observations')}


async def run_async(mode):
    p=protocol();rt=Runtime(STATE)
    params=StdioServerParameters(command=sys.executable,args=['-B','-m','causalbank.mcp_server_v12'],env=environment(),cwd=str(ROOT))
    with (BASE/(mode+'-server-stderr.txt')).open('x') as errors:
        async with stdio_client(params,errlog=errors) as (read,write_stream):
            async with ClientSession(read,write_stream,read_timeout_seconds=timedelta(seconds=25)) as session:
                init=await session.initialize();listed=await session.list_tools()
                assert init.protocolVersion=='2025-11-25' and len(listed.tools)==9
                names=sorted(t.name for t in listed.tools)
                if mode in ['a','b']:observed=await scientific(session,rt,p,mode)
                elif mode=='adverse':observed=await adverse(session,rt,p)
                else:observed=await lifecycle(session,rt,p)
                observed.update(protocol=init.protocolVersion,advertised_tools=names,
                    execution_identity=execution_identity(),harness=ref(Path(__file__),'Frozen executed harness'))
                write(BASE/(mode+'-observations.json'),observed)
                print(json.dumps({'batch':mode,'status':observed['status']}),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','a','b','adverse','lifecycle']);args=p.parse_args()
    if args.command=='prepare':prepare();return
    assert not (BASE/(args.command+'-observations.json')).exists()
    try:asyncio.run(asyncio.wait_for(run_async(args.command),timeout=80))
    except BaseException as e:
        write(BASE/(args.command+'-failure.json'),{'status':'failed','type':type(e).__name__,'message':str(e)[:1200],
            'harness':ref(Path(__file__),'Preserved failed attempt'),'next_action':'Inspect saved outputs;do not rerun over observed cases;prepare successor if a harness repair is necessary.'})
        raise


if __name__=='__main__':main()
