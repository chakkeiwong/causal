#!/usr/bin/env python3
"""Preserve the current reader while integrating the archival reuse decision."""
import argparse
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import review_causalnex_reuse_20261014 as work
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

ROOT = work.ROOT
DOCS = ROOT/'docs'
BASE = work.BASE/'publication'
OUT = BASE/'reader'
OLD = DOCS/'causal_proposal_longitudinal_review_2026-10-14.tex'
NAME = 'causal_proposal_software_lifecycle_2026-10-14'
DRIVER = DOCS/(NAME+'.tex')
PDF = DRIVER.with_suffix('.pdf')
PRIOR = DOCS/'program/execution/2026-10-14/l5-depth/reader/source-audit.json'


def configure():
    for name, value in {'BASE':BASE, 'OUT':OUT, 'OLD':OLD, 'NAME':NAME,
                        'DRIVER':DRIVER, 'PDF':PDF, 'PRIOR_AUDIT':PRIOR}.items():
        setattr(engine, name, value)


def prepare():
    assert not DRIVER.exists() and not (BASE/'prepared-inputs.json').exists()
    primary = json.loads((work.BASE/'primary-review.json').read_text())
    decision = json.loads(work.OUTPUT.read_text())
    verify_bindings(primary)
    verify_bindings(decision)
    assert decision['decision'] == 'reject' and decision['integration_allowed'] is False
    assert work.exact() == json.loads((work.BASE/'exact-oracle.json').read_text())
    sources = [engine.source('exec14_causalnex_primary',
        'CausalNex archived maintenance, graph semantics and dependency source review',
        'mckinsey/causalnex', 'software_primary_sources', 'https://github.com/mckinsey/causalnex',
        primary['revision']+'; '+primary['source_date']+'; declared0.12.2; inspected2026-10-14',
        work.BASE/'primary-review.json', 'Seven matched source blobs; recorded inspected anchors',
        [claim for record in primary['sources'] for claim in record['supported_claims']], primary['sources']),
        engine.source('exec14_causalnex_oracle', 'Exact preprocessing, cycle-pruning and threshold references',
        'Causal banking proposal', 'project_derivation', 'Project-authored algebraic examples', '2026-10-14',
        work.BASE/'exact-oracle.json', 'Threshold equality, two-cycle unit change, shifted fixed-direction regression',
        ['Exact imposed examples illustrate semantic changes; no upstream run or causal performance claim.'],
        [{'local_copy':ref(ROOT/'tools/review_causalnex_reuse_20261014.py', 'Fraction-based independent calculations')}])]
    BASE.mkdir(exist_ok=True)
    write(BASE/'source-audit.json', {'cutoff':'2026-10-07', 'sources':sources,
        'prior':ref(PRIOR,'516 inherited cited records')})
    bib = []
    for source in sources:
        bib.append('@misc{'+source['integrated_citation_key']+',\n author={{'+engine.shared.escape(source['author'])+
            '}},\n title={'+engine.shared.escape(source['title'])+'},\n year={2026},\n note={'+
            engine.shared.escape(source['version_date'])+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib))
    text = OLD.read_text()
    marker = r'\input{program/execution/2026-10-14/causalml-reuse/decision.tex}'
    assert text.count(marker) == 1
    text = text.replace(marker, marker+'\n'+r'\input{program/execution/2026-10-14/causalnex-reuse/decision.tex}')
    text = re.sub(r'\\bibliography\{([^}]+)\}', lambda m:r'\bibliography{'+m.group(1)+
        ',program/execution/2026-10-14/causalnex-reuse/publication/refs}', text)
    DRIVER.write_text(text)
    write(BASE/'prepared-inputs.json', {'inputs':[ref(p,'Preserved or reviewed input') for p in
        [OLD, PRIOR, work.OUTPUT, work.BASE/'primary-review.json', work.BASE/'exact-oracle.json',
         work.BASE/'decision.tex', work.BASE/'plan-review.md', Path(__file__)]],
        'generated':[ref(p,'Successor source') for p in [DRIVER, BASE/'source-audit.json', BASE/'refs.bib']],
        'credit_policy':'No automatic depth credit or mandatory repair closure.', 'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)), 'new_sources':2}))


def build():
    configure()
    engine.build()
    report = json.loads((OUT/'build-report.json').read_text())
    aux = (OUT/(NAME+'.aux')).read_text()
    report.update(builder=ref(Path(__file__),'Preserving lifecycle reader with inherited compile engine'),
        predecessor_pdf=ref(OLD.with_suffix('.pdf'),'Frozen702-page working reader'),
        lifecycle_sections={name:int(re.search(r'\\newlabel\{exec14:'+name+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
                            for name in ['causalnex','causalnex-end']})
    engine.core.write(OUT/'build-report.json',report)
    result = trace.audit(DRIVER, OUT/'source-audit.json')
    write(BASE/'traceability-review.json',result)
    assert result['status']=='pass' and not result['issues']
    print(json.dumps({'pages':report['pages'], 'cited_records':report['cited_records'],
        'sections':report['lifecycle_sections'], 'scholarly_pdfs':result['scholarly_pdfs']}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
