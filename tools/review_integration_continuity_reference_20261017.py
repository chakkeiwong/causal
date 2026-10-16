#!/usr/bin/env python3
"""Independent arithmetic/model checks for the integration continuity examples."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

import integration_continuity_reference_20261017 as candidate


def review():
    result = candidate.calculate()
    ordered = ('a', 'b', 'c')
    # Generate a Cartesian space including repetitions, then remove repetitions;
    # the reference uses permutations. Compare every row, not just its count.
    prefixes = [x for k in range(4) for x in product(ordered, repeat=k)
                if len(set(x)) == len(x)]
    valid = [(), ('a',), ('a', 'b'), ('a', 'b', 'c')]
    assert len(prefixes) == 16 and len(valid) == 4
    assert result['prefix_publication_cancellation']['valid_prefixes'] == len(valid)
    assert result['prefix_publication_cancellation']['rejected_nonprefixes'] == len(prefixes)-len(valid)
    rows = result['prefix_publication_cancellation']['prefix_rows']
    assert {tuple(r['completed']): r['is_prefix'] for r in rows} == {
        x: x in valid for x in prefixes}
    schedules = result['prefix_publication_cancellation']['lock_respecting_cancel_schedules']
    assert [r['cancel_after_events'] for r in schedules] == [0, 1, 2, 3, 5]
    assert [r['terminal'] for r in schedules] == ['cancelled']*4 + ['completed']
    assert [r['published_artifact'] for r in schedules] == [False]*4 + [True]
    crash = result['prefix_publication_cancellation']['crash_between_publication_and_acknowledgement']
    assert crash['terminal'] == 'cancelled' and crash['published_artifact']
    for row in result['deadline']['rows']:
        created, budget = 1000, 60
        assert row['formula_remaining_seconds'] == budget-row['real_elapsed_seconds']-row['wall_adjustment_seconds']
        assert row['elapsed_budget_remaining_seconds'] == max(0, budget-row['real_elapsed_seconds'])
    # Aggregate integer cents first; convert to USD only at the final boundary.
    cents = [1000*x-1000*300 for x in (-200, 600)]
    assert [Fraction(x,100) for x in cents] == result['scientific_meaning']['net_value_USD']
    assert result['scientific_meaning']['unit_conversion_with_cost_preserved_USD'] == [-5000,3000]
    protocol = result['protocol_negotiation']['rows']
    assert len(protocol) == 9
    assert [r['proposed_action'] for r in protocol] == ['modern', 'incompatible',
        'retry_supported_modern', 'incompatible',
        'remain_modern_handle_error_without_unconditional_retry',
        'legacy_initialize', 'legacy_initialize', 'legacy_initialize', 'incompatible']
    adoption = result['adoption']['gate_rows']
    assert len(adoption) == 2**6 and len({tuple(x['gates'].values()) for x in adoption}) == 64
    assert all(x['eligible_for_scoped_adoption'] == (list(x['gates'].values()).count(False) == 0)
               for x in adoption)
    assert sum(all(x['gates'].values()) for x in adoption) == 1
    assert all(x['exact_release_match'] is False for x in
               result['adoption']['exact_release_staleness_cases'])
    return {'status': 'pass', 'reviewer': 'Separate author calculation; not independent institutional review',
        'checks': ['Cartesian enumeration and literal expected prefixes; five lock placements and separate crash window',
            'deadline formula verified as budget minus elapsed time minus clock adjustment',
            'net monetary interval verified by aggregating integer cents before conversion',
            'modern/legacy decision categories and no fallback after recognized modern errors',
            'all 64 adoption truth-table rows and six exact-release changes'],
        'scope': 'Exact authored examples only; no runtime, MCP peer, bank data, signer or platform exercised.',
        'candidate_sha256': __import__('hashlib').sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
        'results': result}


if __name__ == '__main__':
    print(json.dumps(review(), indent=2, allow_nan=False))
