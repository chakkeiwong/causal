#!/usr/bin/env python3
"""Independent finite-law and derivative checks for the scope revision."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.validated_latent import ModelShape,pack,unpack,likelihood_score,recover_marked_model,policy_value
from scope_latent import generate


def main():
    spec=json.loads((ROOT/'docs/studies/scope-latent-spec.json').read_text()); spec['trajectories']=3;spec['horizon']=3
    shape=ModelShape(); true=[np.array(spec[k]) for k in ['mu','emission','logger','transition','reward']]
    theta=pack(*true,shape); mu,e,q,t,reward=true; obs,cal=generate(spec,30,np.random.default_rng(41)); o,a,r=obs
    with threadpool_limits(limits=1):
        ll,score=likelihood_score(theta,obs,cal,shape)
        direct=0.
        for i in range(len(o)):
            probability=0.
            for states in itertools.product(range(shape.states),repeat=3):
                v=mu[states[0]]
                for j,s in enumerate(states):
                    v*=e[s,o[i,j]]*q[s,a[i,j]]*norm.pdf(r[i,j],loc=reward[a[i,j],s],scale=shape.reward_sd)
                    if j<2: v*=t[a[i,j],s,states[j+1]]
                probability+=v
            direct+=np.log(probability)
        direct+=np.log(e[cal[0],cal[1]]).sum()
        derivative=np.empty(len(theta))
        for j in range(len(theta)):
            move=np.zeros_like(theta); move[j]=1e-5
            derivative[j]=(likelihood_score(theta+move,obs,cal,shape)[0]-likelihood_score(theta-move,obs,cal,shape)[0])/2e-5
        joint=np.array([e.T@np.diag(mu*q[:,action])@t[action]@e for action in range(2)])
        marked=np.array([e.T@(mu*q[:,action]*reward[action]) for action in range(2)])
        recovered=recover_marked_model(e,joint,marked)
        recovery_error=max(float(abs(x-y).max()) for x,y in zip(recovered,[mu,q,t,reward]))
        # Exhaustive two-period policy value sums over signals, actions and hidden paths.
        policy=np.array([[1.,0.],[.8,.2],[.3,.7],[0.,1.]])
        exhaustive=0.
        for s0,s1,o0,o1,a0,a1 in itertools.product(range(3),range(3),range(4),range(4),range(2),range(2)):
            probability=mu[s0]*e[s0,o0]*policy[o0,a0]*t[a0,s0,s1]*e[s1,o1]*policy[o1,a1]
            exhaustive+=probability*(reward[a0,s0]+.99*reward[a1,s1])
        errors={'hidden_path_likelihood':abs(ll-direct),'analytic_score':float(abs(score-derivative).max()),
            'private_logger_population_recovery':recovery_error,'observable_policy_value':abs(exhaustive-policy_value(theta,shape,policy,horizon=2))}
        limits={'hidden_path_likelihood':1e-10,'analytic_score':2e-6,'private_logger_population_recovery':1e-10,'observable_policy_value':1e-10}
        assert all(errors[k]<limits[k] for k in errors),errors
    files=[Path(__file__),ROOT/'src/causalbank/validated_latent.py',ROOT/'tools/scope_latent.py',ROOT/'docs/studies/scope-latent-spec.json']
    result={'status':'pass','errors':errors,'tolerances':limits,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'Independent path enumeration, observed-likelihood differentiation, population measurement inversion and fixed-policy value. Not empirical identification or global optimization.'}
    (ROOT/'docs/reviews/scope-scientific-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
