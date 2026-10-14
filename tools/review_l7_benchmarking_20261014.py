#!/usr/bin/env python3
"""Exact-reader author review of L7, with explicit nonduplicate page credit."""
import json
from pathlib import Path
import build_l7_benchmarking_v3_20261014 as build
import build_l7_benchmarking_v2_20261014 as repair
import develop_l7_benchmarking_20261014 as work
import review_l7_frontier_20261014 as frontier
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
REVIEWER=work.REVIEWER
REVIEW=ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.L7/chapter-review.json'
LIMITS=[
    'Author proposal topic/depth review; no independent scientific, bank or institutional acceptance.',
    'Exact examples are exposed project development constructions, not empirical model-performance results.',
    'The exposure fraction, truthful labels, positive audit inclusion and monetary quantities are stated assumptions.',
    'Two new benchmark originals are inspected; upstream datasets, code, rights and exact runtime settings remain unqualified.',
    'Nine principal evaluation papers plus inherited adjacent evidence do not establish exhaustive frontier search saturation.',
    'Live-model performance and bank validation require later scoped experiments; their absence does not block this proposal chapter.',
    'Visual acceptance and Q5 remain open under the exhausted inherited image allowance.',
]


def main():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text())
    trace=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,trace,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((work.BASE/'derivation-review.json').read_text()),
                json.loads((frontier.BASE/'primary-review.json').read_text())]:
        verify_bindings(obj)
    assert trace['status']=='pass' and not trace['issues'] and trace['scholarly_pdfs']==162
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==568 and len(new)==573 and all(new[k]==s for k,s in old.items())
    files={r['path']:r for r in audit['tex_files']}
    replacements={'docs/'+oldpath:str((repair.BASE/name).relative_to(ROOT))
                  for oldpath,name in repair.REPAIRS.items()}
    for oldpath,newpath in replacements.items():
        assert (ROOT/newpath).read_text()==repair.corrected(oldpath,(ROOT/oldpath).read_text())
    kept=[r for r in prior['tex_files'] if r['path'] not in [str(build.OLD.relative_to(ROOT)),*replacements]]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    previous_trace=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts'] for r in trace['records']}
    preserved_contexts=0
    for row in previous_trace['records']:
        for ctx in row['citation_contexts']:
            if ctx['path'] in replacements:
                assert any(c['path']==replacements[ctx['path']] and c['line']==ctx['line']
                           for c in contexts[row['citation_key']])
            else:
                assert ctx in contexts[row['citation_key']],row['citation_key']
            preserved_contexts+=1
    assert work.calculate()==json.loads((work.BASE/'exact-results.json').read_text())
    assert frontier.exact()==json.loads((frontier.BASE/'exact-results.json').read_text())
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Selective adjudication is an observation mechanism','unknown exposure history',
                   '2%–92%','11/6','CausalGraphBench','28.6%','61.4%','88.7%',
                   'USD60','always-zero rule','probability of 1/16']:
        assert phrase.lower() in text.lower(),phrase
    assert '95more' not in text and '95%' in pages[489]
    assert 'causal reasoning’ ’' not in pages[491]
    assert report['chapter_sections']['la:evaluation']==469
    assert report['chapter_sections']['la:economics']==490
    # Read all21 printed chapter pages; credit only unique developed content.
    credits=[
        (.5,'Benchmark unit and information contract; shared causal framing discounted.'),
        (.5,'Matched design and target-label diagnostic; IV construction already credited elsewhere excluded.'),
        (.25,'Set/refusal and exposure framing largely repeated in L3/L6 and later L7 development.'),
        (.5,'Unique coverage-screen operating characteristic; repeated costs and live-input prose excluded.'),
        (.25,'Specific conformance failure remedies; repeated matched-budget argument excluded.'),
        (.5,'Relation-extraction and evidence-object comparison; census/graph-construction overlap discounted.'),
        (.5,'Nested-repeat variance and source-specific comparison; duplicate CausalEval scores and general sequence excluded.'),
        (.5,'Mechanism/template split and independent-reference design; repeated introductory prose excluded.'),
        (.5,'Arm-specific information and critique controls; L6 factorial and generic budget overlap discounted.'),
        (.5,'Refusal rubric and rare-error design; repeated graph/set semantics excluded.'),
        (.75,'Paired exact-power derivation, multiplicity and prospective sample planning.'),
        (.25,'Final-study admission detail; budget arithmetic belongs to economics and recap excluded.'),
        (.5,'Published evaluation comparisons; discovery-method claims already credited in L4 excluded.'),
        (.75,'Pinned benchmark generator/scorer reuse and explicit label boundary; repeated cost/discovery background excluded.'),
        (.5,'Exposure variable and mixture setup plus scoped score accounting; repeated interval-score exposition excluded.'),
        (1,'New mixture-bound derivation, paired ranking ambiguity and exposure sensitivity interpretation.'),
        (1,'New missing-label bounds, design-unbiased audit and exact variance/clipping example.'),
        (.75,'New wrong-but-consistent rule and banking consequence; affine transform mechanics already credited in L6 excluded.'),
        (.5,'New nonlinear target distinction and oracle admission; general prototype sequence and repeated splits excluded.'),
        (.75,'CausalBench joint-score derivation and source-specific reuse concerns; repeated adjudication explanation discounted.'),
        (.75,'CausalGraphBench matched-scope, recall-threshold discrepancy and conditional reuse; general graph-score framing excluded.'),
    ]
    credit=sum(c for c,_ in credits)
    assert len(credits)==21 and credit==12
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Exact756-page reader'),
        (OUT/'source-audit.json','573 citation records including162 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Full citation index and source integrity'),
        (OUT/'text-layout-review.json','Every-page bounds and extraction'),
        (OUT/'reader.txt','Inspected printed469-489, physical487-507'),
        (work.BASE/'plan-review.md','Reviewed chapter-development plan'),
        (work.BASE/'derivation-review.json','Exposure, probability audit and consistency review'),
        (work.BASE/'primary-review.json','Feng and CausalDS primary rereads'),
        (work.BASE/'exact-results.json','221 exposure allocations and8 probability-audit outcomes'),
        (frontier.BASE/'primary-review.json','Two genuine publisher originals and exact claims'),
        (frontier.BASE/'exact-results.json','Joint score and contamination threshold arithmetic'),
        (frontier.BASE/'candidate-reassessment.json','Resolved omissions and unclosed broader artifacts'),
        (repair.BASE/'repair-review.json','Preserved punctuation defects and successor replacements'),
        (BASE/'prepared-inputs.json','Preserving integrations'),
        (Path(__file__).resolve(),'Exact author-review procedure and page-credit rationale'),
    ]]
    findings=[
        'Benchmark units, information-matched alternatives, graph/effect/refusal outcomes, statistical planning, contamination, counterexamples and remedies are developed for the proposal.',
        'All568 inherited source records remain exact; only two inherited TeX files receive deterministic punctuation repairs.',
        'All original citation uses remain, with two moved repaired sources and new inspected contexts;162 genuine scholarly PDFs are locally bound.',
        'Exact mixture, audit and consistency references reproduce; their unobserved assumptions and nonempirical scope remain explicit.',
        'Two relevant benchmark omissions are repaired with publisher originals; no code/data adoption or empirical model ranking is awarded.',
        'Twelve nonduplicate substantive pages across21 physical pages meet10/11/12 allocation; no additional credit to L3,L4,L6,L8 or software/integration chapters.',
    ]
    scope='Author review of allocated L7 proposal topics and substantive depth; no exhaustive-census or live-performance acceptance'
    write(BASE/'release-source-review.json',{
        'status':'pass','issues':[],'scope':scope,'reviewer':REVIEWER,'reviewed_reader':report['pdf'],
        'evidence':evidence,'findings':findings,'preserved_source_records':568,
        'new_source_records':5,'preserved_citation_uses':preserved_contexts,
        'inherited_source_replacements':replacements,'unchanged_compiled_sources':len(kept),
        'limitations':LIMITS,'visual_acceptance':False,
    })
    write(REVIEW,{
        'operation_id':'TEXT.REVIEW.L7','status':'pass','scope':scope,'reviewer':REVIEWER,
        'allocated_title':'Benchmarking, counterexamples, contamination and remedies',
        'allocation':{'min':10,'target':11,'max':12},'substantive_page_credit':credit,
        'physical_span':{'first_printed_page':469,'last_printed_page':489,'first_pdf_page':487,'last_pdf_page':507,'pages':21},
        'per_page':[{'printed_page':469+i,'credit':c,'rationale':why} for i,(c,why) in enumerate(credits)],
        'measurement':'Conservative standard-typography page equivalents; exclude catalogs, process prose, repetition and prior chapter credit.',
        'double_counting':'L7 only; adjacent L3,L4,L6 and economics contributions excluded explicitly.',
        'allocation_exception':None,'reviewed_reader':report['pdf'],'findings':findings,
        'topic_coverage':{
            'benchmark_unit_and_sampling':'Mechanism units, nested repeats, paired design and exact power',
            'alternatives':'Numerical, structured-form, language-only, retrieval, hybrid and expert workflows',
            'counterexamples':'Target substitution, graph/set ambiguity, wrong consistent rule and nonlinear targets',
            'contamination':'Split/exposure controls, source diagnostics and explicit mixture sensitivity bounds',
            'adjudication':'Missing-label bounds, probability audit and oracle independence',
            'literature_and_reuse':'Nine principal evaluation papers; scoped generator/scorer/rubric comparisons and conditional reuse',
            'remedies':'Public/generated oracle checks and a bounded live pilot before costly bank work',
        },
        'followups_not_awarded':[
            'Broader census reconciliation and search saturation under LL.CENSUS/mandatory repair review.',
            'Benchmark artifact/code/rights qualification before integration.',
            'Fresh independent live-model performance experiment only when claiming such performance.',
            'Whole-reader editorial, sponsor and rendered acceptance under Q1/Q5.',
        ],
        'evidence':evidence+[ref(BASE/'release-source-review.json','Exact-reader source and math review')],
        'limitations':LIMITS,'visual_acceptance':False,'original_gap_qualification':False,
    })
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,outputs,facts in [
        ('TEXT.DRAFT.L7',[ref(ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L7/chapter.tex','Preserved initial developed chapter'),
                          ref(build.CHAPTER,'Reviewed preserving successor chapter')],
         ['Connected proposal development covers the allocated benchmarking, contamination, counterexample and remedy topics.',
          'Primary audits and exact examples support all additions; inherited scientific source records are preserved and original defects repaired.']),
        ('TEXT.REVIEW.L7',[ref(REVIEW,'Actual author topic/depth review')],
         ['Allocated L7 topics are developed and reviewed under proposal scope; no live or exhaustive-census acceptance inferred.',
          'Measured12 nonduplicate substantive pages across21 physical pages against10/11/12 allocation, with no allocation exception.']),
    ]:
        node=run.ledger.operation(graph,identifier)
        receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=REVIEWER,
                       limitations=LIMITS,outputs=outputs,nonexecution_reason='',revisit_trigger='',
                       criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence+[ref(REVIEW,'Topic and depth review')]}
                                 for i,f in enumerate(facts)])
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps({'draft':'pass','topic_depth_review':'pass','substantive_pages':credit,
                      'physical_pages':21,'whole_reader_pages':report['pages'],'proposal_accepted':False}))


if __name__=='__main__':
    main()
