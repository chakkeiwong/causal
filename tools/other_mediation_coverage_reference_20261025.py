#!/usr/bin/env python3
"""Independent finite witnesses; downloaded implementations are not executed."""
from fractions import Fraction as F
from math import erfc,sqrt
import json

def determinant3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0]) + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def calculate():
    original=[[4,1,2],[1,9,3],[2,3,16]]
    selected=[r[:] for r in original]
    for i in range(1,3):
        for j in range(1,3):selected[i-1][j-1]=selected[i][j]
    selected[2][2]=selected[0][0]
    for i in range(2):
        selected[i][2]=selected[i][0]
        selected[2][i]=selected[0][i]
    order=[1,2,0];correct=[[original[i][j] for j in order] for i in order]
    bootstrap_means=[F(x+y,2) for x in [0,2] for y in [0,2]]
    mean=sum(bootstrap_means)/4;variance=sum((x-mean)**2 for x in bootstrap_means)/4
    out={
        'bootstrap_index':{'data':[0,2],'true_resample_means':[str(x) for x in bootstrap_means],'true_resample_variance':str(variance),'unchanged_data_mean':'1','unchanged_fit_variance':'0','effect_simulation_variance_not_claimed_zero':True},
        'covariance_alias':{'original':original,'correct_permutation':correct,'selected_inplace':selected,'original_determinant':determinant3(original),'selected_determinant':determinant3(selected)},
        'signed_two_sided_tail':{'z':-1,'selected':erfc(-1/sqrt(2)),'absolute_value_reference':erfc(1/sqrt(2))},
        'conditional_bootstrap':{'x':[0,1],'constant_resample_probability':'1/2','accepted_resamples':[[0,1],[1,0]],'acceptance_probability':'1/2','bootstrap_mean_variance_unconditional':'1/8','bootstrap_mean_variance_conditional':'0'},
        'bca_unbiased_symmetric_limit':{'alpha_0_25_central_probability':'1/2','alpha_0_025_central_probability':'19/20'},
        'nonlinear_mediator_mean':{'model':'Y=A*M^2;M standard normal independent of A','true_direct':'1','mean_substitution_direct':'0'},
        'correlated_mediators':{'model':'Y=A*M1*M2;zero means,unit variances,covariance1/2','true_direct':'1/2','independent_gaussian_direct':'0'},
        'coordinate_ratio_truncation':{'mediators':3,'per_coordinate_upper':5,'joint_upper':125,'with_exposure_weight10':1250},
        'linear_contrast':{'a':2,'b':4,'c':3,'d':2,'dstar':0,'direct':6,'indirect':16,'total':22},
        'hypothetical_bank_value':{'customers':10000,'dollars_per_unit':10,'missed_units':'1/2','missed_dollars':50000},
        'native_execution':False,
    }
    assert determinant3(original)==500 and determinant3(selected)==0
    assert variance==F(1,2) and out['signed_two_sided_tail']['selected']>1
    assert selected==[[9,3,9],[3,16,3],[9,3,9]]
    return out

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
