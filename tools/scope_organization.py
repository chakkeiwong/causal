#!/usr/bin/env python3
"""Generated observation hypotheses and independent audit uncertainty."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd
from scipy.special import expit
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.observation_search import propose,projection,resolve,next_question


def effect(view,a,y):
    x=np.array([r['value'] for r in view],float)
    if not np.isfinite(x).all():return None
    return float(np.linalg.lstsq(np.column_stack((np.ones(len(x)),a,x)),y,rcond=None)[0][1])


def fixture(rng,n,case):
    x,w=rng.normal(size=(2,n));a=rng.binomial(1,expit(.7*x));y=20*a+30*x+rng.normal(scale=5,size=n)
    base=pd.Timestamp('2024-01-01');rows=[];decisions=[]
    for i in range(n):
        entity='account_'+str(i);decisions.append({'id':str(i),'entity':entity,'at':base+pd.Timedelta(days=10),'begin':base})
        if case=='third_key_required':
            for j in range(8):
                rows.append({'entity':entity,'record':str(j%2),'key_b':str((j//2)%2),'key_c':str(j//4),'version':1,'event':base+pd.Timedelta(days=2),'available':base+pd.Timedelta(days=3),'value':float(x[i]/8)})
            continue
        first=x[i]-w[i] if case=='renamed_flow' else x[i]
        for record,version,event,available,value in [('recent',1,5,6,first),('recent',2,5,12,first+2*a[i]),('earlier',1,2,3,w[i])]:
            row={'entity':entity,'record':record,'version':version,'event':base+pd.Timedelta(days=event),'available':base+pd.Timedelta(days=available),'value':float(value)}
            if case=='ambiguous_value':row['second_value']=float(value+3*a[i])
            rows.append(row)
    frame=pd.DataFrame(rows);frame['_row_id']=['raw_'+str(i) for i in range(len(frame))]
    names={c:'f_'+str(j) for c,j in zip([c for c in frame if c!='_row_id'],rng.permutation(len(frame.columns)-1))}
    frame=frame.rename(columns=names).sample(frac=1,random_state=int(rng.integers(2**30))).reset_index(drop=True)
    frame=frame[list(rng.permutation(frame.columns))]
    oracle={'entity':names['entity'],'key':[names['record']],'version':names['version'],'event':names['event'],'available':names['available'],'value':names['value'],'revision':'latest','aggregation':'flow' if case=='renamed_flow' else 'stock'}
    return frame,decisions,oracle,a,y


def main():
    path=ROOT/'docs/studies/scope-organization-spec.json';spec=json.loads(path.read_text());results=[];start=time.perf_counter()
    for j,case in enumerate(spec['cases']):
        runs=[]
        for rep in range(spec['repetitions']):
            frame,decisions,oracle,a,y=fixture(np.random.default_rng(np.random.SeedSequence([spec['seed'],j,rep])),spec['entities'],case)
            out=propose(frame,decisions,realized_event_feed=True);survivors=out['survivors'];questions=[]
            oracle_view=None if case=='third_key_required' else projection(frame,decisions,oracle)
            retained=any(s['view']==oracle_view and s['plan']['aggregation']==oracle['aggregation'] and s['plan']['value']==oracle['value'] for s in survivors)
            estimates=[effect(s['view'],a,y) for s in survivors]
            initial_range=float(np.ptp(estimates)) if estimates and all(v is not None for v in estimates) else None
            while survivors and len({s['signature'] for s in survivors})>1 and len(questions)<8:
                vals=[effect(s['view'],a,y) for s in survivors]
                question=next_question(survivors,vals if all(v is not None for v in vals) else None)
                if question is None:break
                questions.append(question);survivors=resolve(survivors,{question['field']:oracle[question['field']]})
            accepted=bool(survivors) and len({s['signature'] for s in survivors})==1
            runs.append({'initial_status':out['status'],'generated':out['generated'],'survivors':len(out['survivors']),
                'oracle_retained':retained,'questions':questions,'resolved':accepted,'wrong_acceptance':accepted and survivors[0]['view']!=oracle_view,
                'initial_effect_range':initial_range,'resolved_effect':effect(survivors[0]['view'],a,y) if accepted else None})
        row={'case':case,'runs':runs,'oracle_retention':float(np.mean([r['oracle_retained'] for r in runs])),
            'resolved_fraction':float(np.mean([r['resolved'] for r in runs])),'wrong_acceptance':float(np.mean([r['wrong_acceptance'] for r in runs])),
            'mean_questions':float(np.mean([len(r['questions']) for r in runs])),'initial_statuses':{s:sum(r['initial_status']==s for r in runs) for s in set(r['initial_status'] for r in runs)}}
        results.append(row);print(json.dumps({k:v for k,v in row.items() if k!='runs'}),flush=True)
    linkage=spec['linkage'];metrics={k:[] for k in ['naive','corrected_joint','corrected_fixed_audit','biased_audit']};estimates={k:[] for k in metrics}
    for rep in range(linkage['repetitions']):
        rng=np.random.default_rng(np.random.SeedSequence([spec['seed'],7,rep]));n=linkage['rows'];m=linkage['audit_rows'];alpha=linkage['mismatch_probability'];tau=linkage['effect']
        a=rng.binomial(1,.5,n);original=tau*a+rng.normal(size=n);replacement=tau*rng.binomial(1,.5,n)+rng.normal(size=n)
        mismatch=rng.binomial(1,alpha,n);observed=np.where(mismatch,replacement,original)
        # Known randomized assignment makes the replacement attenuation transparent.
        scores=2*(2*a-1)*observed;num=float(scores.mean());var=float(scores.var(ddof=0)/n)
        ahat=float(rng.binomial(1,alpha,m).mean());bad=float(rng.binomial(1,.05,m).mean());den=1-ahat
        corrected=num/den;joint=var/den**2+num**2*ahat*(1-ahat)/(m*den**4)
        values={'naive':(num,var),'corrected_joint':(corrected,joint),'corrected_fixed_audit':(corrected,var/den**2),
            'biased_audit':(num/(1-bad),var/(1-bad)**2+num**2*bad*(1-bad)/(m*(1-bad)**4))}
        for key,(point,variance) in values.items():metrics[key].append(abs(point-tau)<=1.959963984540054*np.sqrt(variance));estimates[key].append(point)
    link_result={k:{'coverage':float(np.mean(v)),'bias':float(np.mean(estimates[k])-linkage['effect'])} for k,v in metrics.items()};print(json.dumps({'linkage':link_result}),flush=True)
    files=[path,Path(__file__),ROOT/'src/causalbank/observation_search.py']
    receipt={'spec':spec,'results':results,'linkage':link_result,'seconds':time.perf_counter()-start,
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'scope':'Generated finite schema hypotheses, oracle-answered questions and a separate independent-mismatch audit model; no universal semantic recovery or match calibration.'}
    (ROOT/'docs/studies/scope-organization-results.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
