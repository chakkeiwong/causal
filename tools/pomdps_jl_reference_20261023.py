#!/usr/bin/env python3
"""Project-owned finite-law witnesses; never execute upstream Julia."""
from fractions import Fraction as F
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def calculate():
    p = F(1, 4)
    joint = [(u, u, -40 if u else 8, p if u else 1-p) for u in [0, 1]]
    expected = sum(m*r for s,o,r,m in joint)
    coherent = sum(m for s,o,r,m in joint if s == o)
    independent = sum((p if s else 1-p)*(p if o else 1-p)
                      for s in [0, 1] for o in [0, 1] if s == o)
    rescue_joint = sum(m*(35 if s else -15) for s,o,r,m in joint if o)
    rescue_split = p*(p*35+(1-p)*(-15))
    assert expected == -4 and coherent == 1 and independent == F(5, 8)
    assert rescue_joint == F(35, 4) and rescue_split == F(-5, 8)
    raw = ROOT/'docs/literature/raw'
    generative = (raw/'exec23_pomdpsjl_05.txt').read_text()
    model = (raw/'exec23_pomdpsjl_03.txt').read_text()
    belief = (raw/'exec23_pomdpsjl_06.txt').read_text()
    assert 'x = gen(m, s, a, rng)' in generative
    assert 'if haskey(x, $sym)' in generative
    assert ':o => [:s, :a, :sp]' in generative
    assert ':r => [:s, :a, :sp, :o]' in generative
    assert 'reward(m::Union{POMDP,MDP}, s, a, sp) = reward(m, s, a)' in model
    assert 'isterminal(problem::Union{POMDP,MDP}, state) = false' in model
    assert 'initialize_belief(updater::Updater, belief) = belief' in belief
    return dict(kind='authored_exact_reference_not_native_execution',
        joint_generator=dict(distress_probability=str(p), expected_reward=str(expected),
            coherent_state_observation_probability=str(coherent),
            split_call_state_observation_probability=str(independent),
            joint_alert_loss_probability=str(p), split_alert_loss_probability=str(p*p),
            coherent_signal_rescue_value=str(rescue_joint), split_signal_rescue_value=str(rescue_split)),
        reward_conversion=dict(probability_weighted_reward=str(expected),
            unweighted_state_average=str(F(-40+8,2))),
        terminal_clock=dict(reward_on_entry='12', terminal_continuation='0',
            correctly_retained_value='12', destination_masked_value='0'),
        observation_domain=dict(previous_state_zero_next_zero_alert='0',
            previous_state_one_next_zero_alert='1',
            same_action_next_state_cannot_determine_both=True),
        native_execution=False)

if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
