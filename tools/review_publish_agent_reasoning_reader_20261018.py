#!/usr/bin/env python3
"""Review and publish a preserving agent-reasoning proposal delta."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_agent_reasoning_reader_20261018 as build
import agent_reasoning_reference_20261018 as exact
import master_control as core
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author primary-source, exact mathematical and extracted-page review; no independent or rendered visual acceptance.',
    'Original census44 inspected/69 unread of113; no complete-frontier or L1/L6 acceptance.',
    'The biomedical position paper supports its authors agenda; constituent performance requires primary originals.',
    'The neuron-diagram study proposes a scoped attribution criterion and illustrative historical runs, not general causal identification or a current model ranking.',
    'Citation, transcription and target inconsistencies need adjudication before adopting benchmark cases; image/table verification remains open.',
    'Authored servicing mechanisms, probabilities and costs are stipulated; no DEF-1 implementation, live agent performance or bank ROI.',
    'Q1/Q5, all three mandatory manuscript repairs, full reconciliation and final proposal acceptance remain open.'
]


def read(path):
    return json.loads(path.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    for path in [BASE/'prepared-inputs.json', BASE/'source-audit.json', BASE/'primary-review.json',
                 BASE/'mathematical-review.json', BASE/'copyedit-review.json', BASE/'manuscript-plan-review.json',
                 BASE/'reconciliation-review.json', BASE/'traceability-review.json',
                 OUT/'source-audit.json', OUT/'build-report.json']:
        verify_bindings(read(path))
    report = read(OUT/'build-report.json')
    audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    assert report['cited_records'] == 784 and index['scholarly_pdfs'] == 203
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 781 and all(new[k] == v for k, v in old.items())
    added = sorted(new.keys()-old.keys())
    assert set(added) == {'exec18_reasoning_biomedical', 'exec18_reasoning_neuron', 'exec18_reasoning_reference'}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if
        'Transfer an agent design only with its causal' in p and 'An agent can give a convincing account' in p]
    assert len(starts) == 1
    start = starts[0]
    ends = [i for i in range(start, min(start+12, len(pages))) if
            'validity of institutional causal premises.' in pages[i]]
    assert len(ends) == 1
    end = ends[0]
    text = ' '.join(pages[start:end+1])
    for phrase in ['position paper', 'DEF-1', '13 of 25', 'USD160', 'USD190',
                   'minus USD30', '16/19', '160', '190p', 'predecision', 'compound']:
        assert phrase in text, phrase
    equations = {k: v['number'] for k, v in report['added_anchors'].items()
                 if k in ['exec18:reasoning-mechanism', 'exec18:reasoning-interventions',
                          'exec18:reasoning-money', 'exec18:reasoning-threshold']}
    assert len(equations) == 4 and all('('+n+')' in text for n in equations.values())
    return report, dict(preserved_records=781, added_records=added,
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        context_rule='Exclude only the new development.tex path when comparing predecessor context multisets.',
        equations=equations, physical_pages=[start+1, end+1], added_anchors=report['added_anchors'],
        original_candidates=113, inspected=44, unread=69, visual_acceptance=False)


def review():
    report, checks = verify()
    paths = [BASE/n for n in ['prepared-inputs.json', 'manuscript-plan-review.json',
        'source-audit.json', 'primary-review.json', 'mathematical-review.json', 'copyedit-review.json',
        'reconciliation-review.json', 'census-register.json', 'task-map.json', 'traceability-review.json',
        'exact-results.json', 'development.tex', 'reader/build-report.json',
        'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving agent-reasoning source, mathematical and extracted-page delta',
        checks=checks, evidence=[ref(p, 'Reviewed delta and preservation evidence') for p in paths]+[
            ref(Path(__file__), 'Exact preservation and manuscript review')],
        findings=['All781 predecessor source records, citation contexts and unchanged compiled inputs survive.',
                  'Two authentic selected v1 originals support a bounded agenda, a proposed diagram test, historical author observations and explicit source defects.',
                  'Exact structural single and compound interventions, information timing and the160-190pUSD value difference are explained.',
                  'Only two census candidates change; no L1/L6 or complete-framework acceptance is awarded.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def yield_for_publication():
    report, _ = verify()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'LL.CENSUS'
    path = BASE/'publication-progress.json'
    write(path, dict(finding='Two primary inspections and preserving agent-reasoning reader pass source, exact arithmetic, citation and all-page text checks.',
        next_action='Publish reviewed agent-reasoning successor, renew exact-reader Q2-Q4, reconcile sponsor pairing and continue independent proposal work.',
        evidence=[ref(BASE/'release-source-review.json', 'Bounded author review'), report['pdf']],
        yield_reason='Reader publication and exact-reader reviews require an idle active-operation slot; a scheduling transition only.'))
    transition('yield', 'LL.CENSUS', path)


def publish():
    report, _ = verify()
    review_record = read(BASE/'release-source-review.json')
    verify_bindings(review_record)
    assert review_record['status'] == 'pass' and not review_record['issues']
    state = core.read(ROOT, core.STATE)
    before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest = dict(kind='working_monograph', final_acceptance=False,
        pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving agent-reasoning build'),
        source_review=ref(BASE/'release-source-review.json', 'Source/math/preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Add source-critical biomedical agenda and neuron-diagram evaluation, with an exact banking example distinguishing attribution, intervention and value.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor remains paired to its exact predecessor; create a preserving current-reader sponsor successor before Q5.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed agent-reasoning working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_agent_reasoning_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': 'All781 predecessor citation records and contexts survive. Two authentic selected v1 originals and one project reference produce784 records and203 scholarly PDFs. Inspected source defects, secondary constituent claims and visual limits remain explicit; original census44/113 inspected.',
        'Q3': 'Exact authored structural enumeration preserves success when only priority is removed and eliminates it under compound priority-plus-backup removal. Distinct attribution, intervention and evaluation targets are retained; no DEF-1 implementation or live model qualification.',
        'Q4': 'Stipulated USD200 success, USD40 priority and USD10 backup costs give160/190USD at available backup and priority advantage160-190p with threshold16/19. This conditional authored example is not observed bank economics; all earlier monetary examples remain unchanged.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]
        old = core.read(ROOT, previous['path'])
        if old.get('reviewed_reader', {}).get('sha256') == report['pdf']['sha256']:
            continue
        folder = BASE/q
        folder.mkdir(exist_ok=False)
        evidence = [previous, binding, ref(BASE/'release-source-review.json', 'Preserving author delta'),
                    ref(BASE/'source-audit.json', 'Authentic selected source identities'),
                    ref(BASE/'mathematical-review.json', 'Exact structural mechanisms and stipulated value'),
                    ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded agent-reasoning source, mathematical and economic delta.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS))
        scope = 'Author exact-reader preserving delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0],
            reviewer=REVIEWER, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', scope=scope, findings=[finding], evidence=evidence,
            limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER,
            limitations=limits, reviewed_reader=report['pdf'], review_attempt=attempt,
            acceptance_scope='proposal_only', outputs=[ref(output, 'Exact-reader '+q+' author review')],
            nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder/'operation-receipt.json', receipt)
        transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = dict(review=review, yield_for_publication=yield_for_publication, publish=publish, renew=renew)
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
