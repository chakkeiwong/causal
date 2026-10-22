#!/usr/bin/env python3
"""Preserve a stale-directory preparation failure and create a clean successor."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v3'
BASE = V3.with_name('semantics-reader-v4')


def main():
    assert not BASE.exists()
    driver = ROOT / 'docs/causal_proposal_semantics_reviewed_v3_2026-10-23.tex'
    assert driver.is_file() and not (V3 / 'reader').exists()
    write(V3 / 'prepare-failure.json', dict(status='failed_prepare_recovery',
        reason='v3 prepare emitted its driver before detecting an existing generated driver path; no v3 PDF or reader output was produced.',
        evidence=[ref(driver, 'Emitted v3 driver before stale-directory assertion'),
            ref(V3 / 'source-audit.json', 'Prepared v3 source records'), ref(Path(__file__), 'Clean successor repair')],
        repair='Create a new immutable v4 output directory and driver; do not overwrite v3 emitted bytes.',
        scientific_or_content_change=False, final_acceptance=False))
    BASE.mkdir()
    carry = ['integration-plan.md', 'iv-development.tex', 'longitudinal-development.tex',
        'context-development.tex', 'conflict-development.tex', 'sponsor-addition.md',
        'layout-correction.json', 'source-schema-correction.json', 'traceability-failure.json',
        'failure-carryforward.json', 'layout-carryforward.json', 'prepare-failure.json']
    for name in carry:
        source = V3 / name
        assert source.is_file(), name
        (BASE / name).write_bytes(source.read_bytes())
    old = ROOT / 'tools/build_semantics_reader_v3_20261023.py'
    new = ROOT / 'tools/build_semantics_reader_v4_20261023.py'
    code = old.read_text().replace('semantics-reader-v3', 'semantics-reader-v4').replace(
        'causal_proposal_semantics_reviewed_v3_2026-10-23', 'causal_proposal_semantics_reviewed_v4_2026-10-23')
    code = code.replace("paths = [BASE / 'layout-correction.json', OLD, PRIOR, Path(__file__),", "paths = [BASE / 'prepare-failure.json', BASE / 'source-schema-correction.json', BASE / 'prepare-correction.json', OLD, PRIOR, Path(__file__),")
    new.write_text(code)
    write(BASE / 'prepare-correction.json', dict(status='clean_successor_preparation',
        evidence=[ref(V3 / 'prepare-failure.json', 'Preserved v3 preparation failure'), ref(old, 'v3 generator'),
            ref(new, 'v4 clean successor'), ref(Path(__file__), 'Exact clean-output repair')],
        changed_output_directory=True, scientific_claims_changed=False, overwrite=False, visual_acceptance=False))
    print(json.dumps(dict(successor=str(new.relative_to(ROOT)), correction='clean v4 output directory')))


if __name__ == '__main__':
    main()
