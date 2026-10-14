#!/usr/bin/env python3
"""Write project-authored problem/diagram schemas and four synthetic cases."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT/'docs/program/repair-v12/work/LA02'


def obj(properties, required=None):
    return {'type':'object', 'properties':properties, 'required':list(properties) if required is None else required,
            'additionalProperties':False}


def arr(items, minimum=0, unique=False):
    return {'type':'array','items':items,'minItems':minimum, **({'uniqueItems':True} if unique else {})}


S = {'type':'string','minLength':1}
N = {'type':'number'}
NS = {'type':['string','null'],'minLength':1}
NN = {'type':['number','null']}
IDS = arr(S, unique=True)
ENUM = lambda *x: {'enum':list(x)}
REVIEW = obj({'status':ENUM('unreviewed','accepted_assumption','rejected','synthetic_fixture'), 'reviewer':NS})
EVIDENCE = obj({'id':S,'kind':ENUM('primary_source','expert_assertion','observational_data','experiment','model_proposal','project_synthetic_definition'),
                'source_identity':S,'version_date':S,'local_path':S,'sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'},
                'anchor':S,'claim':S})
VARIABLE = obj({'id':S,'definition':S,'unit':S,'measurement':ENUM('observed','latent','derived'),
                'event_time':N,'available_time':NN,'derived_from':IDS,'selection_indicator':{'type':'boolean'}})
RULE = obj({'variable':S,'operator':ENUM('eq','lt','le','gt','ge'),'threshold':N,
            'then_value':{'type':['number','string']},'else_value':{'type':['number','string']}})
ACTION = obj({'decision_id':S,'variable':S,'value':{'type':['number','string','null']},
              'rule':{'anyOf':[{'type':'null'},RULE]},'depends_on':IDS,
              'feasibility':ENUM('hypothetical','verified_by_owner','unknown','infeasible'),'evidence_refs':arr(S,1,True)})
INTERVENTION = obj({'kind':ENUM('static','dynamic'),'actions':arr(ACTION,1)})
TARGET = obj({'id':S,'family':ENUM('ATE','ATT','overlap_ATE','trimmed_ATE','policy_value','policy_contrast','population_mean'),
              'treatment':S,'outcome':S,'population':S,'target_weight_rule':S,
              'target_measure':obj({'kind':ENUM('population_uniform','treated_population','overlap_propensity','propensity_trimmed'),
                                    'trimming_bounds':{'anyOf':[{'type':'null'},{'type':'array','items':N,'minItems':2,'maxItems':2}]}}),
              'population_condition':arr(obj({'variable':S,'operator':ENUM('eq','lt','le','gt','ge'),'value':{'type':['number','string']}})),
              'horizon':obj({'origin':S,'start':N,'end':N}),
              'intervention':INTERVENTION,'comparator':INTERVENTION,
              'loss':obj({'definition':S,'unit':S,'direction':ENUM('minimize','maximize'),'discount_rule':S}),
              'adjustment':obj({'purpose':ENUM('total_effect','policy_history','unspecified'),'variables':IDS,'status':ENUM('proposed','unknown','declared_for_fixture')})})


def schemas():
    problem = obj({'schema_version':{'const':1},'problem_id':S,'provenance_mode':ENUM('synthetic_fixture','proposed_bank_analysis'),
       'business_question':S,'decision_owner':NS,'unit_of_analysis':S,
       'clock':obj({'unit':{'const':'days'},'origin_definition':S}),
       'variables':arr(VARIABLE,1),
       'decision_points':arr(obj({'id':S,'time':N,'information_set':IDS}),1),
       'estimand_alternatives':arr(TARGET,1),
       'resolution':obj({'status':ENUM('ambiguous','selected','refused'),'selected_id':NS,'reason':S,'review':REVIEW}),
       'assumptions':arr(obj({'id':S,'statement':S,'status':ENUM('hypothesis','accepted_assumption','synthetic_fixture','contradicted'),
                              'evidence_refs':arr(S,1,True),'review':REVIEW})),
       'evidence':arr(EVIDENCE,1)})
    counter = obj({'status':ENUM('not_searched','none_in_declared_scope','reported'),'scope':S,'evidence_refs':IDS})
    score = obj({'value':{'type':'number','minimum':0,'maximum':1},
                 'meaning':{'const':'uncalibrated_model_response'},'model_id':S,'prompt_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}})
    edge = obj({'id':S,'left':S,'right':S,'left_mark':ENUM('tail','arrow','circle'),
                'right_mark':ENUM('tail','arrow','circle'),'status':ENUM('possible','required'),
                'evidence_refs':arr(S,1,True),'counterevidence':counter,'review':REVIEW,
                'model_score':{'anyOf':[{'type':'null'},score]}})
    graph = obj({'id':S,'kind':ENUM('DAG','ADMG','CPDAG','PAG'),'nodes':arr(S,1,True),
                 'edges':arr(edge),'forbidden_directions':arr(obj({'source':S,'target':S,'evidence_refs':arr(S,1,True)})),
                 'assumption_ids':IDS,'estimand_ids':arr(S,1,True)})
    diagram = obj({'schema_version':{'const':1},'problem_id':S,'revision_id':S,
                   'prior_revision_sha256':{'type':['string','null'],'pattern':'^[0-9a-f]{64}$'},
                   'revision_reason':S,'models':arr(graph,1)})
    for name, schema in [('problem-schema.json',problem),('diagram-schema.json',diagram)]:
        schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema',
                       '$id':'urn:causalbank:la02:'+name,'title':'LA02 '+name})
        save(name,schema)


def save(name,value):
    (WORK/name).write_text(json.dumps(value,indent=2)+'\n')


def var(name,event,available,unit='dimensionless',latent=False,selection=False):
    return {'id':name,'definition':name.replace('_',' ')+' in the explicitly synthetic case',
            'unit':unit,'measurement':'latent' if latent else 'observed','event_time':event,
            'available_time':available,'derived_from':[],'selection_indicator':selection}


def action(d,v,value,depends=(),rule=None):
    return {'decision_id':d,'variable':v,'value':value,'depends_on':list(depends),'rule':rule,
            'feasibility':'hypothetical','evidence_refs':['case_definition']}


def target(name,treatment,outcome,intervention,comparator,population='All eligible synthetic units',end=30,family='ATE',adjustment=()):
    return {'id':name,'family':family,'treatment':treatment,'outcome':outcome,'population':population,
            'target_weight_rule':'Uniform over the declared synthetic population',
            'target_measure':{'kind':'population_uniform','trimming_bounds':None},'population_condition':[],
            'horizon':{'origin':'case decision origin','start':0,'end':end},
            'intervention':{'kind':'dynamic' if any(x['rule'] for x in intervention) else 'static','actions':intervention},
            'comparator':{'kind':'dynamic' if any(x['rule'] for x in comparator) else 'static','actions':comparator},
            'loss':{'definition':'Expected '+outcome,'unit':'case outcome units','direction':'maximize','discount_rule':'none in this finite synthetic example'},
            'adjustment':{'purpose':'policy_history' if family.startswith('policy') else 'total_effect',
                          'variables':list(adjustment),'status':'declared_for_fixture'}}


def edge(left,right,marks=('tail','arrow'),name=None):
    return {'id':name or left+'_'+right,'left':left,'right':right,'left_mark':marks[0],'right_mark':marks[1],
            'status':'possible','evidence_refs':['case_definition'],
            'counterevidence':{'status':'none_in_declared_scope','scope':'Synthetic defining model only; no bank empirical corroboration sought.','evidence_refs':[]},
            'review':{'status':'synthetic_fixture','reviewer':'Project synthetic case author'},'model_score':None}


def graph(name,kind,nodes,edges,targets):
    return {'id':name,'kind':kind,'nodes':list(nodes),'edges':edges,'forbidden_directions':[],
            'assumption_ids':['case_law'],'estimand_ids':list(targets)}


def case(name,question,variables,decisions,targets,models,selected=None):
    design = WORK/'case-design.md'
    problem={'schema_version':1,'problem_id':name,'provenance_mode':'synthetic_fixture',
       'business_question':question,'decision_owner':None,'unit_of_analysis':'Synthetic banking unit; see defining case',
       'clock':{'unit':'days','origin_definition':'Case-specific first decision, t=0'},
       'variables':variables,'decision_points':decisions,'estimand_alternatives':targets,
       'resolution':{'status':'selected' if selected else 'ambiguous','selected_id':selected,
                     'reason':'Explicit synthetic analytical choice' if selected else 'Business wording leaves distinct scientific targets open.',
                     'review':{'status':'synthetic_fixture','reviewer':'Project synthetic case author'}},
       'assumptions':[{'id':'case_law','statement':'The defining synthetic graph is a hypothesis about a possible world, not bank truth.',
                       'status':'synthetic_fixture','evidence_refs':['case_definition'],
                       'review':{'status':'synthetic_fixture','reviewer':'Project synthetic case author'}}],
       'evidence':[{'id':'case_definition','kind':'project_synthetic_definition','source_identity':'LA02 case design',
                    'version_date':'2026-10-12','local_path':str(design.relative_to(ROOT)),
                    'sha256':hashlib.sha256(design.read_bytes()).hexdigest(),'anchor':name.title()+' case definition',
                    'claim':'Defines an explicit synthetic example only.'}]}
    by_name={v['id']:v for v in variables}
    for t in targets:
        t['loss']['unit']=by_name[t['outcome']]['unit']
    diagram={'schema_version':1,'problem_id':name,'revision_id':name+'-v1','prior_revision_sha256':None,
             'revision_reason':'Initial explicit synthetic alternatives','models':models}
    return {'id':name,'problem':problem,'diagram':diagram,
            'expected_gate':'needs_review' if not selected else 'ready_for_formal_analysis',
            'qualification':'No bank or effect qualification; syntactic/semantic design fixture only.'}


def build_cases():
    cases=[]
    variables=[var('market',-1,-1),var('risk',-1,-1),var('offer',0,0,'basis points'),
               var('balance',30,31,'CNY'),var('net_cost',30,31,'CNY')]
    targets=[target('balance_response','offer','balance',[action('d0','offer',25)],[action('d0','offer',0)],adjustment=['market','risk']),
             target('net_cost_change','offer','net_cost',[action('d0','offer',25)],[action('d0','offer',0)],adjustment=['market','risk'])]
    targets[1]['loss']['direction']='minimize'
    names=[v['id'] for v in variables]
    edges=[edge('market','offer'),edge('market','balance'),edge('risk','offer'),edge('risk','balance'),
           edge('offer','balance'),edge('offer','net_cost'),edge('balance','net_cost')]
    cases.append(case('funding','Should we increase the deposit offer?',variables,
                     [{'id':'d0','time':0,'information_set':['market','risk']}],targets,
                     [graph('sufficient','DAG',names,edges,[t['id'] for t in targets]),
                      graph('unmeasured_response','ADMG',names,deepcopy(edges)+[edge('offer','balance',('arrow','arrow'),'hidden_offer_balance')],[t['id'] for t in targets])]))
    variables=[var('L0',-1,-1),var('A0',0,0),var('L1',10,11),var('A1',11,11),var('Y',30,31,'CNY')]
    rule={'variable':'L1','operator':'gt','threshold':0,'then_value':1,'else_value':0}
    targets=[target('dynamic_value','A0','Y',[action('d0','A0',1),action('d1','A1',None,['L1'],rule)],
                    [action('d0','A0',0),action('d1','A1',0)],family='policy_contrast',adjustment=['L0','L1']),
             target('static_total','A0','Y',[action('d0','A0',1)],[action('d0','A0',0)],adjustment=['L0'])]
    names=[v['id'] for v in variables]
    edges=[edge('L0','A0'),edge('L0','Y'),edge('A0','L1'),edge('A0','Y'),edge('L1','A1'),edge('L1','Y'),edge('A1','Y')]
    cases.append(case('servicing','Which contact policy improves net recovery?',variables,
                     [{'id':'d0','time':0,'information_set':['L0']},{'id':'d1','time':11,'information_set':['L0','A0','L1']}],targets,
                     [graph('sequential_law','DAG',names,edges,[t['id'] for t in targets])],'dynamic_value'))
    variables=[var('A',0,0),var('Y',0,0)]
    targets=[target('offer_effect','A','Y',[action('d0','A',1)],[action('d0','A',0)],end=0)]
    cases.append(case('discovery','Does an offer change the response within this coarse recorded episode?',variables,
                     [{'id':'d0','time':0,'information_set':[]}],targets,
                     [graph('equivalence_class','CPDAG',['A','Y'],[edge('A','Y',('tail','tail'))],['offer_effect']),
                      graph('forward','DAG',['A','Y'],[edge('A','Y')],['offer_effect']),
                      graph('reverse','DAG',['A','Y'],[edge('Y','A')],['offer_effect'])],'offer_effect'))
    variables=[var('link_score',-1,0),var('ownership',-1,None,latent=True),var('A',0,0),
               var('Y',30,31,'CNY'),var('S',31,32,selection=True)]
    targets=[target('all_accounts','A','Y',[action('d0','A',1)],[action('d0','A',0)]),
             target('linked_accounts','A','Y',[action('d0','A',1)],[action('d0','A',0)],population='Records with S=1; a post-treatment selected population needs additional definition')]
    targets[1]['population_condition']=[{'variable':'S','operator':'eq','value':1}]
    names=[v['id'] for v in variables]
    edges=[edge('ownership','A'),edge('ownership','Y'),edge('ownership','link_score'),edge('A','Y'),edge('A','S'),edge('Y','S')]
    cases.append(case('observation','What is the servicing effect in our linked repayment records?',variables,
                     [{'id':'d0','time':0,'information_set':['link_score']}],targets,
                     [graph('ownership_selection','DAG',names,edges,[t['id'] for t in targets])]))
    save('casebook.json',{'schema_version':1,'scope':'Four explicit project-synthetic banking cases; no authentic bank validation.', 'cases':cases})


if __name__=='__main__':
    WORK.mkdir(parents=True,exist_ok=True)
    schemas()
    build_cases()
    print('Wrote two schemas and four synthetic cases.')
