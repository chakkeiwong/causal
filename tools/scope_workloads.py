#!/usr/bin/env python3
"""Dominant scientific workloads in fresh processes, with dimensions preserved."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/causal-matplotlib')
for variable in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[variable]='1'
import argparse
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
import numpy as np
from threadpoolctl import threadpool_limits,threadpool_info
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def worker(spec,index,repeat,destination):
    case=spec['cases'][index];rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],index,repeat]));clock=time.perf_counter();stages={};result={'case':case,'repeat':repeat}
    def stage(name):
        nonlocal clock
        now=time.perf_counter();stages[name]=now-clock;clock=now
    with tempfile.TemporaryDirectory(prefix='causal-scope-',dir='/tmp') as tmp:
        path=Path(tmp)/'observation.npz'
        if case['kind']=='response':
            from study_responses import generate
            from causalbank.dependent_inference import response_alternatives
            config={'origins':case['dates'],'instrument_persistence':.85,'spectral_radius':.81,'strength':1.,'invalid_loading':0.}
            x,z,truth=generate(config,case['horizon'],rng);np.savez(path,x=x,z=z);restored=np.load(path)
            stage('generate_write_read')
            result['methods']=response_alternatives(restored['x'],restored['z'],case['horizon']);stage('three_covariances_and_weak_sets')
        elif case['kind']=='latent':
            from scope_latent import generate
            from causalbank.validated_latent import ModelShape,fit,uncertainty,contrast,unpack
            k,m=case['states'],case['signals'];shape=ModelShape(states=k,signals=m)
            e=np.ones((k,m))*.3/m;e[np.arange(k),np.arange(k)]+=.7
            q=np.column_stack((np.linspace(.85,.2,k),np.linspace(.15,.8,k)))
            transition=np.stack([.75*np.eye(k)+.25*np.ones((k,k))/k,.55*np.eye(k)+.45*np.ones((k,k))/k])
            config={'trajectories':case['trajectories'],'horizon':case['horizon'],'reward_sd':12.,'mu':np.full(k,1/k).tolist(),
                'emission':e.tolist(),'logger':q.tolist(),'transition':transition.tolist(),'reward':np.array([np.linspace(45,-30,k),np.linspace(35,-20,k)]).tolist()}
            obs,cal=generate(config,case['calibration'],rng);np.savez(path,o=obs[0],a=obs[1],r=obs[2],s=cal[0],c=cal[1]);data=np.load(path)
            obs=tuple(data[x] for x in ['o','a','r']);cal=tuple(data[x] for x in ['s','c']);stage('generate_write_read')
            theta,diag=fit(obs,cal,shape,starts=2,maxiter=450);info=uncertainty(theta,obs,cal,shape,case['horizon']);result.update(fit=diag,information=info,value=contrast(theta,shape,case['horizon']));stage('joint_fit_information_value')
            result['refits']=[]
            for b in range(case['refits']):
                rows=rng.integers(len(obs[0]),size=len(obs[0]));labels=rng.integers(len(cal[0]),size=len(cal[0]))
                estimate,d=fit(tuple(x[rows] for x in obs),tuple(x[labels] for x in cal),shape,seed=b+1,starts=2,maxiter=450)
                result['refits'].append({'value':contrast(estimate,shape,case['horizon']),'diagnostics':d})
            stage('whole_trajectory_and_calibration_refits')
        elif case['kind']=='discovery':
            from tigramite import data_processing as pp
            from tigramite.pcmci import PCMCI
            from tigramite.lpcmci import LPCMCI
            from tigramite.independence_tests.parcorr import ParCorr
            p,n=case['variables'],case['dates'];x=np.zeros((n+300,p));f=.4*np.eye(p)+.15*np.eye(p,k=-1)
            for t in range(1,len(x)):x[t]=f@x[t-1]+rng.normal(size=p)
            np.savez(path,x=x[300:]);data=pp.DataFrame(np.load(path)['x']);stage('generate_write_read')
            result['methods']={}
            for name,engine in [('PCMCI+',PCMCI),('LPCMCI',LPCMCI)]:
                obj=engine(dataframe=data,cond_ind_test=ParCorr(significance='analytic'),verbosity=0)
                fitted=obj.run_pcmciplus(tau_max=case['lags'],pc_alpha=.01) if name=='PCMCI+' else obj.run_lpcmci(tau_max=case['lags'],pc_alpha=.01,max_p_global=3,max_p_non_ancestral=3)
                result['methods'][name]={'graph':fitted['graph'].tolist(),'p_matrix':fitted['p_matrix'].tolist(),'value_matrix':fitted['val_matrix'].tolist()};stage(name+'_search_matrices')
        elif case['kind']=='continuous':
            from scope_continuous import generate
            from causalbank.continuous_controlled import fit,information,value
            settings=json.loads((ROOT/'docs/studies/scope-continuous-spec.json').read_text())
            data=generate(case['trajectories'],case['horizon'],settings['parameter'],settings['noise_variances'],rng)
            np.savez(path,o=data[0],a=data[1],r=data[2]);restored=np.load(path);data=tuple(restored[k] for k in ['o','a','r']);stage('generate_write_read')
            theta,diag=fit(data,settings['noise_variances']);result.update(fit=diag,information=information(theta,data,settings['noise_variances'],case['horizon']),value=value(theta,case['horizon']));stage('joint_gaussian_fit_score_information_value')
        elif case['kind']=='history':
            from scope_history import generate,learn_policy
            from causalbank.history_inference import HistoryQuery,evaluate_history
            from sklearn.ensemble import HistGradientBoostingRegressor
            from sklearn.linear_model import LogisticRegression
            settings=json.loads((ROOT/'docs/studies/scope-history-spec.json').read_text());policies,coef=learn_policy(settings)
            data=generate(case['trajectories'],case['horizon'],rng);np.savez(path,**data);data=dict(np.load(path));stage('independent_policy_training_generate_write_read')
            out=evaluate_history(data,HistoryQuery(case['horizon'],.97,'independent-pilot'),policies,HistGradientBoostingRegressor(max_iter=70,max_leaf_nodes=7,min_samples_leaf=35,l2_regularization=10,random_state=18),LogisticRegression(C=100,max_iter=400))
            out.pop('scores');out.pop('folds');result['result']=out;stage('crossfit_backward_recursion_score_covariance')
        else:
            import pandas as pd
            from sklearn.ensemble import HistGradientBoostingRegressor,HistGradientBoostingClassifier
            from causalbank.causal_workflow import AdjustmentQuery,adjustment_expression,fitted_components,independent_score_result,ratio_result
            from scope_public import matched_irm
            settings=json.loads((ROOT/'docs/studies/scope-public-spec.json').read_text());frame=pd.read_stata(ROOT/settings['data']);frame.to_pickle(Path(tmp)/'data.pkl');frame=pd.read_pickle(Path(tmp)/'data.pkl');stage('read_write_read_public_extract')
            query=AdjustmentQuery('e401','net_tfa',tuple(settings['controls']),'household','archived dollars')
            edges=[(v,'e401') for v in query.controls]+[(v,'net_tfa') for v in query.controls]+[('e401','net_tfa')]
            result['expression']=adjustment_expression(query,edges,list(frame.columns))
            reg=HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=10,random_state=33)
            clf=HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=10,random_state=33)
            components=fitted_components(frame,query,reg,clf,seed=7101+repeat);result['ate']=independent_score_result(components['score'],query.outcome_unit);stage('identification_fit_shared_score_inference')
            result['matched_reference_error']=matched_irm(frame,query,components,reg,clf);stage('direct_doubleml_same_predictions')
            first=fitted_components(frame,AdjustmentQuery('e401','p401',query.controls,'household','probability'),reg,clf,seed=7101+repeat,outcome_bounds=(0,1))
            result['late']=ratio_result(components['score'],first['score'],'archived dollars per complier');stage('first_stage_fit_joint_ratio_inversion')
        destination.write_text(json.dumps(result,indent=2)+'\n');stage('serialize_report')
    result.update(stages=stages,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,threadpools=threadpool_info())
    if any(pool['num_threads']!=spec['threads'] for pool in result['threadpools']):
        raise ValueError('measured thread pools violate workload specification')
    destination.write_text(json.dumps(result,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--worker',type=int);ap.add_argument('--repeat',type=int,default=0);ap.add_argument('--output');args=ap.parse_args()
    path=ROOT/'docs/studies/scope-workload-spec.json';spec=json.loads(path.read_text())
    if args.worker is not None:
        with threadpool_limits(limits=spec['threads']):worker(spec,args.worker,args.repeat,Path(args.output))
        return
    directory=ROOT/'docs/studies/scope-workload-runs';directory.mkdir(exist_ok=True);rows=[]
    for i,case in enumerate(spec['cases']):
        for repeat in range(spec['repeats']):
            destination=directory/(case['id']+'-'+str(repeat)+'.json');start=time.perf_counter()
            process=subprocess.run([sys.executable,str(Path(__file__)),'--worker',str(i),'--repeat',str(repeat),'--output',str(destination)],cwd=ROOT,capture_output=True,text=True)
            row={'case':case['id'],'repeat':repeat,'process_seconds':time.perf_counter()-start,'exit_code':process.returncode}
            if process.returncode:row['error']=process.stderr[-4000:]
            else:row.update(path=str(destination.relative_to(ROOT)),sha256=sha(destination))
            rows.append(row);print(json.dumps(row),flush=True)
    files=[path,Path(__file__)]+[ROOT/'tools'/('scope_'+name+'.py') for name in ['latent','history','public','continuous']]+[ROOT/'tools/study_responses.py']
    files += list((ROOT/'src/causalbank').glob('*.py'))+[ROOT/r['path'] for r in rows if 'path' in r]
    result={'status':'pass' if all(r['exit_code']==0 for r in rows) else 'fail','spec':spec,'runs':rows,
        'host':{'python':platform.python_version(),'cpu':next(s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.startswith('model name')),'logical_cpus':os.cpu_count(),
        'versions':{p:metadata.version(p) for p in ['numpy','scipy','scikit-learn','tigramite','DoubleML']}},
        'input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},'scope':spec['scope']}
    (ROOT/'docs/studies/scope-workload-results.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
