#!/usr/bin/env python3
"""Integrate reviewed ltmle semantics without rewriting earlier reader inputs."""
import argparse
import json
from pathlib import Path
import re
from types import SimpleNamespace

import build_network_commercial_reader_20261020 as engine
import ltmle_policy_oracle_v2_20261023 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-23/ltmle-reader-v2'
OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-23/detailed-workflow-reader-v2'
OLD=DOCS/'causal_proposal_detailed_workflow_reviewed_2026-10-23.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_longitudinal_regimes_reviewed_v2_2026-10-23'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
SOURCE=DOCS/'program/execution/2026-10-23/ltmle-reuse-v1'
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec23:ltmle-'+x for x in ['regimes','hardship','default','gformula','value','censoring','cluster']]
read=lambda p:json.loads(p.read_text())


def calculate():
    return exact.calculate()


def expected_driver():
    text=OLD.read_text()
    marker=r'\input{program/execution/2026-10-23/semantics-reader-v4/longitudinal-development.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{'+str(DEVELOPMENT.relative_to(DOCS))+'}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS','expected_driver']:
        setattr(engine,name,globals()[name])
    engine.exact=SimpleNamespace(calculate=calculate)


def prepare():
    configure()
    assert not BASE.exists() and not DRIVER.exists() and not PDF.exists()
    for p in [PRIOR,PREDECESSOR/'working-release.json',SOURCE/'review-v2.json',SOURCE/'source-audit-v2.json']:
        verify_bindings(read(p))
    assert calculate()==read(SOURCE/'policy-oracle-results-v2.json')
    BASE.mkdir()
    content=(SOURCE/'development-v2.tex').read_text()
    commit='338c029dae9692ef20714125773da7037688993b'
    old_literal=r'\texttt{'+commit+'}'
    new_literal=r'\allowbreak'.join(r'\texttt{'+commit[i:i+8]+'}' for i in range(0,len(commit),8))
    assert content.count(old_literal)==1
    DEVELOPMENT.write_text(content.replace(old_literal,new_literal))
    write(BASE/'source-audit.json',read(SOURCE/'source-audit-v2.json'))
    write(BASE/'exact-results.json',calculate())
    write(BASE/'mathematical-review.json',read(SOURCE/'mathematical-review-v2.json'))
    (BASE/'integration-plan.md').write_text('''# Preserve the reader and integrate effective longitudinal semantics

Insert the reviewed ltmle section after the existing lmtp development in the
longitudinal chapter. Preserve all previous content files, source identities,
citation contexts, scholarly PDFs and negative results. Add two new citation
records for pinned software originals and the validated authored calculation.
Compile and inspect the new argument and all-page text bounds. Renew only
exact-reader Q2-Q4 author reviews and pair the sponsor to the exact new bytes.
Visual acceptance remains blocked by the exhausted session image allowance;
it does not block source work or other independent proposal obligations.
The failed probability law and frozen-file edit are preserved; neither enters
the new reader. This is a proposal reference decision, with no native adoption.
''')
    write(BASE/'plan-review.json',dict(status='pass',issues=[],
        evidence=[ref(BASE/'integration-plan.md','Reviewed preserving plan'),ref(SOURCE/'review-v2.json','Source and scientific review')],
        checks=['The current two S5 inputs retain their original bytes.',
            'The full commit identity gains line-break opportunities only; failed layout is preserved in ltmle-reader-v1.',
            'All old citation identities and contexts remain; new technical claims use new source keys.',
            'All16 probabilities, independent moments, censoring and exact sample covariance checks pass.',
            'The new reader and sponsor remain proposal evidence; visual/final acceptance stays open.']))
    write(BASE/'copyedit-review.json',dict(status='pass',issues=[],evidence=[ref(DEVELOPMENT,'Connected argument')],
        findings=['MSM saturation is distinguished from policy count.',
            'C=1 means observed; outcome horizon, independent observation law and all monetary inputs are explicit.',
            'The factor-of-two heuristic is distinguished from exact degrees-of-freedom correction.',
            'Requested variance, effective variance and suppressed warnings are separate source findings.'],visual_acceptance=False))
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        identity=s['source_identity']
        note=(r'\url{'+identity+'}; ' if identity.startswith('https://') else engine.shared.escape(identity)+'; ')+engine.shared.escape(s['version_date'])
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    DRIVER.write_text(expected_driver())
    entries=engine.sources()
    inputs=[OLD,PRIOR,DEVELOPMENT,Path(__file__),Path(exact.__file__),SOURCE/'review-v2.json',SOURCE/'failed-draft-1/failure-review.json']
    inputs += [BASE/n for n in ['source-audit.json','exact-results.json','mathematical-review.json','integration-plan.md','plan-review.json','copyedit-review.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in inputs],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New source and derivation citations')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),citations=len(entries))))


def build():
    configure()
    engine.build()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[parser.parse_args().command]()
