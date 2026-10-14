#!/usr/bin/env python3
"""Bind a primary-source evaluation synthesis and replay its illustrative arithmetic."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import master_control as core
import run_program as control

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-14/evaluation-cost'
SYN = ROOT / 'docs/program/comprehensive-v14/work/LL.TASK.evaluation_cost/task-synthesis.md'
AUDIT = ROOT / 'docs/program/repair-v12/work/LA01/source-audit.json'
CENSUS = ROOT / 'docs/program/execution/2026-10-13/llm-census/source-audit.json'
OMISSIONS = ROOT / 'docs/program/repair-v12/work/LA01/omissions.json'
SEARCH = ROOT / 'docs/program/execution/2026-10-13/llm-census/search-ledger.json'
PROTOCOL = ROOT / 'docs/program/repair-v12/work/LA06/protocol.json'


def ref(path, anchor):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def calculate():
    effects = [F(105)-F(100), F(135)-F(120)]
    ate = sum(effects, F(0))/2
    assert effects == [F(5), F(15)] and ate == 10
    rates = {'identified_interval_availability': F(70, 80),
             'coverage_given_identified_return': F(63, 70),
             'identified_return_and_cover': F(63, 80),
             'correct_refusal_given_nonidentified': F(16, 20),
             'all_request_admissible_return_and_cover': F(63, 100)}
    wage = F(60)
    token_cost = F(30000)*F(2, 1000000) + F(5000)*F(8, 1000000)
    ordinary = F(30, 60)*wage + 1
    no_escalation = F(10, 60)*wage + 2 + token_cost + F(1, 5) + F(1, 5)
    escalation_charge = F(30, 60)*wage
    assisted = no_escalation + F(1, 5)*escalation_charge
    saving = ordinary - assisted
    added_loss = F(1, 1000)*10000
    net = saving-added_loss
    q_limit = (ordinary-no_escalation)/escalation_charge
    fixed = F(12500)
    assert (token_cost, ordinary, assisted, saving) == (F(1, 10), F(31), F(37, 2), F(25, 2))
    assert (net, fixed/saving, fixed/net, q_limit) == (F(5, 2), F(1000), F(5000), F(37, 60))
    assert saving-F(2, 1000)*10000 == F(-15, 2)
    epsilon, failure = .05, .05
    count = math.ceil(2*math.log(2/failure)/epsilon**2)
    assert count == 2952
    assert 2*math.exp(-count*epsilon**2/2) <= failure
    assert 2*math.exp(-(count-1)*epsilon**2/2) > failure
    return {'status': 'pass', 'evidence_type': 'stipulated_project_examples_not_empirical_results',
            'target_example': {'stratum_masses': ['1/2', '1/2'], 'propensity': '1/2',
                               'control_means': [100, 120], 'treated_means': [105, 135],
                               'CATE': list(map(str, effects)), 'ATE': str(ate),
                               'assumptions': 'Random assignment, consistency, no interference and declared observation law.'},
            'request_accounting': {'requested': 100, 'identified': 80, 'nonidentified': 20,
                                   'admissible_intervals': 70, 'covered': 63, 'identified_failures': 10,
                                   'correct_refusals': 16, 'unsupported_numbers': 4,
                                   'rates': {k: str(v) for k, v in rates.items()}},
            'cost_scenario_USD': {'prices_are_illustrative': True, 'wage_per_hour': str(wage),
                                 'token_cost': str(token_cost), 'ordinary': str(ordinary),
                                 'assisted_before_escalation': str(no_escalation),
                                 'escalation_probability': '1/5', 'escalation_charge': str(escalation_charge),
                                 'assisted_expected': str(assisted), 'variable_saving': str(saving),
                                 'fixed_cost': str(fixed), 'break_even_no_extra_error': str(fixed/saving),
                                 'added_error_probability': '1/1000', 'loss_per_error': '10000',
                                 'added_expected_loss': str(added_loss), 'net_saving': str(net),
                                 'break_even_with_extra_error': str(fixed/net),
                                 'net_saving_at_extra_error_2_per_1000': '-15/2',
                                 'escalation_probability_zero_variable_saving': str(q_limit)},
            'planning': {'independent_mechanisms': 400, 'variants': 4, 'repetitions': 3,
                         'requests_per_arm': 4800, 'normal_single_proportion_half_width': .049,
                         'normal_worst_case_paired_half_width': .098,
                         'bounded_mean_half_width': epsilon, 'bounded_mean_failure_probability': failure,
                         'sufficient_independent_mechanisms': count,
                         'is_final_sample_size': False},
            'scope_limits': ['No upstream package or model executed.',
                             'No observed bank assignment, losses or reviewer times.',
                             'Bounded-mean calculation assumes independent mechanism-level scores in [-1,1].',
                             'Arithmetic break-even is not a measured return on investment.']}


def main():
    assert SYN.exists() and not (BASE/'operation-receipt.json').exists()
    sources = {x['id']: x for x in json.loads(AUDIT.read_text())['sources']}
    anchors = {
        'v12_la_2312_04350': 'PDF pp. 3, 8, 10; Table 2 62.03/70.40; formal query scope and contamination limits',
        'v12_la_2607_08093': 'PDF pp. 10-11; Section 5 and Figure 3: scene composition, settings, tool-output failures; interval n=7 or 5',
        'v12_la_2407_19638': 'PDF pp. 2-3, 8-9; accessible corpora, synthetic exposure and generated contexts; scope of claims',
        'v12_la_2410_14146': 'PDF pp. 10-12; citations concern, six students, fixed stages, self-selected edges and 5/18,7/18,1/18 counts',
        'v12_la_2407_15073': 'PDF pp. 7-8; 16-25x token cost, single-agent ablation, graph and confounding limits',
        'v12_la_2608_09696': 'PDF pp. 4,7,9; open-loop policies, Figure 2 115/171 matched cells; identification and compute limits'}
    papers = []
    for key, anchor in anchors.items():
        row = sources[key]; path = ROOT/row['local_path']
        assert path.read_bytes().startswith(b'%PDF-')
        assert ref(path, anchor)['sha256'] == row['sha256']
        text_path = ROOT/row['extracted_text']
        papers.append({'id': key, 'title': row['title'], 'source_identity': row['url'],
                       'version': row['arxiv_version'],
                       'version_date': row.get('version_date', row.get('updated', row.get('published'))),
                       'accessed': row['accessed'], 'local_original': ref(path, anchor),
                       'extracted_primary_text': ref(text_path, anchor),
                       'inspected_anchors': [anchor], 'inherited_claims': row['claims'],
                       'supported_claims_here': anchor, 'scope': 'Literature inspection only'})
    later = json.loads(CENSUS.read_text())['sources']
    row = next(x for x in later if x['integrated_citation_key'] == 'exec13_census_causaleval')
    path = ROOT/row['local_path']
    assert path.read_bytes().startswith(b'%PDF-') and ref(path, '')['sha256'] == row['sha256']
    assert row['reconciles'] == 'LA01-candidate-107'
    papers.append({'id': row['integrated_citation_key'], 'title': row['title'],
                   'source_identity': row['source_identity'], 'version_date': row['version_date'],
                   'accessed': row['accessed_utc'],
                   'local_original': ref(path, 'PDF pp. 7 and 19; Table 3 task-dependent gains and mixed human baseline'),
                   'inspected_anchors': [x for x in row['inspected_anchors'] if x['pdf_page'] in [7,19]],
                   'supported_claims_here': ['GPT-4o CoT/FunctionCall CLADDER 69/76; e-CARE 90/73.',
                                             'Starred models use 100 samples; human scores mix published reports and trained graduate students.'],
                   'prior_audit': ref(CENSUS, row['integrated_citation_key']), 'scope': 'Literature inspection only'})
    packages = []
    for key in ['v12_la_package_cladder', 'v12_la_package_causalds']:
        row = sources[key]; originals = []
        for item in row['local_sources']:
            path = ROOT/item['path']
            bound = ref(path, 'Pinned primary code, metadata or notice')
            assert bound['sha256'] == item['sha256']
            originals.append(dict(bound, source_identity=item['url']))
        packages.append({'id': key, 'source_identity': row['url'], 'commit': row['commit'],
                         'commit_date': row['commit_date'], 'originals': originals,
                         'inspected_anchors': row['anchors'], 'limitations': row['adverse_findings_and_limits'],
                         'license_notice': row['license_scope'], 'executed': False,
                         'integration_admitted': False})
    write(BASE/'primary-review.json', {'cutoff': '2026-10-07', 'papers': papers, 'packages': packages,
          'source_audit': ref(AUDIT, 'Preserved identities and inspected primary sources'),
          'scorer_correction': 'CausalDS retains both uncapped and capped normalized score means; inspect grader lines 3529-3546.',
          'new_searches_or_provider_calls': 0, 'technical_scope': 'Selected primary text and pinned source; not full-source or dependency review'})
    wanted = {'LA01-candidate-104', 'LA01-candidate-108', 'LA01-candidate-53', 'LA01-candidate-0', 'LA01-candidate-18'}
    pending = [x for x in json.loads(OMISSIONS.read_text())['items'] if x['id'] in wanted]
    assert {x['id'] for x in pending} == wanted
    assert not any(x.get('reconciles') in wanted for x in later)
    write(BASE/'candidate-reassessment.json', {'resolved': [{'id': 'LA01-candidate-107',
          'resolution': 'Original CausalEval PDF inspected in later census and reread here.',
          'audit': ref(CENSUS, 'exec13_census_causaleval')}], 'pending': pending,
          'omissions': ref(OMISSIONS, 'Preserved candidate discoveries; no claims taken from metadata'),
          'search': ref(SEARCH, 'Earlier bounded searches, ten ranked results and no saturation claim'),
          'acquisition_limit': 'ACL Anthology leads are outside the current fixed collector host list; no new fetch attempt or public-source unavailability claim.',
          'collector': ref(ROOT/'tools/public_sources.py', 'Fixed HTTPS host list and bounded reads')})
    protocol = json.loads(PROTOCOL.read_text())
    assert protocol['registration'] is None and protocol['final_evaluation_authorized_to_start'] is False
    write(BASE/'exact-oracle.json', calculate())
    write(BASE/'prospective-inputs.json', {'status': 'design_only_not_a_registration',
          'inherited_protocol': ref(PROTOCOL, 'LA06 prospective design; unchanged'),
          'later_inputs': ['Development pilot cost and reliability evidence',
                          'Fixed model/provider versions, settings and bounded tools',
                          'Independent hidden mechanisms, truth and adjudication',
                          'Qualified numerical and ordinary analyst baselines',
                          'Dated actual component prices and human timing',
                          'Decision loss, thresholds, sample size and stopping rule'],
          'proposal_blocker': False, 'reason': 'Proposal claims literature and design; live comparative performance is a later experiment.',
          'next_experiment': 'Use public development cases to measure feasibility and value of a subsequent hidden comparison before costly bank work.'})
    evidence = [ref(SYN, 'Connected evaluation, worked banking target, full cost, remedies and limits'),
                ref(BASE/'primary-review.json', 'Seven genuine PDFs and two pinned package source sets'),
                ref(BASE/'candidate-reassessment.json', 'Resolved and uninspected candidates with acquisition/search limits'),
                ref(BASE/'exact-oracle.json', 'Exact target, denominators, costs, sensitivities and planning bound'),
                ref(BASE/'prospective-inputs.json', 'Future prototype inputs; no invented registration or results'),
                ref(Path(__file__), 'Reproducible source binding and example arithmetic')]
    criteria = [
        {'index': 0, 'verdict': 'pass', 'finding': 'Seven primary evaluations and two pinned package source sets compared; favorable/adverse evidence, candidate coverage, remedies and open research explicit.'},
        {'index': 1, 'verdict': 'pass', 'finding': 'Bank offer target, clock and identification premises developed; exact randomized baseline, denominator failures, total-cost sensitivity and mechanism-level precision derived.'},
        {'index': 2, 'verdict': 'pass', 'finding': 'All published performance remains source-reported; own calculations are stipulated scenarios; no live model, bank truth, actual pricing or observed ROI claimed.'}]
    limits = ['Author synthesis; not independent scientific acceptance or exhaustive literature saturation.',
              'No upstream package execution, hidden live evaluation or bank validation.',
              'Main-reader integration and its exact release reviews remain separate work.']
    reviewer = {'name': 'Codex author/coordinator', 'kind': 'author'}
    write(BASE/'author-review.json', {'outcome': 'pass', 'scope': 'Evaluation/cost research synthesis and reproducible proposal scenarios',
          'criteria': criteria, 'evidence': evidence, 'reviewer': reviewer, 'limitations': limits,
          'resolved_review_findings': ['Corrected CausalEval omission mapping from candidate 103 to 107 before acceptance.',
                                     'Separated source interval denominator of five/seven from the 100-scene exam.',
                                     'Supplied the elementary bounded-mean derivation and distinguished paired from single-proportion precision.',
                                     'Kept principled refusals separate from failures and interval availability.']})
    graph, _, _ = control.combined(ROOT, core.read(ROOT, core.STATE))
    receipt = control.ledger.receipt_template(control.ledger.operation(graph, 'LL.TASK.evaluation_cost'))
    receipt.update(outcome='pass', execution='performed', scope='Author evaluation/cost literature and design synthesis',
                   reviewer=reviewer, limitations=limits, capabilities=[], outputs=[evidence[0]],
                   nonexecution_reason='', revisit_trigger='')
    for index, row in enumerate(criteria):
        receipt['criteria'][index].update(verdict=row['verdict'], finding=row['finding'], evidence=evidence)
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'review': 'pass', 'primary_papers': len(papers), 'pinned_packages': len(packages),
                      'local_model_or_package_execution': False, 'scenario_assisted_cost_USD': '18.50'}))


if __name__ == '__main__':
    main()
