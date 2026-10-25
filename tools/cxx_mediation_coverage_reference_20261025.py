#!/usr/bin/env python3
"""Authored exact-law witnesses; never imports or executes downloaded software."""
from fractions import Fraction as F
import json

def calculate():
    a,b,c=F(2),F(4),F(3)
    paired=[(F(1),F(2)),(F(3),F(6))]
    joint=sum(x*y for x,y in paired)/2
    independent=sum(x*y for x,_ in paired for _,y in paired)/4
    blocks=['A','M','Y'];paths=[['Y',['M']],['M',['A']]]
    targets=[x for x in blocks if x in [p[0] for p in paths]]
    parents=[[x for x in blocks if x in p[1]] for p in paths]
    dispatch=[[target,parent] for target,parent in zip(targets,parents)]
    determinant=1-F(1,2)*F(1,2)
    epsilon=F(1,1000)
    dosage_vectors=[[0,0,1],[0,1,0],[1,0,0]]
    dosages=[F(v[1])+2*F(v[0]) for v in dosage_vectors]
    retained=[d for d in dosages if d!=0]
    out={
        'linear_target':{'direct':str(c),'indirect':str(a*b),'total':str(c+a*b)},
        'joint_product':{'paired_mean':str(joint),'independent_mean':str(independent),'difference':str(joint-independent)},
        'ram_near_singularity':{'epsilon':str(epsilon),'response':str(1/epsilon),'derivative':str(1/epsilon**2)},
        'path_order':{'named_input':paths,'selected_target_order':targets,'selected_pairings':dispatch,'intended_chain_effect':str(F(1,2)*F(3,4))},
        'cyclic_normalization':{'determinant':str(determinant),'residual_product_integral':str(1/determinant),'required_density_multiplier_per_observation':str(determinant)},
        'prior_scale':{'input_second_parameter':4,'selected_standard_deviation':2,'selected_variance':4,'alternative_standard_deviation_interpretation_variance':16,'negative_location_rejected_by_selected_stan_data_constraint':True},
        'dosage_branch':{'probabilities':dosage_vectors,'mathematical_dosages':[str(x) for x in dosages],'static_outputs':['missing','1','2'],'all_mean':str(sum(dosages)/3),'retained_mean':str(sum(retained)/len(retained))},
        'hypothetical_bank_value':{'customers':10000,'dollars_per_unit':10,'units_bias':str(joint-independent),'dollars_bias':str(10000*10*(joint-independent))},
        'native_execution':False,
    }
    assert joint==10 and independent==8 and determinant==F(3,4)
    assert dispatch==[['M',['M']],['Y',['A']]]
    assert out['ram_near_singularity']['derivative']=='1000000'
    assert out['hypothetical_bank_value']['dollars_bias']=='200000'
    return out

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
