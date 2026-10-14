#!/usr/bin/env python3
"""Record scoped, manually inspected dependency paths; never execute vendor code."""
import copy
import json
from pathlib import Path

import master_control as core
import build_integrated_monograph_v12 as book

ROOT = core.ROOT
BASE = ROOT / 'docs/program/gap-execution-v13_1'
OUT = BASE / 'work/SW01'
PRIOR = ROOT / 'docs/program/gap-repair-v13/work/SW01'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': core.sha(path), 'anchor': anchor}


# These ranges were read as primary text. Claims are deliberately narrower than
# package coverage, statistical correctness or runtime qualification.
SPECS = [
    ('y0', ['id:43-160,431-444', 'idc:15-43', 'graph:65-151,652-655',
            'utils:176-226', 'rule2:19-56'],
     ['ID recursively restricts ancestors, augments interventions and decomposes districts; the connected-district failure raises Unidentifiable, while invariant failures raise RuntimeError.',
      'IDC tests a rule-2 exchange, recurses after exchanging observation/action, then identifies the unconditioned query and normalizes. The rule-2 helper delegates separation to another module.',
      'The inspected graph constructor and edge insertion methods do not enforce acyclicity; these paths alone are not a complete input validator.'],
     ['identification_counterfactual::Python'],
     'Integrate a symbolic operation after explicit DAG/mixed-edge/query validation and a reference suite; preserve nonidentification separately from malformed input and execution error.',
     'Inspect separation, graph mutilation and expression normalization; compare adjustment, front-door and hedge examples against independent symbolic references. No recursive-correctness or full counterfactual claim.'),
    ('lingam', ['base:51-91,123-166', 'bootstrap:36-61', 'var:67-114,132-195,314-366'],
     ['Adjacency is stored as B[target,predictor]; permitted earlier variables are fit by adaptive Lasso or ordinary regression. estimate_total_effect uses source plus its estimated parents, warns on reversed causal order and still returns a regression coefficient.',
      'The generic bootstrap resamples rows and refits; VARLiNGAM fits a lag model, applies DirectLiNGAM to residuals and has a separate residual-resampling path that reconstructs a sequence.',
      'The VAR bootstrap sets the criterion to None during its loop, so lag-selection uncertainty must not be inferred from the existence of this bootstrap.'],
     ['discovery_iid::Python', 'discovery_temporal_interventional::Python'],
     'Integrate distinct IID and VAR operations with explicit matrix orientation and sampling-law metadata; defer porting and graph-confidence claims.',
     'Inspect adaptive-Lasso and total-path helpers, lag selection and residual-law assumptions; execute Gaussian/latent/persistent-residual adverse cases only under a registered qualification design.'),
    ('delicatessen', ['estimation:614-655,690-765,809-851', 'sandwich:173-222,225-289'],
     ['MEstimator solves stacked equations, differentiates their sum, scales bread and meat by the number of supplied contribution columns, and scales the sandwich once more for estimator variance.',
      'compute_meat forms the outer-product sum of supplied columns. It does not add lag products or infer borrower/calendar clusters from data labels.',
      'The default permits a pseudoinverse; solver convergence and a finite sandwich do not establish identification or weak-rank coverage.'],
     ['effects_heterogeneity::Python', 'iv_rd_design::Python'],
     'Integrate a contribution-level interface with explicit independent unit, residual/Jacobian diagnostics and covariance method; retain score inversion as a separate scientific operation.',
     'Compare derivatives against analytic small models, validate independently sampled group aggregation, and derive actual dependence correction before using on persistent calendars.'),
    ('pygformula', ['bootstrap:189-222,241-265,316-323', 'simulate:390-403,453-480',
                   'interventions:35-98,242-318'],
     ['Bootstrap draws subject identifiers with replacement, copies complete histories, assigns new replicate IDs and refits component models; n_simul expansion is a separate resampling step.',
      'Simulation applies interventions and updates histories before outcome prediction; static schedules use the absolute index int_values[t], while threshold rules bound the contemporaneous variable.',
      'Bootstrap exceptions return boot_results=None. The previously inspected caller filters those from boot_results but indexes every original boot_results entry when constructing bootests; a None entry implies a static inconsistency that needs runtime reproduction.'],
     ['longitudinal_survival::Python', 'policies_offpolicy::Python'],
     'Integrate only after clock, history, competing-event and failure-accounting conformance checks; carry failed bootstrap attempts in the denominator.',
     'Reproduce the None-result path in an isolated qualified environment; inspect histories/model fits/output interval routines. Independent subjects do not establish validity under shared calendar shocks.'),
    ('statsmodels', ['gmm:582-646,1039-1090,1212-1293'],
     ['The GMM covariance path defaults to weights_method=cov, an outer-product covariance divided by n; HAC is a separate explicit path requiring maxlag and using a supplied kernel or Bartlett default.',
      'GMMResults obtains the covariance method from fit options and recomputes moment covariance. Preliminary outcome _cov_type settings in TreatmentEffect do not select this final path.',
      'The inspected covariance code centers with moms.mean() rather than a per-column mean; sensitivity to nonzero moment residuals remains a qualification question.'],
     ['effects_heterogeneity::Python', 'computation_workflow::Python'],
     'Integrate only with separately recorded preliminary and final covariance settings; a supported low-level HAC path does not imply the treatment-effect wrapper exposes it.',
     'Trace each estimator call and all options, validate analytic moments and time ordering, then compare covariance and rank diagnostics. Do not infer cluster support or calibration from a generic robust label.'),
    ('grf', ['average:130-168,201-256,267-293,346-366', 'scores:45-101',
             'binding_body:49-104,108-128', 'predictors:34-39', 'instrumental_native:45-63,83-149'],
     ['The R all-sample AIPW path averages get_scores output and sums centered weighted scores within clusters for variance. Early guards reject clustered or sample-weighted TMLE despite later code containing cluster formulas.',
      'Continuous-treatment scores estimate conditional treatment variance with another regression forest and divide treatment residuals by it; zero/near-zero variance needs explicit handling and qualification.',
      'Causal bindings set the instrument index equal to treatment and call instrumental_predictor, which constructs InstrumentalPredictionStrategy. Its point output is a moment ratio, and native variance uses tree groups plus a Bayes debiaser.',
      'The initially fetched src binding is a symlink target string; implementation claims use the separately fetched target body and factory, not that string.'],
     ['effects_heterogeneity::R'],
     'Integrate the maintained R interface first; defer a direct C++ port until ABI, serialization, dependency/license and behavioral review. Preserve target population and unsupported option combinations.',
     'Inspect the Bayes debiaser, serialization, forest sample construction and numerical guards; compare all/treated/control/overlap and continuous-slope targets separately. Tree groups are not bank calendar clusters.'),
    ('causalgps', ['density:16-20', 'resid:16-22'],
     ['compute_resid returns (a-b)/c. compute_density uses stats::density and linear interpolation with rule=2.',
      'The inspected kernel estimate_gps path evaluates density at standardized residuals and stores that value without a division by its scale in that path. A conditional density on the original exposure scale would require the Jacobian 1/scale under a location-scale model.'],
     ['effects_heterogeneity::R'],
     'Defer causal density/weight adoption until scale semantics and downstream uses are traced; keep the package as a comparison candidate. Do not silently patch a vendor routine.',
     'Trace matching/weighting and counterfactual-dose prediction, inspect scale positivity, and reproduce heterogeneous-scale and dose-unit changes. The observed path alone does not establish all package outputs are wrong.'),
    ('causaldrf', ['license:1-2'],
     ['The supplementary LICENSE file names year 2015 and Douglas Galagate; it supplements the previously inspected DESCRIPTION license declaration. It is not a full dependency or redistribution review.'],
     ['effects_heterogeneity::R'],
     'Retain the provisional comparison/reference decision pending function and interval review; the missing accompanying notice has now been acquired.',
     'Inspect full hi_est body and interval procedures, then resolve all dependency/distribution terms before an integration or port decision.'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT/'source-audit.json').exists():
        raise ValueError('Preserve an existing audit; create a versioned successor')
    prior = json.loads((PRIOR/'source-audit.json').read_text())
    identity = {x['name']: x for x in json.loads((ROOT/'docs/program/gap-repair-v13/source-identities.json').read_text())}
    inherited = {x['name'].lower(): x for x in prior['new_entries']}
    entries = []
    for name, paths, claims, cells, decision, remaining in SPECS:
        parent = inherited[name]
        files, anchors = [], []
        for spec in paths:
            slug, ranges = spec.split(':')
            path = ROOT/f'docs/literature/raw/v12_gap4_{name}_{slug}.txt'
            receipt = path.with_suffix('.receipt.json')
            fetched = json.loads(receipt.read_text())
            assert fetched['status'] == 'saved' and fetched['sha256'] == core.sha(path)
            for part in ranges.split(','):
                lo, hi = map(int, part.split('-'))
                assert 1 <= lo <= hi <= len(path.read_text().splitlines()), (name, spec)
                anchors.append(ref(path, f'Inspected lines {lo}-{hi}'))
            files.append({'source_identity': fetched['url'], 'local_copy': ref(path, 'Pinned source bytes'),
                          'acquisition': ref(receipt, 'Collector provenance')})
        entries.append({'id': f'v131:{name}', 'citation_key': f'v131_sw_{name}',
            'integrated_citation_key': f'v131_sw_{name}', 'kind': 'software_source', 'name': parent['name'],
            'candidate_id': parent['candidate_id'], 'source_identity': files[0]['source_identity'],
            'version_date': {'commit': identity[name]['commit'], 'commit_date': identity[name]['date'],
                             'retrieved': '2026-10-12'}, 'identity_evidence': parent['identity_evidence'],
            'local_copy': files[0]['local_copy'], 'technical_files': files, 'inspected_anchors': anchors,
            'inherited_review': ref(PRIOR/'source-audit.json', parent['id']),
            'supported_claims': claims, 'license': parent['license'], 'coverage_cells': cells,
            'decision': {'status': 'provisional_not_SW07_acceptance', 'recommendation': decision,
                         'revisit_trigger': remaining, 'alternative': parent['decision']['alternative']},
            'limits': [remaining, 'Selected source inspection only; no downloaded package executed or qualified.'],
            'runtime_status': 'not_executed', 'reviewer': 'Current author; not independent acceptance'})
    audit = {'status': 'scoped_dependency_reviews', 'cutoff': '2026-10-07',
             'predecessor': ref(PRIOR/'source-audit.json', 'Preserved selected entry-point reviews'),
             'new_entries': entries, 'claim_kind': 'primary-source inspection and explicit project implications'}
    book.verify_refs(audit)
    core.write(OUT/'source-audit.json', audit)
    coverage = copy.deepcopy(json.loads((PRIOR/'coverage-matrix.json').read_text()))
    coverage['predecessor'] = ref(PRIOR/'coverage-matrix.json', 'All 102 prior cells preserved')
    for cell in coverage['cells']:
        additions = [e for e in entries if cell['id'] in e['coverage_cells']]
        if not additions:
            continue
        cell['dependency_inspections'] = [e['id'] for e in additions]
        cell['dependency_finding'] = ' '.join(c for e in additions for c in e['supported_claims'])
        cell['dependency_remaining'] = ' '.join(e['decision']['revisit_trigger'] for e in additions)
        cell['closure_qualified'] = False
        if cell['status'] != 'partial_primary_inspection':
            cell['status'] = 'partial_primary_inspection'
            cell['individual_review'] = {'date': '2026-10-12', 'reviewer': 'Current author',
                'finding': 'Selected VARLiNGAM source and residual-bootstrap paths inspected.',
                'remaining': 'Other temporal/interventional families and complete cell searches remain open.',
                'evidence_register': str((OUT/'source-audit.json').relative_to(ROOT))}
    partial = sum(c['status'] == 'partial_primary_inspection' for c in coverage['cells'])
    coverage['individually_partially_reviewed_cells'] = partial
    coverage['remaining_individual_review_cells'] = len(coverage['cells']) - partial
    coverage['qualified_cell_count'] = 0
    core.write(OUT/'coverage-matrix.json', coverage)
    core.write(OUT/'catalog-delta.json', {'predecessor': ref(PRIOR/'catalog.json', '115 prior rows, including aliases/leads'),
        'new_distinct_candidates': 0, 'revised_scoped_dossiers': [e['candidate_id'] for e in entries],
        'audit': ref(OUT/'source-audit.json', 'Versioned deeper evidence, no adoption acceptance')})
    lines = ['# Dependency-path source review', '', 'These are scoped inspections, not package qualification or complete cell reviews.', '']
    for e in entries:
        lines += ['## '+e['name'], '', *['- '+c for c in e['supported_claims']], '',
                  'Reuse disposition: '+e['decision']['recommendation'], '',
                  'Next evidence: '+e['decision']['revisit_trigger'], '']
    (OUT/'dossiers.md').write_text('\n'.join(lines))
    print(json.dumps({'dossiers': len(entries), 'partial_cells': partial, 'unreviewed_cells': 102-partial,
                      'closed_cells': 0, 'runtime_tests': 0}))


if __name__ == '__main__':
    main()
