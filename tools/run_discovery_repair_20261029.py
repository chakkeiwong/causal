"""Exact project comparison; no downloaded code or Java package is executed."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json
import random
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT/'docs/discovery-repair/2026-10-29/attempt-1'
START = time.monotonic()

def check_budget():
    if time.monotonic()-START > 600:
        raise TimeoutError('Declared ten-minute compute budget exhausted')

def edge(a, b):
    return tuple(sorted((a, b)))

def ancestors(nodes, parents):
    out=set(nodes); todo=list(nodes)
    while todo:
        x=todo.pop()
        for p in parents[x]:
            if p not in out:out.add(p);todo.append(p)
    return out

class Oracle:
    def __init__(self,n,arcs):
        self.n=n;self.arcs=frozenset(arcs);self.parents=[set() for _ in range(n)]
        self.neighbours=[set() for _ in range(n)];self.calls=[]
        for a,b in arcs:
            self.parents[b].add(a);self.neighbours[a].add(b);self.neighbours[b].add(a)
    @lru_cache(None)
    def moral(self,x,y,given):
        z=set(given);a=ancestors({x,y}|z,self.parents);g={v:set() for v in a}
        for child in a:
            pp=self.parents[child]&a
            for parent in pp:g[child].add(parent);g[parent].add(child)
            for p,q in combinations(pp,2):g[p].add(q);g[q].add(p)
        seen={x};todo=[x]
        while todo:
            node=todo.pop()
            for nxt in g[node]-z-seen:seen.add(nxt);todo.append(nxt)
        return y not in seen
    def independent(self,x,y,given):
        x,y=edge(x,y);given=tuple(sorted(given));self.calls.append((x,y,given))
        return self.moral(x,y,given)
    def path_oracle(self,x,y,given):
        z=set(given);ancz=ancestors(z,self.parents)
        def active(path):
            for a,b,c in zip(path,path[1:],path[2:]):
                collider=(a,b) in self.arcs and (c,b) in self.arcs
                if collider and b not in ancz:return False
                if not collider and b in z:return False
            return True
        def visit(path):
            for nxt in self.neighbours[path[-1]]-set(path):
                pp=path+[nxt]
                if nxt==y:
                    if active(pp):return True
                elif visit(pp):return True
            return False
        return not visit([x])

def skeleton_search(oracle,screen=False,cap=None):
    n=oracle.n;links=set(combinations(range(n),2));frozen=set();seps={};trace=[]
    maxdepth=n-2 if cap is None else cap;begin=len(oracle.calls)
    for depth in range(maxdepth+1):
        check_budget();neighbours=[set() for _ in range(n)]
        for a,b in links:neighbours[a].add(b);neighbours[b].add(a)
        active=sorted(links-frozen)
        if not active:break
        if screen and depth>2:
            for a,b in active:
                given=(neighbours[a]|neighbours[b])-{a,b}
                if not oracle.independent(a,b,given):
                    frozen.add((a,b));trace.append(dict(depth=depth,pair=[a,b],given=sorted(given),action='freeze_on_dependence'))
            active=sorted(links-frozen)
        deleted=set()
        for a,b in active:
            candidates=set(combinations(sorted(neighbours[a]-{b}),depth))
            candidates.update(combinations(sorted(neighbours[b]-{a}),depth))
            accepted=[]
            for given in sorted(candidates):
                if oracle.independent(a,b,given):accepted.append(list(given))
            if accepted:
                deleted.add((a,b));seps[f'{a},{b}']=accepted
        links-=deleted
        trace.append(dict(depth=depth,removed=[list(e) for e in sorted(deleted)],remaining=len(links)))
    remaining_candidates={}
    for a,b in sorted(links):
        na={j for i,j in links if i==a}|{i for i,j in links if j==a}
        nb={j for i,j in links if i==b}|{i for i,j in links if j==b}
        if cap is not None and max(len(na-{b}),len(nb-{a}))>cap:
            remaining_candidates[f'{a},{b}']='larger conditioning sets not examined'
    calls=oracle.calls[begin:]
    return dict(links=[list(x) for x in sorted(links)],separators=seps,
        calls=len(calls),distinct_queries=len(set(calls)),frozen=[list(x) for x in sorted(frozen)],
        unresolved=remaining_candidates,
        completion='incomplete_search' if remaining_candidates else ('screened_result' if screen else 'full_search'),trace=trace)

def compare(n,arcs,name,keep=False):
    truth={edge(*a) for a in arcs};o=Oracle(n,arcs)
    full=skeleton_search(o);screen=skeleton_search(o,screen=True);limited=skeleton_search(o,cap=2)
    full_edges={tuple(x) for x in full['links']};assert full_edges==truth,(name,full_edges,truth)
    for run in [full,screen,limited]:
        for key,sets in run['separators'].items():
            a,b=map(int,key.split(','))
            assert all(o.moral(a,b,tuple(z)) for z in sets)
    def summarize(run):
        est={tuple(x) for x in run['links']}
        return {**{k:run[k] for k in ['calls','distinct_queries','completion']},
                'false_positive':len(est-truth),'false_negative':len(truth-est),
                'unresolved_pairs':len(run['unresolved'])}
    row=dict(name=name,n=n,arcs=[list(x) for x in sorted(arcs)],full=summarize(full),screen=summarize(screen),depth2=summarize(limited))
    if keep:row.update(full_trace=full,screen_trace=screen,depth2_trace=limited)
    return row,o

def inverse(a):
    n=len(a);b=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(k for k in range(j,n) if b[k][j]);b[j],b[k]=b[k],b[j];v=b[j][j];b[j]=[x/v for x in b[j]]
        for i in range(n):
            if i!=j:
                v=b[i][j];b[i]=[x-v*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

def gaussian(k):
    n=k+3;load=[]
    for i in range(k):load.append([F(i==j) for j in range(n)])
    load.extend([[F(1)]*k+[F(1),F(0),F(0)],[F(1)]*k+[F(0),F(1),F(0)],[F(2)]*k+[F(1),F(1),F(1)]])
    cov=[[sum(x*y for x,y in zip(a,b)) for b in load] for a in load]
    def cond(i,j,z):
        if not z:return cov[i][j]
        inv=inverse([[cov[a][b] for b in z] for a in z])
        return cov[i][j]-sum(cov[i][a]*inv[r][c]*cov[b][j] for r,a in enumerate(z) for c,b in enumerate(z))
    z=list(range(k));allz=z+[k+2];small=[]
    for size in range(3):
        small.extend(cond(k,k+1,list(s)) for s in combinations(allz,size))
    assert all(x!=0 for x in small)
    base=cond(k,k+1,z);allcov=cond(k,k+1,allz);allvar=cond(k,k,allz)
    assert base==0 and allcov==F(-1,3) and allvar==F(2,3)
    return dict(k=k,baseline_conditional_covariance=str(base),collider_conditional_covariance=str(allcov),
        collider_conditional_variance=str(allvar),collider_adjusted_slope=str(allcov/allvar),
        unadjusted_slope=str(cov[k][k+1]/cov[k][k]),true_intervention_effect='0',small_nonseparators=len(small))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=DEFAULT);args=p.parse_args();out=args.output
    out.mkdir(parents=True,exist_ok=False);rows=[];oracle_checks=0
    try:
        for n in range(2,6):
            possible=list(combinations(range(n),2))
            for mask in range(1<<len(possible)):
                arcs=[a for i,a in enumerate(possible) if mask&(1<<i)]
                row,o=compare(n,arcs,f'ordered-{n}-{mask}');rows.append(row)
                if n==4:
                    for a,b in combinations(range(n),2):
                        other=[x for x in range(n) if x not in [a,b]]
                        for size in range(len(other)+1):
                            for z in combinations(other,size):
                                assert o.moral(a,b,z)==o.path_oracle(a,b,z),(mask,a,b,z);oracle_checks+=1
            print(json.dumps(dict(phase='ordered',nodes=n,cases=len(rows))),flush=True)
        rng=random.Random(20261029)
        for prob in [0.15,0.35,0.65,0.85]:
            for rep in range(64):
                arcs=[a for a in combinations(range(6),2) if rng.random()<prob]
                row,_=compare(6,arcs,f'seeded-6-{prob}-{rep}');rows.append(row)
        witnesses=[]
        for k in [3,4,5]:
            arcs=[(z,t) for z in range(k) for t in [k,k+1]]+[(k,k+2),(k+1,k+2)]
            row,o=compare(k+3,arcs,f'common-causes-{k}',keep=True);witnesses.append(row)
            for a,b,z in set(o.calls):
                assert o.moral(a,b,z)==o.path_oracle(a,b,z),(k,a,b,z);oracle_checks+=1
            assert row['screen']['false_positive']>=1 and row['depth2']['completion']=='incomplete_search'
        k=3;base=[(z,t) for z in range(k) for t in [k,k+1]]+[(k,k+2),(k+1,k+2)]
        relabels=[]
        perms=rng.sample(list(permutations(range(6))),24)
        for i,perm in enumerate(perms):
            row,_=compare(6,[(perm[a],perm[b]) for a,b in base],f'permuted-witness-{i}');row['permutation']=perm;relabels.append(row)
            assert row['screen']['false_positive']>=1 and row['depth2']['completion']=='incomplete_search'
        summary=[]
        for group,data in [('ordered-2-to-5',rows[:1098]),('seeded-six',rows[1098:]),('witness-family',witnesses),('relabelled-witness',relabels)]:
            summary.append(dict(group=group,cases=len(data),full_failures=sum(x['full']['false_positive']+x['full']['false_negative']>0 for x in data),
                screened_failures=sum(x['screen']['false_positive']+x['screen']['false_negative']>0 for x in data),
                depth2_wrong_skeletons=sum(x['depth2']['false_positive']+x['depth2']['false_negative']>0 for x in data),
                depth2_incomplete=sum(x['depth2']['completion']=='incomplete_search' for x in data),
                full_requests=sum(x['full']['calls'] for x in data),screen_requests=sum(x['screen']['calls'] for x in data)))
        result=dict(status='pass_for_declared_project_cases',kind='exact_population_oracle_comparison',native_java_execution=False,
            elapsed_seconds=round(time.monotonic()-START,3),oracle_crosschecks=oracle_checks,summary=summary,
            gaussian=[gaussian(k) for k in [3,4,5]],witnesses=witnesses,
            limits=['Finite ordered/seeded graph suite; not real-world prevalence or a general theorem.','No sample-based CI test, faithfulness, orientation, native Java, bank effect or product acceptance established.'])
        (out/'cases.json').write_text(json.dumps(rows+relabels,indent=2)+'\n');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        manifest=dict(seed=20261029,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),plan_sha256=hashlib.sha256((ROOT/'docs/program/discovery-repair-2026-10-29.md').read_bytes()).hexdigest(),results_sha256=hashlib.sha256((out/'results.json').read_bytes()).hexdigest(),cases_sha256=hashlib.sha256((out/'cases.json').read_bytes()).hexdigest())
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','elapsed_seconds','oracle_crosschecks','summary','gaussian']}),flush=True)
    except Exception as exc:
        (out/'failure.json').write_text(json.dumps(dict(error=repr(exc),completed_cases=len(rows),seconds=time.monotonic()-START),indent=2)+'\n')
        (out/'partial-cases.json').write_text(json.dumps(rows,indent=2)+'\n');raise

if __name__=='__main__':main()
