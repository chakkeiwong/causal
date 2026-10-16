#!/usr/bin/env python3
"""Review the exact S3 successor without rewriting any recovered artifact."""
from collections import Counter
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_s3_reader_v3_20261017 as build
import prepare_s3_20261017 as work
import s3_sensitivity_20261017 as sensitivity
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S3/chapter-review.json'
LIMITS = work.LIMITS + [
    'Ten exclusive substantive page equivalents meet minimum ten; the twelve-page planning target is unmet.',
    'The initial 6.5-page depth failure and subsequent notation repair remain preserved; physical length is not credited as substantive depth.',
    'Exclusion sensitivity is a necessary outer envelope, not a sharp full-table bound; defier budgets are stipulated scientific restrictions.']

# Fractions of final extracted pages after excluding repeated and adjacent subjects.
PAGES = [
    (.25, 'Banking target distinctions; title, general model-class notation and repeated S1 identification framing excluded.'),
    (.75, 'Support and standardization derivation with exact receipt composition; repeated model-class framing discounted.'),
    (.75, 'Total/direct contrast and adjustment completeness domain; general method-selection framing discounted.'),
    (1, 'IDC versus joint-first identification and a positive complete-law structural counterexample.'),
    (1, 'Cross-world coupling, sharp benefit/harm fractions and retrospective attribution under identical experimental marginals.'),
    (1, 'Counterfactual harm restriction and IV principal-stratum derivation with a distinct population target.'),
    (.75, 'Population/encouragement actions and unobserved IV assumptions; numerical ratio discussion excluded as I1 overlap.'),
    (1, 'Consistency-only sharp completion bounds and distinct maximin/minimax-regret decisions.'),
    (0, 'Numerical envelopes and software-route introduction repeat I1 and receive no S3 credit.'),
    (0, 'Software/interface discussion overlaps I1; no duplicate credit.'),
    (.25, 'New common sixteen-type response map; preceding prototype and acquisition prose excluded.'),
    (.5, 'Full-law linear/fractional objectives, exact table and stratum success-mass recovery; repeated monotone means discounted.'),
    (.75, 'Constructive coupling proves full-table attainability; bounded-defier masses and setup; repeated population/net calculation excluded.'),
    (1, 'Sufficient full-cell margin domain, ratio derivatives, sharp witnesses, contrast-only infeasibility and distinct population behavior.'),
    (.75, 'Explicit Y(z,d), fixed-encouragement target, Gamma decomposition and necessary exclusion envelopes; repeated encouragement reward excluded.'),
    (.25, 'Targeted information requirements and full-cell extremal-law verification; repeated confidence-region/interface framing excluded.')]


def read(path):
    return json.loads(path.read_text())


def contexts(index, exclude=None):
    return {r['citation_key']: Counter(json.dumps(x, sort_keys=True) for x in r['citation_contexts']
                                      if x['path'] != exclude) for r in index['records']}


def preserve(audit, index, predecessor, expected_count, replace=()):
    prior = read(predecessor/'reader/source-audit.json')
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == expected_count and all(new[k] == s for k, s in old.items())
    files = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] not in replace]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    current = contexts(index)
    previous = contexts(read(predecessor/'traceability-review.json'))
    for key, old_context in previous.items():
        assert not old_context-current[key], key
    return len(kept)


def main():
    report = read(OUT/'build-report.json'); audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    for path in [OUT/'build-report.json', OUT/'source-audit.json', BASE/'traceability-review.json',
                 BASE/'prepared-inputs.json', BASE/'notation-repair.json',
                 work.BASE/'primary-review.json', work.BASE/'draft-author-review.json',
                 work.BASE/'depth-review-initial.json', sensitivity.BASE/'mathematics-review.json']:
        verify_bindings(read(path))
    assert report['pages'] == 899 and report['cited_records'] == 703
    assert index['status'] == 'pass' and not index['issues'] and index['scholarly_pdfs'] == 187
    layout = read(OUT/'text-layout-review.json')
    assert layout['status'] == 'pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.EXTENSION.read_text() == build.corrected_extension()
    canonical = work.PRIOR.parent.parent
    candidate = build.previous.candidate.BASE
    retained_canonical = preserve(audit, index, canonical, 699,
                                 [str(build.CANONICAL_OLD.relative_to(ROOT))])
    retained_candidate = preserve(audit, index, candidate, 702,
                                 [str(build.previous.OLD.relative_to(ROOT))])
    v2 = read(build.previous.OUT/'source-audit.json')
    old_sources = {s['integrated_citation_key']:s for s in v2['sources']}
    new_sources = {s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old_sources) == 703 and old_sources == new_sources
    files = {r['path']:r for r in audit['tex_files']}
    replaced = {str(build.OLD.relative_to(ROOT)), str(build.previous.EXTENSION.relative_to(ROOT))}
    kept = [r for r in v2['tex_files'] if r['path'] not in replaced]
    assert all(files[r['path']]['sha256'] == r['sha256'] for r in kept)
    # V2's extension path/context changes solely through the deterministic notation repair.
    # Recompute the exact new citation windows; do not falsely call these byte-identical.
    v2_contexts = contexts(read(build.previous.BASE/'traceability-review.json'),
                           str(build.previous.EXTENSION.relative_to(ROOT)))
    current_contexts = contexts(index)
    for key, previous in v2_contexts.items():
        assert not previous-current_contexts[key], key
    expected = {}
    tex = build.corrected_extension()
    for match in re.finditer(shared.CITE, tex):
        for key in match.group(1).split(','):
            expected.setdefault(key.strip(), []).append({
                'path':str(build.EXTENSION.relative_to(ROOT)),
                'line':tex.count('\n',0,match.start())+1,
                'context':tex[max(0,match.start()-550):match.end()+220]})
    found = {r['citation_key']:[x for x in r['citation_contexts']
                              if x['path'] == str(build.EXTENSION.relative_to(ROOT))]
             for r in index['records']}
    assert {k:v for k,v in found.items() if v} == expected
    assert work.examples.calculate() == read(work.BASE/'exact-results.json')
    assert work.independent()['status'] == 'pass'
    exact = read(sensitivity.BASE/'exact-results.json')
    assert sensitivity.calculate() == exact and sensitivity.separate_review(exact)['status'] == 'pass'
    aux = (OUT/(build.NAME+'.aux')).read_text()
    equation_numbers = {}
    for label in ['product-coupling','defier-feasible','defier-ratio','defier-sharp','exclusion-outer']:
        match = re.search(re.escape('\\newlabel{exec17:s3-'+label+'}{{')+r'([^}]+)',aux)
        assert match and re.fullmatch(r'20\.\d+',match.group(1))
        equation_numbers[label] = match.group(1)
    assert equation_numbers['product-coupling'] == '20.4'
    assert equation_numbers['exclusion-outer'] == '20.9'
    pages = (OUT/'reader.txt').read_text().split(chr(12)); per_page=[]
    for offset, (credit, rationale) in enumerate(PAGES):
        printed=181+offset; physical=printed+20
        assert re.search(r'\b'+str(printed)+r'\b',pages[physical-1])
        per_page.append(dict(printed_page=printed,pdf_page=physical,credit=credit,rationale=rationale))
    assert report['identification_sections']['s3-sensitivity-end'] == 196
    assert '(20.4)' in pages[213] and '(20.13)' not in pages[213]
    # The text extractor reorders the stacked fraction on p195. Source retains 6/5.
    assert r'\tfrac65' in tex and '100{E(Y' in ' '.join(pages[214].split())
    credit=sum(row['credit'] for row in per_page); assert credit == 10
    prior_reviews=sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Exact 899-page successor'),
        (OUT/'source-audit.json','703 preserved source records; 187 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Exact-driver primary identity and citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds pass'),
        (OUT/'reader.txt','S3 printed181-196/physical201-216 inspected'),
        (work.CHAPTER,'Connected identification/counterfactual/effect-set chapter'),
        (build.EXTENSION,'Analytic full-table sensitivity and correctly numbered equations'),
        (work.BASE/'plan.md','Reviewed execution plan'),
        (work.BASE/'primary-review.json','Five genuine paper rereads and inherited software-source support'),
        (work.BASE/'exact-results.json','Six exact authored law families'),
        (ROOT/'tools/s3_examples_20261017.py','Exact rational reference implementation'),
        (ROOT/'tools/prepare_s3_20261017.py','Separate author algebra and primary review'),
        (work.BASE/'depth-review-initial.json','Preserved initial6.5-page depth failure'),
        (work.BASE/'sensitivity-plan.md','Reviewed depth repair'),
        (sensitivity.BASE/'exact-results.json','36 feasible vertices and complete endpoint laws'),
        (sensitivity.BASE/'mathematics-review.json','Separate marginal-mixing review'),
        (ROOT/'tools/s3_sensitivity_20261017.py','Exact sensitivity reference and separate review'),
        (work.BASE/'prototype-design.json','Proposed comparison; not executed'),
        (BASE/'notation-repair.json','Preserved equation-reference finding and repair'),
        (ROOT/'docs/program/comprehensive-v14/gap-audit.json','S3 allocation10/12/14'),
        (Path(__file__),'Exact-reader nonduplicate depth, source and mathematics review')]]
    evidence += [ref(p,'Prior allocation checked for duplicate credit') for p in prior_reviews]
    scope='Author S3 subject, primary-source, mathematics and exclusive-depth review; proposal development only'
    findings=[
        'Develops adjustment completeness, ID/IDC, single/cross-world distinctions, IV action targets, sharp effect sets and assumption sensitivity.',
        'Six exact law families, separate algebra, full eight-cell mixing and36 feasible vertices reproduce; no upstream or bank experiment is inferred.',
        'All699 canonical and702 original-candidate records and citation-context multisets survive. All703 V2 source records are unchanged.',
        'V2 extension contexts change only through the deterministic equation-environment/path repair; retained nonextension contexts match exactly.',
        'Corrected equation references20.4-20.9 agree with the inspected source and extracted chapter. The stacked6/5 on p195 is source-correct despite extractor ordering.',
        'Ten exclusive substantive page equivalents meet minimum ten; target twelve is unmet. Repeated I1 numerical/software/interface material receives zero credit.',
        'Exclusion envelopes are necessary outer bounds; full-law sharpness is claimed only for the proven IV classes. Budgets and monetary values are stipulated.',
        'Visual acceptance, Q1/Q5, whole-census coverage, independent review and authentic bank/product qualification remain open.']
    write(BASE/'release-source-review.json',dict(
        status='pass',issues=[],scope=scope,reviewer=work.REVIEWER,reviewed_reader=report['pdf'],
        findings=findings,evidence=evidence,canonical_records_preserved=699,
        original_candidate_records_preserved=702,v2_records_preserved=703,
        canonical_compiled_sources_preserved=retained_canonical,
        candidate_compiled_sources_preserved=retained_candidate,
        v2_unmodified_compiled_sources_preserved=len(kept),
        original_context_multisets_retained=True,v2_extension_contexts_byte_identical=False,
        v2_context_change='Exact deterministic five-environment repair with recomputed citation windows; formula bodies/claims/citations preserved.',
        equation_numbers=equation_numbers,limitations=LIMITS,visual_acceptance=False))
    write(REVIEW,dict(
        operation_id='TEXT.REVIEW.S3',status='pass',scope=scope,reviewer=work.REVIEWER,
        allocated_title='Identification, counterfactuals and effect sets',
        allocation=dict(min=10,target=12,max=14),substantive_page_credit=credit,
        new_synthesis_span=dict(first_printed_page=181,last_printed_page=196,
                                first_pdf_page=201,last_pdf_page=216,pages=16),
        per_page=per_page,allocation_minimum_met=True,planning_target_met=False,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; not visual acceptance or a calibrated prose-quality metric.',
        double_counting='S3 only. No inherited pages borrowed. Numerical/software/interface/prototype overlap with I1 excluded; S1/S2/L3-L8/I3/S10 allocations retained. Repeated monotone results and generic inference framing discounted.',
        reviewed_reader=report['pdf'],findings=findings,
        topic_coverage=['Law-relative identification and support','Adjustment and completeness domains',
                        'ID/IDC conditional versus joint identification','Cross-world response couplings',
                        'Receipt, encouragement and population IV targets','Sharp consistency/IV sets',
                        'Full-law defier and exclusion sensitivity','Scientific versus numerical failure'],
        followups_not_awarded=['Twelve-page planning target','Whole software census',
                               'Sharp full-cell exclusion relaxation','Package/runtime qualification',
                               'Bank assumptions, loss and actual costs','Q1/Q5 and rendered visual acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader author review')],
        limitations=LIMITS,visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S3',['Connected banking argument develops assumptions, notation, derivations, diagnostics and alternatives.',
                          'Genuine audited originals and exact authored examples support the claims; process records stay outside the narrative.']),
        ('TEXT.REVIEW.S3',['Allocated identification/counterfactual/effect-set subject and sensitivity develop fully enough for bounded author review; substantive/citation/math/notation findings resolved.',
                           'Ten nonduplicate substantive page equivalents meet minimum ten; target twelve remains unmet; no allocation exception.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
                       limitations=LIMITS,outputs=[ref(ROOT/p,'Contracted output') for p in node['outputs']],
                       nonexecution_reason='',revisit_trigger='',
                       criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(REVIEW,'Exclusive chapter-depth review')])
                                 for i,f in enumerate(facts)])
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
                          planning_target_met=False,reader_pages=899,visual_acceptance=False)))


if __name__=='__main__':
    main()
