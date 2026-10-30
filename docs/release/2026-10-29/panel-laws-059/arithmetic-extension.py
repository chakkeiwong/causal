def panel_implementation_laws():
    """Check population, covariance and conversion arithmetic in panel comparisons."""
    raw('docs/release/2026-10-29/context-review-153/chapter-051.tex')
    from itertools import product
    projections=[]
    for treatment,outcome in [(np.array([[0,1,1],[0,0,1]],float),np.array([[0,1,10],[0,0,1]],float)),
                              (np.array([[0,1,1],[0,1,1],[0,0,1],[0,0,1],[0,0,0]],float),None)]:
        n,T=treatment.shape;units=np.repeat(np.arange(n),T);dates=np.tile(np.arange(T),n)
        if outcome is None:
            outcome=np.array([[10*i+2*t+(1 if (i<2 and t==1) or (2<=i<4 and t==2) else 100 if i<2 and t==2 else 0) for t in range(T)] for i in range(n)],float)
        x=np.column_stack([np.ones(n*T)]+[(units==i) for i in range(1,n)]+[(dates==t) for t in range(1,T)]+[treatment.ravel()])
        q,r=np.linalg.qr(x,mode='reduced');projections.append(float(np.linalg.solve(r,q.T@outcome.ravel())[-1]))
    close(projections,[-3.5,-91/8]);assert 1000*F(-91,8)-10000==-21375 and 34000-10000==24000
    d=np.array([0,1,1,0,0,1.]);y=np.array([10,12,20,16,30,36.]);g=np.repeat(np.arange(3),2)
    dm=d-np.repeat([np.mean(d[g==j]) for j in range(3)],2);ym=y-np.repeat([np.mean(y[g==j]) for j in range(3)],2)
    beta=(dm@ym)/(dm@dm);u=ym-beta*dm;scores=np.array([sum(dm[g==j]*u[g==j]) for j in range(3)])
    close(beta,4);close(scores,[-1,0,1]);v0=float(scores@scores)/(dm@dm)**2;close(v0,8/9)
    close([v0*5/(6-K)*3/2 for K in [1,4]],[4/3,10/3])
    weights=[F(3,4),F(1,4)];cov=[[F(4),F(1)],[F(1),F(9)]]
    variance=sum(weights[i]*cov[i][j]*weights[j] for i in range(2) for j in range(2))
    assert variance==F(51,16) and variance+F(1,100)*(2-10)**2==F(1531,400)
    assert sum(a*b for a,b in zip(weights,[2,8]))==F(7,2) and sum(a*b for a,b in zip([F(1,4),F(3,4)],[10,-2]))==1
    y=[[10,12,14,16],[20,22,26,28],[15,17,25,27],[18,20,28,30]]
    def contrast(data,w):
        gap=[F(data[2][t]+data[3][t],2)-sum(w[i]*data[i][t] for i in range(2)) for t in range(4)]
        return sum(gap[2:])/2-F(1,4)*gap[0]-F(3,4)*gap[1]
    assert contrast(y,weights)==F(11,2) and 1/sum(v*v for v in weights)==F(8,5)
    shocked=[[v+(100 if j>1 else 0) for j,v in enumerate(row)] for row in y]
    assert contrast(shocked,weights)==contrast(y,weights)
    assert contrast(shocked,[F(1,2),F(1,4)])-contrast(y,[F(1,2),F(1,4)])==25
    assert 2*F(1,2)**4==F(1,8) and 1/(1-F(1,8))==F(8,7)
    treated=[F(10),F(14)];control=[F(2),F(4)];odds=[F(1),F(999)]
    improved=(sum(treated)-sum(a*b for a,b in zip(control,odds)))/2
    normalized=sum(treated)/2-sum(a*b for a,b in zip(control,odds))/sum(odds)
    assert improved==-1987 and normalized==F(4001,500)
    assert (sum(treated)-control[0])/2==11 and sum(treated)/2-control[0]==10
    assert sum(v*v for v in [F(-1,2),F(-1,2),F(1,2),F(1,2)])==1
    cells=[(F(3,4),2),(F(3,4),4),(F(1,4),10)]
    simple=sum(w*t for w,t in cells)/sum(w for w,t in cells)
    group=F(3,4)*3+F(1,4)*10;calendar=(2+F(3,4)*4+F(1,4)*10)/2
    assert [simple,group,calendar]==[4,F(19,4),F(15,4)]
    perturbations=[[sum(sign[i]*co[i] for i in range(2)) for sign in product([-1,1],repeat=2)] for co in [[F(3,4),F(-3,4)],[F(3,2),F(-1,2)]]]
    variances=[sum(x*x for x in row)/4 for row in perturbations];assert variances==[F(9,8),F(5,2)]
    x=list(map(F,[0,1,0,2]));y=list(map(F,[10,13,20,22]));dx=[];dy=[]
    for start in [0,2]:
        dx.extend([v-sum(x[start:start+2])/2 for v in x[start:start+2]]);dy.extend([v-sum(y[start:start+2])/2 for v in y[start:start+2]])
    gram=sum(v*v for v in dx);b=sum(a*c for a,c in zip(dx,dy))/gram;score=[a*(c-a*b) for a,c in zip(dx,dy)]
    cluster=sum(sum(score[j:j+2])**2 for j in [0,2])/gram**2
    assert b==F(7,5) and cluster==F(128,625) and cluster*F(4,3)==F(512,1875) and cluster*2==F(256,625)
    temporal=[F(1),F(1),F(-2)];lagged=(sum(x*x for x in temporal)+sum(temporal[j]*temporal[j-1] for j in [1,2]))/3
    calendar_meat=(sum(x*x for x in temporal)+temporal[1]*temporal[0])/3
    assert [lagged,calendar_meat]==[F(5,3),F(7,3)]
    repaired=[[F(1),F(3,2)],[F(3,2),F(3,2)]];c=[3,-2]
    assert repaired[0][0]*repaired[1][1]-repaired[0][1]**2==F(-3,4)
    assert sum(c[i]*repaired[i][j]*c[j] for i in range(2) for j in range(2))==-3
    assert sum(v*v for v in [1,2,3,4])+1*3+2*4==41 and 2*sum(v*v for v in [1,2,3,4])+1*3+2*4==71
    assert F(3,4)*(-30)+40-F(1,4)*(-30)==25
    assert 40+(55-45)==50 and 95-20-(55-20)==40
    assert F(25+60,2)-F(10+20,2)==F(55,2) and 25-20==5 and F(2*4*8,8-4-1)==F(64,3)
    return dict(twfe_coefficients=projections,fixest_coefficient=beta,fixest_scores=scores.tolist(),aggregate_variance=str(variance),estimated_share_variance=str(variance+F(16,25)),sdid_contrast='11/2',drdid_normalizations=[str(improved),str(normalized)],cohort_targets=list(map(str,[simple,group,calendar])),unequal_cluster_variances=list(map(str,variances)),linearmodels_slope=str(b),linearmodels_cluster_variance=str(cluster),temporal_meats=list(map(str,[lagged,calendar_meat])),block_replacement_variance=-3,scope='Independent finite arithmetic and explicit-design solves retain population, covariance, influence, conversion and monetary distinctions. Static upstream source findings remain scoped; no downloaded engine or native coverage trial is executed.')


def rollout_uncertainty_laws():
    """Verify interval conversion and sharp Gaussian projection examples."""
    raw('docs/release/2026-10-29/context-review-153/chapter-052.tex')
    z=norm.isf(.025);converted=[10-2*z,10+2*z]
    assert [format(v,'.4f') for v in converted]==['6.0801','13.9199'] and int(-.5)==0 and -.5<0
    x,y=-2,4;m,M=1,1
    assert [y-m*abs(x),y+m*abs(x)]==[2,6] and [y+x-M,y+x+M]==[1,3]
    covariance=np.array([[1,1.5],[1.5,4.]]);center=np.array([0.,4.]);r=math.sqrt(-2*math.log(.05));extrema=[]
    for s in [-1,1]:
        a=np.array([s,1.]);variance=float(a@covariance@a)
        for direction in [-1,1]:
            point=center+direction*r*covariance@a/math.sqrt(variance)
            close((point-center)@np.linalg.solve(covariance,point-center),r*r);extrema.append(float(a@point))
    interval=[min(extrema),max(extrema)];assert [format(v,'.4f') for v in interval]==['-2.9233','10.9233']
    diagonal=[4-r*math.sqrt(5),4+r*math.sqrt(5)];ordinary=[4-2*z,4+2*z]
    assert [format(v,'.4f') for v in diagonal]==['-1.4733','9.4733']
    assert [format(v,'.4f') for v in ordinary]==['0.0801','7.9199']
    assert [format(v-1,'.4f') for v in interval]==['-3.9233','9.9233']
    assert not [v for v in [-1,1] if abs(v)<=.2]
    nodes=[v for v in [-2,-1,0,1,2] if abs(v)>=1];assert min(nodes)==-2 and max(nodes)==2 and 0 not in nodes
    return dict(converted_interval=converted,relative_magnitude_population=[2,6],smoothness_population=[1,3],gaussian_projection=interval,diagonal_covariance_projection=diagonal,ordinary_post_interval=ordinary,net_projection=[v-1 for v in interval],scope='Independent support-function endpoint construction verifies the sharp projection of the supplied Gaussian ellipse and its economic implication. Grid and conversion witnesses retain separate native-reachability and scientific validity qualifications.')


def panel_comparison_laws():
    """Reconstruct rollout projection, sensitivity, weighting and feedback laws."""
    raw('docs/release/2026-10-29/context-review-153/chapter-051.tex')
    from itertools import product
    groups=np.repeat([2,3,99],5);dates=np.tile(np.arange(5),3)
    z=np.column_stack([np.ones(15),(groups==3),(groups==99)]+[(dates==j) for j in range(1,5)])
    event=np.column_stack([((groups!=99)&(dates-groups==j)) for j in [-3,-2,0,1,2]]).astype(float)
    design=np.column_stack([z,event]);q,r=np.linalg.qr(design,mode='reduced')
    assert np.linalg.matrix_rank(design)==12
    treated=np.flatnonzero((groups!=99)&(dates>=groups));operator=np.linalg.solve(r,q.T)[-5:,treated]
    wanted=[[F(13,38),F(4,19),0,F(-13,38),F(-4,19)],
            [F(25,171),F(11,171),0,F(-25,171),F(-11,171)],
            [F(11,18),F(-1,9),0,F(7,18),F(1,9)],
            [F(23,114),F(29,57),0,F(-23,114),F(28,57)],
            [F(-8,171),F(17,171),1,F(8,171),F(-17,171)]]
    close(operator,np.array(wanted,dtype=float));false_leads=operator@np.array([20,0,0,0,0])
    close(false_leads,[130/19,500/171,110/9,230/57,-160/171])
    weights=[F(1,3)]*3;kernel=[sum(weights[j]*(j-k+1) for j in range(k,3)) for k in range(3)]
    assert kernel==[2,1,F(1,3)]
    endpoints=[]
    for curvature in product([-3,3],repeat=3):
        path=[F(-20),F(-10)]
        for u in curvature:path.append(2*path[-1]-path[-2]+u)
        endpoints.append(sum(w*(y-(gap+10)) for w,y,gap in zip(weights,[30,35,40],path[2:])))
    assert [min(endpoints),max(endpoints)]==[5,25]
    variance=4+sum(4*w*w for w in weights);assert variance==F(16,3)
    statistical_budget=(5-1.96*math.sqrt(float(variance)))/float(sum(kernel));assert round(statistical_budget,3)==.142
    risks={}
    for a in [F(1),F(3,2),F(2)]:
        worst=F(0)
        for f,c0,c1 in product([-2,2],[-1,1],[-1,1]):
            mse=sum(((2-a)*f-(1-a)*c0-a*c1+et-(1-a)*e0-a*e1)**2 for et,e0,e1 in product([-1,1],repeat=3))/8
            worst=max(worst,mse)
        assert worst==1+(1-a)**2+a*a+(2*abs(2-a)+abs(1-a)+abs(a))**2;risks[str(a)]=str(worst)
    assert list(risks.values())==['11','25/2','15']
    donor_risk=lambda a:1+(1-a)**2+a*a+4*(2-a)**2
    assert [donor_risk(a) for a in [F(1),F(3,2),F(2)]]==[6,F(9,2),6]
    sdid=[]
    for w,lam in [([0,1],[F(1,4),F(3,4)]),([0,1],[F(-1,2),F(3,2)]),([-1,2],[F(1,4),F(3,4)])]:
        row=[F(1),-F(w[0]),-F(w[1])];col=[F(1),-F(lam[0]),-F(lam[1])]
        factor=sum(row[i]*col[j]*[2,0,1][i]*[F(3,2),0,1][j] for i in range(3) for j in range(3))
        sdid.append([factor,sum((x*y)**2 for x in row for y in col)])
    assert sdid==[[F(3,4),F(13,4)],[0,7],[0,F(39,4)]] and F(9,16)/(7-F(13,4))==F(3,20)
    Q=lambda a:1+(1-a)**2+a*a
    def joint(a,b,s):return (2-a)**2*(2-b)**2+s*Q(a)*Q(b)
    for a,b,s in product([F(-2),F(1,3),F(3,2),F(2)],repeat=3):
        if s<=0:continue
        x,y=a-1,b-1;p,t=x+y,x*y
        assert joint(a,b,s)==9*s/(1+s)+3*s*(p+t)**2+(1+s)*(p-t-(1-2*s)/(1+s))**2
    opt=[(7+math.sqrt(13))/6,(7-math.sqrt(13))/6];close(joint(*opt,F(1,8)),1)
    assert [joint(a,b,F(1,8)) for a,b in [(1,1),(2,F(1,2)),(2,2)]]==[F(3,2),F(9,8),F(9,2)]
    calendar=[];rho=F(4,5)
    for h in [1,3]:
        innovation=100*(rho**h-1)**2+100*(1-rho*rho)*sum(rho**(2*j) for j in range(h))
        assert innovation==200*(1-rho**h);calendar.append(innovation+4)
    assert calendar==[44,F(508,5)]
    finite=[];infinite=[]
    for k in [F(2,5),F(0),F(-1,5)]:
        state=F(0);value=F(-200)
        for h in range(4):
            action=F(1) if h==0 else k*state;state=state/2+action;value+=100*state-10*action*action
        finite.append(value);a=F(1,2)+k;d=F(19,20)
        infinite.append(100/(1-d*a)-200-10*(1+k*k*d/(1-d*a*a)))
    close([float(v) for v in finite],[129.95424,-22.5,-68.73924])
    assert [format(float(v),'.2f') for v in infinite]==['473.06','-19.52','-70.56']
    tail=lambda h:F(100)*(F(19,20)*F(9,10))**(h+1)/(1-F(19,20)*F(9,10))
    assert format(float(tail(3)),'.2f')=='368.55' and tail(26)>10 and tail(27)<=10
    full=[];d=F(19,20);oldk=F(2,5);old_a=F(9,10)
    for k,beta in product([F(21,50),F(11,25)],[F(1),F(2)]):
        a=old_a+(k-oldk)*beta;v=[]
        for horizon in [20,80]:
            old=new=F(1);total=F(-200)
            for h in range(horizon+1):
                old_action=oldk*old;new_action=k*new;old*=old_a;new*=a
                total+=d**h*(100*(new-old)-10*(new_action**2-old_action**2))
            v.append(total)
        v.append(100*(a/(1-d*a)-old_a/(1-d*old_a))-10*(k*k/(1-d*a*a)-oldk*oldk/(1-d*old_a*old_a))-200)
        full.append([format(float(x),'.2f') for x in v])
    assert full==[['-112.57','-92.60','-92.59'],['-4.44','53.68','53.77'],['-5.48','52.61','52.70'],['294.31','580.12','584.45']]
    a,k,h=F(49,50),F(11,25),80
    tail4=100*(a*(d*a)**(h+1)/(1-d*a)+old_a*(d*old_a)**(h+1)/(1-d*old_a))+10*(k*k*(d*a*a)**(h+1)/(1-d*a*a)+oldk*oldk*(d*old_a*old_a)**(h+1)/(1-d*old_a*old_a))
    assert format(float(tail4),'.4f')=='4.3532'
    rd=math.sqrt(1/float(d));bounds=[float(oldk)-(rd+float(old_a))/2,float(oldk)+(rd-float(old_a))/2]
    close(bounds,[-.562989176042577,.462989176042577]);assert d*F(26,25)<1 and d*F(26,25)**2>1
    return dict(event_rank=12,false_leads=false_leads.tolist(),curvature_kernel=list(map(str,kernel)),effect_set=[5,25],noisy_slope_variance=str(variance),statistical_curvature_budget=statistical_budget,donor_contaminated_risks=risks,sdid_bias_variance=[[str(v) for v in row] for row in sdid],joint_optimum=opt,calendar_variances=list(map(str,calendar)),feedback_four_period_values=list(map(str,finite)),feedback_infinite_values=[float(v) for v in infinite],full_replacement_values=full,uniform_tail_80=float(tail4),scope='Independent complete-design QR, exact vertex and noise enumeration, polynomial identities and structural recursion verify declared chapter51 laws. No native package or bank execution; robustness is conditional on supplied information.')
