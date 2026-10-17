#!/usr/bin/env python3
"""Review the precise S8 reader, retaining both failed depth candidates."""
import json
from pathlib import Path
import re

import build_s8_reader_v3_20261017 as build
import prepare_s8_20261017 as work
import master_control as core
import run_program as run
from review_s3_20261017 import preserve,contexts
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEW=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S8/chapter-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=work.LIMITS+[
    'Both initial6.25-page and second9.25-page exclusive-depth failures remain preserved.',
    'Known-batch residency, online LRU and worst-support deadlines use different information and objectives.',
    'Cold-recovery readiness assumes a common validation gate; it does not describe interruption of an already loaded engine.',
    'A scoped S8 chapter review does not close the full commercial census, mandatory repairs, Q1/Q5 or overall proposal acceptance.'
]


def read(p):return json.loads(p.read_text())


def main():
    report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
    for p in [OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json',BASE/'prepared-inputs.json',
              BASE/'extension-author-review.json',build.previous.BASE/'extension-author-review.json',
              work.BASE/'primary-review.json',work.BASE/'precompile-author-review.json',
              work.BASE/'depth-review-initial.json',work.BASE/'depth-review-v2.json']:
        verify_bindings(read(p))
    build.verify_exact()
    assert report['cited_records']==726 and report['pages']>997
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==188
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['empty_pages'] and not layout['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.CHAPTER.read_text()==build.expected_chapter() and build.DRIVER.read_text()==build.expected_driver()
    assert build.CHAPTER.read_text().replace('\n'+build.INSERT,'')==build.previous.CHAPTER.read_text()
    kept=preserve(audit,index,work.PRIOR.parent.parent,721,[str(build.CANONICAL_OLD.relative_to(ROOT))])
    new={s['integrated_citation_key']:s for s in audit['sources']}
    for p,count in [(build.previous.previous.OUT/'source-audit.json',724),(build.PRIOR,725)]:
        old=read(p)['sources'];assert len(old)==count and all(new[s['integrated_citation_key']]==s for s in old)
    current=contexts(index)
    for prior,chapter in [(build.previous.previous.BASE,build.previous.previous.CHAPTER),
                          (build.previous.BASE,build.previous.CHAPTER)]:
        old=contexts(read(prior/'traceability-review.json'),str(chapter.relative_to(ROOT)))
        for key,vals in old.items():assert not vals-current[key],key
    # Audit changed chapter windows directly; do not claim byte-identical windows
    # after the explicitly preserved text repairs and inserted source inputs.
    tex=build.CHAPTER.read_text();expected={}
    for m in re.finditer(build.engine.shared.CITE,tex):
        for key in m.group(1).split(','):
            expected.setdefault(key.strip(),[]).append(dict(path=str(build.CHAPTER.relative_to(ROOT)),
                line=tex.count('\n',0,m.start())+1,context=tex[max(0,m.start()-550):m.end()+220]))
    found={r['citation_key']:[x for x in r['citation_contexts'] if x['path']==str(build.CHAPTER.relative_to(ROOT))]
           for r in index['records']}
    assert {k:v for k,v in found.items() if v}==expected
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    first=next(i for i,p in enumerate(pages) if 'Chapter 25\n' in p)
    stop=next(i for i,p in enumerate(pages) if 'Chapter 26\n' in p)
    body=''.join(pages[first:stop]);assert '??' not in body
    assert all('(25.'+str(n)+')' in body for n in range(1,24))
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations=dict(re.findall(r'\\newlabel\{(exec17:s8[^}]+)\}\{\{(25\.[0-9]+)\}\{[^\n]*?\{equation\.',aux))
    assert equations['exec17:s8-common-recovery']=='25.13'
    assert equations['exec17:s8-signal-value']=='25.23'
    measured=read(BASE/'depth-assessment.json');verify_bindings(measured)
    rows=measured['per_page'];credit=sum(r['credit'] for r in rows)
    assert measured['reviewed_reader']['sha256']==report['pdf']['sha256']
    assert measured['substantive_page_credit']==credit and 10<=credit<=15
    assert [r['pdf_page'] for r in rows]==list(range(first+1,stop+1))
    for r in rows:assert re.search(r'\b'+str(r['printed_page'])+r'\b',pages[r['pdf_page']-1])
    limits=LIMITS+[f'{credit} exclusive page equivalents meet minimum10; planning target12 '+('met.' if credit>=12 else 'unmet.')]
    paths=[(OUT/'build-report.json','Exact successor and clean material warnings'),
           (OUT/'source-audit.json','726 audited records and188 genuine scholarly PDFs'),
           (BASE/'traceability-review.json','Exact source identities and citation windows'),
           (OUT/'text-layout-review.json','All-page text bounds, not visual acceptance'),
           (OUT/'reader.txt','Chapter25 extracted text and equations25.1-25.23'),
           (BASE/'depth-assessment.json','Conservative exclusive per-page author assessment'),
           (build.CHAPTER,'Preserving commercial chapter'),
           (work.BASE/'primary-review.json','Eighteen primary-text excerpts with exact versions and limits'),
           (work.BASE/'exact-results.json','Exact cost, signal, utility and schedule references'),
           (work.BASE/'mathematics-review.json','Distinct finite author checks'),
           (work.BASE/'prototype-design.json','Prospective admission cases, no vendor run'),
           (work.BASE/'omissions.json','Scoped unknown originals, edition parity, rights and prices'),
           (work.BASE/'depth-review-initial.json','Preserved6.25-page and typography failure'),
           (work.BASE/'depth-review-v2.json','Preserved9.25-page depth failure'),
           (build.previous.extension.BASE/'mathematics-review.json','Recurrence and exhaustive729-sequence reference'),
           (build.extension.BASE/'mathematics-review.json','Cold-recovery finite joint-event reference'),
           (ROOT/'docs/program/comprehensive-v14/gap-audit.json','S8 allocation10/12/15'),
           (Path(__file__),'Exact-reader review procedure')]
    evidence=[ref(p,a) for p,a in paths]
    evidence += [ref(p,'Earlier allocation inspected for duplicate credit') for p in
                 sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json')) if p!=REVIEW]
    findings=[
        'Four banking purchasing units distinguish documented vendor capability, local dispatcher limits and proposed behavior across a17-area map.',
        'Source-specific graph, effective-model, information-parent, user/instance, residency, upgrade and retirement consequences are developed.',
        'All721 canonical records, compiled sources and citation-context multisets survive; all724 initial and725 second-candidate records are unchanged.',
        'Exact laws reproduce; no paid vendor engine or new upstream package trial is inferred.',
        'Full-choice compatibility test value7250 is conditional; at15000 cost it has negative net value. Utility policy indices change feasible value5 to0 when history is late.',
        'Known-batch, expected-workload and worst-deadline criteria choose different capacities. Shared validation can make a99-percent cold-recovery target unattainable regardless of replica count.',
        f'Exclusive credit{credit} meets minimum10; initial failures are retained. All23 displayed equations resolve and no material compilation warnings remain.',
        'Visual acceptance, exhaustive commercial coverage, rights/prices/runtime parity, mandatory repairs, Q1/Q5 and final proposal acceptance remain open.']
    scope='Author S8 source, mathematical and exclusive-depth review; proposal only'
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,reviewer=REVIEWER,
        reviewed_reader=report['pdf'],findings=findings,evidence=evidence,canonical_records_preserved=721,
        initial_records_preserved=724,second_candidate_records_preserved=725,
        canonical_compiled_sources_preserved=kept,canonical_context_multisets_retained=True,
        changed_chapter_windows='Explicit repairs and inserted inputs recomputed exactly.',
        equation_numbers=equations,limitations=limits,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S8',status='pass',scope=scope,reviewer=REVIEWER,
        allocated_title='Commercial products and the competitive capability gap',allocation=dict(min=10,target=12,max=15),
        substantive_page_credit=credit,new_synthesis_span=dict(first_printed_page=rows[0]['printed_page'],
            last_printed_page=rows[-1]['printed_page'],first_pdf_page=first+1,last_pdf_page=stop,pages=stop-first),
        per_page=rows,allocation_minimum_met=True,planning_target_met=credit>=12,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted text and source mathematics; visual acceptance false.',
        double_counting='S8 only. Inherited catalogs, generic economics, method theory, interface lists and repeated protocol framing excluded.',
        reviewed_reader=report['pdf'],accepted_chapter=ref(build.CHAPTER,'Preserving accepted successor'),
        findings=findings,topic_coverage=['Four target/edition/deployment buying units','17-area commercial map and omissions',
            'Information-parent utility and feasible policy','Rights, upgrades and retirement','Loaded-instance schedules',
            'Known-batch versus online residency','Workload, deadline and capacity price','Shared validation and cold recovery',
            'Matched-route cost, regret and quote ceiling','Complete-choice compatibility information value'],
        followups_not_awarded=['Full commercial census and exact edition parity','Binding rights/prices/support',
                              'Actual vendor and bank trials','Visual and independent review','Q1/Q5 and final proposal acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader review')],limitations=limits,
        visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S8',['Connected commercial acquisition argument develops purchasing units, source-specific alternatives, assumptions and banking consequences.',
                          'Audited originals and reproduced exact laws support scoped proposal claims; process records remain outside the manuscript.']),
        ('TEXT.REVIEW.S8',['Source, mathematics, equation, preservation and topic review passes with explicit omissions and retained failures.',
                           f'{credit} exclusive page equivalents meet minimum10 without duplicate catalog, economics or adjacent-chapter credit.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
            outputs=[ref(ROOT/p,'Contracted logical output') for p in node['outputs']],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(REVIEW,'Exclusive S8 review')]) for i,f in enumerate(facts)])
        if identifier.startswith('TEXT.DRAFT'):
            receipt.update(accepted_successor=ref(build.CHAPTER,'Accepted source in exact successor reader'),
                logical_output_disposition='Preserve original draft and failures; acceptance refers to explicit reviewed successor.')
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
                          reader_pages=report['pages'],visual_acceptance=False)))


if __name__=='__main__':main()
