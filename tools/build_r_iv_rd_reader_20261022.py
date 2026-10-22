#!/usr/bin/env python3
"""Preserve the entire predecessor and integrate the reviewed R IV/RD argument."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import r_iv_rd_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/r-iv-rd-v1'
OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-22/bayesian-commercial-v2'
OLD=DOCS/'causal_proposal_bayesian_commercial_reviewed_v2_2026-10-22.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_r_iv_rd_reviewed_2026-10-22'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec22:riv-'+x for x in ['scope','target','late','population','value','inference','gaussian','set','topology','continuity','support','bound','randomization','reuse']]
read=lambda p:json.loads(p.read_text())


def expected_driver():
    body=OLD.read_text()
    marker=r'\input{program/execution/2026-10-13/commercial-iv-rd/comparison.tex}'
    assert body.count(marker)==1
    body=body.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-22/r-iv-rd-v1/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',body)


def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS']:
        setattr(engine,name,globals()[name])
    engine.exact=exact;engine.expected_driver=expected_driver


def prepare():
    configure();assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    for name in ['source-audit.json','review.json','conversion-contract.json','plan-review.json']:
        verify_bindings(read(BASE/name))
    assert exact.calculate()==read(BASE/'exact-results.json')
    entries=engine.sources()
    write(BASE/'manuscript-plan-review.json',dict(status='pass',
        evidence=[ref(DEVELOPMENT,'Connected product argument'),ref(BASE/'plan.md','Reviewed continuation')],
        checks=['Preserve all earlier source identities, citation contexts and chapter inputs.',
            'Explain distinct IV and RD targets before the package comparison; develop monetary consequences.',
            'Derive Gaussian inversion under its actual known-covariance law; label q4 coverage95.45%, not95%.',
            'Keep package source inspection, exact authored examples and proposed native studies distinct.',
            'Keep process receipts outside the product narrative; visual acceptance remains open.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_argument',issues=[],
        evidence=[ref(ROOT/'tools/r_iv_rd_reference_20261022.py','Exact rational sums and enumerations'),
            ref(BASE/'exact-results.json','Reproduced results'),ref(DEVELOPMENT,'Stated laws, derivations and limits')],
        findings=['Under independence/exclusion/monotonicity, reduced form equals complier probability times mean effect; population effect is a different target.',
            'Explicit law gives first stage2/5, ITT-60, LATE-150, ATE-70 and stipulated margins10,50,-30USD for different policies.',
            'Direct encouragement effect and defiers give-200/-250 ratios; neither is interpreted as the original complier effect.',
            'Known positive-definite Gaussian covariance yields standardized normal null contrast for every first-stage mean; q4 has2Phi(2)-1 coverage.',
            'Quadratic roots and direct inequalities agree on two rays, bounded interval and whole-line cases; finite grid misses a nonempty global set.',
            'Two continuous potential-mean laws agree on all observed integer scores; Lipschitz errors add and endpoints are attainable at L10/delta1.',
            'Uniform3-of6 assignment gives20 allocations and sharp-null two-sided p2/20; not a generic average-effect test.',
            'No package conformance, empirical calibration or bank economics is claimed.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',rendered_review=False,
        evidence=[ref(DEVELOPMENT,'Connected six-profile comparison')],
        findings=['Define eligibility, take-up, loss sign, horizon and population before mathematical use.',
            'Separate local/randomized design assumptions, robust inference meanings, diagnostics and set topology.',
            'State exact cutoff timezone and CRAN distribution scope; distinguish declared rights from full clearance.',
            'No borrowed scholarly claim from an uninspected bibliography; technical package claims use saved primary manuals/source.']))
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date'])
              if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),ROOT/'tools/build_network_commercial_reader_20261020.py',ROOT/'tools/r_iv_rd_reference_20261022.py']
    paths += [BASE/n for n in ['source-audit.json','review.json','conversion-contract.json','omissions-register.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New audited citations')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(entries))))


def build():configure();engine.build()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[p.parse_args().command]()
