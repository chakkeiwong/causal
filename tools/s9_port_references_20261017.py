#!/usr/bin/env python3
"""Exact porting counterexamples; no upstream runtime or calibration claim."""
from fractions import Fraction as F
from itertools import product
import json


def moments(rows):
    n=len(rows)
    means=[sum(F(row[k]) for row in rows)/n for k in (0,1)]
    covariance=[[sum((F(row[j])-means[j])*(F(row[k])-means[k]) for row in rows)/n
                 for k in (0,1)] for j in (0,1)]
    contrast=[F(row[0])-row[1] for row in rows]
    mean=sum(contrast)/n
    return dict(means=list(map(str,means)),covariance=[[str(v) for v in row] for row in covariance],
                contrast_variance=str(sum((v-mean)**2 for v in contrast)/n))


def calculate():
    shared=[(a-c,b-c) for a,b,c in product((-1,1),repeat=3)]
    split=[(a-c,b-d) for a,b,c,d in product((-1,1),repeat=4)]
    alpha=F(1,20)
    ps=[alpha-F(1,10000),alpha,alpha+F(1,10000)]
    thresholds=[dict(p=str(p),source_delete=p>=alpha,strict_port_delete=p>alpha) for p in ps]
    row_means=[sum(F(x) for x in row)/4 for row in product((0,0,2,2),repeat=4)]
    cluster_means=[F(a+b,2) for a,b in product((0,2),repeat=2)]
    variance=lambda x:str(sum((v-sum(x)/len(x))**2 for v in x)/len(x))
    return dict(thresholds=thresholds,alpha=str(alpha),
                na_behavior=dict(delete_true=True,delete_false=False),
                shared_control=moments(shared),split_control=moments(split),
                bootstrap=dict(row_mean='1',cluster_mean='1',row_variance=variance(row_means),
                               cluster_variance=variance(cluster_means),row_paths=len(row_means),cluster_paths=len(cluster_means)),
                limitations=['Finite authored counterexamples, not an executed pcalg/CausalML/Java/C++ port.',
                            'Shared control law is an illustration of joint randomness; not an estimate of CausalML variance.',
                            'Bootstrap distributions are conditional finite examples, not sampling coverage or dependence qualification.'])


def separate(value):
    assert value['thresholds'][1]==dict(p='1/20',source_delete=True,strict_port_delete=False)
    assert value['shared_control']['covariance']==[['2','1'],['1','2']]
    assert value['split_control']['covariance']==[['2','0'],['0','2']]
    assert value['shared_control']['contrast_variance']=='2'
    assert value['split_control']['contrast_variance']=='4'
    # Var of the average of k independent draws from a variance-one empirical law.
    assert F(value['bootstrap']['row_variance'])==F(1,4)
    assert F(value['bootstrap']['cluster_variance'])==F(1,2)
    return dict(status='pass',scope='Same-author algebra distinct from finite tuple enumeration',
                checks=['Exact threshold equality changes >= versus > decision.',
                        'Shared-control cancellation gives contrast variance2; independently redrawn controls give4.',
                        'Conditional empirical variance1 divided by4 rows versus2 independent clusters gives1/4 versus1/2.'])


if __name__=='__main__':
    value=calculate();print(json.dumps(dict(result=value,review=separate(value)),indent=2))
