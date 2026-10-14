#!/usr/bin/env python3
"""Review the economics source delta, calculations and nonduplicate depth."""
import json
from pathlib import Path

import build_l8_economics_v3_20261014 as build
import build_l8_economics_20261014 as work
import l8_economics_examples_20261014 as examples
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = work.REVIEWER
REVIEW = ROOT / 'docs/program/comprehensive-v14/work/TEXT.REVIEW.L8/chapter-review.json'
LIMITS = work.LIMITS + [
    'Author review, not independent scientific or institutional acceptance.',
    '6.5 nonduplicate substantive pages meet the six-page minimum; the seven-page planning target is not claimed.',
    'Whole-reader coverage/depth and sponsor/rendered acceptance remain open under Q1/Q5.',
]


def main():
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(build.PRIOR.read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    for obj in [report, audit, prior, trace, json.loads((BASE / 'prepared-inputs.json').read_text()),
                json.loads((work.BASE / 'derivation-review.json').read_text()),
                json.loads((work.BASE / 'primary-review.json').read_text())]:
        verify_bindings(obj)
    assert trace['status'] == 'pass' and not trace['issues'] and trace['scholarly_pdfs'] == 172
    assert json.loads((OUT / 'text-layout-review.json').read_text())['status'] == 'pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 601 and len(new) == 603 and all(new[k] == s for k, s in old.items())
    replacements = {path: str((BASE / name).relative_to(ROOT)) for path, name in build.REPAIRS.items()}
    for path, dest in replacements.items():
        assert (ROOT / dest).read_text() == build.corrected(path, (ROOT / path).read_text())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] not in [str(build.OLD.relative_to(ROOT)), *replacements]]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous_trace = json.loads((build.PRIOR.parent.parent / 'traceability-review.json').read_text())
    contexts = {r['citation_key']: r['citation_contexts'] for r in trace['records']}
    preserved_contexts = 0
    for row in previous_trace['records']:
        for ctx in row['citation_contexts']:
            if ctx['path'] in replacements:
                assert any(c['path'] == replacements[ctx['path']] and c['line'] == ctx['line']
                           for c in contexts[row['citation_key']])
            else:
                assert ctx in contexts[row['citation_key']], row['citation_key']
            preserved_contexts += 1
    assert examples.calculate() == json.loads((work.BASE / 'exact-results.json').read_text())
    pages = (OUT / 'reader.txt').read_text().split(chr(12))
    text = ' '.join((OUT / 'reader.txt').read_text().split())
    for phrase in ['11,200', '2,500', 'USD 7.68', 'weakly preferred', '451.39',
                   'USD 20,600', '19', 'deployment mixture', 'observationally equivalent worlds']:
        assert phrase.lower() in text.lower(), phrase
    chapter_text = ' '.join(' '.join(pages[522:534]).split())
    for defect in ['overlap.Chou', 'separately.Leban', 'case.(Causal', 'stratum.(Causal']:
        assert defect not in chapter_text
    assert 'poor overlap (Chou et al., 2026).' in chapter_text
    assert 'separately (Leban and Sun, 2026).' in chapter_text
    assert report['chapter_sections']['la:economics'] == 505
    assert report['chapter_sections']['exec14:l8-development-end'] == 516
    credits = [
        (.5, 'Decision/information formulation and initial economic example; chapter heading and repeated ambiguity framing excluded.'),
        (.75, 'Exact signal/posterior, full cost and perfect-information ceiling; repeated refusal and confidence cautions discounted.'),
        (.25, 'Workflow resource distinctions; four-journey introductions and general paired-evaluation framing repeat other chapters.'),
        (.5, 'Full-cost break-even and consequential-error sensitivity; generic live-evaluation prerequisites and repeated accounting excluded.'),
        (.25, 'Economic tolerances and requested-case denominator; sample-size derivation and evaluation design belong to L7 and receive no L8 credit.'),
        (.75, 'Selective full-loss accounting, numerical reversal and review-loss threshold; CausalChat study description overlaps L7.'),
        (.75, 'Capped retry derivation, independent path law and persistent-mixture consequence; CausalDS comparison repeats L7 evidence.'),
        (.75, 'Distinct robust/regret criteria, randomized whole-action solution and joint-policy ranking; inherited funding values and journey recap excluded.'),
        (.75, 'Delayed construction option, current build baseline, stopping and quality thresholds; generic information-value explanation overlaps the early example.'),
        (.75, 'Deployment-mixture reversal and partial weight information; generic source limits and resource accounting recap discounted.'),
        (.5, 'Distinct remaining scientific inputs and investment questions for four journeys; existing integration examples and general prototype narrative excluded.'),
        (0, 'Two-line continuation and citation; no substantive page credit.'),
    ]
    credit = sum(c for c, _ in credits)
    assert len(credits) == 12 and credit == 6.5 and 6 <= credit <= 8
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Exact final 780-page economics reader'),
        (OUT / 'source-audit.json', '603 citation records and preserved identities'),
        (BASE / 'traceability-review.json', 'All citation uses and 172 genuine scholarly PDFs'),
        (OUT / 'text-layout-review.json', 'All-page text extraction and bounds'),
        (OUT / 'reader.txt', 'Inspected printed pages 505-516, physical pages 523-534'),
        (work.BASE / 'plan-review.md', 'Reviewed chapter scope and independent proposal route'),
        (work.BASE / 'primary-review.json', 'Three primary rereads and their task/population limits'),
        (work.BASE / 'derivation-review.json', 'Author mathematical and scenario review'),
        (work.BASE / 'exact-results.json', 'Seven reproduced scenario groups'),
        (ROOT / 'tools/l8_economics_examples_20261014.py', 'Exact arithmetic and full retry path enumeration'),
        (ROOT / 'docs/program/execution/2026-10-14/four-journeys/acceptance-cases.json', 'Public/generated prototypes and later authentic inputs'),
        (BASE / 'repair-review.json', 'Preserved citation fragments and equality wording corrections'),
        (BASE / 'prepared-inputs.json', 'Preserving successor source identities'),
        (build.CHAPTER, 'Reviewed successor of the contracted draft'),
        (Path(__file__).resolve(), 'Author source, mathematical and per-page depth review'),
    ]]
    findings = [
        'Decision value, selective loss, review effort, full costs, correlated retry, ambiguity rules, delayed pilot options and transport are connected to the banking proposal.',
        'All 601 inherited source records and original citation uses remain; two added project records bind scenarios and prototype design, with no new empirical claim.',
        'Three authentic primary works are reread within their original populations and protocols; timing, token use and benchmark results are not converted to bank ROI.',
        'Exact arithmetic and complete retry paths reproduce; comparison to immediate construction, stopping, current cost and delay are included.',
        'The original and v2 candidates remain preserved; four citation-spacing problems, two citation fragments and one equality wording issue are repaired.',
        '6.5 nonduplicate substantive pages across twelve physical pages meet the 6/7/8 allocation minimum; the seven-page target is not claimed and the nearly empty final page receives zero credit.',
        'Four independent prototype routes, conditional bank inputs and unresolved universal scientific claims remain explicit; absent authentic bank evidence is not a proposal blocker.',
    ]
    scope = 'Author review of allocated L8 economics topics and depth; project scenarios and prospective design only'
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'scope': scope, 'reviewer': REVIEWER,
        'reviewed_reader': report['pdf'], 'evidence': evidence, 'findings': findings,
        'preserved_source_records': 601, 'new_source_records': 2,
        'preserved_citation_uses': preserved_contexts, 'inherited_source_replacements': replacements,
        'unchanged_compiled_sources': len(kept), 'limitations': LIMITS, 'visual_acceptance': False,
    })
    write(REVIEW, {
        'operation_id': 'TEXT.REVIEW.L8', 'status': 'pass', 'scope': scope, 'reviewer': REVIEWER,
        'allocated_title': 'Banking cases, economics and remaining research',
        'allocation': {'min': 6, 'target': 7, 'max': 8}, 'substantive_page_credit': credit,
        'physical_span': {'first_printed_page': 505, 'last_printed_page': 516,
                          'first_pdf_page': 523, 'last_pdf_page': 534, 'pages': 12},
        'per_page': [{'printed_page': 505+i, 'credit': c, 'rationale': why} for i, (c, why) in enumerate(credits)],
        'measurement': 'Conservative standard-typography equivalents after excluding repeated content and previous chapter credit.',
        'double_counting': 'L8 only; L7 statistical design, L6 orchestration and integration-journey descriptions excluded.',
        'allocation_exception': None, 'planning_target_met': False, 'allocation_minimum_met': True,
        'reviewed_reader': report['pdf'], 'findings': findings,
        'topic_coverage': {
            'banking_cases': 'Distinct funding, servicing, discovery and observation investment questions and later evidence needs.',
            'economics': 'Complete requested-case costs and losses; selective routing, calibrated review and correlated retries.',
            'decision_uncertainty': 'Expected value, robust value, deterministic/randomized regret and joint policy information.',
            'next_investment': 'Public/generated pilot option with feasible stopping, delay and comparison to the current build option.',
            'remaining_research': 'Deployment-mixture and price inputs; restricted uncertainty research and equal-law information limits.',
            'alternatives': 'Ordinary analyst, numerical and assisted workflows; public prototype before justified authentic experiments.',
        },
        'followups_not_awarded': ['Authentic risk, target mixture, prices, review burden and bank ROI.',
                                 'Universal hidden-state, dependent-learner or temporal-graph theory.',
                                 'Q1 whole-manuscript coverage/depth and Q5 independent sponsor/rendered review.'],
        'evidence': evidence + [ref(BASE / 'release-source-review.json', 'Exact-reader author review')],
        'limitations': LIMITS, 'visual_acceptance': False, 'original_gap_qualification': False,
    })
    graph, _, _ = run.combined(ROOT, core.read(ROOT, core.STATE))
    for identifier, facts in [
        ('TEXT.DRAFT.L8', [
            'Connected economics argument develops notation, assumptions, derivations, alternatives and four banking consequences.',
            'Claims retain primary audits and scenario labels; exact constructions reproduce and process records remain outside the chapter.']),
        ('TEXT.REVIEW.L8', [
            'Allocated banking, economics and remaining-research topics are developed and reviewed; observed wording/citation defects are repaired.',
            'Measured 6.5 nonduplicate substantive pages meet the six-page minimum; target seven is explicitly not claimed and no allocation exception is used.']),
    ]:
        node = run.ledger.operation(graph, identifier)
        receipt = run.ledger.receipt_template(node)
        # Contracted draft stays immutable; its reviewed successor is evidence.
        outputs = [ref(ROOT / path, 'Contracted output; successor linkage in review evidence') for path in node['outputs']]
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
                       limitations=LIMITS, outputs=outputs, nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': i, 'verdict': 'pass', 'finding': f,
                                  'evidence': evidence + [ref(REVIEW, 'Topic/depth and successor review')]}
                                 for i, f in enumerate(facts)])
        write(BASE / ('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT')
                      else 'review-operation-receipt.json'), receipt)
    print(json.dumps({'draft': 'pass', 'topic_depth_review': 'pass', 'substantive_pages': credit,
                      'physical_pages': 12, 'whole_reader_pages': report['pages'], 'proposal_accepted': False}))


if __name__ == '__main__':
    main()
