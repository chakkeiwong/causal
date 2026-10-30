"""Authored exact laws for text scores, intervention effects and target weights."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/release/2026-10-29/text-signals-066'


def main():
    cells = []
    for u, a, y in product([0, 1], repeat=3):
        pa = F(1+3*u, 5)
        py = F(1+6*u, 10)
        mass = F(1, 2) * (pa if a else 1-pa) * (py if y else 1-py)
        cells.append(dict(u=u, a=a, y=y, mass=str(mass)))
    assert sum(F(r['mass']) for r in cells) == 1
    observed = []
    for a in [0, 1]:
        denominator = sum(F(r['mass']) for r in cells if r['a'] == a)
        observed.append(sum(F(r['mass'])*r['y'] for r in cells if r['a'] == a)/denominator)
    intervention = [sum(F(1,2)*F(1+6*u,10) for u in [0,1]) for a in [0,1]]
    assert observed == [F(11,50), F(29,50)]
    assert intervention == [F(2,5),F(2,5)]
    score_gap = observed[1]-observed[0]
    assert score_gap == F(9,25)
    assert 100*score_gap-10 == 26 and 100*(intervention[1]-intervention[0])-10 == -10
    propensities = [F(1,5),F(4,5)]
    effects = [F(0),F(3,10)]
    pa = sum(propensities)/2
    weights = [F(1,2)*p/pa for p in propensities]
    ate = sum(effects)/2
    att = sum(w*t for w,t in zip(weights,effects))
    assert weights == [F(1,5),F(4,5)] and pa == F(1,2)
    assert ate == F(3,20) and att == F(6,25)
    assert [100*ate-20,100*att-20] == [-5,4]
    result = dict(status='pass',scope='Exact authored finite probability constructions. No downloaded code execution or reproduction of source experiments.',
        score=dict(cells=cells,conditional_means=list(map(str,observed)),intervention_means=list(map(str,intervention)),calibrated_score_gap=str(score_gap),naive_net=26,causal_net=-10),
        targets=dict(propensities=list(map(str,propensities)),effects=list(map(str,effects)),treatment_probability=str(pa),treated_weights=list(map(str,weights)),ate=str(ate),att=str(att),net_ate=-5,net_att=4),
        source=dict(path=str(Path(__file__).relative_to(ROOT)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    (OUT/'exact-witnesses.json').write_text(json.dumps(result,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in result.items() if k!='score'}))


if __name__ == '__main__':
    main()
