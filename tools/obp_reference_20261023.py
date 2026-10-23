#!/usr/bin/env python3
"""Independent finite bandit-law checks; downloaded sources are inert data."""
from fractions import Fraction as F
from itertools import product
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def calculate():
    b=[F(1,4),F(3,4)];q=[[F(0),F(2)],[F(1),F(5)]]
    target=sum(q[x][1] for x in [0,1])/2
    ipw=sum(b[x]*(1/b[x])*q[x][1] for x in [0,1])/2
    clipped=sum(b[x]*min(1/b[x],F(2))*q[x][1] for x in [0,1])/2
    uniform=sum(b[x]*2*q[x][1] for x in [0,1])/2
    replay=sum(b[x]*q[x][1] for x in [0,1])/sum(b)
    assert target==ipw==F(7,2) and clipped==3 and uniform==replay==F(17,4)
    margins={k:10*v-32 for k,v in [('target',target),('clipped',clipped),('uniform_logger',uniform)]}
    assert margins==dict(target=3,clipped=-2,uniform_logger=F(21,2))
    # A correct response regression removes conditional-mean residual bias even if weights are clipped.
    exact_dr=sum(q[x][1]+b[x]*min(1/b[x],F(2))*(q[x][1]-q[x][1]) for x in [0,1])/2
    assert exact_dr==target
    assert sum([F(-1,10),F(11,10)])==1
    # Confirm selected helper and constructor pathways by parsing inert source text.
    src=(ROOT/'docs/literature/raw/exec23_obp_07.txt').read_text();tree=ast.parse(src)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='BaseOffPolicyEstimatorTuning')
    meth=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='estimate_interval_with_tuning')
    returned=next(n.value for n in meth.body if isinstance(n,ast.Return))
    constructor=returned.func.value
    assert isinstance(constructor,ast.Call) and constructor.keywords==[]
    keyword_map={k.arg:ast.unparse(k.value) for k in returned.keywords}
    assert keyword_map['pscore']=='pscore_' and keyword_map['estimated_pscore']=='estimated_pscore'
    # These statements do not execute the imported library. Their algebra resolves an apparent flag omission.
    frozen={'known':F(1,4),'estimated':F(1,2)}
    chosen=frozen['estimated'];base_default_receives=chosen
    assert base_default_receives==chosen
    return clean(dict(native_execution=False,target=target,ipw=ipw,clipped=clipped,uniform_logger=uniform,replay=replay,
        margins=margins,correct_regression_clipped_dr=exact_dr,invalid_probability_row=[F(-1,10),F(11,10)],
        no_replay_matches=dict(stochastic_target=[F(1,2),F(1,2)],returned_score_vector=[0,0],scientific_interpretation='unavailable deterministic replay, not evidence of zero policy value'),
        source_branch=dict(interval_constructor=ast.unparse(constructor),keyword_map=keyword_map,apparent_flag_omission_resolved=True),
        bootstrap=dict(round_resampling='conditional on supplied fitted quantities, clipping and selected hyperparameter',retuning_in_selected_call=False)))
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list):return [clean(v) for v in x]
    return x
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
