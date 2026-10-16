#!/usr/bin/env python3
"""Bind S5 inspected originals, exact derivations and prospective reuse design."""
import json
from pathlib import Path
import s5_examples_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT,BASE,CHAPTER=examples.ROOT,examples.BASE,examples.CHAPTER
PRIOR=ROOT/'docs/program/execution/2026-10-17/s4/publication-v2/reader/source-audit.json'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
LIMITS=[
    'Author review, not independent scientific acceptance.',
    'Eight exact stipulated laws and dollar amounts; no new upstream-estimator execution, empirical coverage, bank observation or ROI.',
    'Selected original files and inherited version/date records do not close the software census, full dependency rights or statistical/runtime qualification.',
    'The older gfoRmula/ltmle/lmtp package declarations and separately acquired API bytes are content-bound; package-release and commit membership are not inferred from metadata alone.',
    'The literature cutoff is2026-10-07; inherited mutable-snapshot and historical-cutoff limits are retained.',
    'The natural-action witness deliberately violates strong innovation independence; the capped-shift witnesses omit endpoint regularity.',
    'Uniform transition-error budgets and independent-trajectory sampling are explicit assumptions, not established properties of bank data.',
    'Rendered visual acceptance remains false; inherited image allowance is exhausted.'
]


def main():
    prior=json.loads(PRIOR.read_text());verify_bindings(prior)
    index={r['integrated_citation_key']:r for r in prior['sources']}
    assert examples.calculate()==json.loads((BASE/'exact-results.json').read_text())
    assert examples.separate(examples.calculate())['status']=='pass'
    specifications=[
        ('lmtp2023','docs/literature/text/lmtp2023.txt',266,310,
         'Example2 support-preserving shift; later natural exposure is evaluated under the modified history; shifted-distribution intervention is a different target.'),
        ('lmtp2023','docs/literature/text/lmtp2023.txt',355,422,
         'Assumptions1-3 and Theorem1: standard sequential randomization identifies LMTP-SI; natural-action LMTP uses the stronger innovation condition.'),
        ('lmtp2023','docs/literature/text/lmtp2023.txt',445,550,
         'Threshold nonregularity, piecewise inverse-branch pushforward, fixed-map condition, Theorem2 and one-time influence/variance formula.'),
        ('sequentialdr2018','docs/literature/text/sequentialdr2018.txt',190,295,
         'Definitions distinguish all-outcome/all-treatment double robustness from per-time either robustness and from functional-model specifications.'),
        ('sw_gformula','docs/literature/raw/r3g_api_gformula.txt',1,75,
         'Risk versus end-of-follow-up outcomes, censoring and competing-event options, custom intervention/history roles; selected saved API only.'),
        ('sw_ltmle','docs/literature/raw/r3g_api_ltmle.txt',1,100,
         'Wide time-ordered nodes, event1 absorbing coding, censoring factor, post-event node treatment and continuous Yrange transformation.'),
        ('sw_ltmle','docs/literature/raw/r3g_api_ltmle.txt',152,170,
         'gbounds acts on cumulative g probabilities, not individual time-step probabilities.'),
        ('sw_ltmle','docs/literature/raw/r3g_api_ltmle.txt',200,224,
         'Variance options and documented limitations, positivity/rare-event caution and household/subject id.'),
        ('sw_lmtp','docs/literature/raw/r3g_api_lmtp_estimators.txt',1,92,
         'Chronological trt/L/outcomes, shifted overriding shift, finite memory, cluster id, folds, weights and noncumulative density-ratio output.'),
        ('v12_sw_stremr','docs/literature/raw/v12_sw2_manual_stremr_1.txt',1,66,
         'fitTMLE wraps fitSeqGcomp(TM​LE=TRUE); output survival by time; example distinguishes treatment, monitoring and censoring propensity models.'),
        ('v12_sw_survtmle','docs/literature/raw/v12_sw2_manual_survtmle_1.txt',1,144,
         'Fixed binary treatment, integer times/event codes, default event-derived horizon, mean/hazard methods, finite-sample nonconvergence and gtol; documented tol usage/prose differ.'),
        ('v12_sw_survtmle','docs/literature/raw/v12_sw2_manual_survtmle_1.txt',145,184,
         'Joint covariance, subject influence vectors, meanIC and retained models support declared posthoc comparisons; no inference of actual convergence.'),
        ('v131_sw_pygformula','docs/literature/raw/v12_gap4_pygformula_bootstrap.txt',188,270,
         'Resamples unique subjects and entire histories with fresh IDs, refits models, optionally resamples simulation baselines, resets the same seed for intervention simulation.'),
        ('v13_sw_pygformula','docs/literature/raw/v12_gap4_pygformula_simulate.txt',215,265,
         'Competing event is drawn before target event; target event becomes missing on a competing event. This source path alone does not prove model fitting risk sets.'),
        ('v13_sw_pygformula','docs/literature/raw/v12_gap4_pygformula_simulate.txt',450,480,
         'Aggregation multiplies target probability by no-competing probability and previous survival products; stored survival is1 minus target cumulative incidence.')
    ]
    records=[];folder=BASE/'inspected';folder.mkdir(exist_ok=False)
    for i,(key,path,first,last,claim) in enumerate(specifications,1):
        original=ROOT/path;lines=original.read_text().splitlines()
        assert last<=len(lines)
        excerpt=folder/f'{i:02d}-{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        inherited=index[key]
        version=inherited.get('version_date') or inherited.get('version_status')
        if key.startswith('sw_'):
            snapshot=json.loads((ROOT/inherited['local_path']).read_text())
            version=dict(package_declaration=snapshot.get('package_version'),
                observed_at=snapshot.get('observed_at'),pin_limit=snapshot.get('pin_limit'))
        if key=='lmtp2023': version='JASA2023; saved arXivv4 July2021 technical text'
        if key=='sequentialdr2018': version='2018 scholarly original; inherited identity and PDF hash retained'
        row=dict(citation_key=key,source_identity=inherited.get('source_identity') or inherited.get('title'),
                 version_date=version,local_copy=ref(original,f'Inspected lines{first}-{last}'),
                 inspected_excerpt=ref(excerpt,'Exact inspected original-text range'),
                 supported_claims=[claim])
        if inherited['kind']=='paper':
            row['genuine_pdf']=dict(path=inherited['local_path'],sha256=inherited['sha256'],
                                   anchor='Genuine scholarly PDF; technical text inspected')
        records.append(row)
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_synthesis',reviewer=REVIEWER,
        cutoff='2026-10-07',records=records,
        inherited_source_records=[index[k] for k in sorted({s[0] for s in specifications})],
        evidence=[ref(PRIOR,'707 source identities'),ref(Path(__file__),'Identity binding and inspected anchors')],
        limitations=LIMITS))
    profiles=[
        dict(name='Common-horizon fixed baseline treatment',candidates=['survtmle','commercial fixed-treatment survival comparators'],
             admission='Same baseline population, integer event clock, explicit common horizon, observation law and first-event target; preserve covariance.'),
        dict(name='Repeated binary regime',candidates=['ltmle','stremr','gfoRmula','pygformula'],
             admission='Same chronological intervention/observation law and event convention; no substitution of a baseline or MSM target.'),
        dict(name='Supported modified action',candidates=['lmtp'],
             admission='Freeze the map, natural-versus-redrawn target, support, all inverse branches and ratio orientation; retain strong-condition limitations.'),
        dict(name='Numerical policy contrast',candidates=['gfoRmula','pygformula'],
             admission='Separate fit uncertainty from simulation error; whole-subject histories and explicit coupling, failed replicate and horizon accounting.'),
        dict(name='Unsupported-tail or singular-cap query',candidates=['authored set-valued reference'],
             admission='Return a declared identified set or refusal. A finite scalar from an incompatible engine is a semantic failure.')
    ]
    design=dict(status='proposed_not_executed',profiles=profiles,
        steps=['Freeze target, versions, rights, environment, subject/event clock, policies and common horizon.',
               'Use exact laws to admit target-preserving translations before statistical comparison.',
               'For a future study register fresh full-history laws, sample sizes, seed, all scenarios, repetitions, stopping rule, learners, interval/band methods and every failure denominator.',
               'Separate subject sampling, shared shocks, model misspecification, censor support and numerical draw budgets.',
               'Compare identified target/error, availability, joint uncertainty, monetary decision loss and full observed computation/review cost.',
               'Optional permitted public covariates do not create causal truth; generated potential outcomes establish only the declared constructed truth.'],
        exact_reference=ref(BASE/'exact-results.json','Eight exact semantic laws'),
        primary_review=ref(BASE/'primary-review.json','Selected original software and mathematical texts'),
        future_inputs=['Authentic bank assignment/observation truth, feasible policy versions and accepted loss/cost thresholds.',
                       'Complete dependency licensing and deployed consumer/runtime acceptance.'],
        limitations=LIMITS,bank_qualified=False,whole_census_closed=False)
    write(BASE/'prototype-design.json',design)
    claims=[
        ('math','Finite-horizon, selection, modified-policy and numerical-error references','project_derivation',BASE/'exact-results.json',
         ['Sharp discrete restricted-time tails and endpoint witnesses; frailty survivor selection; ordered-event conversion and monetary ranking.',
          'Observed-law-equivalent natural-action worlds; noninjective pushforward and singular-cap witnesses; normalized fixed-map path derivative and extra variance.',
          'Cumulative versus incremental bounding, paired-policy simulation and whole-subject uncertainty, and proved sequential total-variation error envelope.']),
        ('paths','Longitudinal and survival software: clocks, treatment laws and uncertainty','software_primary_sources',BASE/'primary-review.json',
         ['Selected original APIs and code preserve differences in event coding, time representation, interventions, horizons, density ratios, targeting and uncertainty.',
          'Prospective wrapping/adoption retains exact version, license and complete qualification limits.']),
        ('design','Common-target longitudinal and survival prototype comparison','project_design',BASE/'prototype-design.json',
         ['Semantic admission and exact references precede a frozen prospective public/generated statistical comparison.',
          'No new upstream package execution, bank experiment, software-census closure or adoption is inferred.'])]
    sources=[]
    for key,title,kind,path,supported in claims:
        sources.append(dict(integrated_citation_key='exec17_s5_'+key,title=title,author='Causal banking proposal',
            kind=kind,year=2026,source_identity='Project derivation/design or identity-bound primary-source synthesis',
            version_date='2026-10-17; original identities and historical limits retained in primary review',
            local_copy=ref(path,title),inspected_anchors=supported,supported_claims=supported,
            records=[ref(BASE/'primary-review.json','Genuine originals and inspected technical claims'),
                     ref(BASE/'mathematics-review.json','Separate author algebra, laws and witnesses'),
                     ref(BASE/'plan.md','Reviewed scope and exclusive-depth contract'),
                     ref(Path(__file__),'Evidence preparation')],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,prior=ref(PRIOR,'707 preserved source records'),cutoff='2026-10-07'))
    print(json.dumps(dict(primary_excerpts=len(records),exact_families=8,new_records=3,visual_acceptance=False)))


if __name__=='__main__':main()
