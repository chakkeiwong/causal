"""Complete linked pseudo-outcome streaming and atomic local request semantics."""
import fcntl,hashlib,json,os
from pathlib import Path
import numpy as np
from scipy.stats import norm
from .linked_funding import pseudo_rows,LINKED_DECLARATIONS
from .funding_calibration import pilot_data,LagAccumulator
from .streaming_pilot import _ridge
from .linkage_sets import encode_set,decode_set

def blocks(rows,audit,horizon,size,start=0,end=None):
    end=len(rows) if end is None else end
    for j in range(start,end,size):
        k=min(j+size,end)
        yield pseudo_rows(rows[j:k],*[a[j:k] for a in audit],horizon)

def factor(iterator):
    reduced=None;count=0;mean=None;centered=None
    for block in iterator:
        d=pilot_data(block);y=np.column_stack((d['action'],d['outcomes']));aug=np.column_stack((d['x'],y))
        reduced=np.linalg.qr(aug if reduced is None else np.vstack((reduced,aug)),mode='r')
        bm=y.mean(0);bc=np.sum((y-bm)**2,0)
        if not count:mean,centered=bm,bc
        else:
            difference=bm-mean;centered+=bc+difference**2*count*len(y)/(count+len(y));mean+=difference*len(y)/(count+len(y))
        count+=len(y)
    if reduced is None or count<7 or np.linalg.matrix_rank(reduced[:,:6])!=6:raise ValueError('Pilot rank unavailable')
    return reduced,centered/count

def fit(pilot,rows,target,pa,audit,penalties,chunk_size=257,alpha=.05,declarations=None):
    target.validate()
    if declarations!=LINKED_DECLARATIONS:raise ValueError('Explicit scientific declarations required')
    if len(pilot)<4*len(rows) or len(rows)<=2*(target.horizon+2) or not isinstance(chunk_size,int) or isinstance(chunk_size,bool) or chunk_size<1 or not 0<alpha<1:raise ValueError('Invalid pilot ratio/calendar/chunk/confidence')
    if not penalties or any(not np.isfinite(p) or p<0 for p in penalties):raise ValueError('Invalid penalty grid')
    # Bounded validation precedes scientific refusals, matching the inherited route.
    for source,info in [(pilot,pa),(rows,audit)]:
        for block in blocks(source,info,target.horizon,chunk_size):pass
    for source,info in [(pilot,pa),(rows,audit)]:
        for s in [0,1]:
            if np.sum((source[:,0]==s)&np.asarray(info[0],bool))<2:return dict(status='unavailable_outcome_audit')
    split=len(pilot)//2
    training,scale=factor(blocks(pilot,pa,target.horizon,chunk_size,0,split));validation,_=factor(blocks(pilot,pa,target.horizon,chunk_size,split))
    if np.any(scale<=0):raise ValueError('Pilot target variance unavailable')
    losses=[]
    for penalty in penalties:
        c=_ridge(training,penalty);res=validation[:,6:]-validation[:,:6]@c;losses.append(float(np.sum(res**2/scale)/((len(pilot)-split)*len(scale))))
    selected=int(np.argmin(losses));coefficient=_ridge(np.linalg.qr(np.vstack((training,validation)),mode='r'),penalties[selected])
    n=len(rows);qsum=np.zeros(2);products=np.zeros(2);weights=target.weights()
    for block in blocks(rows,audit,target.horizon,chunk_size):
        d=pilot_data(block);pred=d['x']@coefficient;v=d['action']-pred[:,0];u=(d['outcomes']-pred[:,1:])@weights
        for s in [0,1]:
            k=d['stratum']==s;qsum[s]+=v[k]@v[k];products[s]+=v[k]@u[k]
    if not np.isfinite(qsum).all() or np.any(qsum<=0):return dict(status='unavailable_action_variation')
    slopes=products/qsum;acc=LagAccumulator(target.horizon);energy=0.
    for block in blocks(rows,audit,target.horizon,chunk_size):
        d=pilot_data(block);pred=d['x']@coefficient;v=d['action']-pred[:,0];u=(d['outcomes']-pred[:,1:])@weights;scores=np.empty(len(v))
        for s in [0,1]:
            k=d['stratum']==s;scores[k]=.5*n*v[k]*(u[k]-v[k]*slopes[s])/qsum[s];raw=.5*n*v[k]*u[k]/qsum[s];energy+=raw@raw
        acc.add(scores)
    value=float(.5*slopes.sum()-target.direct_cost());variance=acc.variance_of_mean();floor=(8*np.finfo(float).eps)**2*energy/n**2
    if not np.isfinite(variance) or variance<=max(0.,floor):return dict(status='unavailable_response_variance',estimate=value)
    se=float(np.sqrt(variance));z=norm.ppf(1-alpha/2);bounds=[float(value-z*se),float(value+z*se)]
    return dict(status='computed_set',estimate=value,standard_error=se,financial_set=encode_set([bounds]),interval=bounds,calendar_variance=variance,pilot_penalty=float(penalties[selected]),pilot_validation_losses=losses,peak_pseudo_rows=min(chunk_size,max(len(pilot),n)),pilot_dates=len(pilot),evaluation_dates=n,scope='Same independent-origin conditional linked procedure; engineering equivalence does not improve calibration.')

def envelope(journey,result,units,assumptions,disposition):
    if journey not in 'ABCD' or disposition not in ['conditional_progress','unresolved','external_pending','qualified_in_declared_scope'] or not units or not assumptions:raise ValueError('Journey/units/assumptions/disposition required')
    encoded=result.get('effect_set',result.get('financial_set'))
    if encoded is None and 'interval' in result:encoded=encode_set([result['interval']])
    if encoded is None:topology='unavailable'
    else:
        pieces=decode_set(encoded)
        for i,(a,b) in enumerate(pieces):
            if np.isnan([a,b]).any() or a>b or (i and a<=pieces[i-1][1]):raise ValueError('Invalid or overlapping set pieces')
        if not pieces:topology='empty'
        elif pieces==[(-np.inf,np.inf)]:topology='whole_line'
        elif len(pieces)>1:topology='disconnected'
        elif not np.isfinite(pieces).all():topology='unbounded'
        else:topology='finite_interval'
    if result.get('status','').startswith('computed') and encoded is None:raise ValueError('Computed set requires actual bounds')
    row=dict(version=2,journey=journey,status=result['status'],topology=topology,set=encoded,units=units,assumptions=assumptions,capability_disposition=disposition,scientific_result=result)
    json.dumps(row,allow_nan=False)
    return row

def atomic(path,value,fault=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.pending')
    with tmp.open('w') as f:
        data=json.dumps(value,sort_keys=True,allow_nan=False)
        if fault=='checkpoint':
            f.write(data[:len(data)//2]);f.flush();os.fsync(f.fileno());os._exit(73)
        f.write(data);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path);fd=os.open(path.parent,os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def recover(folder,identity,request,count=12,fault=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    with (folder/'lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        meta=folder/'identity.json'
        if meta.exists():
            if json.loads(meta.read_text())!=identity:raise ValueError('Immutable request inputs changed')
        else:atomic(meta,identity)
        results=[]
        for i in range(count):
            path=folder/f'{i:04d}.json'
            if path.exists():
                row=json.loads(path.read_text())
                if row['id']!=i or row['identity']!=identity:raise ValueError('Request identity mismatch')
            else:
                row=dict(id=i,identity=identity,result=request(i, fault=='fit' and i==3))
                atomic(path,row,'checkpoint' if fault=='checkpoint' and i==3 else None)
            results.append(row)
        if fault=='publication':os._exit(74)
        manifest=dict(identity=identity,request_sha256={f'{i:04d}.json':hashlib.sha256((folder/f'{i:04d}.json').read_bytes()).hexdigest() for i in range(count)},count=count)
        atomic(folder/'manifest.json',manifest)
        return manifest
