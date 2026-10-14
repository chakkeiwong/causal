## Commercial temporal models and intervention discovery

\label{exec13:commercial-temporal}

### The commercial comparison starts with the decision clock

A funding committee asks whether raising a quoted deposit rate by 25 basis
points for one month will increase retained balances enough to cover the
additional expense. A forecasting team asks whether past rates improve its
balance forecast. A risk team asks whether the same relationship survives a
change in the historical pricing policy. All three questions use time series,
but they require different outputs. A predictive lag coefficient can answer
the second question without identifying either of the other two.

The commercial landscape already provides substantial functionality relevant
to these questions. GeNIe and SMILE represent supplied dynamic Bayesian
networks, update beliefs over time, and learn parameters in a declared
structure. IBM SPSS offers automatic selection of predictive inputs in
temporal models. SAS and Stata provide established multivariate time-series
interfaces, while Stata separately exposes structural restrictions and
external-instrument identification. Mplus supplies intensive-longitudinal
models with random effects, latent decompositions and explicit time-series
syntax. BayesiaLab documents the distinction between observation and
intervention and provides graph-based causal-analysis workflows. The
proposal should explain how these capabilities can be used and where its
own implementation is less mature; their existence rules out a claim that
commercial software offers only correlation tables.

This comparison is bounded to inspected official technical text. GeNIe's
manual identifies itself as 5.0.R2, built in November 2024; the SMILE manual
identifies itself as 2.2.4.R1, built in April 2024. Other anchors are SAS/ETS
14.1, the Mplus 8.1 language addendum, IBM's SPSS Statistics 31.0.0
documentation route, and the retrieved Stata command manuals. Mutable pages
were acquired on 13 October 2026, after the 7 October literature cutoff.
Edition labels identify what was inspected; they do not independently
authenticate the exact bytes served on the cutoff date. No vendor engine or
paid deployment was executed for this comparison.
\citep{exec13_genie_readme,exec13_smile_intro,exec13_ct_genie_learning,
exec13_ct_sas_causal,exec13_ct_mplus81,exec13_ct_ibm_tcm,exec13_ct_stata_granger}

The proposed request should state five things before selecting a package.
The sampling interval identifies the meaning of a lag. The information clock
specifies which balances, quotes and macro releases were available at each
decision. The contemporaneous model specifies whether a within-month
response can precede another measured variable. The intervention states
whether the bank replaces an action once, maintains a policy, or responds
to a structural shock. Finally, the sampling law distinguishes a long
calendar, independent experimental units and branches sharing common shocks.
These fields determine which commercial result can be interpreted as an
answer, and which can serve only as a diagnostic or candidate model.

### Dynamic Bayesian networks: a strong supplied-model baseline

The GeNIe dynamic-model overview defines a dynamic Bayesian network as a
discrete-time model of a stochastic process. It explicitly says that the
temporal extension does not itself mean that the structure or parameters
change over time: its described process is stationary. It permits temporal
observations and discusses both discrete and continuous examples. Those
statements concern the representation and evaluation of a supplied model;
they are not a guarantee that the model's scientific mechanisms are stable
under a bank intervention.\citep{exec13_ct_genie_dbn}

The parameter-learning page resolves an otherwise consequential ambiguity.
It states that GeNIe's structure-learning algorithms do not learn the
structure of dynamic models, while the parameters of an existing DBN can be
learned from time series. The network structure must already be defined.
Data columns use a node identifier followed by an underscore and time-step
number, except at time zero. The interface matches model nodes and states
to those columns and then applies EM; the structure remains unchanged and
existing network evidence is ignored during parameter learning.
\citep{exec13_ct_genie_learning}

This is a valuable comparator for a servicing or funding prototype. A bank
can supply a hypothesized state-transition graph, use the tool to fit its
parameters and inspect temporal predictions. It cannot infer from a
successful fit that the same software discovered that graph, identified a
rate intervention, or selected between hidden-information alternatives.
Nor does the discrete-DBN parameter-learning page establish parameter
learning for every continuous model mentioned elsewhere in the manual.

SMILE's C++ tutorial makes the integration contract unusually concrete.
It uses `SetTemporalType` for plate nodes, `AddTemporalArc` with an explicit
lag order, separate initial and temporal conditional probability tables,
and `SetNumberOfSlices` for unrolling. `SetTemporalEvidence` receives a
time index and an integer outcome index. Temporal beliefs are returned in
a matrix whose adjacent entries correspond to outcomes within a slice.
An adapter must preserve those outcome indices, the distinction between
initial and transition distributions, lag order and the number of slices.
A swapped state ordering would change the meaning of the result while
leaving a superficially valid array.\citep{exec13_ct_smile_tutorial}

The maintained C++ library and its documented Java, Python and R wrappers
are plausible integration routes. They are not evidence that every wrapper
exposes the same temporal operations or numerical behavior. The inspected
license distinguishes development from deployment, including server and
distributed-program deployment. Academic use has stated eligibility and
purpose restrictions. The appropriate proposal decision is to consider a
licensed local adapter for supplied-model inference, with wrapper parity
and deployment terms checked for the chosen configuration. Porting its
proprietary engine is not an available open-source reuse strategy.
\citep{exec13_smile_intro,exec13_smile_license}

### Automated temporal prediction and the meaning of “causal”

IBM's Temporal Causal Models page says that the procedure constructs an
autoregressive model for each target and selects inputs from candidate
series. It then explicitly defines “causal” in this context as Granger
causality: past values of another series improve prediction beyond the
target's own past. It supports column-based series and a multidimensional
representation in which categorical dimensions distinguish series. The GUI
can produce `TCM MODEL` syntax. These are substantive workflow capabilities
that the proposed local causal library does not presently reproduce.
\citep{exec13_ct_ibm_tcm}

The correct comparison is with automated predictive model selection.
Representing many branch series does not by itself establish the sampling
law for a policy-effect interval, and selecting a controllable predictor
does not establish that changing it will change the target. The inspected
overview links time-interval, aggregation, missing-value and model-build
options, but the retrieved detailed routes did not return their technical
content. Defaults for lag selection, transformation and aggregation therefore
remain unverified here. The overview is sufficient to establish the
procedure's stated Granger meaning; it is insufficient for a full
configuration or performance comparison.

Stata's `vargranger` is similarly explicit. It performs equation-specific
Wald tests that the coefficients on another endogenous variable's lags are
jointly zero. When it follows a structural VAR command, these tests still
concern the underlying reduced-form VAR. A structural command name does not
change the null hypothesis of the postestimation test.
\citep{exec13_ct_stata_granger}

The SAS/ETS 14.1 `CAUSAL` statement also documents Granger tests based on a
VAR of the variables listed in `GROUP1` and `GROUP2`, with the order supplied
by `MODEL`. It is not applicable with order zero. Its example treats the
group declarations as material to the fitted test. An integration must
therefore record the actual series in each test and its lag specification,
including whether a contextual variable was excluded. A request for
“causality” cannot be translated merely by matching it to a command named
`CAUSAL`.\citep{exec13_ct_sas_causal}

Consider an exact project counterexample. Let an unobserved liquidity factor
follow

\[
 U_t=\tfrac45U_{t-1}+e_t,\qquad
 \operatorname{var}(U_t)=1,\quad \operatorname{var}(e_t)=\tfrac9{25},
\]

with stationary Gaussian initialization. Set the observed rate deviation
and next balance deviation to

\[
 A_t=U_t+\nu_t,\qquad Y_{t+1}=U_t+\eta_{t+1},
\]

where all measurement innovations are independent, centered, and have
variance one; they are also independent of the factor innovations. Rates
are measured in percentage points and balances in USD millions. This is a
stipulated law, not an estimated banking relationship. Conditional on the
single balance lag \(Y_t\),

\[
 \begin{aligned}
 \operatorname{cov}(Y_{t+1},A_t\mid Y_t)&=1-(4/5)^2/2=17/25,\\
 \operatorname{var}(A_t\mid Y_t)&=2-(4/5)^2/2=42/25.
 \end{aligned}
\]

The population predictive coefficient is \(17/42\). Adding the observed
rate reduces prediction mean squared error from \(42/25\) to \(59/42\).
Thus it is a useful predictor relative to this declared one-lag baseline.
Replacing only the equation for \(A_t\) changes neither \(U_t\) nor the
equation for \(Y_{t+1}\); the rate intervention effect is zero. Treating
the predictive coefficient as an effect would attribute
\(\tfrac14(17/42)=17/168\) million dollars of balances to a 25-basis-point
action in this example. No such causal increase occurs.
\citep{exec13_ct_examples}

This calculation neither reports a vendor false positive nor proves a
failure of its documented prediction task. It shows why a bank action
requires an additional identifying argument. It also keeps the conditioning
history explicit: the displayed coefficient is for the stated one-lag
predictor comparison, not an unproved statement about every possible
infinite-history test.

### Structural restrictions and external instruments deserve separate credit

Stata's `svar` is an intervention-relevant comparator beyond a Granger test.
Its manual allows user-specified short-run or long-run restrictions on
structural impulse responses and explains their economic motivation. The
interface records lag choices, exogenous variables and constraint matrices.
It also documents a local-identification check and warns that a model that
is not structurally identified can nevertheless converge. Disabling that
check must not be interpreted by an adapter as scientific approval.
\citep{exec13_ct_stata_svar}

`ivsvar` supplies another route. The inspected manual describes a GMM
estimator for a single target shock and a minimum-distance estimator for
multiple target shocks. An instrument is correlated with the target shock
and uncorrelated with nontarget shocks. The additional information identifies
the relevant impact column up to its normalization; it does not identify
all other shocks. Multiple-target designs require further restrictions.
The GMM interface exposes robust, cluster and HAC variance options and an
impact scale. These are documented capabilities, not a claim that a noisy
bank announcement or an arbitrary policy date satisfies the instrument
conditions.\citep{exec13_ct_stata_ivsvar}

The distinction can be developed without relying on a software run. Suppose
a two-variable monthly reduced-form process for rate and balance deviations
has

\[
 X_t=FX_{t-1}+u_t,\qquad
 F=\begin{pmatrix}1/2&0\\1/5&1/2\end{pmatrix},\quad
 \Sigma_u=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix}.
\]

Its eigenvalues are both \(1/2\), so a stationary Gaussian law exists.
Two structural representations have coefficient matrices

\[
 D_1=\begin{pmatrix}1&0\\-1/2&1\end{pmatrix},\qquad
 D_2=\begin{pmatrix}1&-1/2\\0&1\end{pmatrix}.
\]

Writing \(D_jX_t=D_jFX_{t-1}+\varepsilon_{jt}\), the disturbance
covariances are respectively
\(\operatorname{diag}(1,3/4)\) and
\(\operatorname{diag}(3/4,1)\). Both yield exactly the same \(F\),
\(\Sigma_u\) and stationary observed process. They disagree about the
contemporaneous ordering: the first permits a within-month rate effect on
balances; the second orders the balance before the rate. The structural
lag matrices also differ, as required to preserve the same reduced form.

Replace the rate equation once at month zero, raising its value by
\(\delta=1/4\) relative to the paired baseline, and then restore the
ordinary equations. Keep prior histories and disturbances fixed in that
comparison. The impact changes are \((\delta,\delta/2)'\) under the
first structure and \((\delta,0)'\) under the second. Subsequent expected
differences propagate by \(F^h\). The resulting balance responses are:

| Month after the action | Rate precedes balance, USD million | Balance precedes rate, USD million |
|---|---:|---:|
| 0 | 0.12500 | 0.00000 |
| 1 | 0.11250 | 0.05000 |
| 2 | 0.08125 | 0.05000 |

With an assumed monthly net margin of 0.2 percent on each incremental
balance, no discounting over these three months, and an assumed total
action cost of USD 500, the values are USD 137.50 and minus USD 300.
Every input is a planning assumption. An exact symbolic calculation checks
both structural covariance factorizations, both response recursions and
the monetary conversion.\citep{exec13_ct_examples}

The intervention is a single equation replacement. A policy maintaining
the higher rate in every month is a different sequence of replacements;
it cannot be inferred by silently reusing this impulse response. Likewise,
a unit structural-shock response needs its shock normalization and its
relationship to the controllable rate stated explicitly. A valid external
instrument could provide information that distinguishes particular shock
responses, but its validity is additional evidence rather than a consequence
of fitting this covariance.

SAS's inspected dynamic-simultaneous-equations discussion provides a related
warning. It describes a lower-triangular representation obtained from the
innovation covariance and exposes it through `PRINT=(DYNAMIC)`. That is a
documented model representation. A triangular decomposition alone cannot
choose the economically correct contemporaneous order in the constructed
example. The HTML extraction omitted some equation images, so this
comparison uses the surviving prose and command description; the displayed
matrix derivation above is independently specified project work.
\citep{exec13_ct_sas_structural,exec13_ct_examples}

### Intensive longitudinal models and intervention analysis

Mplus's version 8.1 addendum distinguishes DSEM, which regresses an outcome
on its past, from RDSEM, which places autoregression on the residual after
contemporaneous predictors. RDSEM is documented for a single series and
two-level models. Its syntax examples use `CLUSTER`, `LAGGED`,
`TYPE=TWOLEVEL RANDOM` and `ESTIMATOR=BAYES`, with random slopes and
within/between components. The addendum also includes linear-trend
examples and lagged categorical outcomes. These are valuable alternatives
for heterogeneous customer histories and measurement processes.
\citep{exec13_ct_mplus81}

The time grid matters to the observation law. The addendum warns that a
covariate missing at one or more time points can exclude an observation,
including missingness arising with `TINTERVAL`. It illustrates bringing
that covariate into the model through an autoregression so missing-data
theory can be used. This changes the modeled system; it is not a universal
permission to fill irregular bank records. The analyst still needs a
meaningful time unit, a missingness argument, and assumptions about the
mechanisms and random effects.

For the proposal, Mplus is a model-fitting and heterogeneity comparator,
with richer longitudinal syntax than the current narrow local prototype.
The inspected addendum does not establish automatic discovery of a causal
equivalence class, identification of an observational policy intervention,
or calibrated uncertainty over unknown causal structure. A posterior for
a supplied dynamic model and a confidence set covering alternative
intervention structures answer different questions. Regime changes and
nonstationary mechanisms must be modeled and checked explicitly; a trend
example is not evidence that arbitrary regime drift is supported.

BayesiaLab should also receive explicit causal credit. Its feature page
distinguishes hard and uncertain evidence from intervention analysis and
names Graph Surgery and Likelihood Matching as causal-estimation workflows.
Its technical e-book section distinguishes identification from estimation:
identification requires a causal model or partial knowledge of data
generation, with the chapter expressing the assumptions in a DAG. The text
states that more observations cannot compensate for absent causal
assumptions.\citep{exec13_ct_bayesia_inference,exec13_ct_bayesia_identification}

These sources support an intervention-analysis comparator for an asserted
model. They do not, in the pages inspected here, establish a temporal
discovery algorithm that learns lags, latent confounding, contemporaneous
equivalence classes and regime changes together. A candidate integration
would first check the exact edition/API operation, graph semantics,
supported identification route, and representation of an unavailable
effect. Commercial capability must not be inferred from a feature label,
but the proposal must equally avoid claiming graph-based intervention
analysis as its exclusive innovation.

### Frequency, common calendars and uncertainty belong in the interface

The transition coefficient changes with the sampling interval. For the
constructed monthly process, observing quarter-end stocks gives

\[
 X_{3k}=F^3X_{3k-3}+u_{3k}+Fu_{3k-1}+F^2u_{3k-2},\qquad
 F^3=\begin{pmatrix}1/8&0\\3/20&1/8\end{pmatrix}.
\]

The monthly cross-lag coefficient is \(1/5\), while the quarter-end
coefficient is \(3/20\), not three times the monthly coefficient. The
quarterly innovation covariance is
\(\Sigma_u+F\Sigma_uF'+F^2\Sigma_u(F^2)'\). Quarterly average balances
or cash-flow totals would require a different observation operator.
The exact example checks this covariance both by recursion and by a block
covariance calculation.\citep{exec13_ct_examples}

Consequently, an adapter must preserve whether a field is a stock, a flow,
an average or an end-of-period observation. It must also preserve timezone,
release lag and policy availability. Merely converting a monthly timestamp
to a quarterly label can change both the statistical model and the
banking target. A proposed regime intervention must state which equations
are invariant and which may change, instead of assuming that a historical
forecast carries over.

Common calendars create a separate uncertainty issue. Suppose a single
date's errors across twenty branches are \(C+\epsilon_i\), with common
variance \(1/2\), independent branch variance \(1/2\), and independence
between the two components. The variance of the branch mean is
\(1/2+1/40=21/40\). Incorrectly treating all twenty errors as independent
gives \(1/20\), understating variance by a factor of \(21/2\).
This is a specified example, not an estimated correction for bank data.
\citep{exec13_ct_examples}

A package can expose cluster or HAC options, as the inspected Stata
instrumental-SVAR interface does, while the analyst still has to justify
the chosen asymptotic units and dependence assumptions. A collection of
branch models is not automatically a collection of independent calendars.
Neither a Granger-test level nor a posterior interval in one supplied
graph becomes a simultaneous uncertainty guarantee over searched lags,
selected models, alternative graphs and intervention effects.

### What to assemble, what to retain as a comparator, and what is unresolved

The first product iteration should preserve typed outputs: predictive lag
tests, supplied-model temporal probabilities, structurally identified shock
responses, policy values and unresolved causal sets. It should not collapse
them into one numerical “causal effect” field. A reference result should
carry the time grid, information clock, graph/order restrictions, input
provenance, shock normalization, estimation settings, model-search history
and uncertainty interpretation. This is proposed integration behavior,
not a claim of an installed commercial connector.

| Candidate route | Proposed use | Required boundary before integration |
|---|---|---|
| GeNIe/SMILE | Supplied DBN fitting and temporal inference baseline | Preserve states, lags and initial/transition distributions; verify wrapper parity and development/deployment licenses |
| IBM SPSS TCM | Automated predictive-input and workflow comparator | Retain its Granger meaning; inspect actual lag/aggregation defaults and export contract |
| Stata VAR/SVAR/IV-SVAR | Predictive tests and restricted shock-response comparators | Bind restrictions, instrument assumptions, normalization and uncertainty settings |
| SAS VARMAX | Multivariate forecasting, groupwise prediction tests and supplied dynamic representation | Preserve groups, lag order and covariance/order assumptions; do not infer intervention identification from a triangular representation |
| Mplus DSEM/RDSEM | Supplied longitudinal/latent model and heterogeneity comparator | Bind time-grid/missingness choices and within/between model; no automatic discovery claim |
| BayesiaLab | Graph-based intervention-analysis comparator | Bind asserted causal information and inspect the selected API/edition's actual identification semantics |

The proposal currently lacks much of the mature fitting breadth, graphical
interaction, diagnostic output, temporal data management and commercial
support represented by these tools. Its defensible prospective contribution
is the preservation of scientific meaning across the chosen workflow,
including refusals and alternative models, together with a carefully bounded
banking evaluation. That contribution still needs a working adapter and
matched experiment. Reproducing every commercial estimator would add cost
without demonstrating that the integrated decision is better.

HUGIN, Netica, MATLAB Econometrics Toolbox, EViews, OxMetrics/PcGive,
LISREL and causaLens/decisionOS remain explicit additional candidates.
Their inherited identities, aliases and available official pages were
searched, but the bounded acquisition did not yield enough matching
temporal/intervention technical material for a capability verdict here.
Failures included an inaccessible HUGIN manual, a denied MATLAB page,
unresolved EViews/PcGive technical URLs, and navigation or marketing text
that does not settle method semantics. These are omissions in this
comparison, not findings that those products lack the capabilities.
Current license prices, deployment terms and temporal API parity also
remain unverified for most candidates.

The immediate repair is specific: obtain the edition-matched technical
manuals or public algorithm/API documentation for the unresolved candidates;
inspect the actual time-grid, selection, intervention and uncertainty
semantics; then select a narrowly matched licensed trial only if it could
change the prototype recommendation. Paid trials and bank data are not
prerequisites for writing this proposal. Until the evidence is available,
the recommendation remains a documented shortlist with the missing
comparisons visible.

\label{exec13:commercial-temporal-end}
