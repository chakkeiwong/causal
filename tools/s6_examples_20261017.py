#!/usr/bin/env python3
"""Exact S6 stipulated laws and distinct author checks; no package trials."""
from itertools import product
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'docs/program/execution/2026-10-17/s6'
R = s.Rational


def serial(x):
    if isinstance(x, s.MatrixBase): return serial(x.tolist())
    if isinstance(x, s.Basic):
        return int(x) if x.is_Integer else str(x)
    if isinstance(x, dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [serial(v) for v in x]
    return x


def design():
    cells = [(g,t) for g in [2,3,99] for t in range(5)]
    horizons = [-3,-2,0,1,2]
    z = s.Matrix([[1,int(g==3),int(g==99)]+[int(t==j) for j in range(1,5)]
                  for g,t in cells])
    d = s.Matrix([[int(g!=99 and t-g==k) for k in horizons] for g,t in cells])
    return cells,horizons,z,d


def calculate():
    cells,ks,z,d=design();x=z.row_join(d)
    y=s.Matrix([20*int((g,t)==(2,2)) for g,t in cells])
    fit=(x.T*x).inv()*x.T*y
    m=s.eye(len(cells))-z*(z.T*z).inv()*z.T
    b=(d.T*m*d).inv()*d.T*m
    post=[cells.index(cell) for cell in [(2,2),(2,3),(2,4),(3,3),(3,4)]]
    event=dict(cells=cells,horizons=ks,rank=x.rank(),shape=x.shape,
        post_effect_cells=[cells[i] for i in post],post_weights=b[:,post],
        effect_outcomes=y,coefficients=fit[-5:],normal_equations=x.T*(y-x*fit),
        fwl_coefficients=b*y)
    # Curvature propagation by first differences, then vertex optimization.
    a=s.Matrix([R(1,3)]*3);jmax=3
    kernel=s.Matrix([[j-k+1 if k<=j else 0 for k in range(jmax)] for j in range(jmax)])
    c=kernel.T*a;v=10;obs=s.Matrix([30,35,40]);L=sum(a[j]*(j+1) for j in range(jmax))
    vertices=[s.Matrix(u) for u in product([-3,3],repeat=jmax)]
    effects=[(a.T*obs)[0]-L*v-(c.T*u)[0] for u in vertices]
    signed=s.Matrix([1,-1,1]);cs=kernel.T*signed
    curvature=dict(kernel=kernel,weights=a,curvature_coefficients=c,slope_coefficient=L,
        observed_mean=(a.T*obs)[0],slope_bias=L*v,effect_center=(a.T*obs)[0]-L*v,
        radius_per_M=sum(abs(z) for z in c),M3_bounds=[min(effects),max(effects)],
        cost=10,positive_net_breakdown=R(3,2),
        signed_weights=signed,signed_curvature_coefficients=cs,
        sampling_contrast=[L]+list(a),normal_design_variance=L**2+4*(a.T*a)[0])
    aa=s.symbols('a',real=True)
    risk=1+((1-aa)**2+aa**2)+4*(2-aa)**2
    minimizer=s.solve(s.diff(risk,aa),aa)[0]
    donors=dict(B=2,sigma2=1,sigmaT2=1,minimizer=minimizer,
        weights=[1-minimizer,minimizer],risk=s.expand(risk),
        at_interpolation=risk.subs(aa,1),at_regularized=risk.subs(aa,minimizer),
        at_exact=risk.subs(aa,2),
        l1_interpolation=1,l1_regularized=2,l1_exact=3,
        contamination_radius_at_C3=[3,6,9])
    profiles=[]
    for name,w,lam in [('nonnegative',[0,1],[R(1,4),R(3,4)]),
                       ('signed_time',[0,1],[-R(1,2),R(3,2)]),
                       ('signed_unit',[-1,2],[R(1,4),R(3,4)])]:
        wl=s.Matrix(w);ll=s.Matrix(lam)
        loading=2-wl[1];factor=R(3,2)-ll[1]
        profiles.append(dict(name=name,unit_weights=w,time_weights=lam,
            loading_imbalance=loading,time_imbalance=factor,bias=loading*factor,
            noise_variance_factor=(1+(wl.T*wl)[0])*(1+(ll.T*ll)[0])))
    sdid=dict(profiles=profiles,treated_loading=2,donor_loadings=[0,1],
              pre_factors=[0,1],post_factor=R(3,2))
    rho=R(4,5);gamma=s.Matrix(4,4,lambda t,u:100*rho**abs(t-u))
    calendars=[]
    for gap in [1,3]:
        vv=s.zeros(4,1);vv[0]=-1;vv[gap]=1
        common=(vv.T*gamma*vv)[0];idio=2*(vv.T*vv)[0]
        calendars.append(dict(gap=gap,time_weights=vv,common=common,idiosyncratic=idio,
                              total=common+idio))
    calendar=dict(rho=rho,common_level_variance=100,kappa=1,unit_weights=[1,-1],
                  idiosyncratic_cell_variance=1,covariance=gamma,contrasts=calendars)
    responses=[]
    for name,coef in [('maintained_feedback',R(9,10)),('open_loop',R(1,2)),
                       ('replacement_feedback',R(3,10))]:
        path=[coef**h for h in range(4)]
        responses.append(dict(name=name,coefficient=coef,path=path,cumulative=sum(path),
                              net_USD=100*sum(path)-200))
    feedback=dict(rho=R(1,2),beta=1,k=R(2,5),replacement_k=-R(1,5),
        responses=responses,tail_example=dict(C=100,discount=R(19,20),r=R(9,10),H=3,
            bound=100*R(171,200)**4/(1-R(171,200))))
    return serial(dict(event_study=event,curvature=curvature,donors=donors,
                       synthetic_did=sdid,calendar=calendar,feedback=feedback))


def separate(exact):
    # Double demean cell arrays, without forming the nuisance projection matrix.
    cells,ks,z,d=design();n=len(cells)
    def within(q):
        return s.Matrix([q[i]-sum(q[cells.index((g,tt))] for tt in range(5))/5
             -sum(q[cells.index((gg,t))] for gg in [2,3,99])/3+sum(q)/n
             for i,(g,t) in enumerate(cells)])
    dd=s.Matrix.hstack(*(within(d[:,j]) for j in range(5)))
    yy=within(s.Matrix([20*int(c==(2,2)) for c in cells]))
    coef=(dd.T*dd).inv()*dd.T*yy
    assert serial(list(coef))==exact['event_study']['coefficients']
    assert coef[0]==R(130,19) and coef[1]==R(500,171)
    # Recurrence reconstructs each gap path and target for every box vertex.
    for weights in [[R(1,3)]*3,[1,-1,1],[1,-2,0]]:
        c=[sum(weights[j]*(j-k+1) for j in range(k,3)) for k in range(3)]
        vals=[]
        for u in product([-3,3],repeat=3):
            gaps=[-20,-10]
            for uk in u:gaps.append(2*gaps[-1]-gaps[-2]+uk)
            bias=sum(weights[j]*(gaps[j+2]+10) for j in range(3))
            center=10*sum(weights[j]*(j+1) for j in range(3))
            assert bias==center+sum(c[k]*u[k] for k in range(3))
            vals.append(bias)
        radius=3*sum(abs(x) for x in c)
        assert min(vals)==center-radius and max(vals)==center+radius
    # Completing the square, separately from the derivative minimization.
    a=s.symbols('a',real=True)
    assert s.expand(1+(1-a)**2+a**2+4*(2-a)**2-R(9,2)-6*(a-R(3,2))**2)==0
    # Contrast the actual 3x3 factor-cell outcomes, separately from imbalance.
    f=[0,1,R(3,2)];load=[0,1,2]
    for row in exact['synthetic_did']['profiles']:
        w=list(map(R,row['unit_weights']));lam=list(map(R,row['time_weights']))
        q=[-w[0],-w[1],1];v=[-lam[0],-lam[1],1]
        cell=s.Matrix(3,3,lambda i,t:load[i]*f[t])
        contrast=sum(q[i]*v[t]*cell[i,t] for i in range(3) for t in range(3))
        variance=sum((q[i]*v[t])**2 for i in range(3) for t in range(3))
        assert serial(contrast)==row['bias'] and serial(variance)==row['noise_variance_factor']
    # Independent innovation expansion for stationary AR(1) contrast variance.
    rho=R(4,5)
    for row in exact['calendar']['contrasts']:
        h=row['gap'];innovation_variance=100*(1-rho**2)
        expanded=100*(rho**h-1)**2+innovation_variance*sum(rho**(2*j) for j in range(h))
        assert serial(expanded)==row['common']
    # Structural recursion with a unit action innovation at0; separate regimes.
    for row,k in zip(exact['feedback']['responses'],[R(2,5),0,-R(1,5)]):
        prev=s.Integer(0);path=[]
        for h in range(4):
            action=k*prev+int(h==0);prev=prev/2+action;path.append(prev)
        assert serial(path)==row['path'] and serial(sum(path))==row['cumulative']
    return dict(status='pass',reviewer={'name':'Codex author/coordinator','kind':'author'},
        checks=['Full normal-equation projection vs double-demeaned FWL; exact full rank and false leads.',
                'Every curvature-box vertex reconstructed by a gap recurrence; equal, signed and cancelling targets.',
                'Minimax derivative vs completed square.',
                'SDID imbalance and norm formulas vs direct factor-cell contrasts and cell variance sums.',
                'Signed-calendar Toeplitz covariance vs stationary independent-innovation expansion.',
                'Three response powers vs structural action/outcome recursion.'],
        limitations=['Exact stipulated population laws and a conditional Gaussian design; no upstream package execution, statistical study or bank observations.',
                     'Distinct checks by the same author are not independent scientific review.'])


if __name__=='__main__':
    from publish_latent_r_review_v2_20261013 import ref,write
    exact=calculate();review=separate(exact)
    write(BASE/'exact-results.json',exact)
    review['evidence']=[ref(BASE/'exact-results.json','Six exact S6 families'),
                        ref(Path(__file__),'Rational references and distinct author checks')]
    write(BASE/'mathematics-review.json',review)
    print(json.dumps(dict(status=review['status'],families=list(exact),
        false_leads=exact['event_study']['coefficients'][:2],
        sensitivity=exact['curvature']['M3_bounds'])))
