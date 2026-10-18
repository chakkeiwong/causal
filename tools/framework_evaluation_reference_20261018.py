#!/usr/bin/env python3
"""Exact authored evaluation accounting; no model, framework or bank calls."""
from fractions import Fraction as F
import json


def calculate():
    # Twenty business contracts; two wordings share exactly the same outcome.
    # True/False denotes stipulated correct/incorrect completed answers.
    # None is an unanswered request, not a correct scientific refusal.
    systems = {
        'A': ([True] * 11 + [False] + [None] * 8, F(12)),
        'B': ([True] * 15 + [False] * 3 + [None] * 2, F(24)),
    }
    results = {}
    for name, (contracts, cost) in systems.items():
        jobs = [value for value in contracts for _ in range(2)]
        completed = sum(value is not None for value in jobs)
        correct = sum(value is True for value in jobs)
        wrong = sum(value is False for value in jobs)
        assert correct + wrong == completed
        results[name] = dict(
            contract_families=len(contracts), planned_requests=len(jobs),
            completed=completed, correct=correct, wrong=wrong,
            unanswered=len(jobs) - completed,
            completion_fraction=str(F(completed, len(jobs))),
            joint_correct_fraction=str(F(correct, len(jobs))),
            conditional_correct_fraction=str(F(correct, completed)),
            assumed_total_cost_USD=str(cost),
            assumed_net_USD_per_planned_request={
                str(penalty): str((10 * correct - penalty * wrong - cost) / len(jobs))
                for penalty in [F(20), F(5)]
            },
            paired_wordings_identical=True,
        )
    assert results['A']['assumed_net_USD_per_planned_request'] == {'20': '21/5', '5': '99/20'}
    assert results['B']['assumed_net_USD_per_planned_request'] == {'20': '39/10', '5': '123/20'}
    return dict(
        provenance='Project-authored exact bookkeeping example, 18 October 2026',
        empirical_model_or_bank_evidence=False, systems=results,
        sampling_note='Forty fixed requests form twenty paired contract families; no confidence interval or independent-request model is asserted.',
        semantic_note='A correct nonidentification certificate or clarification may be a completed correct answer; None is missing execution, not that scientific response.',
    )


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
