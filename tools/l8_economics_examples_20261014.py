#!/usr/bin/env python3
"""Exact planning examples, with no empirical prices or performance claims."""
from fractions import Fraction as F
from itertools import product


def calculate():
    workflows = []
    for name, low_answer, high_answer, low_errors, high_errors, unit_cost in [
        ('A',80,10,1,1,2), ('B',60,10,3,0,4),
    ]:
        low_defer, high_defer = 80-low_answer, 20-high_answer
        loss = 100*low_errors + 10000*high_errors
        base = unit_cost*100
        fallback = 40*(low_defer+high_defer)
        delay = 5*low_defer+50*high_defer
        workflows.append({'workflow': name, 'answered': low_answer+high_answer,
                          'conditional_accuracy': str(F(low_answer+high_answer-low_errors-high_errors,low_answer+high_answer)),
                          'error_loss':loss,'base_cost':base,'fallback_cost':fallback,'delay_loss':delay,
                          'total_loss_and_cost':loss+base+fallback+delay})
    assert [r['total_loss_and_cost'] for r in workflows] == [11200,2500]
    q,r,c = F(1,100),F(1,500),F(20)
    risk = {'threshold_loss_USD':str(c/(q-r)), 'low_net_review_value':str((q-r)*100-c),
            'high_net_review_value':str((q-r)*10000-c)}
    assert risk == {'threshold_loss_USD':'2500','low_net_review_value':'-96/5','high_net_review_value':'60'}
    retry = []
    for name, persistent, transient in [('independent',F(0),F(1,5)),('persistent_mixture',F(1,10),F(1,9))]:
        # Enumerate latent permanent failure and three transient outcomes, then
        # compare the full-path law with the tail-sum stopping identity.
        nbar,fail,mass=F(0),F(0),F(0)
        for permanent in [False,True]:
            pm=persistent if permanent else 1-persistent
            for bits in product([False,True],repeat=3):
                prob=pm
                for b in bits:prob*=transient if b else 1-transient
                fails=[permanent or b for b in bits]
                attempts=next((i+1 for i,x in enumerate(fails) if not x),3)
                nbar+=prob*attempts;fail+=prob*int(all(fails));mass+=prob
        surv=[F(1)]+[persistent+(1-persistent)*transient**k for k in range(1,4)]
        assert mass==1 and nbar==sum(surv[:3]) and fail==surv[3] and surv[1]==F(1,5)
        retry.append({'law':name,'reach_probabilities':list(map(str,surv[:3])),
                      'expected_attempts':str(nbar),'terminal_failure':str(fail),'expected_cost_USD':str(2*nbar+50*fail)})
    assert retry[0]['expected_cost_USD']=='72/25'
    assert retry[1]['terminal_failure']=='41/405'
    low,high=F(-625),F(1625)
    p=high/(high-low)
    regret = {'state_net_values_USD':[str(low),str(high)], 'robust_action':'hold',
              'deterministic_minimax_action':'act','act_worst_regret':str(-low),'hold_worst_regret':str(high),
              'randomized_action_probability':str(p),'randomized_worst_regret':str(p*(-low))}
    assert p*(-low)==(1-p)*high and p==F(13,18)
    # Projected common interval cannot retain the policy ranking of a joint set.
    pairs=[(F(-100),F(-200)),(F(100),F(0))]
    paired=[b-a for a,b in pairs]
    assert paired==[F(-100),F(-100)]
    projection=[min(b for a,b in pairs)-max(a for a,b in pairs),max(b for a,b in pairs)-min(a for a,b in pairs)]
    joint={'world_values_policy_A_B':[[str(x) for x in row] for row in pairs],
           'B_minus_A_joint':list(map(str,paired)), 'B_minus_A_from_coordinate_box':list(map(str,projection))}
    good,bad,prior,sensitivity,discount,pilot_cost=F(100000),F(-60000),F(1,2),F(4,5),F(9,10),F(10000)
    immediate=max(F(0),prior*good+(1-prior)*bad)
    joint_events=[];gross=F(0)
    for positive in [True,False]:
        a=sensitivity if positive else 1-sensitivity
        b=1-sensitivity if positive else sensitivity
        prob=prior*a+(1-prior)*b
        conditional=(prior*a*good+(1-prior)*b*bad)/prob
        chosen=conditional>0
        gross+=prob*max(F(0),conditional)
        joint_events.append({'signal':'positive' if positive else 'negative','probability':str(prob),
                             'conditional_build_value':str(conditional),'build':chosen})
    direct=prior*sensitivity*good+(1-prior)*(1-sensitivity)*bad
    assert direct==gross==34000 and immediate==20000
    pilot={'immediate_build_value':str(immediate),'events':joint_events,'gross_after_signal':str(gross),
           'pilot_net_no_delay':str(gross-pilot_cost),'pilot_net_discounted':str(discount*gross-pilot_cost),
           'increment_over_immediate':str(discount*gross-pilot_cost-immediate),
           'break_even_discount':str((immediate+pilot_cost)/gross),
           'break_even_symmetric_accuracy':str((30000+(immediate+pilot_cost)/discount)/80000),
           'perfect_information_gross':str(prior*good),'perfect_information_increment':str(prior*good-immediate)}
    assert pilot['increment_over_immediate']=='600' and pilot['break_even_symmetric_accuracy']=='19/24'
    transfer={'formula':'10-40*w USD per request','public_w':'1/5','public_value':str(10-40*F(1,5)),
              'deployment_w':'3/5','deployment_value':str(10-40*F(3,5)),
              'break_even_w':'1/4','w_range':['1/10','2/5'],'value_range':['-6','6']}
    return {'kind':'exact_project_planning_scenarios','prices_probabilities_losses':'All stipulated; no provider or bank estimates',
            'workflow_loss':workflows,'review_triage':risk,'retry':retry,'ambiguity':regret,'joint_policy_values':joint,
            'pilot_option':pilot,'transport_of_workflow_value':transfer,'new_model_calls':0,'new_bank_observations':0}
