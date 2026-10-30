def relationship_audit_design_laws():
    """Enumerate relationship/action laws and reconstruct audit design bounds."""
    raw('docs/release/2026-10-29/context-review-162/chapter-056.tex')
    from itertools import product
    from decimal import Decimal,localcontext
    states=list(product([0,1],repeat=2))
    def exposure(theta,p,r):
        graph={(1,1):theta,(0,0):theta,(1,0):F(1,2)-theta,(0,1):F(1,2)-theta}
        action={(1,1):r,(0,0):1-2*p+r,(1,0):p-r,(0,1):p-r}
        assert sum(graph.values())==sum(action.values())==1 and min(graph.values())>=0 and min(action.values())>=0
        return sum(pg*pa*int(any(g[i]*a[i] for i in [0,1])) for g,pg in graph.items() for a,pa in action.items())
    independent_values=[];coordinated=[]
    for theta in [F(0),F(1,4),F(1,2)]:
        for p in [F(1,5),F(3,5)]:assert exposure(theta,p,p*p)==p-p*p*theta
        value=100*(exposure(theta,F(3,5),F(9,25))-exposure(theta,F(1,5),F(1,25)))-16-16
        assert value==8-32*theta;independent_values.append(value)
        row=[]
        for r in [F(9,25),F(3,5),F(1,5)]:
            v=100*(exposure(theta,F(3,5),r)-exposure(theta,F(1,5),F(1,5)))-32
            assert v==8-100*(r-F(1,5))*theta;row.append(v)
        coordinated.append(row)
    assert independent_values==[8,0,-8] and coordinated[0]==[8,8,8] and coordinated[-1]==[0,-12,8]
    source_edges=[(0,1),(2,3),(4,5),(6,7)];target_edges=[(4,5),(5,6),(6,7),(7,4)]
    def graph_exposure(edges,p):
        neighbors=[set() for _ in range(8)]
        for i,j in edges:neighbors[i].add(j);neighbors[j].add(i)
        total=F(0)
        for actions in product([0,1],repeat=8):
            probability=p**sum(actions)*(1-p)**(8-sum(actions))
            total+=probability*sum(any(actions[j] for j in neighbors[i]) for i in range(8))/8
        return total
    topology=[]
    for edges in [source_edges,target_edges]:
        low,high=[graph_exposure(edges,p) for p in [F(1,5),F(3,5)]]
        topology.append([low,high,100*(high-low)-8-24])
    assert [row[-1] for row in topology]==[8,-8]
    feasible=[(F(1,6),F(1,2)),(F(1,3),F(0))]
    values=[]
    for t0,t1 in feasible:
        assert F(3,4)*t0+F(1,4)*t1==F(1,4)
        values.append(22-8*t0-48*t1)
    assert values==[F(-10,3),F(58,3)]
    # Enumerate all vertices of the line/box intersection rather than choosing
    # incompatible marginal extrema.
    vertices=set()
    for coordinate in [0,1]:
        for bound in [F(0),F(1,2)]:
            point=(bound,1-3*bound) if coordinate==0 else ((1-bound)/3,bound)
            if all(0<=v<=F(1,2) for v in point):vertices.add(point)
    assert vertices==set(feasible) and 22-8*F(1,4)-48*F(1,4)==8
    mixture=[mean+noise for mean in [-8,8] for noise in [-1,1]]
    assert sum(F(v*v,4) for v in mixture)==65
    with localcontext() as context:
        context.prec=60
        threshold=Decimal(128)*Decimal(40).ln();r472=(Decimal(40).ln()/(2*472)).sqrt();r473=(Decimal(40).ln()/(2*473)).sqrt()
        assert 472<threshold<473 and 2*r472>=Decimal(1)/8 and 2*r473<Decimal(1)/8
    variance=lambda n0,n1:F(16,n0)+F(576,n1)
    assert variance(100,600)==F(28,25) and variance(525,175)==F(1744,525)
    assert variance(140,420)==F(52,35) and variance(780,260)==F(436,195)
    # Enumerate every feasible positive integer allocation for the two budgets.
    best_count=min((variance(n,700-n),n,700-n) for n in range(1,700))
    best_price=min((variance(1820-4*n,n),1820-4*n,n) for n in range(1,455))
    assert best_count==(F(28,25),100,600) and best_price==(F(52,35),140,420)
    for lam in [F(-20),F(0),F(32,3),F(24),F(100),F(192),F(300)]:
        a0,a1=-8+F(3,4)*lam,-48+F(1,4)*lam
        assert a0-3*a1==136
        for theta0,theta1 in feasible+[(F(1,4),F(1,4))]:
            assert 22-lam/4+a0*theta0+a1*theta1==22-8*theta0-48*theta1
        for price_root in [F(1),F(2),F(3),F(4)]:
            norm=abs(a0)+price_root*abs(a1)
            assert norm>=136*min(F(1),price_root/3)
    constrained=[F(136,3)**2/(4*700),F(136,3)**2/(4*455)]
    assert constrained==[F(1156,1575),F(4624,4095)]
    laws=0
    for theta0,theta1 in feasible+[(F(1,4),F(1,4))]:
        for n0,n1,lam in [(0,2,F(32,3)),(2,0,F(192)),(2,3,F(0)),(1,1,F(24))]:
            a0,a1=-8+F(3,4)*lam,-48+F(1,4)*lam;terms=[]
            for k0,k1 in product(range(n0+1),range(n1+1)):
                prob=F(math.comb(n0,k0))*theta0**k0*(1-theta0)**(n0-k0)*F(math.comb(n1,k1))*theta1**k1*(1-theta1)**(n1-k1)
                value=22-lam/4+(a0*F(k0,n0) if n0 else 0)+(a1*F(k1,n1) if n1 else 0)
                terms.append((prob,value))
            mean=sum(p*v for p,v in terms);var=sum(p*(v-mean)**2 for p,v in terms)
            assert sum(p for p,v in terms)==1 and mean==22-8*theta0-48*theta1
            assert var==(a0*a0*theta0*(1-theta0)/n0 if n0 else 0)+(a1*a1*theta1*(1-theta1)/n1 if n1 else 0)
            laws+=1
    a,b=F(-32,3),F(-136,3);assert [a*a,b*b,2*a*b]==[F(1024,9),F(18496,9),F(8704,9)]
    return dict(independent_graph_values=list(map(str,independent_values)),coordinated_values=[[str(x) for x in row] for row in coordinated],topology_results=[[str(x) for x in row] for row in topology],pooled_sharp_set=list(map(str,values)),completion_variance=65,audit_threshold=str(threshold),audit_radius473=str(r473),optimal_count=[str(best_count[0]),100,600],optimal_budget=[str(best_price[0]),140,420],pooled_envelopes=list(map(str,constrained)),enumerated_audit_laws=laws,noisy_pool_variance_coefficients=list(map(str,[a*a,b*b,2*a*b])),scope='Independent exact global action enumeration, feasible-set vertices, complete integer allocations and finite audit sampling laws. Optimality remains scoped to the declared variance envelope and information; no bank audit is claimed.')


def transport_completion_laws():
    """Check transport scores, imputation, support and covariance examples."""
    raw('docs/release/2026-10-29/context-review-162/chapter-056.tex')
    from itertools import product
    # A finite heterogeneous law checks the augmented functional under either
    # correct response or correct selection/assignment models.
    mass=[F(2,5),F(3,5)];rho=[F(4,5),F(1,5)];e=[F(1,4),F(3,4)]
    means=[[F(2),F(5)],[F(-1),F(7)]];p0=sum(m*(1-r) for m,r in zip(mass,rho))
    target=sum(m*(1-r)*(mu[1]-mu[0]) for m,r,mu in zip(mass,rho,means))/p0
    def augmented(rstar,estar,mstar):
        total=F(0)
        for x,s,a in product(range(2),[0,1],[0,1]):
            prob=mass[x]*(rho[x] if s else 1-rho[x])*(e[x] if a else 1-e[x])
            outcome=means[x][a]
            residual=(a/estar[x]*(outcome-mstar[x][1])-(1-a)/(1-estar[x])*(outcome-mstar[x][0]))
            total+=prob*((1-s)*(mstar[x][1]-mstar[x][0])+s*(1-rstar[x])/rstar[x]*residual)
        return total/p0
    assert augmented(rho,e,[[F(0),F(0)],[F(0),F(0)]])==target
    assert augmented([F(1,2)]*2,[F(1,2)]*2,means)==target
    risk0,risk1=F(1,10),F(1,5)
    assert risk1-risk0==F(1,10) and risk1/(1-risk1)/(risk0/(1-risk0))==F(9,4)
    source_support={(0,0),(1,1)};target_point=(0,1)
    assert target_point not in source_support and all(min(p[j] for p in source_support)<=target_point[j]<=max(p[j] for p in source_support) for j in [0,1])
    p,assignment=F(4,5),F(1,2)
    correct=p*assignment*((1-p)/p)*(1/assignment)/(1-p)
    reversed_score=p*assignment*(p/(1-p))*(1/assignment)/(1-p)
    assert correct==1 and reversed_score==16 and (reversed_score-correct)*10000*10==1500000
    assert p*assignment/(1-p)==2 and p*assignment==F(2,5)
    assert F(3,10)*2==F(3,5)
    estimates=[F(0),F(2),F(4)];mean=sum(estimates)/3;between=sum((v-mean)**2 for v in estimates)/2
    total=1+F(4,3)*between;synthetic=1+between/3;r=F(4,3)*between;df=2*(1+1/r)**2
    assert between==4 and total==F(19,3) and synthetic==F(7,3) and df==F(361,128)
    assert (F(1,2)*F(4,5))/(F(1,2)*F(4,5)+F(1,2)*F(1,5))==F(4,5)
    rejection=F(9,10)**26;assert 0<rejection<1
    assert 1/(F(1)**2+F(3)**2)==F(1,10) and 1/(F(1,4)**2+F(3,4)**2)==F(8,5)
    prevalence=np.array([.25,.75]);probability=np.ones((2,2))*.5
    row_stabilized=prevalence[:,None]/probability;column_stabilized=prevalence[None,:]/probability
    close(row_stabilized,[[.5,.5],[1.5,1.5]]);close(column_stabilized,[[.5,1.5],[.5,1.5]])
    close(np.diag(row_stabilized),np.diag(column_stabilized));close(np.clip([.98,.01,.01],.1,.9).sum(),1.1)
    binary=F(1,4);assert binary*(1-binary)==F(3,16)
    vectors=np.array([[0.,0],[2,2],[4,4]])
    pooled=np.eye(2)+(1+1/3)*np.cov(vectors,rowvar=False,ddof=1)
    close(pooled,[[19/3,16/3],[16/3,19/3]]);contrast=np.array([1.,-1.])
    close(contrast@pooled@contrast,2);close(contrast@np.diag(np.diag(pooled))@contrast,38/3)
    close(math.sqrt(3-0-3),0);close(2*norm.sf(0),1)
    close(contrast@np.ones((2,2))@contrast,0);close(contrast@np.eye(2)@contrast,2)
    assert 1+F(1,4)==F(5,4)
    graphs=[{('A','B'),('B','C')},{('B','C'),('C','A')},{('C','A'),('A','B')}]
    majority={edge for edge in set.union(*graphs) if sum(edge in graph for graph in graphs)>len(graphs)/2}
    assert majority=={('A','B'),('B','C'),('C','A')}
    rows=np.array([[1,1,np.nan],[-1,-1,np.nan],[1,np.nan,1],[-1,np.nan,-1],[np.nan,1,-1],[np.nan,-1,1.]])
    covariance=np.zeros((3,3))
    for i,j in product(range(3),repeat=2):
        keep=np.isfinite(rows[:,i])&np.isfinite(rows[:,j]);x=rows[keep,i];y=rows[keep,j]
        covariance[i,j]=np.dot(x-x.mean(),y-y.mean())/(len(x)-1)
    close(covariance,[[4/3,2,2],[2,4/3,-2],[2,-2,4/3]]);v=np.array([-1.,1.,1.]);close(v@covariance@v,-8)
    assert (0*1+2*3)/4==1.5 and F(1,2)*F(3,4)/(F(1,2)*F(3,4)+F(1,2)*F(1,4))==F(3,4)
    assert sum(F(x,2) for x in [0,2])==1 and sum(F(x*x,2) for x in [0,2])==2
    # Observational conditioning and surgery are enumerated on the same SCM.
    factual=[(u,u,u,F(1,2)) for u in [0,1]]
    conditional=sum(y*w for u,a,y,w in factual if a==1)/sum(w for u,a,y,w in factual if a==1)
    intervention=sum(u*F(1,2) for u in [0,1]);assert conditional==1 and intervention==F(1,2)
    pseudocounts=[F(c+1,4) for c in [2,0]];assert pseudocounts==[F(3,4),F(1,4)]
    assert F(9,10)-F(1,10)==F(4,5)
    assert int(F(7,3))==2 and [int(10000*(.5-.001)),int(10000*(.5+.001))]==[4990,5010]
    assert (0+10)/2==5 and F(1-0,10-0)*10==1
    # Both observed-data laws agree exactly despite opposite missing outcomes.
    observed=[];true_effects=[]
    for hidden_effect in [-10,10]:
        law={};effect=F(0)
        for h,a in product([0,1],repeat=2):
            y1=10 if h else hidden_effect;y=a*y1;key=(a,h,h*y)
            law[key]=law.get(key,F(0))+F(1,4);effect+=F(y1,4)
        observed.append(law);true_effects.append(effect)
    assert observed[0]==observed[1] and true_effects==[0,10]
    states=list(product([0,1],repeat=2));transition_uv=[];transition_vu=[]
    for u,v in states:
        row_uv=[];row_vu=[]
        for up,vp in states:
            pv=F(1,4) if up==0 else F(3,4);old_pv=F(1,4) if u==0 else F(3,4)
            row_uv.append(F(1,2)*(pv if vp else 1-pv));row_vu.append((old_pv if vp else 1-old_pv)*F(1,2))
        transition_uv.append(row_uv);transition_vu.append(row_vu)
    for probability,transition in [([F(3,8),F(1,8),F(1,8),F(3,8)],transition_uv),([F(1,4)]*4,transition_vu)]:
        assert [sum(probability[i]*transition[i][j] for i in range(4)) for j in range(4)]==probability
    assert (F(3,4)/F(1,4))/(F(1,4)/F(3,4))==9
    close(math.exp((math.log(1)+math.log(9))/2),3);assert (1+9)/2==5
    source=[F(4,5),F(1,5)];target_weights=[F(1,5),F(4,5)];effects=[10,-10]
    assert sum(p*v for p,v in zip(source,effects))==6 and sum(p*v for p,v in zip(target_weights,effects))==-6
    recovered=F(0);response=[[F(1,2),F(3,4)],[F(2,3),F(4,5)]];assignment=[F(1,4),F(3,4)]
    for x,a,r_obs in product([0,1],repeat=3):
        pa=assignment[x] if a else 1-assignment[x];pr=response[x][a]
        mass=source[x]*pa*(pr if r_obs else 1-pr);y=a*effects[x]
        recovered+=mass*(target_weights[x]/source[x])*(2*a-1)*r_obs*y/(pa*pr)
    assert recovered==-6 and [2+F(4,5)*v-2 for v in [-10,10]]==[-8,8]
    return dict(heterogeneous_augmented_target=str(target),correct_and_reversed_scores=[str(correct),str(reversed_score)],binary_risk_difference=str(risk1-risk0),odds_ratio='9/4',pooling_variances=[str(total),str(synthetic)],pooling_df=str(df),rejection_probability=float(rejection),effective_sample_sizes=['1/10','8/5'],pooled_covariance=pooled.tolist(),contrast_variance=2,pairwise_covariance=covariance.tolist(),pairwise_quadratic=-8,missing_outcome_effects=list(map(str,true_effects)),incompatible_scan_stationary=[['3/8','1/8','1/8','3/8'],['1/4']*4],transport_recovered=str(recovered),support_net_set=[-8,8],scope='Independent finite probability enumeration, matrix reconstruction and typed arithmetic for declared authored laws. No fitted package performance, general MNAR recovery, calibration or rights clearance is claimed.')


def observation_history_units_laws():
    """Check linkage, availability, sample inclusion, hazards and density units."""
    raw('docs/release/2026-10-29/context-review-162/chapter-056.tex')
    raw('docs/release/2026-10-29/context-review-162/chapter-059.tex')
    p=F(4,5);map_contrasts=[F(8+6,2)-F(4+2,2),F(4+2,2)-F(8+6,2)]
    assert map_contrasts==[4,-4]
    outcomes=[(p*F(1,2),4+noise) for noise in [F(-1,2),F(1,2)]]+[((1-p)*F(1,2),-4+noise) for noise in [F(-1,2),F(1,2)]]
    mean=sum(prob*y for prob,y in outcomes);variance=sum(prob*(y-mean)**2 for prob,y in outcomes)
    assert mean==F(12,5) and variance==F(1049,100) and 10*mean-30==-6
    assert 80*F(7,8)-70==0
    versions=[{'value':2,'event':8,'available':9},{'value':9,'event':9,'available':12}];decision=10
    event_only=max((v for v in versions if v['event']<=decision),key=lambda v:v['event'])
    usable=max((v for v in versions if v['event']<=decision and v['available']<=decision),key=lambda v:v['event'])
    assert [event_only['value'],usable['value']]==[9,2]
    proportions=[F(1,2)]*2;retention=[F(1),F(1,4)];effects=[F(6),F(2)]
    retained=[a*b for a,b in zip(proportions,retention)];linked=sum(p*e for p,e in zip(retained,effects))/sum(retained)
    corrected=sum(p/r*e for p,r,e in zip(retained,retention,effects))/sum(p/r for p,r in zip(retained,retention))
    assert linked==F(26,5) and corrected==4
    hazards=[F(1,10),F(1,5)];competing=[F(1,20),F(1,10)];survival=F(1);contributions=[]
    for y,d in zip(hazards,competing):
        contributions.append(survival*(1-d)*y);survival*=(1-d)*(1-y)
    incidence=sum(contributions);eliminated=1-math.prod(1-y for y in hazards)
    assert contributions==[F(19,200),F(1539,10000)] and incidence==F(2489,10000) and eliminated==F(7,25)
    assert (eliminated-incidence)*10000*100==31100
    density=norm.pdf(0);close([density,density/2],[.3989422804014327,.19947114020071635])
    # Integrating in each physical unit system verifies the Jacobian, rather
    # than merely comparing a displayed value at the mean.
    from scipy.integrate import quad
    for scale in [1,2]:
        physical=quad(lambda a:norm.pdf(a/scale)/scale,-scale,scale)[0]
        converted=quad(lambda z:norm.pdf(z/(100*scale))/(100*scale),-100*scale,100*scale)[0]
        close(physical,converted);close(physical,norm.cdf(1)-norm.cdf(-1))
    return dict(linkage_contrasts=list(map(int,map_contrasts)),linkage_mean=str(mean),linkage_variance=str(variance),linkage_net=-6,positive_threshold='7/8',historical_features=[event_only['value'],usable['value']],linked_effect=str(linked),inclusion_corrected_effect=str(corrected),competing_incidence=str(incidence),eliminated_incidence=str(eliminated),illustrative_loss_difference_cny=31100,densities=[density,density/2],unit_interval_probability=float(physical),scope='Independent authored complete-map mixtures, bitemporal selection, inclusion weighting, competing-event recursion and unit-preserving integration. No authentic customer identity, intervention invariance or native conformance is inferred.')
