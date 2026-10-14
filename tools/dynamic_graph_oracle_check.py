#!/usr/bin/env python3
"""Separate deterministic CI/search correctness from finite-data graph errors."""
import hashlib,json,sys,itertools
from pathlib import Path
import numpy as np
import networkx as nx
from tigramite import data_processing as pp
from tigramite.lpcmci import LPCMCI
from tigramite.independence_tests.oracle_conditional_independence import OracleCI
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.ancestral_oracle import marginal_ancestral_graph,score_endpoints
from dynamic_discovery_study import mechanism


def main():
    path=ROOT/'docs/studies/dynamic-discovery-spec.json';spec=json.loads(path.read_text());nodes,weighted,order=mechanism(spec)
    nodes=spec['observed']+spec['latent'];links={i:[] for i in range(len(nodes))};edges=[(a,b) for a,b,w in weighted]
    for a,b in edges:links[nodes.index(b)].append((nodes.index(a),0))
    oracle=OracleCI(links=links,observed_vars=list(range(len(spec['observed']))),tau_max=0)
    dag=nx.DiGraph(edges);comparisons=0;mismatches=[]
    for i,j in itertools.combinations(range(len(spec['observed'])),2):
        other=[k for k in range(len(spec['observed'])) if k not in (i,j)]
        for size in range(len(other)+1):
            for z in itertools.combinations(other,size):
                val,p=oracle.run_test([(i,0)],[(j,0)],[(k,0) for k in z]);nx_sep=nx.is_d_separator(dag,{nodes[i]},{nodes[j]},{nodes[k] for k in z});comparisons+=1
                if bool(p==1)!=nx_sep:mismatches.append([i,j,list(z)])
    truth=marginal_ancestral_graph(nodes,edges,spec['observed'])
    fitted=LPCMCI(dataframe=pp.DataFrame(np.zeros((20,len(spec['observed'])))),cond_ind_test=oracle,verbosity=0).run_lpcmci(tau_max=0,pc_alpha=.01,max_p_global=spec['search_limit'],max_p_non_ancestral=spec['search_limit'])
    graph=fitted['graph'][:,:,0];score=score_endpoints(graph,truth)
    result={'status':'pass' if not mismatches and score['false_positive']==0 and score['false_negative']==0 and score['wrong_definite_endpoints']==0 else 'fail',
        'independent_dseparation_comparisons':comparisons,'mismatches':mismatches,'oracle_lpcmci_graph':graph.tolist(),'score':score,
        'scope':'Finite-DAG oracle crosscheck; correctness with population independence does not qualify finite-data graph selection.',
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [path,Path(__file__),ROOT/'tools/dynamic_discovery_study.py',ROOT/'src/causalbank/ancestral_oracle.py']}}
    (ROOT/'docs/reviews/dynamic-graph-oracle.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(result['status']!='pass')


if __name__=='__main__':main()
