#!/usr/bin/env python3
"""Proposed consumer/reference calculations; does not change the actual service."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from causalbank.operation_contract_v12 import validate_response,finite_json


def parse(text,limit=1000000):
    if len(text.encode('utf-8'))>limit:raise ValueError('byte_limit')
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate_key')
            result[key]=value
        return result
    def constant(value):raise ValueError('nonfinite_token')
    result=json.loads(text,object_pairs_hook=pairs,parse_constant=constant)
    finite_json(result)
    return result


def identity(value):
    finite_json(value)
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)


def meaning(request,response):
    validate_response(request,response)
    if response['status'] in {'failed','rejected'}:return 'execution_failure'
    result=response['result']
    if result and result['kind']=='job':
        state=result['payload']['state']
        if state not in {'queued','running','completed','failed','cancelled'}:raise ValueError('unknown_job_state')
        return 'job_'+state
    if response['disposition']!='computed':return 'scientific_'+response['disposition']
    if response['status']!='completed':raise ValueError('incomplete_result')
    if result['kind']=='identification':return 'conditional_expression'
    if result['kind']=='effect':
        sets=result['coordinate_sets']
        if sets is not None:return 'effect_sets:'+','.join(x['topology'] for x in sets)
        return 'effect_estimate' if result['estimate'] is not None else 'effect_without_numeric_value'
    return 'typed_'+result['kind']


def calculate():
    source=ROOT/'docs/program/execution/2026-10-13/interfaces/examples'
    cases={};fixtures={}
    for name in ['backdoor','unsupported-discovery','unsupported-sampling','contradicted-premise','finite','empty','whole','disconnected','weak-moments','changed-context','clock']:
        row=json.loads((source/'results'/f'{name}.json').read_text())
        request=json.loads((ROOT/row['request']['path']).read_text())
        response=row['library'];fixtures[name]=(request,response)
        assert response==row['cli']['response']
        cases[name]=meaning(request,response)
    rejected=[]
    for label,text in [('duplicate','{"status":"completed","status":"failed"}'),
                       ('nan','{"estimate":NaN}'),('overflow','{"estimate":1e999}'),
                       ('trailing','{"x":1} unrelated'),('banner','ready\n{"x":1}')]:
        try:parse(text)
        except (ValueError,TypeError):rejected.append(label)
        else:raise AssertionError(label)
    try:parse('{"x":1}',limit=2)
    except ValueError:rejected.append('byte_limit')
    else:raise AssertionError('byte_limit')
    req,good=fixtures['backdoor']
    for label,field,value in [('wrong_id','request_id','other'),('wrong_operation','operation','estimate.effect'),('wrong_context','context_sha256','0'*64)]:
        bad=deepcopy(good);bad[field]=value
        try:meaning(req,bad)
        except ValueError:rejected.append(label)
        else:raise AssertionError(label)
    req,response=fixtures['empty'];bad=deepcopy(response)
    bad['result']['coordinate_sets'][0]['topology']='whole_line'
    try:meaning(req,bad)
    except ValueError:rejected.append('wrong_topology')
    else:raise AssertionError('wrong_topology')
    req,response=fixtures['unsupported-discovery'];bad=deepcopy(response)
    bad['result']=deepcopy(fixtures['finite'][1]['result'])
    try:meaning(req,bad)
    except ValueError:rejected.append('unsupported_with_number')
    else:raise AssertionError('unsupported_with_number')
    structured=deepcopy(fixtures['backdoor'][1]);same=parse(json.dumps(structured,indent=2))
    assert identity(same)==identity(structured)
    conflicting=deepcopy(same);conflicting['qualification']['level']='none'
    assert identity(conflicting)!=identity(structured)
    # A proposed consumer treats this conflict as an integrity failure.
    rejected.append('structured_text_conflict')
    # These are newly authored valid-shaped job fixtures, not an actual job run.
    req,response=fixtures['backdoor'];req=deepcopy(req);req['operation']='job.status'
    job=deepcopy(response);job['operation']='job.status'
    job['result'].update(kind='job',payload={'state':'running'})
    running=meaning(req,job);job['result']['payload']['state']='completed'
    completed=meaning(req,job)
    assert running=='job_running' and completed=='job_completed'
    assert cases['backdoor']=='conditional_expression'
    assert cases['unsupported-discovery']=='scientific_unsupported'
    assert cases['contradicted-premise']=='scientific_refused'
    assert cases['empty']=='effect_sets:empty' and cases['whole']=='effect_sets:whole_line'
    assert cases['disconnected']=='effect_sets:unbounded_union'
    # Reachability over immutable dependency identities, with two live roots.
    deps={'report':['result'],'result':['data','code'],'data':[],'code':[],
          'checkpoint':['result'],'orphan':[],'old_result':['old_data'],'old_data':[]}
    roots={'report','checkpoint'};reachable=set();todo=list(roots)
    while todo:
        x=todo.pop()
        if x not in reachable:reachable.add(x);todo.extend(deps[x])
    garbage=set(deps)-reachable
    assert garbage=={'orphan','old_result','old_data'}
    arrival=[0,0,0,0,0];workers=[0,0];finish=[]
    for t in arrival:
        j=min(range(2),key=lambda i:workers[i]);end=max(t,workers[j])+3
        workers[j]=end;finish.append(end)
    assert finish==[3,3,6,6,9]
    assert sum(x<=8 for x in finish)==4
    # Independent formula for identical jobs in this deterministic burst.
    assert finish==[3*((j+2)//2) for j in range(5)]
    budget=dict(host_mib=1024,parent_mib=128,reserve_mib=128,worker_mib=256)
    admissible=(budget['host_mib']-budget['parent_mib']-budget['reserve_mib'])//budget['worker_mib']
    assert admissible==3
    # Ordered cancellation/publication abstract machine with indivisible lock section.
    transitions={}
    for events in [('cancel','publish'),('publish','cancel')]:
        state='running';public=False
        for event in events:
            if state=='running':
                if event=='cancel':state='cancelled'
                else:state='completed';public=True
        transitions[' then '.join(events)]={'state':state,'public':public}
    return dict(client={'recorded_fixtures':cases,'rejected_adverse_cases':rejected,
        'structured_text_equal':True,'job_query_completed_with_running_payload':running,
        'job_terminal_payload':completed,'scope':'Proposed finite semantic consumer, not full schema/SDK/client qualification'},
        retention={'roots':sorted(roots),'reachable':sorted(reachable),'candidate_garbage':sorted(garbage),
        'condition':'Stable root snapshot and complete immutable dependency graph; no files deleted'},
        admission={'assumed_budget':budget,'admissible_workers':admissible},
        queue={'workers':2,'service_seconds':3,'simultaneous_arrivals':5,'finishes':finish,
        'deadline_seconds':8,'on_time':4,'scope':'Deterministic stipulated burst; not measured SLO'},
        cancellation=transitions,live_transport_runs=0,bank_evidence=False)


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
