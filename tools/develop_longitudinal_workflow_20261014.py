#!/usr/bin/env python3
"""Exact finite-law references and primary-text audit for the L5 workflow draft.

This executes project-authored enumeration, never an upstream causal engine.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/l5-workflow'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.L5/chapter.tex'
ADDITION = BASE / 'longitudinal-panel-observation.tex'
PRIOR = ROOT / 'docs/program/execution/2026-10-14/native-evaluation-reader/v3/reader/source-audit.json'
ref = shared.ref


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(obj, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def number(value):
    value = F(value)
    return {'exact': str(value), 'decimal': float(value)}


def bernoulli(value, probability):
    return probability if value else 1 - probability


def calculate():
    paths = []
    for a0 in (0, 1):
        risk = F(4, 5) if a0 == 0 else F(2, 5)
        for l1 in (0, 1):
            e1 = F(3, 4) if l1 else F(1, 2)
            retention = F(1, 2) if l1 else F(1)
            for a1 in (0, 1):
                p = F(1, 2) * bernoulli(l1, risk) * bernoulli(a1, e1)
                y = F(100 - 40*l1 + 2*a0 + (30*l1 - 8)*a1)
                paths.append((a0, l1, a1, p, y, e1, retention))
    assert sum(x[3] for x in paths) == 1
    rules = {'risk': (1, lambda l: l), 'none': (0, lambda l: 0),
             'all': (1, lambda l: 1)}
    values, raw, scores, normalized, retained, corrected = {}, {}, {}, {}, {}, {}
    for name, (first, second) in rules.items():
        risk = F(4, 5) if first == 0 else F(2, 5)
        direct = sum(bernoulli(l, risk) *
                     (100 - 40*l + 2*first + (30*l - 8)*second(l)) for l in (0, 1))
        weights = [F(2) / bernoulli(a1, e1) if a0 == first and a1 == second(l)
                   else F(0) for a0, l, a1, p, y, e1, r in paths]
        ipw = sum(p*w*y for w, (a0, l, a1, p, y, e1, r) in zip(weights, paths))
        assert direct == ipw
        assert sum(p*w for w, (a0, l, a1, p, y, e1, r) in zip(weights, paths)) == 1
        values[name] = direct
        matching = [x for x in paths if x[0] == first and x[2] == second(x[1])]
        raw[name] = sum(x[3]*x[4] for x in matching) / sum(x[3] for x in matching)
        score = []
        for a0, l, a1, p, y, e1, r in paths:
            m_g = F(100 - 40*l + 2*a0 + (30*l - 8)*second(l))
            score.append(F(2)*(m_g-direct) if a0 == first else F(0))
        assert sum(p*s for s, (a0, l, a1, p, y, e1, r) in zip(score, paths)) == 0
        scores[name] = score
        normalized[name] = sum(p*(w*(y-direct))**2 for w, (a0,l,a1,p,y,e1,r) in zip(weights, paths))
        retained[name] = sum(bernoulli(l, risk)*(F(1,2) if l else 1)*
                             (100-40*l+2*first+(30*l-8)*second(l)) for l in (0,1)) / \
                         sum(bernoulli(l, risk)*(F(1,2) if l else 1) for l in (0,1))
        total = F(0)
        for w, (a0,l,a1,p,y,e1,r) in zip(weights, paths):
            for observed in (0,1):
                total += p*bernoulli(observed,r)*w*observed/r*y
        assert total == direct
        corrected[name] = total
    variances = {key: sum(p*s*s for s, (a0,l,a1,p,y,e1,r) in zip(score,paths))
                 for key, score in scores.items()}
    contrast_score = [a-b for a,b in zip(scores['risk'],scores['none'])]
    variances['contrast'] = sum(p*s*s for s, (a0,l,a1,p,y,e1,r) in zip(contrast_score,paths))
    pooled_risk = F(3,5)
    pooled_value = sum(bernoulli(l,pooled_risk)*(102-18*l) for l in (0,1))
    assert values == {'risk': F(474,5), 'none': F(68), 'all': F(90)}
    assert raw['risk'] == 93 and raw['none'] == F(220,3)
    assert variances['contrast'] == F(16688,25)
    assert retained['risk'] == F(195,2)
    assert normalized['risk'] == F(31104,125)
    panel = [[F(100),F(107),F(119)], [F(100),F(102),F(108)], [F(100),F(102),F(104)]]
    treatment = [[F(0),F(1),F(1)], [F(0),F(0),F(1)], [F(0),F(0),F(0)]]
    residual = [[treatment[i][t]-sum(treatment[i])/3-
                 sum(treatment[j][t] for j in range(3))/3+
                 sum(sum(row) for row in treatment)/9 for t in range(3)] for i in range(3)]
    twfe = sum(residual[i][t]*panel[i][t] for i in range(3) for t in range(3)) / \
           sum(x*x for row in residual for x in row)
    contaminated = (panel[1][2]-panel[1][1])-(panel[0][2]-panel[0][1])
    effects = {'early_t1':(panel[0][1]-panel[0][0])-(panel[2][1]-panel[2][0]),
               'early_t2':(panel[0][2]-panel[0][0])-(panel[2][2]-panel[2][0]),
               'late_t2':(panel[1][2]-panel[1][1])-(panel[2][2]-panel[2][1])}
    assert list(effects.values()) == [5,15,4] and contaminated == -6 and twfe == F(9,2)
    strata = [(F(1,2),F(0),F(1)), (F(1,2),F(100),F(1,4))]
    ht_mean = sum(p*y for p,y,inclusion in strata)
    ht_second = sum(p*inclusion*(y/inclusion)**2 for p,y,inclusion in strata)
    respondent_mean = sum(p*inclusion*y for p,y,inclusion in strata) / sum(p*inclusion for p,y,inclusion in strata)
    prevalence, sensitivity, specificity = F(2,5),F(4,5),F(9,10)
    positive = sensitivity*prevalence+(1-specificity)*(1-prevalence)
    slope = sensitivity+specificity-1
    inverted = (positive+specificity-1)/slope
    assert ht_mean == 50 and ht_second-ht_mean**2 == 17500
    assert respondent_mean == 20 and positive == F(19,50) and inverted == prevalence
    return {'scope':'Exact project laws; independent-origin moments; no fitted estimator, interval study, upstream engine or bank data.',
            'path_count':len(paths), 'servicing':{
                'policy_values':{k:number(v) for k,v in values.items()},
                'risk_minus_none':number(values['risk']-values['none']),
                'contrast_decomposition':[number(x) for x in [2,16,F(44,5)]],
                'unweighted_matching_path_means':{k:number(v) for k,v in raw.items()},
                'unweighted_contrast':number(raw['risk']-raw['none']),
                'pooled_risk_value':number(pooled_value),
                'complete_case_policy_values':{k:number(v) for k,v in retained.items()},
                'inverse_retention_policy_values':{k:number(v) for k,v in corrected.items()},
                'centered_augmented_score_variances':{k:number(v) for k,v in variances.items()},
                'normalized_ipw_score_variances':{k:number(v) for k,v in normalized.items()}},
            'panel':{'observed':[[number(v) for v in row] for row in panel],
                'cohort_time_effects':{k:number(v) for k,v in effects.items()},
                'contaminated_late_vs_early':number(contaminated),
                'equal_cell_target':number(sum(effects.values())/3),
                'equal_first_exposure_target':number(F(effects['early_t1']+effects['late_t2'],2)),
                'twfe_coefficient':number(twfe),
                'alternative_early_t2_effect_with_untreated_shock3':number(12)},
            'observations':{'respondent_mean':number(respondent_mean),'framed_mean':number(ht_mean),
                'ht_per_unit_variance':number(ht_second-ht_mean**2),
                'positive_label_probability':number(positive),'inverted_prevalence':number(inverted),
                'known_error_prevalence_variance_coefficient':number(positive*(1-positive)/slope**2),
                'independent_branch_mean_variance':'1/B for two identical accounts per branch',
                'naive_independent_row_variance':'1/(2B)',
                'shared_calendar_mean_variance':'4+1/B'}}


def prepare():
    BASE.mkdir(parents=True,exist_ok=True)
    write(BASE/'plan-review.json',{
        'status':'pass','reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'operation_id':'TEXT.DRAFT.L5','plan':[
            'Preserve the existing workflow chapter and develop policy feedback, censoring, influence components and matched fixed-policy comparisons.',
            'Separate cohort/time panel targets from dynamic policies; derive valid and contaminated comparisons and a counterfactual ambiguity.',
            'Develop sampling-frame, measurement-error and shared-dependence limits with independent finite references.',
            'Compare a deterministic analyst workflow, point-treatment assistants and restricted longitudinal reuse; never transfer qualification by name.',
            'Audit primary texts, execute exact references, integrate and text-check a preserving reader, then review nonduplicate depth.'],
        'review_findings':[
            'All three pathways have distinct identification restrictions and useful diagnostics; panel data is not treated as a generic sequential-policy design.',
            'Known-nuisance exact moments are distinguished from fitted-estimator coverage; neither synthetic arithmetic nor static software review earns empirical qualification.',
            'Policy and retention clocks are explicit, and full costs remain inside the target.',
            'Target11 substantive pages is an allocation for depth review, not a typography or padding instruction.',
            'Independent software/source work remains eligible during Git publication; rendered acceptance alone needs a fresh image allowance.'],
        'next_action':'Execute independent rational enumeration, author connected substantive additions and inspect citation/notation/target consistency.'})
    result=calculate()
    write(BASE/'exact-oracle.json',result)
    entries={s['integrated_citation_key']:s for s in json.loads(PRIOR.read_text())['sources']}
    rereads=[('hernan2020','docs/literature/text/hernan2020.txt',14004,14095,
              'Ordering, causal conditions, removal of treatment factors and product treatment weights.'),
             ('callaway2021','docs/literature/text/callaway2021.txt',320,405,
              'Assumptions3–6: anticipation, alternative comparison groups, untreated trends and overlap.'),
             ('sequentialdr2018','docs/literature/text/sequentialdr2018.txt',185,235,
              'Definitions1–3 distinguish global and sequential robustness; OR is not identical to TM consistency.'),
             ('panelreview2024','docs/literature/text/panelreview2024.txt',95,178,
              'Data dimensions and assignment patterns distinguish methods; authors qualify claims against TWFE.'),
             ('sw_ltmle','docs/literature/raw/r3g_api_ltmle.txt',1,122,
              'Column chronology, binary action, absorbing event, outcome truncation/scaling and dynamic rules.')]
    sources=[]
    for key,path,first,last,claim in rereads:
        text=ROOT/path
        copy=entries[key].get('local_path') or entries[key]['local_copy']['path']
        assert core.sha(ROOT/copy) == entries[key].get('sha256',entries[key].get('local_copy',{}).get('sha256'))
        assert len(text.read_text().splitlines()) >= last
        sources.append({'citation_key':key,'identity_record':entries[key],
            'primary_copy':ref(ROOT/copy,'Authentic primary work or saved original software-source record'),
            'inspected_text':ref(text,f'Lines{first}–{last}'),
            'supported_claim':claim,'inspection_date':'2026-10-14','cutoff':'2026-10-07'})
    write(BASE/'primary-review.json',{'status':'pass','sources':sources,
        'preserved_prior_audit':ref(PRIOR,'514 preserved source identities'),
        'limits':['Rereading pre-cutoff sources is not a new frontier search. No ltmle or OCI execution.']})
    source={'integrated_citation_key':'exec14_workflow_oracle',
        'title':'Exact two-stage servicing, staggered-adoption and observation references',
        'author':'Causal banking proposal','kind':'project_derivation','year':2026,
        'source_identity':'Project-authored finite mechanisms, not empirical bank observations',
        'version_date':'2026-10-14', 'local_copy':ref(BASE/'exact-oracle.json','Eight history paths and exact alternative targets'),
        'inspected_anchors':['Servicing policy and matching paths; augmented/normalized score moments; cohort-time/within regression; observation inclusion/label inversion'],
        'supported_claims':['Exact policy values94.8/68/90 and biased matching/pooled/complete-case means.',
                            'Cohort effects5/15/4, contaminated contrast−6 and within coefficient4.5.',
                            'Respondent mean20 versus framed50; known-error prevalence.4 and branch/calendar dependence.'],
        'records':[{'local_copy':ref(Path(__file__),'Fraction enumeration and independent forward/weighted identities')}],
        'limitations':['Known project laws only; no nuisance estimation, confidence coverage, learned-policy guarantee or bank ROI.']}
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':[source],
        'primary_review':ref(BASE/'primary-review.json','Exact current rereads of preserved authentic works'),
        'prior':ref(PRIOR,'Predecessor integrated audit')})
    (BASE/'refs.bib').write_text('@misc{exec14_workflow_oracle,\n author={{Causal banking proposal}},\n title={Exact two-stage servicing, staggered-adoption and observation references},\n year={2026},\n note={Project-authored exact mechanisms; no bank data or fitted-estimator coverage}\n}\n')
    print(json.dumps({'plan_review':'pass','exact_reference':'pass','primary_rereads':len(sources)}))


def verify():
    assert calculate()==json.loads((BASE/'exact-oracle.json').read_text())
    for name in ['primary-review.json','source-audit.json']:
        shared.verify_refs(json.loads((BASE/name).read_text()))
    prior=json.loads(PRIOR.read_text())
    known={s['integrated_citation_key'] for s in prior['sources']}|{'exec14_workflow_oracle'}
    texts=[CHAPTER.read_text(),ADDITION.read_text()]
    keys={k.strip() for text in texts for group in re.findall(r'\\cite\{([^}]+)\}',text) for k in group.split(',')}
    assert keys<=known,keys-known
    assert CHAPTER.read_text().count('repair-v12/work/LA04/chapter-draft.tex')==1
    for expected in ['474','134','16688','17500','callaway2021','sequentialdr2018','sw_ltmle']:
        assert expected in ADDITION.read_text(),expected
    print(json.dumps({'exact_replay':'pass','citation_keys':len(keys),'addition_words':len(ADDITION.read_text().split())}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','verify'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else verify()
