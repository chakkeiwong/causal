# R04: temporal graph classes and effect uncertainty

The finite class is a stationary linear Gaussian temporal model with observed
encouragement Z_t, action A_t, response Y_t and latent disturbance U_t. A
member has stable lag coefficients, contemporaneous Z-to-A, optional Z-to-Y,
optional U-to-A/U-to-Y and a target contemporaneous intervention effect
tau (the persistent long-run effect is a separate query). The observed likelihood is the finite Gaussian law of the
history. We estimate it through a lag residual window only to make the
temporal dependence explicit; the retained set still uses a simultaneous
covariance region for the residual episodes.

For each retained graph class, the procedure propagates every compatible
coefficient ratio into an effect interval. The observational latent class
retains 40 finite edge/latent members and its direct-effect members permit
the unrestricted real line. This is an identified-set result: a chosen graph
or a narrow optimizer is not a confidence region. Randomized encouragement
removes latent confounding and exclusion of Z-to-Y gives a finite Wald ratio;
observed sufficiency gives a regression restriction. Both are additional
scientific inputs and are rejected when their design rank fails.

The covariance-region construction uses nine Bonferroni chi-square variance
pivots and interval arithmetic. It is an outer region, so it can be wide or
disconnected. Exact small-class enumeration checks every retained member’s
structural effect against the propagated set. A separate witness constructs
different latent linear systems with exactly the same positive-definite
observed covariance and arbitrary direct effect. Therefore observational
temporal data alone cannot identify the requested effect in this class.

The temporal residual approximation has an explicit limitation: finite lag
history and estimation error are not a universal dependent-episode theorem.
The registered study therefore compares finite horizons, weak rank, hidden
history, selection, near-unfaithfulness and false restrictions. Rank failure,
unrestricted sets and numerical timeouts are recorded separately. The exact
oracle is a diagnostic, not a deployable input. Additional intervention,
exclusion, measured confounders or a structural bank audit is required to
contract the observational set. Arbitrary PAG confidence and unrestricted
latent temporal graphs remain open.
