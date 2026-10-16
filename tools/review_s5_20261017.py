#!/usr/bin/env python3
"""Review the preserving S5 depth successor and its exact citation contexts."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_s5_reader_v3_20261017 as build
import prepare_s5_20261017 as work
import s5_covariance_20261017 as joint
import s5_occupied_error_20261017 as extension
import master_control as core
import run_program as run
from review_s3_20261017 import contexts, preserve
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S5/chapter-review.json'
LIMITS = work.LIMITS + [
    '14.25 exclusive substantive page equivalents meet minimum14; planning target17 is unmet.',
    'The initial10.75-page failure, unpublished934-page candidate and all first-draft repairs remain preserved.',
    'The occupied-history identity compares the same fixed policy, initial law and rewards under two transition laws; it is not itself a policy effect.',
    'Reference occupancies, signed-support restrictions and genuine independent reference-row draws are explicit conditional premises, not bank findings.',
    'The validation intervals are prospective. No new validation draw, measured coverage, optimal integer allocation or bank validation price is reported.'
]


def read(path):
    return json.loads(path.read_text())


def copied_contexts(index):
    """Verify changed paths/windows by deterministic source, not a false byte claim."""
    previous = read(build.previous.BASE/'traceability-review.json')
    retained = contexts(previous, str(build.previous.CHAPTER.relative_to(ROOT)))
    current = contexts(index)
    for key, old in retained.items():
        assert not old-current[key], key
    expected = {}
    tex = build.expected_chapter()
    for match in re.finditer(shared.CITE, tex):
        for key in match.group(1).split(','):
            expected.setdefault(key.strip(), []).append(dict(
                path=str(build.CHAPTER.relative_to(ROOT)),
                line=tex.count('\n',0,match.start())+1,
                context=tex[max(0,match.start()-550):match.end()+220]))
    found = {r['citation_key']:[x for x in r['citation_contexts']
                              if x['path']==str(build.CHAPTER.relative_to(ROOT))]
             for r in index['records']}
    assert {k:v for k,v in found.items() if v} == expected


def main():
    report=read(OUT/'build-report.json'); audit=read(OUT/'source-audit.json')
    index=read(BASE/'traceability-review.json')
    for path in [OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json',
                 BASE/'prepared-inputs.json',BASE/'extension-author-review.json',
                 work.BASE/'primary-review.json',build.previous.BASE/'draft-author-review.json',
                 work.BASE/'depth-review-initial.json',work.BASE/'revision-v2/mathematics-review.json',
                 extension.BASE/'mathematics-review.json']:
        verify_bindings(read(path))
    assert report['pages']==939 and report['cited_records']==712
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==187
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.CHAPTER.read_text()==build.expected_chapter()
    assert build.CHAPTER.read_text().replace(build.INSERT+'\n\n','')==build.previous.CHAPTER.read_text()
    canonical=build.previous.PRIOR.parent.parent
    retained_canonical=preserve(audit,index,canonical,707,
                               [str(build.CANONICAL_OLD.relative_to(ROOT))])
    prior=read(build.PRIOR)
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==711 and all(new[k]==s for k,s in old.items())
    replaced={str(build.OLD.relative_to(ROOT)),str(build.previous.CHAPTER.relative_to(ROOT))}
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path'] not in replaced]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    copied_contexts(index)
    for module,name in [(work.examples,'exact-results.json'),(joint,'covariance-results.json')]:
        exact=read(work.BASE/name)
        assert module.calculate()==exact and module.separate(exact)['status']=='pass'
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations=dict(re.findall(r'\\newlabel\{(exec17:s5[^}]+)\}\{\{(22\.[0-9]+)\}\{',aux))
    assert set('22.'+str(n) for n in range(1,41)) <= set(equations.values())
    assert equations['exec17:s5-occupied-values']=='22.29'
    assert equations['exec17:s5-validation-allocation']=='22.40'
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    text=''.join(pages[235:256])
    assert all('('+str('22.'+str(n))+')' in text for n in range(1,41))
    assert '??' not in text
    initial=read(work.BASE/'depth-review-initial.json')
    per_page=[dict(row) for row in initial['per_page'][:-1]]
    assert sum(row['credit'] for row in per_page)==10.75
    additions=[
        (.75,'Exact reference-occupancy signed residual identity and telescoping proof; generic backward recursion, introduction and title discounted.'),
        (1,'Local signed-support envelope, three-period event-law witness, exact dollar discrepancy and occupied/restricted/uniform comparisons.'),
        (.75,'Validation-law transport proof, rare-history factor and zero-support monetary boundary; generic clocks/confounding/public-data prose excluded.'),
        (.5,'Conditional longitudinal residual interval with fixed known occupancies and sampling-premise consequences; generic concentration, union bound and optimization setup excluded.'),
        (.5,'Horizon/unequal-cost validation composition and worked feasible allocations with financial precision consequence; generic KKT proof, resource-allocation framing and conclusion excluded.'),
        (0,'Conclusion receives no additional depth.')]
    for offset,(credit,rationale) in enumerate(additions):
        per_page.append(dict(printed_page=230+offset,pdf_page=251+offset,
                             credit=credit,rationale=rationale))
    for row in per_page:
        assert re.search(r'\b'+str(row['printed_page'])+r'\b',pages[row['pdf_page']-1])
    assert report['effect_sections']['s5-end']==234
    assert 'Chapter 23' in pages[256] and 'Conclusion' in pages[254]
    credit=sum(row['credit'] for row in per_page); assert credit==14.25
    prior_reviews=sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Exact939-page preserving successor; no material compile warnings'),
        (OUT/'source-audit.json','712 audited records;187 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Exact-driver source identity and citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds pass; not visual acceptance'),
        (OUT/'reader.txt','Chapter22 printed215-235/physical236-256, extension and next boundary inspected'),
        (build.CHAPTER,'Preserving source copy with extension before original conclusion'),
        (build.EXTENSION,'Occupied-history error, validation transport and conditional validation'),
        (work.BASE/'plan.md','Reviewed14/17/20 allocation and overlap exclusions'),
        (work.BASE/'primary-review.json','Fifteen inspected primary-paper/software excerpts'),
        (work.BASE/'exact-results.json','Eight original exact authored families'),
        (work.BASE/'mathematics-review.json','Original separate author checks'),
        (work.BASE/'covariance-results.json','Joint event covariance and sharp first-split witness'),
        (work.BASE/'revision-v2/mathematics-review.json','Separate moment and coupling review'),
        (work.BASE/'draft-review-v1.json','Preserved initial semantic and TeX findings'),
        (BASE/'review-invocation-failure.json','Corrected review-only input path before any output'),
        (work.BASE/'depth-review-initial.json','Preserved10.75-page depth failure'),
        (work.BASE/'depth-extension-plan.md','Reviewed substantive repair'),
        (extension.BASE/'exact-results.json','Exact occupied errors, transport and prospective allocations'),
        (extension.BASE/'mathematics-review.json','Separate geometric/backward/support/KKT checks'),
        (ROOT/'tools/s5_occupied_error_20261017.py','Exact reference calculations and distinct author checks'),
        (work.BASE/'prototype-design.json','Common-target proposed comparison, not a new experiment'),
        (ROOT/'docs/program/comprehensive-v14/gap-audit.json','Exclusive S5 allocation14/17/20'),
        (Path(__file__),'Conservative per-page, source, mathematics and context review')]]
    evidence += [ref(p,'Prior chapter allocation checked for duplicate credit') for p in prior_reviews]
    scope='Author S5 subject, primary-source, mathematics and exclusive-depth review; proposal development only'
    findings=[
        'Develops discrete horizon bounds, survivor selection, ordered competing events, natural-action versus redraw targets, singular/noninjective shifts and the one-time fixed-map derivative.',
        'Fifteen primary excerpts, eight original exact families, joint-event/coupling constructions and the occupied-history extension support the bounded claims; no new upstream or bank experiment is inferred.',
        'All707 canonical records and citation-context multisets survive; all711 v2 source records are unchanged. The copied chapter retains every original byte after removing one inserted input.',
        'V2 chapter paths and nearby citation windows change deterministically; all other contexts are preserved and copied windows are regenerated from exact expected source.',
        'Equations22.1-22.40 resolve; extension printed230-234, conclusion235 and next-chapter boundary agree with source. All-page text bounds pass.',
        '14.25 exclusive substantive page equivalents meet minimum14; target17 remains unmet. Generic Bellman, concentration, resource-allocation, software-catalog and interface material receives no duplicate credit.',
        'The exact20.805USD event-value error can coexist with identical survival. Occupied/full-support, event-support and uniform envelopes are21.05,20.805 and30.299USD under explicit restrictions.',
        'A1USD validation mean can hide90USD target residual; prospective unequal-cost radius31.4016USD would not certify the20.805USD error sign. No validation sample or bank economics is reported.',
        'Q1/Q5, rendered visual acceptance, the three mandatory repairs, complete coverage/rights, independent review and product qualification remain open.']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,
        reviewer=work.REVIEWER,reviewed_reader=report['pdf'],findings=findings,evidence=evidence,
        canonical_records_preserved=707,v2_records_preserved=711,
        canonical_compiled_sources_preserved=retained_canonical,v2_unmodified_compiled_sources_preserved=len(kept),
        canonical_context_multisets_retained=True,v2_nonchapter_contexts_retained=True,
        v2_chapter_contexts_byte_identical=False,v2_context_change='Preserving path copy plus one inserted input; regenerated exact citation windows match.',
        equation_numbers=equations,limitations=LIMITS,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S5',status='pass',scope=scope,
        reviewer=work.REVIEWER,allocated_title='Longitudinal, survival and sequential software',
        allocation=dict(min=14,target=17,max=20),substantive_page_credit=credit,
        new_synthesis_span=dict(first_printed_page=215,last_printed_page=235,
                                first_pdf_page=236,last_pdf_page=256,pages=21),
        per_page=per_page,allocation_minimum_met=True,planning_target_met=False,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; no visual acceptance or calibrated prose-quality measure.',
        double_counting='S5 only. Prior longitudinal g-formula/gradient/remainder, S4 assignment framing, earlier software/CLI/MCP catalogs and generic Bellman/concentration/resource principles receive no duplicate credit.',
        reviewed_reader=report['pdf'],accepted_chapter=ref(build.CHAPTER,'Accepted preserving successor; initial logical draft stays archived'),findings=findings,
        topic_coverage=['Discrete restricted horizon and sharp tails','Survivor selection and ordered first events',
            'Natural-action identification and noninjective/singular policies','Fixed-map LMTP influence components',
            'Selected six-package longitudinal semantics','Joint event reward covariance and coupling',
            'Occupied-history transition error and validation transport','Conditional finite reference-row validation and horizon costs'],
        followups_not_awarded=['Seventeen-page planning target','Complete software census and dependency rights',
            'Actual package/adapter qualification','Estimated-occupancy/dependent observational validation',
            'Independent acceptance, bank truth and actual costs','Q1/Q5 and rendered visual acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader review')],
        limitations=LIMITS,visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S5',['Connected banking argument develops the allocated longitudinal/survival questions with notation, assumptions, proofs, diagnostics, alternatives and proposed software routes.',
            'Audited originals and exact authored laws support bounded proposal findings with process records outside the narrative.']),
        ('TEXT.REVIEW.S5',['Author topic, source, mathematics, context and equation review passes; the initial depth failure and all frozen candidate evidence remain preserved.',
            '14.25 exclusive substantive page equivalents meet minimum14; target17 remains unmet with no allocation exception.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
            limitations=LIMITS,outputs=[ref(ROOT/p,'Contracted output') for p in node['outputs']],
            nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(REVIEW,'Exclusive S5 depth review')])
                      for i,f in enumerate(facts)])
        if identifier.startswith('TEXT.DRAFT'):
            receipt['outputs'][0]['anchor']='Preserved initial logical draft; corrected accepted source is the separately bound successor'
            receipt['accepted_successor']=ref(build.CHAPTER,'Corrected source compiled in the reviewed939-page reader')
            receipt['logical_output_disposition']='Preserve hash-bound initial draft and its failure. Acceptance refers to the explicit versioned successor and reviewed reader, not the initial source defects.'
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
        planning_target_met=False,reader_pages=939,visual_acceptance=False)))


if __name__=='__main__':main()
