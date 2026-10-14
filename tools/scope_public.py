#!/usr/bin/env python3
"""Public financial application and matched substantive DoubleML adapter."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-matplotlib')
import hashlib
import importlib.metadata as metadata
import inspect
import json
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor,HistGradientBoostingClassifier
from sklearn.linear_model import Ridge,LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures,StandardScaler
from threadpoolctl import threadpool_limits
import doubleml as dml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.causal_workflow import AdjustmentQuery,adjustment_expression,fitted_components,independent_score_result,ratio_result


def matched_irm(frame,query,components,reg,clf):
    data=dml.DoubleMLData(frame,y_col=query.outcome,d_cols=query.action,x_cols=list(query.controls))
    backend=dml.DoubleMLIRM(data,reg,clf,n_folds=len(components['splits']),draw_sample_splitting=False,
                           normalize_ipw=False,trimming_threshold=.01)
    backend.set_sample_splitting(components['splits'])
    g0,g1,p=components['nuisance'].T
    backend.fit(external_predictions={query.action:{'ml_g0':g0[:,None],'ml_g1':g1[:,None],'ml_m':p[:,None]}})
    reference=independent_score_result(components['score'],query.outcome_unit)
    errors={'coefficient':abs(float(backend.coef[0])-reference['estimate']),
            'standard_error':abs(float(backend.se[0])-np.sqrt(reference['variance']))}
    if errors['coefficient']>1e-8 or errors['standard_error']>1e-8:raise AssertionError(errors)
    return errors


def main():
    path=ROOT/'docs/studies/scope-public-spec.json';spec=json.loads(path.read_text()); data_path=ROOT/spec['data']
    frame=pd.read_stata(data_path); original=len(frame); required=[spec[k] for k in ['outcome','eligibility','participation']]+spec['controls']
    frame=frame.dropna(subset=required).reset_index(drop=True)
    query=AdjustmentQuery(spec['eligibility'],spec['outcome'],tuple(spec['controls']),'sample household','archived dollars')
    edges=[(c,query.action) for c in query.controls]+[(c,query.outcome) for c in query.controls]+[(query.action,query.outcome)]
    expression=adjustment_expression(query,edges,required); results=[]; start=time.perf_counter()
    for family in spec['learners']:
        if family=='quadratic_ridge_logit':
            reg=make_pipeline(StandardScaler(),PolynomialFeatures(2,include_bias=False),Ridge(alpha=10.))
            clf=make_pipeline(StandardScaler(),PolynomialFeatures(2,include_bias=False),LogisticRegression(C=.1,max_iter=1500))
        else:
            reg=HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=10,random_state=33)
            clf=HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=10,random_state=33)
        with threadpool_limits(limits=1):
            for seed in spec['seeds']:
                tic=time.perf_counter();components=fitted_components(frame,query,reg,clf,seed,spec['folds'],spec['propensity_clip'])
                ate=independent_score_result(components['score'],query.outcome_unit)
                match=matched_irm(frame,query,components,reg,clf)
                # The same observation roles, split and adjustment operation produce
                # the first-stage functional; Bernoulli outcome regression is bounded.
                first_query=AdjustmentQuery(query.action,spec['participation'],query.controls,query.unit,'probability')
                first=fitted_components(frame,first_query,reg,clf,seed,spec['folds'],spec['propensity_clip'],outcome_bounds=(0,1))
                late=ratio_result(components['score'],first['score'],'archived dollars per complier')
                row={'learner':family,'seed':seed,'seconds':time.perf_counter()-tic,'eligibility_ate':ate,'participation_late':late,
                     'overlap':components['diagnostics'],'matched_doubleml_error':match}
                results.append(row);print(json.dumps(row),flush=True)
    # A second dataset exercises the same graph/expression/score/backend objects
    # with different roles, currency and adjustment dimension.
    rng=np.random.default_rng(510);n=1600;risk=rng.normal(size=n);contact=rng.binomial(1,1/(1+np.exp(-.5*risk)));profit=7*contact+12*risk+rng.normal(size=n)
    synthetic=pd.DataFrame({'risk':risk,'contact':contact,'contribution':profit})
    other=AdjustmentQuery('contact','contribution',('risk',),'customer','GBP');other_expression=adjustment_expression(other,[('risk','contact'),('risk','contribution'),('contact','contribution')],synthetic.columns)
    with threadpool_limits(limits=1):
        components=fitted_components(synthetic,other,Ridge(alpha=.1),LogisticRegression(C=10,max_iter=500),84)
        reuse={'expression':other_expression,'result':independent_score_result(components['score'],'GBP'),'known_truth':7,
               'matched_doubleml_error':matched_irm(synthetic,other,components,Ridge(alpha=.1),LogisticRegression(C=10,max_iter=500))}
    runtime_dir=ROOT/'docs/literature/runtime-scope';runtime_dir.mkdir(exist_ok=True)
    runtime=[]
    for name,objects in [('doubleml',[dml.DoubleMLIRM,dml.DoubleMLIRM.fit,dml.DoubleMLData])]:
        dist=metadata.distribution(name);artifacts=[]
        for i,obj in enumerate(objects):
            file=runtime_dir/(name+'-'+str(i)+'.txt');file.write_text(inspect.getsource(obj));artifacts.append({'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'object':obj.__qualname__})
        file=runtime_dir/(name+'-metadata.txt');file.write_text(dist.read_text('METADATA') or '');artifacts.append({'path':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
        runtime.append({'distribution':name,'version':dist.version,'artifacts':artifacts})
    files=[path,data_path,Path(__file__),ROOT/'src/causalbank/causal_workflow.py',ROOT/'src/causalbank/responses.py']
    receipt={'status':'pass','data_rows':len(frame),'original_rows':original,'columns':required,'naive_difference':float(frame.groupby(query.action)[query.outcome].mean().diff().iloc[-1]),
       'expression':expression,'results':results,'synthetic_reuse':reuse,'runtime':runtime,'seconds':time.perf_counter()-start,
       'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
       'scope':'Public empirical financial design reproduction with declared new learners/splits; matched IRM runtime algebra; empirical causal truth, survey-design validity and transfer to banks not established.'}
    (ROOT/'docs/studies/scope-public-results.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
