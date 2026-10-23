#!/usr/bin/env python3
"""Independent finite-law witnesses; no upstream source or tests are executed."""
from fractions import Fraction as F
import json


def calculate():
    # A fails at 1, B enters strictly after 1, C remains at risk.
    rows = [(F(0), F(1), 1), (F(1), F(2), 0), (F(0), F(2), 0)]
    risk_count = sum(start < 1 <= stop for start, stop, _ in rows)
    assert risk_count == 2
    correct_increment, all_rows_increment = F(1, risk_count), F(1, len(rows))
    breslow, efron = F(2, 3), F(1, 3) + F(1, 2)
    # Coefficient log(2), event covariate zero, other covariate one.
    denominator = F(2) * 1 + F(1) * 2
    displayed_no_ties, weighted_breslow = 1 / denominator, 1 / denominator**2
    # Model log-risk log(2) implies exponentiated score 2, not an absolute risk.
    survival_a, survival_b = F(1, 2)**2, F(3, 4)**2
    risk_a, risk_b = 1 - survival_a, 1 - survival_b
    # Cluster contributions and arbitrary example inverse-information scalar.
    row_scores = [1, 1, -1, -1]
    bread = F(1, 4)
    row_variance = bread**2 * sum(v*v for v in row_scores)
    cluster_scores = [sum(row_scores[:2]), sum(row_scores[2:])]
    cluster_variance = bread**2 * sum(v*v for v in cluster_scores)
    # Trace of the inspected unclustered robust cleanup's missing increment.
    original_lp, original_score = [2, 3], [4, 8]
    saved_lp, saved_score = [0, 0], [0, 0]
    for lp, score in zip(original_lp, original_score):
        saved_lp[0], saved_score[0] = lp, score
    assert saved_lp == [3, 0] and saved_score == [8, 0]
    return {
        'delayed_entry': {'risk_set': ['A', 'C'], 'correct_increment': str(correct_increment),
            'all_rows_decrement_path_increment': str(all_rows_increment), 'native_reachability_tested': False},
        'ties': {'unit_risks': 3, 'tied_events': 2, 'breslow': str(breslow), 'efron': str(efron)},
        'weighted_no_ties': {'weights': [2, 1], 'risk_scores': [1, 2],
            'displayed_formula': str(displayed_no_ties), 'weighted_breslow_formula': str(weighted_breslow),
            'displayed_score_derivative': '-1/2', 'weighted_breslow_score_derivative': '-1'},
        'absolute_risk': {'same_exponentiated_score': 2, 'baseline_survival': ['1/2', '3/4'],
            'survival': [str(survival_a), str(survival_b)], 'risk': [str(risk_a), str(risk_b)],
            'stipulated_loss_usd': 1000, 'stipulated_premium_usd': 600,
            'expected_loss_usd': [str(1000*risk_a), str(1000*risk_b)],
            'margin_usd': [str(600-1000*risk_a), str(600-1000*risk_b)]},
        'event_coding': {'subjects': 10, 'default': 1, 'prepayment': 4,
            'default_incidence': '1/10', 'collapsed_nonminimum_event_incidence': '1/2',
            'stipulated_loss_usd': 1000, 'expected_default_loss_usd': 100, 'collapsed_event_loss_usd': 500},
        'sandwich': {'row_scores': row_scores, 'cluster_scores': cluster_scores, 'bread': str(bread),
            'row_variance': str(row_variance), 'cluster_variance': str(cluster_variance)},
        'biojava_unclustered_cleanup_trace': {'original_lp': original_lp, 'original_score': original_score,
            'restored_lp': saved_lp, 'restored_score': saved_score, 'full_fit_executed': False},
        'biojava_cluster_guard': {'null_value': 'dereference before intended exception',
            'empty_string': 'passes the inspected conjunction', 'nonempty_string': 'passes'},
        'secure_tie_partition': {'times_A': [1, 1, 2], 'times_B': [10, 10, 20],
            'same_equality_partition': [[0, 1], [2]], 'raw_times_reconstructed': False},
        'scope': 'Project-owned exact formulas and abstract traces; no fitted estimates, empirical coverage, native software execution, measured prices or bank observations.'
    }


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
