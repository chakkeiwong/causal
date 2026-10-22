#!/usr/bin/env python3
"""Preserve the superseded first refresh and verify its recovered generator."""
import hashlib
import json
from pathlib import Path

from publish_latent_r_review_v2_20261013 import ROOT, ref, write, verify_bindings


def main():
    base = ROOT / 'docs/program/execution/2026-10-23/refresh-preservation-v1'
    assert not base.exists(), 'Preserve completed correction records.'
    first = ROOT / 'docs/program/execution/2026-10-23/program-refresh-policy-v1'
    second = ROOT / 'docs/program/execution/2026-10-23/program-refresh-policy-v2'
    generator = ROOT / 'tools/refresh_policy_program_20261023.py'
    replacement = """        # Earlier source audits corrected the generic graph action. Carry that
        # exact action forward unless a newer durable checkpoint supersedes it.
        if not progress and key in {
                'SW.CELL.iv_rd_design.R',
                'SW.CELL.observations_data.commercial',
                'SW.COMM.observations_data'}:
            item['action'] = old['action']
"""
    original = """        if old.get('corrected_source_followup') and not progress:
            item['action'] = old['action']
"""
    assert generator.read_text().count(replacement) == 1
    recovered = generator.read_text().replace(replacement, original).encode()
    review = json.loads((first / 'program-review.json').read_text())
    old_binding = next(x for x in review['evidence']
                       if x['path'] == str(generator.relative_to(ROOT)))
    assert hashlib.sha256(recovered).hexdigest() == old_binding['sha256']
    base.mkdir(parents=True)
    (base / 'refresh-generator-attempt-1.py').write_bytes(recovered)
    verify_bindings(json.loads((second / 'program-review.json').read_text()))
    write(base / 'correction-review.json', dict(
        status='preserved_failure_with_verified_successor',
        failures=[
            'The first refresh regressed three reviewed source follow-up actions to generic graph actions.',
            'Its original tool path was edited after the first review bound its SHA-256; that binding is stale.'],
        affected_operations=['SW.CELL.iv_rd_design.R',
                             'SW.CELL.observations_data.commercial',
                             'SW.COMM.observations_data'],
        preserved_attempt=ref(first / 'program-review.json',
                              'Unchanged superseded review; stale tool binding remains recorded'),
        recovered_original=ref(base / 'refresh-generator-attempt-1.py',
                               'Recovered bytes exactly match the original bound SHA-256'),
        verified_successor=ref(second / 'program-review.json',
                               'Successor restores all three actions and binds the current generator'),
        original_tool_path=old_binding['path'],
        original_tool_sha256=old_binding['sha256'],
        interpretation='The first refresh is superseded, not a second valid current review. No historical record was rewritten.',
        preventive_action='Use a new immutable generator and output directory for subsequent refreshes.'))
    print(json.dumps(dict(status='preserved_failure_with_verified_successor',
                          original_sha256=old_binding['sha256'])))


if __name__ == '__main__':
    main()
