#!/usr/bin/env python3
"""Preserve the traceability schema failure and prepare a corrected successor."""
import json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / 'docs/program/execution/2026-10-23/semantics-reader-v2'
BASE = V2.with_name('semantics-reader-v3')


def main():
    assert not BASE.exists()
    report = json.loads((V2 / 'reader/build-report.json').read_text())
    assert report['pages'] == 1245 and report['cited_records'] == 939
    detail = dict(status='failed_traceability_schema',
        failure='Established scholarly-PDF verifier requires filename_title; two authentic papers supplied local_path, first_author, year and hash but not this derived field.',
        evidence=[ref(V2 / 'source-audit.json', 'Original authentic paper identities without filename_title'),
            ref(V2 / 'prepared-inputs.json', 'Bound v2 inputs'),
            ref(V2 / 'reader/build-report.json', '1245-page compile and all-page text-layout pass'),
            ref(V2 / 'reader/reader.txt', 'Extracted rendered text'),
            ref(Path(__file__), 'Separate conserving schema repair')],
        repair='Derive filename_title from the already authenticated local PDF basename and first-author/year suffix; verify the prescribed filename exactly.',
        scientific_or_content_change=False, canonical_reader_changed=False, final_acceptance=False)
    write(V2 / 'traceability-failure.json', detail)
    BASE.mkdir()
    names = ['integration-plan.md', 'iv-development.tex', 'longitudinal-development.tex',
        'context-development.tex', 'conflict-development.tex', 'sponsor-addition.md']
    for name in names:
        (BASE / name).write_bytes((V2 / name).read_bytes())
    plan = BASE / 'integration-plan.md'
    plan.write_text(plan.read_text() + '\nThe v2 reader compiled and passed page-boundary checks, then its inherited\ntraceability verifier rejected two paper records for omitting a derived\nfilename_title field. v2 bytes and failure are preserved. v3 derives and verifies\nthat field from each already authenticated PDF filename.\n')
    old = ROOT / 'tools/build_semantics_reader_v2_20261023.py'
    new = ROOT / 'tools/build_semantics_reader_v3_20261023.py'
    code = old.read_text().replace('semantics-reader-v2', 'semantics-reader-v3').replace(
        'causal_proposal_semantics_reviewed_v2_2026-10-23', 'causal_proposal_semantics_reviewed_v3_2026-10-23')
    code = code.replace("records += read(folder / 'source-audit.json')['sources']", """records += read(folder / 'source-audit.json')['sources']
    for source in records:
        if source['kind'] == 'paper':
            suffix = f\" {source['first_author']}({source['year']}).pdf\"
            filename = Path(source['local_path']).name
            assert filename.endswith(suffix)
            source['filename_title'] = filename[:-len(suffix)]
            assert source['filename_title'] and Path('docs/papers', filename).is_file()""")
    # Keep the generator syntactically simple: inject the failure path after list construction.
    code = code.replace("extra_paths += [ROOT / 'tools/complete_census_context_conflict_20261023.py']", "extra_paths = [BASE / 'traceability-failure.json'] + extra_paths\n    extra_paths += [ROOT / 'tools/complete_census_context_conflict_20261023.py']")
    code = code.replace("semantic_change=False, visual_acceptance=False))", "semantic_change=False, traceability_failure=ref(V2 / 'traceability-failure.json', 'Preserved v2 schema failure'), visual_acceptance=False))")
    new.write_text(code)
    tool = ROOT / 'tools/repair_semantics_layout_20261023.py'
    write(BASE / 'source-schema-correction.json', dict(status='reviewed_schema_correction',
        evidence=[ref(V2 / 'traceability-failure.json', 'Preserved traceability failure'),
            ref(V2 / 'source-audit.json', 'Original source records'), ref(old, 'Failed v2 builder'),
            ref(new, 'v3 exact-schema successor'), ref(tool, 'Preserved preceding line-break repair'),
            ref(Path(__file__), 'Exact record-schema correction')],
        affected_fields=['filename_title for the two authenticated new scholarly PDFs'],
        derived_only=True, scientific_claims_changed=False, visual_acceptance=False))
    print(json.dumps(dict(successor=str(new.relative_to(ROOT)), correction='derive and verify filename_title')))


if __name__ == '__main__':
    main()
