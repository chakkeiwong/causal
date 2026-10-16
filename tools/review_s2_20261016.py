#!/usr/bin/env python3
"""Review the recovered S2 reader, retained sources and exclusive topic depth."""
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path
import re

import build_s2_reader_v2_20261016 as build
import prepare_s2_v2_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT / 'docs/program/comprehensive-v14/work/TEXT.REVIEW.S2/chapter-review.json'
LIMITS = work.LIMITS + [
    '16.5 exclusive substantive page equivalents meet the 16-page minimum; the 20-page planning target remains unmet.',
    'Depth includes explicitly selected distributed inherited S2 material, not just the eight-page new synthesis; it does not close MR01 or its census operations.']


def read(path):
    return json.loads(path.read_text())


# Credit concerns distinct developed arguments, not page length or number of packages.
BLOCKS = [
    ('New discovery synthesis', 173, [
        (.25, 'Observation-experiment notation and question selection; chapter title and common S1 graph/effect/confidence contract excluded.'),
        (0, 'Constraint, score and functional-family overview repeats the detailed comparisons credited below.'),
        (.75, 'Cancellation derivation, distinct mechanism targets and robust decision consequence; generic stability framing discounted.'),
        (.5, 'Three-model action/effect ambiguity and decision criteria; repeated graph-class and selection motivation discounted.'),
        (.25, 'Average-versus-endpoint impulse decision; common temporal equation, clocks and package recap excluded.'),
        (.5, 'Joint versus outcome-only intervention contrasts; known-target assumptions and native score motivation credited in detailed comparisons.'),
        (.5, 'Exact information-value comparison and measurement implication; portfolio recap excluded.'),
        (0, 'Generic reuse, prototype and omissions framing belongs to S1/S9/S10 and receives no S2 credit.')]),
    ('Java discovery and conditional independence', 182, [
        (0, 'Repeated Gaussian equivalence, common endpoint meanings and introduction excluded.'),
        (.75, 'Distinct PC, FGES, DirectLiNGAM and Java DAGMA scientific procedures; source-version introduction excluded.'),
        (.75, 'Fisher transform, missingness and rank/failure interpretation; generic interface requirements discounted.'),
        (.75, 'Nonmonotone conditioning, depth-three separator and exact collider calculation; repeated prototype advice excluded.')]),
    ('Python independent and functional discovery', 189, [
        (0, 'Prior Java qualification continuation and Python introduction excluded.'),
        (.25, 'Finite structural path-sum derivation; matrix/endpoint interchange and portfolio introduction reserved for integration/S9.'),
        (.25, 'Method-specific PC test, collider and search qualifications; package table and aliases are catalog material.'),
        (.75, 'Conditioning limits, distinct scores and DirectLiNGAM pruning/functional premises; repeated row-count warning discounted.'),
        (.5, 'Distinct exponential, polynomial and log-determinant acyclicity arguments; repeated Gaussian equivalence excluded.'),
        (.75, 'Weak-cycle diagnostic and unit-dependent objective derivation; environment and adapter discussion excluded.'),
        (.75, 'Causica variational objective, intervention simulation and conditional uncertainty; CDT bridge discussion excluded.'),
        (.5, 'Selection-induced Gaussian dependence and missingness alternatives; rights and general adapter framing excluded.'),
        (0, 'Generic prototype/economics continuation and following symbolic-identification section excluded.')]),
    ('R latent and selection discovery', 225, [
        (.25, 'Selection-sensitive ancestral endpoint interpretation; previous reuse passage, introductions and repeated RFCI recap excluded.'),
        (.75, 'Strictly positive hidden/selection countermodels and FCI/RFCI information tradeoff; repeated ambiguity motivation discounted.'),
        (.75, 'Specific consistency and FCI+ complexity conditions, search caps and order dependence; repeated test-level cautions discounted.'),
        (.25, 'Joint selection/context restrictions and limits of diagnostic completeness; graph-conversion implementation belongs to integration/S9.'),
        (0, 'Reuse/prototype continuation and following pgmpy section excluded.')]),
    ('Python temporal, context and intervention discovery', 295, [
        (0, 'Previous R continuation and Python introduction excluded.'),
        (.75, 'Structural versus reduced responses, cumulative decision and exact sampling-frequency ambiguity; repeated clock notation discounted.'),
        (.75, 'JPCMCI context assumptions and RPCMCI regime experiment/mask limits; rights and generic adapter prose excluded.'),
        (.75, 'Selected-model uncertainty, VARLiNGAM bootstrap scope, DYNOTEARS clock transformation and soft/perfect mechanisms; maintenance excluded.'),
        (.75, 'Known-target score and equivalence class, UT-IGSP premises and lexicographic-versus-sum score; facade/environment detail excluded.'),
        (.75, 'DCDI, ENCO and SDCD theorem/finite-optimizer distinctions and intervention-mask meaning; repeated portfolio and trial design excluded.'),
        (0, 'Repeated comparison/omissions framing and next Java section excluded.')]),
    ('Native temporal and interventional engines', 306, [
        (0, 'Prior Java continuation and native-family introduction excluded.'),
        (.25, 'Intervention variance as additional information; repeated observational equivalence, values and GIES premises excluded.'),
        (.75, 'Nonintervened-row local likelihood and exact intercept consequence; Rcpp bridge, rights and state conversion excluded.'),
        (.25, 'Supplied latent-model learning versus discovery and sDBN sampling construction; state permutation and environment/rights excluded.'),
        (.5, 'Overlapping-subject variance and candidate-versus-directed search/constraint meanings; transport and dependency details excluded.'),
        (.25, 'Different constraint predicates over the two-node graph universe; repeated reuse table and CLI/MCP contract excluded.'),
        (0, 'Repeated qualification, costs and omissions continuation excluded.')]),
]


def main():
    report = read(OUT / 'build-report.json'); audit = read(OUT / 'source-audit.json')
    prior = read(build.PRIOR); index = read(BASE / 'traceability-review.json')
    for obj in [report, audit, prior, index, read(BASE / 'prepared-inputs.json'),
                read(work.BASE / 'draft-author-review.json'), read(work.BASE / 'primary-review.json')]:
        verify_bindings(obj)
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 175
    layout = read(OUT / 'text-layout-review.json')
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert report['pages'] == 845 and report['discovery_sections'] == {'s2': 173, 's2-end': 180}
    assert build.DRIVER.read_text() == build.expected_driver()
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 658 and len(new) == 660 and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    previous = read(build.PRIOR.parent.parent / 'traceability-review.json')
    contexts = {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for row in previous['records']:
        assert not Counter(json.dumps(x, sort_keys=True) for x in row['citation_contexts']) - contexts[row['citation_key']]
    exact = read(work.BASE / 'exact-results.json')
    assert work.examples.calculate() == exact
    # Independent direct structural substitutions, separate from the matrix/path routine.
    assert exact['chain']['forward']['do_M_one_minus_zero_mean_XMY'] == ['0', '1', '1']
    assert exact['chain']['reverse']['do_M_one_minus_zero_mean_XMY'] == ['1/2', '1', '0']
    assert exact['chain']['fork']['do_M_one_minus_zero_mean_XMY'] == ['1/2', '1', '1']
    selected = [row for row in exact['selection']['rows'] if row['selected']]
    means = [sum(F(row['probability'])*row['Y'] for row in selected if row['X'] == a) /
             sum(F(row['probability']) for row in selected if row['X'] == a) for a in [0, 1]]
    assert means[1] - means[0] == 1
    assert F(2, 3)*max(F(0), F(22-8, 2)) - F(22-8-8, 3) == F(8, 3)
    pages = (OUT / 'reader.txt').read_text().split(chr(12))
    chapter_text = ' '.join(' '.join(pages[191:199]).split())
    for phrase in ['Faithfulness and the business target', 'three-variable example', 'USD 22',
                   '16/3', '8/3', 'end-of-period', 'not trial budgets']:
        assert phrase in chapter_text, phrase
    per_page = []
    for block, start, rows in BLOCKS:
        for offset, (credit, reason) in enumerate(rows):
            printed = start + offset; physical = printed + 19
            assert re.search(r'\b' + str(printed) + r'\b', pages[physical-1])
            per_page.append({'block': block, 'printed_page': printed, 'pdf_page': physical,
                             'credit': credit, 'rationale': reason})
    assert len({r['pdf_page'] for r in per_page}) == len(per_page)
    credit = sum(r['credit'] for r in per_page); assert credit == 16.5
    prior_reviews = sorted((ROOT / 'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    # Text extraction drops math delimiters. Check the source instead of "repairing" correct mathematics.
    fisher_source = ROOT / 'docs/program/execution/2026-10-13/python-discovery/comparison.tex'
    assert r'\bigl|\operatorname{atanh}(\widehat r_{ij\mid S})\bigr|' in fisher_source.read_text()
    evidence = [ref(p, a) for p, a in [
        (OUT / 'build-report.json', 'Exact 845-page discovery reader'),
        (OUT / 'source-audit.json', '660 source records'),
        (BASE / 'traceability-review.json', '658 inherited citation records/contexts retained; 175 genuine scholarly PDFs'),
        (OUT / 'text-layout-review.json', 'All-page text bounds'),
        (OUT / 'reader.txt', 'Inspected synthesis and distributed discovery pages listed in depth review'),
        (work.CHAPTER, 'Connected discovery synthesis'),
        (work.BASE / 'primary-review.json', 'Four paper rereads, four software excerpts and 29 inherited citation keys'),
        (work.BASE / 'exact-results.json', 'Four exact authored reference families'),
        (ROOT / 'tools/s2_examples_20261016.py', 'Rational structural matrix, directed paths and decision grouping'),
        (work.BASE / 'discovery-design.json', 'Proposed portfolio and preserved omissions'),
        (work.BASE / 'draft-author-review.json', 'Draft review and preserved preparation failures'),
        (work.BASE / 'plan.md', 'Reviewed execution plan'),
        (ROOT / 'docs/program/comprehensive-v14/gap-audit.json', 'S2 allocation 16/20/24 and distributed development labels'),
        (fisher_source, 'Absolute value retained in original Fisher transform despite text-extraction loss'),
        (Path(__file__), 'Exact-reader and exclusive-depth review')]]
    evidence += [ref(p, 'Prior chapter allocation checked for duplicate credit') for p in prior_reviews]
    scope = 'Author review of S2 discovery proposal argument and distributed nonduplicate depth; not whole-census or product acceptance'
    findings = [
        'IID constraint/score/functional, latent/selection, temporal/context and known/unknown-intervention subjects have developed scientific and software comparisons.',
        'Exact authored Gaussian, cancellation, selection, intervention-information and horizon consequences reproduce without upstream execution.',
        '658 inherited source records, compiled sources and all citation contexts survive; two project additions yield 660 records and 175 genuine scholarly PDFs.',
        '16.5 exclusive substantive page equivalents meet minimum 16; target 20 remains unmet. Catalogs, process records, repeated arguments and adjacent allocations are excluded.',
        'No unresolved source/math contradiction found in this bounded review. Fisher absolute-value delimiters are present in LaTeX although absent in extracted text.',
        'Broader software searches and source-specific omissions remain open; no discovery-cell census or whole MR01 closure is inferred.']
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'scope': scope, 'reviewer': work.REVIEWER,
        'reviewed_reader': report['pdf'], 'evidence': evidence, 'findings': findings,
        'preserved_records': 658, 'new_records': 2, 'preserved_compiled_sources': len(kept),
        'original_contexts_retained': True, 'limitations': LIMITS, 'visual_acceptance': False})
    write(REVIEW, {
        'operation_id': 'TEXT.REVIEW.S2', 'status': 'pass', 'scope': scope, 'reviewer': work.REVIEWER,
        'allocated_title': 'Discovery across IID, latent, temporal and experimental settings',
        'allocation': {'min': 16, 'target': 20, 'max': 24}, 'substantive_page_credit': credit,
        'new_synthesis_span': {'first_printed_page': 173, 'last_printed_page': 180, 'first_pdf_page': 192, 'last_pdf_page': 199, 'pages': 8},
        'distributed_blocks': [{'name': name, 'first_printed_page': start, 'last_printed_page': start+len(rows)-1,
                                'substantive_credit': sum(c for c, _ in rows)} for name, start, rows in BLOCKS],
        'per_page': per_page,
        'measurement': 'Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; not a calibrated measure of prose quality or visual acceptance.',
        'double_counting': 'S2 only. Existing accepted S1/S10/I1/I3/L3-L8 allocations excluded. General acquisition, interoperability and qualification prose reserved for S8/S9/S10 and integration chapters. Repeated S2 examples across blocks are discounted. Other distributed discovery material receives no credit in this review.',
        'allocation_exception': None, 'allocation_minimum_met': True, 'planning_target_met': False,
        'reviewed_reader': report['pdf'], 'findings': findings,
        'topic_coverage': ['Observation experiment and graph/effect/decision target', 'Independent constraint, score and functional discovery',
                           'Hidden variables and selected populations', 'Temporal horizons, physical sampling and contexts',
                           'Known/unknown and perfect/soft interventions', 'Source-specific comparative roles and scientific failure modes',
                           'Reproducible decision and information consequences'],
        'followups_not_awarded': ['Complete software census and omitted originals', '20-page planning target',
                                 'Actual new package or bank experiments', 'General graph/effect calibration', 'Q1/Q5 and visual acceptance'],
        'evidence': evidence + [ref(BASE / 'release-source-review.json', 'Exact-reader author review')],
        'limitations': LIMITS, 'visual_acceptance': False, 'whole_census_closed': False, 'original_gap_qualification': False})
    graph, _, _ = run.combined(ROOT, core.read(ROOT, core.STATE))
    for identifier, facts in [
        ('TEXT.DRAFT.S2', ['Connected argument develops notation, assumptions, derivations, diagnostics, alternatives and banking consequences.',
                           'Audited originals and exact authored examples support claims; process records stay outside the product narrative.']),
        ('TEXT.REVIEW.S2', ['Allocated discovery settings are developed across the synthesis and selected inherited comparisons; bounded source and mathematics review passes.',
                            '16.5 nonduplicate substantive page equivalents meet minimum 16; target 20 remains unmet; no allocation exception.'])]:
        node = run.ledger.operation(graph, identifier); receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=work.REVIEWER, limitations=LIMITS,
                       outputs=[ref(ROOT / p, 'Contracted output') for p in node['outputs']], nonexecution_reason='', revisit_trigger='',
                       criteria=[{'index': i, 'verdict': 'pass', 'finding': finding,
                                  'evidence': evidence + [ref(REVIEW, 'Exclusive topic/depth review')]} for i, finding in enumerate(facts)])
        write(BASE / ('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'), receipt)
    print(json.dumps({'draft': 'pass', 'topic_depth_review': 'pass', 'substantive_pages': credit,
                      'planning_target_met': False, 'reader_pages': report['pages'], 'whole_census_closed': False}))


if __name__ == '__main__':
    main()
