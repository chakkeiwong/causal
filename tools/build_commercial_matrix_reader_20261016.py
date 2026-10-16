#!/usr/bin/env python3
"""Integrate the reviewed commercial survival matrix into a preserving reader."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-16/commercial-survival/publication'
OUT=BASE/'reader'
OLD=ROOT/'docs/causal_proposal_qualification_2026-10-16.tex'
PRIOR=ROOT/'docs/program/execution/2026-10-16/s10/publication/reader/source-audit.json'
MATRIX=ROOT/'docs/program/comprehensive-v14/work/SW.COMM.longitudinal_survival/vendor-comparison.json'
WORK=ROOT/'docs/program/execution/2026-10-16/commercial-survival'
NAME='causal_proposal_commercial_matrix_2026-10-16'
DRIVER=ROOT/'docs'/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');BS,NL=chr(92),chr(10)

def prepare():
    assert not DRIVER.exists() and not BASE.exists()
    BASE.mkdir(parents=True)
    audit=json.loads((WORK/'author-review.json').read_text())
    matrix=json.loads(MATRIX.read_text())
    verify_bindings(audit);verify_bindings(matrix)
    prior=json.loads(PRIOR.read_text());verify_bindings(prior)
    sources=[
      {'integrated_citation_key':'exec16_commercial_matrix','title':'Edition-specific commercial survival comparison against the bounded local service','kind':'project_implementation','author':'Causal banking research project','year':2026,
       'source_identity':str(MATRIX.relative_to(ROOT)),'version_date':'2026-10-16;author matrix and actual local method-dispatch probes',
       'local_copy':ref(MATRIX,'Nine-row current/proposed/vendor matrix'),'inspected_anchors':['current_capability','vendor_matrix','proposed_acceptance_profiles'],
       'supported_claims':['Current local request enum and dispatcher expose no named survival operation;three authored survival profiles return unsupported.','Nine vendor-family rows distinguish documented strengths,limits,proposed comparison,current gap,rights and unknown prices.','Coverage remains inconclusive;MATLAB and exact editions/rights stay unresolved.'],
       'primary_artifacts':[ref(WORK/'local-probe.json','Actual local operation responses'),ref(WORK/'survival-method-probes.json','Three unsupported survival method probes'),ref(WORK/'primary-review.json','Preserved source and local review'),ref(WORK/'author-review.json','Author source/capability review')],
       'limitations':json.loads((WORK/'author-review.json').read_text())['limitations']},
      {'integrated_citation_key':'exec16_commercial_runtime','title':'Actual bounded local survival-method dispatch observations','kind':'project_implementation','author':'Causal banking research project','year':2026,
       'source_identity':str((WORK/'survival-method-probes.json').relative_to(ROOT)),'version_date':'2026-10-16;local reference runtime;no vendor execution',
       'local_copy':ref(WORK/'survival-method-probes.json','Three authored profiles returned unsupported'),'inspected_anchors':['estimate.effect engine/estimator guard','completed unsupported null-result envelopes'],
       'supported_claims':['fixed-treatment-survival,competing-risk-incidence and sequential-policy-survival identifiers return completed unsupported null results in the current local dispatcher.','This is a local implementation boundary,not a claim that commercial or open-source survival software lacks these methods.'],
       'primary_artifacts':[ref(ROOT/'src/causalbank/operation_service_v12.py','SUPPORTED and _estimate method-pair guard'),ref(ROOT/'tools/probe_survival_methods_20261016.py','Bounded dispatch probe')],
       'limitations':['No vendor/upstream package run,bank data or product qualification.']}]
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,'prior':ref(PRIOR,'641 preserved citation records'),'visual_acceptance':False})
    bib=[]
    for s in sources:
      bib.append('@misc{'+s['integrated_citation_key']+','+NL+' author={{'+engine.shared.escape(s['author'])+'}},'+NL+' title={'+engine.shared.escape(s['title'])+'},'+NL+' year={2026},'+NL+' note={'+engine.shared.escape(s['version_date'])+'}'+NL+'}'+NL)
    (BASE/'refs.bib').write_text(NL.join(bib))
    book=OLD.read_text();marker=BS+'input{program/execution/2026-10-14/commercial-survival/v3/comparison.tex}'
    assert book.count(marker)==1
    book=book.replace(marker,marker+NL+BS+'input{program/execution/2026-10-16/commercial-survival/development.tex}')
    pat=re.compile(re.escape(BS+'bibliography{')+'([^}]+)'+re.escape('}'));assert len(pat.findall(book))==1
    book=pat.sub(lambda m:BS+'bibliography{'+m.group(1)+',program/execution/2026-10-16/commercial-survival/publication/refs}',book)
    DRIVER.write_text(book)
    write(BASE/'prepared-inputs.json',{'inputs':[ref(p,'Reviewed preserving input') for p in [OLD,PRIOR,MATRIX,WORK/'primary-review.json',WORK/'author-review.json',Path(__file__)]],
      'generated':[ref(p,'Successor source') for p in [DRIVER,BASE/'source-audit.json',BASE/'refs.bib']],
      'credit_policy':'No automatic census closure,product qualification or depth credit','visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'new_records':2}))

def build():
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF,'PRIOR_AUDIT':PRIOR}.items():setattr(engine,key,value)
    with (BASE/'compile-summary.log').open('x') as stream:
      with redirect_stdout(stream):engine.build()
    report=json.loads((OUT/'build-report.json').read_text());aux=(OUT/(NAME+'.aux')).read_text()
    def page(label):
      m=re.search(re.escape(BS+'newlabel{'+label+'}{{')+'[^}]*'+re.escape('}{')+'([0-9]+)',aux);assert m,label;return int(m.group(1))
    report.update(builder=ref(Path(__file__),'Preserving commercial matrix reader builder'),predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen816-page qualification reader'),
      commercial_matrix_sections={x:page('exec16:'+x) for x in ['commercial-matrix','commercial-matrix-end']})
    engine.core.write(OUT/'build-report.json',report)
    audited=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',audited)
    assert report['cited_records']==643 and report['pages']>816
    assert audited['status']=='pass' and not audited['issues'] and audited['scholarly_pdfs']==175
    print(json.dumps({'pages':report['pages'],'cited_records':report['cited_records'],'sections':report['commercial_matrix_sections'],'scholarly_pdfs':audited['scholarly_pdfs'],'material_warnings':[w for w in report['warnings'] if 'Underfull' not in w]}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args();{'prepare':prepare,'build':build}[a.command]()
