# Common scientific specification

8 October 2026. S01 execution specification, version 1. These choices define
the investigation and initial supported regimes; method qualification is
established by subsequent derivations and experiments, not this document.

Every request is (model class, observation map, intervention, population,
functional, sampling law, decision information). A method must return the
same functional under a valid information-preserving conversion. A confidence
set covers a parameter or identified set under a specified repetition law;
a posterior conditions on a supplied model/prior. Neither validates causal
restrictions by itself.

## Units, clocks and economic targets

An event has entity, event time, available time, source record and revision
identity. A feature at decision t uses the latest eligible version available
strictly before the decision, with an explicit tie rule. A flow is summed
over an interval; a stock is evaluated at a declared instant. Household,
account, branch, bank and calendar date are different statistical units.
The initial oracle views preserve all these distinctions. Study D receives
ambiguous raw records and must recover candidates rather than redefine truth.

For A, one unit of structural policy-rate impact is one percentage point;
response coefficients report balances/lending in declared currency units.
Discounted funding contribution is a separate deterministic functional of
the response path, pricing exposure and cost account. For B, the primary
target is a prespecified fixed-policy contrast in discounted reward over
eight decisions. Policies use recorded predecision history and eligible
actions. C queries a total intervention effect within each candidate
structural model. D returns observation interpretations and the scientific
queries each can support.

## Sampling regimes and initial support

| ID | Repeated experiment | Core model and initial inference route | Boundary |
|---|---|---|---|
| A-G | One long stationary calendar series | Finite-dimensional stable Gaussian linear process, fixed horizons and valid external instrument; moment ratio, Bartlett HAC and simultaneous bands; weak-IV residual-test inversion. | Fixed stability margin and dimension; not uniform near unit roots or an increasing horizon. |
| A-L | A series with many observed controls | Partially linear IV moments, two separated training/evaluation blocks under absolute regularity; bounded fitted functions, explicit product and HAC-error rates. Sparse regression is an initial fitted nuisance route. | Rates must hold for the actual learner; independent rows are not an alternative split. |
| A-P | Bank panel with shared shocks | Aggregate target-weighted entity scores by date, then use a time-series variance argument for that aggregate. | Large cross-section does not create independent monetary shocks. Random-population targets require additional cross-sectional uncertainty. |
| A-I | Persistent/integrated variables | Lag-augmented structural response or identified stationary transformation with explicit mapping to levels. | A-G HAC is not inherited by a unit-root process. Cointegrating rank and economic shock are distinct restrictions. |
| B-H | Independent full customer trajectories | Fixed-horizon observed-history sequential augmentation/targeting, whole-trajectory folds and trajectory score covariance. | Common calendar shocks need a different experiment; no arbitrary increasing-horizon guarantee. |
| B-L | Independent trajectories of a controlled hidden Markov model | Finite states/signals, exogenous randomized logging, full-rank informative emissions and transitions; constructive identification, likelihood fitting and fixed-policy value uncertainty. | Private-state logger and persistent hidden confounding are separate model assumptions, not automatic extensions. |
| C-G | Independent Gaussian vectors in a bounded graph class | Simultaneous covariance confidence set mapped through all compatible linear-Gaussian structural models; union of effect sets. | Conservative computation, fixed dimension; no faithfulness-based single-graph certainty required. |
| C-T | Stationary temporal data | Qualified temporal CI/graph procedure with lag, sufficiency and dependence conditions, followed by effect/ambiguity analysis. | If inferential graph coverage is unavailable, label output exploratory; no false arrow probabilities. |
| D-O | Raw records with known synthetic generating semantics | Candidate grammar, hard constraints, evidence ranking, retained alternatives and abstention. | Economic exclusion/exchangeability cannot be inferred from table syntax. |

These regimes are deliberately distinct. The monograph must explain how
their assumptions relate, including diagram/IV restrictions, semiparametric
gradients, state reduction, time aggregation and partial observation. The
14-domain field synthesis remains broader than these implementations.

## Method hierarchy to test

For A-G use direct response moments as the transparent primary reference,
with correctly specified proxy-VAR propagation as a challenger. Weak-IV
test inversion is an alternate inferential operation, not a normal-interval
fallback triggered by a convenient first-stage threshold. For A-L use a
cross-fitted orthogonal IV score; compare fixed low-dimensional regression
and sparse learned controls on the same target. Factor reduction is a
separate approximation hypothesis.

For B-H use sequential augmentation as the principal mean/value reference,
targeting for bounded outcomes and direct/weighting estimates as challengers.
For B-L compare a joint finite-state likelihood with a source-consistent
alternative and exact enumeration on small cases. An omitted logger is an
adverse misspecification, not an equally valid causal estimator.

For C-G retain model ambiguity explicitly. C-T evaluates a temporal discovery
library only within its stated assumptions; equivalence marks survive the
interface. D-O begins with deterministic, inspectable evidence and does not
fabricate probabilistic mapping confidence.

## Evidence and closure

Each study dossier states its primary sources already preserved, additional
search questions, algorithms to derive, repeated-sample contrasts and
unsupported cases. Source additions follow the genuine-PDF and audit rule.
Final simulations record seeds, failures and Monte Carlo precision. The
scientific operation is qualified only when its derivation, code, result
representation and empirical behavior refer to the same regime.

The next action is the A-G construction, with A-L/A-P/A-I developed as
distinct extensions. No claim that S02 or the monograph is complete follows
from fixing these specifications.

## Executed method decisions (S02–S07)

The version-1 specification above is retained as the pre-experiment plan.
The selected A-I route is stationary-change IV with cumulative level mapping;
lag augmentation remains a source-qualified alternative for its reduced-form
projection target. The selected C-T inference route is a stable Gaussian
VAR(1), supplied independent innovations/no contemporaneous edges and known
lag one. It yields a joint coefficient box and its intervention-response
image. PCMCI/LPCMCI and functional methods remain substantive survey
alternatives; generic graph-confidence coverage is not claimed for them.
This selection supplies the construction that the generic initial C-T row
left open; it does not silently promote exploratory discovery outputs.

The B-L fitted family has two states, binary signals, binary repayment,
exogenous randomized logging, unknown informative emissions and an eight-step
fixed reactive-versus-never-assist value contrast. The scale experiment also
evaluates a twelve-step contrast, under the same family and inference
argument. B-H uses an observed three-state servicing family, trajectory
cross-fitting and both augmentation and weighted-intercept targeting.
Six bounded recipes execute through tools/causal_study.py. A-L remains a
separately executable blocked-learning recipe with explicit learner settings.
