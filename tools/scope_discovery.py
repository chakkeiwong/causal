#!/usr/bin/env python3
"""Mature temporal discovery operations, endpoint retention and effect scope."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-matplotlib')
import argparse
import hashlib
import importlib.metadata as metadata
import inspect
import json
from pathlib import Path
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits
from tigramite import data_processing as pp
from tigramite.pcmci import PCMCI
from tigramite.lpcmci import LPCMCI
from tigramite.independence_tests.parcorr import ParCorr
ROOT=Path(__file__).resolve().parents[1]


def generate(n,burn,rng,hidden=False):
    p=6;c=np.zeros((p,p));c[1,0]=.4;c[3,2]=-.3
    f=np.eye(p)*.45;f[2,1]=.4;f[4,3]=-.4;f[5,4]=.2
    second=np.zeros((p,p));second[5,2]=-.25
    inverse=np.linalg.inv(np.eye(p)-c);x=np.zeros((n+burn+2,p));u=0.
    for t in range(2,len(x)):
        u=.65*u+rng.normal();noise=rng.normal(size=p)
        if hidden: noise+=np.array([0,0,.8,0,.8,0])*u
        x[t]=inverse@(f@x[t-1]+second@x[t-2]+noise)
    truth=np.zeros((p,p,3),bool);truth[:,:,0]=(c.T!=0);truth[:,:,1]=(f.T!=0);truth[:,:,2]=(second.T!=0)
    return x[burn+2:],truth,(c,f,second)


def structural_response(x,order,lag=2,horizon=8):
    """Response conditional on a supplied sufficient recursive structural model.

    The order is substantive input, not inferred from an ambiguous PAG.
    All allowed lagged parents are retained, preventing search-selected
    nuisance omission from being hidden in this separate sensitivity fit.
    """
    n,p=x.shape;c=np.zeros((p,p));f=np.zeros((lag,p,p))
    for j,node in enumerate(order):
        parent=order[:j]
        design=np.column_stack([np.ones(n-lag),x[lag:,parent]]+[x[lag-l:n-l] for l in range(1,lag+1)])
        beta=np.linalg.lstsq(design,x[lag:,node],rcond=None)[0]
        c[node,parent]=beta[1:1+j]
        for l in range(lag):f[l,node]=beta[1+j+l*p:1+j+(l+1)*p]
    return response_from_matrices(c,f,horizon)


def response_from_matrices(c,f,horizon):
    p=len(c);lag=len(f);inverse=np.linalg.inv(np.eye(p)-c)
    companion=np.zeros((p*lag,p*lag));companion[:p]=np.concatenate([inverse@a for a in f],axis=1)
    if lag>1:companion[p:,:p*(lag-1)]=np.eye(p*(lag-1))
    impact=np.zeros(p*lag);impact[:p]=inverse[:,1]
    values=[]
    for _ in range(horizon+1):values.append(float(impact[2]));impact=companion@impact
    return values


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args()
    path=ROOT/'docs/studies/scope-discovery-spec.json';spec=json.loads(path.read_text());reps=1 if args.pilot else spec['repetitions']
    results=[];start=time.perf_counter()
    for j,case in enumerate(spec['cases']):
        runs=[]
        for r in range(reps):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],j,r]));x,truth,matrices=generate(spec['dates'],spec['burn_in'],rng,case=='hidden_common')
            lag=1 if case=='omitted_lag' else spec['lags'];data=pp.DataFrame(x,var_names=spec['variables'])
            for method in spec['methods']:
                tic=time.perf_counter()
                with threadpool_limits(limits=1):
                    if method=='PCMCI+':
                        engine=PCMCI(dataframe=data,cond_ind_test=ParCorr(significance='analytic'),verbosity=0)
                        fitted=engine.run_pcmciplus(tau_min=0,tau_max=lag,pc_alpha=spec['pc_alpha'])
                    else:
                        engine=LPCMCI(dataframe=data,cond_ind_test=ParCorr(significance='analytic'),verbosity=0)
                        fitted=engine.run_lpcmci(tau_min=0,tau_max=lag,pc_alpha=spec['pc_alpha'],max_p_global=spec['lpcmci_search_limit'],max_p_non_ancestral=spec['lpcmci_search_limit'])
                graph=np.asarray(fitted['graph']);pred=graph!='';actual=truth[:,:,:lag+1].copy();actual[:,:,0]|=actual[:,:,0].T
                # Adjacency against the observed structural DAG is descriptive in
                # the hidden case, since a PAG targets a different graph object.
                selected=int(pred.sum());tp=int((pred&actual).sum());total=int(actual.sum())
                full_truth=truth.copy();full_truth[:,:,0]|=full_truth[:,:,0].T
                row={'repetition':r,'method':method,'lag':lag,'seconds':time.perf_counter()-tic,
                    'graph':graph.tolist(),'value_matrix':np.asarray(fitted['val_matrix']).tolist(),
                    'p_matrix':np.asarray(fitted['p_matrix']).tolist(),
                    'adjacency_precision':tp/selected if selected else 0,'adjacency_recall':tp/int(full_truth.sum()),
                    'in_window_adjacency_recall':tp/total,'omitted_true_adjacencies':int(full_truth.sum())-total,
                    'marks':{str(v):int((graph==v).sum()) for v in np.unique(graph)},
                    'query_status':'unresolved_latent_graph' if case=='hidden_common' else 'exploratory_graph_requires_structural_assumptions'}
                runs.append(row)
            if r==0:
                fresh,_,_=generate(3000,spec['burn_in'],np.random.default_rng(spec['seed']+19+j),case=='hidden_common')
                orders=[list(range(6)),[0,2,1,3,4,5]]
                sensitivity={'target':'additive innovation in deposit-price equation to balances, fixed unit impulse',
                    'truth':response_from_matrices(matrices[0],np.stack(matrices[1:]),8),
                    'fitted_curves':[structural_response(fresh,order,lag=lag) for order in orders],
                    'orders':orders,'effect_status':'unavailable_under_latent_sufficiency_violation' if case=='hidden_common' else 'conditional_on_declared_order_and_lag',
                    'scope':'Alternative-model sensitivity, not graph confidence or a post-selection interval'}
            if r%5==0:print(json.dumps({'case':case,'repetition':r,'methods':[{k:v[k] for k in ['method','seconds','marks','adjacency_precision','adjacency_recall']} for v in runs[-2:]]}),flush=True)
        results.append({'case':case,'runs':runs,'effect_sensitivity':sensitivity})
    directory=ROOT/'docs/literature/runtime-scope';directory.mkdir(exist_ok=True);artifacts=[]
    for name,obj in [('pcmci',PCMCI.run_pcmciplus),('lpcmci',LPCMCI.run_lpcmci),('parcorr',ParCorr)]:
        file=directory/(name+'-operation.txt');file.write_text(inspect.getsource(obj));artifacts.append({'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'object':obj.__qualname__})
    dist=metadata.distribution('tigramite');file=directory/'tigramite-metadata.txt';file.write_text(dist.read_text('METADATA') or '');artifacts.append({'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    files=[path,Path(__file__)]
    receipt={'mode':'pilot' if args.pilot else 'final','spec':spec,'results':results,'seconds':time.perf_counter()-start,
        'runtime':{'distribution':'tigramite','version':dist.version,'artifacts':artifacts},
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'scope':'Selected temporal-search runtime and conditional response sensitivity; no discovery confidence guarantee or bank-data validation.'}
    (ROOT/'docs/studies'/('scope-discovery-pilot.json' if args.pilot else 'scope-discovery-results.json')).write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
