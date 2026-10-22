#!/usr/bin/env python3
"""Preserve the entire predecessor and integrate the domain-knowledge discovery argument."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import domain_knowledge_reference_20261022 as reference
from types import SimpleNamespace
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/census-domain-knowledge-v1'
OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-22/r-iv-rd-v1'
OLD=DOCS/'causal_proposal_r_iv_rd_reviewed_2026-10-22.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_domain_knowledge_reviewed_2026-10-22'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec22:domain-'+x for x in ['scope','elicitation','retrieval','semantics','chain','f1','value','causal','latent','covariance','margin','validation']]
read=lambda p:json.loads(p.read_text())
exact=SimpleNamespace(calculate=lambda:json.loads(json.dumps(reference.calculate())))


def expected_driver():
    body=OLD.read_text()
    marker=r'\input{program/execution/2026-10-20/census-expert-averaging-v1/development.tex}'
    assert body.count(marker)==1
    body=body.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-22/census-domain-knowledge-v1/development.tex}')
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
        evidence=[ref(DEVELOPMENT,'Connected graph-evidence argument'),ref(BASE/'plan.md','Reviewed continuation')],
        checks=['Preserve all preceding source identities, citation contexts and chapter inputs.',
            'Separate variable recall, graph fit, expert reconstruction and causal intervention truth.',
            'Explain contradictory evidence, cyclic reference, same-corpus retrieval and query-specific comparisons.',
            'Develop exact graph/observational-equivalence examples and a public prototype design before private studies.',
            'No figure-pixel, native execution, live-model or complete coverage claim.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_authored_argument',issues=[],
        evidence=[ref(ROOT/'tools/domain_knowledge_reference_20261022.py','Exact authored calculations'),
            ref(BASE/'exact-results.json','Reproduced results'),ref(DEVELOPMENT,'Stated models and qualifications')],
        findings=['F1 differences.349,.031,.008 and query-rank reversals follow printed rounded scores; no paired inference.',
            'One added false edge yields F1=4/5 and a three-cycle without a reciprocal pair.',
            'Ancestral reachability differs from adjacency; moralization additionally joins co-parents.',
            'Independent centered Gaussian structural equations give identical observed covariance and means.',
            'Replacing action equations gives causal derivatives-1/2 and0, despite equal observed regression slope.',
            'Stipulated USD100 loss-unit and USD20 cost give margins30/-20 and subjective weight threshold2/5.',
            'No observed joint law can distinguish these constructed twins; no actual bank return or calibrated model probability claimed.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',rendered_review=False,
        evidence=[ref(DEVELOPMENT,'Connected source-critical comparison')],
        findings=['Define targets, clocks, units, loss sign and latent variables before use.',
            'Describe source discrepancies without claiming corrected raw results.',
            'Compare ordinary and graph retrieval using incremental gains and query-dependent rankings.',
            'Keep acquisition failures and process history outside product narrative.']))
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date'])
              if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={'+(s['author'] if s['kind']=='paper' else '{'+engine.shared.escape(s['author'])+'}')+'},\n title={'+engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),ROOT/'tools/build_network_commercial_reader_20261020.py',ROOT/'tools/domain_knowledge_reference_20261022.py']
    paths += [BASE/n for n in ['source-audit.json','review.json','conversion-contract.json','omissions-register.json','mathematical-review.json','copyedit-review.json','manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','New audited citations')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs']+2,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),records=len(entries))))


def build():configure();engine.build()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[p.parse_args().command]()
