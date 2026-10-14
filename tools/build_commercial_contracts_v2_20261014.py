#!/usr/bin/env python3
"""Repair a lost TeX input delimiter in a preserving unpublished successor."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_commercial_contracts_reader_20261014 as prior
import build_native_evaluation_reader_v3_20261014 as engine
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=prior.ROOT
BASE=prior.work.BASE/'v2'
OUT=BASE/'reader'
OLD=prior.OLD
PRIOR=prior.PRIOR
NAME='causal_proposal_commercial_contracts_v2_2026-10-14'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
BS=chr(92)

def prepare():
 assert not DRIVER.exists()and not(BASE/'prepared-inputs.json').exists()
 BASE.mkdir(exist_ok=True)
 old=prior.DRIVER.read_text()
 bad='input{program/execution/2026-10-14/commercial-identification-comparison/publication/development.tex}'
 assert old.count(bad)==1 and BS+bad not in old
 report=json.loads((prior.OUT/'build-report.json').read_text())
 assert report['pages']==730 and report['cited_records']==538
 assert 'Abduction must preserve'not in(prior.OUT/'reader.txt').read_text()
 audit=json.loads((prior.BASE/'source-audit.json').read_text());verify_bindings(audit)
 write(BASE/'source-audit.json',audit)
 for fn in ['development.tex','refs.bib']:(BASE/fn).write_bytes((prior.BASE/fn).read_bytes())
 marker=BS+'input{program/execution/2026-10-13/commercial-identification/comparison-final.tex}'
 text=OLD.read_text();assert text.count(marker)==1
 new=BS+'input{program/execution/2026-10-14/commercial-identification-comparison/v2/development.tex}'
 text=text.replace(marker,marker+'\n'+new)
 pattern=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'))
 assert len(pattern.findall(text))==1
 text=pattern.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-14/commercial-identification-comparison/v2/refs}',text)
 DRIVER.write_text(text)
 assert text.count(new)==1
 write(BASE/'repair-review.json',{'status':'reviewed_repair','failure':'Transport omitted the backslash in the newly inserted TeX input directive.',
  'observed_result':'Compiled730 pages with538 old citations and no new chapter labels. Post-build label assertion stopped publication.',
  'repair':'Use explicit chr(92) delimiters and assert exact input, chapter labels, new citations and extracted prose.',
  'preserved_failed_attempt':[ref(p,'Unpublished failed build artifact')for p in[prior.DRIVER,prior.PDF,prior.OUT/'build-report.json',prior.OUT/'reader.txt',ROOT/'tools/build_commercial_contracts_reader_20261014.py']],
  'prior_registered_reader_unchanged':True,'new_source_content_changed':False,
  'acceptance':'New source count549, all original records retained, inspected new text and all-page bounds.'})
 write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Preserved reviewed input')for p in
  [OLD,PRIOR,prior.BASE/'prepared-inputs.json',BASE/'repair-review.json',Path(__file__).resolve()]],
  'generated':[ref(p,'Successor input')for p in[DRIVER,BASE/'source-audit.json',BASE/'development.tex',BASE/'refs.bib']],
  'credit_policy':'No automatic substantive-page or mandatory-repair credit.','visual_acceptance':False})
 print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'failed_attempt_preserved':True}))

def build():
 for name,value in{'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():setattr(engine,name,value)
 with(BASE/'compile-summary.log').open('x')as stream:
  with redirect_stdout(stream):engine.build()
 report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
 def page(label):
  pattern=re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)'
  return int(re.search(pattern,aux).group(1))
 report.update(builder=ref(Path(__file__).resolve(),'Preserving commercial-driver repair'),
  predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen730-page working reader'),
  commercial_sections={label:page('exec14:'+label)for label in['commercial-contracts','commercial-contracts-end']})
 engine.core.write(OUT/'build-report.json',report)
 assert report['cited_records']==549 and report['pages']>730
 result=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',result)
 assert result['status']=='pass'and not result['issues']
 print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['commercial_sections'],
  'scholarly_pdfs':result['scholarly_pdfs'],'material_warnings':[w for w in report['warnings']if 'Underfull'not in w]}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
 {'prepare':prepare,'build':build}[a.command]()
