#!/usr/bin/env python3
"""Review the preserving S6 successor against its exact evidence and allocation."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_s6_reader_v2_20261017 as build
import prepare_s6_20261017 as work
import s6_depth_extension_20261017 as extension
import master_control as core
import run_program as run
from review_s3_20261017 import contexts, preserve
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S6/chapter-review.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = work.LIMITS + [
    '14.75 exclusive substantive page equivalents meet minimum14; planning target17 remains unmet.',
    'The initial10.25-page failure and unpublished957-page candidate remain preserved.',
    'Joint weights solve a known-factor, independent-cell oracle law; this does not qualify weights learned from noisy data.',
    'The controller beta[1,2] range is supplied sensitivity information, not an empirically identified or confidence region.',
    'Feedback replacement assumes a common nonzero initial state, structural invariance, feasible actions and stipulated monetary inputs.'
]


def read(path):
    return json.loads(path.read_text())


def copied_contexts(index):
    old = contexts(read(build.previous.BASE/'traceability-review.json'),
                   str(build.previous.CHAPTER.relative_to(ROOT)))
    current = contexts(index)
    for key, values in old.items():
        assert not values-current[key], key
    expected = {}
    tex = build.expected_chapter()
    for match in re.finditer(shared.CITE, tex):
        for key in match.group(1).split(','):
            expected.setdefault(key.strip(), []).append(dict(
                path=str(build.CHAPTER.relative_to(ROOT)),
                line=tex.count('\n', 0, match.start())+1,
                context=tex[max(0, match.start()-550):match.end()+220]))
    found = {row['citation_key']:[x for x in row['citation_contexts']
             if x['path']==str(build.CHAPTER.relative_to(ROOT))]
             for row in index['records']}
    assert {key:value for key,value in found.items() if value} == expected


def main():
    report=read(OUT/'build-report.json'); audit=read(OUT/'source-audit.json')
    index=read(BASE/'traceability-review.json')
    paths=[OUT/'build-report.json', OUT/'source-audit.json', BASE/'traceability-review.json',
           BASE/'prepared-inputs.json', BASE/'extension-author-review.json',
           build.previous.BASE/'copy-author-review.json', work.BASE/'primary-review.json',
           work.BASE/'precompile-author-review.json', work.BASE/'depth-review-initial.json',
           extension.BASE/'mathematics-review.json']
    for path in paths:
        verify_bindings(read(path))
    build.previous.verify_exact()
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    assert report['pages']==963 and report['cited_records']==717
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==188
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.CHAPTER.read_text()==build.expected_chapter()
    assert build.CHAPTER.read_text().replace(build.INSERT+'\n\n','')==build.previous.CHAPTER.read_text()
    canonical=work.PRIOR.parent.parent
    kept_canonical=preserve(audit,index,canonical,712,
                           [str(build.CANONICAL_OLD.relative_to(ROOT))])
    prior=read(build.PRIOR)
    old={row['integrated_citation_key']:row for row in prior['sources']}
    new={row['integrated_citation_key']:row for row in audit['sources']}
    assert len(old)==716 and all(new[key]==row for key,row in old.items())
    replaced={str(build.OLD.relative_to(ROOT)),str(build.previous.CHAPTER.relative_to(ROOT))}
    files={row['path']:row for row in audit['tex_files']}
    kept=[row for row in prior['tex_files'] if row['path'] not in replaced]
    assert all(files[row['path']]['sha256']==row['sha256'] for row in kept)
    copied_contexts(index)
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations=dict(re.findall(r'\\newlabel\{(exec17:s6[^}]+)\}\{\{(23\.[0-9]+)\}\{[^\n]*?\{equation\.',aux))
    assert set(equations.values())=={'23.'+str(n) for n in range(1,63)}
    assert equations['exec17:s6-joint-certificate']=='23.47'
    assert equations['exec17:s6-full-tail']=='23.62'
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    chapter=''.join(pages[256:279])
    assert all('('+str('23.'+str(n))+')' in chapter for n in range(1,63))
    assert '??' not in chapter
    assert 'Chapter 24' in pages[279] and 'Conclusion' in pages[278]
    initial=read(work.BASE/'depth-review-initial.json')
    per_page=[dict(row) for row in initial['per_page'][:-1]]
    assert sum(row['credit'] for row in per_page)==10.25
    additions=[
        (.5,'New nine-cell joint target, contrast, bias/noise risk and conditional optimum; preceding interface prose and generic optimization introduction excluded.'),
        (.75,'Exact global sum-of-squares certificate, attainable real roots and unique boundary solution; generic square-completion explanation discounted.'),
        (.5,'Strict constrained optimum and same-law exact-balance comparisons; repeated checks, prototype framing and controller introduction excluded.'),
        (.75,'Old-law-equivalent continuous structural class, common occupied state and full paired action-cost value; generic geometric-series algebra discounted.'),
        (.75,'Robust stability versus quadratic-cost boundary, adverse divergence witness and conditional infinite value; generic convergence framing discounted.'),
        (.75,'Uniform derivative bounds prove finite and infinite adverse worlds; exact same-state/different-action expense and horizon-dependent monetary decisions.'),
        (.5,'Four-term paired-regime tail, uniform dollar envelope and direct two-regime recursion; general information-acquisition prose and conclusion excluded.')]
    for offset,(credit,rationale) in enumerate(additions):
        per_page.append(dict(printed_page=252+offset,pdf_page=273+offset,
                             credit=credit,rationale=rationale))
    for row in per_page:
        assert re.search(r'\b'+str(row['printed_page'])+r'\b',pages[row['pdf_page']-1])
    credit=sum(row['credit'] for row in per_page); assert credit==14.75
    prior_reviews=sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    evidence=[ref(path,anchor) for path,anchor in [
        (OUT/'build-report.json','Exact963-page preserving reader; no material compile warnings'),
        (OUT/'source-audit.json','717 audited records;188 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Exact-driver identities and inspected citation contexts'),
        (OUT/'text-layout-review.json','All-page extracted-text bounds; not visual acceptance'),
        (OUT/'reader.txt','Printed236-258/physical257-279 and next chapter boundary inspected'),
        (build.CHAPTER,'Byte-recoverable preserving chapter'),
        (build.EXTENSION,'Global joint weights and complete feedback-controller replacement'),
        (work.BASE/'plan.md','Reviewed14/17/20 allocation and duplicate exclusions'),
        (work.BASE/'primary-review.json','Eleven inspected primary-paper/software excerpts'),
        (work.BASE/'exact-results.json','Exact event-study, curvature, factor and feedback references'),
        (work.BASE/'mathematics-review.json','Separate original author checks'),
        (work.BASE/'robust-results.json','Signed-contamination and finite-calendar exact references'),
        (work.BASE/'robust-mathematics-review.json','Separate support and covariance checks'),
        (work.BASE/'value-checks/exact-results.json','Action paths and geometric value/tail references'),
        (work.BASE/'value-checks/mathematics-review.json','Separate direct-recursion checks'),
        (build.previous.BASE/'copy-author-review.json','Preserved C>0 and28-period corrections'),
        (work.BASE/'depth-review-initial.json','Preserved10.25-page exclusive-depth failure'),
        (work.BASE/'depth-extension-plan.md','Reviewed substantive depth repair'),
        (extension.BASE/'exact-results.json','Exact risks, full-controller values and uniform tails'),
        (extension.BASE/'mathematics-review.json','512-sign checks, polynomial certificate and direct structural recursions'),
        (ROOT/'tools/s6_depth_extension_20261017.py','Reproducible reference and distinct author checks'),
        (work.BASE/'prototype-design.json','Proposed common-target comparison; no package execution'),
        (ROOT/'docs/program/comprehensive-v14/gap-audit.json','Exclusive S6 allocation14/17/20'),
        (Path(__file__),'Source, mathematics, contexts and conservative depth review')]]
    evidence += [ref(path,'Prior chapter allocation checked for duplicate credit') for path in prior_reviews]
    scope='Author S6 subject, primary-source, mathematics and exclusive-depth review; proposal development only'
    findings=[
        'Develops false event-study leads, sharp target-specific trend budgets, signed donor risk, unit/calendar balance, dependent-calendar uncertainty and intervention-specific feedback values.',
        'Eleven primary excerpts and exact authored laws reproduce; the selected software paths and prototype remain proposed rather than runtime-qualified.',
        'All712 canonical records and citation-context multisets survive. All716 initial-candidate source records remain unchanged; nonchapter contexts survive and copied windows are recomputed exactly.',
        'Equations23.1-23.62 resolve, the copied chapter is byte-recoverable, chapter boundaries agree and all-page text bounds pass.',
        '14.75 exclusive substantive page equivalents meet minimum14; planning target17 remains unmet. Repeated catalogs, interface/prototype prose and generic control/optimization principles receive no duplicate credit.',
        'Joint oracle risk at s1/8 is1, compared with1.5 for nonnegative weights and4.5 for exact matching on both axes. The global certificate concerns fixed known-factor weights.',
        'Within the supplied beta[1,2] class, rule.44 has52.7002USD worst infinite value but-5.4812USD through index20; rule.47 has convergent benefits but adverse divergent costs. The H80 uniform four-term tail bound is4.3531689459USD.',
        'The initial depth failure and corrected4.36USD tail assertion remain preserved. Q1/Q5, the three mandatory repairs, visual acceptance, independent review and bank/product qualification remain open.']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,
        reviewer=REVIEWER,reviewed_reader=report['pdf'],findings=findings,evidence=evidence,
        canonical_records_preserved=712,initial_records_preserved=716,
        canonical_compiled_sources_preserved=kept_canonical,initial_unmodified_compiled_sources_preserved=len(kept),
        canonical_context_multisets_retained=True,initial_nonchapter_contexts_retained=True,
        initial_chapter_contexts_byte_identical=False,
        context_change='Preserving path copy plus single inserted input; regenerated exact citation windows match.',
        equation_numbers=equations,limitations=LIMITS,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S6',status='pass',scope=scope,reviewer=REVIEWER,
        allocated_title='Panel, synthetic-control and time-series software',
        allocation=dict(min=14,target=17,max=20),substantive_page_credit=credit,
        new_synthesis_span=dict(first_printed_page=236,last_printed_page=258,
            first_pdf_page=257,last_pdf_page=279,pages=23),per_page=per_page,
        allocation_minimum_met=True,planning_target_met=False,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; no visual acceptance or calibrated prose-quality measure.',
        double_counting='S6 only. Inherited generic DiD, donor balance, dynamic-panel/temporal discovery, prior sensitivity, catalogs, interfaces and prototype design receive no duplicate credit.',
        reviewed_reader=report['pdf'],accepted_chapter=ref(build.CHAPTER,'Accepted preserving successor; initial logical draft stays archived'),
        findings=findings,topic_coverage=['Event-study heterogeneity contamination','Sharp horizon-specific curvature sensitivity',
            'Signed donor contamination and bias/noise risk','Joint unit/time global optimization',
            'Signed dependent-calendar covariance','Feedback intervention and whole-controller values',
            'Stability, squared-cost convergence and uniform monetary tails','Selected original software routes'],
        followups_not_awarded=['Seventeen-page planning target','Complete software census and dependency rights',
            'Fitted-weight and adapter qualification','Empirically defended controller class and feasible bank costs',
            'Independent acceptance and bank truth','Q1/Q5 and rendered visual acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader review')],
        limitations=LIMITS,visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S6',['Connected banking argument develops allocated panel/time-series questions with notation, assumptions, proofs, diagnostics, alternatives and proposed software routes.',
            'Audited originals and exact authored laws support bounded proposal findings with process records outside the narrative.']),
        ('TEXT.REVIEW.S6',['Author topic, source, mathematics, contexts and equation review passes; initial depth failure and frozen evidence remain preserved.',
            '14.75 exclusive substantive page equivalents meet minimum14; target17 remains unmet without an allocation exception.'])]:
        node=run.ledger.operation(graph,identifier); receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,
            limitations=LIMITS,outputs=[ref(ROOT/path,'Contracted output') for path in node['outputs']],
            nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=finding,evidence=evidence+[ref(REVIEW,'Exclusive S6 review')])
                      for i,finding in enumerate(facts)])
        if identifier.startswith('TEXT.DRAFT'):
            receipt['accepted_successor']=ref(build.CHAPTER,'Corrected preserving source in the reviewed963-page reader')
            receipt['logical_output_disposition']='Preserve the hash-bound original draft and findings. Acceptance refers to the explicit successor and exact reviewed reader.'
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
        planning_target_met=False,reader_pages=963,visual_acceptance=False)))


if __name__=='__main__': main()
