#!/usr/bin/env python3
"""Bind inspected S6 originals, exact authored laws and prospective routes."""
import copy
import json
from pathlib import Path
import s6_examples_20261017 as examples
import s6_value_checks_20261017 as value
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR=ROOT/'docs/program/execution/2026-10-17/s5/publication-v3/reader/source-audit.json'
CHAPTER=ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S6/chapter.tex'
LIMITS=[
    'Author review only; no independent scientific or institutional acceptance.',
    'Exact stipulated laws and illustrative monetary amounts, not bank observations, package runtime trials or a fresh statistical study.',
    'Conditional known loadings, factor/contamination bounds and covariance do not establish their truth for a bank.',
    'Feedback responses require the stated intervention and structural invariance; tail and quadratic-cost convergence need separate defended premises.',
    'Selected package documentation and inherited snapshots do not close the exhaustive software census, full dependency rights or runtime qualification.',
    'Literature cutoff2026-10-07; historical snapshot and commit-membership limits are retained.',
    'Rendered visual acceptance remains false under the exhausted inherited image allowance.'
]
SPECS=[
    ('sun2021','docs/literature/text/sun2021.txt',1,85,
     'arXivv2 dated22September2020; relative-time coefficients can mix heterogeneous effects from other periods and generate apparent pretrends.'),
    ('rambachan2023','docs/literature/text/rambachan2023_verified.txt',90,220,
     'Distinct smoothness/relative-magnitude restrictions; noisy pretreatment information and conditional/hybrid/fixed-length inference have distinct regimes.'),
    ('benmichael2021','docs/literature/text/benmichael2021.txt',310,378,
     'Outcome-model augmentation and ridge representation can adjust balance and imply negative donor weights.'),
    ('benmichael2021','docs/literature/text/benmichael2021.txt',410,465,
     'Regularization and balance/weight tradeoffs in the saved July2020 technical manuscript.'),
    ('synthdid2021','docs/literature/text/synthdid2021.txt',1248,1356,
     'Assumptions1-4 and Theorem1 require iid Gaussian rows, growth, spectral/predictive-weight and regularization-rate conditions.'),
    ('synthdid2021','docs/literature/text/synthdid2021.txt',1400,1515,
     'Unit bootstrap, fixed-weight jackknife restrictions, undefined single-treated-unit jackknife and placebo homoskedasticity.'),
    ('sw_synthdid','docs/literature/raw/raw_readme_synthdid.md',1,49,
     'Saved beta matrix interface, simultaneous block layout and documented estimator/variance usage.'),
    ('sw_honestdid','docs/literature/raw/raw_readme_honestdid.md',1,90,
     'Relative-magnitude and smoothness restrictions differ; uncertainty in pretrend estimates remains relevant.'),
    ('sw_honestdid','docs/literature/raw/raw_readme_honestdid.md',395,548,
     'Documented bridge uses a universal baseline, consecutive periods, influence covariance, normalized-coefficient removal and a single-horizon target vector.'),
    ('v12_sw_augsynth','docs/literature/raw/v12_sw2_manual_augsynth_1.txt',1,54,
     'Dispatcher distinguishes single/multiple-outcome and staggered paths, with different balance and regularization controls.'),
    ('v12_sw_eventstudyinteract','docs/literature/raw/v12_sw2_manual_eventstudyinteract_1.txt',1,115,
     'Long format, cohort/control specification, balanced/no-covariate warning, last-treated exclusion, weighted versus underlying-regression outputs.')
]


def main():
    prior=json.loads(PRIOR.read_text());verify_bindings(prior)
    index={r['integrated_citation_key']:r for r in prior['sources']}
    assert len(index)==712 and 'sun2021' not in index
    sun=copy.deepcopy(next(x for x in json.loads((ROOT/'docs/literature/sources.json').read_text())
                           if x['id']=='sun2021'))
    sun.update(integrated_citation_key='sun2021',
        version_status='Journal of Econometrics2021 bibliographic year; genuine saved technical PDF is arXiv1804.05785v2,22September2020',
        inspected=['Saved primary text lines1-85: version identity, abstract and relative-time coefficient contamination; exact excerpt in S6 primary review.'],
        claims=['Heterogeneous effects from other relative periods can contaminate an event-study lead or lag and generate apparent pretrends.'],
        limits='Saved preprint is not asserted to be the final journal version. Project finite projection witness is separately derived.')
    index['sun2021']=sun
    for p in [BASE/'mathematics-review.json',BASE/'robust-mathematics-review.json',
              BASE/'value-checks/mathematics-review.json']:
        verify_bindings(json.loads(p.read_text()))
    exact=json.loads((BASE/'exact-results.json').read_text())
    assert examples.calculate()==exact and examples.separate(exact)['status']=='pass'
    assert value.calculate()==json.loads((BASE/'value-checks/exact-results.json').read_text())
    rows=[];folder=BASE/'inspected';folder.mkdir(exist_ok=False)
    for i,(key,path,first,last,claim) in enumerate(SPECS,1):
        p=ROOT/path;lines=p.read_text().splitlines();assert last<=len(lines)
        excerpt=folder/f'{i:02d}-{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        old=index[key]
        row=dict(citation_key=key,source_identity=old.get('source_identity') or old.get('title'),
            version_date=old.get('version_date') or old.get('version_status'),
            local_copy=ref(p,f'Inspected lines{first}-{last}'),
            inspected_excerpt=ref(excerpt,'Exact primary-text excerpt'),supported_claims=[claim])
        if old['kind']=='paper':
            row['genuine_pdf']=dict(path=old['local_path'],sha256=old['sha256'],
                                    anchor='Genuine scholarly original')
        rows.append(row)
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_synthesis',
        reviewer=dict(name='Codex author/coordinator',kind='author'),cutoff='2026-10-07',
        records=rows,inherited_source_records=[index[k] for k in sorted({x[0] for x in SPECS})],
        evidence=[ref(PRIOR,'712 preserved source records'),ref(Path(__file__),'Evidence preparation')],
        limitations=LIMITS))
    profiles=[
        dict(target='Cohort/horizon effects and fixed monetary weights',
             routes=['cohort-aware estimator','HonestDiD sensitivity wrapper'],
             admission='Universal baseline and full joint covariance, unchanged population, consecutive clock, fixed restriction and target; covariance law justified separately.'),
        dict(target='Donor counterfactual under declared balance and noise class',
             routes=['original R augsynth path'],
             admission='Correct dispatcher and common target; retain signed weights, penalty, contamination assumptions and justified inference; inspect downstream path first.'),
        dict(target='Simultaneous block rollout',routes=['original R synthdid beta interface'],
             admission='Explicit unit/time rectangle and inferential regime; staggered requests refused by the block route or separately redesigned.'),
        dict(target='Innovation or replacement-controller response',routes=['authored structural reference'],
             admission='Action excitation or supplied identifying restriction, intervention-specific recursion, feasibility, cost and both tail convergence conditions.')
    ]
    write(BASE/'prototype-design.json',dict(status='proposed_not_executed',profiles=profiles,
        exact_references=[ref(p,'Exact authored semantic reference') for p in
            [BASE/'exact-results.json',BASE/'robust-results.json',BASE/'value-checks/exact-results.json']],
        primary_review=ref(BASE/'primary-review.json','Inspected original texts'),
        steps=['Freeze common estimand, supported cells, clock, versions, rights and environment.',
               'Admit the semantic translation against exact authored references before statistical evaluation.',
               'Permitted public covariate panels can supply realistic structure; generated potential outcomes remain explicitly constructed truth.',
               'Register fresh laws/seed, sample sizes, repetitions, all scenarios, uncertainty methods, fixed stopping and every failure denominator.',
               'Vary heterogeneity, curvature, donor contamination, factor extrapolation, calendar dependence, action excitation and stability.',
               'Report target error, coverage in the stipulated law, availability, width, monetary loss and full observed workflow cost.'],
        future_inputs=['Authentic assignment/observation and shock truth, feasible policies and accepted precision/loss thresholds.',
                       'Complete package/dependency rights, permitted runtimes and target consumer acceptance.'],
        upstream_packages_executed=False,bank_qualified=False,whole_census_closed=False,limitations=LIMITS))
    claims=[
        ('math','Panel rollout projections, sharp horizon budgets, donor risk and feedback value references','project_derivation',BASE/'exact-results.json',
         ['Exact rank12 event-study projection and independent within/FWL check give false leads under no anticipation.',
          'Sharp signed-target curvature bounds, monetary threshold and normal-design interval retain the noisy slope.',
          'Donor minimax risk changes under signed contamination; factor-cell SDID bias/noise and finite-calendar covariance are checked separately.',
          'Feedback intervention paths, observationally equivalent controllers, action costs and conditional finite/infinite tail budgets have exact rational references.']),
        ('paths','Panel and time-series software routes preserving targets and uncertainty','software_primary_sources',BASE/'primary-review.json',
         ['Selected original manuals preserve cohort/base-period/covariance distinctions, dispatcher paths and simultaneous block restrictions.',
          'Original R and conditional Stata wrappers are proposed; automatic estimator substitution and an unqualified native port are not admitted.']),
        ('design','Target-preserving public/generated panel and controller prototype design','project_design',BASE/'prototype-design.json',
         ['Exact semantic admission precedes a frozen prospective statistical comparison with public structure and explicitly generated causal truth.',
          'Full failed-request accounting and monetary loss/cost reporting do not constitute executed upstream packages, bank validation or software-census closure.'])]
    sources=[sun]
    for key,title,kind,path,supported in claims:
        sources.append(dict(integrated_citation_key='exec17_s6_'+key,title=title,
            author='Causal banking proposal',kind=kind,year=2026,
            source_identity='Authored exact law, conditional proof, design or identity-bound primary-source synthesis',
            version_date='2026-10-17; inherited source snapshots and2026-10-07 cutoff limits retained',
            local_copy=ref(path,title),inspected_anchors=supported,supported_claims=supported,
            records=[ref(p,'Reviewed source or mathematical evidence') for p in
                [BASE/'primary-review.json',BASE/'mathematics-review.json',
                 BASE/'robust-mathematics-review.json',BASE/'value-checks/mathematics-review.json',
                 BASE/'plan.md',Path(__file__)]],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,prior=ref(PRIOR,'712 preserved source identities'),
                                      cutoff='2026-10-07'))
    write(BASE/'precompile-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(p,'Inspected input') for p in
                  [CHAPTER,BASE/'plan.md',BASE/'primary-review.json',BASE/'prototype-design.json',
                   BASE/'value-checks/mathematics-review.json',BASE/'source-audit.json']],
        findings=['Rank, omitted period, zero anticipation, signed kernels and monetary units are explicit.',
                  'Curvature identified set and Gaussian sampling interval are distinct; fixed-M/target and covariance conditions retained.',
                  'Fixed donor/unit/time weights and exact risk comparisons do not qualify fitted upstream inference.',
                  'Controller innovation response and whole regime replacement are distinguished; quadratic incremental cost cross term is explained.',
                  'Source versions, genuine Sun original, package rights, historical snapshots and public-data truth limitations retained.',
                  'Inherited generic foundations receive no duplicate exclusive-depth credit; depth assessed only after compilation.'],
        visual_acceptance=False,limitations=LIMITS))
    print(json.dumps(dict(primary_excerpts=len(rows),new_records=4,expected_total=716,
                          scholarly_pdfs=188,visual_acceptance=False)))


if __name__=='__main__':main()
