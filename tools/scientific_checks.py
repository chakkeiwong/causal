#!/usr/bin/env python3
"""Independent finite references for new scientific constructions, not proofs."""
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.responses import bartlett_lrv,quadratic_sublevel,set_contains,level_response_from_changes,propagation_value_jacobian
from causalbank.controlled import pack,unpack,forward_backward,score,value,simulate
from causalbank.discovery_sets import dag_class,effect_interval,can_exclude
from causalbank.temporal_discovery import interval_matrix_product
from causalbank.organization import Candidate,materialize,organize


def run():
    rng=np.random.default_rng(20261008)
    checks={}
    a=rng.normal(size=(79,4)); a-=a.mean(axis=0)
    length=8
    padded=np.pad(a,((length, length),(0,0)))
    sums=np.array([padded[t:t+length+1].sum(axis=0) for t in range(len(a)+length)])
    moving=sums.T@sums/(len(a)*(length+1))
    hac=bartlett_lrv(a,length)
    checks["bartlett_moving_sum_identity"]=float(abs(hac-moving).max())<1e-12
    checks["bartlett_positive_semidefinite"]=bool(np.linalg.eigvalsh(hac).min()>-1e-12)
    cases=[(1.,0.,-1.),(-1.,0.,1.),(0.,1.,2.),(0.,0.,1.),(0.,0.,-1.),(1.,2.,1.),(-1.,2.,-1.)]
    cases.extend(rng.normal(size=(200,3)))
    checks["quadratic_sets_against_direct_inequality"]=all(
        set_contains(quadratic_sublevel(*coeff),x)==(coeff[0]*x*x+coeff[1]*x+coeff[2]<=0)
        for coeff in cases for x in [-1e5,-3.11,-.73,.23,2.17,1e5])
    x=rng.normal(size=(240,3)); z=rng.normal(size=240)
    fit=level_response_from_changes(x,z,5)
    n=fit.origins
    numerators=np.array([np.mean(z[1:1+n]*(x[1+h:1+h+n,j]-x[:n,j]))
                         for j in (1,2) for h in range(6)])
    checks["level_response_telescope"]=float(abs(numerators-fit.moment_mean[:-1]).max())<1e-12
    model={"mu":np.array([.65,.35]),"emission":np.array([[.8,.2],[.2,.8]]),
           "transition":np.array([[[.9,.1],[.2,.8]],[[.92,.08],[.48,.52]]]),
           "reward":np.array([[.85,.3],[.88,.48]])}
    parameter=pack(model)
    data=simulate(model,7,3,rng)
    ll=forward_backward(data,model,False)
    brute=[]
    o,a,r=data
    for i in range(len(o)):
        probability=0.
        for states in itertools.product(range(2),repeat=3):
            w=model["mu"][states[0]]
            for t,s in enumerate(states):
                b=model["reward"][a[i,t],s]
                w*=model["emission"][s,o[i,t]]*(b if r[i,t] else 1-b)
                if t<2: w*=model["transition"][a[i,t],s,states[t+1]]
            probability+=w
        brute.append(np.log(probability))
    checks["forward_likelihood_hidden_path_enumeration"]=float(abs(ll-brute).max())<1e-12
    analytic=score(parameter,data)[1].sum(axis=0)
    step=1e-5
    numerical=np.array([(forward_backward(data,unpack(parameter+step*v),False).sum()-
                         forward_backward(data,unpack(parameter-step*v),False).sum())/(2*step)
                        for v in np.eye(11)])
    checks["observed_score_direct_likelihood_derivative"]=float(abs(analytic-numerical).max())<1e-7
    # Independent sum over signals and hidden states for a fixed observable rule.
    brute_value=0.
    for states in itertools.product(range(2),repeat=3):
        for signals in itertools.product(range(2),repeat=3):
            w=model["mu"][states[0]]
            reward=0.
            for t,(s,observation) in enumerate(zip(states,signals)):
                action=observation
                w*=model["emission"][s,observation]
                reward+=.99**t*(100*model["reward"][action,s]-12*action)
                if t<2: w*=model["transition"][action,s,states[t+1]]
            brute_value+=w*reward
    checks["fixed_policy_value_path_enumeration"]=abs(brute_value-value(parameter,horizon=3))<1e-10
    # Unknown-emission recovery from exact three-view probabilities.
    e=model["emission"].T; t=model["transition"][0]; mu=model["mu"]
    mu1=t.T@mu
    left=e@np.diag(mu)@t@np.diag(1/mu1); right=e@t.T
    slices=np.array([left@np.diag(mu1*e[j])@right.T for j in range(2)])
    p02=slices.sum(axis=0)
    eigen,vectors=np.linalg.eig(slices[1]@np.linalg.inv(p02))
    order=np.argsort(eigen); vectors=vectors[:,order]; vectors/=vectors.sum(axis=0)
    recovered_e=np.array([np.diag(np.linalg.solve(vectors,s@np.linalg.inv(p02)@vectors)) for s in slices])
    recovered_mu=np.linalg.solve(recovered_e,e@mu)
    recovered_t=[]
    for transition in model["transition"]:
        joint=e@np.diag(mu)@transition@e.T
        inv=np.linalg.inv(recovered_e)
        recovered_t.append(np.diag(1/recovered_mu)@inv@joint@inv.T)
    checks["controlled_unknown_emission_population_recovery"]=bool(
        np.max(abs(recovered_e-e))<1e-12 and np.max(abs(recovered_mu-mu))<1e-12
        and np.max(abs(np.array(recovered_t)-model["transition"]))<1e-12)
    f=np.array([[.4,.1,0],[.2,.5,.1],[0,.1,.3]]); kappa=np.array([1.,.4,.3])
    _,jacobian=propagation_value_jacobian(f,kappa,5)
    parameter=np.r_[f.ravel(),kappa]
    def direct_propagation(v):
        matrix=v[:9].reshape(3,3); shock=v[9:]
        return np.array([(np.linalg.matrix_power(matrix,h)@shock)[j]/shock[0] for j in (1,2) for h in range(6)])
    numerical=np.column_stack([(direct_propagation(parameter+step*v)-direct_propagation(parameter-step*v))/(2*step) for v in np.eye(12)])
    checks["proxy_propagation_jacobian_finite_difference"]=np.max(abs(jacobian-numerical))<1e-8
    checks["three_vertex_dag_count"]=len(dag_class())==25 and len(dag_class([0,1,2]))==8
    interval_ok=True
    for graph in dag_class():
        beta=graph.T*rng.uniform(-.8,.8,size=(3,3))
        inverse=np.linalg.inv(np.eye(3)-beta); covariance=inverse@inverse.T
        entries=[[(v-.001,v+.001) for v in row] for row in covariance]
        lo,hi=effect_interval(graph,entries)
        interval_ok &= not can_exclude(graph,entries) and lo<=inverse[2,1]<=hi
    checks["all_three_vertex_graphs_population_effect_enclosed"]=interval_ok
    box=[[(float(v-.03),float(v+.03)) for v in row] for row in f]
    powers=[[(float(i==j),float(i==j)) for j in range(3)] for i in range(3)]
    samples=f+rng.uniform(-.03,.03,size=(100,3,3)); temporal_ok=True
    for h in range(6):
        enclosing=np.array(powers); actual=np.array([np.linalg.matrix_power(v,h) for v in samples])
        temporal_ok &= np.all(actual>=enclosing[:,:,0]) and np.all(actual<=enclosing[:,:,1])
        powers=interval_matrix_product(powers,box)
    checks["temporal_box_contains_direct_matrix_powers"]=temporal_ok
    oracle=json.loads((ROOT/"docs/studies/observation-oracle.json").read_text())
    events=[{**r,"entity":r.get("entity","macro"),"currency":r.get("currency","USD")} for r in oracle["events"]]
    obs_ok=True
    candidate=Candidate("event_time","available_time","latest_available","stock","account")
    for query in oracle["oracle_checks"]:
        subset=[r for r in events if r["record_id"]==query["record_id"]]
        result=materialize(subset,[{"entity":subset[0]["entity"],"decision_id":"q","at":query["decision_time"]}],candidate)[0]
        actual=result["lineage"][0][-1] if result["lineage"] else None
        obs_ok &= actual==query["eligible_version"]
    checks["organization_strict_availability_frozen_oracle"]=obs_ok
    paths=[Path(__file__),ROOT/"docs/studies/observation-oracle.json"]+[ROOT/"src/causalbank"/name for name in
        ("responses.py","controlled.py","discovery_sets.py","temporal_discovery.py","organization.py")]
    checks={key:bool(value) for key,value in checks.items()}
    receipt={"status":"pass" if all(checks.values()) else "fail","checks":checks,
             "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
             "scope":"Finite independent identities/derivatives; not general theorem verification or model validation."}
    (ROOT/"docs/reviews/scientific-completion-checks.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
    return not all(checks.values())


if __name__=="__main__":
    with threadpool_limits(limits=1):
        raise SystemExit(run())
