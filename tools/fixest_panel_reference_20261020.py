#!/usr/bin/env python3
"""Authored exact algebraic reference, never execution of fixest or R."""
from fractions import Fraction as F
import json


def solve(a, b):
    m = [[F(x) for x in row] + [F(y)] for row, y in zip(a, b)]
    for j in range(len(b)):
        pivot = next(i for i in range(j, len(b)) if m[i][j])
        m[j], m[pivot] = m[pivot], m[j]
        div = m[j][j]
        m[j] = [x / div for x in m[j]]
        for i in range(len(b)):
            if i != j:
                factor = m[i][j]
                m[i] = [x-factor*y for x, y in zip(m[i], m[j])]
    return [row[-1] for row in m]


def fit(rows):
    groups = sorted({r['branch'] for r in rows})
    within = []
    for g in groups:
        rr = [r for r in rows if r['branch'] == g]
        md = sum(F(r['treatment']) for r in rr)/len(rr)
        my = sum(F(r['margin_usd']) for r in rr)/len(rr)
        within += [(r['row_id'], g, F(r['treatment'])-md, F(r['margin_usd'])-my) for r in rr]
    gram = sum(d*d for _, _, d, _ in within)
    if gram == 0:
        return dict(status='treatment_absorbed', coefficient=None, input_ids=[r['row_id'] for r in rows])
    beta = sum(d*y for _, _, d, y in within)/gram
    x = [[F(r['branch'] == g) for g in groups] + [F(r['treatment'])] for r in rows]
    y = [F(r['margin_usd']) for r in rows]
    p = len(x[0])
    xtx = [[sum(row[j]*row[k] for row in x) for k in range(p)] for j in range(p)]
    xty = [sum(row[j]*yy for row, yy in zip(x, y)) for j in range(p)]
    dummy = solve(xtx, xty)
    assert dummy[-1] == beta
    scores = {g:sum(d*(yy-d*beta) for _, gg, d, yy in within if gg == g) for g in groups}
    assert sum(scores.values()) == 0
    cr0 = sum(s*s for s in scores.values())/(gram*gram)
    n, G = len(rows), len(groups)
    k_none, k_full = 1, p
    adjusted = {str(k):cr0*F(n-1,n-k)*F(G,G-1) for k in [k_none,k_full]}
    return dict(status='algebraic_reference', beta=str(beta), dummy_coefficients=[str(v) for v in dummy],
        within_gram=str(gram), scores={g:str(v) for g,v in scores.items()}, cr0=str(cr0),
        covariance_by_K={k:str(v) for k,v in adjusted.items()}, cluster_t_df=G-1,
        input_ids=[r['row_id'] for r in rows], n=n, clusters=G)


def calculate():
    rows=[dict(row_id=f'{g}{t+1}',branch=g,period=t+1,treatment=d,margin_usd=y)
        for g, ds, ys in [('A',[0,1],[10,12]),('B',[1,0],[20,16]),('C',[0,1],[30,36])]
        for t,(d,y) in enumerate(zip(ds,ys))]
    fitted=fit(rows)
    assert fitted['beta']=='4' and fitted['cr0']=='8/9'
    assert fitted['covariance_by_K']=={'1':'4/3','4':'10/3'}
    shuffled=fit(list(reversed(rows)))
    assert all(fitted[k]==shuffled[k] for k in ['beta','scores','cr0','covariance_by_K'])
    absorbed=fit([dict(r,treatment=int(r['branch']=='B')) for r in rows])
    assert absorbed['coefficient'] is None and absorbed['status']=='treatment_absorbed'
    b=[F(2),F(8)]; a=[F(3,4),F(1,4)]; V=[[F(4),F(1)],[F(1),F(9)]]
    effect=sum(w*v for w,v in zip(a,b))
    variance=sum(a[i]*V[i][j]*a[j] for i in range(2) for j in range(2))
    diagonal=sum(a[i]**2*V[i][i] for i in range(2))
    assert effect==F(7,2) and variance==F(51,16) and diagonal==F(45,16)
    return dict(kind='project_authored_exact_reference',software_executed=False,bank_observations=False,
        input_rows=rows,units='Outcome USD margin per account-period; binary outreach indicator',
        projection=fitted,row_permutation_invariant=True,absorbed_treatment=absorbed,
        aggregation=dict(coefficients=[str(x) for x in b],weights=[str(x) for x in a],
            covariance=[[str(x) for x in row] for row in V],effect=str(effect),variance=str(variance),
            diagonal_only_variance=str(diagonal),wrong_weighted_standard_error='9/4',
            equal_share_effect='5',stipulated_incremental_cost_usd='4',
            target_net_margin=str(effect-4),equal_share_net_margin='1'),
        limitations=['Algebraic oracles only; no identification, sampling coverage, native conformance or observed economics.',
            'Three clusters are intentionally small; t degrees of freedom are bookkeeping, not evidence of calibration.',
            'K conventions are explicit alternatives; no assertion that every fixest option returns these values without native qualification.'])


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
