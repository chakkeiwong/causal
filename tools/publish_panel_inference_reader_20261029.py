"""Review exact preservation and publish the panel-inference working successor."""
import argparse
import json
import re

import build_panel_inference_reader_20261029 as build
import run_program_checkpoint_v3 as controller
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run = controller.base
core = run.core
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
read = lambda p: json.loads(p.read_text())
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author source, exact logic/arithmetic and all-page text/bounds review; no fresh visual or independent acceptance.',
          'Selected source-derived baseline, target and weighting findings are distinct from native execution, authentic truth and calibration.',
          'Q1/Q5, mandatory coverage/depth, native port qualification, dependency rights and bank acceptance remain open.']


def verify():
    for name in ('prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'mathematical-review.json',
                 'copyedit-review.json', 'traceability-review.json', 'reader/source-audit.json',
                 'reader/build-report.json', 'reader/text-layout-review.json'):
        verify_bindings(read(BASE / name))
    report = read(OUT / 'build-report.json')
    audit = read(OUT / 'source-audit.json')
    index = read(BASE / 'traceability-review.json')
    bounds = read(OUT / 'text-layout-review.json')
    assert index['status'] == bounds['status'] == 'pass' and not index['issues']
    assert report['cited_records'] == 1451 and index['scholarly_pdfs'] == 277
    assert not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.DEVELOPMENT.read_text() == build.expected_development()
    assert build.exact.calculate() == read(BASE / 'exact-results.json')
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR)['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == 1449 and all(new[k] == v for k, v in old.items())
    assert new.keys() - old.keys() == {'exec29_panel_inference_sources','exec29_panel_inference_reference'}
    compiled = {item['path']: item for item in audit['tex_files']}
    kept = [item for item in read(build.PRIOR)['tex_files'] if item['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[item['path']]['sha256'] == item['sha256'] for item in kept)
    before = contexts(read(build.PREDECESSOR / 'traceability-review.json'))
    after = contexts(index, {str(build.DEVELOPMENT.relative_to(ROOT))})
    assert all(value == after[key] for key, value in before.items())
    pages = [' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', p).split()).replace('- ', '-')
             for p in (OUT / 'reader.txt').read_text().split(chr(12))]
    opening = 'A common panel schema must preserve the meaning of uncertainty as well as the numbers it displays.'
    closing = 'Unknown counterfactual trends and unqualified dependent-data uncertainty remain scientific limits that these adapter repairs cannot remove.'
    starts = [i for i, page in enumerate(pages) if opening in page]
    assert len(starts) == 1, starts
    start = starts[0]
    ends = [i for i in range(start, min(start + 24, len(pages))) if closing in pages[i]]
    assert len(ends) == 1, ends
    end = ends[0]
    text = ' '.join(pages[start:end + 1])
    text = text[text.index(opening):text.index(closing) + len(closing)]
    for token in ('9/8', '5/2', 'nonabsdid', 'parglm', 'leaps'):
        assert token in text, token
    return report, dict(preserved_citation_records=1449, added_citation_records=2,
          scholarly_pdfs=277, unchanged_compiled_inputs=len(kept), prior_citation_contexts_preserved=True,
          rendered_pages=[start + 1, end + 1], native_execution=False, visual_acceptance=False)


def review():
    report, checks = verify()
    evidence = [ref(BASE / n, 'Reviewed preserving integration') for n in
                ('prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'mathematical-review.json',
                 'copyedit-review.json', 'traceability-review.json', 'development.tex',
                 'reader/build-report.json', 'reader/text-layout-review.json')]
    evidence.append(ref(build.ROOT / 'tools/publish_panel_inference_reader_20261029.py', 'Performed preservation checks'))
    write(BASE / 'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
          scope='Exact panel-inference delta with complete predecessor preservation', reviewed_reader=report['pdf'],
          checks=checks, evidence=evidence,
          findings=['All predecessor source records, citation contexts and compiled content inputs are retained.',
                    'Twelve inspected schema/delegate files, metadata and exact conditional normalization witnesses and conditional reuse have distinct evidence and limits.'],
          limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def publish():
    report, _ = verify()
    reviewed = read(BASE / 'release-source-review.json')
    verify_bindings(reviewed)
    state = core.read(ROOT, core.STATE)
    digest = core.sha(ROOT / core.STATE)
    assert state['execution_runtime']['active'] is None
    assert run.same_reader(state['reader'], ref(build.OLD.with_suffix('.pdf'), 'Predecessor'))
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ('path', 'sha256')},
        build_report=ref(OUT / 'build-report.json', 'Preserving build'),
        source_review=ref(BASE / 'release-source-review.json', 'Author preservation review'),
        text_layout=ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT / 'source-audit.json')['tex_files'] + reviewed['evidence'],
        changes=['Integrate reviewed panel estimator support, nuisance and conversion contracts.'],
        visual_acceptance=False, mandatory_repairs_closed=[], sponsor_binding='Pair sponsor to exact reader bytes.')
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed panel-inference successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ('path', 'sha256')}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, digest, state, dict(action='publish_fixture_java_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, _ = verify()
    binding = ref(BASE / 'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = dict(
        Q2='All 1449 predecessor source records, contexts and compiled content inputs preserved; 1451 audited records and 277 scholarly PDFs.',
        Q3='Prior mathematics preserved. Exact normalization, partial-interval, label and clock examples retain source and native limits; no native or statistical calibration.',
        Q4='The panel review specifies intervention clocks, clean-control populations, baselines, weights and dependence; no acquired engine or bank qualification is claimed.')
    for q, finding in findings.items():
        op = 'PROPOSAL.' + q
        state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][op]
        old = core.read(ROOT, previous['path'])
        assert old['reviewed_reader']['sha256'] != report['pdf']['sha256']
        folder = BASE / q
        folder.mkdir()
        evidence = [previous, binding, ref(BASE / 'release-source-review.json', 'Preservation review'),
                    ref(BASE / 'mathematical-review.json', 'Exact arguments'), ref(BASE / 'source-audit.json', 'Primary evidence')]
        write(folder / 'reopen.json', dict(reason='Preserving successor requires an exact-byte delta review.',
              prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
              next_action='Record bounded exact-reader author review.'))
        transition('reopen', op, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = run.ledger.operation(graph, op)
        attempt = len(state['execution_runtime']['review_history'][op])
        output = ROOT / run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations'] + LIMITS))
        scope = 'Author panel-inference delta; proposal only'
        write(output, dict(operation=op, status='pass', criterion=node['criteria'][0], reviewer=REVIEWER,
              reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only', scope=scope,
              findings=[finding], evidence=evidence, limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER, limitations=limits,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Exact-reader author review')], nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder / 'operation-receipt.json', receipt)
        transition('record', op, folder / 'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['review', 'publish', 'renew'])
    globals()[parser.parse_args().command]()
