#!/usr/bin/env python3
"""Freeze reviewed commercial sources, exact examples and prospective design."""
import json
import re
from pathlib import Path

import s8_examples_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT/'docs/program/execution/2026-10-17/s7/publication-v2/reader/source-audit.json'
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S8/chapter.tex'
LIMITS = [
    'Author review only; no independent or institutional acceptance.',
    'No paid vendor engine, new upstream package trial or bank experiment was executed.',
    'Costs, volumes, durations, utilities, priors and signal errors are stipulated planning inputs, not observed prices or performance.',
    'Every compared route must achieve matched scientific acceptance, including remedial work in the bad compatibility state.',
    'Selected inspected commercial originals do not close the full seventeen-area census or exact edition, deployment rights, price and support questions.',
    'Literature cutoff 2026-10-07; mutable vendor copies acquired later do not establish historical cutoff bytes.',
    'Rendered visual acceptance remains false under the exhausted inherited image allowance.'
]
SPECS = [
 ('exec13_genie_pattern','2026-10-13/commercial/genie_pattern.txt',1,23,
  'Pattern-class representation and random Create DAG completion; neither selects a causally true representative.'),
 ('exec13_smile_pc','2026-10-13/commercial/smile_pc.txt',1,23,
  'DSL_pattern output; interruption return; elapsed time checked after iterations, not a hard wall-time guarantee.'),
 ('exec13_smile_pattern','2026-10-13/commercial/smile_pattern.txt',1,30,
  'Pattern coordinates and dataset variable order must correspond in conversion.'),
 ('exec13_bayesia_eq','2026-10-13/commercial/bayesia_eq.txt',125,136,
  'EQ equivalence-class search treats fixed arcs as ordinary arcs and respects forbidden arcs and temporal indices.'),
 ('exec13_bayesia_api','2026-10-13/commercial/bayesia_api.txt',75,108,
  'Loaded-model instance licensing, Java and REST configurations, model residency and license connectivity; flattened table does not establish exact edition-feature parity.'),
 ('exec13_smile_license','2026-10-13/commercial/smile_license.txt',1,11,
  'Academic/commercial development and server/end-user deployment distinctions; no numeric quote or new rights grant.'),
 ('exec13_ci_bayesserver_causality','2026-10-13/commercial-identification/bayesserver_causality.txt',137,205,
  'Interventional optimization; explicit abduction, removal of factual evidence and intervention; helper10+ versus calculation9.4+; not general latent identification.'),
 ('exec13_ci_stata_causal_intro','2026-10-13/commercial-identification/stata_causal_intro.txt',459,491,
  'IID, conditional independence and overlap restrict the documented treatment-effect estimators.'),
 ('exec13_ivrd_stata','2026-10-13/commercial-iv-rd/stata_post.txt',845,864,
  'Five possible weak-IV confidence-set forms; empty-set model rejection distinguished from inadequate grid bounds.'),
 ('exec13_ivrd_license','2026-10-13/commercial-iv-rd/stata_license.txt',179,185,
  'Identified-user licensing is not general unattended service permission.'),
 ('exec13_ivrd_license','2026-10-13/commercial-iv-rd/stata_license.txt',234,247,
  'Concurrent-user/site and annual/perpetual categories; no conversion to engine-instance entitlement.'),
 ('exec13_ch_stata','2026-10-13/commercial-heterogeneity/stata_post.txt',795,815,
  'Prespecified probability-valued static policy evaluation and policy contrast, not arbitrary sequential-policy inference.'),
 ('exec13_ch_jmp_causal','2026-10-13/commercial-heterogeneity/jmp_assumptions.txt',1,19,
  'Positivity, consistency and conditional exchangeability; assumption checks do not manufacture causal truth.'),
 ('exec13_ch_jmp_causal','2026-10-13/commercial-heterogeneity/jmp_causal.txt',1,26,
  'ATE/ATET and continuous-treatment MSM/GPS outputs; quadratic centering and density-plot interpretation limits.'),
 ('exec14_survival_stata','2026-10-14/commercial-survival/v2/stata_intro.txt',72,100,
  'Survival treatment command excludes delayed entry, time-varying covariates and multiple-record data.'),
 ('exec14_survival_sas','2026-10-14/commercial-survival/v2/sas_competing_retry.txt',20,44,
  'Competing-event modified risk sets, covariance controls and options ignored under EVENTCODE.'),
 ('exec16_cp_bayesfusion','2026-10-16/commercial-policy/smile_influence.txt',1,17,
  'Decision, value and MAU nodes; indexing parents and policy-specific matrix interpretation.'),
 ('exec16_cp_azure','2026-10-16/commercial-policy/azure_overview-elevated.txt',22,64,
  'Documented2026-08-25 retirement; Rank/Reward, delayed reward, no maintained individual histories; no replacement parity.')
]


def main():
    assert not CHAPTER.exists() and not (BASE/'primary-review.json').exists()
    prior=json.loads(PRIOR.read_text()); verify_bindings(prior)
    index={s['integrated_citation_key']:s for s in prior['sources']}
    assert len(index)==721
    exact=examples.calculate(); checked=examples.separate(exact)
    write(BASE/'exact-results.json',exact)
    write(BASE/'mathematics-review.json',dict(checked,
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/'exact-results.json','Exact rational laws'),
                  ref(ROOT/'tools/s8_examples_20261017.py','Separate finite choice and subset-sum checks')],
        findings=['All three acquisition routes enter the signal decision; hybrid dominates licensed in both compatibility states.',
                  'No-signal hybrid475000; signal467750 before test; gross7250; net2250 at5000 and minus7750 at15000; perfect-information10000.',
                  'Worst regret selects hybrid; worst absolute cost selects build over the declared volumes.',
                  'Two-instance schedule is7 and5+4, makespan9; three instances attain7.',
                  'Quote ceiling35000 at50000; continuous-volume peak1185000/19.',
                  'Four indexed policies have values0,-15,5,-10; restricted no-history optimum0; full-history optimum5.'],
        limitations=LIMITS))
    folder=BASE/'inspected'; folder.mkdir()
    rows=[]
    for i,(key,path,first,last,claim) in enumerate(SPECS,1):
        original=ROOT/'docs/program/execution'/path
        lines=original.read_text().splitlines(); assert last<=len(lines)
        excerpt=folder/f'{i:02d}-{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        source=index[key]
        rows.append(dict(citation_key=key,source_identity=source.get('source_identity') or source['title'],
            version_date=source.get('version_date'),
            local_copy=ref(original,f'Inspected primary-text lines{first}-{last}'),
            inspected_excerpt=ref(excerpt,'Exact excerpt from preserved primary text'),supported_claims=[claim]))
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_commercial_synthesis',
        reviewer=dict(name='Codex author/coordinator',kind='author'),cutoff='2026-10-07',
        records=rows,inherited_source_records=[index[k] for k in sorted({s[0] for s in SPECS})],
        evidence=[ref(PRIOR,'721 unchanged audited records'),ref(Path(__file__),'Primary excerpt preparation')],
        limitations=LIMITS))
    cases=[
        ('Funding population/dose','JMP Pro and Stata documented static treatment routes',
         'Generate unequal assignment and heterogeneous strata; preserve ATE versus ATET, dose levels, centering, target weights and shared-calendar refusal.'),
        ('Discovery class','GeNIe pattern and BayesiaLab EQ',
         'Preserve unresolved class and source of orientation; distinguish fixed, forbidden and temporal restrictions; random DAG selection is a scenario only.'),
        ('Weak IV','Stata weak-IV postestimation',
         'Preserve disconnected/infinite/whole-line/empty sets, grid and test identity; distinguish model rejection from inadequate numerical bounds.'),
        ('Survival conversion','Stata stteffects and SAS EVENTCODE',
         'Retain entry, repeated rows, competing-event identity and effective options; reject unsupported delayed-entry conversion and ignored-option claims.'),
        ('Information-dependent decision','SMILE indexing parents and Stata static policy evaluation',
         'Preserve utility axes, history clock and feasible policies; recover all four exact values, then restrict to constant actions when history is late.'),
        ('Observation identity','Dataset/pattern conversion and local declared-clock contract',
         'Accept explicit consistent permutations; reject ambiguous coordinate maps and late fields; do not claim truthful owners or identities.'),
        ('Loaded models and interruption','Bayesia instance units and SMILE iteration time check',
         'Trace loading, retained occupancy, unload and effective completion; include interrupted searches and missing licenses; no throughput assumptions.'),
        ('Retirement and migration','Historical Azure Rank/Reward interface',
         'Retain event IDs, external history, action probabilities and reward timing; assess replacement behavior without assuming feature parity.')]
    write(BASE/'prototype-design.json',dict(status='prospective_design',
        question='Which commercial configuration preserves the same banking target and output before a paid trial?',
        cases=[dict(target=t,comparator=c,admission=a) for t,c,a in cases],
        stages=['Use already inspected public manuals and exact generated semantic cases to specify the purchasing unit.',
                'Build only the selected narrow adapter with a permitted original-language/runtime route.',
                'Freeze target, edition, mechanisms, seeds, assigned cases, clock, rights, resources, error tolerances and stopping rules before measured comparison.',
                'Keep failures, unsupported operations and human rework in assigned-request denominators; separate engine, wrapper and license failures.',
                'Use prospective costs and signal thresholds to justify a narrow paid trial; actual bank experiments and adoption remain later.'],
        paid_engine_executed=False,prototype_executed=False,bank_qualified=False,
        limitations=LIMITS))
    write(BASE/'omissions.json',dict(status='open_scoped_inputs',
        items=[dict(gap='Exact commercial edition/API operation matrix',
                    route='Inspect original feature markers and relevant edition manuals; obtain applicable binding terms later.',
                    blocks='Only claims of exact parity or permitted unattended deployment.'),
               dict(gap='Prices, support, recovery replicas, geographic and redistribution rights',
                    route='Specify purchasing unit and feasible instance schedule; request a scoped quote/terms after prototype merit.',
                    blocks='Actual procurement and economic superiority, not hypothetical comparison.'),
               dict(gap='Uninspected commercial panel, synthetic-control, transport and latent-discovery scope',
                    route='Continue primary-original census; separate vendor-supported commands from community add-ons.',
                    blocks='Exhaustive family coverage and claims of absence.'),
               dict(gap='Inaccessible policy originals including selected MATLAB, HUGIN and SAS material',
                    route='Acquire genuine accessible original or record omission; do not substitute an authored summary.',
                    blocks='Those source-specific technical claims only.'),
               dict(gap='Actual engine and bank transfer behavior',
                    route='Execute permitted prototype and matched trial; measure workload/rights/costs and independent truth separately.',
                    blocks='Runtime, statistical, bank or ROI qualification.'),
               dict(gap='Exact historical bytes at2026-10-07',
                    route='Use independently dated snapshot when available; retain later retrieval limit otherwise.',
                    blocks='As-of-cutoff byte identity claims.')],
        global_blocker=False,limitations=LIMITS))
    claims=[
        ('examples','Exact commercial acquisition, scheduling and information-parent references','project_derivation',BASE/'exact-results.json',
         ['Full-choice compatibility test has gross value7250, below perfect-information value10000; all costs and probabilities are stipulated.',
          'Exact cost/quote/regret and scheduling comparisons concern matched routes and the specified finite cases.',
          'History availability changes the feasible utility policy set; flattened scalar maximum is invalid.']),
        ('paths','Commercial purchasing units and source-specific semantic boundaries','software_primary_sources',BASE/'primary-review.json',
         ['Four banking journeys require target/edition/deployment/output purchasing units.',
          'Inspected primary texts distinguish graph classes, effective models, information parents, rights and loaded instances; no product superiority or uninspected absence is inferred.']),
        ('design','Prospective commercial semantic admission and acquisition design','project_design',BASE/'prototype-design.json',
         ['Eight public/generated admission cases precede paid trials and retain failed and unsupported requests.',
          'Unknown edition, rights, prices, inaccessible originals and bank transfer remain scoped omissions.'])]
    sources=[]
    for key,title,kind,path,supported in claims:
        sources.append(dict(integrated_citation_key='exec17_s8_'+key,title=title,
            author='Causal banking proposal',kind=kind,year=2026,
            source_identity='Authored source-bound synthesis, exact hypothetical law or prospective design',
            version_date='2026-10-17; inherited source versions and2026-10-07 cutoff retained',
            local_copy=ref(path,title),inspected_anchors=supported,supported_claims=supported,
            records=[ref(p,'Inspected primary, exact or scoped evidence') for p in
                     [BASE/'primary-review.json',BASE/'mathematics-review.json',BASE/'omissions.json',BASE/'plan.md',Path(__file__)]],
            limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',prior=ref(PRIOR,'721 unchanged source identities')))
    draft=(BASE/'chapter.tex').read_text()
    cited={k.strip() for g in re.findall(r'\\cite\w*\{([^}]+)\}',draft) for k in g.split(',')}
    assert cited <= set(index)|{s['integrated_citation_key'] for s in sources}
    assert draft.count(r'\chapter{')==1
    CHAPTER.parent.mkdir(parents=True);CHAPTER.write_text(draft)
    write(BASE/'precompile-author-review.json',dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=['Seventeen-area map retains uninspected scope as unknown; four journeys specify distinct purchasing units.',
                  'Primary-derived deployment/rights/clock distinctions are separated from documented capability and present local refusals.',
                  'Random completions, prespecified policies, ignored options, utility indices and interruption do not silently change targets.',
                  'All routes enter the compatibility comparison; costs fund remedy to equal acceptance and no paid engine run is claimed.',
                  'Initial arithmetic, scheduling, incomplete-map and builder failures remain in the development-failures record.',
                  'Inherited catalogs and generic economics receive no duplicate depth; actual rendered exclusive credit is still to be reviewed.'],
        evidence=[ref(p,'Reviewed source, exact or design input') for p in
                  [CHAPTER,BASE/'chapter.tex',BASE/'plan.md',BASE/'primary-review.json',BASE/'mathematics-review.json',
                   BASE/'source-audit.json',BASE/'prototype-design.json',BASE/'omissions.json',BASE/'development-failures/findings.json']],
        visual_acceptance=False,limitations=LIMITS))
    print(json.dumps(dict(primary_excerpts=len(rows),new_records=3,expected_total=724,scholarly_pdfs=188,visual_acceptance=False)))


if __name__=='__main__': main()
