Reporting causal results and monitoring their continued applicability {#exec16:reporting}
=====================================================================

A servicing manager needs to know whether a contact policy improves
thirty-day net recovery, which accounts the conclusion concerns, and
what could make it inapplicable next month. A fluent explanation is
useful only if it preserves the answer supplied by the scientific
analysis. A point estimate must not emerge from a set of unresolved
possibilities; a failed retrieval must not become evidence that an
assumption is false; and a successful replay must not certify that a
customer's information was available at the historical decision time.
Reporting joins the earlier formulation, identification, estimation and
artifact contracts. Monitoring asks which parts of that argument still
apply after the context changes.

A banking report starts with a target and an information clock
--------------------------------------------------------------

Let $P$ be the eligible account population at the first servicing
decision, $\pi$ a frozen contact policy, and $\pi_0$ its comparator.
Write $Y_{30}^{\pi}$ for thirty-day cash receipts and $C^\pi$ for the
associated contact costs, both measured in USD per eligible account. The
proposed target is $$\theta(P,\pi,\pi_0)
   =\mathbb E_P[Y_{30}^{\pi}-Y_{30}^{\pi_0}]
     -\mathbb E_P[C^\pi-C^{\pi_0}].$$ The report must bind the
eligibility rule, treatment versions, outcome horizon, currency and
censoring convention. A later change of price can change the second term
without changing the already computed cash-receipt contrast. A change of
assignment or historical feature availability can instead undermine the
interpretation of that contrast itself.

At every action time, the available history contains only values whose
availability precedes the decision. Event time, availability time and
reporting time answer different questions. A recovered timestamp for a
transaction does not prove that the decision system could see it then.
Consistency, an appropriate sequential assignment assumption, policy
support, and the declared observation and dependence laws remain
premises of the longitudinal analysis. The language layer may explain
those premises, organize their evidence and flag contradictions. It
cannot make them true by restating them. The preceding policy chapter
supplies the identification route; the present chapter carries its
meaning into a decision report.

Consider a stipulated finite result object whose possible gross gains
are $\{0,100\}$ USD per account and whose incremental cost is $40$ USD.
Subtracting that cost gives the net set $\{-40,60\}$. Neither a
probability distribution over the two cases nor a sampling confidence
level has been supplied. The midpoint is $10$, which is not even a
member of this set. Reporting an expected gain of $10$, or a $95\%$
chance of benefit, introduces information that the result object does
not contain. The convex hull $[-40,60]$ can be displayed as an
explicitly labelled outer envelope, but it also contains values absent
from the original object. Under a stipulated worst-case criterion
relative to doing nothing, the minimum gain is negative; under a
probability-weighted criterion, further weights are needed. A useful
report explains this decision ambiguity and the information that would
resolve it. The exact calculation is a project reference, not a bank
estimate. [@exec16_report_oracle]

Evidence-grounded auditing: useful questions and unfavorable answers
--------------------------------------------------------------------

ARGUS studies whether reported evidence supports identification
assumptions in climate-policy evaluations. Its construct is
reported-evidence adequacy, not causal validity. An auditor can locate
an assignment description or an overlap diagnostic without certifying
the actual assignment mechanism or the unobserved outcomes. In its
eleven injected-flaw cases, the paper reports detection rates of $.182$
for a keyword method, $.727$ for a two-stage pipeline, $.818$ for a
single-pass variant and $1.000$ for a per-dimension variant, with zero
synthetic false alarms in those headline rows. These are small,
constructed cases. Changes in evidence access and pipeline structure
prevent attributing the entire difference to one judging component.
[@v12_la_2609_30867]

The same paper's reconciled five-paper pilot is less reassuring. Of $55$
assumption cells, the human labels comprise seven low, forty-six medium
and two high cases. ARGUS abstains on $22$; among the $33$ answered
cells, $25$ judgments are too severe. Both annotators find relevant
reported evidence in $19$ of the $22$ abstained cells, and at least one
finds it in $21$. An abstention is consequently not interchangeable with
a substantive high-risk finding. A rule using retrieval quality and
evidence status increases agreement on answered cells from $8/33$ to
$25/33$ in the same pilot. Always predicting medium gives $26/33$ on
that selected subset. Weighted kappa increases from $.08$ to $.23$, with
an interval including zero. The alternative abstention rule reduces
answered coverage from $33/55$ to $13/55$. The improvement is in-sample
and does not qualify future bank monitoring.

These findings imply a practical remedy. A report should distinguish
evidence found and supportive, evidence found and adverse, inadequate
retrieval, conflicting evidence, and an assumption requiring external
facts. Each judgment needs the inspected passage, its source version,
the claim being assessed and the reason for the disposition. Missing
retrieval should trigger a bounded retrieval or human-review route. It
should not increase a scientific risk score by an undocumented
convention. Calibration requires held-out examples, a declared labeling
protocol and a reported coverage--error tradeoff.

The observational causal inference workflow of Chou and colleagues
offers a different form of assistance: a human principal, actor and
critic coordinate analysis notebooks, diagnostics and versioned reports.
The authors report $192$ satisfactory and $39$ unsatisfactory critic
judgments across $231$ ACIC datasets. Their smaller scaffolding
comparison is favorable, but a disguised LaLonde evaluation using twenty
bootstrap replications has median absolute percentage errors of $52\%$
for PSID and $19\%$ for CPS; the critic declines the PSID result in all
but one replication. These results motivate both assistance and refusal.
They do not make a critic's acceptance a new confidence guarantee.
Moreover, the inspected notebook's uniform average after propensity
trimming targets the retained population; calling it ATO does not make
it the conventional overlap-weighted estimand. A report must bind the
actual population and weighting, even when a package's label is
familiar. [@v12_la_2607_22443; @v12_la_package_oci_agent]

For discovery, *Causal Discovery in the Era of Agents* separates agent
suggestions, user decisions, algorithm settings and graph output. Its
proposed benchmarks for method selection, diagnosis and interpretation
remain an evaluation agenda. A reporting assistant should preserve CPDAG
or PAG ambiguity and the restrictions under which an effect query is
answered. The medical causal-copilot paper likewise proposes assistance
with target specification and study design while acknowledging
contamination and inadequate study-design benchmarks. Its discussion of
missed or false post-market signals motivates evaluation; it does not
supply a validated alarm procedure. These are substantive design
contributions with different evidential status from completed
causal-effect studies. [@v12_la_2606_23608; @v12_la_2407_19118]

What adjacent monitoring and repair literature contributes
----------------------------------------------------------

CausalPulse coordinates manufacturing diagnostics through agents, domain
rules and tools, including an MCP utility layer. Its inspected
evaluation distinguishes workflow completion from root-cause
attribution: PSE planning and tool-use success are reported at
$98.75\%$, while root-cause Hits\@1 is $.44$ and F1 is $.39$. The local
hardware and workflow timings are author-reported manufacturing
evidence. A bank report should borrow the separation of stages and their
denominators. Reusing a cached graph also requires its contextual
applicability to be checked; cache availability alone does not settle
that question. [@exec13_pulse]

FlowFixer makes workflow repair more concrete. It converts execution
traces to symbolic descriptions, infers behavioral assertions,
attributes failures, proposes edits and verifies candidates. The
evaluated collection combines $307$ AgentFail logs with $136$ n8n
failure cases. The reported repair success is $71.3\%$, compared with
$59.4\%$ for ReCreat, an absolute difference of $11.9$ percentage
points. Failure-attribution accuracy is $84.4\%$; the reported $87.9\%$
root-cause accuracy is conditional on correct failure attribution. These
percentages do not share a denominator. Repairs are repeated three times
per case and assessed through dynamic verification on the original
inputs. Passing those inputs does not establish generalization to an
unseen incident or preservation of a causal estimand.
[@exec16_report_flowfixer]

The proposed reuse is methodological: make dependencies explicit,
separate symptoms from an attributed cause, and check an edit against an
executable contract. An inferred assertion that an itinerary respects a
budget is not the same kind of statement as sequential exchangeability.
FlowFixer's pre-execution filter reports $99.7\%$ precision and $84.6\%$
recall for invalid workflows; some model and tool failures still appear
only at execution. For a causal report, a repair should preserve the
frozen target, inputs and uncertainty type, then be tested on separate
adverse cases. Changing the target or deleting failures to obtain a
successful narrative is a scientific change requiring a new analysis.
The paper justifies studying this mechanism; its distribution,
dependency rights and actual integration remain to be reviewed.

PSEBench supplies an adjacent benchmark construction. Human-reviewed
clause cards factor policy conditions, facts, evidence anchors and
constraints, then generate complete, missing-information and uncertain
cases. The cutoff-compatible second version contains $3{,}455$,
$1{,}362$ and $257$ cases in these groups. The authors compare fifteen
models and report separate verdict, evidence-citation,
missing-information and uncertainty metrics. For example, the paper
reports $90.2\%$ verdict accuracy and $12.8\%$ uncertainty-detection F1
for its GPT-5 configuration. This is a reported configuration result,
not a current model recommendation or our replication. Its meaning is
that classification success can coexist with a large weakness in
identifying cases that should remain unresolved.
[@exec16_report_psebench]

The benchmark reports expert review of ninety generated cases: agreement
on $28/30$ complete verdicts, $29/30$ missing-case indeterminacies and
$30/30$ uncertain-case ambiguities. That supports a bounded quality
check, not universal correctness of generated labels. The narratives are
synthetic, the Ask tool idealizes retrieval, and the rules are tied to
Minnesota's framework. For banking, the transferable idea is to author
explicit result-and-evidence cards with separately known failure
dispositions. Medical reportability labels should not be imported as
causal truth. Generated cases can test faithful reporting now, while
realistic retrieval failures and different institutional meanings need
distinct later evidence.

The NetOps/AIOps survey adds an operational perspective. Its inspected
preprint distinguishes freshness and provenance of logs, metrics, traces
and change records, and separates static questions, trace replay,
sandbox execution, live testbeds and canary evidence. It recommends
scoring tool costs, abstention, latency, drift and trace quality
separately, with LLM judging as an auxiliary signal. These are helpful
contract categories. Proposed service invariants written using
probabilities do not themselves provide calibrated probability models.
The retrieved June preprint is not assumed identical to the journal
edition identified in the original search metadata.
[@exec16_report_netops]

An economic illustration supplies a caution closer to the application
domain. Kim presents ChatGPT-generated growth and stock-market diagrams
and explicitly says that the backdoor response needs confirmation and
that the generated figures should not all be believed correct. The paper
can motivate checking the distinction between a prediction and an
intervention query. It cannot support a claim of verified economic
forecasts or calibrated causal alarms. This negative interpretation is
more informative than counting every paper with causal terminology as
affirmative evidence. [@exec16_report_kimeconomy]

The report object and the actual implementation gap
---------------------------------------------------

The proposed report has three linked layers. Its scientific layer binds
the target, population, clocks, graph or graph class, assumptions and
exact result type. Its evidence layer binds the source data, code,
environment, diagnostics, source passages and review dispositions. Its
decision layer states the monetary conversion, loss criterion,
alternatives and unresolved obligations. A sentence asserting a number
must point to a specific field or a separately checked derivation. A
sentence asserting a premise must identify whether it is stipulated,
supported, contradicted or unknown. These links distinguish faithful
transcription from scientific endorsement. [@exec16_report_contract]

The current local report implementation provides a narrower foundation.
It accepts one to one hundred distinct authorized canonical-response
artifacts, checks their schema, binds input hashes and execution
identity, and verifies a completed checkpoint prefix before resumption.
Its summaries retain declared status, disposition, context hash,
qualification and source reference. The verification flag explicitly
says that the check is schema-only and is neither causal nor external
review. The inspected worker does not yet copy the full numerical result
into a developed causal narrative or implement an assumption-monitoring
service. The agent workflow also preserves unresolved obligations and
denies authorization for a bank action.
[@exec16_report_sources; @exec14_custody_implementation; @exec14_failure_implementation]

OCI's pinned notebook runner checks interpreter identity and serializes
per-estimand estimates, intervals and diagnostics. It also accepts a
selected notebook and uses an unbounded notebook timeout. Its artifact
concepts can inform the proposed report boundary, but execution requires
separate resource and authority limits. The inspected CausalAgent output
parser extracts text between the first and last braces and returns an
empty dictionary on a JSON decoding error. A consumer must preserve that
condition as a typed parse failure; an empty object must not silently
become successful analysis. These are static source observations, with
no new upstream execution.
[@v12_la_package_oci_agent; @v12_la_package_causalagent; @exec16_report_sources]

The proposed CLI and MCP operations should use the same scientific
object as the library. A report request selects immutable result
references, an audience, a template revision and a bounded presentation
budget. It does not supply a replacement estimate. The response includes
generated prose, checked claim links, unresolved statements and a
reference to deterministic rendering. A change-review request supplies a
versioned event and returns affected dependencies, reasons and proposed
follow-up work. It does not mutate old results. Both operations
distinguish unsupported input, retrieval failure, invalid result
structure, unresolved science and completed presentation. The new fields
and monitor remain a proposed extension; the existing schema-only report
is not retroactively described as implementing them.

Denominators and uncertainty after a critic selects reports
-----------------------------------------------------------

Suppose a generated evaluation contains one hundred requests. Sixty
produce computed answers, of which forty-eight are correct; twenty are
ambiguous, ten are unsupported and ten fail retrieval. Conditional
computed-answer accuracy is $48/60=.80$, whereas correct computed output
per submitted request is $48/100=.48$. Neither fraction determines
whether the ambiguous or unsupported dispositions were appropriate.
Those require independent case-level labels, and correct refusals can be
useful outcomes. A report should show the full partition, the scientific
status within each group and the corresponding cost. Dropping an
expensive failure changes both the quality and economic comparison.
[@exec16_report_oracle]

Selection also changes uncertainty. Let $C$ be the event that an
estimated interval covers the true effect and $A$ the event that a
critic accepts the report. Then
$$\Pr(C\mid A)=\frac{\Pr(C\cap A)}{\Pr(A)}.$$ Marginal coverage
$\Pr(C)=.95$ supplies no equality between this conditional probability
and $.95$. In an exact constructed law with one hundred equiprobable
cases, ninety-five intervals cover. Let acceptance select five covering
and five noncovering cases. Acceptance is $10\%$ and coverage among
accepted cases is $5/10=.50$. The example does not assert that a
particular critic behaves this way. It disproves an unjustified
inference.

A possible remedy is to qualify the complete selection-and-estimation
rule, including every refusal, under a declared joint experiment.
Another is to design an appropriate conditional inference procedure and
establish its assumptions. A genuinely independent acceptance event
would preserve marginal coverage, but the required independence often
fails when a critic reads the same data, intervals and diagnostics.
Adding a second agent, or training the critic elsewhere, does not
establish independence of the acceptance event in the current analysis.

Monitoring requires a statistical design and an owner
-----------------------------------------------------

A service can monitor whether an artifact hash changed, whether a
response arrived, whether a measured distribution shifted, or whether a
causal claim remains applicable. These are different events. The first
two admit direct engineering checks. Distributional change can sometimes
be tested under a specified sampling law. Continued causal applicability
depends also on assignment, measurement, support and target population.
The catalog example's observationally equivalent worlds demonstrate why
an unchanged observed distribution need not settle an intervention
contrast. Repeated queries to the same observations cannot remove that
ambiguity. [@exec16_dh_exact]

Even a valid individual test needs a repeated-use design. For twelve
independent tests under their nulls, each with false-alarm probability
$.05$, $$\Pr(\text{at least one false alarm})=1-.95^{12}
       \simeq .459640.$$ Independence is required for this exact product
formula. A simple alternative allocates the total budget through
$$\alpha_t=\frac{.05}{t(t+1)},\qquad
 \sum_{t=1}^{T}\alpha_t=.05\frac{T}{T+1}<.05.$$ If each test has a valid
null rejection probability bounded by its allocated $\alpha_t$, a union
bound controls the probability of any false rejection; independence is
unnecessary for that bound. For adaptive choice of a test or population,
validity must survive that choice, for example through an appropriate
conditional guarantee. Four equally budgeted monitor families would each
receive $.0125$, rather than independently spending the full $.05$. The
allocation, tested family, restart policy and observation clock must be
explicit. An LLM's severity label is not a p-value.
[@exec16_report_oracle]

This spending construction is a transparent reference, not a recommended
high-power monitor for every dependent banking series. Late thresholds
can be stringent, repeated looks can reuse dependent observations, and
weak support can make effects uninformative before any test rejects. A
proposed monitor must state its null, unit, dependence assumptions,
delay, false-alarm criterion, detectable changes and response policy. A
scientific owner decides whether the signal warrants a new design or
narrower claim; the data owner explains availability and assignment
changes; the operator owns delivery and recovery. The agent may
summarize signals and prepare the review. No bank-action authority
follows from its text.

Version changes should invalidate the affected argument
-------------------------------------------------------

Let a dependency graph connect clocks and assignment to a design, the
design and cohort to an estimate, the estimate and prices to economics,
and the estimate and economics to the report. This graph describes
provenance and applicability, not causal relationships between
customers. A change in price reopens economics and the report while
preserving the stored statistical estimate. A change in the availability
clock reopens the design, estimate, economics and report. A change to an
unrelated cohort reopens its own estimate without invalidating this
entire analysis. The exact reachability example reproduces all three
behaviors. [@exec16_report_oracle]

Reachability identifies review obligations, not a verdict that every
descendant is wrong. A source correction may be editorial; an assignment
correction may be decisive. Each change carries its effective time,
observation time, affected field, old and new identity, evidence and
responsible reviewer. Historical artifacts stay immutable. A separate
applicability state records current, review-required, superseded, or
unknown, with a reason. Revalidation creates a new linked decision. This
prevents an old report from being silently rewritten while also
preventing a stable byte hash from being mistaken for current scientific
validity.

A public and generated prototype can settle the next engineering questions
--------------------------------------------------------------------------

The immediate comparison can use frozen public source passages and
authored result cards. Begin with a deterministic renderer that carries
all numbers, units, result types and dispositions exactly. Add a
constrained language renderer that may explain those facts, and then an
optional retrieval assistant. The prototype case families should include
the finite set and selection examples above; a conflicting citation; an
absent passage; a late feature; a revised price; an unchanged observed
law with unresolved causal meaning; malformed output; a stale
dependency; and an appropriate refusal. Withholding a necessary fact
differs from stipulating that two possibilities remain observationally
indistinguishable. [@exec16_report_contract]

Before any optional live-model experiment, freeze the generator, truth
fields, source snapshots, split unit, budgets, prompts, model revision
and evaluation rules. Keep related variants on the same side of a split
so that near-duplicate cards do not masquerade as new evidence. Verify
quantitative and structural statements deterministically. Independently
review scientific meaning and explanation quality, with an adjudication
rule for disagreement. Report coverage, wrong numbers or units, lost
ambiguity, unsupported claims, correct and incorrect refusals,
provenance defects, delay and full cost. Generation, retrieval, human
review, retries, storage and maintenance belong in that cost. A
readability gain is useful only alongside an explicitly acceptable
semantic error profile.

The exact authored cases have been executed; this comparative model
experiment has not. A first finite conformance gate requires every
declared number, unit, result type and mandatory limitation to survive
the selected reference cases. Passing establishes those cases only.
Generalization and alarm calibration require fresh evaluations under
their declared laws. Rights and complete dependency review precede
adoption of adjacent packages. A manual report remains an alternative
when automation saves too little review effort.

The literature limits are concrete. The broad safety-review PDF was only
partially retrieved; the marketing context-graph original returned an
access denial; and the traceable-agent bioinformatics lead returned an
HTML download page. None supplies technical evidence here. Their next
step is an authentic accessible original, version verification and
inspection of relevant methods and adverse findings. Meanwhile, the
public and generated comparison can proceed. It can establish faithful
handling of declared evidence and known cases; bank assignment truth,
general causal identification, selective calibration and useful
institutional monitoring remain separate questions.
[@exec16_report_contract]
[\[exec16:reporting-end\]]{#exec16:reporting-end
label="exec16:reporting-end"}
