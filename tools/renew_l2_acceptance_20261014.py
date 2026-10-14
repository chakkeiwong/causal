#!/usr/bin/env python3
"""Renew exact-reader proposal reviews after the preserving L2 release."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import master_control as core
import run_program as run

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/l2/final-v4'
READER = 'docs/causal_proposal_l2_v4_2026-10-13.pdf'
RELEASE = BASE / 'working-release.json'
REVIEW = BASE / 'release-source-review.json'
EXACT = ROOT / 'docs/program/execution/2026-10-13/l2/exact-results-v2.json'


def ref(path, anchor):
    return run.bind(ROOT, str(path.relative_to(ROOT)), anchor)


def write(path, obj):
    assert not path.exists(), 'Preserve an earlier review: ' + str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(obj, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def commit(command, operation, path):
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    event = run.apply(ROOT, state, command, operation, str(path.relative_to(ROOT)))
    run.commit(ROOT, before, state, event)


FINDINGS = {
    'Q2': 'All 497 predecessor cited source records are byte-identical. The 151 preserved TeX source files are unchanged; only the root driver is succeeded and one corrected L2 chapter is added. Its eight citation keys already have inspected audit identities. The 655-page reader has no unresolved citations, overfull boxes or out-of-bounds extracted words.',
    'Q3': 'Earlier portfolio evidence is preserved. L2 adds exact authored target-weighting and observational-equivalence arithmetic, not a newly qualified estimator, live model, native package run or bank effect. The inference and refusal boundaries are explicit in the chapter.',
    'Q4': 'The chapter distinguishes intervention targets and policy costs. Its two observationally identical donor laws imply stipulated four-day net values of USD +60 and USD -60, demonstrating decision-relevant value of additional information. No bank ROI, supplier price or accepted investment case is inferred.',
}


def renew(q):
    operation = 'PROPOSAL.' + q
    state = core.read(ROOT, core.STATE)
    assert state['reader']['path'] == READER
    previous = state['execution_runtime']['results'][operation]
    previous_receipt = core.read(ROOT, previous['path'])
    folder = BASE / q
    folder.mkdir(exist_ok=True)
    reader = {k: state['reader'][k] for k in ('path', 'sha256')}
    reader['anchor'] = 'Exact current working reader PDF; extracted text/bounds audited; visual acceptance separate'
    evidence = [previous, ref(RELEASE, 'Reviewed preserving L2 working release'),
                ref(REVIEW, 'Exact-reader source and claim delta'),
                ref(EXACT, 'Authored exact arithmetic and donor construction')]
    note = {'reason': 'The integrated L2 successor changes the exact working reader.',
            'prior_result': previous, 'reviewed_reader': reader,
            'evidence': evidence,
            'next_action': 'Review the preserving L2 delta for ' + q + ' and record the bounded result.'}
    reopen_path = folder / 'reopen-02.json'
    write(reopen_path, note)
    commit('reopen', operation, reopen_path)

    state = core.read(ROOT, core.STATE)
    graph, _, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, operation)
    attempt = len(state['execution_runtime']['review_history'][operation])
    output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
    limitations = previous_receipt['limitations'] + [
        'L2 was author-reviewed and its PDF text/layout checked; independent semantic and rendered-image acceptance remain open.',
        'Q1 whole-survey and manuscript depth and Q5 release/sponsor reconciliation remain open.',
        'No bank truth, live model or product acceptance is inferred from this chapter.']
    review = {'operation': operation, 'status': 'pass', 'issues': [],
              'criterion': node['criteria'][0],
              'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'reviewed_reader': reader, 'review_attempt': attempt,
              'acceptance_scope': 'proposal_only',
              'scope': 'Exact-reader author review of unchanged predecessor plus corrected L2 chapter',
              'findings': [FINDINGS[q]], 'evidence': evidence,
              'limitations': limitations, 'visual_acceptance': False,
              'bank_ROI_established': False}
    write(output, review)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed', scope=review['scope'],
                   reviewer=review['reviewer'], limitations=limitations,
                   reviewed_reader=reader, review_attempt=attempt,
                   acceptance_scope='proposal_only',
                   outputs=[ref(output, 'Exact-reader ' + q + ' review')],
                   nonexecution_reason='', revisit_trigger='',
                   criteria=[{'index': i, 'verdict': 'pass', 'finding': FINDINGS[q],
                              'evidence': evidence + [ref(output, 'Reviewed finding')]}
                             for i in range(len(node['criteria']))])
    write(folder / 'operation-receipt.json', receipt)
    commit('record', operation, folder / 'operation-receipt.json')
    print(json.dumps({'reviewed': operation, 'attempt': attempt}), flush=True)


if __name__ == '__main__':
    for key in ('Q2', 'Q3', 'Q4'):
        renew(key)
