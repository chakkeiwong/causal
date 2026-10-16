#!/usr/bin/env python3
"""Preserve the recovered S5 candidate's conservative depth failure."""
import json
from pathlib import Path
import re

import build_s5_reader_v2_20261017 as build
import s5_examples_20261017 as exact
import s5_covariance_20261017 as joint
from review_s3_20261017 import preserve
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.WORK, build.OUT
PAGES = [
    (.5, 'New discrete payment-clock identity; title and repeated banking/availability framing excluded.'),
    (1, 'Sharp discrete-tail proof, continuation witnesses and monetary contrast endpoints.'),
    (1, 'Survivor-composition derivation, exact hazard reversal and common-population monetary ranking.'),
    (.5, 'Ordered-event factorization and boundary case; inherited competing-risk accounting and generic diagnostics excluded.'),
    (.75, 'Decision-reversing adapter example and inspected aggregation semantics; repeated event objective and general wrapper advice discounted.'),
    (1, 'Complete observed-law natural-versus-redrawn counterexample, innovation conditions and target-specific remedies.'),
    (1, 'Noninjective pushforward branches, moments, singular cap, sharp endpoint-world construction and money.'),
    (1, 'Endpoint regularity distinction and fixed-map derivative proof; generic assignment-dependent framing discounted.'),
    (.75, 'Target-specific assignment perturbation and exact influence components; generic S4 covariance argument excluded.'),
    (.25, 'Quantitative cumulative-versus-incremental floor example and specific corrected API semantics; inherited vendor descriptions excluded.'),
    (.5, 'New common-target distinctions and joint-event-vector setup; version catalog, generic result fields and prior SDR material excluded.'),
    (1, 'Whole-history indicator covariance derivation, monetary variance and explicit distinction from observational estimation.'),
    (.5, 'Conditional simulation decomposition and paired Bernoulli coupling; previously credited coverage denominators and generic cluster/band advice excluded.'),
    (1, 'First-split recursion, sharper reward envelope and jointly attaining transition-law witness.'),
    (0, 'Generic prototype, adoption, CLI/MCP and later bank-evidence material is already credited elsewhere.'),
    (0, 'Conclusion receives no additional substantive credit.')
]


def main():
    read = lambda p: json.loads(p.read_text())
    report, audit = read(OUT/'build-report.json'), read(OUT/'source-audit.json')
    index = read(build.BASE/'traceability-review.json')
    for p in [OUT/'build-report.json', OUT/'source-audit.json',
              build.BASE/'prepared-inputs.json', build.BASE/'draft-author-review.json',
              build.BASE/'traceability-review.json', BASE/'primary-review.json',
              BASE/'revision-v2/mathematics-review.json']:
        verify_bindings(read(p))
    assert report['pages'] == 934 and report['cited_records'] == 711
    assert index['status'] == 'pass' and index['scholarly_pdfs'] == 187
    assert read(OUT/'text-layout-review.json')['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    retained = preserve(audit, index, build.PRIOR.parent.parent, 707,
                        [str(build.OLD.relative_to(ROOT))])
    for module, name in [(exact, 'exact-results.json'), (joint, 'covariance-results.json')]:
        saved = read(BASE/name)
        assert module.calculate() == saved and module.separate(saved)['status'] == 'pass'
    pages = (OUT/'reader.txt').read_text().split(chr(12))
    equations = dict(re.findall(r'\\newlabel\{(exec17:s5[^}]+)\}\{\{(22\.[0-9]+)\}\{',
                               (OUT/(build.NAME+'.aux')).read_text()))
    assert set('22.'+str(n) for n in range(1,29)) <= set(equations.values())
    text = ''.join(pages[235:251])
    assert all('('+str('22.'+str(n))+')' in text for n in range(1,29))
    assert '??' not in text
    rows = [dict(printed_page=215+i, pdf_page=236+i, credit=c, rationale=r)
            for i,(c,r) in enumerate(PAGES)]
    for row in rows:
        assert re.search(r'\b'+str(row['printed_page'])+r'\b', pages[row['pdf_page']-1])
    credit = sum(r['credit'] for r in rows)
    assert credit == 10.75 and credit < 14
    evidence = [ref(p,a) for p,a in [
        (OUT/'build-report.json', 'Recovered934-page candidate, not published'),
        (build.BASE/'traceability-review.json', '711 source records;187 genuine scholarly PDFs'),
        (OUT/'reader.txt', 'All printed215-230/physical236-251 and next-chapter boundary inspected'),
        (OUT/'text-layout-review.json', 'All-page text bounds; not visual acceptance'),
        (build.CHAPTER, 'Preserved candidate chapter'),
        (BASE/'plan.md', '14/17/20 exclusive allocation and overlap exclusions'),
        (BASE/'exact-results.json', 'Eight original exact authored families'),
        (BASE/'covariance-results.json', 'Joint history covariance and sharper coupling'),
        (BASE/'primary-review.json', 'Inspected primary originals and version limits'),
        (Path(__file__), 'Conservative per-page source/text assessment')]]
    write(BASE/'depth-review-initial.json',dict(status='requires_revision',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        reviewed_reader=report['pdf'], allocation=dict(min=14,target=17,max=20),
        substantive_page_credit=credit, per_page=rows, allocation_minimum_met=False,
        planning_target_met=False, equation_numbers=equations,
        canonical_records_preserved=707, canonical_compiled_sources_preserved=retained,
        findings=['Recovered build, sources, exact calculations, equations and extracted layout pass.',
                  'Only10.75 exclusive page equivalents survive overlap exclusions; minimum14 is not met.',
                  'No draft/review operation is completed and no candidate is promoted by this assessment.'],
        measurement='Conservative author-assessed page equivalents under inherited typography; no visual acceptance.',
        evidence=evidence, visual_acceptance=False,
        next_action='Develop event-specific occupied-history perturbation and validation analysis in a preserving successor.'))
    print(json.dumps(dict(depth='requires_revision',credit=credit,minimum=14,
                          reader_pages=934,canonical_unchanged=True)))


if __name__ == '__main__':
    main()
