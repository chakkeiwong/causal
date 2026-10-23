# Compare longitudinal software on the policy and event law

A servicing comparison should begin with the accounts eligible at a common
time zero, the history available before each action, the observation mechanism,
and the financial horizon. A terminal default probability, the complement of
default cumulative incidence, an event-free survival probability, and a hazard
among current survivors are different targets. Early repayment can prevent
default while removing future margin. Dropping an unobserved outcome and
declaring an account event-free changes the observation law. Identification of
the requested policy value requires consistency, sequential exchangeability,
support for the policy histories, and justified censoring assumptions; no
software setting supplies those facts. The existing S5 development supplies
exact examples of these distinctions. \citep{exec17_s5_math}

## Match the engine to the question

The pinned gfoRmula source distinguishes survival from continuous or binary
terminal outcomes. It simulates covariates in the supplied order, applies the
intervention and updates histories. Its observed people, simulated histories
and bootstrap replicates are three separate sample sizes. The current review
retains revision-specific version 1.1.2 with the changelog's release date still
TBD. The source's survival calculation gives the competing event precedence
within a period. For main and competing conditional probabilities 1/5 and 1/10
over two periods, default incidence is
\( (1/5)(9/10)[1+(4/5)(9/10)]=387/1250 \).
Removing the competing mechanism gives 9/25. Their difference implies USD
50.40 at USD 1,000 per default, under the declared hypothetical law. This is a
difference between event worlds, not evidence that one output is erroneous.
\citep{exec20_gformula_reuse,exec20_gformula_reference}

The selected ltmle implementation instead offers binary longitudinal regime
means and a working marginal structural model. A working-model projection must
not be reported as an unrestricted regime mean unless the parameterization
justifies it. Wide chronological data, binary action coding, C=1 for observed
outcomes, and absorbing-event checks are part of conversion. Its default GLM
and cumulative probability floor 0.01 are scientific choices to retain in the
result. Flooring each incremental probability before multiplication is a
different operation. Requested additional variance can fall back to IC
variance, including with a supplied household identifier; that fallback need
not warn. Household IC aggregation preserves a record-weighted target unless
weights explicitly change it. Paired means require their full covariance.
\citep{exec23_ltmle_source}

lmtp is a further alternative when the question concerns a modified treatment
law. At the inspected 1.5.4 revision, its ipsi transformation and an odds tilt
are different probability maps even at the same numerical parameter. Supplied
shifted data, the information window, actual folds and effective prediction
bounds belong to its contract. The inspected outer-fold identifier mismatch
needs native reproduction; downstream ife variance and complete survival
handling remain unqualified. These limits prohibit treating the package name
as interchangeable with a deterministic g-formula regime or ltmle mean.
\citep{exec22_lmtp_reuse,exec23_policy_reference}

Commercial products offer substantive comparisons in their documented scopes.
The inspected Stata stteffects manual describes fixed-treatment potential mean
survival and average effects with weighting/regression alternatives and
overlap diagnostics, while excluding delayed entry, time-varying covariates
and multiple records. Its stcrreg route is a separate subhazard target.
SAS/STAT 14.1 PHREG supports interval records and an EVENTCODE subdistribution
path whose effective options differ from an ordinary Cox fit. SPSS Statistics
30 supplies time expressions and measured-covariate segments. Such facilities
can test record conversion without establishing repeated-policy identification.
Mutable manual and edition limits remain attached to the sources; no licensed
execution, price advantage or procurement recommendation follows here.
\citep{exec14_survival_stata,exec14_survival_stata_competing,exec14_survival_sas,exec14_survival_ibm}

## A reproducible decision comparison

Let baseline risk H have probability 1/3 and let hardship L follow the first
contact A0 with probabilities 1/4, 1/8, 3/4, 1/2 for (H,A0)=00,01,10,11.
Default risk given history is
\(1/10+H/10+L/5-A0/25-A1/20\); it lies in [1/100,2/5] on every binary
history. Enumerating the histories under no contacts (0,0), targeted contacts
(H,L), and broad contacts (1,1) gives 13/60, 17/100 and 7/75. With USD 1,000
default loss and USD 6 and USD 4 contact costs, incremental net values relative
to no contacts are 0, 130/3 and 340/3 dollars. This matches independent moment
identities, not an external estimator's output. \citep{exec23_ltmle_exact}

If observation is conditionally independent of default given history, with
probability 9/10 when L=0 and 3/4 when L=1, complete-case risks for the first
two regimes become 69/335 and 139/850. Their biases are -43/4020 and -11/1700.
The population identity E(CY/pi)=E(Y) restores the requested risks using the
known observation law. In a native trial, fitting pi and the treatment law
adds estimation and overlap obligations. The paired covariance fixture gives
contrast variance 1/3 using covariance, versus 7/3 after dropping it. Neither
this fixture nor a larger variance estimate proves interval coverage.
\citep{exec23_ltmle_exact,exec23_ltmle_source}

A survival comparison must also respect unsupported horizons. With survival
known only through period m, opening-period reward through K>m has restricted
time between R(m)+S(m) and R(m)+(K-m)S(m). The known S(m) contribution cannot
be omitted in a discrete clock. S5's two explicit survival sequences give
six-period policy-minus-reference active time in [-1.55,0.65]; USD 20 per
period and USD 3 upfront cost give [-34,10]. This is an identification set
under a tail restriction, distinct from sampling uncertainty. A positive
point extrapolation needs additional assumptions. \citep{exec17_s5_math}

## Diagnostics, failure handling and reuse route

Preserve event order, availability time, support, time zero, policy callbacks,
the actual model/variance branch, convergence, and requested versus successful
fits. gfoRmula's default range clipping changes simulated laws; its bootstrap
resamples whole people and removes missing results in downstream summaries.
It therefore needs explicit failed-replicate accounting and separate testing
under common calendar shocks. ltmle suppresses some fit warnings and can return
missing standard errors after failed matrix solves. A finite curve cannot
erase either behavior. \citep{exec20_gformula_reuse,exec23_ltmle_source}

The proposal retains pinned R references before considering a port. A future
worker can compare exact histories, events, paired uncertainty and deliberate
failures against independent finite laws, then evaluate public longitudinal
data for realistic support and computational burden. A port would additionally
need parity for histories, event coding, clipping, learners and covariance.
GPL-3 gfoRmula, GPL-2 ltmle and AGPL-3 lmtp each require the intended dependency
and distribution assessment; a process boundary alone settles none of them.
Python, Java, C++ and unread alternatives remain separate coverage obligations.
This scientific comparison closes neither native qualification nor the wider
survey, visual review or bank acceptance. \citep{exec20_gformula_reuse,exec23_ltmle_source,exec22_lmtp_reuse}
