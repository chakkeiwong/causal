#!/usr/bin/env python3
"""Preserve candidate and clarify the weighted-outcome identity and typography."""
import argparse
import json
from pathlib import Path
import build_commercial_survival_20261015 as previous
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
ROOT=previous.ROOT
BASE=previous.BASE.parent/'v3'
OUT=BASE/'reader'
OLD,PRIOR=previous.OLD,previous.PRIOR
NAME='causal_proposal_commercial_survival_v3_2026-10-15'
DRIVER=ROOT/'docs'/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')


def corrected(text):
    changes=[('stratification and proportional-'+chr(10)+'hazards diagnostics','stratification and proportional hazards diagnostics'),
             ('by summing the complete'+chr(10)+'sixteen-state law with weights','by averaging the default indicator $Y$ over the complete'+chr(10)+'sixteen-state law with weights')]
    for old,new in changes:
        assert text.count(old)==1
        text=text.replace(old,new)
    return text


def prepare():
    assert not DRIVER.exists()
    verify_bindings(json.loads((previous.OUT/'build-report.json').read_text()))
    BASE.mkdir(exist_ok=False)
    (BASE/'comparison.tex').write_text(corrected((previous.BASE/'comparison.tex').read_text()))
    (BASE/'refs.bib').write_bytes((previous.BASE/'refs.bib').read_bytes())
    write(BASE/'source-audit.json',json.loads((previous.BASE/'source-audit.json').read_text()))
    book=previous.DRIVER.read_text()
    for suffix in ['comparison.tex','refs']:
        old=str((previous.BASE/suffix).relative_to(ROOT/'docs'))
        assert book.count(old)==1
        book=book.replace(old,str((BASE/suffix).relative_to(ROOT/'docs')))
    DRIVER.write_text(book)
    write(BASE/'repair-review.json',{'reviewer':{'name':'Codex author/coordinator','kind':'author'},
        'prior_candidate':ref(previous.OUT/'build-report.json','Preserved unpublished785-page candidate'),
        'findings':['A source-line hyphen rendered proportional- hazards with a spurious space.',
                    'Weighted calculation wording now explicitly says to average Y, not merely the weights; the code already included Y.'],
        'scientific_change':'No equation, numeric result, assumption or source record changed.',
        'deferred_inherited_finding':'Adjacent CausalPy introductory citation lacks a preceding space; unchanged inherited source. Include in whole-reader editorial review.',
        'visual_acceptance':False})
    write(BASE/'prepared-inputs.json',{'prepared_on':'2026-10-15 Asia/Shanghai',
        'inputs':[ref(p,'Preserved reviewed input') for p in [OLD,PRIOR,previous.DRIVER,
                  previous.OUT/'build-report.json',previous.BASE/'comparison.tex',previous.BASE/'primary-review.json',
                  previous.BASE/'derivation-review.json',Path(__file__).resolve()]],
        'generated':[ref(p,'Reviewed successor') for p in [DRIVER,BASE/'comparison.tex',BASE/'refs.bib',BASE/'source-audit.json',BASE/'repair-review.json']],
        'visual_acceptance':False})
    print(json.dumps({'prepared':str(DRIVER.relative_to(ROOT)),'repairs':2}))


def build():
    for key,value in {'BASE':BASE,'OUT':OUT,'OLD':OLD,'PRIOR':PRIOR,'NAME':NAME,'DRIVER':DRIVER,'PDF':PDF}.items():
        setattr(previous,key,value)
    previous.build()
    report=json.loads((OUT/'build-report.json').read_text())
    report.update(builder=ref(Path(__file__).resolve(),'Preserving wording successor'),repair_review=ref(BASE/'repair-review.json','Two inspected corrections'))
    previous.engine.core.write(OUT/'build-report.json',report)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build']);a=p.parse_args()
    {'prepare':prepare,'build':build}[a.command]()
