import json,sys,itertools
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import minimize
sys.path.insert(0,'src')
from causalbank.temporal_class_v3 import simulate,infer
from causalbank.latent_temporal_sets import unrestricted_witness
from causalbank.linkage_sets import decode_set
from causalbank.sparse_learning_v2 import lasso,train,predict,estimate
from master_experiment import atomic
from master_experiment_v2 import summary

def main():
 rng=np.random.default_rng(718411)
 x=rng.normal(size=(100,7));y=rng.normal(size=(100,2));fit=lasso(x,y,.05)
 # Independent convex constrained formulation: squared loss + lambda sum t_j, -t<=b<=t.
 z=(x-x.mean(0))/x.std(0);yc=y-y.mean(0);refs=[]
 for j in range(2):
  objective=lambda v: .5*np.mean((yc[:,j]-z@v[:7])**2)+.05*v[7:].sum()
  constraints=[{'type':'ineq','fun':lambda v:v[7:]-v[:7]},{'type':'ineq','fun':lambda v:v[7:]+v[:7]}]
  opt=minimize(objective,np.zeros(14),method='SLSQP',constraints=constraints,options={'ftol':1e-12,'maxiter':1000})
  assert opt.success;refs.append(opt.x[:7]/x.std(0))
 error=float(abs(np.column_stack(refs)-fit['coefficient']).max());assert error<1e-5
 # The exact orthogonal solution checks the selection boundary independently.
 q,_=np.linalg.qr(rng.normal(size=(100,5)));q-=q.mean(0);q,_=np.linalg.qr(q);q*=10
 target=q@np.array([[.1],[.2],[0.],[.05],[-.3]])
 f=lasso(q,target,.1);expected=np.sign(q.T@target/100)*np.maximum(abs(q.T@target/100)-.1,0)
 assert np.max(abs(f['coefficient']-expected))<1e-7
 # train() accepts training rows only; perturbing disjoint evaluation cannot change fit.
 f1=train(x,y,[.02,.08],10);held=rng.normal(size=(40,7));p1=predict(f1,held);held_y=rng.normal(size=(40,2))*1e6
 f2=train(x,y,[.02,.08],10);assert np.array_equal(f1['coefficient'],f2['coefficient'])
 # Fully independent score/covariance reconstruction for dense route.
 xx=rng.normal(size=(200,7));zz=xx[:,0]+rng.normal(size=200);aa=.8*zz+xx[:,1]+rng.normal(size=200);yy=1.2*aa+xx[:,2]+rng.normal(size=200);targets=np.column_stack([yy,aa,zz]);out=estimate(xx,targets,20,[.01],dense=True)
 residual=[]
 for ev,tr in [(slice(0,90),slice(110,200)),(slice(110,200),slice(0,90))]:
  dt=np.column_stack([np.ones(90),xx[tr]]);de=np.column_stack([np.ones(90),xx[ev]]);coef=np.linalg.solve(dt.T@dt,dt.T@targets[tr]);residual.append(targets[ev]-de@coef)
 rr=np.vstack(residual);den=np.mean(rr[:,2]*rr[:,1]);theta=np.mean(rr[:,2]*rr[:,0])/den;var=0;bw=out['bandwidth']
 for r in residual:
  sc=r[:,2]*(r[:,0]-theta*r[:,1]);sc-=sc.mean();lags=abs(np.arange(90)[:,None]-np.arange(90)[None,:]);kernel=np.maximum(1-lags/(bw+1),0);var+=sc@kernel@sc
 se=np.sqrt(var)/180/abs(den);assert np.isclose(se,out['standard_error'],rtol=1e-10)
 atomic('docs/program/master/work/R05-v2/fixtures.json',dict(status='pass',independent_convex_coefficient_error=error,orthogonal_soft_threshold=True,evaluation_label_isolation=True,independent_dense_score_se_error=abs(se-out['standard_error']),limitations='Finite dimension numerical reference; no finite inference theorem supplied by optimizer agreement.'))
 # Exact symbolic oracle for the structural innovation law.
 import sympy as sp
 z,u,ea,ey=sp.symbols('z u ea ey'); strength=sp.Rational(4,5);tau=sp.Rational(3,4);action=strength*z+sp.Rational(3,5)*u+ea;response=tau*action+sp.Rational(7,10)*u+ey
 assert sp.diff(response,ea)==tau
 co=sp.Matrix([[sp.diff(v,w) for w in (z,u,ea,ey)] for v in (z,action,response)]);sigma=co*co.T
 assert sigma[0,2]/sigma[0,1]==tau
 d=dict(tau=.75);history=simulate(1000,np.random.default_rng(718412),d);got=infer(history,[0.,.4,.8],'randomized_encouragement');pieces=decode_set(got['effect_set']);assert any(a<=.75<=b for a,b in pieces)
 # In an exact covariance box enumerate all coefficient/latent structures, without sampled CI selection.
 for b in [-10.,0.,10.]:
  witness=unrestricted_witness(np.array(sigma).astype(float),b);assert np.max(abs(witness['recovered_covariance']-np.array(sigma).astype(float)))<1e-10
 raw=simulate(1000,np.random.default_rng(1),dict(rho=.4));obs=infer(raw,[0.,.4,.8],'observational_latent');assert decode_set(obs['effect_set'])==[(-np.inf,np.inf)]
 # Roundtrip unbounded and disconnected JSON values and coverage summary.
 spec=dict(designs=[{'name':'encoding'}],methods=['set']);r=[]
 for i,pieces in enumerate([[{'lower':None,'upper':None}],[{'lower':None,'upper':-1.},{'lower':1.,'upper':None}]]):
  row=dict(cell=0,result=dict(truth=2.,methods={'set':dict(status='computed_set',effect_set=pieces)}),elapsed_seconds=0.,process_rss_kib=0);r.append(json.loads(json.dumps(row,allow_nan=False)))
 summed=summary(r,spec);assert summed['cells'][0]['methods']['set']['covered']==2 and summed['cells'][0]['methods']['set']['topologies']['disconnected']==1
 atomic('docs/program/master/work/R04-v3/fixtures.json',dict(status='pass',exact_structural_innovation_covariance=str(sigma),exact_wald_ratio=str(tau),ar_lag_union=got['effect_set'],whole_line_json_roundtrip=True,disconnected_json_roundtrip=True,arbitrary_effect_witnesses=[-10,0,10],note='Exact symbolic innovation target and covariance oracle; interval outer projection is conservative, floating point endpoint certification is limited to roundoff checks.'))
 print(json.dumps(dict(status='pass',independent_lasso_error=error,dense_score_error=abs(se-out['standard_error']))))

if __name__=='__main__':main()
