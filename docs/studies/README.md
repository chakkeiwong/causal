# V10: precision grid and complete streaming pilot

The current `precision-streaming-spec.json` freezes eight synthetic designs,
three procedures and 2,000 fresh requests per design. Its original reporting
specification remains unchanged; the later conservative exact-binomial
reporting is identified in the [author review](../reviews/precision-streaming-author-review.md).

| Evidence | Replay command with `python3` | Saved result |
|---|---|---|
| Independent numerical comparisons and refusals | `tools/precision_checks.py` | `../reviews/precision-streaming-checks.json` |
| 24 separate pilot requests | `tools/precision_study.py --pilot` | `precision-pilot-results.json` |
| 16,000 fresh final requests | `tools/precision_study.py` | `precision-final-results.json` |
| Eight complete dense/streaming worker runs | `tools/precision_workload_launcher.py` | `precision-workloads-results.json` |
| Conservative Monte Carlo reporting | `tools/precision_interval_review.py` | `../reviews/precision-interval-review.json` |
| Generated chapter tables | `tools/precision_tables.py` | `../derivations/precision_tables.tex` |
| Current primary-source roles and preserved V9 review | `tools/precision_source_trace.py` | `../literature/precision-source-review.json` |

Read-only final checks are `python3 tools/precision_delivery.py check` and
`python3 tools/delivery_manifest.py verify`. The reconstruction commands
`python3 tools/precision_exact_replay.py` and `python3 tools/precision_verify.py`
write current receipts; they must precede rebuilding/reviewing a new delivery.
The verifier reconstructs saved requests and binds unchanged inherited claim
artifacts to the verified V9 archive. It does not rerun every simulation.
Preserve the journal header, seeds, failures and original input identities when
resuming an unchanged study. A new procedure or scientific input requires a
new registered experiment, not updated hashes on old results.

Small-audit undercoverage, near-rank unavailability and false-exogeneity failure
remain. Streaming reduces selected large-case local memory without a consistent
time advantage; doubling pilot history has no demonstrated coverage benefit.
The [gap register](../program/deferred-gaps-2026-10-10.md) and preserved external
protocol give exact scientific and institutional continuation requirements.

# Preserved V9: calibration attribution, fresh follow-up and complete execution

The V9 program uses `calibration-repair-spec.json` and the separately
registered `calibration-followup-spec.json`. All known-truth laws are synthetic.
The [author review](../reviews/calibration-author-review.md) retains failed
calibration and absent clear paired superiority. Read-only delivery verification:
`python3 tools/delivery_manifest.py verify`.

| Study | Command with `.venv-scope/bin/python` | Retained result |
|---|---|---|
| 1,000 paired pilot/nuisance/covariance/audit diagnostic requests | `tools/calibration_study.py diagnostics` | `calibration-diagnostics-results.json` |
| 4,200 requests across seven fixed-regression laws | `tools/calibration_study.py validation` | `calibration-validation-results.json` |
| 1,800 fresh growing-pilot requests | `tools/calibration_followup.py` | `calibration-followup-results.json` |
| Eight original complete requests, inherited-RSS contamination retained | `tools/calibration_workloads.py` | `calibration-workloads-results.json` |
| Eight corrected requests with small launcher, unchanged data/worker | `tools/calibration_workload_remeasure.py` | `calibration-workload-remeasurement-results.json` |

The three statistical commands support `--pilot`, with 16/56/24 separate pilot
requests. Journals bind code and specifications and preserve every contribution.
Resume unchanged commands after interruption. Changed scientific inputs require
preservation and a fresh registered experiment, never relabeling old hashes.
The corrected workload output IDs are 100/101; do not use the original equal
RSS ratios as memory evidence. Workload outputs, immutable inputs, timing and
thread records are retained in `calibration-workload-runs/`.

Current checks and saved-evidence reconstruction (these write receipts):

```bash
.venv-scope/bin/python tools/calibration_checks.py
.venv-scope/bin/python tools/calibration_followup_checks.py
.venv-scope/bin/python tools/calibration_rehearsal.py
.venv-scope/bin/python tools/calibration_tables.py
.venv-scope/bin/python tools/calibration_source_trace.py
.venv-scope/bin/python tools/calibration_exact_replay.py
.venv-scope/bin/python tools/calibration_verify.py
```

The verifier reconstructs 7,016 final journal requests and 96 pilots, including
paired method arms and repeated workloads, not 7,016 independent method trials.
It binds unchanged inherited scientific evidence against preserved V8. Old
verification/source receipts remain historical; do not regenerate them against
new manuscripts. The whole-request recovery rehearsal is
`tools/calibration_workloads.py --rehearsal`; it does not test partial-fit or
distributed recovery. Joint QR has bounded working state, whereas growing-pilot
fitting still stores arrays. Independent histories, acquisition costs and all
external acceptance remain obligations in the
[V9 delta](../program/external-validation-v9.md).

# Preserved V8: reliability extension and selected follow-up

The V8 studies execute `reliability-spec.json` and the separately
registered `reliability-followup-spec.json`. All known-truth populations are
synthetic. The [author review](../reviews/reliability-author-review.md) explains
the constructions and retained negative results. For read-only verification
of the delivered files, use `python3 tools/delivery_manifest.py verify`.

| Study | Replay command with `.venv-scope/bin/python` | Result file in this directory |
|---|---|---|
| Persistent pairs, common calendar, audit allocation and label truth | `tools/reliability_joint_study.py` | `reliability-joint-results.json` |
| Funding covariance, information-size and reference diagnostics | `tools/reliability_calibration_study.py` | `reliability-calibration-results.json` |
| Finite Gaussian sufficient-information and encouragement confidence | `tools/reliability_graph_study.py` | `reliability-graphs-results.json` |
| Audited action-dependent nonlinear variance | `tools/reliability_nonlinear_study.py` | `reliability-nonlinear-results.json` |
| Fixed richer dependent dictionary, QR/SVD and omission | `tools/reliability_learning_study.py` | `reliability-learning-results.json` |
| Fresh larger joint and learner designs, paired windows | `tools/reliability_followup_study.py` | `reliability-followup-results.json` |
| Eight complete dense/chunked fresh-process requests | `tools/reliability_workloads.py` | `reliability-workloads-results.json` |

Run from the repository root. The first five scripts support `--pilot` with
separate seeds. Final `reliability-*-final.jsonl` journals persist completed
requests and bind exact code/specification inputs; resume the identical command
after interruption. Changed scientific inputs require a new specification and
fresh journal, never replacement of old recorded hashes. Preserve failures and
unavailable fits. The nonlinear policy is frozen from the independent earlier
`closure-nonlinear-results.json` planning sample. Complete workload measurements
include imports, mapped-input verification, fitting, prediction, uncertainty,
output persistence and read-back; input acquisition is excluded equally.
Chunked fitting still retains O(n) input/score/residual storage.

The following execute finite checks or reconstruct retained records without
repeating the completed Monte Carlo studies. They write evidence receipts and
therefore may change a frozen delivery identity:

```bash
.venv-scope/bin/python tools/reliability_independent_checks.py
.venv-scope/bin/python tools/reliability_rehearsal.py
.venv-scope/bin/python tools/reliability_tables.py
python3 tools/reliability_source_trace.py
.venv-scope/bin/python tools/reliability_exact_replay.py
.venv-scope/bin/python tools/reliability_verify.py
```

The final verification reconstructs 21,251 journal requests, including
independent training, numerical and workload records, not that many independent
final inferential replications. A passing receipt is consistent execution,
not nominal calibration or economic superiority. Funding calibration stays
open; first joint/learner designs under-cover; the larger follow-up is conditional.
False restrictions and omitted features remain adverse. All external acceptance
is pending under the [prepared protocol](../program/external-validation-v8.md).
Earlier V7 and V6.1 commands below apply to their preserved scope.

# V6.1: weak-linkage continuation

The retained 2,000-draw study compares regular delta inference and two
confidence-region projections on the same dynamic funding target. All
regimes, seeds, pilot sizes and error allocation are in
`linkage-projection-spec.json`. Missing audit information, topology and
public input failures are separately checked. Earlier V6 studies below
remain preserved and applicable to their original assumptions.

```bash
.venv-scope/bin/python tools/linkage_projection_study.py
.venv-scope/bin/python tools/linkage_scientific_checks.py
.venv-scope/bin/python tools/verify_linkage.py
```

The initial candidate-coordinate pilot and its bound code are retained in
`linkage-candidate-box-pilot.zip`. Later finite-variance/revision-conflict
repairs preserve previous outputs; exact scientific draws remain unchanged.
Rerunning the study changes execution-time bytes and therefore a frozen
delivery identity. The affected `dynamic_product_study.py` workload is
replayed separately after simulations finish; unchanged servicing and
discovery studies need no new random draws.

# Scientific studies and local replay

These studies support the bounded constructions in the V6 monograph. The
public 401(k) and quarterly monetary applications are empirical with unknown causal truth; all other
known-truth populations and financial scenarios are synthetic. Specifications
precede their final repetitions; separate follow-ups and failed pilots remain
preserved. A passing execution receipt includes adverse scientific results
and does not imply that a method is suitable for routine inference.

## Current dynamic constructions

Run from the repository root with `.venv-scope/bin/python`. Specifications
precede final draws; all replication records, availability failures and adverse
results are retained. The reference code supplies statistical assumptions as
explicit inputs; successful execution cannot establish those assumptions.

| Construction | Final replay command | Evidence |
|---|---|---|
| Funding response, calendar inference and direct statsmodels match | `.venv-scope/bin/python tools/dynamic_funding_study.py` | `dynamic-funding-spec/results.json` |
| Reproduce and decompose original hidden-likelihood failures | `.venv-scope/bin/python tools/dynamic_servicing_study.py diagnose` | `dynamic-servicing-diagnose-results.json` |
| Larger hidden-likelihood information regime | `.venv-scope/bin/python tools/dynamic_servicing_study.py latent` | `dynamic-servicing-latent-results.json` |
| Whole-path audit estimation and independently trained belief policy | `.venv-scope/bin/python tools/dynamic_servicing_study.py audit` | `dynamic-servicing-audit-results.json` |
| Same-policy information comparison and audit misclassification | `.venv-scope/bin/python tools/dynamic_servicing_diagnostics.py` | `dynamic-servicing-diagnostics-results.json` |
| Correct finite ancestral target and learned endpoints | `.venv-scope/bin/python tools/dynamic_discovery_study.py` | `dynamic-discovery-spec/results.json` |
| Conflicting source fixtures and calibrated candidate histories | `.venv-scope/bin/python tools/dynamic_observation_study.py` | `observation-fixtures-v6.json`; `dynamic-observation-results.json` |
| Public quarterly monetary projection and design sensitivities | `.venv-scope/bin/python tools/dynamic_public_study.py` | `dynamic-public-spec/results.json` |
| Full source/learning/calibration/inference composition, 18 fresh processes | `.venv-scope/bin/python tools/dynamic_product_study.py` | `dynamic-product-spec/results.json`; `dynamic-product-runs/` |

The compact `spec/results` notation denotes separate `-spec.json` and
`-results.json` files. Funding, servicing, discovery and observation scripts
also support `--pilot`. Run the audit policy study before its diagnostics;
run discovery before its independent oracle check. Reconstruct the new
finite identities and retained summaries with:

```bash
.venv-scope/bin/python tools/dynamic_graph_oracle_check.py
.venv-scope/bin/python tools/dynamic_scientific_checks.py
.venv-scope/bin/python tools/verify_dynamic.py
```

The first two execute finite graph/path/derivative/covariance checks. The
last verifies executed input identities and reconstructs retained summaries;
it does not rerun the simulation studies. The larger hidden-likelihood study
is expensive and need not be repeated merely to inspect the proposal. New
usable regimes do not qualify the original 600-path or failed bootstrap
intervals. Misclassified audits, wrong metadata and poor discovered endpoints
remain adverse results. Mapping is by complete origin window, not a
persistent customer alias. Public monetary results are conditional projections.
Parallel funding is slower than serial on this one-host workload grid.

The [substantive review](../reviews/dynamic-construction-author-review.md)
explains the method decisions and boundaries. `DynamicBrief`, `run_funding`,
`treasury_report` and `application_result` in
`src/causalbank/dynamic_product.py` are the shared local reference operations;
the product study is their complete executable caller. Replaying writes
new receipts and invalidates the final delivery identity. For a read-only
check use `python3 tools/delivery_manifest.py verify`.

## Retained V5 scope-completion studies

Run from the repository root using the preserved local `.venv-scope`
environment. The following table gives actual commands; each final script
writes its result receipt under `docs/studies/`. Inference, latent, history
and discovery also support a separate `--pilot` mode. A pilot is not the
delivered full experiment. Run latent before its bootstrap challenger and
discovery before the graph-effect adapter.

| Construction | Final replay command | Specification and result |
|---|---|---|
| Same-target responses, common dates and dynamic panels | `.venv-scope/bin/python tools/scope_inference.py` | `scope-inference-spec.json`; `scope-inference-results.json` |
| Validated private multistate logger and two-sample uncertainty | `.venv-scope/bin/python tools/scope_latent.py` | `scope-latent-spec.json`; `scope-latent-results.json` |
| Prespecified latent bootstrap and numerical challenger | `.venv-scope/bin/python tools/scope_latent_bootstrap.py` | `scope-latent-bootstrap-spec.json`; `scope-latent-bootstrap-results.json` |
| Continuous censored histories and separately trained policy | `.venv-scope/bin/python tools/scope_history.py` | `scope-history-spec.json`; `scope-history-results.json` |
| Exact Gaussian private-logger estimation and policy value | `.venv-scope/bin/python tools/scope_continuous.py` | `scope-continuous-spec.json`; `scope-continuous-results.json` |
| PCMCI+/LPCMCI temporal search and adverse regimes | `.venv-scope/bin/python tools/scope_discovery.py` | `scope-discovery-spec.json`; `scope-discovery-results.json` |
| Actual search output to fresh-data conditional effect curves | `.venv-scope/bin/python tools/scope_graph_effect.py` | Frozen construction in script and discovery input; `scope-graph-effect-results.json` |
| Generated observation candidates, questions and audited linkage | `.venv-scope/bin/python tools/scope_organization.py` | `scope-organization-spec.json`; `scope-organization-results.json` |
| Archived public 401(k) ATE/LATE and matched DoubleML | `.venv-scope/bin/python tools/scope_public.py` | `scope-public-spec.json`; `scope-public-results.json` |
| Eleven complete workload cases, two fresh processes each | `.venv-scope/bin/python tools/scope_workloads.py` | `scope-workload-spec.json`; `scope-workload-results.json`; `scope-workload-runs/` |

Independent finite checks and retained-result reconstruction:

```bash
.venv-scope/bin/python tools/scope_checks.py
.venv-scope/bin/python tools/scope_workflow_checks.py
.venv-scope/bin/python tools/verify_scope.py
```

The first two commands re-execute exact likelihood/score/value and
graph/history/censoring checks. The last checks input identities and
reconstructs retained study summaries, including all failure denominators,
public ratios and workload accounting. It also regenerates
`scope-workload-summary.json`. It does not rerun complete simulations;
inference/linkage aggregate counters have only arithmetic/identity checks.
These commands write receipts and can invalidate the frozen delivery. For
read-only verification use `python3 tools/delivery_manifest.py verify`.

The current environment records Python 3.13.13, NumPy 2.5.2, SciPy 1.18.1,
scikit-learn 1.9.0, DoubleML 0.11.4 and Tigramite 5.2.10.1. Local copies of
selected runtime source and package metadata are preserved. Separate release
records establish the two causal packages' cutoff eligibility; installed
versions alone do not establish release dates. Workload processes set thread
limits before imports and verify every observed numerical pool uses one thread.

The original 600-path finite-state intervals remain unqualified: nominal 95% coverage is
.850–.875 and 17 of 199 bootstrap refits are invalid or at a boundary, so
the interval is withheld. Three latent refits in each workload measure cost
only. Search effect envelopes are conditional structural sensitivity, not
graph-selection confidence. Public analysis uses an iid working covariance
without survey design fields. The [author review](../reviews/scope-completion-author-review.md)
explains these limits and their product consequences.

## Earlier scientific-completion studies retained in V5

The S-program experiments below remain evidence under their original bounded
models. Their populations are synthetic. Current scope additions above do not
overwrite their adverse findings or expand their original guarantees.

| Construction | Frozen specification | Execution | Result |
|---|---|---|---|
| Direct/proxy responses, joint bands and weak-IV sets | a-experiment-v1.json | tools/study_responses.py | a-results.json |
| Integrated responses, sparse/factor learning and bandwidth follow-up | a-extension-v1.json | tools/study_response_extensions.py | a-extension-results.json |
| Common-shock bank panels | a-panel-v1.json | tools/study_panel.py | a-panel-results.json |
| Unknown-emission controlled likelihood and fixed-policy value | b-latent-experiment-v1.json | tools/study_controlled.py | b-latent-results.json |
| Fitted history augmentation and backward targeting | b-history-experiment-v1.json | tools/study_longitudinal.py | b-history-results.json |
| Finite Gaussian graph/effect outer sets | c-experiment-v1.json | tools/study_discovery.py | c-results.json |
| Structural VAR1 graph/response bands | c-temporal-experiment-v1.json | tools/study_temporal_discovery.py | c-temporal-results.json |
| Constrained observation candidates and abstention | d-experiment-v1.json | tools/study_organization.py | d-results.json |
| Complete fresh-process workflows | workflow-v1.json | tools/study_workflows.py | workflow-results.json; workflow-runs/ |

Run the listed scripts with `python3` from the repository root. Running a
study replaces its result receipt and invalidates dependent file identities;
preserve any assessed delivery first. The fixed seeds reproduce the
scientific design, while timing and floating-point optimizer behavior can
depend on the host and libraries. Expensive controlled-model repetitions
and bootstrap refits may take several minutes. There is no need to rerun
them merely to read or verify the delivered proposal.

Verify current stored experiment inputs and results without rerunning them:

```bash
python3 tools/verify_completion.py
python3 tools/delivery_manifest.py verify
```

The second command checks the frozen delivery. To reproduce the local
software/interface probes and six standalone reference requests:

```bash
python3 tools/qualify_interfaces.py
python3 tools/standalone_examples.py
python3 tools/scientific_checks.py
```

These commands inspect sibling source files read-only and create local
snapshots/mappings. They do not execute or adopt code in sibling repositories.
The standalone command-line interface accepts an archived request and its
NumPy data file, with explicit scientific regime and typed result:

```bash
python3 tools/causal_study.py --help
```

Versioned example requests, data, diagnostics and results are in `standalone/`.
The [scientific protocol guide](../../contracts/scientific/README.md) defines
supported regimes and rejection behavior. Automatic organization has its
own candidate/abstention output and is exercised by the D script.

After changes to study inputs, rerun the affected study and its independent
checks, then regenerate tables with `python3 tools/completion_assets.py` and
verify with `python3 tools/verify_completion.py`. Follow the root README's
source/build/render review sequence before creating a replacement delivery.
The verifier deliberately refuses stale evidence; changing a recorded hash
without re-execution does not repair a changed experiment.

The measured environment uses NumPy 2.5.2, SciPy 1.18.1, scikit-learn 1.9.0,
DuckDB 1.5.5 and Polars 1.44.1 on the recorded EPYC 7773X host. These are
observed installed versions on 8 October 2026, not evidence of their release
availability at the 7 October literature cutoff. Complete timings explicitly
limit BLAS, DuckDB and Polars to one thread each. They include generated raw
records, Parquet I/O, reconstruction, fitting, inference, sensitivity/refits
and JSON reporting. They do not establish bank throughput, distributed
scaling or analyst-hour savings. The 19-refit workload measures cost, while
the separate 79-refit interval remains a coarse bootstrap calculation.
