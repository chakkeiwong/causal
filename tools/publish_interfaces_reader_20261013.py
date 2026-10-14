#!/usr/bin/env python3
"""Publish the reviewed working I2 successor and prepare its scoped draft receipt."""
import json
from pathlib import Path
import re

import build_integrated_monograph_v12 as shared
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/interfaces'
OUT = BASE / 'reader'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.I2/chapter.tex'
ref = shared.ref


def write(path, value):
    if path.exists():
        raise ValueError('Preserve frozen evidence: ' + str(path))
    core.write(path, value)


def main():
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'TEXT.DRAFT.I2'
    assert state['reader']['path'] == 'docs/causal_proposal_census_2026-10-13.pdf'
    report = core.read(ROOT, str((OUT / 'build-report.json').relative_to(ROOT)))
    audit = json.loads((OUT / 'source-audit.json').read_text())
    shared.verify_refs(audit)
    shared.verify_refs(json.loads((BASE / 'prepared-inputs.json').read_text()))
    bounds = json.loads((OUT / 'text-layout-review.json').read_text())
    assert bounds['status'] == 'pass' and bounds['pages'] == report['pages']
    assert not any('Overfull' in w or 'undefined' in w for w in report['warnings'])
    assert 10 <= report['i2']['physical_span'] <= 16
    log = (OUT / 'causal_proposal_interfaces_2026-10-13.log').read_text()
    assert 'build-failure-' not in log
    bbl = (OUT / 'causal_proposal_interfaces_2026-10-13.bbl').read_text()
    assert r'\natexlab{aa}' in bbl and r'\natexlab{{}' not in bbl
    pages = (OUT / 'reader.txt').read_text().split('\f')
    first = next(i for i, p in enumerate(pages)
                 if 'Chapter 39' in p and 'An interface must preserve a scientific question' in p)
    body = pages[first:first + report['i2']['physical_span']]
    assert len(body) == 11 and 'What the evidence supports' in body[-1]
    assert 'claim.Causal' not in ''.join(body) and 'null.Causal' not in ''.join(body)
    text_review = {'status': 'pass', 'scope': 'I2 author source/text inspection; no rendered visual acceptance',
        'chapter': ref(CHAPTER, 'Eleven developed sections with runnable request and mathematical examples'),
        'pdf': report['pdf'], 'printed_span': report['i2'],
        'physical_pages': list(range(first+1, first+len(body)+1)),
        'page_word_counts': [len(p.split()) for p in body],
        'findings': ['Substantive argument, code, mathematical derivations and alternatives fill the eleven-page span.',
                     'No logs or catalogs receive body credit; formal chapter-depth acceptance remains a later operation.',
                     'Parenthetical citation spacing corrected after first text review; new code listings unchanged.',
                     'Extended suffix aa renders through the final bibliography; no preserved failed bibliography was used.'],
        'visual_acceptance': False}
    write(BASE / 'chapter-text-review.json', text_review)
    review_inputs = [BASE / 'substantive-review.md', BASE / 'source-audit.json', BASE / 'claim-map.json',
                    BASE / 'examples/review.json', BASE / 'printed-listings/review.json',
                    BASE / 'chapter-text-review.json', BASE / 'build-repair.json', BASE / 'build-repair-02.json',
                    BASE / 'bibliography-test.json', BASE / 'copyedit-review.json', OUT / 'source-audit.json']
    write(BASE / 'release-source-review.json', {
        'status': 'pass', 'issues': [], 'reviewer': {'name': 'Current author/coordinator', 'kind': 'author'},
        'scope': 'I2 incremental argument, implementation/source bindings, generated examples and preserving reader',
        'evidence': [ref(p, 'Reviewed bounded evidence') for p in review_inputs],
        'limits': ['Not visual acceptance', 'Not independent or bank acceptance',
                   'No new MCP execution; exact prior MCP trial retained', 'Whole-program Q1–Q5 remain open']})
    sources = list(audit['tex_files'])
    sources += [ref(p, 'Added source/evidence for the working successor') for p in
                [BASE / 'refs.bib', BASE / 'causalplainnat.bst', BASE / 'plainnat-upstream.bst',
                 BASE / 'prepared-inputs.json', BASE / 'source-audit.json', BASE / 'claim-map.json',
                 BASE / 'substantive-review.md', ROOT / 'tools/build_interfaces_reader_20261013.py', Path(__file__)]]
    release = {'kind': 'working_monograph', 'final_acceptance': False, 'pdf': report['pdf'],
        'pages': report['pages'], 'supersedes': {k: state['reader'][k] for k in ['path', 'sha256']},
        'build_report': ref(OUT / 'build-report.json', 'Compiled preserving successor'),
        'source_review': ref(BASE / 'release-source-review.json', 'Incremental author source and claim review'),
        'text_layout': ref(OUT / 'text-layout-review.json', 'Physical bounds and text review only'),
        'source_artifacts': sources, 'visual_acceptance': False, 'mandatory_repairs_closed': [],
        'changes': ['Developed I2 chapter: eleven pages on actual library/CLI/MCP paths and proposed client behavior.',
                    'Thirteen library/CLI examples, ten lifecycle checks and exact printed instructions executed.',
                    'Preserving bibliography-style repair supports more than 26 identical author/year citations.'],
        'sponsor_binding': 'Sponsor snapshot remains bound to the 475-page predecessor; Q5 must publish a preserving exact-reader refresh.'}
    release_path = BASE / 'working-release.json'
    write(release_path, release)
    binding = ref(release_path, 'Reviewed working interface-chapter delivery')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, {'action': 'publish_i2_working_reader', 'manifest': binding,
                                    'original_gap_qualification': False, 'final_acceptance': False})
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'TEXT.DRAFT.I2')
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
        scope='Developed I2 scholarly draft and integrated 496-page working reader; scoped local examples only',
        reviewer={'name': 'Current author/coordinator', 'kind': 'author'},
        limitations=['Chapter-specific coverage/depth acceptance remains TEXT.REVIEW.I2.',
                     'Visual acceptance remains pending under inherited image allowance.',
                     'No new MCP run, modern-protocol/HTTP acceptance, external client acceptance or bank validation.',
                     'MR03 and Q1–Q5 remain open.'],
        outputs=[ref(CHAPTER, 'Developed library, CLI, MCP and client-design chapter')])
    receipt['criteria'] = [
        {'index': 0, 'verdict': 'pass',
         'finding': 'Connected banking argument develops a full request, conditional identification, exact set algebra, uncertainty interpretation, client outcomes, context/custody, protocol negotiation, replay/jobs, resource limits and substantive alternatives.',
         'evidence': [ref(CHAPTER, 'Eleven substantive sections'), ref(BASE / 'substantive-review.md', 'Detailed author argument/source review'),
                      ref(BASE / 'chapter-text-review.json', 'Rendered text and actual eleven-page span')]},
        {'index': 1, 'verdict': 'pass',
         'finding': 'All citations have hash-bound primary/project records. Thirteen generated examples and lifecycle checks pass; printed instructions reproduce them. Historical MCP evidence and proposed paths remain distinct. Process records are outside the chapter.',
         'evidence': [ref(BASE / 'source-audit.json', 'Exact implementation and generated evidence'),
                      ref(BASE / 'claim-map.json', 'Claim/protocol/implementation boundaries'),
                      ref(BASE / 'examples/review.json', 'Observed examples'),
                      ref(BASE / 'printed-listings/review.json', 'Executed printed instructions'),
                      ref(release_path, 'Compiled source-audited working delivery')]}]
    write(BASE / 'TEXT.DRAFT.I2.receipt.json', receipt)
    print(json.dumps({'published': state['reader'], 'draft_receipt': str((BASE / 'TEXT.DRAFT.I2.receipt.json').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
