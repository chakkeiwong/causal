def mediation_target_laws():
    """Enumerate nested and intervention means; preserve sensitivity scales."""
    import itertools
    raw('docs/release/2026-10-29/context-review-151/chapter-046.tex')
    base='docs/program/execution/'
    commercial=read(base+'2026-10-20/mediation-commercial-v1/exact-results.json')
    rm=read(base+'2026-10-24/mediation-reuse-reader-v1/exact-results.json')
    medflex=read(base+'2026-10-23/medflex-reuse-reader-v1/exact-results.json')
    sensitivity=read(base+'2026-10-23/sensitivity-reuse-reader-v1/exact-results.json')
    rc=read(base+'2026-10-25/r-mediation-coverage-reader-v2/exact-results.json')
    mu={(a,b):sum(F(5+4*a+2*(2+3*b+u)+a*(2+3*b+u)+v,4) for u,v in itertools.product([-1,1],repeat=2)) for a,b in itertools.product([0,1],repeat=2)}
    assert {str(a)+str(b):str(v) for (a,b),v in mu.items()}==commercial['linear_interaction']['means']
    components=[mu[1,0]-mu[0,0],mu[1,1]-mu[1,0],mu[0,1]-mu[0,0],mu[1,1]-mu[0,1]]
    assert components==[6,9,6,9] and mu[1,1]-mu[0,0]-10==5
    worlds=[];nested=[];mediator_actions=[]
    for world in ['direct','mediated']:
        law=defaultdict(F);means={};controlled=[]
        outcome=lambda a,m,u:a if world=='direct' else m^u
        for a,u in itertools.product([0,1],repeat=2):law[(a,a^u,outcome(a,a^u,u))]+=F(1,4)
        for a,b in itertools.product([0,1],repeat=2):means[str(a)+str(b)]=sum(F(outcome(a,b^u,u),2) for u in [0,1])
        for m in [0,1]:controlled.append(sum(F(outcome(0,m,u),2) for u in [0,1]))
        assert {str(k):str(v) for k,v in law.items()}==commercial['observational_equivalence']['observed'][world]
        assert {k:str(v) for k,v in means.items()}==commercial['observational_equivalence']['nested_means'][world]
        worlds.append(law);nested.append(means);mediator_actions.append(controlled[1]-controlled[0])
    assert worlds[0]==worlds[1] and mediator_actions==[0,0]
    population=sum((F(1,10)+F(x*x,10))/2 for x in [-1,1]);atmean=F(1,10)
    assert population==F(1,5) and [100*population-15,100*atmean-15]==[5,-5]
    scenarios={str(rho):2*(3-2*rho) for rho in [F(-1,2),F(0),F(1,2)]}
    assert {k:str(v) for k,v in scenarios.items()}==commercial['residual_sensitivity']['scenarios']
    rmu={(a,b):a+3*(2*b+1)+4*a*(2*b+1) for a,b in itertools.product([0,1],repeat=2)}
    indirect=[rmu[t,1]-rmu[t,0] for t in [0,1]];direct=[rmu[1,t]-rmu[0,t] for t in [0,1]]
    assert indirect==[6,14] and direct==[5,13] and rmu[1,1]-rmu[0,0]==19
    assert [indirect[t]+direct[t] for t in [0,1]]==[11,27]
    ratios=[F(i,t) for i,t in zip([1,2,9],[1,4,10])]
    assert statistics.median(ratios)==F(9,10) and F(1+2+9,1+4+10)==F(4,5)
    cluster=(1+24*F(3,5))/500;assert cluster==F(77,2500) and F(1,500)==F(rm['cluster_bootstrap']['naive_variance']['numerator'],rm['cluster_bootstrap']['naive_variance']['denominator'])
    assert sum(map(F,[1,3,100]))/3==F(104,3) and sum(map(F,[1,3]))/2==2
    p=[F(1,5),F(3,5)]
    fmu={(a,b):sum((p[b] if m else 1-p[b])*(10+2*a+5*m+4*a*m) for m in [0,1]) for a,b in itertools.product([0,1],repeat=2)}
    assert {str(a)+str(b):str(v) for (a,b),v in fmu.items()}==medflex['nested_means']
    assert fmu[1,1]-fmu[0,0]==F(32,5) and 10*(fmu[1,1]-fmu[0,0])-50==14
    scores=[F(-1),F(1)];expanded=[s for s in scores for _ in range(2)]
    assert sum(s*s for s in scores)/len(scores)**2==F(1,2) and sum(s*s for s in expanded)/len(expanded)**2==F(1,4)
    inv=[[F(1),F(2)],[F(0),F(1)]];meat=[[F(1),F(1,2)],[F(1,2),F(1)]]
    sandwich=sum(inv[0][i]*meat[i][j]*inv[0][j] for i,j in itertools.product(range(2),repeat=2));assert sandwich==7
    bias_squared=8*F(1,5)*F(1,2)/(1-F(1,5));adjusted_var=(1-F(1,2))/(1-F(1,5))*F(8,7)
    assert bias_squared==1 and adjusted_var==F(sensitivity['regression']['adjusted_variance'])
    thresholds=[]
    for ratio in [F(9,5),F(5,9)]:
        q=max(ratio,1/ratio);root=q*(q-1);assert root==F(36,25);thresholds.append(q+F(6,5))
    assert thresholds==[3,3]
    exact_rr=F(81,25)/(1-F(1,5)+F(1,5)*F(81,25));assert exact_rr==F(sensitivity['odds_ratio']['exact_rr_under_that_baseline'])
    # Enumerate dependence before and after the mediator intervention.
    pz=[F(1,4),F(1,2)];pm=[sum((zprob if z else 1-zprob)*(F(1,4)+F(z,2)) for z in [0,1]) for zprob in pz]
    ordinary=[sum((zprob if z else 1-zprob)*(F(1,4)+F(z,2))*z for z in [0,1]) for zprob in pz]
    theta={(a,b):sum((pz[a] if z else 1-pz[a])*(pm[b] if m else 1-pm[b])*z*m for z,m in itertools.product([0,1],repeat=2)) for a,b in itertools.product([0,1],repeat=2)}
    interventional=[theta[1,0]-theta[0,0],theta[1,1]-theta[1,0]]
    assert ordinary[1]-ordinary[0]==F(3,16) and interventional==[F(3,32),F(1,16)] and sum(interventional)==F(5,32)
    conditional=sum(F(1,2)*w*(F(1,4)+F(w,2)) for w in [0,1]);shuffled=F(1,2)*F(1,2)
    assert conditional==F(rc['conditional_mediator_target']) and shuffled==F(rc['global_shuffle_target'])
    joint=sum(F(m*m,2) for m in [0,1]);independent=sum(F(m1*m2,4) for m1,m2 in itertools.product([0,1],repeat=2))
    assert joint==F(1,2) and independent==F(1,4)
    reg={(a,b):3*a+4*(1+2*b)+5*a*(1+2*b) for a,b in itertools.product([0,1],repeat=2)}
    reg_effects=[reg[1,0]-reg[0,0],reg[1,1]-reg[1,0],reg[1,1]-reg[0,1],reg[0,1]-reg[0,0]]
    assert reg_effects==[8,18,18,8] and reg[1,1]-reg[0,0]==26
    components_p=[F(1,4),F(3,4)];components_y=[F(1,5),F(4,5)];prevalence=F(4,5);true={};literal={}
    for m,y in itertools.product([0,1],repeat=2):
        density=[(components_p[u] if m else 1-components_p[u])*(components_y[u] if y else 1-components_y[u]) for u in [0,1]]
        true[m,y]=(1-prevalence)*density[0]+prevalence*density[1];literal[m,y]=(1-prevalence)*sum(density)
    assert sum(true.values())==1 and sum(literal.values())==F(2,5)
    assert true[1,1]==F(49,100) and literal[1,1]==F(13,100) and literal[1,1]/sum(literal.values())==F(13,40)
    observed=F(3)/F(1,2)-(1/F(1,2)-1);missing=F(1);assert (observed+missing)/2==3
    weight_variances=[sum((w*s-2*w)**2 for s in [1,3])/2 for w in [1,2]];assert weight_variances==[1,4]
    one_sided=[4*(F(a)-F(1,2)) for a in [0,1]];aligned=[4*(F(1,2)*a+F(1,2)*(1-a)) for a in [0,1]]
    assert one_sided==[-2,2] and aligned==[2,2]
    rr=F(2)/(1-F(1,2)+F(1,2)*2);assert rr==F(4,3) and rr+F(2,3)==2
    return dict(commercial_means={str(k):str(v) for k,v in mu.items()},xor_nested=[{k:str(v) for k,v in d.items()} for d in nested],population_margins=[5,-5],sensitivity_scenarios={k:str(v) for k,v in scenarios.items()},r_indirect=indirect,r_direct=direct,cluster_variance=str(cluster),medflex_means={str(k):str(v) for k,v in fmu.items()},sandwich_factor=str(sandwich),adjusted_variance=str(adjusted_var),exact_rr=str(exact_rr),interventional_components=list(map(str,interventional)),ordinary_total=str(ordinary[1]-ordinary[0]),conditional_and_shuffled_means=list(map(str,[conditional,shuffled])),regmedint_components=reg_effects,mixture_masses=list(map(str,[sum(true.values()),sum(literal.values())])),mixture_event=list(map(str,[true[1,1],literal[1,1]])),weight_variances=weight_variances,scope='Independent nested-mean and finite-probability reconstruction under stipulated laws. Sensitivity scenarios, identification assumptions, package source behavior and empirical qualification remain distinct.')


def mediation_implementation_laws():
    """Verify selected resampling, covariance, normalization and unit witnesses."""
    import itertools
    base='docs/program/execution/2026-10-25/'
    py=read(base+'python-mediation-coverage-reader-v2/exact-results.json')
    java=read(base+'java-mediation-coverage-reader-v1/exact-results.json')
    cxx=read(base+'cxx-mediation-coverage-reader-v1/exact-results.json')
    other=read(base+'other-mediation-coverage-reader-v1/exact-results.json')
    indirect=4*(F(3,4)-F(1,4));logit=4*(math.log(3)-math.log(F(1,3)))
    assert indirect==2;close(logit,py['binary_mediator']['logit_coefficient_product'])
    sample_means=[F(a+b,2) for a,b in itertools.product([-1,1],repeat=2)]
    paired_product=sum(v*v for v in sample_means)/4;independent_product=sum(a*b for a,b in itertools.product(sample_means,repeat=2))/16
    paired_sum=sum((2*v)**2 for v in sample_means)/4;independent_sum=sum((a+b)**2 for a,b in itertools.product(sample_means,repeat=2))/16
    assert [paired_product,independent_product,paired_sum,independent_sum]==[F(1,2),0,2,1]
    contrast=2;total=(3+2*4)*contrast;doubled=(2*contrast)*(4*contrast)
    assert [2*4*contrast,doubled,total-doubled,3*contrast]==[16,32,-10,6]
    # Piecewise integration supplies the equality case independently of branch dispatch.
    intervals=[(F(0),F(3,4)),(F(3,4),F(1))];threshold=F(3,4);low=F(1,3);high=F(3)
    intended=[max(F(0),min(hi,threshold)-lo)*low+max(F(0),hi-max(lo,threshold))*high for lo,hi in intervals]
    selected=[]
    for lo,hi in intervals:
        value=(hi-lo)*low if hi<threshold else F(0)
        if lo>=threshold:value+=(hi-lo)*high
        if hi>threshold and lo<threshold:value+=(threshold-lo)*low+(hi-threshold)*high
        selected.append(value)
    assert intended==[F(1,4),F(3,4)] and selected==[F(v) for v in py['sharp_discrete_equality']['masses']]
    upper_weights=[F(1,2)]*3+[F(2)];lower_weights=[F(2)]*2+[F(1,2)]*2
    assert sum(upper_weights)/4==F(7,8) and sum(lower_weights)/4==F(5,4)
    assert sum(upper_weights)/sum(upper_weights)==sum(lower_weights)/sum(lower_weights)==1
    close((1-.001)**100,py['missed_rare_violation']['miss_probability'])
    memory=1000**2*256*4;assert memory==py['overcast_pairwise_tensor']['one_tensor_bytes']
    net=[10000*(benefit-5) for benefit in [2,8]];assert net==[-30000,30000]
    B=np.array([[0.,0.,0.],[2.,0.,0.],[3.,4.,0.]])
    omega=np.array([[1.,.25,.5],[.25,1.,0.],[.5,0.,1.]])
    inverse=np.linalg.inv(np.eye(3)-B);cov=inverse@omega@inverse.T
    close(np.linalg.det(omega),float(F(11,16)));close(cov[0,2]/cov[0,0],12.5);close(inverse[2,0],11)
    errors=np.array([[1.,0.,0.],[0.,1.,.5],[0.,.5,1.]])
    observed=inverse@errors@inverse.T;coef=np.linalg.solve(observed[:2,:2],observed[:2,2])
    close(coef,[2,4.5]);close(coef[1]*2,9)
    variance=4**2*F(1,25)+2**2*F(9,100)+2*2*4*F(1,50);assert variance==F(33,25)
    path=[('A','M1',2),('M1','M2',3),('M2','Y',4)]
    paths=[('A',F(1),0)];found=[]
    while paths:
        node,value,length=paths.pop()
        if node=='Y':found.append((value,length));continue
        paths.extend((dest,value*coef,length+1) for source,dest,coef in path if source==node)
    assert found==[(24,3)] and not [p for p in found if p[1]<=2]
    assert (F(25,2)-11)*10000*10==java['hypothetical_value']['overstatement_usd']
    joint=[(1,2),(3,6)];paired=sum(a*b for a,b in joint)/2;recombined=sum(a*b for a in [1,3] for b in [2,6])/4
    assert paired==10 and recombined==8 and (paired-recombined)*100000==200000
    eps=F(1,1000);assert 1/eps==1000 and 1/eps**2==1000000
    determinant=1-F(1,2)*F(1,2);assert determinant==F(3,4) and 1/abs(determinant)==F(4,3)
    path_names=[('Y',['M']),('M',['A'])];targets=[node for node in ['A','M','Y'] if node in {x[0] for x in path_names}]
    mapped=[[target,parents] for target,(_,parents) in zip(targets,path_names)];assert mapped==cxx['path_order']['selected_pairings']
    dosage=[F(p[1]+2*p[0]) for p in [(0,0,1),(0,1,0),(1,0,0)]]
    assert sum(dosage)/3==1 and sum(v for v in dosage if v)/2==F(3,2)
    original=other['covariance_alias']['original'];order=[1,2,0];permuted=[[original[i][j] for j in order] for i in order]
    selected_matrix=[row[:] for row in original]
    for i,j in itertools.product(range(1,3),repeat=2):selected_matrix[i-1][j-1]=selected_matrix[i][j]
    selected_matrix[2][2]=selected_matrix[0][0]
    for i in range(2):selected_matrix[i][2]=selected_matrix[i][0];selected_matrix[2][i]=selected_matrix[0][i]
    assert permuted==other['covariance_alias']['correct_permutation'] and selected_matrix==other['covariance_alias']['selected_inplace']
    close(np.linalg.det(permuted),500);close(np.linalg.det(selected_matrix),0)
    samples=list(itertools.product([0,1],repeat=2));means=[F(sum(s),2) for s in samples];accepted=[m for s,m in zip(samples,means) if len(set(s))==2]
    variance_mean=lambda values:sum((v-sum(values)/len(values))**2 for v in values)/len(values)
    assert variance_mean(means)==F(1,8) and variance_mean(accepted)==0 and variance_mean([2*m for m in means])==F(1,2)
    assert [1-2*a for a in [F(1,4),F(1,40)]]==[F(1,2),F(19,20)]
    close(2*norm.sf(-1),other['signed_two_sided_tail']['selected']);close(2*norm.sf(1),other['signed_two_sided_tail']['absolute_value_reference'])
    # Gaussian identities use exact moments; no random draws are required.
    assert F(1)+F(0)**2==1 and F(1,2)+F(0)*F(0)==F(1,2)
    assert 5**3==125 and 10*5**3==1250 and F(1,2)*100000==50000
    return dict(binary_indirect=str(indirect),mixed_scale_product=logit,bootstrap_moments=list(map(str,[paired_product,independent_product,paired_sum,independent_sum])),sharp_intended_masses=list(map(str,intended)),sharp_selected_masses=list(map(str,selected)),constant_weight_mass=list(map(str,[sum(upper_weights)/4,sum(lower_weights)/4])),rare_violation_miss=(1-.001)**100,pairwise_bytes=memory,net_interval=net,treatment_error_covariance_ratio=float(cov[0,2]/cov[0,0]),regression_path_coefficients=coef.tolist(),product_variance=str(variance),path_total=24,paired_product=paired,recombined_product=recombined,cyclic_normalizer=str(determinant),mapped_paths=mapped,dosages=list(map(str,dosage)),permuted_covariance=permuted,aliased_covariance=selected_matrix,conditional_bootstrap_variance='0',scope='Independent algebra, matrix propagation and finite-resample enumeration for inspected implementation witnesses. No acquired package executed, native failure rate inferred or sampling coverage established.')


def dose_decision_laws():
    """Reconstruct density units, covariance and dose economics."""
    raw('docs/release/2026-10-29/context-review-151/chapter-046.tex')
    previous=read('docs/program/execution/2026-10-24/dose-response-reader-v1/exact-results.json')
    slope=F(2)+3*F(1,2);assert slope==F(7,2) and [100*slope-220,100*2-220]==[130,-20]
    marginal,residual=F(1,5),F(2,5);scales=[F(2),F(1,2)]
    proper=[marginal/(residual/s) for s in scales];assert proper==[F(1),F(1,4)]
    assert F(1,5)/4==F(1,20) and F(1,5)/F(1,10)==F(1,500)/F(1,1000)==2
    x=list(map(F,[-2,-1,1,2]));a=[v*v for v in x];mean=lambda v:sum(v)/len(v)
    covariance=mean([xx*aa for xx,aa in zip(x,a)])-mean(x)*mean(a);assert covariance==0 and len(set(a))==2
    weighted=lambda w,y:sum(ww*yy for ww,yy in zip(w,y))/sum(w)
    ess=lambda w:sum(w)**2/sum(v*v for v in w)
    original=list(map(F,[1,1,8]));capped=list(map(F,[1,1,2]));outcome=list(map(F,[0,0,100]))
    assert weighted(original,outcome)==80 and weighted(capped,outcome)==50
    assert ess(original)==F(50,33) and ess(capped)==F(8,3) and F(4,5)*10+F(1,5)*100==28
    misses=[set(range(5)),set(range(5,10))];coverages=[F(100-len(s),100) for s in misses];joint=F(100-len(set.union(*misses)),100)
    assert coverages==[F(19,20)]*2 and joint==F(9,10)
    assert (F(1,40)*20).__floor__()==0 and (F(1,40)*40).__floor__()==1
    contrast=list(map(F,[-1,0,1]));signal=sum(c*y for c,y in zip(contrast,[0,1,2]));var=sum(c*c*F(1,100) for c in contrast)
    assert signal==2 and var==F(1,50) and signal**2/var==200
    adjusted=[[F(1,50),F(1,100)],[F(1,100),F(1,50)]];cc=[-1,1]
    avar=sum(cc[i]*adjusted[i][j]*cc[j] for i in range(2) for j in range(2));assert avar==var
    assert sum(cc[i]**2*adjusted[i][i] for i in range(2))==F(1,25)
    response=lambda dose:4*dose/(1+dose);profit=lambda dose:response(dose)-2*dose
    assert response(F(1,3))==1 and [profit(F(a)) for a in [0,1,2]]==[0,0,F(-4,3)]
    optimum=math.sqrt(2)-1;close(4/(1+optimum)**2-2,0);assert -8/(1+optimum)**3<0
    close(optimum,previous['contrasts']['optimum_dose'])
    assert [F(2400,n) for n in [100,80,60]]==[24,30,40]
    return dict(observational_slope=str(slope),decision_margins=[130,-20],proper_density_ratios=list(map(str,proper)),nonlinear_covariance=str(covariance),weighted_means=[80,50],ess=list(map(str,[ess(original),ess(capped)])),pointwise_coverage=list(map(str,coverages)),joint_coverage=str(joint),contrast_variance=str(var),shared_baseline_variance=str(avar),target_dose='1/3',optimal_dose=optimum,net_values=[str(profit(F(a))) for a in [0,1,2]],scope='Independent exact reconstruction of dose-target, density-unit, weight, covariance and financial examples. Historical paper figures remain attributed reported values; no native trial or empirical calibration.')


