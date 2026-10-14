## Evaluate the claim behind the benchmark score
\label{exec13:census-evaluation}

CausalEval places diverse language tasks in one comparative survey, including
commonsense cause selection, correlation-to-causation questions, graph-based
inference and judgments about described events. This is useful navigation,
but the common label ``causal reasoning'' does not make their outcomes
interchangeable. Correctly classifying a relation mentioned in a sentence,
recovering a graph from observations and identifying a policy value test
different information and assumptions.
\cite{exec13_census_causaleval}

| Evidence object | What the inspected source measures | Additional evidence needed for the proposed causal role |
|---|---|---|
| Susanti--Holsmoelle relation extraction | Binary relations between entities in text | Joint graph constraints, target-population meaning and effect identification |
| Sng and colleagues' hallucination study | Consistency of causal ratings, including a supplied mocked graph | Accuracy against independently justified causal truth |
| Augur | Trend prediction and explanation consistency | Intervention recovery under declared temporal and confounding assumptions |
| ORCA and CausalPulse | Workflow outcomes plus distinct scientific metrics | Defined oracles, retained failures and matched target-level evaluation |
| CausalSmith | Reported proof checks and internal run dispositions | Statement fidelity, independent scientific significance and target assumptions |

### Relation extraction is a serious baseline, with a narrower claim

Susanti and Holsmoelle compare prompting with fine-tuned models on four
relation datasets. On DDI, Table 1 reports F1 of 67.4 for Single-Prompt C
and 87.9 for PubMedBERT: a 20.5-point difference. The paper reports
five-fold averages and explicitly limits its evaluation to binary pairwise
causality assessment. It neither demonstrates joint graph verification nor
establishes a universal advantage for fine-tuning under equal annotation
costs. The comparison does establish that a supervised smaller model deserves
consideration when the proposed task is extraction from a stable document
domain.
\cite{exec13_census_graph_validation}

For banking notes, evaluate the extraction role on held-out documents with
independently specified labels and timestamps. Track abstention and the
treatment of ambiguous or contradictory passages. Then separately evaluate
whether extracted statements are admissible graph evidence. A sentence that
says ``the waiver caused repayment'' is evidence of what the author claimed;
it is not, by itself, evidence that assignment was unconfounded. A useful
agent should retain the quotation, its source and the alternative causal
interpretations.

Sng and colleagues illustrate why agreement is a separate target. Their
retrieval experiment supplies a mocked true causal graph, and their
conclusion explicitly says that reducing inconsistent ratings does not imply
accurate causal prediction. A comparison in which one arm receives such a
graph evaluates its use of supplied information. It does not measure whether
retrieval can discover the graph in a bank setting. Registering both correct
and misleading retrieved evidence is necessary to expose that distinction.
\cite{exec13_hallucination}

### Task-specific gains should remain task-specific

In CausalEval's Table 3, GPT-4o scores 69 on CLADDER with ordinary
chain-of-thought and 76 with FunctionCall, but its e-CARE scores are 90 and
73, respectively. These are author-reported pass@1 results for the named
versions and samples. The gains and losses should remain visible rather
than being replaced by the claim that tools always improve causal reasoning.
The table is also preferable to silently repeating inconsistent numerical
values in the paper's surrounding discussion.
\cite{exec13_census_causaleval}

The study repeats each question five times with greedy decoding. Repeated
calls can reveal response variation, but five calls to the same question
are not five independent causal problems. For illustration, suppose there
are \(N\) independent mechanisms, \(m\) calls per mechanism, equal marginal
score variance \(\sigma^2\), and common within-mechanism correlation
\(\rho\). Then

\[
 \operatorname{Var}(\bar S)
 =\frac{\sigma^2}{Nm}\{1+(m-1)\rho\}.
\]

At \(N=100,m=5,\rho=1\), the effective independent count is 100, not 500.
This is a project-derived sampling illustration, not an estimate of the
paper's unreported correlation. The appropriate prototype analysis clusters
calls and paraphrases by underlying mechanism, reports the number of distinct
mechanisms, and uses paired comparisons when methods see the same cases.

CausalEval also evaluates some expensive models on 100 cases rather than
the usual 500. Its human row combines scores from original benchmark papers
with a study of three graduate students on 100 questions for remaining
datasets. A combined human/model gap therefore is not one uniform matched
experiment. Any investment argument should state the comparison actually
performed, the cost and failure accounting, and the uncertainty that remains.

### An affordable, falsifiable evaluation sequence

The proposed sequence starts with fixed causal mechanisms, explicit public
document provenance and deterministic numerical answers. It then tests
formulation, variable timing, graph uncertainty, identification, execution
and reporting separately, followed by their composition. Baselines receive
the same data, permitted documentation and tools. Model-only reasoning,
retrieval, a typed numerical workflow, and a supervised extractor answer
different engineering questions and should be included where relevant.

The primary denominator includes every attempted case, with scientific
refusals distinguished from crashes and wrong answers. Numerical accuracy
conditional on successful execution is a secondary outcome. Cost includes
failed calls, retrieval, annotation, retries and human review. Deliberately
adverse cases include an accurate quotation supporting a false causal claim,
a timestamp that makes a proposed control post-treatment, alternative
graphs with different effects, a misleading retrieved graph, and an
unsupported edit policy.

Public and generated data can establish that these failure cases are handled
as specified and can compare methods under a known law. They do not establish
the frequency of those failures in a target bank or the value of changing its
real decisions. The next expensive experiment should address a remaining
uncertainty that could change the build or adoption decision. Until such
evidence exists, the proposal can recommend a bounded prototype and a
testable research direction while preserving uncertainty about live-model
performance, source completeness and bank transport.

\label{exec13:census-evaluation-end}
