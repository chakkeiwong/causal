#!/usr/bin/env python3
"""Review and preserve the exact-reader sensitivity and IV manuscript successor."""
import argparse
import json
from pathlib import Path

import build_sensitivity_iv_reader_20261022 as build
import review_publish_observations_v2_20261022 as prior_review
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write

run, core = prior_review.run, prior_review.core
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = [
    'Selected original-source and authored mathematical review; no downloaded software executed.',
    'HonestDiD is reference-only; native worker, solver status and dependency qualification remain open.',
    'Python IV/RD coverage remains unfinished; RD, CausalPy IV and complementary searches require review.',
    'No uniform calibration, live-model superiority, measured bank economics or independent acceptance.',
    'Q1/Q5, mandatory repairs, fresh rendered review and final acceptance remain open.']
read = lambda p: json.loads(p.read_text())


def verify():
    for name in ['prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'review.json',
            'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
            'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']:
        verify_bindings(read(BASE/name))
    prepared, report, audit, index = [read(BASE/n) for n in
        ['prepared-inputs.json', 'reader/build-report.json', 'reader/source-audit.json', 'traceability-review.json']]
    assert report['cited_records'] == prepared['expected_cited_records']
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs']
    bounds = read(OUT/'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in w for w in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.exact.calculate() == read(BASE/'exact-results.json')
    prior = read(build.PRIOR)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == prepared['prior_cited_records'] and all(new[k] == v for k, v in old.items())
    assert new.keys()-old.keys() == {r['integrated_citation_key'] for r in read(BASE/'source-audit.json')['sources']}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in prior['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = prior_review.contexts(read(build.PREDECESSOR/'traceability-review.json'))
    excluded = {str(p.relative_to(ROOT)) for p in [build.DEVELOPMENT, build.IV_DEVELOPMENT]}
    after = prior_review.contexts(index, excluded)
    assert all(c == after[k] for k, c in before.items())
    pages = [' '.join(p.split()) for p in (OUT/'reader.txt').read_text().split(chr(12))]
    sections = {}
    for key, first, last, tokens, labels in [
        ('sensitivity', 'A funding manager evaluating a branch offer needs to distinguish a plausible',
         'whether a later bank experiment is worth its cost.',
         ['HonestDiD', '0.2.8', '2.9233', '10.9233', '7/4', 'C-LF', 'CVXR', 'T'],
         ['exec22:hd-'+s for s in ['rm', 'sd', 'law', 'ellipse', 'components', 'endpoints', 'example']]),
        ('python_iv', 'An instrument-based banking proposal must say which variation changes the',
         'with its unresolved assumptions visible to the decision maker.',
         ['linearmodels', 'pyfixest', '0.0183', '0.0346', 'CausalPy', 'MCP'],
         ['exec22:pyiv-witness', 'exec22:pyiv-ratio'])]:
        starts = [i for i, p in enumerate(pages) if first in p]
        assert len(starts) == 1, (key, starts)
        start = starts[0]
        ends = [i for i, p in enumerate(pages) if i >= start and last in p]
        assert len(ends) == 1, (key, ends)
        end = ends[0]
        text = ' '.join(pages[start:end+1])
        for token in tokens:
            assert token in text, (key, token)
        equations = {k: report['added_anchors'][k]['number'] for k in labels}
        assert all('('+n+')' in text for n in equations.values())
        sections[key] = dict(physical_pages=[start+1, end+1], equations=equations)
    decision = read(ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_honestdid/decision.json')
    assert decision['decision'] == 'reference' and decision['integration_allowed'] is False
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys()-old.keys()),
        unchanged_compiled_inputs=len(kept), all_prior_citation_contexts_preserved=True,
        sections=sections, visual_acceptance=False, native_execution=False)


def review():
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'plan-review.json', 'review.json',
        'mathematical-review.json', 'copyedit-review.json', 'manuscript-plan-review.json',
        'traceability-review.json', 'exact-results.json', 'development.tex', 'python-development.tex',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']
    write(BASE/'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving sensitivity and Python IV source and argument review',
        checks=checks, evidence=[ref(BASE/n, 'Reviewed delta and preservation evidence') for n in names]+
            [ref(Path(__file__), 'Exact preservation checks')], findings=[
            'All prior source identities, contexts and compiled content inputs survive.',
            'RM and SD restrictions have different zero points and tuning units; joint covariance changes uncertainty.',
            'The conservative known-Gaussian projection is independently derived and does not reproduce optimized package inference.',
            'Grid membership, bounds, warnings, solver status, target ordering and covariance must survive conversion.',
            'Separate matrix ranks do not establish projected rank or exclusion; weighted fits require preserved sample and weight roles.',
            'First-stage scalings and actual reference distributions can differ; overidentification diagnostics are not coefficient-null inversions.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], checks=checks)))


def publish():
    report, _ = verify()
    review_record = read(BASE/'release-source-review.json'); verify_bindings(review_record)
    state = core.read(ROOT, core.STATE); before = core.sha(ROOT/core.STATE)
    assert state['execution_runtime']['active'] is None
    assert state['reader']['path'] == str(build.OLD.with_suffix('.pdf').relative_to(ROOT))
    manifest = dict(kind='working_monograph', final_acceptance=False, pdf=report['pdf'], pages=report['pages'],
        supersedes={k: state['reader'][k] for k in ['path', 'sha256']},
        build_report=ref(OUT/'build-report.json', 'Preserving sensitivity and IV build'),
        source_review=ref(BASE/'release-source-review.json', 'Source, arithmetic and preservation review'),
        text_layout=ref(OUT/'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT/'source-audit.json')['tex_files']+review_record['evidence'],
        changes=['Integrate trend restrictions, Gaussian projection, reference-only reuse, projected rank and diagnostic distribution semantics.'],
        visual_acceptance=False, mandatory_repairs_closed=[], sponsor_binding='Pair a preserving sponsor to exact reader bytes.')
    write(BASE/'working-release.json', manifest)
    binding = ref(BASE/'working-release.json', 'Reviewed sensitivity and IV working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_sensitivity_iv_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify(); binding = ref(BASE/'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = {
        'Q2': f'All {checks["preserved_records"]} prior source identities and citation contexts survive. Seven audited records add pinned sensitivity and IV originals and labeled authored references. The genuine Rambachan-Roth paper remains unchanged. Release equivalence, dependencies and incomplete Python landscape review are explicit.',
        'Q3': 'RM and SD identified intervals, known-Gaussian ellipse projection with attained extrema, covariance counterfactuals, grid counterexamples, exact projected-rank/exclusion witness and Wald distribution examples reproduce. No package equivalence, empirical coverage or general identification claim is made.',
        'Q4': 'Stipulated contribution4 and cost1 give net3; full Gaussian sensitivity projection gives net bounds-3.9233/9.9233 and cannot justify confidently positive value. Public generated panels and matched baselines precede native qualification or bank experiments; reference-only reuse limits avoid asserting unmeasured benefits.'}
    for q, finding in findings.items():
        identifier = 'PROPOSAL.'+q; state = core.read(ROOT, core.STATE)
        assert run.same_reader(state['reader'], report['pdf'])
        previous = state['execution_runtime']['results'][identifier]; old = core.read(ROOT, previous['path'])
        if old.get('reviewed_reader', {}).get('sha256') == report['pdf']['sha256']: continue
        folder = BASE/q; folder.mkdir(exist_ok=False)
        evidence = [previous, binding, ref(BASE/'release-source-review.json', 'Preserving author review'),
            ref(BASE/'source-audit.json', 'Audited sources'), ref(BASE/'mathematical-review.json', 'Scoped exact laws'),
            ref(Path(__file__), 'Exact-reader findings')]
        write(folder/'reopen.json', dict(reason='Changed reader requires preserving delta review.', prior_result=previous,
            reviewed_reader=report['pdf'], evidence=evidence, next_action='Record sensitivity and IV source, mathematical and value delta.'))
        transition('reopen', identifier, folder/'reopen.json')
        state = core.read(ROOT, core.STATE); graph, _, _ = run.combined(ROOT, state); node = run.ledger.operation(graph, identifier)
        attempt = len(state['execution_runtime']['review_history'][identifier])
        output = ROOT/run.review_output_paths(node, state['reader'], attempt)[0]
        limits = list(dict.fromkeys(old['limitations']+LIMITS)); scope = 'Author exact-reader preserving delta review; proposal evidence only'
        write(output, dict(operation=identifier, status='pass', criterion=node['criteria'][0], reviewer=REVIEWER,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only', scope=scope,
            findings=[finding], evidence=evidence, limitations=limits, visual_acceptance=False))
        receipt = run.ledger.receipt_template(node)
        receipt.update(outcome='pass', execution='performed', scope=scope, reviewer=REVIEWER, limitations=limits,
            reviewed_reader=report['pdf'], review_attempt=attempt, acceptance_scope='proposal_only',
            outputs=[ref(output, 'Exact-reader '+q+' review')], nonexecution_reason='', revisit_trigger='',
            criteria=[dict(index=0, verdict='pass', finding=finding, evidence=evidence)])
        write(folder/'operation-receipt.json', receipt); transition('record', identifier, folder/'operation-receipt.json')
    print(json.dumps(dict(exact_reader_reviews='Q2-Q4 pass', Q1_Q5='open', proposal_accepted=False)))


if __name__ == '__main__':
    commands = dict(review=review, publish=publish, renew=renew)
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=commands)
    commands[parser.parse_args().command]()
