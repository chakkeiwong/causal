#!/usr/bin/env python3
"""Save the author's completed primary-text review; never award whole Q2."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/traceability'
INDEX = ROOT / 'docs/program/execution/2026-10-13/identification-review/traceability-review.json'

# These are the passages actually inspected in this continuation, not generated
# verdicts based on the presence of an audit field or a package name.
REVIEWS = {
    'sw_linearmodels': ('raw_readme_linearmodels.md', [[11, 38], [121, 139]],
        'The reader correctly distinguishes linear panel, IV and system baselines from pydynpd dynamic GMM. The primary roadmap explicitly leaves panel IV and dynamic panel models unstarted; the collective list must not be read as panel-IV support.'),
    'sw_pyfixest': ('raw_readme_pyfixest.md', [[28, 42], [72, 88]],
        'FE/IV/GLM and multiple DiD families are documented. Reader restrictions on estimand, demeaning backend and non-transferrable speed claims are appropriate; no package execution is asserted.'),
    'sw_fixest': ('raw_readme_fixest.md', [[10, 35], [47, 80]],
        'Unified regression/IV/GLM, fixed effects and inference declarations support the narrow package comparison. The example itself records missing observations and removed singletons; formula fit is not proof of causal restrictions.'),
    'sw_pydynpd': ('raw_readme_pydynpd.md', [[5, 27], [36, 67]],
        'Difference/system GMM, transformations, corrected standard errors, diagnostics and lag/collapse options are documented. Reader does not promote lag search or a nonrejected diagnostic to valid instruments.'),
    'sw_did': ('r3g_api_did.txt', [[1, 145]],
        'First-treatment cohort, panel-specific sampling weights, anchor-period dropping, one additional coarser cluster, bootstrap bands and compute_inffunc=False consequences agree exactly with the inspected att_gt documentation.'),
    'sw_synthdid': ('raw_readme_synthdid.md', [[5, 15], [33, 43]],
        'Simultaneous adoption and block layout are explicit; reader does not offer this documented interface as direct staggered-adoption support.'),
    'sw_gsynth': ('raw_readme_gsynth.md', [[14, 27], [53, 76]],
        'Interactive fixed-effect imputation and the current fect wrapper/backward-compatibility notice are both present. Reader requires separate qualification of that dependency.'),
    'sw_honestdid': ('raw_readme_honestdid.md', [[4, 56]],
        'Relative-magnitude and smoothness restriction classes support a sensitivity comparator. Reader retains the selected violation class as an assumption, not a discovered true trend.'),
    'sw_causalimpact': ('readme_causalimpact.md', [[8, 31]],
        'Primary text explicitly requires unaffected control series and a stable post-intervention relationship. Reader carries those assumptions and does not equate predictive fit with causal validation.'),
    'sw_causalpy': ('readme_causalpy.md', [[23, 31]],
        'Distinct quasi-experimental designs and Bayesian/OLS alternatives are explicit. Reader limits the comparison to their targets and assumptions, without a local runtime or coverage claim.'),
    'sw_dynamax': ('r3g_api_dynamax.txt', [[524, 559], [575, 650]],
        'HMM law and inference code contain initial, transition and emission factors; the standard transition law can ignore inputs. The absence of an automatic private action logger and the distinction between filtering and smoothing are correctly stated.'),
    'sw_pymc': ('raw_readme_pymc.txt', [[8, 29], [70, 111]],
        'MCMC/VI capabilities and the do-versus-observe example support numerical/model-transformation claims only. Reader explicitly requires separate causal semantics and identification.'),
    'sw_numpyro': ('raw_readme_numpyro.md', [[25, 34], [97, 105]],
        'Primary README explicitly supports HMC/NUTS, MixedHMC and discrete variational inference. Reader correctly avoids claiming that marginalization is the only route for discrete variables and separates numerical from causal uncertainty.'),
    'sw_pomdp_py': ('readme_pomdp_py_rst.txt', [[1, 22]],
        'Python/Cython framework to build and solve supplied POMDPs supports the modeling/planning role. No causal parameter identification or online validity of smoothed beliefs is attributed to the package.'),
    'sw_pomdps': ('raw_readme_pomdps.md', [[12, 38], [60, 89], [102, 114]],
        'Core interface, tools, solvers and Python bridges are separate. Reader correctly requires versioning and transition/observation/reward conventions instead of treating the interface as all solver implementations.'),
    'sw_d3rlpy': ('readme_d3rlpy.md', [[14, 35], [88, 91], [119, 122]],
        'Offline/online policy fitting and v2 breaking changes support the policy-learning comparator. Reader does not infer policy-value inference, state sufficiency or bank performance from training APIs.'),
    'sw_scope_rl': ('raw_readme_scope_rl.md', [[44, 58], [69, 113], [131, 150]],
        'Sequential offline RL, trajectory and marginal estimators, CDF evaluation and interval routines are documented. Reader distinguishes return targets and does not infer valid coverage under hidden logging from a routine name.'),
    'sw_obp': ('raw_readme_obp.md', [[67, 83], [91, 118]],
        'Logged contextual-bandit data, policy and OPE modules support the one-period comparator. Reader correctly refuses to substitute that reward for a multimonth path with carryover.'),
    'sw_duckdb': ('raw_readme_duckdb.md', [[18, 41]],
        'SQL, windows, nested types and multiple clients support the proposed relational path. Both cited reader contexts keep event/availability/revision semantics as product obligations.'),
    'sw_polars': ('raw_readme_polars.md', [[45, 60], [66, 95]],
        'Columnar execution, streaming and optional GPU support are documented. All three reader contexts preserve scientific partitions and information clocks; no measured bank-scale speed is inferred.'),
    'sw_pandera': ('raw_readme_pandera.md', [[34, 42], [88, 124], [132, 147]],
        'Multiple dataframe engines, schemas and user-defined value checks support the data-contract role. Both reader contexts state that passing such checks does not establish correct decision history or causal identification.'),
    'sw_feast': ('api_feast.txt', [[1988, 2065]],
        'Historical retrieval defaults filter_by_created_timestamp to False; enabling it affects only views with created_timestamp_column. Reader accurately distinguishes this documented capability from a guaranteed match to the bank information clock.'),
    'sw_datahub': ('raw_readme_datahub.md', [[44, 60]],
        'OSS metadata graph, lineage, governance and discovery are explicitly distinguished from managed-cloud context/agent features. Reader presents catalog reuse, not a deployed commercial capability or a causal graph.'),
    'sw_openmetadata': ('raw_readme_openmetadata.md', [[9, 11], [85, 111]],
        'Metadata/ownership/glossary/lineage relationships support the catalog role. The reader correctly distinguishes computed-data lineage from a causal intervention graph in both contexts.'),
    'sw_openlineage': ('raw_readme_openlineage.md', [[12, 15], [35, 48]],
        'Run/job/dataset entities and custom facets are explicit. Reader marks target, graph, split and estimator facets as proposed causal extensions, not an already standardized semantics.'),
    'sw_splink': ('raw_readme_splink.md', [[14, 50]],
        'Fellegi-Sunter linkage, pair probabilities and estimated clusters are documented with correlated-field limitations. Reader retains linkage uncertainty and the decision clock rather than treating a hard entity ID as known truth.'),
    'sw_ray': ('raw_readme_ray.txt', [[18, 45]],
        'Tasks, actors and immutable objects support the proposed scheduling role. Both reader contexts keep cluster/time assumptions, profiling and duplicate-contribution prevention outside that runtime capability.'),
}


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'anchor': anchor}


def main():
    prior_path = BASE / 'semantic-review-07.json'
    prior = json.loads(prior_path.read_text())
    index = json.loads(INDEX.read_text())
    state = json.loads((ROOT / 'docs/program/state.json').read_text())
    reader = prior['reader']
    assert hashlib.sha256((ROOT / reader['path']).read_bytes()).hexdigest() == reader['sha256']
    assert index['pdf']['sha256'] == reader['sha256']
    indexed = {r['citation_key']: r for r in index['records']}
    records = []
    for key, (name, ranges, finding) in REVIEWS.items():
        assert key in prior['remaining_source_keys']
        entry = indexed[key]
        for copy in entry['local_copies']:
            assert hashlib.sha256((ROOT / copy['path']).read_bytes()).hexdigest() == copy['sha256']
        primary = ROOT / 'docs/literature/raw' / name
        lines = primary.read_text().splitlines()
        assert all(1 <= a <= b <= len(lines) for a, b in ranges)
        records.append({'citation_key': key, 'verdict': 'pass_in_stated_scope',
                        'finding': finding,
                        'primary_sources': [dict(ref(primary, 'Inspected primary technical text'),
                                                 inspected_line_ranges=ranges)],
                        'source_audit_copies': entry['local_copies'],
                        'contexts_reviewed': entry['citation_contexts'],
                        'limits': 'Author source/claim review of the saved documentation snapshot. No new package execution, institutional acceptance or claim beyond the cited reader contexts.'})
    reviewed = sorted(set(prior['reviewed_source_key_list']) | set(REVIEWS))
    remaining = sorted(set(indexed) - set(reviewed))
    next_action = ('Review remaining foundational and panel/state-space/OPE scholarly claims against the exact 626-page reader, then remaining LLM, software, commercial and public-data source contexts. Resume from semantic-review-08.json; no source/claim acceptance for unreviewed keys.')
    result = {'status': 'partial_semantic_review_not_Q2_acceptance',
              'reviewer': {'name': 'Codex author/coordinator', 'kind': 'author'},
              'reader': reader, 'structural_review': ref(INDEX, 'Exact current reader source/context index'),
              'prior_review': ref(prior_path, 'Ninety completed source reviews, same unchanged reader'),
              'prior_review_continuity': 'Same exact reader hash; predecessor source/context reviews retained without duplicating their text.',
              'review_procedure': ref(Path(__file__).resolve(), 'Explicit author findings and inspected primary line ranges'),
              'records': records, 'cumulative_reviewed_source_keys': len(reviewed),
              'reviewed_source_key_list': reviewed, 'remaining_source_keys': remaining,
              'next_action': next_action, 'proposal_q2_acceptance': False}
    output = BASE / 'semantic-review-08.json'
    with output.open('x') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write('\n')
    checkpoint = {'finding': f'Reviewed {len(records)} additional inherited panel, state-space, OPE and data-engine software source contexts against primary text. {len(reviewed)}/{len(indexed)} current-reader source keys reviewed; {len(remaining)} remain. No new package execution or whole Q2 acceptance.',
                  'next_action': next_action,
                  'evidence': [ref(output, 'Twenty-seven new source/context dispositions and cumulative exact-reader coverage')]}
    with (BASE / 'checkpoint-07.json').open('x') as f:
        json.dump(checkpoint, f, indent=2)
        f.write('\n')
    print(json.dumps({'reviewed_now': len(records), 'cumulative': len(reviewed),
                      'remaining': len(remaining), 'whole_q2_accepted': False}))


if __name__ == '__main__':
    main()
