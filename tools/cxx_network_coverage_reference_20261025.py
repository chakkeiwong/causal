#!/usr/bin/env python3
"""Authored finite-law and graph-contract examples; no acquired source executed."""
from fractions import Fraction as F
from itertools import permutations,product
from collections import Counter
import json

def calculate():
    neighborhoods=[{0,1},{0,1,2},{1,2}];law=[];partitions=Counter()
    for ranks in permutations(range(3)):
        partition=tuple(max(ranks[j] for j in neighbors) for neighbors in neighborhoods)
        partitions[partition]+=1;clusters=sorted(set(partition))
        for assignment in product([0,1],repeat=len(clusters)):
            cluster_assignment=dict(zip(clusters,assignment));z=[cluster_assignment[c] for c in partition]
            exposed=[[all(z[j]==a for j in neighbors) for neighbors in neighborhoods] for a in [0,1]]
            law.append(dict(prob=F(1,6*2**len(clusters)),partition=partition,assignment=z,exposed=exposed))
    assert sum(x['prob'] for x in law)==1
    pi=[[sum(x['prob'] for x in law if x['exposed'][a][i]) for i in range(3)] for a in [0,1]]
    y=[[F(i+1) for i in range(3)],[F(i+2) for i in range(3)]]
    for x in law:
        ht=[];hajek=[]
        for a in [0,1]:
            denominator=sum(F(x['exposed'][a][i])/pi[a][i] for i in range(3))
            numerator=sum(F(x['exposed'][a][i])*y[a][i]/pi[a][i] for i in range(3))
            ht.append(numerator/3);hajek.append(numerator/denominator if denominator else F(0))
        x['ht']=ht[1]-ht[0];x['hajek_zero_extension']=hajek[1]-hajek[0]
    ht_mean=sum(x['prob']*x['ht'] for x in law)
    ht_var=sum(x['prob']*(x['ht']-ht_mean)**2 for x in law)
    second_moment=F(0)
    for a,i,c,j in product(range(2),range(3),range(2),range(3)):
        joint=sum(x['prob'] for x in law if x['exposed'][a][i] and x['exposed'][c][j])
        sign=(1 if a else -1)*(1 if c else -1)
        second_moment+=sign*y[a][i]*y[c][j]*joint/(9*pi[a][i]*pi[c][j])
    assert second_moment-ht_mean**2==ht_var==F(2242,75)
    hajek_mean=sum(x['prob']*x['hajek_zero_extension'] for x in law)
    treated_available=sum(x['prob'] for x in law if any(x['exposed'][1]))
    assert ht_mean==1 and hajek_mean==treated_available<1
    one_cluster=[dict(prob=F(1,2),ht=F(-4),hajek=F(-2)),dict(prob=F(1,2),ht=F(6),hajek=F(3))]
    assert sum(x['prob']*x['ht'] for x in one_cluster)==1
    assert sum(x['prob']*x['hajek'] for x in one_cluster)==F(1,2)
    p=F(1,5);asymmetric=dict(treatment=p**2,control=(1-p)**2,hardcoded_half=F(1,4))
    assert asymmetric['treatment']==F(1,25) and asymmetric['control']==F(16,25)
    hypothetical_pi=[F(1,4),F(1,2)];mix_pi=sum(hypothetical_pi)/2
    weighted=F(9,10);restored_unit=F(1,2)
    independent_variance=sum(F(1,4)*(F(a+b,2)-F(1,2))**2 for a,b in product([0,1],repeat=2))
    copied_variance=sum(F(1,2)*(F(a)-F(1,2))**2 for a in [0,1])
    assert independent_variance==F(1,8) and copied_variance==F(1,4)
    return dict(provenance='Project-authored finite enumeration and helper-expression examples;not native execution.',native_execution=False,
      path_three_one_hop_max=dict(rank_orders=6,assignment_cases=len(law),unique_partitions=len(partitions),pi=[[str(v) for v in row] for row in pi],target='1',ht_mean=str(ht_mean),ht_variance=str(ht_var),hajek_zero_extension_mean=str(hajek_mean),probability_treated_exposed_denominator_positive=str(treated_available),missing_treated_probability=str(1-treated_available)),
      single_cluster=dict(y0=['1','2','3'],y1=['2','3','4'],target='1',ht_outputs=['-4','6'],ht_mean='1',hajek_zero_extension_outputs=['-2','3'],hajek_mean='1/2',all_assignments_have_one_empty_arm=True),
      assignment_probability={k:str(v) for k,v in asymmetric.items()},
      probability_mixture=dict(conditional=[str(v) for v in hypothetical_pi],marginal=str(mix_pi),inverse_marginal=str(1/mix_pi),mean_inverse_conditional=str(sum(1/v for v in hypothetical_pi)/2)),
      restored_weight=dict(original_weights=[9,1],restored_default_weights=[1,1],neighbor_treatments=[1,0],original_exposure=str(weighted),restored_exposure=str(restored_unit),scope='Selected restoreGraph inserts edges without weight argument;authored helper-expression witness.'),
      random_streams=dict(independent_two_draw_mean_variance=str(independent_variance),identical_two_draw_mean_variance=str(copied_variance),scope='Hypothetical equal-position independent versus copied Bernoulli streams;not a PRNG statistical certification.'),
      sparse_ids=dict(remaining_ids=[0,2],actual_units=2,upper_id_bound=3,zero_filled_mean=str(F(2,3)),correct_mean='1'),
      costs={str(n):str(F(30000,n)) for n in [1000,600,400]})

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
