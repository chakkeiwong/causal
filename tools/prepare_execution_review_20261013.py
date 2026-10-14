#!/usr/bin/env python3
"""Materialize the author's inspected-source notes and bounded R review."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'docs/program/execution/2026-10-13'
RAW = 'docs/literature/raw/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ref(path, anchor):
    return {'path': path, 'sha256': digest((ROOT / path).read_bytes()), 'anchor': anchor}


def write(path, value):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def source(identifier, filename, title, author, version, findings, related=()):
    path = RAW + filename
    receipt_path = RAW + filename.rsplit('.', 1)[0] + '.receipt.json'
    receipt = json.loads((ROOT / receipt_path).read_text())
    data = (ROOT / path).read_bytes()
    assert receipt['sha256'] == digest(data)
    pdf = filename.endswith('.pdf')
    text = (subprocess.check_output(['pdftotext', '-layout', str(ROOT / path), '-'], text=True)
            if pdf else data.decode())
    anchors = []
    for anchor, finding in findings:
        if isinstance(anchor, int):
            block = text.split('\f')[anchor - 1]
            name = f'Physical PDF page {anchor}'
        else:
            start, end = anchor
            block = '\n'.join(text.splitlines()[start - 1:end])
            name = f'Lines {start}–{end}'
        assert block.strip()
        anchors.append({'anchor': name, 'text_sha256': digest(block.encode()), 'finding': finding})
    return {'integrated_citation_key': identifier, 'kind': 'software_documentation',
            'title': title, 'author': author, 'source_identity': receipt['url'],
            'version_date': version, 'accessed_utc': receipt['accessed_utc'],
            'cutoff': '2026-10-07', 'local_copy': ref(path, 'Inspected primary text'),
            'acquisition_receipt': ref(receipt_path, 'Public acquisition identity and bytes'),
            'inspected_anchors': anchors, 'supported_claims': [x['finding'] for x in anchors],
            'related_primary_bytes': [ref(RAW + f, a) for f, a in related],
            'limits': 'Text/source inspection; no package execution, statistical qualification or bank truth. Acquisition after cutoff is distinct from the stated source revision.'}


def main():
    sources = [
        source('exec13_pcalg', 'v12_sw_cran_manual_pcalg.pdf', 'pcalg reference manual', 'pcalg contributors',
               '2.7-12; package Date 2024-09-12; manual generated 2026-05-09', [
                   (1, 'PC, FCI/RFCI, GIES, IDA and adjustment criteria have distinct scopes. GPL >=2, R >=3.5, compiled Rcpp/RcppArmadillo/BH path and graph dependencies.'),
                   (39, 'Ancestral-graph endpoint matrix: entry [i,j] denotes the endpoint at j; 0 absent, 1 circle, 2 arrow, 3 tail. This is not a coefficient or DAG binary adjacency matrix.'),
                   (88, 'IDA requires a linear Gaussian causal model, covariance information and an estimated graph; the target is a total effect.'),
                   (89, 'IDA returns a multiset of possible total effects over compatible DAGs; a multiset is not a confidence interval.'),
                   (119, 'pc requires alpha and indepTest; NAdelete defaults true, m.max infinite; explicit node labels and constraints are inputs.'),
                   (120, 'Stable skeleton is distinguished from orientation rules; acyclicity, sufficient information, Markov and faithfulness assumptions matter.'),
                   (121, 'Orientation order dependence and conservative/majority/conflict options require separate attention; do not infer that stable skeleton fixes every orientation issue.')]),
        source('exec13_bnlearn', 'v12_sw_cran_manual_bnlearn.pdf', 'bnlearn reference manual', 'Marco Scutari and contributors',
               '5.2.1; package and manual date 2026-07-17 (corrects predecessor note of July 18)', [
                   (1, 'Structure/parameter learning, interventions and counterfactuals are documented. GPL >=2; R >=4.4; compiled C17 requirement.'),
                   (35, 'DirectLiNGAM exposes pwling/default and gkernel order criteria with adaptive LASSO selection; this is a functional-model route.'),
                   (37, 'Intervention and counterfactual operations treat networks as causal models; availability of the operation does not validate causal assumptions.'),
                   (44, 'Constraint learning has explicit CI tests/alpha and can return a partially directed graph.'),
                   (45, 'Defaults depend on data type; alpha .05; incomplete data use locally complete subsets for the individual tests.'),
                   (69, 'Hybrid algorithms combine restriction and score maximization rather than creating independent causal guarantees.'),
                   (70, 'mmhc uses mmpc plus hc; h2pc uses hpc plus hc.'),
                   (105, 'hc/tabu are score searches; data type determines the BIC default.'),
                   (106, 'hc has no random restarts by default; max iterations and max parents can be unbounded; tabu length defaults 10.')]),
        source('exec13_bcdag', 'exec13_bcdag_manual.pdf', 'BCDAG reference manual', 'Federico Castelletti and Alessandro Mascaro',
               '1.1.4; 2026-06-21; CRAN mirror dee5679affbb34112a8a6bdab3491f368aa8ce55', [
                   (1, 'Gaussian DAG structure and joint causal-effect learning; MIT plus LICENSE; graph/gRbase/Rgraphviz/mvtnorm dependencies; no package compilation declared.'),
                   (3, 'causaleffect returns the total joint intervention effects for a specified Gaussian DAG and Cholesky parameters.'),
                   (4, 'confint.bcdagCE explicitly computes credible, not confidence, intervals.'),
                   (7, 'get_diagnostics uses traces and posterior edge-probability stability; a finite trace diagnostic does not prove convergence.'),
                   (9, 'Edge-inclusion frequencies summarize the sampled posterior; [u,v] denotes u to v.'),
                   (14, 'S/burn/a/U/w are explicit. fast=false is the default; fast=true approximates the proposal ratio. collapse=true omits parameter draws.'),
                   (15, 'Posterior graph/parameter draws, compressed storage and MAP/MPM summaries are distinct outputs.')], [
                       ('exec13_bcdag_description.txt', 'Version, dependencies, declared license and publication date'),
                       ('exec13_bcdag_license.txt', 'MIT template copyright metadata, year 2024; not a dependency license grant'),
                       ('exec13_bcdag_commit.json', 'Eligible mirror commit identity'),
                       ('exec13_bcdag_learn.txt', 'Pinned learn_DAG implementation and argument checks'),
                       ('exec13_bcdag_effect.txt', 'Pinned joint-intervention implementation'),
                       ('exec13_bcdag_interval.txt', 'Pinned quantile interval implementation'),
                       ('exec13_bcdag_tests.txt', 'Source of score-equivalence tests; not run here')]),
        source('exec13_bidag', 'exec13_BiDAG_manual.pdf', 'BiDAG reference manual', 'Polina Suter and Jack Kuipers',
               '2.1.4; release 2023-05-16; manual generated 2026-05-06; mirror 6097d8ea159f5e4dc3c95b6d815d8e827efd5532', [
                   (1, 'BGe/BDe scores, order/partition MCMC, continuous/discrete and dynamic BN scope; GPL >=2; Rcpp and pcalg dependencies.'),
                   (23, 'iterativeMCMC expands a PC-derived search space; retained search-space restriction affects conclusions.'),
                   (24, 'Defaults include alpha .05, softlimit 9, hardlimit 12 and cpdag=false.'),
                   (32, 'learnBN is a wrapper over MCMC MAP searches; plus1 expansion and iterative runs have different computation costs.'),
                   (42, 'Partition sampling has explicit iteration/thinning and search-space controls; graph sampling is conditional on this configuration.')], [
                       ('exec13_BiDAG_description.txt', 'Pinned version, dependencies and declared license'),
                       ('exec13_BiDAG_commit.json', 'Eligible mirror revision; not evidence of maintenance inactivity')]),
        source('exec13_mcmcabn', 'exec13_mcmcabn_mcmc.txt', 'mcmcabn structural MCMC documentation', 'Gilles Kratzer and contributors',
               '0.6; 2023-09-28; mirror ee6a6f0518fc13e06ef58baa074d10a678ca54e5', [
                   ((7, 42), 'Input is an abn score cache; max.parents defaults 1, seed 42, scheme c(100,1000,1000), prior.choice 2.'),
                   ((43, 69), 'Structural MC3/REV/MBR moves, mixed node distributions and prior/heating choices are documented; multiple long chains are advised.'),
                   ((163, 180), 'The example stores the Smoking to LungCancer prior at [LungCancer,Smoking], so package array orientation cannot be assumed from a generic DAG label.')], [
                       ('exec13_mcmcabn_description.txt', 'GPL-3; abn>=3.0.0, coda, gRbase and plotting dependencies; no own compilation'),
                       ('exec13_mcmcabn_query.txt', 'Structural query frequencies, not outcome intervention derivatives'),
                       ('exec13_mcmcabn_vignette.txt', 'Score cache and prior discussion; prose describes rows as parents/columns as children, inconsistent with the named example'),
                       ('exec13_mcmcabn_commit.json', 'Pinned eligible source identity')]),
        source('exec13_dowhy', 'exec13_dowhy_model.txt', 'DoWhy CausalModel and identification source', 'PyWhy contributors',
               'commit b06369ed4a01a54c9d6422a24f103626fbcaec19; 2026-10-04; no release tag inferred from dynamic version placeholder', [
                   ((20, 90), 'CausalModel accepts graph/treatment/outcome and can construct a graph from inputs; the proposed integration must require an explicit reviewed graph.'),
                   ((195, 269), 'learn_graph is deprecated; identify_effect separates ID from AutoIdentifier. The inspected function assigns proceed_when_unidentifiable but does not pass it to the identifier.'),
                   ((271, 327), 'Estimation requires an explicit method and target_units; confidence intervals default false and are method-dependent.')], [
                       ('exec13_dowhy_identifier.txt', 'AutoIdentifier backdoor/IV/frontdoor/general-adjustment source'),
                       ('exec13_dowhy_license.txt', 'MIT license grant with notice retention'),
                       ('exec13_dowhy_project.txt', 'Python/dependency constraints and dynamic version declaration'),
                       ('exec13_dowhy_readme.txt', 'Repository workflow and project identity'),
                       ('exec13_dowhy_commit.json', 'Pinned source revision and date')]),
    ]
    paper = source('exec13_bcdag_paper', 'exec13_bcdag_paper.pdf',
                   'BCDAG: An R package for Bayesian structure and Causal learning of Gaussian DAGs',
                   'Federico Castelletti and Alessandro Mascaro', 'arXiv:2201.12003v1; 2022-01-28', [
                       (1, 'Original preprint identifies the Gaussian structure-and-effect learning problem.'),
                       (2, 'Observational equivalence motivates uncertainty over DAGs and effects.'),
                       (3, 'BiDAG/mcmcabn are related R package leads; historical comparative statements require checking against current manuals.'),
                       (5, 'Independent-observation Gaussian SEM factorization and conjugate prior parameters.'),
                       (6, 'Compatible DAG-Wishart hyperparameters give equal marginal likelihoods to Markov-equivalent DAGs.'),
                       (9, 'Skeleton prior, hard interventions and total joint-effect definition.'),
                       (10, 'Intervention effect calculation and MCMC target. Interpret intervention equations with fixed intervention coordinates, not random variation in the assigned coordinates.')])
    title = 'BCDAG An R package for Bayesian structure and Causal learning of Gaussian DAGs'
    name = f'docs/papers/{title} Castelletti(2022).pdf'
    assert (ROOT / name).read_bytes() == (ROOT / RAW / 'exec13_bcdag_paper.pdf').read_bytes()
    paper.update(kind='paper', local_path=name, sha256=digest((ROOT / name).read_bytes()),
                 filename_title=title, first_author='Castelletti', year=2022)
    paper['limits'] = '2022 preprint, not the later JSS publication. Historical package-comparison claims are superseded by the inspected current manuals. Its cited references are discovery leads, not separately inspected originals.'
    sources.append(paper)
    sources.append({'integrated_citation_key': 'exec13_examples', 'kind': 'project_derivation',
                    'title': 'Exact examples of graph, target and unit preservation', 'author': 'Causal banking research project',
                    'source_identity': 'Project-authored exact rational calculations', 'version_date': '2026-10-13',
                    'local_copy': ref('tools/proposal_contract_examples_20261013.py', 'Derivation and reproducible arithmetic'),
                    'inspected_anchors': [{'anchor': 'calculate; implied_covariance', 'finding': 'Three equal Gaussian covariance laws give effects {0,.48}; named target law gives ATE2, ATT2.6, ATC1.4, naive4.4.'}],
                    'supported_claims': ['Exact algebraic examples only; no package performance, live model or bank validation claim'],
                    'results': ref(BASE + '/exact-examples.json', 'Executed exact calculations')})
    audit = {'cutoff': '2026-10-07', 'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
             'status': 'inspected_primary_sources_with_explicit_limits', 'sources': sources,
             'source_count': len(sources), 'not_independent_review': True,
             'maintenance_limit': 'Versions, publication dates, commit histories and declared dependencies were inspected; no issue-resolution rate, support SLA or future support is inferred.',
             'failures': [ref(RAW + f, 'Retained acquisition failure') for f in [
                 'exec13_mcmcabn_manual.receipt.json', 'exec13_mcmcabn_readme.receipt.json']]}
    write(BASE + '/source-audit.json', audit)
    prior = json.loads((ROOT / 'docs/program/comprehensive-v14/work/SW.CELL.discovery_iid.R/coverage-review.json').read_text())
    discovery = json.loads((ROOT / RAW / 'v12_sw_cell_discovery_iid_r.json').read_text())
    leads = []
    for result in discovery['results']:
        title0 = result['display_name']
        leads.append({'id': result['id'], 'title': title0, 'publication_date': result['publication_date'],
                      'disposition': ('BCDAG primary package/manual/source/preprint inspected; canonical aliases resolved.'
                                      if 'BCDAG' in title0 else
                                      'Retained methodology/literature lead. Metadata identifies this work only; implementation language, package identity and technical merit are unresolved here. Route to discovery literature synthesis; no absence claim.')})
    packages = [
        {'name': 'pcalg', 'aliases': ['PC/PC-stable', 'FCI/RFCI', 'GIES', 'IDA'],
         'category': 'Constraint/equivalence/effect-set toolkit; aliases here are algorithms, not separate packages',
         'returned_object': 'CPDAG/PAG as appropriate; IDA multiset under its model',
         'candidate_use': 'Propose a narrow R discovery/IDA adapter; keep latent and interventional methods in their own cells',
         'conditions': 'Pin test and alpha; wrapper aborts on missing CI tests; preserve orientation conflicts and equivalence; no financial effect from PC alone'},
        {'name': 'bnlearn', 'aliases': ['hc', 'tabu', 'mmhc', 'h2pc', 'DirectLiNGAM'],
         'category': 'One package exposing constraint, score, hybrid and functional routes',
         'returned_object': 'BN/partially directed structure; parameters and causal queries are separate operations',
         'candidate_use': 'Alternative R baseline across supported data types; do not port all algorithms',
         'conditions': 'Make defaults/restarts/caps/missing-data subsets explicit; distinguish assumed causal BN from discovered identification; LiNGAM functional assumptions differ'},
        {'name': 'BCDAG', 'aliases': ['BCDAG', 'learn_DAG'],
         'category': 'Bayesian Gaussian observational DAG and joint-effect posterior',
         'returned_object': 'Graph/parameter draws, edge probabilities, MAP/MPM summaries, effect draws and credible intervals',
         'candidate_use': 'Optional Bayesian sensitivity comparator',
         'conditions': 'Record graph/parameter priors, S/burn/seeds/chains; fast=false baseline; reject silent posterior-to-confidence relabeling; review parameter validation and parm-specific interval source before use'},
        {'name': 'BiDAG', 'aliases': ['learnBN', 'orderMCMC', 'partitionMCMC', 'iterativeMCMC'],
         'category': 'Bayesian structure-search/sampling family; pcalg is a dependency, not an alias',
         'returned_object': 'MAP or sampled DAGs under declared score, search space and sampling configuration',
         'candidate_use': 'Reference and optional structure sensitivity comparator',
         'conditions': 'Retain score, search-space mask, parent limits, plus1 expansion and diagnostics; do not transfer Gaussian/discrete structure results to longitudinal causal claims'},
        {'name': 'mcmcabn', 'aliases': ['mcmcabn()', 'structural MC3/REV/MBR'],
         'category': 'Score-cache structural sampler; abn is a scoring dependency, not a duplicate sampler',
         'returned_object': 'Sampled DAGs and structural query frequencies',
         'candidate_use': 'Defer adapter; retain mixed-distribution and explicit-prior alternative in the comparison',
         'conditions': 'Resolve documented matrix-orientation conflict using named-node source/runtime oracle; freeze abn score cache and priors; do not convert structural frequency to an intervention effect'},
    ]
    omissions = [
        {'item': 'Complete R family census and continuous-optimization implementations', 'reason': 'First-page ten-result search plus one package-reference hop is bounded; it cannot establish completeness or absence.', 'next_action': 'Run the separate S2 literature/depth review, page further results and identify source-backed continuous-optimization R candidates before a family-completeness claim.'},
        {'item': 'Methodology leads other than BCDAG in saved response', 'reason': 'Identities retained individually; primary papers/code are outside this bounded source inspection.', 'next_action': 'Resolve in S2 with real PDFs and language-specific code; not an essential source for the five compared package claims.'},
        {'item': 'Later BCDAG JSS edition and BiDAG/mcmcabn method papers', 'reason': 'Known from package references; not independently acquired/inspected here. Only the authentic 2022 BCDAG original and package technical docs support the present comparison.', 'next_action': 'Acquire final scholarly editions before citing their changed results; do not reuse historical package-absence claims.'},
        {'item': 'mcmcabn current CRAN manual and README', 'reason': 'Both registered URLs returned HTTP404. Pinned Rd/vignette/DESCRIPTION fallback is available.', 'next_action': 'Use the eligible pinned primary text; reassess distribution availability during a reuse decision.'},
        {'item': 'abn and transitive dependency census', 'reason': 'Identified dependency lead, not fully reviewed as another discovery package in this one-hop boundary.', 'next_action': 'Pin and audit abn score semantics/licensing before selecting a mcmcabn integration.'},
        {'item': 'Numerical/package qualification', 'reason': 'No R engines or downloaded code were executed in this task.', 'next_action': 'Separate prospective adapter/benchmark task with exact version, oracle, resources and retained failures.'},
    ]
    review = {'operation_id': 'SW.CELL.discovery_iid.R', 'status': 'completed_bounded_source_review',
              'cutoff': '2026-10-07', 'scope': 'Five identified R package paths; not an exhaustive R census, S2 depth acceptance or numerical qualification',
              'sources': ref(BASE + '/source-audit.json', 'Primary bytes/version/anchors and claim limits'),
              'preserved_checkpoint': ref('docs/program/comprehensive-v14/work/SW.CELL.discovery_iid.R/coverage-review.json', 'Untouched partial predecessor'),
              'search': copy.deepcopy(prior['search']), 'candidate_dispositions': leads, 'packages': packages,
              'stopping_rule': 'Inspect the two inherited R seeds, all ten saved first-page metadata identities, BCDAG primary evidence, and its two explicitly named R package alternatives. Stop after that one package-reference hop. Log second-hop/methodology leads; do not infer complete coverage or unsupported absence.',
              'corrections': ['bnlearn manual/package date is 2026-07-17, not July18 in the predecessor note.', 'Current bnlearn causal-query support supersedes the 2022 BCDAG preprint package-absence comparison.', 'mcmcabn matrix orientation is unresolved because named examples and prose conflict.'],
              'nonidentification_example': ref(BASE + '/exact-examples.json', 'Same Gaussian law, effect set {0,.48}, and unit conversion'),
              'omissions': omissions, 'runtime_execution': False, 'integration_capabilities_granted': [],
              'essential_source_waiver': False,
              'review_findings': ['Five package identities and algorithm aliases resolved within the declared search boundary.', 'Primary source bytes support every package comparison; no claim relies on OpenAlex metadata alone.', 'A documented result type or score is not a causal identification or confidence guarantee.', 'License/maintenance observations are source evidence, not a distribution approval or support prediction.']}
    write('docs/program/comprehensive-v14/work/SW.CELL.discovery_iid.R/coverage-review-final.json', review)
    write(BASE + '/omissions-register.json', {'operation': review['operation_id'], 'entries': omissions,
                                           'acquisition_failures': audit['failures']})
    print(json.dumps({'sources': len(sources), 'packages': len(packages), 'metadata_candidates': len(leads),
                      'output': 'coverage-review-final.json', 'runtime_execution': False}))


if __name__ == '__main__':
    main()
