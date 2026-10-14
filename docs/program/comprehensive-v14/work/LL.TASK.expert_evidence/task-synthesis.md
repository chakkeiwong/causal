# Expert evidence, disagreement and causal refusal

\label{exec14:expert-evidence}

A collections manager asks whether a new contact offer will increase repayment
within thirty days. An experienced officer says that offers are allocated to
accounts thought most likely to respond. Another describes assignment as
effectively random within the day's queue. A retrieved operational note
describes the standard queue but predates a change in the assignment system.
An assistant can locate those accounts, identify the disagreement and make its
consequences explicit. Counting two statements in favor of one story does not
resolve which assignment mechanism operated for the accounts under study.
This distinction determines what the proposed product should accept from
experts, documents and language models.

The useful output is a collection of inspectable claims with their supporting
and opposing evidence, the assumptions still being made, and the decisions
that depend on them. A causal diagram becomes one representation of those
claims. The central design problem is how to retain a plausible alternative
when a passage is missing, an expert account conflicts with a log, or two
documents repeat the same original assertion. The literature supplies useful
components for this task, with different evidence boundaries.

## What retrieval, elicitation and interactive auditing establish

Zhang et al.'s LACR constructs a skeleton using model background knowledge,
retrieved documents and optionally statistical discovery output, before
orienting the retained edges. Its experiments support a conditional role for
retrieval: the ASIA background-only skeleton has reported F1 of 1, while adding
documents lowers it to approximately 0.727; other benchmark cells improve.
The orientation score conditions on true-positive skeleton edges and must not
be presented as whole-graph accuracy. More retrieved text is therefore an
input whose relevance and reliability need evaluation.
\citep{v12_la_2402_15301}

The algorithm also reveals an uncertainty problem that a superficial reading
of its prompts would miss. Individual responses may be UNKNOWN and contribute
zero to an aggregation score. Nevertheless, the final rule deletes an edge
when that score is nonpositive. If every response is unknown, the edge is
deleted. Retaining an unknown token in a prompt is thus insufficient: the
aggregation and graph-conversion stages must preserve its meaning. The banking
proposal should retain an unresolved adjacency when evidence was not located,
unless a separately justified statistical or structural argument excludes it.
\citep{v12_la_2402_15301}

Soft elicitation offers a different route. Darvariu et al. query both variable
orders, average the corresponding judgments and use the resulting priors to
bias graph search. Combined mutual-information and LLM priors improve selected
benchmark comparisons, but LLM-only priors are not consistently beneficial;
mutual information alone is strongest on the specialized Child benchmark.
This motivates sensitivity to the influence assigned to elicited knowledge.
It does not convert the model's stated probability into a calibrated
probability of a banking edge. Selby et al. provide complementary adverse
evidence: some elicited priors conflict with data, and ordinary nearest-neighbor
and random-forest imputations provide strong alternatives. Their discussion
of ambiguous units and recognizable public datasets is directly relevant to
financial data dictionaries and evaluation contamination.
\citep{v12_la_2405_13551,v12_la_2402_07770}

Interactive auditing can make suggestions easier to inspect. The early
*Causal Auditor* organizes ratings, proposed confounders and mediators into
visual summaries. It reports 103 correct directions out of 110 queries in its
selected setting. That is a literature observation from early cases, with no
new evidence about collection offers. Its reported BIC change also needs
caution: the text calls a change from -3673.4 to -6270.3 an improvement while
the captions say higher scores are better. Without a reconciled convention and
reproduction, the claimed percentage should not support the product's value
case. In any event, a change in model fit alone would not validate a causal
direction. \citep{exec14_expert_auditor}

The later CausalChat study reports incorrect-edge counts of 5/18 with BIC
feedback, 7/18 with LLM text, and 1/18 with its integrated interface. Six
students completed the stages in a fixed sequence and selected different edges
as they proceeded. These observations motivate usability hypotheses but do
not isolate the causal effect of assistance under randomized task allocation.
Expert feedback explicitly identifies missing citations and uncertainty about
the scientific evidence behind the model's explanations. A persuasive display
must therefore preserve a route back to the primary passage and its limits.
\citep{v12_la_2410_14146}

Sng et al. show why a metric also needs a precise interpretation. Their
hallucination criterion concerns contradictions across causal-rating prompts.
The retrieval experiment supplies a textual, mocked true graph, and the paper
explicitly cautions that reduced contradiction does not establish accurate
causal prediction. The proposed banking evaluation should separately measure
retrieval, statement support, graph admissibility and intervention error;
success on one cannot silently substitute for the others.
\citep{exec13_hallucination}

## Formal disagreement handling still depends on its premises

Li and Russo's 2026 ABAPC-LLM supplies a more explicit combination of semantic
and statistical constraints. It elicits required and forbidden directions,
parses them into a schema, and retains their intersection across five model
responses. Conditional-independence results enter a causal argumentation
framework; its solver seeks an admissible extension after relaxing selected
constraints. This makes the provenance and consequences of a conflict more
visible than an unrecorded majority vote. \citep{exec14_expert_argumentation}

The implementation described by the paper is more restrictive than the general
idea of defeasible knowledge. A preliminary skeleton reduction removes edges
that are never reintroduced. Required LLM arrows are discarded when their
adjacencies have already been removed; the remaining required and forbidden
directions are enforced as hard constraints. A stable output therefore
establishes consistency relative to the surviving restrictions. It cannot
recover an edge excluded by an erroneous preliminary decision, nor guarantee
that a repeatedly suggested hard constraint is true. The paper acknowledges
this tradeoff between tractability and reconsideration of the hard constraints.
\citep{exec14_expert_argumentation}

The study uses 54 generated graphs with five, ten or fifteen nodes and repeated
samples from their stipulated distributions. It reports structural gains over
several statistical and language-model alternatives. The evaluation is useful
because it exposes both data constraints and semantic constraints, but its
metadata construction must accompany the result: variable descriptions are
generated with access to the true graph, although prompts request descriptions
that do not explicitly state the links. The same elicited constraint set is
reused across data repetitions for a dataset. Such repetitions assess sampling
variation conditional on that set; they are not independent replications of
the full elicitation process. Neutral descriptions, alternative descriptions
and misleading semantic controls remain necessary in a banking prototype.
\citep{exec14_expert_argumentation}

Other qualifications affect the comparison. The consensus procedure can return
no constraints and sacrifices recall for precision. Runtime tables omit
external model latency. Hidden-confounder extensions and calibrated adaptive
weights are proposed future work. The appendix's statistical-test description
also uses inconsistent observation and degrees-of-freedom descriptions, so its
significance calculations are not independently reconstructed here. The
proposal can adopt the idea of explicit conflict traces while keeping the
reported gains as bounded literature evidence and leaving runtime adoption
subject to a separate code, license and environment review.
\citep{exec14_expert_argumentation}

## Evidence adequacy differs from the truth of an assumption

ARGUS audits whether a paper reports evidence supporting difference-in-differences
assumptions. It expressly does not adjudicate causal truth. Its bounded
retrieval and assessment stages can locate design flaws that a keyword
baseline misses, but retrieval gating trades some omission detection for
abstention. In the five-paper pilot, it abstains on 22 of 55 cells; among the
33 answered cells, 25 judgments are more severe than the reconciled human
labels. The subsequent calibration is evaluated on the same small pilot and
does not establish performance on unseen papers.
\citep{v12_la_2609_30867}

This evidence suggests three separate unknown states for the banking workflow.
First, the source may not be accessible or the retrieval procedure may fail.
Second, an inspected source may simply not discuss the needed assumption.
Third, it may state an assumption without evidence that establishes its
applicability to the current accounts, dates or intervention. An operational
manual can support the claim that a randomization procedure was prescribed;
assignment logs and an appropriate design are still needed to establish which
procedure actually occurred. A paper's favorable finding in another population
does not settle transport to the proposed collection policy.

A claim record should identify the source version and passage, the population,
time and intervention it concerns, what the passage supports, the contrary
evidence and the remaining inference. It should distinguish direct observation,
reported procedure, expert assertion, mathematical implication and hypothesis.
Repeated copies should point to a common source family. An expert should be
able to correct the extracted claim without silently replacing the original
text. The system should retain both interpretations when the disagreement is
substantive, then show which graph restrictions and estimands each would permit.
These are proposed product requirements; this synthesis does not claim that an
agent already performs them reliably.

## A banking contrast that documents alone cannot identify

Let $A$ indicate receipt of a contact offer at decision time zero, and let $Y$
indicate a repayment by day thirty. The eligible population is fixed before
assignment. Suppose the value of repayment is USD 100 and each offer costs
USD 20. The target is the incremental expected value per eligible account,
$100\{E[Y(1)]-E[Y(0)]\}-20$. Both the intervention and the cost are stipulated
for this illustrative calculation; there is no observed bank experiment.

Consider two mechanisms. In the first, $A$ is an independent fair coin and
$Y=A\mathbin{\oplus}E$, where $E$ is an independent Bernoulli variable with
probability $1/4$ and $\oplus$ denotes exclusive-or. In the second, a latent
pre-offer state $U$ is a fair coin, $A=U\mathbin{\oplus}E$, and $Y=U$. Both
mechanisms produce exactly the same observed distribution:

```{=latex}
\[
\begin{array}{c|cc}
 &Y=0&Y=1\\\hline
A=0&3/8&1/8\\
A=1&1/8&3/8
\end{array}.
\]
```

They therefore have the same observed repayment contrast of $1/2$. Under an
intervention, however, the first mechanism gives repayment probabilities
$1/4$ and $3/4$, whereas the second gives $1/2$ under either action. The causal
risk differences are $1/2$ and zero, and the net values are USD 30 and minus
USD 20. In the restricted class containing just these two mechanisms, the
effect set is $\{0,1/2\}$ and the net-value set is $\{-20,30\}$. These sets
are not advertised as sharp bounds over every possible structural model.
\citep{exec14_expert_oracle}

An assistant that selects the first diagram because several sources call the
offer effective would authorize a different decision from one retaining the
latent-selection explanation. More rows from the same observed law cannot
distinguish these two mechanisms. A useful expert question concerns the actual
assignment rule and the information available at assignment, rather than a
generic opinion about whether contact helps. A verified randomized assignment
or defensible additional measurement and assumptions can change the inference.
Until then, retaining both models and refusing a uniquely identified benefit
is an informative result.

This example also supplies an inexpensive formal baseline for a prototype.
Enumerate both candidate mechanisms, verify their observational equality and
compare the assistant's admitted graph and effect claim with the declared
information. The correct behavior under ambiguous evidence is to retain the
distinction between observational fit and intervention value. The exercise
evaluates consistency with stipulated truth, not whether a public document
accurately describes an actual bank.

## Why repeated agreement can exaggerate evidence

Suppose an illustrative hypothesis has prior probability $1/2$ and one
independent source has a known likelihood ratio of four. The posterior is
$4/5$. Five copies of the same source still supply that same evidence. If they
are incorrectly multiplied as independent likelihood ratios, the reported
posterior becomes $4^5/(1+4^5)=1024/1025$. In practice a citation rarely comes
with a defensible numerical likelihood ratio at all. The example demonstrates
the need to track shared provenance rather than prescribing a Bayesian score
for every passage. \citep{exec14_expert_oracle}

The analogous issue arises with repeated model calls. For a binary judgment
with independent error probability $1/5$, five-call unanimity has probability
$(4/5)^5+(1/5)^5=41/125$; the probability of an incorrect answer conditional
on unanimity is $1/1025$. Now impose perfectly shared errors with the same
marginal error probability. Every call agrees, and the conditional error
remains $1/5$. These exact constructed laws show that marginal reliability and
agreement alone do not determine the value of consensus. They do not estimate
the dependence or accuracy of any current model.
\citep{exec14_expert_oracle}

The prototype should accordingly compare individual judgment, consensus,
source-family aggregation and a human-led baseline. It should vary misleading
shared evidence, missing evidence and contradictory passages, while retaining
all requests in the denominator. Conditional correctness among returned claims
must appear beside availability, false assertions of no relationship and
incorrect refusals. Source-family or task-family dependence also matters for
uncertainty: many paraphrases of one mechanism do not provide the same evidence
as many independent mechanisms.

## What a package can contribute, and what must be repaired

The inspected PyWhyLLM revision of 6 January 2026 provides concrete suggestion
and retrieval components under a root MIT notice. Its packaging uses a dynamic
version placeholder and a substantial model, embedding and retrieval dependency
stack; that declaration is not a qualified environment. The selected
identification wrapper delegates backdoor suggestions to a model-based
confounder suggester. Its frontdoor method is a placeholder, while a different
simple class does generate frontdoor names through a prompt. Neither a method
name nor a generated list establishes that a graphical identification theorem
has been applied. \citep{exec14_expert_pywhy}

The role-based confounder path initializes a treatment-to-outcome edge, asks
model personas for candidate confounders and accumulates counts. Such counts
represent agreement across prompts, with no calibrated probability or source
independence attached. Some selected calls retry a missing-key error without a
finite bound in the inspected loop. These findings support explicit caller
budgets and preservation of failure; they are static-source findings, not
observed failures of an executed service. \citep{exec14_expert_pywhy}

The augmented pairwise path adds a second boundary. It downloads a knowledge
resource at construction, finds a matching pair through lexical and embedding
retrieval, and concatenates selected source sentences into the retrieval
context. That concatenation does not carry their document identity into a
structured claim record. When no matching pair is found, it falls back to model
knowledge. The answer parser accepts only the two directions or neither;
neither is not an explicit insufficient-evidence state. The helper also creates
its own model client instead of consistently using the wrapper's supplied model.
These behaviors make direct adoption inappropriate for the proposed evidence
contract. \citep{exec14_expert_pywhy}

A permissible first integration would be a small, optional elicitation
component whose output remains a proposal for review. It needs explicit model
configuration, pre-acquired versioned source inputs, retained passage identities,
bounded calls and retries, and distinct supported, contradicted, unknown and
unavailable outcomes. Graph conversion must keep negative and unresolved
judgments as records, validate clocks and direction restrictions, and run a
separately specified identification procedure. Dataset licenses, transitive
dependencies, provider behavior and the remaining import paths require review
before the component is enabled. The current review enables no adapter.

The alternatives remain substantive. A manual evidence table with an explicit
diagram may be sufficient for a small proposal. A deterministic retrieval and
graph-checking system can expose evidence without delegating judgment. Soft
priors preserve alternative graphs but require sensitivity to their strength.
Argumentation provides explicit conflict traces but requires a policy for hard
and defeasible restrictions. An unqualified hard-constraint pipeline can
produce confident answers efficiently by excluding the correct model.

The known next step is therefore a public/generated-data prototype comparing
these workflows under declared evidence conditions. It should measure total
retrieval and model cost, expert correction time, failed requests and the effect
of evidence handling on the banking decision. The unresolved research concerns
calibration across new domains, dependence among sources and models, and useful
uncertainty when graph and observation assumptions remain disputed. The truth
of an undocumented historical assignment cannot be manufactured by a better
prompt. That boundary is part of the proposed product's behavior, while bank
experiments and institutional acceptance remain later work.

\label{exec14:expert-evidence-end}
