#!/usr/bin/env python3
"""Exact authored causal-law and prediction-audit examples; no model execution."""
from fractions import Fraction as F
import json


def number(value):
    value = F(value)
    return dict(exact=str(value), decimal=float(value))


def calculate():
    worlds = []
    for name in ['action_causes_response', 'latent_state_causes_both']:
        observed = {}
        means = {}
        for action in [0, 1]:
            means[action] = sum(F(1, 2) * (100 * action if name == 'action_causes_response' else 100 * u)
                                for u in [0, 1])
        for u in [0, 1]:
            action = u
            outcome = 100 * action if name == 'action_causes_response' else 100 * u
            observed[f'A={action},Y={outcome}'] = str(F(1, 2))
        effect = means[1] - means[0]
        worlds.append(dict(name=name, observational_law=observed,
            intervention_means={str(a): number(y) for a, y in means.items()},
            average_effect=number(effect), contact_cost=number(10),
            all_contact_versus_no_contact_incremental_net=number(effect - 10)))
    assert worlds[0]['observational_law'] == worlds[1]['observational_law']
    assert [x['average_effect']['exact'] for x in worlds] == ['100', '0']
    assert [x['all_contact_versus_no_contact_incremental_net']['exact'] for x in worlds] == ['90', '-10']

    examples = []
    for name, gold, text, visual in [
            ('agreement_can_be_wrong', 'AAAA', 'BBBB', 'BBBB'),
            ('equal_accuracy_can_disagree_everywhere', 'AAAA', 'AABB', 'BBAA')]:
        n = len(gold)
        ta = sum(F(t == g, n) for t, g in zip(text, gold))
        va = sum(F(v == g, n) for v, g in zip(visual, gold))
        flip = sum(F(t != v, n) for t, v in zip(text, visual))
        p01 = sum(F(t != g and v == g, n) for t, v, g in zip(text, visual, gold))
        p00d = sum(F(t != g and v != g and t != v, n) for t, v, g in zip(text, visual, gold))
        assert flip - (ta - va) == 2 * p01 + p00d
        examples.append(dict(name=name, gold=list(gold), text=list(text), visual=list(visual),
            text_accuracy=number(ta), visual_accuracy=number(va), flip_rate=number(flip),
            accuracy_difference=number(ta-va), flip_minus_accuracy_difference=number(flip-(ta-va)),
            visual_only_correct_mass=number(p01), both_wrong_disagree_mass=number(p00d)))

    rows = []
    for label, baseline, value, printed_delta in [
            ('Table5 LLaVA7b ViQuAE reminder Acc', '53.26', '53.99', '-1.66'),
            ('Table5 LLaVA7b ViQuAE answer-conflict Acc', '53.26', '54.58', '-1.07'),
            ('Table5 LLaVA7b ViQuAE reminder R.Acc', '58.11', '57.25', '-2.53'),
            ('Table5 LLaVA7b ViQuAE answer-conflict R.Acc', '58.11', '58.51', '-1.27'),
            ('Table5 LLaVA7b InfoSeek reminder Acc', '22.11', '21.25', '-0.86'),
            ('Table5 LLaVA7b InfoSeek answer-conflict Acc', '22.11', '20.23', '-1.88'),
            ('Table4 LLaVA34b ViQuAE DCD Acc', '80.99', '83.35', '2.36'),
            ('Table4 LLaVA34b InfoSeek DCD Acc', '66.02', '68.14', '2.12'),
            ('Table4 InstructBlip7b InfoSeek DCD Acc', '50.53', '50.53', '0.00')]:
        delta = F(value) - F(baseline)
        rows.append(dict(anchor=label, printed_baseline=baseline, printed_value=value,
            printed_delta_pp=printed_delta, recomputed_delta_pp=number(delta),
            displayed_arithmetic_consistent=delta == F(printed_delta)))
    assert sum(not r['displayed_arithmetic_consistent'] for r in rows) == 4
    return dict(status='authored_exact_reference_not_model_or_bank_execution',
        assumptions=['U is Bernoulli(1/2); natural action A=U; gross outcomes and costs are stipulated USD per eligible account.',
            'World1 has Y(a)=100a; World2 has Y(a)=100U; both observe only A and Y.',
            'Prediction examples stipulate answer arrays, not hidden representations or empirical model behavior.',
            'Paper arithmetic transcribes selected v1 cells; it does not resolve the underlying raw experimental values.'],
        observational_twins=worlds, prediction_diagnostics=examples,
        correctness_identity='FR-(Acc_text-Acc_visual)=2*P(text_wrong,visual_correct)+P(both_wrong,answers_differ)',
        displayed_table_arithmetic=rows,
        cross_table_baseline_conflict=dict(anchor='Selected v1 physical pages5/9,Tables2/4,LLaVA34b ViQuAE textual Acc',
            table2='82.46', table4='80.99', difference_pp=number(F('82.46')-F('80.99')),
            disposition='Preserve both; raw data and author clarification unacquired.'),
        reported_mean_34b_DCD_gain_pp=number((F('2.36')+F('2.12'))/2),
        interpretation='Text support, answer agreement, correctness, causal identification and decision value require distinct checks. No native capability or measured bank return follows.')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2) + '\n', end='')
