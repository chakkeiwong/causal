def synthetic_target_laws():
    """Reconstruct donor, target and fitting choices from stated synthetic laws."""
    raw('docs/release/2026-10-29/context-review-159/chapter-053.tex')
    donors=np.array([[90,110,120],[110,130,140]],float)
    treated=np.array([100,120,150.]);weights=np.array([.5,.5])
    close(weights@donors,[100,120,130]);close(treated[-1]-(weights@donors)[-1],20)
    contaminated=donors.copy();contaminated[1,-1]=160
    close(weights@contaminated,[100,120,140]);close(np.array([.25,.75])@contaminated,[105,125,150])
    effects=[F(-6),F(10)];weighted=sum(w*v for w,v in zip([9,1],effects))/10
    assert sum(effects)/2==2 and weighted==F(-22,5)
    duration=[F(10),F(10),F(10),F(-6)]
    assert sum(duration)/4==6 and (sum(duration[:3])/3+duration[3])/2==2
    factors=np.array([[1,0],[2,0],[1,1.]])
    predictions=[factors@load for load in [np.array([2,0]),np.array([2,4])]]
    close(predictions[0][:2],predictions[1][:2]);close([8-p[-1] for p in predictions],[6,2])
    treatment=np.array([[0,1,1],[0,0,1.]])
    outcome=np.array([[0,1,4],[0,0,1.]])
    units=np.repeat(np.arange(2),3);dates=np.tile(np.arange(3),2)
    design=np.column_stack([np.ones(6),units,dates==1,dates==2,treatment.ravel()])
    q,r=np.linalg.qr(design,mode='reduced');twfe=np.linalg.solve(r,q.T@outcome.ravel())[-1]
    close(twfe,-.5);close(outcome[treatment==1].mean(),2)
    assert F(1,2)+F(4,2)==F(5,2) and F(3,4)+4*F(1,4)==F(7,4)
    values=np.array([1.,2.,3.]);entities=np.array([0,0,1]);times=np.array([0,1,0])
    transformed=values-np.array([values[entities==i].mean() for i in entities])-np.array([values[times==t].mean() for t in times])+values.mean()
    close(transformed,[-.5,.5,0]);assert any(abs(sum(transformed[times==t]))>1e-8 for t in [0,1])
    simple_donors=[F(80),F(120)];original_gap=120-sum(simple_donors)/2
    assert original_gap==20 and 120-(80+160)/2==0 and 120-simple_donors[1]==0
    assert statistics.median([0,0,9])==statistics.median([0,0,12])==0 and statistics.mean([0,0,12])==4
    metric=[F(-1),F(2)];absolute=[abs(v)/sum(abs(x) for x in metric) for v in metric]
    signed=[abs(v)/sum(metric) for v in metric]
    assert absolute==[F(1,3),F(2,3)] and signed==[1,2]
    w=F(3,4);assert (w-F(1,2))**2==F(1,16) and 2*(w-F(1,2))==F(1,2)
    X=np.array([[-1.],[1.]]);x=np.array([2.]);base=np.array([0.,1.]);lam=2
    augmented=base+X@np.linalg.solve(X.T@X+lam*np.eye(1),x-X.T@base)
    close(augmented,[-.25,1.25]);close(x-X.T@augmented,.5);close(abs(augmented).sum(),1.5)
    close(augmented@np.array([80,120.]),130);close(150-augmented@np.array([80,120.]),20)
    grid=[4*F(1,16)**F(i,2) for i in range(3)];close(grid,[4,1,.25])
    losses=np.array([[0,0,0,100],[4,4,4,4.]])
    close(losses[:,:3].mean(1),[0,4]);close(losses.mean(1),[25,4])
    assert np.argmin(losses[:,:3].mean(1))!=np.argmin(losses.mean(1))
    # All donors share identical pretreatment history; objective ties cannot
    # determine the post-treatment contrast.
    post_gaps=[150-(a*100+(1-a)*200) for a in [F(1),F(1,2),F(0)]]
    assert post_gaps==[50,0,-50]
    return dict(stata_equal_weight_gap=20,contaminated_gap=10,postselected_gap=0,gsynth_unit_mean=2,gsynth_exposure_mean=str(weighted),duration_targets=[6,2],factor_effects=[6,2],twfe=float(twfe),att=2,one_pass_unbalanced=transformed.tolist(),synth_gaps=[int(original_gap),0,0],ridge_weights=augmented.tolist(),ridge_counterfactual=130,cv_means=[losses[:,:3].mean(1).tolist(),losses.mean(1).tolist()],nonunique_weight_gaps=list(map(float,post_gaps)),scope='Independent authored target, matrix and fitting reconstructions; no native runs or identification claim.')


def synthetic_uncertainty_laws():
    """Reconstruct reported tails, normalization, calendars and failure bounds."""
    raw('docs/release/2026-10-29/context-review-159/chapter-053.tex')
    interval=[100-5-10,100+5+10];assert interval==[85,115]
    effect_interval=[120-interval[1],120-interval[0]];assert effect_interval==[5,35]
    assert 1-F(5,100)-F(5,100)==F(9,10)
    draws=np.array([0.]*9+[100.]);close(np.quantile(draws,.975),77.5);close(np.quantile(draws[:-1],.975),0)
    matrix=np.diag([-1.,4.]);u,s,vh=np.linalg.svd(matrix);root=u@np.diag(np.sqrt(s))
    close(root@root.T,np.diag([1,4]));assert not np.allclose(root@root.T,matrix)
    effects=[F(2),F(4),F(10)]
    assert sum(effects)/3==F(16,3) and ((effects[0]+effects[1])/2+effects[2])/2==F(13,2)
    assert sum(a*b for a,b in zip(effects,[1,1,4]))/6==F(23,3)
    treatment=[0,1,0,0,1,0];carry=[2 if i and not a and treatment[i-1] else a for i,a in enumerate(treatment)]
    assert carry==[0,1,2,0,1,2]
    errors=[F(1),F(9)];counts=[100,1]
    assert sum(errors)/2==5 and sum(e*n for e,n in zip(errors,counts))/sum(counts)==F(109,101)
    means=np.array([1.2,1,1.1]);best=int(np.argmin(means))
    chosen=[best,int(np.flatnonzero(means<=means[best]*1.01)[0]),int(np.flatnonzero(means<=means[best]+.3)[0])]
    assert chosen==[1,1,0]
    E=np.diag([12.,4.]);u,s,vh=np.linalg.svd(E/4);thresholded=(u@np.diag(np.maximum(s-1.5,0))@vh)*4
    close(thresholded,np.diag([6,0]))
    null=np.arange(-2,3);quantiles=np.quantile(null,[.25,.75])
    close(20-quantiles[::-1],[19,21]);close(20-(10+quantiles[::-1]),[9,11])
    ratios=[4,4,1];inclusive=[F(sum(y>=x for y in ratios),len(ratios)) for x in ratios]
    assert inclusive==[F(2,3),F(2,3),1] and [F(i,3) for i in [1,2,3]]!=inclusive
    assert F(1,19+1)==F(1,20) and F(1,5)==F(1,5)
    replicates=[F(0),F(2)];ss=sum((x-sum(replicates)/2)**2 for x in replicates)
    assert ss==2 and F(3,4)*ss==F(3,2) and F(1,2)*ss==1
    missing_bounds=[F(2,19),F(2+9,19)];assert F(2,10)==F(1,5)
    gap=np.array([1.,1.,4.,2.]);cut=2
    overlap=(sum(gap[cut:]**2)/(len(gap)-(cut+1)))/(sum(gap[:cut+1]**2)/(cut+1))
    inclusive_pre=np.mean(gap[cut+1:]**2)/np.mean(gap[:cut+1]**2)
    exclusive_pre=np.mean(gap[cut:]**2)/np.mean(gap[:cut]**2)
    close([overlap,inclusive_pre,exclusive_pre],[10/3,2/3,10])
    assert sum([2,2])==4 and sum(x*d for x,d in zip([2,2],[1,3]))==8
    covariance=np.ones((2,2));close(np.ones(2)@covariance@np.ones(2),4);close(np.trace(covariance),2)
    close(120-np.array([90,110]),[30,10]);close(120-np.array([70,130]),[50,-10])
    paths=np.array([[1.,-1.],[-1.,1.]])
    close(np.sqrt((paths**2).mean(1)).mean(),1);close(np.sqrt((paths.mean(0)**2).mean()),0)
    def variance(xs):
        mu=sum(xs)/len(xs)
        return sum((x-mu)**2 for x in xs)/(len(xs)-1)
    assert variance([F(2),F(4),F(10)])==F(52,3) and variance([F(2),F(4),F(6),F(10)])==F(35,3)
    incomplete_ranks=[F(1,5),F(3,5)];assert incomplete_ranks[0]<=F(1,3)<=incomplete_ranks[1]
    return dict(scpi_prediction=interval,scpi_effect=effect_interval,filtered_quantiles=[77.5,0],fect_targets=list(map(str,[F(16,3),F(13,2),F(23,3)])),carryover=carry,fect_selection=chosen,thresholded=thresholded.tolist(),basic_intervals=[[19,21],[9,11]],inclusive_tails=list(map(str,inclusive)),missing_permutation_bounds=list(map(str,missing_bounds)),calendar_ratios=[float(overlap),float(inclusive_pre),float(exclusive_pre)],duration_totals=[4,8],cumulative_variances=[4,2],placebo_variances=[str(F(52,3)),str(F(35,3))],coresynth_bounds=list(map(str,incomplete_ranks)),scope='Exact examples distinguish uncertainty objects and denominators; no exchangeability, empirical coverage or native qualification is inferred.')


def impact_prediction_laws():
    """Verify target reversal and observationally equivalent impact laws."""
    raw('docs/release/2026-10-29/context-review-159/chapter-054.tex')
    high=F(1,2);treat_high=F(4,5);treat_low=F(1,5)
    treated_high=high*treat_high/(high*treat_high+(1-high)*treat_low)
    ate=high*400+(1-high)*100;att=treated_high*400+(1-treated_high)*100
    assert ate==250 and att==340 and [ate-300,att-300]==[-50,40]
    joint=F(19,20)**10;assert format(float(joint),'.7f')=='0.5987369'
    times=np.arange(1,13);action=(times>8).astype(int);x0=10+times
    observed_x=x0+15*action;observed_y=100+2*x0+20*action
    law_a_y0=100+2*x0;law_b_y0=100+2*observed_x
    law_b_y1=law_b_y0-10;law_b_observed=np.where(action,law_b_y1,law_b_y0)
    close(observed_y,law_b_observed);close(observed_y[action==1]-law_a_y0[action==1],20)
    close(observed_y[action==1]-law_b_y0[action==1],-10)
    net=[int(sum((observed_y-y0)[action==1])-20) for y0 in [law_a_y0,law_b_y0]];assert net==[60,-60]
    draws=np.array([[80.,120.],[120,80],[80,120],[120,80]])
    marginal=np.quantile(draws,[.025,.975],axis=0);totals=draws.sum(1)
    close(marginal,[[80,80],[120,120]]);close(np.quantile(totals,[.025,.975]),[200,200])
    close(marginal.sum(1),[160,240]);close(220-totals,20)
    denominators=[F(-1),F(1),F(2)];relative=[10/x-1 for x in denominators]
    assert relative==[-11,9,4] and sum(relative)/3==F(2,3) and 10/(sum(denominators)/3)-1==14
    predictive=list(totals)+[220];p=min(sum(v<=220 for v in predictive),sum(v>=220 for v in predictive))/len(predictive);close(p,.2)
    balances=[10000]*3;assert balances[-1]==10000 and sum(balances)==30000
    return dict(ate=int(ate),att=int(att),net_by_target=[-50,40],pointwise_joint=float(joint),observationally_equivalent=True,causal_effects=[20,-10],four_day_net=net,predictive_total_interval=[200,200],sum_marginal_interval=[160,240],cumulative_effect=20,relative_draws=list(map(str,relative)),relative_mean=str(sum(relative)/3),ratio_of_means=14,simulation_tail=p,stock=10000,balance_days=30000,scope='Independent authored probability, observational-equivalence and draw-aggregation calculations; no fitted experiment or calibrated causal interpretation.')
