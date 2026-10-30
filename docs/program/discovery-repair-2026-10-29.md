# Discovery repair: when a search shortcut changes the question

This is an independent S01/S02 scientific continuation while the separate
editorial pass reads chapters. It answers a recorded Aitiotita follow-up:
can removing the all-neighbour screening rule recover the intended skeleton,
and how should a bounded search report an unfinished result?

## Research question and reviewed design

Compare two project-authored stable skeleton searches with the same exact
conditional-independence oracle: exhaustive neighbour subsets, and the same
search with the inspected depth-greater-than-two all-neighbour screen. The
screen freezes a link if dependence remains after conditioning on the union
of neighbours. This is a source-derived logical comparison, not a Java run.
The bundled linguistic oracle, arrow rules and complete package are outside
this experiment. A third run limits conditioning depth to two and must label
remaining untested adjacencies as unresolved rather than proved causal links.

Use every acyclic graph whose arrows follow a fixed order for n=2,...,5
(1,098 graphs); 256 seeded ordered six-node graphs with edge probabilities
0.15, 0.35, 0.65 and 0.85; and the existing six-node three-confounder/collider
witness under 24 fixed relabellings. Also inspect the analogous witness with
four and five independent common causes. These finite cases are not a uniform
distribution over all DAGs and cannot estimate a real-world failure rate.
The seed is 20261029 and serves reproducibility, not model tuning.

The main correctness reference is the generating graph's undirected skeleton.
The primary independence oracle moralises the ancestral graph. Independently
check it against active-path enumeration for every conditioning set in all
four-node ordered DAGs and all queries actually used on the six-node witness.
Use rational covariance arithmetic for the Gaussian witness and a separate
structural-substitution derivation to show its intervention and regression
consequences. Exact oracles eliminate sampling error only for this comparison.
They do not establish practical faithfulness, test calibration or bank truth.

Promotion criterion: full search equals the reference skeleton on every
declared case; all removed links have verified separators; the independent
oracle agrees; capped results carry an explicit incomplete-search status.
A failure of the screened candidate is an expected diagnostic, not a reason
to stop testing the repair. An oracle disagreement, incorrect generating
graph, missing trace or arithmetic error stops the affected inference until
repaired. Preserve each failed attempt.

Count actual independence requests and distinct queries, plus elapsed time.
No claim about Java speed follows. The stable search freezes neighbourhoods
within a depth and deduplicates identical subsets across endpoints; the same
convention applies to both candidates. Stop after 10 CPU minutes or two local
infrastructure retries. No new package, network permission, GPU or paid model
is required. Compile and inspect a separate reading supplement, then integrate
it into a named successor without changing the concurrent editorial files.

## Skeptical review

The earlier work already proves a counterexample; repeating it alone would
not be progress. This study instead tests an explicit repair against an
independent oracle, locates the cost/validity tradeoff and defines what a
budget-limited result can honestly say. Skeleton recovery is not effect
identification or orientation recovery. The generated law is a hypothetical
banking example, and its financial units and uncertainty limits must be
explained. No source census or native adapter status is automatically closed.
