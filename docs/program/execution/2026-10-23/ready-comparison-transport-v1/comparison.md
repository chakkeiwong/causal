# Transport the causal target through missing-data workflows

A pilot effect is a statement about the pilot population under a specified
intervention and observation law. Deploying the same action in another branch
requires a target population, sufficient covariates for transporting the
relevant response, and source support for target histories. Completing missing
records supplies none of these assumptions by itself. Missingness reasons,
including an undefined variable, nonresponse and administrative follow-up,
must also remain distinct. The comparison therefore separates imputation,
analysis of completed datasets and causal transfer. \citep{exec21_transport_reference,exec17_s7_paths}

## Compare the documented workflows and their effective defaults

Stata's inspected mi manuals preserve original data at m=0 and completed
datasets at m=1,...,M, with four storage styles and regular, imputed and passive
variable roles. Extended missing values .a through .z remain hard missing in
that profile. The chained-equations manual documents a default ten-iteration
burn-in and ordering from most to least observed variable; perfect prediction
raises an error unless explicit augmentation is requested. Trace summaries
and a stable chain do not establish compatibility of the conditional models
or adequacy for a causal target. Treatment interactions needed by the analysis
cannot be omitted merely to simplify automatic imputation.
\citep{exec21_transport_stata_mi,exec21_transport_stata_chained,exec21_transport_stata_substantive}

SAS/STAT 14.1 separates MI, complete-data analysis and MIANALYZE. Its documented
alternatives include sequential methods for monotone patterns, multivariate-
normal MCMC and fully conditional specification for arbitrary patterns.
MIANALYZE requires parameter estimates with standard errors or covariance
matrices; it is not simply an average of filled tables. The inspected
sensitivity chapter supplies pattern-mixture analysis, while saying its
selection-model approach is not supplied in that profile. Later releases and
technical equations available only as images were not authenticated by this
text inspection. The pooling calculation below uses the readable Stata
technical text. \citep{exec21_transport_sas_mi_intro,exec21_transport_sas_mianalyze_intro,exec21_transport_sas_combining,exec21_transport_sas_sensitivity}

IBM SPSS Missing Values 31.0.2 selects monotone methods where possible and
otherwise FCS, with ten automatic FCS iterations and main effects by default.
Its predictive mean matching default uses five donors. Reproduction depends
on seed, variable order, case order and settings. It distinguishes naive
parameter pooling from output-specific univariate pooling with uncertainty;
unsupported output has no pooled result. Analysis weights do not establish
complex-sample inference: the manual says the imputer does not explicitly
handle strata or clusters, and Complex Samples procedures do not automatically
analyze these MI datasets. Preserve that limitation rather than attaching a
generic standard error. \citep{exec21_transport_spss_missing}

The inspected Stata manuals contain release-19 examples and July 2026 PDF
metadata; later acquisition does not authenticate every technical byte at
the cutoff. SAS's version identity and IBM's version likewise delimit their
profiles. EViews, Mplus and additional commercial and open implementations
remain individual coverage obligations. The inspected S7 composition also
distinguishes missing-value graph discovery from imputation or transport:
causal-learn's missing-value PC dispatch is a selected graph-search route
under its missingness restrictions, not a universal response-adjustment
engine. A native-language reference should retain its own assumptions and
failure states before any cross-language port. \citep{exec17_s7_paths}

## Missing outcomes can reverse the decision without changing observations

Let A be randomized independently of a fair binary latent response type H,
and let response R=H. Set Y(0)=0 and Y(1)=10 for responders. Two worlds set
the nonresponders' Y(1) to -10 and 10 respectively. Each observable
(A,R) cell has probability 1/4 and all observed treated outcomes equal 10,
so the two observed laws coincide. Complete-population effects are nevertheless
0 and 10. USD 4 action cost gives margins -4 and 6. A specified imputation
model chooses among restrictions on the missing outcomes; increasing its
draw count cannot identify which world is true. \citep{exec21_transport_reference}

Writing the unobserved treated mean as 10+delta gives effect 10+delta/2 and
net value 6+delta/2. The stipulated delta range [-20,0] gives [-4,6], with a
zero margin at -12. This is a nonprobabilistic sensitivity range supplied by
the analyst, not a confidence interval or a learned probability of MAR.
The SAS assumptions text distinguishes MAR, MCAR and ignorability conditions;
checking observed-data fit cannot verify a restriction on unobserved values.
\citep{exec21_transport_reference,exec21_transport_sas_assumptions}

## Preserve both population weights and covariance

Suppose source stratum proportions are (4/5,1/5), target proportions (1/5,4/5),
and stratum causal effects are USD 10 and -10. Under invariant stratum effects
and full support, source-to-target weights are 1/4 and 4. The source average
6 becomes target average -6; USD 2 cost changes margin from 4 to -8. The
exact oracle also enumerates randomized treatment and positive stratum/action
response probabilities to verify the combined population, treatment and
response weighting identity. Estimating these probabilities or sampling the
target covariates introduces additional uncertainty. The three types of
weights must retain their separate meanings. \citep{exec21_transport_reference}

If only the first stratum exists in the source, reweighting cannot recover
the second response. Supplying a scientifically justified second effect in
[-10,10] yields target effect 2+(4/5)tau2 in [-6,10], and net [-8,8]. Trimming
the missing stratum changes the population; extrapolating a point value adds
a model. Both require explicit choices and cannot be hidden as convergence
or numerical repairs. \citep{exec21_transport_reference}

For a scalar estimand, proper MI pooling under its assumptions gives total
variance T=Ubar+(1+1/M)B. The exact values Q=(0,2,4), completed-data variances
U=(1,1,1), and M=3 give Qbar=2, B=4 and T=19/3. Neither 1 nor 1/3 is the
same uncertainty statement. Ratios should retain the declared analysis scale:
odds ratios 1 and 9 have geometric mean 3 and arithmetic mean 5. For vector
effects, preserve coefficient identities and off-diagonal covariance before
forming a contrast. \citep{exec21_transport_stata_estimate,exec21_transport_reference}

The oracle supplies an additional failure diagnostic: binary conditional odds
ratios 1 and 9 cannot belong to one positive joint distribution. Alternating
updates can still have stable, order-dependent distributions (3,1,1,3)/8 and
(1,1,1,1)/4. This is a constructed incompatibility example, not a recorded
vendor failure. Stable trace output alone cannot settle model compatibility.
\citep{exec21_transport_reference}

The proposed public trial should compare complete records, complete cases,
single imputation, proper MI and a justified response-weight method on fixed
MAR/MNAR, support, interaction and sampling scenarios. Preserve all failed
fits and unavailable pooled outputs, then assess bias, coverage, width,
availability and whole-workflow cost. Integration should transmit unit and
imputation IDs, missingness reasons, actual model settings, populations,
covariance and refusal through the library, CLI and MCP. Licensed execution,
native conformance, full source coverage and bank economics remain open;
the mathematical examples justify a prototype comparison only.
