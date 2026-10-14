#!/usr/bin/env python3
"""Independent finite identities for the selected dynamic constructions."""
import hashlib,json,sys,itertools
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.audited_servicing import generate_audit,fit_audit,trajectory_contributions,tree_value,never_value,value_inference
from causalbank.validated_latent import ModelShape,pack,unpack
from causalbank.dynamic_funding import FundingTarget
from causalbank.dynamic_product import Backend
from causalbank.responses import bartlett_lrv
from dynamic_discovery_study import hidden_queries,mechanism
from causalbank.ancestral_oracle import marginal_ancestral_graph


def main():
    rng=np.random.default_rng(2026100907);errors={};checks={};details={}
    with threadpool_limits(limits=1):
        # Distribution-weight perturbation checks the normalizers, not the
        # same algebra evaluated twice as an estimator.
        n=1000;g=rng.binomial(1,.4,n);x=rng.normal(size=n);d=.8*g+1.3*x+rng.normal(size=n);m=1.3*x;p=.4;w=(1-g)*p/(1-p)
        def att(weights):
            return np.sum(weights*g*(d-m))/np.sum(weights*g)-np.sum(weights*w*(d-m))/np.sum(weights*w)
        tau=att(np.ones(n));mg=np.mean(g*(d-m))/np.mean(g);mc=np.mean(w*(d-m))/np.mean(w)
        influence=g*(d-m-mg)/g.mean()-w*(d-m-mc)/w.mean();direction=rng.normal(size=n);step=1e-5
        derivative=(att(1+step*direction)-att(1-step*direction))/(2*step)
        errors['normalized_att_influence']=abs(derivative-np.mean(direction*influence))
        groups=rng.choice(3,n,p=[.3,.5,.2]);effects=np.array([1.,2.,4.]);target=np.mean(effects[groups]);if_share=effects[groups]-target
        def aggregate(weight):return np.sum(weight*effects[groups])/sum(weight)
        derivative=(aggregate(1+step*direction)-aggregate(1-step*direction))/(2*step)
        errors['estimated_cohort_share_influence']=abs(derivative-np.mean(direction*if_share))
        # A full-path likelihood/count perturbation checks audited parameter
        # influence and the independently frozen decision-tree value.
        basepath=ROOT/'docs/studies/scope-latent-spec.json';base=json.loads(basepath.read_text());shape=ModelShape(reward_sd=base['reward_sd']);data=generate_audit(base,2000,rng);fit=fit_audit(data,shape);parts=trajectory_contributions(data,shape);direction=rng.normal(size=2000)
        def weighted_fit(weight):
            totals=[np.tensordot(weight,count,axes=1) for count in parts];prob=[v/v.sum(axis=-1,keepdims=True) for v in totals[:4]];return pack(*prob,totals[5]/totals[4],shape)
        numerical=(weighted_fit(1+step*direction)-weighted_fit(1-step*direction))/(2*step)
        errors['audited_path_parameter_influence']=float(abs(numerical-np.mean(direction[:,None]*fit['influence'],axis=0)).max())
        auditpath=ROOT/'docs/studies/dynamic-servicing-audit-results.json';policy=json.loads(auditpath.read_text())['policy'];value=value_inference(fit,shape,policy)
        def functional(th):return tree_value(th,shape,policy)-never_value(th,shape,policy['horizon'])
        numerical=(functional(weighted_fit(1+step*direction))-functional(weighted_fit(1-step*direction)))/(2*step)
        errors['audited_policy_path_influence']=abs(numerical-float(np.mean(direction*value['influence'])))
        mu,e,q,t,r=unpack(fit['theta'],shape);enumerated=0.;h=policy['horizon']
        for states in itertools.product(range(shape.states),repeat=h):
            for signals in itertools.product(range(shape.signals),repeat=h):
                mass=mu[states[0]];reward=0.;tree=policy['tree']
                for k,(s,o) in enumerate(zip(states,signals)):
                    mass*=e[s,o];a=tree[o]['action'];reward+=policy['discount']**k*r[a,s];tree=tree[o]['next']
                    if k<h-1:mass*=t[a,s,states[k+1]]
                enumerated+=mass*reward
        errors['policy_hidden_path_enumeration']=abs(enumerated-tree_value(fit['theta'],shape,policy))
        # Calendar halos: arbitrary scores and inconvenient boundaries exercise
        # the lag accounting independently of the funding generator.
        scores=rng.normal(size=(101,7));reference=bartlett_lrv(scores,13)
        for workers in [1,2,4]:
            with Backend(workers) as backend:got=backend.lrv(scores,13)
            errors[f'halo_covariance_{workers}']=float(abs(got-reference).max())
        # Pair-map inverse and its calibration derivative.
        eta1=np.array([1.8,.8]);eta2=np.array([.7,.4]);p=.8
        inverse=lambda z:(z*eta1-(1-z)*eta2)/(2*z-1)
        errors['map_calibration_derivative']=float(abs((inverse(p+step)-inverse(p-step))/(2*step)-(eta2-eta1)/(2*p-1)**2).max())
        first=np.array([2.,1.]);second=np.array([.5,.2]);mixed1=p*first+(1-p)*second;mixed2=(1-p)*first+p*second
        errors['pair_assignment_inverse']=float(abs((p*mixed1-(1-p)*mixed2)/(2*p-1)-first).max())
        # Finite assignment test: enumerate which region was assigned, with
        # donor weights refitted separately for every potential assignment.
        regions=20;pre=24;post=6;factor=rng.normal(size=pre+post);paths=rng.normal(size=(regions,1))*factor+rng.normal(scale=.3,size=(regions,pre+post));statistics=[]
        for j in range(regions):
            donor=np.delete(paths,j,axis=0);a=donor[:,:pre].T;b=paths[j,:pre]
            objective=lambda w:float(np.sum((a@w-b)**2))
            opt=minimize(objective,np.ones(regions-1)/(regions-1),method='SLSQP',bounds=[(0,1)]*(regions-1),constraints=[{'type':'eq','fun':lambda w:sum(w)-1}],options={'ftol':1e-10,'maxiter':400})
            if not opt.success:raise RuntimeError('donor fit did not converge')
            gap=paths[j]-opt.x@donor;statistics.append(float(np.mean(gap[pre:]**2)/max(np.mean(gap[:pre]**2),1e-8)))
        pvalues=np.array([np.mean(np.array(statistics)>=v) for v in statistics]);checks['sharp_null_randomization_rank']=bool(np.mean(pvalues<=.05)<=.05)
        details['synthetic_control_assignment']={'regions':regions,'null_rejection_probability_over_all_assignments':float(np.mean(pvalues<=.05)),'pvalues':pvalues.tolist(),'scope':'One fixed finite outcome matrix, all uniform assignments; identity check rather than Monte Carlo power claim'}
        query=hidden_queries();errors['frontdoor_population_identity']=abs(query['frontdoor']['identified_contrast']-query['frontdoor']['structural_contrast']);checks['unresolved_same_law_different_effect']=query['unresolved_direct']['effects']==[1.,0.]
        # Population partial-correlation diagnostic distinguishes weak graph
        # information from an incorrect oracle target or endpoint parser.
        graphspecpath=ROOT/'docs/studies/dynamic-discovery-spec.json';spec=json.loads(graphspecpath.read_text());nodes,weighted,order=mechanism(spec);nodes=spec['observed']+spec['latent'];c=np.zeros((len(nodes),len(nodes)))
        for a,b,v in weighted:c[nodes.index(b),nodes.index(a)]=v
        inv=np.linalg.inv(np.eye(len(nodes))-c);cov=inv@inv.T;truth=marginal_ancestral_graph(nodes,[(a,b) for a,b,w in weighted],spec['observed']);weak=[]
        for i,j in itertools.combinations(range(6),2):
            if not truth['graph'][i,j]:continue
            alternatives=[];other=[k for k in range(6) if k not in (i,j)]
            for size in range(5):
                for z in itertools.combinations(other,size):
                    ids=[i,j,*z];precision=np.linalg.inv(cov[np.ix_(ids,ids)]);partial=-precision[0,1]/np.sqrt(precision[0,0]*precision[1,1]);alternatives.append((float(abs(partial)),list(z)))
            minimum,z=min(alternatives);weak.append({'pair':[nodes[i],nodes[j]],'minimum_partial_correlation':minimum,'conditioning':[nodes[k] for k in z]})
        details['population_graph_weakness']=weak
    tolerances={key:1e-6 for key in errors};checks.update({key:bool(value<tolerances[key]) for key,value in errors.items()})
    files=[Path(__file__),basepath,auditpath,graphspecpath,*[ROOT/'src/causalbank'/name for name in ['audited_servicing.py','validated_latent.py','dynamic_product.py','responses.py','ancestral_oracle.py']],ROOT/'tools/dynamic_discovery_study.py']
    result={'status':'pass' if all(checks.values()) else 'fail','errors':errors,'tolerances':tolerances,'checks':checks,'details':details,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'Independent finite derivatives, path enumeration, exact assignment rank and partition identities; not general proof or bank validation'}
    (ROOT/'docs/reviews/dynamic-scientific-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','details')},indent=2));raise SystemExit(result['status']!='pass')


if __name__=='__main__':main()
