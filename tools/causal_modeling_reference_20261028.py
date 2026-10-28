"""Independent finite causal-modeling witnesses; no native LLM or benchmark execution."""
from fractions import Fraction as F

def calculate():
    additive={(a,b):100+10*a+20*b for a in (0,1) for b in (0,1)}
    interaction={(a,b):y+5*a*b for (a,b),y in additive.items()}
    contrast=lambda d:d[1,1]-d[1,0]-d[0,1]+d[0,0]
    assert contrast(additive)==0 and contrast(interaction)==5
    means=[];mediator=[]
    for a in (0,1):
        b=[int(u<1+2*a) for u in range(4)]
        mediator.append(F(sum(b),4));means.append(F(sum(100+20*x-10*a for x in b),4))
    assert mediator==[F(1,4),F(3,4)] and means==[F(105),F(105)]
    return dict(additive_cells=[dict(a=a,b=b,outcome_usd=y) for (a,b),y in additive.items()],
       interaction_cells=[dict(a=a,b=b,outcome_usd=y) for (a,b),y in interaction.items()],
       additive_interaction_usd=contrast(additive),modified_interaction_usd=contrast(interaction),
       cancellation_mediator_probabilities=list(map(str,mediator)),cancellation_outcome_means_usd=list(map(str,means)),
       cancellation_total_effect_usd=str(means[1]-means[0]),direct_effect_usd=-10,mediated_effect_usd=10,
       inconsistent_pairwise_partition=dict(pairs=[[0,1,True],[1,2,True],[0,2,False]],transitive=False),
       source_result_replication=False,bank_evidence=False)

if __name__=='__main__':
    import json
    print(json.dumps(calculate(),indent=2))
