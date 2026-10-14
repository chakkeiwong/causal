#!/usr/bin/env python3
"""Complete joint refits as a numerical challenger for private-logger value."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.validated_latent import ModelShape,unpack,fit,contrast,uncertainty
from scope_latent import generate,categorical


def main():
    path=ROOT/'docs/studies/scope-latent-bootstrap-spec.json';spec=json.loads(path.read_text())
    base_path=ROOT/'docs/studies/scope-latent-spec.json';base=json.loads(base_path.read_text());shape=ModelShape(reward_sd=base['reward_sd'])
    size=spec['calibration_size'];j=base['calibration_sizes'].index(size);rep=spec['data_repetition']
    obs,cal=generate(base,size,np.random.default_rng(np.random.SeedSequence([base['seed'],j,rep])))
    start=time.perf_counter();rows=[]
    with threadpool_limits(limits=1):
        theta,diag=fit(obs,cal,shape,seed=rep+19,starts=base['starts'],maxiter=base['maxiter'])
        # Additional starts probe numerical multimodality without claiming globality.
        challenger,extra=fit(obs,cal,shape,seed=spec['seed'],starts=6,maxiter=800)
        infos={str(step):uncertainty(theta,obs,cal,shape,base['horizon'],step=step) for step in [3e-5,1e-4,3e-4]}
        parameters=unpack(theta,shape);fit_spec={**base,**{k:v.tolist() for k,v in zip(['mu','emission','logger','transition','reward'],parameters)}}
        for b in range(spec['bootstrap_refits']):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],b]))
            sample,_=generate(fit_spec,size,rng)
            labels=cal[0].copy();calibration=(labels,categorical(parameters[1][labels],rng))
            fitted,d=fit(sample,calibration,shape,seed=spec['seed']+b,starts=spec['starts'],maxiter=base['maxiter'])
            rows.append({'replication':b,'estimate':contrast(fitted,shape,base['horizon']),'diagnostics':d})
            if b%20==0:print(json.dumps({'bootstrap_refit':b,'success':d['optimizer_success'],'boundary':d['on_boundary']}),flush=True)
    valid=[r['estimate'] for r in rows if r['diagnostics']['optimizer_success'] and not r['diagnostics']['on_boundary']]
    estimate=contrast(theta,shape,base['horizon']);failures=len(rows)-len(valid)
    summary={'requested_refits':len(rows),'failures':failures,'usable_refits':len(valid),'estimate':estimate,'bootstrap_se':float(np.std(valid,ddof=1)),
        'extra_starts_value_difference':contrast(challenger,shape,base['horizon'])-estimate,
        'extra_starts_objective_difference':min(extra['objectives'])-min(diag['objectives'])}
    if failures/len(rows)<.05:
        quantile=np.quantile(valid,[.025,.975]);summary.update(percentile_interval=quantile.tolist(),basic_interval=[float(2*estimate-quantile[1]),float(2*estimate-quantile[0])])
    else:summary['interval_status']='unavailable: excessive invalid refits'
    files=[path,base_path,Path(__file__),ROOT/'tools/scope_latent.py',ROOT/'src/causalbank/validated_latent.py']
    receipt={'spec':spec,'summary':summary,'fit':diag,'extra_fit':extra,'derivative_sensitivity':infos,'refits':rows,'seconds':time.perf_counter()-start,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':spec['scope']}
    (ROOT/'docs/studies/scope-latent-bootstrap-results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
