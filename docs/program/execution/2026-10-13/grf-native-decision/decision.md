# Native grf reuse decision

Reject direct native embedding and a forest-algorithm port for the initial
proposal prototype. Recommend a pinned isolated R process that invokes the
maintained C++ core. This is a route selection, not implemented or qualified
integration; integration_allowed remains false for this native seed.

The seed `seed:080` (“grf native core”) and `inherited:grf` identify components
of the same grf-labs/grf source lineage. Commit
`5bee99b51471f76cb2d63acbc8a9b0ffec408ba0`, dated 30 April 2026, declares
package version 2.6.1. The R API performs nuisance estimation/residualization
and constructs the average-effect score/uncertainty around its C++ calls.
Treating the native seed as a separate fully featured estimator would double
count the engine and omit statistical behavior supplied by the R layer.

The initial target is the ATE for complete independent customer rows, one
binary offer and a fixed scalar outcome/horizon, under consistency, no
interference, exchangeability or declared randomization, and positivity.
Use the all-sample AIPW path specified in the existing adapter contract;
averaging fitted CATEs or reporting conditional-prediction variance does not
silently implement that path. Clusters, panel/calendar dependence, continuous
treatments, IV, longitudinal policies and unresolved graph identification
remain excluded from this profile. These exclusions describe the selected
proposal route, not the complete capabilities of upstream grf.

The source declares R >= 3.5.0, C++17, GNU make, Rcpp/RcppEigen linkage and
DiceKriging, lmtest, Matrix, methods, Rcpp and sandwich imports. Those are
source requirements, not a locked or tested installed environment. The
inspected CMake target combines source and test files into an executable;
it does not establish a stable shared-library ABI. Native data uses borrowed
column-major buffers, and the inspected serialization moves tree ownership.
A direct embedding would have to preserve lifetimes, feature/role coordinates,
global runtime context, residualization, seeds, scores, uncertainty and reload
semantics together. A full port adds algorithm maintenance and conformance
obligations without a measured workload benefit in this repository.

The package declares GPL-3, source headers describe GPL version 3 or later,
and the genuine COPYING text is preserved. Section 2 expressly permits running
the unmodified program. A complete dependency/license inventory and the
intended distribution remain distinct questions. An R subprocess is an
engineering boundary; it does not decide distribution obligations. No unknown
license is reclassified as permissive and no blanket deployment clearance is
awarded by this decision.

Maintenance evidence is limited and explicit: the pinned commit has a dated
upstream identity; DESCRIPTION names a maintainer and an issue tracker; the
source declares tests/build machinery. This establishes provenance and a route
for future maintenance inspection. It does not establish responsiveness,
future support, security status or passing upstream tests at our environment.
The project-owned arithmetic/reference exercise already checks selected score,
coordinate and failure behavior. It supplies no grf forest execution or
sampling coverage result, and it is not rerun as a new vendor study.

The owner of a future adapter must first freeze the complete source and
dependency environment, implement the request/response contract, and compare
real R execution with independent exact references. Missing engine/environment
evidence returns unavailable. Unsupported targets retain the original query.
Failed assumptions/support receive explicit refusal; corrupt results, timeout,
nonfinite output or process failure cannot become a computed numeric effect.
Source identity and parameter/split/seed identity travel with every response.

Cost comparison must include conversion, nuisance estimation, forest fitting,
score/variance aggregation, serialization, validation and failed requests.
There is no observed startup-cost or end-to-end saving here. Revisit a direct
native route only if an identical-workload comparison or a concrete host
constraint justifies taking ownership of the omitted R behavior, and the
native implementation passes lifetime, parity, restart and failure tests.
Prospectively registered generated/public studies are needed for new
statistical performance claims; authentic bank data are unnecessary to make
this initial engineering choice.

The integrated monograph already develops this exact route selection in
“A native forest boundary that preserves the banking question,” including its
deployment alternatives and next informative comparison. The decision binds
that existing text and the current PDF rather than adding a duplicate chapter.
