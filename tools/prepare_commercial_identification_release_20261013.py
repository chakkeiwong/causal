#!/usr/bin/env python3
"""Prepare an honest working release and reviewed commercial coverage receipt."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/commercial-identification'
OUT = BASE / 'reader'
OP = 'SW.CELL.identification_counterfactual.commercial'
ref = shared.ref


def main():
    state = core.read(ROOT, core.STATE)
    report = json.loads((OUT / 'build-report.json').read_text())
    audit = json.loads((OUT / 'source-audit.json').read_text())
    old = ROOT / 'docs/causal_proposal_dependent_learning_2026-10-13.tex'
    prior = json.loads((ROOT / 'docs/program/execution/2026-10-13/dependent-learner/reader/source-audit.json').read_text())
    trace = json.loads((BASE / 'traceability-review.json').read_text())
    assert trace['status'] == 'pass' and trace['issues'] == []
    assert trace['pdf']['sha256'] == report['pdf']['sha256']
    assert state['reader']['sha256'] == report['predecessor_pdf']['sha256']
    for name in ['author-review-final.json', 'source-audit.json', 'prepared-inputs.json', 'reader/source-audit.json']:
        shared.verify_refs(json.loads((BASE / name).read_text()))
    previous = {x['integrated_citation_key']: x for x in prior['sources']}
    current = {x['integrated_citation_key']: x for x in audit['sources']}
    assert len(current)-len(previous) == 10
    assert all(current[k] == v for k, v in previous.items())
    old_files = [x for x in prior['tex_files'] if x['path'] != str(old.relative_to(ROOT))]
    for item in old_files:
        core.bound(ROOT, item)
    marker = r'\input{program/execution/2026-10-13/commercial-temporal/comparison.tex}'
    expected = old.read_text().replace(marker, marker + '\n' +
        r'\input{program/execution/2026-10-13/commercial-identification/comparison-final.tex}', 1)
    expected = expected.replace('program/execution/2026-10-13/dependent-learner/refs}',
        'program/execution/2026-10-13/dependent-learner/refs,program/execution/2026-10-13/commercial-identification/refs}', 1)
    assert (ROOT / report['driver']['path']).read_text() == expected
    assert not any('overfull' in w.lower() or 'undefined' in w.lower() or 'missing character' in w.lower() for w in report['warnings'])
    text = re.sub(r'\s+', ' ', (OUT / 'reader.txt').read_text())
    for phrase in ['sixteen commercial families', '27 bounded', 'Abduction', '16 resulting vertices',
                   '0.24', '0.44', 'USD 270', 'USD 730']:
        assert phrase in text, phrase
    assert (BASE / 'exact-results.json').read_bytes() == (BASE / 'exact-replay.json').read_bytes()
    names = ['search-protocol.json', 'local-search.json', 'followup-plan.json', 'followup-plan-02.json',
             'acquisition-review.json', 'candidate-register.json', 'omissions-register.json', 'source-audit.json',
             'exact-results.json', 'exact-replay.json', 'author-review-final.json', 'prepared-inputs.json',
             'refs.bib', 'traceability-review.json']
    names += [f'acquisition-{i:02d}.json' for i in range(1, 9)]
    evidence = [ref(BASE / n, n) for n in names]
    review = {
        'status': 'pass', 'issues': [],
        'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
        'scope': 'Preserving working-reader delta with explicit unresolved commercial coverage',
        'old_compiled_files_unchanged': len(old_files), 'prior_citation_records_unchanged': len(previous),
        'new_citation_records': 10,
        'findings': [
            'Nine developed pages distinguish adjustment, general identification, individual counterfactuals, mediation and bounds.',
            'Commercial strengths and local capability gaps are matched to inspected primary technical passages; metadata-only Mplus leads are restricted to discovery claims.',
            'All four exact constructions reproduce; hypothetical dollars do not claim measured bank economics.',
            'Unavailable originals, source/edition/rights unknowns and post-cutoff acquisition limits remain explicit; no vendor runtime or full-cell acceptance.',
            'The final text corrects the extracted integral punctuation while retaining the checkpoint-bound draft and review.',
            'Compilation, exact-reader traceability and whole-reader physical text bounds pass; visual acceptance remains pending.'
        ], 'evidence': evidence + [ref(BASE / 'comparison-final.tex', 'Reviewed final chapter'),
                                   ref(OUT / 'build-report.json', 'Final integrated build'),
                                   ref(OUT / 'text-layout-review.json', 'Text bounds')],
        'visual_acceptance': False}
    core.write(BASE / 'release-source-review.json', review)
    code = ['prepare_commercial_identification_20261013.py', 'normalize_commercial_identification_20261013.py',
            'audit_commercial_identification_20261013.py', 'commercial_identification_examples_20261013.py',
            'build_commercial_identification_reader_20261013.py', 'prepare_commercial_identification_release_20261013.py']
    release = {
        'kind': 'working_monograph', 'final_acceptance': False,
        'pdf': report['pdf'], 'pages': report['pages'],
        'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Final 571-page working reader'),
        'source_review': ref(BASE / 'release-source-review.json', 'Reviewed bounded claims'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical text bounds'),
        'source_artifacts': audit['tex_files'] + evidence
            + [ref(BASE / 'release-source-review.json', 'Release review')]
            + [ref(ROOT / 'tools' / name, 'Preserved search/audit/construction/build code') for name in code],
        'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Integrated developed commercial identification/counterfactual comparisons and exact lending examples.'],
        'sponsor_binding': 'Prior sponsor preserved; exact-reader coherence remains Q5 work.'}
    core.write(BASE / 'working-release.json', release)
    binding = ref(BASE / 'working-release.json', 'Reviewed preserving commercial identification reader')
    run.ledger.validate_working_release(ROOT, binding)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    coverage = {
        'operation': OP, 'outcome': 'inconclusive', 'execution': 'performed',
        'scope': 'Developed sixteen-family bounded comparison with exact lending constructions and explicit missing technical/edition evidence',
        'candidate_register': ref(BASE / 'candidate-register.json', 'Every declared alias searched'),
        'source_audit': ref(BASE / 'source-audit.json', 'Primary claim identities and inspected anchors'),
        'review': ref(BASE / 'author-review-final.json', 'Substantive argument and alternatives review'),
        'omissions': ref(BASE / 'omissions-register.json', 'Unclosed essential comparisons'),
        'working_reader': binding, 'full_cell_coverage_accepted': False,
        'runtime_qualified': False, 'original_gap_qualification': False}
    output = ROOT / node['outputs'][0]
    core.write(output, coverage)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed', scope=coverage['scope'],
                   reviewer={'name': 'Codex author/coordinator', 'kind': 'author'},
                   limitations=['The declared finite corpus is not a complete market or exact-cutoff census.',
                                'Essential technical methods, versioned APIs and rights remain unresolved for multiple families.',
                                'No paid vendor execution, bank evidence, whole MR01 closure or rendered visual acceptance.'],
                   outputs=[ref(output, 'Reviewed commercial coverage disposition')], nonexecution_reason='',
                   revisit_trigger='Acquire the family-specific missing primary texts, API/edition and rights records in the omissions register, then use a reviewed successor comparison.')
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'inconclusive',
         'finding': 'All sixteen declared families and aliases received finite local/source searches under explicit cutoff and 27-request bounds; unresolved primary/alias/edition coverage prevents complete-cell acceptance.',
         'evidence': [ref(BASE / 'search-protocol.json', 'Declared candidates and stopping rule'),
                      ref(BASE / 'candidate-register.json', 'Completed literal searches and dispositions'),
                      ref(BASE / 'acquisition-review.json', 'Successful and failed official requests')]},
        {'index': 1, 'verdict': 'pass',
         'finding': 'Every newly asserted technical/documentary or project claim binds authentic bytes, identity/version limits, hashes and inspected anchors; exact examples reproduce and final reader traceability passes.',
         'evidence': [ref(BASE / 'source-audit.json', 'Ten audited records'),
                      ref(BASE / 'author-review-final.json', 'Substantive review'),
                      ref(BASE / 'traceability-review.json', 'Final exact-reader audit')]},
        {'index': 2, 'verdict': 'inconclusive',
         'finding': 'Alternatives and adoption routes are explicit; no essential unavailable original, technical comparison or license/API question is waived or converted into a capability absence claim.',
         'evidence': [ref(BASE / 'omissions-register.json', 'Unclosed sources and revisit actions'), binding]}]
    core.write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps({'manifest': str((BASE / 'working-release.json').relative_to(ROOT)),
                      'receipt': str((BASE / 'operation-receipt.json').relative_to(ROOT)),
                      'pages': report['pages'], 'coverage': 'inconclusive'}))


if __name__ == '__main__':
    main()
