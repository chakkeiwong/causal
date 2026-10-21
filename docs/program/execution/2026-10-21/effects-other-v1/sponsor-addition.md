## Match software outputs to the servicing decision

The Julia comparison distinguishes CausalELM 0.8.0, CausalForest 0.1.5,
TMLE 0.20.5 and CausalTables 1.3.4 at selected revisions preceding the literature
cutoff. Their inspected source supports different roles: fitted effect
contrasts, tree predictions, targeted mean estimation and supplied-model
reference generation. These roles need distinct adoption decisions.
\cite{exec21_effects_causalelm,exec21_effects_causalforest,exec21_effects_tmle,exec21_effects_causaltables}

An exact public example gives a population effect of USD 4 but a residual
regression coefficient of 4/17 dollars. At cost USD 2, the population margin
is USD 2 while the coefficient-based calculation is negative. Another example
with missingness depending only on observed risk changes the complete-case
average to -12/5 dollars. Neither a method name nor a more accurate treatment
propensity model settles the required population. The selected CausalELM
standard-error expression also has squared outcome units; converting dollars
to cents scales it by 10,000 instead of 100. These are exact authored and
source-level findings, not native runtime results. \cite{exec21_effects_reference}

The proposal should prioritize a bounded TMLE worker design and CausalTables
public reference generation while preserving influence scales, missingness
targets, unit identities and the provenance of supplied graphs. CausalELM's
selected uncertainty path needs repair and fresh qualification; the inspected
CausalForest prediction paths do not supply a calibrated variance object.
Additional Rust candidates were found in bounded official metadata searches,
but their technical originals and historical versions remain unread.
\cite{exec21_effects_discovery}

