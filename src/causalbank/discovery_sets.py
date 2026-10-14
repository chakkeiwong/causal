"""Conservative Gaussian covariance-to-DAG/effect confidence construction.

Supports three observed variables, independent Gaussian samples and a supplied
causally sufficient linear structural class. Returned intervals are outer
bounds, not a certified minimal identified set or posterior graph probabilities.
"""
import itertools

import numpy as np
from scipy.stats import chi2


def add(a,b):
    return np.nextafter(a[0]+b[0],-np.inf),np.nextafter(a[1]+b[1],np.inf)


def negate(a):
    return -a[1],-a[0]


def multiply(a,b):
    if a==(0.,0.) or b==(0.,0.):
        return 0.,0.
    if not np.all(np.isfinite([*a,*b])):
        return -np.inf,np.inf
    products=[x*y for x in a for y in b]
    return np.nextafter(min(products),-np.inf),np.nextafter(max(products),np.inf)


def divide_positive(a,b):
    if b[0]<=0:
        return -np.inf,np.inf
    return multiply(a,(np.nextafter(1/b[1],-np.inf),np.nextafter(1/b[0],np.inf)))


def covariance_region(data,alpha=.05):
    n,p=data.shape
    if p!=3 or n<=p or not np.all(np.isfinite(data)):
        raise ValueError("finite n-by-3 independent Gaussian data required")
    directions=[np.eye(p)[j] for j in range(p)]
    for i,j in itertools.combinations(range(p),2):
        directions.extend([np.eye(p)[i]+np.eye(p)[j],np.eye(p)[i]-np.eye(p)[j]])
    lower_quantile=chi2.ppf(alpha/(2*len(directions)),n-1)
    upper_quantile=chi2.ppf(1-alpha/(2*len(directions)),n-1)
    bounds=[]
    for v in directions:
        sample_variance=np.var(data@v,ddof=1)
        # Statistical quantiles/variance are floating-point approximations;
        # only subsequent interval operations have outward rounding.
        bounds.append((np.nextafter((n-1)*sample_variance/upper_quantile,-np.inf),
                       np.nextafter((n-1)*sample_variance/lower_quantile,np.inf)))
    entries=[[None]*p for _ in range(p)]
    for j in range(p):
        entries[j][j]=bounds[j]
    at=p
    for i,j in itertools.combinations(range(p),2):
        plus,minus=bounds[at:at+2]; at+=2
        entries[i][j]=entries[j][i]=multiply(add(plus,negate(minus)),(.25,.25))
    return entries,{"directions":[v.tolist() for v in directions],"variance_bounds":bounds}


def dag_class(time_order=None):
    edges=[(i,j) for i in range(3) for j in range(3) if i!=j]
    dags=[]
    for selected in itertools.product((0,1),repeat=len(edges)):
        matrix=np.zeros((3,3),dtype=int)
        for include,(i,j) in zip(selected,edges):
            matrix[i,j]=include
        if time_order is not None:
            rank={v:k for k,v in enumerate(time_order)}
            if any(matrix[i,j] and rank[i]>=rank[j] for i,j in edges):
                continue
        # A 3-node digraph is acyclic iff it has no length-2/3 closed walk.
        if np.trace(matrix@matrix)==0 and np.trace(matrix@matrix@matrix)==0:
            dags.append(matrix)
    return dags


def separated(graph,x,y,condition):
    ancestors=set([x,y,*condition])
    changed=True
    while changed:
        prior=len(ancestors)
        ancestors.update(i for i in range(3) if any(graph[i,j] for j in list(ancestors)))
        changed=len(ancestors)>prior
    moral=graph+graph.T
    for child in ancestors:
        parents=[i for i in ancestors if graph[i,child]]
        for i,j in itertools.combinations(parents,2):
            moral[i,j]=moral[j,i]=1
    reached={x}; pending=[x]
    while pending:
        v=pending.pop()
        for j in ancestors-set(condition)-reached:
            if moral[v,j]:
                reached.add(j); pending.append(j)
    return y not in reached


def can_exclude(graph,entries):
    for i,j in itertools.combinations(range(3),2):
        third=3-i-j
        for condition in ([],[third]):
            if not separated(graph,i,j,condition):
                continue
            interval=entries[i][j]
            if condition:
                interval=add(multiply(entries[i][j],entries[third][third]),
                             negate(multiply(entries[i][third],entries[j][third])))
            if interval[0]>0 or interval[1]<0:
                return True
    return False


def effect_interval(graph,entries,treatment=1,outcome=2):
    coefficients={}
    for child in range(3):
        parents=[i for i in range(3) if graph[i,child]]
        if len(parents)==1:
            p=parents[0]
            coefficients[p,child]=divide_positive(entries[child][p],entries[p][p])
        elif len(parents)==2:
            i,j=parents
            # Squaring by interval multiplication is conservative if it crosses zero.
            denominator=add(multiply(entries[i][i],entries[j][j]),negate(multiply(entries[i][j],entries[i][j])))
            for p,q in ((i,j),(j,i)):
                numerator=add(multiply(entries[child][p],entries[q][q]),negate(multiply(entries[child][q],entries[p][q])))
                coefficients[p,child]=divide_positive(numerator,denominator)
    def paths(node,visited):
        if node==outcome:
            return (1.,1.)
        total=(0.,0.)
        for following in range(3):
            if graph[node,following] and following not in visited:
                total=add(total,multiply(coefficients[node,following],paths(following,visited|{following})))
        return total
    return paths(treatment,{treatment})


def confidence_effects(data,time_order=None,alpha=.05):
    entries,region=covariance_region(data,alpha)
    retained=[]
    for graph in dag_class(time_order):
        if not can_exclude(graph,entries):
            interval=effect_interval(graph,entries)
            retained.append({"graph":graph.tolist(),"interval":[float(v) for v in interval]})
    intervals=sorted((tuple(r["interval"]) for r in retained))
    merged=[]
    for lo,hi in intervals:
        if merged and lo<=merged[-1][1]:
            merged[-1][1]=max(merged[-1][1],hi)
        else:
            merged.append([lo,hi])
    for row in retained:
        row["interval"]=[v if np.isfinite(v) else None for v in row["interval"]]
    merged=[[v if np.isfinite(v) else None for v in pair] for pair in merged]
    return {"kind":"outer_confidence_set","level":1-alpha,"effect_intervals":merged,
            "retained_models":retained,"covariance_region":region,
            "assumptions":["iid Gaussian","linear acyclic structural equations","independent errors"]
                          +(["supplied background order"] if time_order is not None else []),
            "scope":"Finite-sample construction in exact arithmetic; outward interval operations with ordinary floating-point variance/chi-square quantiles. Outer bounds can be loose; not a certified numerical enclosure."}


def population_effects(covariance,time_order=None):
    output=[]
    for graph in dag_class(time_order):
        coefficient=np.zeros((3,3))
        for child in range(3):
            parents=np.flatnonzero(graph[:,child])
            if len(parents):
                coefficient[child,parents]=np.linalg.solve(covariance[np.ix_(parents,parents)],covariance[parents,child])
        residual=(np.eye(3)-coefficient)@covariance@(np.eye(3)-coefficient).T
        if np.max(abs(residual-np.diag(np.diag(residual))))<1e-9:
            output.append(float(np.linalg.inv(np.eye(3)-coefficient)[2,1]))
    return sorted(set(round(x,10) for x in output))
