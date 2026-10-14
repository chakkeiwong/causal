#!/usr/bin/env python3
"""Renew proposal Q2–Q4 for the exact L5 depth successor."""
import json
from pathlib import Path

import master_control as core
import publish_l5_depth_20261014 as published
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, transition, write

ROOT = core.ROOT
BASE = published.BASE
REVIEWER = published.REVIEWER
LIMITS = published.LIMITS


def main():
    report = json.loads((published.OUT / 'build-report.json').read_text())
    review = json.loads((BASE / 'release-source-review.json').read_text())
    published.verify_bindings(review)
    assert review['unchanged_source_records'] == 515
    findings = {
        'Q2': 'All 515 predecessor source records and inherited compiled chapters are preserved; one additional record binds the exact nuisance-error and panel-composition constructions. Actual review inspects the new contexts for two inherited primary sources and whole-reader traceability verifies 516 records, including 153 genuine scholarly PDFs. Whole-survey coverage and depth remain separate.',
        'Q3': 'Earlier demonstration evidence and negative verdicts remain unchanged. Independent enumeration matches the exact sequential remainder, bias −2 and value 92.8; the correctly specified assignment or outcome components restore 94.8. Conditional panel standardization and weighting both produce control change 8 and ATT 7 instead of naive 11. Planning size 4007 is arithmetic under a known law, not achieved coverage or an executed study.',
        'Q4': 'Inherited investment scenarios are preserved. The new panel example has stipulated deployment cost 6, true gross benefit 7 and net margin 1, while the pooled comparison suggests margin 5. This motivates an inexpensive public/generated-data prototype that checks target preservation before an expensive bank trial. Prices, complete operating costs, learned-policy value and measured bank ROI remain unestablished.',
    }
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert state['reader']['sha256'] == report['pdf']['sha256']
        previous = state['execution_runtime']['results'][identifier]
        old = json.loads((ROOT / previous['path']).read_text())
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact 702-page successor'),
                    ref(BASE / 'release-source-review.json', 'Reviewed mathematical/source/business delta'),
                    ref(published.REVIEW, 'Actual nonduplicate L5 depth review'),
                    ref(Path(__file__), 'Current exact-reader renewal findings')]
        write(folder / 'reopen.json', {
            'reason': 'Reader changed; preserve the preceding exact-reader review and review the actual delta.',
            'prior_result': previous, 'reviewed_reader': report['pdf'], 'evidence': evidence,
            'next_action': 'Record the reviewed L5 depth successor with the current source counts and scoped findings.'})
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, {'operation': identifier, 'status': 'pass', 'criterion': node['criteria'][0],
            'reviewer': REVIEWER, 'reviewed_reader': report['pdf'], 'review_attempt': attempt,
            'acceptance_scope': 'proposal_only', 'scope': scope, 'findings': [finding],
            'evidence': evidence, 'limitations': limits, 'visual_acceptance': False})
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Current-reader ' + q + ' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[{'index': 0, 'verdict': 'pass', 'finding': finding, 'evidence': evidence}])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps({'reader_sha256': report['pdf']['sha256'], 'Q2_Q3_Q4': 'pass',
                      'proposal_accepted': False}))


if __name__ == '__main__':
    main()
