#!/usr/bin/env python3
"""Preserve the working monograph and integrate the commercial contract review."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_commercial_identification_choice_20261014 as work
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=work.ROOT
BASE=work.BASE/'publication'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_agent_backends_v2_2026-10-14.tex'
PRIOR=work.AUDIT
NAME='causal_proposal_commercial_contracts_2026-10-14'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')

def prepare():
 assert not DRIVER.exists()and not(BASE/'prepared-inputs.json').exists()
 audit=json.loads((work.BASE/'source-audit.json').read_text())
 verify_bindings(audit);verify_bindings(json.loads((work.BASE/'author-review.json').read_text()))
 BASE.mkdir(exist_ok=True)
 development=(work.BASE/'development.tex').read_text()
 for phrase in ['before proposing another broad implementation.',
                'matching source rather than borrow a conclusion from another software area.']:
  assert development.count(phrase)==1
  development=development.replace(phrase,phrase+' '+chr(92)+'citep{exec14_ci_comparison}')
 (BASE/'development.tex').write_text(development)
 audit['sources'].append({'integrated_citation_key':'exec14_ci_comparison','kind':'project_analysis',
  'title':'Commercial identification scope and canonical-service comparison','author':'Causal banking proposal','year':2026,
  'source_identity':'Recorded sixteen-family proposal comparison','version_date':'2026-10-14',
  'local_copy':ref(work.OUTPUT,'Four scoped commercial comparisons and twelve unresolved/adjacent families'),
  'inspected_anchors':['vendors: observed current, proposed, gap, deployment, price; unresolved families'],
  'supported_claims':['Canonical service is narrower than documented vendor functions; coverage and rights unknowns remain explicit.'],
  'records':[ref(ROOT/'src/causalbank/operation_service_v12.py','SUPPORTED and dispatch; local reference scope'),
             ref(work.BASE/'primary-review.json','Fourteen inherited original records and nine new official originals')]})
 write(BASE/'source-audit.json',audit)
 bib=[]
 for s in audit['sources']:
  bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+
   '}},\n title={'+engine.shared.escape(s['title'])+'},\n year={2026},\n note={'+
   engine.shared.escape(s['version_date'])+'}\n}\n')
 (BASE/'refs.bib').write_text('\n'.join(bib))
 text=OLD.read_text();marker=r'input{program/execution/2026-10-13/commercial-identification/comparison-final.tex}'
 assert text.count(marker)==1
 text=text.replace(marker,marker+'\n'+r'input{program/execution/2026-10-14/commercial-identification-comparison/publication/development.tex}')
 pattern=re.compile(r'\\bibliography\{([^}]+)\}')
 assert len(pattern.findall(text))==1
 text=pattern.sub(lambda m:chr(92)+'bibliography{'+m.group(1)+',program/execution/2026-10-14/commercial-identification-comparison/publication/refs}',text)
 DRIVER.write_text(text)
 write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved or reviewed input')for p in
  [OLD,PRIOR,work.BASE/'development.tex',work.BASE/'source-audit.json',work.BASE/'author-review.json',Path(__file__).resolve()]],
  'generated':[ref(p,'Successor input')for p in[DRIVER,BASE/'source-audit.json',BASE/'refs.bib',BASE/'development.tex']],
  'credit_policy':'No automatic substantive-page or mandatory-repair completion credit.',
  'visual_acceptance':False})
 print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'added_records':len(audit['sources'])}))

def build():
 for name,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():
  setattr(engine,name,value)
 with(BASE/'compile-summary.log').open('x')as stream:
  with redirect_stdout(stream):engine.build()
 report=json.loads((OUT/'build-report.json').read_text())
 aux=(OUT/(NAME+'.aux')).read_text()
 def page(label):
  token=chr(92)+'newlabel{'+label+'}{{'
  line=next(l for l in aux.splitlines()if l.startswith(token))
  return int(line.split('}{')[2])
 report.update(builder=ref(Path(__file__).resolve(),'Preserving commercial comparison builder'),
  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen730-page reader'),
  commercial_sections={label:page('exec14:'+label)for label in ['commercial-contracts','commercial-contracts-end']})
 engine.core.write(OUT/'build-report.json',report)
 result=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',result)
 assert result['status']=='pass'and not result['issues']
 print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],
  'sections':report['commercial_sections'],'scholarly_pdfs':result['scholarly_pdfs'],
  'material_warnings':[w for w in report['warnings']if 'Underfull'not in w]}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
 {'prepare':prepare,'build':build}[a.command]()
