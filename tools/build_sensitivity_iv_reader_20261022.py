#!/usr/bin/env python3
"""Preserve the entire reader and integrate sensitivity reuse and Python IV semantics."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import sensitivity_iv_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref,verify_bindings,write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/sensitivity-iv-reader-v1';OUT=BASE/'reader'
HD=DOCS/'program/execution/2026-10-22/honestdid-reuse-v1'
IV=DOCS/'program/execution/2026-10-22/python-iv-kernels-v1'
PREFLIGHT=DOCS/'program/execution/2026-10-22/python-iv-rd-preflight-v2'
PREDECESSOR=DOCS/'program/execution/2026-10-22/observations-commercial-v1/publication-v2'
OLD=DOCS/'causal_proposal_observations_reviewed_v2_2026-10-22.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_sensitivity_iv_reviewed_2026-10-22'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
IV_DEVELOPMENT=BASE/'python-development.tex'
LABELS=['exec22:hd-'+s for s in ['scope','restrictions','rm','sd','projection','law','ellipse','components','endpoints','example','numerics','reuse']]
LABELS+=['exec22:pyiv-'+s for s in ['scope','rank','witness','ratio','covariance','diagnostics']]
read=lambda p:json.loads(p.read_text())


def expected_driver():
    text=OLD.read_text()
    for marker,source in [
        (r'\input{program/execution/2026-10-17/s4/depth-extension/development.tex}',IV_DEVELOPMENT),
        (r'\input{program/execution/2026-10-21/gsynth-reuse-v1/development.tex}',DEVELOPMENT)]:
        assert text.count(marker)==1
        text=text.replace(marker,marker+'\n'+r'\input{'+str(source.relative_to(DOCS))+'}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS']:
        setattr(engine,name,globals()[name])
    engine.exact=exact;engine.expected_driver=expected_driver


def prepare():
    configure();assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    evidence=[];records=[]
    for folder in [HD,IV]:
        for name in ['source-audit.json','review.json','conversion-contract.json','exact-results.json']:
            obj=read(folder/name);verify_bindings(obj);evidence.append(ref(folder/name,'Reviewed source and authored evidence'))
        records+=read(folder/'source-audit.json')['sources']
    assert exact.calculate()['sensitivity']==read(HD/'exact-results.json')
    assert exact.calculate()['iv']==read(IV/'exact-results.json')
    original=next(s for s in read(PREFLIGHT/'source-audit.json')['sources'] if s['local_copy']['path'].endswith('exec22_pyiv_linearmodels_source_1.txt'))
    verify_bindings(original)
    records.append(dict(integrated_citation_key='exec22_pyiv_diagnostics_linearmodels',kind='software_primary_source',
        title='linearmodels cutoff first-stage and overidentification diagnostics',author='Kevin Sheppard and contributors',year=2026,
        source_identity=original['source_identity'],version_date=original['version_date'],local_copy=original['local_copy'],
        primary_sources=[original],inspected_anchors=original['inspected_anchors'],supported_claims=original['supported_claims'],
        limitations=['Selected source inspection only; no coefficient-null inversion or native execution is established.']))
    write(BASE/'source-audit.json',dict(sources=records,cutoff='2026-10-07',source_reviews=evidence))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'plan-review.json',dict(status='pass',evidence=[ref(HD/'plan.md','Reviewed continuation'),ref(IV/'plan.md','Independent reviewed continuation')],
        checks=['Preserve prior citation identity and context; insert each argument into its relevant chapter.',
            'Separate published guarantees, observed code paths and independent authored derivations.',
            'Reference-only HonestDiD outcome and unfinished Python cell remain distinct.',
            'Compile and check text without claiming fresh visual acceptance; pair sponsor to exact reader.']))
    write(BASE/'review.json',dict(status='pass',scope='Connected reuse, uncertainty and diagnostic synthesis',
        evidence=evidence+[ref(HD/'paper-inspection.json','Genuine original reread')],
        findings=['RM/SD assumptions and full covariance have different decision consequences.',
            'Grid extent, membership, status and actual methods belong in the sensitivity interface.',
            'Projected-rank checks and causal exclusion are distinct from separate matrix ranks.',
            'Diagnostic distribution and covariance configuration must survive library/CLI/MCP conversion.'],
        native_execution=False,visual_acceptance=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_derivations',issues=[],
        evidence=[ref(DEVELOPMENT,'Identification and Gaussian ellipse projection'),ref(IV_DEVELOPMENT,'Rank/exclusion and diagnostic scaling'),
            ref(ROOT/'tools/honestdid_reference_20261022.py','Analytic extrema with attained witnesses'),
            ref(ROOT/'tools/python_iv_reference_20261022.py','Rational IV witness and exact F survival'),ref(BASE/'exact-results.json','Reproduced values')],
        findings=['RM gives y+/-m|x|; SD gives y+x+/-M under one preperiod and normalized baseline.',
            'Ellipsoid support functions give component extrema; connected continuous image proves projection is an interval.',
            'Joint ellipse event implies target coverage under known Gaussian covariance, not package equivalence.',
            'Full covariance determinant7/4 gives component variances2/8 and endpoints-2.9233/10.9233.',
            'Separate centred rank-one d,z can have zero projected Gram; exclusion term1/100 yields ratios3/12 as epsilon shrinks.',
            'W8 and2 restrictions give F-scaled4 with different stipulated chi-square2 and F2,20 p-values.'],
        empirical_coverage=False,native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(DEVELOPMENT,'Sensitivity narrative'),ref(IV_DEVELOPMENT,'Python IV narrative')],
        findings=['Define baseline, clocks, units, weights and targets before equations.',
            'Avoid equating source paths with observed runtime failures or mathematical oracles with optimized package inference.',
            'Explain decision consequences, reuse alternatives and experiment merit; no process log in the product narrative.',
            'Report unresolved RD, solvers, release equivalence and rendered review.'],rendered_review=False))
    write(BASE/'manuscript-plan-review.json',dict(status='pass',evidence=[ref(BASE/'plan-review.json','Reviewed integration scope')],
        checks=['No duplicated curvature derivation; new three-period RM/SD and projection argument extends earlier S6.',
            'Python kernel comparison adds exact diagnostic metadata and weighted-fit semantics in S4.',
            'All seven added records are authentic primary sources or labeled project derivations.']))
    bib=[]
    for s in records:
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date']) if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    entries=engine.sources()
    paths=[OLD,PRIOR,DEVELOPMENT,IV_DEVELOPMENT,Path(__file__),ROOT/'tools/build_network_commercial_reader_20261020.py',
        ROOT/'tools/sensitivity_iv_reference_20261022.py',ROOT/'tools/honestdid_reference_20261022.py',ROOT/'tools/python_iv_reference_20261022.py']
    paths += [BASE/n for n in ['source-audit.json','review.json','plan-review.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Audited additions')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(entries))))


def build():configure();engine.build()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[parser.parse_args().command]()
