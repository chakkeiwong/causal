"""Exact and scalar checks for the release's graph-confidence comparison."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/release/2026-10-29/graph-source-064'


def bernoulli_kl(p, q):
    return sum(x * math.log(x / y) for x, y in [(p, q), (1-p, 1-q)] if x)


def main():
    q, budget = .1, .5
    lower, upper = q, 1.
    for _ in range(100):
        middle = (lower + upper) / 2
        if bernoulli_kl(middle, q) <= budget:
            lower = middle
        else:
            upper = middle
    assert abs(bernoulli_kl(lower, q) - budget) < 1e-14
    assert bernoulli_kl(q, q) == 0 and 1-q > 1-lower
    reference = [F(1,20), F(1,20), F(899,1000), F(1,1000)]
    predictive = [F(1,20), F(1,20), F(1,1000), F(899,1000)]
    full_kl = sum(float(p) * math.log(float(p/s)) for p,s in zip(reference,predictive))
    required = bernoulli_kl(.95, .1)
    assert sum(reference) == sum(predictive) == 1
    assert sum(reference[:2]) == sum(predictive[:2]) == F(1,10)
    assert abs(full_kl - .898*math.log(899)) < 1e-14 and full_kl > required
    branches = [bernoulli_kl(p,.5) for p in [.05,.95]]
    assert abs(branches[0]-branches[1]) < 1e-14
    assert all(abs(x/branches[1]-1) < 1e-14 for x in branches)
    p = F(4,5)
    rows = []
    for edges in product([0,1], repeat=3):
        probability = p**sum(edges) * (1-p)**(3-sum(edges))
        rows.append(dict(edges=list(edges), probability=str(probability), cycle=all(edges)))
    acyclic = sum(F(r['probability']) for r in rows if not r['cycle'])
    conditional = [sum(F(r['probability']) for r in rows if not r['cycle'] and r['edges'][i])/acyclic for i in range(3)]
    assert 1-acyclic == F(64,125) and conditional == [F(36,61)]*3
    assert max(sum(r['edges']) for r in rows if not r['cycle']) == 2
    assert 3*p > 2
    difference = F(723,1000)-F(712,1000)
    assert difference == F(11,1000)
    overlap = (min(F(7,10),F(7,10))-max(F(1,2),F(1,2)))/(F(7,10)-F(1,2))
    assert overlap == 1 and not F(1,2) <= 0 <= F(7,10)
    jensen = (bernoulli_kl(.5,.2)+bernoulli_kl(.5,.8))/2
    assert jensen > 0 and bernoulli_kl(.5,.5) == 0
    selected_lift = math.log(.1/.01)
    distribution_kl = bernoulli_kl(.1,.01)
    assert selected_lift > distribution_kl
    result = dict(status='pass', scope='Project exact constructions and scalar algebra; no upstream package execution, model calls or new empirical study.',
        bound=dict(q=q,budget=budget,p_max=lower,error_floor=1-lower,feasible_p=q,feasible_error=1-q),
        information=dict(reference=list(map(str,reference)),predictive=list(map(str,predictive)),event=[0,1],full_kl=full_kl,required_95=required,event_probability=.1,branches=branches,branch_ratios=[x/branches[1] for x in branches],jensen_gap=jensen,selected_lift=selected_lift,distribution_kl=distribution_kl),
        graphs=dict(rows=rows,cycle_probability=str(1-acyclic),conditional_marginals=list(map(str,conditional)),proposed_expected_edges=str(3*p),maximum_dag_edges=2),
        evaluation=dict(reported_iou_difference=str(difference),identical_interval_iou=str(overlap),true_effect=0,contains_effect=False,margins=[20,-40]),
        source=dict(path=str(Path(__file__).relative_to(ROOT)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    (BASE/'exact-witnesses.json').write_text(json.dumps(result,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in result.items() if k!='graphs'}))


if __name__ == '__main__':
    main()
