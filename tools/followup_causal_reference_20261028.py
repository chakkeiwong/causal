"""Exact authored witnesses; no downloaded code or source experiment execution."""
from fractions import Fraction as F
import json
def calculate():
    target_weights=[F(3,4),F(1,4)]
    conditional_probabilities=[F(1,10),F(9,10)]
    arithmetic=sum(w*p for w,p in zip(target_weights,conditional_probabilities))
    # Weighted logits are -.5*log(9)=-log(3); normalized geometric probability=1/4.
    geometric=F(1,4)
    uniform=sum(conditional_probabilities)/2
    attention=F(1,5)*conditional_probabilities[0]+F(4,5)*conditional_probabilities[1]
    assert (arithmetic,geometric,uniform,attention)==(F(3,10),F(1,4),F(1,2),F(37,50))
    assert arithmetic-geometric==F(1,20)
    correlated_joint=F(1,2);factorized_marginals=F(1,4)
    rows=[dict(name=n,probability=str(p),loss_usd=str(1000*p)) for n,p in [('target_arithmetic',arithmetic),('normalized_geometric',geometric),('uniform_reweighting',uniform),('conditional_attention',attention)]]
    return dict(kind='authored_exact_examples_not_observed_model_results',probabilities=rows,geometric_gap=str(arithmetic-geometric),joint_event=dict(correlated=str(correlated_joint),product_marginals=str(factorized_marginals)),assumptions=['Binary event conditional probabilities1/10and9/10;targetconfounderprobability1/4.','USD1000loss per event stipulated,not estimated.','Conditional attention weight4/5is stipulated,not source implementation output.','Perfectly correlated Bernoulli confounders give joint probability1/2;independence substitution gives1/4.'])
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
