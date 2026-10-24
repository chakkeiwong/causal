#!/usr/bin/env python3
"""Project-authored rational witnesses; no downloaded package is imported."""
from fractions import Fraction as F
import json

def calculate():
    y=list(map(F,[0,0,2,2]));n=len(y);mean=sum(y)/n
    scores=[v-mean for v in y];raw_bread=F(n)
    raw_meat=sum(x*x for x in scores)
    covariance=raw_meat/raw_bread**2
    clustered=[sum(scores[:2]),sum(scores[2:])]
    cluster_meat=sum(x*x for x in clustered)
    cluster_covariance=cluster_meat/raw_bread**2
    assert covariance==F(1,4) and cluster_covariance==F(1,2)
    # Follow the selected standalone normalization symbolically, not by
    # importing or executing upstream code. The reported count depends on
    # one-parameter vector versus one-row-array representation.
    def standalone(n_used):
        bread=raw_bread/n_used;meat=raw_meat/n_used
        return meat/bread**2
    standalone_vector=standalone(F(4));standalone_row=standalone(F(1))
    assert standalone_vector==1 and standalone_row==F(1,4)
    assert standalone_row/n==F(1,16)
    # A rank-deficient moment system psi=(Y-theta_1,0) does not constrain
    # theta_2. The diagonal pseudoinverse gives zero in that direction.
    singular_bread=[[F(1),F(0)],[F(0),F(0)]]
    singular_covariance=[[F(1,4),F(0)],[F(0),F(0)]]
    # Fully specified one-stratum population: e=.1, q1=.8, q0=.2,
    # An intercept-only outcome model deliberately omits treatment. Its
    # population score gives m1=m0=E[Y]=.26, while clipped e=.2.
    e,q1,q0,m1,m0,clipped=map(F,['1/10','4/5','1/5','13/50','13/50','1/5'])
    assert m1==e*q1+(1-e)*q0
    def means(p):
        return (m1+e/p*(q1-m1),m0+(1-e)/(1-p)*(q0-m0))
    unclipped=means(e);clipped_means=means(clipped)
    truth=q1-q0;clipped_effect=clipped_means[0]-clipped_means[1]
    bias=clipped_effect-truth
    assert unclipped==(q1,q0) and clipped_effect==F(27,80) and bias==F(-21,80)
    assert clipped_means==(F(53,100),F(77,400))
    # Conditional scenario: 1000 accounts, 100 USD per successful
    # resolution, and 50000 USD intervention cost.
    scale=F(1000*100);cost=F(50000)
    true_net=truth*scale-cost;clipped_net=clipped_effect*scale-cost
    assert true_net==10000 and clipped_net==-16250
    encode=lambda a:[[str(x) for x in row] for row in a]
    return dict(status='exact_authored_reference',downloaded_code_executed=False,
        root=dict(data=list(map(str,y)),mean=str(mean),bad_candidate='0',mean_residual_at_bad_candidate='1',
            qualification='A custom return value is not a verified root'),
        sampling=dict(scores=list(map(str,scores)),raw_bread=str(raw_bread),raw_meat=str(raw_meat),
            individual_covariance=str(covariance),cluster_sums=list(map(str,clustered)),
            cluster_meat=str(cluster_meat),cluster_covariance=str(cluster_covariance),
            qualification='Two-cluster arithmetic witness, not adequate asymptotic calibration evidence'),
        standalone_shape=dict(vector_n_used=4,row_n_used=1,vector_asymptotic=str(standalone_vector),
            row_return=str(standalone_row),vector_after_documented_division=str(standalone_vector/n),
            row_after_documented_division=str(standalone_row/n),mestimator_row_covariance=str(covariance),
            row_hc1='n_used=1<=p=1 triggers refusal',
            qualification='Conditional static control-flow witness; no native execution'),
        rank=dict(bread=encode(singular_bread),pseudoinverse=encode(singular_bread),
            covariance=encode(singular_covariance),unidentified_coordinate=2,
            qualification='Zero projected variance is not identified certainty'),
        clipping=dict(true_propensity=str(e),clipped_propensity=str(clipped),true_means=list(map(str,unclipped)),
            clipped_means=list(map(str,clipped_means)),true_effect=str(truth),clipped_effect=str(clipped_effect),bias=str(bias),
            qualification='Correct propensity branch can be lost by clipping with misspecified outcomes; correct-outcome branch differs'),
        banking=dict(accounts=1000,value_per_event_usd=100,cost_usd=50000,true_net_usd=str(true_net),clipped_net_usd=str(clipped_net),
            qualification='Stipulated successful-resolution illustration, not observed bank returns'),
        costs=dict(total_usd=4800,requested=240,finite=200,accepted=160,
            per_requested=str(F(4800,240)),per_finite=str(F(4800,200)),per_accepted=str(F(4800,160)),
            qualification='Authored costs and denominators, not measured economics'))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
