#!/usr/bin/env python3
"""Common-mechanism information comparisons and audited-state sensitivity."""
import hashlib,json,sys,time
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.validated_latent import ModelShape,pack,unpack,contrast
from causalbank.audited_servicing import generate_audit,fit_audit,value_inference,tree_value,never_value


def visible_history_gformula(theta,shape,policy,logger=True):
    mu,e,q,t,r=unpack(theta,shape)
    def integrate(prior,tree):
        if tree is None:return 0.
        result=0.
        for o,node in enumerate(tree):
            mass=prior*e[:,o];p=mass.sum();posterior=mass/p;a=node['action']
            if logger:
                posterior=posterior*q[:,a];posterior/=posterior.sum()
            result+=p*(posterior@r[a]+policy['discount']*integrate(posterior@t[a],node['next']))
        return float(result)
    return integrate(mu,policy['tree'])


def main():
    basepath=ROOT/'docs/studies/scope-latent-spec.json';base=json.loads(basepath.read_text());shape=ModelShape(reward_sd=base['reward_sd']);theta=pack(*[np.array(base[k]) for k in ('mu','emission','logger','transition','reward')],shape)
    auditpath=ROOT/'docs/studies/dynamic-servicing-audit-results.json';audit=json.loads(auditpath.read_text());policy=audit['policy'];truth=contrast(theta,shape,8)
    def constant_tree(h):return None if h==0 else [{'action':0,'next':constant_tree(h-1)} for _ in range(shape.signals)]
    never=dict(policy,tree=constant_tree(policy['horizon']))
    observed=visible_history_gformula(theta,shape,policy)-visible_history_gformula(theta,shape,never)
    action_sets={}
    def walk(tree,depth):
        if tree is None:return
        for signal,node in enumerate(tree):action_sets.setdefault((depth,signal),set()).add(node['action']);walk(node['next'],depth+1)
    walk(policy['tree'],0)
    # Registration is a separate immutable specification made before draws.
    specpath=ROOT/'docs/studies/dynamic-servicing-sensitivity-spec.json';spec=json.loads(specpath.read_text());rows=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for rep in range(spec['repetitions']):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],rep]));data=generate_audit(base,spec['trajectories'],rng)
            incorrect=rng.random(data['states'].shape)<spec['label_error_probability'];data['states']=np.where(incorrect,(data['states']+rng.integers(1,shape.states,size=data['states'].shape))%shape.states,data['states'])
            fitted=fit_audit(data,shape);result=value_inference(fitted,shape,horizon=8)
            rows.append({'rep':rep,'estimate':result['estimate'],'se':result['se'],'covered':bool(result['interval'][0]<=truth<=result['interval'][1])})
    result={'common_problem':{'correct_policy_contrast':audit['dynamic_truth'],'observed_history_gformula_contrast':observed,
        'interventional_filter_crosscheck_error':visible_history_gformula(theta,shape,policy,logger=False)-tree_value(theta,shape,policy),
        'history_dependent_action_cases':[{'depth':k[0],'current_signal':k[1],'actions':sorted(v)} for k,v in action_sets.items() if len(v)>1],
        'scope':'Exact same mechanism, fixed public-history policy and reward clock. Observed-history g-formula includes the observational action update and fails sequential exchangeability.'},
        'audit_error':{'spec':spec,'truth':truth,'bias':float(np.mean([r['estimate'] for r in rows])-truth),'coverage':float(np.mean([r['covered'] for r in rows])),'runs':rows},'seconds':time.perf_counter()-start,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [basepath,auditpath,specpath,Path(__file__),ROOT/'src/causalbank/audited_servicing.py',ROOT/'src/causalbank/validated_latent.py']}}
    (ROOT/'docs/studies/dynamic-servicing-diagnostics-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'common_problem':result['common_problem'],'audit_error':{k:v for k,v in result['audit_error'].items() if k!='runs'}},indent=2))


if __name__=='__main__':main()
