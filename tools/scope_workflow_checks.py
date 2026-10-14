#!/usr/bin/env python3
"""Independent causal-path and coarsening identities for shared workflows."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.causal_workflow import AdjustmentQuery,adjustment_expression,adjustment_score,ratio_result
from causalbank.history_inference import HistoryQuery,evaluate_history
from causalbank.discovery_workflow import compatible_orders
from scope_history import generate,learn_policy


def finite_censoring():
    """Exact sum over observed stopping paths, independently of fitted routine."""
    pi=lambda l:.45+.2*l
    p=lambda l:.25+.4*l
    c=lambda l,a:.8-.1*l+.05*a
    reward=lambda t,l,a:2+l+(1-.7*l)*a+.2*t
    q1=lambda l,a:reward(1,l,a)
    v1=lambda l:(1-pi(l))*q1(l,0)+pi(l)*q1(l,1)
    q0=lambda l,a:reward(0,l,a)+.97*v1(l^a)
    v0=lambda l:(1-pi(l))*q0(l,0)+pi(l)*q0(l,1)
    truth=.6*v0(0)+.4*v0(1)
    errors={}
    for mode in ['correct_probabilities','correct_outcomes','both_wrong','omit_censoring']:
        value=0.
        for l,a,d,b,e in itertools.product(range(2),repeat=5):
            # Represent complete latent records then sum their observed score;
            # unseen b,e integrate to one when the first censoring occurs.
            next_l=l^a
            prob=(.4 if l else .6)*(p(l) if a else 1-p(l))*(c(l,a) if d else 1-c(l,a))
            prob*=(p(next_l) if b else 1-p(next_l))*(c(next_l,b) if e else 1-c(next_l,b))
            qhat=[q0,q1] if mode=='correct_outcomes' else [lambda l,a:1+.3*l+.1*a,lambda l,a:1+.2*l+.2*a]
            vh=lambda t,l:(1-pi(l))*qhat[t](l,0)+pi(l)*qhat[t](l,1)
            ph=p if mode in ['correct_probabilities','omit_censoring'] else lambda l:.5
            ch=c if mode=='correct_probabilities' else lambda l,a:1. if mode=='omit_censoring' else .9
            w0=d*(pi(l) if a else 1-pi(l))/(ph(l) if a else 1-ph(l))/ch(l,a)
            w1=w0*e*(pi(next_l) if b else 1-pi(next_l))/(ph(next_l) if b else 1-ph(next_l))/ch(next_l,b)
            score=vh(0,l)+w0*(reward(0,l,a)+.97*vh(1,next_l)-qhat[0](l,a))
            score+=.97*w1*(reward(1,next_l,b)-qhat[1](next_l,b))
            value+=prob*score
        errors[mode]=value-truth
    assert abs(errors['correct_probabilities'])<1e-12 and abs(errors['correct_outcomes'])<1e-12
    assert abs(errors['both_wrong'])>.01 and abs(errors['omit_censoring'])>.01
    return {'truth':truth,'bias':errors}


def main():
    checks={};q=AdjustmentQuery('A','Y',('X',),'household','dollars')
    chain=np.full((3,3,2),'',dtype='<U3')
    chain[0,1,0]=chain[1,0,0]=chain[1,2,0]=chain[2,1,0]='o-o'
    orders=compatible_orders(chain)
    checks['completion_excludes_new_unshielded_collider']=len(orders)==4 and all(order[-1]!=1 for order in orders)
    collider=chain.copy()
    collider[0,1,0]=collider[2,1,0]='-->'
    collider[1,0,0]=collider[1,2,0]='<--'
    orders=compatible_orders(collider)
    checks['completion_preserves_existing_collider']=len(orders)==2 and all(order[-1]==1 for order in orders)
    temporal=np.full((3,3,2),'',dtype='<U3')
    temporal[0,1,1]='-->'
    temporal[1,2,0]=temporal[2,1,0]='o-o'
    orders=compatible_orders(temporal)
    checks['completion_excludes_new_lagged_parent_collider']=len(orders)==3 and all(order.index(1)<order.index(2) for order in orders)
    checks['confounder_blocked']=adjustment_expression(q,[('X','A'),('X','Y'),('A','Y')],['X','A','Y'])['operator']=='adjustment_contrast'
    rejected=[]
    requests=[
      (AdjustmentQuery('A','Y',(),'unit','u'),[('U','A'),('U','Y'),('A','Y')],['A','Y']),
      (AdjustmentQuery('A','Y',('M',),'unit','u'),[('A','M'),('M','Y')],['A','M','Y']),
      (AdjustmentQuery('A','Y',('C',),'unit','u'),[('U','A'),('U','C'),('V','C'),('V','Y')],['A','Y','C']),
      (AdjustmentQuery('A','Y',(),'unit','u',sampling='calendar_dependence'),[('A','Y')],['A','Y']),
      (AdjustmentQuery('A','Y',(),'unit','u'),[('A','Y'),('Y','A')],['A','Y'])]
    for query,edges,nodes in requests:
        try:adjustment_expression(query,edges,nodes);rejected.append(False)
        except ValueError:rejected.append(True)
    checks['hidden_confounder_descendant_collider_dependence_cycle_rejected']=all(rejected)
    # Collider left unconditioned does not create a back-door association.
    checks['collider_unconditioned']=bool(adjustment_expression(AdjustmentQuery('A','Y',(),'u','v'),requests[2][1],['A','Y']))
    finite=finite_censoring();checks['exact_censoring_double_robustness']=True
    spec=json.loads((ROOT/'docs/studies/scope-history-spec.json').read_text());policies,_=learn_policy(spec)
    data=generate(800,4,np.random.default_rng(1));changed={k:v.copy() for k,v in data.items()}
    risk=np.column_stack((np.ones(800,bool),data['observed'][:,:-1]))
    changed['history'][:,:-1][~risk]=9876543;changed['history'][:,-1][~data['observed'][:,-1]]=9876543
    changed['reward'][~data['observed']]=9876543;changed['action'][~risk]=1
    query=HistoryQuery(4,.97,'independent-pilot')
    reg=HistGradientBoostingRegressor(max_iter=15,max_leaf_nodes=5,random_state=1);clf=LogisticRegression(max_iter=400)
    with threadpool_limits(limits=1):
        original=evaluate_history(data,query,policies,reg,clf)
        altered=evaluate_history(changed,query,policies,reg,clf)
    leak_error=float(np.max(abs(original['scores']-altered['scores'])))
    checks['post_dropout_hidden_values_unused']=leak_error==0
    checks['whole_trajectory_fold_partition']=all(len(set(tr)&set(te))==0 for tr,te in original['folds']) and sorted(np.concatenate([te for _,te in original['folds']]).tolist())==list(range(800))
    assert all(checks.values()),checks
    files=[Path(__file__),ROOT/'tools/scope_history.py',ROOT/'src/causalbank/history_inference.py',ROOT/'src/causalbank/causal_workflow.py',ROOT/'src/causalbank/discovery_workflow.py',ROOT/'docs/studies/scope-history-spec.json']
    result={'status':'pass','checks':checks,'censoring_identity':finite,'post_dropout_score_difference':leak_error,
      'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
      'scope':'Specified graphical counterexamples, exact observed stopping-path score identities, trajectory partition and hidden-value leakage. Not proof of general learner rates.'}
    (ROOT/'docs/reviews/scope-workflow-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
