#!/usr/bin/env python3
"""Review preserving workflow integration and renew only exact-reader author gates."""
import argparse
import json
from pathlib import Path

import build_workflow_reader_20261022 as build
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write
import run_program_reviews_v2 as extension

run = extension.base
core = run.core
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author primary-source, arithmetic and extracted rendered-text review; no independent or visual acceptance.',
    'Six current manuals lack authenticated cutoff editions and do not close historical survey coverage.',
    'The finite-table reference is authored exact arithmetic; no commercial runtime or adapter was executed.',
    'No statistical calibration, vendor superiority, actual prices or measured bank returns are established.',
    'Census remains61/52 with four crosscutting searches; Q1/Q5 and all mandatory repairs remain open.']
read = lambda p: json.loads(p.read_text())


def verify():
    for name in ['prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'review.json',
            'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
            'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']:
        verify_bindings(read(BASE / name))
    prepared, report, audit, index = [read(BASE / n) for n in
        ['prepared-inputs.json', 'reader/build-report.json', 'reader/source-audit.json', 'traceability-review.json']]
    assert report['cited_records'] == prepared['expected_cited_records'] == 932
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs'] == 221
    bounds = read(OUT / 'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.exact.calculate() == read(BASE / 'exact-results.json')
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR)['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == prepared['prior_cited_records'] == 925
    assert all(new[k] == v for k, v in old.items())
    assert new.keys() - old.keys() == {s['integrated_citation_key'] for s in read(BASE / 'source-audit.json')['sources']}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in read(build.PRIOR)['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR / 'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(v == after[k] for k, v in before.items())
    pages = [' '.join(p.split()) for p in (OUT / 'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if 'A recovered causal batch is useful only if its result answers the declared' in p]
    assert len(starts) == 1, starts
    start = starts[0]
    ends = [i for i, p in enumerate(pages) if i >= start and 'already adopted the causal library.' in p]
    assert len(ends) == 1, ends
    end = ends[0]
    text = ' '.join(pages[start:end + 1]).replace('- ', '-')
    for token in ['14/3', '5/6', '60-day', 'DataLimitExceeded', '19 October', 'MCP',
            'statistical', 'known', 'manifest', 'Dataiku', 'Domino']:
        assert token in text, token
    equations = {label: report['added_anchors'][label]['number'] for label in build.LABELS[1:]}
    assert all('(' + n + ')' in text for n in equations.values())
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys() - old.keys()),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        physical_pages=[start + 1, end + 1], equations=equations,
        current_manuals=6, cutoff_accepted_manuals=0, vendor_execution=False, visual_acceptance=False)


def review():
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
        'traceability-review.json', 'exact-results.json', 'development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']
    write(BASE / 'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving current workflow-source and scientific-replay integration',
        checks=checks, evidence=[ref(BASE / n, 'Reviewed preserving integration') for n in names] +
            [ref(Path(__file__), 'Exact delta review')],
        findings=['All925 earlier source identities, citation contexts and earlier compiled content inputs survive.',
            'Six authenticated current manuals retain explicit historical exclusions and candidate omissions.',
            'Duplicate-write arithmetic, target/vintage changes and manifest checks reproduce.',
            'Scientific replay, scheduling success, causal identification and calibration remain distinct.',
            'Public/known-law qualification is specified before costly native commercial and bank trials.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def publish():
    report, _ = verify()
    record = read(BASE / 'release-source-review.json')
    verify_bindings(record)
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT / 'build-report.json', 'Preserving workflow build'),
        source_review=ref(BASE / 'release-source-review.json', 'Primary-source and preservation review'),
        text_layout=ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT / 'source-audit.json')['tex_files'] + record['evidence'],
        changes=['Integrate temporally qualified commercial workflow mechanisms and exact semantic-replay examples.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Pair preserving sponsor to exact current reader.')
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed workflow working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_workflow_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify()
    binding = ref(BASE / 'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = dict(
        Q2=f'All{checks["preserved_records"]} earlier identities/contexts survive. Six current authentic manuals have exact inspected anchors and historical exclusions; one labeled authored reference is added. No cutoff coverage or market completeness is claimed.',
        Q3='The equal-unit target, duplicate-weight change3/4 to5/6, mean4 versus14/3 and bias2/3 reproduce with exact rational arithmetic. Same-manifest keyed recovery preserves four units; different target/vintage and manifest checks are separate. Replay, causal identification and calibration are not conflated.',
        Q4='Stipulated per-unit cost1 yields baseline net3, duplicate-row apparent net11/3, alternate-target net-1 and changed-vintage net1. The comparison motivates public known-law recovery tests and full attempt/cost accounting, with no vendor prices, measured runtime or bank returns.')
    for q, finding in findings.items():
        identifier = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = core.read(ROOT, previous['path'])
        assert old.get('reviewed_reader', {}).get('sha256') != report['pdf']['sha256'], 'Do not rerun a completed renewal.'
        folder = BASE / q
        folder.mkdir(exist_ok=False)
        evidence = [previous, binding, ref(BASE / 'release-source-review.json', 'Preserving author review'),
            ref(BASE / 'source-audit.json', 'Current manuals and authored reference'),
            ref(BASE / 'mathematical-review.json', 'Exact arithmetic'), ref(Path(__file__), 'Exact-reader findings')]
        write(folder / 'reopen.json', dict(reason='Changed reader requires preserving delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record source, arithmetic and value delta for this exact reader.'))
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author exact-reader preserving delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0], reviewer=REVIEWER,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            scope=scope, findings=[finding], evidence=evidence, limitations=limits, visual_acceptance=False))
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
