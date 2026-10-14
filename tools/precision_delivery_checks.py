#!/usr/bin/env python3
"""Challenge V10 delivery gates in memory; never modify delivered evidence."""
from copy import deepcopy
from functools import lru_cache
import json
from unittest.mock import patch

import precision_delivery as gate


def main():
    # Files are read-only throughout this run. Cache their real hashes once;
    # injected record changes exercise semantic checks, not disk mutation.
    original_read = gate.read
    real_digest = lru_cache(maxsize=None)(gate.digest)
    rejected = []

    def reject(name, path, change, expected):
        altered = deepcopy(original_read(path))
        change(altered)

        def read(candidate):
            return altered if candidate == path else original_read(candidate)

        with patch.object(gate, 'read', side_effect=read):
            try:
                gate.gates()
            except ValueError as error:
                if expected not in str(error):
                    raise AssertionError(f'{name}: unexpected rejection: {error}') from error
                rejected.append(name)
            else:
                raise AssertionError(f'{name}: invalid delivery was accepted')

    with patch.object(gate, 'digest', side_effect=real_digest):
        gate.gates()
        reject('incomplete_current_phase', 'docs/program/state.json',
               lambda row: row['phases'][-1].update(status='in_progress'),
               'Incorrect phase status: J05')
        reject('stale_dashboard', 'docs/program/state.json',
               lambda row: row.update(next_action='Unrecorded action'), 'Stale Mission Control')
        reject('historical_source_review_as_current', 'docs/literature/precision-source-review.json',
               lambda row: row.update(revision='9.0'), 'Stale current source review')
        old_claim_hash = original_read('docs/literature/calibration-source-review.json')['input_sha256'][
            'docs/literature/reconstruction-claims.json']
        reject('source_review_bound_to_old_claims', 'docs/literature/precision-source-review.json',
               lambda row: row['input_sha256'].update(
                   {'docs/literature/reconstruction-claims.json': old_claim_hash}),
               'precision-source-review.json: changed docs/literature/reconstruction-claims.json')
        reject('stale_author_review_pointer', gate.REVIEW,
               lambda row: row.update(review='docs/reviews/calibration-author-review.md'),
               'Stale author review document')
        reject('missing_remaining_gap_evidence', gate.REVIEW,
               lambda row: row['gap_dispositions']['D10'].pop('remaining'),
               'Missing scoped judgment and remaining evidence')
        reject('different_reviewed_pdf', gate.REVIEW,
               lambda row: row['final_documents'][0].update(sha256='0' * 64),
               'PDF identity differs across gates')
        reject('uninspected_contact_sheet', gate.VISUAL,
               lambda row: row['documents'][0]['contact_sheets_viewed'].pop(),
               'Uninspected or duplicate contact sheet')
        reject('changed_image_without_new_view', gate.VISUAL,
               lambda row: row['images_viewed_after_repair'].pop(),
               'Changed image lacks a new view')

        verified = original_read('docs/reviews/precision-verification.json')['input_sha256']
        inherited = next(path for claim in original_read('docs/literature/reconstruction-claims.json')
                         if not claim['id'].startswith('J-R')
                         for path in claim.get('artifacts', []) if path in verified)
        with patch.object(gate, 'digest', side_effect=lambda path:
                          '0' * 64 if path == inherited else real_digest(path)):
            try:
                gate.gates()
            except ValueError as error:
                if f'changed {inherited}' not in str(error):
                    raise AssertionError(f'Unexpected inherited-artifact rejection: {error}') from error
                rejected.append('changed_inherited_claim_artifact')
            else:
                raise AssertionError('Changed inherited claim artifact was accepted')

    print(json.dumps(dict(status='pass', unchanged_delivery='pass',
                          rejected_cases=rejected,
                          scope='Read-only author gate challenges; no scientific evidence was modified.'),
                     indent=2))


if __name__ == '__main__':
    main()
