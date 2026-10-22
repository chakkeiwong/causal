# Preserve evidence and the customer population

A causal assistant needs to check what the source supports and whose effect is
being estimated. A correct quotation can describe an association, a different
customer population or an intervention whose identifying assumptions do not
hold for the proposed decision. Wang and colleagues' factuality survey helps
organize retrieval, attribution, human review and model judging. Its surveyed
finance language tasks do not establish causal validity, and its accounts of
other studies do not replace independent inspection of those originals.
\citep{exec22_factuality_wang}

The proposal should retain evidence spans and their population/time scope,
separate supported premises from unverified causal assumptions, and expose
conflicting or insufficient evidence. Structured retrieval can help map entities
and policies, but a knowledge-graph relationship is not automatically a causal
edge. Several agents agreeing on the same retrieved premise do not create
independent evidence. Compare these workflows against simpler retrieval and
human-assisted baselines with matched documents, review time and budgets.
Evaluate citation support, causal identification/refusal, target preservation
and decision loss separately. These are proposed public prototype studies,
with actual reliability and cost still to be measured.
\citep{exec22_factuality_wang}

Vilfort's weighted-estimands paper addresses another failure route: different
reasonable customer mixtures can imply different effects even when group
effects are valid. In an authored illustration, stipulated group effects of
USD 6 and USD -2 per customer give contribution USD 4 under weights 3/4 and
1/4, but contribution USD 0 under weights 1/4 and 3/4. A stipulated USD 1 cost
changes the respective net values to USD 3 and USD -1. Allowing a fraction
epsilon of baseline weight to move to any group gives a worst-case net value
of 3-6 epsilon; strictly positive value requires epsilon below 1/2. This
illustrates target sensitivity, with no observed bank effects or unknown
population weights inferred from the example.
\citep{exec22_weighted_vilfort,exec22_weighted_reference}

Sampling uncertainty adds a separate requirement. The paper's exact model uses
normally distributed group-effect estimates, known positive-definite joint
covariance and fixed known weight classes. Its guarantees distinguish coverage
for each fixed alternative target from simultaneous coverage of the entire
target set. At alpha=beta=0.05, the lower guarantees are 90% for each fixed
target and 85% for the simultaneous two-sided event. A possible allocation for
a 95% simultaneous guarantee is alpha=0.0125 and beta=0.025, under the exact
assumptions. A result-selected customer mix needs the appropriate protection;
the words "95% confidence" alone cannot specify it.
\citep{exec22_weighted_vilfort,exec22_weighted_reference}

The feasible extensions require covariance/weight consistency and conditions
on estimated classes. Boundary targets need a containment argument; the
paper's positive-slack theorem cannot be justified merely by unchanged rounded
results at zero slack. The proposed library, CLI and MCP output should carry
the target, full covariance, class, confidence event, error budgets and numerical
status. No native robust-interval solver or adapter has been qualified here.
Public known-law effects and independent evidence corpora can test these
requirements before expensive bank experiments. Weight robustness still
presupposes valid group effects and does not repair confounding.
\citep{exec22_weighted_vilfort}
