"""Small compositional adjustment/IV workflow with explicit causal obligations."""
from dataclasses import dataclass, asdict
import numpy as np
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold
from .responses import moment_test_sets


@dataclass(frozen=True)
class AdjustmentQuery:
    action: str
    outcome: str
    controls: tuple
    unit: str
    outcome_unit: str
    sampling: str = 'independent_units'


def adjustment_expression(query, edges, observed_nodes):
    """Classical sufficient back-door criterion via ancestral moral graph.

    Graph is an analyst-supplied acyclic SCM graph. Observed data cannot verify
    its missing arrows. An unavailable adjustment set is not nonidentification.
    """
    nodes=set(observed_nodes)|{x for edge in edges for x in edge}
    parents={v:set() for v in nodes}; children={v:set() for v in nodes}
    for u,v in edges: parents[v].add(u); children[u].add(v)
    def closure(start,links):
        out=set(start); queue=list(start)
        while queue:
            for v in links[queue.pop()]:
                if v not in out: out.add(v);queue.append(v)
        return out
    for v in nodes:
        if any(v in closure([c],children) for c in children[v]):
            raise ValueError('cyclic graph outside adjustment workflow')
    a,y,z=query.action,query.outcome,set(query.controls)
    if not ({a,y}|z)<=set(observed_nodes):raise ValueError('unobserved variable in adjustment request')
    if {a,y}&z or z&(closure([a],children)-{a}):raise ValueError('invalid descendant/outcome adjustment')
    back_parents={v:ps-{a} for v,ps in parents.items()}
    ancestral=closure({a,y}|z,back_parents)
    moral={v:set() for v in ancestral}
    for v in ancestral:
        ps=back_parents[v]&ancestral
        for p in ps:moral[p].add(v);moral[v].add(p)
        for p in ps:
            moral[p].update(ps-{p})
    for v in moral:moral[v]-=z
    if y in closure([a],moral):raise ValueError('declared controls do not block the back-door paths')
    if query.sampling!='independent_units':raise ValueError('iid adjustment backend cannot inherit a dependent sampling law')
    return {'operator':'adjustment_contrast','query':asdict(query),
        'expression':{'difference_of_actions':[1,0],'conditional_outcome':{'random':y,'given':[a,*query.controls]},'integrate':list(query.controls)},
        'nuisances':['outcome_under_0','outcome_under_1','action_probability'],
        'assumptions':['supplied DAG causal semantics','consistency','back-door identification','positivity','independent units'],
        'trace':{'criterion':'back-door by ancestral moral separation','edges':[list(e) for e in edges],'adjustment':list(query.controls)}}


def fitted_components(frame,query,regressor,classifier,seed=71,folds=3,clip=.01,outcome_bounds=None):
    x=frame[list(query.controls)].to_numpy(float);a=frame[query.action].to_numpy(int);y=frame[query.outcome].to_numpy(float)
    if not np.isin(a,[0,1]).all() or not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('binary action and finite numeric data required')
    if len(np.unique(a))!=2:raise ValueError('both actions must be observed')
    nuisance=np.empty((len(y),3)); splits=list(StratifiedKFold(folds,shuffle=True,random_state=seed).split(x,a))
    for train,test in splits:
        model=clone(classifier).fit(x[train],a[train]);nuisance[test,2]=model.predict_proba(x[test])[:,list(model.classes_).index(1)]
        for arm in [0,1]:
            rows=train[a[train]==arm]; outcome_model=clone(regressor).fit(x[rows],y[rows]);nuisance[test,arm]=outcome_model.predict(x[test])
    if outcome_bounds is not None:
        if not np.all((y>=outcome_bounds[0])&(y<=outcome_bounds[1])):raise ValueError('outcome outside declared support')
        nuisance[:,:2]=np.clip(nuisance[:,:2],*outcome_bounds)
    raw=nuisance[:,2].copy(); nuisance[:,2]=np.clip(raw,clip,1-clip)
    score=adjustment_score(y,a,nuisance)
    return {'nuisance':nuisance,'score':score,'splits':splits,
        'diagnostics':{'clipped':int(np.count_nonzero(raw!=nuisance[:,2])),'propensity_quantiles':np.quantile(raw,[0,.01,.5,.99,1]).tolist(),
        'largest_weight':float(np.max(a/nuisance[:,2]+(1-a)/(1-nuisance[:,2]))),'fold_seed':seed,'folds':folds}}


def adjustment_score(y,a,nuisance):
    g0,g1,p=np.asarray(nuisance).T
    return g1-g0+a*(y-g1)/p-(1-a)*(y-g0)/(1-p)


def independent_score_result(score,unit):
    score=np.asarray(score,float);estimate=float(score.mean());variance=float(np.mean((score-estimate)**2)/len(score))
    return {'operator':'mean_score','estimate':estimate,'variance':variance,'unit':unit,'sampling_units':len(score),
        'interval':[estimate-1.959963984540054*np.sqrt(variance),estimate+1.959963984540054*np.sqrt(variance)],
        'scope':'Asymptotic independent-unit inference conditional on identification and nuisance-rate assumptions'}


def ratio_result(numerator_scores,denominator_scores,unit):
    moments=np.column_stack((numerator_scores,denominator_scores));mean=moments.mean(axis=0)
    lrv=np.cov(moments,rowvar=False,ddof=0)
    sets=moment_test_sets(mean,lrv,len(moments),simultaneous=False)[0]
    theta=float(mean[0]/mean[1]);influence=(moments[:,0]-theta*moments[:,1])/mean[1]
    return {'operator':'ratio_of_functionals','estimate':theta,'variance':float(np.mean(influence**2)/len(moments)),
        'denominator':float(mean[1]),'interval_union':sets,'unit':unit,
        'additional_assumptions':['instrument exclusion','conditional instrument independence','monotonicity','nonzero complier mass'],
        'scope':'LATE only under additional IV assumptions; interval inversion retains weak denominator topology'}
