#!/usr/bin/env python3
"""Link temporal graph output to explicitly conditional structural effect queries."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.discovery_workflow import TemporalEffectQuery,conditional_effects,compatible_orders
from scope_discovery import generate


def main():
    source=ROOT/'docs/studies/scope-discovery-results.json';data=json.loads(source.read_text());rows=[]
    for j,case in enumerate(data['results']):
        x,_,_=generate(3000,250,np.random.default_rng(2026100847+j),case['case']=='hidden_common')
        for run in [r for r in case['runs'] if r['repetition']==0]:
            query=TemporalEffectQuery(1,2,8,'balance units per unit price-equation impulse',case['case']!='hidden_common',run['lag'])
            try: result=conditional_effects(x,run['graph'],query)
            except ValueError as exc:result={'status':'unsupported_graph_marks','reason':str(exc)}
            rows.append({'case':case['case'],'method':run['method'],'result':result})
    # Observationally equivalent Gaussian innovations make the decision
    # ambiguity material: both contemporaneous directions fit the same law.
    rng=np.random.default_rng(2026100848);n=8000;u=rng.normal(size=(n+300,2));x=np.zeros_like(u)
    for t in range(1,len(x)):
        x[t,0]=.5*x[t-1,0]+u[t,0]
        x[t,1]=.5*x[t-1,1]+.6*u[t,0]+u[t,1]
    graph=np.full((2,2,2),'',dtype='<U3');graph[0,1,0]=graph[1,0,0]='o-o';graph[:,:,1]='-->'
    ambiguous=conditional_effects(x[300:],graph,TemporalEffectQuery(0,1,4,'balance per price unit',True,1))
    assert len(ambiguous['curves'])==2 and ambiguous['pointwise_envelope'][0][1]>.5 and abs(ambiguous['pointwise_envelope'][0][0])<1e-12
    mixed=graph.copy();mixed[0,1,0]=mixed[1,0,0]='<->'
    try:compatible_orders(mixed);raise AssertionError('bidirected endpoint erased')
    except ValueError:pass
    files=[source,Path(__file__),ROOT/'tools/scope_discovery.py',ROOT/'src/causalbank/discovery_workflow.py']
    receipt={'status':'pass','queries':rows,'ambiguous_gaussian_example':ambiguous,'checks':['unresolved contemporaneous direction yields different effects','bidirected endpoints rejected by DAG adapter'],
      'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
      'scope':'Actual search graph to fresh-sample conditional structural point sets; no selected-graph confidence guarantee or general PAG completion.'}
    (ROOT/'docs/studies/scope-graph-effect-results.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'queries':[(r['case'],r['method'],r['result']['status'],len(r['result'].get('curves',[]))) for r in rows],
                      'ambiguity_envelope':ambiguous['pointwise_envelope']}))


if __name__=='__main__':main()
