#!/usr/bin/env python3
"""Bind the scoped author disposition and exact supplement reading PDFs."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'docs/reviews/weak-audit-author-review.json'
VISUAL = 'docs/reviews/weak-audit-visual-inspection-2026-10-11.json'


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    with (ROOT / name).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    study = read('docs/studies/weak-audit-projection-results.json')
    by_name = {r['design']['name']: r['summary']['methods'] for r in study['results']}
    if (study['requests'] != 3000 or
            by_name['near_rank_1200']['weak_audit_projection']['whole_line'] != 546 or
            by_name['false_exogeneity_1200']['weak_audit_projection']['covered'] != 591):
        raise ValueError('Author conclusions differ from final study')
    visual = read(VISUAL)
    sources = read('docs/reviews/weak-audit-source-review.json')
    inputs = {
        'AGENTS.md', 'docs/causal_foundations.pdf',
        'docs/program/reconstruction-delivery-manifest.json',
        'docs/program/state.json',
        'docs/program/weak-audit-projection-plan-2026-10-11.md',
        'docs/program/weak-audit-delivery-2026-10-11.md',
        'docs/program/continuation-status-2026-10-11.md',
        'docs/reviews/weak-audit-projection-plan-review-2026-10-11.md',
        'docs/reviews/weak-audit-projection-author-review-2026-10-11.md',
        'docs/reviews/remaining-gaps-weak-audit-2026-10-11.md',
        'docs/reviews/weak-audit-execution-notes-2026-10-11.md',
        'docs/reviews/weak-audit-projection-checks.json',
        'docs/reviews/weak-audit-verification.json',
        'docs/reviews/weak-audit-source-review.json',
        'docs/reviews/weak-audit-table-generation.json', VISUAL,
        'docs/reviews/weak-audit-visual-inspection-2026-10-11.md',
        'docs/studies/weak-audit-projection-spec.json',
        'docs/studies/weak-audit-projection-final.jsonl',
        'docs/studies/weak-audit-projection-results.json',
        'docs/supplements/weak_audit_projection_2026-10-11.tex',
        'docs/supplements/weak_audit_projection_2026-10-11.log',
        'docs/supplements/weak-audit-table.tex',
        'docs/literature/sources.json',
        'src/causalbank/weak_audit_projection.py',
        'tools/weak_audit_checks.py', 'tools/weak_audit_study.py',
        'tools/weak_audit_tables.py', 'tools/weak_audit_source_trace.py',
        'tools/weak_audit_verify.py', 'tools/weak_audit_delivery.py',
        'tools/weak_audit_author_receipt.py',
    }
    inputs.update(visual['images_sha256'])
    inputs.update(row['path'] for row in (visual['supplement'], visual['reader']))
    inputs.update(row['local_path'] for row in sources['cited_primary_works'])
    if TARGET in inputs or 'docs/program/weak-audit-delivery-manifest.json' in inputs:
        raise ValueError('Circular author receipt')
    missing = [name for name in inputs if not (ROOT / name).is_file()]
    if missing:
        raise ValueError('Missing author evidence: ' + repr(missing))
    record = dict(status='author_reviewed_with_stated_limits', date='2026-10-11',
                  review='docs/reviews/weak-audit-projection-author-review-2026-10-11.md',
                  blocking_findings=[],
                  final_documents=[visual['supplement'], visual['reader']],
                  scientific_disposition='Pointwise asymptotic response bands and exact audit inversion imply rank-robust set containment under stated laws, not finite-sample or uniform calibration.',
                  capability_disposition='Selected synthetic coverage is high but sets are wider; 546/600 near-rank outputs are whole-line, so useful precision remains open.',
                  remaining='Sharpen or change information before fresh registered draws; obtain independent, bank, platform and economic evidence under the preserved external protocol.',
                  scope='Bounded author-reviewed research supplement; frozen V10 unchanged. Not general calibration, independent acceptance or a bank product.',
                  input_sha256={name: digest(name) for name in sorted(inputs)})
    (ROOT / TARGET).write_text(json.dumps(record, indent=2) + '\n')
    print(f'Author receipt bound: {len(inputs)} inputs, two exact reading PDFs.')


if __name__ == '__main__':
    main()
