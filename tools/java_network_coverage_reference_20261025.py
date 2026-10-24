#!/usr/bin/env python3
"""Project-authored network arithmetic; no acquired JVM source is executed."""
from fractions import Fraction as F
from itertools import permutations,product
from collections import deque
from heapq import heappop,heappush
import json

def calculate():
    edges=[('a','b'),('a','b'),('b','c')];t={'a':1,'b':0,'c':0}
    incoming=[s for s,d in edges if d=='b'];adjacent=[s if d=='b' else d for s,d in edges if s=='b' or d=='b']
    incoming_list=F(sum(t[x] for x in incoming),len(incoming))
    neighbor_list=F(sum(t[x] for x in adjacent),len(adjacent))
    neighbor_set=F(sum(t[x] for x in set(adjacent)),len(set(adjacent)))
    assert (incoming_list,neighbor_list,neighbor_set)==(1,F(2,3),F(1,2))
    initial=(1,0);sync=(initial[1],initial[0]);seq=[]
    for order in permutations([0,1]):
        x=list(initial)
        for i in order:x[i]=x[1-i]
        seq.append(dict(order=list(order),result=x,mean=str(F(sum(x),2))))
    assert sync==(0,1) and seq[0]['result']==[0,0] and seq[1]['result']==[1,1]
    means=[F(x['mean']) for x in seq];mixture_mean=sum(means)/len(means)
    mixture_variance=sum((x-mixture_mean)**2 for x in means)/len(means)
    assert mixture_mean==F(1,2) and mixture_variance==F(1,4)
    def hops(graph,source,target):
        pending=deque([(source,0)]);seen={source}
        while pending:
            node,distance=pending.popleft()
            if node==target:return distance
            for neighbor in graph.get(node,[]):
                if neighbor not in seen:seen.add(neighbor);pending.append((neighbor,distance+1))
        return None
    full={'a':['b'],'b':['c'],'c':[]};induced={n:[v for v in full[n] if v in {'a','c'}] for n in ['a','c']}
    triangle={'a':[('b',10),('c',1)],'c':[('b',1)],'b':[]}
    pending=[(0,'a')];minimum={}
    while pending:
        distance,node=heappop(pending)
        if node in minimum:continue
        minimum[node]=distance
        for neighbor,weight in triangle[node]:heappush(pending,(distance+weight,neighbor))
    assert hops(full,'a','c')==2 and hops(induced,'a','c') is None
    assert hops({n:[v for v,w in a] for n,a in triangle.items()},'a','b')==1 and minimum['b']==2
    signed=lambda x:((x+2**31)%2**32)-2**31
    assert signed(7)==signed(7+2**32)==7
    allocations=list(product([0,1],repeat=2));law=[]
    for p in [F(1,2),F(1,5)]:
        probs={''.join(map(str,z)):str(p**sum(z)*(1-p)**(2-sum(z))) for z in allocations}
        assert sum(F(v) for v in probs.values())==1
        law.append(dict(p=str(p),independent=probs,one_cluster={'00':str(1-p),'11':str(p),'01':'0','10':'0'}))
    return dict(provenance='Authored graph and arithmetic examples;not native JVM outputs.',native_execution=False,
      exposure=dict(edges=[list(e) for e in edges],treatment=t,incoming_list=str(incoming_list),all_incident_list=str(neighbor_list),unique_neighbors=str(neighbor_set)),
      distances=dict(directed_path=['a','b','c'],full_graph_a_to_c_hops=2,induced_a_c_path_exists=False,weighted_triangle={'ab':10,'ac':1,'cb':1},a_to_b_hops=1,minimum_weight=2,bfs_selected_direct_edge_weight=10),
      scheduling=dict(initial=list(initial),synchronous=list(sync),sequential=seq,equal_order_mixture_mean='1/2',equal_order_mixture_variance='1/4',synchronous_mean='1/2',synchronous_mean_variance='0',scope='Assumed equiprobable order of two authored updates;not a fitted simulation.'),
      seed_conversion=dict(originals=[7,7+2**32],effective=[signed(7),signed(7+2**32)],collision=True),
      assignment_laws=law,
      costs={str(n):str(F(30000,n)) for n in [1000,600,400]})

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
