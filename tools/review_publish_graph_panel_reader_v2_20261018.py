#!/usr/bin/env python3
"""Preserve predecessor evidence and publish a graph/panel author-reviewed delta."""
import argparse
from collections import Counter
import json
from pathlib import Path

import build_graph_panel_reader_v2_20261018 as build
import graph_panel_reference_20261018 as exact
import master_control as core
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = extension.base
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Author primary-source, mathematical and extracted-page review; no independent or rendered visual acceptance.',
    'Commercial coverage is bounded to four Stata manuals and an EViews introduction; other families and exact editions remain unresolved.',
    'DAGitty R-wrapper selection is proposed reference reuse; runtime, resolved dependencies and distribution rights remain unqualified.',
    'Authored structural and branch-rollout laws are exact examples; no sampling coverage, vendor benchmark or bank ROI follows.',
    'The saved local panel request is unsupported at the common dispatcher; this does not assert absence of other panel research code.',
    'Q1/Q5, MR01/MR02/MR03, original census and L1/L6 coverage, and final proposal acceptance remain open.'
]


def read(path):
    return json.loads(path.read_text())


def contexts(index, excluded=()):
    return {r['citation_key']: Counter(json.dumps(c, sort_keys=True)
        for c in r['citation_contexts'] if c['path'] not in excluded) for r in index['records']}


def verify():
    for path in [BASE/n for n in ['prepared-inputs.json', 'source-audit.json',
        'manuscript-plan-review.json', 'mathematical-review.json', 'copyedit-review.json',
        'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']]:
        verify_bindings(read(path))
    report = read(OUT/'build-report.json')
    audit = read(OUT/'source-audit.json')
    index = read(BASE/'traceability-review.json')
    assert report['cited_records'] == 772 and index['scholarly_pdfs'] == 201
    assert index['status'] == 'pass' and not index['issues']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    assert build.DRIVER.read_text() == build.expected_driver()
    assert exact.calculate() == read(BASE/'exact-results.json')
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR)['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 763 and all(new[k] == v for k, v in old.items())
    added = set(new)-set(old)
    assert added == {'exec18_gp_'+k for k in ['dagitty', 'stata_did', 'stata_hdid',
        'stata_xthdid', 'stata_post', 'eviews', 'graph_reference', 'panel_reference', 'dispatch']}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in read(build.PRIOR)['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR/'traceability-review.json'))
    after = contexts(index, {str(p.relative_to(ROOT)) for p in [build.GRAPH, build.PANEL]})
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    ranges = {}
    sections = [
        ('graph', 'A bank analyst who supplies a causal diagram',
         'bounded trial and rights review are complete.',
         ['0.3-4', 'max.results', '3/16', '7/16', '5/16', '7/96', '1/8', '1.8.3', '1.13.1',
          'not an installed adapter', 'GPL-2', 'MAG/PAG']),
        ('panel', 'A staggered branch rollout poses a different question',
         'trend validity or bank qualification.',
         ['hdidregress', 'xthdidregress', '11.375', '21,375', '24,000',
          'weights(timecohort)', 'weights(cohort)', 'vce(robust)', 'unsupported disposition', 'no sampling'])]
    section_text = {}
    for name, start_phrase, end_phrase, phrases in sections:
        starts = [i for i, p in enumerate(pages) if start_phrase in p]
        assert len(starts) == 1, (name, starts)
        start = starts[0]
        ends = [i for i in range(start, min(start+20, len(pages))) if end_phrase in pages[i]]
        assert len(ends) == 1, (name, ends)
        end = ends[0]
        text = ' '.join(pages[start:end+1])
        for phrase in phrases:
            assert phrase.lower() in text.lower(), (name, phrase)
        ranges[name] = [start+1, end+1]
        section_text[name] = text
    equations = {}
    for label in ['exec18:gp-confounding', 'exec18:gp-collider', 'exec18:gp-cohort-target',
                  'exec18:gp-fwl', 'exec18:gp-negative-weight']:
        number = report['added_anchors'][label]['number']
        name = 'graph' if label in ['exec18:gp-confounding', 'exec18:gp-collider'] else 'panel'
        assert '('+number+')' in section_text[name], label
        equations[label] = number
    return report, dict(preserved_records=763, added_records=sorted(added),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        context_rule='Exclude only the two new development paths from predecessor context multisets.',
        physical_pages=ranges, equations=equations, added_anchors=report['added_anchors'],
        visual_acceptance=False)


def review():
    report, checks = verify()
    paths = [BASE/n for n in ['plan.md', 'prepared-inputs.json', 'manuscript-plan-review.json',
        'source-audit.json', 'mathematical-review.json', 'copyedit-review.json',
        'traceability-review.json', 'exact-results.json', 'graph-development.tex', 'panel-development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']]
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving graph-wrapper and commercial-panel source/math/text delta',
        checks=checks, evidence=[ref(p, 'Reviewed delta and preservation evidence') for p in paths]+[
            ref(Path(__file__), 'Exact preservation and manuscript review')],
        findings=['All763 predecessor source records,201 scholarly PDFs, citation contexts and unchanged compiled inputs survive.',
            'Wrapper preconditions, graph type, empty-result semantics, search completeness and component-specific rights remain explicit.',
            'Exact structural calculations explain confounding, collider and mediation conversion failures.',
            'The normal-equation solution and inverse-Gram functional independently verify the negative projection and positive ATT.',
            'Commercial control/base/aggregation/inference options are source-specific, and cutoff/edition/source omissions remain visible.',
            'The common dispatcher refusal is observed; native graph/panel integration and licensed vendor trials are proposed.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


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
        build_report=ref(OUT/'build-report.json', 'Preserving graph/panel build'),
        source_review=ref(BASE/'release-source-review.json', 'Author source/math/preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Add bounded DAGitty wrapper/rights comparison with exact structural examples.',
                 'Add commercial cohort-time DID targets, negative-weight example, aggregation and inference boundaries.'],
        visual_acceptance=False, mandatory_repairs_closed=[],
        sponsor_binding='Predecessor sponsor stays paired to its original reader; a preserving exact-reader sponsor follows.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed graph/panel working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_graph_panel_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': 'All763 predecessor citation records and contexts survive with201 genuine scholarly PDFs. Nine bounded primary/project records add fourteen pinned DAGitty blobs, five official panel originals, exact authored references and an actual dispatcher probe. Cutoff bytes/editions and other commercial families remain unresolved.',
        'Q3': 'Separate direct structural calculations reproduce confounding, collider and mediation contrasts. Rational normal equations and inverse-Gram weights reproduce ATT34 versus TWFE -91/8 thousand USD. The saved panel dispatcher request is completed/unsupported; no native DAGitty, vendor run, sampling coverage or installed adapter is inferred.',
        'Q4': 'The stipulated branch-period cost10000USD yields retrospective average net24000USD under the declared law. Treating the scalar projection as ATT would give the explicitly invalid -21375USD. No prospective policy value or bank ROI is claimed; prior financial examples remain unchanged.'}
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
                    ref(BASE/'source-audit.json', 'Authentic primary identities and project references'),
                    ref(BASE/'mathematical-review.json', 'Independent exact calculations'),
                    ref(Path(__file__), 'Exact-reader author findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving author delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record bounded graph/panel source, mathematics and monetary interpretation.'))
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
    commands = dict(review=review, publish=publish, renew=renew)
    parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
