#!/usr/bin/env python3
"""Authored deterministic servicing routes; not an implementation of DEF-1."""
from fractions import Fraction
import json


def outcome(backup_available, priority_active, fixed_backup=None):
    assert backup_available in (0, 1) and priority_active in (0, 1)
    assert fixed_backup in (None, 0, 1)
    backup = backup_available * (1 - priority_active) if fixed_backup is None else fixed_backup
    direct = priority_active
    recovery = max(backup, direct)
    return dict(backup_available=backup_available, priority_active=priority_active,
                backup_active=backup, direct=direct, recovery=recovery,
                net_usd=200 * recovery - 40 * priority_active - 10 * backup)


def calculate():
    rows = [outcome(a, c) for a in (0, 1) for c in (0, 1)]
    factual = outcome(1, 1)
    disable_priority = outcome(1, 0)
    disable_both = outcome(1, 0, fixed_backup=0)
    assert [r['recovery'] for r in rows] == [0, 1, 1, 1]
    assert [r['net_usd'] for r in rows] == [0, 160, 190, 160]
    threshold = Fraction(160, 190)
    probes = []
    for p in [Fraction(0), Fraction(1, 2), threshold, Fraction(1)]:
        gain = 160 - 190 * p
        probes.append(dict(backup_probability=str(p), priority_gain_usd=str(gain)))
    assert [r['priority_gain_usd'] for r in probes] == ['160', '65', '0', '-30']
    return dict(kind='exact_authored_structural_reference', natural_rows=rows,
        factual=factual, do_priority_zero=disable_priority, do_priority_and_backup_zero=disable_both,
        priority_recovery_gain_at_available_backup=factual['recovery']-disable_priority['recovery'],
        compound_removal_recovery_loss=factual['recovery']-disable_both['recovery'],
        priority_net_gain_at_available_backup=factual['net_usd']-disable_priority['net_usd'],
        priority_net_gain_formula='160 - 190*p USD per case',
        priority_threshold=str(threshold), probes=probes,
        assumptions=['Deterministic stipulated routes; no causal identification from empirical data is claimed.',
            'A is backup availability known only in the conditional calculation; p is a stipulated predecision probability in the population calculation.',
            'Success value USD200, priority cost USD40 and executed backup cost USD10 are illustrative assumptions.',
            'Fixed B=0 is a distinct compound intervention; no implementation or validation of the papers DEF-1 is inferred.'],
        live_model_or_bank_observations=False)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
