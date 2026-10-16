#!/usr/bin/env python3
"""Bind official policy documentation, source-specific omissions and exact examples."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

import commercial_policy_examples_20261016 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT/'docs/program/execution/2026-10-16/s2/publication-v2/reader/source-audit.json'
OP = 'SW.CELL.policies_offpolicy.commercial'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Bounded eleven-family portfolio, not a systematic market census or complete cutoff-era feature inventory.',
    'Official documents were acquired after 2026-10-07; displayed version/update dates do not authenticate exact historical bytes.',
    'MATLAB, SAS reinforcement learning and HUGIN originals remain unavailable; IBM, Mplus and Bayesia policy-specific coverage remains unresolved.',
    'No commercial engine was executed; prices, entitlements and embedding/distribution rights are not inferred from public documentation.',
    'Exact examples are generated laws and stipulated dollar values, not bank data or ROI.',
    'Three local method refusals concern the common reference dispatcher, not every research module in this repository.',
    'General hidden-state identification, dependent evaluation and useful finite-sample precision remain research obligations.',
    'Rendered visual acceptance remains open under the exhausted inherited six-preview allowance.']


def read(path):
    return json.loads(path.read_text())


def excerpt(path, markers):
    lines = path.read_text().splitlines(); anchors = []
    for marker in markers:
        positions = [i for i, line in enumerate(lines) if marker in line]
        assert positions, (path, marker)
        i = positions[0]
        anchors.append({'anchor': f'Extracted primary text lines {i+1}-{min(i+3, len(lines))}',
                        'quote': '\n'.join(lines[i:i+3])})
    return anchors


def document(name, url, title, version, markers, claims):
    html = BASE/(name+'.html'); txt = BASE/(name+'.txt')
    raw = html.read_text(); anchors = excerpt(txt, markers)
    metadata = {k: re.findall(r'<meta name="'+re.escape(k)+r'" content="([^"]*)"', raw)
                for k in ['ms.date', 'updated_at', 'gitcommit', 'source_path']}
    record = {'source_identity': url, 'title': title, 'version_date': version, 'cutoff': '2026-10-07',
              'accessed_utc': datetime.fromtimestamp(html.stat().st_mtime, timezone.utc).isoformat(),
              'local_copy': ref(html, 'Original public official HTML bytes'),
              'text_copy': ref(txt, 'Inert extraction; original HTML authoritative'),
              'headers': ref(BASE/(name+'.headers'), 'Saved public GET response headers'),
              'inspected_anchors': anchors, 'supported_claims': claims, 'page_metadata': metadata,
              'limits': 'Later acquisition. No exact cutoff byte, vendor runtime, entitlement or statistical guarantee inferred.'}
    verify_bindings(record)
    return record


def main():
    assert not (BASE/'source-audit.json').exists()
    prior = read(PRIOR); verify_bindings(prior)
    old = {s['integrated_citation_key']: s for s in prior['sources']}
    assert len(old) == 660 and examples.calculate() == read(BASE/'exact-results.json')
    verify_bindings(read(BASE/'local-probe.json'))
    azure_version = 'Displayed 2024-01-19; archived official pages acquired 2026-10-16; page metadata retained, exact cutoff bytes unverified'
    azure = [
        document('azure_ope-elevated', 'https://learn.microsoft.com/en-us/previous-versions/azure/ai-services/personalizer/concepts-offline-evaluation',
                 'Personalizer: Offline evaluation', azure_version,
                 ['Starting 20 September 2023', 'recommended minimum is at least 50,000', 'Initialize a virtual instance',
                  'If they don\'t match', 'confidence bounds'],
                 ['Historical offline policy comparison and chronological replay account; practical event guidance and reported bounds.',
                  'Page states retirement on 2026-08-25 and migration recommendation; full estimator/uncertainty specification is not established.']),
        document('azure_how-elevated', 'https://learn.microsoft.com/en-us/previous-versions/azure/ai-services/personalizer/how-to-offline-evaluation',
                 'Personalizer: Analyze your learning loop with an offline evaluation', azure_version,
                 ['Optimization discovery option', 'estimated average reward, confidence intervals', 'Select Apply'],
                 ['Optimization discovery, uploaded policy comparison, downloads and apply workflow are documented, not executed.']),
        document('azure_overview-elevated', 'https://learn.microsoft.com/en-us/previous-versions/azure/ai-services/personalizer/what-is-personalizer',
                 'Personalizer overview', azure_version,
                 ['Rank API is called', 'Reward API is called', 'Log individual users', 'Apprentice mode'],
                 ['Rank/Reward event interface, 0-to-1 reward, delayed feedback and separate apprentice/online modes.',
                  'Overview says the service does not log individual user historical data; no general trajectory causal model inferred.'])]
    bayes = [
        document('genie_decision-elevated', 'https://support.bayesfusion.com/docs/GeNIe/da_decisionanalysis.html',
                 'GeNIe: Decision analysis', 'Inherited manual family 5.0.R2, built 2024-11-23; acquired mutable page 2026-10-16',
                 ['Decision analysis comes with'], ['Decision framing, preference/uncertainty elicitation and value-of-information tools.']),
        document('smile_influence', 'https://support.bayesfusion.com/docs/SMILE/influence-diagrams.html',
                 'SMILE: Influence diagrams', 'Inherited manual family 2.2.4.R1, built 2024-04-27; acquired mutable page 2026-10-16',
                 ['Decision nodes represent', 'Value nodes', 'Multi-attribute utility', 'indexing parents', 'for decision nodes'],
                 ['Decision states, utility tables, multi-attribute utilities and indexing-parent interpretation.',
                  'Output type controls whether stored matrices contain probabilities or expected utilities conditional on the supplied decision model.'])]
    aws = [document('aws_evaluation', 'https://docs.aws.amazon.com/personalize/latest/dg/working-with-training-metrics.html',
                    'Amazon Personalize: Evaluating a solution version with metrics',
                    'Mutable latest guide; acquired 2026-10-16; exact edition and cutoff availability unverified',
                    ['Avoid comparing metrics', 'splits the input interactions', 'GetSolutionMetrics operation',
                     'average_rewards_at_k', 'rewards_per_user ='],
                    ['Documented split-dependent held-out recommendation metrics, metric retrieval and reward normalization.',
                     'These inspected metric definitions are not a sequential causal-policy value estimator.'])]
    inherited_keys = ['jiang2016', 'exec13_ch_stata', 'exec13_ch_jmp_uplift', 'exec13_smile_license',
                      'exec13_genie_readme', 'exec13_smile_intro', 'exec13_ct_mplus81', 'exec14_survival_sas',
                      'exec13_ci_stata_causal_intro', 'exec15_d3rlpy_contract', 'sw_scope_rl']
    assert all(k in old for k in inherited_keys), [k for k in inherited_keys if k not in old]
    inspected = BASE/'inspected'; inspected.mkdir(exist_ok=False)
    scholarly = []
    for n in [2, 3]:
        out = inspected/f'jiang2016-{n}.txt'
        subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-layout', str(ROOT/old['jiang2016']['local_path']), str(out)], check=True, timeout=20)
        scholarly.append(ref(out, f'Genuine Jiang/Li primary PDF physical page {n}; finite-horizon target, importance ratios and sample separation'))
    primary = {'status': 'pass_for_bounded_comparison', 'reviewer': REVIEWER, 'cutoff': '2026-10-07',
               'new_official_originals': azure+bayes+aws, 'inherited_source_records': [old[k] for k in inherited_keys],
               'new_primary_rereads': scholarly,
               'stata_reread': {'source': ref(ROOT/'docs/program/execution/2026-10-13/commercial-heterogeneity/stata_post.txt',
                                            'Lines 105-107, 145-148 and 780-801'),
                                 'finding': 'Prespecified probability-valued static policies; policy value and policy contrast; tassigneval alias.'},
               'local_source_rereads': [ref(ROOT/'src/causalbank/history_inference.py', 'HistoryQuery and evaluate_history, lines 1-95; separate research module'),
                                        ref(ROOT/'src/causalbank/controlled.py', 'value and contrast; supplied controlled-model research')],
               'evidence': [ref(PRIOR, 'Preserved audited corpus'), ref(BASE/'acquisition-manifest.json', 'Ten initial official routes'),
                            ref(BASE/'fallback-manifest.json', 'Four bounded alternate official routes'),
                            ref(BASE/'acquisition-observations.json', 'DNS failures and observed HTTP responses'),
                            ref(BASE/'fallback-observations.json', 'Recovered alternate-route outcomes checked against saved HTTP headers'),
                            ref(Path(__file__), 'Bounded primary-source preparation')], 'limits': LIMITS}
    write(BASE/'primary-review.json', primary)
    candidates = [
        ('Stata', ['cate', 'estat policyeval', 'estat tassigneval'], ['exec13_ch_stata'],
         'Static probability-valued prespecified treatment-assignment value and contrasts.',
         'Licensed static-policy comparator; retain underlying assumptions, units and policy/sample separation.', 'Sequential history and selected-policy inference are not established by this static command.'),
        ('JMP', ['Uplift', 'JMP Pro'], ['exec13_ch_jmp_uplift'],
         'Partition targeting using treatment interactions; older-guide validation details separately scoped.',
         'Targeting comparator; compare net incremental value and capacity, not response ranking alone.', 'Edition-specific policy inference and sequential capabilities remain unverified.'),
        ('Microsoft', ['Azure Personalizer', 'Personalizer', 'microsoft/learning-loop'], ['exec16_cp_azure'],
         'Historical Rank/Reward, offline replay, baseline/custom/optimized policies and documented bounds.',
         'Historical workflow reference; no new hosted dependency after documented 2026-08-25 retirement.', 'Open-source migration lead needs a separate pinned review; full estimator and bounds implementation unresolved.'),
        ('BayesFusion', ['GeNIe', 'SMILE'], ['exec16_cp_bayesfusion', 'exec13_smile_license'],
         'Supplied influence diagrams with decision states, indexed expected utilities and preferences.',
         'Conditional licensed model-based comparator; preserve information sets and utility units; do not port vendor code.', 'Model optimization does not identify mechanisms from arbitrary logged histories; entitlement and price unresolved.'),
        ('Amazon', ['Amazon Personalize', 'Next-Best-Action', 'PERSONALIZED_ACTIONS'], ['exec16_cp_aws'],
         'Split-dependent recommendation metrics and metric API/CLI; reward normalization.',
         'Predictive workflow comparator on its documented metrics; separate causal-value evaluation.', 'Exact cutoff edition, intervention interpretation, policy guarantees and runtime remain unresolved.'),
        ('MathWorks', ['MATLAB', 'Reinforcement Learning Toolbox', 'trainFromData'], [],
         'No acquired technical original in this bounded review.',
         'Acquire version-specific official offline-training and evaluation manual through an accessible public or owner-provided authorized route.', 'Three selected official routes returned HTTP403; no absent-feature conclusion.'),
        ('SAS', ['SAS Viya', 'reinforcementLearn', 'SAS/STAT'], ['exec14_survival_sas'],
         'Inherited survival-model documentation is a distinct comparator; policy capability unresolved.',
         'Acquire correct versioned reinforcement-learning action-set manual; retain module and edition distinctions.', 'Two guessed official paths returned HTTP404; not evidence of feature absence.'),
        ('HUGIN', ['HUGIN Decision Engine', 'HUGIN Developer'], [],
         'No acquired technical original in this bounded review.',
         'Acquire version-specific influence-diagram algorithm and API documentation before a model-based comparison.', 'Two selected official routes returned HTTP455; capability and rights remain unknown.'),
        ('IBM', ['SPSS Statistics', 'SPSS Modeler'], [],
         'Inherited regression/forecasting coverage does not resolve policy evaluation.',
         'Inspect separate versioned policy/decision-optimization documentation; do not transfer a regression feature to sequential OPE.', 'No policy-specific original inspected in this bounded pass.'),
        ('Mplus', ['DSEM', 'RDSEM'], ['exec13_ct_mplus81'],
         'Inherited supplied dynamic-model syntax and fitting assumptions.',
         'Retain model-based alternative; acquire policy-specific target and evaluation evidence before any wider claim.', 'Dynamic model fitting is not by itself sequential policy identification.'),
        ('Bayesia', ['BayesiaLab'], [],
         'Inherited causal-model material does not settle policy evaluation or optimization scope.',
         'Acquire exact-edition decision/utility and policy export/evaluation primary text.', 'No policy-specific original inspected in this bounded pass.')]
    matrix = [{'family': family, 'aliases': aliases, 'evidence_keys': keys, 'documented_scope': scope,
               'proposed_choice': choice, 'remaining_gap': gap, 'price': 'unavailable', 'entitlement': 'not established',
               'current_common_service': 'No qualified policy method; three actual proposed identifiers returned unsupported.',
               'proposed_capability': 'Typed static, sequential, adapting-learner or supplied-model request with explicit policy identity and evidence scope.'}
              for family, aliases, keys, scope, choice, gap in candidates]
    raw = ROOT/'docs/literature/raw/v12_sw_cell_policies_offpolicy_commercial.json'
    leads = read(raw)['results']
    search = {'cutoff': '2026-10-07 Asia/Shanghai', 'searched_on': '2026-10-16',
              'inherited_query': ref(ROOT/'docs/literature/raw/v12_sw_cell_policies_offpolicy_commercial.receipt.json', 'Original overly combined scholarly query'),
              'inherited_results': ref(raw, 'Six nonsoftware scholarly hits retained'),
              'lead_dispositions': [{'id': x['id'], 'title': x.get('title'), 'disposition': 'Not an identified software implementation; no capability or absence inference'} for x in leads],
              'strategy': 'Named official technical routes and retained authenticated manuals; no general web-search capability available in this turn.',
              'initial_route_count': 10, 'fallback_route_count': 4, 'same_url_dns_retries': 4,
              'technical_original_count': 6, 'families': 11, 'exhaustive': False,
              'stopping_rule': 'Ten initial official routes and at most four specific alternates; no further speculative URL retries.',
              'limits': ['No exhaustive commercial universe or long-tail search.', 'Broader decision platforms, simulators, optimization and historical editions remain unscreened.']}
    write(BASE/'search-ledger.json', search)
    omissions = {'coverage_outcome': 'inconclusive', 'whole_census_closed': False,
                 'candidates': [r for r in matrix if r['family'] in ['MathWorks','SAS','HUGIN','IBM','Mplus','Bayesia']],
                 'unresolved_across_candidates': ['Exact-cutoff original identity', 'Installed entitlement and execution', 'Real prices and full workflow cost',
                                                   'General dependent/hidden-state evaluation guarantees', 'Open-source learning-loop successor review'],
                 'revisit_trigger': 'Accessible exact-edition originals, resolved algorithm/rights identity and a consequential matched prototype request.',
                 'alternatives': ['Existing source-audited open-source policy references', 'Exact generated mechanisms and public-data clocks',
                                  'Documented static Stata/JMP comparators', 'Licensed supplied-model decision comparator when available'],
                 'evidence': [ref(BASE/'search-ledger.json', 'Bounded search and preserved irrelevant leads')], 'limits': LIMITS}
    write(BASE/'omissions-register.json', omissions)
    design = {'status': 'proposed_not_executed', 'vendor_matrix': matrix,
              'profiles': ['Static rule with net outcome and capacity', 'Fixed observable-history policy under known logging',
                           'Separately selected versus independently evaluated policy', 'Supplied influence diagram with declared information/utility',
                           'Predictive recommendation baseline on distinct targets'],
              'public_generated_plan': ['Keep complete customer trajectories and availability clocks.',
                                        'Compare identical eligible mechanisms; report scope violations and every refusal.',
                                        'Freeze policy identity, source/environment, independent final sample, bounds and stopping before final evaluation.',
                                        'Measure preparation, rights, conversion, diagnostics, review and maintenance as well as runtime.'],
              'known_routes': ['Version-specific manual acquisition and source matching', 'Explicit policy and reward contract',
                               'Public/generated matched prototype with source-audited open alternatives', 'License-specific trial only for an admitted comparator'],
              'unresolved_science': ['General hidden-history identification', 'Useful dependent and selected-policy uncertainty',
                                     'Target-bank assignment and utility truth; later conditional inputs'],
              'evidence': [ref(BASE/'primary-review.json', 'Inspected official methods'), ref(BASE/'local-probe.json', 'Actual local capability boundary'),
                           ref(BASE/'omissions-register.json', 'Bounded source/census limits')], 'limits': LIMITS}
    write(BASE/'comparison-design.json', design)
    sources = []
    for key, title, author, year, records, claims in [
        ('azure', 'Archived Azure Personalizer policy evaluation and retirement documentation', 'Microsoft', 2026, azure,
         ['Rank/Reward workflow, replay/optimization comparison, practical data guidance and reported bounds.', 'Official retirement date 2026-08-25 precedes cutoff; migration lead is separately unreviewed.']),
        ('bayesfusion', 'GeNIe and SMILE supplied-model decision analysis', 'BayesFusion, LLC', 2024, bayes,
         ['Decision/utility/MAU types, indexing parents and expected-utility interpretation.', 'Model-based comparison is distinct from logged-history identification.']),
        ('aws', 'Amazon Personalize recommendation evaluation metrics', 'Amazon Web Services', 2026, aws,
         ['Held-out splits, precision/recall/NDCG and normalized reward metrics; CLI/SDK retrieval.', 'No causal policy-value guarantee follows from these inspected definitions.'])]:
        sources.append({'integrated_citation_key': 'exec16_cp_'+key, 'title': title, 'author': author, 'year': year,
                        'kind': 'official_documentation', 'source_identity': '; '.join(r['source_identity'] for r in records),
                        'version_date': '; '.join(dict.fromkeys(r['version_date'] for r in records)),
                        'local_copy': records[0]['local_copy'], 'records': records,
                        'inspected_anchors': [a for r in records for a in r['inspected_anchors']],
                        'supported_claims': claims, 'limits': LIMITS})
    for key, title, kind, path, claims, records in [
        ('exact', 'Exact commercial-policy comparison and servicing references', 'project_derivation', BASE/'exact-results.json',
         ['Full-history value -10 versus wrong final-action values 42.5/84.5; population weight moment 20.',
          'Matched-only mean 19 versus population 55; finite selection optimism; capacity net 1.5 versus -0.3 USD.'],
         [ref(ROOT/'tools/commercial_policy_examples_20261016.py', 'Exact Fraction enumeration and independent structural calculations')]),
        ('matrix', 'Commercial policy portfolio, capability gaps and proposed prototype', 'project_design', BASE/'comparison-design.json',
         ['Eleven-family choices separate documented features, unknowns, local reference and proposed capability.',
          'Bounded inconclusive coverage; rights, source acquisition and scientific remedies retained.'],
         [ref(BASE/'primary-review.json', 'Original-source and inherited review'), ref(BASE/'search-ledger.json', 'Bounded search'),
          ref(BASE/'omissions-register.json', 'Remaining candidates and exact revisit triggers')]),
        ('runtime', 'Actual common-service policy method refusals and separate research modules', 'project_implementation', BASE/'local-probe.json',
         ['Three schema-valid proposed policy identifiers return unsupported with null result in the current common service.',
          'Separate research modules exist; these refusals do not classify all repository capabilities.'],
         [ref(ROOT/'src/causalbank/history_inference.py', 'Separate observed-history research evaluator'),
          ref(ROOT/'src/causalbank/controlled.py', 'Separate supplied controlled-model value'),
          ref(ROOT/'tools/probe_commercial_policy_20261016.py', 'Bounded actual local probe')])]:
        sources.append({'integrated_citation_key': 'exec16_cp_'+key, 'title': title, 'author': 'Causal banking proposal', 'year': 2026,
                        'kind': kind, 'source_identity': str(path.relative_to(ROOT)), 'version_date': '2026-10-16',
                        'local_copy': ref(path, title), 'inspected_anchors': claims, 'supported_claims': claims, 'records': records, 'limits': LIMITS})
    write(BASE/'source-audit.json', {'sources': sources, 'prior': ref(PRIOR, '660 preserved source records'), 'cutoff': '2026-10-07'})
    text = (BASE/'development.template').read_text().replace('§', chr(92))
    assert ',+' not in text
    cited = {key.strip() for group in re.findall(r'\\citep\{([^}]+)\}', text) for key in group.split(',')}
    assert cited <= set(old) | {s['integrated_citation_key'] for s in sources}
    assert not (BASE/'development.tex').exists(); (BASE/'development.tex').write_text(text)
    write(BASE/'author-review.json', {'status': 'pass_for_integration', 'reviewer': REVIEWER,
              'coverage_outcome': 'inconclusive', 'criteria_verdicts': ['inconclusive','pass','pass'],
              'findings': ['Eleven named families and six irrelevant inherited hits are accounted for; search and source gaps prevent census closure.',
                           'Six official originals and inherited audited manuals/paper support scoped technical comparisons.',
                           'Four exact generated reference families reproduce; three actual local method refusals are distinct from vendor execution.',
                           'Known acquisition/prototype routes and unresolved science are explicit; no unsupported vendor absence claim.'],
              'evidence': [ref(BASE/p, p) for p in ['primary-review.json','source-audit.json','search-ledger.json','omissions-register.json',
                                                  'comparison-design.json','exact-results.json','local-probe.json','development.tex','plan.md']],
              'limits': LIMITS, 'visual_acceptance': False, 'whole_census_closed': False})
    print(json.dumps({'new_source_records': len(sources), 'official_originals': 6, 'families': len(matrix),
                      'coverage_outcome': 'inconclusive', 'prepared': str((BASE/'development.tex').relative_to(ROOT))}))


if __name__ == '__main__':
    main()
