# Recovery of a causal batch: what the selected manuals establish

A causal batch is useful only if its recovered result answers the declared
question for the declared population and information set. Finishing an execution
graph is one part of that requirement. A bank also needs to know which observations
were available, which customer mixture defines the effect, which code and numerical
configuration produced it, and whether unsuccessful requests remain visible.
The selected manuals describe substantial orchestration mechanisms that should be
compared with the proposed library before building another scheduler.

The observations below concern the authentic manuals retrieved on 22 October
2026. They do **not** establish an unchanged capability as of the client cutoff,
7 October 2026. Both Databricks manuals explicitly display later update dates;
Azure's displayed March date conflicts with an October repository-update field.
The remaining mutable manuals lack authenticated cutoff revisions. This temporal
limitation is material: even the current AWS description of payload-limit errors
permits an explicit retry/catch that an older blanket characterization would miss.
The source audit binds original bytes, extractions, exact inspected lines and
claim-specific limits. No vendor runtime or licensed deployment was exercised.

## Partial repair and the meaning of a successful run

Databricks' repair manual describes rerunning unsuccessful and dependent tasks
using current job/task settings. Each unsuccessful task starts again; the manual
explicitly warns that the service does not make task writes idempotent. An append
that succeeded partially can therefore duplicate data on repair. A new shared job
cluster uses current settings. These are precise reasons to pin input snapshots,
code, environment and output commits around a causal request. They are not evidence
that Databricks cannot support such a design. They show what the application must
make explicit when using the documented repair mechanism.

The monitoring manual distinguishes ordinary success from “Succeeded with
failures,” using leaf-task outcomes. A recovered causal batch must therefore
report both its scheduler status and the disposition of every requested effect.
A green descendant that tolerates an upstream failure cannot certify that every
customer cohort or sensitivity scenario was evaluated. The documented 60-day run
history and 48-hour graph window also motivate exporting a durable experiment
ledger. These are observations of the post-cutoff manuals, not backdated features.

Snowflake's task graphs provide dependent SQL execution, retries, finalizers,
overlap controls and graph versions. An execution DAG records scheduling
dependencies; it does not establish causal arrows or identify an intervention.
The inspected text says that graph versions include task properties but exclude
the definitions of called stored procedures. A procedure changed during a graph
run may consequently be executed in that run. A proposed replay manifest must pin
the procedure definition and its dependencies separately. The manual also says
that suspended children can be treated as successful and that a finalizer does
not start when the root is skipped. Request accounting must distinguish completed,
skipped, refused, failed and reused results rather than collapse these states.

## Reuse and recovery budgets

Azure Machine Learning's API-v2 reuse description requires a deterministic
component, ForceReRun=false, and matching code, environment, inputs, parameters,
output and run settings. The reused component displays the earlier status,
outputs, logs and metrics. This is a useful model for preserving lineage. The
application still has to express every scientific dependency in those artifacts:
a mutable external table behind an unchanged URI or an undeclared population
revision must not silently become “the same input.” The manual's determinism flag
is a declaration, not an independent test of determinism or causal validity.
The HTML contains authorization notices, but its substantive technical body was
returned; it would be inaccurate to record the entire retrieval as unavailable.

AWS Step Functions describes ordered retriers and catchers, bounded retry counts,
backoff/jitter, error classes and the resetting of retry counts on eligible
redrives. Its current text excludes DataLimitExceeded and Runtime from the
States.ALL wildcard; it explicitly permits a named DataLimitExceeded retry/catch,
while Runtime remains non-retryable. Catchers belong to Task, Parallel and Map
states, not top-level execution failures. A causal request therefore needs a
durable budget across redrives as well as a per-state retry policy. Otherwise a
new execution can obscure earlier attempts, time or cost. The documentation says
retries are billed as state transitions; an actual cost comparison still needs
the chosen service edition, region, rates, compute, storage and human work.

Dataiku's retrieved DSS 15 page establishes the scope of automation scenarios
and points to build, checking, metrics, code, trigger and failure-handling topics.
It is mainly an index. Headings do not establish its detailed transaction,
retry, concurrency or conditional-execution semantics. Those linked originals and
the cutoff edition remain to be inspected. SAS Viya, Domino and Posit are also
unread candidates; complementary discovery is necessary before any market-wide
coverage or absence conclusion.

| Family | Documented mechanism in inspected current bytes | Proposed library responsibility and unresolved evidence |
|---|---|---|
| Databricks Lakeflow Jobs, AWS edition | Partial repair with current settings; explicit idempotency warning; qualified run states | Pin scientific manifest and output commits; export request ledger; cutoff edition, native behavior and terms unverified |
| Snowflake task graphs | Dependency DAG, retry/finalizer/overlap controls, task-property versions | Pin procedure and data definitions separately; retain skipped requests; cutoff/API edition and native qualification open |
| Azure ML, API v2 | Reuse conditional on declared determinism and matching execution artifacts | Include all target/vintage dependencies in artifacts; verify temporal edition, external-input semantics and actual reuse |
| AWS Step Functions | Ordered error handling, retry/redrive semantics, transition billing | Preserve total attempt budget, failure denominators and full workflow cost; cutoff semantics and native results open |
| Dataiku DSS 15 scenarios | Automation scope and linked technical topics | Read detailed pages and cutoff edition before making semantic comparisons |

The defensible proposal is to reuse suitable orchestration and add a scientific
contract at the library/CLI/MCP boundary. This is an architectural hypothesis.
It grants no adoption or superiority decision: official documentation describes
behavior, source inspection supports a bounded comparison, and a later frozen
native trial must establish that an adapter actually preserves the contract.

## Exact public demonstration before a costly trial

The accompanying authored reference uses four stipulated units: three in group
A with effect 6 and one in group B with effect -2. The declared finite-population
effect is (18-2)/4=4. At stipulated per-unit cost 1, net value is 3. Suppose the
first two A outputs are appended before a failure and all four outputs are
appended on retry. The six-row mean becomes (30-2)/6=14/3: the computationally
complete batch has changed the population weights from 3/4 to 5/6. Its bias is
2/3. An identifier-keyed, conflict-checked atomic final commit returns the
original four unique units and effect 4. Six write attempts still belong in
the history; deduplication must not erase the failed attempt or its costs.

Idempotency alone does not fix the scientific target. Reweighting the same
group effects to 1/4 and 3/4 produces effect 0 and net -1. Changing the B outcome
vintage to effect -10 produces effect 2 and net 1 at the original mixture.
The reference's content-bound manifest rejects data, target or environment
changes before accepting a replay. A hash establishes equality of specified
bytes and declarations; it cannot prove that all dependencies were declared,
that the provenance is truthful or that causal assumptions hold. These are exact
constructed examples, not estimated bank benefits or vendor failures.

The proposed next experiment freezes a public dataset and a separate generated
potential-outcome fixture with known truth. The public dataset exercises schema,
size and custody; generated outcomes supply the causal reference. It compares
uninterrupted and interrupted executions using the same methods, targets,
randomization and resource envelope. Faults are fixed in advance: partial
writes, lost responses after commit, changed data/procedures, stale cache,
skipped children, payload limits and exhausted redrive budgets. Every requested
case remains in the denominator. Acceptance requires exact identity and status
agreement for deterministic cases, predeclared tolerances and coupled randomness
where appropriate, refusal of incompatible replays, no duplicate commits, and a
complete attempt/cost ledger. A statistical procedure retains a separate
calibration protocol; execution equivalence does not establish coverage.

At the CLI/MCP boundary, request identity binds the population/estimand,
information clock, data versions, graph assumptions, method/covariance settings,
code and environment, seed, tolerance and output schema. Responses carry lineage
and distinguish success, reuse, sensitivity limits, refusal and operational
failure. Adapters should preserve the same manifest across both entry points.
This specification can be developed with public fixtures now; native commercial
qualification, real prices, licenses, bank data and institutional acceptance are
separate later evidence. No sibling repository has been changed or integration
claimed on the strength of its presence in the workspace.
