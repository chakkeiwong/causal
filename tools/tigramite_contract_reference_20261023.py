#!/usr/bin/env python3
"""Independent exact proposal examples; never import or execute downloaded code."""
from fractions import Fraction as F
from collections import Counter
import json

def calculate():
    # These are stipulated populations and independent combinatorial witnesses.
    covariance=F(20); var_x=F(1); var_y=F(625)
    slope=covariance/var_x; correlation=covariance/F(25)
    cost=F(12); baseline=F(100)
    split=Counter({'-->':5,'<--':5})
    no_edge=Counter({'':4,'-->':3,'<--':3})
    n,L=6,2
    source_starts=list(range(n-L)); complete_starts=list(range(n-L+1))
    source_reachable=sorted({s+k for s in source_starts for k in range(L)})
    missing_positions={5}; expanded=sorted({i+k for i in missing_positions for k in range(3)})
    x=[F(0),F(2)]; mean=lambda a:sum(a)/len(a)
    square_hard=F(1)**2-F(0)**2
    square_soft=mean([(v+1)**2-v**2 for v in x])
    out=dict(linear=dict(partial_correlation=str(correlation),coefficient_usd=str(slope),
      mean_under_zero=str(baseline),mean_under_one=str(baseline+slope),net_usd=str(slope-cost),
      wrong_statistic_as_dollars_net=str(correlation-cost)),
      interventions=dict(hard_zero_to_one_square=str(square_hard),soft_plus_one_square=str(square_soft)),
      graph_aggregation=dict(split_direction_counts=dict(split),tied_modal_mass=str(F(sum(split.values()),10)),
       conflict_input_count=0,no_edge_plurality=str(F(4,10)),adjacency_majority=str(F(6,10))),
      block_sampling=dict(n=n,block_length=L,selected_expression_starts=source_starts,
       complete_nonwrapping_starts=complete_starts,selected_expression_reachable=source_reachable),
      missing_extension=dict(sample_count=n,expanded_positions=expanded,out_of_range=[i for i in expanded if i>=n]),
      limits=['Exact authored population/algebra and finite-enumeration references only.',
       'No Tigramite import, call, empirical coverage, real bank price or execution evidence.'])
    assert slope==20 and correlation==F(4,5) and slope-cost==8
    assert square_hard==1 and square_soft==3
    assert source_reachable==[0,1,2,3,4] and expanded==[5,6,7]
    return out
if __name__=='__main__': print(json.dumps(calculate(),indent=2))
