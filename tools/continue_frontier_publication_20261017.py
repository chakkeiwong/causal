#!/usr/bin/env python3
"""Preserve a failed publication attempt and repair its review-schema omission."""
import argparse
import copy
import json
from pathlib import Path

import review_publish_frontier_20261017 as prior
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

ROOT = prior.ROOT
BASE = prior.BASE / 'publication-schema-repair'


def publish():
    report, checks = prior.verify()
    old_review = prior.read(prior.BASE / 'release-source-review.json')
    old_manifest = prior.read(prior.BASE / 'working-release.json')
    verify_bindings(old_review)
    verify_bindings(old_manifest)
    assert old_review['status'] == 'pass' and 'issues' not in old_review
    state = prior.core.read(ROOT, prior.core.STATE)
    before = prior.core.sha(ROOT / prior.core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == old_manifest['supersedes']['path']
    assert state['reader']['sha256'] == old_manifest['supersedes']['sha256']
    BASE.mkdir(exist_ok=False)
    write(BASE / 'failure-and-repair.json', dict(
        observed_failure='ValueError: Working book source/claim review has unresolved issues',
        cause='The successful source review omitted the required explicit issues=[] field. Publication validation failed before canonical state mutation.',
        failed_attempt=ref(prior.BASE / 'working-release.json', 'Preserved rejected manifest'),
        prior_review=ref(prior.BASE / 'release-source-review.json', 'Preserved successful checks with schema omission'),
        repair='Re-run the original verification and issue a preserving review successor with the required empty issues list.',
        checks=checks, altered_pdf=False, acceptance_scope='working_proposal_only'))
    review = copy.deepcopy(old_review)
    review['issues'] = []
    review['evidence'] += [ref(BASE / 'failure-and-repair.json', 'Observed failure and preserving repair'),
                           ref(prior.BASE / 'release-source-review.json', 'Preserved source review'),
                           ref(Path(__file__), 'Publication schema repair and exact-reader renewal')]
    write(BASE / 'release-source-review.json', review)
    manifest = copy.deepcopy(old_manifest)
    manifest['source_review'] = ref(BASE / 'release-source-review.json', 'Verified review schema successor')
    manifest['source_artifacts'] += review['evidence'][-3:]
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed frontier working successor')
    prior.run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    prior.run.commit(ROOT, before, state, dict(action='publish_frontier_reader_schema_repaired',
                                              manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = prior.verify()
    prior.run.ledger.validate_working_release(ROOT, ref(BASE / 'working-release.json', 'Exact working reader'))
    findings = {
        'Q2': 'All731 canonical records and citation-context multisets survive.735 audited records retain191 genuine scholarly PDFs; the three inspected originals have identity, version/date, hashes, primary anchors and bounded claims.35 inspected/78 unread originals do not establish census closure.',
        'Q3': 'Four added equations, exact rational laws and independent threshold enumeration reproduce. Binary Table4 and three selected rounding checks are correctly scoped; the L1 denominator conflict stays unresolved. All-page text bounds pass without material compilation warnings. No depth or visual acceptance is awarded.',
        'Q4': 'Equal observed joint laws permit causal effects+1/10,0,-1/10. Stipulated USD100 outcome value and USD5 action cost yield incremental USD5,-5,-15. These are authored information counterexamples, not measured bank returns.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = prior.core.read(ROOT, prior.core.STATE)
        assert prior.run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = prior.read(ROOT / previous['path'])
        if prior.run.same_reader(old.get('reviewed_reader', {}), report['pdf']):
            assert old['outcome'] == 'pass'
            continue
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, ref(BASE / 'working-release.json', 'Exact current reader'),
                    ref(BASE / 'release-source-review.json', 'Preserving source/math delta'),
                    ref(prior.TRANCHE / 'primary-review.json', 'Three inspected originals'),
                    ref(prior.TRANCHE / 'exact-results.json', 'Exact authored laws and rounding checks'),
                    ref(Path(__file__), 'Exact-reader review findings')]
        write(folder / 'reopen.json', dict(reason='Changed reader requires a preserving author delta review.',
              prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
              next_action='Record the bounded source, mathematical and economic delta.'))
        transition('reopen', identifier, folder / 'reopen.json')
        state = prior.core.read(ROOT, prior.core.STATE)
        graph, _, _ = prior.run.combined(ROOT, state)
        node = prior.run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / prior.run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + prior.LIMITS))
        scope = 'Author exact-reader delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0],
              reviewer=prior.REVIEWER, reviewed_reader=report['pdf'], review_attempt=attempt,
              acceptance_scope='proposal_only', scope=scope, findings=[finding],
              evidence=evidence, limitations=limits, visual_acceptance=False))
        receipt = prior.run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=prior.REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact-reader ' + q + ' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2–Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['publish', 'renew'])
    args = parser.parse_args()
    {'publish': publish, 'renew': renew}[args.command]()
