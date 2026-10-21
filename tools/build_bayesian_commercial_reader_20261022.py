#!/usr/bin/env python3
"""Preserving reader successor using the frozen, parameterized build routine."""
import argparse
import json
from pathlib import Path
import re
import build_network_commercial_reader_20261020 as engine
import bayesian_state_reference_20261022 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-22/bayesian-commercial-v1'
OUT=BASE/'reader'
PREDECESSOR=DOCS/'program/execution/2026-10-21/prophets-repository-v1/publication-v2'
OLD=DOCS/'causal_proposal_prophets_repository_reviewed_v2_2026-10-21.tex'
PRIOR=PREDECESSOR/'reader/source-audit.json'
NAME='causal_proposal_bayesian_commercial_reviewed_2026-10-22'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=['exec22:state-'+x for x in ['scope','identification','selection','table','prior','clock','model',
    'smoothing','uncertainty','variance','approximation','bound','comparison']]
read=lambda p:json.loads(p.read_text())


def expected_driver():
    text=OLD.read_text()
    marker=r'\input{program/execution/2026-10-17/s8/publication-v3/chapter.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-22/bayesian-commercial-v1/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def configure():
    for name in ['ROOT','DOCS','BASE','OUT','PREDECESSOR','OLD','PRIOR','NAME','DRIVER','PDF','DEVELOPMENT','LABELS']:
        setattr(engine,name,globals()[name])
    engine.exact=exact
    engine.expected_driver=expected_driver


def prepare():
    configure()
    assert not DRIVER.exists() and not PDF.exists() and not OUT.exists()
    for n in ['source-audit.json','review.json','comparison-review.json','conversion-contract.json']:
        verify_bindings(read(BASE/n))
    assert exact.calculate()==read(BASE/'exact-results.json')
    entries=engine.sources()
    write(BASE/'manuscript-plan-review.json',dict(status='pass',
        evidence=[ref(DEVELOPMENT,'Connected banking argument'),ref(BASE/'plan.md','Reviewed program plan')],
        checks=['Preserve all predecessor sources, citation contexts and inputs.',
            'Separate five supported vendor profiles from five unresolved candidate families.',
            'Develop identification, filtering/smoothing, observability, uncertainty and numerical decision examples.',
            'Keep local process records out of the manuscript; qualify rights, native tests and cutoff identity.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_argument',issues=[],
        evidence=[ref(ROOT/'tools/bayesian_state_reference_20261022.py','Exact laws and two-route checks'),
            ref(BASE/'exact-results.json','Reproduced outputs'),ref(DEVELOPMENT,'Assumptions and derivations')],
        findings=['Complete joint laws agree while surgical default reductions are0 and3/5; model weights remain priors.',
            'Bayes enumeration and direct ratios agree at filter3/4 and smoother1/2; assumed margins15 and-10USD.',
            'Observability rank1 has null direction(1,-1); equal outputs do not identify the state contrast.',
            'Total variance separates1/6 and1/12; shared-parameter count variance2/3 differs from plug-in1/2.',
            'Expanded chain and compressed weighted mean both9/50; unweighted rows give1/2.',
            'TV inequality uses reward span and same fixed policy; geometric sum equals exact rational result.',
            'No empirical coverage, native behavior or measured economic benefit follows.'],
        native_execution=False,empirical_coverage=False,all_source_theorems_independently_verified=False))
    write(BASE/'copyedit-review.json',dict(status='pass',rendered_review=False,
        evidence=[ref(DEVELOPMENT,'Connected product narrative')],findings=[
            'Notation, timing and all hypothetical financial inputs are explained before decision comparisons.',
            'State, parameter, structural and simulation uncertainty remain distinct.',
            'Vendor strengths and unresolved technical sources are described without unsupported absence claims.',
            'No source bibliography is cited as an independently inspected scholarly paper.']))
    bib=[]
    for s in read(BASE/'source-audit.json')['sources']:
        note=(r'\url{'+s['source_identity']+'}; '+engine.shared.escape(s['version_date'])
              if s['source_identity'].startswith('https://') else engine.shared.escape(s['source_identity']+'; '+s['version_date']))
        bib.append('@misc{'+s['integrated_citation_key']+',\n author={{'+engine.shared.escape(s['author'])+'}},\n title={'+
            engine.shared.escape(s['title'])+'},\n year={'+str(s['year'])+'},\n note={'+note+'}\n}\n')
    (BASE/'refs.bib').write_text('\n'.join(bib));DRIVER.write_text(expected_driver())
    paths=[OLD,PRIOR,DEVELOPMENT,Path(__file__),ROOT/'tools/build_network_commercial_reader_20261020.py',
        ROOT/'tools/bayesian_state_reference_20261022.py']+[BASE/n for n in ['source-audit.json','review.json',
        'comparison-review.json','omissions-register.json','mathematical-review.json','copyedit-review.json',
        'manuscript-plan-review.json','exact-results.json']]
    write(BASE/'prepared-inputs.json',dict(inputs=[ref(p,'Reviewed preserving input') for p in paths],
        generated=[ref(DRIVER,'Preserving driver'),ref(BASE/'refs.bib','Added audited citations')],
        prior_cited_records=len(read(PRIOR)['sources']),expected_cited_records=len(entries),
        expected_scholarly_pdfs=read(PREDECESSOR/'traceability-review.json')['scholarly_pdfs'],visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),expected_records=len(entries))))


def build():
    configure();engine.build()


if __name__=='__main__':
    commands=dict(prepare=prepare,build=build)
    p=argparse.ArgumentParser();p.add_argument('command',choices=commands)
    commands[p.parse_args().command]()
