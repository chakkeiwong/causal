# Version 4: remaining gaps against the requested standard

Assessment date: 8 October 2026. Literature cutoff: 7 October 2026.

This is a comparative author assessment requested after the V4 delivery. It
does not replace the frozen files, reopen an execution program automatically,
or constitute independent review. It supersedes the implication that only
production construction and bank validation remain. The S-phase work was
executed, but phase completion is not sufficient evidence of satisfying the
full breadth and depth of the user's commissioned survey and product proposal.

## Judgment and comparison basis

V4 is a substantial research monograph with useful, reproducible reference
constructions. Its strongest passages now connect causal semantics,
identification, an estimator, uncertainty and an adverse example. The original
omissions of graph construction, IV, semiparametric learning and the
longitudinal/state-space connection have been materially repaired. The source
archive, explicit nonidentification arguments and retention of adverse
results are strengths.

The remaining defect is uneven completion of that chain across the central
product ambitions. Four narrowly specified worked problems cannot by
themselves establish that the wider time-series, panel, controlled-latent,
discovery and data-organization design is sufficiently developed. Narrow
examples are appropriate references; the question is whether the survey
also develops and selects credible routes for the proposed users' problems.

The comparison uses substantive passages, not page counts:

- FinMarketing, `docs/chapters/ch07_uplift.tex`, lines 385–475: the R-loss
  identification calculation, DR conditional-bias remainder, source-specific
  rate conditions and the distinction between conditional-effect learning
  and ATE inference.
- BayesFilter, `docs/chapters/ch09_kalman_score.tex`, especially lines 40–145:
  initial-condition, innovation, gain and update derivatives, solve forms,
  and the obligation to differentiate the likelihood actually evaluated.
- CIP, `docs/latex-papers/CIP_monograph/chapters/ch18b_midas_identification.tex`,
  the literature/method-choice discussion beginning at line 387: the
  mathematical contribution and restrictions of each alternative, followed
  by a justified hierarchy of primary method, challenger and diagnostic.

The prior reference-inspection record is
`reference-standards-2026-10-08.json`. This assessment is a targeted comparison
of central arguments and their boundaries, not a fresh proof audit of every
chapter in four monographs.

## G1. Time series, panels and dependent learning: a usable inference strategy

**Present.** `07_time_series.tex` and `07a_dependent_construction.tex`
distinguish shock interventions from policy replacement, derive direct-IV
responses and VAR propagation, prove a bounded dependent inference route,
retain weak-IV sets, develop separated-block learning, aggregate common-shock
scores by date, and map stationary changes into integrated level responses.
`06_panels.tex` derives fixed/random/correlated effects, difference-GMM
moments, DID functionals and synthetic-control factor errors.

**Remaining.** Depth is much greater for the selected Gaussian response and
bounded sparse-learning experiments than for the broader banking series and
panels. Persistence, unknown dynamics/rank, breaks, heavy tails and mixed
frequency are discussed, but they do not yet lead to an equally complete
selection and inferential path for a realistic combined use case. The panel
chapter explicitly leaves system-GMM theory and finite-sample corrections
for separate source qualification. Modern panel and synthetic-control
branches are not developed into fitted comparative inference at the depth
of the main response experiment.

This is consequential rather than a request for more named methods. In
`20a_completion_studies.tex`, nominal 95% Bonferroni whole-curve coverage is
81.8% in the specified near-unit experiment. Date-HAC panel intervals cover
85.6% at 800 dates and 89.0% at 2,000. Those are empirical properties of
particular generators, not refutations of fixed-parameter asymptotic results.
They nevertheless leave the practical default unresolved. Reporting the
failure and bandwidth sensitivity is necessary; selecting a credible
alternative or restricting the supported problem still requires work.

**Closure.** Develop one realistic response/panel dossier with an explicit
method hierarchy, source-specific inferential conditions, implemented primary
and substantive challenger, and qualification across persistence and dependence
regimes. Explain which model restrictions require external judgment and how
the product responds when they cannot be defended. Broader survey branches
need mathematical comparisons and defended exclusions, not implementation of
every estimator or a promise of uniform validity under arbitrary processes.

## G2. Longitudinal and POMDP estimation: beyond the finite randomized reference

**Present.** `10_controlled_identification.tex`,
`10a_controlled_estimation.tex`, `11a_fitted_history.tex` and
`12_decision_learning.tex` connect observed and interventional likelihoods,
private logging, proxy bridges, finite-state identification, likelihood/EM,
fixed-policy value, observed-history augmentation/targeting and policy-selection
restrictions. The binary unknown-emission reference has a real identification
and regular sampling argument; it is not merely an HMM fit called causal.

**Remaining.** The completed latent fit has two states, binary signals,
randomized actions and independent complete trajectories of fixed length.
The value comparison uses fixed observable policies. Observational private
logging, richer state/observation models and continuous-state approximation
are addressed theoretically, but lack the same complete fitted comparison.
The observed-history qualification uses a finite observed-state model.
Combining richer histories with censoring, irregular visits and learned
decision rules is still a design obligation where those capabilities are
part of the product claim.

BayesFilter's standard also exposes a numerical-depth gap for the proposed
continuous-state route: giving Kalman recursions and particle weights does
not supply a selected controlled-model likelihood, derivative implementation,
conditioning analysis and a decision-value error budget for that route. The
binary implementation checks its analytic score and uses finite-difference
information/value gradients; its own text correctly requires renewed
step-size and conditioning analysis beyond that example.

**Closure.** Select a representative observational servicing problem and
derive when observed-history adjustment, a validated controlled latent model,
or a proxy-value route is defensible. Carry the selected tractable route
through fitting and uncertainty, with a substantive numerical challenger.
Make estimation error, numerical error and policy-selection effects explicit.
Use nonidentification or sensitivity where assumptions cannot identify value;
unrestricted POMDP identification is not a reasonable completion requirement.

## G3. Discovery: a practical graph-to-effect route at the advertised scope

**Present.** `08_discovery.tex` treats mixed-graph semantics, independence
search, signal restrictions, functional assumptions, time-series discovery,
equivalence-class adjustment and effect sets. `08a_discovery_inference.tex`
adds a genuine simultaneous covariance-region construction for three observed
Gaussian variables and a separate stable VAR(1) coefficient-box construction.

**Remaining.** The strongest inferential demonstrations are much narrower
than a large time-series discovery product. The temporal construction assumes
a known lag bound, independent innovations and no contemporaneous edges.
The static construction assumes causal sufficiency and can return very wide
outer sets. General temporal or latent-confounder discovery is appropriately
labelled exploratory, but the product does not yet have an equally developed
choice between mature temporal-search and structural-model alternatives for
a realistic workflow. Hidden-confounding and omitted-lag failures show why
larger runtimes alone cannot close this gap.

**Closure.** Work through a multivariate temporal example with justified
background knowledge, an explicitly chosen discovery family, an alternative
with different assumptions, and the resulting supported effect query. Show
what additional data or restrictions resolve decision-relevant ambiguity.
Keep graph stability, conditional identification and confidence claims
separate; a general confidence theorem for arbitrary large PAGs is outside
the required closure.

## G4. Automatic organization: candidate generation and ambiguity resolution

**Present.** `09a_organization_algorithm.tex` implements 32 observation-plan
candidates covering clocks, keys, versions, aggregation and a supplied entity
map. It has explicit constraints, ranking, material-ambiguity abstention and
reproducible downstream effect consequences. Its conditional correctness
argument is clear about oracle inclusion and valid constraints.

**Remaining.** The key semantic hypotheses and candidate household map are
supplied. The work does not yet establish how realistic heterogeneous feeds
generate that candidate space, how missing interpretations are discovered,
or how targeted analyst questions and probabilistic linkage are handled.
Always accepting the resolved fixtures and abstaining on ambiguous fixtures
does not establish usefulness or error rates on new source structures.

**Closure.** Specify and evaluate candidate generation on heterogeneous
schemas; distinguish hard evidence from hints; derive a workflow for acquiring
the missing metadata or measurement. Propagate unresolved observation/linkage
alternatives into effects and decisions. Evaluate wrong acceptance, useful
resolution and analyst burden, with unrepresented interpretations included as
failure cases. General inference of economic meaning from column names is
not the required claim.

## G5. Common product and software choice: demonstrate representative reuse

**Present.** `17_software.tex` contains substantive source-level comparisons,
including intervention-law differences, weighting restrictions, graph endpoint
semantics and observation clocks. `18_product.tex` and
`18a_scientific_language.tex` derive rich request/result types, finite-kernel
semantics, admissible transformations and concrete sibling mappings.

**Remaining.** `tools/causal_study.py` dispatches six bounded recipes; some
enforce specific reward families and policies. The finite-kernel interpreter
and those dispatch rules do not yet demonstrate broad composition from a
new supported scientific question into an estimation/inference plan. Installed
qualification concerns numerical and data primitives; the 44-project causal
software review is a separate source/document review. Local sibling mappings
are useful but do not yet show the proposed common layer accommodating
substantively different analyses with reusable estimator components.

**Closure.** Demonstrate a small number of distinct analyses using common
scientific objects and target-preserving transformations, including one
selected substantive causal-package adapter and a matched numerical reference.
Use those comparisons to defend what the project should build, reuse or defer.
A full generic causal compiler, all-package runtime qualification and completed
production integrations are not necessary to establish the proposal.

## G6. Literature coverage and critical synthesis: completion by question

**Present.** The archive and technical anchors are substantial, and several
chapters now make source-specific distinctions rather than list citations.
`scientific-choice-map.md` connects the 14 domains to four worked problems.

**Remaining.** The search remains purposive and bounded. Recent additions
concentrate on dependent inference and a controlled spectral source; the
executed selection record explicitly disclaims a fresh exhaustive forward
search across all domains. A preserved source is evidence for its cited claim,
not evidence that the important alternatives, corrections and later results
for that question have been covered. Some method hierarchies are well
developed; others end at a source description or extension boundary.

**Closure.** For the core G1–G5 decisions, complete backward/forward searches
to the agreed cutoff, inspect the decisive primary results and relevant
corrections, and write a common comparison of estimand, identifying assumptions,
sampling conditions, approximation, computation and failure modes. State
coverage limits. Exhaustive coverage of the whole causal literature is neither
possible nor needed. New citations must retain the existing real-PDF and
source/hash/anchor obligations.

## G7. Empirical and scale evidence: connect the design to a real analysis

**Present.** The synthetic studies provide known truth, adverse comparisons
and complete local workload measurements. The largest response reconstruction
has about 3.85 million versioned records; the larger latent workload includes
19 bootstrap refits. Their statistical and computational limits are disclosed.

**Remaining.** No complete public empirical banking/financial application
yet demonstrates how the proposed scientific choices interact with real
measurement and assignment ambiguity. Single-host, single-thread workloads
do not qualify distributed nuisance fitting, graph search or latent inference
at banking-group scale. The source text correctly says 19 refits measure cost,
not accurate confidence-interval endpoints. Illustrative adoption economics
remain unmeasured.

**Closure.** After the central theoretical choices are settled, reproduce a
public financial analysis with archived data and a defended observation and
identification design; do not describe its unknown causal truth as validated.
Compare the same task using direct expert composition of existing software.
Specify and measure the dominant computation at relevant dimensions. Bank
confidential-data qualification, independent validation and adoption remain
later institutional work, rather than prerequisites for the scholarly repair.

## Continuation and status interpretation

The recommended order is G1 and G2, then G3–G5, followed by G7. G6 accompanies
each scientific question throughout. The first substantive checkpoint should
resolve a practical method choice exposed by an existing adverse result; a
new inventory or another set of phase-completion counts would not do so.

The appropriate next acceptance test is whether a reader can reconstruct a
representative banking question through observation semantics, identification,
estimator choice, derivation, inference, numerical validation and reusable
product behavior, while understanding why the important alternatives change
the answer. Several V4 examples now meet this test within their narrow models.
The remaining task is to make the selected wider product scope meet it too.

There is also minor document-control cleanup: the top update in
`coverage-and-omissions.md` still describes an earlier reconstruction count,
and the initial C-T row in `scientific-choice-map.md` describes a temporal-CI
route while the delivered reference is a VAR(1) coefficient box. Later records
explain the limits; a future revision should reconcile the active summaries.
These editorial defects are secondary to G1–G6.

The current dashboard's next action of independent review followed by
production construction is therefore incomplete as a comparative assessment.
This note records that correction without modifying or re-freezing V4. The
user has asked for an assessment in this turn; this note does not execute a
further revision. Existing authorization for local research work remains in
force.
