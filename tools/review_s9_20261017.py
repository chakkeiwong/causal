#!/usr/bin/env python3
"""Exact-reader review; no acceptance without measured exclusive depth."""
import json
import re
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import s9_successor_v4_20261017 as build
import master_control as core
import run_program as run
from review_s3_20261017 import preserve,contexts
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.PUB,build.OUT
REVIEW=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S9/chapter-review.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=[
    'Proposal-only author review; no upstream engine, cross-language implementation or bank trial is qualified.',
    'Numerical domains, Lipschitz constants, conditional kernels and failure laws require independent implementation evidence.',
    'Retained-result and redraw retry schemes have different laws; completed-only reports do not establish all-assigned behavior.',
    'Inverse selection requires the correct positive completion law and a finite second moment; it does not reproduce the entire output law.',
    'Primary-source review covers bounded source decisions, not complete license/dependency closure or historical cutoff bytes.',
    'All three failed-depth S9 candidates remain preserved; catalogs and earlier shared-control/interface theory receive no duplicate credit.',
    'Visual acceptance remains false under the inherited image allowance. Q1/Q5, mandatory repairs and overall proposal acceptance remain open.']


def read(p):return json.loads(p.read_text())


def main():
    build.verify_exact()
    report=read(OUT/'build-report.json');audit=read(OUT/'source-audit.json');index=read(BASE/'traceability-review.json')
    for p in [OUT/'build-report.json',OUT/'source-audit.json',BASE/'traceability-review.json',BASE/'prepared-inputs.json',
              BASE/'mathematics-review.json',BASE/'primary-source-review-successor.json',BASE/'additional-algebra-review.json']:
        verify_bindings(read(p))
    assert report['cited_records']==731 and index['scholarly_pdfs']==188
    assert index['status']=='pass' and not index['issues']
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['empty_pages'] and not layout['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    kept=preserve(audit,index,build.CANONICAL,726,[str(build.CANONICAL_OLD.relative_to(ROOT))])
    new={s['integrated_citation_key']:s for s in audit['sources']}
    old=read(build.PRIOR)['sources'];assert len(old)==730 and all(new[s['integrated_citation_key']]==s for s in old)
    current=contexts(index)
    prior=contexts(read(build.PREVIOUS/'traceability-review.json'),str((build.PREVIOUS/'chapter.tex').relative_to(ROOT)))
    for key,vals in prior.items():assert not vals-current[key],key
    previous_files=read(build.PRIOR)['tex_files'];files={r['path']:r for r in audit['tex_files']}
    excluded={str(build.OLD.relative_to(ROOT)),str((build.PREVIOUS/'chapter.tex').relative_to(ROOT))}
    for r in previous_files:
        if r['path'] not in excluded:assert files[r['path']]['sha256']==r['sha256']
    tex=build.CHAPTER.read_text();expected={}
    for m in re.finditer(build.engine.shared.CITE,tex):
        for key in m.group(1).split(','):
            expected.setdefault(key.strip(),[]).append(dict(path=str(build.CHAPTER.relative_to(ROOT)),
                line=tex.count('\n',0,m.start())+1,context=tex[max(0,m.start()-550):m.end()+220]))
    found={r['citation_key']:[x for x in r['citation_contexts'] if x['path']==str(build.CHAPTER.relative_to(ROOT))] for r in index['records']}
    assert {k:v for k,v in found.items() if v}==expected
    for k in range(2,7):
        for q0,q1 in product([F(0),F(1,4),F(1,2),F(3,4),F(1)],repeat=2):
            assert ((1-q0)**k+(1-q1)**k)/2 >= (1-(q0+q1)/2)**k
    r=F(23,32);mu=F(9,23);assert (r*mu-(1-r),r*mu+(1-r))==(0,F(9,16))
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    first=next(i for i,p in enumerate(pages) if 'Chapter 26\n' in p)
    stop=next(i for i,p in enumerate(pages) if 'Chapter 27\n' in p)
    body=''.join(pages[first:stop]);assert '??' not in body
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations=dict(re.findall(r'\\newlabel\{(exec17:s9[^}]+)\}\{\{(26\.[0-9]+)\}\{[^\n]*?\{equation\.',aux))
    assert len(equations)==19,len(equations)
    assert all('(26.'+str(n)+')' in body for n in range(1,20))
    measured=read(BASE/'depth-assessment.json');verify_bindings(measured)
    rows=measured['per_page'];credit=sum(r['credit'] for r in rows)
    assert measured['reviewed_reader']['sha256']==report['pdf']['sha256']
    assert measured['substantive_page_credit']==credit and 6<=credit<=10
    assert [r['pdf_page'] for r in rows]==list(range(first+1,stop+1))
    assert len(rows)==stop-first
    limits=LIMITS+[f'{credit} exclusive page equivalents meet minimum6; planning target8 '+('met.' if credit>=8 else 'unmet.')]
    paths=[(OUT/'build-report.json','Exact reader and compilation'),(OUT/'source-audit.json','731 records and188 genuine scholarly PDFs'),
           (BASE/'traceability-review.json','Exact citation windows'),(OUT/'text-layout-review.json','All-page bounds; not visual acceptance'),
           (OUT/'reader.txt','Chapter26 extracted text and equations'),(BASE/'depth-assessment.json','Conservative exclusive depth'),
           (build.CHAPTER,'Preserving S9 source'),(build.EXTENSION,'Composition and retry-selection derivations'),
           (BASE/'exact-results.json','Exact Fraction reference laws'),(BASE/'mathematics-review.json','Author domain and algebra review'),
           (BASE/'primary-source-review-successor.json','Fourteen corrected pointers; original records unchanged'),
           (build.BASE/'route-decisions.json','Bounded reuse decisions'),(build.BASE/'admission-protocol.json','Prospective qualification path'),
           (build.BASE/'semantic-results.json','Earlier finite references'),(Path(__file__),'Review and independent finite inequalities')]
    paths += [(build.BASE/f'publication-v{i}/exclusive-depth-failure.json','Preserved failed-depth candidate') for i in (1,2,3)]
    paths += [(ROOT/f'docs/program/comprehensive-v14/work/TEXT.DRAFT.{c}/chapter.tex','Duplicate-credit exclusion') for c in ['I1','S4','S10']]
    evidence=[ref(p,a) for p,a in paths]
    findings=[
        'Original-language reuse is scoped to pinned package profiles; a wrapper, port and independent implementation are distinguished.',
        'All726 canonical records, compiled sources and citation contexts survive; all730 v3 source records remain unchanged.',
        'v3 chapter is an exact prefix of v4; changed citation windows are recomputed and14 misleading descriptive pointers have a preserving correction.',
        'Composed numerical errors require common domains and sequential branch margins; adaptive laws require conditional kernels and retained state.',
        'Exact finite paths distinguish redraw from retained-result retries. Same expected calls11/8 gives different completion55/64 versus23/32 and returned mean3/5 versus9/23.',
        'Persistent regimes, fixed-result missingness bounds, fallback utility and selection correction have separate assumptions; corrected-score variance23/14 exceeds ideal1.',
        f'Exclusive depth{credit} meets minimum6; all19 equations and all-page bounds pass. Prior failures and actual qualification gaps remain explicit.']
    scope='Author S9 source, mathematical, preservation and exclusive-depth review; proposal only'
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,reviewer=REVIEWER,reviewed_reader=report['pdf'],
        findings=findings,evidence=evidence,canonical_records_preserved=726,previous_records_preserved=730,
        canonical_compiled_sources_preserved=kept,canonical_context_multisets_retained=True,equation_numbers=equations,
        limitations=limits,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S9',status='pass',scope=scope,reviewer=REVIEWER,
        allocated_title='R/Python/Java/C++ reuse, bridging and justified ports',allocation=dict(min=6,target=8,max=10),
        substantive_page_credit=credit,new_synthesis_span=dict(first_printed_page=rows[0]['printed_page'],last_printed_page=rows[-1]['printed_page'],
            first_pdf_page=first+1,last_pdf_page=stop,pages=stop-first),per_page=rows,allocation_minimum_met=True,
        planning_target_met=credit>=8,allocation_exception=None,measurement='Conservative author page-equivalent assessment; rendered visual acceptance false.',
        double_counting='Earlier catalogs, shared-control/action-margin theory, generic interfaces and scalar numerical budgets excluded.',
        reviewed_reader=report['pdf'],accepted_chapter=ref(build.CHAPTER,'Reviewed preserving S9 successor'),findings=findings,
        topic_coverage=['Pinned-language routes','Compositional errors and adaptive branches','Conditional joint laws',
            'Failure and retry selection','Persistent regimes','All-assigned bounds and fallback value','Selection correction and variance'],
        followups_not_awarded=['Upstream and bridge runtime qualification','Dependency and rights closure','General numerical certificates','Visual/independent/bank acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader source review')],limitations=limits,visual_acceptance=False,
        whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S9',['Connected language-reuse argument develops pinned routes, assumptions, composition, retry laws, diagnostics and banking consequences.',
                          'Audited originals and exact authored examples support bounded proposal claims; no upstream or bank execution is invented.']),
        ('TEXT.REVIEW.S9',['Source, preservation, mathematics, equation and topic review passes with explicit limitations and preserved failures.',
                           f'{credit} exclusive page equivalents meet minimum6 without duplicate I1/S4/S10 credit.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,limitations=limits,
            outputs=[ref(ROOT/p,'Contracted logical output') for p in node['outputs']],nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(REVIEW,'Exclusive S9 review')]) for i,f in enumerate(facts)])
        if identifier.startswith('TEXT.DRAFT'):
            receipt.update(accepted_successor=ref(build.CHAPTER,'Accepted exact-reader source'),logical_output_disposition='Original draft retained; acceptance refers to explicit preserving successor.')
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',review='pass',exclusive_depth=credit,pages=report['pages'],visual_acceptance=False)))


if __name__=='__main__':main()
