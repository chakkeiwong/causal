# Match temporal discovery to its clock and intervention experiment

A funding-rate movement may be a decision, a response to a market shock,
a changed assignment mechanism or another observation of a persistent
process. A method must declare physical frequency, availability time,
subject boundaries, lag range, contemporaneous edges, stationarity and
regime information before its graph can support a causal question. An
intervention request additionally needs target variables, perfect versus
soft mechanisms, known versus unknown targets and assumptions about
mechanisms left unchanged. \citep{exec14_pt_contract,exec15_javatemporal_design}

For column vectors, write x_t=B_0 x_t+sum_l B_l x_(t-l)+epsilon_t, with
B_l[target,source]. Reduced coefficients are Phi_l=(I-B_0)^(-1)B_l.
An acyclic B_0 does not ensure dynamic stability. A structural innovation,
an equation replacement and a sustained feedback policy are distinct
interventions; prediction coefficients cannot be labeled their responses
without the identifying restrictions. Horizon, discounting and units also
belong to the query. \citep{exec14_pt_paper_dynotears,exec14_pt_exact}

## The available temporal families

Tigramite's PCMCI+, LPCMCI, J-PCMCI+ and RPCMCI profiles answer different
questions. LPCMCI retains latent-graph endpoints; J-PCMCI+ uses context
assumptions including exogeneity and restrictions on context-system
confounding; RPCMCI learns persistent regimes rather than observing
randomized intervention labels. The reviewed RPCMCI constructor replaces
a supplied mask, so an adapter must explicitly reject or resolve that
request. Context-to-system orientations and effective graph restrictions
must be retained rather than attributed wholly to tests on the data.
\citep{exec14_pt_tigramite,exec14_pt_paper_jpcmci,exec14_pt_paper_rpcmci}

CausalAI's selected PC and Granger routes search strictly negative lags;
its VARLiNGAM wrapper also exposes lag zero. It forms windows separately
within arrays but has no physical timestamp argument. Singular-design
branches substitute p-values of one, which must remain distinguishable
from valid large p-values. CausalNex DYNOTEARS checks integer ordering and
splits gaps but permits duplicate indices in the inspected transformer;
within-slice acyclicity and numerical convergence still do not establish
stationarity or causal identification. Its maintenance notice supports
reference use while default dependency adoption remains deferred.
\citep{exec14_pt_causalai,exec14_pt_causalnex,exec14_causalnex_primary}

R causalDisco's tiered TPC/TFCI and the separate tpc package primarily
constrain variable order. Their knowledge sentinels and graph-class
conversions need explicit provenance. dbnR supplies Gaussian dynamic-network
and folding routes with an ID filter, but matching IDs does not establish
equal physical intervals. Java Tetrad's selected lag builder likewise
uses row positions without subject or timestamp arguments. Its tuple-first
bootstrap avoids fabricated raw-row transitions on the applicable path
but does not establish dependence-valid uncertainty. These are separate
cohort, series and resampling contracts. \citep{exec14_rtime_causaldisco,exec14_rtime_tpc,exec14_rtime_dbnr,exec15_javatemporal_tetrad}

Native pcalg supplies a C++ interventional search kernel through R, including
target-row preprocessing, index conversion and score configuration. aGrUM's
reviewed dynamic helper constructs supplied models; Mocapy++ performs
inference and parameter learning on supplied structures; sDBN offers native
temporal training paths. A common C++ label does not make those operations
equivalent. Commercial GeNIe/SMILE supplies dynamic-model inference and
parameter learning with explicit slice/state APIs, while the inspected
GeNIe manual says its structure learner does not learn DBN structure.
IBM's Temporal Causal Models describes Granger prediction. These are useful
baselines with different targets and edition/cutoff limits.
\citep{exec16_ct_pcalg,exec16_ct_agrum,exec16_ct_mocapy,exec16_ct_sdbn,exec13_ct_genie_learning,exec13_ct_smile_tutorial,exec13_ct_ibm_tcm}

## Common calendars and physical aggregation can defeat a causal reading

Let U be an independent fair shock each day, S=U XOR E_S, and next-period
T=U XOR E_T, where the two errors are independent Bernoulli(1/4). The
joint probabilities of (S,T) are 5/16,3/16,3/16,5/16. Observed future risks
are 3/8 and 5/8; changing S leaves both causal risks at 1/2. Thus temporal
predictive information coexists with zero intervention effect. At USD 100
per event, the naive risk difference suggests USD 25 per account. Duplicating
accounts under the same calendar shock creates no new independent shock
units. The exact finite-law replay checks this counterexample.
\citep{exec17_temporal_oracle}

In another exact system, B_0=[[0,0],[1/2,0]] and
B_1=diag(1/2,1/4). Then Phi_1=[[1/2,0],[1/4,1/4]] and a unit structural
innovation in the first equation has second-coordinate responses
1/2,3/8,7/32 at horizons zero, one and two. Their first-three-period sum
is 35/32, or USD 109.375 at USD 100 per unit, before any action cost.
Recovering B_1 requires (I-B_0)Phi_1; applying the inverse again answers
another algebraic question. This construction fixes a daily clock and
a structural shock; it does not define a sustained rate policy.
\citep{exec17_temporal_oracle}

Sampling every second day can also erase the target sign. Stationary AR(1)
laws with rho=1/2 and rho=-1/2 and innovation variance 3/4 both have unit
variance; their two-day observed transitions have coefficient 1/4 and
innovation variance 15/16. Their observed Gaussian laws coincide while
one-day impulses have opposite signs. No additional rows from the same
coarsened law recover that lost sign without restrictions or new information.
Pooling equal-sized eras with slopes +1 and -1 similarly gives zero pooled
linear slope while hiding opposing regime responses.
\citep{exec14_pt_exact,exec17_temporal_oracle}

## Known interventions, unknown targets and numerical search

The GIES formulation uses independent observations under a conservative
family of known perfect interventions: every variable remains unmanipulated
in at least one environment. Python's reviewed Gaussian score centers by
environment and uses rows not intervened on the scored node. Its estimated
I-essential graph retains reversible edges, distinct from a representative
DAG. The R/native path additionally has a documented versus actual intercept
default discrepancy and integer-index conversion. Explicit targets, row
alignment, intercepts, effective sample counts and failed scores are part
of the method. Shared-calendar panel observations need an additional
sampling argument. \citep{exec14_pt_paper_gies,exec14_pt_gies,exec16_ct_pcalg}

Perfect replacement and a soft shift cannot be distinguished by action
means alone. With independent standard Gaussian H,U,W, take A=H+U and
Y=2A+H+W. Replacing A by delta+Z with independent Var(Z)=2 and shifting
it to H+U+delta both give mean delta, variance 2 and mean outcome 2delta.
But Cov(H,A) is zero versus one and Cov(A,Y) four versus five. The target
label must carry the intervention's mechanism, not just an indicator.
\citep{exec14_pt_exact}

Unknown-target IGSP needs both CI and invariance testers under the paper's
conditions. The selected facade delegates to other packages, and its
inspected default lexicographic score differs from the paper's sum.
DCDI distinguishes perfect known/unknown and imperfect known targets,
while imperfect unknown targets raise an unimplemented error. Population
optimum arguments do not certify a finite nonconvex run. These routes
remain scoped candidates, with exact dependency identities and method
correspondence required before qualification.
\citep{exec14_pt_causaldag,exec14_pt_gml,exec14_pt_paper_utigsp,exec14_pt_dcdi,exec14_pt_paper_dcdi}

The proposed comparison should preserve graph endpoints, both clocks,
window membership, effective constraints, context and intervention metadata,
score settings, missing tests and search exits. Use independent structural
and graph oracles, include common shocks, irregular dates, wrong targets,
soft/perfect mismatches, hidden confounding and regime changes, and retain
all failures. Source coverage, dependency rights and native qualification
remain open. Exact examples demonstrate why these contracts matter; they
do not establish bank ROI, general graph confidence or final acceptance.
