import hashlib,importlib,json,sys
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
import master_control as mc
ROOT=mc.ROOT;sys.path.insert(0,str(ROOT/'src'));P=ROOT/'docs/program/master/work/I01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b):
 if isinstance(a,dict):return set(a)==set(b) and all(close(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
 if isinstance(a,(float,int)) and not isinstance(a,bool):return np.isclose(a,b,rtol=1e-9,atol=1e-7)
 return a==b

def main():
 replay=[];bs=chr(92)
 for ident,folder in [('R01','R01'),('R02','R02'),('R03','R03'),('R04','R04-v3'),('R05','R05-v2')]:
  path=ROOT/'docs/program/master/work'/folder;spec=json.loads((path/'protocol.json').read_text());module=importlib.import_module(spec['module']);result=json.loads((path/'results.json').read_text())
  for cell,index in [(0,0),(len(spec['designs'])//2,256),(len(spec['designs'])-1,511)]:
   saved=json.loads((path/'requests'/f'{cell:02d}-{index:05d}.json').read_text())['result'];fresh=module.request(spec,cell,index)
   assert close(saved,fresh),(ident,cell,index)
   replay.append(dict(task=ident,cell=cell,index=index,status='reproduced'))
  rows=[bs+'begin{center}'+bs+'footnotesize'+bs+'begin{tabular}{lrrrrr}'+bs+'toprule','Scenario & Covers & MC lower & Finite & Median width & Challenger'+bs*2,bs+'midrule']
  for c in result['cells']:
   primary=c['methods'][spec['methods'][0]];challenger=c['methods'][spec['methods'][1]];name=c['design']['name'].replace('_',' ')
   median='--' if primary['width_quantiles'] is None else (f"{primary['width_quantiles'][1]:,.0f}" if ident in ['R01','R02','R03'] else f"{primary['width_quantiles'][1]:.3f}")
   rows.append(f"{name} & {primary['covered']}/512 & {primary['simultaneous_lower95']:.3f} & {primary['finite']}/512 & {median} & {challenger['covered']}/512 "+bs*2)
  rows.append(bs+'bottomrule'+bs+'end{tabular}'+bs+'end{center}')
  (ROOT/'docs/supplements'/f'master-{ident}-table.tex').write_text('\n'.join(rows)+'\n')
 sources=json.loads((ROOT/'docs/literature/sources.json').read_text());selected=[]
 for key,anchor,claim,limit in [('dml2018','Section 4.1 equation (4.4), Assumption 4.1(ii); Section 4.2 (4.8); extracted lines 1590-1720 reread','Orthogonal scores and nuisance product requirement','IID DML does not prove project dependent-calendar, sparse-rate or finite-grid results.'),('pearl2009','Corollary 1, equation (17), extracted lines 755-790 reread','Replacement of assignment mechanism in intervention factorization','Does not validate bank logger truth, latent structure or the new policy-value integration.')]:
  source=next(s for s in sources if s['id']==key);assert sha(ROOT/source['local_path'])==source['sha256']
  selected.append(dict(id=key,title=source['title'],version_date=source['version_status'],local_path=source['local_path'],sha256=source['sha256'],inspected_anchor=anchor,supported_claim=claim,limit=limit))
 audit=dict(status='pass',publication_cutoff='2026-10-07',scope='Reinspection of frozen primary texts. No comprehensive current literature update; limited external search returned no usable new source. New equations are project derivations, finite studies synthetic, independent acceptance absent.',sources=selected,corrections=['R05 first attempt rate/selection claims withdrawn for leakage, covariance and scenario defects.','R04 residual pooling claim withdrawn; true-candidate innovation union replaces it.','E01 first pass superseded by full streaming, strict sets, measurements and real crashes.','R03 independent reference checks are post-evaluation and timing is disclosed.'])
 mc.write(P/'source-audit.json',audit);mc.write(P/'request-reproduction.json',dict(status='pass',requests=replay,tolerance=dict(rtol=1e-9,atol=1e-7)))
 print(json.dumps(dict(status='pass',regenerated=len(replay),audited_primary_sources=len(selected))))
if __name__=='__main__':
 with threadpool_limits(limits=1):main()
