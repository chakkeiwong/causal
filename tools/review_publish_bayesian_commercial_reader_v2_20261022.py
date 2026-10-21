#!/usr/bin/env python3
"""Publish the explicit saved-anchor repair and renew reviews of its exact bytes."""
import argparse
import json
from pathlib import Path
import build_bayesian_commercial_reader_v2_20261022 as build
import review_publish_bayesian_commercial_reader_20261022 as engine
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run,core,ROOT=engine.run,engine.core,build.ROOT
BASE,OUT=build.BASE,build.OUT
PRIOR=ROOT/'docs/program/execution/2026-10-22/bayesian-commercial-v1'
read=lambda p:json.loads(p.read_text())


def configure():
    engine.build=build;engine.BASE=BASE;engine.OUT=OUT


def review():
    configure();verify_bindings(read(BASE/'anchor-repair-review.json'));engine.review()


def publish():
    configure();report,_=engine.verify()
    review_record=read(BASE/'release-source-review.json');verify_bindings(review_record)
    repair=read(BASE/'anchor-repair-review.json');verify_bindings(repair)
    state=core.read(ROOT,core.STATE);before=core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    prior_release=read(PRIOR/'working-release.json')
    assert run.same_reader(state['reader'],prior_release['pdf'])
    evidence=review_record['evidence']+[ref(BASE/'anchor-repair-review.json','Explicit corrected-anchor review'),
        ref(BASE/'operation-followup.json','Corrected coverage evidence successor'),ref(Path(__file__),'Exact repair publication')]
    manifest=dict(kind='working_monograph',final_acceptance=False,pdf=report['pdf'],pages=report['pages'],
        supersedes={k:state['reader'][k] for k in ['path','sha256']},
        build_report=ref(OUT/'build-report.json','Preserving corrected-anchor successor'),
        source_review=ref(BASE/'release-source-review.json','Source, arithmetic and original-content preservation'),
        anchor_repair=ref(BASE/'anchor-repair-review.json','Same science and source bytes; corrected saved snippets'),
        text_layout=ref(OUT/'text-layout-review.json','All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+evidence,
        changes=['Preserve the first Bayesian/state release and repair saved line anchors using newline-only indexing; no scientific claims changed.'],
        visual_acceptance=False,mandatory_repairs_closed=[],sponsor_binding='Pair sponsor to this repaired exact reader.')
    write(BASE/'working-release.json',manifest)
    binding=ref(BASE/'working-release.json','Reviewed anchor-repaired working successor')
    run.ledger.validate_working_release(ROOT,binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader']={k:report['pdf'][k] for k in ['path','sha256']}
    state['reader'].update(pages=report['pages'],status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT,before,state,dict(action='publish_bayesian_anchor_repair',manifest=binding,final_acceptance=False))
    print(json.dumps(dict(published=state['reader'],anchor_repair='pass',proposal_accepted=False)))


def renew():configure();engine.renew()


if __name__=='__main__':
    commands=dict(review=review,publish=publish,renew=renew)
    p=argparse.ArgumentParser();p.add_argument('command',choices=commands)
    commands[p.parse_args().command]()
