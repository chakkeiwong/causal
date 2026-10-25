#!/usr/bin/env python3
"""Authored finite references; never imports or executes acquired software."""
from fractions import Fraction as F
from itertools import product
import json
import math

def calculate():
    p0,p1=F(1,4),F(3,4)
    natural_indirect=4*(p1-p0)
    logit_product=4*math.log(9)
    assert natural_indirect==2 and logit_product>8
    paired=[F(sum(x),2) for x in product([-1,1],repeat=2)]
    paired_product=sum(x*x for x in paired)/4
    independent_product=sum(a*b for a,b in product(paired,repeat=2))/16
    assert (paired_product,independent_product)==(F(1,2),0)
    delta=2; first=2*delta; second=4*delta
    intended=2*4*delta; combined=first*second; total=(3+2*4)*delta
    assert (intended,combined,total-combined,3*delta)==(16,32,-10,6)
    # Exact reading of selected sharp-source branch conditions, without importing it.
    probabilities=[F(3,4),F(1,4)];threshold=F(3,4);low,high=F(1,3),F(3)
    before=F(0);masses=[]
    for p in probabilities:
        after=before+p
        mass=p*low if after<threshold else F(0)
        if before>=threshold:mass+=p*high
        if after>threshold and before<threshold:mass+=(threshold-before)*low+(after-threshold)*high
        masses.append(mass);before=after
    assert masses==[0,F(3,4)]
    # Four constant samples, Gamma=2, no y_regression branch.
    upper=(3*F(1,2)+1*2)/4
    lower=(2*2+2*F(1,2))/4
    assert (upper,lower)==(F(7,8),F(5,4))
    memory=1000*1000*256*4
    assert memory==1024000000
    return {
      'scope':'authored exact arithmetic and static-expression witnesses; no native package execution',
      'binary_mediator':{'p0':str(p0),'p1':str(p1),'natural_indirect':str(natural_indirect),'logit_coefficient_product':logit_product},
      'bootstrap_dependence':{'paired_product_mean':str(paired_product),'independent_product_mean':str(independent_product),'paired_sum_variance':'2','independent_sum_variance':'1'},
      'nonunit_contrast':{'delta':delta,'intended_indirect':intended,'two_contrasts_product':combined,'residual_direct':total-combined,'intended_direct':3*delta},
      'zero_sign_tail':{'positive':0,'negative':0,'replicates':4,'expression_value':0,'probability_test_validity_established':False},
      'sharp_discrete_equality':{'masses':[str(x) for x in masses],'total':str(sum(masses)),'required_total':'1'},
      'sharp_constant_samples':{'samples':[1,1,1,1],'gamma':2,'selected_upper':str(upper),'selected_lower':str(lower),'normalized_target':'1'},
      'missed_rare_violation':{'rare_probability':0.001,'draws':100,'miss_probability':0.999**100},
      'overcast_pairwise_tensor':{'samples':1000,'batch':256,'outcomes':1,'bytes_per_value':4,'one_tensor_bytes':memory,'measured_runtime':False},
      'hypothetical_bank_value':{'customers':10000,'benefit_per_customer_bounds':[2,8],'cost_per_customer':5,'net_bounds_usd':[-30000,30000],'observed_bank_data':False}
    }

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
