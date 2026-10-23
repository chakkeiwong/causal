# Preserve the one-decision target when reusing a bandit library

Open Bandit Pipeline 0.5.5 provides a source-qualified reference for one-time
offer allocation. Its inspected contextual-bandit estimators, regression and
tuning wrappers do not replace a longitudinal servicing analysis. Eleven
authenticated files establish a concrete profile at the selected November 2022
revision. The proposal retains this profile as a reference; complete adoption,
runtime integration and broad porting remain unqualified.
\citep{exec23_obp_sources}

Correct logging probabilities materially affect the business decision. In an
exact two-context example, the target always gives offer one and has value 7/2.
Clipping the importance ratio at two gives 3, while substituting uniform logging
probabilities gives 17/4. At an assumed USD 10 per reward unit and USD 32 offer
cost, the margins are USD 3, USD -2 and USD 10.50. Deterministic replay can also
produce 17/4 here because unequal logging changes the composition of matched
contexts. For a stochastic target with no exact-one action matches, the selected
replay source leaves zero scores; the proposed product must report unavailable
replay evidence instead of interpreting that as zero policy value.
\citep{exec23_obp_sources,exec23_obp_reference}

The core validators and preparation paths need a strict adapter contract.
Probability rows must be finite and nonnegative as well as sum to one; row,
action and position identities must agree. The regression wrapper's uniform
propensity fallback is not authenticated logging truth. Its default fit is
in-sample, while its multi-fold alternative shuffles rows without imposing
customer groups or calendar separation. The interval helper resamples fixed
scores, and a tuned estimator retains its selected threshold on the object.
Those operations do not by themselves account for all fitting, selection or
dependence uncertainty.
\citep{exec23_obp_sources}

The source review also rejects an apparent defect: the tuned interval's omitted
estimated-propensity constructor flag does not establish a wrong-array error,
because the chosen propensity array is already forwarded as the base estimator's
ordinary input. OBP's Student helper is a one-sided lower bound, so its quantile
must not inherit the symmetric-interval criticism from SCOPE-RL. This distinction
keeps review findings tied to actual contracts.
\citep{exec23_obp_sources,exec23_obp_reference}

The public-data route is useful but bounded. The inspected Open Bandit Dataset
class compares empirical campaign reward means, sorts by timestamp and prepares
features before optional chronological splitting. That is observable benchmark
evidence with sampling and population limits, not exact counterfactual truth or
bank validation. The prototype should use known finite laws and adverse tests
for logging imbalance, clipping, no matches, invalid probabilities, position
permutations, repeated customers and tuned-object reuse. Dataset rights, actual
dependencies, native outputs and costs still require review and measurement.
Library, CLI and MCP requests must preserve these same target and refusal rules.
\citep{exec23_obp_sources,exec23_obp_reference}

The current reader has 996 audited citations and 232 genuine scholarly PDFs.
There are 44 passing proposal reuse dispositions, three inconclusive and 68
open entries; the reference decisions grant no native capability. This narrows
the build-versus-reuse question while preserving the remaining scientific and
operating gates.
\citep{sp23obp_reader,sp23obp_progress}
