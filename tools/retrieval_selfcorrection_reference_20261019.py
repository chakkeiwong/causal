#!/usr/bin/env python3
"""Authored all-attempt accounting and exact arithmetic on printed percentages."""
from fractions import Fraction as F
import json


def calculate():
    # Ten authored requests: first test success at1,2,3, or no success by3.
    first=[1,1,2,2,2,3,None,None,None,None]
    attempts=[x if x is not None else 3 for x in first]
    cumulative=[sum(x is not None and x<=n for x in first) for n in [1,2,3]]
    total=sum(attempts);successful=sum(x is not None for x in first)
    accepted=4;cost=F(2)*total;benefit=F(15)*accepted
    assert cumulative==[2,5,6] and total==23 and successful==6
    assert benefit-cost==14 and F(15)*successful-cost==44
    return dict(kind='project_authored_exact_reference',live_model_execution=False,
        requests=10,max_attempts=3,first_test_success=first,attempts_by_request=attempts,
        cumulative_test_passes=cumulative,eventual_test_success=str(F(successful,10)),
        attempts_all_requests=total,attempts_per_request=str(F(total,10)),
        attempts_successful_requests=sum(x for x in first if x),
        success_only_attempt_mean=str(F(sum(x for x in first if x),successful)),
        causal_accepted_requests=accepted,causal_acceptance_fraction=str(F(accepted,10)),
        assumed_attempt_cost_USD='2',assumed_value_per_accepted_request_USD='15',
        total_cost_USD=str(cost),cost_per_accepted_USD=str(cost/accepted),
        accepted_net_USD=str(benefit-cost),test_only_net_USD=str(15*successful-cost),
        test_only_overstatement_USD='30',
        printed_percentage_arithmetic={
            'Table1_30.5_to_35.5_pp':str(F('35.5')-F('30.5')),
            'Table1_relative_gain':str((F('35.5')-F('30.5'))/F('30.5')),
            'Table2_35.5_to_39.5_pp':str(F('39.5')-F('35.5')),
            'Table2_relative_gain':str((F('39.5')-F('35.5'))/F('35.5')),
            'Table1_SciPy_both_on_minus_both_off_pp':str(F('32.08')-F('33.02')),
            'prompt_token_ratio_9.29_to_2.54':str(F('9.29')/F('2.54'))},
        limitations=['First-success sequence, acceptance and prices are stipulated examples, not study or bank observations.',
                    'Printed percentages are rounded reported values, not recovered raw trial counts or uncertainty intervals.',
                    'Adaptive test feedback is not an independent candidate pool; this calculation makes no pass@k or sampling-calibration claim.'])

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
