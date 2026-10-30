# Scholarly sufficiency review and withdrawal of version 2

8 October 2026 (Asia/Shanghai).

The user's diagnosis is accepted. The remaining problem precedes banking
validation: the commissioned theoretical survey and the scientific derivation
of the product are incomplete. The version 2 scholarly-completion claim is
withdrawn. Its PDF, code, numerical results and archived sources remain usable
inputs where correct. Their existence does not establish the required scholarship.

## What the additional references establish

Selected substantive passages were read in all three reference projects.
[The inspection record](reference-standards-2026-10-08.json) preserves exact
passages and hashes. This is a comparison of exposition and construction,
not an independent correctness review of the reference monographs.

| Reference passage | Observed structure | Requirement for the causal monograph |
|---|---|---|
| BayesFilter: state-space contracts | Defines the initial, transition and observation laws; distinguishes stochastic innovations, deterministic coordinates and masks; derives consequences for backend behavior. | Define causal model classes, information sets, observations and interventions precisely before designing APIs. A field name or JSON validator is not the mathematical contract. |
| BayesFilter: Kalman score | Derives prediction, innovation, likelihood-score, gain and update derivatives; follows the same scalar likelihood through missing-data masks and numerical representations. | Follow an identified functional through nuisance estimation, estimator construction and inference. Explain which approximations preserve or change the target. |
| BayesFilter: particle-flow foundations and target suitability | Starts with probability laws, derives the normalized homotopy, states conditions for differentiation, and compares the targets of successive algorithmic constructions. | Develop each major method from its mathematical objects and assumptions; compare alternatives at the level of the object they identify or estimate. Naming a method or caveating its limits is insufficient. |
| CIP: identification and parameterization | Relates physical dynamics, risk prices and risk-neutral dynamics before deciding free parameters. | Derive the constraints connecting causal, structural, observational and statistical representations before choosing a parameterization or estimator. |
| CIP: MIDAS construction and literature comparison | Distinguishes forecasting, filtering and structural weights; derives a persistence-related near-equivalence; compares source-specific estimators and their different targets. | Explain what each neighboring literature solves, prove or delimit the connections, and use those distinctions to select product capabilities. |
| FinMarketing: heterogeneous effects and DML | Develops T/S/X/R/DR constructions, conditional losses and remainders, orthogonality and target-specific rate requirements. | The causal product requires at least this depth on its core field, including inference and inverse problems beyond one AIPW example. |
| FinMarketing: dynamic discrete choice bridge | Matches primitives to MDPs; derives the contraction, likelihood loop and CCP continuation system; preserves the difference between observed behavior and a bank's objective. | Derive the longitudinal/SCM/state-space/POMDP relationships and identify the extra assumptions needed at every transition. |

The standard is a research monograph that builds understanding and an
implementable scientific design. It can explain why a construction is valid,
when it fails, how its neighbors differ, and how those conclusions change the
product. This requires sustained argument and intellectual coverage.

## Why the previous acceptance process failed

The first structure treated method names as coverage units. The corrective
version then improved selected derivations and added fitted examples around
that structure. That repaired individual passages while leaving the field's
foundations and connections incomplete.

The resulting review asked whether topics were present and claims were
cautioned, rather than whether the reader could reconstruct the theory.
It also relied too heavily on checks that were easy to finish: preserved
PDFs, compiled references, exact examples, generated tables and rendered pages.
Those checks were useful but could all pass for a scientifically incomplete book.

The previous response about remaining gaps repeated the error: it foregrounded
bank-data validation and runtime evidence when elementary scholarly work was
still missing. A real-data pilot is not needed to derive graphical identification,
instrumental-variable arguments, semiparametric estimation or the relationship
between longitudinal interventions and state-space likelihoods.

A further failure was the definition of scope. Calling the work a proposal
correctly limits claims of implemented software. It does not lower the standard
of theoretical scholarship or excuse gaps in the core scientific design.

## Current gaps: presence is not adequate treatment

| Topic | Material actually present in version 2 | Missing construction |
|---|---|---|
| Causal diagrams | Brief DAG/CPDAG/PAG descriptions, a discovery table and graph-related cautions. | A worked process for constructing a diagram from mechanisms; SCM semantics; exogenous variables; d- and m-separation; latent projection; adjustment and intervention transformations; mediation/selection; the relation between assumed and discovered graphs. |
| Graphs and IV | A Wald expression, short assumption list, panel moments and a local-projection IV formula. | The graphical/structural derivation of validity; why the IV graph does not generally identify the ATE; linear moments and 2SLS/GMM, heterogeneous LATE, weak identification, nonlinear/nonparametric IV, and the connection to learned nuisance functions and proxies. |
| Causal inference and ML | AIPW bias, partially linear residualization and brief learner/sequence-model descriptions. | Statistical models and pathwise derivatives; efficient influence functions and orthogonalization; target-specific rates; complete learner comparisons; honest effect/policy learning; IV inverse problems; representation and invariance theories; their dependence assumptions. |
| Longitudinal causal inference | G-formula/IPW, recursive DR, a feedback example and sketches of targeting and structural blips. | A coherent development from longitudinal causal graphs through sequential identification, MSMs/SNMMs/g-estimation/TMLE, policy learning and censoring; proofs of the relevant bridges rather than parallel descriptions. |
| Longitudinal methods and state-space models | A separate controlled-HMM likelihood, filter, EM study and nonidentification example. | One generative account joining observed histories, latent mechanisms, action assignment and observation selection; conditions for policy replacement and state reduction; likelihood identification versus intervention identification; filtered versus smoothed information and parameter uncertainty. |
| Time series and discovery | Dependence formulas, simple VAR equivalence and algorithm summaries. | Sustained causal time-series/system-identification treatment; aggregation/feedback/latent projection; inference with learned quantities; derivations of discovery procedures and how graph uncertainty propagates into effect identification. |
| Scientific product design | Proposed compiler/adapters/evidence records and two narrow components. | The representations and supported mathematical transformations the compiler actually needs; derivation or witness for an identification result; an explicit distinction between nonidentification and unsupported software; estimand-specific estimation and inference composition. |

Existing useful results must be reviewed in their proper place. They must not
dictate the new book's architecture simply because they have already been written.

## Corrective decision

Rebuild from a connected field map. Primary literature and theoretical
reconstruction precede the final product design. Treat graphs-to-IV,
identification-to-ML, and longitudinal-to-state-space as central arguments,
with worked examples, explicit extra assumptions and counterexamples.

The active program is [master-program.md](../program/master-program.md).
The initial [theory coverage map](../program/theory-map.md) identifies the
questions and dependencies to research. It is a planning artifact, not evidence
that the corresponding scholarship has been completed.

The source archive remains mandatory: every paper eventually cited in the
monograph must have its real PDF, required filename, version identity, inspected
anchors and auditable claim record. Existing source-byte audits stay useful;
their scope must never be promoted to scholarly sufficiency.

The version 2 delivery and completion records are preserved in
[the history archive](../program/history/v2-rejected-delivery.zip).
Mission control now records an incomplete scholarly reconstruction. No new
completed monograph or independent review is claimed.
