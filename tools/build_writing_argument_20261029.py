"""Build a separately named reader and aligned sponsor; retain every pass log."""
from pathlib import Path
import subprocess,time,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs';O=D/'writing-repair/2026-10-29'
NAMES={'full':'causal_banking_integrated_argument_2026-10-29','sponsor':'causal_banking_sponsor_integrated_2026-10-29'}
def build(kind):
 stem=NAMES[kind];folder=O/('build-'+kind);folder.mkdir(exist_ok=True)
 cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(folder),stem+'.tex']
 commands=[cmd]
 if kind=='full':commands.append(['bibtex',str((folder/stem).relative_to(D))])
 commands.extend([cmd,cmd]);results=[]
 for i,c in enumerate(commands,1):
  log=folder/f'pass-{i}.txt';start=time.monotonic()
  with log.open('w') as f:p=subprocess.run(c,cwd=D,stdout=f,stderr=subprocess.STDOUT,timeout=300)
  row={'pass':i,'returncode':p.returncode,'seconds':round(time.monotonic()-start,2),'log':str(log.relative_to(R))};results.append(row);print(json.dumps(row),flush=True)
  (O/('build-'+kind+'.json')).write_text(json.dumps(results,indent=2)+'\n')
  if p.returncode:print('\n'.join(log.read_text(errors='replace').splitlines()[-30:]));raise SystemExit(p.returncode)
 target=D/(stem+'.pdf');target.write_bytes((folder/(stem+'.pdf')).read_bytes());print(json.dumps({'pdf':str(target.relative_to(R)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}),flush=True)
if __name__=='__main__':
 import sys
 for kind in sys.argv[1:] or ['full','sponsor']:build(kind)
