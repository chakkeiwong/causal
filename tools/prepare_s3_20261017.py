#!/usr/bin/env python3
"""Audit the recovered S3 draft, separately recompute examples and bind a design."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import re

import s3_examples_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT / 'docs/program/execution/2026-10-17/integration-continuity/publication/reader/source-audit.json'
CHAPTER = ROOT / 'docs/program/comprehensive-v14/work/TEXT.DRAFT.S3/chapter.tex'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Author/coordinator review, not independent acceptance.',
    'Six exact authored law families and stipulated USD100/USD12 rewards; no bank data, upstream runtime benchmark or ROI observation.',
    'Mathematical examples do not qualify every graph class, conditional algorithm, IV estimator or numerical implementation.',
    'Public/generated prototype is proposed, not executed; pinned environments, rights and statistical protocols remain prerequisites to new runtime claims.',
    'Whole software census, bank assignment/cross-world truth, feasible actions, accepted loss and actual costs remain open.',
    'Rendered visual acceptance remains false; inherited six-image allowance is exhausted.'
]


def independent():
    """Separate algebra/cell summation, without invoking the reference enumerator."""
    x = json.loads((BASE / 'exact-results.json').read_text())
    a = x['adjustment']
    raw = [F(4, 5)*F(1, 10)+F(1, 5)*F(3, 5),
           F(1, 5)*F(1, 5)+F(4, 5)*F(7, 10)]
    adjusted = [(F(1, 10)+F(3, 5))/2, (F(1, 5)+F(7, 10))/2]
    assert list(map(str, raw)) == a['raw_means']
    assert list(map(str, adjusted)) == a['adjusted_means']
    assert 100*(raw[1]-raw[0])-12 == 28
    assert 100*(adjusted[1]-adjusted[0])-12 == -2
    assert 2+3*1 == a['linear_mediation']['total_effect']
    c = x['conditional_identification']
    # Direct outcome-mechanism averaging, separate from enumerated exogenous rows.
    assert c[0]['laws']['observed'] == c[1]['laws']['observed']
    assert len(c[0]['laws']['observed']) == 8
    assert min(map(F, c[0]['laws']['observed'].values())) > 0
    means = [[F(1, 2), F(1, 2)],
             [F(3, 4)*F(1, 5)+F(1, 4)*F(4, 5),
              F(1, 4)*F(1, 5)+F(3, 4)*F(4, 5)]]
    for row, expected in zip(c, means):
        assert row['Y_means_do_A'] == list(map(str, expected))
        assert row['conditional_Y_given_Z'] == [['1/5', '4/5']]*2
    # Frechet cell constraints and randomized-arm marginals.
    for row in x['coupling']['examples']:
        law = {k: F(v) for k, v in row['response_type_law'].items()}
        assert sum(law.values()) == 1 and min(law.values()) >= 0
        assert law['10']+law['11'] == F(2, 5)
        assert law['01']+law['11'] == F(3, 5)
        assert law['01']-law['10'] == F(1, 5)
        assert law['01']/F(3, 5) == F(row['attribution_given_treated_success'])
    iv = x['iv']
    d0, d1 = F(3, 10), F(3, 10)+F(2, 5)
    y0 = F(3, 10)*F(1, 5)+F(2, 5)*F(3, 10)+F(3, 10)*F(2, 5)
    y1 = F(3, 10)*F(1, 5)+F(2, 5)*F(1, 2)+F(3, 10)*F(2, 5)
    assert (y1-y0)/(d1-d0) == F(1, 5)
    assert 100*(y1-y0)-12*(d1-d0) == F(16, 5)
    for row in iv['completions']:
        n, b = F(row['missing_never_Y1']), F(row['missing_always_Y0'])
        assert F(row['population_ATE']) == F(7, 50)+F(3, 10)*(n-b)
        assert row['observable_ZDY'] == iv['completions'][0]['observable_ZDY']
        # Recover the fixed IV observable table by mixing principal-stratum cells.
        for z, d, y in product([0, 1], repeat=3):
            mass = F(0)
            for weight, receipt, success in [
                (F(3, 10), 0, F(1, 5)),
                (F(2, 5), z, F(3, 10) if z == 0 else F(1, 2)),
                (F(3, 10), 1, F(2, 5))]:
                if receipt == d:
                    mass += weight*(success if y else 1-success)/2
            assert mass == F(row['observable_ZDY'][f'{z}{d}{y}'])
    assert iv['ATE_bounds'] == ['-4/25', '11/25']
    bound = x['consistency_bounds']
    cells = {k: F(v) for k, v in bound['observable_AY'].items()}
    ey1 = [cells['11'], cells['11']+cells['00']+cells['01']]
    ey0 = [cells['01'], cells['01']+cells['10']+cells['11']]
    theta = [ey1[0]-ey0[1], ey1[1]-ey0[0]]
    assert list(map(str, theta)) == bound['ATE_bounds'] == ['-3/10', '7/10']
    assert min(F(r['EY0']) for r in bound['completions']) == ey0[0]
    assert max(F(r['EY1']) for r in bound['completions']) == ey1[1]
    for row in bound['completions']:
        assert F(row['ATE']) == F(row['EY1'])-F(row['EY0'])
    eps = F(1, 10000000)
    for name, denominator in [('rare', F(1, 1000000)), ('common', F(1, 10))]:
        nominal = F(3, 5)*denominator
        q = [(nominal-eps)/(denominator+eps), (nominal+eps)/(denominator-eps)]
        assert list(map(str, q)) == x['numerical'][name]['ratio_interval']
        assert list(map(str, [100*(v-F(2, 5))-12 for v in q])) == x['numerical'][name]['incremental_net_USD']
    assert x['numerical']['rare']['ratio_interval'] == ['5/11', '7/9']
    return {'status': 'pass', 'method': 'Separate author algebra, marginal constraints and direct principal-stratum cell mixing; not an independent reviewer.',
            'families_checked': ['adjustment and mediation', 'conditional versus joint',
                                 'cross-world coupling', 'IV and population bounds',
                                 'consistency extreme completions', 'numerical ratio envelopes'],
            'evidence': [ref(BASE / 'exact-results.json', 'Six saved exact authored laws'),
                         ref(Path(__file__), 'Separate algebraic recomputation')], 'limitations': LIMITS}


def main():
    assert examples.calculate() == json.loads((BASE / 'exact-results.json').read_text())
    write(BASE / 'mathematics-review.json', independent())
    lower, upper = F(-42), F(58)
    r = upper/(upper-lower)
    assert r == F(29, 50) and -lower*r == upper*(1-r) == F(609, 25)
    decision = {'status': 'project_derivation_not_empirical', 'net_interval_USD': [str(lower), str(upper)],
        'feasible_actions': 'No receipt or universal receipt; optional independent randomized fraction with no interference and proportional costs.',
        'maximin_action': 'no_receipt', 'deterministic_minimax_regret_action': 'receipt',
        'deterministic_regrets_USD': {'receipt': str(-lower), 'no_receipt': str(upper)},
        'randomized_minimax_fraction': str(r), 'randomized_regret_USD': str(-lower*r),
        'argument': 'For receipt fraction r the endpoint regrets are 42r and 58(1-r); the decreasing and increasing lines cross at the unique minimax solution.',
        'evidence': [ref(BASE / 'exact-results.json', 'Consistency-only net interval'),
                     ref(Path(__file__), 'Separate rational decision derivation')], 'limitations': LIMITS}
    write(BASE / 'decision-reference.json', decision)
    prior = json.loads(PRIOR.read_text()); verify_bindings(prior)
    index = {s['integrated_citation_key']: s for s in prior['sources']}
    text = CHAPTER.read_text()
    cited = {k.strip() for g in re.findall(r'\\citep\{([^}]+)\}', text) for k in g.split(',')}
    additions = {'exec17_s3_exact', 'exec17_s3_decision', 'exec17_s3_design'}
    assert cited-additions <= index.keys() and additions <= cited
    paper_specs = [
        ('id2006', 210, 367, ['ID and hedge scope; Theorems6-9 establish maximal conditional reduction, IDC soundness/completeness and do-calculus completeness.']),
        ('perkovic2018', 450, 520, ['Definition4 and Theorems5/7 characterize adjustment, not all identification; endpoint classes matter.']),
        ('perkovic2018', 665, 705, ['MAG/PAG treatment excludes selection bias; adjustment completeness is not universal identification completeness.']),
        ('swig2013', 1, 145, ['Single-world counterfactual factorization and distinction between FFRCISTG and NPSEM-IE.']),
        ('angrist1996', 242, 375, ['Independence, exclusion, relevance and monotonicity give complier LATE; specific complier membership and population effects generally unavailable.']),
        ('pearl2009', 1210, 1300, ['Structural counterfactuals retain exogenous state under the changed intervention; structural meaning alone is not observational identification.'])
    ]
    papers = []
    (BASE / 'inspected').mkdir(exist_ok=False)
    for key, first, last, claims in paper_specs:
        s = index[key]; original = ROOT / s['local_path']
        extracted = ROOT / 'docs/literature/text' / (key+'.txt')
        lines = extracted.read_text().splitlines()
        excerpt = BASE / 'inspected' / f'{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        papers.append({'citation_key': key, 'original': {'path': s['local_path'], 'sha256': s['sha256'],
            'anchor': 'Genuine primary PDF'}, 'version_date': s['version_status'],
            'text_copy': ref(extracted, f'Lines {first}-{last}'), 'inspected_excerpt': ref(excerpt, 'Saved inspected technical text'),
            'supported_claims': claims})
    software = []
    for name, first, last, claims in [
        ('v12_gap3_y0_technical.txt', 35, 90, 'Explicit ID/IDC dispatch, Unidentifiable-only handling and strict mode.'),
        ('v12_gap4_y0_utils.txt', 154, 178, 'Query.expression conditional/unconditional branch; separate fields retained.'),
        ('exec13_dowhy_model.txt', 200, 273, 'IDIdentifier versus AutoIdentifier and examined local option propagation.'),
        ('exec13_other_file_dagitty_3.txt', 386, 420, 'Adjustment graph types and target checks.'),
        ('exec13_other_file_dagitty_3.txt', 1594, 1640, 'Full MAG/PAG validation TODO.'),
        ('exec14_other_latent_dagitty_0.txt', 1418, 1446, 'PAG-to-PDAG projection loses endpoint marks.')]:
        p = ROOT / 'docs/literature/raw' / name
        software.append({'local_copy': ref(p, f'Lines {first}-{last}'), 'supported_claims': [claims],
                         'excerpt': '\n'.join(p.read_text().splitlines()[first-1:last])})
    primary = {'status': 'pass_for_synthesis', 'reviewer': REVIEWER, 'cutoff': '2026-10-07',
        'paper_rereads': papers, 'software_rereads': software,
        'inherited_source_records': [index[k] for k in sorted(cited-additions)],
        'isolated_node_trace': ref(ROOT / 'docs/program/execution/2026-10-13/identification-review/isolated-conditions.tex',
                                   'Inherited static source trace, not installed-runtime execution'),
        'scope': 'Five genuine scholarly PDFs, six saved technical excerpts, six software excerpts and retained source-specific audits.',
        'evidence': [ref(PRIOR, '699 preserved records'), ref(Path(__file__), 'Primary-claim preparation')],
        'limitations': LIMITS}
    write(BASE / 'primary-review.json', primary)
    profiles = [
        ('adjustment', ['DAGitty graph-adjustment route', 'DoWhy explicitly selected identification route'],
         'Supported graph class, baseline information and positivity', 'Population-standardized means and total/direct target distinction'),
        ('conditional identification', ['Pinned y0 ID/IDC routes', 'A joint-first fallback labeled as a partial route'],
         'Semi-Markovian graph, explicit query fields, isolated nodes and positive conditioning',
         'Conditional point answer can exist while joint is nonidentified; preserve formula, hedge or exact failure origin'),
        ('counterfactual interpretation', ['Explicit supplied structural-model simulator'],
         'Recorded extra response-type coupling or exogenous mechanisms',
         'Same experimental marginals and different individual attribution; no automatic observational uniqueness'),
        ('IV and effect bounds', ['Explicit binary monotone-IV reference', 'Consistency-only completion reference'],
         'Declare encouragement, receipt, assignment law, exclusion, monotonicity and feasible action',
         'Same observable IV law with distinct population ATE; LATE, encouragement and universal receipt values retained'),
        ('numerical realization', ['Rational reference', 'Candidate numeric evaluator with certified error handling'],
         'Positive denominator, specified absolute errors and exact comparison risk',
         'Scientific identification, sampling uncertainty and numerical unavailability are separate outcomes')
    ]
    design = {'status': 'proposed_not_executed', 'cutoff': '2026-10-07',
        'profiles': [{'topic': t, 'candidates': c, 'admission': a, 'expected_semantics': o} for t,c,a,o in profiles],
        'reference_evidence': [ref(BASE / 'exact-results.json', 'Six exact law families'),
                               ref(BASE / 'decision-reference.json', 'Alternative decision criteria')],
        'sequence': ['Freeze candidate revision, rights decision, environment and shared scientific domain.',
                     'Run supported exact cases before noisy finite-sample comparisons; preserve unsupported cases in accounting.',
                     'Check query construction, graph surgery, expression normalization, option propagation and typed failures.',
                     'For new statistical claims, register sampling laws, target, denominator rules, intervals, seeds, failures and stopping rule before fresh draws.',
                     'Compare error in expected monetary decisions, diagnosis burden, maintenance and actual observed costs.'],
        'outcomes': ['point_functional', 'identified_set', 'valid_nonidentification_witness',
                     'unsupported_route', 'invalid_input_or_support', 'numerical_unavailability', 'execution_failure'],
        'public_data_role': 'Permitted public covariates can inform realistic generated mechanisms; they do not reveal missing potential outcomes or bank assignment truth.',
        'known_routes': ['Complete scoped originals review without blocking admitted profiles.',
                         'Repair or constrain demonstrated source paths before any adapter is enabled.',
                         'Use additional feasible interventions or justified restrictions for questions outside observed identification.'],
        'unknown_or_external': ['Bank causal sufficiency, valid instruments and cross-world restrictions.',
                                'Feasible interventions, accepted harm/loss/precision and actual operating costs.',
                                'No promised universal positive identification or inference theorem.'],
        'primary_review': ref(BASE / 'primary-review.json', 'Inherited exact versions and inspected claims'),
        'bank_qualified': False, 'whole_census_closed': False, 'limitations': LIMITS}
    write(BASE / 'prototype-design.json', design)
    rows = []
    for key, title, kind, path, claims, records in [
        ('exact', 'Exact identification, counterfactual coupling, IV, effect-bound and numerical references', 'project_derivation', BASE/'exact-results.json',
         ['Six exact authored laws with explicit information classes and stipulated USD100 success/USD12 receipt values.',
          'Conditional-versus-joint counterexample, randomized marginals with different attribution, identical IV observables with sharp population bounds.',
          'Consistency extremes and certified deterministic numerical envelopes.'],
         [ref(ROOT/'tools/s3_examples_20261017.py', 'Exact rational exogenous-law enumeration'),
          ref(BASE/'mathematics-review.json', 'Separate author algebra and cell-summation review')]),
        ('decision', 'Maximin and minimax-regret decisions for a consistency-only effect set', 'project_derivation', BASE/'decision-reference.json',
         ['Net interval[-42,58]; maximin no receipt; deterministic minimax regret receipt.',
          'Optional randomized fraction29/50 equalizes regret609/25 under the stated admissible-action assumptions.'],
         [ref(Path(__file__), 'Separate exact decision algebra')]),
        ('design', 'Proposed public and generated identification prototype comparison', 'project_design', BASE/'prototype-design.json',
         ['Scientific route, graph/query semantics, typed failures, exact examples and later statistical qualification remain distinct.',
          'Concrete public/generated comparison, rights/environment prerequisites and external scientific/decision inputs.'],
         [ref(BASE/'primary-review.json', 'Primary evidence and retained limitations'), ref(BASE/'plan.md', 'Reviewed synthesis plan')])]:
        rows.append({'integrated_citation_key': 'exec17_s3_'+key, 'title': title, 'author': 'Causal banking proposal',
            'kind': kind, 'year': 2026, 'source_identity': 'Project-authored derivations or proposed comparison',
            'version_date': '2026-10-17', 'local_copy': ref(path, title),
            'inspected_anchors': claims, 'supported_claims': claims, 'records': records, 'limitations': LIMITS})
    write(BASE/'source-audit.json', {'sources': rows, 'prior': ref(PRIOR, '699 retained source records'), 'cutoff': '2026-10-07'})
    write(BASE/'recovery-work-record.json', {
        'observed': ['Crash recovery found the S3 chapter, six-family exact-results and original reference script intact.',
                     'Unified queue and preserved-history check pass; TEXT.DRAFT.S3 remains active.',
                     'The preceding large apply_patch request failed at JavaScript template evaluation because of literal backticks; no file mutation occurred. The corrected bounded request produced the saved chapter.'],
        'repair': 'Use literal-safe patches, short commands, saved evidence and bounded text output.',
        'next_action': 'Compile a preserving successor; inspect source/text/math and measure exclusive S3 credit before recording outcomes.',
        'evidence': [ref(CHAPTER, 'Recovered chapter'), ref(BASE/'mathematics-review.json', 'Recovered calculations verified'),
                     ref(BASE/'plan.md', 'Reviewed continuation')], 'visual_acceptance': False})
    write(BASE/'draft-author-review.json', {'status': 'pass_for_draft_integration', 'reviewer': REVIEWER,
        'criteria_verdicts': ['pass', 'pass'],
        'findings': ['Connected law-relative identification, adjustment, ID/IDC, counterfactual coupling, IV, effect sets and numerical decisions.',
                     'Five primary scholarly originals and retained pinned software support inherited claims; six authored laws and separate decision algebra reproduce.',
                     'Source traces remain static findings, prototype remains a proposal and process records remain outside the manuscript.'],
        'evidence': [ref(p, p.name) for p in [CHAPTER, BASE/'primary-review.json', BASE/'exact-results.json',
                    BASE/'mathematics-review.json', BASE/'decision-reference.json', BASE/'prototype-design.json',
                    BASE/'source-audit.json', BASE/'plan.md', BASE/'recovery-work-record.json']],
        'depth_status': 'Pending compiled nonduplicate page assessment; no physical-length pass inferred.',
        'limitations': LIMITS, 'visual_acceptance': False, 'whole_census_closed': False})
    print(json.dumps({'draft_prepared': str(CHAPTER.relative_to(ROOT)), 'new_citations': 3,
                      'inherited_citation_keys': len(cited-additions), 'exact_and_separate_algebra': 'pass'}))


if __name__ == '__main__':
    main()
