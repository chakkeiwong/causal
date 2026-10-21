"""Authored exact checks for bowtie extraction metrics and intervention meaning."""
from fractions import Fraction as F
import json


def calculate():
    baseline, guided = [21, 10, 49], [9, 11, 60]
    assert sum(baseline) == sum(guided) == 80
    # An independent two-by-two design whose score depends entirely on interaction.
    cells = {(p,c): F(p==c) for p in [0,1] for c in [0,1]}
    mean = sum(cells.values())/4
    variance = sum((y-mean)**2 for y in cells.values())/4
    first, total = {}, {}
    for j,name in enumerate(['prompt','context']):
        conditional_means = [sum(v for k,v in cells.items() if k[j]==x)/2 for x in [0,1]]
        first[name] = sum((v-mean)**2 for v in conditional_means)/2/variance
        complement = 1-j
        conditional_variances=[]
        for x in [0,1]:
            vals=[v for k,v in cells.items() if k[complement]==x]
            conditional_variances.append(sum((v-sum(vals)/2)**2 for v in vals)/2)
        total[name]=sum(conditional_variances)/2/variance
    assert first == {'prompt':F(0),'context':F(0)}
    assert total == {'prompt':F(1),'context':F(1)}
    # Complete node recovery with one missing decision-critical bridge.
    nodes=set(range(101));gold={(i,i+1) for i in range(100)}
    predicted=gold-{(49,50)}
    reached={0}
    while True:
        next_reached=reached|{b for a,b in predicted if a in reached}
        if next_reached==reached:break
        reached=next_reached
    assert 100 not in reached and len(nodes)==101
    effect_risk_increasing = F(1)-F(0)
    effect_risk_decreasing = F(0)-F(1)
    margin=lambda effect: -10*effect-2
    assert (margin(effect_risk_increasing),margin(effect_risk_decreasing)) == (-12,8)
    return dict(reported_counts=dict(baseline=baseline,guided=guided,per_condition=80,
        baseline_hallucination_rate=str(F(21,80)),guided_hallucination_rate=str(F(9,80)),
        hallucination_reduction_points=str(100*F(12,80)),unclear_change=1,
        schema_invalid=12,schema_total=32,schema_invalid_rate=str(F(12,32))),
        interaction_witness=dict(cells=[dict(prompt=p,context=c,score=str(y)) for (p,c),y in cells.items()],
            mean=str(mean),variance=str(variance),first_order={k:str(v) for k,v in first.items()},
            total_order={k:str(v) for k,v in total.items()},conditional_context_change=['-1','1']),
        critical_path=dict(nodes=101,gold_edges=100,predicted_edges=99,node_f1='1',
            edge_f1=str(F(2*99,2*99+1)),end_to_end_path_retained=False),
        same_topology=dict(graph='A -> Y',models=['Y=A','Y=1-A'],
            effects=[str(effect_risk_increasing),str(effect_risk_decreasing)],
            assumed_loss_per_event=10,assumed_action_cost=2,margins=[-12,8]),
        limits=['Printed counts are transcriptions, not reproduced model outputs.',
            'Independent binary factors and uniform design probabilities are stipulated in the interaction example.',
            'No first-order Sobol index or repeated identical output alone proves pipeline equivalence or scientific truth.',
            'Identical graph topology does not supply mechanisms; the two example laws need not have the same observed distribution.',
            'High graph F1 can coexist with a missing decision-critical path; example graphs are authored.',
            'Assumed loss and cost values are hypothetical, not bank evidence.'])


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
