"""Explicitly conditional effects from supplied temporal graph completions."""
from dataclasses import dataclass,asdict
import itertools
import numpy as np


@dataclass(frozen=True)
class TemporalEffectQuery:
    action: int
    outcome: int
    horizon: int
    unit: str
    causal_sufficiency: bool
    maximum_lag: int


def compatible_orders(graph):
    """Temporal-search CPDAG-like marks under a separate sufficiency declaration.

    This is a bounded order enumeration. It does not complete general PAGs,
    erase conflicts, or establish that a sample graph contains the truth.
    """
    graph=np.asarray(graph);p=graph.shape[0]
    if p>7:raise ValueError('order enumeration limited to seven variables')
    allowed={'','-->','<--','o-o'}
    if any(str(mark) not in allowed for mark in graph[:,:,0].ravel()):
        raise ValueError('mixed or conflicting endpoints require a PAG identification backend')
    if any(str(mark) not in {'','-->'} for mark in graph[:,:,1:].ravel()):
        raise ValueError('unresolved lagged marks require a richer graph backend')
    arrows=[(i,j) for i in range(p) for j in range(p) if graph[i,j,0]=='-->']
    lag=graph.shape[2]-1
    def adjacent(left,right):
        (u,s),(v,t)=left,right
        if s>t:return adjacent(right,left)
        return t-s<=lag and graph[u,v,t-s]!=''
    def no_new_colliders(order):
        for node in range(p):
            contemporary=[v for v in order[:order.index(node)] if graph[v,node,0]!='']
            parents=[(v,0) for v in contemporary]+[(v,-l) for l in range(1,lag+1) for v in range(p) if graph[v,node,l]!='']
            for left,right in itertools.combinations(parents,2):
                if not adjacent(left,right) and not all(graph[v,node,-t]=='-->' for v,t in [left,right]):
                    return False
        return True
    return [order for order in itertools.permutations(range(p))
            if all(order.index(i)<order.index(j) for i,j in arrows) and no_new_colliders(order)]


def conditional_effects(series,graph,query):
    if not query.causal_sufficiency:
        return {'status':'unsupported_latent_effect_query','query':asdict(query),
                'reason':'This recursive structural adapter assumes sufficiency; other identification routes may exist.'}
    graph=np.asarray(graph);x=np.asarray(series);n,p=x.shape;lag=query.maximum_lag
    if graph.shape!=(p,p,lag+1):raise ValueError('declared lag and graph shape differ')
    orders=compatible_orders(graph)
    if not orders:return {'status':'incompatible_directed_constraints','query':asdict(query)}
    curves=[];models=[]
    for order in orders:
        c=np.zeros((p,p));f=np.zeros((lag,p,p))
        for j,node in enumerate(order):
            contemporary=[v for v in order[:j] if graph[v,node,0]!='']
            temporal=[(v,l) for l in range(1,lag+1) for v in range(p) if graph[v,node,l]!='']
            cols=[np.ones(n-lag)]+[x[lag:,v] for v in contemporary]+[x[lag-l:n-l,v] for v,l in temporal]
            design=np.column_stack(cols);beta,_,rank,_=np.linalg.lstsq(design,x[lag:,node],rcond=None)
            if rank!=len(cols):raise ValueError('singular structural fit')
            c[node,contemporary]=beta[1:1+len(contemporary)]
            for coefficient,(v,l) in zip(beta[1+len(contemporary):],temporal):f[l-1,node,v]=coefficient
        inv=np.linalg.solve(np.eye(p)-c,np.eye(p));comp=np.zeros((p*lag,p*lag))
        comp[:p]=np.concatenate([inv@a for a in f],axis=1)
        if lag>1:comp[p:,:-p]=np.eye(p*(lag-1))
        impulse=np.zeros(p*lag);impulse[:p]=inv[:,query.action]
        curve=[]
        for h in range(query.horizon+1):curve.append(float(impulse[query.outcome]));impulse=comp@impulse
        curves.append(curve);models.append({'order':order,'radius':float(max(abs(np.linalg.eigvals(comp))))})
    return {'status':'conditional_structural_effect_set','query':asdict(query),'curves':curves,'models':models,
      'pointwise_envelope':np.array([np.min(curves,axis=0),np.max(curves,axis=0)]).T.tolist(),
      'inference':'No confidence claim: sample graph and linear sufficient structural model are imposed; envelope represents enumerated order ambiguity only.'}
