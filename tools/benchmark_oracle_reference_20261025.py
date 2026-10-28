#!/usr/bin/env python3
"""Independent finite reference witnesses; imports no third-party benchmark code."""
from collections import defaultdict
from fractions import Fraction as F
import json,math

def iv_model(never_treated_outcome):
    joint=defaultdict(F);ez={z:dict(x=F(0),y=F(0)) for z in [0,1]}
    ate=F(0)
    for u,weight in [(0,F(1,4)),(1,F(3,4))]:
        def outcome(x):return x if u==0 else (1 if x==0 else never_treated_outcome)
        ate+=weight*(outcome(1)-outcome(0))
        for z in [0,1]:
            x=(1-u)*z;y=outcome(x)
            joint[(z,x,y)]+=F(1,2)*weight
            ez[z]['x']+=weight*x;ez[z]['y']+=weight*y
    first=ez[1]['x']-ez[0]['x'];reduced=ez[1]['y']-ez[0]['y']
    return dict(joint={','.join(map(str,k)):str(v) for k,v in sorted(joint.items())},ate=str(ate),first_stage=str(first),reduced_form=str(reduced),wald=str(reduced/first),complier_effect='1')

def oracle_state(value):
    if value is True:return 'identified'
    if value is False:return 'not_identified'
    return 'unknown'

def gate(identification,prediction,valid=True):
    state=oracle_state(identification)
    if state=='unknown':return 'quarantine_unknown_oracle'
    if not valid:return 'invalid_answer'
    if state=='not_identified':return 'correct_refusal' if prediction is None else 'unsupported_estimate'
    return 'unnecessary_refusal' if prediction is None else 'score_identified_target'

def interval_oracle(lower,upper,truth,alpha):
    values=(lower,upper,truth,alpha)
    if any(isinstance(x,bool) or not isinstance(x,(int,float,F)) for x in values):return dict(status='invalid_type')
    if any(not math.isfinite(x) for x in values):return dict(status='nonfinite')
    if not 0<alpha<1:return dict(status='invalid_alpha')
    if lower>upper:return dict(status='reversed_interval')
    width=upper-lower
    loss=width+(2/alpha)*(max(lower-truth,0)+max(truth-upper,0))
    if not math.isfinite(width) or not math.isfinite(loss):return dict(status='nonfinite_arithmetic')
    return dict(status='valid',covered=lower<=truth<=upper,width=str(width),loss=str(loss),normalized_loss=str(loss/(1+abs(truth))))

def calculate():
    a,b=iv_model(0),iv_model(1)
    assert a['joint']==b['joint'] and a['wald']==b['wald']=='1'
    assert a['ate']=='-1/2' and b['ate']=='1/4'
    labels={'true':True,'false':False,'null':None,'missing':object(),'string_false':'false','numeric_zero':0}
    states={name:oracle_state(value) for name,value in labels.items()}
    assert states==dict(true='identified',false='not_identified',null='unknown',missing='unknown',string_false='unknown',numeric_zero='unknown')
    decisions={}
    for label,value in [('true',True),('false',False),('null',None)]:
        for prediction_name,prediction,valid in [('estimate',0,True),('refusal',None,True),('malformed',None,False)]:
            decisions[label+'_'+prediction_name]=gate(value,prediction,valid)
    cases={
        'covered':(F(-1),F(1),F(0),F(1,20)),
        'missed':(F(1),F(2),F(0),F(1,20)),
        'nan_lower':(float('nan'),1,0,.05),
        'infinite_bounds':(-float('inf'),float('inf'),0,.05),
        'nonfinite_truth':(-1,1,float('nan'),.05),
        'reversed':(2,1,0,.05),
        'alpha_zero':(-1,1,0,0),
        'alpha_one':(-1,1,0,1),
        'boolean_lower':(False,1,0,.05),
        'overflow':(-1e308,1e308,0,.05)}
    intervals={name:interval_oracle(*args) for name,args in cases.items()}
    assert intervals['covered']['loss']=='2' and intervals['missed']['loss']=='41'
    assert all(v['status']!='valid' for k,v in intervals.items() if k not in ['covered','missed'])
    # Exact aggregate witness: clipping reverses the ranking of two loss vectors.
    losses={'A':[F(0)]*99+[F(1000)],'B':[F(1)]*100}
    aggregates={k:dict(raw_mean=str(sum(v)/len(v)),capped_mean=str(sum(min(x,F(10)) for x in v)/len(v)),max_loss=str(max(v)),count=len(v)) for k,v in losses.items()}
    assert F(aggregates['A']['raw_mean'])>F(aggregates['B']['raw_mean'])
    assert F(aggregates['A']['capped_mean'])<F(aggregates['B']['capped_mean'])
    # IEEE-754 facts explain why ordered-comparison-only validation is incomplete.
    nan=float('nan');ieee=dict(nan_greater_than_one=nan>1,nan_less_equal_zero=nan<=0,nan_subtraction_is_nonfinite=not math.isfinite(1-nan),infinite_interval_covers_zero=(-float('inf')<=0<=float('inf')))
    money={k:str(F(v['ate'])*100*10000) for k,v in [('A',a),('B',b)]}
    assert money=={'A':'-500000','B':'250000'}
    return dict(scope='Authored finite proposal qualification fixtures; not native benchmark execution',iv=dict(model_a=a,model_b=b,observed_law_equal=True,assumptions=['Randomized independent binary instrument','Exclusion','Monotone treatment','Nonzero first stage','Binary latent confounder'],population_ate_identified_from_observed_law=False,stipulated_population_value_usd=money),identification_states=states,decision_matrix=decisions,intervals=intervals,capped_loss_ranking=aggregates,ieee754=ieee,native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2,allow_nan=False))
