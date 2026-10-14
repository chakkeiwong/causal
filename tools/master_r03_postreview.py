import json,sys
from pathlib import Path
import numpy as np
from scipy.stats import norm,bernoulli
from scipy.special import ndtr
from scipy.optimize._numdiff import approx_derivative
from numpy.polynomial.hermite import hermgauss
from threadpoolctl import threadpool_limits
sys.path.insert(0,'src')
from causalbank.audited_policy_v11 import TRUTH,simulate,complete_loglik,grid_value
from master_experiment import atomic

def gaussian_tree(p,policy,nodes,misspec=False):
 q,w=hermgauss(nodes);q=q*np.sqrt(2);w=w/np.sqrt(np.pi)
 def walk(s,t):
  prob=ndtr((s-policy[t])*np.exp(-p[4]/2));reward=p[8]+p[9]*s+(p[10]+p[11]*s+p[16]*np.tanh(s))*prob
  if t==len(policy)-1:return reward
  mean=p[0]*s+p[1]*np.tanh(s)
  if misspec:mean+=.35*np.sin(2*s)
  future=0
  for a in [0,1]:
   nx=mean[:,None]+p[2]*a+np.exp((p[3] if a==0 else p[15])/2)*q
   ev=walk(nx.reshape(-1),t+1).reshape(len(s),nodes)@w
   future+=((1-prob) if a==0 else prob)*ev
  return reward+.97*future
 return float(1000*(w@walk(p[13]+np.exp(p[14]/2)*q,0)))

def main():
 data,states=simulate(TRUTH,9,3,np.random.default_rng(718413));p=TRUTH;reference=[]
 for i in range(len(data)):
  ll=norm.logpdf(states[i,0],p[13],np.exp(p[14]/2))
  for t,(o,a,r) in enumerate(data[i]):
   x=states[i,t];pr=.05+.9/(1+np.exp(-(p[5]+p[6]*x+p[7]*o)));reward=p[8]+p[9]*x+p[10]*a+p[11]*x*a+p[16]*np.tanh(x)*a
   ll+=norm.logpdf(o,x,np.exp(p[4]/2))+bernoulli.logpmf(a,pr)+norm.logpdf(r,reward,np.exp(p[12]/2))
   if t<2:ll+=norm.logpdf(states[i,t+1],p[0]*x+p[1]*np.tanh(x)+p[2]*a,np.exp((p[3] if a==0 else p[15])/2))
  reference.append(ll)
 error=float(np.max(abs(np.array(reference)-complete_loglik(p,data,states))));assert error<1e-12
 gradient=approx_derivative(lambda p:np.array([complete_loglik(p,data,states).sum()]),p,method='3-point').reshape(-1)
 complex_score=[]
 for k in range(17):
  q=p.astype(complex);q[k]+=1e-20j;complex_score.append(np.imag(complete_loglik(q,data,states).sum())/1e-20)
 score_error=float(np.max(abs(gradient-complex_score)));assert score_error<1e-5
 spec=json.load(open('docs/program/master/work/R03/protocol.json'));values=[]
 for d in spec['designs']:
  q=p.copy();q[4]=d.get('log_emission_variance',q[4]);a=gaussian_tree(q,spec['policy'],32,d.get('transition_misspecification',False));b=gaussian_tree(q,spec['policy'],64,d.get('transition_misspecification',False));g=grid_value(q,spec['policy'],1601,12.,d.get('transition_misspecification',False));
  values.append(dict(name=d['name'],gauss_hermite32=a,gauss_hermite64=b,grid=g,grid_difference=b-g,refinement_difference=b-a,registered_reference=d['reference_value']))
  assert abs(b-g)<.01
 atomic('docs/program/master/work/R03/postreview-checks.json',dict(status='pass',independent_scipy_loglik_error=error,complex_step_vs_finite_difference_max_error=score_error,values=values,limitations='Post-evaluation numerical audit, not preregistration. Earlier fixture did not contain the independent checks it claimed. Grid agreement remains empirical, not a uniform certified quadrature bound. No method or requests changed.'))
 print(json.dumps(dict(status='pass',score_error=score_error,max_value_discrepancy=max(abs(v['grid_difference']) for v in values))))
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
