"""Shared result semantics, streamed linked outcomes and local recovery."""
import hashlib
import json
from pathlib import Path
import os
import tempfile
import numpy as np
from .linked_funding import pseudo_rows, LINKED_DECLARATIONS
from .streaming_pilot import train_streaming_pilot
from .funding_calibration import pilot_data, LagAccumulator


RESULT_FIELDS=('status','set_topology','assumptions','currency','capability_disposition','estimate','interval')


def validate_result(result):
    if any(k not in result for k in RESULT_FIELDS): raise ValueError('common result contract missing '+','.join(RESULT_FIELDS))
    if result['status'] not in ('computed','refused','unavailable','error'): raise ValueError('invalid common result status')
    if result['set_topology'] not in ('finite_interval','finite_union','whole_line','empty','unavailable'): raise ValueError('invalid set topology')
    if not isinstance(result['assumptions'],list) or not result['currency']: raise ValueError('result assumptions/currency required')
    if result['capability_disposition'] not in ('qualified_in_declared_scope','conditional_progress','unresolved','external_pending'): raise ValueError('invalid capability disposition')
    return True


def streamed_pseudo_blocks(rows, audit, horizon, chunk_size=257, *, augmentation=True):
    rows=np.asarray(rows)
    if chunk_size<1: raise ValueError('positive chunk size required')
    for start in range(0,len(rows),chunk_size):
        yield pseudo_rows(rows[start:start+chunk_size], audit[0][start:start+chunk_size], audit[1][start:start+chunk_size], audit[2][start:start+chunk_size], horizon, augmentation=augmentation)


def fit_linked_stream(pilot_rows, rows, target, pilot_audit, audit, penalties, *, chunk_size=257, augmentation=True):
    pilot=pseudo_rows(pilot_rows,*pilot_audit,target.horizon,augmentation=augmentation); fit=train_streaming_pilot(pilot,penalties,chunk_size); coefficient=fit['coefficient'];n=len(rows);qsum=np.zeros(2);products=np.zeros(2)
    for block in streamed_pseudo_blocks(rows,audit,target.horizon,chunk_size,augmentation=augmentation):
        data=pilot_data(block); pred=data['x']@coefficient; v=data['action']-pred[:,0]; out=data['outcomes']-pred[:,1:];
        for s in (0,1):
            keep=data['stratum']==s;qsum[s]+=v[keep]@v[keep];products[s]+=v[keep]@(out[keep]@target.weights())
    if np.any(qsum<=0):return dict(status='unavailable_action_variation')
    slopes=products/qsum;acc=LagAccumulator(target.horizon);raw=0.
    for block in streamed_pseudo_blocks(rows,audit,target.horizon,chunk_size,augmentation=augmentation):
        data=pilot_data(block);pred=data['x']@coefficient;v=data['action']-pred[:,0];out=(data['outcomes']-pred[:,1:])@target.weights();score=np.empty(len(block))
        for s in (0,1):
            keep=data['stratum']==s;score[keep]=.5*n*v[keep]*(out[keep]-v[keep]*slopes[s])/qsum[s];raw+=float((.5*n*v[keep]*out[keep]/qsum[s])@( .5*n*v[keep]*out[keep]/qsum[s]))
        acc.add(score)
    variance=acc.variance_of_mean();value=float(.5*slopes.sum()-target.direct_cost());
    if not np.isfinite(variance) or variance<=0:return dict(status='unavailable_response_variance',estimate=value)
    se=float(np.sqrt(variance));return dict(status='computed_set',estimate=value,standard_error=se,interval=[value-1.96*se,value+1.96*se],calendar_variance=variance,streamed=True,pilot_dates=len(pilot_rows),evaluation_dates=len(rows),peak_pseudo_rows=chunk_size)


def recovery_trial(path, requests=40, fault_after=13):
    path=Path(path);path.mkdir(parents=True,exist_ok=True); journal=path/'journal.jsonl'; state={}
    def load():
        if journal.exists():
            for line in journal.read_text().splitlines():
                row=json.loads(line); state[row['key']]=row
    load();fault=False
    for i in range(requests):
        key=f'{i:04d}'
        if key in state:continue
        if i==fault_after and not (path/'fault.marker').exists():
            (path/'fault.marker').write_text('fault');fault=True;break
        payload={'key':key,'value':hashlib.sha256(key.encode()).hexdigest()}
        with journal.open('a') as stream:stream.write(json.dumps(payload)+'\n');stream.flush();os.fsync(stream.fileno())
        state[key]=payload
    if fault:
        load()
        for i in range(requests):
            key=f'{i:04d}'
            if key in state:continue
            payload={'key':key,'value':hashlib.sha256(key.encode()).hexdigest()}
            with journal.open('a') as stream:stream.write(json.dumps(payload)+'\n');stream.flush();os.fsync(stream.fileno())
            state[key]=payload
    rows=journal.read_text().splitlines(); keys=[json.loads(x)['key'] for x in rows]
    return dict(requests=requests,fault_after=fault_after,fault_injected=fault,rows=len(rows),unique_keys=len(set(keys)),complete=len(rows)==requests,atomic_publication=all(json.loads(x).get('value') for x in rows),duplicates=len(keys)-len(set(keys)))
