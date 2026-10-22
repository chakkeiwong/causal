#!/usr/bin/env python3
"""Exact authored finite-table replay example; no vendor code or service execution."""
from fractions import Fraction as F
import hashlib
import json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def number(value):
    return dict(exact=str(value), decimal=float(value))


def calculate():
    # Effects are stipulated potential-outcome contrasts, not estimated bank effects.
    rows = [('A1', 'A', F(6)), ('A2', 'A', F(6)),
            ('A3', 'A', F(6)), ('B1', 'B', F(-2))]
    cost = F(1)
    baseline = sum(r[2] for r in rows) / len(rows)
    interrupted = rows[:2]
    append_replay = interrupted + rows
    duplicated = sum(r[2] for r in append_replay) / len(append_replay)
    keyed_replay = {r[0]: r for r in interrupted}
    keyed_replay.update({r[0]: r for r in rows})
    recovered = sum(r[2] for r in keyed_replay.values()) / len(keyed_replay)
    alternative = F(1, 4) * F(6) + F(3, 4) * F(-2)
    vintage_two = [('A1', 'A', F(6)), ('A2', 'A', F(6)),
                   ('A3', 'A', F(6)), ('B1', 'B', F(-10))]
    vintage_effect = sum(r[2] for r in vintage_two) / len(vintage_two)
    # The declared target, data, code/environment and all semantics travel together.
    manifest = dict(data=digest([(a, b, str(c)) for a, b, c in rows]),
        target=dict(population='four stipulated units', weights=dict(A='3/4', B='1/4'),
                    contrast='Y(1)-Y(0)', information_clock='fixed-vintage-1'),
        method='finite-known-law-standardization-v1',
        uncertainty='exact finite truth; no confidence-interval claim',
        environment='declared-reference-environment-v1',
        output_schema='effect-net-status-v1', tolerance='exact rational equality',
        randomization='none')
    changed = dict(manifest, data=digest([(a, b, str(c)) for a, b, c in vintage_two]))
    changed_target = dict(manifest, target=dict(manifest['target'], weights=dict(A='1/4', B='3/4')))
    changed_environment = dict(manifest, environment='declared-reference-environment-v2')
    checks = dict(baseline_equals_four=baseline == 4,
        append_bias_equals_two_thirds=duplicated - baseline == F(2, 3),
        keyed_replay_equals_baseline=recovered == baseline,
        changed_target_reverses_net_sign=baseline - cost > 0 > alternative - cost,
        vintage_changes_answer=vintage_effect != baseline,
        data_change_rejected=digest(manifest) != digest(changed),
        target_change_rejected=digest(manifest) != digest(changed_target),
        environment_change_rejected=digest(manifest) != digest(changed_environment))
    assert all(checks.values())
    return dict(evidence_kind='authored exact finite-table example',
        vendor_execution=False, bank_data=False,
        stipulated_rows=[dict(id=a, group=b, effect=str(c)) for a, b, c in rows],
        manifest=manifest, manifest_sha256=digest(manifest),
        baseline_effect=number(baseline), baseline_net=number(baseline-cost),
        append_replay_effect=number(duplicated), append_replay_net=number(duplicated-cost),
        append_replay_bias=number(duplicated-baseline),
        recovered_effect=number(recovered), recovered_net=number(recovered-cost),
        alternate_target_effect=number(alternative), alternate_target_net=number(alternative-cost),
        changed_vintage_effect=number(vintage_effect), changed_vintage_net=number(vintage_effect-cost),
        write_attempts=6, append_rows=6, keyed_unique_rows=4,
        qualifications=['An identifier is idempotent only with a fixed semantic manifest and atomic/conflict-checked commit.',
            'Equal hashes bind declarations and bytes; they do not establish causal assumptions or truthful provenance.',
            'The check is exact rational arithmetic, not a native vendor test or a statistical calibration experiment.',
            'No vendor price, measured runtime, reliability or institutional acceptance is inferred.'],
        checks=checks)


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
