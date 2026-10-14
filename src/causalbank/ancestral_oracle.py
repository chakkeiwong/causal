"""Small finite-window marginal ancestral target using exhaustive separators."""
import itertools
import networkx as nx
import numpy as np


def marginal_ancestral_graph(nodes,edges,observed):
    dag=nx.DiGraph();dag.add_nodes_from(nodes);dag.add_edges_from(edges)
    if not nx.is_directed_acyclic_graph(dag):raise ValueError('oracle requires a finite DAG')
    observed=list(observed);p=len(observed);graph=np.full((p,p),'',dtype='<U3');separators={}
    for i,j in itertools.combinations(range(p),2):
        left,right=observed[i],observed[j];others=[x for x in observed if x not in (left,right)]
        separator=None
        for size in range(len(others)+1):
            for z in itertools.combinations(others,size):
                if nx.is_d_separator(dag,{left},{right},set(z)):
                    separator=list(z);break
            if separator is not None:break
        if separator is not None:separators[f'{left}|{right}']=separator;continue
        forward=nx.has_path(dag,left,right);backward=nx.has_path(dag,right,left)
        graph[i,j]='-->' if forward else '<--' if backward else '<->'
        graph[j,i]={'-->':'<--','<--':'-->','<->':'<->'}[graph[i,j]]
    return {'graph':graph,'separators':separators,'ancestry':np.array([[nx.has_path(dag,a,b) and a!=b for b in observed] for a in observed]),
            'scope':'Finite observed margin, no selection variables. Oracle MAG of supplied DAG, not its PAG equivalence class.'}


def score_endpoints(graph,truth):
    graph=np.asarray(graph);target=truth['graph'];p=len(graph);tp=fp=fn=claimed=wrong=circles=0
    for i,j in itertools.combinations(range(p),2):
        actual=bool(target[i,j]);pred=bool(graph[i,j]);tp+=actual and pred;fp+=pred and not actual;fn+=actual and not pred
        if not pred:continue
        for side,node,other in [(0,i,j),(2,j,i)]:
            mark=graph[i,j][side]
            if mark=='o':circles+=1;continue
            if mark not in ('-','<','>'):continue
            claimed+=1;tail=mark=='-'
            wrong+=not actual or bool(truth['ancestry'][node,other])!=tail
    return {'true_adjacencies':tp+fn,'selected_adjacencies':tp+fp,'true_positive':tp,'false_positive':fp,'false_negative':fn,
            'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,
            'definite_endpoint_claims':claimed,'wrong_definite_endpoints':wrong,'circles':circles,
            'endpoint_claim_accuracy':1-wrong/claimed if claimed else None,
            'scope':'Empirical soundness relative to generating ancestry; no assertion of orientation completeness or graph confidence.'}
