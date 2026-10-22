#!/usr/bin/env python3
"""Preserving source/argument/text review and exact-reader proposal delta."""
import argparse
import json
from pathlib import Path

import build_detailed_workflow_reader_v2_20261023 as build
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = controller.base
core, ROOT, BASE, OUT = run.core, build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author source, arithmetic and rendered-text review; no independent or visual acceptance.',
    'Exact cutoff patch originals, remaining commercial candidates, rights, price and native qualification remain open.',
    'The finite constructed effects and bounds are stipulated, not estimated bank returns or statistical confidence.',
    'No absence finding, whole-market completion or general causal capability is established.',
    'Q1/Q5 and mandatory repairs remain open.']
read = lambda p: json.loads(p.read_text())


def verify():
    for name in ['prepared-inputs.json', 'source-audit.json', 'source-completion-review.json',
        'plan-review.json', 'mathematical-review.json', 'copyedit-review.json', 'traceability-review.json',
        'reader/source-audit.json', 'reader/build-report.json', 'reader/text-layout-review.json']:
        verify_bindings(read(BASE / name))
    prepared, report, audit, index, bounds = [read(BASE / n) for n in
        ['prepared-inputs.json', 'reader/build-report.json', 'reader/source-audit.json',
         'traceability-review.json', 'reader/text-layout-review.json']]
    assert index['status'] == bounds['status'] == 'pass' and not index['issues']
    assert report['cited_records'] == prepared['expected_cited_records'] == 946
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs'] == 223
    assert not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in x for x in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.calculate() == read(BASE / 'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == prepared['prior_cited_records'] == 939
    assert all(new[k] == value for k, value in old.items())
    assert new.keys() - old.keys() == {s['integrated_citation_key'] for s in read(BASE / 'source-audit.json')['sources']}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR / 'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(value == after[key] for key, value in before.items())
    pages = [' '.join(p.split()).replace('- ', '-') for p in (OUT / 'reader.txt').read_text().split(chr(12))]
    first = 'The previous orchestration comparison motivates a closer question'
    last = 'requiring an explicit scientific workload before an integration is accepted.'
    starts = [i for i, p in enumerate(pages) if first in p]
    assert len(starts) == 1, starts
    start = starts[0]
    ends = [i for i, p in enumerate(pages) if i >= start and last in p]
    assert len(ends) == 1, ends
    end = ends[0]
    text = ' '.join(pages[start:end + 1])
    tokens = ['ABORTED', 'tolerated', 'suppression', 'Squash', '15.0.2', '15.1.0',
        '15.2.0', '14.7.5', 'maximum', 'pytest', 'native', '-11', '-21', '29']
    assert all(t in text for t in tokens), [t for t in tokens if t not in text]
    for anchor in report['added_anchors'].values():
        if anchor['number'].count('.'):
            assert '(' + anchor['number'] + ')' in text or anchor['number'] in text
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys() - old.keys()),
        scholarly_pdfs=223, unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        rendered_ranges=dict(workflow=dict(physical_pages=[start + 1, end + 1], checked_tokens=tokens)),
        native_execution=False, visual_acceptance=False)


def review():
    assert not (BASE / 'release-source-review.json').exists()
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'source-completion-review.json',
        'plan-review.json', 'mathematical-review.json', 'copyedit-review.json', 'traceability-review.json',
        'exact-results.json', 'development.tex', 'reader/build-report.json', 'reader/source-audit.json',
        'reader/reader.txt', 'reader/text-layout-review.json']
    write(BASE / 'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Connected detailed commercial-workflow argument and preservation',
        checks=checks, evidence=[ref(BASE / n, 'Reviewed preserving workflow integration') for n in names] +
            [ref(Path(__file__), 'Exact source, context, arithmetic and text review')],
        findings=['All939 prior citation identities and contexts and all earlier content inputs survive.',
            'Six detailed official originals and one exact authored reference develop the existing chapter.',
            'The fixed scientific denominator and explicit missing-effect bounds retain their monetary meaning.',
            'A pre-cutoff DSS15 release is distinguished from unauthenticated current patch bytes.',
            'Public/generated prototype tests precede expensive bank experiments.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], records=946, checks=checks)))


def publish():
    report, _ = verify()
    review_record = read(BASE / 'release-source-review.json')
    verify_bindings(review_record)
    assert review_record['status'] == 'pass' and not review_record['issues']
    state, digest = core.read(ROOT, core.STATE), core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], ref(build.OLD.with_suffix('.pdf'), 'Previous reader'))
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT / 'build-report.json', 'Detailed workflow preserving build'),
        source_review=ref(BASE / 'release-source-review.json', 'Primary-source and preservation review'),
        text_layout=ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT / 'source-audit.json')['tex_files'] + review_record['evidence'],
        changes=['Develop existing commercial-workflow chapter with detailed Dataiku semantics, missing-effect target and cutoff comparison.'],
        visual_acceptance=False, mandatory_repairs_closed=[], sponsor_binding='Pair sponsor to exact current reader.')
    assert not (BASE / 'working-release.json').exists()
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed detailed workflow working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, digest, state, dict(action='publish_detailed_workflow_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify()
    binding = ref(BASE / 'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = dict(Q2=f'All{checks["preserved_records"]} prior identities/contexts survive; six inspected official originals retain local bytes, exact anchors and temporal omissions. Current DSS15 is distinguished from its pre-cutoff patch identity.',
        Q3='The fixed two-cohort target net is-11 USD, available-only net9, difference20; independent cents accounting agrees. Assumed missing-effect bounds[-50,50] give net[-21,29]; a count/max-date proxy can be unchanged as net changes to19.',
        Q4='Failure-dependent population changes can reverse the contact-policy monetary sign under explicit stipulated effects. Public/generated fixed-manifest trials precede expensive bank studies; no vendor runtime or bank returns are asserted.')
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = core.read(ROOT, previous['path'])
        assert old.get('reviewed_reader', {}).get('sha256') != report['pdf']['sha256']
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, binding, ref(BASE / 'release-source-review.json', 'Preserving author review'),
            ref(BASE / 'source-audit.json', 'Primary technical originals'),
            ref(BASE / 'mathematical-review.json', 'Exact finite target'), ref(Path(__file__), 'Exact-reader author delta')]
        write(folder / 'reopen.json', dict(reason='Changed reader needs exact source, arithmetic and economic delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record exact-reader bounded author review.'))
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = next(n for n in graph['nodes'] if n['id'] == identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author exact-reader workflow delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0], reviewer=REVIEWER,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only', scope=scope,
            findings=[finding], evidence=evidence, limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER, limitations=limits,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Exact-reader ' + q + ' review')], nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', identifier, folder / 'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    commands = dict(review=review, publish=publish, renew=renew)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
