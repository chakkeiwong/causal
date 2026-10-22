#!/usr/bin/env python3
"""Preserve the complete reader and add commercial observation semantics."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import observations_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/observations-commercial-v1';OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-22/census-domain-knowledge-v1'
OLD=DOCS/'causal_proposal_domain_knowledge_reviewed_2026-10-22.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_observations_reviewed_2026-10-22'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf');DEVELOPMENT=BASE/'development.tex'
LABELS=['exec22:obs-'+x for x in ['scope','linkage','maps','mixture','variance','value','clocks','availability','selection','inclusion']]
read=lambda p:json.loads(p.read_text())

def expected_driver():
    body=OLD.read_text();marker=r'\input{program/execution/2026-10-17/s7/publication-v2/chapter.tex}'
    assert body.count(marker)==1
    body=body.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-22/observations-commercial-v1/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',body)

def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS']:
        setattr(engine,name,globals()[name])
    engine.exact=exact;engine.expected_driver=expected_driver

def prepare():
    configure();assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    for name in ['source-audit.json','review.json','comparison-review.json','conversion-contract.json','plan-review.json']:
        verify_bindings(read(BASE/name))
    assert exact.calculate()==read(BASE/'exact-results.json')
    entries=engine.sources()
    write(BASE/'manuscript-plan-review.json',dict(status='pass',
        evidence=[ref(DEVELOPMENT,'Connected observation argument'),ref(BASE/'plan.md','Reviewed plan')],
        checks=['Preserve all preceding source identities, citation contexts and chapter inputs.',
            'Compare matching, feature lookup and storage snapshots against identity, clocks, inclusion and audit requirements.',
            'Separate native score scope from coherent map probabilities and event time from availability.',
            'Treat legacy/current clients, manual discrepancy, unknown cutoff bytes and commercial rights explicitly.',
            'No market-completion, vendor execution, calibrated score or rendered acceptance claim.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_argument',issues=[],
        evidence=[ref(ROOT/'tools/observations_reference_20261022.py','Exact calculation'),ref(BASE/'exact-results.json','Exact replay'),ref(DEVELOPMENT,'Assumptions and derivation')],
        findings=['Event-only retrieval returns9; decision-time availability excludes it and returns2.',
            'Two complete map contrasts+4/-4 give8p-4; p=4/5 produces12/5.',
            'Independent equiprobable +/-1/2 noise gives total variance1/4+64p(1-p)=1049/100; distinct from fixed sample variance.',
            'Stipulated USD10 per unit and USD30 cost give margins10/-6 and probability threshold7/8.',
            'Equal strata with effects6/2 and inclusion1/1/4 yield retained effect26/5 versus population4; normalized inverse inclusion weighting returns4.',
            'Causal interpretation, map calibration, positivity and conditional transport are assumptions, not vendor guarantees.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',rendered_review=False,evidence=[ref(DEVELOPMENT,'Connected comparison')],
        findings=['Define units, probability scope, clocks, strata and monetary inputs.',
            'Separate observed documentation from proposed integration and actual current examples.',
            'Do not equate vendor group IDs, source metadata, point-in-time labels or public access with truth, cutoff proof or rights.',
            'Keep acquisition history and controller records outside product narrative.']))
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date']) if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),ROOT/'tools/build_network_commercial_reader_20261020.py',ROOT/'tools/observations_reference_20261022.py']
    paths += [BASE/n for n in ['source-audit.json','review.json','comparison-review.json','conversion-contract.json','omissions-register.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Audited additions')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(entries))))

def build():configure();engine.build()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);{'prepare':prepare,'build':build}[p.parse_args().command]()
