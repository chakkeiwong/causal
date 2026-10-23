# Preserve longitudinal regimes and the requested decision population

The selected `ltmle` source is a useful R reference for binary longitudinal
treatment and censoring histories, treatment-specific means, and a working
marginal structural model. Its interface supports a single regime or a pair;
the working model can be saturated or a projection, so a sponsor-facing
comparison must state the regime, history, outcome, and target population
before interpreting a number. The source review also records defaults that
matter for reuse: a default GLM, a cumulative probability floor of 0.01, and
variance branches that can fall back to influence-curve variance when the
additional method is unavailable. With a supplied identifier, those influence
contributions are aggregated by household. These facts motivate a candidate
native comparator and exact contract tests; they do not establish native
adoption or bank qualification. \citep{exec23_ltmle_source}

An exact public/generated construction makes the population issue visible. Let
baseline risk \(H\) have probability \(1/3\), let the first action \(A_0\)
affect later hardship \(L_1\), and let a binary default outcome satisfy
\[
 P(Y=1\mid H,A_0,L_1,A_1)=1/10+H/10+L_1/5-A_0/25-A_1/20.
\]
The law stays between 0.01 and 0.40 over all histories. Hardship probabilities
for \((H,A_0)=(0,0),(0,1),(1,0),(1,1)\) are \(1/4,1/8,3/4,1/2\).
The status-quo \((0,0)\), targeted \((H,L_1)\), and broad-contact \((1,1)\)
regimes then give risks \(13/60\), \(17/100\), and \(7/75\).
With USD 1,000 per default and USD 6 and USD 4 per contact at the two times,
their net values relative to status quo are USD 0, USD \(130/3\), and USD
\(340/3\). Suppose outcome observation is conditionally independent of default
given history, with probabilities \(9/10\) for \(L_1=0\) and \(3/4\) for
\(L_1=1\). Complete-case risks under status quo and targeted servicing then
become \(69/335\) and \(139/850\), with biases \(-43/4020\) and \(-11/1700\); known-probability
inverse-probability weighting recovers the stipulated population risks. These
are exact witnesses for target, censoring, and missingness contracts, not
fitted package results or measured bank returns. \citep{exec23_ltmle_exact}

The same source review finds household influence contributions summed within a
household and multiplied by the household-to-record count ratio; this does not silently
turn a record-weighted target into an equally weighted household target. Paired
contrasts preserve their covariance, while extreme probabilities, rank failures,
nonconvergence, and unsupported variance requests require explicit warnings or
refusal. A future public prototype should replay the exact law, adverse
observation regimes, and covariance fixture, then compare a pinned native
environment with the proposal's typed target and refusal ledger. Native engine
rights, dependency closure, numerical calibration, and a live bank workflow
remain open. \citep{exec23_ltmle_source,exec23_ltmle_exact}

The paired reader has 1,251 pages and 948 audited records, including 223
genuine scholarly PDFs. This increment closes one selected reuse review and
adds exact public/generated evidence; it does not close the wider software
coverage census, visual acceptance, independent review, bank validation, or
final investment decision. \citep{sp23lt_reader,sp23lt_progress}
