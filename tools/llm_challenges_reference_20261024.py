#!/usr/bin/env python3
"""Exact authored proposal witnesses; no language model or upstream code runs."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    shared, residual = F(1, 10), F(1, 10)
    marginal = shared + (1-shared)*residual
    def majority(p):
        return sum(p**sum(bits)*(1-p)**(3-sum(bits))
                   for bits in product([0, 1], repeat=3) if sum(bits)>=2)
    correlated = shared + (1-shared)*majority(residual)
    independent = majority(marginal)
    cells = {'neither': F(20,100), 'retrieval_only': F(50,100),
             'oracle_only': F(40,100), 'both': F(90,100)}
    costs = {'model': F(20), 'expert': F(60), 'infrastructure': F(20)}
    total = sum(costs.values())
    result = dict(
        scope='Authored exact examples, not observed model performance or bank prices',
        correlated_votes=dict(shared_failure=str(shared), residual_error=str(residual),
            marginal_error=str(marginal), majority_three_actual=str(correlated),
            majority_three_independence_assumption=str(independent),
            excess=str(correlated-independent), common_failure_floor=str(shared)),
        generated_population=dict(low_type_gain_usd='20',high_type_gain_usd='-30',
            treatment_cost_usd='5', generated_high_share='1/5',
            generated_net_usd=str(F(15)-50*F(1,5)),
            alternate_high_share='3/5',alternate_net_usd=str(F(15)-50*F(3,5)),
            zero_net_share=str(F(15,50))),
        failure_complete=dict(requests=100,completed=80,numeric=60,accepted=36,
            conditional_acceptance=str(F(36,60)),overall_acceptance=str(F(36,100)),
            costs_usd={k:str(v) for k,v in costs.items()},total_usd=str(total),
            cost_per_completed_usd=str(total/80),cost_per_numeric_usd=str(total/60),
            cost_per_accepted_usd=str(total/36)),
        factorial_design=dict(cells={k:str(v) for k,v in cells.items()},
            retrieval_without_oracle=str(cells['retrieval_only']-cells['neither']),
            retrieval_with_oracle=str(cells['both']-cells['oracle_only']),
            oracle_without_retrieval=str(cells['oracle_only']-cells['neither']),
            oracle_with_retrieval=str(cells['both']-cells['retrieval_only']),
            interaction=str(cells['both']-cells['retrieval_only']-cells['oracle_only']+cells['neither'])))
    assert correlated==F(313,2500) and independent==F(47291,500000)
    assert result['generated_population']['generated_net_usd']=='5'
    assert result['generated_population']['alternate_net_usd']=='-15'
    assert result['factorial_design']['interaction']=='1/5'
    return result

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
