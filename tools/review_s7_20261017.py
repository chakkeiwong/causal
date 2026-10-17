#!/usr/bin/env python3
"""Review the recovered S7 reader, preserving the initial depth failure."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import build_s7_reader_v2_20261017 as build
import prepare_s7_20261017 as work
import s7_depth_extension_20261017 as extension
import master_control as core
import run_program as run
from review_s3_20261017 import contexts, preserve
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S7/chapter-review.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = work.LIMITS + [
    '9.25 exclusive substantive page equivalents meet minimum8 and planning target9 within maximum11.',
    'The initial7.5-page depth failure and unpublished975-page candidate remain preserved.',
    'Constraint-aware optimality concerns the common-one-quarter variance envelope, linear unbiased family and continuous allocations, not actual minimax variance or arbitrary estimators.',
    'Known pooled information is available to both incremental audit comparisons; acquisition costs are unmeasured.',
    'A noisy pool requires its own variance, covariance and joint probability argument; fixed bias is not removed by more stratum audits.'
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
    for path in [OUT/'build-report.json', OUT/'source-audit.json', BASE/'traceability-review.json',
                 BASE/'prepared-inputs.json', BASE/'extension-author-review.json',
                 work.BASE/'primary-review.json', work.BASE/'precompile-author-review.json',
                 work.BASE/'depth-review-initial.json', extension.BASE/'mathematics-review.json']:
        verify_bindings(read(path))
    build.previous.verify_exact()
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    assert report['pages']==977 and report['cited_records']==721
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==188
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    assert build.CHAPTER.read_text()==build.expected_chapter()
    assert build.CHAPTER.read_text().replace(build.INSERT+'\n\n','')==build.previous.CHAPTER.read_text()
    canonical=work.PRIOR.parent.parent
    kept_canonical=preserve(audit,index,canonical,717,
                           [str(build.CANONICAL_OLD.relative_to(ROOT))])
    prior=read(build.PRIOR)
    old={row['integrated_citation_key']:row for row in prior['sources']}
    new={row['integrated_citation_key']:row for row in audit['sources']}
    assert len(old)==720 and all(new[key]==row for key,row in old.items())
    replaced={str(build.OLD.relative_to(ROOT)),str(build.previous.CHAPTER.relative_to(ROOT))}
    files={row['path']:row for row in audit['tex_files']}
    kept=[row for row in prior['tex_files'] if row['path'] not in replaced]
    assert all(files[row['path']]['sha256']==row['sha256'] for row in kept)
    copied_contexts(index)
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations=dict(re.findall(r'\\newlabel\{(exec17:s7[^}]+)\}\{\{(24\.[0-9]+)\}\{[^\n]*?\{equation\.',aux))
    assert set(equations.values())=={'24.'+str(n) for n in range(1,34)}
    assert equations['exec17:s7-constrained-estimator']=='24.23'
    assert equations['exec17:s7-noisy-envelope']=='24.33'
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    chapter=''.join(pages[279:293])
    assert all('(24.'+str(n)+')' in chapter for n in range(1,34))
    assert '??' not in chapter
    assert 'Chapter 25' in pages[293] and 'Conclusion' in pages[292]
    initial=read(work.BASE/'depth-review-initial.json')
    per_page=[dict(row) for row in initial['per_page'][:-1]]
    assert sum(row['credit'] for row in per_page)==7.5
    additions=[
        (.5,'Constraint-compatible estimator family, unbiasedness and actual-versus-envelope variance; preceding repeated benchmark prose excluded.'),
        (.75,'Global coefficient/budget inequality, price-nine transition, boundary designs, exact matched comparisons and feasible projection; generic Cauchy-Schwarz explanation discounted.'),
        (.5,'Noisy-pool value/error identity, covariance from reused labels and simultaneous monetary propagation; acquisition framing and conclusion excluded.')]
    for offset,(credit,rationale) in enumerate(additions):
        per_page.append(dict(printed_page=270+offset,pdf_page=291+offset,
                             credit=credit,rationale=rationale))
    for row in per_page:
        assert re.search(r'\b'+str(row['printed_page'])+r'\b',pages[row['pdf_page']-1])
    credit=sum(row['credit'] for row in per_page); assert credit==9.25
    prior_reviews=sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    evidence=[ref(path,anchor) for path,anchor in [
        (OUT/'build-report.json','Exact977-page reader; no material compilation warnings'),
        (OUT/'source-audit.json','721 audited records;188 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Exact-driver identities and citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds; not rendered visual acceptance'),
        (OUT/'reader.txt','Printed259-272/physical280-293 and next chapter boundary inspected'),
        (build.CHAPTER,'Byte-recoverable preserving chapter'),
        (build.EXTENSION,'Constraint-aware global envelope design and noisy-pool propagation'),
        (work.BASE/'plan.md','Reviewed8/9/11 allocation and duplicate exclusions'),
        (work.BASE/'primary-review.json','Ten authentic primary-text excerpts'),
        (work.BASE/'exact-results.json','Exact graph/action, topology, transport and audit references'),
        (work.BASE/'mathematics-review.json','Distinct original author checks'),
        (work.BASE/'depth-review-initial.json','Preserved7.5-page exclusive-depth failure'),
        (work.BASE/'depth-extension-plan.md','Reviewed substantive depth repair'),
        (extension.BASE/'exact-results.json','Coefficient, global design, budget and covariance references'),
        (extension.BASE/'mathematics-review.json','Separate symbolic and twelve finite Bernoulli audit-law checks'),
        (ROOT/'tools/s7_examples_20261017.py','Reproducible original mathematical references'),
        (ROOT/'tools/s7_depth_extension_20261017.py','Reproducible depth extension and separate checks'),
        (work.BASE/'prototype-design.json','Prospective public/generated study; not executed'),
        (ROOT/'docs/program/comprehensive-v14/gap-audit.json','S7 allocation8/9/11'),
        (Path(__file__),'Exact-reader source, mathematics and exclusive-depth author review')]]
    evidence += [ref(path,'Prior allocation inspected for duplicate credit') for path in prior_reviews]
    scope='Author S7 source, mathematics and exclusive-depth review; proposal development only'
    findings=[
        'Develops joint relationship/action meaning, feasible coordination, topology transport, pooled-information sharp bounds and target-specific audit design.',
        'All717 canonical source records and citation-context multisets survive; all720 first-candidate records are unchanged.721 records cite188 genuine scholarly PDFs.',
        'Removing the single inserted input recovers every byte of the initial draft; changed chapter paths/windows match explicit recomputation.',
        'Equations24.1-24.33 resolve and all-page text bounds pass; ten primary excerpts retain version, scientific and cutoff limits.',
        '9.25 exclusive substantive page equivalents meet minimum8 and target9 within maximum11; repeated catalogs, generic theory, interfaces and prototype framing receive no duplicate credit.',
        'Separate edge margins leave value[-8,8]; matched coordinated actions can remove the overlap parameter. Pooled information yields sharp target[-10/3,58/3].473 truthful independent joint audits suffice for the declared prospective sign condition.',
        'Constraint-aware envelope optimum4624*min(c0,c1/9)/C uses a single stratum away from the price-ratio-nine tie. Equal-count700 gives1156/1575 versus28/25; budget1820 at prices(1,4) gives4624/4095 versus52/35. This is an envelope comparison, not actual minimax or empirical improvement.',
        'Noisy pooled information adds variance and8704/9 times covariance; joint error radii propagate with coefficients32/3 and136/3. Fixed pool bias persists with more stratum audits.',
        'The initial depth failure remains preserved. Q1/Q5, all three mandatory repairs, visual review, independent review and bank/product qualification remain open.']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,
        reviewer=REVIEWER,reviewed_reader=report['pdf'],findings=findings,evidence=evidence,
        canonical_records_preserved=717,initial_records_preserved=720,
        canonical_compiled_sources_preserved=kept_canonical,initial_unmodified_compiled_sources_preserved=len(kept),
        canonical_context_multisets_retained=True,initial_nonchapter_contexts_retained=True,
        initial_chapter_contexts_byte_identical=False,
        context_change='Preserving path copy plus one inserted input; regenerated exact citation windows match.',
        equation_numbers=equations,limitations=LIMITS,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S7',status='pass',scope=scope,reviewer=REVIEWER,
        allocated_title='Observation, sensitivity, transport and network software',
        allocation=dict(min=8,target=9,max=11),substantive_page_credit=credit,
        new_synthesis_span=dict(first_printed_page=259,last_printed_page=272,
            first_pdf_page=280,last_pdf_page=293,pages=14),per_page=per_page,
        allocation_minimum_met=True,planning_target_met=True,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; no visual acceptance or calibrated prose-quality measure.',
        double_counting='S7 only. Inherited missingness/linkage, generic sensitivity/transport, network catalogs, generic allocation inequalities, interfaces and prototype framing receive no duplicate credit.',
        reviewed_reader=report['pdf'],accepted_chapter=ref(build.CHAPTER,'Accepted preserving successor; initial logical draft archived'),
        findings=findings,topic_coverage=['Relationship versus identity versus influence',
            'Joint graph and feasible action laws','Topology, support and conditional transport',
            'Sharp pooled-moment value sets','Completion versus sampling versus numerical uncertainty',
            'Truthful joint audit design','Target-weighted and price-constrained audits',
            'Constraint-aware global envelope design','Noisy-pool covariance and systematic error',
            'Source-specific compatible software routes'],
        followups_not_awarded=['Complete software census and dependency rights',
            'Actual minimax audit design beyond the common variance relaxation',
            'Estimated-pool joint design and empirical calibration','Package runtime qualification',
            'Owned bank influence, feasible actions, truthful audits, prices and accepted loss',
            'Independent acceptance, Q1/Q5 and rendered visual review'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader author review')],
        limitations=LIMITS,visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S7',['Connected banking argument develops allocated observation/transport/network questions with notation, assumptions, derivations, diagnostics, alternatives and conditional software routes.',
            'Audited originals and reproduced exact laws support bounded proposal findings, with process records outside the manuscript.']),
        ('TEXT.REVIEW.S7',['Author topic, primary-source, mathematics, context and equation review passes; initial depth failure and frozen evidence remain preserved.',
            '9.25 exclusive substantive page equivalents meet minimum8 and target9 within maximum11 without an allocation exception.'])]:
        node=run.ledger.operation(graph,identifier); receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,
            limitations=LIMITS,outputs=[ref(ROOT/path,'Contracted output') for path in node['outputs']],
            nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=finding,evidence=evidence+[ref(REVIEW,'Exclusive S7 review')])
                      for i,finding in enumerate(facts)])
        if identifier.startswith('TEXT.DRAFT'):
            receipt['accepted_successor']=ref(build.CHAPTER,'Preserving source in the reviewed977-page reader')
            receipt['logical_output_disposition']='Preserve the hash-bound original draft and failure. Acceptance refers to the explicit successor and exact reader.'
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
        planning_target_met=True,reader_pages=977,visual_acceptance=False)))


if __name__=='__main__': main()
