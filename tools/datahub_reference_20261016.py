#!/usr/bin/env python3
"""Exact authored catalog/causal references; no upstream code or service run."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-16/datahub-reuse'


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def calculate():
    # Independent fair offer in world C; hidden borrower state drives both
    # assignment and response in world H. The complete observed laws coincide.
    worlds = {}
    for kind in ['causal_offer', 'hidden_risk']:
        joint = {str((a, y)): F(0) for a, y in product([0, 1], repeat=2)}
        means = []
        for bit, noise in product([0, 1], repeat=2):
            mass = F(1, 2) * (F(1, 4) if noise else F(3, 4))
            action = bit
            outcome = (action if kind == 'causal_offer' else bit) ^ noise
            joint[str((action, outcome))] += mass
        for intervention in [0, 1]:
            mean = F(0)
            for bit, noise in product([0, 1], repeat=2):
                mass = F(1, 2) * (F(1, 4) if noise else F(3, 4))
                mean += mass * ((intervention if kind == 'causal_offer' else bit) ^ noise)
            means.append(mean)
        worlds[kind] = {'observed_joint': joint, 'intervention_means': means,
                        'effect': means[1]-means[0], 'net_incremental_USD': 100*(means[1]-means[0])-30}
    assert worlds['causal_offer']['observed_joint'] == worlds['hidden_risk']['observed_joint']
    assert worlds['causal_offer']['effect'] == F(1, 2) and worlds['hidden_risk']['effect'] == 0
    assert [w['net_incremental_USD'] for w in worlds.values()] == [20, -30]
    clock_rows = [{'baseline': b, 'outcome_day30': y, 'late_feature': y} for b, y in product([0, 1], repeat=2)]
    baseline_accuracy = sum(F(r['baseline'] == r['outcome_day30'], 4) for r in clock_rows)
    late_accuracy = sum(F(r['late_feature'] == r['outcome_day30'], 4) for r in clock_rows)
    assert baseline_accuracy == F(1, 2) and late_accuracy == 1
    clocks = [{'field': 'baseline', 'event_day': -1, 'available_day': -1, 'schema_created_day': -60, 'catalog_observed_day': 40},
              {'field': 'late_feature', 'event_day': 0, 'available_day': 31, 'schema_created_day': -60, 'catalog_observed_day': 40},
              {'field': 'unknown_feature', 'event_day': -1, 'available_day': None, 'schema_created_day': -60, 'catalog_observed_day': 40}]
    eligible = [r['field'] for r in clocks if r['available_day'] is not None and r['available_day'] <= 0]
    event_only = [r['field'] for r in clocks if r['event_day'] <= 0]
    assert eligible == ['baseline'] and len(event_only) == 3
    identities = [
        {'platform': 'warehouse', 'instance': 'east', 'dataset': 'loans', 'environment': 'PROD', 'field_path': 'balance'},
        {'platform': 'warehouse', 'instance': 'east', 'dataset': 'loans', 'environment': 'DEV', 'field_path': 'balance'},
        {'platform': 'warehouse', 'instance': 'west', 'dataset': 'loans', 'environment': 'PROD', 'field_path': 'balance'}]
    full_count = len({tuple(r.values()) for r in identities})
    leaf_count = len({r['field_path'] for r in identities})
    assert full_count == 3 and leaf_count == 1
    # Static source interpretation, not execution of the downloaded method.
    distances = [1, 2, 3, 4]
    literal_three = [d for d in distances if d <= 3]
    buckets = [str(d) if d <= 2 else '3+' for d in distances]
    source_bucket_three = [d for d, b in zip(distances, buckets) if b in ['1', '2', '3+']]
    assert literal_three == [1, 2, 3] and source_bucket_three == [1, 2, 3, 4]
    page_lengths = [500, 1]
    assert sum(page_lengths) == 501
    # Proposed bounded-reader contract: a repeated token prevents a claim of a
    # complete export. An empty page with a continuation token is not completion.
    cursor_sequence = ['cursor-A', 'cursor-A']
    seen = set(); calls = 0; complete = False; disposition = 'partial'
    for token in cursor_sequence:
        calls += 1
        if token in seen:
            disposition = 'repeated_cursor'; break
        seen.add(token)
    assert calls == 2 and disposition == 'repeated_cursor' and not complete
    missing = [
        {'source_case': 'aspect HTTP 404', 'meaning': 'requested aspect absent', 'causal_context': 'unknown'},
        {'source_case': 'HTTP 403 or 500', 'meaning': 'read failed', 'causal_context': 'unavailable'},
        {'source_case': 'status removed=false with lifecycleStage set', 'meaning': 'needs stage visibility semantics', 'causal_context': 'unknown'},
        {'source_case': 'lineage confidenceScore=1.0', 'meaning': 'lineage field/default', 'causal_context': 'no causal probability supplied'},
        {'source_case': 'ownership lastModified.time=0', 'meaning': 'missing audit time', 'causal_context': 'unknown'}]
    return encode({'status': 'exact_authored_reference', 'worlds': worlds,
        'clock': {'rows': clock_rows, 'field_clocks': clocks, 'decision_day': 0,
                  'baseline_accuracy': baseline_accuracy, 'late_accuracy': late_accuracy,
                  'eligible_by_availability': eligible, 'admitted_by_event_only': event_only},
        'identity': {'records': identities, 'full_identity_count': full_count, 'leaf_only_count': leaf_count,
                     'scope': 'Abstract identity tuples, not executed DataHub URN construction'},
        'traversal': {'distances': distances, 'literal_three_hops': literal_three,
                      'source_3plus_bucket_selection': source_bucket_three, 'page_lengths': page_lengths,
                      'accumulated_count': sum(page_lengths), 'repeated_cursor_calls': calls,
                      'proposed_disposition': disposition, 'complete': complete,
                      'scope': 'Static source semantics plus authored bounded-export oracle; no server or SDK execution'},
        'missing_context_contract': missing,
        'limits': ['Generated worlds and stipulated dollars; no bank result, learned accuracy or ROI.',
                   'Metadata cannot supply missing causal assignment or past feature-availability truth.',
                   'No DataHub service, SDK, cloud product, connector or MCP server was run.']})


if __name__ == '__main__':
    with (BASE / 'exact-results.json').open('x') as stream:
        json.dump(calculate(), stream, indent=2); stream.write('\n')
    print(json.dumps({'reference_families': 4, 'missing_context_cases': 5, 'status': 'pass', 'upstream_execution': False}))
