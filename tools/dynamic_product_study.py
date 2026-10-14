#!/usr/bin/env python3
"""Fresh-process full composition and partition comparison."""
import argparse,hashlib,json,sys,time,subprocess,resource,dataclasses,importlib.metadata,copy
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits,threadpool_info
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.dynamic_funding import FundingTarget,train_pilot
from causalbank.linked_observation import linked_response
from causalbank.dynamic_product import DynamicBrief,run_funding,treasury_report,application_result,materialize_candidate_feed
from dynamic_observation_study import make_linked


def default(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


def source_feed(data,horizon):
    n=len(data['action']);records=[];features=[];cutoff=n+horizon+2
    for i in range(n):
        features.append({'origin':i,'decision_day':i,'received_day':i,'features':data['x'][i].tolist(),'action':float(data['action'][i]),'stratum':int(data['stratum'][i])})
        for candidate in (0,1):
            for h in range(horizon+1):
                balance=float(data['outcomes'][i,candidate*(horizon+1)+h])
                records.append({'origin':i,'candidate':candidate,'horizon':h,'business_day':i+h,'received_day':i+h+1,'revision':1,'balance':balance})
                if h==0:records.append({'origin':i,'candidate':candidate,'horizon':h,'business_day':i,'received_day':cutoff+1,'revision':2,'balance':balance+3*data['action'][i]})
    return {'predecision_records':features,'outcome_records':records,'extraction_cutoff':cutoff}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--worker',action='store_true');ap.add_argument('--dates',type=int);ap.add_argument('--workers',type=int);ap.add_argument('--rep',type=int);args=ap.parse_args()
    path=ROOT/'docs/studies/dynamic-product-spec.json';spec=json.loads(path.read_text());obspath=ROOT/spec['observation_spec'];obs=json.loads(obspath.read_text());basepath=ROOT/obs['funding_spec'];base=json.loads(basepath.read_text());outdir=ROOT/'docs/studies/dynamic-product-runs';outdir.mkdir(exist_ok=True)
    if not args.worker:
        rows=[]
        for dates in spec['workloads']:
            for workers in spec['workers']:
                for rep in range(spec['repetitions']):
                    command=[sys.executable,str(Path(__file__)),'--worker','--dates',str(dates),'--workers',str(workers),'--rep',str(rep)]
                    process=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
                    if process.returncode:print(process.stdout,process.stderr);raise SystemExit(process.returncode)
                    name=f'{dates}-{workers}-{rep}.json';row=json.loads((outdir/name).read_text());rows.append({'path':str((outdir/name).relative_to(ROOT)),'sha256':hashlib.sha256((outdir/name).read_bytes()).hexdigest(),**{k:row[k] for k in ['dates','workers','rep','seconds','maximum_reference_error','rss_parent_kib','rss_child_max_kib']}});print(json.dumps(rows[-1]),flush=True)
        files=[path,obspath,basepath,Path(__file__),ROOT/'src/causalbank/dynamic_product.py',ROOT/'src/causalbank/dynamic_validation.py',ROOT/'src/causalbank/linkage_sets.py',ROOT/'src/causalbank/dynamic_funding.py',ROOT/'src/causalbank/linked_observation.py',ROOT/'tools/dynamic_observation_study.py',ROOT/'docs/studies/observation-fixtures-v6.json']
        result={'status':'pass' if all(r['maximum_reference_error']<1e-6 for r in rows) else 'fail','spec':spec,'runs':rows,'scope':'Complete local single-host partitioned construction; process overhead included; no multi-host service qualification',
                'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
        (ROOT/'docs/studies/dynamic-product-results.json').write_text(json.dumps(result,indent=2)+'\n');return
    dates=args.dates;target=FundingTarget(horizon=base['horizon'],branches=base['branches']);fixturepath=ROOT/'docs/studies/observation-fixtures-v6.json';fixture=json.loads(fixturepath.read_text())['cases'][0]
    start=time.perf_counter()
    with threadpool_limits(limits=1):
        pilot=make_linked(base,obs,spec['pilot_multiple']*dates,[spec['seed'],dates,0]);data=make_linked(base,obs,dates,[spec['seed'],dates,1]);rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],dates,2]));m=spec['audit_per_stratum'];strata=np.repeat([0,1],m);correct=(rng.random(2*m)<np.array(obs['correct_pair_probability'])[strata]).astype(int)
        brief=DynamicBrief(target,'fixture:'+hashlib.sha256(fixturepath.read_bytes()).hexdigest(),'pilot:'+str(spec['seed'])+':'+str(dates),'audit:'+str(spec['seed'])+':'+str(dates),int(2*dates**.2))
        feed=source_feed(data,target.horizon)
        result=run_funding(brief,fixture,pilot,feed,strata,correct,base['penalties'],workers=args.workers);seconds=time.perf_counter()-start
        # Independent direct reference is excluded from the workflow timing.
        direct_pilot=train_pilot(pilot,base['penalties']);success=np.bincount(strata,weights=correct,minlength=2);direct=linked_response(data,direct_pilot,success,[m,m],target,brief.bandwidth)
        errors=[float(abs(result['response']-direct['estimate']).max()),float(abs(result['covariance']-direct['covariance']).max()),abs(result['financial_value']-direct['financial_value']),abs(result['financial_se']-direct['financial_se'])]
        reconstructed=materialize_candidate_feed(feed,target.horizon)
        checks={'late_revision_excluded':bool(np.array_equal(reconstructed['outcomes'],data['outcomes']))}
        changed=dataclasses.replace(brief,target=dataclasses.replace(target,monthly_margin=.0015))
        changed_result=run_funding(changed,fixture,pilot,feed,strata,correct,base['penalties'],workers=1)
        checks['supported_margin_change']=bool(np.allclose(changed_result['response'],result['response']) and changed_result['identity']!=result['identity'])
        for name,bad in [('changed_sampling',dataclasses.replace(brief,target=dataclasses.replace(target,sampling='independent_branches'))),('economic_stock_flow',dataclasses.replace(brief,target=dataclasses.replace(target,outcome_kind='cash_flow')))]:
            try:run_funding(bad,fixture,pilot,feed,strata,correct,base['penalties'],workers=1);checks[name]=False
            except ValueError as exc:checks[name]=str(exc)
        try:run_funding(changed,fixture,pilot,feed,strata,correct,base['penalties'],cached_identity=result['identity']);checks['stale_cache_rejected']=False
        except ValueError as exc:checks['stale_cache_rejected']=str(exc)
        modified=dict(feed,outcome_records=[dict(row,balance=row['balance']+.1) for row in feed['outcome_records']])
        try:run_funding(brief,fixture,pilot,modified,strata,correct,base['penalties'],cached_identity=result['identity']);checks['changed_bytes_cache_rejected']=False
        except ValueError as exc:checks['changed_bytes_cache_rejected']=str(exc)
        try:run_funding(brief,fixture,pilot,feed,strata,correct,[0.0,1.0],cached_identity=result['identity']);checks['changed_learning_cache_rejected']=False
        except ValueError as exc:checks['changed_learning_cache_rejected']=str(exc)
        updated_fixture=copy.deepcopy(fixture);updated_fixture['claims'][0]['owner']='amended source authority'
        try:run_funding(brief,updated_fixture,pilot,feed,strata,correct,base['penalties'],cached_identity=result['identity']);checks['changed_source_contract_cache_rejected']=False
        except ValueError as exc:checks['changed_source_contract_cache_rejected']=str(exc)
        later_view=dict(feed,extraction_cutoff=feed['extraction_cutoff']+.1)
        try:run_funding(brief,fixture,pilot,later_view,strata,correct,base['penalties'],cached_identity=result['identity']);checks['changed_extraction_clock_cache_rejected']=False
        except ValueError as exc:checks['changed_extraction_clock_cache_rejected']=str(exc)
        wrong_clock=copy.deepcopy(fixture);wrong_clock['claims'][0]['column']='business_day'
        try:run_funding(brief,wrong_clock,pilot,feed,strata,correct,base['penalties']);checks['unsupported_source_clock_rejected']=False
        except ValueError as exc:checks['unsupported_source_clock_rejected']=str(exc)
    row={'dates':dates,'workers':args.workers,'rep':args.rep,'seconds':seconds,'rss_parent_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rss_child_max_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'maximum_reference_error':max(errors),'reference_errors':errors,'result':result,'treasury_consumer':treasury_report(result),'application_consumer':application_result(result,480000),'supported_change':treasury_report(changed_result),'checks':checks,
         'runtime':{k:importlib.metadata.version(k) for k in ['numpy','scipy','statsmodels','threadpoolctl']}}
    (outdir/f'{dates}-{args.workers}-{args.rep}.json').write_text(json.dumps(row,default=default,indent=2)+'\n')


if __name__=='__main__':main()
