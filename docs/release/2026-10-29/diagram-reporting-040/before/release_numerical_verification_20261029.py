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
        close(leverage.max(),old['max_leverage'])
        methods.append(dict(method=method,estimate=float(beta[1]),variance=float(hc2[1,1]),interval=interval,net_at_cost_1000=[float(v-1000) for v in interval]))
    for decision in previous['decisions']:
        m=next(v for v in methods if v['method']==decision['method']);cost=decision['illustrative_cost']
        close(m['estimate']-cost,decision['net_point']);close([v-cost for v in m['interval']],decision['net_interval'])
        assert (m['interval'][0]>cost)==decision['lower_bound_supports_spending']
    # Direct arm sums reconstruct influence and predeclared subgroup summaries
    # independently of the historical regression and row-deletion loops.
    arms=[y[a==v] for v in [0,1]];sums=[v.sum() for v in arms];sizes=[len(v) for v in arms]
    loo=[sums[1]/sizes[1]-(sums[0]-v)/(sizes[0]-1) for v in arms[0]]
    loo += [(sums[1]-v)/(sizes[1]-1)-sums[0]/sizes[0] for v in arms[1]]
    diagnostics=dict(zero_share=float(np.mean(y==0)),max=float(y.max()),leave_one_out_unadjusted_range=[min(loo),max(loo)])
    for k,v in diagnostics.items():close(v,previous['outcome_diagnostics'][k])
    subgroups=[]
    for row in previous['subgroups']:
        selected=(data[:,8]==0) if row['group']=='zero_1975' else (data[:,8]>0)
        group=[y[selected & (a==v)] for v in [0,1]]
        estimate=group[1].mean()-group[0].mean()
        variance=sum(v.var(ddof=1)/len(v) for v in group)
        interval=[estimate-norm.isf(.025)*math.sqrt(variance),estimate+norm.isf(.025)*math.sqrt(variance)]
        assert sum(map(len,group))==row['n'] and len(group[1])==row['treated']
        close(estimate,row['result']['estimate']);close(variance,row['result']['variance']);close(interval,row['result']['interval'])
        subgroups.append(dict(group=row['group'],n=row['n'],estimate=float(estimate),interval=interval))
    for row in previous['bias_sensitivity']:
        lower,upper=methods[0]['interval'];bound=row['absolute_bias_bound']
        close([lower-bound,upper+bound],row['interval'])
    return dict(n=445,methods=methods,diagnostics=diagnostics,subgroups=subgroups,
                scope='Retained public experimental subset; QR and direct-arm reconstruction check estimates, influence, predeclared subgroups and stated bias envelopes, not assignment or transport assumptions')

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

def foundational_laws():
    """Enumerate the stated finite worlds; do not simulate or run old generators."""
    base='docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'
    sources={k:raw(base+v+'.tex').decode() for k,v in {
        'graphs':'09d5d80790539d10','iv':'23868f4d3823c1bb',
        'learning':'3f523ca38e341a9c','inverse':'7ccd8624e4c82556'}.items()}
    for chapter,anchors in {
        'graphs':[r'P(A=1\mid U)=.2+.6U',r'\E[Y(a)]=.25+.35a',r'$[-0.32,0.68]$'],
        'iv':[r'Take $40\%$ compliers, $30\%$ always-takers and $30\%$ never-takers',r'$.8c$'],
        'learning':[r'\label{r3:exact-remainder}',r'$0.5$ and $0.01$',r'$0.381$'],
        'inverse':[r'p_A(U)=1/5+3U/5',r'h(w,a)=2a-3/8+15w/4',r'\label{r3:proximal-remainder}']
    }.items():
        for anchor in anchors:assert anchor in sources[chapter],(chapter,anchor)
    def bernoulli(p,value):return p if value else 1-p
    def serial(values):return [str(v) for v in values]
    # Distinct structural worlds have the same complete observational table.
    confounded=defaultdict(F);unconfounded=defaultdict(F)
    for a in [0,1]:
        for y in [0,1]:
            for u in [0,1]:
                p=F(1,5)+F(3,5)*u
                confounded[a,y]+=F(1,2)*bernoulli(p,a)*bernoulli(p,y)
            unconfounded[a,y]=F(1,2)*bernoulli(F(8,25)+F(9,25)*a,y)
    assert confounded==unconfounded=={(0,0):F(17,50),(0,1):F(4,25),(1,0):F(4,25),(1,1):F(17,50)}
    bounds=[confounded[1,1]-confounded[0,1]-F(1,2),confounded[1,1]+F(1,2)-confounded[0,1]]
    assert bounds==[-F(8,25),F(17,25)]
    # Latent enumeration independently supplies the front-door factorization.
    joint=defaultdict(F)
    for u in [0,1]:
        for a in [0,1]:
            for m in [0,1]:
                for y in [0,1]:
                    joint[a,m,y]+=F(1,2)*bernoulli(F(1,5)+F(3,5)*u,a)*bernoulli(F(1,10)+F(7,10)*a,m)*bernoulli(F(1,10)+F(1,2)*m+F(1,5)*u,y)
    frontdoor=[];observed=[];direct=[]
    for a in [0,1]:
        pa=sum(p for (aa,m,y),p in joint.items() if aa==a)
        observed.append(sum(p*y for (aa,m,y),p in joint.items() if aa==a)/pa)
        value=F(0)
        for m in [0,1]:
            pm=sum(joint[a,m,y] for y in [0,1])/pa
            inner=F(0)
            for other in [0,1]:
                pother=sum(p for (aa,mm,y),p in joint.items() if aa==other)
                inner+=pother*joint[other,m,1]/sum(joint[other,m,y] for y in [0,1])
            value+=pm*inner
        frontdoor.append(value)
        direct.append(sum(F(1,2)*bernoulli(F(1,10)+F(7,10)*a,m)*(F(1,10)+F(1,2)*m+F(1,5)*u) for u in [0,1] for m in [0,1]))
    assert frontdoor==direct==[F(1,4),F(3,5)] and observed==[F(19,100),F(33,50)]
    # Same randomized-invitation law, distinct population effects.
    observed_iv=[];ates=[]
    for completion in [0,1]:
        law=defaultdict(F);ate=F(0)
        for mass,receipts,outcomes in [(F(2,5),(0,1),(0,1)),(F(3,10),(1,1),(1-completion,1)),(F(3,10),(0,0),(0,completion))]:
            ate+=mass*(outcomes[1]-outcomes[0])
            for z in [0,1]:
                a=receipts[z];law[z,a,outcomes[a]]+=mass/2
        observed_iv.append(law);ates.append(ate)
    assert observed_iv[0]==observed_iv[1] and ates==[F(2,5),F(1)]
    first_stage=sum(2*p*(2*z-1)*a for (z,a,y),p in observed_iv[0].items())
    reduced_form=sum(2*p*(2*z-1)*y for (z,a,y),p in observed_iv[0].items())
    assert first_stage==reduced_form==F(2,5)
    # The R-loss constant solves its normal equation, with overlap weights.
    e=[F(1,2),F(1,100)];effects=[F(0),F(10)]
    projection=sum(p*(1-p)*v for p,v in zip(e,effects))/sum(p*(1-p) for p in e)
    assert projection==F(990,2599) and format(float(projection),'.3f')=='0.381'
    # An explicit finite-law perturbation checks both signs in the exact
    # ATE remainder and its union-model zero-bias cases; no estimated study.
    remainder_checks=[]
    for correct_propensity,correct_outcome in [(False,False),(True,False),(False,True),(True,True)]:
        mean=F(0);rhs=F(0)
        for x in [0,1]:
            true_e=F(1,5)+F(3,5)*x;true_m=F(1,5)+F(3,5)*x
            fit_e=true_e if correct_propensity else F(3,10)+F(2,5)*x
            fit_m=[true_m if correct_outcome else true_m+F(1,20)*(1-2*x),true_m if correct_outcome else true_m-F(1,10)]
            rhs+=F(1,2)*(fit_e-true_e)*((fit_m[1]-true_m)/fit_e+(fit_m[0]-true_m)/(1-fit_e))
            for a in [0,1]:
                for y in [0,1]:
                    phi=fit_m[1]-fit_m[0]+a*(y-fit_m[1])/fit_e-(1-a)*(y-fit_m[0])/(1-fit_e)
                    mean+=F(1,2)*bernoulli(true_e,a)*bernoulli(true_m,y)*phi
        assert mean==rhs
        if correct_propensity or correct_outcome:assert mean==0
        remainder_checks.append(dict(correct_propensity=correct_propensity,correct_outcome=correct_outcome,bias=str(mean)))
    # Enumerate the complete latent proxy law and solve its observable
    # two-by-two conditional-moment systems using rational elimination.
    rows=[]
    for u in [0,1]:
        for a in [0,1]:
            for z in [0,1]:
                for w in [0,1]:
                    p=F(1,2)*bernoulli(F(1,5)+F(3,5)*u,a)*bernoulli(F(3,10)+F(2,5)*u,z)*bernoulli(F(1,10)+F(4,5)*u,w)
                    rows.append((u,a,z,w,F(2*a+3*u),p))
    def solve(matrix,response):
        det=matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
        assert det!=0
        return [(response[0]*matrix[1][1]-matrix[0][1]*response[1])/det,(matrix[0][0]*response[1]-response[0]*matrix[1][0])/det],det
    proxy=[]
    for action in [0,1]:
        matrix=[];response=[]
        for z in [0,1]:
            selected=[r for r in rows if r[1]==action and r[2]==z];mass=sum(r[-1] for r in selected)
            matrix.append([sum(r[-1] for r in selected if r[3]==w)/mass for w in [0,1]])
            response.append(sum(r[-2]*r[-1] for r in selected)/mass)
        h,det=solve(matrix,response)
        assert h==[F(2*action)-F(3,8),F(2*action)+F(27,8)]
        qmatrix=[];qresponse=[]
        for w in [0,1]:
            selected=[r for r in rows if r[1]==action and r[3]==w];mass=sum(r[-1] for r in selected)
            qmatrix.append([sum(r[-1] for r in selected if r[2]==z)/mass for z in [0,1]])
            qresponse.append(sum(r[-1] for r in rows if r[3]==w)/mass)
        q,qdet=solve(qmatrix,qresponse)
        if action==0:
            assert [row[1] for row in qmatrix]==[F(23,74),F(15,26)]
            assert qresponse==[F(50,37),F(50,13)]
        target=sum(p*h[w] for u,a,z,w,y,p in rows)
        assert target==2*action+F(3,2)
        weighted=sum(p*q[z]*y for u,a,z,w,y,p in rows if a==action)
        clipped=sum(p*max(q[z],0)*y for u,a,z,w,y,p in rows if a==action)
        clipped_mass=sum(p*max(q[z],0) for u,a,z,w,y,p in rows if a==action)
        assert weighted==target and clipped_mass==F(95,64)
        assert clipped==[F(105,64),F(185,32)][action]
        perturbations=[]
        for dh,dq in [(F(0),F(1,10)),(F(1,10),F(0)),(F(1,10),F(1,5))]:
            left=right=F(0)
            for u,a,z,w,y,p in rows:
                eh=dh*(1+w);eq=dq*(2*z-1);hh=h[w]+eh;qq=q[z]+eq
                left+=p*(hh+(qq*(y-hh) if a==action else 0))
                if a==action:right-=p*eh*eq
            assert left-target==right
            perturbations.append(str(right))
        factual=sum(p*sum(rr[-1]*rr[-2] for rr in rows if rr[1]==action and rr[3]==w)/sum(rr[-1] for rr in rows if rr[1]==action and rr[3]==w) for u,a,z,w,y,p in rows)
        proxy.append(dict(action=action,outcome_bridge=serial(h),treatment_bridge=serial(q),conditional_treatment_matrix=[serial(row) for row in qmatrix],conditional_treatment_response=serial(qresponse),outcome_determinant=str(det),treatment_determinant=str(qdet),mean=str(target),clipped_mean=str(clipped),clipped_mass=str(clipped_mass),normalized_clipped_mean=str(clipped/clipped_mass),factual_regression_average=str(factual),perturbed_remainders=perturbations))
    clipped_contrast=F(proxy[1]['clipped_mean'])-F(proxy[0]['clipped_mean'])
    normalized_contrast=F(proxy[1]['normalized_clipped_mean'])-F(proxy[0]['normalized_clipped_mean'])
    assert clipped_contrast==F(265,64) and normalized_contrast==F(53,19)
    raw_means=[sum(y*p for u,a,z,w,y,p in rows if a==action)/sum(p for u,a,z,w,y,p in rows if a==action) for action in [0,1]]
    assert raw_means[1]-raw_means[0]==F(19,5)
    # Conditional expectation rows identify one policy average but not all.
    operator=[[F(1,2),F(1,2),F(0)],[F(0),F(1,2),F(1,2)]]
    responses=[[F(1),F(2),F(3)],[F(2),F(1),F(4)]]
    moments=[[sum(a*b for a,b in zip(row,h)) for row in operator] for h in responses]
    policy=[F(1,4),F(1,2),F(1,4)]
    identified=[sum(a*b for a,b in zip(policy,h)) for h in responses]
    unidentified=[sum(h)/3 for h in responses]
    assert moments==[[F(3,2),F(5,2)]]*2 and identified==[F(2)]*2 and unidentified==[F(2),F(7,3)]
    return dict(paired_world_observed={str(k):str(v) for k,v in confounded.items()},consistency_bounds=serial(bounds),
                frontdoor_means=serial(frontdoor),observed_means=serial(observed),compliance_ates=serial(ates),
                first_stage=str(first_stage),late=str(reduced_form/first_stage),r_loss_projection=str(projection),
                ate_remainder_perturbations=remainder_checks,proxy=proxy,clipped_proxy_contrast=str(clipped_contrast),normalized_clipped_proxy_contrast=str(normalized_contrast),raw_proxy_contrast=str(raw_means[1]-raw_means[0]),
                identified_policy_means=serial(identified),unidentified_equal_means=serial(unidentified),
                scope='Exact independent finite-law reconstruction of retained chapters6–9 examples and direct perturbation checks of displayed ATE/proximal remainders. No new empirical study, general ID implementation, theorem validation or bank qualification.')

def longitudinal_laws():
    """Reconstruct finite history and controlled-state identities in chapters10–12."""
    base='docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'
    sources={key:raw(base+name+'.tex').decode() for key,name in {
        'history':'19bce971619f032a','policy':'7cc06a3bd2696253',
        'controlled':'73ae9588bcea9fe8','unknown':'e764484b76fb2cf1',
        'private':'ce2741b43a3eca45'}.items()}
    for key,anchor in {'history':r'\label{r3:long-remainder}',
                       'policy':r'\label{r3:incremental-gradient}',
                       'controlled':r'\label{r3:controlled-inversion}',
                       'unknown':r'\label{s4:controlled-spectral}',
                       'private':r'\label{s5:marked-identification}'}.items():assert anchor in sources[key]
    def coin(p,a):return p if a else 1-p
    def e0(l):return F(1,5)+F(3,5)*l
    def e1(l,a,m):return F(3,20)+F(1,2)*m+F(1,10)*a
    def next_m(l,a):return F(1,10)+F(1,2)*l+F(1,5)*a
    def g0(l):return F(1,3)+F(l,3)
    def g1(l,a,m):return F(1,4)+F(m,4)+F(a,8)
    def y(l,a,m,b):return F(20+3*a+4*b+10*m+6*l)
    def v1(l,a,m):return sum(coin(g1(l,a,m),b)*y(l,a,m,b) for b in [0,1])
    def q0(l,a):return sum(coin(next_m(l,a),m)*v1(l,a,m) for m in [0,1])
    def v0(l):return sum(coin(g0(l),a)*q0(l,a) for a in [0,1])
    rows=[]
    for l in [0,1]:
        for a in [0,1]:
            for m in [0,1]:
                for b in [0,1]:
                    p=F(1,2)*coin(e0(l),a)*coin(next_m(l,a),m)*coin(e1(l,a,m),b)
                    target=F(1,2)*coin(g0(l),a)*coin(next_m(l,a),m)*coin(g1(l,a,m),b)
                    w0=coin(g0(l),a)/coin(e0(l),a)
                    w1=w0*coin(g1(l,a,m),b)/coin(e1(l,a,m),b)
                    rows.append((l,a,m,b,y(l,a,m,b),p,target,w0,w1))
    value=sum(target*outcome for l,a,m,b,outcome,p,target,w0,w1 in rows)
    ipw=sum(p*w1*outcome for l,a,m,b,outcome,p,target,w0,w1 in rows)
    score=[(v0(l)+w0*(v1(l,a,m)-q0(l,a)),p) for l,a,m,b,outcome,p,target,w0,w1 in rows]
    assert value==ipw==sum(s*p for s,p in score)==sum(v0(l)/2 for l in [0,1])
    variance=sum(p*(s-value)**2 for s,p in score)
    initial_variance=sum((v0(l)-value)**2/2 for l in [0,1])
    innovation_variance=sum(p*w0*w0*(v1(l,a,m)-q0(l,a))**2 for l,a,m,b,outcome,p,target,w0,w1 in rows)
    assert variance==initial_variance+innovation_variance
    moments=[sum(p*(b-e1(l,a,m))*(outcome-4*b) for l,a,m,b,outcome,p,target,w0,w1 in rows),
             sum(p*(a-e0(l))*(outcome-4*b-5*a) for l,a,m,b,outcome,p,target,w0,w1 in rows)]
    wrong=sum(p*(a-e0(l))*(outcome-4*b-3*a) for l,a,m,b,outcome,p,target,w0,w1 in rows)
    assert moments==[0,0] and wrong==F(8,25)
    # Sixteen fixed perturbations vary both times' propensity and continuation
    # errors independently. They test the stated algebra, not fitted rates.
    perturbations=[]
    for mask in range(16):
        ce0,ce1,cq0,cq1=[bool(mask&(1<<i)) for i in range(4)]
        def fit_e0(l):return e0(l) if ce0 else F(3,10)+F(2,5)*l
        def fit_e1(l,a,m):return e1(l,a,m) if ce1 else F(1,4)+F(2,5)*m+F(a,10)
        def d0(l,a):return F(0) if cq0 else F(1+2*l-a,5)
        def d1(l,a,m,b):return F(0) if cq1 else F(1+l+a-2*m+b,7)
        def fit_q0(l,a):return q0(l,a)+d0(l,a)
        def fit_q1(l,a,m,b):return y(l,a,m,b)+d1(l,a,m,b)
        def fit_v0(l):return sum(coin(g0(l),a)*fit_q0(l,a) for a in [0,1])
        def fit_v1(l,a,m):return sum(coin(g1(l,a,m),b)*fit_q1(l,a,m,b) for b in [0,1])
        mean=rhs=F(0)
        for l,a,m,b,outcome,p,target,w0,w1 in rows:
            fw0=coin(g0(l),a)/coin(fit_e0(l),a)
            fw1=fw0*coin(g1(l,a,m),b)/coin(fit_e1(l,a,m),b)
            mean+=p*(fit_v0(l)+fw0*(fit_v1(l,a,m)-fit_q0(l,a))+fw1*(outcome-fit_q1(l,a,m,b)))
            rhs+=p*(sum(coin(g0(l),aa)*(1-coin(e0(l),aa)/coin(fit_e0(l),aa))*d0(l,aa) for aa in [0,1])
                    +fw0*sum(coin(g1(l,a,m),bb)*(1-coin(e1(l,a,m),bb)/coin(fit_e1(l,a,m),bb))*d1(l,a,m,bb) for bb in [0,1]))
        assert mean-value==rhs
        if (ce0 or cq0) and (ce1 or cq1):assert rhs==0
        perturbations.append(dict(correct=[ce0,ce1,cq0,cq1],bias=str(rhs)))
    # Incremental-policy differentiation in an entirely positive finite law.
    # Perturb each cell mass against a fixed cell; complex steps differentiate
    # the rational target, independently of its displayed score formula.
    cells=[(x,a,z) for x in [0,1] for a in [0,1] for z in [0,1]]
    probability=np.array([float(F(1,2)*coin(F(1,5)+F(3,5)*x,a)*coin((F(1,5)+F(3,5)*x) if a==0 else (F(2,5)+F(x,5)),z)) for x,a,z in cells])
    def incremental(p,delta):
        total=0j if np.iscomplexobj(p) else 0.
        for x in [0,1]:
            px=sum(p[i] for i,c in enumerate(cells) if c[0]==x)
            masses=[sum(p[i] for i,c in enumerate(cells) if c[:2]==(x,a)) for a in [0,1]]
            means=[sum(p[i]*c[2] for i,c in enumerate(cells) if c[:2]==(x,a))/masses[a] for a in [0,1]]
            e=masses[1]/px;den=1+(delta-1)*e
            total+=px*(delta*e*means[1]+(1-e)*means[0])/den
        return total
    gradient_checks=[]
    for delta in [F(1,2),F(1),F(2)]:
        target=incremental(probability,float(delta));phi=[]
        for x,a,z in cells:
            e=F(1,5)+F(3,5)*x;m0=F(1,5)+F(3,5)*x;m1=F(2,5)+F(x,5);den=1+(delta-1)*e
            conditional=(delta*e*m1+(1-e)*m0)/den
            phi.append(float((delta*a+1-a)/den*(z-(m1 if a else m0))+conditional+delta*(m1-m0)/(den*den)*(a-e))-target)
        close(np.dot(probability,phi),0)
        errors=[]
        for j in range(1,len(cells)):
            direction=np.zeros(len(cells));direction[j]=1;direction[0]=-1
            derivative=incremental(probability.astype(complex)+1j*1e-20*direction,float(delta)).imag/1e-20
            expected=float(np.dot(direction,phi));close(derivative,expected);errors.append(abs(derivative-expected))
        if delta==1:close(phi,[z-target for x,a,z in cells])
        gradient_checks.append(dict(delta=str(delta),value=float(target),max_derivative_error=max(errors)))
    # Rational matrix recovery, marked private-logger inversion and spectral
    # similarity. These calculations do not call a package identification API.
    def transpose(m):return [list(v) for v in zip(*m)]
    def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
    def diag(v):return [[x if i==j else F(0) for j in range(len(v))] for i,x in enumerate(v)]
    def inverse(m):
        d=m[0][0]*m[1][1]-m[0][1]*m[1][0];assert d!=0
        return [[m[1][1]/d,-m[0][1]/d],[-m[1][0]/d,m[0][0]/d]]
    def serialize(m):return [[str(x) for x in row] for row in m]
    emission=[[F(4,5),F(1,5)],[F(1,5),F(4,5)]];mu=[F(3,5),F(2,5)]
    transitions=[[[F(4,5),F(1,5)],[F(3,10),F(7,10)]],[[F(3,5),F(2,5)],[F(1,10),F(9,10)]]]
    left=inverse(emission);joint=[];private=[]
    logger=[F(1,5),F(4,5)]
    for action,transition in enumerate(transitions):
        j=matmul(matmul(matmul(emission,diag(mu)),transition),transpose(emission))
        recovered=matmul(diag([1/v for v in mu]),matmul(matmul(left,j),transpose(left)))
        assert recovered==transition;joint.append(serialize(j))
        mass=[mu[s]*coin(logger[s],action) for s in [0,1]]
        marked=matmul(matmul(matmul(emission,diag(mass)),transition),transpose(emission))
        recovered_marked=matmul(matmul(left,marked),transpose(left));recovered_mass=list(map(sum,recovered_marked))
        assert recovered_mass==mass
        assert matmul(diag([1/v for v in mass]),recovered_marked)==transition
        reward=[F(10+3*action),F(20+5*action)]
        k=matmul(matmul(emission,diag(mass)),[[v] for v in reward])
        assert matmul(matmul(diag([1/v for v in mass]),left),k)==[[v] for v in reward]
        private.append(dict(state_action_mass=list(map(str,mass)),transition=serialize(recovered)))
    t0=transitions[0];mu1=[sum(mu[s]*t0[s][u] for s in [0,1]) for u in [0,1]]
    past=matmul(matmul(matmul(emission,diag(mu)),t0),diag([1/v for v in mu1]));future=matmul(emission,transpose(t0))
    p02=matmul(matmul(past,diag(mu1)),transpose(future));slices=[]
    for middle in [0,1]:
        observed=[[sum(mu[s]*emission[i][s]*t0[s][u]*emission[middle][u]*t0[u][v]*emission[k][v] for s in [0,1] for u in [0,1] for v in [0,1]) for k in [0,1]] for i in [0,1]]
        similarity=matmul(matmul(past,diag(emission[middle])),inverse(past))
        assert matmul(observed,inverse(p02))==similarity
        assert matmul(matmul(inverse(past),similarity),past)==diag(emission[middle])
        slices.append(serialize(observed))
    # Dynamic-choice observational equivalence and its changed-transition
    # prediction checked against an independent value-iteration solution.
    beta=.5;values=np.zeros(2)
    for iteration in range(200):
        action0=np.array([0.,1.])+beta*values
        action1=np.array([0.,1.])+beta*values[1]
        new=np.logaddexp(action0,action1)
        if np.max(np.abs(new-values))<1e-13:values=new;break
        values=new
    z=(1+math.sqrt(1+8*math.e))/2
    predicted=1-1/z;direct=float(np.exp(beta*values[1]-values[0]))
    close(predicted,direct);close(values[1],2*(1+math.log(2)));assert predicted>.5
    return dict(history_value=str(value),history_ipw=str(ipw),score_variance=str(variance),
                initial_variance=str(initial_variance),innovation_variance=str(innovation_variance),
                correct_blip_moments=list(map(str,moments)),wrong_early_blip_moment=str(wrong),
                remainder_perturbations=perturbations,incremental_gradient_checks=gradient_checks,
                known_emission_joint_matrices=joint,private_marked_recovery=private,spectral_slices=slices,
                counterfactual_customer_choice=predicted,value_iteration_choice=direct,
                scope='Independent exact finite-law and matrix reconstructions, derivative checks and fixed-point calculation of retained chapters10–12 arguments. Verification perturbations are authored checks, not newly sampled studies or evidence for all hidden-state models.')

def gmm_variance_contracts():
    prior=read('docs/release/2026-10-29/source-windmeijer-032/exact-witnesses.json')
    cells=[(u,v) for u in [-1,1] for v in [-1,1]]
    gs=np.array([[1,1+u/2] for u,v in cells]);bs=np.array([[1+u,3+2*v] for u,v in cells])
    def functional(p,center=False):
        G=p@gs;b=p@bs;t1=(G@b)/(G@G);r=bs-t1*gs
        omega=np.einsum('i,ij,ik->jk',p,r,r)
        if center:
            mean=p@r;omega-=np.outer(mean,mean)
        w=np.linalg.inv(omega);t2=(G@w@b)/(G@w@G)
        return np.array([t1,t2])
    probability=np.ones(4)/4;t=functional(probability);close(t,[2,5/3]);close(functional(probability,True)[1],1.5)
    influence=[]
    for j in range(4):
        direction=np.eye(4)[j]-probability
        influence.append(functional(probability+1j*1e-20*direction).imag/1e-20)
    influence=np.array(influence)
    close(influence[:,0],[-5/4,3/4,-3/4,5/4]);close(influence[:,1],[-151/144,65/144,-97/144,61/48]);close(influence.mean(0),[0,0])
    variances=np.mean(influence**2,axis=0);close(variances,[17/16,5827/6912])
    close(variances[1],float(F(prior['influences']['variance2'])))
    # Independent truncated series division around x=2 gives the exact fifth
    # derivative of Q=(44h-2h²)/(144+24h+3h²), without symbolic differentiation.
    coefficients=[]
    for k in range(6):
        numerator=F(44) if k==1 else F(-2) if k==2 else F(0)
        subtract=(24*coefficients[k-1] if k>=1 else 0)+(3*coefficients[k-2] if k>=2 else 0)
        coefficients.append((numerator-subtract)/144)
    fifth=math.factorial(5)*coefficients[5];assert fifth==F(-725,31104)
    close(float(coefficients[1]),11/36)
    amounts=[100*v-160 for v in [2,5/3,1.5]];close(amounts,[40,20/3,-10])
    return dict(targets=[2,5/3,1.5],influences=influence.tolist(),variances=variances.tolist(),Q_fifth_derivative_at_2=str(fifth),illustrative_dollars=amounts,
                scope='Independent probability-functional differentiation and rational-series division of a declared four-cell law; this verifies the authored comparison, not native panel execution, finite-sample coverage or causal validity.')

def panel_continuous_laws():
    from scipy.linalg import expm
    from scipy.integrate import quad,solve_ivp
    for name in ['2347859d224b8c12','ce2960f99921f249']:
        raw('docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'+name+'.tex')
    # Direct least-squares projection, independent of double-demeaning formula.
    treatment=np.array([[0,1,1,1],[0,0,0,1],[0,0,0,0]],dtype=float)
    units=np.repeat(np.arange(3),4);dates=np.tile(np.arange(4),3)
    design=np.column_stack([np.ones(12)]+[(units==i).astype(float) for i in [1,2]]+[(dates==t).astype(float) for t in [1,2,3]])
    residual=treatment.ravel()-design@np.linalg.lstsq(design,treatment.ravel(),rcond=None)[0]
    selected=treatment.ravel()==1;weights=residual[selected]/sum(residual[selected]);close(weights,[.3,.3,-.1,.5])
    effect=np.array([1,1,20,1]);coefficient=weights@effect;close(coefficient,-.9);close(effect.mean(),5.75)
    # Differencing the two observed transitions makes the first innovation both
    # a regressor component and a negative part of the error.
    rho=F(7,10);num=den=F(0)
    for u1 in [-1,1]:
        for u2 in [-1,1]:
            dx=F(u1);dy=(rho-1)*u1+u2;num+=dx*dy/4;den+=dx*dx/4
    assert num/den==rho-1
    # Equal regular-grid diffusions checked through independent ODE quadrature.
    B=np.array([1.,0.]);J=np.array([[0.,-1.],[1.,0.]])
    alias=[]
    for omega in [0,2*math.pi]:
        Fm=-np.eye(2)+omega*J;transition=expm(Fm)
        integrated=np.array([quad(lambda t:float((expm(Fm*t)@B)[j]),0,1,epsabs=1e-12)[0] for j in range(2)])
        Q=np.array([[quad(lambda t:float((expm(Fm*t)@expm(Fm.T*t))[i,j]),0,1,epsabs=1e-12)[0] for j in range(2)] for i in range(2)])
        expected=(1-math.exp(-1))*np.array([1.,omega])/(1+omega**2)
        close(integrated,expected);close(Q,(1-math.exp(-2))/2*np.eye(2));close(transition,math.exp(-1)*np.eye(2))
        half=expm(Fm*.5);alias.append(dict(omega=omega,regular_transition=transition.tolist(),control_integral=integrated.tolist(),half_transition=half.tolist()))
    assert not np.allclose(alias[0]['half_transition'],alias[1]['half_transition'])
    # Solve the feedback equilibrium directly and differentiate its two policy
    # mechanisms. Random customer disturbances induce the negative regression.
    b,c,k=2.,.5,3.;system=np.array([[-1.,b],[-k*c,-k]])
    assert np.max(np.linalg.eigvals(system).real)<0
    def equilibrium(r0,u):return np.linalg.solve(system,-np.array([u,k*r0]))
    slope=(equilibrium(2,0)[0]-equilibrium(1,0)[0]);close(slope,b/(1+b*c))
    observations=np.array([equilibrium(1,u) for u in [-2,-1,0,1,2]])
    observed_slope=np.cov(observations.T,ddof=0)[0,1]/np.var(observations[:,1]);close(observed_slope,-1/c)
    # Sum the probability law, retaining no-event likelihood contribution.
    mass=weighted_count=uncompensated=0.
    for n in range(40):
        probability=math.exp(-1)/math.factorial(n);weight=math.exp(-1)*2**n
        mass+=probability*weight;weighted_count+=n*probability*weight;uncompensated+=probability*2**n
    close(mass,1);close(weighted_count,2);close(uncompensated,math.e)
    hazard=.7;T=2.;path_values=[]
    for event in [.1,.9,1.99]:
        martingale=-math.exp(-hazard*(T-event))+quad(lambda t:hazard*math.exp(-hazard*(T-t)),0,event)[0]
        close(martingale,-math.exp(-hazard*T));path_values.append(martingale)
    no_event=quad(lambda t:hazard*math.exp(-hazard*(T-t)),0,T)[0];close(no_event,1-math.exp(-hazard*T))
    # Static silence/update construction; event density and survival exhaust1.
    rate=np.array([.1,1.]);prior=np.array([.5,.5]);silence=prior*np.exp(-rate);p=silence/silence.sum();after=p*rate;after/=after.sum()
    close(p[1],1/(1+math.exp(.9)));close(after[1],1/(1+.1*math.exp(.9)))
    assert format(p[1],'.4f')=='0.2891' and format(after[1],'.4f')=='0.8026'
    # Dynamic forward killed-state equation independently matches normalized ODE.
    Q=np.array([[-.3,.3],[.2,-.2]]);alpha=prior@expm((Q-np.diag(rate))*1.7);normalized=alpha/alpha.sum()
    solution=solve_ivp(lambda t,x:x@Q-x*(rate-x@rate),(0,1.7),prior,rtol=1e-11,atol=1e-13)
    close(normalized,solution.y[:,-1]);event_density=quad(lambda t:float(prior@expm((Q-np.diag(rate))*t)@rate),0,1.7)[0]
    close(event_density+alpha.sum(),1)
    return dict(twfe_weights=weights.tolist(),twfe_coefficient=float(coefficient),treated_cell_average=float(effect.mean()),two_transition_coefficient=str(num/den),alias=alias,
                equilibrium_rule_derivative=slope,clamped_rate_derivative=b,observed_equilibrium_slope=observed_slope,
                poisson_mean_weight=mass,poisson_target_count=weighted_count,uncompensated_mean=uncompensated,
                absorbing_event_gradient=path_values,no_event_gradient=no_event,silence_distress=float(p[1]),report_after_silence=float(after[1]),dynamic_filter=normalized.tolist(),event_or_survival_probability=float(event_density+alpha.sum()),
                scope='Independent projection,finite-law enumeration,matrix exponential/quadrature,ODE and pathwise-martingale checks of retained chapters15and18. No new sample or universal diffusion/event identification claim.')

def observation_learning_laws():
    from scipy.stats import binom,beta,chi2
    for name in ['f3b8a7764b223a39','a5debbffee003dd5','04d7d5e1eb08aee3','d9a40f35a20919a9','b5464e652d9d5b66']:
        raw('docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'+name+'.tex')
    # Full observed cells recover MAR and the nuisance-product remainder.
    coin=lambda p,b:p if b else 1-p;rows=[]
    for x in [0,1]:
        pi=F(1,4)+F(x,2);m=F(1,5)+F(x,2)
        for r in [0,1]:
            for y in [0,1]:rows.append((x,r,y,F(1,2)*coin(pi,r)*coin(m,y)))
    mean=sum(p*y for x,r,y,p in rows);checks=[]
    for dm in [F(0),F(1,10)]:
        for dp in [F(0),F(1,10)]:
            augmented=F(0);remainder=F(0)
            for x,r,y,p in rows:
                pi=F(1,4)+F(x,2);m=F(1,5)+F(x,2);augmented+=p*(m+dm+F(r)*(y-m-dm)/(pi+dp))
            for x in [0,1]:
                pi=F(1,4)+F(x,2);remainder+=F(1,2)*dp*dm/(pi+dp)
            assert augmented-mean==remainder;checks.append(dict(dm=str(dm),dp=str(dp),bias=str(remainder)))
    missing_laws=[]
    for unobserved in [F(0),F(1)]:
        observed=[F(1,4),F(1,4),F(1,2)];total=F(1,4)+F(1,2)*unobserved;missing_laws.append(dict(observed=list(map(str,observed)),mean=str(total)))
    assert missing_laws[0]['observed']==missing_laws[1]['observed']
    # Known receipt error: joint probabilities, not conditional means inverted.
    K=np.array([[.8,.2],[.2,.8]]);truth=np.array([[.4,.1],[.1,.4]]);seen=K@truth
    close(seen[:,1]/seen.sum(1),[8/25,17/25]);close(np.linalg.solve(K,seen),truth)
    mixture_variance=F(1,4)+(F(0)-1)**2/2+(F(2)-1)**2/2;assert mixture_variance==F(5,4)
    # Observational pair inverse and its complete differential from independent
    # probability/response perturbations of the scalar rational functional.
    def inverse(x):
        eta1,eta2,p=x;return (p*eta1-(1-p)*eta2)/(2*p-1)
    vector=np.array([2.,.5,.8]);gradient=[]
    for j in range(3):
        z=vector.astype(complex);z[j]+=1j*1e-20;gradient.append(float(inverse(z).imag/1e-20))
    e1,e2,p=vector;close(gradient,[p/(2*p-1),-(1-p)/(2*p-1),(e2-e1)/(2*p-1)**2])
    # Uniform binomial inversion at all counts in the stated diagnostic grid.
    minimum=1.;minimum_at=None
    for n in range(1,26):
        count=np.arange(n+1);lower=np.array([0. if k==0 else beta.ppf(.025,k,n-k+1) for k in count]);upper=np.array([1. if k==n else beta.ppf(.975,k+1,n-k) for k in count])
        for p in np.linspace(0,1,201):
            coverage=float(np.sum(binom.pmf(count,n,p)*((p>=lower)&(p<=upper))))
            if coverage<minimum:minimum=coverage;minimum_at=[n,p]
    assert format(minimum,'.5f')=='0.95096'
    # Whole-line/disconnected inverse laws tested without dividing by rank.
    inside=[]
    for v in [-100,-1,-.99,0,3.99,4,100]:
        lower=min(-.2*(v-1.5),.2*(v-1.5));upper=max(-.2*(v-1.5),.2*(v-1.5));accepted=lower<=.5<=upper
        assert accepted==(v<=-1 or v>=4);inside.append(dict(value=v,accepted=accepted))
    # Known unequal inclusion and noisy audit labels: exact expectation over
    # audit and label mechanisms, conditional on each complete pair.
    audit=[]
    for focal in [F(-1),F(3)]:
        companion=F(2);T=(focal+companion)/2
        for q in [F(1,10),F(3,5)]:
            for error in [F(0),F(3,20)]:
                estimate=F(0)
                for selected in [0,1]:
                    for correct in [0,1]:
                        prob=coin(q,selected)*coin(1-error,correct)
                        observed=focal if correct else companion
                        corrected=T+(observed-T)/(1-2*error)
                        estimate+=prob*(T+F(selected)*(corrected-T)/q)
                assert estimate==focal;audit.append(dict(focal=str(focal),inclusion=str(q),error=str(error),expectation=str(estimate)))
    # Ellipsoid support: explicit extremizer and independently dense reciprocal
    # rectangle search both lie within the vertex-based enclosure.
    m=np.array([1.,.5,2.,.25]);V=np.array([[2.,.4,.2,0],[.4,1.,0,.1],[.2,0,2.,.3],[0,.1,.3,.8]])
    critical=chi2.ppf(.975,4);cost=.7
    def support(u0,u1):
        c=np.array([.5,u0/2,.5,u1/2]);radius=np.sqrt(critical*c@V@c);extreme=m+np.sqrt(critical/(c@V@c))*(V@c)
        close((extreme-m)@np.linalg.solve(V,extreme-m),critical);close(c@extreme-cost,c@m+radius-cost)
        return c@m-radius-cost,c@m+radius-cost
    vertices=[support(x,y) for x in [1.1,2.] for y in [-3.,-1.2]];bounds=[min(v[0] for v in vertices),max(v[1] for v in vertices)]
    for x in np.linspace(1.1,2,11):
        for y in np.linspace(-3,-1.2,11):
            low,high=support(x,y);assert low>=bounds[0]-1e-10 and high<=bounds[1]+1e-10
    # Five wide noisy proxy bits still omit one latent coordinate.
    from itertools import product
    latent=list(product([0,1],repeat=2));proxies=list(product([0,1],repeat=5));matrix=np.array([[float(np.prod([.8 if z==u1 else .2 for z in bits])) for u1,u2 in latent] for bits in proxies])
    assert np.linalg.matrix_rank(matrix)==2;close(matrix[:,0],matrix[:,1]);close(matrix[:,2],matrix[:,3]);close(matrix.sum(0),np.ones(4))
    null_checks=[]
    for action in [0,1]:
        probabilities=[coin(F(1,10)+F(u1,5)+F(u2,2),action) for u1,u2 in latent]
        center={u1:sum(probabilities[j]*u2 for j,(a,u2) in enumerate(latent) if a==u1)/sum(probabilities[j] for j,(a,u2) in enumerate(latent) if a==u1) for u1 in [0,1]}
        h=np.array([float(u2-center[u1]) for u1,u2 in latent]);weighted=np.array(list(map(float,probabilities)))/4
        residual=matrix@(weighted*h);close(residual,np.zeros(32));null_checks.append(float(np.max(np.abs(residual))))
    rare=[]
    for H in [2,5,10,20]:
        p=F(1,3)*F(2,3)**(H-2);Q0=np.array([float(1-p),float(3*p/4),float(p/4)]);Q1=np.array([float(1-p),float(p/4),float(3*p/4)])
        divergence=float(np.sum(Q0*np.log(Q0/Q1)));close(divergence,float(p)*math.log(3)/2)
        delta=.1;binary_kl=(1-2*delta)*math.log((1-delta)/delta);bound=2*binary_kl/(float(p)*math.log(3));rare.append(dict(horizon=H,informative_probability=str(p),kl=divergence,necessary_episodes=bound))
    return dict(missing_mean=str(mean),missing_remainders=checks,equal_observed_missing_laws=missing_laws,known_error_naive_contrast=.36,known_error_recovered_contrast=.6,linkage_total_variance=str(mixture_variance),pair_inverse_gradient=gradient,binomial_minimum_coverage=minimum,binomial_minimum_at=minimum_at,disconnected_membership=inside,audit_expectations=audit,ellipsoid_enclosure=bounds,proxy_rank=2,proxy_conditional_null_errors=null_checks,rare_path_bounds=rare,
                scope='Independent finite-law,probability-derivative,binomial-tail and geometric checks of retained observation/learning arguments. No new bank data,native fit or empirical theorem qualification.')


def financial_information_laws():
    """Enumerate retained planning examples without inventing bank observations."""
    base='docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'
    sources={key:raw(base+name+'.tex').decode() for key,name in {
        'linked':'ef0385a590696022','information':'c53a57c97a7c2a65',
        'cost':'45875b508399ecf9','selection':'af6f7fa75bf002ac',
        'pilot':'65a610a93e0ddf97','pilot_tables':'73d03246565dc76d',
        'structure':'a6a49cf680d32a49'}.items()}
    for key,anchor in {'linked':r'\label{integrated:linked_funding:eq:value}',
                       'information':'50{,}000/20=2{,}500',
                       'cost':'37/60', 'selection':'B minus A',
                       'pilot':'point estimate at the largest evaluation sample size',
                       'pilot_tables':'0.9333',
                       'structure':r'\label{exec23:structured-weights}'}.items():assert anchor in sources[key],key
    weights=[48*10**6*(F(2,1000)*F(99,100)**h-(F(1,12000) if h==0 else 0)) for h in range(7)]
    shift=sum(w*F(82,100)**h for h,w in enumerate(weights))
    values=[sum(w*2*rho**h for h,w in enumerate(weights))-400000 for rho in [F(82,100),F(96,100)]]
    assert [round(float(v)) for v in values]==[375149,751749]
    assert round(float(shift))==387575
    # Conditional selection and symmetric label-noise expectations, by
    # enumerating the three observed outcomes, rather than using the formula.
    focal,companion=F(2),F(1,2);average=(focal+companion)/2
    augmented=[]
    for actual,declared,error in [(F(1,4),F(1,4),F(0)),(F(1,10),F(1,4),F(0)),(F(1,4),F(1,4),F(3,20))]:
        states=[(1-actual,average),(actual*(1-error),average+(focal-average)/declared),(actual*error,average+(companion-average)/declared)]
        expectation=sum(p*z for p,z in states)
        augmented.append(dict(actual=str(actual),declared=str(declared),error=str(error),mean=str(expectation),monetary_bias=float((expectation-focal)*shift)))
    assert [v['mean'] for v in augmented]==['2','31/20','71/40']
    assert [round(v['monetary_bias']) for v in augmented]==[0,-174409,-87204]
    for q in [F(1,10),F(1,4),F(1)]:
        outcomes=[(1-q,average),(q,average+(focal-average)/q)]
        mean=sum(p*z for p,z in outcomes);variance=sum(p*(z-mean)**2 for p,z in outcomes)
        assert mean==focal and variance==(1/q-1)*(focal-average)**2
    # An independent product-measure calculation checks the exact
    # fixed-pilot population ratio, including the action-error square.
    from numpy.polynomial.hermite import hermgauss
    nodes,quadrature=hermgauss(8);nodes=nodes*math.sqrt(2);quadrature=quadrature/math.sqrt(math.pi)
    da=np.array([.1,-.2,.05]);dy=np.array([.2,.3,-.1]);eta=2.;num=den=0.
    for wi,w in enumerate(nodes):
        x=np.array([1.,w,w*w-1])
        for ei,e in enumerate(nodes):
            probability=quadrature[wi]*quadrature[ei]
            ra=e-x@da;ry=eta*e-x@dy
            num+=probability*ra*ry;den+=probability*ra*ra
    Q=np.diag([1.,1.,2.]);predicted=(eta+da@Q@dy)/(1+da@Q@da)
    close(num/den,predicted)
    assert max([.9600,.9417,.9333])>.95 and .9333<.95
    # Actual policies are selected at each signal. This is a finite Bayes
    # decision calculation, independent of the prose's posterior shortcut.
    signal=[]
    for s in [0,1]:
        joint=[F(1,2)*(F(9,10) if s==world else F(1,10)) for world in [0,1]]
        mass=sum(joint);gain=sum(p*(400*world-300) for world,p in enumerate(joint))/mass
        signal.append(dict(signal=s,mass=str(mass),act_value=str(gain),act=gain>0))
    gross=sum(F(r['mass'])*max(F(0),F(r['act_value'])) for r in signal)
    perfect=sum(max(F(0),400*world-300)/2 for world in [0,1])
    assert gross==30 and perfect==50 and 50000/(gross-10)==2500
    token=F(30000*2+5000*8,10**6);ordinary=F(30,60)*60+1
    base_cost=F(10,60)*60+2+token+F(1,5)+F(1,5)
    assisted=base_cost+F(1,5)*F(30,60)*60;saving=ordinary-assisted
    assert token==F(1,10) and assisted==F(37,2) and saving==F(25,2)
    assert 12500/saving==1000 and 12500/(saving-F(1,1000)*10000)==5000
    assert saving-F(2,1000)*10000<0 and (ordinary-base_cost)/30==F(37,60)
    # Count every requested case; referrals retain their delay and loss.
    a_total=100*2+100+10000+10*40+10*50
    b_total=100*4+3*100+30*40+20*5+10*50
    assert (a_total,b_total,a_total-b_total)==(11200,2500,8700)
    assert F(88,90)>F(67,70)
    review_delta=F(1,100)-F(1,500)
    assert 20/review_delta==2500 and review_delta*100-20==-F(96,5) and review_delta*10000-20==60
    # Enumerate all capped attempt trajectories, including permanent faults.
    import itertools
    retries=[]
    for permanent,transient in [(F(0),F(1,5)),(F(1,10),F(1,9))]:
        expected=3*permanent;failure=permanent
        for outcomes in itertools.product([0,1],repeat=3):
            probability=(1-permanent)*math.prod(transient if x==0 else 1-transient for x in outcomes)
            calls=next((i+1 for i,x in enumerate(outcomes) if x),3)
            expected+=probability*calls
            if not any(outcomes):failure+=probability
        retries.append(dict(calls=str(expected),failure=str(failure),cost=str(2*expected+50*failure)))
    assert [r['calls'] for r in retries]==['31/25','59/45']
    assert [r['failure'] for r in retries]==['1/125','41/405']
    assert F(retries[0]['cost'])==F(72,25) and round(float(F(retries[1]['cost'])),2)==7.68
    # Solve the two-state minimax regret equality and retain the joint
    # policy relation before comparing it with the coordinate enlargement.
    p=F(1625,625+1625);regret=625*p
    assert p==F(13,18) and regret==F(8125,18)
    worlds=[(-100,-200),(100,0)]
    assert {a-b for a,b in worlds}=={100}
    b_minus_a=[min(b for a,b in worlds)-max(a for a,b in worlds),max(b for a,b in worlds)-min(a for a,b in worlds)]
    assert b_minus_a==[-300,100]
    # Pilot option by direct joint sums across state and signal, retaining
    # immediate construction as the comparator and charging delay once.
    gain=[F(-60000),F(100000)];quality=F(4,5);pilot_gross=F(0);post=[]
    for s in [0,1]:
        joint=[F(1,2)*(quality if s==world else 1-quality) for world in [0,1]]
        conditional=sum(p*g for p,g in zip(joint,gain))/sum(joint)
        pilot_gross+=max(F(0),sum(p*g for p,g in zip(joint,gain)));post.append(conditional)
    immediate=max(F(0),sum(gain)/2);net=-10000+F(9,10)*pilot_gross
    assert post==[-28000,68000] and pilot_gross==34000 and immediate==20000 and net==20600
    assert (immediate+10000)/pilot_gross==F(15,17)
    assert (30000+(immediate+10000)/F(9,10))/80000==F(19,24)
    mixture=[10-40*w for w in [F(1,5),F(3,5),F(1,10),F(2,5)]]
    assert mixture==[2,-14,6,-6]
    assert (F(20)-4)/2-2==6 and (10*F(20)-90*4)/100-2==-F(18,5)
    original=F(1,4)*20-F(3,4)*4;normalized=F(2,5)*20-F(3,5)*4
    assert original==2 and normalized==F(28,5)
    return dict(funding_values=list(map(float,values)),one_unit_funding_shift=float(shift),linked_law_examples=augmented,
                fixed_pilot_ratio=float(num/den),signal=signal,signal_gross=str(gross),perfect_information=str(perfect),
                assisted_cost=str(assisted),variable_saving=str(saving),automation_costs=[a_total,b_total],
                retries=retries,randomized_regret=str(regret),B_minus_A_coordinate_range=b_minus_a,
                pilot_option=str(net),immediate_build=str(immediate),deployment_mixture=list(map(str,mixture)),
                scope='Independent exact state/path enumeration, quadrature and monetary reconstruction of retained planning laws. No new empirical study, market price, live-model result, bank benefit or qualification.')


def qualification_design_laws():
    """Check the retained finite bounds and design power, without final draws."""
    from scipy.stats import beta,binom,chi2
    import itertools
    base='docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'
    for stem in ['cfe939aa8760d37c','0086cf696f3dce80','72275a22fb653cf2','db9ea6894074d6d4','e2385e937c19dd4e','e5b668b040ce402c']:
        raw(base+stem+'.tex')
    # Persistent signed-audit multiplier moments and the three-way
    # variance decomposition follow from a complete finite reference.
    q,e=F(2,5),F(2,25);rank=1-2*e;difference=F(3,4)
    states=[(1-q,F(0)),(q*(1-e),1/q),(q*e,-1/q)]
    assert sum(p*w for p,w in states)==rank and sum(p*w*w for p,w in states)==1/q
    pair=[];cell=[]
    for p,w in states:
        for u,v in itertools.product([-1,1],repeat=2):
            pair.append((p/4,F(u+v,2)+(w/rank)*F(u-v,2)+difference*(w/rank-1)))
            cell.append((p/4,F(u+v,2)+(w/rank)*F(u-v,2)))
    a=1/(q*rank*rank)
    assert sum(p*z for p,z in pair)==sum(p*z for p,z in cell)==0
    assert sum(p*z*z for p,z in pair)==(1+a)/2+difference*difference*(a-1)
    assert sum(p*z*z for p,z in cell)==(1+a)/2
    coefficients=[rank*rank*(F(1,50)+F(1,n))-1/(q*n) for n in [100,320]]
    assert coefficients==[-F(479,125000),F(17009,2000000)]
    calendar=[];precision=[]
    for n in [2,3,10,40,160]:
        rho=.95;cov=.36*rho**np.abs(np.arange(n)[:,None]-np.arange(n)[None,:])
        variance=cov.sum()/n**2
        formula=.36*(n+2*sum((n-k)*rho**k for k in range(1,n)))/n**2
        information=np.ones(n)@np.linalg.solve(cov,np.ones(n))
        closed=(n*(1-rho)+2*rho)/(.36*(1+rho))
        close(variance,formula);close(information,closed)
        if n in [40,160]:calendar.append(math.sqrt(variance))
        persistence=1-1/n**2;information_limit=(n*(1-persistence)+2*persistence)/(1+persistence)
        precision.append(dict(n=n,information=information_limit))
    assert [format(v,'.4f') for v in calendar]==['0.4494','0.2776']
    tv=2*norm.cdf(.5)-1;diameter_bound=.9-tv
    assert format(tv,'.4f')=='0.3829' and format(diameter_bound,'.4f')=='0.5171'
    # Backward recursion supplies intervention values. Complete observed
    # prefix enumeration independently supplies fitted-weight means.
    def bern(p,x):return p if x else 1-p
    def action_probability(s):return F(3,10)+F(2,5)*s
    def retention(s,a):return F(9,10)-F(s,10)-F(a,10)
    def transition(s,a):return F(1,5)+F(s,2)-F(3*a,20)
    def reward(snew,a):return 2-3*snew-F(a,4)
    policies=[lambda s:0,lambda s:1,lambda s:s];policy_results=[]
    for policy in policies:
        val=[F(0),F(0)]
        for time in range(2):
            val=[sum(bern(transition(s,policy(s)),ss)*(reward(ss,policy(s))+val[ss]) for ss in [0,1]) for s in [0,1]]
        target=sum(val)/2;fitted_mean=true_mean=F(0)
        for s0,a0,s1,c0,a1,s2,c1 in itertools.product([0,1],repeat=7):
            e0=bern(action_probability(s0),a0);e1=bern(action_probability(s1),a1)
            g0=retention(s0,a0);g1=retention(s1,a1)
            probability=F(1,2)*e0*bern(transition(s0,a0),s1)*bern(g0,c0)*e1*bern(transition(s1,a1),s2)*bern(g1,c1)
            fitted_e0=bern(action_probability(s0)+F(1,25),a0);fitted_e1=bern(action_probability(s1)+F(1,25),a1)
            fw0=F(int(policy(s0)==a0)*c0)/(fitted_e0*(g0-F(3,100)))
            fw1=fw0*int(policy(s1)==a1)*c1/(fitted_e1*(g1-F(3,100)))
            w0=F(int(policy(s0)==a0)*c0)/(e0*g0);w1=w0*int(policy(s1)==a1)*c1/(e1*g1)
            fitted_mean+=probability*(fw0*reward(s1,a0)+fw1*reward(s2,a1))
            true_mean+=probability*(w0*reward(s1,a0)+w1*reward(s2,a1))
        assert true_mean==target
        policy_results.append(dict(value=str(target),fitted_bias=float(fitted_mean-target)))
    assert [p['value'] for p in policy_results]==['11/8','2','133/80']
    assert [format(p['fitted_bias'],'.5f') for p in policy_results]==['0.21997','-0.22321','0.20834']
    ce,cg=F(1,4),F(13,20);factor=(1+F(1,25)/ce)*(1+F(3,100)/cg)
    bias_envelope=sum(2*(factor**(t+1)-1) for t in range(2))
    assert format(float(bias_envelope),'.5f')=='1.37243'
    maxscore=sum(2*(ce*cg)**(-(t+1)) for t in range(2))
    eval_radius=float(maxscore)*math.sqrt(2*math.log(80)/1000);assert eval_radius>8
    # Exact binomial lower-limit equivalence: reject coverage <=.95 only
    # when the binomial upper tail is at most the allocated family error.
    alpha=.05/16;n=512
    threshold=next(k for k in range(1,n+1) if binom.sf(k-1,n,.95)<=alpha)
    assert threshold==500 and beta.ppf(alpha,threshold,n-threshold+1)>=.95
    assert beta.ppf(alpha,threshold-1,n-threshold+2)<.95
    powers=[float(binom.sf(threshold-1,n,p)) for p in [.95,.97,.98,.99]]
    assert [format(v,'.6f') for v in powers]==['0.001849','0.234929','0.770054','0.997670']
    availability=[float(beta.ppf(alpha,k,n-k+1)) for k in [507,512]]
    assert F(507,512)>F(99,100) and all(v<.99 for v in availability)
    assert [format(v,'.5f') for v in availability]==['0.97130','0.98880']
    degrees=math.ceil(18/(.02*.25**2));assert degrees==14400
    multipliers=[239/chi2.ppf(1-.02/18,239),239/chi2.ppf(.02/18,239)]
    assert [format(v,'.5f') for v in multipliers]==['0.76731','1.34533']
    def halfwidth(m):
        nu=2*m-2;b2=F(nu,nu-2)/F(3,100)
        return math.sqrt(float(b2*100/(2*m*F(1,4))))
    first_m=next(m for m in range(3,1000) if halfwidth(m)<5)
    assert first_m==268 and format(halfwidth(200),'.5f')=='5.78806'
    assert format(halfwidth(400),'.5f')=='4.08761'
    assert format(3000*(20-halfwidth(200)-15),'.2f')=='-2364.19'
    # Enumerated sign law supplies moment targets and irreducible loss
    # floors; independent analytic thresholds test the proposed bound.
    rows=[]
    for x,v,h,noise in itertools.product([-1,1],repeat=4):
        z=F(3*x,10)+v;act=F(4,5)*z+F(x,5)+h;y=F(6,5)*act+F(2*x,5)+noise
        vz=z-F(3*x,10);va=act-F(11*x,25);vy=y-F(116*x,125)
        rows.append((z,act,y,vz,va,vy))
    BZ,BA,BY=[max(abs(row[j]) for row in rows) for j in range(3)]
    Q=sum(row[3]*row[4] for row in rows)/16;M=sum(row[3]*row[5] for row in rows)/16
    assert [BZ,BA,BY,Q,M]==[F(13,10),F(56,25),F(511,125),F(4,5),F(24,25)]
    losses=[sum(row[j]**2 for row in rows)/16 for j in [3,4,5]]
    assert losses==[1,F(41,25),F(2101,625)]
    for d in [0,4,19]:
        common=math.sqrt(math.log(4*(d+1)/.03)/(2*(640//(d+1))))
        assert 8*float(BZ*BA)*common>float(Q) and 8*float(BZ*BY)*common>float(M)
    denominator_threshold=math.floor((8*float(BZ*BA)/float(Q))**2*math.log(4/.03)/2)+1
    decision_threshold=math.floor((8*float(BZ*(BY+F(23,20)*BA))/float(M-F(23,20)*Q))**2*math.log(4/.03)/2)+1
    assert denominator_threshold==2075 and decision_threshold==7344273
    certs=[]
    for features,support,pilot in [(20,3,1024),(60,3,1024),(20,8,1024),(60,8,65536),(60,8,1048576)]:
        lam=2*math.sqrt(2*math.log(2*features/.005)/pilot)
        tau=math.sqrt(2*math.log(2*features**2/.005)/pilot)
        squared=9*support*lam**2+144*tau*support**2*lam**2
        certs.append([math.sqrt(squared),squared])
    assert [format(v[0],'.4f') for v in certs]==['3.9770','4.3729','10.2004','0.5698','0.0961']
    assert [format(v[1],'.4f') for v in certs]==['15.8166','19.1221','104.0480','0.3247','0.0092']
    assert F(72,100)/(F(4,5)*(1+F(72,100)))==F(45,86)
    return dict(persistent_quadratic_coefficients=list(map(str,coefficients)),calendar_mean_sd=calendar,
                gaussian_information_sequence=precision,diameter_probability_limit=diameter_bound,
                servicing_policy_examples=policy_results,servicing_bias_envelope=str(bias_envelope),servicing_evaluation_radius=eval_radius,
                coverage_success_threshold=threshold,screen_power=powers,availability_lower_bounds=availability,
                temporal_degrees_requirement=degrees,development_variance_multipliers=multipliers,
                intervention_first_centered_sample=first_m,centered_offer_lower=3000*(20-halfwidth(200)-15),
                dependent_denominator_threshold=denominator_threshold,dependent_decision_threshold=decision_threshold,
                sparse_certificates=certs,irreducible_loss_floors=list(map(str,losses)),
                scope='Independent finite-law enumeration, covariance solving, binomial-tail and deterministic planning reconstruction. Quantiles are numerical development checks, not certified outward endpoints; no final successor draws, bank sample-size recommendation or empirical qualification.')


def network_allocation_laws():
    """Reconstruct specified network laws, not acquired implementations."""
    import itertools
    base='docs/release/2026-10-29/source/docs/writing-repair/2026-10-29/src/'
    for stem in ['b627a1d6f5e463b2','89ab4d3132a15fc3','82b72f77cea3839f','ff4336dd688ce96a','04b976aba7e67a1e','a6a9c3beac1b082c','1979e0a1a216a89e','9a61f7787de4fb1a']:
        raw(base+stem+'.tex')
    def bern(p,x):return p if x else 1-p
    two=[]
    for p in [F(1,5),F(4,5)]:
        mean=sum(bern(p,a)*bern(p,b)*(100*a+40*b-30*a*b) for a,b in itertools.product([0,1],repeat=2))
        assert mean==140*p-30*p*p
        two.append(mean)
    assert two==[F(134,5),F(464,5)] and two[1]-two[0]==66
    # Exact design-weighted means use known joint assignments, even though
    # two realized observations cannot supply a general variance estimate.
    ht_means={}
    for exposure in itertools.product([0,1],repeat=2):
        total=F(0)
        for z in itertools.product([0,1],repeat=2):
            estimate=sum(F(int((z[i],z[1-i])==exposure))*(5+2*z[i]+3*z[1-i])/F(1,4) for i in [0,1])/2
            total+=estimate/4
        ht_means[str(exposure)]=str(total)
    assert list(ht_means.values())==['5','8','7','10']
    assert F(1,4)/F(1,2)**2==1 and F(1,4)**2/F(1,2)**2==F(1,4)
    ratio=F(1,4)**2/F(1,2)**2;duplicated=ratio*F(1,4)**2
    assert ratio==F(1,4) and duplicated==F(1,64)
    assert -2*(1-F(1,2))*ratio==-F(1,4)
    # Linear equilibrium computed as a matrix solve and a separate convergent
    # propagation series; input transforms are compared on identical actions.
    swap=np.array([[0.,1.],[1.,0.]])
    S=np.linalg.solve(np.eye(2)-.5*swap,10*np.eye(2));expected=np.array([[40,20],[20,40]])/3
    close(S,expected)
    series=np.zeros((2,2));power=np.eye(2)
    for k in range(100):series+=10*(.5**k)*power;power=power@swap
    close(series,S)
    W=np.array([[0.,1.,1.],[1.,0.,0.],[1.,0.,0.]])
    row=W/W.sum(1)[:,None];action=np.array([1.,0.,0.])
    star=np.linalg.solve(np.eye(3)-.25*W,10*action)
    normalized=np.linalg.solve(np.eye(3)-.25*row,10*action)
    close(star,np.array([80,20,20])/7);close(normalized,np.array([32,8,8])/3)
    close(star,np.linalg.solve(np.eye(3)-.5*(W/2),10*action))
    covariance=np.array([[1.,.05],[.05,.01]]);gradient=np.array([2.,40.])
    close(gradient@covariance@gradient,28);close(gradient@np.diag(np.diag(covariance))@gradient,20)
    K=np.array([[1.,1.,0.],[1.,1.,1.],[0.,1.,1.]])
    u=np.array([1.,-2.,1.]);v=np.array([1.,0.,-1.]);B=K/np.sqrt(K.sum(1))[:,None];P=B@B.T
    close(u@K@u/9,-2/9);close(v@K@v/9,2/9)
    close(u@P@u/9,(7-16/math.sqrt(6))/9);close(v@P@v/9,1/9)
    Cs=np.array([[[1,-2],[-2,5]],[[5,-2],[-2,1]],[[1,0],[0,1]]],dtype=float)
    assert all(np.linalg.eigvalsh(c).min()>0 for c in Cs)
    median=np.median(Cs,axis=0);close(np.linalg.det(median),-3);close(np.ones(2)@median@np.ones(2),-2)
    # Approximate ties overlapping a strict tail can leave the probability
    # domain; these authored inputs are not an executed package example.
    t0=0;stats=[F(1,10**15),F(1,10**15),F(1)];epsilon=F(1,10**14)
    strict=sum(x>t0 for x in stats);ties=sum(abs(x-t0)<epsilon for x in stats)
    tail=(strict+F(3,4)*(1+ties))/(len(stats)+1)
    assert tail==F(21,16) and 2*min(tail,1-tail)==-F(5,8)
    assert 6*sum(F(1,k) for k in range(1,7))==F(147,10)
    # Enumerate every node ranking and cluster assignment for the 3-path.
    neighborhoods=[{0,1},{0,1,2},{1,2}];cases=[]
    for scores in itertools.permutations(range(3)):
        cluster=[max(neighborhood,key=lambda j:scores[j]) for neighborhood in neighborhoods]
        labels=sorted(set(cluster))
        for choices in itertools.product([0,1],repeat=len(labels)):
            by_cluster=dict(zip(labels,choices));z=[by_cluster[c] for c in cluster]
            expose=[[int(all(z[j]==a for j in neighborhood)) for a in [0,1]] for neighborhood in neighborhoods]
            cases.append((F(1,6*2**len(labels)),expose))
    assert len(cases)==20 and sum(p for p,x in cases)==1
    pi=[[sum(p*x[i][a] for p,x in cases) for a in [0,1]] for i in range(3)]
    assert pi==[[F(5,12)]*2,[F(1,3)]*2,[F(5,12)]*2]
    outcomes=[[F(1),F(2)],[F(2),F(3)],[F(3),F(4)]];ht=[];hajek=[]
    for p,exposure in cases:
        arm_num=[sum(exposure[i][a]*outcomes[i][a]/pi[i][a] for i in range(3)) for a in [0,1]]
        arm_den=[sum(F(exposure[i][a])/pi[i][a] for i in range(3)) for a in [0,1]]
        ht.append((p,(arm_num[1]-arm_num[0])/3))
        hajek.append((p,(arm_num[1]/arm_den[1] if arm_den[1] else 0)-(arm_num[0]/arm_den[0] if arm_den[0] else 0)))
    ht_mean=sum(p*z for p,z in ht);var=sum(p*(z-ht_mean)**2 for p,z in ht);hj_mean=sum(p*z for p,z in hajek)
    assert ht_mean==1 and var==F(2242,75) and hj_mean==F(1,2)
    variance_joint=F(0)
    for i,j,a,b in itertools.product(range(3),range(3),[0,1],[0,1]):
        joint=sum(p*x[i][a]*x[j][b] for p,x in cases)
        variance_joint+=(2*a-1)*(2*b-1)*outcomes[i][a]*outcomes[j][b]*(joint/(pi[i][a]*pi[j][b])-1)/9
    assert variance_joint==var
    # Full-history probability by enumeration of block assignments, including
    # every uniform start phase. This also covers windows longer than a block.
    path_probability=[]
    for length in [1,2,3,10]:
        ell=4;prob=F(0)
        for phase in range(ell):
            blocks=[(phase+j)//ell for j in range(length)];distinct=sorted(set(blocks))
            for choices in itertools.product([0,1],repeat=len(distinct)):
                assignment=dict(zip(distinct,choices))
                if all(assignment[b] for b in blocks):prob+=F(1,ell*2**len(distinct))
        path_probability.append(prob)
    assert path_probability==[F(1,2),F(7,16),F(3,8),F(7,64)]
    assert F(1,2)-F(10-1,4*4)==-F(1,16)
    scores=[F(1),F(-1),F(1),F(-1)]
    variances=[sum(x*x for x in scores)/4+sum(2*sum(scores[t]*scores[t-k] for t in range(k,4))/4 for k in range(1,limit+1)) for limit in [1,2]]
    assert variances==[-F(1,2),F(1,2)]
    # Updating both nodes from old state and sequentially are different laws.
    states=[]
    for order in [(0,1),(1,0)]:
        x=[1,0]
        for node in order:x[node]=x[1-node]
        states.append(x)
    assert states==[[0,0],[1,1]] and [(0+1)/2,(0+0)/2,(1+1)/2]==[.5,0.,1.]
    for count,cost in [(1000,30),(600,50),(400,75)]:assert 30000/count==cost
    assert F(1,5)*F(4,5)==F(4,25) and F(1,2)*F(1,5)==F(1,10) and F(1,5)**2==F(1,25)
    assert F(9,10)!=F(1,2) and F(10,11)!=F(1,2)
    return dict(two_borrower_policy_means=list(map(str,two)),exposure_ht_means=ht_means,
                spatial_response=S.tolist(),star_response=star.tolist(),row_normalized_response=normalized.tolist(),
                original_path_quadratics=[float(u@K@u/9),float(v@K@v/9)],overlap_quadratics=[float(u@P@u/9),float(v@P@v/9)],
                elementwise_covariance_median=median.tolist(),overlapping_tail=str(tail),
                randomized_cluster_cases=len(cases),marginal_exposure=[[str(v) for v in row] for row in pi],
                ht_mean=str(ht_mean),ht_variance=str(var),zero_extended_hajek_mean=str(hj_mean),
                block_path_probability=list(map(str,path_probability)),finite_lag_variances=list(map(str,variances)),
                sequential_states=states,study_cost_per_unit=[30,50,75],
                scope='Independent exact assignment/ranking/block enumeration, linear solves and deterministic helper-input arithmetic for retained network comparisons. No acquired package execution, new experiment, generalized covariance qualification, market price or bank truth.')

def consumer_operating_laws():
    import itertools
    # Bind the complete source contexts whose retained laws are checked here.
    manifest=read('docs/release/2026-10-29/context-review-129/manifest.json')
    names={name for chapter in manifest['chapters'] if 78<=chapter['chapter']<=83 for name in chapter['source_bindings']}
    for name in sorted(names):raw(name)
    # Quarterly cash-flow valuation, independently summed in dollars.
    quarters=[100_000_000*.001*.25/(1.04**(q/4)) for q in range(1,5)]
    slope=sum(quarters);midpoint=sum(.75*x for x in quarters)-40000
    values=[sum(theta*x for x in quarters)-40000 for theta in [.6,.9]]
    assert [f'{v:.2f}' for v in values]==['18550.62','47825.93']
    assert f'{midpoint:.2f}'=='33188.28' and f'{4*sum(.75*x for x in quarters)-40000:.2f}'=='252753.11'
    assert f'{40000/slope:.6f}'=='0.409902'
    target=F(3,5)*F(3,5)+F(2,5)*F(9,10);approx=(F(3,5)+F(9,10))/2
    assert target==F(18,25) and approx==F(3,4)
    target_value=float(target)*slope-40000;difference=midpoint-target_value
    close(difference,.1*(values[1]-values[0]));assert f'{target_value:.2f}'=='30260.75'
    assert [f'{v:.2f}' for v in [midpoint-difference,midpoint+difference]]==['30260.75','36115.81']
    # Enumerate all observed histories, independently cancel the logger, then
    # compare with a backwards conditional-reward calculation.
    probabilities=[];ipw=[F(0),F(0)];gformula=[F(0),F(0)]
    def pL(x,a):return F(1+x+a,5)
    def pY(x,a,l,b):return F(1+2*x+3*l+2*b+a,10)
    for x,a,l,b,y in itertools.product([0,1],repeat=5):
        pl=pL(x,a);pb=F(1,4) if l else F(3,4);py=pY(x,a,l,b)
        behavior=(F(1,2))**2*(pl if l else 1-pl)*(pb if b else 1-pb)*(py if y else 1-py)
        probabilities.append(behavior)
        for j in [0,1]:
            first=(1-x) if j else 0;second=(1-l) if j else 0
            if (a,b)==(first,second):ipw[j]+=behavior*(100*y-6*a-4*b)/(F(1,2)*(pb if b else 1-pb))
    for j in [0,1]:
        for x,l in itertools.product([0,1],repeat=2):
            a=1-x if j else 0;b=1-l if j else 0;pl=pL(x,a)
            gformula[j]+=F(1,2)*(pl if l else 1-pl)*(100*pY(x,a,l,b)-6*a-4*b)
    assert len(probabilities)==32 and sum(probabilities)==1
    assert ipw==gformula==[F(29),F(218,5)] and ipw[1]-ipw[0]==F(73,5)
    # Fixed finite-population selection; unavailable values are not zero.
    y=[20,40,60,80];pi=[F(1,2),F(1),F(1,4),F(1,2)];selection=[]
    for flags in itertools.product([0,1],repeat=4):
        probability=math.prod(p if flag else 1-p for flag,p in zip(flags,pi))
        ht=sum(F(flag*value,4)/p for flag,value,p in zip(flags,y,pi))
        observed=F(sum(flag*value for flag,value in zip(flags,y)),sum(flags)) if sum(flags) else F(0)
        selection.append((probability,ht,observed))
    mean=sum(p*v for p,v,o in selection);variance=sum(p*(v-mean)**2 for p,v,o in selection)
    assert mean==50 and variance==1100 and sum(p*o for p,v,o in selection)==F(365,8)
    # Two-group transport and joint-policy interactions have different targets.
    effects=[10,-10];source=[F(4,5),F(1,5)];target=[F(1,5),F(4,5)]
    assert sum(p*v for p,v in zip(source,effects))==6 and sum(p*v for p,v in zip(target,effects))==-6
    assert [q/p for p,q in zip(source,target)]==[F(1,4),F(4)]
    val=lambda f,s:100+20*f+15*s-30*f*s
    joint=val(1,1)-val(0,0);interaction=val(1,1)-val(1,0)-val(0,1)+val(0,0)
    assert joint==5 and interaction==-30
    assert 80*(val(1,0)-100)+40*(val(0,1)-100)+20*joint==2300
    assert 100*20+60*15==2900 and 2900+20*interaction==2300
    # Preserve exactly one contribution, including all repeated attempt costs.
    assert sum([100,-40,-40,70])==90 and sum(dict(A=100,B=-40,C=70).values())==130
    attempted=[('A',2),('B',4),('B',4),('C',-1),('D',3)]
    assert len(list(itertools.permutations(attempted)))==120
    for events in itertools.permutations(attempted):
        contributions={}
        for identity,value in events:
            assert identity not in contributions or contributions[identity]==value
            contributions[identity]=value
        assert F(sum(contributions.values()),len(contributions))==2
    assert F(sum(v for k,v in attempted),5)==F(12,5) and F(sum(v for k,v in attempted),4)==3
    # Exhaust all ten ordered publisher/collector interleavings. A rejected
    # pin is an availability outcome, not an invalid public reference.
    schedules=[]
    for positions in itertools.combinations(range(5),3):
        publisher=iter(['pin','publish','unpin']);collector=iter(['snapshot','sweep'])
        schedules.append([next(publisher) if i in positions else next(collector) for i in range(5)])
    def retention(schedule,recheck):
        present={'report','input'};roots=set();pins=set();marked=set();admitted=False;bad=False;published=False
        closure=lambda nodes: set(nodes)|({'input'} if 'report' in nodes else set())
        for event in schedule:
            if event=='pin':
                admitted=closure({'report'})<=present
                if admitted:pins.add('report')
            elif event=='publish' and admitted:
                roots.add('report');published=True
            elif event=='unpin':pins.discard('report')
            elif event=='snapshot':marked=closure(roots|pins)
            elif event=='sweep':
                keep=marked|(closure(roots|pins) if recheck else set())
                present&=keep
            bad=bad or not closure(roots|pins)<=present
        return bad,published
    stale=[retention(events,False) for events in schedules];safe=[retention(events,True) for events in schedules]
    assert len(schedules)==10 and sum(x[0] for x in stale)==3
    assert not any(x[0] for x in safe) and sum(x[1] for x in safe)==9
    # A model with indivisible terminal transitions has two distinct outcomes.
    terminals=[]
    for order in itertools.permutations(['cancel','publish']):
        state='running'
        for event in order:
            if state=='running':state='cancelled' if event=='cancel' else 'completed'
        terminals.append(state)
    assert sorted(terminals)==['cancelled','completed']
    # Queueing and total memory, not merely each worker's service time.
    assert (1024-128-128)//256==3
    workers=[0,0];finish=[]
    for request in range(5):
        worker=min(range(2),key=lambda k:workers[k]);workers[worker]+=3;finish.append(workers[worker])
    assert finish==[3,3,6,6,9] and sum(v<=8 for v in finish)==4
    assert F(7,10)*10+F(3,20)*(-30)-2-F(3,20)*20==-F(5,2)
    assert (F(7,10)*10+F(3,20)*(-30))/F(17,20)-2==F(16,17)
    # A missing nuisance term changes the exact Gaussian coverage and decision.
    influence=[]
    for x,y in itertools.product([-1,1],repeat=2):influence.append(F(x)+2*F(y)*math.sqrt(2))
    close(sum(float(v*v) for v in influence)/4,9)
    close(2*norm.cdf(2)-1,.9544997361036416);close(2*norm.cdf(2/3)-1,.4950149249061542)
    profit=lambda b:3750*b-7000
    assert [profit(v) for v in [F(19,10),F(21,10)]]==[125,875]
    assert [profit(v) for v in [F(17,10),F(23,10)]]==[-625,1625]
    assert [profit(v) for v in [-1,1]]==[-10750,-3250]
    roots=np.sort(np.roots([96,-400,396]));close(roots,[(25-math.sqrt(31))/12,(25+math.sqrt(31))/12])
    # Joint measurement-score covariance by complete sign enumeration.
    scores=[]
    for x,y in itertools.product([-1,1],repeat=2):scores.append((F(x)-F(3,10)*(-x+y))/F(4,5))
    assert sum(v*v for v in scores)/4==F(89,32) and F(1)/F(4,5)**2==F(25,16)
    assert F(1,10)+(F(9,10)-F(1,10))*F(3,10)==F(17,50)
    assert F(1,10)+(F(1,2)-F(1,10))*F(3,5)==F(17,50)
    assert [500*p-200 for p in [F(3,10),F(3,5)]]==[-50,100]
    assert [500*(q-F(1,10))/F(4,5)-200 for q in [F(3,10),F(19,50)]]==[-75,-25]
    # Preparation, blocking and linkage; exact enumerations require no engine.
    completion_values={F(u+v,3) for u,v in itertools.product([0,1],repeat=2)}
    assert completion_values=={F(0),F(1,3),F(2,3)} and {300*v-40 for v in completion_values}=={-40,60,160}
    assert F(100,2)==50 and F(300,4)==75
    assert F(math.comb(98,10),math.comb(100,10))==F(89,110)
    overlapping=[]
    for x,y,z in itertools.product([-1,1],repeat=3):overlapping.append((F(x+y,2),F(y+z,2)))
    assert sum(a*b for a,b in overlapping)/8==F(1,4)
    assert sum(((a+b)/2)**2 for a,b in overlapping)/8==F(3,8)
    posterior=lambda prior,lr:prior*lr/(1-prior+prior*lr)
    assert posterior(F(1,100),100)==F(100,199) and posterior(F(1,1000),100)==F(100,1099)
    assert posterior(F(1,100),10)==F(10,109)
    assert F(54,60)==F(9,10) and F(54,100)==F(27,50)
    assert F(96,100)*2-1==F(23,25)>F(1,10)
    assert F(90,100)+F(10,100)==1 and F(80,100)+F(85,100)==F(33,20)
    assert F(3,4)*20+F(1,4)*(-20)==10
    assert F(3,4)*(20-10)**2+F(1,4)*(-20-10)**2+4==304
    assert F(4,5)*100+F(1,5)*1000==280 and F(4,5)*F(1,5)*900**2==129600
    # Commercial workflow accounting and physical-plan examples.
    assert F(5*6-2,6)==F(14,3) and F(3*6-2,4)==4
    assert F(10-1,2)+F(-30-1,2)==-11
    assert [4+F(v,2) for v in [-50,50]]==[-21,29]
    assert F(10-1,2)+F(30-1,2)==19
    assert F(1+0+0,3)==F(1,3) and F(1+0+1+0,4)==F(1,2)
    sleep=sum(F(1,5)*F(11,10)**i for i in range(3));assert sleep==F(331,500) and sleep+6==F(3331,500)
    assert F(1)/(F(1,5)+F(4,5)/4)==F(5,2)
    assert F(1)/(F(1,5)+F(4,5)/4+F(3,10))==F(10,7)
    assert F((1+1)**2+(-1-1)**2,16)==F(1,2) and F(1+1+1+1,16)==F(1,4)
    return dict(funding_slope=slope,funding_range=values,funding_midpoint=midpoint,funding_tv_difference=difference,
                servicing_ipw=list(map(str,ipw)),servicing_gformula=list(map(str,gformula)),selection_mean=str(mean),selection_variance=str(variance),
                retention_schedules=schedules,stale_snapshot_violations=sum(x[0] for x in stale),coordinated_violations=0,coordinated_publications=9,
                queue_completions=finish,terminal_outcomes=terminals,gaussian_coverages=[float(2*norm.cdf(v)-1) for v in [2,2/3]],
                scope='Independent cash-flow sums, complete finite-history/selection/sign enumerations and all ten stated retention interleavings. Reconstructs retained authored laws and operating examples only; no downloaded code, vendor/native trial, new empirical study, bank data or universal storage proof.')

def assistance_information_laws():
    """Independently enumerate the declared assistance/translation laws."""
    import itertools
    manifest=read('docs/release/2026-10-29/context-review-130/manifest.json')
    for chapter in manifest['chapters']:
        if chapter['chapter'] in [64,66,67]:
            for name in chapter['source_bindings']:raw(name)
    # Task composition, conditional chain and attainable marginal bounds.
    delta=lambda w:F(7,100)*w-F(17,100)*(1-w)
    assert delta(F(17,24))==0 and delta(F(1,2))==F(-1,20) and delta(F(4,5))==F(11,500)
    marginals=[F(96,100),F(95,100),F(90,100),F(97,100),F(98,100)]
    chain=math.prod(marginals);assert chain==F(4876578,6250000)
    counts=[4,5,10,3,2];offset=0;disjoint=[]
    for n in counts:disjoint.append(set(range(offset,offset+n)));offset+=n
    nested=[set(range(n)) for n in counts]
    assert [len(set(range(100))-set.union(*fs)) for fs in [disjoint,nested]]==[76,90]
    truth=[0]*100;key=[1]*10+[0]*90
    for answer,correct in [([1]*20+[0]*80,80),(truth,100)]:
        assert sum(a==b for a,b in zip(answer,key))==90
        assert sum(a==b for a,b in zip(answer,truth))==correct
    pi=[F(3,5),F(1,5),F(1,5)];transition=[[F(9,10),F(1,20),F(1,20)],[F(1,5),F(3,10),F(1,2)],[F(1,10),F(3,5),F(3,10)]]
    final=[sum(pi[i]*transition[i][j] for i in range(3)) for j in range(3)]
    assert final==[F(3,5),F(21,100),F(19,100)]
    switch=sum(pi[i]*(1-transition[i][i]) for i in [1,2])/(1-pi[0])
    correction=sum(pi[i]*transition[i][0] for i in [1,2])/(1-pi[0])
    assert switch==F(7,10) and correction==F(3,20) and pi[0]*F(9,10)+(1-pi[0])*switch==F(41,50)
    # Full observed joint tables versus intervention means, with positive support.
    worlds=[(F(7,20),F(1,5),F(1,10)),(F(3,10),F(2,5),F(0)),(F(1,4),F(3,5),F(-1,10))]
    world_reports=[]
    for alpha,beta,tau in worlds:
        observed=defaultdict(F);means=[]
        for u,a,y in itertools.product([0,1],repeat=3):
            pa=F(1,4)+F(1,2)*u;py=alpha+beta*u+tau*a
            assert 0<pa<1 and 0<py<1
            observed[a,y]+=F(1,2)*(pa if a else 1-pa)*(py if y else 1-py)
        assert [observed[a,y] for a,y in itertools.product([0,1],repeat=2)]==[F(3,10),F(1,5),F(1,5),F(3,10)]
        for a in [0,1]:means.append(sum(F(1,2)*(alpha+beta*u+tau*a) for u in [0,1]))
        assert means[1]-means[0]==tau
        world_reports.append(dict(means=list(map(str,means)),net=str(100*tau-5)))
    # Enumerate shared-context plus independent residual errors.
    joint=defaultdict(F)
    for shared in [0,1]:
        for errors in itertools.product([0,1],repeat=3):
            probability=(F(1,10) if shared else F(9,10))*math.prod(F(1,10) if e else F(9,10) for e in errors)
            actual=tuple(1 if shared else e for e in errors);joint[actual]+=probability
    marginal=sum(p for e,p in joint.items() if e[0]);majority=sum(p for e,p in joint.items() if sum(e)>=2)
    assert marginal==F(19,100) and majority==F(313,2500)
    naive=3*marginal*marginal*(1-marginal)+marginal**3;assert naive==F(47291,500000)
    assert majority-naive==F(15309,500000)
    assert [15-50*w for w in [F(1,5),F(3,5),F(3,10),0,1]]==[5,-15,0,15,-35]
    assert F(9,10)-F(1,2)-F(2,5)+F(1,5)==F(1,5)
    assert [F(100,n) for n in [80,60,36]]==[F(5,4),F(5,3),F(25,9)]
    # Target weighting and residual confounding from covariance normal equations.
    assert (F(9,100)*2+F(1,4)*8)/(F(9,100)+F(1,4))==F(109,17)
    proxy=[]
    for noise,expected in [(0,F(-1,5)),(F(1,4),F(-1,30)),(1,F(2,15)),(4,F(11,45))]:
        noise=F(noise)
        tau=F(-1,5);cov_ay=2*tau+1;cov_wy=tau+1
        coefficient=(cov_ay*(1+noise)-cov_wy)/(2*(1+noise)-1)
        assert coefficient==expected==tau+noise/(1+2*noise);proxy.append(str(coefficient))
    # Daily funding ledger independently reconstructs both cost and value.
    daily=[]
    for balance,rate,cost in [(100000,F(2,100),4),(110000,F(9,400),8)]:
        n=sum((rate*balance+F(5,100)*(150000-balance))/365 for day in range(30))+cost
        value=sum((F(5,100)-rate)*balance/365 for day in range(30))-cost
        assert n+value==30*F(5,100)*150000/365;daily.append((n,value))
    assert daily[1][1]-daily[0][1]==F(-142,73)==-(daily[1][0]-daily[0][0])
    r_inc=(F(9,400)*3300000-F(2,100)*3000000+365*4)/300000;assert r_inc==F(1571,30000)
    assert [(q-r_inc)*300000/365 for q in [F(4,100),F(6,100)]]==[F(-742,73),F(458,73)]
    assert [sum(q*b for q,b in zip([F(1,10),F(1,100)],balances))/365 for balances in [[200,0],[0,200]]]==[F(4,73),F(2,365)]
    assert min(100,100)*F(1,100)-F(3,4)==F(1,4)
    assert (min(0,100)+min(200,100))*F(1,200)-F(3,4)==F(-1,4)
    # Differential measurement and a complete selected-note law.
    measured=lambda risk,sensitivity,specificity:risk*sensitivity+(1-risk)*(1-specificity)
    base=measured(F(2,5),F(4,5),F(9,10))
    assert measured(F(1,2),F(4,5),F(9,10))-base==F(7,100)
    assert measured(F(1,2),F(1,2),F(19,20))-base==F(-21,200)
    selected=defaultdict(F)
    for a,u in itertools.product([0,1],repeat=2):selected[a,u]=F(1,4)*(F(3,4) if a==u else F(1,4))
    assert [selected[a,1]/sum(selected[a,u] for u in [0,1]) for a in [0,1]]==[F(1,4),F(3,4)]
    # Complete logger enumeration, then intervention calculation separately.
    reward=lambda a,l,b:100+20*a-40*l+30*b*l-10*b
    policies=[]
    for a in [0,1]:
        risk=F(1,4)+F(1,2)*a
        direct=sum((risk if l else 1-risk)*reward(a,l,l) for l in [0,1])
        weighted=sum(F(1,4)*(risk if l else 1-risk)*4*reward(aa,l,b) for aa,l,b in itertools.product([0,1],repeat=3) if aa==a and b==l)
        fixed=[sum((risk if l else 1-risk)*reward(a,l,b) for l in [0,1]) for b in [0,1]]
        assert direct==weighted;policies.append(dict(adaptive=str(direct),fixed=list(map(str,fixed))))
    assert policies==[dict(adaptive='95',fixed=['90','175/2']),dict(adaptive='105',fixed=['90','205/2'])]
    assert [F(1,5)*100+F(1,10)*v for v in [50,-50]]==[25,15]
    assert [F(v,1)/F(3,10) for v in [25,15]]==[F(250,3),50]
    assert [F(1,10)*v for v in [-200,100]]==[-20,10]
    # Linguistic treatment proxy: enumerate all eight cells.
    cells=[]
    for s,r,z in itertools.product([0,1],repeat=3):
        flip=F(9,20) if s==0 else F(0)
        probability=F(1,4)*(1-flip if z==r else flip)
        cells.append((s,r,z,100+(20 if s==0 else -10)*r,probability))
    contrasts=[]
    for s in [0,1]:
        means=[sum(y*p for ss,r,zz,y,p in cells if ss==s and zz==z)/sum(p for ss,r,zz,y,p in cells if ss==s and zz==z) for z in [0,1]]
        contrasts.append(means[1]-means[0])
    assert contrasts==[2,-10] and sum(contrasts)/2==-4
    assert sum(p for s,r,z,y,p in cells if r==z)==F(31,40)
    assert [sum(F(1,4)*(100+20*(u<1+2*a)-10*a) for u in range(4)) for a in [0,1]]==[105,105]
    arithmetic=F(3,4)*F(1,10)+F(1,4)*F(9,10)
    geometric=1/(1+math.exp(-(-.75*math.log(9)+.25*math.log(9))))
    assert arithmetic==F(3,10);close(geometric,.25)
    assert F(1,5)*F(1,10)+F(4,5)*F(9,10)==F(37,50)
    # Ontology error rates, unit weighting and independent provenance checks.
    ontology=[]
    for sensitivity,falsepositive in [(F(4,5),F(1,20)),(F(9,10),F(3,20))]:
        prevalence=F(1,5);q=sensitivity*prevalence+falsepositive*(1-prevalence)
        accuracy=sensitivity*prevalence+(1-falsepositive)*(1-prevalence)
        assert (q-falsepositive)/(sensitivity-falsepositive)==prevalence
        ontology.append([str(q),str(accuracy)])
    assert ontology==[['1/5','23/25'],['3/10','43/50']]
    assert (9*10-10)/10==8 and F(1500,36000)==F(1,24)
    phrase='monthly household income before tax during the reporting period'.split()
    left=set(['doc-one']+phrase);right=set(['doc-two']+phrase)
    assert F(len(left&right),len(left|right))==F(9,11)>F(4,5)
    assert measured(F(1,5),F(9,10),F(9,10))==F(13,50)
    assert measured(F(1,5),F(7,10),F(19,20))==F(9,50)
    assert (1+4*F(4,5))/5==F(21,25)
    assert F(81,100)==F(9,10)**2 and [F(240,n) for n in [100,90,81]]==[F(12,5),F(8,3),F(80,27)]
    # Enumerate legal graphs; edges need not remain independent after admission.
    graphs=[(1,1),(0,1),(0,0)];posteriors=[]
    for advice in [(1,1),(1,0)]:
        weights=[math.prod(F(9,10) if g==e else F(1,10) for g,e in zip(graph,advice)) for graph in graphs]
        posteriors.append([w/sum(weights) for w in weights])
    assert posteriors==[[F(81,91),F(9,91),F(1,91)],[F(9,19),F(1,19),F(9,19)]]
    unanimity=F(4,5)**5+F(1,5)**5
    assert unanimity==F(41,125) and F(1,5)**5/unanimity==F(1,1025)
    assert F(9**5,1+9**5)==F(59049,59050)
    legal=[g for g in itertools.product([0,1],repeat=2) if sum(g)<2]
    assert F(sum(g[0] for g in legal),len(legal))==F(1,3)
    weights=[F(4,10)*F(1,10),F(3,10)*F(7,10),F(2,10)*F(1,10),F(1,10)*F(1,10)]
    posterior=[w/sum(weights) for w in weights]
    assert posterior==[F(1,7),F(3,4),F(1,14),F(1,28)]
    return dict(stage_chain=str(chain),stage_marginal_bounds=['19/25','9/10'],transition=list(map(str,final)),three_worlds=world_reports,
                shared_majority=str(majority),false_independence_majority=str(naive),proxy_regression=proxy,funding_value=str(daily[1][1]-daily[0][1]),
                funding_break_even=str(r_inc),servicing_policies=policies,linguistic_proxy_contrasts=list(map(str,contrasts)),ontology_rates=ontology,
                graph_posteriors=[list(map(str,x)) for x in posteriors],feedback_posterior=list(map(str,posterior)),
                scope='Independent exact finite enumeration, covariance algebra, daily cash-flow sums and joint-graph calculations for chapters64,66,67. No new experiments, provider calls, source-code execution, causal truth or bank qualification.')

def main():
    checks=dict(deposit=deposit(),public_experiment=public_experiment(),exact_journeys=exact_journeys(),repeated_studies=repeated_studies(),corrected_width=corrected_width(),measurement_floor=measurement_floor(),investment_account=investment_account(),delegate_contracts=delegate_contracts(),flexbcf_contracts=flexbcf_contracts(),parallel_trends=parallel_trends(),financing_equivalence=financing_equivalence(),temporal_contracts=temporal_contracts(),survival_contracts=survival_contracts(),influence_contracts=influence_contracts(),fitting_contracts=fitting_contracts())
    checks['joint_law_contracts']=joint_law_contracts()
    checks['foundational_laws']=foundational_laws()
    checks['longitudinal_laws']=longitudinal_laws()
    checks['gmm_variance_contracts']=gmm_variance_contracts()
    checks['panel_continuous_laws']=panel_continuous_laws()
    checks['observation_learning_laws']=observation_learning_laws()
    checks['financial_information_laws']=financial_information_laws()
    checks['qualification_design_laws']=qualification_design_laws()
    checks['network_allocation_laws']=network_allocation_laws()
    checks['consumer_operating_laws']=consumer_operating_laws()
    checks['assistance_information_laws']=assistance_information_laws()
    source=Path(__file__);bindings[str(source.relative_to(ROOT))]=hashlib.sha256(source.read_bytes()).hexdigest()
    report=dict(status='pass',scope='Release arithmetic and retained-study reconstruction; no independent scientific acceptance, bank validity or new empirical qualification.',versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),checks=checks,bindings=bindings)
    (OUT/'numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='pass',checks=list(checks),bound_files=len(bindings),deposit=checks['deposit'],public_methods=checks['public_experiment']['methods'],repeated_summary_counts={k:v['summaries'] for k,v in checks['repeated_studies'].items()})))
if __name__=='__main__':main()
