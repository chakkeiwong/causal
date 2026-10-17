#!/usr/bin/env python3
"""Preserve all failed candidates while adding reviewed S9 composition laws."""
import argparse
import copy
import json
import re
from pathlib import Path
import audit_reader_traceability_v2_20261013 as trace
import build_java_temporal_engine_20261016 as engine
import s9_retry_composition_20261017 as exact
from build_integrated_monograph_v12 import ref
from publish_latent_r_review_v2_20261013 import verify_bindings,write

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
BASE=DOCS/'program/execution/2026-10-17/s9'
PREVIOUS=BASE/'publication-v3';PUB=BASE/'publication-v4';OUT=PUB/'reader'
CANONICAL=DOCS/'program/execution/2026-10-17/s8/publication-v3'
CANONICAL_OLD=DOCS/'causal_proposal_commercial_gap_reviewed_v3_2026-10-17.tex'
OLD=DOCS/'causal_proposal_language_reuse_reviewed_v3_2026-10-17.tex'
NAME='causal_proposal_language_reuse_reviewed_v4_2026-10-17'
DRIVER=DOCS/(NAME+'.tex');PDF=DRIVER.with_suffix('.pdf')
CHAPTER=PUB/'chapter.tex';EXTENSION=BASE/'extension-v4.tex'
PRIOR=PREVIOUS/'reader/source-audit.json'


def read(p):return json.loads(p.read_text())


def expected_chapter():return (PREVIOUS/'chapter.tex').read_text().rstrip()+'\n\n'+EXTENSION.read_text()


def verify_exact():
    assert exact.serial(exact.calculate())==read(PUB/'exact-results.json')
    assert CHAPTER.read_text()==expected_chapter()


def prepare():
    assert not PUB.exists() and not DRIVER.exists() and not PDF.exists()
    PUB.mkdir()
    write(PUB/'exact-results.json',exact.serial(exact.calculate()))
    # Repair descriptive pointers; retain every original embedded source record.
    old=read(BASE/'completed-source-review.json');fixed=copy.deepcopy(old)
    sources={s['integrated_citation_key']:s for s in read(CANONICAL/'reader/source-audit.json')['sources']}
    repairs=[]
    for package,items in fixed['reviewed_packages'].items():
        for item in items:
            prior=item['source_audit_record'];key=prior['anchor'].split()[-1]
            assert key in sources
            item['source_audit_record']=ref(CANONICAL/'reader/source-audit.json','Exact integrated_citation_key='+key+'; original records and line anchors')
            item['authoritative_primary_record']=sources[key]['local_copy']
            repairs.append(dict(package=package,key=key,old_pointer=prior,replacement=item['source_audit_record']))
    fixed['status']='pass_bounded_primary_source_routes_with_repaired_pointers'
    fixed['supersedes']=ref(BASE/'completed-source-review.json','Preserved misleading descriptive pointers; embedded originals were available')
    fixed['pointer_repairs']=repairs
    fixed['limitations']+=['Completed means bounded source decisions only, not a resolved dependency/license inventory or executed upstream bridge.',
        'Corrected pointers refer to exact source keys in the canonical audit; primary records and inspected line anchors remain unchanged.']
    assert fixed['package_audit_records']==old['package_audit_records']
    verify_bindings(fixed);write(PUB/'primary-source-review-successor.json',fixed)
    CHAPTER.write_text(expected_chapter())
    source=dict(integrated_citation_key='exec17_s9_composition',
        title='Adaptive bridge composition and outcome-dependent retry laws',author='Causal banking proposal',
        kind='project_derivation',year=2026,source_identity='Authored finite laws and explicit conditional derivations',
        version_date='2026-10-17',local_copy=ref(PUB/'exact-results.json','retry_examples, affine_composition, inverse_selection'),
        inspected_anchors=['Exact finite attempt enumeration for K1–4','Affine two-stage recursion and attained bound',
            'Retained-result versus independent-redraw laws','Adaptive shared-state counterexample',
            'Inverse completion weighting expectation, variance and misspecification'],
        supported_claims=['Local errors compose under declared domain/Lipschitz assumptions; adaptive branch agreement needs sequential margins.',
            'Conditional kernels, not marginal laws, govern adaptive path equivalence.',
            'Independent-redraw and retained-result retry policies yield different all-assigned and completed laws.',
            'Persistent difficulty invalidates the independent-attempt completion formula.',
            'Inverse selection recovers a mean only under correct positivity and completion-law assumptions, with explicit variance cost.'],
        records=[ref(ROOT/'tools/s9_retry_composition_20261017.py','Fraction references plus independent attempt enumeration'),
                 ref(EXTENSION,'Equations and their derivations; authored examples, no upstream execution')],
        limitations=['Finite examples and conditional project derivations only; not measured runtime, port qualification, causal identification or bank calibration.',
                     'Uniform numerical and kernel bounds, positivity and failure laws require independent justification in an actual implementation.'])
    write(PUB/'source-audit.json',dict(sources=[source],cutoff='2026-10-07',prior=ref(PRIOR,'All730 previous records preserved')))
    (PUB/'refs.bib').write_text('@misc{exec17_s9_composition,\n author={{Causal banking proposal}},\n title={Adaptive bridge composition and outcome-dependent retry laws},\n year={2026},\n note={Authored conditional derivations and exact finite references}\n}\n')
    marker=r'\input{program/execution/2026-10-17/s9/publication-v3/chapter.tex}'
    raw=OLD.read_text();assert raw.count(marker)==1
    raw=raw.replace(marker,r'\input{program/execution/2026-10-17/s9/publication-v4/chapter.tex}')
    raw=re.sub(r'\\bibliography\{([^}]+)\}',lambda m:r'\bibliography{'+m.group(1)+',program/execution/2026-10-17/s9/publication-v4/refs}',raw)
    DRIVER.write_text(raw)
    write(PUB/'mathematics-review.json',dict(status='pass',reviewer=dict(name='Codex author/coordinator',kind='author'),
        checks=exact.serial(exact.calculate())['checks'],derivation_review=[
            'Triangle inequality induction requires both trajectories in the same certified domain.',
            'Finite-kernel common-mass coupling applies only on common reachable histories; continuous values need metric/margin treatment.',
            'First-success and retained-result laws are separately derived; failed calls remain in all-assigned denominators.',
            'Missing-result bounds use a fixed latent result per request, and cannot recover the first-draw target from later independent redraws.',
            'Operating payoff state V is distinct from randomized computation result Y.',
            'Inverse weighting is a functional correction and not reproduced output law; unknown failure law and infinite variance remain explicit.'],
        evidence=[ref(EXTENSION,'Inspected definitions, algebra and domain limits'),ref(PUB/'exact-results.json','Independent finite enumeration'),
                  ref(ROOT/'tools/s9_retry_composition_20261017.py','Exact calculation')],visual_acceptance=False))
    write(PUB/'prepared-inputs.json',dict(inputs=[ref(OLD,'Preserved v3 driver'),ref(PRIOR,'730-record audit'),
        ref(PREVIOUS/'chapter.tex','Frozen prior chapter'),ref(EXTENSION,'Substantive composition extension'),
        ref(PUB/'source-audit.json','One new project derivation'),ref(PUB/'primary-source-review-successor.json','Corrected provenance pointers'),
        ref(PUB/'mathematics-review.json','Conditional mathematical review'),ref(BASE/'recovery-extension-plan-v4.md','Reviewed recovery plan'),
        ref(Path(__file__),'Preserving builder')],generated=[ref(DRIVER,'v4 driver'),ref(CHAPTER,'Preserving v4 chapter'),ref(PUB/'refs.bib','New reference')],
        previous_records=730,added_records=1,visual_acceptance=False))
    print(json.dumps(dict(prepared=str(DRIVER.relative_to(ROOT)),repaired_pointers=len(repairs),source_records=731)))


def build():
    verify_bindings(read(PUB/'prepared-inputs.json'));verify_exact()
    assert not OUT.exists() and not PDF.exists()
    engine.BASE=PUB;engine.OUT=OUT;engine.OLD=OLD;engine.NAME=NAME
    engine.DRIVER=DRIVER;engine.PDF=PDF;engine.PRIOR_AUDIT=PRIOR
    engine.build()
    report=read(OUT/'build-report.json');assert report['cited_records']==731
    idx=trace.audit(DRIVER,OUT/'source-audit.json');write(PUB/'traceability-review.json',idx)
    assert idx['status']=='pass' and not idx['issues'] and idx['scholarly_pdfs']==188
    write(PUB/'build-review.json',dict(status='pass',reader=report['pdf'],pages=report['pages'],cited_records=731,
        scholarly_pdfs=188,material_warnings=[w for w in report['warnings'] if 'Underfull' not in w],visual_acceptance=False))
    print(json.dumps(dict(pages=report['pages'],cited_records=731,traceability='pass',visual_acceptance=False)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()
