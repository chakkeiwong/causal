#!/usr/bin/env python3
"""Exact benchmark deductions and stipulated banking examples; no model calls."""
from fractions import Fraction as F


def f1(response, gold, epsilon=F(1, 100_000_000)):
    overlap = len(response & gold)
    precision = F(overlap) / (len(response) + epsilon)
    recall = F(overlap) / (len(gold) + epsilon)
    return 2 * precision * recall / (precision + recall + epsilon)


def calculate():
    tasks = list(map(F, ['.83', '.70', '.52', '.50', '.35', '.75',
                         '.81', '.72', '.79', '.77', '.90', '.61']))
    mean = sum(tasks) / 12
    half_rounding_unit = F(1, 200)
    task_interval = [mean-half_rounding_unit, mean+half_rounding_unit]
    reported = F('.70')
    report_interval = [reported-half_rounding_unit, reported+half_rounding_unit]
    assert mean == F(11, 16) and task_interval[1] < report_interval[0]
    # Independent integer denominator calculation, conditional on 100 cases/task.
    successes = [83, 70, 52, 50, 35, 75, 81, 72, 79, 77, 90, 61]
    assert sum(successes) == 825 and F(sum(successes), 1200) == mean

    prevalence = F(1, 2)
    classifiers = []
    for label, tpr, fpr in [('A', F(4, 5), F(1, 10)),
                             ('B', F(19, 20), F(1, 5)),
                             ('always_no', F(0), F(0))]:
        accuracy = prevalence*tpr + (1-prevalence)*(1-fpr)
        value = 20*prevalence*tpr - 80*(1-prevalence)*fpr
        tp, fp = int(200*tpr), int(200*fpr)
        tn, fn = 200-fp, 200-tp
        assert F(tp+tn, 400) == accuracy
        assert F(20*tp-80*fp, 400) == value
        classifiers.append(dict(name=label, tpr=tpr, fpr=fpr,
            accuracy=accuracy, value_usd=value,
            counts=dict(tp=tp, fp=fp, tn=tn, fn=fn)))
    assert classifiers[0]['accuracy'] == F(17, 20)
    assert classifiers[0]['value_usd'] == 4
    assert classifiers[1]['accuracy'] == F(7, 8)
    assert classifiers[1]['value_usd'] == F(3, 2)

    # Equal response-token sets can express opposite direction; no upstream
    # regex behavior, tokenization implementation or whole-score exploit assumed.
    forward = 'funding causes deposits'
    reverse = 'deposits causes funding'
    gold = {'funding', 'causes', 'deposits'}
    r_forward, r_reverse = set(forward.split()), set(reverse.split())
    assert r_forward == r_reverse == gold
    overlap_score = f1(r_forward, gold)
    assert overlap_score == f1(r_reverse, gold)
    noncounterfactual = []
    for cir in [F(0), F(1, 3), F(4, 5), F(1)]:
        for clp in [F(0), F(1, 2), F(1)]:
            original = F(2, 5)*cir + F(7, 20)*clp + F(1, 4)*cir
            reduced = F(13, 20)*cir + F(7, 20)*clp
            assert original == reduced
            noncounterfactual.append(dict(cir=cir, clp=clp, car=original))

    # Law: D_ij = U_i + E_ij, Var(U)=1, Var(E)=1; independent across
    # mechanisms, with independent within-mechanism E. Exact second moments.
    n, repeats = 12, 8
    true_variance = (F(1)+F(1, repeats))/n
    naive_variance = F(2, n*repeats)
    design_effect = true_variance/naive_variance
    assert design_effect == 1+(repeats-1)*F(1, 2) == F(9, 2)
    # Separate count of equal-mechanism and within-mechanism covariance terms.
    ordered_covariance_sum = n*(2*repeats + repeats*(repeats-1))
    assert F(ordered_covariance_sum, (n*repeats)**2) == true_variance

    return dict(
        cello=dict(task_accuracies=tasks, arithmetic_mean=mean,
            equal_task_rounding_envelope=task_interval,
            reported_all=reported, reported_rounding_envelope=report_interval,
            integer_successes=sum(successes), conditional_denominator=1200,
            finding='Disjoint conventional-rounding envelopes under the stated equal-task interpretation; cause unresolved.'),
        bank_example=dict(prevalence=prevalence, valid_reward_usd=20,
            invalid_loss_usd=80, withholding_value_usd=0,
            endorsement_probability_threshold=F(4, 5), classifiers=classifiers,
            always_no_balanced_accuracy=F(1, 2), always_no_all_no_accuracy=F(1)),
        metric=dict(epsilon=F(1, 100_000_000), same_set_direction_examples=[forward, reverse],
            common_f1=overlap_score, full_composite_exploit_demonstrated=False,
            noncounterfactual_reduction='CAR = 13/20 CIR + 7/20 CLP',
            rational_checks=noncounterfactual),
        clustered_example=dict(mechanisms=n, paired_variants_per_mechanism=repeats,
            common_variance=1, idiosyncratic_variance=1,
            true_mean_variance=true_variance, naive_independent_variance=naive_variance,
            design_effect=design_effect, standard_error_ratio_squared=design_effect),
        checks=['Rounding envelopes are disjoint even with conservative closed endpoints.',
            'Separate integer totals agree with the equal-task arithmetic mean.',
            'Independent confusion-count enumeration reproduces accuracy and stipulated value.',
            'Equal response-token sets have equal set-F1 despite reversed word order.',
            'Non-counterfactual CAR reduction checked at twelve rational pairs.',
            'Ordered covariance count reproduces the random-effects variance.'],
        limits=['No live-model evaluation, upstream execution, sample-level source reconstruction or measured bank ROI.',
            'The source discrepancy is conditional on its stated equal-task interpretation; its cause is unknown.',
            'Bank values and the random-effects law are project assumptions, not literature observations.'])


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serial(v) for v in value]
    return value


if __name__ == '__main__':
    import json
    print(json.dumps(serial(calculate()), indent=2))
