"""Reconstruct release-critical results from retained data without redrawing studies."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import hashlib,json,math,platform,statistics
import numpy as np
import scipy
from scipy.stats import t,norm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/release/2026-10-29'
bindings={}
def raw(name):
    value=(ROOT/name).read_bytes();bindings[name]=hashlib.sha256(value).hexdigest();return value
def read(name):return json.loads(raw(name))
def close(a,b):assert np.allclose(a,b,atol=1e-7,rtol=1e-10),(a,b)

def deposit():
    base='docs/developmental-rewrite/2026-10-29/'
    plan=read(base+'example-plan.json');previous=read(base+'example-results.json')['report']
    rows=[line.split(',') for line in raw(base+'generated-deposit-data.csv').decode().splitlines()[1:]]
    cells=defaultdict(list)
    for x,a,y in rows:cells[int(x),int(a)].append(float(y))
    assert len(rows)==plan['sample_size']==8000
    effect=radius=0.;counts={}
    for x,weight in enumerate(plan['target_weights']):
        for a in [0,1]:
            values=cells[x,a];mean=statistics.mean(values)
            half=t.isf(plan['alpha']/8,len(values)-1)*statistics.stdev(values)/math.sqrt(len(values))
            effect+=weight*(2*a-1)*mean;radius+=weight*half;counts[f'{x},{a}']=len(values)
    interval=[effect-radius,effect+radius];slope=plan['margin_per_year']-plan['rate_increment_per_year']
    intercept=-plan['rate_increment_per_year']*plan['baseline_balance_gbp']-plan['direct_cost_gbp']
    net=slope*effect+intercept;net_interval=sorted(slope*v+intercept for v in interval)
    close(effect,previous['effect_gbp']);close(interval,previous['interval_gbp'])
    close(net,previous['net_annual_gbp_per_household']);close(net_interval,previous['net_interval_gbp'])
    assert [format(v,',.2f') for v in [effect,*interval,net,*net_interval]]==['1,183.47','1,128.34','1,238.60','2.55','1.03','4.06']
    return dict(n=len(rows),counts=counts,balance_effect=effect,balance_interval=interval,contribution=net,contribution_interval=net_interval,scope='Same retained generated sample, independently aggregated; no new calibration or bank data')

def public_experiment():
    base='docs/scientific-gap-closure/2026-10-29/'
    plan=read(base+'study-plan.json');previous=read(base+'study-results.json')
    arrays=[np.array([[float(v) for v in line.split()] for line in raw(name).decode().splitlines() if line.strip()]) for name in plan['data']]
    assert [len(a) for a in arrays]==[185,260]
    data=np.concatenate(arrays);assert data.shape==(445,10) and np.all(data[:185,0]==1) and np.all(data[185:,0]==0)
    a,y=data[:,0],data[:,-1];covariates=data[:,1:9];x=(covariates-covariates.mean(0))/covariates.std(0,ddof=1);methods=[]
    for method in ['unadjusted','common_slope','interacted']:
        columns=[np.ones(len(y)),a]
        if method!='unadjusted':columns += [x[:,j] for j in range(x.shape[1])]
        if method=='interacted':columns += [a*x[:,j] for j in range(x.shape[1])]
        design=np.column_stack(columns)
        # QR triangular solves independently reconstruct the original SVD fit.
        q,r=np.linalg.qr(design,mode='reduced');beta=np.linalg.solve(r,q.T@y)
        leverage=np.sum(q*q,axis=1);residual=y-design@beta;inverse=np.linalg.solve(r,q.T)
        hc2=(inverse*(residual**2/(1-leverage)))@inverse.T;hc3=(inverse*(residual**2/(1-leverage)**2))@inverse.T
        se=math.sqrt(hc2[1,1]);interval=[beta[1]-norm.isf(.025)*se,beta[1]+norm.isf(.025)*se]
        old=next(v for v in previous['methods'] if v['method']==method)
        close(beta[1],old['estimate']);close(hc2[1,1],old['variance']);close(interval,old['interval']);close(math.sqrt(hc3[1,1]),old['hc3_standard_error'])
        methods.append(dict(method=method,estimate=float(beta[1]),variance=float(hc2[1,1]),interval=interval,net_at_cost_1000=[float(v-1000) for v in interval]))
    for decision in previous['decisions']:
        m=next(v for v in methods if v['method']==decision['method']);cost=decision['illustrative_cost']
        close(m['estimate']-cost,decision['net_point']);close([v-cost for v in m['interval']],decision['net_interval'])
        assert (m['interval'][0]>cost)==decision['lower_bound_supports_spending']
    return dict(n=445,methods=methods,scope='Retained public experimental subset; QR reconstruction checks arithmetic, not assignment or transport assumptions')

def exact_journeys():
    prior=read('docs/developmental-rewrite/2026-10-29/example-results.json')['exact_checks'];values=[];weighted=[]
    for policy in [0,1]:
        value=F(0);ipw=F(0)
        for l0 in [0,1]:
            p1=F(1,10)+F(1,2)*l0+F(1,5)*policy
            for l1 in [0,1]:value+=F(1,2)*(p1 if l1 else 1-p1)*(20+7*policy+10*l1+6*l0)
            e0=F(1,5)+F(3,5)*l0
            for a0 in [0,1]:
                p1=F(1,10)+F(1,2)*l0+F(1,5)*a0
                for l1 in [0,1]:
                    e1=F(3,20)+F(1,2)*l1+F(1,10)*a0
                    for a1 in [0,1]:
                        prop=(e0 if a0 else 1-e0)*(e1 if a1 else 1-e1);probability=F(1,2)*(p1 if l1 else 1-p1)*prop
                        if a0==a1==policy:ipw+=probability*(20+3*a0+4*a1+10*l1+6*l0)/prop
        values.append(value);weighted.append(ipw)
    assert values==weighted==[F(53,2),F(71,2)];close([float(v) for v in values],prior['servicing']['gformula_means'])
    recorded=F(61)/F(45,100)-F(59)/F(55,100);assert recorded==F(2800,99)
    close(float(recorded),prior['observation']['recorded_contrast']);close([float(recorded-35),5],[prior['observation']['net_recorded'],prior['observation']['net_corrected']])
    sigma=np.array(prior['discovery']['covariance']);effects=[]
    for order in [(0,1,2),(1,0,2),(2,1,0)]:
        perm=sigma[np.ix_(order,order)];chol=np.linalg.cholesky(perm)
        structural=np.eye(3)-np.diag(np.diag(chol))@np.linalg.inv(chol)
        translated=np.zeros((3,3));translated[np.ix_(order,order)]=structural
        response=np.linalg.solve(np.eye(3)-translated,np.eye(3));effects.append(float(response[2,0]))
        variance=(np.eye(3)-translated)@sigma@(np.eye(3)-translated).T
        close(variance,np.diag(np.diag(variance)));assert np.all(np.diag(variance)>0)
        close(response@variance@response.T,sigma)
    close(effects,prior['discovery']['effects'])
    return dict(servicing_gformula=[str(v) for v in values],servicing_ipw=[str(v) for v in weighted],servicing_net=str(values[1]-values[0]-4),observation_recorded=str(recorded),observation_corrected='40',graph_effects=effects,graph_net_values=[v*.25*1000-60 for v in effects],scope='Exact or independently reconstructed stipulated laws; no fitted bank effect')

def repeated_studies():
    result={}
    for stem,keys in [('observation',['scenario','rate','method']),('policy-uncertainty',['scenario','policy','target','method'])]:
        base='docs/scientific-gap-closure/2026-10-29/';rows=read(base+stem+'-replications.json');old=read(base+stem+'-results.json');groups=defaultdict(list)
        for row in rows:groups[tuple(row[k] for k in keys)].append(row)
        checks=[]
        for summary in old['scenarios']:
            group=groups[tuple(summary[k] for k in keys)];n=len(group);count=sum(bool(v['covered']) for v in group)
            close(count/n,summary.get('coverage',summary.get('coverage_all_requests')))
            widths=[v['interval'][1]-v['interval'][0] for v in group] if stem=='policy-uncertainty' else [v['width'] for v in group if v.get('available') and v.get('width') is not None]
            close(statistics.mean(widths),summary['mean_width'])
            checks.append({**{k:summary[k] for k in keys},'n':n,'covered':count,'mean_width':statistics.mean(widths)})
        result[stem]=dict(records=len(rows),summaries=len(checks),checks=checks)
    return result

def corrected_width():
    correction=read('docs/writing-repair/2026-10-29/numeric-corrections.json')['corrections'][0]
    value=raw(correction['journal']);assert hashlib.sha256(value).hexdigest()==correction['journal_sha256'];widths=[];keys=set()
    for line in value.decode().splitlines():
        row=json.loads(line)
        if not row.get('key','').startswith(correction['request_prefix']):continue
        assert row['key'] not in keys;keys.add(row['key']);lo,hi=row['result']['methods'][correction['method']]['interval'];widths.append(hi-lo)
    assert len(widths)==600;median=statistics.median(widths);assert median==correction['median_width_usd'] and format(median/1e6,'.3f')=='1.341'
    return dict(requests=600,median_width_usd=median,printed_millions='1.341',scope='Retained corrected result; no new requests')

def measurement_floor():
    previous=read('docs/scientific-gap-closure/2026-10-29/measurement-results.json')
    cases=[];tau=-F(1,5)
    for row in previous['rows']:
        m=row['readings'];rho=F(row['error_correlation']);s=F(1)
        # Exchangeable error covariance has a mean direction and m-1 contrasts.
        mean_eigenvalue=s*(1+(m-1)*rho);contrast_eigenvalue=s*(1-rho)
        assert mean_eigenvalue>0 and contrast_eigenvalue>0
        error_mean=mean_eigenvalue/m
        # Cramer's rule on Cov(A,Wbar), independently of the full-system solver.
        determinant=2*(1+error_mean)-1
        beta=((2*tau+1)*(1+error_mean)-(tau+1))/determinant
        assert beta==F(row['adjusted_coefficient'])
        assert error_mean==F(row['error_variance'])
        close(float(beta),row['independent_covariance_solution'])
        cases.append(dict(readings=m,rho=str(rho),mean_eigenvalue=str(mean_eigenvalue),contrast_eigenvalue=str(contrast_eigenvalue),coefficient=str(beta)))
    boundary=[]
    for rho in [F(0),F(1,5)]:
        minimum=next(m for m in range(1,100) if rho+(1-rho)/m<F(1,3))
        assert minimum==({F(0):4,F(1,5):7}[rho])
        boundary.append(dict(rho=str(rho),first_correct_sign=minimum))
    # A fixed negative correlation cannot define arbitrarily long sequences.
    assert 1+(3-1)*F(-1,2)==0 and 1+(4-1)*F(-1,2)<0
    assert F(1)-F(1)==0  # Perfectly duplicated readings have singular contrasts.
    assert tau+F(1,2)/(1+2*F(1,2))==F(1,20)
    return dict(cases=cases,sign_boundaries=boundary,domain='s>0 and 0<=rho<1 give positive covariance eigenvalues for every finite m; fixed negative rho fails for sufficiently large m; rho=1 has singular contrasts.',scope='Exact retained project law; no language-model observations or empirical qualification')

def investment_account():
    previous=read('docs/derivations/economics.json');a=previous['assumptions'];r=F(str(a['discount_rate']));h=a['horizon_years']
    annuity=sum((1+r)**(-t) for t in range(1,h+1));close(float(annuity),previous['annuity'])
    e={k:F(str(v)) for k,v in a['expert'].items()};p={k:F(str(v)) for k,v in a['platform'].items()}
    initial_gap=p['initial']-e['initial'];shared_gap=p['annual_shared']-e['annual_shared'];saving=e['per_completed_study']-p['per_completed_study']
    threshold=(initial_gap/annuity+shared_gap)/saving
    close(float(threshold),previous['constant_annual_study_threshold'])
    costs=[]
    for row in previous['scenarios']:
        values=[]
        for inputs in [e,p]:
            values.append(inputs['initial']+sum((inputs['annual_shared']+inputs['per_completed_study']*n)/(1+r)**t for t,n in enumerate(row['completed_studies'],1)))
        extra=max(F(0),(values[1]-values[0])/annuity)
        for v,key in zip([*values,values[0]-values[1],extra],['expert_present_cost','platform_present_cost','platform_cost_saving','additional_constant_annual_decision_benefit_to_break_even']):close(float(v),row[key])
        costs.append(dict(scenario=row['scenario'],expert=float(values[0]),platform=float(values[1]),saving=float(values[0]-values[1]),annual_extra=float(extra)))
    close(float(2*threshold),previous['sensitivity']['half_per_study_saving_threshold'])
    close(float((initial_gap/annuity+2)/saving),previous['sensitivity']['annual_shared_gap_2m_threshold'])
    budget=previous['pilot_budget'];staff=budget['fte']*budget['months']*budget['loaded_person_month_usd'];total=(staff+budget['compute_usd'])*(1+F(str(budget['contingency_rate'])))
    assert staff==budget['staff_usd'] and total==budget['total_usd']==1140000
    return dict(annuity=float(annuity),annual_threshold=float(threshold),scenarios=costs,broader_construction_tranche_usd=int(total),scope='Exact rational reconstruction of retained stipulated costs; the initial matched analyst comparison remains separately unpriced. No observed labour saving, vendor quotation or bank ROI.')

def delegate_contracts():
    previous=read('docs/release/2026-10-29/source-delegates-015/exact-witnesses.json')
    assert previous['status']=='pass'
    # Independent two-point symmetry calculation: unit signed margins require
    # weight magnitude one, hence equal dual multipliers 1/(1^2+1^2).
    dual=1/(F(-1)**2+F(1)**2)
    results=[]
    for row in previous['orientation']:
        first=F(row['rows'][0]);slope=first
        coefficients=[dual,-dual]
        expected=[1 if slope*x>0 else -1 for x in row['rows']]
        assert coefficients==list(map(F,row['stipulated_coefficients']))
        assert F(row['reconstructed_weight'])==slope and F(row['reconstructed_bias'])==0
        assert expected==row['predictions']
        assert (expected==row['rows'])==row['matches_original_labels']
        results.append(dict(first_label=int(first),dual=str(dual),slope=str(slope),predictions=expected))
    # Reconstruct normalized weights through posterior odds, independently of
    # the original vector-normalization implementation.
    likelihood=previous['clustering']['transition_likelihoods']
    a,b=[list(map(F,x)) for x in likelihood]
    odds=(a[0]/b[0])*(a[1]/b[1]);stationary_odds=(a[0]/b[0])**2
    posterior=[odds/(1+odds),1/(1+odds)]
    stationary=[stationary_odds/(1+stationary_odds),1/(1+stationary_odds)]
    assert posterior==list(map(F,previous['clustering']['correct_posterior']))
    assert stationary==list(map(F,previous['clustering']['stationary_posterior']))
    prior=list(map(F,previous['clustering']['prior']));like=list(map(F,previous['clustering']['likelihood']))
    assert like[1]>like[0] and prior[0]/prior[1]>like[1]/like[0]
    assert [prior[i]*like[i] for i in range(2)]==list(map(F,previous['clustering']['mixture_products']))
    return dict(orientation=results,transition_posterior=list(map(str,posterior)),stationary_posterior=list(map(str,stationary)),likelihood_only_choice=1,prior_weighted_choice=0,scope='Independent rational reconstruction of authored source-contract witnesses, not numerical vendor execution or Java clustering.')

def flexbcf_contracts():
    previous=read('docs/release/2026-10-29/source-flexbcf-016/exact-witnesses.json')
    a=previous['scale'];values=list(map(F,a['raw_draw']))
    # Independently restore each customer before taking the cohort mean.
    restored=[F(a['outcome_sd'])*v for v in values]
    effect=sum(restored)/F(a['customers'])
    wrong=sum(x+F(a['outcome_mean']) for x in restored)/len(restored)
    assert effect==F(a['correct_effect'])==3
    assert wrong==F(a['wrong_restoration'])==103
    cost=F(a['cost'])
    assert effect-cost==F(a['correct_margin'])==-2
    assert wrong-cost==F(a['wrong_margin'])==98
    assert wrong+F(a['outcome_shift'])==F(a['shifted_wrong_restoration'])
    rows=previous['row_alignment']
    controls=[x for x,z in zip(rows['original_ids'],rows['treatment']) if z==0]
    treated=[x for x,z in zip(rows['original_ids'],rows['treatment']) if z==1]
    assert controls+treated==rows['control_first_ids'] and treated==rows['treated_only_ids']
    assert [rows['original_ids'][i] for i in rows['joint_order_zero_based']]==controls+treated
    for n,value in previous['small_progress_defaults'].items():
        assert int(n)<10 and value==0
    return dict(correct_effect=str(effect),incorrect_restoration=str(wrong),
                correct_margin=str(effect-cost),incorrect_margin=str(wrong-cost),
                aligned_ids=controls+treated,scope='Independent per-customer rational reconstruction of authored scale and row-identity witnesses; no upstream execution.')

def parallel_trends():
    previous=read('docs/release/2026-10-29/source-flexpaper-017/exact-witnesses.json')
    rows=previous['rows']
    # Independent first-difference computation, not post-gap subtraction.
    changes=[F(r['observed_post'])-F(r['pre']) for r in rows]
    effect=changes[1]-changes[0]
    increments=[F(r['untreated_post'])-F(r['pre']) for r in rows]
    assert increments==[F(3),F(3)] and changes==[F(3),F(5)]
    assert sum(F(r['probability']) for r in rows)==1
    assert all(F(r['treated_post'])-F(r['untreated_post'])==effect for r in rows)
    assert effect==F(previous['identified_effect'])==2
    pre=F(rows[1]['pre'])-F(rows[0]['pre'])
    post=F(rows[1]['observed_post'])-F(rows[0]['observed_post'])
    assert pre==F(previous['pre_gap'])==4 and post==F(previous['post_gap'])==6
    cost=F(previous['action_cost'])
    assert effect-cost==F(previous['correct_margin'])==-1
    assert post-cost==F(previous['post_gap_margin'])==3
    return dict(untreated_increments=list(map(str,increments)),observed_changes=list(map(str,changes)),
                effect=str(effect),correct_margin=str(effect-cost),post_gap_margin=str(post-cost),
                scope='Independent first-difference reconstruction of stipulated branch law, not empirical replication or native qualification.')

def financing_equivalence():
    previous=read('docs/twelve-hour-closure/2026-10-29/formulation-attempt-1/results.json')
    witness=read('docs/release/2026-10-29/source-closure-018/exact-witnesses.json')
    # Reconstruct by conditional mixtures. This does not invoke the original
    # exogenous-state enumerator or execute either reported language model.
    p=F(1,5);discordance=p*(1-p)+(1-p)*p
    risk={0:1-discordance,1:discordance}
    joint={(f,y):F(1,2)*(risk[f] if y else 1-risk[f]) for f in [0,1] for y in [0,1]}
    for result in [previous,witness]:
        assert joint=={(x['F'],x['Y']):F(x['probability']) for x in result['observed_joint']}
    assert sum(joint.values())==1
    for f in [0,1]:
        assert risk[f]==F(previous['observational_risks']['F'+str(f)])
        assert risk[f]==F(previous['interventions']['causal']['do_'+str(f)])
        assert F(1,2)==F(previous['interventions']['confounded']['do_'+str(f)])
    relief=risk[0]-risk[1]
    assert relief==F(9,25)==F(witness['relief_effects']['causal'])
    assert F(witness['relief_effects']['confounded'])==0
    return dict(observed_joint=[str(joint[f,y]) for f in [0,1] for y in [0,1]],
                risk_unconstrained=str(risk[0]),risk_constrained=str(risk[1]),
                relief_effects={'confounded':'0','causal':str(relief)},
                scope='Retained stipulated binary laws, identical transcript argument and independent closed-form arithmetic; not sharp bounds, a live-model test or a bank effect.')

def temporal_contracts():
    previous=read('docs/release/2026-10-29/source-dbn-019/exact-witnesses.json')
    outcomes={}
    # Closed-form binary prediction and Bayes odds, independently of the
    # latent-transition mass enumeration in the retained witness.
    for name, q0, q1 in [('A',F(1,10),F(4,5)),('B',F(2,5),F(9,10))]:
        forecast=q0+(q1-q0)/4
        odds=4*forecast/(1-forecast)
        posterior=odds/(1+odds)
        net=14*posterior-10
        old=previous['transition']['outcomes'][name]
        assert forecast==F(old['forecast']) and posterior==F(old['posterior'])
        assert net==F(old['stipulated_action_net'])
        outcomes[name]=dict(forecast=str(forecast),posterior=str(posterior),net=str(net))
    assert F(outcomes['A']['net'])<0<F(outcomes['B']['net'])
    # Analytical potential-outcome and selected-population means.
    tau=100*F(1,2)
    retained_control_mean=F(100)
    retained_treated_mean=F(100)
    selected=retained_treated_mean-retained_control_mean
    for key,value in [('population_effect',tau),('retained_contrast',selected),
                      ('population_net',tau-20),('retained_net',selected-20)]:
        assert value==F(previous['cleaning'][key])
    masses=list(map(F,previous['ternary']['probabilities']))
    assert masses[0]==F(1,5) and sum(masses[1:])==F(4,5)
    assert previous['dummy']['sequence_count']*previous['dummy']['per_sequence_return']==previous['dummy']['inferred_last_iteration_sum']==40000
    return dict(transition=outcomes,cleaning_effect=str(tau),cleaned_contrast=str(selected),
                cleaning_net=str(tau-20),cleaned_net=str(selected-20),
                scope='Exact retained authored laws reconstructed by binary Bayes odds and population/selection means; no downloaded-code execution or bank qualification.')

def survival_contracts():
    previous=read('docs/release/2026-10-29/source-survival-022/exact-witnesses.json')
    # Independent likelihood-score construction from observed exits/entries.
    exposure=F(0);origin=F(0);events=0
    for l,t,event in previous['delayed_entry']['records']:
        exposure+=F(t)-F(l);origin+=F(t);events+=event
    rates=[F(events)/exposure,F(events)/origin]
    assert rates==[F(1,3),F(1,11)]
    close([100*(1-np.exp(-float(rate))) for rate in rates],previous['delayed_entry']['next_month_loss'])
    # The algebraic identified combination independently reconstructs the
    # witness that used time and hazard multipliers separately.
    shape=previous['weibull_ridge']['shape'];scale=F(previous['weibull_ridge']['scale'])
    pairs=[list(map(F,p)) for p in previous['weibull_ridge']['exp_alpha_beta']]
    factors=[a**(shape-1)*b for a,b in pairs]
    assert factors==[F(3),F(3)]
    for row in previous['weibull_ridge']['evaluations']:
        t=F(row['t']);x=row['x'];factor=factors[0]**x
        assert (t/scale)**shape*factor==F(row['H'])
        assert F(shape)*t**(shape-1)/scale**shape*factor==F(row['hazard'])
    # Verify the exact ridge direction annihilates a two-coefficient
    # information contribution for every shared covariate at fixed shape.
    v=np.array([shape-1.,1.]);null=np.array([1.,-(shape-1.)])
    close(np.outer(v,v)@null,[0.,0.])
    units=previous['loglogistic_units'];close(np.exp([units['mu_month'],units['mu_day']]),[.5,15.])
    assert units['mu_month']<0<units['mu_day']
    # Root inversion and numerical quadrature independent of analytic witness.
    from scipy.optimize import brentq
    from scipy.integrate import quad
    tail=previous['piecewise_tail'];rate=1/5
    quantile=brentq(lambda t:1-np.exp(-rate*t)-.9,0,100)
    close(quantile,tail['correct_quantile'])
    full=quad(lambda t:np.exp(-rate*t),0,np.inf)[0]
    restricted=quad(lambda t:np.exp(-rate*t),0,1)[0]
    close([100*full,100*restricted],[tail['expected_cashflow'],tail['one_month_restricted_cashflow']])
    assert tail['quantile_branch']==1 and quantile>11
    output=previous['output_meaning'];close(100*(1-np.exp(-2)),output['expected_loss'])
    return dict(entry_rates=list(map(str,rates)),identified_factor=str(factors[0]),
                information_null_direction=null.tolist(),tail_quantile=quantile,
                full_receipts=100*full,restricted_receipts=100*restricted,
                scope='Independent likelihood score, identified-factor algebra, root inversion and quadrature; no downloaded code executed.')

def influence_contracts():
    previous=read('docs/release/2026-10-29/source-ife-023/exact-witnesses.json')
    # Reconstruct the ratio influence by differentiating a categorical
    # empirical distribution, independently of the witness's weighted loop.
    weighted=previous['weighted_location']
    z=np.array(list(map(float,weighted['pseudo_outcomes'])))
    w=np.array([float(F(v)) for v in weighted['weights']])
    p=np.ones(len(z))/len(z)
    numerator=p@(w*z);denominator=p@w;theta=numerator/denominator
    derivative=(w*z*denominator-numerator*w)/denominator**2
    close(derivative,[float(F(v)) for v in weighted['centered_influence']])
    close(np.var(derivative,ddof=1)/len(z),float(F(weighted['centered_variance'])))
    close(np.var(w*z,ddof=1)/len(z),float(F(weighted['uncentered_variance'])))
    close(np.var(w*(z+100),ddof=1)/len(z),float(F(weighted['shifted_uncentered_variance'])))
    for j in range(len(z)):
        direction=np.eye(len(z))[j]-p
        eps=1e-6
        value=lambda q:(q@(w*z))/(q@w)
        close((value(p+eps*direction)-value(p-eps*direction))/(2*eps),derivative[j])
    close(np.var(2*w,ddof=1)/len(z),float(F(previous['constant_contrast']['uncentered_weighted_variance'])))
    cluster=previous['unequal_clusters']
    incidence=np.array([[1.,0,0,0],[0,1,1,1]])
    outcomes=np.array(list(map(float,cluster['pseudo_outcomes'])))
    n=len(outcomes);K=len(incidence)
    for name,values in [('centered',outcomes-outcomes.mean()),('uncentered',outcomes),('shifted_uncentered',outcomes+100)]:
        grouped=(K/n)*(incidence@values)
        close(np.var(grouped,ddof=1)/K,float(F(cluster[name+'_variance'])))
    rows=previous['row_alignment']
    a=np.array(list(map(float,rows['first_influence'])))
    b=np.array(list(map(float,rows['reversed_second'])))
    covariance=np.cov(np.stack([a,b]),ddof=1)/len(a)
    close(np.array([1,-1])@covariance@np.array([1,-1]),float(F(rows['reversed_difference_variance'])))
    scales=previous['contrast_scales'];ratio=scales['ratio'];s=scales['log_standard_error']
    interval=norm.interval(.95,loc=np.log(ratio),scale=s)
    close(np.exp(interval),scales['transformed_log_interval'])
    close(norm.interval(.95,loc=ratio,scale=ratio*s),scales['direct_ratio_wald_interval'])
    return dict(weighted_ratio=theta,ratio_derivative=derivative.tolist(),
                centered_variance=weighted['centered_variance'],shifted_uncentered_variance=weighted['shifted_uncentered_variance'],
                unequal_cluster_variances={name:cluster[name] for name in ['centered_variance','uncentered_variance','shifted_uncentered_variance']},
                log_interval_exp=np.exp(interval).tolist(),
                scope='Independent quotient derivative, centered finite difference, matrix aggregation/covariance and normal quantile reconstruction; no upstream execution or coverage claim.')

def fitting_contracts():
    previous=read('docs/release/2026-10-29/source-pygformula-025/exact-witnesses.json')
    from scipy.optimize import root
    from scipy.special import expit
    records=previous['restrictions']['records'];fits={}
    # Independently solve both logistic score equations rather than using the
    # witness's conditional-frequency formula. No upstream package is imported.
    for name in ['restricted','unrestricted']:
        rows=[r for r in records if name=='unrestricted' or r['eligible']]
        x=np.array([[1.,r['x']] for r in rows]);y=np.array([r['z'] for r in rows])
        score=lambda beta:x.T@(y-expit(x@beta))
        solved=root(score,np.zeros(2));assert solved.success
        close(score(solved.x),[0,0])
        prob=expit(np.array([[1.,0],[1.,1]])@solved.x)
        old=previous['restrictions']['fits'][name]
        close(prob,[float(F(v)) for v in old['conditional_probabilities']])
        fitted=expit(x@solved.x)
        information=x.T@((fitted*(1-fitted))[:,None]*x)
        assert np.all(np.linalg.eigvalsh(information)>0)
        close(np.linalg.det(information),float(F(old['information_determinant'])))
        # Enumerate the four equal target cells, including two forced zeros.
        rewards=[100*prob[0],0,100*prob[1],0]
        net=np.mean(rewards)-30
        close(net,float(F(old['net'])))
        fits[name]=dict(coefficients=solved.x.tolist(),target_net=net)
    c=previous['censoring'];d=c['observed_defaults'];n=c['accounts'];m=c['missing_outcomes']
    completions=[F(d+j,n) for j in range(m+1)]
    assert [min(completions),max(completions)]==list(map(F,c['finite_population_bounds']))
    observed=F(d,n-m);zero=F(d,n)
    assert observed==F(c['observed_risk']) and zero==F(c['zero_encoded_risk'])
    assert [10000*observed-900,10000*zero-900]==[F(c['observed_model_margin']),F(c['zero_encoded_margin'])]
    comp=previous['competing'];q=F(comp['prepayments'],100);p=F(comp['defaults'],100-comp['prepayments'])
    # A three-state transition matrix independently gives cumulative default
    # probability after one and two periods (active, prepaid, defaulted).
    transition=np.array([[float((1-q)*(1-p)),float(q),float((1-q)*p)],
                         [0.,1.,0.],[0.,0.,1.]])
    initial=np.array([1.,0.,0.])
    close((initial@transition)[2],float(F(comp['default_incidence'])))
    close((initial@transition@transition)[2],float(F(comp['two_period_incidence'])))
    close(transition.sum(axis=1),np.ones(3))
    return dict(logistic_fits=fits,finite_population_bounds=list(map(str,[min(completions),max(completions)])),
                default_incidence_one_period=(initial@transition)[2],default_incidence_two_periods=(initial@transition@transition)[2],
                scope='Independent logistic score root, positive-information check, finite-outcome completion and absorbing-chain reconstruction; no downloaded-code execution or bank effect.')

def joint_law_contracts():
    base='docs/program/execution/2026-10-17/s9/'
    semantic=read(base+'semantic-results.json')
    law=read(base+'publication-v2/law-results.json')
    retry=read(base+'publication-v4/exact-results.json')
    # Convolution of coefficient polynomials, rather than the historical
    # enumeration of sign/control tuples, reconstructs the difference laws.
    def convolve(a,b):
        out=defaultdict(F)
        for x,px in a.items():
            for y,py in b.items():out[x+y]+=px*py
        return dict(out)
    def power(a,n):
        out={0:F(1)}
        for _ in range(n):out=convolve(out,a)
        return out
    def serial(a):return {str(k):str(v) for k,v in sorted(a.items())}
    signs={-1:F(1,2),1:F(1,2)}
    shared=power(signs,2);split=power(signs,4)
    assert serial(shared)==law['shared_difference_law']
    assert serial(split)==law['split_difference_law']
    tv=sum(abs(shared.get(k,F(0))-split.get(k,F(0))) for k in set(shared)|set(split))/2
    assert tv==F(law['total_variation'])==F(1,8)
    positive={k:sum(p for x,p in d.items() if x>0) for k,d in [('shared',shared),('split',split)]}
    for k,v in positive.items():assert v==F(law['positive_probability'][k])
    assert abs(positive['shared']-positive['split'])==F(law['positive_probability']['absolute_difference'])
    ref=semantic['inherited_exact_references']
    # Linear transformation of independent unit-variance signs gives the
    # complete covariance, without reusing historical sampled tuples.
    for name,rows in [('shared_control',[[1,0,-1],[0,1,-1]]),
                      ('split_control',[[1,-1,0,0],[0,0,1,-1]])]:
        cov=[[sum(F(x)*y for x,y in zip(a,b)) for b in rows] for a in rows]
        assert [[str(v) for v in row] for row in cov]==ref[name]['covariance']
        assert cov[0][0]+cov[1][1]-2*cov[0][1]==F(ref[name]['contrast_variance'])
    boot={}
    for name,n in [('row',4),('cluster',2)]:
        distribution=power({0:F(1,2),2:F(1,2)},n)
        mean=sum(F(x,n)*p for x,p in distribution.items())
        variance=sum((F(x,n)-mean)**2*p for x,p in distribution.items())
        assert mean==F(ref['bootstrap'][name+'_mean'])
        assert variance==F(ref['bootstrap'][name+'_variance'])
        boot[name]=dict(mean=str(mean),variance=str(variance),law=serial({F(x,n):p for x,p in distribution.items()}))
    # Absorbing Markov chains independently reconstruct completion, selected
    # results and the expected attempts; no historical generator is executed.
    def advance(v,m):return [sum(v[i]*m[i][j] for i in range(len(v))) for j in range(len(v))]
    structures={
        'redraw':([F(1),F(0),F(0)],
                  [[F(3,8),F(1,8),F(1,2)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]],1),
        'frozen':([F(1,2),F(1,2),F(0),F(0)],
                  [[F(3,4),F(0),F(1,4),F(0)],[F(0),F(0),F(0),F(1)],
                   [F(0),F(0),F(1),F(0)],[F(0),F(0),F(0),F(1)]],2)}
    reconstructed={}
    for mode,(initial,transition,unresolved) in structures.items():
        assert all(sum(row)==1 for row in transition)
        state=initial;calls=F(0)
        for k in range(1,5):
            calls+=sum(state[:unresolved]);state=advance(state,transition)
            mass={'-1':state[-2],'failure':sum(state[:unresolved]),'1':state[-1]}
            completion=1-mass['failure']
            values=dict(all_assigned_law={s:str(p) for s,p in mass.items()},
                        completion=str(completion),completed_positive=str(mass['1']/completion),
                        completed_mean=str((mass['1']-mass['-1'])/completion),expected_calls=str(calls))
            assert values==retry['retry_examples'][mode+'_K'+str(k)]
            reconstructed[mode+'_K'+str(k)]=values
    frozen=reconstructed['frozen_K2'];mass={k:F(v) for k,v in frozen['all_assigned_law'].items()}
    successful_moment=mass['1']-mass['-1'];failed=mass['failure']
    bounds=[successful_moment-failed,successful_moment+failed]
    assert bounds==[F(0),F(9,16)]
    # Weighted-result law includes an explicit zero contribution on failure.
    qnegative=mass['-1']/F(1,2)
    weighted={-1/qnegative:mass['-1'],F(0):failed,F(1):mass['1']}
    mean=sum(v*p for v,p in weighted.items());second=sum(v*v*p for v,p in weighted.items())
    inv=retry['inverse_selection']
    assert mean==F(inv['mean']) and second==F(inv['second_moment'])
    assert second-mean*mean==F(inv['variance'])==F(23,14)
    wrong=mass['1']-mass['-1']/F(1,2)
    assert wrong==F(inv['imperfect_q_bias'])==F(1,16)
    # Affine maps compose by homogeneous matrices; endpoints attain the bound.
    source=F(1,5)*F(3,25)+F(1,10)
    stage1_error=F(2)*F(1,1000)+F(1,500)
    delta=stage1_error/F(10)+F(1,10000)
    affine={k:str(v) for k,v in dict(source=source,bridge=source+delta,error=delta,stage_one_error=stage1_error).items()}
    assert affine==retry['affine_composition']
    joint=[[F(1,2),F(0)],[F(0),F(1,2)]]
    joint_tv=sum(abs(v-F(1,4)) for row in joint for v in row)/2
    assert joint_tv==F(retry['adaptive_joint_total_variation'])==F(1,2)
    eps=F(retry['uncertainty_envelope']['relative_completion_error']);mu=F(3,5)
    ratios=[(mu+s*eps)/(1+t*eps) for s in [-1,1] for t in [-1,1]]
    assert min(ratios)==F(retry['uncertainty_envelope']['mean_min'])
    assert max(ratios)==F(retry['uncertainty_envelope']['mean_max'])
    persistent=[sum(F(1,2)*(1-q)**k for q in [F(0),F(1)]) for k in range(1,5)]
    assert persistent==[F(1,2)]*4
    # Exact retained monetary scaling, a reporting distortion rather than
    # observed intervention value or runtime cost.
    monetary=[100*F(reconstructed[mode+'_K2']['completed_mean']) for mode in ['redraw','frozen']]
    assert monetary==[F(60),F(900,23)] and format(float(monetary[1]),'.2f')=='39.13'
    alpha=F(ref['alpha'])
    for row in ref['thresholds']:
        assert (F(row['p'])>=alpha)==row['source_delete']
        assert (F(row['p'])>alpha)==row['strict_port_delete']
    return dict(shared_law=serial(shared),split_law=serial(split),total_variation=str(tv),
                bootstrap=boot,retries=reconstructed,retained_missing_bounds=list(map(str,bounds)),
                inverse_variance=str(second-mean*mean),wrong_probability_bias=str(wrong),
                affine=affine,adaptive_total_variation=str(joint_tv),
                persistent_failure=list(map(str,persistent)),completed_only_usd=list(map(str,monetary)),
                scope='Independent polynomial convolution, covariance transformation and absorbing-chain reconstruction of retained chapter62 authored laws; no regenerated studies, upstream execution, empirical calibration or bank value.')

def main():
    checks=dict(deposit=deposit(),public_experiment=public_experiment(),exact_journeys=exact_journeys(),repeated_studies=repeated_studies(),corrected_width=corrected_width(),measurement_floor=measurement_floor(),investment_account=investment_account(),delegate_contracts=delegate_contracts(),flexbcf_contracts=flexbcf_contracts(),parallel_trends=parallel_trends(),financing_equivalence=financing_equivalence(),temporal_contracts=temporal_contracts(),survival_contracts=survival_contracts(),influence_contracts=influence_contracts(),fitting_contracts=fitting_contracts())
    checks['joint_law_contracts']=joint_law_contracts()
    source=Path(__file__);bindings[str(source.relative_to(ROOT))]=hashlib.sha256(source.read_bytes()).hexdigest()
    report=dict(status='pass',scope='Release arithmetic and retained-study reconstruction; no independent scientific acceptance, bank validity or new empirical qualification.',versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),checks=checks,bindings=bindings)
    (OUT/'numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='pass',checks=list(checks),bound_files=len(bindings),deposit=checks['deposit'],public_methods=checks['public_experiment']['methods'],repeated_summary_counts={k:v['summaries'] for k,v in checks['repeated_studies'].items()})))
if __name__=='__main__':main()
