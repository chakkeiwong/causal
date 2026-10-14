#!/usr/bin/env python3
"""Prepare the reviewed I4 chapter outcome and preserving working release."""
import json
from pathlib import Path
import re

import build_operations_reader_20261013 as builder
import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = builder.BASE
OUT = builder.OUT
OP = 'TEXT.DRAFT.I4'
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
    for n in ['source-audit.json', 'author-review.json', 'source-and-fault-review.json', 'exact-review.json', 'prepared-inputs.json', 'reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE / n).read_text()))
    previous = {x['integrated_citation_key']: x for x in prior['sources']}
    current = {x['integrated_citation_key']: x for x in audit['sources']}
    assert len(current)-len(previous) == 3
    assert all(current[k] == v for k, v in previous.items())
    for item in prior['tex_files']: core.bound(ROOT, item)
    assert builder.DRIVER.read_text() == builder.expected_driver()
    assert (BASE / 'integration-preserving.tex').read_text() == builder.expected_wrapper()
    assert report['pages'] > 581
    assert not any(any(t in w.lower() for t in ['overfull', 'undefined', 'missing character']) for w in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['Checkpoint invariants', '0.8991', '0.993141', '0.142625',
                   'every attempted request', 'selected fingerprint', '100 unique entries']:
        assert phrase in text, phrase
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == report['pages']
    source_review = json.loads((BASE / 'source-and-fault-review.json').read_text())
    assert source_review['matches_fault_execution_source_digest']
    (BASE / 'execution-review.md').write_text('''# Operational adoption execution review\n\nThe chapter retains all previously delivered operating paragraphs and the existing I1/I2/I3 chapters. New material develops selected versus complete execution identities, checkpoint invariants, publication/cancellation boundaries, retry dependence, statistical redraw, ownership and all-attempt costs.\n\nThe preserved nine fault cases were inspected, including 100 unique completed work IDs after two worker starts. The selected current source digest matches that replay. No new runtime, MCP, platform or bank trial is claimed. Four exact project constructions replay identically; independent finite enumerations check retry and cost arithmetic.\n\nPreparation caught two path assumptions before publication: the request/response schemas are located in the inspected service's IN02 contract directory, and the current reader reaches its operating text through workspace/integration-tail.tex rather than the historical IN06 whole-chapter include. Both were repaired using the actual source and compiled-file inventory. The builder's preservation assertions passed afterward; no delivered predecessor was edited.\n\nThe final build, whole-reader source traceability and text bounds pass. Visual acceptance remains pending under the inherited image allowance. Record the chapter outcome, publish this working release and continue eligible work. Q4 must be re-reviewed against this reader before its earlier-reader pass can carry forward.\n''')
    names = ['plan-review.md', 'source-audit.json', 'source-and-fault-review.json', 'exact-results.json',
             'exact-replay.json', 'exact-review.json', 'author-review.json', 'prepared-inputs.json',
             'refs.bib', 'traceability-review.json', 'execution-review.md', 'inherited-operations.tex', 'development.tex']
    evidence = [ref(BASE / n, n) for n in names]
    review = {'status': 'pass', 'issues': [], 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Developed I4 chapter and preserving working-reader integration',
        'prior_citation_records_unchanged': len(previous), 'new_citation_records': 3,
        'chapter_pages': report['operational_adoption'],
        'findings': ['Earlier operating paragraphs, I1/I2/I3 includes and all earlier cited source records are preserved.',
            'Current selected source identity matches the actual preserved fault replay; claim boundaries are explicitly narrower than production qualification.',
            'Exact failure/cost/retry/recovery constructions reproduce and independent enumerations pass.',
            'Compilation, exact-reader traceability and physical text bounds pass; visual acceptance remains pending.'],
        'evidence': evidence+[ref(builder.CHAPTER, 'Developed I4 chapter'), ref(OUT / 'build-report.json', 'Preserving final build'),
                              ref(OUT / 'text-layout-review.json', 'Text bounds')],
        'visual_acceptance': False, 'MR03_acceptance': False, 'runtime_qualification': False}
    core.write(BASE / 'release-source-review.json', review)
    code = ['operation_planning_examples_20261013.py', 'prepare_operational_adoption_20261013.py',
            'build_operations_reader_20261013.py', 'prepare_operations_release_20261013.py']
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Working operations reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed preserved and new claims'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
        'source_artifacts': audit['tex_files']+evidence+[ref(BASE / 'release-source-review.json', 'Release review')]
            +[ref(ROOT / 'tools' / n, 'Preserved source/review/build code') for n in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Developed I4 operational adoption, fault/compatibility/ownership and whole-cost argument.'],
        'sponsor_binding': 'Prior sponsor preserved; exact-reader coherence remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed preserving operations working reader')
    run.ledger.validate_working_release(ROOT, binding)
    graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, OP)
    assert node['outputs'] == [str(builder.CHAPTER.relative_to(ROOT))]
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope='Developed source-audited operating chapter with exact project examples',
        reviewer=review['reviewer'], limitations=['Draft chapter completion is not MR03 depth/coverage acceptance.',
            'No new runtime/MCP, multi-host, consumer, bank or platform qualification.',
            'All new failure probabilities, costs and utilities are planning assumptions.',
            'Author/source/text review is not independent or visual acceptance.'],
        outputs=[ref(builder.CHAPTER, 'Completed developed I4 chapter')], nonexecution_reason='', revisit_trigger='')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass', 'finding': 'Connected banking argument develops formal recovery invariants, retry/selection mechanisms, resource and cancellation limits, semantic alternatives, ownership and complete cost accounting.',
         'evidence': [ref(builder.CHAPTER, 'Developed chapter'), ref(BASE / 'exact-review.json', 'Independent exact checks'), binding]},
        {'index': 1, 'verdict': 'pass', 'finding': 'New claims bind inspected runtime snapshots, actual preserved fault evidence or explicitly stipulated reproducible examples. Existing citations are preserved and final exact-reader traceability passes.',
         'evidence': [ref(BASE / 'source-audit.json', 'Audited claims and anchors'), ref(BASE / 'author-review.json', 'Semantic review'),
                      ref(BASE / 'traceability-review.json', 'Whole-reader identities')]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'pages': report['pages'], 'receipt': str((BASE / 'operation-receipt.json').relative_to(ROOT)),
                      'manifest': str((BASE / 'working-release.json').relative_to(ROOT)), 'outcome': 'pass'}))


if __name__ == '__main__':
    main()
