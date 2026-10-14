"""Two-pass streamed Bartlett statistics with immutable, exactly-once inputs.

Only the sufficient-statistic passes stream here; the selected nuisance learner
may still materialize its fitting matrices. Execution stays on one host.
"""
import hashlib
import json
import os
from pathlib import Path
import numpy as np


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def atomic_json(path,value,fail=False):
    path=Path(path);temporary=path.with_suffix(path.suffix+'.partial')
    if 'identity' in value:
        checksum=hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()
        value=dict(value,checkpoint_sha256=checksum)
    with temporary.open('w') as stream:
        json.dump(value,stream,sort_keys=True,allow_nan=False);stream.flush();os.fsync(stream.fileno())
    if fail:raise InterruptedError('injected interruption before atomic checkpoint commit')
    os.replace(temporary,path)


def write_partitions(folder,scores,folds,chunk=257):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);scores=np.asarray(scores,float);folds=np.asarray(folds)
    if scores.ndim!=1 or folds.shape!=scores.shape or not np.all(np.isfinite(scores)) or chunk<1:
        raise ValueError('finite aligned scalar scores and folds required')
    rows=[];offset=0
    # Fold identity can reoccur only in one contiguous run; concatenating
    # disconnected windows would fabricate lag pairs.
    transitions=np.r_[True,folds[1:]!=folds[:-1]]
    if len(np.unique(folds))!=int(transitions.sum()):raise ValueError('fold windows must be contiguous')
    for fold in dict.fromkeys(folds.tolist()):
        values=scores[folds==fold]
        for start in range(0,len(values),chunk):
            name=f'part-{len(rows):05d}.npy';path=folder/name
            if path.exists():raise ValueError('refusing to overwrite immutable score partition')
            data=values[start:start+chunk];np.save(path,data,allow_pickle=False)
            rows.append(dict(id=len(rows),path=name,sha256=sha(path),count=len(data),fold=int(fold),origin_offset=offset))
            offset+=len(data)
    manifest=dict(schema_version=1,partitions=rows,count=len(scores));atomic_json(folder/'manifest.json',manifest)
    return folder/'manifest.json'


def stream_lrv(manifest_path,checkpoint,bandwidth,*,interrupt_after=None,partial_write=False,retry_duplicate=False):
    manifest_path=Path(manifest_path);manifest=json.loads(manifest_path.read_text());rows=manifest['partitions'];folder=manifest_path.parent
    if not isinstance(bandwidth,int) or not 0<=bandwidth<manifest['count'] or [r['id'] for r in rows]!=list(range(len(rows))):
        raise ValueError('invalid bandwidth or duplicate/reordered partition manifest')
    offset=0;lastfold=None;finished_folds=set()
    for row in rows:
        if row['origin_offset']!=offset or row['count']<=0:raise ValueError('overlapping or missing source contributions')
        offset+=row['count']
        if row['fold']!=lastfold:
            if row['fold'] in finished_folds:raise ValueError('disconnected windows cannot share a fold')
            finished_folds.add(row['fold']);lastfold=row['fold']
    if offset!=manifest['count']:raise ValueError('source count mismatch')
    identity=hashlib.sha256(manifest_path.read_bytes()+f'centered-bartlett-v1:{bandwidth}'.encode()).hexdigest()
    checkpoint=Path(checkpoint)
    if checkpoint.exists():
        state=json.loads(checkpoint.read_text())
        expected=state.pop('checkpoint_sha256',None)
        if expected!=hashlib.sha256(json.dumps(state,sort_keys=True,allow_nan=False).encode()).hexdigest():
            raise ValueError('checkpoint content checksum failed')
        if state['identity']!=identity:raise ValueError('checkpoint scientific inputs changed')
    else:state=dict(identity=identity,moment_done=[],lag_done=[],count=0,total=0.,products=[0.]*(bandwidth+1),halo=[],last_fold=None)
    reads=0;written=0;commits=0
    def read(row):
        nonlocal reads
        path=folder/row['path']
        if sha(path)!=row['sha256']:raise ValueError('immutable partition bytes changed')
        data=np.load(path,allow_pickle=False)
        if data.shape!=(row['count'],) or not np.all(np.isfinite(data)):raise ValueError('invalid score partition')
        reads+=path.stat().st_size*2
        return data
    def commit():
        nonlocal commits,written
        commits+=1
        fail=interrupt_after is not None and commits==interrupt_after
        atomic_json(checkpoint,state,fail=fail and partial_write);written+=checkpoint.stat().st_size
        if fail:raise InterruptedError('injected interruption after committed partition')
    attempt_rows=[r for row in rows for r in ([row,row] if retry_duplicate else [row])]
    for row in attempt_rows:
        data=read(row)
        if row['id'] in state['moment_done']:continue
        if row['id']!=len(state['moment_done']):raise ValueError('out-of-order moment contribution')
        state['total']+=float(data.sum());state['count']+=len(data);state['moment_done'].append(row['id']);commit()
    mean=state['total']/state['count']
    for row in attempt_rows:
        data=read(row)
        if row['id'] in state['lag_done']:continue
        if row['id']!=len(state['lag_done']):raise ValueError('out-of-order lag contribution')
        centered=data-mean;halo=np.array(state['halo']) if state['last_fold']==row['fold'] else np.array([])
        full=np.r_[halo,centered];start=len(halo)
        state['products'][0]+=float(centered@centered)
        for lag in range(1,bandwidth+1):
            first=max(0,lag-start)
            if first<len(centered):state['products'][lag]+=float(centered[first:]@full[start+first-lag:len(full)-lag])
        state['halo']=full[-bandwidth:].tolist() if bandwidth else [];state['last_fold']=row['fold'];state['lag_done'].append(row['id']);commit()
    covariance=(state['products'][0]+sum(2*(1-k/(bandwidth+1))*state['products'][k] for k in range(1,bandwidth+1)))/state['count']
    return dict(lrv=covariance,count=state['count'],identity=identity,mean=mean,bytes_read_including_hash_pass=reads,
                checkpoint_bytes_written=written,partitions=len(rows),maximum_halo=bandwidth,
                scope='Single-host streamed score covariance, global centering and same-fold chronological halos; exactly-once committed contributions')


def materialize_calendar_feed(source,target,nrows,ncontrols,*,horizon=0,cutoff=None,mode='stream'):
    """Materialize a sorted, clock-checked retrospective IV feed in bounded memory.

    Predecision features arrive before the decision; later realized outcomes
    belong to a fixed horizon and extraction cutoff. The learner can still copy
    the resulting memory map while fitting.
    """
    source,target=Path(source),Path(target)
    if target.exists() or mode not in ('stream','dense') or nrows<1 or ncontrols<1 or cutoff is None:
        raise ValueError('new target and explicit feed dimensions/cutoff required')
    original=sha(source);temporary=target.with_suffix('.partial.npy')
    array=np.lib.format.open_memmap(temporary,mode='w+',dtype='float64',shape=(nrows,ncontrols+3)) if mode=='stream' else np.empty((nrows,ncontrols+3))
    count=0
    with source.open() as records:
        for line in records:
            row=json.loads(line)
            if count>=nrows or row['origin']!=count:raise ValueError('missing, duplicate or reordered source origin')
            clock=[row[k] for k in ('feature_available_day','decision_day','outcome_day','outcome_received_day')]
            if not all(np.isfinite(clock)) or row['feature_available_day']>row['decision_day'] or row['outcome_day']!=row['decision_day']+horizon or not row['outcome_day']<=row['outcome_received_day']<=cutoff:
                raise ValueError('incompatible feature/outcome information clock')
            values=np.array(row['controls']+[row['outcome'],row['treatment'],row['instrument']],float)
            if values.shape!=(ncontrols+3,) or not np.all(np.isfinite(values)):raise ValueError('invalid source values')
            array[count]=values;count+=1
    if count!=nrows or sha(source)!=original:raise ValueError('incomplete or changed source during materialization')
    if mode=='stream':array.flush();del array
    else:np.save(temporary,array,allow_pickle=False)
    os.replace(temporary,target)
    return np.load(target,mmap_mode='r',allow_pickle=False),dict(source_sha256=original,materialized_sha256=sha(target),rows=count,mode=mode)
