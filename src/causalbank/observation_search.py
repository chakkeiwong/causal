"""Schema-derived finite observation search with answerable ambiguity.

Profiles propose hypotheses. Supplied constraints/questions attach economic
meaning; scores never assert that an unrepresented interpretation is false.
"""
import hashlib
import itertools
import json
import numpy as np
import pandas as pd


def profile(frame,decision_units):
    columns=[c for c in frame if not c.startswith('_')]
    times=[c for c in columns if pd.api.types.is_datetime64_any_dtype(frame[c])]
    categories=[c for c in columns if pd.api.types.is_string_dtype(frame[c])]
    versions=[c for c in columns if pd.api.types.is_integer_dtype(frame[c]) and frame[c].nunique()<=20 and frame[c].min()>=0]
    values=[c for c in columns if pd.api.types.is_float_dtype(frame[c]) and np.isfinite(frame[c]).all()]
    entities=[c for c in categories if set(decision_units)<=set(frame[c])]
    return {'clocks':times,'identifier_fields':categories,'version_fields':versions,'value_fields':values,'entity_fields':entities}


def projection(frame,decisions,plan):
    entity,event,available,value=map(plan.get,['entity','event','available','value'])
    keys=list(plan['key']);version=plan['version']
    identity=[entity,*[k for k in keys if k!=entity]]
    unique=identity+([version] if version is not None else [])
    if frame.duplicated(unique).any():raise ValueError('nonunique_revision_identity')
    result=[]
    for decision in decisions:
        known=frame[(frame[entity]==decision['entity'])&(frame[available]<decision['at'])]
        if plan['revision']=='latest':
            if version is None:raise ValueError('revision_order_absent')
            known=known.sort_values(version).drop_duplicates(identity,keep='last')
        known=known[(known[event]<decision['at'])&(known[event]>=decision['begin'])]
        if plan['aggregation']=='stock' and len(known):
            known=known[known[event]==known[event].max()]
            if len(known)>1:raise ValueError('multiple_stock_values_at_one_instant')
        result.append({'decision':decision['id'],'value':float(known[value].sum()) if len(known) else None,
                       'rows':sorted(known['_row_id'].tolist())})
    return result


def propose(frame,decisions,*,realized_event_feed=False,max_key_size=2,max_candidates=5000):
    summary=profile(frame,[d['entity'] for d in decisions]);plans=[];rejected={};generated=0
    for entity in summary['entity_fields']:
        key_fields=[c for c in summary['identifier_fields'] if c!=entity]
        keys=[v for size in range(1,max_key_size+1) for v in itertools.combinations(key_fields,size)]
        for key,(event,available),value,version,aggregation in itertools.product(keys,itertools.permutations(summary['clocks'],2),summary['value_fields'],[None,*summary['version_fields']],['stock','flow']):
            for revision in (['append'] if version is None else ['latest','append']):
                generated+=1
                if generated>max_candidates:return {'status':'unsupported_search_size','profile':summary,'generated':generated,'survivors':[]}
                plan={'entity':entity,'key':list(key),'event':event,'available':available,'value':value,'version':version,'revision':revision,'aggregation':aggregation}
                if realized_event_feed and (frame[event]>frame[available]).any():
                    rejected['declared_realized_event_order']=rejected.get('declared_realized_event_order',0)+1;continue
                try: view=projection(frame,decisions,plan)
                except ValueError as error:
                    rejected[str(error)]=rejected.get(str(error),0)+1;continue
                signature={'rows':view,'value_role':value,'aggregation':aggregation}
                plans.append({'plan':plan,'view':view,'signature':hashlib.sha256(json.dumps(signature,sort_keys=True).encode()).hexdigest()})
    return {'status':'incompatible' if not plans else 'accepted_view' if len({r['signature'] for r in plans})==1 else 'abstain',
        'profile':summary,'generated':generated,'rejections':rejected,'survivors':plans,
        'scope':'Finite profiles and key-size bound; acceptance conditional on supplied constraints and grammar inclusion'}


def resolve(survivors,answers):
    return [r for r in survivors if all(r['plan'][key]==value for key,value in answers.items())]


def next_question(survivors,effects=None):
    """Minimize worst remaining effect width, then remaining material views.

    Scores rank questions; only an externally supplied answer eliminates a
    candidate. No probability of semantic correctness is inferred.
    """
    if len({r['signature'] for r in survivors})<=1:return None
    choices=[]
    for field in ['entity','event','available','value','version','revision','aggregation','key']:
        groups={}
        for i,row in enumerate(survivors):groups.setdefault(json.dumps(row['plan'][field]),[]).append(i)
        if len(groups)<2:continue
        worst_views=max(len({survivors[i]['signature'] for i in ids}) for ids in groups.values())
        worst_width=max(float(np.ptp([effects[i] for i in ids])) for ids in groups.values()) if effects is not None else 0
        choices.append((worst_width,worst_views,len(groups),field))
    if not choices:return None
    best=min(choices)
    return {'field':best[3],'worst_remaining_effect_width':best[0],'worst_remaining_views':best[1],
        'answer_source_required':True}
