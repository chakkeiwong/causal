#!/usr/bin/env python3
"""Independent arithmetic and semantic examples; no clinical code execution."""
from fractions import Fraction as F
import json


def calculate():
    deletion={'SE':F('3'),'SHD':F('5.4'),'SID':F('5.1')}
    full={'SE':F('4.8'),'SHD':F('6.6'),'SID':F('6.2')}
    adverse={k:full[k]-deletion[k] for k in deletion}
    assert adverse==dict(SE=F('1.8'),SHD=F('1.2'),SID=F('1.1'))
    llama_shd=F('6.1')-5
    assert llama_shd==F('1.1')
    # Conditional example: six files with score8, four absent slots left zero.
    score_sum,expected,observed=F(48),10,6
    fixed=score_sum/expected;conditional=score_sum/observed
    assert fixed==F('4.8') and conditional==8
    # A one-character identifier cannot encode distinct ids1and10.
    parsed={name:name.split('_')[1].split('.')[0][0] for name in ['model_1-2.bif','model_10-2.bif']}
    assert parsed['model_1-2.bif']==parsed['model_10-2.bif']=='1'
    traces=[dict(A_hour=2,B_hour=20),dict(A_hour=20,B_hour=2)]
    summaries=[(int(0<=x['A_hour']<=24),int(0<=x['B_hour']<=24)) for x in traces]
    assert summaries==[(1,1),(1,1)]
    cost=F(1800);submitted=100;usable=60
    return dict(table1_full_minus_deletion={k:str(v) for k,v in adverse.items()},llama_deletion_minus_initial_shd=str(llama_shd),missing_files=dict(expected=expected,observed=observed,fixed_zero_slot_mean=str(fixed),conditional_mean=str(conditional),actual_missing_files_observed=False),identifier_collision=parsed,time_aggregation=dict(traces=traces,boolean_summaries=summaries,within_window_order_identified=False),cost=dict(illustrative_usd=str(cost),submitted=submitted,usable=usable,per_submitted=str(cost/submitted),per_usable=str(cost/usable),observed_price=False),native_execution=False)


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
