#!/usr/bin/env python3
"""Review S10 sources, exact derivations and conservative substantive depth."""
from collections import Counter
import json
from pathlib import Path

import build_s10_reader_20261016 as build
import prepare_s10_20261016 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEW=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S10/chapter-review.json'
LIMITS=work.LIMITS+['Four nonduplicate substantive pages meet the four-page minimum;the six-page planning target is not claimed.']


def main():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text());prior=json.loads(build.PRIOR.read_text())
    index=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,index,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'draft-author-review.json').read_text())]:verify_bindings(obj)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==175
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']};new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==639 and len(new)==641 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts']) for r in index['records']}
    for r in previous['records']:
        assert not Counter(json.dumps(x,sort_keys=True) for x in r['citation_contexts'])-contexts[r['citation_key']]
    assert work.examples.calculate()==json.loads((work.BASE/'exact-results.json').read_text())
    assert report['qualification_sections']=={'s10':353,'s10-end':359}
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    start=next(i for i,t in enumerate(pages) if i>100 and 'An admissible route before a preferred supplier' in t)
    assert start+1==372
    text=' '.join(' '.join(pages[start:start+7]).split())
    for phrase in ['0.2011','0.3931','299','505','USD 610,000','USD 690,000','not an observed package trial','independent approval']:
        assert phrase in text,phrase
    credits=[
      (.5,'Admission rule and scientific-versus-engineering classification;chapter title and repeated common-contract motivation excluded.'),
      (.5,'Method comparison versus compatibility-port objective and matched workloads;source recap,denominator/public-data and timing framing overlap S1/L7.'),
      (.75,'New joint table,discordant pairs and exact covariance derivation;conditional-availability and error-loss accounting discounted against L8/S1.'),
      (.75,'Exact zero-failure inversion and eight-profile allocation;generic registered-protocol and finite-example cautions overlap L7.'),
      (.75,'Deterministic coordinate error propagation and decision reversal;CausalPy/d3rlpy source recaps and generic port/test advice receive no new credit.'),
      (.75,'Maintenance-adjusted bridge/port threshold and scoped acquisition alternatives;generic cost,commercial and proposal recap excluded.'),
      (0,'Short continuation repeats four-journey and external-evidence limits;no new substantive credit.'),
    ]
    credit=sum(c for c,_ in credits);assert credit==4 and 4<=credit<=7
    evidence=[ref(p,a) for p,a in [
      (OUT/'build-report.json','Exact816-page qualification reader'),(OUT/'source-audit.json','641 source records'),
      (BASE/'traceability-review.json','All inherited citation contexts;175 genuine scholarly PDFs'),
      (OUT/'text-layout-review.json','All-page text bounds'),(OUT/'reader.txt','Inspected printed353-359,physical372-378'),
      (work.CHAPTER,'Connected qualification/acquisition chapter'),(work.BASE/'primary-review.json','Pinned prior sources and adjacent chapter overlap'),
      (work.BASE/'exact-results.json','Four exact authored qualification/planning families'),
      (ROOT/'tools/s10_examples_20261016.py','Exact Fraction arithmetic and zero-failure inequalities'),
      (work.BASE/'qualification-design.json','Proposed acceptance profile and route alternatives'),
      (work.BASE/'draft-author-review.json','Source/math draft review'),(work.BASE/'plan.md','Reviewed execution plan'),
      (Path(__file__),'Exact-reader and nonduplicate-depth review')]]
    findings=[
      'Admission conditions,matched scientific/operating experiment,paired comparisons,qualification limits,full-procedure ports and lifecycle alternatives are developed.',
      'Four exact authored reference families reproduce;counts,losses,costs and numerical bounds are explicitly stipulated.',
      'Pinned software findings remain source-grounded;no native trials,market census,bank ROI or independent approval inferred.',
      '639 inherited source records and all citation contexts retained;two project additions yield641 records and175 genuine scholarly PDFs.',
      'Four nonduplicate substantive pages across seven physical pages meet4/6/7 allocation minimum;target6 remains unmet;no exception or duplicate credit.',
    ]
    scope='Author review of S10 proposal qualification and acquisition topics;no package/bridge trial or whole-repair acceptance'
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'scope':scope,'reviewer':work.REVIEWER,
      'reviewed_reader':report['pdf'],'evidence':evidence,'findings':findings,'preserved_records':639,'new_records':2,
      'preserved_compiled_sources':len(kept),'original_contexts_retained':True,'limitations':LIMITS,'visual_acceptance':False})
    write(REVIEW,{'operation_id':'TEXT.REVIEW.S10','status':'pass','scope':scope,'reviewer':work.REVIEWER,
      'allocated_title':'Matched qualification and build/buy/integrate decisions','allocation':{'min':4,'target':6,'max':7},
      'substantive_page_credit':credit,'physical_span':{'first_printed_page':353,'last_printed_page':359,'first_pdf_page':372,'last_pdf_page':378,'pages':7},
      'per_page':[{'printed_page':353+i,'credit':c,'rationale':why} for i,(c,why) in enumerate(credits)],
      'measurement':'Conservative standard-typography page equivalents from inspected extracted pages and mathematical content;not a calibrated measure of prose quality.',
      'double_counting':'Credit S10 only.Exclude repeated S1 search/contracts,L7 general trial design,L8 loss/cost framing and integration semantics.',
      'allocation_exception':None,'allocation_minimum_met':True,'planning_target_met':False,'reviewed_reader':report['pdf'],
      'findings':findings,'topic_coverage':['Scientific/representation/operating/rights admission','Matched request and resource experiment','Paired failures and cost-sensitive outcomes',
        'Fixed-sample and simultaneous profile qualification','Procedural equivalence and numerical error','Direct adoption,bridge,port,build,buy,reference-only and rejection','Public/generated prototypes and later owner inputs'],
      'followups_not_awarded':['Actual package/bridge/port trials','Measured costs/vendor quotations','Universal scientific capability','Q1/Q5 and visual acceptance'],
      'evidence':evidence+[ref(BASE/'release-source-review.json','Exact-reader author review')],'limitations':LIMITS,'visual_acceptance':False,'original_gap_qualification':False})
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
      ('TEXT.DRAFT.S10',['Connected argument develops notation,assumptions,derivations,alternatives and banking consequences.','All claims retain source audits;four exact examples reproduce;process records stay outside narrative.']),
      ('TEXT.REVIEW.S10',['Allocated subjects and mathematical/source findings reviewed in the compiled reader.','Four nonduplicate substantive pages meet minimum4;target6 is explicitly not claimed;no allocation exception.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,limitations=LIMITS,
          outputs=[ref(ROOT/p,'Contracted output') for p in node['outputs']],nonexecution_reason='',revisit_trigger='',
          criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence+[ref(REVIEW,'Topic/depth review')]} for i,f in enumerate(facts)])
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps({'draft':'pass','topic_depth_review':'pass','substantive_pages':credit,'target_met':False,'reader_pages':report['pages']}))

if __name__=='__main__':main()
