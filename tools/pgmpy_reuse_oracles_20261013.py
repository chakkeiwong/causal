#!/usr/bin/env python3
"""Project graph/SEM oracles. Does not import or execute pgmpy source."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-13/pgmpy-reuse'

def reachable(edges,seeds,reverse=False):
    result=set(seeds)
    while True:
        newer=result|{a if reverse else b for a,b in edges if (b if reverse else a) in result}
        if newer==result:return result
        result=newer

def acyclic(nodes,edges):
    remaining=set(nodes)
    while remaining:
        roots={n for n in remaining if not any(b==n and a in remaining for a,b in edges)}
        if not roots:return False
        remaining-=roots
    return True

def moral_separated(nodes,edges,x,y,conditioned):
    ancestors=reachable(edges,{x,y}|set(conditioned),reverse=True)
    undirected={frozenset((a,b)) for a,b in edges if a in ancestors and b in ancestors}
    for child in ancestors:
        parents={a for a,b in edges if b==child and a in ancestors}
        undirected|={frozenset(pair) for pair in combinations(parents,2)}
    allowed=ancestors-set(conditioned);seen={x};todo=[x]
    while todo:
        n=todo.pop()
        for pair in undirected:
            if n in pair:
                for other in pair-{n}:
                    if other in allowed and other not in seen:seen.add(other);todo.append(other)
    return y not in seen

def path_separated(nodes,edges,x,y,conditioned):
    # Enumerate simple skeleton paths and apply the collider/noncollider definition.
    adjacent={n:set() for n in nodes}
    for a,b in edges:adjacent[a].add(b);adjacent[b].add(a)
    paths=[]
    def visit(path):
        if path[-1]==y:paths.append(path);return
        for nxt in adjacent[path[-1]]-set(path):visit(path+[nxt])
    visit([x]);active_ancestors=reachable(edges,set(conditioned),reverse=True)
    for path in paths:
        active=True
        for i in range(1,len(path)-1):
            a,v,b=path[i-1:i+2];collider=(a,v) in edges and (b,v) in edges
            if collider and v not in active_ancestors:active=False;break
            if not collider and v in conditioned:active=False;break
        if active:return False
    return True

def strict_backdoor(nodes,edges,x,y,z):
    if set(z)&(reachable(edges,{x})-{x}):return False
    cut={(a,b) for a,b in edges if a!=x}
    return moral_separated(nodes,cut,x,y,z)

def valid_sets(nodes,edges,x,y):
    other=sorted(set(nodes)-{x,y});out=[]
    for k in range(len(other)+1):
        for z in combinations(other,k):
            if strict_backdoor(nodes,edges,x,y,z):out.append(set(z))
    return out

def main():
    out=BASE/'oracle-results.json';assert not out.exists()
    nodes=('A','B','X','Y');pairs=list(combinations(nodes,2));dags=0;checks=0
    for choices in product([0,1,2],repeat=len(pairs)):
        edges={(a,b) if c==1 else (b,a) for (a,b),c in zip(pairs,choices) if c}
        if not acyclic(nodes,edges):continue
        dags+=1
        for x,y in permutations(nodes,2):
            rest=set(nodes)-{x,y}
            for k in range(3):
                for z in combinations(sorted(rest),k):
                    assert moral_separated(nodes,edges,x,y,z)==path_separated(nodes,edges,x,y,set(z)),(edges,x,y,z)
                    checks+=1
    assert dags==543 and checks==26064
    # A graph has two inclusion-minimal separating sets with distinct cardinalities.
    nodes5={'C','A','B','X','Y'}
    edges5={('C','A'),('C','B'),('A','X'),('B','X'),('C','Y'),('X','Y')}
    sets=valid_sets(nodes5,edges5,'X','Y');minimal=[s for s in sets if not any(t<s for t in sets)]
    assert {frozenset(s) for s in minimal}=={frozenset({'C'}),frozenset({'A','B'})}
    greedy=[]
    for order in permutations(['A','B','C']):
        candidate={'A','B','C'}
        for n in order:
            if strict_backdoor(nodes5,edges5,'X','Y',candidate-{n}):candidate.remove(n)
        greedy.append({'deletion_order':order,'remaining':sorted(candidate)})
    assert {tuple(x['remaining']) for x in greedy}=={('A','B'),('C',)}
    # Mediated effect: U_X,U_M,U_Y independent, unit variance; M=2X+U_M, Y=3M+U_Y.
    cov={'xx':F(1),'xm':F(2),'xy':F(6),'mm':F(5),'my':F(15),'yy':F(46)}
    adjusted=(cov['xy']*cov['mm']-cov['xm']*cov['my'])/(cov['xx']*cov['mm']-cov['xm']**2)
    total=F(2)*3
    assert adjusted==0 and total==6
    chain={('X','M'),('M','Y')};parents={a for a,b in chain if b=='X'}
    # Transparent source-logic trace: the inspected _validate predicate is all(...) over parents.
    parent_only_accept=all(False for _ in parents)
    assert parent_only_accept is True and strict_backdoor({'X','M','Y'},chain,'X','Y',{'M'}) is False
    cycle=[('A','B'),('B','C'),('C','D'),('D','A')];orientations=[]
    for bits in product([0,1],repeat=4):
        edges={pair if bit else pair[::-1] for pair,bit in zip(cycle,bits)}
        if not acyclic('ABCD',edges):continue
        colliders=[]
        for v in 'ABCD':
            parents={a for a,b in edges if b==v}
            for a,b in combinations(sorted(parents),2):
                if (a,b) not in edges and (b,a) not in edges:colliders.append([a,v,b])
        orientations.append({'edges':sorted(edges),'unshielded_colliders':colliders})
    assert len(orientations)==14 and all(x['unshielded_colliders'] for x in orientations)
    result={'kind':'project_exact_graph_and_SEM_oracles','status':'pass','vendor_imports':0,'random_draws':0,'graph_independent_agreement':{'DAGs':dags,'dseparation_checks':checks,'implementations':['ancestral moralization','simple paths with collider ancestry']},'minimal_versus_minimum':{'edges':sorted(edges5),'inclusion_minimal_sets':[sorted(s) for s in minimal],'greedy_deletion_orders':greedy,'limit':'Project illustration of greedy semantics, not observed pgmpy output.'},'mediator_boundary':{'edges':sorted(chain),'covariance_entries':{k:str(v) for k,v in cov.items()},'total_effect':str(total),'regression_effect_conditioning_on_M':str(adjusted),'empty_parent_source_logic_accepts':parent_only_accept,'strict_preaction_backdoor_accepts':False,'USD_for_1000_accounts_one_unit_total':'6000','USD_if_mediator_coefficient_misreported':'0','limit':'Static call-path and exact project SEM argument; no installed pgmpy execution.'},'nonextendible_PDAG':{'skeleton':cycle,'acyclic_orientations':len(orientations),'extensions_preserving_no_unshielded_colliders':0,'enumeration':orientations},'claim_limits':['No upstream engine run, adapter conversion, finite-sample graph confidence or maintenance guarantee.','Conservative descendant exclusion is the proposed first-path restriction; it does not claim to enumerate all generalized valid adjustment sets.']}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','dags':dags,'independent_dseparation_checks':checks,'total_effect':6,'mediator_adjusted':0,'four_cycle_consistent_extensions':0,'pgmpy_executed':False}))

if __name__=='__main__':main()
