#!/usr/bin/env python3
"""Publish reviewed V13 execution evidence through the original atomic writer."""
import json
from pathlib import Path

import master_control as core
import causal_program_v13 as control
import build_gap_successor_v13 as book

ROOT=core.ROOT
BASE=ROOT/control.BASE


def ref(path,anchor):return {'path':str(path.relative_to(ROOT)),'sha256':core.sha(path),'anchor':anchor}


def main():
    control.install_hooks()
    state=core.read(ROOT,core.STATE)
    before=core.sha(ROOT/core.STATE)
    if state.get('successor_document'):raise ValueError('Successor already published; preserve its bytes')
    book.check()
    report=core.read(ROOT,str((book.OUT/'build-report.json').relative_to(ROOT)))
    layout=core.read(ROOT,str((book.OUT/'text-layout-review.json').relative_to(ROOT)))
    if layout['status']!='pass' or layout['pages']!=report['pages']:
        raise ValueError('Text/layout checks do not match successor')
    state['successor_document']=ref(book.OUT/'build-report.json','Compiled source-audited successor book; visual review pending')
    state['reader']={'path':report['pdf']['path'],'sha256':report['pdf']['sha256'],'pages':report['pages'],
                     'status':'Working V13 successor; all three substantive repairs and final visual review remain open; not I02'}
    state['deliveries'].append(dict(state['reader']))
    documents=state['gap_execution']['documents']
    paths={
        'book_report':book.OUT/'build-report.json','book_audit':book.OUT/'source-audit.json',
        'book_review':book.OUT/'review.md','book_layout':book.OUT/'text-layout-review.json',
        'chapter_progress':book.OUT/'chapter-progress.json','book_builder':ROOT/'tools/build_gap_successor_v13.py',
        'book_reviewer':ROOT/'tools/review_gap_reader_v13.py','book_tests':ROOT/'tests/test_gap_reader_v13.py',
        'publisher':Path(__file__),'continuation':BASE/'continuation.md','remaining_gaps':BASE/'remaining-gaps.md',
        'software_audit':BASE/'work/SW01/source-audit.json','software_coverage':BASE/'work/SW01/coverage-matrix.json',
        'software_catalog':BASE/'work/SW01/catalog.json','software_dossiers':BASE/'work/SW01/dossiers.md',
        'software_review_builder':ROOT/'tools/inspect_gap_sources_v13.py',
        'acquisition_review':BASE/'acquisition-review.md','acquisition_identities':BASE/'source-identities.json',
        'acquisition_report':ROOT/'docs/program/repair-v12/source-collection/batch-gap3-primary-20261012T093116875548Z/report.json',
        'verification':BASE/'prepublication-verification.json'}
    for key,path in paths.items():documents[key]=ref(path,'V13 execution: '+key)
    book.check(state['successor_document'])
    issues=control.validate_state(ROOT,state)
    if issues:raise ValueError(str(issues))
    core.commit_state(ROOT,before,state,{'action':'publish_v13_source_reviews_and_main_book',
       'reader':state['reader'],'completed_preparation':['RG1','X00'],
       'source_reviews_added':10,'partial_software_cells':29,'major_repairs_closed':[],
       'visual_acceptance':False,'qualification_claim':False})
    print(json.dumps({'published':True,'pages':report['pages'],'recorded_outcomes':len(state['results']),
                      'work_packages':len(state['work_packages']),'qualified_gaps':0}))


if __name__=='__main__':main()
