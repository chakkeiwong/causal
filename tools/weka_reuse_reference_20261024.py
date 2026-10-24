#!/usr/bin/env python3
"""Authored exact classifier/intervention witnesses; no Weka code imported."""
from fractions import Fraction as F
import json

def calculate():
    joint={}
    for u in [0,1]:
        ea=F(4,5) if u else F(1,5)
        for a in [0,1]:joint[(u,a)]=F(1,2)*(ea if a else 1-ea)
    conditional={a:sum(p for (u,b),p in joint.items() if b==a and u==1)/sum(p for (u,b),p in joint.items() if b==a) for a in [0,1]}
    observed=conditional[1]-conditional[0];true=F(0)
    assert conditional=={0:F(1,5),1:F(4,5)} and observed==F(3,5)
    alpha=F(1,2)
    smooth=lambda counts:[(n+alpha)/(sum(counts)+len(counts)*alpha) for n in counts]
    assert smooth([0,1])==[F(1,4),F(3,4)] and smooth([0,10])==[F(1,22),F(21,22)]
    selected=F(1,2)/(F(1,2)+F(1,2)*F(1,4));assert selected==F(4,5)
    # A -> B imported when dataset order B,A differs from source order A,B.
    source=['A','B'];data=['B','A'];parents={'A':[],'B':['A']}
    imported=[];attempted=[]
    for i,name in enumerate(data):
        mapped=source.index(name)
        count=len(parents[source[i]])
        attempted.append(dict(data_node=name,mapped_node=source[mapped],loop_count=count,true_count=len(parents[name])))
        if count>len(parents[name]):break
        imported.extend([[p,name] for p in parents[name][:count]])
    assert attempted[0]['loop_count']==0 and attempted[0]['true_count']==1
    assert attempted[1]['loop_count']==1 and attempted[1]['true_count']==0
    zero_vector=[0,0];assert sum(zero_vector)!=1
    return dict(native_execution=False,
        confounding=dict(joint=[dict(u=u,a=a,p=str(p)) for (u,a),p in joint.items()],
            conditional={str(a):str(p) for a,p in conditional.items()},intervention_means=['1/2','1/2'],
            observed_difference=str(observed),causal_difference=str(true),
            accounts=1000,usd_per_success=100,cost_usd=10000,naive_net_usd=str(100000*observed-10000),causal_net_usd='-10000'),
        smoothing=dict(alpha='1/2',unit_weights=[str(p) for p in smooth([0,1])],scaled_weights=[str(p) for p in smooth([0,10])],
            empty_row=[str(p) for p in smooth([0,0])],comment='Positive smoothing probabilities do not create intervention support.'),
        weighting=dict(rows=[0,1],weights=[1,9],plain_score_counts=[1,1],weighted_cpt_counts=[1,9],
            smoothed_plain=[str(p) for p in smooth([1,1])],smoothed_weighted=[str(p) for p in smooth([1,9])],
            scope='Selected plain local-score counts versus SimpleEstimator weighted counts;no native run.'),
        label_selection=dict(population_success='1/2',response_if_success='1',response_if_failure='1/4',selected_success=str(selected)),
        bif_order=dict(source_order=source,data_order=data,attempted=attempted,imported_before_invalid_index=imported,scope='Authored index reasoning,not native import'),
        failure_output=dict(vector=zero_vector,probability_simplex_valid=False),
        cost=dict(total_usd=7200,submitted=360,completed=300,qualified=240,usd_per=[str(F(7200,n)) for n in [360,300,240]]))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
