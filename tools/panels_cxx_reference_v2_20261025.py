#!/usr/bin/env python3
"""Keep algebraic weights separate from the source's short-panel lag cap."""
import json
import panels_cxx_reference_20261025 as original

def calculate():
    result=original.calculate()
    result['newey_west_contract']['source_two_period_weight_count_after_cap']=1
    result['newey_west_contract']['source_two_period_lag_one_entered']=False
    result['newey_west_contract']['two_period_zero_lag_algebra']='30'
    result['newey_west_contract']['three_period_zero_padded_lag_one_algebra']='41'
    result['newey_west_contract']['native_execution']=False
    return result

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
