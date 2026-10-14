# Theoretical field map and reconstruction obligations

8 October 2026 (Asia/Shanghai). This is an initial research map, not a
completed survey. It names the concepts and connections the new monograph
must derive. It neither asserts that all listed primary texts have been
inspected nor imports the contents of the benchmark monographs as authority.

The unit of coverage is a scientific question and its proof obligations, not
a list of algorithms or a paper count. Every chapter must distinguish:

1. The decision, population, time scale, intervention and counterfactual target.
2. The generative/structural model and the observed-data law.
3. The assumptions under which the target is identified from that law, or a
   constructive demonstration of nonidentification.
4. The resulting statistical functional, estimator, uncertainty calculation
   and dependence or inverse-problem conditions.
5. At least one substantively different method, its different target or
   assumptions, and a case in which the choice matters.
6. A small derivation or checked counterexample and a banking interpretation.
7. The precise product operation, input evidence, admissible output and
   unsupported state justified by the mathematics.
8. Primary-source anchors and the exact limitations of inherited claims.

An existing calculation may satisfy one element, but not the entire chain.
Both apparently successful and negative calculations should be preserved.

## Foundational dependency graph

The intended logical order is:

economic intervention and observed information
  -> SCM/potential-outcome or longitudinal process
  -> graph with latent, selection and measurement assumptions
  -> identifiable target or identified set
  -> observable statistical functional
  -> estimator, influence function/inverse problem and dependence law
  -> uncertainty and sensitivity
  -> financial decision
  -> justified operation/result contract.

Discovery may propose graphs and experiments, but the proposed graph is an
input to an identification argument. An estimator never supplies the missing
causal assumptions. A fitted state-space model supplies an observational law
under its model; an intervention law requires further restrictions.

## Required theoretical domains and cross-connections

| Domain | Derivations and comparisons required | Cross-connection that must be explicit |
|---|---|---|
| 1. Causal semantics | Potential outcomes, consistency, treatment versions, SCM equations and exogenous disturbances, single-world intervention graphs, interventions on nodes or mechanisms, interference boundaries. Clarify where model classes impose different cross-world restrictions. | A bank action and its recorded proxy must be separate nodes; graph arrows have intervention meaning unlike lineage arrows. |
| 2. Diagram construction | Build a time-indexed bank graph from actor, decision clock, business mechanism, observation and outcome. Distinguish assumed DAG, latent projection/ADMG, CPDAG/PAG and proposed discovery output. Work d-separation, colliders, backdoor adjustment, frontdoor conditions, selection and post-treatment covariates through concrete graphs. | Show how the graph changes the admissible covariates and which uncertainty cannot be learned from a discovery score. |
| 3. Identification logic | Factorization and truncated factorization under stated SCM assumptions; adjustment and g-formula proofs; do-calculus/ID as scoped tools; observational equivalence and bounds. Include a failed identification query with two models that agree observationally. | A typed effect should carry a functional or a nonidentification witness, not just a preferred package name. |
| 4. Randomization and adaptive assignment | Cluster and individual randomization, encouragement, interference, sequential/adaptive randomization and stopping. Derive what known assignment probabilities allow; distinguish ITT from receipt and policy value. | Connect experiments to IV, longitudinal actions and dependence-aware inference. |
| 5. Instrumental variables | Construct the Z-to-A-to-Y graph with latent A/Y confounding, conditional exclusions and relevance. Derive linear moment/rank, 2SLS/GMM and the Wald quantity; then contrast heterogeneous LATE, weak-IV-robust inference, control functions, nonparametric IV and proximal bridges under their own assumptions. | Explain why the graph alone does not identify a population ATE; identify the distinct returned object for linear effects, complier effects and ill-posed structural functions. |
| 6. Semiparametric statistics and causal ML | Statistical models, nuisance tangent directions and influence functions for common targets; orthogonality, sample splitting, second-order remainders, rate and sampling conditions. Compare response learners, R/DR learners, causal forests, targeted methods and policy learning under aligned targets. | ML improves nuisance or effect estimation after identification; factual prediction, target drift and distribution shift are separate questions. |
| 7. ML with endogeneity, measurement and transport | IV-ML/orthogonal moments, NPIV inverse operators and weak identification; proxy bridges/completeness; measurement error, missingness, causal representations and environment invariance with source-specific restrictions. | Predictive embeddings cannot silently become valid instruments, proxies or adjustment variables; learning can regularize but cannot create rank/completeness. |
| 8. Longitudinal counterfactuals | Time-varying confounding affected by prior actions; observed-data factorization versus policy replacement; g-computation, IPW, MSMs, SNMMs/g-estimation, recursive DR and longitudinal targeting. Derive policy scores and censoring/eligibility terms with their information sets. | Show when feedback makes ordinary regression inappropriate and how the estimand differs between sustained, modified and incremental policies. |
| 9. State-space/longitudinal bridge | One time-indexed SCM with latent state, action, reward, observation and missingness processes. Derive its observed likelihood and interventional law. Compare g-formula recursion, forward filtering/smoothing and controlled planning under fully observed and partially observed special cases. | Spell out when a belief is a sufficient predictive state; why a filtered state does not prove sequential exchangeability; how private logging changes posterior state selection. |
| 10. POMDP and structural behavior | Controlled hidden-state identification, label/rotation invariance, emission/transition/reward support, Bayesian/EM/particle alternatives, policy value and uncertainty. Distinguish bank policy, customer dynamic choice and equilibrium response. | Connect BayesFilter's numerical filters to the causal model's intervention and information contract without treating its likelihood as a causal certificate. |
| 11. Econometric panels and dynamic systems | FE/RE and correlated effects, dynamic-panel moments, staggered/reversible DiD, synthetic controls, anticipation and spillovers; LP, SVAR, external instruments and structural shock normalization. | Connect graph and moment restrictions to financial shocks, entity/time dependence, sample splitting and local versus equilibrium effects. |
| 12. Causal discovery | Conditional-independence, score and functional-model routes; Markov equivalence, faithfulness, latent/selection assumptions, time aggregation, feedback and invariance; algorithms as attempts to recover the specified equivalence object. | Carry unresolved graph marks into identified effect sets or a data/experiment request; do not silently orient them to enable estimation. |
| 13. Observation and data organization | Event time, recorded/available time, revision validity, sampling, coarsening, entity resolution, imputation and accounting identities. Analyze what each observation operator does to identification. | Separate data-lineage provenance from causal structure; pass measurement uncertainty into estimation rather than replacing uncertain data with a clean table. |
| 14. Scientific computing and product design | Identification compiler for a bounded, explicitly supported subset; estimation/inference adapters with matched estimands; source and evidence receipts; conditional versus causal model states; tests of failure and recovery. | A method's input/result contract follows from its mathematical objects, with explicit cannot-identify/cannot-estimate/not-yet-implemented distinctions. |

This is a dependency map, not a promise that all advanced subfields will be
implemented in the first release. The book must cover the core intellectual
relations; product support can be explicitly bounded.

## Required bridges, with minimum demonstrations

### Diagram to instrument to estimand

Begin with an actual business decision, for example randomized offer
encouragement Z, accepted product A and financial outcome Y. State which
unmeasured variable U affects both A and Y. Draw and describe the graph,
including a forbidden direct Z-to-Y path and possible measurement or
spillover routes. Write a structural system and identify the exact condition
that makes Z orthogonal to the outcome disturbance. Derive the observed
covariance ratio and its target under a homogeneous linear model. Show the
different target under heterogeneous compliance and monotonicity. Give a
weak-instrument or invalid-exclusion counterexample. Then specify which
result type and diagnostics the product can return under each route.

This bridge fails the acceptance test if it merely displays the Wald ratio or
if a drawn arrow is treated as empirical proof of exclusion or monotonicity.

### Identification to machine learning to inference

Start with an identified functional under explicit graph/sequential
assumptions. Derive an influence function or orthogonal moment for it,
including its nuisance directions and remainder. Explain sample splitting
and the relevant independence/dependence units; compare at least two ML
estimators on an aligned target and a change-of-target case. Include one
failure from support, confounding or distribution shift that prediction
accuracy cannot repair. The product design must preserve target weights,
fold boundaries and inference status.

This bridge fails if methods are compared by accuracy alone or if an
orthogonal score is presented as a generic causal-identification theorem.

### Longitudinal intervention to state-space likelihood and policy value

Use one shared event clock for initial state, observation, action, reward,
transition and next observation. Write the observed generative law including
behavior action and observation factors. Derive the law under a specified
policy as a mechanism replacement and state the extra causal assumptions.
When the full relevant history is observed, recover the longitudinal
g-formula and one recursive evaluation. When a state is hidden, derive
filtering/smoothing separately from policy replacement. Add a private
logger and exhibit how conditioning on its action changes the posterior
without making an intervention equivalent to conditioning. Compare model
likelihood fit, state identifiability and policy-value identifiability.

This bridge fails if a good filter or Bellman recursion is used as evidence
of an identified historical effect.

## Bounded release language

A full theorem-proving identification engine for arbitrary dynamic graphs is
not assumed. The proposal should specify a tractable supported subset and
record manual scientific judgments outside it. The book, however, must
explain the theory beyond the supported subset so that these boundaries are
defensible.

The prior synthetic studies, data component and software census are reusable
supporting material after the new intellectual structure is established.
Their existing byte and numerical audits remain valid for the version 2
artifacts, not for claims that have not yet been written and reviewed.
