#!/usr/bin/env python3
"""Preserve and separately check the recovered S4 references and primary text."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sympy as sp

import s4_examples_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT/'docs/program/execution/2026-10-17/s3/publication-v3/reader/source-audit.json'
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S4/chapter.tex'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Author review, not independent scientific acceptance.',
    'Stipulated exact finite laws and monetary amounts; no bank data, ROI observation or new upstream estimator run.',
    'Selected primary paths and versions do not establish whole-package equivalence, complete dependency rights or statistical qualification.',
    'The rdrobust revision uses an inherited UTC end-of-day query; strict Shanghai-cutoff identity is unresolved. Mutable Stata manual cutoff bytes remain unresolved.',
    'Public/generated comparisons are proposed; new statistical qualification requires a frozen prospective protocol.',
    'Rendered visual acceptance remains false; inherited image allowance is exhausted.'
]


def independent():
    """Symbolic identities and separate moment/LP certificates, not a new study."""
    saved = json.loads((BASE/'exact-results.json').read_text())
    assert examples.calculate() == saved
    e,q,t,t0,u,v,a,mu = sp.symbols('e q t t0 u v a mu')
    D = a*(1-q)**2+(1-a)*q**2
    N = D*(t+u-v)+a*(1-q)*(mu+t-(mu+t+u))-(1-a)*q*(mu-(mu+v))
    expect_D = sp.expand(e*D.subs(a,1)+(1-e)*D.subs(a,0))
    expect_N = sp.expand(e*N.subs(a,1)+(1-e)*N.subs(a,0))
    assert sp.expand(expect_D-e*(1-e)-(q-e)**2) == 0
    assert sp.expand(expect_N-t0*expect_D-e*(1-e)*(t-t0)-
                     ((q-e)**2*(t-t0)+(q-e)*(q*u+(1-q)*v))) == 0
    H,p=sp.symbols('H p', nonzero=True)
    y,b=sp.symbols('y b')
    generic_att = e/p*(t-t0+a/e*(y-b-t)-(1-a)/(1-e)*(y-b))+(a-e)/p*(t-t0)
    reduced_att = a/p*(y-b-t0)-(1-a)*e/(p*(1-e))*(y-b)
    assert sp.simplify(generic_att-reduced_att) == 0
    # At truth, the residual-regression score equals the full overlap IF;
    # conditional on binary A, the equalities hold separately for both arms.
    full = (e*(1-e)*(t-t0)+(1-2*e)*(a-e)*(t-t0)+(a-e)*y)/H
    residual = ((a-e)**2*(t-t0)+(a-e)*y)/H
    assert all(sp.simplify((full-residual).subs(a,x)) == 0 for x in [0,1])
    weights=[F(1,4),F(1,2),F(1,4)]
    prop=[F(1,10),F(1,2),F(9,10)]
    fitted=[F(1,5),F(1,2),F(4,5)]
    tau=list(map(F,[-4,4,20]))
    h=[x*(1-x) for x in prop]
    overlap_mass=sum(w*x for w,x in zip(weights,h))
    overlap_total=sum(w*x*z for w,x,z in zip(weights,h,tau))
    error2=sum(w*(x-z)**2 for w,x,z in zip(weights,fitted,prop))
    assert overlap_mass == F(17,100) and error2 == F(1,200)
    # True marginal outcome residual has zero conditional mean. In this law
    # mean(A-q)=0, so the fitted residual-regression intercept does not alter slope.
    assert sum(w*(x-z) for w,x,z in zip(weights,prop,fitted)) == 0
    residual_slope=overlap_total/(overlap_mass+error2)
    assert residual_slope == F(172,35)
    assert saved['weighting']['corrected_overlap_with_true_outcomes'] == '36/7'
    # Independent quotient-rule path derivatives from target numerator/mass.
    direction=[F(1,20),F(-1,10),F(1,20)]
    derivatives={}
    for name,hh,hp in [('ATT',prop,[F(1)]*3),
                       ('overlap',h,[1-2*x for x in prop])]:
        mass=sum(w*x for w,x in zip(weights,hh))
        total=sum(w*x*z for w,x,z in zip(weights,hh,tau))
        mass_dot=sum(w*x*z for w,x,z in zip(weights,hp,direction))
        total_dot=sum(w*x*z*r for w,x,z,r in zip(weights,hp,direction,tau))
        derivative=(total_dot*mass-total*mass_dot)/mass**2
        row=saved['weighting']['influence_paths'][name]
        assert str(derivative) == row['exact_target_derivative']
        var0,var1=map(F,row['fixed_and_full_variance'])
        extra=sum(w*x*x*z*(1-z)*(tt-total/mass)**2
                  for w,x,z,tt in zip(weights,hp,prop,tau))/mass**2
        assert var1-var0 == extra >= 0
        derivatives[name]=str(derivative)
    # Multiarm variances by conditional residual contribution, not cell enumeration.
    var0=F(4)/F(1,2); var1=var2=F(4)/F(1,4)
    cov=[[var0+var1,var0],[var0,var0+var2]]
    assert cov == [[24,8],[8,24]] and var1+var2 == 32
    # An LP dual bound certifies the optimum without invoking the vertex enumerator.
    w=[F(2,5),F(3,10),F(1,5),F(1,10)]
    gain=list(map(F,[3,6,8,11])); units=list(map(F,[1,1,2,4]))
    decision=[F(0),F(1),F(1,2),F(0)]
    shadow=F(4); budget=F(1,2)
    assert sum(x*z*d for x,z,d in zip(w,units,decision)) == budget
    assert all((d==0 if g<shadow*r else d==1 if g>shadow*r else True)
               for d,g,r in zip(decision,gain,units))
    value=sum(x*g*d for x,g,d in zip(w,gain,decision))
    bound=shadow*budget+sum(x*max(F(0),g-shadow*r) for x,g,r in zip(w,gain,units))
    assert value == bound == F(13,5)
    # Check the deterministic regret inequality over every binary policy pair
    # satisfying this same budget for a finite set of signed estimation errors.
    feasible=[d for d in product([F(0),F(1)],repeat=4)
              if sum(x*r*z for x,r,z in zip(w,units,d)) <= budget]
    true_best=max(feasible,key=lambda d:sum(x*g*z for x,g,z in zip(w,gain,d)))
    regret_cases=0
    for err in product([F(-2),F(0),F(2)],repeat=4):
        gh=[g+z for g,z in zip(gain,err)]
        estimated=max(feasible,key=lambda d:sum(x*g*z for x,g,z in zip(w,gh,d)))
        regret=sum(x*g*(d1-d2) for x,g,d1,d2 in zip(w,gain,true_best,estimated))
        envelope=sum(x*abs(z)*abs(d1-d2) for x,z,d1,d2 in zip(w,err,true_best,estimated))
        assert 0 <= regret <= envelope
        regret_cases+=1
    # Solve the local-linear normal equations symbolically for a quadratic mean.
    z,hb,b0,b1,kappa=sp.symbols('z hb b0 b1 kappa', real=True)
    G=sp.Matrix([[1,sp.Rational(1,2)],[sp.Rational(1,2),sp.Rational(1,3)]])
    rhs=sp.Matrix([sp.integrate(z**j*(b0+b1*hb*z+kappa*hb**2*z**2),(z,0,1))
                   for j in [0,1]])
    coef=sp.simplify(G.inv()*rhs)
    assert sp.expand(coef[0]-(b0-kappa*hb**2/6)) == 0
    for row in saved['threshold']['fuzzy_projection']:
        stage,band=F(row['receipt_jump']),F(row['bandwidth'])
        ratio=(8*stage-2*band**2)/(stage-band**2/12)
        assert str(ratio) == row['projected_ratio_USD']
    # Same discrete observations; distinct smooth response surfaces.
    for score in [F(-1),F(1)]:
        arm=int(score>=0)
        assert 10+4*arm == 12+2*score
    # Construct threshold-law-preserving witness potential-mean surfaces:
    # on each observed arm keep m_A(s)=10+2s+8A, then fill only the
    # unobserved arm to attain tau(s)=8 +/-6|s|.
    witnesses=[]
    for sign in [-1,1]:
        effects=[]
        for score in [F(-1,2),F(1,2)]:
            arm=int(score>=0); observed=10+2*score+8*arm
            effect=8+sign*6*abs(score)
            m0=observed-arm*effect; m1=m0+effect
            assert (m1 if arm else m0) == observed
            effects.append(effect)
        witnesses.append(sum(effects)/2)
    assert witnesses == [5,11]
    return dict(status='pass', reviewer=REVIEWER,
        method='Separate symbolic identities, quotient-rule moments, covariance components, LP dual certificate, finite regret check, normal equations and witness surfaces.',
        influence_path_derivatives=derivatives,
        overlap_regression=dict(assumptions='True marginal mean; symmetric clipped propensity errors have mean zero.',
            denominator=str(overlap_mass+error2),slope=str(residual_slope),
            corrected_ratio=saved['weighting']['corrected_overlap_with_true_outcomes'],
            same_population_target_at_truth=True,same_finite_fitted_algorithm=False),
        regret_cases_checked=regret_cases,transport_endpoint_witnesses=list(map(str,witnesses)),
        evidence=[ref(BASE/'exact-results.json','Recovered seven exact law families'),
                  ref(ROOT/'tools/s4_examples_20261017.py','Recovered reference enumeration'),
                  ref(Path(__file__),'Separate author calculations')],limitations=LIMITS)


def main():
    write(BASE/'mathematics-review.json',independent())
    prior=json.loads(PRIOR.read_text());verify_bindings(prior)
    index={r['integrated_citation_key']:r for r in prior['sources']}
    inspected=BASE/'inspected';inspected.mkdir(exist_ok=False)
    specifications=[
        ('dml2018','docs/literature/text/dml2018.txt',1787,1899,
         'Equations5.3/5.4 and Assumption5.1: distinct ATE/ATTE scores, control-only ATTE nuisance and conditional cross-fitting/product-rate asymptotics.'),
        ('grf2018','docs/literature/text/grf2018.txt',631,649,
         'Specification1: honesty, regular splits and subsampling restrictions; no universal learner guarantee.'),
        ('grf2018','docs/literature/text/grf2018.txt',749,783,
         'Theorem5 is conditional on Assumptions1-6 and forest specification; pointwise CLT is not an arbitrary selected-policy theorem.'),
        ('grf2018','docs/literature/text/grf2018.txt',1140,1172,
         'Section6.2 distinguishes binary unconfoundedness, forest algorithms and residualized moments.'),
        ('policy2021','docs/literature/text/athey2021.txt',367,460,
         'Assumptions1/2 and score11: identified binary decisions and nuisance-rate conditions.'),
        ('policy2021','docs/literature/text/athey2021.txt',534,687,
         'Assumptions3/4, cross-fitting and Theorem1: policy-class, overlap, noise and rate restrictions; approximate optimization allowed conditionally.'),
        ('doubleml2022','docs/literature/text/doubleml2022.txt',155,180,
         'Linear score architecture, model-specific nuisances, callable scores and customizable splitting are extension routes, not validation of an arbitrary new score.'),
        ('runtime_doubleml_scope','docs/literature/runtime-scope/doubleml-0.txt',336,388,
         'Selected installed0.11.4 score path adjusts propensity before weighted augmentation/callable score. Earlier runtime claim remains its selected ATE operation only.'),
        ('exec13_grf_rpath','docs/literature/raw/v12_gap4_grf_average.txt',125,155,
         'Target/method selection and early TMLE cluster/sample-weight rejections.'),
        ('exec13_grf_rpath','docs/literature/raw/v12_gap4_grf_average.txt',202,291,
         'All/AIPW score aggregation with clustered variance; other forest targets limited. Binary overlap branch uses residual lm with intercept and HC/cluster sandwich, ignoring method only after earlier guards.'),
        ('exec14_causalml_primary','docs/literature/raw/exec14_causalml_tlearner.txt',325,395,
         'Point mean over full prediction X but selected analytic variance uses pair subset; multiarm common target and covariance must be checked.'),
        ('exec14_causalpy_primary','docs/program/execution/2026-10-14/causalpy-reuse/causalpy__experiments__regression_discontinuity.py',175,253,
         'Finite-epsilon upper-treated minus lower-control design rows; bandwidth masks and small-sample warning do not prove a valid cutoff design.'),
        ('exec13_ivrd_rdrobust','docs/program/execution/2026-10-13/commercial-iv-rd/rdrobust_help.txt',1,88,
         'Selected Stata11.1.1 help declares local polynomial/bias-corrected procedures, fuzzy target and bandwidth/variance controls; Stata>=16. UTC-query cutoff qualification retained.')
    ]
    records=[]
    for i,(key,path,first,last,claim) in enumerate(specifications):
        original=ROOT/path;lines=original.read_text().splitlines()
        excerpt=inspected/f'{i+1:02d}-{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        record=dict(citation_key=key,version_date=index[key].get('version_date',index[key].get('version_status')),
            local_copy=ref(original,f'Lines{first}-{last}'),inspected_excerpt=ref(excerpt,'Inspected primary text'),
            supported_claims=[claim])
        if index[key].get('kind') == 'paper':
            record['genuine_pdf']={'path':index[key]['local_path'],'sha256':index[key]['sha256'],
                                   'anchor':'Genuine scholarly original; extracted-text range inspected'}
        records.append(record)
    keys=sorted({x[0] for x in specifications}|{'exec13_grf_native','exec13_ivrd_stata'})
    primary=dict(status='pass_for_bounded_synthesis',reviewer=REVIEWER,cutoff='2026-10-07',
        records=records,inherited_source_records=[index[k] for k in keys],
        evidence=[ref(PRIOR,'703 inherited records'),ref(Path(__file__),'Reread and identity binding')],
        limitations=LIMITS)
    write(BASE/'primary-review.json',primary)
    profiles=[
        ('target weighting',['DoubleML selected IRM ATE path','grf all/treated/overlap paths','exact reference'],
         'Fixed population versus assignment-dependent target, fitted clipping and known assignment are explicit.',
         'Exact targets, score/denominator and path derivative agree in the claimed regime; misspecification differences retained.'),
        ('heterogeneous actions',['CausalML predictions','grf scores','explicit common-population multiarm evaluator'],
         'One common covariate law, action/cost units, shared controls and declared resource class.',
         'Joint contrasts and covariance, feasible allocation and decision loss; separate evaluation for selected policies.'),
        ('threshold approximation',['CausalPy selected sharp path','selected rdrobust local polynomial path','exact projection reference'],
         'Continuous-support identification or declared discrete-score alternative, receipt versus assignment, fixed model and bandwidth.',
         'Cutoff, finite-epsilon and smoothed-projection quantities kept distinct; weak-stage and numerical failures preserved.'),
        ('licensed alternatives',['Stata licensed host plus separately licensed rdrobust','inspected official weak-IV reference'],
         'Exact host, package rights and version/cutoff identity; same scientific domain before comparison.',
         'Compare documented procedures and scoped statistical behavior; no claimed commercial victory or universal graph capability.')
    ]
    design=dict(status='proposed_not_executed',cutoff='2026-10-07',
        profiles=[dict(topic=t,candidates=c,admission=a,expected_semantics=o) for t,c,a,o in profiles],
        sequence=['Freeze each admitted revision, environment, complete rights and scientific target.',
            'Reproduce exact laws and deliberately changed targets before finite-sample comparisons.',
            'Register fresh sampling/assignment laws, splits, nuisance fits, interval algorithms, seed, all failures and fixed stopping rule for statistical claims.',
            'Compare common-target error, availability, interval behavior, resource feasibility, decision loss and full observed cost.',
            'Use permitted public covariates and generated potential outcomes; preserve the distinction between known generated truth and authentic bank validity.'],
        exact_reference=ref(BASE/'exact-results.json','Seven authored reference families'),
        primary_review=ref(BASE/'primary-review.json','Inspected versions and claims'),
        mathematics=ref(BASE/'mathematics-review.json','Separate algebra and witnesses'),
        external_inputs=['Bank assignment/confounding truth and threshold manipulability.',
            'Accepted feasible actions, resource capacity, precision/loss, costs and institutional adoption.'],
        limitations=LIMITS,bank_qualified=False,whole_census_closed=False)
    write(BASE/'prototype-design.json',design)
    rows=[]
    for key,title,kind,path,claims in [
        ('math','Target-dependent weights, shared-control decisions and threshold references','project_derivation',BASE/'exact-results.json',
         ['Seven stipulated exact law families; target influence derivative, overlap remainder, joint covariance, resource duality, threshold curvature, discrete nonidentification and sharp transport bounds.',
          'Separate symbolic/moment/dual/witness verification; residual regression and corrected ratio have the same true target/IF but differ under fitted nuisance error.']),
        ('paths','Effect and threshold software: selected target and uncertainty paths','software_primary_sources',BASE/'primary-review.json',
         ['Inspected DoubleML0.11.4, pinned grf, CausalML, CausalPy and rdrobust paths retain their distinct target, variance and method semantics.',
          'Prospective wrapping/adoption decisions are limited by target equivalence, rights, cutoff identity and runtime qualification.']),
        ('design','Public/generated common-target effect and threshold comparison','project_design',BASE/'prototype-design.json',
         ['Proposed exact and prospective statistical comparison with common targets, supported regimes and complete failure accounting.',
          'Public evidence can justify a prototype; it does not establish authentic bank assumptions or costs.'])]:
        rows.append(dict(integrated_citation_key='exec17_s4_'+key,title=title,author='Causal banking proposal',
            kind=kind,year=2026,source_identity='Project derivation/design or identity-bound primary-source review',
            version_date='2026-10-17; underlying sources and inherited cutoff limits in primary review',
            local_copy=ref(path,title),inspected_anchors=claims,supported_claims=claims,
            records=[ref(BASE/'mathematics-review.json','Separate author verification'),
                     ref(BASE/'primary-review.json','Underlying original identities and claims'),
                     ref(Path(__file__),'Preparation procedure')],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=rows,prior=ref(PRIOR,'703 preserved source records'),cutoff='2026-10-07'))
    write(BASE/'recovery-work-record.json',dict(
        observed=['Both program checks pass; saved active operation is TEXT.DRAFT.S4.',
            'The899-page canonical reader, reviewed S4 plan, exact-results and enumerator survived.',
            'A bounded metadata probe assumed every legacy record had a title and raised KeyError; no mutation occurred. It was corrected to use optional fields.'],
        repair='Resume existing active operation; preserve exact results and add separate verification. Use bounded text output; no image previews.',
        next_action='Draft connected S4 argument, compile a preserving successor and review its exclusive substantive depth.',
        evidence=[ref(BASE/'plan.md','Reviewed saved continuation'),ref(BASE/'mathematics-review.json','Recomputed evidence')],
        visual_acceptance=False))
    print(json.dumps(dict(mathematics='pass',primary_excerpts=len(records),new_citations=len(rows),
                          exact_families=7,visual_acceptance=False)))


if __name__ == '__main__':
    main()
