#!/usr/bin/env python3
"""Compile the preserving proposal successor with bounded output."""
import contextlib,json,re
from pathlib import Path
import build_java_reader_20261013 as compiler
import build_integrated_monograph_v12 as shared
import prepare_reader_repair_20261014 as prepared
import master_control as core
ROOT=prepared.ROOT;BASE=prepared.BASE;OUT=BASE/'reader';NAME=prepared.NAME
OLD=prepared.OLD;DRIVER=prepared.DRIVER;PDF=prepared.PDF;PRIOR_AUDIT=prepared.PRIOR_AUDIT

def main():
 assert not OUT.exists() and not PDF.exists(),'Preserve attempted reader; use successor for repairs'
 shared.verify_refs(json.loads((BASE/'prepared-inputs.json').read_text()))
 for key in ['BASE','OUT','NAME','OLD','DRIVER','PDF','PRIOR_AUDIT']:setattr(compiler,key,globals()[key])
 OUT.mkdir()
 with (OUT/'compile-summary.txt').open('x') as stream,contextlib.redirect_stdout(stream):compiler.build()
 report=json.loads((OUT/'build-report.json').read_text());report.pop('java_comparison',None)
 aux=(OUT/(NAME+'.aux')).read_text()
 def page(label):return int(re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
 report.update(builder=shared.ref(Path(__file__),'Preserving integration builder'),pdf=shared.ref(PDF,'Integrated working monograph'),predecessor_pdf=shared.ref(OLD.with_suffix('.pdf'),'Preserved 655-page reader'),
    reviewed_l4={'start':page('ch:la03-discovery'),'end':page('exec14:l4-development-end'),'physical_span':page('exec14:l4-development-end')-page('ch:la03-discovery')+1,'allocation':[20,22],'substantive_acceptance':False},
    new_sections={k:page(k) for k in ['exec14:commercial-latent-choice','exec14:causallearn-decision','exec14:estimation-validation','exec14:execution-meaning','exec14:servicing-evidence']})
 core.write(OUT/'build-report.json',report)
 print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'l4':report['reviewed_l4'],'warning_count':len(report['warnings'])}))
if __name__=='__main__':main()
