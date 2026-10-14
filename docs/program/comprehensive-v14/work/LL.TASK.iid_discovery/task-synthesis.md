# From language guidance to a defensible discovery decision {#exec14:iid-discovery}

Language assistance can make a discovery workflow more useful by clarifying
variables, locating applicable knowledge, comparing algorithms and exposing
conflicting assumptions. Its strongest proposal is a supervised route from
meaning to an explicitly restricted causal model. The decisive question is
whether that route improves the intervention decision while preserving what
the observations cannot distinguish. A graph that is more fluent, more stable
under repeated prompting, or easier to fit need not answer that question.

Consider a bank choosing a one-unit increase in a standardized deposit offer
$A$ at the start of a month. Let $Y$ be a standardized measure of the following
month's retained balances. The population consists of accounts eligible when
the offer is set; post-offer behavior cannot become baseline information by
renaming a column. For the example below, account histories are independent,
there is no interference, and the decision compares $do(A=1)$ with $do(A=0)$.
These are stipulated conditions for a calculation, not properties inferred
from a real bank. Shared branches, calendar shocks, selection and equilibrium
responses would require a different observation model.

## A clock-compatible ambiguity that more observational data cannot remove

Two centered Gaussian structural models illustrate the information problem.
In the first, the offer changes the outcome:

\[
 A=U_A,\qquad Y=\tfrac12 A+U_Y,\qquad
 U_A\perp U_Y,\quad
 \operatorname{Var}(U_A)=2,\quad\operatorname{Var}(U_Y)=\tfrac32.
\]

In the second, a pre-offer latent condition $H$ affects both variables:

\[
 A=H+V,\qquad Y=H+W,\qquad
 H,V,W\ \text{independent }N(0,1).
\]

Both mechanisms respect the recorded order of offer and outcome. Both produce
the same nonsingular observed distribution,

\[
 (A,Y)\sim N\!\left(0,
 \begin{pmatrix}2&1\\1&2\end{pmatrix}\right),
 \qquad E(Y\mid A=a)=\tfrac12a.
\]

The covariance determinant is three, so this ambiguity does not depend on a
degenerate observed table. Nevertheless, the intervention contrast is $1/2$
in the first model and zero in the second. Causal sufficiency would exclude
the second model by assumption. The clock alone does not exclude it. A
language system that interprets the phrase “offer response” as proof of a
direct effect has supplied a scientific restriction that was absent from the
numerical data.

There is also an exact limit on a forced choice based only on these
observations. If an algorithm selects the first model with probability $q$,
its success probabilities in the two worlds are $q$ and $1-q$, because the
input distribution is identical. Their sum is one and the smaller is at most
one half, for any observational sample size. This statement includes
randomized algorithms. It does not say that all causal discovery is impossible;
it identifies the information missing in this particular comparison. An
applicable assignment restriction or an intervention could distinguish the
worlds. A repeated description of the same observed association cannot.

This distinction determines the numerical baseline. A PC analysis under
causal sufficiency and the stipulated order answers a conditional question.
A latent-aware analysis must retain the possibility of common causes. Neither
method should be scored as wrong merely for declining to select a single DAG
when its declared model class permits both mechanisms. For these two
stipulated worlds the compatible effect values are $\{0,1/2\}$. That pair is
not an exhaustive identified set over arbitrary latent models, and it is not
a finite-sample confidence set. A prototype should retain those qualifications
in the returned object.
\citep{exec14_iid_oracle}

## What the reported gains do and do not support

The available studies motivate several distinct product options. Retrieval
can supply missing definitions or restrictions; soft priors can guide a
limited numerical search; statistical prompting can make existing numerical
evidence intelligible; and debate can organize competing explanations. The
appropriate comparator changes with the role. A retrieved definition is
compared with a dictionary and a documented expert rule, whereas a search
prior is compared with the same numerical algorithm and resource budget.

The primary results also preclude a single claim of uniform improvement.
LACR's retrieved-document condition reduces ASIA skeleton F1 from 1 to 0.73,
while additional knowledge improves CORONARY. Its reported perfect
orientation score is conditional on recovered true-positive edges. Missing
and false edges therefore remain outside that particular denominator.
\citep{v12_la_2402_15301}
Darvariu and colleagues report useful combined mutual-information and
language priors, especially with limited search, but mutual information alone
performs best on Child in the reported comparison. Keeping positive search
support is useful; it does not calibrate the probability of a causal effect.
\citep{v12_la_2405_13551}

Statistical prompting is similarly task dependent. In Takayama and
colleagues' Table 3, the Sachs PC baseline has F1 0.44, the language condition
without the statistical prompt has 0.52, and the two statistical-prompt
conditions have 0.29 and 0.27. Other algorithm/dataset combinations improve.
These are comparisons within the authors' experiment, not local replications
or evidence that one algorithm always dominates. Their lower fit criterion
and their closer-to-reference graph are different outcomes.
\citep{v12_la_2402_01454}

Cohrs and colleagues report query-order agreement of 0.510 and 0.870 for
their two model configurations, and a data-based method has higher SACHS F1
than either language method. Their answer-proportion null concerns the
response process. Even a correctly calibrated test of that null would not
automatically test conditional independence in the bank population.
\citep{v12_la_2406_07378}
The response-count calculation developed earlier in this chapter supplies a
separate finite-binomial counterexample; it should be reused as a diagnostic,
not represented as a new model experiment.

The newer multi-agent comparison combines algorithm selection and code
execution with graph debate. Its inspected version reports that additional
debate rounds can degrade Survey and Auto results and that the complete
workflow consumes 16--25 times the tokens of standard baselines. Those
findings support a bounded single-round comparator and full cost accounting,
without establishing bank economics. \citep{v12_la_2407_15073}
The 2026 argumentation approach makes conflicts explicit but retains hard
semantic constraints after an irreversible preliminary skeleton reduction.
Its synthetic descriptions are generated with access to the true graph and
its runtime comparison omits external model latency. These limits motivate
neutral descriptions, misleading-description controls and complete timing.
\citep{exec14_expert_argumentation}

Exposure and semantics require separate tests. The accessible-corpus study
by Feng and colleagues links relation frequency to performance and examines
contradictory statements and context changes. Its scope does not establish
the behavior of every closed model. Moreover, a changed context may genuinely
change the causal claim. A fixed-world paraphrase test must preserve the
population, timing and intervention; a changed-world test must change its
reference answer accordingly. \citep{v12_la_2407_19638}
Contradiction reduction and graph agreement are useful diagnostics, but neither
is a substitute for effect truth. The inspected hallucination study explicitly
retains that distinction. \citep{exec13_hallucination}

Barakati and colleagues provide a domain application that usefully exposes
the translation problem. Their materials study maps microscopy-derived
unit-cell descriptors to literature terminology, queries relationships using
LangChain and a language model, and reruns gCastle PC with required and
forbidden relations. The stated response schema includes insufficient
information. This is a concrete architecture for connecting measurements,
terminology and candidate restrictions. Its comparison chiefly discusses
agreement between inferred pathways and prior LiNGAM findings. Agreement
does not establish an intervention oracle, and spatial unit cells are not
automatically independent samples. The abstract uses the term fine-tuning,
whereas the inspected methods describe querying literature and give no
reproducible training recipe or checkpoint. The proposal should therefore
retain the documented workflow without inferring a trained artifact or
calibrated effect uncertainty. The linked repository is a separate reuse
lead requiring its own revision, rights and execution review.
\citep{exec14_iid_materials}

## Missing answers and recorded identity are part of the causal interface

Tracing the pinned research code reveals obligations that are less visible
in a method name. In the selected `causal_GPT` interface, the pure PC wrapper
reads variable descriptions and stored language answers. Its numerical
`pvalue` method pools the two query orders, then converts a decision to zero
or one. A missing stored row returns zero. The advertised weighted-vote
branch also returns zero beside an unfinished implementation marker. Thus
unavailable evidence, an unsupported aggregation method and a dependence
decision can share one numerical representation. These observations concern
the inspected source, not measured frequencies in an installed package.
\citep{exec14_iid_gpt}

The hybrid path contains a genuine numerical fallback for queries outside
the selected language-variable/conditioning scope. Within that scope it
collects unanswered queries, uses temporary decisions while assembling them,
and requests their answers in the surrounding driver. That driver also saves
result metadata with fixed model and temperature strings despite accepting
different values as arguments. For example, a configured model B at
temperature 0.2 would still receive the inspected record's fixed model label
and temperature 0.6. This is a literal assignment trace, not an API call. A
comparison cannot be reproduced reliably if result identity and actual
configuration can diverge. \citep{exec14_iid_gpt}

The proposal should therefore adopt the useful separation of language and
numerical query channels while replacing the ambiguous interchange. A
language-answer object needs the target statement, operational definitions,
source evidence, model revision, settings, parsing status and an explicit
unknown state. A statistical test object needs its observations, null,
sampling law and calibration. A pending query must not be published as a
completed dependence judgment. Unsupported weighted voting should refuse
until implemented and checked. Result identity should be populated from the
actual request and response, with missing metadata retained as missing.

## A token score does not have the same meaning in three discovery engines

The five pinned LLM-and-SCD notebooks expose a complete research route from
an initial graph and bootstrap summaries through two prompts to constrained
rediscovery. In a selected collection cell, the code sums the first token's
top-five probability mass only when the token is exactly `Yes` or `yes`.
It separately accumulates `No` or `no`. It does not identify all semantically
equivalent strings or turn the unreported mass into an explicit uncertainty
object. The resulting score is a property of the prompted token
distribution, not a probability that an edge exists in the bank.
\citep{exec14_iid_scd}

An exact authored example makes the parsing boundary visible. Suppose the
five tokens have masses 0.96, 0.02, 0.01, 0.005 and 0.005, assigned to `Yes`,
`No`, a newline, `I` and `It`. The literal affirmative score is 0.96. Change
only the first token to a leading-space `Yes`; the exact-string collector
assigns affirmative score zero, although a whitespace-normalized semantic
class still has mass 0.96. These are constructed input distributions, not
observed endpoint outputs. They show why unrecognized formats and truncated
token lists need explicit treatment before any scientific constraint is
created. Simple normalization would fix this example but would not establish
causal calibration or solve multi-token answer semantics.
\citep{exec14_iid_oracle}

The conversion then magnifies a parsing choice. The selected notebook marks
a score below 0.05 as forbidden, above 0.95 as required, and the interval
between them as unknown. Consequently the two constructed representations
above become opposite hard constraints. At exactly 0.95 the notebook returns
unknown, while the inspected paper's Algorithm 2 uses an inclusive upper
threshold. The 0.05 boundary is unknown in both. The notebook commit predates
the inspected paper revision, so the discrepancy is a version-alignment
obligation, not evidence about the authors' later experimental execution.
\citep{exec14_iid_scd,v12_la_2402_01454}

The target backend introduces another semantic choice. The PC conversion
creates required and forbidden directed-edge objects; exact search receives
an allowed supergraph, in which a high score permits rather than forces an
edge. The proposed pinned DirectLiNGAM target documents directed-path prior
knowledge. Its meaning must be checked against the notebook's direct-impact
question and the chosen matrix convention. For a chain $A\to M\to Y$, no
direct $A\to Y$ edge exists, but an $A$-to-$Y$ directed path does. Converting
“no direct impact” to “no directed path” rules out this chain and its mediated
effect. A common matrix with numbers $-1,0,1$ does not make these three
contracts interchangeable. \citep{exec14_iid_scd,v13_sw_lingam}

Notebook dependency installation is not locked to a reproducible environment.
The separate cycle-conversion notebook also passes the data positionally
into a constructor whose first parameter is `random_state` in the later
inspected target, before calling `fit` with the data. Compatibility must be
established at an actual chosen dependency revision; this source comparison
does not demonstrate what ran in the historical notebook. Acyclic conversion
and choosing among repaired constraints by fit on the same observations are
further parts of the adaptive procedure, and must accompany any later
uncertainty claim. \citep{exec14_iid_scd,v13_sw_lingam}

LLM-CD offers a useful alternative representation. The inspected evaluation
checks generated relations against directed reachability. Its backend
wrappers serialize ancestral constraints separately from absent edges and,
for one backend, order constraints. This is consistent with the primary
paper's distinction between ancestral priors and local adjacency. The paper
also states that the factorization of path priors is approximate and that
their common strength is problem dependent.
\citep{exec14_iid_cd,v12_la_2306_16902}
Adoption still needs a bounded adapter: the selected wrappers use shared
working paths and shell calls whose exit status is not checked before
parsing, then remove intermediate files. A nested backend license does not
resolve missing root-project terms. The proposed adapter should retain typed
constraints, use isolated run directories, check process results and preserve
all scientific inputs and outputs. Its terms and dependency boundaries must
be resolved before enabling it.

## A public and generated prototype with a decision criterion

A useful first prototype has two stages. Deterministic semantic fixtures
check missing answers, unsupported methods, token variants, exact threshold
boundaries, graph endpoint preservation, cycles, edge-versus-path conversion
and request/result identity. These tests are cheap and have known expected
answers. They establish an adapter contract; they do not estimate live model
quality. Only then should the team profile a matched discovery experiment
and register its final design.

The experiment should split by mechanism family. Repeated numerical samples,
variable names, retrieved packets and prompts belong inside a mechanism's
cluster. The Gaussian pair above is a compulsory ambiguity case, accompanied
by causally sufficient, non-Gaussian and latent cases with explicit clocks.
Generator truth and effect oracles remain outside the prompts. Natural
descriptions, neutral renamed descriptions and deliberately misleading
descriptions are crossed with no retrieval, applicable original evidence,
wrong-domain evidence and contradiction. Removing meaningful definitions
changes the information supplied, so the comparison must say when it tests
robustness and when it tests the value of information.

Each language arm needs the same numerical inputs and a declared comparator:
a dictionary/clock baseline; PC or FCI under the appropriate assumptions;
score or non-Gaussian methods within their qualified regimes; language-only
proposals; and soft or hard guidance with declared strength and refusal
rules. Final graphs alone are insufficient. Record class and endpoint
retention, invalid outputs, valid abstentions, conditional effect-set
retention and width, and downstream action regret under known truth. Include
every requested case in the denominator, including parse failures, timeouts,
empty outputs and conflicting constraints. Measure total calls, tokens,
retries, numerical resources, latency and adjudication effort.

Before final runs, freeze versions, rights, splits, targets, sample sizes,
replication counts, tolerances, primary paired comparisons and multiplicity
treatment. Development profiling may set resource caps; it cannot become
an unannounced final experiment. Prompt variants and prior strengths must
not be selected on the final mechanisms. An optional live model experiment
needs the chosen endpoint's actual revision and measured costs, but none of
these design steps requires bank data or a paid experiment now.

The banking example supplies a transparent economic threshold. Stipulate
USD 200 per outcome unit and USD 60 for the unit offer increase. Net values
are USD 40 in the direct-effect world and minus USD 60 in the latent world.
If a planner assigns probability $p$ to the former, the expected net action
value is $100p-60$. Because the observed likelihood is the same, additional
observational records alone cannot update those odds within this two-world
comparison. At $p=0.9$ the expected value is USD 30, while perfect knowledge
would produce USD 36 by taking the action only in the favorable world. Thus
USD 6 per decision is an upper bound on the expected value of any information
experiment under those assumptions. At $p=0.5$ it is USD 20. A real noisy
experiment supplies less information and incurs costs; neither number is
bank ROI or an authorized spending budget.
\citep{exec14_iid_oracle}

The resulting recommendation is to reuse typed evidence, explicit conflict
handling and bounded search guidance as design references; to defer enabled
package integration until the specified contracts are verified; and to reject
automatic conversion of response agreement into causal confidence. The
unresolved scientific task is to justify useful graph/effect uncertainty for
the complete adaptive procedure in declared regimes. The small-language-model
discovery lead currently has metadata but no acquired original; its methods
cannot support a technical comparison yet. Broader literature coverage and
that original remain explicit survey work. They do not prevent
the proposed public/generated prototype from testing the concrete semantic
and decision boundaries established here.

\label{exec14:iid-discovery-end}
