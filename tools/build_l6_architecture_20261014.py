#!/usr/bin/env python3
"""Prepare exact architectural examples and a preserving L6 chapter successor."""
import argparse
from contextlib import redirect_stdout
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import re

import audit_reader_traceability_v2_20261013 as trace
import build_native_evaluation_reader_v3_20261014 as engine
import master_control as core
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-14/l6-architecture'
OUT = BASE / 'reader'
OLD = ROOT / 'docs/causal_proposal_artifact_custody_2026-10-14.tex'
PRIOR = ROOT / 'docs/program/execution/2026-10-14/artifact-custody/publication/reader/source-audit.json'
NAME = 'causal_proposal_agent_backends_2026-10-14'
DRIVER = ROOT / 'docs' / (NAME + '.tex')
PDF = DRIVER.with_suffix('.pdf')
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.L6/chapter.tex'
PROTOTYPE = ROOT / 'docs/program/repair-v12/work/LA05/chapter-draft.tex'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}


def calculate():
    deps = {'identification': ['target', 'graph'],
            'estimation': ['identification', 'data'],
            'valuation': ['estimation', 'cost'], 'report': ['valuation'],
            'clock_diagnostic': ['data', 'clock_rule']}
    def descendants(changed):
        reached = set(changed)
        while True:
            extra = {node for node, parents in deps.items() if set(parents) & reached}
            if extra <= reached:
                return sorted(reached - set(changed))
            reached |= extra
    assert descendants(['target']) == ['estimation', 'identification', 'report', 'valuation']
    assert descendants(['cost']) == ['report', 'valuation']
    assert descendants(['data']) == ['clock_diagnostic', 'estimation', 'report', 'valuation']
    budget, settled, bound = F(10), F(6), F(3)
    naive = [settled + bound <= budget for _ in range(2)]
    assert all(naive) and settled + 2 * bound == 12
    orders = []
    for order in itertools.permutations(['A', 'B']):
        reserved = F(0)
        admitted = []
        for task in order:
            accept = settled + reserved + bound <= budget
            if accept:
                reserved += bound
            assert settled + reserved <= budget
            admitted.append({'task': task, 'admitted': accept, 'total_with_reservations': str(settled + reserved)})
        assert [row['admitted'] for row in admitted] == [True, False]
        final_settled = settled + 2
        final_reserved = reserved - bound
        assert final_settled == 8 and final_reserved == 0
        orders.append({'order': list(order), 'transitions': admitted,
                       'after_settlement': str(final_settled),
                       'second_fits_after_settlement': final_settled + bound <= budget})
    histories = []
    for completed_before_timeout in [0, 1]:
        histories.append({'local_observation': ['submitted', 'timeout_without_receipt'],
                          'remote_completions_before_retry': completed_before_timeout,
                          'after_one_successful_resubmission': completed_before_timeout + 1,
                          'without_resubmission': completed_before_timeout})
    assert histories[0]['local_observation'] == histories[1]['local_observation']
    cost_a, cost_b, error_a, error_b = F(1), F(4), F(2, 25), F(1, 50)
    threshold = (cost_b - cost_a) / (error_a - error_b)
    assert threshold == 50
    route = []
    for loss in [F(10), F(100)]:
        total_a, total_b = cost_a + loss * error_a, cost_b + loss * error_b
        route.append({'loss': str(loss), 'A': str(total_a), 'B': str(total_b),
                      'preferred': 'A' if total_a < total_b else 'B'})
    assert route == [{'loss': '10', 'A': '9/5', 'B': '21/5', 'preferred': 'A'},
                     {'loss': '100', 'A': '9', 'B': '6', 'preferred': 'B'}]
    return {'kind': 'project_exact_algebra_and_finite_state_examples',
            'dependency_graph': deps,
            'invalidated': {key: descendants([key]) for key in ['target', 'cost', 'data']},
            'budget': {'ceiling': '10', 'initial_settled': '6', 'per_request_upper_bound': '3',
                       'naive_admission': naive, 'naive_total': '12', 'serialized_orders': orders},
            'unknown_outcome_histories': histories,
            'routing': {'A_cost': str(cost_a), 'B_cost': str(cost_b), 'A_error': str(error_a),
                        'B_error': str(error_b), 'equal_loss_threshold': str(threshold), 'scenarios': route},
            'limitations': ['Stipulated values, no measured prices/model errors or bank ROI.',
                           'Dependency/reservation invariants rely on stated atomic transitions and complete dependency/bound premises.',
                           'Unknown-outcome argument is restricted to identical local observations without additional provider information.',
                           'No provider or downloaded framework code executed.']}


def prepare():
    assert not DRIVER.exists() and not CHAPTER.exists() and not (BASE / 'prepared-inputs.json').exists()
    prior = json.loads(PRIOR.read_text())
    verify_bindings(prior)
    write(BASE / 'exact-results.json', calculate())
    keyset = {'v12_la04_langgraph', 'v12_la04_pydantic_ai', 'v12_la04_autogen',
              'v12_la_package_pywhy_llm', 'v12_la_package_causalagent', 'v12_la_package_oci_agent',
              'v12_la_package_cladder', 'v12_la_package_causalds', 'v12_la_package_ontolearner',
              'v12_la_package_lcm', 'v12_la_package_llm_cd', 'v12_la_package_llm_scd',
              'exec13_architecture_local'}
    selected = [row for row in prior['sources'] if row['integrated_citation_key'] in keyset]
    assert len(selected) == len(keyset)
    primary = {'reviewer': REVIEWER, 'cutoff': '2026-10-07',
               'selected_inherited_records': selected,
               'source_reinspection': [ref(ROOT / p, anchor) for p, anchor in [
                   ('docs/literature/raw/v12_la04_langgraph_source_1.txt', '1177-1213 compile/checkpointer'),
                   ('docs/literature/raw/v12_la04_langgraph_source_2.txt', '893-925 interrupt restarts node'),
                   ('docs/literature/raw/v12_la04_pydantic_ai_source_1.txt', '470-625 request/token/cost checks and missing-price warning'),
                   ('docs/literature/raw/v12_la04_pydantic_ai_source_2.txt', '335-390 tool fields, sequential=False and requires_approval=False'),
                   ('docs/literature/raw/v12_la04_autogen_source_1.txt', '114-165 state/concurrency/reflect; 1630-1640 model-context persistence'),
                   ('src/causalbank/agent_workflow_v12.py', 'validate_proposal, verify_sources, project_context, prepare and run')]],
               'inherited_package_decisions': ref(ROOT / 'docs/program/repair-v12/work/LA04/agent-package-decisions.json',
                                                 'Component-specific adoption, integration, rejection and defer decisions'),
               'scope': 'Selected pinned semantics and inherited audited package boundaries; no exhaustive provider/framework census or new upstream execution.'}
    write(BASE / 'primary-review.json', primary)
    original = PROTOTYPE.read_text()
    marker = '\\section{The implemented boundary}'
    body = original[original.index(marker):]
    (BASE / 'prototype-body.tex').write_text(body)
    assert (BASE / 'prototype-body.tex').read_text() == body
    draft = (BASE / 'development.tex').read_text()
    inferred_keys = {key.strip() for group in re.findall(engine.shared.CITE, draft) for key in group.split(',')}
    assert inferred_keys - keyset == {'exec14_l6_exact', 'exec14_l6_design', 'exec14_l6_local'}
    CHAPTER.parent.mkdir(parents=True)
    CHAPTER.write_text('\\input{program/execution/2026-10-14/l6-architecture/development.tex}\n' +
        '\\input{program/execution/2026-10-14/l6-architecture/prototype-body.tex}\n' +
        '\\par The local implementation and historical conformance counts in this chapter are bound to the preserved source, original trials and subsequent six-case replay. They do not constitute new provider execution.\\cite{exec14_l6_local}\n' +
        '\\label{exec14:l6-end}\n')
    design = {'kind': 'project_architecture_design', 'reviewer': REVIEWER,
              'scope': 'Provider-neutral analysis contracts; no service-specific feature, price or availability claim.',
              'decisions': ['Plain controller baseline; conditional LangGraph/Pydantic AI adapters; AutoGen comparative/isolated candidate.',
                            'Model envelopes retain raw inputs/outputs, revisions, settings and failure states.',
                            'External grants cannot be supplied by model response; scientific status promotion requires new evidence.',
                            'Backend eligibility precedes cost/performance routing; public/generated pilot before bank trials.'],
              'derivation_review': ['Reuse invariant induction assumes all dependencies are recorded and changed descendants are retired.',
                                    'Reservation invariant assumes atomic admission and credible upper bounds; unknown charges retain reservation.',
                                    'Identical local submitted/timeout histories cannot distinguish zero from one remote completion.',
                                    'Routing threshold assumes one error category with calibrated conditional probability and fixed loss.'],
              'evidence': [ref(BASE / 'primary-review.json', 'Inherited and reinspected source identities'),
                           ref(BASE / 'exact-results.json', 'Exact calculations'),
                           ref(BASE / 'plan-review.md', 'Reviewed scope and official-source access limitation')],
              'open_questions': ['Broader backend/framework census', 'Pre-cutoff official provider capabilities and contract terms',
                                 'Actual model quality, costs and adjudication effort', 'Runtime/dependency/rights closure',
                                 'Owner custody and institutional acceptance']}
    write(BASE / 'design-review.json', design)
    omission = {'status': 'open', 'cutoff': '2026-10-07',
                'attempts': [{'url': url, 'sandbox_http': 403, 'elevated_retry_http': 403,
                              'bytes_inspected': False} for url in [
                    'https://developers.openai.com/api/docs/guides/structured-outputs',
                    'https://platform.openai.com/docs/guides/structured-outputs']],
                'impact': 'No new OpenAI service-specific claim or exhaustive backend census closure.',
                'trigger': 'Acquire and inspect authentic official evidence with version/date and applicable pre-cutoff status.',
                'independent_work': 'Framework comparison, local controller, project derivations and chapter development remain eligible.'}
    write(BASE / 'omissions-register.json', omission)
    evidence = [ref(ROOT / 'docs/program/repair-v12/work/LA05' / n, anchor) for n, anchor in [
        ('verification.json', 'Historical 6 cases, 29 controller tests and 80 combined checks'),
        ('prototype-evidence.json', 'Original executed local cases'),
        ('failure-trials.json', 'Original adverse local inputs and recovery'),
        ('receipt.json', 'Preserved scoped author review')]]
    local = {'source': ref(ROOT / 'src/causalbank/agent_workflow_v12.py', 'Offline fixed-operation controller'),
             'original_chapter': ref(PROTOTYPE, 'Original prototype exposition preserved byte for byte after its heading'),
             'body': ref(BASE / 'prototype-body.tex', 'Exact body copy under L6'),
             'historical_evidence': evidence,
             'replay': ref(ROOT / 'docs/program/execution/2026-10-13/prototype-review/agent-replay/receipt.json',
                           'Six-case successor local replay, no upstream framework or model execution')}
    verify_bindings(local)
    write(BASE / 'local-evidence-review.json', local)
    sources = []
    for key, title, kind, path, anchor, claims, records in [
        ('exact', 'Exact state invalidation, unknown-outcome, reservation and routing examples', 'project_derivation',
         BASE / 'exact-results.json', 'Four finite/rational examples; calculate() independently enumerates the stated cases',
         ['Target change retires four descendants; cost change retires two.',
          'Naive parallel cost12 exceeds10; serialized reservations admit only one request.',
          'Identical timeout histories conceal zero or one completed external effect.',
          'Stipulated route threshold50USD; totals9/6 at loss100,1.8/4.2 at loss10.'],
         [{'local_copy': ref(Path(__file__).resolve(), 'calculate(): exact fractions, permutations and descendant traversal')}]),
        ('design', 'Scoped model-backend and orchestration architecture design', 'project_design',
         BASE / 'design-review.json', 'Backend contracts, framework choices and proof premises',
         design['decisions'] + design['derivation_review'],
         [{'local_copy': ref(BASE / 'primary-review.json', 'Selected inherited primary records and reinspection')},
          {'local_copy': ref(BASE / 'omissions-register.json', 'Source outage and broader census limitations')}]),
        ('local', 'Preserved proposal-to-tool controller implementation and historical trial evidence', 'project_implementation_evidence',
         BASE / 'local-evidence-review.json', 'Current source hash, preserved original chapter body and original/replayed cases',
         ['Offline/authored/recorded controller; local grants, narrow ATE projection, source and journal binding.',
          'Original six cases and 80 conformance checks remain historical evidence, not new model accuracy.'],
         evidence + [{'local_copy': ref(ROOT / 'src/causalbank/agent_workflow_v12.py', 'Inspected fixed operation path')}]),
    ]:
        sources.append(engine.source('exec14_l6_' + key, title, 'Causal banking proposal', kind,
                                     'Project-authored source and derivation', '2026-10-14; source bytes bound by SHA-256',
                                     path, anchor, claims, records))
    write(BASE / 'source-audit.json', {'sources': sources, 'cutoff': '2026-10-07',
                                     'prior': ref(PRIOR, '534 preserved citation records'),
                                     'recontextualized_source_review': ref(BASE / 'primary-review.json', 'New L6 contexts use scoped inherited claims')})
    bib = []
    for source in sources:
        bib.append('@misc{' + source['integrated_citation_key'] + ',\n author={{Causal banking proposal}},\n title={' +
                   engine.shared.escape(source['title']) + '},\n year={2026},\n note={' +
                   engine.shared.escape(source['version_date']) + '}\n}\n')
    (BASE / 'refs.bib').write_text('\n'.join(bib))
    text = OLD.read_text()
    old_input = r'\input{program/repair-v12/work/LA05/chapter-draft.tex}'
    assert text.count(old_input) == 1
    text = text.replace(old_input, r'\input{program/comprehensive-v14/work/TEXT.DRAFT.L6/chapter.tex}')
    text = re.sub(r'\\bibliography\{([^}]+)\}', lambda m: r'\bibliography{' + m.group(1) +
                  ',program/execution/2026-10-14/l6-architecture/refs}', text)
    DRIVER.write_text(text)
    write(BASE / 'prepared-inputs.json', {
        'inputs': [ref(p, 'Reviewed or preserved input') for p in [OLD, PRIOR, PROTOTYPE,
            BASE / 'plan-review.md', BASE / 'primary-review.json', BASE / 'design-review.json',
            BASE / 'exact-results.json', BASE / 'local-evidence-review.json', Path(__file__).resolve()]],
        'generated': [ref(p, 'Successor chapter/driver/source') for p in [
            DRIVER, CHAPTER, BASE / 'development.tex', BASE / 'prototype-body.tex', BASE / 'refs.bib', BASE / 'source-audit.json']],
        'preservation': 'Existing prototype body preserved; heading replaced by L6; every other inherited input unchanged.',
        'credit_policy': 'Measure after build; discount material allocated to other chapters. No automatic mandatory-repair closure.',
        'visual_acceptance': False})
    print(json.dumps({'prepared': str(DRIVER.relative_to(ROOT)), 'exact_examples': 'pass', 'new_sources': 3}))


def build():
    for name, value in {'BASE': BASE, 'OUT': OUT, 'OLD': OLD, 'NAME': NAME,
                        'DRIVER': DRIVER, 'PDF': PDF, 'PRIOR_AUDIT': PRIOR}.items():
        setattr(engine, name, value)
    with (BASE / 'compile-summary.log').open('x') as stream:
        with redirect_stdout(stream):
            engine.build()
    report = json.loads((OUT / 'build-report.json').read_text())
    aux = (OUT / (NAME + '.aux')).read_text()
    report.update(builder=ref(Path(__file__).resolve(), 'Preserving L6 builder'),
                  predecessor_pdf=ref(OLD.with_suffix('.pdf'), 'Frozen 719-page custody reader'),
                  chapter_sections={name: int(re.search(r'\\newlabel\{exec14:' + name +
                                    r'\}\{\{[^}]*\}\{(\d+)\}', aux).group(1))
                                    for name in ['l6', 'l6-extension-end', 'l6-end']})
    engine.core.write(OUT / 'build-report.json', report)
    result = trace.audit(DRIVER, OUT / 'source-audit.json')
    write(BASE / 'traceability-review.json', result)
    assert result['status'] == 'pass' and not result['issues']
    print(json.dumps({'pages': report['pages'], 'cited_records': report['cited_records'],
                      'chapter_sections': report['chapter_sections'], 'scholarly_pdfs': result['scholarly_pdfs'],
                      'material_warnings': [w for w in report['warnings'] if 'Underfull' not in w]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare', 'build'])
    args = parser.parse_args()
    prepare() if args.command == 'prepare' else build()
