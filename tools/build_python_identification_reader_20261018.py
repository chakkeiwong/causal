#!/usr/bin/env python3
"""Preserve predecessor bytes and integrate bounded Python identification findings."""
import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess

import audit_reader_traceability_v2_20261013 as trace
import build_integrated_monograph_v12 as shared
import python_counterfactual_reference_20261018 as exact
import review_gap_reader_v13 as layout
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs'
BASE = DOCS/'program/execution/2026-10-18/python-identification-reader-v1'
OUT = BASE/'reader'
PREDECESSOR = DOCS/'program/execution/2026-10-18/graph-panel-reader-v2'
OLD = DOCS/'causal_proposal_graph_panels_reviewed_v2_2026-10-18.tex'
PRIOR = PREDECESSOR/'reader/source-audit.json'
DEVELOPMENT = BASE/'development.tex'
EVIDENCE = DOCS/'program/execution/2026-10-18/python-identification-v1'
NAME = 'causal_proposal_python_identification_reviewed_2026-10-18'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
LABELS = ['exec18:pyid-'+s for s in ['question','packages','coupling','equal-laws',
          'conditional','sharp','bounds','integration']]
NEW_KEYS = ['exec18_pyid_'+s for s in ['one_line','oracle','missing','mean','graph',
            'metadata','license','coupling','contract']]


def read(path):
    return json.loads(path.read_text())


def expected_driver():
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-18/graph-panel-reader-v2/graph-development.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
    assert len(re.findall(r'\\bibliography\{([^}]+)\}',text))==1
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:
        r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def source_records():
    original=EVIDENCE/'source-audit.json'
    audit=read(original)
    records=[]
    for key,raw in zip(NEW_KEYS[:7],audit['sources']):
        source=copy.deepcopy(raw)
        source.update(integrated_citation_key=key,
            original_audit=ref(original,'Seven new inspected archive sources and inherited pinned evidence'),
            bibliography_note='Selected Ananke0.5.0 release uploaded5December2023; acquired18October2026; authenticated inert source inspection, no installation or execution')
        records.append(source)
    records.append(dict(integrated_citation_key='exec18_pyid_coupling',
        kind='project_derivation',author='Causal banking proposal project',year=2026,
        title='Exact randomized response-type coupling and sharp counterfactual bounds',
        source_identity='Project-authored structural construction and rational enumeration',version_date='18October2026',
        local_copy=ref(ROOT/'tools/python_counterfactual_reference_20261018.py','Exact authored coupling construction'),
        inspected_anchors=[ref(EVIDENCE/'exact-reference.json','Preserved reference results'),
                           ref(BASE/'exact-results.json','Fresh exact replay and direct marginal checks')],
        supported_claims=['Identical randomized observed/intervention laws allow conditional recovery0 versus1.',
                          'Response-type parameter t gives sharp benefit-share[0,1/2] and conditional[0,1] bounds.',
                          'Stipulated retrospective net range is[-50,350]USD; no prospective policy value follows.'],
        limitations=['Authored deterministic proof; no native software, sampling uncertainty or bank evidence.']))
    records.append(dict(integrated_citation_key='exec18_pyid_contract',
        kind='project_design',author='Causal banking proposal project',year=2026,
        title='Proposed typed four-family Python identification boundary and omissions',
        source_identity='Project-authored proposal design based on inspected pinned originals',version_date='18October2026',
        local_copy=ref(EVIDENCE/'conversion-contract.json','Proposed query, result, conversion and environment boundaries'),
        inspected_anchors=[ref(EVIDENCE/'candidate-register.json','Four inherited candidates and aliases'),
                           ref(EVIDENCE/'omissions-register.json','Specific GCM, cross-world and bounds follow-up'),
                           ref(EVIDENCE/'author-review.json','Author scoped inconclusive review')],
        supported_claims=['Separate adjustment, ID, conditional intervention, cross-world and bounds queries.',
                          'Distinguish scientific nonidentification, unsupported requests, invalid input and engine failure.',
                          'Selected declared dependencies conflict; separate pinned environments and typed conversion are proposed.',
                          'Wider counterfactual/bounds coverage and executable admission remain open.'],
        limitations=['Design reference, not installed integration, rights clearance or complete market survey.']))
    assert len(records)==9
    return records


def calculate():
    result=exact.calculate()
    assert result==read(EVIDENCE/'exact-reference.json')['coupling']
    for model in result['models']:
        assert set(model['observed'].values())=={'1/4'}
        assert model['do_means']==['1/2','1/2'] and model['ATE']=='0'
    return result


def prepare():
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    originals=[EVIDENCE/n for n in ['plan-review.json','source-audit.json','author-review.json','operation-receipt.json']]
    for path in [PRIOR]+originals:
        verify_bindings(read(path))
    write(BASE/'manuscript-plan-review.json',dict(status='pass',reviewer='Author/coordinator',
        evidence=[ref(BASE/'plan.md','Preserving five-step plan'),ref(DEVELOPMENT,'Connected query/source/coupling/integration argument')]+[ref(p,'Inspected reviewed evidence') for p in originals],
        findings=['All772 earlier records,201 scholarly PDFs, unchanged compiled inputs and citation contexts must survive.',
                  'Seven new archive records retain authentic bytes, upload/acquisition dates, hashes and inspected ranges.',
                  'Independent randomization, response-type bounds, hypothetical money and the retrospective clock are explicit.',
                  'Additional scientific monotonicity is not claimed as learned from randomization.',
                  'Reuse/port decisions, failed-precondition semantics and dependency conflicts remain proposals.',
                  'No full Python coverage, native execution, visual or final acceptance follows.'],
        repairs=['Converted inadvertent tab characters in newly authored TeX to texttt commands before freezing inputs.'],
        visual_acceptance=False,final_acceptance=False))
    write(BASE/'exact-results.json',calculate())
    audit=dict(sources=source_records(),cutoff='2026-10-07',scope='Seven Ananke originals and two authored project references')
    verify_bindings(audit)
    write(BASE/'source-audit.json',audit)
    write(BASE/'mathematical-review.json',dict(status='pass',issues=[],
        evidence=[ref(ROOT/'tools/python_counterfactual_reference_20261018.py','Rational enumeration and feasible-table proof'),
                  ref(BASE/'exact-results.json','Fresh replay'),ref(DEVELOPMENT,'Explained assumptions, notation and target')],
        findings=['Both models have all four observed cells1/4 and intervention means1/2.',
                  'Retrospective conditional recoveries0 and1 disagree on events of probability1/4.',
                  'Marginal constraints force(p00,p01,p10,p11)=(1/2-t,t,t,1/2-t); nonnegativity and structural construction prove sharpness.',
                  'Randomization makes conditional recovery2t; hypothetical net800t-50 ranges[-50,350]USD.',
                  'Monotonicity forces t=0 under equal marginals but is an extra restriction.',
                  'Identification bounds are not confidence intervals; retrospective selection is not a prospective information set.']))
    write(BASE/'copyedit-review.json',dict(status='pass',rendered_review=False,
        evidence=[ref(DEVELOPMENT,'Connected source and mathematical argument')],
        findings=['Explained binary variables, factual clock and response-type notation.',
                  'Selected historical release is not labeled latest support.',
                  'Static source findings, deterministic construction, proposed integrations and omitted searches are explicit.',
                  'No process ledger or permission discussion enters the product narrative.']))
    bib=[]
    for s in audit['sources']:
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+shared.escape(s['author'])+
            '}},\n title={'+shared.escape(s['title'])+'},\n year={'+str(s['year'])+
            '},\n note={'+shared.escape(s.get('bibliography_note',s['source_identity']+'; '+s['version_date']))+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,BASE/'plan.md',BASE/'source-audit.json',
           BASE/'manuscript-plan-review.json',BASE/'mathematical-review.json',
           BASE/'copyedit-review.json',BASE/'exact-results.json',
           ROOT/'tools/python_counterfactual_reference_20261018.py',Path(__file__)]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Preserving reviewed input') for p in paths],
        generated=[ref(DRIVER,'Preserving identification driver'),ref(BASE/'refs.bib','Nine new records')],
        expected_cited_records=781,expected_scholarly_pdfs=201,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=781,exact='pass')))


def build():
    verify_bindings(read(BASE/'prepared-inputs.json'))
    assert DRIVER.read_text()==expected_driver() and calculate()==read(BASE/'exact-results.json')
    assert not OUT.exists() and not PDF.exists()
    OUT.mkdir()
    env=dict(os.environ)
    env['TEXINPUTS']=str(DOCS)+'//:'+env.get('TEXINPUTS','')
    env['BIBINPUTS']=str(DOCS)+'//:'+env.get('BIBINPUTS','')
    command=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
             '-output-directory='+str(OUT),str(DRIVER)]
    def execute(args,name):
        with (OUT/name).open('x') as stream:
            result=subprocess.run(args,cwd=DOCS,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
        assert result.returncode==0,'Failure preserved in '+str(OUT/name)
    execute(command,'pass-1.log')
    execute(['bibtex',str((OUT/NAME).relative_to(DOCS))],'bibtex-pass.log')
    for turn in range(2,6):
        execute(command,f'pass-{turn}.log')
        log=(OUT/(NAME+'.log')).read_text(errors='replace')
        if turn>=3 and not any(t in log for t in ['Label(s) may have changed','Rerun to get']):
            break
    for token in ['undefined citations','undefined references','multiply defined','Missing character','Overfull']:
        assert token not in log,token
    files=shared.scan(DRIVER)
    joined='\n'.join(t for _,t in files)
    labels=re.findall(shared.LABEL,joined)
    assert len(labels)==len(set(labels))
    cited={k.strip() for g in re.findall(shared.CITE,joined) for k in g.split(',')}
    entries={}
    for path in [PRIOR,BASE/'source-audit.json']:
        audit=read(path);verify_bindings(audit)
        for s in audit['sources']:
            k=s['integrated_citation_key'];assert k not in entries or entries[k]==s;entries[k]=s
    assert cited<=entries.keys(),cited-entries.keys()
    assert len(cited)==781
    PDF.write_bytes((OUT/(NAME+'.pdf')).read_bytes())
    write(OUT/'source-audit.json',dict(sources=[entries[k] for k in sorted(cited)],
        tex_files=[ref(p,'Compiled source') for p in sorted({p for p,_ in files})],
        source_audits=[ref(p,'Preserved audited input') for p in [PRIOR,BASE/'source-audit.json']],
        cutoff='2026-10-07',visual_acceptance=False))
    subprocess.run(['pdftotext','-layout',str(PDF),str(OUT/'reader.txt')],check=True,timeout=30)
    info=subprocess.check_output(['pdfinfo',str(PDF)],text=True,timeout=15)
    pages=int(re.search(r'(?m)^Pages:\s+(\d+)',info).group(1))
    aux=(OUT/(NAME+'.aux')).read_text();anchors={}
    for label in LABELS:
        m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^}]+)\}\{(\d+)\}',aux)
        assert m,label
        anchors[label]=dict(number=m.group(1),printed_page=int(m.group(2)))
    report=dict(status='compiled_source_and_text_checked_working_draft',pages=pages,
        pdf=ref(PDF,'Preserving Python identification successor'),driver=ref(DRIVER,'Preserving driver'),
        builder=ref(Path(__file__),'Exact preserving builder'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Immutable1074-page graph/panel reader'),
        source_audit=ref(OUT/'source-audit.json','781 audited citation records'),cited_records=len(cited),
        added_anchors=anchors,warnings=[line for line in log.splitlines() if any(t in line for t in ['Warning','Overfull','Underfull','Missing character'])],
        final_acceptance=False,mandatory_repairs_closed=[],visual_acceptance=False,
        visual_review='Pending fresh image allowance; inherited allowance exhausted')
    write(OUT/'build-report.json',report)
    layout.OUT=OUT;layout.main()
    assert read(OUT/'text-layout-review.json')['status']=='pass'
    index=trace.audit(DRIVER,OUT/'source-audit.json');write(BASE/'traceability-review.json',index)
    assert index['status']=='pass' and not index['issues'] and index['scholarly_pdfs']==201
    print(json.dumps(dict(pages=pages,records=781,scholarly_pdfs=201,anchors=anchors,warnings=report['warnings'],visual_acceptance=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[parser.parse_args().command]()
