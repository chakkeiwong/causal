#!/usr/bin/env python3
"""Bind the recovered S7 argument to primary originals and exact authored laws."""
import json
from pathlib import Path

import s7_examples_20261017 as examples
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT, BASE = examples.ROOT, examples.BASE
PRIOR = ROOT/'docs/program/execution/2026-10-17/s6/publication-v2/reader/source-audit.json'
CHAPTER = ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.S7/chapter.tex'
LIMITS = [
    'Author review only; no independent scientific or institutional acceptance.',
    'Exact stipulated structural laws and hypothetical USD amounts are not bank observations, upstream runtime trials or sampled coverage results.',
    'Graph invariance, truthful joint audits, independent neighborhoods, feasible action laws and monetary inputs require their own evidence.',
    'The concentration design is prospective and conditional; audit allocations optimize only the stated worst-case variance criterion.',
    'Selected source inspection does not close the complete software census, downstream numerical qualification or dependency rights.',
    'Literature cutoff 2026-10-07; pinned versions and historical snapshot/commit-membership limits remain attached.',
    'Rendered visual acceptance remains false under the exhausted inherited image allowance.'
]
SPECS = [
    ('guha2022', 'docs/literature/text/guha2022.txt', 78, 215,
     'Joint outcome/linkage approach; duplicate-free one-to-one bipartite files, SUTVA/no interference and ignorability restrict the causal use.'),
    ('guha2022', 'docs/literature/text/guha2022.txt', 215, 260,
     'One-to-one matching prior and Section 2.3 coupling of linked outcome regressions, unmatched outcomes and record linkage; not an arbitrary interference likelihood.'),
    ('tu2019', 'docs/literature/text/tu2019.txt', 150, 216,
     'Causal sufficiency, Markov/faithfulness, no substantive effects from missingness indicators, faithful observability, no deterministic indicator relations and no self-masking.'),
    ('corrupt2022', 'docs/literature/text/corrupt2022.txt', 782, 860,
     'Section 5.1 bounded approximately low-rank signal, mean-zero subexponential errors independent across rows and row-independent masking with within-row dependence allowed.'),
    ('pearltransport2014', 'docs/literature/text/pearltransport2014.txt', 610, 710,
     'Selection-diagram invariance, Theorem 2 and pretreatment S-admissibility corollary justify transport only under their declared graphical conditions.'),
    ('sw_splink', 'docs/literature/raw/raw_readme_splink.md', 1, 160,
     'Fellegi-Sunter linkage, pair predictions and estimated clusters; multiple informative non-highly-correlated fields; upstream performance claims are unmeasured here.'),
    ('v12_sw_causallearn', 'docs/literature/raw/v12_sw2_source_causallearn_pc.txt', 1, 140,
     'Pinned PC dispatch sends mvpc=True to the missing-value route, substitutes mv_fisherz and passes correction_name; dispatch does not prove arbitrary MNAR identification.'),
    ('v12_sw_sensemakr', 'docs/literature/raw/v12_sw2_manual_sensemakr_1.txt', 1, 186,
     'Partial-R-squared regression sensitivity and benchmark kd/ky inputs remain supplied assumptions; coefficient/standard-error/df inputs are distinct; GPL-3 declaration is not complete rights clearance.'),
    ('v13_sw_mossspider', 'docs/literature/raw/v12_gap3_mossspider_technical.txt', 1, 205,
     'Direct-contact stochastic NetworkTMLE, complete node attributes/no missing-data procedure, unweighted adjacency, degree background and directed influence convention; observed MIT text does not qualify all dependencies.'),
    ('v13_sw_inferference', 'docs/literature/raw/v12_gap3_inferference_technical.txt', 1, 205,
     'Grouped IPW formula/model routes, at least two groups, default one-random-effect integrand and integrate_allocation prose/signature disagreement; GPL>=2 metadata only.')
]


def main():
    prior = json.loads(PRIOR.read_text()); verify_bindings(prior)
    index = {s['integrated_citation_key']: s for s in prior['sources']}
    assert len(index) == 717
    verify_bindings(json.loads((BASE/'mathematics-review.json').read_text()))
    exact = json.loads((BASE/'exact-results.json').read_text())
    assert examples.calculate() == exact and examples.separate(exact)['status'] == 'pass'
    assert abs(float(exact['neighborhood_design']['radius_at_473']) - .062446) < .0000005
    folder = BASE/'inspected'; folder.mkdir(exist_ok=False)
    rows = []
    for i, (key, path, first, last, claim) in enumerate(SPECS, 1):
        original = ROOT/path; lines = original.read_text().splitlines()
        assert last <= len(lines)
        excerpt = folder/f'{i:02d}-{key}-{first}-{last}.txt'
        excerpt.write_text('\n'.join(lines[first-1:last])+'\n')
        old = index[key]
        row = dict(citation_key=key,
            source_identity=old.get('source_identity') or old.get('title'),
            version_date=old.get('version_date') or old.get('version_status'),
            local_copy=ref(original, f'Inspected lines {first}-{last}'),
            inspected_excerpt=ref(excerpt, 'Exact inspected primary-text excerpt'),
            supported_claims=[claim])
        if old['kind'] == 'paper':
            row['genuine_pdf'] = dict(path=old['local_path'], sha256=old['sha256'],
                                      anchor='Genuine scholarly original')
        rows.append(row)
    write(BASE/'primary-review.json', dict(status='pass_for_bounded_synthesis',
        reviewer=dict(name='Codex author/coordinator', kind='author'), cutoff='2026-10-07',
        records=rows, inherited_source_records=[index[k] for k in sorted({s[0] for s in SPECS})],
        evidence=[ref(PRIOR, '717 preserved audited records'), ref(Path(__file__), 'Evidence preparation')],
        limitations=LIMITS))
    write(BASE/'prototype-design.json', dict(status='prospective_design',
        question='Can observation, graph uncertainty, feasible action allocation and target transport preserve the same causal decision before costly bank experiments?',
        routes=[
            dict(target='Identity and missing observations',
                 candidates=['Original Python Splink', 'Original Python causal-learn missing-value route',
                             'Source-compatible low-rank corruption model'],
                 admission='Preserve identity versus influence meaning, blocking coverage, clock, joint constraints, missingness/test assumptions and row sampling law.'),
            dict(target='Conditional network/group value',
                 candidates=['Original Python MossSpider', 'Original R inferference'],
                 admission='Retain complete graph attributes, direction, exposure, group dependence, full allocation law, integration settings and a justified variance law.'),
            dict(target='Sensitivity and outer graph/transport uncertainty',
                 candidates=['Original R sensemakr for supported regression targets', 'Explicit joint graph-moment optimization'],
                 admission='Keep partial-R-squared restrictions distinct from graph overlap, target weights, pooled constraints and scientific transport invariance.')],
        stages=[
            'Use exact finite graph/action enumeration and affine-box witnesses for target, baseline, support, units and monetary admission.',
            'Use permitted public structure only with its published meaning; add declared generated causal, identity, observation and audit truth.',
            'Freeze versions, mechanisms, seeds, all scenarios, repetitions, numerical tolerances and stopping rules before a fresh statistical study.',
            'Compare hard completion, warranted joint probability, identified sets and joint audits on matched target/action laws; include independent and coordinated allocations.',
            'Report graph-region retention, target error, set containment, availability, width, decision loss, numerical error and observed full workflow cost; retain every failed/refused request.'],
        negative_controls=['One-edge-only audits', 'Wrong relationship direction', 'Shared adjudication errors',
                           'Unsupported missingness', 'Pooled-to-target aggregation', 'Infeasible overlapping pair laws'],
        future_inputs=['Owned influence meaning and truthful joint audit law', 'Feasible global action design',
                       'Bank target composition and accepted loss/precision thresholds', 'Actual prices',
                       'Complete dependency rights, permitted package runtimes and consumer acceptance'],
        upstream_packages_executed=False, sampled_coverage_established=False,
        bank_qualified=False, whole_census_closed=False, limitations=LIMITS))
    claims = [
        ('math', 'Joint relationship, policy, transport and audit-design exact references',
         'project_derivation', BASE/'exact-results.json', [
             'Edge marginals permit sharp net value [-8,8]; changing the feasible action dependence can remove the overlap parameter under the matched specified baseline.',
             'Matching and isolate/cycle graphs have equal mean degree but opposite target decisions; pooled source overlap gives sharp target bounds [-10/3,58/3].',
             'A supplied completion mixture has variance 65; truthful independent whole-neighborhood audits have the derived prospective radius and conditional 473-audit sufficient design.',
             'Target-weighted audit allocations attain the exact stated equal-price and relative-price variance bounds.']),
        ('paths', 'Source-specific observation, network and transport software composition',
         'software_primary_sources', BASE/'primary-review.json', [
             'Inspected pinned or hash-bound originals retain their distinct linkage, missingness, row-independence, regression sensitivity and network/group restrictions.',
             'Original-language adapters are proposed conditionally; dispatch, license metadata and conditional graph evaluation do not qualify a new joint causal composition or native port.']),
        ('design', 'Prospective public and generated observation-to-policy comparison',
         'project_design', BASE/'prototype-design.json', [
             'Semantic and exact finite-law admission precedes a frozen generated statistical comparison with separate uncertainty and complete failure accounting.',
             'Public structure and explicitly generated truth can demonstrate a prototype question; no bank influence truth, actual cost, package execution or ROI is inferred.'])]
    sources = []
    for key, title, kind, path, supported in claims:
        sources.append(dict(integrated_citation_key='exec17_s7_'+key, title=title,
            author='Causal banking proposal', kind=kind, year=2026,
            source_identity='Authored exact law, conditional proof, prospective design or identity-bound primary-source synthesis',
            version_date='2026-10-17; inherited versions and 2026-10-07 cutoff retained',
            local_copy=ref(path, title), inspected_anchors=supported, supported_claims=supported,
            records=[ref(p, 'Inspected mathematical or primary-source evidence') for p in
                [BASE/'primary-review.json', BASE/'mathematics-review.json', BASE/'plan.md', Path(__file__)]],
            limitations=LIMITS))
    write(BASE/'source-audit.json', dict(sources=sources, cutoff='2026-10-07',
        prior=ref(PRIOR, '717 unchanged source identities')))
    write(BASE/'precompile-author-review.json', dict(status='pass_for_compilation',
        reviewer=dict(name='Codex author/coordinator', kind='author'),
        findings=[
            'Graph and action probability tables are coherent; action independence from graph and disjoint pair feasibility are explicit.',
            'Each financial contrast declares its own matched baseline, beneficiary denominator, incremental contact expenses and investment.',
            'Topology support failure is separated from stipulated invariant response; pooled information is not silently enlarged by unobserved experiments.',
            'Compatible value sets, supplied posterior weights, sampling confidence and numerical integration error remain distinct.',
            'The 473-audit radius rounds correctly; the prospective sign guarantee needs truthful independent joint units and theta<=1/8.',
            'Target-weighted allocations optimize only the supplied variance bound; a valid pooled constraint could support a different estimator.',
            'Software claims retain genuine originals, exact versions, incompatible assumptions and unqualified runtime/rights; no native port or bank benefit is claimed.',
            'Inherited catalogs, generic observation/transport/sensitivity and prototype/interface framing receive no duplicate depth; rendered depth remains to be reviewed.'],
        evidence=[ref(p, 'Reviewed source or exact evidence') for p in
            [CHAPTER, BASE/'plan.md', BASE/'primary-review.json', BASE/'mathematics-review.json',
             BASE/'source-audit.json', BASE/'prototype-design.json']],
        visual_acceptance=False, limitations=LIMITS))
    print(json.dumps(dict(primary_excerpts=len(rows), new_records=3,
        expected_total=720, scholarly_pdfs=188, visual_acceptance=False)))


if __name__ == '__main__':
    main()
