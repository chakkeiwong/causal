#!/usr/bin/env python3
"""Exact authored target, clipping and centering examples; no package execution."""
from fractions import Fraction as F
import json


def aipw_expectation(p,q,mu0,mu1,m0,m1):
    return m1-m0+p/q*(mu1-m1)-(1-p)/(1-q)*(mu0-m0)


def gram(rows):
    n=len(rows);k=len(rows[0])
    return [[sum(r[i]*r[j] for r in rows)/n for j in range(k)] for i in range(k)]


def encoded(matrix):return [[str(x) for x in row] for row in matrix]


def calculate():
    # Independent customers; risk group is equally common, with known assignment.
    groups=[dict(name='low',mass=F(1,2),p=F(1,4),mu0=F(0),mu1=F(20)),
            dict(name='high',mass=F(1,2),p=F(3,4),mu0=F(0),mu1=F(80))]
    treat=sum(g['mass']*g['p'] for g in groups)
    ate=sum(g['mass']*(g['mu1']-g['mu0']) for g in groups)
    att=sum(g['mass']*g['p']*(g['mu1']-g['mu0']) for g in groups)/treat
    atu=sum(g['mass']*(1-g['p'])*(g['mu1']-g['mu0']) for g in groups)/(1-treat)
    assert (ate,att,atu)==(50,65,35)
    # Deliberately poor outcome model and clipping at the selected default upper bound.
    p=F(1999,2000);q=F(999,1000);mu0=F(20);mu1=F(80);m0=m1=F(0)
    raw=aipw_expectation(p,p,mu0,mu1,m0,m1)
    clipped=aipw_expectation(p,q,mu0,mu1,m0,m1)
    bias=(p-q)*((mu1-m1)/q+(mu0-m0)/(1-q))
    assert raw==60 and clipped-raw==bias==F(10030,999)
    assert aipw_expectation(p,q,mu0,mu1,mu0,mu1)==60
    cost=F(65)
    rows=[[F(1),F(0)],[F(3),F(0)]]
    means=[sum(r[j] for r in rows)/len(rows) for j in range(2)]
    grand=sum(means)/len(means)
    col=gram([[r[j]-means[j] for j in range(2)] for r in rows])
    scalar=gram([[x-grand for x in r] for r in rows])
    d=[x-grand for x in means];delta=[[scalar[i][j]-col[i][j] for j in range(2)] for i in range(2)]
    assert delta==[[d[i]*d[j] for j in range(2)] for i in range(2)]
    assert scalar==[[2,-1],[-1,1]] and col==[[1,0],[0,0]]
    centered=[[F(-1),F(-2)],[F(1),F(2)]]
    assert gram(centered)==gram(list(reversed(centered)))
    return dict(kind='project_authored_exact_reference',native_package_execution=False,
        population=dict(groups=[{k:str(v) if isinstance(v,F) else v for k,v in g.items()} for g in groups],
            ATE=str(ate),ATT=str(att),ATU=str(atu),treatment_probability=str(treat),
            margin_at_cost55=dict(all=str(ate-55),treated=str(att-55),untreated=str(atu-55))),
        clipping=dict(p=str(p),q=str(q),mu0=str(mu0),mu1=str(mu1),m0=str(m0),m1=str(m1),
            unclipped_expected_score=str(raw),clipped_expected_score=str(clipped),bias=str(bias),
            correct_outcome_expected_score='60',stipulated_cost=str(cost),
            true_margin=str(raw-cost),clipped_score_margin=str(clipped-cost)),
        centering=dict(moment_rows=encoded(rows),column_means=[str(x) for x in means],
            grand_mean=str(grand),column_centered=encoded(col),scalar_centered=encoded(scalar),
            difference=encoded(delta),zero_column_means_agree=True),
        limitations=['Known imposed law with independent customers and deterministic potential outcomes; no bank data.',
            'The clipping contrast is a population score calculation with deliberately incorrect outcome models; it is not a native estimate or a universal AIPW failure.',
            'The centering contrast concerns nonzero sample moment means; exactly solved zero means make the centering rules coincide.',
            'Covariance and target identities do not establish finite-sample coverage or qualify any package.'])


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
