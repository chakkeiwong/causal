#!/usr/bin/env python3
"""Corrected-anchor successor; preserve the original publication and source bytes."""
import argparse
import re
import build_bayesian_commercial_reader_20261022 as original

ROOT,DOCS=original.ROOT,original.DOCS
BASE=DOCS/'program/execution/2026-10-22/bayesian-commercial-v2'
OUT=BASE/'reader'
PREDECESSOR,OLD,PRIOR=original.PREDECESSOR,original.OLD,original.PRIOR
NAME='causal_proposal_bayesian_commercial_reviewed_v2_2026-10-22'
DRIVER=DOCS/(NAME+'.tex')
PDF=DRIVER.with_suffix('.pdf')
DEVELOPMENT=BASE/'development.tex'
LABELS=original.LABELS


def expected_driver():
    text=OLD.read_text();marker=r'\input{program/execution/2026-10-17/s8/publication-v3/chapter.tex}'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'\n'+r'\input{program/execution/2026-10-22/bayesian-commercial-v2/development.tex}')
    return re.sub(r'\\bibliography\{([^}]+)\}',
        lambda m:r'\bibliography{'+m.group(1)+','+str((BASE/'refs').relative_to(DOCS))+'}',text)


def configure():
    for name in ['BASE','OUT','NAME','DRIVER','PDF','DEVELOPMENT']:
        setattr(original,name,globals()[name])
    original.expected_driver=expected_driver


def prepare():configure();original.prepare()
def build():configure();original.build()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','build'])
    {'prepare':prepare,'build':build}[p.parse_args().command]()
