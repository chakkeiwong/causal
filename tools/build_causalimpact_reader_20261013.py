#!/usr/bin/env python3
"""Build a preserving successor of the frozen working monograph with CausalImpact review."""
import contextlib,json,os,re,subprocess
from pathlib import Path
import build_integrated_monograph_v12 as shared
import master_control as core
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import verify_bindings,write

ROOT=core.ROOT; BASE=ROOT/'docs/program/execution/2026-10-13/causalimpact-reuse'; OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_commercial_iv_rd_2026-10-13.tex'; NAME='causal_proposal_causalimpact_2026-10-13'
DRIVER=ROOT/'docs'/(NAME+'.tex'); PDF=DRIVER.with_suffix('.pdf'); PRIOR=ROOT/'docs/program/execution/2026-10-13/commercial-iv-rd/reader/source-audit.json'; ref=shared.ref

def prepare():
 for f in ['source-audit.json','manuscript-review.json','decision-proposal.json','adapter-contract.json']: verify_bindings(json.loads((BASE/f).read_text()))
 text=OLD.read_text(); marker=r'\input{program/execution/2026-10-13/commercial-iv-rd/dependent-feasibility.tex}'; assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-13/causalimpact-reuse/decision.tex}',1)
 marker='program/execution/2026-10-13/commercial-iv-rd/refs}'; assert text.count(marker)==1
 text=text.replace(marker,'program/execution/2026-10-13/commercial-iv-rd/refs,program/execution/2026-10-13/causalimpact-reuse/refs}',1)
 if DRIVER.exists(): assert DRIVER.read_text()==text
 else: DRIVER.write_text(text)
 write(BASE/'prepared-inputs-v4.json',{'inputs':[ref(OLD,'Frozen predecessor'),ref(PRIOR,'Predecessor source audit'),ref(BASE/'source-audit.json','New audit'),ref(BASE/'decision.tex','New manuscript'),ref(Path(__file__),'Builder')],'generated':[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New bibliography')]})
 print(json.dumps({'driver':str(DRIVER.relative_to(ROOT))}))

def build():
 assert not PDF.exists(); OUT.mkdir(exist_ok=True)
 env=dict(os.environ);env['TEXINPUTS']=str(ROOT/'docs')+'//:'+env.get('TEXINPUTS','');env['BIBINPUTS']=str(ROOT/'docs')+'//:'+env.get('BIBINPUTS','')
 cmd=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(OUT),str(DRIVER)]
 with (OUT/'compile.log').open('w') as f:
  p=subprocess.run(cmd,cwd=ROOT/'docs',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=55)
  if p.returncode: raise RuntimeError('pdflatex failed; inspect compile.log')
 subprocess.run(['bibtex',str((OUT/NAME).relative_to(ROOT/'docs'))],cwd=ROOT/'docs',env=env,stdout=(OUT/'bibtex.log').open('w'),stderr=subprocess.STDOUT,timeout=30,check=True)
 for i in range(3):
  subprocess.run(cmd,cwd=ROOT/'docs',env=env,stdout=(OUT/f'compile-rerun-{i}.log').open('w'),stderr=subprocess.STDOUT,timeout=55,check=True)
 files=shared.scan(DRIVER); joined='\n'.join(x for _,x in files); labels=re.findall(shared.LABEL,joined); assert len(labels)==len(set(labels))
 audit=json.loads((BASE/'source-audit.json').read_text()); prior=json.loads(PRIOR.read_text()); entries={s['integrated_citation_key']:s for s in prior['sources']}
 for s in audit['sources']: entries[s['integrated_citation_key']]=s
 cited={x.strip() for g in re.findall(shared.CITE,joined) for x in g.split(',')}; assert cited<=entries.keys(),sorted(cited-set(entries))
 PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes());subprocess.run(['pdftotext','-layout',str(PDF),str(OUT/'reader.txt')],check=True,timeout=25)
 info=subprocess.check_output(['pdfinfo',str(PDF)],text=True);pages=int(re.search(r'(?m)^Pages:\s+(\d+)',info).group(1)); text=re.sub(r'\s+',' ',(OUT/'reader.txt').read_text())
 for phrase in ['Bayesian intervention analysis for branch campaigns','same twelve observed rows','joint posterior predictive','integration capability'] : assert phrase in text,phrase
 merged={'sources':[entries[k] for k in sorted(cited)],'tex_files':[ref(p,'Compiled source') for p,_ in files],'source_audits':[ref(PRIOR,'Predecessor audit'),ref(BASE/'source-audit.json','New audit')],'added_bibliography':ref(BASE/'refs.bib','CausalImpact bibliography'),'cutoff':'2026-10-07','visual_acceptance':False};verify_bindings(merged);write(OUT/'source-audit.json',merged)
 report={'status':'compiled_source_and_text_checked_working_draft','pages':pages,'pdf':ref(PDF,'Preserving CausalImpact reader'),'driver':ref(DRIVER,'Preserving driver'),'source_audit':ref(OUT/'source-audit.json','Whole-reader audit'),'predecessor_pdf':ref(OLD.with_suffix('.pdf'),'642-page predecessor'),'cited_records':len(cited),'warnings':[line for line in (OUT/'compile-rerun-2.log').read_text().splitlines() if 'Overfull' in line or 'undefined' in line.lower()],'final_acceptance':False,'mandatory_repairs_closed':[],'visual_acceptance':False}
 write(OUT/'build-report.json',report); layout.OUT=OUT; layout.main(); print(json.dumps({'pages':pages,'cited_records':len(cited)}))

if __name__=='__main__':
 import argparse;p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();prepare() if a.command=='prepare' else build()
