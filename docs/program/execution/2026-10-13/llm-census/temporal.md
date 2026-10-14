## Temporal predictions and interventions on conversations
\label{exec13:census-temporal}

A time series can support a useful prediction without identifying a useful
intervention. The distinction remains necessary when a language model
produces a graph and an accompanying explanation. Augur offers a concrete
example: a teacher model proposes relations between covariates, a student
learns from selected explanations, and the downstream task predicts a future
trend. The inspected preprint evaluates air, power, traffic and finance
settings, using classification F1 and AUROC for prediction. These are
relevant forecasting outcomes; they do not estimate the value of a deposit
rate change or a sequence of servicing actions.
\cite{exec13_census_augur_arxiv}

### What a temporal graph proposal establishes

Augur first retains highly correlated pairs using Spearman ranks, asks a
language model to choose among directed, confounded and spurious
relationships, and repairs graph cycles. Its stability score measures
agreement across candidate graphs. Its groundedness score checks that a
summary agrees with the graph from which it was generated. Each component
has a clear engineering purpose, but the latter two can be high when all
candidates share the same wrong causal premise. Acyclicity is a structural
property; agreement with one's own graph is an internal consistency
property.
\cite{exec13_census_augur_arxiv}

The authors explicitly acknowledge causal sufficiency and the possibility
that correlation pruning misses nonlinear or lagged dependence. Asking the
model to output ``confounded'' does not independently demonstrate hidden-state
identification. Nor does a chronological train/test split create
exchangeability of a proposed action. In a deposit application, funding cost
and deposit outflow may respond to an unobserved liquidity shock. A predictor
can exploit that relationship while remaining unable to answer what outflow
would have been under a different offered rate.

The proposal should retain this architecture as a forecasting and hypothesis
generation comparator. A causal evaluation needs a separate target and
separate truth: for example, generated lagged mechanisms with known
interventions, omitted common causes and nonlinear dependence deliberately
missed by marginal screening. Report predictive performance and intervention
performance separately. A failure of intervention recovery can coexist with
a useful forecast and should lead to a restricted product role, rather than
erasing the forecast result or relabeling it as policy evidence.

### A directly relevant longitudinal method

Zhang, Wang and Dhillon study sequences of human edits and model replies.
Their CausalCollab method proposes an Incremental Stylistic Effect (ISE),
uses a conditional variational autoencoder to represent editing styles, and
combines a fitted outcome model with Monte Carlo evaluation of a longitudinal
functional. Their identification theorem explicitly assumes sequential
exchangeability and positivity for the style interventions. Thus there is a
concrete literature route for studying longitudinal human--LM collaboration;
its existence should not be obscured by a search that returns mostly generic
causal-inference papers.
\cite{exec13_census_collaboration}

For clarity, let \(L_t\) denote information presented before editing step
\(t\), \(A_t\) the human edit, and \(H_t=(\bar L_t,\bar A_{t-1})\) the
recorded history. A potential terminal outcome is \(Y(\bar a_T)\).
Exchangeability requires the recorded history to remove the common causes
of the edit and its downstream outcome. An analyst's private customer
knowledge, skill or intention can violate this requirement even when every
message has been logged. The low dimensionality of a style score also does
not establish overlap: legally required text may allow little variation in
some histories, and certain kinds of edit may never occur for distressed
customers.

The source defines the outcome associated with a style functional through a
conditional mixture over text versions having that style. This matters for
implementation. A learned coordinate and an instruction such as ``make this
more reassuring'' need not describe the same intervention. A model can make
a response more reassuring by changing tone, by promising compensation, or
by omitting a warning. Those changes can have different effects and costs.
Before adopting the estimand, the proposal must specify which distribution
of complete edits implements the change and which content must be held
fixed.

Consider a second project-generated reference example. Two proposed messages
receive the same ``polite'' label. Their stipulated response probabilities
are \(1/5\) and \(4/5\), while the reference message has response probability
\(1/10\). Suppose an editing policy selects the second message with
probability \(q\). Its effect against the reference is

\[
 (1-q)\frac15+q\frac45-\frac1{10}
 =\frac1{10}+\frac35q.
\]

The effects are \(1/10,2/5,7/10\) at \(q=0,1/2,1\), respectively, despite
an identical style label. These are exact values under an invented law,
not observed customer effects. They show why the mixture is part of the
intervention definition. A randomized choice among fixed text variants is a
substantive alternative to inferring a latent stylistic effect. It has a
narrower target but makes treatment versions directly inspectable.

### What the available evidence leaves open

CausalCollab constructs counterfactual edits with ChatGPT, uses model-assigned
outcome labels, and changes the association between a confounding signal and
the outcome in its evaluation data. Its three sources include human--model
collaborative writing, model self-chat, and a hybrid dialogue setting. They
should not all be described as independently observed human intervention
outcomes. Performance under this constructed design is useful evidence about
that design, but is not a direct measurement of how real users would have
responded to unchosen edits.
\cite{exec13_census_collaboration}

This supports an affordable proposal-stage evaluation. Begin with public or
generated interaction histories, fix a small set of content-preserving edit
policies, and expose the evaluator to known latent intentions and missing
history in deliberately adverse cases. Compare a fixed editing policy,
an observed-association rule, a correctly specified numerical longitudinal
method, and the proposed representation-based method. Keep the true
generator inaccessible to the method. Assess policy-value error, support,
refusal and total review effort, in addition to language quality. Generated
labels should be identified as such and their sensitivity to a second label
rule should be reported.

A live human or bank experiment becomes valuable when this work identifies
a consequential uncertainty that the generated law cannot answer. It is not
a prerequisite for specifying the architecture or exposing its failure
mechanisms. Conversely, neither the inspected theorem nor a generated
experiment entitles the proposal to claim identification under unrecorded
human intentions. Direct replication still requires review of the exact
representation training, integration scheme, outcome labels and source-code
versions.

\label{exec13:census-temporal-end}
