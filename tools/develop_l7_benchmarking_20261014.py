#!/usr/bin/env python3
"""Exact proposal references and primary rereads; no model or bank trial."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import subprocess

from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-14/l7-benchmarking'
PRIOR = ROOT / 'docs/program/execution/2026-10-14/failure-trials/publication/reader/source-audit.json'
REVIEWER = {'name': 'Codex author/coordinator', 'kind': 'author'}
INHERITED = [
    'program/repair-v12/work/LA07/evaluation-chapter.tex',
    'program/gap-repair-v13/work/LA07/evaluation-extension.tex',
    'program/execution/2026-10-13/llm-census/evaluation.tex',
    'program/execution/2026-10-13/live-evaluation/evaluation.tex',
    'program/execution/2026-10-14/native-evaluation-reader/v3/evaluation-development.tex',
]


def serial(value):
    if isinstance(value, F):
        return {'exact': str(value), 'decimal': float(value)}
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def clean_bounds(p, upper_exposure):
    assert 0 <= p <= 1 and 0 <= upper_exposure < 1
    return (max(F(0), (p - upper_exposure) / (1 - upper_exposure)),
            min(F(1), p / (1 - upper_exposure)))


def calculate():
    # Exhaust every allocation of 20 exposed cases to the fixed paired table.
    counts = [64, 20, 16, 0]  # both correct, A only, B only, neither
    admissible = []
    for both, only_a, only_b in product(range(21), repeat=3):
        neither = 20 - both - only_a - only_b
        chosen = [both, only_a, only_b, neither]
        if any(not 0 <= k <= n for k, n in zip(chosen, counts)):
            continue
        clean = [n - k for n, k in zip(counts, chosen)]
        a, b = F(clean[0] + clean[1], 80), F(clean[0] + clean[2], 80)
        admissible.append((chosen, a, b, a - b))
    a_bounds = clean_bounds(F(84, 100), F(1, 5))
    b_bounds = clean_bounds(F(80, 100), F(1, 5))
    assert a_bounds == (min(v[1] for v in admissible), max(v[1] for v in admissible))
    assert b_bounds == (min(v[2] for v in admissible), max(v[2] for v in admissible))
    lo = min(admissible, key=lambda v: v[3])
    hi = max(admissible, key=lambda v: v[3])
    assert lo[3] == F(-1, 5) and hi[3] == F(1, 4)
    assert clean_bounds(F(21, 25), F(0)) == (F(21, 25), F(21, 25))

    # Independent Bernoulli inclusion; every error label is stipulated and exact.
    labels = (1, 1, 1, 0)
    inclusion = (F(1, 2), F(1, 4), F(3, 4), F(1))
    rows = []
    for selected in product((0, 1), repeat=4):
        prob = F(1)
        for z, pi in zip(selected, inclusion):
            prob *= pi if z else 1 - pi
        if not prob:
            continue
        estimate = sum((F(z * d) / pi for z, d, pi in zip(selected, labels, inclusion)), F(0)) / 4
        rows.append({'selected': selected, 'probability': prob, 'estimate': estimate})
    mean = sum((r['probability'] * r['estimate'] for r in rows), F(0))
    variance = sum((r['probability'] * (r['estimate'] - mean)**2 for r in rows), F(0))
    variance_formula = sum(((1-pi) / pi * d*d for d, pi in zip(labels, inclusion)), F(0)) / 16
    clipped_mean = sum((r['probability'] * min(F(1), r['estimate']) for r in rows), F(0))
    assert sum((r['probability'] for r in rows), F(0)) == 1
    assert mean == F(3, 4) and variance == variance_formula == F(13, 48)
    assert max(r['estimate'] for r in rows) == F(11, 6)
    assert clipped_mean != mean
    partial = (F(2, 100), F(2 + 90, 100))
    assert partial == (F(1, 50), F(23, 25))

    # Independent SCM enumeration and analytic action/outcome references.
    def effect(x_law, response):
        return sum((p * (response(1, x) - response(0, x)) for x, p in x_law), F(0))
    fair_x = [(0, F(1, 2)), (1, F(1, 2))]
    constant_x = [(0, F(1))]
    direct = effect(fair_x, lambda a, x: a+x)
    reversed_action = effect(fair_x, lambda b, x: 1-b+x)
    squared = effect(fair_x, lambda a, x: (a+x)**2)
    squared_constant = effect(constant_x, lambda a, x: (a+x)**2)
    threshold = effect(fair_x, lambda a, x: int(a+x >= 1))
    assert direct == 1 and reversed_action == -1
    assert squared == 2 and squared_constant == 1 and threshold == F(1, 2)
    # Check the exact rename, action-reversal and unit relations for the zero rule.
    wrong = F(0)
    assert wrong == -wrong and wrong == 100 * wrong
    assert wrong != direct
    return serial({
        'evidential_status': 'Project-authored exact development constructions; no stochastic or live-model study',
        'contamination': {
            'observed_paired_counts': dict(zip(['both','A_only','B_only','neither'], counts)),
            'observed_accuracy_A': F(21,25), 'observed_accuracy_B': F(4,5),
            'assumed_max_exposure': F(1,5), 'clean_A_bounds': a_bounds, 'clean_B_bounds': b_bounds,
            'enumerated_exposure_allocations': len(admissible),
            'minimum_clean_difference': {'exposed_counts': lo[0], 'A': lo[1], 'B': lo[2], 'difference': lo[3]},
            'maximum_clean_difference': {'exposed_counts': hi[0], 'A': hi[1], 'B': hi[2], 'difference': hi[3]},
            'interpretation': 'Descriptive accuracy conditional on no exposure; not retraining under removed exposure',
        },
        'verification': {
            'population': 100, 'reviewed': 10, 'reviewed_errors': 2,
            'finite_population_error_bounds': partial,
            'known_labels_small_population': labels, 'independent_inclusion_probabilities': inclusion,
            'enumeration': rows, 'weighted_mean': mean, 'weighted_variance': variance,
            'algebraic_variance': variance_formula, 'clipped_mean': clipped_mean,
            'assumptions': 'Fixed frozen outputs; correct labels; known positive independent Bernoulli inclusion; no review nonresponse',
        },
        'metamorphic': {
            'SCM': 'Independent fair Bernoulli A and X; Y=A+X, in hundreds of USD',
            'effect': direct, 'action_reversed_effect': reversed_action,
            'squared_effect_fair_X': squared, 'squared_effect_X_zero': squared_constant,
            'threshold_at_one_effect': threshold, 'wrong_rule_output': wrong,
            'wrong_zero_rule_passes_rename_reversal_unit_relations': True,
            'illustrative_cost_USD': 40, 'true_net_USD': direct*100-40,
            'wrong_rule_predicted_net_USD': wrong*100-40,
            'limit': 'Stipulated development algebra; no model performance, effect inference or bank ROI',
        },
    })


def prepare():
    assert not (BASE/'exact-results.json').exists()
    write(BASE/'exact-results.json', calculate())
    prior = json.loads(PRIOR.read_text())
    source = next(s for s in prior['sources'] if s['integrated_citation_key'] == 'v12_la_2407_19638')
    verify_bindings(prior)
    inspected = BASE/'inspected'
    inspected.mkdir(exist_ok=False)
    pages = []
    anchors = {
        2: 'Accessible-corpus motivation and relation-prediction scope; not a universal contamination estimate.',
        3: 'RQ1 accessible OLMo/BLOOM corpus and synthetic-frequency interventions; RQ2 response-frequency definition; RQ3 contexts.',
        8: 'Context sample, thirteen annotators and Table1 affirmative ratios; contextual change can change the claim.',
        9: 'Conclusion and limitations: accessible corpora and predominantly commonsense relations.',
    }
    for n, finding in anchors.items():
        dest = inspected / ('feng-page-'+str(n)+'.txt')
        subprocess.run(['pdftotext','-f',str(n),'-l',str(n),str(ROOT/source['local_path']),str(dest)],
                       check=True,timeout=15)
        pages.append({'pdf_page':n,'finding':finding,'extract':ref(dest,'Inspected primary text')})
    code = ROOT/'docs/literature/raw/v12_la_causalds_source_2.txt'
    assert 'return not ident.get("identifiable", True)' in code.read_text()
    write(BASE/'primary-review.json', {
        'reviewer':REVIEWER, 'cutoff':'2026-10-07',
        'exposure_source':source, 'reread':pages,
        'supported_claims':[
            'Observed relation-frequency association and controlled synthetic exposure/context studies motivate sensitivity analysis.',
            'The inspected source supplies no exposure upper bound for an arbitrary closed provider or this proposed banking benchmark.',
            'Response frequency and annotator agreement do not themselves establish a causal relation as true.',
        ],
        'scorer_reread':{
            'original':ref(code,'Pinned CausalDS grader.py lines152-174'),
            'claim':'Missing identification metadata defaults require explicit unknown-oracle admission handling before reuse.',
            'revision':'c74671d0a0924efc5bb021fc8966f856d5b80a4f;2026-07-17',
            'source_identity':'https://github.com/andleb/causalds',
        },
        'inherited_chapter_inputs':[ref(ROOT/'docs'/p,'Unchanged L7 argument and citation context') for p in INHERITED],
        'inherited_benchmark_review':ref(ROOT/'docs/program/execution/2026-10-14/evaluation-cost/primary-review.json',
                                       'Seven primary papers and two pinned benchmark sources; scoped inherited findings'),
        'limits':'No new source search, live calls, source-package execution or independent review.',
    })
    old = ROOT/'docs/program/execution/2026-10-14/evaluation-cost/candidate-reassessment.json'
    write(BASE/'omissions-register.json',{
        'inherited_candidates':ref(old,'Five uninspected leads; no absence or completed-frontier claim'),
        'status':'Selected benchmark evidence is developed; broader census remains open.',
        'next_action':'Reconcile each candidate with acquired originals, use allowed primary routes, then extend the benchmark comparison.',
        'external':[
            'Exact current model revisions, training exposure and provider pricing are not measured.',
            'Human/adjudicator accuracy and independent mechanisms need real evidence for a live-performance claim.',
            'The visual review requires a fresh session under the exhausted six-image allowance.',
        ],
    })
    write(BASE/'derivation-review.json',{
        'reviewer':REVIEWER, 'status':'pass',
        'plan':ref(BASE/'plan-review.md','Reviewed scope and independence'),
        'exact':ref(BASE/'exact-results.json','Finite enumerations and algebraic checks'),
        'procedure':ref(Path(__file__).resolve(),'Exact executable reference'),
        'findings':[
            'Exposure mixture bounds are sharp over a bounded exposure fraction; descriptive clean-subset and retrained counterfactual targets differ.',
            'One paired score table admits opposite clean-subset rankings at the same20% exposure fraction.',
            'Selective verified labels alone give finite bounds2%-92%; positive known inclusion permits a design-unbiased alternative only under truthful complete review.',
            'Eight possible audit selections reproduce mean3/4 and variance13/48; clipping changes the expectation.',
            'Wrong zero effect satisfies renaming, action-reversal and unit relations; a known nonzero oracle detects it.',
            'A nonlinear outcome objective changes the effect and requires its own reference; identical original effects need not share transformed effects.',
        ],
        'limitations':[
            'No empirical claim about model exposure, correctness, label quality, live costs or bank effects.',
            'An exposure bound and sampling design must be independently justified; formulas cannot supply missing inputs.',
            'Mathematical checks do not replace rendered review or full frontier coverage.',
        ],
    })
    sources = []
    for suffix, title, filename, anchor, claims in [
        ('exposure_audit','Exposure and oracle-admission primary reread','primary-review.json',
         'Feng physical pages2,3,8,9; pinned CausalDS grader lines152-174',
         ['Scoped primary-source motivation and scorer boundary; no model exposure estimate.']),
        ('exact','Exact exposure, verification and consistency counterexamples','exact-results.json',
         'contamination;verification;metamorphic',
         ['Sharp sensitivity ranges, exact probability-sampling moments, wrong consistent rule and transformed targets.']),
    ]:
        sources.append({
            'integrated_citation_key':'exec14_l7_'+suffix,
            'kind':'project_derivation' if suffix=='exact' else 'project_source_review',
            'title':title,'author':'Causal banking proposal','year':2026,'version_date':'2026-10-14',
            'source_identity':'Project-authored L7 analysis; independently identified primary bytes where stated',
            'local_copy':ref(BASE/filename,anchor),'inspected_anchors':[anchor],'supported_claims':claims,
            'records':[ref(Path(__file__).resolve(),'Exact source and mathematical review procedure')],
            'limitations':['Proposal development; no live-model, bank or independent acceptance.'],
        })
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,
                                  'prior':ref(PRIOR,'568 inherited source records')})
    print(json.dumps({'exact_references':'pass','source_records':len(sources),
                      'exposure_allocations':calculate()['contamination']['enumerated_exposure_allocations']}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','calculate'])
    args=parser.parse_args()
    if args.command=='prepare':
        prepare()
    else:
        print(json.dumps(calculate(),indent=2))
