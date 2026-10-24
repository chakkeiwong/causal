#!/usr/bin/env python3
"""Independent target, selection, support and competing-risk witnesses."""
from fractions import Fraction as F
from itertools import product
import json

def calculate():
    rates=[F(1,5),F(3,5),F(9,10)]
    mixture_a=F(3,4)*rates[1]+F(1,4)*rates[2]
    mixture_b=F(1,4)*rates[1]+F(3,4)*rates[2]
    contrasts=[mixture_a-rates[0],mixture_b-rates[0]]
    assert contrasts==[F(19,40),F(5,8)]
    k=4;max_mean=sum(max(row) for row in product([-1,1],repeat=k))/F(2**k)
    assert max_mean==F(7,8)
    support=[F(i,10) for i in range(11)]
    f1=lambda a:a/2
    f2=lambda a:a/2 if a<=1 else 1-a/2
    assert all(f1(a)==f2(a) for a in support) and (f1(F(2)),f2(F(2)))==(1,0)
    # Half have competing event at1 and default at2; half default at2 and competitor at3.
    # Observed default before the competing event occurs in half; eliminating competitor
    # with unchanged latent default times yields all. Other removal mechanisms may differ.
    observed_default=F(1,2);independent_removal_default=F(1)
    assert observed_default!=independent_removal_default
    return dict(kind='authored_exact_witnesses_not_JMP_execution',
        pooled_treatments=dict(rates=[str(x) for x in rates],weights_a=['3/4','1/4'],weights_b=['1/4','3/4'],pooled_contrasts=[str(x) for x in contrasts],hypothetical_1000_accounts_100usd=[str(1000*100*x) for x in contrasts],not_native_default=True),
        adaptive_selection=dict(independent_zero_mean_scores=k,each_values=[-1,1],expected_selected_max=str(max_mean),native_multiplicity_correction_not_tested=True),
        unsupported_dose=dict(observed_support=['0','1'],target_dose='2',compatible_means=['1','0'],observed_functions_equal=True,parametric_positive_density_not_empirical_support=True),
        competing_events=dict(observed_default_before_competitor=str(observed_default),default_by2_under_specified_removal=str(independent_removal_default),removal_preserves_latent_default_time_assumption=True,arbitrary_bank_removal_not_identified=True),
        economics=dict(hypothetical_usd=21000,submitted=700,completed=525,qualified=350,costs_usd=[30,40,60]),native_execution=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
