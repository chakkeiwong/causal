#!/usr/bin/env python3
"""Bind official panel-DID text, exact authored references and scoped omissions."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import run_program_reviews_v2 as extension

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-18/commercial-panels'
OP = 'SW.CELL.panels_did.commercial'
OUTPUT = ROOT / ('docs/program/comprehensive-v14/work/' + OP + '/coverage-review.json')
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
LIMITS = [
    'Five inspected official originals cover selected Stata and introductory EViews claims; no complete commercial market or cutoff-era inventory.',
    'Acquired 2026-10-18. PDF creation dates and displayed page dates are metadata, not authentication of exact 2026-10-07 bytes or every StataNow option.',
    'EViews introductory text names TWFE and diagnostic references; their complete algorithms, implementation and inference are not established by that introductory page.',
    'SAS, IBM, MATLAB and commercial open-source frontends remain source-specific omissions; general panel regression is not automatically a causal DID estimator.',
    'No licensed vendor engine, upstream panel package or new adapter was executed. Prices, entitlements, embedding/distribution rights and current support remain unresolved.',
    'Exact dollar examples are authored deterministic laws, not bank observations, prospective performance trials, calibrated uncertainty or measured ROI.',
    'Common dispatcher observations concern its declared operation surface, not every research module in this repository.',
    'These additional findings are execution evidence pending a preserving manuscript successor; the current 1068-page reader is unchanged.',
    'Author review; rendered visual, independent and final proposal acceptance remain open.',
]


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    assert not path.exists(), str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def rational(value):
    return {'fraction': str(value), 'decimal': float(value)}


def exact_reference():
    units = ['E1', 'E2', 'L1', 'L2', 'N']
    treatment, outcomes, effects = {}, {}, {}
    for i, unit in enumerate(units):
        for time in range(3):
            d = int((unit[0] == 'E' and time >= 1) or (unit[0] == 'L' and time >= 2))
            effect = F(100 if unit[0] == 'E' and time == 2 else d)
            treatment[unit, time] = F(d)
            effects[unit, time] = effect
            outcomes[unit, time] = F(10*i + 2*time) + effect
    grand = sum(treatment.values()) / len(treatment)
    residual = {(unit, time): treatment[unit, time]
                - sum(treatment[unit, s] for s in range(3))/3
                - sum(treatment[v, time] for v in units)/5 + grand
                for unit, time in treatment}
    denominator = sum(v*v for v in residual.values())
    beta = sum(residual[k]*outcomes[k] for k in residual)/denominator
    weights = {group+str(time): sum(residual[unit, time]*treatment[unit, time]
                                  for unit in units if unit[0] == group)/denominator
               for group, time in [('E', 1), ('E', 2), ('L', 2)]}
    att = sum(effects.values())/sum(treatment.values())
    contrasts = {}
    for group, time, base in [('E', 1, 0), ('E', 2, 0), ('L', 2, 1)]:
        member = group+'1'
        contrasts[group+str(time)] = (outcomes[member, time]-outcomes[member, base]
                                      - outcomes['N', time]+outcomes['N', base])
    assert weights == {'E1': F(5, 8), 'E2': F(-1, 8), 'L2': F(1, 2)}
    assert sum(weights.values()) == 1
    assert beta == F(-91, 8) == sum(weights[k]*contrasts[k] for k in weights)
    assert att == 34 and contrasts == {'E1': F(1), 'E2': F(100), 'L2': F(1)}
    assert sum(2*v for v in contrasts.values())/6 == att
    rows = [{'unit': unit, 'time': time, 'treated': int(treatment[unit, time]),
             'outcome_thousand_USD': rational(outcomes[unit, time]),
             'true_effect_thousand_USD': rational(effects[unit, time]),
             'residualized_treatment': rational(residual[unit, time])}
            for unit, time in treatment]
    # Zero pretreatment differences do not exclude an unobserved concurrent shock.
    baseline_difference = [F(0), F(0)]
    true_effect, shock = F(2), F(3)
    apparent_did = true_effect+shock
    assert apparent_did == 5
    return {
        'status': 'exact_authored_reference', 'vendor_runtime': False,
        'law': 'Five equally weighted branches, three dates. E1/E2 adopt at t=1; L1/L2 at t=2; N never. Y(0)=10*i+2*t; no anticipation; no spillovers; all rows observed.',
        'units': 'Thousands of stipulated USD per branch-period; treatment costs excluded from outcomes.',
        'rows': rows, 'FWL_denominator': rational(denominator),
        'cohort_time_effects': {k: rational(v) for k, v in contrasts.items()},
        'TWFE_effect_weights': {k: rational(v) for k, v in weights.items()},
        'TWFE_projection_coefficient': rational(beta), 'treated_branch_period_ATT': rational(att),
        'comparison': 'All treated cohort/time effects are positive. The scalar projection is negative because its E2 weight is -1/8; it is not the six-treated-period average effect.',
        'stipulated_net_value': {'cost_USD_per_treated_period': 10000,
                                'true_average_net_USD': 24000,
                                'invalid_projection_as_value_USD': -21375,
                                'interpretation': 'The last number illustrates misuse of the projection as the ATT. Neither figure evaluates a new rollout policy or measured bank ROI.'},
        'trend_counterexample': {'times': [-2, -1, 0, 1], 'adoption_time': 0,
                                'pretreatment_group_differences': [rational(x) for x in baseline_difference],
                                'true_effect': rational(true_effect), 'concurrent_untreated_outcome_shock': rational(shock),
                                'observed_post_DID': rational(apparent_did),
                                'finding': 'Identical preperiod paths cannot rule out a postperiod differential counterfactual shock. A nonrejection is not proof of parallel untreated trends.'},
        'reversal_case': {'treatment_history': [0, 1, 0], 'absorbing_profile_admissible': False,
                          'finding': 'A return to zero violates the selected absorbing treatment profile. Refuse or select a separately justified switching design; do not collapse history to first treatment.'},
        'uncertainty': 'No sampling distribution or confidence coverage is claimed. Five branches do not qualify cluster or multiplier inference.',
    }


def source(name, title, url, markers, claims, kind='pdf'):
    original = BASE/(name+'.'+kind)
    text = BASE/(name+'.txt')
    body = text.read_text()
    lines = body.splitlines()
    anchors = []
    for marker in markers:
        positions = [i for i, line in enumerate(lines) if marker in line]
        assert positions, (name, marker)
        i = positions[0]
        char = body.find(lines[i])
        anchors.append({'marker': marker, 'line': i+1,
                        'physical_page': body[:char].count('\f')+1 if kind == 'pdf' else None,
                        'quote': '\n'.join(lines[max(0, i-1):i+5])})
    metadata = subprocess.run(['pdfinfo', str(original)], capture_output=True, text=True, check=True).stdout if kind == 'pdf' else 'Displayed last updated Wed, 12 Mar 2025 03:51:52 PST; exact product edition unresolved.'
    return {'source_identity': url, 'title': title, 'kind': 'official_technical_documentation',
            'cutoff': '2026-10-07', 'accessed_utc': datetime.fromtimestamp(original.stat().st_mtime, timezone.utc).isoformat(),
            'version_date': metadata, 'local_copy': ref(original, 'Authentic public official bytes'),
            'text_copy': ref(text, 'Inert extraction; original authoritative'),
            'headers': ref(BASE/(name+'.headers'), 'Saved original GET headers'),
            'inspected_anchors': anchors, 'supported_claims': claims,
            'limits': 'No exact cutoff bytes, engine execution, price, entitlement, product-wide absence or scientific guarantee inferred.'}


def local_probe():
    sys.path[:0] = [str(ROOT/'src'), str(ROOT/'tests')]
    from causalbank.operation_service_v12 import OperationService, REQUEST_SCHEMA, SUPPORTED
    from test_operation_service_v12 import context, request
    with tempfile.TemporaryDirectory(prefix='causal-panel-review-', dir=ROOT/'.runtime') as tmp:
        service = OperationService(Path(tmp))
        ctx = context()
        ctx['sampling'] = {'law': 'dependent_panel', 'unit': 'branch', 'fold_unit': 'branch'}
        response = service.invoke(request('identify.effect', {'method_id': 'did'}, ctx=ctx))
        enum = REQUEST_SCHEMA['properties']['operation']['enum']
        assert response['disposition'] == 'unsupported', response
        return {'mode': 'actual bounded local dispatcher probe; no vendor execution',
                'operation_enum': enum, 'implemented': SUPPORTED, 'panel_DID_request': response,
                'schema_source': ref(ROOT/'src/causalbank/operation_service_v12.py', 'Declared operation surface and dispatcher'),
                'limit': 'This transport refusal does not assert that the repository contains no other panel research code.'}


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    exact = exact_reference()
    write(BASE/'exact-reference.json', exact)
    records = [
        source('stata_did', 'didregress: Difference-in-differences estimation, including xtdidregress',
               'https://www.stata.com/manuals/causaldidregress.pdf',
               ['didregress estimates the average treatment effect', 'xtdidregress estimates the ATET',
                'wildbootstrap[ (wildopts) ] computes', 'Default cluster'],
               ['Repeated cross-sectional didregress and panel xtdidregress use a linear time/group or time/panel fixed-effect model.',
                'The inspected manual documents cluster-robust and restricted wild-bootstrap options; their presence does not qualify a chosen bank sampling law.']),
        source('stata_hdid', 'hdidregress: Heterogeneous difference in differences',
               'https://www.stata.com/manuals/causalhdidregress.pdf',
               ['controlgroup(cgtype) specifies', 'basetime(btspec) specifies',
                'is treated, it will remain treated.', 'hdidregress for repeated cross-sectional data implements'],
               ['Cohort/time ATET; never-treated versus not-yet-treated controls; adaptive versus common preperiod base.',
                'Selected formulas assume treatment remains on after adoption. Repeated cross-section and panel paths are separate.']),
        source('stata_xthdid', 'xthdidregress: Heterogeneous difference in differences for panel data',
               'https://www.stata.com/manuals/causalxthdidregress.pdf',
               ['xthdidregress is for panel data.', 'Specifying vce(robust) is equivalent',
                'groupvar may be, for example'],
               ['Panel RA/IPW/AIPW/extended-TWFE paths are documented; explicit unit/time/assignment clustering must survive conversion.',
                'For this command robust is documented as equivalent to clustering using the group variable; the label is command-specific.']),
        source('stata_hdid_post', 'Postestimation tools for hdidregress and xthdidregress',
               'https://www.stata.com/manuals/causalhdidregresspostestimation.pdf',
               ['estat ptrends tests', 'weights(weight type) defines',
                'sci or sci() is not allowed after the TWFE', 'estat aggregation is not allowed after estimation'],
               ['Overall/cohort/calendar/exposure aggregations and timecohort versus cohort weights have distinct targets.',
                'Multiplier simultaneous confidence options exclude TWFE in the inspected manual; aggregation is not allowed after bootstrap/jackknife estimation.',
                'The documented pretreatment test is not a proof of untreated counterfactual trends.']),
        source('eviews_did', 'EViews Help: Difference-in-Difference Estimation',
               'https://help.eviews.com/content/paneldid-Difference-in-Difference_Estimation.html',
               ['EViews offers built in tools', 'This chapter will introduce estimation', 'Wed, 12 Mar 2025'],
               ['The introductory page describes built-in DID within panel workfiles and introduces TWFE plus named postestimation diagnostic references.',
                'The short introduction does not establish the complete referenced estimator implementations, exact edition or covariance behavior.'], 'html'),
    ]
    audit = {'status': 'pass_for_bounded_primary_claims', 'reviewer': REVIEWER,
             'sources': records, 'limitations': LIMITS}
    write(BASE/'source-audit.json', audit)
    local = local_probe()
    write(BASE/'local-probe.json', local)
    acquisition = [ref(BASE/n, 'Original acquisition record, including failed routes') for n in
                   ['acquisition-manifest.json', 'alternate-acquisition.json', 'details-acquisition.json']]
    failures = [{'file': ref(p, 'Preserved request result'), 'observed': p.read_text().strip()}
                for p in sorted(BASE.glob('*.log')) if '200 https://' not in p.read_text()]
    write(BASE/'acquisition-review.json', {'status': 'observed', 'records': acquisition,
                                         'failures': failures, 'successful_technical_originals': 5,
                                         'finding': 'Initial sandbox DNS failures were retried with authorization. Three initial guessed paths and two later routes returned HTTP404; none establishes absent capability.'})
    candidates = [
        {'family': 'Stata', 'aliases': ['didregress', 'xtdidregress', 'hdidregress', 'xthdidregress', 'estat aggregation', 'estat sci'],
         'status': 'selected_primary_inspected', 'sources': [r['source_identity'] for r in records[:4]],
         'documented': 'Scalar fixed-effects and distinct heterogeneous cohort/time paths; data layout, absorbing treatment, controls, base time, aggregation and inference-option restrictions.',
         'proposal_route': 'Candidate licensed comparator; prefer cohort/time outputs for heterogeneous rollout. No vendor code port or executable admission.',
         'unresolved': 'Exact selected edition/options and cutoff bytes, native output matching, license/automation/export rights, price/support and valid finite cluster inference.'},
        {'family': 'EViews', 'aliases': ['DiD', 'panel workfiles', 'TWFE', 'Goodman-Bacon diagnostics'],
         'status': 'introductory_primary_only', 'sources': [records[4]['source_identity']],
         'documented': 'Introductory panel-only built-in DID description and named diagnostic references.',
         'proposal_route': 'Candidate documentation comparator; obtain full estimation/diagnostic originals before choosing a matched numerical comparison.',
         'unresolved': 'Complete technical pages, selected edition, supported estimands/controls, covariance, automation/rights and prices.'},
    ]
    for family, aliases in [
        ('SAS', ['SAS/STAT', 'SAS Econometrics', 'panel and causal procedures']),
        ('IBM', ['SPSS Statistics', 'MIXED', 'panel regression']),
        ('MathWorks', ['MATLAB', 'Econometrics Toolbox', 'panel regression']),
        ('Commercial open-source frontends', ['Posit', 'RStudio', 'licensed hosting of R/Python DID'])]:
        candidates.append({'family': family, 'aliases': aliases, 'status': 'relevant_original_not_inspected',
                           'sources': [], 'documented': 'No DID-specific technical capability established in this bounded review.',
                           'proposal_route': 'Identify the edition-specific DID procedure and inspect original technical documentation; generic regression or hosting is not sufficient.',
                           'unresolved': 'Identity of applicable DID module and original method documentation; rights, price, runtime and causal semantics.'})
    write(BASE/'candidate-register.json', {'cutoff': '2026-10-07', 'candidates': candidates,
                                         'stopping_rule': 'Local-first inspected scopes plus three initial paths, four alternate routes and three linked detail/index routes; no further speculative route search in this attempt.',
                                         'local_search': ref(BASE/'local-search.txt', 'Recorded local search; integrated readers are not treated as vendor originals'),
                                         'market_saturation': False})
    contract = {
        'status': 'proposed_not_implemented', 'target': 'ATT(g,t) and declared aggregation for a staggered branch-policy rollout',
        'inputs': ['branch identity, calendar and actual adoption history including reversals', 'panel versus repeated cross-section identity',
                   'assignment/cluster unit, comparison-group rule, anticipation window and covariate availability clock',
                   'base-time rule, estimable cohort/time support, missing/attrited rows, weights and chosen uncertainty method'],
        'outputs': ['cohort/time estimates and support counts before aggregation', 'explicit aggregation weights and calendar/exposure interpretation',
                    'cluster/covariance identity, effective sample and retained unavailable cells', 'pointwise versus simultaneous uncertainty and effective option restrictions',
                    'trend/overlap diagnostics separate from assumptions, sensitivity and money conversion'],
        'refusals': ['reversals under an absorbing-only profile', 'unobserved adoption concealed by sample gaps',
                     'unsupported control cells or no identifying comparison', 'unsupported inference/estimator combination',
                     'missing assignment unit, future covariates, unidentified units or silently changed aggregation'],
        'trial': ['Reproduce the exact 15-row FWL/ATT reference under a licensed selected edition.',
                  'Add an unbalanced/missing-period case and compare retained rows, exposure support and aggregation weights.',
                  'Exercise reversal, anticipation, no-control, unsupported SCI and failed-fit cases with failures retained.',
                  'Use a separately registered generated multi-cluster law for uncertainty qualification; the five-branch exact law is only an arithmetic oracle.'],
        'later_obligations': ['licensed runtime and terms for numerical comparison', 'prototype implementation and output conversion',
                              'authentic assignment/trend/economic premises only for later bank claims'],
    }
    write(BASE/'conversion-contract.json', contract)
    omissions = {'status': 'open_scoped', 'items': [
        {'gap': c['family'], 'details': c['unresolved'], 'route': c['proposal_route']} for c in candidates],
        'manuscript': 'Integrate bounded technical findings through a preserving reviewed reader successor; do not count this receipt as new manuscript depth.',
        'global_blocker': None, 'unavailable_is_not_absent': True}
    write(BASE/'omissions-register.json', omissions)
    evidence = [ref(BASE/n, anchor) for n, anchor in [
        ('plan.md', 'Bounded reviewed execution plan'), ('plan-review.json', 'Author plan review'),
        ('source-audit.json', 'Five authentic originals and inspected technical anchors'),
        ('candidate-register.json', 'Six candidate families, aliases and search bounds'),
        ('acquisition-review.json', 'Successful originals and preserved DNS/HTTP failures'),
        ('exact-reference.json', 'Exact authored staggered rollout and trend/reversal counterexamples'),
        ('local-probe.json', 'Actual local dependent-panel DID refusal'),
        ('conversion-contract.json', 'Proposed target, conversion, uncertainty and refusal contract'),
        ('omissions-register.json', 'Open sources, editions, rights, runtime and manuscript obligations')]]
    evidence.append(ref(Path(__file__).resolve(), 'Exact computation and bounded source review'))
    review = {'status': 'pass_for_scoped_inconclusive_disposition', 'reviewer': REVIEWER,
              'findings': ['The exact ATT is +34 thousand USD; the same panel TWFE projection is -91/8 thousand with weights 5/8,-1/8,1/2.',
                           'Never-treated cohort/time differences reproduce the three true effects in the authored parallel-trend law.',
                           'A postperiod counterfactual shock defeats an inference of parallel trends from zero preperiod differences.',
                           'Five primary manuals/pages support bounded documented behavior; unresolved vendor families and exact editions prohibit full cell acceptance.',
                           'The current dispatcher actually refuses the selected dependent-panel DID request; a proposed engine/interface is not an installed capability.'],
              'evidence': evidence, 'limitations': LIMITS, 'integration_allowed': False, 'visual_acceptance': False}
    write(BASE/'author-review.json', review)
    write(OUTPUT, {'operation_id': OP, 'status': 'inconclusive', 'scope': 'Six-family source-bounded commercial panel-DID comparison',
                   'reviewer': REVIEWER, 'cutoff': '2026-10-07', 'candidates': candidates,
                   'exact_reference': ref(BASE/'exact-reference.json', 'Exact authored laws'),
                   'local_runtime': ref(BASE/'local-probe.json', 'Actual bounded dispatcher observation'),
                   'proposed_contract': ref(BASE/'conversion-contract.json', 'Unimplemented comparator design'),
                   'evidence': evidence, 'limitations': LIMITS, 'capabilities': [], 'integration_allowed': False})
    run = extension.base
    state = run.core.read(ROOT, run.core.STATE)
    graph, merged, stages = extension.combined(ROOT, state)
    node = run.ledger.operation(graph, OP)
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive', execution='performed',
                   scope='Performed bounded source, exact-reference and actual local-interface review; complete commercial coverage remains unresolved.',
                   reviewer=REVIEWER, limitations=LIMITS, outputs=[ref(OUTPUT, 'Contracted commercial panel coverage review')],
                   capabilities=[], original_gap_qualification=False,
                   revisit_trigger='Acquire identified edition-specific missing originals, full EViews methods, selected rights and a licensed comparison environment; publish a reviewed manuscript successor.')
    findings = [
        ('inconclusive', 'Six candidate families/aliases and a bounded local/official search are recorded, but complete market saturation and missing DID-specific originals remain unresolved.'),
        ('pass', 'Every positive technical claim is bounded to five authentic local originals with SHA-256, acquisition metadata and inspected anchors; authored arithmetic and actual local refusal are separate.'),
        ('inconclusive', 'Alternatives and omissions are explicit. Four source-specific vendor families, complete EViews technical text and selected edition/rights/runtime evidence remain open without an unavailable-source waiver.')]
    receipt['criteria'] = [{'index': i, 'verdict': verdict, 'finding': finding, 'evidence': evidence}
                           for i, (verdict, finding) in enumerate(findings)]
    write(BASE/'operation-receipt.json', receipt)
    print(json.dumps({'status': 'inconclusive', 'originals': len(records), 'families': len(candidates),
                      'exact_ATT': 34, 'TWFE': '-91/8', 'local_DID': 'unsupported', 'integration_allowed': False}))


if __name__ == '__main__':
    main()
