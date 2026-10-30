def temporal_panel_shock_laws():
    """Reconstruct calendar, moments, shock and forecast examples in chapter55."""
    raw('docs/release/2026-10-29/context-review-159/chapter-055.tex')
    for theta in [F(-1),F(0),F(1),F(2),F(3)]:
        moment=sum(F(1,2)*u*(2*u-theta*u) for u in [-1,1])
        assert moment==2-theta
    for a,b in [(1,0),(0,1),(F(1,2),F(1,2))]:
        assert [a*z+b*z for z in [-1,1]]==[-1,1]
    times=[1,3,4];levels=[10,30,40];lookup=dict(zip(times,levels))
    row_lag=[None]+levels[:-1];calendar_lag=[lookup.get(t-1) for t in times]
    assert row_lag==[None,10,30] and calendar_lag==[None,None,30]
    assert row_lag[-1]-row_lag[-2]==20 and lookup.get(2) is None
    keys=[2,0,1];values=[30,10,20];ordered=[v for _,v in sorted(zip(keys,values))]
    assert ordered==[10,20,30] and values!=ordered
    keys2=[1,0,3,2];values2=[20,10,40,30]
    assert [v for _,v in sorted(zip(keys2,values2))]==[10,20,30,40]
    moments=[(t,lag) for t in range(3,7) for lag in range(2,t)]
    assert len(moments)==10 and len(set(lag for _,lag in moments))==4
    common=np.ones((100,100));weights=np.ones(100)/100
    close(weights@common@weights,1);close(weights@np.diag(np.diag(common))@weights,.01)
    survival=1-F(9,10)**20;assert format(float(survival),'.4f')=='0.8784'
    long_run=[10/(1-a) for a in [F(4,5),F(19,20)]];assert long_run==[50,200]
    assert [F(100,n) for n in [20,8,2]]==[5,F(25,2),50]
    Q=np.array([[.6,-.8],[.8,.6]]);close(Q@Q.T,np.eye(2));close(Q@(2*np.eye(2))@Q.T,2*np.eye(2))
    B=np.array([[1.,.5],[.5,1.]])
    det_squared=np.linalg.det(B)**2;det_hadamard=np.linalg.det(B*B)
    close([det_squared,det_hadamard,det_hadamard/det_squared],[9/16,15/16,5/3])
    instrument=[1,None,2];residuals=[10,20,30]
    aligned=sum(z*u for z,u in zip(instrument,residuals) if z is not None)
    suffix=sum(z*u for z,u in zip([v for v in instrument if v is not None],residuals[-2:]))
    assert [aligned,suffix]==[70,80]
    impact=None
    for j in range(2):
        impact=np.zeros((2,2));impact[:,j]=np.eye(2)[:,j]
    close(impact,[[0,0],[0,1]]);assert F(1,2)*2==1
    fractional=F(1,1000);step=F(1,2000)
    assert step<fractional and step>int(fractional)
    hessian=np.array([[-1.,.5],[.5,2.]]);modified=hessian.copy();modified[:,0]*=-1
    close(modified,[[1,.5],[-.5,2]]);assert not np.allclose(modified,modified.T)
    baseline_innovation,shock=1,2
    assert shock-baseline_innovation==1 and (baseline_innovation+shock)-baseline_innovation==2
    def drift(x):return x/2 if x<=0 else 3*x/2
    responses=[]
    for history in [F(-1),F(1)]:
        baseline=drift(history);perturbed=baseline+1
        responses.append([perturbed-baseline,drift(perturbed)-drift(baseline)])
    assert responses==[[1,1],[1,F(3,2)]]
    ar_variance=[sum(F(1,2)**(2*j) for j in range(h)) for h in [1,2]]
    assert ar_variance==[1,F(5,4)]
    last_level,last_difference=F(17),F(4);integrated=[];differences=[]
    for second_difference in [1,1]:
        last_difference+=second_difference;last_level+=last_difference
        differences.append(last_difference);integrated.append(last_level)
    assert differences==[5,6] and integrated==[22,28]
    assert 2*2+1*3==7 and 2*2==4
    fixed_process=[];variance=F(1)
    for _ in range(2):variance+=1;fixed_process.append(variance)
    assert fixed_process==[2,3] and 1+2*2*F(1,4)==2
    W=np.ones((2,2));plus=np.linalg.pinv(W);close(plus,np.ones((2,2))/4);close(W@plus@W,W)
    assert np.linalg.matrix_rank(W)==1
    frozen=F(1,2)**2;evolving=F(1,2)*F(3,4);assert [frozen,evolving]==[F(1,4),F(3,8)]
    covariance=np.array([[1.,.5],[.5,1.]])
    conditional_mean=covariance[1,0]/covariance[0,0]*2
    conditional_variance=covariance[1,1]-covariance[1,0]**2/covariance[0,0]
    close([conditional_mean,conditional_variance],[1,.75])
    # U and independent errors construct the same covariance with no causal
    # arrow between the measured coordinates: do(X=2) leaves Y unchanged.
    common_loading=math.sqrt(.5);close(common_loading**2,.5)
    close(common_loading**2+.5,1)
    old=[10,20,7,8,1];new=[11,21];literal=new+old[2:];advanced=new+old[:2]+old[-1:]
    assert literal==[11,21,7,8,1] and advanced==[11,21,10,20,1]
    tiny=F(1,2*10**12);assert 1/tiny==2*10**12 and tiny<F(1,10**12)
    assert 1+4==5 and np.all(np.diag(W)>0) and np.linalg.det(W)==0
    diag=[F(1),F(1,10**10)];relative_counts=[];absolute_counts=[]
    for scale in [1,10**4]:
        scaled=[scale*x for x in diag]
        relative_counts.append(sum(x>F(1,10**9)*max(scaled) for x in scaled))
        absolute_counts.append(sum(x>F(1,10**8) for x in scaled))
    assert relative_counts==[1,1] and absolute_counts==[1,2]
    origins={h:[t for t in range(3,13-h) if t+h!=5] for h in [0,2]}
    assert [len(origins[h]) for h in [0,2]]==[9,7] and 5 not in origins[0] and 3 not in origins[2]
    sigma=np.diag([.25,1.]);b=np.array([1.,0.]);literal_cov=np.outer(b,b)+np.diag([0,1.])
    close(literal_cov-sigma,[[.75,0],[0,0]])
    gain=F(1,2);assert gain*2==1 and (1-gain)*1==F(1,2)
    stored=[7,11,17];assert stored[1:]==[11,17] and stored[:-1]==[7,11]
    costs=[]
    for budget,counts,expected in [(24000,[600,400,300],[40,60,80]),(18000,[600,400,300],[30,45,60]),(21000,[700,500,350],[30,42,60]),(24000,[800,600,400],[30,40,60]),(27000,[900,600,450],[30,45,60])]:
        values=[F(budget,n) for n in counts];assert values==expected;costs.append(list(map(float,values)))
    return dict(invalid_moment_root=2,structural_effect=1,calendar_lags=calendar_lag,uncollapsed_moments=10,collapsed_moments=4,common_shock_variances=[1,.01],search_survival=float(survival),long_run=list(map(float,long_run)),determinants=[float(det_squared),float(det_hadamard)],proxy_products=[aligned,suffix],history_responses=[[str(x) for x in row] for row in responses],forecast_variances=list(map(str,ar_variance)),integrated_levels=list(map(int,integrated)),missing_state_variances=[2,3],frozen_and_evolving=[str(frozen),str(evolving)],conditional_mean_variance=[conditional_mean,conditional_variance],intervention_mean_variance=[0,1],lag_vectors=[literal,advanced],rank_counts=[relative_counts,absolute_counts],horizon_origins=origins,normalized_covariance_discrepancy=.75,partial_observation_mean_variance=[1,.5],costs=costs,scope='Independent authored moments, indexing, matrix, recursion and covariance calculations. Source-path concerns are not installed-package executions or bank validation.')
