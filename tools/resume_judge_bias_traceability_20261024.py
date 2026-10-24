#!/usr/bin/env python3
"""Resume only failed traceability after preserving the successful PDF build."""
import json
from copy import deepcopy
from pathlib import Path
import audit_reader_traceability_v3_20261024 as trace
import build_judge_bias_reader_20261024 as build
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
read = lambda p: json.loads(p.read_text())


def main():
    assert not (BASE / 'traceability-review.json').exists()
    for name in ['prepared-inputs.json', 'reader/build-report.json',
                 'reader/source-audit.json', 'reader/text-layout-review.json']:
        verify_bindings(read(BASE / name))
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.DEVELOPMENT.read_bytes() == (build.SOURCE / 'development.tex').read_bytes()
    assert build.exact.calculate() == read(BASE / 'exact-results.json')
    source = read(build.SOURCE / 'source-audit.json')['sources'][0]
    trace.verify_refs(source)
    rejected = []
    mutations = [('wrong_digest', {'sha256': '0' * 64}),
                 ('wrong_basename', {'first_author': 'Different'}),
                 ('wrong_version', {'source_identity': 'https://arxiv.org/abs/2604.18164v1'}),
                 ('missing_version', {'version_date': 'Unversioned'})]
    for label, mutation in mutations:
        changed = deepcopy(source); changed.update(mutation)
        try:
            trace.verify_refs(changed)
        except (AssertionError, ValueError):
            rejected.append(label)
        else:
            raise AssertionError('Invalid original admitted: ' + label)
    report = read(OUT / 'build-report.json')
    bounds = read(OUT / 'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    index = trace.audit(build.DRIVER, OUT / 'source-audit.json')
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == 257 and index['audit_records'] == 1180
    write(BASE / 'traceability-review.json', index)
    write(BASE / 'traceability-repair.json', dict(
        status='pass', failure='Legacy validator required every paper to be immediately under docs/papers.',
        repair='Exact version-qualified subdirectory accepted without moving or replacing either original; all bytes and names verified.',
        pdf_rebuilt=False, originals_unchanged=True, invalid_cases_rejected=rejected,
        evidence=[ref(build.SOURCE / 'reader-build.log', 'Preserved failed traceability attempt'),
                  ref(OUT / 'build-report.json', 'Already compiled PDF'),
                  ref(BASE / 'traceability-review.json', 'Successful full source audit'),
                  ref(Path(trace.__file__), 'Version-aware validator'), ref(Path(__file__), 'Resume and negative checks')],
        visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(status='pass', pages=report['pages'], records=1180, papers=257,
                          invalid_cases_rejected=rejected, rebuilt=False)))


if __name__ == '__main__':
    main()
