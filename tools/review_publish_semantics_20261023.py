#!/usr/bin/env python3
"""Review preservation, exact arithmetic and rendered text before publishing."""
import argparse
import json
from pathlib import Path

import build_semantics_reader_v2_20261023 as build
from review_publish_observations_v2_20261022 import contexts
from publish_latent_r_review_v2_20261013 import ref, transition, verify_bindings, write
import run_program_reviews_v2 as extension

run = extension.base
core = run.core
ROOT, BASE, OUT = build.ROOT, build.BASE, build.OUT
REVIEWER = dict(name='Codex author/coordinator', kind='author')
LIMITS = ['Author primary-source, exact-arithmetic and rendered-text review; no independent or visual acceptance.',
    'Census63/50 and four crosscutting searches remain open; Q1/Q5 and mandatory repairs remain open.',
    'Selected scholarly v1 editions do not qualify their cited originals or later revisions.',
    'Source mismatches are unexecuted; reference-only decisions grant no adapter capability or native adoption.',
    'Authored laws and printed-table arithmetic establish no live-model superiority, statistical calibration or bank returns.']
read = lambda p: json.loads(p.read_text())


def verify():
    names = ['prepared-inputs.json', 'source-audit.json', 'source-completion-review.json',
        'plan-review.json', 'mathematical-review.json', 'copyedit-review.json',
        'traceability-review.json', 'reader/source-audit.json', 'reader/build-report.json']
    for name in names:
        verify_bindings(read(BASE / name))
    prepared = read(BASE / 'prepared-inputs.json')
    report, audit, index = [read(BASE / n) for n in
        ['reader/build-report.json', 'reader/source-audit.json', 'traceability-review.json']]
    assert report['cited_records'] == prepared['expected_cited_records']
    assert index['status'] == 'pass' and not index['issues']
    assert index['scholarly_pdfs'] == prepared['expected_scholarly_pdfs']
    bounds = read(OUT / 'text-layout-review.json')
    assert bounds['status'] == 'pass' and not bounds['empty_pages'] and not bounds['out_of_bounds']
    assert all('Underfull' in warning for warning in report['warnings'])
    assert build.DRIVER.read_text() == build.expected_driver()
    assert build.calculate() == read(BASE / 'exact-results.json')
    old = {s['integrated_citation_key']: s for s in read(build.PRIOR)['sources']}
    new = {s['integrated_citation_key']: s for s in audit['sources']}
    assert len(old) == prepared['prior_cited_records']
    assert all(new[k] == value for k, value in old.items())
    assert new.keys() - old.keys() == {s['integrated_citation_key'] for s in read(BASE / 'source-audit.json')['sources']}
    compiled = {r['path']: r for r in audit['tex_files']}
    kept = [r for r in read(build.PRIOR)['tex_files'] if r['path'] != str(build.OLD.relative_to(ROOT))]
    assert all(compiled[r['path']]['sha256'] == r['sha256'] for r in kept)
    before = contexts(read(build.PREDECESSOR / 'traceability-review.json'))
    additions = {str((BASE / name).relative_to(ROOT)) for name in build.INSERTIONS.values()}
    after = contexts(index, additions)
    assert all(value == after[key] for key, value in before.items())
    pages = [' '.join(p.split()).replace('- ', '-') for p in (OUT / 'reader.txt').read_text().split(chr(12))]
    ranges = {}
    specs = [
        ('iv', 'A reusable IV component must preserve', 'closes the broader IV/RD software landscape.',
         ['NCSA', 'Maven', 'lexicographic', 'EJML', 'covariance', 'source mismatch']),
        ('longitudinal', 'Sequential servicing software becomes useful', 'longitudinal reference while keeping adoption and coverage as later claims.',
         ['AGPL', '18.24', '11.89', '0.999', 'TMLE', 'SDR', 'ife']),
        ('context', 'A causal sentence in a service note', 'conditional on the authored mechanisms and cannot establish actual bank value.',
         ['Bernoulli', '90', '100', 'no-contact', 'FinCausal', 'text-only']),
        ('conflict', 'A bank analyst may encounter a chart', 'sequence makes the expensive study conditional on a demonstrated prototype merit.',
         ['82.46', '80.99', '53.99', '54.58', '57.25', '58.51', '2.24', '50.53', 'logits'])]
    for name, first, last, tokens in specs:
        starts = [i for i, p in enumerate(pages) if first in p]
        assert len(starts) == 1, (name, starts)
        start = starts[0]
        ends = [i for i, p in enumerate(pages) if i >= start and last in p]
        assert len(ends) == 1, (name, ends)
        end = ends[0]
        text = ' '.join(pages[start:end + 1])
        assert all(token in text for token in tokens), (name, [t for t in tokens if t not in text])
        ranges[name] = dict(physical_pages=[start + 1, end + 1], checked_tokens=tokens)
    equations = {key: report['added_anchors'][key] for key in ['exec23:lmtp-shift', 'exec23:lmtp-odds',
        'exec23:lmtp-value', 'exec23:context-laws', 'exec23:context-observed', 'exec23:context-net', 'exec23:conflict-identity']}
    for key, anchor in equations.items():
        text = ' '.join(pages)
        assert '(' + anchor['number'] + ')' in text, key
    return report, dict(preserved_records=len(old), added_records=sorted(new.keys() - old.keys()),
        scholarly_pdfs=index['scholarly_pdfs'], unchanged_compiled_inputs=len(kept),
        all_prior_citation_contexts_preserved=True, rendered_ranges=ranges, equations=equations,
        census_inspected=63, census_unread=50, crosscutting_open=4,
        native_execution=False, visual_acceptance=False)


def review():
    report, checks = verify()
    names = ['prepared-inputs.json', 'source-audit.json', 'source-completion-review.json', 'plan-review.json',
        'mathematical-review.json', 'copyedit-review.json', 'traceability-review.json', 'exact-results.json',
        'reader/build-report.json', 'reader/source-audit.json', 'reader/reader.txt', 'reader/text-layout-review.json']
    names += list(build.INSERTIONS.values())
    write(BASE / 'release-source-review.json', dict(status='pass', issues=[], reviewer=REVIEWER,
        reviewed_reader=report['pdf'], scope='Preserving connected software and causal-language synthesis',
        checks=checks, evidence=[ref(BASE / n, 'Reviewed preserving integration') for n in names] +
            [ref(Path(__file__), 'Exact preservation and rendered-text review')],
        findings=['All prior citation identities, contexts and compiled content inputs are preserved.',
            'Two genuine pre-cutoff papers and three reasoned software source findings are integrated.',
            'Policy-law values, observational equivalence, prediction partition and table arithmetic reproduce.',
            'Reported paper contradictions are retained without silently repairing experimental data.',
            'Public/generated prototype comparisons precede costly bank trials; native and bank claims remain separate.'],
        limitations=LIMITS, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', pages=report['pages'], records=report['cited_records'], checks=checks)))


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
        build_report=ref(OUT / 'build-report.json', 'Preserving semantics build'),
        source_review=ref(BASE / 'release-source-review.json', 'Primary-source and preservation review'),
        text_layout=ref(OUT / 'text-layout-review.json', 'All-page text bounds'),
        source_artifacts=read(OUT / 'source-audit.json')['tex_files'] + record['evidence'],
        changes=['Integrate causal-language boundaries, multimodal conflict critique, IV reference choices and longitudinal policy semantics.'],
        visual_acceptance=False, mandatory_repairs_closed=[], sponsor_binding='Pair sponsor to exact current reader.')
    write(BASE / 'working-release.json', manifest)
    binding = ref(BASE / 'working-release.json', 'Reviewed semantics working successor')
    run.ledger.validate_working_release(ROOT, binding)
    state['execution_program']['working_releases'].append(binding)
    state['reader'] = {k: report['pdf'][k] for k in ['path', 'sha256']}
    state['reader'].update(pages=report['pages'], status='Working monograph; not I02 acceptance')
    state['deliveries'].append(dict(state['reader']))
    run.commit(ROOT, before, state, dict(action='publish_semantics_reader', manifest=binding, final_acceptance=False))
    print(json.dumps(dict(published=state['reader'], proposal_accepted=False)))


def renew():
    report, checks = verify()
    binding = ref(BASE / 'working-release.json', 'Exact current reader')
    run.ledger.validate_working_release(ROOT, binding)
    findings = dict(
        Q2=f'All{checks["preserved_records"]} earlier source identities/contexts are preserved. Two selected pre-cutoff genuine PDFs and three pinned software source reviews retain primary anchors and edition/rights limits. Census63/50 and four searches remain open.',
        Q3='The two-period policy law yields184/25,456/25,107/9; observational twins have equal observed laws but effects100/0; the correctness partition and printed-table subtractions reproduce. Source flags, authored proofs and empirical model results remain distinct.',
        Q4='All-contact versus no-contact incremental net90 versus-10 USD and different two-period contact-policy values make target ambiguity economically material under stipulated laws. Public/generated trials are proposed before costly bank studies; no measured bank benefit is claimed.')
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
            ref(BASE / 'source-audit.json', 'Primary originals and authored references'),
            ref(BASE / 'mathematical-review.json', 'Exact arguments'), ref(Path(__file__), 'Exact-reader findings')]
        write(folder / 'reopen.json', dict(reason='Changed reader requires exact delta review.',
            prior_result=previous, reviewed_reader=report['pdf'], evidence=evidence,
            next_action='Record primary-source, arithmetic and monetary delta for exact reader.'))
        transition('reopen', identifier, folder / 'reopen.json')
        state = core.read(ROOT, core.STATE)
        graph, _, _ = run.combined(ROOT, state)
        node = next(n for n in graph['nodes'] if n['id'] == identifier)
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
