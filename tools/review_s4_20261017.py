#!/usr/bin/env python3
"""Review the preserved S4 successor, including exclusive substantive depth."""
import json
from pathlib import Path
import re

import build_s4_reader_v2_20261017 as build
import prepare_s4_20261017 as work
import s4_extension_20261017 as extension
import master_control as core
import run_program as run
from review_s3_20261017 import contexts, preserve
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEW = ROOT/'docs/program/comprehensive-v14/work/TEXT.REVIEW.S4/chapter-review.json'
LIMITS = work.LIMITS + [
    'Twelve exclusive substantive page equivalents meet minimum ten; the fourteen-page planning target is unmet.',
    'The initial eight-page depth failure is preserved. Physical length and material credited to earlier chapters are not counted as new depth.',
    'The finite-policy bound assumes independent evaluation, a conditionally fixed finite policy set, known correct randomization and known bounded scores.',
    'Rectangular gain classes and Lipschitz budgets are stipulated scientific restrictions, not automatically valid confidence regions.'
]


def read(path):
    return json.loads(path.read_text())


def main():
    report=read(OUT/'build-report.json'); audit=read(OUT/'source-audit.json')
    index=read(BASE/'traceability-review.json')
    for path in [OUT/'build-report.json', OUT/'source-audit.json', BASE/'traceability-review.json',
                 BASE/'prepared-inputs.json', BASE/'extension-author-review.json',
                 work.BASE/'primary-review.json', work.BASE/'draft-author-review.json',
                 work.BASE/'depth-review-initial.json', extension.BASE/'mathematics-review.json']:
        verify_bindings(read(path))
    assert report['pages']==917 and report['cited_records']==707
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==187
    layout=read(OUT/'text-layout-review.json')
    assert layout['status']=='pass' and not layout['out_of_bounds'] and not layout['empty_pages']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text()==build.expected_driver()
    canonical=work.PRIOR.parent.parent
    retained_canonical=preserve(audit,index,canonical,703,
                               [str(build.CANONICAL_OLD.relative_to(ROOT))])
    retained_candidate=preserve(audit,index,build.previous.BASE,706,
                               [str(build.OLD.relative_to(ROOT))])
    assert work.examples.calculate()==read(work.BASE/'exact-results.json')
    assert work.independent()['status']=='pass'
    exact=read(extension.BASE/'exact-results.json')
    assert extension.calculate()==exact and extension.separate(exact)['status']=='pass'
    aux=(OUT/(build.NAME+'.aux')).read_text()
    equations={}
    labels=['pair-target','negative-joint','design-trace','maximin','robust-regret',
            'robust-example','policy-score','uniform-bound','evaluation-size','gap-sharp']
    for number,label in enumerate(labels,14):
        match=re.search(re.escape('\\newlabel{exec17:s4-'+label+'}{{')+r'([^}]+)',aux)
        assert match and match.group(1)=='21.'+str(number),label
        equations[label]=match.group(1)
    pages=(OUT/'reader.txt').read_text().split(chr(12))
    initial=read(work.BASE/'depth-review-initial.json')
    per_page=[dict(row) for row in initial['per_page']]
    assert sum(row['credit'] for row in per_page)==8
    per_page[-1].update(credit=.5,rationale=
        'New pair-selection law, Bayes reweighting and distinct common/pair effects; preceding generic prototype prose excluded.')
    additional=[
        (.75,'Negative joint covariance, twelve-atom and cancellation checks, and design criterion; generic proposed-wrapper prose discounted.'),
        (.5,'Distinct precision-objective design optima and new rectangular allocation formula; generic robust/regret framing already credited to L8 excluded.'),
        (.5,'Rectangular feasible-allocation endpoint witnesses and finite-policy score expectation; L8 objective/randomization discussion and generic evaluation setup discounted.'),
        (1,'Complete exponential-moment, two-tail and finite-policy union proof, selected-policy regret, monetary score range and sufficient sample size.'),
        (.75,'Sharp discrete-score Lipschitz set, explicit endpoint extensions and information consequences; general product/prototype conclusion excluded.')]
    for offset,(credit,rationale) in enumerate(additional):
        per_page.append(dict(printed_page=210+offset,pdf_page=230+offset,
                             credit=credit,rationale=rationale))
    for row in per_page:
        assert re.search(r'\b'+str(row['printed_page'])+r'\b',pages[row['pdf_page']-1])
    assert report['effect_sections']['s4-extension-end']==214
    for label,number in equations.items():
        assert '('+number+')' in ''.join(pages[228:234]),label
    assert not any('??' in p for p in pages[216:234])
    credit=sum(row['credit'] for row in per_page); assert credit==12
    prior_reviews=sorted((ROOT/'docs/program/comprehensive-v14/work').glob('TEXT.REVIEW.*/chapter-review.json'))
    assert REVIEW not in prior_reviews
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Exact917-page successor; no material warnings'),
        (OUT/'source-audit.json','707 source records and187 genuine scholarly PDFs'),
        (BASE/'traceability-review.json','Exact-driver identity, primary text and citation contexts'),
        (OUT/'text-layout-review.json','All-page text bounds pass; not visual acceptance'),
        (OUT/'reader.txt','All S4 printed197-214/physical217-234 inspected'),
        (work.CHAPTER,'Preserved effects, heterogeneity and threshold chapter'),
        (build.EXTENSION,'Common-population, allocation, finite-policy and score-gap derivations'),
        (work.BASE/'plan.md','Reviewed initial execution and overlap exclusions'),
        (work.BASE/'primary-review.json','Thirteen inspected original-paper/software excerpts'),
        (work.BASE/'exact-results.json','Seven exact authored families'),
        (work.BASE/'mathematics-review.json','Separate symbolic, moment, dual and witness checks'),
        (ROOT/'tools/s4_examples_20261017.py','Exact rational reference'),
        (ROOT/'tools/prepare_s4_20261017.py','Separate mathematics and primary review'),
        (work.BASE/'depth-review-initial.json','Preserved initial eight-page depth failure'),
        (work.BASE/'depth-extension-plan.md','Reviewed preserving depth repair'),
        (extension.BASE/'exact-results.json','Five additional authored law/bound families'),
        (extension.BASE/'mathematics-review.json','Twelve atoms, design, rectangle, score and endpoint checks'),
        (ROOT/'tools/s4_extension_20261017.py','Separate reference and verification'),
        (work.BASE/'prototype-design.json','Proposed comparison; not an executed study'),
        (ROOT/'docs/program/comprehensive-v14/gap-audit.json','S4 allocation10/14/17'),
        (Path(__file__),'Exclusive-depth, mathematics, source and equation review')]]
    evidence += [ref(p,'Prior chapter allocation inspected for duplicate credit') for p in prior_reviews]
    scope='Author S4 subject, primary-source, mathematics and exclusive-depth review; proposal development only'
    findings=[
        'Develops assignment-dependent target derivatives, exact overlap remainder, fitted-path distinctions, joint multiarm comparison, resource allocation and threshold approximation/support.',
        'Seven original and five extension exact-reference families reproduce with separate author checks. No new upstream or bank experiment is inferred.',
        'All703 canonical and706 first-candidate records, compiled-source hashes except replaced drivers, and citation-context multisets remain.',
        'The selected CausalML full-input point mean10 is distinguished from the explanatory pair-population mean8; neither is a newly observed package result.',
        'Extension equations21.14-21.23 agree with source and extracted pages. All eighteen chapter pages and all-page text bounds were inspected.',
        'Twelve exclusive substantive page equivalents meet minimum ten; target fourteen remains unmet. Generic robust/regret framing credited to L8 and earlier software/score material are discounted.',
        'Finite-policy concentration is a proved conditional bound, not measured coverage. Robust rectangles and sharp Lipschitz sets retain their explicit restrictions.',
        'Q1/Q5, visual acceptance, whole software coverage, independent review and product/bank qualification remain open.']
    write(BASE/'release-source-review.json',dict(status='pass',issues=[],scope=scope,
        reviewer=work.REVIEWER,reviewed_reader=report['pdf'],findings=findings,evidence=evidence,
        canonical_records_preserved=703,first_candidate_records_preserved=706,
        canonical_compiled_sources_preserved=retained_canonical,
        candidate_compiled_sources_preserved=retained_candidate,
        original_context_multisets_retained=True,equation_numbers=equations,
        limitations=LIMITS,visual_acceptance=False))
    write(REVIEW,dict(operation_id='TEXT.REVIEW.S4',status='pass',scope=scope,
        reviewer=work.REVIEWER,allocated_title='Effect estimation, heterogeneous effects and quasi-experiments',
        allocation=dict(min=10,target=14,max=17),substantive_page_credit=credit,
        new_synthesis_span=dict(first_printed_page=197,last_printed_page=214,
                                first_pdf_page=217,last_pdf_page=234,pages=18),
        per_page=per_page,allocation_minimum_met=True,planning_target_met=False,allocation_exception=None,
        measurement='Conservative author-assessed standard-typography page equivalents from extracted pages and source mathematics; not visual acceptance or a calibrated prose-quality metric.',
        double_counting='S4 only. Initial repeated ATE/ATT/clipping/IPW, finite-epsilon and software facts remain discounted. L8 generic robust/regret and randomized-action framing receive no new credit; only new rectangular feasible-allocation mathematics is counted. S5/S6 longitudinal/panel subjects are reserved.',
        reviewed_reader=report['pdf'],findings=findings,
        topic_coverage=['Assignment-dependent target derivatives','Exact orthogonal overlap remainder',
            'Selected DoubleML/grf/CausalML/CausalPy/rdrobust semantics','Common-population joint covariance',
            'Resource-constrained and robust allocation','Restricted finite-policy evaluation proof',
            'Local-linear/fuzzy approximation','Sharp score-gap and portfolio bounds'],
        followups_not_awarded=['Fourteen-page planning target','Whole software census and dependency rights',
            'Actual wrapped/ported estimator qualification','Dependent/estimated-propensity finite-policy theory',
            'Bank scientific assumptions, capacities, acceptable loss and costs','Q1/Q5 and rendered visual acceptance'],
        evidence=evidence+[ref(BASE/'release-source-review.json','Exact-reader review')],
        limitations=LIMITS,visual_acceptance=False,whole_census_closed=False,original_gap_qualification=False))
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE))
    for identifier,facts in [
        ('TEXT.DRAFT.S4',['Connected banking argument explains targets, notation, assumptions, derivations, diagnostics, alternatives and software routes.',
            'Audited genuine originals, exact authored examples and proved bounded results support the scoped claims; process records remain outside the narrative.']),
        ('TEXT.REVIEW.S4',['Allocated effects/heterogeneity/quasi-experiment subject has a bounded author source, mathematics and equation review; the original depth failure remains preserved.',
            'Twelve exclusive substantive page equivalents meet minimum ten; fourteen-page target remains unmet, with no allocation exception.'])]:
        node=run.ledger.operation(graph,identifier);receipt=run.ledger.receipt_template(node)
        receipt.update(outcome='pass',execution='performed',scope=scope,reviewer=work.REVIEWER,
            limitations=LIMITS,outputs=[ref(ROOT/p,'Contracted output') for p in node['outputs']],
            nonexecution_reason='',revisit_trigger='',
            criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(REVIEW,'Exclusive chapter-depth review')])
                      for i,f in enumerate(facts)])
        write(BASE/('draft-operation-receipt.json' if identifier.startswith('TEXT.DRAFT') else 'review-operation-receipt.json'),receipt)
    print(json.dumps(dict(draft='pass',topic_review='pass',exclusive_substantive_pages=credit,
        planning_target_met=False,reader_pages=917,visual_acceptance=False)))


if __name__=='__main__':main()
