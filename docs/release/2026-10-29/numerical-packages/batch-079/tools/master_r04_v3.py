import numpy as np
from causalbank.temporal_class_v3 import simulate,infer,selected_challenger

def request(spec,cell,index):
    d=spec['designs'][cell];rng=np.random.default_rng([spec['seed'],cell,index])
    x=simulate(spec['dates'],rng,d);info=d.get('information','randomized_encouragement')
    out=infer(x,spec['candidate_lags'],info,spec['alpha'])
    true_edges=['Z_to_A','A_to_Y']
    if d.get('direct',0):true_edges.append('Z_to_Y')
    support=[1,2] if d.get('ua',.6) and d.get('uy',.7) else []
    out['true_class_retained']=any(r['rho']==d.get('rho',.4) and any(set(g['graph']['edges'])==set(true_edges) and g['graph']['latent_support']==support for g in r['graphs']) for r in out['candidates'])
    return dict(truth=d.get('tau',.8),methods=dict(class_union=out,selected_lag=selected_challenger(x,spec['candidate_lags'],info)),history_rows=int(x.size),labels=0)
