#!/usr/bin/env python3
"""Audited sampling alternative, frozen belief policy and retained-fit diagnosis."""
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.stats import norm
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.validated_latent import ModelShape,pack,unpack,fit,contrast,uncertainty
from causalbank.audited_servicing import generate_audit,fit_audit,optimal_signal_tree,tree_value,never_value,value_inference
from scope_latent import generate


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def serializable(value):
    if isinstance(value,np.ndarray):return value.tolist()
    if isinstance(value,np.generic):return value.item()
    raise TypeError(type(value).__name__)


def summarize(rows,truth,key='fixed'):
    available=[r for r in rows if r.get('available')]
    values=[r[key]['estimate'] for r in available];ses=[r[key]['se'] for r in available]
    covered=[r.get('available',False) and r[key]['interval'][0]<=truth<=r[key]['interval'][1] for r in rows]
    z=[(a-truth)/b for a,b in zip(values,ses)]
    return {'requested':len(rows),'available':len(available),'coverage_all':float(np.mean(covered)),
            'coverage_given_available':float(sum(covered)/len(available)) if available else None,
            'bias_available':float(np.mean(values)-truth) if available else None,
            'empirical_sd':float(np.std(values,ddof=1)) if len(values)>1 else None,
            'mean_se':float(np.mean(ses)) if available else None,'studentized_mean':float(np.mean(z)) if available else None,
            'studentized_sd':float(np.std(z,ddof=1)) if len(z)>1 else None}


def retained_diagnosis():
    oldpath=ROOT/'docs/studies/scope-latent-results.json';old=json.loads(oldpath.read_text());output=[]
    for case in old['results']:
        truth=case['summary']['truth'];rows=[]
        for r in case['runs']:
            available=r['fit']['optimizer_success'] and not r['fit']['on_boundary'] and r['information']['available']
            se=r['information'].get('model_se',0);v=r['estimate']
            rows.append({'rep':r['repetition'],'available':available,'fixed':{'estimate':v,'se':se,'interval':[v-1.95996398454*se,v+1.95996398454*se]},'boundary':r['fit']['on_boundary'],'information':r['information']})
        output.append({'calibration':case['summary']['calibration'],'summary':summarize(rows,truth),'runs':rows})
    return {'source':str(oldpath.relative_to(ROOT)),'source_sha256':digest(oldpath),'results':output,
            'interpretation':'Availability and conditional calibration are distinct. Retained draws do not identify a unique cause of finite-sample error.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('part',choices=['audit','latent','diagnose']);ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/studies/dynamic-servicing-spec.json';spec=json.loads(path.read_text());basepath=ROOT/spec['base_mechanism'];base=json.loads(basepath.read_text());shape=ModelShape(reward_sd=base['reward_sd'])
    true_theta=pack(*[np.array(base[k]) for k in ['mu','emission','logger','transition','reward']],shape);truth=contrast(true_theta,shape,base['horizon'])
    start=time.perf_counter();result={'part':args.part,'mode':'pilot' if args.pilot else 'final','spec':spec,'fixed_truth':truth}
    with threadpool_limits(limits=1):
        if args.part=='diagnose':
            result['retained']=retained_diagnosis();boundary=[]
            old=json.loads((ROOT/'docs/studies/scope-latent-results.json').read_text())
            for j,c in enumerate(old['results']):
                for row in c['runs']:
                    if not row['fit']['on_boundary']:continue
                    rep=row['repetition'];obs,cal=generate(base,c['summary']['calibration'],np.random.default_rng(np.random.SeedSequence([base['seed'],j,rep])))
                    theta,diag=fit(obs,cal,shape,seed=rep+19,starts=base['starts'],maxiter=base['maxiter'])
                    mu,e,q,t,r=unpack(theta,shape)
                    boundary.append({'calibration':c['summary']['calibration'],'rep':rep,'value_reconstruction_error':float(contrast(theta,shape,base['horizon'])-row['estimate']),
                                     'boundary_coordinates':np.flatnonzero(abs(theta[:-6])>=7.999).tolist(),'transition':t.tolist(),'emission':e.tolist(),'initial':mu.tolist(),'logger':q.tolist(),'fit':diag})
            result['boundary_reconstructions']=boundary
        elif args.part=='audit':
            pilot=generate_audit(base,spec['pilot_trajectories'],np.random.default_rng(np.random.SeedSequence([spec['seed'],99])))
            pilot_fit=fit_audit(pilot,shape);policy=optimal_signal_tree(pilot_fit['theta'],shape,spec['decision_horizon'])
            dynamic_truth=tree_value(true_theta,shape,policy)-never_value(true_theta,shape,spec['decision_horizon'])
            result.update(policy=policy,dynamic_truth=dynamic_truth,results=[])
            for case,n in enumerate(spec['audit_sizes']):
                rows=[]
                for rep in range(3 if args.pilot else spec['repetitions']):
                    data=generate_audit(base,n,np.random.default_rng(np.random.SeedSequence([spec['seed'],case,rep])))
                    try:
                        fitted=fit_audit(data,shape);fixed=value_inference(fitted,shape,horizon=spec['evaluation_horizon']);dynamic=value_inference(fitted,shape,policy)
                        row={'rep':rep,'available':True,'minimum_transition_count':fitted['minimum_transition_count'],'theta':fitted['theta'],'fixed':{k:v for k,v in fixed.items() if k not in ('influence','gradient')},'dynamic':{k:v for k,v in dynamic.items() if k not in ('influence','gradient')}}
                        if rep==0:
                            refined=value_inference(fitted,shape,policy,step=3e-6)
                            row['derivative_step_se_difference']=refined['se']-dynamic['se']
                            row['influence_centred_max']=float(abs(fitted['influence'].mean(axis=0)).max())
                    except (ValueError,np.linalg.LinAlgError) as exc:row={'rep':rep,'available':False,'error':str(exc)}
                    rows.append(row)
                entry={'audit_trajectories':n,'fixed_summary':summarize(rows,truth),'dynamic_summary':summarize(rows,dynamic_truth,'dynamic'),'runs':rows}
                result['results'].append(entry);print(json.dumps({k:v for k,v in entry.items() if k!='runs'}),flush=True)
        else:
            n=spec['latent_followup_trajectories'];base['trajectories']=n;rows=[]
            for rep in range(2 if args.pilot else spec['latent_followup_repetitions']):
                obs,cal=generate(base,spec['latent_followup_calibration'],np.random.default_rng(np.random.SeedSequence([spec['seed'],30,rep])))
                theta,diag=fit(obs,cal,shape,seed=rep+217,starts=2,maxiter=450);info=uncertainty(theta,obs,cal,shape,base['horizon']);v=contrast(theta,shape,base['horizon']);se=info.get('model_se',0)
                available=diag['optimizer_success'] and not diag['on_boundary'] and info['available']
                rows.append({'rep':rep,'available':available,'theta':theta,'fit':diag,'information':info,'fixed':{'estimate':v,'se':se,'interval':[v-1.95996398454*se,v+1.95996398454*se]}})
                if rep%10==0:print(json.dumps({'part':'latent','rep':rep,'available':available,'estimate':v}),flush=True)
            result.update(summary=summarize(rows,truth),runs=rows);print(json.dumps(result['summary']),flush=True)
    files=[path,basepath,Path(__file__),ROOT/'tools/scope_latent.py',ROOT/'src/causalbank/validated_latent.py',ROOT/'src/causalbank/audited_servicing.py']
    result.update(seconds=time.perf_counter()-start,input_sha256={str(p.relative_to(ROOT)):digest(p) for p in files})
    suffix='pilot' if args.pilot else 'results'
    (ROOT/f'docs/studies/dynamic-servicing-{args.part}-{suffix}.json').write_text(json.dumps(result,default=serializable,indent=2)+'\n')


if __name__=='__main__':main()
