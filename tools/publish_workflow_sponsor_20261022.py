#!/usr/bin/env python3
"""Publish an already completed sponsor review without rewriting its evidence."""
import json
from pathlib import Path

import build_workflow_sponsor_20261022 as build
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write


def main():
    run, core, root, base = build.run, build.core, build.ROOT, build.BASE
    read = lambda p: json.loads(p.read_text())
    report = read(base / 'build-report.json')
    review = read(base / 'author-review.json')
    verify_bindings(report)
    verify_bindings(review)
    assert review['status'] == 'pass' and not review['issues']
    assert run.same_reader(review['sponsor'], report['reader_copy'])
    assert run.same_reader(review['paired_monograph'], report['paired_monograph'])
    state = core.read(root, core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], report['paired_monograph'])
    evidence = [ref(base / name, 'Reviewed paired sponsor') for name in
        ['build-report.json', 'author-review.json', 'source-audit.json', 'reader.txt']]
    evidence.append(ref(Path(__file__), 'Consume immutable successful review'))
    manifest = dict(kind='working_sponsor', pdf=report['reader_copy'], pages=report['pages'],
        paired_monograph=report['paired_monograph'],
        predecessor=ref(build.PRIOR / 'reader/sponsor-proposal.pdf', 'Preserved sponsor'),
        predecessor_release=ref(build.PRIOR / 'working-release.json', 'Preserved release'),
        predecessor_operation=state['execution_program']['results']['RELEASE.SPONSOR'],
        build=ref(base / 'build-report.json', 'Sponsor build'),
        review=ref(base / 'author-review.json', 'Exact-reader author review'),
        evidence=evidence, visual_acceptance=False, final_acceptance=False)
    verify_bindings(manifest)
    write(base / 'working-release.json', manifest)
    digest = core.sha(root / core.STATE)
    delivery = {k: report['reader_copy'][k] for k in ['path', 'sha256']}
    delivery.update(pages=report['pages'], kind='working_sponsor',
        status='Working sponsor; visual and final acceptance remain open',
        paired_monograph=report['paired_monograph'],
        release=ref(base / 'working-release.json', 'Preserving workflow sponsor'))
    assert not any(x['path'] == delivery['path'] for x in state['deliveries'])
    state['deliveries'].append(delivery)
    run.commit(root, digest, state, dict(action='publish_workflow_sponsor',
        release=delivery['release'], prior_operation_preserved=True, final_acceptance=False))
    print(json.dumps(dict(published=delivery['path'], pages=delivery['pages'],
        paired_monograph=state['reader']['path'], final_acceptance=False)))


if __name__ == '__main__':
    main()
