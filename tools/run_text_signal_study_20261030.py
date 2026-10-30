"""Exact constructed example: text contrasts versus a hardship intervention.

Project-written enumeration; no downloaded source code is executed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib, datetime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/twelve-hour-closure/2026-10-29/text-signal-attempt-1'

def joint(tau, intervention=None):
    rows = []
    for u, a, r, y in product((0, 1), repeat=4):
        pa = (F(4, 5) if a == u else F(1, 5)) if intervention is None else F(a == intervention)
        pr = F(3, 4) if r == u else F(1, 4)
        py = F(1, 10) + F(3, 5)*u - tau*a
        assert 0 <= py <= 1
        rows.append(dict(u=u, a=a, r=r, y=y, p=F(1, 2)*pa*pr*(py if y else 1-py)))
    assert sum(x['p'] for x in rows) == 1
    return rows

def expectation(rows, value, condition=lambda x: True):
    chosen = [x for x in rows if condition(x)]
    return sum(x['p']*value(x) for x in chosen)/sum(x['p'] for x in chosen)

def study(tau):
    rows = joint(tau)
    m = {(a,r):expectation(rows,lambda x:x['y'],lambda x:x['a']==a and x['r']==r) for a,r in product((0,1),repeat=2)}
    group_means = {a:expectation(rows,lambda x:m[x['a'],x['r']],lambda x:x['a']==a) for a in (0,1)}
    score_gap = group_means[1]-group_means[0]
    outcome_gap = expectation(rows,lambda x:x['y'],lambda x:x['a']==1)-expectation(rows,lambda x:x['y'],lambda x:x['a']==0)
    rewrite = expectation(rows,lambda x:m[1,x['r']]-m[0,x['r']])
    intervention = expectation(joint(tau,1),lambda x:x['y'])-expectation(joint(tau,0),lambda x:x['y'])
    measured_risk = sum(F(1,2)*(expectation(rows,lambda x:x['y'],lambda x:x['a']==1 and x['u']==u)-expectation(rows,lambda x:x['y'],lambda x:x['a']==0 and x['u']==u)) for u in (0,1))
    # Separate closed-form calculations from the structural probabilities.
    assert score_gap == outcome_gap == F(9,25)-tau
    assert rewrite == F(27,91)-tau
    assert intervention == measured_risk == -tau
    # Conditional calibration holds at every document value, including both arms.
    for (a,r),prob in m.items():
        assert expectation(rows,lambda x:x['y']-prob,lambda x:x['a']==a and x['r']==r)==0
    # All source-style score groups have nonzero score variance here.
    variance={a:expectation(rows,lambda x:(m[x['a'],x['r']]-group_means[a])**2,lambda x:x['a']==a) for a in (0,1)}
    assert all(v>0 for v in variance.values())
    return {'tau':str(tau),'joint':[{**x,'p':str(x['p'])} for x in rows],
            'calibrated_predictions':{f'A{a}_R{r}':str(v) for (a,r),v in m.items()},
            'group_means':{str(k):str(v) for k,v in group_means.items()},
            'contrasts':{k:{'exact':str(v),'decimal':float(v)} for k,v in [('entity_group',score_gap),('outcome_group',outcome_gap),('text_rewrite',rewrite),('actual_intervention',intervention),('truthful_baseline_adjustment',measured_risk)]},
            'score_group_variances':{str(k):str(v) for k,v in variance.items()}}

if __name__ == '__main__':
    assert not OUT.exists(), 'Preserve the first exact study; checks may read it'
    results=[study(F(0)),study(F(1,20))]
    OUT.mkdir(parents=True)
    report={'status':'pass','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'question':'Does exact text prediction turn entity-group contrasts into hardship intervention effects?',
            'scope':'Two finite constructed economies; no bank data, neural training, source-code execution, or general impossibility claim.',
            'design':'U fair binary, P(A=U)=4/5, P(R=U)=3/4; A and R conditionally independent given U. P(Y=1|U,A)=1/10+(3/5)U-tau A. Document W=(A,R).',
            'results':results,'checks':['16 observed cells per economy sum to one','All four prediction cells calibrated exactly','Enumeration matches separate analytic contrasts','Intervention enumeration matches truthful-U adjustment','Nonzero score variance within each entity group'],
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'result.json').write_text(json.dumps(report,indent=2)+chr(10))
    print(json.dumps({'status':'pass','cases':[{'tau':r['tau'],'contrasts':r['contrasts']} for r in results]},indent=2))
