#!/usr/bin/env python3
"""Exact authored availability-clock reference; imports no Feast code."""
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import permutations
import json


@dataclass(frozen=True)
class Row:
    entity: str
    event: int
    created: int | None
    available: int | None
    value: F | None
    identity: str


def select(rows, entity, decision, ttl, clock):
    """Proposed strict boundary, not a reproduction of any provider implementation.

    Clocks are integer hours in one declared timezone. Positive TTL endpoints
    are inclusive. Event/created profiles are deliberately weaker comparisons.
    Availability mode refuses unknown availability; conflicting equal-rank
    records are ambiguous, not arbitrarily ordered by their record identity.
    """
    assert ttl > 0 and clock in {'event', 'created', 'available'}
    candidates = [r for r in rows if r.entity == entity and decision-ttl <= r.event <= decision]
    if clock == 'available' and any(r.available is None for r in candidates):
        return {'status': 'unknown_availability', 'value': None}
    if clock == 'created':
        candidates = [r for r in candidates if r.created is not None and r.created <= decision]
    if clock == 'available':
        candidates = [r for r in candidates if r.available <= decision]
    if not candidates:
        return {'status': 'no_eligible_version', 'value': None}
    if any(r.created is None for r in candidates):
        return {'status': 'unknown_revision_order', 'value': None}
    rank = max((r.event, r.created) for r in candidates)
    best = [r for r in candidates if (r.event, r.created) == rank]
    if len({r.value for r in best}) > 1:
        return {'status': 'ambiguous_revision', 'value': None}
    value = best[0].value
    return dict(status='observed_missing' if value is None else 'value',
        value=None if value is None else str(value), source_ids=sorted(r.identity for r in best))


def calculate():
    # The type is unavailable at the decision. The four joint probabilities
    # define a complete finite law for type and potential success under action.
    law = [('good', 1, F(2, 5)), ('good', 0, F(1, 10)),
           ('bad', 1, F(1, 10)), ('bad', 0, F(2, 5))]
    assert sum(p for _, _, p in law) == 1
    q = {'good': F(4, 5), 'bad': F(1, 5)}
    pay, cost = F(100), F(50)
    results, permutation_cases = {}, 0
    for case, delay in [('late_revision', False), ('creation_precedes_availability', True)]:
        net = {clock: F(0) for clock in ['event', 'created', 'available']}
        actions = {clock: F(0) for clock in net}
        selections = {}
        for kind in q:
            # These are alternative worlds for the same observed entity key;
            # neither the key nor any other predecision input reveals type.
            rows = [Row('customer', 6, 7, 7, F(1, 2), 'original'),
                    Row('customer', 6, 11, 11, q[kind], 'correction')]
            if delay:
                rows.append(Row('customer', 9, 9, 12, q[kind], 'delayed_delivery'))
            selections[kind] = {}
            for clock in net:
                result = select(rows, 'customer', 10, 4, clock)
                assert result['status'] == 'value'
                for order in permutations(rows):
                    assert select(order, 'customer', 10, 4, clock) == result
                    permutation_cases += 1
                selections[kind][clock] = result
                take = F(result['value']) > F(1, 2)
                for t, success, probability in law:
                    if t == kind and take:
                        net[clock] += probability * (pay*success-cost)
                        actions[clock] += probability
        expected = {'event': F(15), 'created': F(15) if delay else F(0), 'available': F(0)}
        assert net == expected
        results[case] = dict(net_usd={k: str(v) for k, v in net.items()},
            action_probability={k: str(v) for k, v in actions.items()}, selections=selections)
    assert sum(p*(pay*y-cost) for _, y, p in law) == 0
    base = Row('customer', 6, 7, 7, F(1, 2), 'original')
    checks = {}
    checks['ttl_lower_boundary_included'] = select([base], 'customer', 10, 4, 'available')['status'] == 'value'
    checks['ttl_older_excluded'] = select([replace(base, event=5)], 'customer', 10, 4, 'available')['status'] == 'no_eligible_version'
    checks['equality_included_under_declared_clock_order'] = select([replace(base, event=10, created=10, available=10)], 'customer', 10, 4, 'available')['status'] == 'value'
    checks['future_event_excluded'] = select([replace(base, event=11)], 'customer', 10, 4, 'available')['status'] == 'no_eligible_version'
    checks['all_late_preserves_missing_state'] = select([replace(base, available=12)], 'customer', 10, 4, 'available')['status'] == 'no_eligible_version'
    checks['unknown_availability_refused'] = select([replace(base, available=None)], 'customer', 10, 4, 'available')['status'] == 'unknown_availability'
    checks['null_creation_excluded_by_creation_profile'] = select([replace(base, created=None)], 'customer', 10, 4, 'created')['status'] == 'no_eligible_version'
    checks['unknown_revision_order_refused'] = select([replace(base, created=None)], 'customer', 10, 4, 'available')['status'] == 'unknown_revision_order'
    checks['zero_is_observed'] = select([replace(base, value=F(0))], 'customer', 10, 4, 'available')['value'] == '0'
    checks['null_is_not_zero'] = select([replace(base, value=None)], 'customer', 10, 4, 'available')['status'] == 'observed_missing'
    checks['entities_do_not_borrow'] = select([base], 'different', 10, 4, 'available')['status'] == 'no_eligible_version'
    tie = [base, replace(base, value=F(4, 5), identity='conflict')]
    for order in permutations(tie):
        assert select(order, 'customer', 10, 4, 'available')['status'] == 'ambiguous_revision'
    checks['conflicting_equal_timestamps_refused_in_both_orders'] = True
    assert all(checks.values())
    return dict(kind='project_authored_exact_synthetic_reference', assumptions=dict(
        type_probability={'good': '1/2', 'bad': '1/2'}, success_under_action={k: str(v) for k, v in q.items()},
        payoff_usd='100', action_cost_usd='50', no_action_value='0', decision_hour=10, ttl_hours=4,
        information='At decision all customers have score1/2. Type is revealed only later. Any independent randomization at decision has expected net0.',
        policy='Take action exactly when retrieved score exceeds1/2.'),
        joint_law=[dict(type=t, success=y, probability=str(p)) for t, y, p in law],
        results=results, invariance_cases=permutation_cases, edge_checks=checks,
        execution='Only this authored finite law and selector executed. No Feast/provider/template or downloaded code executed.',
        interpretation='USD15 is the value of an unavailable type-dependent rule, not demonstrated feasible bank value or a measured Feast error.')


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
