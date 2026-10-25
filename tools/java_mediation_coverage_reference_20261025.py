#!/usr/bin/env python3
"""Independent finite SEM witnesses; no acquired Java code is executed."""
from fractions import Fraction as F
import json

def calculate():
    a,b,c=F(2),F(4),F(3)
    rho_am,rho_ay=F(1,4),F(1,2)
    determinant=1-rho_am**2-rho_ay**2
    structural=c+a*b
    covariance_ratio=structural+b*rho_am+rho_ay
    assert determinant==F(11,16) and structural==11 and covariance_ratio==F(25,2)
    # Mediator/outcome disturbance confounding changes regression product.
    rho_my=F(1,2)
    fitted_b=b+rho_my
    fitted_direct=c-a*rho_my
    assert (a*b,a*fitted_b,fitted_direct)==(8,9,2)
    va,vb,cab=F(1,25),F(9,100),F(1,50)
    product_variance=b*b*va+a*a*vb+2*a*b*cab
    assert product_variance==F(33,25)
    edges=[('A','M1',2),('M1','M2',3),('M2','Y',4)]
    assert len(edges)>2
    path_total=1
    for _,_,coef in edges:path_total*=coef
    assert path_total==24
    return {
      'scope':'authored algebra and static-expression consequences; no native Java or Julia execution',
      'correlated_treatment_errors':{'residual_covariance_determinant':str(determinant),'structural_total':str(structural),'unchanged_error_covariance_ratio':str(covariance_ratio),'residual_correlation_bias':str(covariance_ratio-structural)},
      'mediator_outcome_confounding':{'true_indirect':'8','regression_product':'9','regression_direct':'2','total':'11'},
      'product_delta_variance':{'with_covariance':str(product_variance),'without_covariance':'1','standard_errors_are_not_additive':True},
      'path_cutoff':{'edges':edges,'max_edges':2,'bounded_search_paths':0,'structural_total':path_total,'zero_not_proven_by_cutoff':True},
      'singular_ram':{'A':'1','S':'1','mean_parameter':'2','I_minus_A':'0','inverse_exists':False,'inverse_buffer_initialized':'1','continued_covariance_expression':'1','continued_mean_expression':'2','native_result_observed':False},
      'export_direction':{'internal_edge':'A -> M','selected_lavaan_string':'M ~ A','selected_julia_string':'M -> A','target_runtime_parity_verified':False},
      'hypothetical_value':{'customers':10000,'causal_units_per_customer':'11','covariance_ratio_units_per_customer':'12.5','usd_per_unit':10,'overstatement_usd':150000,'observed_bank_data':False}
    }

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
