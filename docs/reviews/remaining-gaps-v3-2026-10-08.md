# Remaining gaps against the requested monograph standard

8 October 2026, Asia/Shanghai. Assessment requested by the user after the
version 3 delivery. This is a comparative scholarly assessment, not a new
delivery or a claim that remediation has been executed.

The manuscript has substantially repaired the original omissions, but it
does not yet consistently meet the requested standard. The earlier
author-reviewed completion judgment was too strong. Substantive theory,
method selection and scientific specification remain unfinished before
institutional validation becomes the main outstanding task.

This assessment supersedes that judgment of comparative sufficiency. The
original version 3 PDFs, source files, mission records and manifest are
retained as the assessed snapshot; this review does not silently rewrite or
re-freeze them. Their completion labels record the previous author judgment,
not the conclusion of this assessment. The next scholarly pass must reopen
the affected exit tests described below.

## Evidence and comparison scope

Assessed monograph: `docs/causal_foundations.pdf`, SHA-256
`8429397875e0089c569a1c9c6a3889c52467c20fd73f4d03f399920615537c2e`.
Companion sponsor proposal: `docs/sponsor_reconstruction.pdf`, SHA-256
`08c9af0b4974b2191849ebbc548a21ab6d60e10e91346b7d2a8348fa0c48be41`.
Both identities were checked against the delivery manifest during this
assessment. No manuscript or PDF was changed.

The benchmark comparison uses substantive passages documented in
[the reference inspection record](reference-standards-2026-10-08.json),
including FinMarketing's learner and dynamic-choice constructions,
BayesFilter's state contract, Kalman score and numerical-target discussion,
and CIP's MIDAS method comparison. The six corresponding original chapter
hashes still match the preserved inspection record. This is not an
independent correctness audit of the entirety of those three monographs.

The local program consistency/source-identity check passes. Its stated
scope is explicitly not scholarly sufficiency. A Git status query returned
that this directory is not a Git repository; no version-control operation
or sibling-repository modification followed. This review introduces no new
scholarly citations or external-source acquisitions.

## What the benchmarks require

The common standard is a recoverable scientific construction: define the
economic question and information, establish the identifying restrictions,
derive an estimand and estimator, justify uncertainty and numerical choices,
compare substantive alternatives, and use those results to determine the
product's behavior.

- FinMarketing's learner comparison derives different losses and targets,
  discusses source-specific evidence and connects the comparison to choices
  in a particular application. Its value is not the number of learner names.
- BayesFilter carries the likelihood through prediction, innovation, gain,
  state-update and score recursions, including initialization and missing
  observations. Its numerical-target discussion distinguishes the scalar
  objective actually evaluated from other approximate or random objectives.
  An integration can therefore be assessed against concrete mathematics.
- CIP's MIDAS discussion chooses a primary estimator, mandatory shape
  diagnostics and conditional extension arms. An explicit normalization
  identity explains why an additional shrinkage method is not an independent
  shape comparison. Literature changes the method hierarchy.

The causal manuscript has passages of comparable substance. Graph
construction and IV are no longer missing; neither are causal ML or the
longitudinal/state-space connection. In particular,
[the longitudinal chapter](../reconstruction/04_longitudinal_states.tex)
derives a fixed-horizon canonical gradient, a general nuisance remainder,
backward augmentation and targeting, and a controlled observation law on
one decision clock. These are substantial assets to retain. The problem is
uneven completion of the scientific chain across the central capabilities.

## 1. Dependent, high-dimensional time-series inference is still incomplete

**Observed evidence.** In
[the time-series chapter](../reconstruction/07_time_series.tex), lines
98–172 carefully distinguish LP-IV, structural propagation, normalization
and noninvertibility. Lines 174–234 give useful aggregation and state
coordinate examples. However, lines 236–287 impose a stationary score CLT
and negligible remainder, refer to a suitably slow HAC bandwidth, describe
block separation qualitatively, and state the need for joint-horizon
inference. They do not instantiate a complete estimator and uncertainty
procedure under one specified dependence regime. Lines 297–303 name sparse
VARs, low-rank factors and screening without a developed statistical and
computational comparison. Unit roots and breaks are boundary warnings;
cointegration has no substantive treatment in the reconstruction chapters.

**Why this matters.** Large-scale causal time series is central to the
commission. Independent customer trajectories, a single dependent series
and bank panels exposed to common shocks are different experiments. A
general warning about their differences cannot determine a supported
estimation operation.

**Closure criterion.** Select explicit initial regimes and develop their
assumptions, estimator construction, tuning, dependence/splitting conditions,
remainder control, covariance estimation and response-band or test-inversion
procedure. Compare a principal estimator with justified challengers on the
same target. Explain the treatment or deliberate exclusion of persistence,
cointegration, breaks, weak instruments and high-dimensional nuisance
learning. This requires a bounded construction, not a universal theorem
covering every dependent process.

## 2. POMDP estimation needs a complete supported route to decision uncertainty

**Observed evidence.** The controlled-state chapters distinguish private
logging from intervention and supply a constructive known-emission
identification route. The estimation section in
[controlled identification](../reconstruction/10_controlled_identification.tex),
lines 206–329, gives finite-state EM, a Gaussian update, a particle weight
and useful error distinctions. It does not carry a selected nonlinear or
unknown-emission controlled model through a fully specified parameter
inference and decision-uncertainty construction. The simulation bound is
for a common finite Markov state space; the text correctly says that a
POMDP extension requires a comparison of belief processes and information.

[The hidden-state study](../reconstruction/20_banking_studies.tex), lines
207–269, already includes unknown-emission fitting, adverse logger results
and a refitted bootstrap for a fixed reactive policy. These are real
evidence, so it would be incorrect to say there is no estimation or no
parameter-to-value uncertainty. They do not qualify arbitrary controlled
latent identification or uncertainty after choosing an optimal policy.

**Closure criterion.** Choose a bounded identifiable controlled model and
link its identification conditions to the model actually estimated. Specify
the likelihood, parameter restrictions, fitting/derivative route, uncertainty
procedure and value calculation. Determine how numerical and statistical
errors affect the decision. Either justify policy-selection inference or
limit the supported output explicitly to fixed-policy evaluation. Compare
the chosen backend with a meaningful alternative and state when each fails.
BayesFilter supplies a standard of explicit numerical contracts; causal
integration must supply the additional logger and intervention semantics.

## 3. Discovery does not yet have a complete statistical path to an effect report

**Observed evidence.**
[The discovery chapter](../reconstruction/08_discovery.tex) explains PC/FCI,
graph semantics, signal conditions, functional restrictions and temporal
window effects. Its three-variable equivalence example correctly gives an
effect set. Lines 302–311 describe coverage conditional on a valid graph
confidence set and valid effect confidence sets. They expressly identify
obtaining those properties as the hard part; no selected general procedure
there constructs both for the proposed temporal workload.

**Closure criterion.** For a declared initial graph and sampling class,
specify discovery, background restrictions, tuning, graph/effect uncertainty
and computational limits together. Show how uncertainty and screening affect
the reported intervention conclusion, using a reproducible adverse example.
Where valid inferential propagation is unavailable, define an exploratory
result with explicit unresolved alternatives. Neither an edge stability
frequency nor a chosen DAG can silently supply an effect confidence level.
Full general PAG inference is not a necessary first-release requirement.

## 4. Literature synthesis must end more often in justified method choices

**Observed evidence.** The recent-methods chapter now contains substantial
source-specific arguments and counterexamples. The deficiency is not a
uniform lack of reading. Its closing comparison and the software/product
catalogue nevertheless often end with candidate methods and obligations,
rather than a selected default, mandatory challenger and rejection or
extension rule for a concrete banking workload. The
[operation catalogue](../../contracts/scientific/operation-catalogue.json)
repeatedly calls for a "qualified" construction that is not itself
instantiated there.

**Closure criterion.** For each central workload, compare methods under a
common target and information set: identification, regularity, finite-sample
behavior, uncertainty, computational burden and software feasibility.
Choose a hierarchy conditional on the workload, as CIP does. Explain which
source results transfer, which do not, and why a plausible alternative is
deferred. Prioritize literature acquisition and forward/backward searches
around unresolved choices rather than adding a general wave of citations.

The [coverage record](../literature/coverage-and-omissions.md) remains a
bounded purposive survey. Some original historical texts and correction
chains remain unavailable; later primary author texts can support specific
results without closing that history. Copies and source anchors establish
traceability, not comprehensive intellectual coverage. Existing recent
preprint readings likewise should not be confused with replication.

## 5. The scientific product representation is not yet sufficient for its catalogue

**Observed evidence.**
[The product chapter](../reconstruction/18_product.tex), lines 116–131,
proposes a typed kernel/expression language. Its syntax, validation and
transformation rules and lowering to selected estimators are not fully
specified. The request schema binds model, target, observation and sampling
artifacts by path and hash; that verifies identity without defining all
their internal mathematical semantics.

There is a concrete representation boundary:
[the result schema](../../contracts/scientific/result.schema.json) allows a
numeric-or-null estimate and scalar interval unions, while the catalogue
includes a response vector and graph/effect-set operations. The chapter
explicitly leaves multivariate regions, curve bands and graph distributions
to extensions. Attaching an arbitrary evidence file does not establish a
typed interoperable result for these objects.

**Closure criterion.** Specify a bounded expression and model language,
allowed transformations, estimator/inference selection and result types
for the operations actually promised. Fully instantiate at least the
central dynamic and sequential requests, including unsupported cases and
their mappings to specific backend APIs. Another team should be able to
reconstruct the same target, computation and uncertainty without inventing
missing scientific rules. This is specification work; a deployed product
is not required to establish it.

## 6. Automatic data organization remains a proposed behavior without a selected mechanism

**Observed evidence.**
[The execution chapter](../reconstruction/19_execution.tex), lines 15–100,
gives valuable revision, availability, clock and linkage semantics. Its
automatic component can "propose" keys and clocks and "rank" competing
interpretations. No concrete proposal/ranking/abstention procedure or
evaluation design is selected. The broader observation chapter explains
why linkage and measurement uncertainty matter; this does not by itself
construct the automatic organization product.

**Closure criterion.** Define inputs and candidate interpretations, the
constraints and evidence used to compare them, when to retain alternatives
or seek an analyst decision, and what downstream conclusions change.
Evaluate against known ambiguous clocks, revisions, entity links and
stock/flow mappings. Explicitly separate fields recoverable from records
from economic assumptions supplied by a human. Specify the integration
with dataml's actual interface through read-only inspection and local
adapter examples; no sibling modification is needed.

## 7. Scale and software evidence do not yet test the central scientific workflow

**Observed evidence.** The complexity discussion distinguishes sequential
fitting, discovery and reductions, which is useful. The measured scale
experiment covers precomputed score reduction. It does not establish the
cost or error of data reconstruction, nuisance fitting, repeated latent
optimization, discovery, uncertainty and sensitivity together. The 44
software entries have source/document qualification; none has runtime
qualification. Existing banking studies contain important adverse results,
but are separate bounded demonstrations rather than an integrated test of
the proposed reusable operations.

**Closure criterion.** Design end-to-end synthetic workloads with declared
entities, time points, variables, horizons, latent states and dependence.
Compare the selected principal methods and challengers on statistical error,
coverage or decision quality and computational cost. Include uncertainty,
multiple fits and failures in the cost account. Execute small feasibility
probes for the selected backend routes, with pinned versions and independent
references; installing or benchmarking all 44 packages is unnecessary.
Connect scale optimizations to the assumptions and approximation error they
change. Bank-specific performance and adoption remain later validation.

## Why the previous review closed too early

The master program has stronger exit tests than the completion evidence
consistently satisfies. R06 calls for dependable inference and graph-effect
propagation; the manuscript sometimes specifies obligations rather than a
complete supported construction. R07 requires an estimator/inference
contract for each supported operation; the scalar result protocol cannot
directly represent some of the advertised outputs. R08 requires benchmark
depth across the cumulative argument; strength in the graph and
longitudinal derivations does not establish that depth for every central
capability.

The author review repaired substantive mathematical defects, and those
repairs should be retained. Its remaining mistake was to allow coverage,
correct warnings, bounded demonstrations and audit completion to close
unfinished construction questions. Listing an unresolved matter as a
boundary is adequate only if the product's initial supported claim has been
coherently narrowed and still answers the commission.

## Exact continuation actions

1. Reopen the affected R05–R09 exit tests and the method-selection portions
   of R01/R03/R04. Preserve completed derivations and historical receipts.
   Correct the active mission/state completion judgment when resuming the
   revision, with an explicit history of the superseded assessment.
2. Write four concrete study specifications: dependent structural responses;
   longitudinal policy value with observed-history and controlled-latent
   routes; discovery followed by an intervention query; and automatic
   observation construction reused by those analyses. Declare support and
   deliberate exclusions before choosing additional methods.
3. Close the missing mathematical and literature arguments for those
   specifications, starting with dependent time-series inference. Every new
   citation retains the genuine-PDF, filename, version/hash, inspected-anchor
   and claim-audit requirements.
4. Select primary methods and challengers. Complete their algorithm,
   uncertainty, numerical and interface specifications; then align the
   scientific schemas and proposed backend integrations with those choices.
5. Run targeted adverse, repeated-sample and performance experiments that
   distinguish competing constructions. Use their findings to revise the
   theory and design, not merely to populate evidence tables.
6. Review each scientific chain by asking whether a reader can reconstruct
   it without supplying missing mathematics. Repair the resulting defects,
   then update the sponsor case, source audit, build and rendered review.
   A new delivery identity belongs at the end of that process.

Full bank deployment, accepted sibling adoption, customer demand and
unrestricted latent identification are not prerequisites for closing this
scholarly revision. Nor does closure require reproducing every theorem in
the field. It requires sustained depth for a justified core, explicit
alternatives and an honest relation between the mathematics and the product
being proposed.
