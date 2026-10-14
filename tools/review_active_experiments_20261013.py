#!/usr/bin/env python3
"""Record the author review of the developed active-experiment chapter."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/active-experiments'
ref = shared.ref


def main():
    audit = json.loads((BASE / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    exact = json.loads((BASE / 'exact-review.json').read_text())
    assert exact['status'] == 'pass'
    shared.verify_refs(exact)
    prior_path = ROOT / 'docs/program/execution/2026-10-13/commercial-identification/reader/source-audit.json'
    prior = json.loads(prior_path.read_text())
    specifications = [
        ('v12_la_2305_16183', '2305.16183.txt', [(602, 640)],
         'Passive strategy learning still permits evaluation-time interventions; finite graphs and constrained spaces restrict transfer.'),
        ('v12_la_2506_16234', '2506.16234.txt', [(796, 822), (1174, 1195)],
         'Fixed query-budget comparison concerns graph learning; calibration, uncertainty, interventions and sequential theory remain research questions.'),
        ('v12_la_2608_09696', '2608.09696.txt', [(100, 126), (250, 285), (306, 325), (448, 466), (4098, 4172)],
         'Report sample-efficiency and matched-evaluable denominators, candidate-pool limits, and the source-location adverse/null design findings.')]
    checks = []
    for key, filename, ranges, finding in specifications:
        s = next(x for x in prior['sources'] if x['integrated_citation_key'] == key)
        text = ROOT / 'docs/program/repair-v12/work/LA01/extracted' / filename
        contents = text.read_text()
        lines = contents.split('\n')
        selected = []
        for first, last in ranges:
            assert last <= len(lines)
            selected.append({'lines': [first, last],
                'first_physical_pdf_page': '\n'.join(lines[:first-1]).count('\f')+1,
                'excerpt': '\n'.join(lines[first-1:last])})
        checks.append({'citation_key': key, 'preserved_record': s,
            'extracted_text': ref(text, 'Selected primary technical passages re-inspected'),
            'anchors': selected, 'finding': finding})
    core.write(BASE / 'primary-reinspection.json', {'records': checks,
        'prior_audit': ref(prior_path, 'Inherited records retained unchanged'),
        'scope': 'Selected primary text; no claim to inspect every page or reproduce experiments'})
    chapter = BASE / 'chapter.tex'
    text = chapter.read_text()
    cited = {k.strip() for group in re.findall(shared.CITE, text) for k in group.split(',')}
    allowed = {x['integrated_citation_key'] for x in prior['sources']+audit['sources']}
    assert cited <= allowed
    assert {x['integrated_citation_key'] for x in audit['sources']} <= cited
    for phrase in ['not a measured', 'all-attempt', 'information clock',
                   'first remaining protocol', '115 matched evaluable',
                   'at most two', 'uninspected', 'not a guarantee']:
        assert phrase in text, phrase
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Focused literature, source-code comparison and exact planning chapter; not MR02 or frontier-census acceptance',
        'reviewed': ref(chapter, 'Developed connected argument with target, clock and alternatives'),
        'plan_review': ref(BASE / 'plan-review.md', 'Declared scope and matched acquisition comparison'),
        'criteria': [
            {'index': 0, 'verdict': 'pass', 'finding': 'Five inspected primary works compare favorable and adverse results; three pinned software sources have concrete reuse/deferral decisions and unresolved full implementations remain explicit.'},
            {'index': 1, 'verdict': 'pass', 'finding': 'Fee-waiver target and two clocks are stated; full-world versus decision information, all-attempt costs, correlated errors, finite-horizon stopping and omitted support are developed and independently checked.'},
            {'index': 2, 'verdict': 'pass', 'finding': 'Published benchmarks are attributed, new numbers are stipulated exact planning results, and no live model, vendor, package or bank performance is claimed.'}],
        'substantive_checks': [
            'Full-world EIG is explicitly distinguished from information about H; no general claim that information design fails.',
            'Costs and terminal values share normalized deployment units; no measured ROI or calibrated signal accuracy.',
            'Stopping optimality is restricted to the declared menu and horizon at most two.',
            'DISCERN levels are independently instantiated; rubric percentages are not discovery probabilities.',
            'MDA matched-evaluable results and compute limits are not generalized to all attempts.',
            'Benchmark source interfaces and parser fallbacks are inspected without execution; overview repository is not an executable implementation.',
            'Secondary account of the therapeutic case does not validate an uninspected biomedical original.',
            'Unavailable original routes and candidate identities remain in the omissions register.'],
        'evidence': [ref(BASE / n, n) for n in ['source-audit.json', 'primary-reinspection.json', 'exact-review.json',
                                              'candidate-register.json', 'omissions-register.json', 'acquisition-review.json']],
        'independent_review': False, 'visual_acceptance': False, 'frontier_census_closed': False,
        'runtime_qualification': False, 'original_gap_qualification': False}
    core.write(BASE / 'author-review.json', review)
    print(json.dumps({'review': 'pass', 'cited_in_chapter': len(cited), 'new_audited_records': len(audit['sources'])}))


if __name__ == '__main__':
    main()
