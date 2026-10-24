#!/usr/bin/env python3
"""Authored arithmetic witnesses; never imports or executes acquired source."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from statistics import median
import json

def quadratic(v, a):
    return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))

def calculate():
    k=[[1,1,0],[1,1,1],[0,1,1]]
    u=[1,-2,1];v=[1,0,-1]
    assert quadratic(u,k)==-2 and quadratic(v,k)==2
    with localcontext() as c:
        c.prec=40
        fallback_u=(Decimal(7)-Decimal(16)/Decimal(6).sqrt())/9
    matrices=[[[1,-2],[-2,5]],[[5,-2],[-2,1]],[[1,0],[0,1]]]
    determinants=[a[0][0]*a[1][1]-a[0][1]**2 for a in matrices]
    assert determinants==[1,1,1]
    med=[[median([a[i][j] for a in matrices]) for j in range(2)] for i in range(2)]
    assert med==[[1,-2],[-2,1]] and quadratic([1,1],med)==-2
    p=F(1,5)
    prob_own0_neighbor1=(1-p)*p
    traversal_selected=F(1,2)*p
    mc_selected=p*p
    assert (prob_own0_neighbor1,traversal_selected,mc_selected)==(F(4,25),F(1,10),F(1,25))
    cast256=((256+128)%256)-128
    assert 4096==16**3 and 256==16**2 and cast256==0
    costs={str(n):str(F(30000,n)) for n in [1000,600,400]}
    return dict(
        provenance='Project-authored calculations from inspected expressions, not native fitted-package output.',native_execution=False,
        ani=dict(cutoff=k,first_score=u,second_score=v,cutoff_variances=[str(F(-2,9)),str(F(2,9))],fallback_first_variance_decimal=str(fallback_u),second_variance_after_first_fallback=str(F(1,9)),second_variance_when_first=str(F(2,9)),order_dependence=True),
        median_covariance=dict(inputs=matrices,input_determinants=determinants,identical_coefficient_vectors=True,elementwise_median=med,median_determinant=-3,total_weights=[1,1],total_variance=-2,scope='Admissible positive-definite helper inputs; not an observed fitted GraphDML repetition.'),
        motif_rule=dict(rule=True,treatment=1,selected_add_then_compare=(int(True)+1)==1,conjunction=True,scope='One-rule Boolean/numeric expression; array/caller qualification remains separate.'),
        graph_cut=dict(nodes=4096,unwrapped_default_clusters=256,signed_eight_bit_result=cast256,requested_samples=7,forced_batch_size=5,complete_batches=7//5,processed_samples=(7//5)*5,unprocessed_samples=7%5,scope='Exact signed-eight-bit wrapping arithmetic and batch count; not a native NumPy run.'),
        policy=dict(bernoulli_p=str(p),target_own=0,target_neighbor=1,true_joint=str(prob_own0_neighbor1),uniform_traversal_times_p=str(traversal_selected),bernoulli_mc_limit_times_p=str(mc_selected),zero_embedding_matches=(F(0)<F(1,10)*0),empty_selection_actual_sum=0,synthetic_first_record_residual=6,NT=10,sentinel_correction=str(F(6,10)),scope='Injective two-action embedding and no clipping/no noise; synthetic residual witness is not data.'),
        hypothetical_cost_per_output=costs)

if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
