#!/usr/bin/env python3
"""Prepare the reviewed working release and scoped active-design task receipt."""
import json
from pathlib import Path
import re

import build_active_reader_20261013 as builder
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = builder.BASE
OUT = builder.OUT
OP = 'LL.TASK.active_experiments'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    prior = json.loads(builder.PRIOR_AUDIT.read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    assert trace['status'] == 'pass' and not trace['issues']
    assert trace['pdf']['sha256'] == report['pdf']['sha256']
    assert state['reader']['sha256'] == report['predecessor_pdf']['sha256']
    for n in ['source-audit.json', 'author-review.json', 'primary-reinspection.json', 'exact-review.json', 'prepared-inputs.json', 'reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE / n).read_text()))
    previous = {x['integrated_citation_key']: x for x in prior['sources']}
    current = {x['integrated_citation_key']: x for x in audit['sources']}
    assert len(current)-len(previous) == 7
    assert all(current[k] == v for k, v in previous.items())
    old_files = [x for x in prior['tex_files'] if x['path'] != str(builder.OLD.relative_to(ROOT))]
    for item in old_files: core.bound(ROOT, item)
    assert builder.DRIVER.read_text() == builder.expected_driver()
    assert report['pages'] > 571
    assert not any(any(t in w.lower() for t in ['overfull', 'undefined', 'missing character']) for w in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['Choosing the next experiment', '115 matched evaluable', '60.8%',
                   'all-attempt net value', 'first remaining protocol', '0.278', '1024']:
        assert phrase in text, phrase
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == report['pages']
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    output = ROOT / node['outputs'][0]
    assert output.is_file()
    names = ['plan-review.md', 'source-audit.json', 'primary-reinspection.json', 'exact-results.json',
             'exact-replay.json', 'exact-review.json', 'author-review.json', 'acquisition-review.json',
             'candidate-register.json', 'omissions-register.json', 'prepared-inputs.json', 'refs.bib',
             'traceability-review.json', 'execution-review.md']+[f'fetch-{i:02}.json' for i in range(1,5)]
    evidence = [ref(BASE / n, n) for n in names]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Preserving reader delta and scoped active-experiment literature/design synthesis',
        'prior_citation_records_unchanged': len(previous), 'old_compiled_files_unchanged': len(old_files),
        'new_citation_records': 7, 'chapter_pages': report['active_experiments'],
        'findings': ['Connected banking argument develops information/decision value, timing, costs and actionable alternatives.',
                     'Five primary papers and three pinned source comparisons preserve favorable/adverse findings and unresolved identities.',
                     'Exact rational replay and independent conditional stopping calculation pass.',
                     'Compilation, exact-reader traceability and physical text bounds pass; no visual acceptance.'],
        'evidence': evidence+[ref(BASE / 'chapter.tex', 'Reviewed chapter'), ref(output, 'Reviewed scoped task synthesis'),
                              ref(OUT / 'build-report.json', 'Compiled preserving reader'),
                              ref(OUT / 'text-layout-review.json', 'Text bounds')],
        'visual_acceptance': False, 'frontier_census_closed': False, 'runtime_qualification': False}
    core.write(BASE / 'release-source-review.json', review)
    code = ['active_experiments_examples_20261013.py', 'review_active_experiments_examples_20261013.py',
            'audit_active_experiments_20261013.py', 'review_active_experiments_20261013.py',
            'build_active_reader_20261013.py', 'prepare_active_release_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Working active-experiment reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed bounded claims and preservation'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
        'source_artifacts': audit['tex_files']+evidence+[ref(output, 'Task synthesis'),
            ref(BASE / 'release-source-review.json', 'Release review')]+[ref(ROOT / 'tools' / n, 'Preserved construction/review/build code') for n in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Developed active-experiment literature/package comparison and exact decision-value banking constructions.'],
        'sponsor_binding': 'Prior sponsor preserved; exact-reader coherence remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed preserving active-experiment working reader')
    run.ledger.validate_working_release(ROOT, binding)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
        scope='Reviewed focused primary-literature/package comparison and exact planning example with explicit unresolved research',
        reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
        limitations=['Finite literature follow-up, not full frontier/MR02 or whole-proposal acceptance.',
                     'No live model, downloaded package, bank intervention or measured ROI.',
                     'Model likelihoods and dollar values are stipulated; missing originals/implementations and calibration remain explicit.',
                     'Author/source/text checks do not constitute independent or rendered visual acceptance.'],
        outputs=[ref(output, 'Reviewed active-experiment synthesis')], nonexecution_reason='', revisit_trigger='')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass',
         'finding': 'Five primary works and three pinned package sources compare favorable/adverse findings, concrete reuse/deferral, remedies and unresolved originals/implementations.',
         'evidence': [ref(BASE / n, n) for n in ['source-audit.json', 'primary-reinspection.json', 'omissions-register.json', 'author-review.json']]},
        {'index': 1, 'verdict': 'pass',
         'finding': 'Bank target and information clock, formal acquisition criterion, equal-budget alternatives and exact failure/stopping examples are explained and independently checked.',
         'evidence': [ref(BASE / 'chapter.tex', 'Developed target/clock/alternatives'), ref(BASE / 'exact-review.json', 'Exact replay and independent calculation'), binding]},
        {'index': 2, 'verdict': 'pass',
         'finding': 'Published evaluations are attributed and restricted; project results are exact stipulated planning values, with no live causal performance or bank truth claimed.',
         'evidence': [ref(BASE / 'author-review.json', 'Semantic limits'), ref(BASE / 'release-source-review.json', 'Release boundaries')]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'manifest': str((BASE / 'working-release.json').relative_to(ROOT)),
                      'receipt': str((BASE / 'operation-receipt.json').relative_to(ROOT)),
                      'pages': report['pages'], 'task_outcome': 'pass'}))


if __name__ == '__main__':
    main()
