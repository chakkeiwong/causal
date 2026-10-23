# Compare dynamic funding models on moments, shocks and policy targets

Forecasting balances, estimating a dynamic-panel coefficient, tracing an
identified structural shock and evaluating a changed pricing rule are four
different requests. A common interface must retain the observation and
availability clocks, branch and date population, action definition,
instrument restrictions, horizon and uncertainty event. A successful fit
or impulse-response plot cannot supply missing identification.
\citep{exec19_dynamic_stata_ab,exec19_dynamic_stata_lp,exec13_ct_stata_svar}

For B_it=rho B_i,t-1+beta A_it+nu_i+epsilon_it, differencing removes nu_i
but leaves a lagged outcome correlated with the differenced disturbance.
Lagged-level instruments require timing and error restrictions. Strictly
exogenous, predetermined and endogenous actions admit different moments.
The reviewed Stata xtabond path uses a many-panel/few-period regime and
requires the stated idiosyncratic-error conditions. Its robust two-step
Windmeijer correction changes variance estimation; it cannot establish
instrument exclusion or remove a nonzero population moment.
\citep{exec19_dynamic_stata_ab}

System GMM adds level equations instrumented by lagged differences. The
reviewed xtdpdsys manual supplies an additional initial-condition restriction,
motivated in part by weak difference-equation instruments under persistence.
That is additional model information. In an exact example with rho=1/2
and independent fair signs nu,eta,epsilon_2,epsilon_3, initialization B_1=nu
gives Delta B_2=nu/2+epsilon_2 and
E[Delta B_2(nu+epsilon_3)]=1/2. Initialization B_1=2nu+eta instead gives
Delta B_2=-eta/2+epsilon_2 and that moment zero. Enumeration of all sixteen
states verifies both identities. More branches cannot cure the first
population violation; the second identity does not qualify every other
system-GMM moment. \citep{exec19_dynamic_stata_system,exec19_dynamic_reference}

## Instrument construction and uncertainty defaults

EViews' inspected panel chapter distinguishes first differences and
orthogonal deviations, period-specific lag expansion through @DYN and
level instruments within transformed equations through @LEV. For one
series with all eligible period-specific levels from lag two backward,
K(T)=(T-1)(T-2)/2 gives 171 instruments at twenty dates. This counts a
declared uncollapsed construction, not effective rank under every missing
history. Return actual columns, lag windows, transformations, rank and
one/two-step weighting rather than only the estimator name.
\citep{exec19_dynamic_eviews_panel,exec19_dynamic_reference}

The EViews source also distinguishes period, individual and two-way
covariance choices and restricts some weights after transformation. One
displayed label requires edition-specific clarification. Stata supplies
serial-correlation and instrument diagnostics and warns about proliferation.
Nonrejection of an overidentification or serial-correlation test does not
prove all moments or the treatment assignment story. A collapsed or
restricted instrument design changes the estimator and must be frozen
before the qualification study, not selected to obtain favorable tests.
\citep{exec19_dynamic_eviews_panel,exec19_dynamic_stata_ab}

The open-source linearmodels review currently supports a narrower pinned
linear-IV reference. Its rank, weighting and covariance contracts do not
establish a qualified dynamic-panel-GMM implementation. Statsmodels and
other dynamic-panel candidates require operation-specific technical review
and matched trials before a broader adoption or port decision. R dbnR,
Python CausalAI and native Mocapy++ provide other reviewed modeling routes,
but their dynamic prediction, discovery or supplied-model inference targets
are not substitutes for panel instrument validity.
\citep{exec22_linearmodels_reuse,exec14_rtime_dbnr,exec14_pt_causalai,exec16_ct_mocapy}

## Common shocks determine the independent information

In the authored law Z_it=theta+U_t+E_it, independent dates have unit-variance
common shocks U_t and independent unit-variance branch-date shocks E_it.
The grand mean has variance 1/T+1/(NT); declaring all NT rows independent
instead gives 2/(NT). For three branches and two dates, enumeration of 256
fair-sign histories gives 2/3 versus 1/3. At N=100,T=25 the values are
101/2500 and 1/1250, a ratio of 50.5. At a stipulated USD 10,000 per
response unit, their standard deviations are approximately USD 2,010 and
USD 283. These are population standard deviations under a constructed law,
not empirical confidence intervals or evidence of a package failure.
\citep{exec19_dynamic_reference}

Clustering by date is a relevant option, but 25 dates alone does not prove
finite-sample calibration. Persistent calendar shocks, heterogeneous
loadings and missing dates require more analysis. Saturated date effects
can also absorb a bank-wide action that varies only by date. The appropriate
repair may require exposure variation, an external instrument, a longer
independent calendar or a different design. It cannot be chosen separately
from the target and information available.

## Structural restrictions and horizons change monetary value

Consider a two-variable reduced transition F=[[1/2,0],[1/5,1/2]] with
innovation covariance [[1,1/2],[1/2,1]]. Two structural orderings with
independent disturbances reproduce this same reduced law. A 0.25-point
rate shock has initial deviations (1/4,1/8) when rate is ordered first
and (1/4,0) when balance is ordered first. At horizons zero through two,
the balance responses sum to 51/160 and 1/10 million dollars respectively.
At monthly margin 1/500 per balance dollar and total cost USD 500, the
three-period net values are USD 137.50 and minus USD 300. Matrix-power
and direct-recursion calculations agree. These supplied restrictions
produce different intervention experiments despite identical reduced fit.
\citep{exec13_ct_examples}

Stata's structural-VAR manual accordingly warns that convergence may occur
without identification. Its external-instrument VAR route requires
relevance, exclusion and normalization and distinguishes single- and
multiple-shock specifications. The lpirf route offers horizon/lag controls,
OLS/robust/HAC covariance, divisor and small-sample options. Long horizons
reduce usable observations; pointwise bands do not imply simultaneous
coverage across horizons. Compare methods only after shock units, available
information, retained horizons and the coverage event agree.
\citep{exec13_ct_stata_svar,exec13_ct_stata_ivsvar,exec19_dynamic_stata_lp}

SAS VARMAX's inspected Granger and structural descriptions, IBM's predictive
TCM and Mplus DSEM/RDSEM are substantive commercial alternatives with their
own assumptions. Supplied latent-state inference also remains a different
route. Documentary evidence does not establish licenses, wrapper parity or
current prices. The inspected Stata/EViews dates and later acquisition do
not authenticate every byte or entitlement at the client cutoff; inaccessible
MathWorks and unresolved OxMetrics originals remain omissions.
\citep{exec13_ct_sas_causal,exec13_ct_sas_structural,exec13_ct_ibm_tcm,exec13_ct_mplus81}

The proposed public comparison should freeze valid and invalid initial
conditions, weak moments, common shocks, rank failure, irregular dates and
long-horizon loss of support. Use independent moment and response oracles;
retain instruments, effective dates, pointwise/joint uncertainty definitions,
all failures and whole-workflow costs. These steps can justify a prototype
and later expensive experiments. Source census completion, general dependence
repair, native qualification and bank economics remain separate gaps.
