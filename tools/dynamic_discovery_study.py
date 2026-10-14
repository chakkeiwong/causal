#!/usr/bin/env python3
import argparse,hashlib,json,sys,time,itertools
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
from tigramite import data_processing as pp
from tigramite.lpcmci import LPCMCI
from tigramite.independence_tests.parcorr import ParCorr
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.ancestral_oracle import marginal_ancestral_graph,score_endpoints


def mechanism(spec):
    observed=spec['observed'];latent=spec['latent'];nodes=latent+observed
    weighted=[]
    for t in (0,1):
        u,x,m,y=[f'{v}_{t}' for v in ('liquidity','price','uptake','balance')]
        weighted.extend([(u,x,.8),(u,y,.8),(x,m,.7),(m,y,.5)])
    for name in ('liquidity','price','uptake','balance'):weighted.append((name+'_0',name+'_1',.6 if name=='liquidity' else .4))
    order=['liquidity_0','price_0','uptake_0','balance_0','liquidity_1','price_1','uptake_1','balance_1']
    return nodes,weighted,order


def hidden_queries():
    joint=np.zeros((2,2,2))
    for u,x,m,y in itertools.product(range(2),repeat=4):
        px=.2+.6*u;pm=.15+.6*x;py=.1+.3*m+.4*u
        joint[x,m,y]+=.5*(px if x else 1-px)*(pm if m else 1-pm)*(py if y else 1-py)
    px=joint.sum(axis=(1,2));pmx=joint.sum(axis=2)/px[:,None];eymx=joint[:,:,1]/joint.sum(axis=2)
    effects=[float(sum(pmx[a,m]*sum(eymx[x,m]*px[x] for x in (0,1)) for m in (0,1))) for a in (0,1)]
    naive=joint[1,:,1].sum()/px[1]-joint[0,:,1].sum()/px[0]
    # Same P(A,Y): A=U, Y=A versus A=U, Y=U. Intervention changes only A.
    return {'frontdoor':{'observed_joint':joint.tolist(),'identified_means':effects,'identified_contrast':effects[1]-effects[0],'structural_contrast':.6*.3,'naive_contrast':float(naive),
            'required_graph':'A -> M -> Y; A <-> Y; no direct A -> Y; no unblocked A-M backdoor and all M-Y backdoors blocked by A'},
            'unresolved_direct':{'observed_joint_both_models':[[.5,0],[0,.5]],'model_1':'U fair binary; A=U; Y=A','model_2':'U fair binary; A=U; Y=U','effects':[1.,0.],
            'required_additional_information':['randomized feasible action','sufficient observed confounder with positivity','valid instrument with its own identified target','defensible front-door mediator restrictions']}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',action='store_true');args=ap.parse_args();path=ROOT/'docs/studies/dynamic-discovery-spec.json';spec=json.loads(path.read_text())
    nodes,weighted,order=mechanism(spec);truth=marginal_ancestral_graph(nodes,[(a,b) for a,b,w in weighted],spec['observed']);runs=[];start=time.perf_counter()
    with threadpool_limits(limits=1):
        for rep in range(1 if args.pilot else spec['repetitions']):
            rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],rep]));values={}
            for node in order:values[node]=rng.normal(size=spec['episodes'])+sum(w*values[a] for a,b,w in weighted if b==node)
            data=np.column_stack([values[n] for n in spec['observed']]);engine=LPCMCI(dataframe=pp.DataFrame(data,var_names=spec['observed']),cond_ind_test=ParCorr(significance='analytic'),verbosity=0)
            fitted=engine.run_lpcmci(tau_min=0,tau_max=0,pc_alpha=spec['pc_alpha'],max_p_global=spec['search_limit'],max_p_non_ancestral=spec['search_limit'])
            graph=fitted['graph'][:,:,0];score=score_endpoints(graph,truth);runs.append({'rep':rep,'graph':graph.tolist(),'score':score})
            if rep%10==0:print(json.dumps({'rep':rep,'score':score}),flush=True)
    files=[path,Path(__file__),ROOT/'src/causalbank/ancestral_oracle.py'];result={'mode':'pilot' if args.pilot else 'final','spec':spec,'mechanism_edges':weighted,
        'truth':{k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in truth.items()},'runs':runs,'queries':hidden_queries(),'seconds':time.perf_counter()-start,
        'summary':{k:float(np.mean([r['score'][k] for r in runs])) for k in ('precision','recall','endpoint_claim_accuracy','circles','definite_endpoint_claims','wrong_definite_endpoints')},
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (ROOT/'docs/studies'/('dynamic-discovery-pilot.json' if args.pilot else 'dynamic-discovery-results.json')).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
