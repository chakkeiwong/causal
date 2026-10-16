#!/usr/bin/env python3
"""Actual bounded semantic probes and exact proposal counterexamples; no fixes."""
import argparse
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests')]
import jsonschema
from causalbank.operation_contract_v12 import context_digest, validate_response, validate_set
from causalbank.operation_service_v12 import OperationService, REQUEST_SCHEMA, RESPONSE_SCHEMA
from causalbank.linkage_sets import weighted_sum
from causalbank.problem_contract_v12 import review_problem
from test_operation_contract_v12 import fixture
from test_operation_service_v12 import context, request
from test_problem_contract_v12 import case
from publish_latent_r_review_v2_20261013 import ref, write

BASE = ROOT/'docs/program/execution/2026-10-16/topology'
OP = 'IN.REQ.graph_and_set_topology'
OUTPUT = ROOT/'docs/program/comprehensive-v14/work'/OP/'requirement-review.json'
REVIEWER = {'name':'Codex author/coordinator','kind':'author'}
LIMITS = [
    'Proposal requirement review, not full graph recognition or a qualified causal product.',
    'Actual Python validator/service and Node JSON probes use authored fixtures, not bank observations.',
    'No R/Java/C++ adapter, MCP transport, sibling consumer, discovery package or live model execution.',
    'Exact sets and monetary values are stipulated constructions, not fitted uncertainty or bank ROI.',
    'General PAG/temporal class recognition, identification, retention and useful joint uncertainty remain research/engineering obligations.',
    'Public/generated prototype cases precede later authentic owner, clock, graph, platform and economic acceptance.',
    'Rendered visual acceptance and whole-program coverage/depth remain open.',
]


def checked(q,r):
    jsonschema.validate(q,REQUEST_SCHEMA)
    jsonschema.validate(r,RESPONSE_SCHEMA)
    return validate_response(q,r)


def outcome(call):
    try:
        value=call()
        return {'accepted':True,'returned':value}
    except (ValueError,jsonschema.ValidationError) as exc:
        return {'accepted':False,'error_type':type(exc).__name__,'message':str(exc).splitlines()[0]}


def edge(u,v,l='tail',r='arrow'):
    return {'left_node':u,'right_node':v,'left_mark':l,'right_mark':r,
        'evidence_type':'assumption','evidence_refs':[],'review_status':'unverified'}


def exact():
    # Exhaust every directed simple graph on three labelled nodes.
    nodes=('A','M','Y'); possible=[(u,v) for u in nodes for v in nodes if u!=v]
    def acyclic(arcs):
        remaining=set(nodes)
        while remaining:
            roots={v for v in remaining if not any(w==v and u in remaining for u,w in arcs)}
            if not roots:return False
            remaining-=roots
        return True
    classes={};dags=[]
    for bits in range(1<<len(possible)):
        arcs=tuple(e for i,e in enumerate(possible) if bits&(1<<i))
        if not acyclic(arcs):continue
        skeleton=tuple(sorted({tuple(sorted(e)) for e in arcs}))
        colliders=[]
        for v in nodes:
            parents=sorted(u for u,w in arcs if w==v)
            for a,b in combinations(parents,2):
                if tuple(sorted((a,b))) not in skeleton:colliders.append((a,v,b))
        key=(skeleton,tuple(sorted(colliders)))
        classes.setdefault(key,[]).append(arcs);dags.append(arcs)
    chain=classes[((('A','M'),('M','Y')),())]
    combined=tuple(sorted({a for g in chain for a in g}))
    assert len(dags)==25 and len(classes)==11 and len(chain)==3 and not acyclic(combined)
    # A common scalar multiplies both coordinates: marginals lose the relation.
    vertices=[(F(0),F(10)),(F(10),F(0))]
    true_sum=sorted({a+b for a,b in vertices})
    rectangle=[(0.,10.),(0.,10.)]
    outer=weighted_sum([[rectangle[0]],[rectangle[1]]],[1,1],-12)
    signed=weighted_sum([[(-math.inf,-2),(2,math.inf)]],[-2],1)
    encode=lambda s:[[None if math.isinf(a) else a,None if math.isinf(b) else b] for a,b in s]
    assert outer==[(-12.,8.)] and signed==[(-math.inf,-3.),(5.,math.inf)]
    disconnected=weighted_sum([[(-3,-2),(4,5)]],[-2],1)
    assert disconnected==[(-9.,-7.),(5.,7.)]
    weights=[F(4,5),F(1,5)];values=[F(40),F(-10)]
    net=sum(w*x for w,x in zip(weights,values))-5
    swapped=sum(w*x for w,x in zip(weights,reversed(values)))-5
    assert net==25 and swapped==-5
    beta=F(1,2); noise=1-beta*beta
    forward_cov=[[F(1),beta],[beta,beta*beta+noise]]
    reverse_cov=[[beta*beta+noise,beta],[beta,F(1)]]
    assert forward_cov==reverse_cov and noise==F(3,4)
    causal_nets=[20*effect-8 for effect in [beta,F(0)]]
    assert causal_nets==[F(2),F(-8)]
    return {
      'classification':'exact authored derivations; zero random draws',
      'graph_enumeration':{'nodes':list(nodes),'DAGs':len(dags),'skeleton_collider_groups':len(classes),
        'chain_members':[[list(e) for e in g] for g in chain],
        'flattened_union':[list(e) for e in combined],'flattened_is_DAG':acyclic(combined),
        'scope':'Finite three-node grouping by skeleton and unshielded colliders; no general graph recognizer.'},
      'equal_observed_Gaussian_models':{'observed_covariance':[[str(x) for x in row] for row in forward_cov],
        'forward':'A=epsilon_A;Y=A/2+epsilon_Y;independent Gaussian noises with variances1,3/4',
        'reverse':'Y=epsilon_Y;A=Y/2+epsilon_A;independent Gaussian noises with variances1,3/4',
        'effects_of_unit_A_increase':['1/2','0'],'value_per_outcome_unit_USD':20,'action_cost_USD':8,
        'net_values_USD':[str(x) for x in causal_nets],'scope':'Effects are conditional on two stipulated SCMs; equal covariance establishes equal zero-mean Gaussian laws.'},
      'coordinate_order':{'request_order':['retail','corporate'],'returned_order':['corporate','retail'],
        'units':['USD','USD'],'requested_weights':['4/5','1/5'],'original_effects':['40','-10'],
        'correct_net_USD':str(net),'positional_misread_net_USD':str(swapped)},
      'joint_region':{'definition':'(x,10-x),0<=x<=10','coordinate_projections':[[0,10],[0,10]],
        'joint_sum':[str(x) for x in true_sum],'joint_net_USD':['-2'],
        'rectangular_outer_net_USD':encode(outer),'product_is_exact_joint_image':False},
      'signed_set_image':{'map':'1-2*x','rays_input':[[None,-2],[2,None]],'rays_output':encode(signed),
        'finite_input':[[-3,-2],[4,5]],'finite_output':encode(disconnected),
        'finite_convex_hull':[-9,7],'hull_fills_unsupported_gap':[-7,5]},
      'coverage_composition':{'marginal_coverages':['19/20','19/20'],
        'union_bound':'9/10','independent_joint':'361/400','claimed_joint_19_over_20_justified':False},
    }


def probes():
    results=[]
    with tempfile.TemporaryDirectory(prefix='causal-topology-',dir=ROOT/'.runtime') as tmp:
        service=OperationService(Path(tmp))
        graph_cases=[
          ('DAG_circle','DAG',[edge('offer','value','circle','arrow')],False),
          ('DAG_cycle','DAG',[edge('offer','value'),edge('value','offer')],False),
          ('ADMG_circle_syntax_only','ADMG',[edge('offer','value','circle','arrow')],True),
          ('ADMG_cycle_syntax_only','ADMG',[edge('offer','value'),edge('value','offer')],True),
          ('CPDAG_bidirected_syntax_only','CPDAG',[edge('offer','value','arrow','arrow')],True),
          ('PAG_marks_preserved','PAG',[edge('offer','value','circle','arrow')],True),
        ]
        for name,kind,edges,expected in graph_cases:
            c=context();c['graph']={'kind':kind,'edges':edges}
            q=request('graph.review',{'review_kind':'syntax'},ctx=c)
            got=outcome(lambda:service.invoke(q));assert got['accepted']==expected,(name,got)
            if expected:
                assert got['returned']['result']['payload']['graph']==c['graph']
                assert 'full graph class not tested' in got['returned']['result']['payload']['reviewed']
            results.append({'id':name,'mode':'actual local service','request':q,'observation':got})
        c=context();c['graph']={'kind':'DAG_set','edges':[],'member_artifacts':[{
            'artifact_id':'deliberately-absent-member','sha256':'a'*64,'media_type':'application/json',
            'schema_version':'graph-set/1','role':'graph_set','bytes':10,'custody':'local'}]}
        got=service.invoke(request('graph.review',{'review_kind':'syntax'},ctx=c))
        assert got['result']['payload']['member_artifact_count']==1
        results.append({'id':'unresolved_member','mode':'actual local service','observation':got,
            'member_bytes_present':False,'scope':'Syntax counts references; it does not resolve members.'})
        for kind in ['PAG','CPDAG','ADMG','DAG_set']:
            c=context()
            c['graph']={'kind':kind,'edges':[edge('offer','value','circle','arrow')]} if kind!='DAG_set' else {
              'kind':'DAG_set','edges':[],'member_artifacts':deepcopy(results[-1]['observation']['result']['payload']['graph']['member_artifacts'])}
            got=service.invoke(request('identify.effect',{'method_id':'backdoor'},ctx=c))
            assert got['disposition']=='unsupported' and got['result'] is None
        results.append({'id':'other_graph_identification','mode':'actual local service',
            'kinds':['PAG','CPDAG','ADMG','DAG_set'],'disposition':'unsupported','numeric_result':None})
        c=context();c['variables'].append({'id':'U','role':'latent','unit':'dimensionless'})
        c['graph']['edges'] += [edge('U','offer'),edge('U','value')]
        got=service.invoke(request('identify.effect',{'method_id':'backdoor'},ctx=c))
        assert got['disposition']=='unsupported' and 'not general nonidentification' in got['result']['payload']['boundary']
        results.append({'id':'failed_backdoor_is_not_nonidentification','mode':'actual local service','observation':got})
    # Compare the stronger author problem-declaration review, preserving its scope.
    p=case('discovery');p['diagram']['models']=p['diagram']['models'][:1]
    p['diagram']['models'][0]['kind']='ADMG';p['diagram']['models'][0]['edges'][0]['left_mark']='circle'
    strong=review_problem(p['problem'],p['diagram'])
    assert any('marks cannot represent ADMG' in x for x in strong['errors'])
    results.append({'id':'problem_review_rejects_ADMG_circle','mode':'actual local declaration review','observation':strong})
    # Generic payload carries an explicit order; current checks do not bind it.
    q,r=fixture();q['scientific_context']['units']=['USD','USD']
    q['scientific_context']['population']['definition']='Declared coordinate order: retail, corporate'
    r['context_sha256']=context_digest(q['scientific_context'])
    r['result'].update(units=['USD','USD'],estimate=[-10,40],
      coordinate_sets=[{'topology':'finite_interval','intervals':[[x,x]]} for x in [-10,40]],
      payload={'coordinate_order':['corporate','retail']})
    assert checked(q,r)==r
    results.append({'id':'same_unit_order_mismatch_admitted','mode':'actual schema and semantic validation',
        'request':q,'response':r,'accepted':True,'scope':'No bound coordinate ID/order vector; no claim that validation proves numeric truth.'})
    cases=[{'topology':'unknown','intervals':None},{'topology':'empty','intervals':[]},
      {'topology':'whole_line','intervals':[[None,None]]},{'topology':'unbounded_union','intervals':[[None,-2],[2,None]]},
      {'topology':'finite_union','intervals':[[-3,-2],[4,5]]},{'topology':'finite_interval','intervals':[[3,3]]}]
    for value in cases:validate_set(value)
    bad=[{'topology':'empty','intervals':None},{'topology':'finite_union','intervals':[[0,2],[1,3]]},
         {'topology':'finite_interval','intervals':[[2,1]]},{'topology':'finite_interval','intervals':[[None,None]]}]
    rejects=[outcome(lambda value=value:validate_set(value)) for value in bad]
    assert all(not x['accepted'] for x in rejects)
    results.append({'id':'topology_states','mode':'actual semantic validation','accepted_values':cases,'rejections':rejects})
    return {'mode':'actual local execution on authored fixtures','results':results,
            'source':ref(Path(__file__),'probes and exact authored references'),'limitations':LIMITS}


def node_probes():
    js=BASE/'json-roundtrip.js'
    def roundtrip(value):
        p=subprocess.run(['node',str(js)],input=json.dumps(value,allow_nan=False),
            text=True,capture_output=True,check=True,timeout=10)
        return json.loads(p.stdout)
    sets=[{'topology':'unknown','intervals':None},{'topology':'empty','intervals':[]},
      {'topology':'whole_line','intervals':[[None,None]]},
      {'topology':'unbounded_union','intervals':[[None,-2],[2,None]]},
      {'topology':'finite_union','intervals':[[-3,-2],[4,5]]}]
    structural={'graph':{'kind':'PAG','edges':[edge('offer','value','circle','arrow')]},
      'sets':sets,'exact_identifier':'9007199254740993','member_sha256':'a'*64}
    assert roundtrip(structural)==structural
    n=2**53+1;q,r=fixture();r['result'].update(estimate=[n],coordinate_sets=[{'topology':'finite_interval','intervals':[[n,n]]}])
    checked(q,r);numeric=roundtrip({'request':q,'response':r})
    checked(numeric['request'],numeric['response'])
    m=numeric['response']['result']['estimate'][0]
    assert m==2**53 and m!=n
    q,r=fixture();q['scientific_context']['horizon']['value']=12.0
    r['context_sha256']=context_digest(q['scientific_context']);checked(q,r)
    types=roundtrip({'request':q,'response':r})
    rejected=outcome(lambda:checked(types['request'],types['response']))
    assert not rejected['accepted'] and 'context changed' in rejected['message']
    return {'mode':'actual Python-to-Node-to-Python JSON execution; generic codec only',
      'runtime':{'python':platform.python_version(),'node':subprocess.check_output(['node','--version'],text=True,timeout=10).strip(),
        'java_compiler':shutil.which('javac')},
      'structural':{'input':structural,'output':roundtrip(structural),'preserved':True},
      'unsafe_integer':{'input_estimate':n,'output_estimate':m,'both_validated':True,
        'input_singleton':[n,n],'output_singleton':numeric['response']['result']['coordinate_sets'][0]['intervals'][0],
        'remedy':'Reject unsafe numeric integers or use exact typed decimal strings; string identifier preserved.'},
      'integral_float_context':{'before_value':12.0,'after_value':types['request']['scientific_context']['horizon']['value'],
        'before_digest':r['context_sha256'],'after_digest':context_digest(types['request']['scientific_context']),
        'response_validation':rejected,'remedy':'Specify a shared canonical number/Unicode/key encoding, or hash retained canonical context bytes.'},
      'evidence':[ref(js,'Exact parse/stringify program'),ref(Path(__file__),'Python driver and assertions')],
      'limitations':LIMITS}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['exact','probes','node']);args=p.parse_args()
    value={'exact':exact,'probes':probes,'node':node_probes}[args.command]()
    dest=BASE/({'exact':'exact-results.json','probes':'runtime-probes.json','node':'node-roundtrip.json'}[args.command])
    write(dest,value)
    print(json.dumps({'saved':str(dest.relative_to(ROOT)),'mode':value.get('mode',value.get('classification'))}))
