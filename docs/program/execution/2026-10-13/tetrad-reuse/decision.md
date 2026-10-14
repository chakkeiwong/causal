# Selecting Tetrad without adopting an unrestricted discovery service
\label{exec13:tetrad-reuse}

The Java comparison and adapter contract support a concrete reuse decision.
Tetrad is the preferred Java candidate for a first restricted PC discovery
comparison, while executable admission remains deferred until its actual
environment and failure wrapper are qualified. The selected source is
\texttt{cmu-phil/tetrad} at commit
\texttt{b89afaf952a4fd647df0d85b08102250106c6764}, whose preserved commit
record is dated 22 September 2026 and whose POM declares
\texttt{7.6.11-SNAPSHOT}. A snapshot version string does not identify an
immutable binary. Any later runnable artifact must be tied to the source
revision, dependency artifacts and build configuration actually used.
\citep{exec13_tetrad_reuse_primary,exec13_tetrad_reuse_decision}

Tetrad, its Java library and its graphical application are related surfaces of
one repository. The README also directs users to Python and R bridges. Those
bridges are not independent discoveries or evidence that the selected Java
service has already been integrated. They add their own environment and
transport requirements. The root and library POMs inspected here target Java
21, whereas the README's Python and R bridge descriptions request JDK 25 or
later. These statements need not describe the same binary or execution route.
The proposed first comparison uses a direct local Java process and records its
actual compiler and runtime; it does not infer compatibility for every bridge
from either declaration. \citep{exec13_tetrad_reuse_primary}

## What the dependency and maintenance evidence establishes

Parsing the active library-POM dependency elements yields twenty direct
declarations. This count excludes commented examples. It includes numerical
libraries, data readers, serialization and text utilities, an explicit JUnit
entry, GUI-related libraries and the DJL API and PyTorch engine. Several have
no explicit scope in that POM; the data-reader version is expressed through the
project version. This is the declared module configuration, not a measured
minimal dependency set for PC. The presence of a PyTorch-related dependency
does not show that a PC request uses a GPU, and a commented dependency is not
an active requirement. \citep{exec13_tetrad_reuse_primary}

An executable comparison should therefore resolve and hash the selected
artifacts, distinguish build and runtime needs, and inspect the effective
dependency tree. Removing apparently unused dependencies without checking
imports, service loading, packaged resources and tests would create a new
distribution whose behavior needs review. Conversely, inheriting the complete
application environment may impose avoidable setup and maintenance costs.
These two alternatives can be measured on the same PC request; neither is
declared faster or cheaper in this proposal.

The source tree and README provide a maintenance route: a named project,
build/test commands and an issue tracker. The inspected PC tests include
graph-oracle assertions and a result explicitly described in its comment as
a regression snapshot. That snapshot is useful for detecting a changed
implementation, but it is not an independent proof of a statistical property.
No upstream CI success, current support service level or future response time
has been measured. Upgrades must repeat semantic, numerical and failure checks
instead of relying on an unchanged method name. \citep{exec13_java_tetrad,
exec13_tetrad_reuse_primary}

## Rights and the actual reuse choice

The saved root license is GPL version 3; the inspected PC source header grants
version 3 or later. The license's basic permissions explicitly address running
an unmodified program and making/running works that are not conveyed. Its
conveyance sections require preservation of notices and, in the applicable
object-code arrangements, corresponding source. Modified source has additional
notice and license conditions. These primary terms support consideration of
a local research comparison while leaving the actual packaged distribution
and third-party components to be reviewed. A process boundary is an engineering
choice, not a blanket exemption from these terms.
\citep{exec13_tetrad_reuse_primary}

The proposal therefore selects the restricted Java PC route for further work
but does not yet mark an engine as available. Direct unrestricted adoption is
rejected for this route because it would expose unreviewed algorithms, defaults
and input regimes under one apparent guarantee. Porting PC into a new local
implementation is deferred: it would add responsibility for orientation rules,
tests and maintenance without a measured deployment constraint that justifies
the duplication. The existing shared semantic layer and exact examples remain
useful regardless of the selected engine. The choice can change if resolved
dependencies, distribution obligations or measured workflow costs make another
candidate more suitable. \citep{exec13_tetrad_reuse_decision}

## The first comparison has a graph target and a failure contract

The retained prototype profile concerns complete IID continuous data under
explicit linear-Gaussian, acyclic, causally sufficient, faithful and
no-selection assumptions. It uses the fixed settings specified by the Java
adapter contract and retains the banking target, population, units, sampling
unit and information clock. The immediate output is a validated CPDAG. It is
not an intervention estimate, an effect confidence region or a declaration
that the assumptions are true. Latent-variable FCI, FGES, time-series search,
background-knowledge constraints and missing-data procedures require separate
profiles. \citep{exec13_java_adapter_contract}

The independent exact reference gives three Gaussian causal models with the
same observed covariance and the same noncollider chain class. Their
intervention responses from the first to the third variable are zero, zero
and \(2/5\). Thus a unique selected orientation can change a banking
recommendation while leaving the observed law unchanged. An adapter must
retain the unresolved chain rather than silently report one member's effect.
The reference also checks endpoint direction, isolated variables, unit
conversion and changes in scientific context. These are project calculations,
not outputs from a Java executable. \citep{exec13_java_adapter_oracles}

Failure handling is a material selection condition. In the pinned Fisher-Z
implementation, \texttt{checkIndependence} catches a singular-matrix exception
and returns a dependence result with \(p=0\). The exception-preserving
\texttt{getResult} path permits a different wrapper design. That wrapper must
validate each result, record a failed numerical query and withhold the job's
graph when its computation did not complete. The inspection establishes source
behavior at one revision; it is not a measured failure rate or a claim that
every data set triggers it. \citep{exec13_java_tetrad}

The stable skeleton search also uses parallel work. Its pair routine catches
an interruption, restores that worker's interrupt flag and returns from the
pair. The parent wrapper therefore needs a job-level failure state and complete
terminal query records before publication. An independent whole-process time
and memory limit complements the engine's cooperative behavior. Neither a
returned graph object nor an elapsed timeout setting alone proves that every
required query completed. The complete interface, concurrency behavior and
failure propagation remain implementation tests, not benefits already
delivered by the contract. \citep{exec13_java_adapter_source,
exec13_java_adapter_contract,exec13_tetrad_reuse_decision}

## Alternatives, costs and a revisable admission decision

The first executable comparison should include the separately reviewed R or
Python PC candidate using the same scientific assumptions, test settings,
data and graph target. Such a comparator is selected only after its own
source and environment review. Weka's predictive Bayesian-network workflow,
supplied commercial latent-model fits and symbolic effect-identification
engines answer different questions; they can be useful components without
serving as substitutes for this CPDAG comparison.
\citep{exec13_java_tetrad,exec13_tetrad_reuse_decision}

Measure environment setup, retained disk footprint, full-request runtime,
peak memory, conversion overhead, analyst corrections and maintenance effort.
Failed queries, numerical failures, cancellations and unsupported requests
remain in the account. A computation of the wrong scientific object cannot
win by being fast. No vendor price, bank workload or analyst-time saving is
assigned from the current source inspection.

Three responsibilities make admission concrete. The adapter maintainer resolves
and records the build/runtime and dependency rights. The scientific reviewer
checks the selected profile, graph-class recognition and matched references.
The workflow owner evaluates full-request failure handling and the actual cost
against a usable baseline. These are proposed roles, not fabricated acceptance
by named institutions. Revisit executable admission when the pinned build,
conversion, graph-class, numerical and interruption cases have actual results;
reopen the choice when revision, license, API, dependency or target assumptions
change. Other proposal and prototype work remains independent of this local
admission question. \citep{exec13_tetrad_reuse_decision}
\label{exec13:tetrad-reuse-end}
