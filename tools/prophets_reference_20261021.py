#!/usr/bin/env python3
"""Exact arithmetic for published rounded LLM benchmark table entries."""
from decimal import Decimal
from fractions import Fraction as F
import json


def calculate():
    scores={
      'overall':{'baseline':Decimal('82.0'),'causal_tree':Decimal('86.4'),'causal_program':Decimal('90.8'),'deepseek_r1_baseline':Decimal('88.1')},
      'commonsensical':{'baseline':Decimal('84.3'),'causal_tree':Decimal('87.5'),'causal_program':Decimal('92.5'),'cf_baseline':Decimal('70.1'),'cf_program':Decimal('92.5')},
      'anti_commonsense':{'baseline':Decimal('82.4'),'cf_baseline':Decimal('68.8'),'cf_program':Decimal('90.2')},
      'nonsense':{'baseline':Decimal('79.3'),'cf_baseline':Decimal('64.1'),'cf_program':Decimal('87.4')}}
    program_gain=scores['overall']['causal_program']-scores['overall']['baseline']
    tree_gain=scores['overall']['causal_tree']-scores['overall']['baseline']
    cf_gains={k:str(v['cf_program']-v['cf_baseline']) for k,v in scores.items() if k!='overall'}
    query_sample=[209,174,174,137,95,92,73,23,22]
    query_original=[1702,1518,1518,1288,874,870,552,184,184]
    rung_sample=[405,398,197]
    rung_original=[3584,3404,1702]
    assert program_gain==Decimal('8.8') and tree_gain==Decimal('4.4')
    assert cf_gains=={'commonsensical':'22.4','anti_commonsense':'21.4','nonsense':'23.3'}
    assert sum(query_sample)==999 and sum(query_original)==8690
    assert sum(rung_sample)==1000 and sum(rung_original)==8690
    sc10=[403,169,127,128,109,59]
    sc5=[535,246,218]
    error10=[10,37,13]
    # Appendix D.3 step4 evaluated literally from its displayed table.
    fixed_x0=(F(60,100)-F(28,100))*(F(22,100)-F(57,100))
    # The different expression printed in D.3 step6, evaluated literally.
    mixed=(F(22,100)*(F(60,100)-F(28,100))+
           F(78,100)*(F(74,100)-F(35,100))-
           (F(57,100)*(F(60,100)-F(28,100))+
            F(43,100)*(F(74,100)-F(35,100))))
    assert fixed_x0==F(-14,125) and mixed==F(49,2000)
    assert sum(sc10)==995 and sum(sc5)==999 and sum(error10)==60
    return {'scope':'Arithmetic only over paper-rounded percentages and displayed dataset counts; no raw replication or statistical uncertainty.',
      'gains_percentage_points':{'causal_program_vs_input_output':str(program_gain),'causal_tree_vs_input_output':str(tree_gain),'causal_program_counterfactual_by_subset':cf_gains,
        'commonsensical_program_vs_baseline':str(scores['commonsensical']['causal_program']-scores['commonsensical']['baseline']),
        'program_minus_deepseek_r1_baseline_overall':str(scores['overall']['causal_program']-scores['overall']['deepseek_r1_baseline'])},
      'appendix_checks':{'SC10_count_sum':sum(sc10),'SC5_count_sum':sum(sc5),
        'table10_error_count_sum':sum(error10),'prose_error_sample_size':50,
        'D3_step4_literal':str(fixed_x0),'D3_step6_literal':str(mixed),'D3_step6_reported':'0.0173',
        'limitation':'Literal arithmetic only; coding, actual generator/SCM and intended NIE target must be reconciled before declaring corrected benchmark truth.'},
      'table5_counts':{'sample_query_types':query_sample,'sum_sample_query_types':sum(query_sample),'sample_rungs':rung_sample,'sum_sample_rungs':sum(rung_sample),'original_query_types':query_original,'sum_original_query_types':sum(query_original),'original_rungs':rung_original,'sum_original_rungs':sum(rung_original),'unresolved_sample_query_type_count_difference':sum(rung_sample)-sum(query_sample)}}

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
