#!/usr/bin/env python3
"""Authored finite proposal witnesses; no downloaded implementation is run."""
from fractions import Fraction as F
import json


def calculate():
    loans = [('k', 100), ('k', 200)]
    contacts = [('k', 'a'), ('k', 'b')]
    joined = [(k, amount, contact) for k, amount in loans
              for match, contact in contacts if k == match]
    records = [dict(event=2, available=3, value=20),
               dict(event=4, available=8, value=200)]
    event_only = max((r for r in records if r['event'] <= 5), key=lambda r: r['event'])
    available = max((r for r in records if r['event'] <= 5 and r['available'] <= 5),
                    key=lambda r: r['event'])
    p = F(4, 5)
    losses = [100, 1000]
    expected_loss = p * losses[0] + (1 - p) * losses[1]
    match_variance = p * (1 - p) * (losses[1] - losses[0]) ** 2
    attempts = [('a', 'failed_after_effect', 3), ('a', 'success', 1),
                ('b', 'failed_before_effect', 3), ('b', 'success', 1)]
    success_cost = sum(cost for _, status, cost in attempts if status == 'success')
    total_cost = sum(cost for _, _, cost in attempts)
    side_effects = ['payment-1', 'payment-1']
    left_sum = (1e16 + -1e16) + 1.0
    right_sum = 1e16 + (-1e16 + 1.0)
    assert len(joined) == 4 and sum(x[1] for x in joined) == 600
    assert len(joined) <= len(loans) + len(contacts)
    assert event_only['value'] == 200 and available['value'] == 20
    assert expected_loss == 280 and match_variance == 129600
    assert total_cost == 8 and success_cost == 2
    assert left_sum == 1.0 and right_sum == 0.0
    return dict(
        kind='authored_finite_examples_not_native_benchmarks',
        cardinality=dict(left_rows=2, right_rows=2, joined_rows=len(joined),
            row_limit=4, exceeds_strict_limit=False, logical_exposure_usd=300,
            repeated_exposure_usd=600, excess_usd=300),
        clock=dict(decision=5, records=records, event_only_value=200,
            available_value=20, hindsight_difference=180,
            positive_tolerance_example=dict(left_time=5,right_time=7,tolerance=2,accepted=True)),
        linkage=dict(probability_correct=str(p), possible_losses_usd=losses,
            expected_loss_usd=str(expected_loss), plug_in_loss_usd=100,
            conditional_variance_usd_squared=str(match_variance),
            hypothetical_10000_account_understatement_usd=str(10000*(expected_loss-100))),
        missing_identity=dict(left_missing_keys=2,right_missing_keys=2,
            equal_missing_join_pairs=4,verified_person_matches=0),
        effects=dict(attempted_effects=len(side_effects),logical_effects=len(set(side_effects)),
            naive_payment_usd=100*len(side_effects),deduplicated_payment_usd=100*len(set(side_effects))),
        retry_accounting=dict(attempts=attempts,requested_logical_jobs=2,attempt_count=4,
            success_count=2,failed_attempt_count=2,total_cost=total_cost,success_only_cost=success_cost,
            cost_per_completed_request=str(F(total_cost,2)),misleading_cost_per_success=str(F(success_cost,2))),
        replicated_rng=dict(independent_logical_draws=100,stored_copies=200,
            true_mean_variance='1/100',naive_mean_variance='1/200',
            standard_error_understatement_factor='sqrt(2)'),
        reduction=dict(terms=['1e16','-1e16','1'],exact_real_sum='1',
            binary64_left_grouping=left_sum,binary64_right_grouping=right_sum),
        native_execution=False,bank_observations=False,
    )


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
