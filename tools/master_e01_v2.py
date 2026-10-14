import argparse,json,os,resource,subprocess,sys,tempfile,time,hashlib
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from causalbank.linked_funding import simulate_linked,fit_linked_funding,LINKED_DECLARATIONS
from causalbank.dynamic_funding import FundingTarget
from causalbank.engineering_v2 import fit,envelope,recover
from master_experiment import atomic
FOLDER=ROOT/'docs/program/master/work/E01-v2'
base=json.loads((ROOT/'docs/studies/dynamic-funding-spec.json').read_text());obs=json.loads((ROOT/'docs/studies/dynamic-observation-spec.json').read_text());target=FundingTarget(horizon=base['horizon'],branches=base['branches'])

def data(n,seed=9120,q=.25,p=.5,rho=.82):
 b=dict(base,rho=rho);o=dict(obs,correct_pair_probability=[p,p])
 pilot,pa=simulate_linked(b,o,n*4,[seed,0],[seed,1],inclusion=q);rows,a=simulate_linked(b,o,n,[seed,2],[seed,3],inclusion=q)
 return pilot,rows,pa,a

def calculate(d,stream,size=257):
 p,r,pa,a=d
 if stream:return fit(p,r,target,pa,a,base['penalties'],chunk_size=size,declarations=LINKED_DECLARATIONS)
 return fit_linked_funding(p,r,target,pa,a,base['penalties'],chunk_size=size,declarations=LINKED_DECLARATIONS)

def crash_request(i,fail):
 d=data(40,91200+i)
 if fail:
  # Abrupt process death while a real streamed pilot factorization is in progress.
  import causalbank.engineering_v2 as engine
  original=engine.factor
  def interrupted(iterator):
   next(iterator);os._exit(72)
  engine.factor=interrupted
 return calculate(d,True,17)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workload',type=int);ap.add_argument('--mode');ap.add_argument('--recovery');ap.add_argument('--fault');ap.add_argument('--changed',action='store_true');args=ap.parse_args()
 if args.workload:
  start=time.perf_counter();d=data(args.workload);generated=time.perf_counter();out=calculate(d,args.mode=='stream');fitted=time.perf_counter();blob=json.dumps(out,allow_nan=False);ended=time.perf_counter()
  print(json.dumps(dict(mode=args.mode,origins=args.workload,pilot_origins=4*args.workload,generation_seconds=generated-start,fit_seconds=fitted-generated,serialization_seconds=ended-fitted,total_seconds=ended-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,serialized_bytes=len(blob.encode()),estimate=out.get('estimate'),standard_error=out.get('standard_error'),status=out['status'])))
  return
 if args.recovery:
  dependencies=['tools/master_e01_v2.py','src/causalbank/engineering_v2.py','src/causalbank/linked_funding.py','src/causalbank/streaming_pilot.py','src/causalbank/funding_calibration.py','src/causalbank/dynamic_funding.py','docs/studies/dynamic-funding-spec.json','docs/studies/dynamic-observation-spec.json']
  identity=dict(input_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in dependencies},seed=91200+int(args.changed),count=12)
  print(json.dumps(recover(args.recovery,identity,crash_request,fault=args.fault)));return
 cases=[]
 for n,q,p,rho in [(40,.25,.5,.82),(240,.1,.515,.82),(240,.25,.5,.96),(1200,.25,.9,.82)]:
  d=data(n,q=q,p=p,rho=rho)
  for size in [1,37,257]:
   dense=calculate(d,False,size);stream=calculate(d,True,size);assert dense['status']==stream['status']
   if 'estimate' in dense:
    assert np.allclose(dense['interval'],stream['interval'],rtol=1e-9,atol=1e-6)
    assert dense['pilot_penalty']==stream['pilot_penalty']
   cases.append(dict(n=n,q=q,p=p,rho=rho,chunk=size,status=stream['status'],estimate_error=abs(dense.get('estimate',0)-stream.get('estimate',0)),se_error=abs(dense.get('standard_error',0)-stream.get('standard_error',0))))
 d=data(40);p,r,pa,a=d;none=(np.zeros(40,dtype=int),np.full(40,np.nan),a[2]);assert calculate((p,r,pa,none),False)['status']==calculate((p,r,pa,none),True)['status']=='unavailable_outcome_audit'
 fixtures=[]
 for journey,pieces,status,disposition in [('A',[{'lower':1.,'upper':2.}],'computed_set','conditional_progress'),('B',[{'lower':None,'upper':-2.},{'lower':3.,'upper':None}],'computed_set','unresolved'),('C',[{'lower':None,'upper':None}],'computed_set','unresolved'),('D',None,'unavailable_audit','external_pending')]:
  raw=dict(status=status)
  if pieces is not None:raw['effect_set']=pieces
  fixtures.append(envelope(journey,raw,'USD' if journey in 'AB' else 'outcome per action' if journey=='C' else 'identity probability',['Supplied information must be true'],disposition))
 for bad in [dict(status='computed_set'),dict(status='computed_set',effect_set=[{'lower':3.,'upper':2.}])]:
  try:envelope('A',bad,'USD',['true'],'unresolved');raise AssertionError('invalid contract accepted')
  except ValueError:pass
 atomic(FOLDER/'checks.json',dict(status='pass',tolerance=dict(rtol=1e-9,atol_currency=1e-6),cases=cases,no_audit_refusal=True,consumer_fixtures=fixtures,malformed_results_rejected=True))
 workloads=[]
 for n in [240,12000,120000]:
  for mode in ['dense','stream']:
   completed=subprocess.run([sys.executable,__file__,'--workload',str(n),'--mode',mode],capture_output=True,text=True,check=True,timeout=120)
   workloads.append(json.loads(completed.stdout))
 atomic(FOLDER/'workloads.json',dict(status='measured',rows=workloads,scope='Separate single-thread CPU processes; data generation, tuning/refit, inference, serialization and whole-process peak RSS. No bank platform claim.'))
 recovery=[]
 for fault in ['fit','checkpoint','publication']:
  with tempfile.TemporaryDirectory(prefix='causal-e01-v2-') as td:
   initial=subprocess.run([sys.executable,__file__,'--recovery',td,'--fault',fault],capture_output=True,text=True,timeout=60)
   assert initial.returncode=={'fit':72,'checkpoint':73,'publication':74}[fault]
   assert not (Path(td)/'manifest.json').exists()
   done=subprocess.run([sys.executable,__file__,'--recovery',td],capture_output=True,text=True,check=True,timeout=60);manifest=json.loads(done.stdout)
   replay=subprocess.run([sys.executable,__file__,'--recovery',td],capture_output=True,text=True,check=True,timeout=60);assert json.loads(replay.stdout)==manifest
   tamper=subprocess.run([sys.executable,__file__,'--recovery',td,'--changed'],capture_output=True,text=True,timeout=60);assert tamper.returncode!=0 and 'Immutable request inputs changed' in tamper.stderr
   recovery.append(dict(fault=fault,actual_exit=initial.returncode,no_premature_manifest=True,recovered_requests=manifest['count'],idempotent_replay=True,changed_inputs_rejected=True,manifest=manifest))
 atomic(FOLDER/'recovery.json',dict(status='pass',trials=recovery,scope='Actual abrupt local subprocess exits, partial checkpoint rejection, atomic publication and idempotent recovery; no multi-host service guarantee.'))
 print(json.dumps(dict(status='pass',equivalence_cases=len(cases),workloads=len(workloads),faults=len(recovery))))

if __name__=='__main__':
 with threadpool_limits(limits=1):main()
