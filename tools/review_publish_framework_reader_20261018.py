#!/usr/bin/env python3
"""Review and publish a preserving framework-evaluation proposal delta."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_framework_reader_20261018 as build
import framework_evaluation_reference_20261018 as exact
import master_control as core
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author source, mathematical and extracted-page review; no independent or rendered visual acceptance.',
    'Original census42 inspected/71 unread of113; no complete-frontier or L6 coverage acceptance.',
    'General evaluation and architecture papers do not establish causal identification or calibrated agent performance.',
    'No new framework, model or adapter execution; package/dependency rights and environment remain unqualified.',
    'Paired counts and USD values are exact authored assumptions, not model or bank observations.',
    'Q1/Q5, all three mandatory manuscript repairs and final proposal acceptance remain open.'
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
    assert report['cited_records'] == 763 and index['scholarly_pdfs'] == 201
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 760 and all(new[k] == v for k, v in old.items())
    added = sorted(new.keys()-old.keys())
    assert set(added) == {'exec18_framework_promptbench', 'exec18_framework_agents_survey', 'exec18_framework_reference'}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    starts = [i for i, p in enumerate(pages) if
        'Evaluate the causal contract across the agent' in p and 'An agent framework becomes useful' in p]
    assert len(starts) == 1
    start = starts[0]
    ends = [i for i in range(start, min(start+12, len(pages))) if
            'a qualified banking agent.' in pages[i]]
    assert len(ends) == 1
    end = ends[0]
    text = ' '.join(pages[start:end+1])
    for phrase in ['PromptBench', 'CC-BY-4.0', '11/12', '5/6', '4.20', '3.90',
                   '4.95', '6.15', 'undefined if none', 'twenty paired families']:
        assert phrase in text, phrase
    equations = {k: v['number'] for k, v in report['added_anchors'].items()
                 if k in ['exec18:framework-denominators', 'exec18:framework-value']}
    assert all('('+n+')' in text for n in equations.values())
    return report, dict(preserved_records=760, added_records=added,
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        context_rule='Exclude only the new development.tex path when comparing predecessor context multisets.',
        equations=equations, physical_pages=[start+1, end+1], added_anchors=report['added_anchors'],
        original_candidates=113, inspected=42, unread=71, visual_acceptance=False)


def review():
    report, checks = verify()
    paths = [BASE/n for n in ['prepared-inputs.json', 'manuscript-plan-review.json',
        'source-audit.json', 'primary-review.json', 'mathematical-review.json', 'copyedit-review.json',
        'reconciliation-review.json', 'census-register.json', 'task-map.json', 'traceability-review.json',
        'exact-results.json', 'development.tex', 'reader/build-report.json',
        'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving framework-evaluation source, mathematical and extracted-page delta',
        checks=checks, evidence=[ref(p, 'Reviewed delta and preservation evidence') for p in paths]+[
            ref(Path(__file__), 'Exact preservation and manuscript review')],
        findings=['All760 predecessor source records, citation contexts and unchanged compiled inputs survive.',
                  'Two authentic pre-cutoff revisions support explicitly limited taxonomy/interface and historical qualitative claims.',
                  'Finite denominators, zero-completion boundary, paired-family dependence and exact stipulated economic reversal are explained.',
                  'Only two census candidates change; no L1/L6 or complete-framework acceptance is awarded.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def yield_for_publication():
    report, _ = verify()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == 'LL.CENSUS'
    path = BASE/'publication-progress.json'
    write(path, dict(finding='Two primary inspections and preserving framework-evaluation reader pass source, exact arithmetic, citation and all-page text checks.',
        next_action='Publish reviewed framework successor, renew exact-reader Q2-Q4, reconcile sponsor pairing and continue independent proposal work.',
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
        build_report=ref(OUT/'build-report.json', 'Preserving framework-evaluation build'),
        source_review=ref(BASE/'release-source-review.json', 'Source/math/preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Add bounded framework taxonomy, evaluation hooks, causal-reference responsibilities and exact paired-denominator/economic example.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Preserved sponsor remains paired to its exact predecessor; create a preserving current-reader sponsor successor before Q5.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed framework-evaluation working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_framework_evaluation_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': 'All760 predecessor citation records,201 total genuine scholarly PDFs and original citation contexts are traceable; three bounded source records are added. Selected paper versions predate the cutoff; taxonomy and historical qualitative results do not establish current census or package rights.',
        'Q3': 'Exact paired-contract counts and J=C*A reproduce, with conditional accuracy undefined at zero completion. Correct scientific refusal is distinct from unanswered execution; no independent-request confidence interval or live framework performance is claimed.',
        'Q4': 'Stipulated correct-answer value10USD, total costs12/24USD and error losses20/5USD yield exact per-planned-request net values4.20/3.90 and4.95/6.15USD. The ranking reversal is conditional bookkeeping, not observed bank benefit, prices or ROI; prior financial examples survive unchanged.'}
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
                    ref(BASE/'mathematical-review.json', 'Exact finite accounting'),
                    ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded framework-evaluation source, mathematical and economic delta.'))
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
