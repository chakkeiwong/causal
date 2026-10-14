# Mathematical qualification of the software census

Scientific source/document qualification of the 44-project census. Inputs/outputs are proposed adapter contracts; only statements in evidence findings are claims about inspected software. Acceptance tests and restrictions are proposed, not executed adapters or runtime qualification.

Observed package versions and README/source bytes are independent observations unless a source URL pins a commit. Hashes identify inspected bytes; a commit-pinned API is not automatically the published package release.

Cutoff: 7 October 2026. Inspected: 8 October 2026. No reviewed package was run by this qualification pass.

## dowhy: Identification front end

Repository: `py-why/dowhy`. Observed package version: `0.14`. License observation: MIT.
Source snapshot: [dowhy.json](software/dowhy.json), SHA-256 `21e1ac5c0dccf35bca5ab1f5e39c88e56f33e29878f353370e830439dbbb6d31`.

**Mathematical input.** A named observed/latent graph, intervention variables, outcome and target population.

**Mathematical output.** An identification expression, or a recorded identification failure; estimation is a separate operation.

**Scientific restrictions.** The supplied graph and intervention semantics are substantively justified; the selected identification algorithm applies to its graph class.

**Proposed adapter behavior.** Keep graph and expression identities. A successful identify_effect call does not imply an available estimator for its returned expression. Do not reinterpret an unsupported expression as nonidentification.

**Proposed acceptance test.** Use adjustment, front-door and nonidentified latent-IV witnesses; independently evaluate supported expressions on finite laws and verify unsupported-estimator status.

**Inspected support.**

- `docs/literature/raw/api_dowhy.txt` lines 234--310, SHA-256 `a8e4ad065055de504c5e28cc7ee1a7a3e3db9068e1d847c17c0d3dbe3edc3b0f`: identify_effect selects IDIdentifier for id-algorithm; estimate_effect requires a separate method and identified estimand. (primary_technical_text).

## econml: Heterogeneous effects and dynamic moment estimation

Repository: `py-why/EconML`. Observed package version: `0.17.0`. License observation: MIT.
Source snapshot: [econml.json](software/econml.json), SHA-256 `9804fa71e3a59ed318bb0345007d81a5c75d23b2471d6d4ca2aec48fe31dc7a1`.

**Mathematical input.** Outcome, treatment, controls, heterogeneity features and estimator-specific IV or equal-length trajectory groups.

**Mathematical output.** A selected CATE or structural blip coefficient with its model-specific inference object.

**Scientific restrictions.** Exchangeability or valid-IV assumptions, residual relevance, specified treatment-response form, and independent/dependent sampling assumptions appropriate to the selected estimator.

**Proposed adapter behavior.** For inspected DynamicDML, sort and validate actual periods, require equal group lengths and group-aware splitting, restrict heterogeneity features to baseline. Reject nontrivial sample_weight or sample_var because fit warns and ignores both. Do not pad missing periods without an observation model.

**Proposed acceptance test.** Permute rows then reconstruct chronological groups and obtain equivalent inputs; reject duplicate/missing periods and unsupported weights. Compare the backward blip solution with a finite linear oracle.

**Inspected support.**

- `docs/literature/raw/api_econml_dynamic.txt` lines 603--682, SHA-256 `ba4f200a3e87ef543893c1146c7ba5b30f2dc93471f6a49f4fd02e5f37db036f`: Equal-length groups, occurrence-order periods, baseline heterogeneity, group-aware CV; weights and sample variance ignored. (primary_technical_text).

## doubleml: Orthogonal score and inference reference

Repository: `DoubleML/doubleml-for-py`. Observed package version: `0.11.4`. License observation: BSD-3-Clause.
Source snapshot: [doubleml.json](software/doubleml.json), SHA-256 `95cc4b0a829fdbd224001821336944d7d7da60000f62a1ed1942fe54bb60ae26`.

Selected API commit: `6884b5f9816f180324d854a4d81b22e9d334f5e0` (2026-09-23T14:49:03Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Outcome, treatment, covariates, optional instruments and explicit cluster variables; separate static or staggered-adoption panel schema.

**Mathematical output.** Specified score-model coefficient and inference; data containers alone return no causal effect.

**Scientific restrictions.** The selected PLR/PLIV/IRM/IIVM or panel score matches the identified target, nuisance rates and sampling structure.

**Proposed adapter behavior.** Do not treat DoubleMLPanelData as an arbitrary trajectory container. Default static_panel=False treats d as first-treatment timing; constructor permits only one treatment column. Distinguish clustered scores from general time-series inference and explicitly list adjustment columns.

**Proposed acceptance test.** Round-trip treatment-date and static-treatment examples without target change; reject two treatment columns and mixed cohort/action encoding. Compare a selected orthogonal score with its finite-law remainder and cluster-level splitting.

**Inspected support.**

- `docs/literature/raw/raw_readme_doubleml.md` lines 26--62, SHA-256 `3acd95665390a87abdd0afa58006c7d7506ab040d82e456d0fa653a76d495e4b`: Model families, fit, bootstrap, confidence intervals and tuning. (primary_technical_text).
- `docs/literature/raw/r3g_api_doubleml_base.txt` lines 81--176, SHA-256 `8b64f384520aa46f4c160e97941708d4bddaa6be9a87620ba4cfae428e3ba1b8`: Data roles and cluster_cols belong to DoubleMLData. (primary_technical_text).
- `docs/literature/raw/r3g_api_doubleml_panel.txt` lines 11--145, SHA-256 `b187b13487f78497fd7706b2069de9dc0200c0911a226fe180532613304f4f92`: Long-format panel semantics, static_panel default and single-treatment restriction. (primary_technical_text).

## causalml: CATE and targeting challenger

Repository: `uber/causalml`. Observed package version: `0.17.0`. License observation: Apache-2.0.
Source snapshot: [causalml.json](software/causalml.json), SHA-256 `06a69025b92ea9d9be2eece32874b7bcc80b7e481d3ab25d3f900cdce14be18b`.

**Mathematical input.** Experimental or observational (X,T,Y) with a separately established causal design.

**Mathematical output.** Method-specific heterogeneous-effect predictions used as inputs to targeting analysis.

**Scientific restrictions.** Exchangeability, support and treatment consistency; CATE estimation and policy evaluation have separate accuracy and uncertainty requirements.

**Proposed adapter behavior.** Limit the current qualification to the documented CATE/uplift role and benchmark facilities. Preserve method/target definitions; do not certify a policy from uplift ranking alone. Detailed method APIs require additional inspection before implementation.

**Proposed acceptance test.** Evaluate effect calibration and held-out policy value under known heterogeneous effects and a confounded challenger; separate treatment-response prediction from causal ranking.

**Inspected support.**

- `docs/literature/raw/readme_causalml.md` lines 14--73, SHA-256 `cf374e9759db7dc53d16c0ae8b81e401a4b919db2b9e31ba3220e11483e75826`: CATE/uplift purpose, experimental API warning and benchmark dataset/metric declarations. (primary_technical_text).

## grf: Honest local-moment forest reference

Repository: `grf-labs/grf`. Observed package version: `not established`. License observation: GPL-3.0.
Source snapshot: [grf.json](software/grf.json), SHA-256 `ef11e1453230ff6fc0137c100d052984b79310e21322c975b92609e8ae041472`.

Selected API commit: `5bee99b51471f76cb2d63acbc8a9b0ffec408ba0` (2026-04-30T18:40:08Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Numeric X,Y,W, nuisance predictions, optional sampling weights and clusters.

**Mathematical output.** Binary-treatment CATE; for continuous W the documented local covariance/variance coefficient, with selected forest uncertainty.

**Scientific restrictions.** Unconfounded treatment and support; forest regularity and sampling assumptions; a continuous-treatment projection is not automatically a pointwise dose derivative.

**Proposed adapter behavior.** Preserve equalize.cluster.weights and sample.weights as target metadata. Equalization requires sample.weights=NULL. Record honesty and ci.group.size; the latter must be at least two for interval computation.

**Proposed acceptance test.** Two clusters of sizes 1 and 9 with effects 0 and 10 distinguish cluster mean 5 from unit mean 9; verify target metadata and weighted aggregation. Compare continuous-treatment projection with a nonlinear dose derivative.

**Inspected support.**

- `docs/literature/raw/r3g_api_grf.txt` lines 1--74, SHA-256 `55910469846d24075b04e614fe06fb3473f7ed58ea75e698497d6f4f07c16c3d`: Binary/continuous estimands, sample/cluster weights, honesty, interval group size and seeds. (primary_technical_text).

## tigramite: Temporal graph equivalence and graph-based effects

Repository: `jakobrunge/tigramite`. Observed package version: `5.2.10.1`. License observation: GPL-3.0.
Source snapshot: [tigramite.json](software/tigramite.json), SHA-256 `ba3aa889012876325142d079e18a11a827f64b9175f670dd58106aca47fe1c0a`.

**Mathematical input.** Time series, declared lag window, masks, background knowledge, discovery method and conditional-independence test.

**Mathematical output.** Method-specific directed/undirected lag graph, time-series CPDAG or PAG; effects additionally require an assumed graph.

**Scientific restrictions.** Method-specific stationarity and hidden-variable conditions; CI-test family matches distribution and dependence; an observed mask does not itself justify missingness.

**Proposed adapter behavior.** Retain every endpoint, lag, test, window and method. PCMCI+, LPCMCI and regime variants are different model classes. A p-value matrix is not an effect estimate.

**Proposed acceptance test.** Use an autocorrelated confounded VAR and an observationally equivalent orientation example; assess graph-class coverage and admissible effect sets separately from edge F1.

**Inspected support.**

- `docs/literature/raw/raw_readme_tigramite.md` lines 14--80, SHA-256 `b8c9760f1dd27932606a20338b65028982de9d8ddbb07328648cc00e859c3cd2`: Explicit method assumptions/output classes, CI-test assumptions and declared features. (primary_technical_text).

## causallearn: Static discovery reference

Repository: `py-why/causal-learn`. Observed package version: `0.1.4.8`. License observation: MIT.
Source snapshot: [causallearn.json](software/causallearn.json), SHA-256 `f0e2b9622674756c26f064e734a64d0c8fc6a002ab7e0c1b10a18c9531b68030`.

Selected API commit: `0dacacf36390e3084704636bc3c36e82e35ee0cc` (2026-09-04T16:50:44Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Sample-by-feature data, CI test, significance level, background knowledge and FCI search limits.

**Mathematical output.** FCI GeneralGraph flagged as PAG plus edge-property objects.

**Scientific restrictions.** Causal Markov/faithfulness and test assumptions; latent/selection semantics of FCI; finite samples do not turn uncertain endpoints into oriented arrows.

**Proposed adapter behavior.** Serialize tails, arrowheads, circles, bidirected and undirected edges without collapsing to Boolean adjacency. Retain depth/max_path_length and distinguish restricted search from a full oracle result.

**Proposed acceptance test.** Round-trip all FCI endpoint pairs; verify an o-> edge stays unresolved and a bidirected edge stays distinct from two directed edges. Apply effect identification over compatible graphs.

**Inspected support.**

- `docs/literature/raw/r3g_api_causallearn.txt` lines 1061--1181, SHA-256 `8f0f14f9d31847efa30fa056a162f1f9d21d07595880c1ad2b099ec11e544ead`: FCI input/output documentation, endpoint integer codes, search controls and graph.set_pag(True). (primary_technical_text).

## causalnex: Deferred candidate

Repository: `quantumblacklabs/causalnex`. Observed package version: `0.12.2`. License observation: Unverified in this audit.
Source snapshot: [causalnex.json](software/causalnex.json), SHA-256 `1def16a1af650b9394dd081040d461d5c54577890aca897a825c7177ade1d0cf`.

**Mathematical input.** No scientifically qualified interface in this source audit.

**Mathematical output.** No supported operation assigned.

**Scientific restrictions.** A readable primary technical artifact is required before judging capabilities or current maintenance.

**Proposed adapter behavior.** Defer dependency selection. Repository-access failures establish retrieval failure only; they do not prove abandonment or archive status.

**Proposed acceptance test.** Before evaluation, recover a licensed primary technical version, verify identity and inspect actual graph/estimation contracts.

**Inspected support.**

- `docs/literature/raw/repo_causalnex.receipt.json` lines 1--7, SHA-256 `7904bcc8f2dbe25f2ccaaa024aec1cc932571776c889b44006e50f8f50b12519`: Repository retrieval failure only; no technical support. (discovery_only).

## causica: Joint graph and mechanism research comparator

Repository: `microsoft/causica`. Observed package version: `not established`. License observation: MIT.
Source snapshot: [causica.json](software/causica.json), SHA-256 `7d41f817131a08479cf372b388da8e55d43f08fa0586ed0b32838c63aa8970a8`.

**Mathematical input.** Observational variables and an additive-noise structural model with a graph prior/variational family.

**Mathematical output.** A fitted graph distribution and neural mechanisms; intervention simulation yields model-conditional ATE/CATE.

**Scientific restrictions.** Structural ANM/noise/prior restrictions, sufficient causal information and adequate variational/optimization approximation.

**Proposed adapter behavior.** Record structural priors and graph uncertainty. The current README says Rhino and DDECI were removed and points to v0.0.0; do not advertise temporal or latent-ADMG implementations from their cited papers alone.

**Proposed acceptance test.** Use Gaussian observational equivalence and non-Gaussian identifiable cases; distinguish data information from prior-driven orientation. Verify the exact installed release exposes each proposed model.

**Inspected support.**

- `docs/literature/raw/readme_causica.md` lines 17--97, SHA-256 `5028ca8edf4efe0809b0ca98affaaa9cfc9739edcb2d4996bea680ab09d31524`: DECI model, simulation, known-graph option and removed extensions. (primary_technical_text).

## gcastle: Algorithm-family discovery comparator

Repository: `huawei-noah/trustworthyAI`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [gcastle.json](software/gcastle.json), SHA-256 `627c5f773aa602b740a50b77b758ed22b0e492324219ee664592c214bf1079c7`.

**Mathematical input.** Method-specific sample data or event sequences, prior constraints and selected algorithm.

**Mathematical output.** Learned structure and graph comparison metrics for that method.

**Scientific restrictions.** IID/function/score restrictions differ by algorithm; Hawkes/event-sequence models are separate from static ANMs.

**Proposed adapter behavior.** Pin the gcastle submodule and backend. Its README labels HPCI under development; a monorepo push does not qualify it. Preserve graph equivalence where required and separate metric computation from identification.

**Proposed acceptance test.** Compare static ANM and event-sequence inputs using valid/invalid model assignments; reject routing generic time series to an IID algorithm without a declared reduction.

**Inspected support.**

- `docs/literature/raw/readme_gcastle_module.md` lines 7--94, SHA-256 `6ca15cda8d1bf5f7729a457702f8dbc954e5f0a39aeb09269fff554ae0b8c596`: Version declaration, algorithm categories, HPCI status, dependencies and PC example. (primary_technical_text).

## dagma: Continuous DAG-optimization comparator

Repository: `kevinsbello/dagma`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [dagma.json](software/dagma.json), SHA-256 `63adfbba614c121497bd413663a6e449b9fb923a1d2a2d372c1523c0d5e73e0f`.

**Mathematical input.** Data and a linear/nonlinear structural loss with sparsity and acyclicity controls.

**Mathematical output.** A numerically optimized weighted DAG candidate.

**Scientific restrictions.** Causal sufficiency and functional/noise identifiability separately from the log-determinant acyclicity construction.

**Proposed adapter behavior.** Preserve optimization tolerance, threshold and seed; optimization feasibility and graph acyclicity are numerical statements, not evidence for causal orientation.

**Proposed acceptance test.** Check acyclicity before/after thresholding and compare equivalent Gaussian orientations; vary initialization and report target-effect sensitivity.

**Inspected support.**

- `docs/literature/raw/raw_readme_dagma.md` lines 1--117, SHA-256 `3594480ca8f3b95de7d732200e8239a05c84f2fb9df9cfea8d2a4bf8ccf5f3f3`: DAGMA log-determinant/M-matrix formulation and linear/nonlinear usage. (primary_technical_text).

## notears: Reference continuous acyclicity algorithm

Repository: `xunzheng/notears`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [notears.json](software/notears.json), SHA-256 `fd8a20fd674512d01802d903d4d680c4c54f0756f06b3293641a57a9530831ea`.

**Mathematical input.** Data, regression loss, sparsity and numerical convergence/threshold choices.

**Mathematical output.** Estimated adjacency under an acyclicity constraint.

**Scientific restrictions.** Graph interpretation needs structural/noise identifiability and valid observations beyond a differentiable DAG constraint.

**Proposed adapter behavior.** Expose solver failure and thresholding; preserve pre-threshold weights. Do not label every fitted acyclic graph uniquely identified.

**Proposed acceptance test.** Use a cyclic near-threshold candidate, equivalent linear-Gaussian DAGs and a nonlinear identifiable case; compare feasibility with intervention correctness.

**Inspected support.**

- `docs/literature/raw/raw_readme_notears.md` lines 1--110, SHA-256 `54b163ec3c3a5a5cefde4c2622871ae56cce57617a0ed6c5bfbeab982a848c67`: Continuous constrained structure-learning formulation and reference code usage. (primary_technical_text).

## tetrad: Independent-language discovery comparator candidate

Repository: `cmu-phil/tetrad`. Observed package version: `not established`. License observation: GPL-3.0.
Source snapshot: [tetrad.json](software/tetrad.json), SHA-256 `3edc8f833b5becfb197a4922ce4117d4c1d77ae26353dd4099c039d6c25f2b44`.

**Mathematical input.** A chosen discovery search and its test/score/data schema; exact search API still requires inspection.

**Mathematical output.** Search-specific graph through Java library/GUI or a separately pinned language bridge.

**Scientific restrictions.** Each search retains its own equivalence class, latent-variable and sampling restrictions.

**Proposed adapter behavior.** Do not count a Java repository snapshot as a qualified Python adapter. Pin tetrad-lib, bridge and JDK; README currently names JDK25+ and describes bridge installation as nonstandard.

**Proposed acceptance test.** For a selected FCI/PC route, compare oracle graph endpoints with the Python reference and require lossless cross-language graph serialization.

**Inspected support.**

- `docs/literature/raw/raw_readme_tetrad.md` lines 1--81, SHA-256 `77727077d53262773e66de728130ba7b3ebe61061f3d30b6bcc1f3817876aed6`: Java model/GUI separation, Python/R bridges and runtime requirements; no selected search implementation inspected. (primary_technical_text).

## causalimpact: Aggregate intervention time-series comparator

Repository: `google/CausalImpact`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [causalimpact.json](software/causalimpact.json), SHA-256 `8c8990ab9b09960c1c3ec96aa87be6af3d0b96d9436c3582259467e8153777a2`.

**Mathematical input.** A treated outcome series, a pre/post intervention split and unaffected control series.

**Mathematical output.** Posterior counterfactual series and intervention contrasts conditional on the structural time-series model.

**Scientific restrictions.** Controls are unaffected by treatment; the pre-period outcome/control relation extends to the untreated post-period and competing shocks are accounted for.

**Proposed adapter behavior.** Register donor/control exposure and the intervention date. Do not interpret posterior predictive fit or interval width as a test of no spillovers or stable counterfactual extrapolation.

**Proposed acceptance test.** Simulate a known campaign shock, then contaminate controls and introduce a post-period coefficient break; check model-conditional effects and failure diagnostics.

**Inspected support.**

- `docs/literature/raw/readme_causalimpact.md` lines 8--30, SHA-256 `72a797f60f6ccd3b482610e127d745d24c4204261b9c79029d81c366c596477f`: Structural time-series target, unaffected-control and stable-relationship assumptions. (primary_technical_text).

## causalpy: Bayesian quasi-experimental challenger

Repository: `pymc-labs/CausalPy`. Observed package version: `0.9.0`. License observation: Apache-2.0.
Source snapshot: [causalpy.json](software/causalpy.json), SHA-256 `b5ad310eaaa3fd4d5be3b1b9322578775855b040eab4c29b082a834e4140bca1`.

**Mathematical input.** A named quasi-experimental design, formula, timing/threshold variables and chosen Bayesian or OLS model.

**Mathematical output.** Design-specific contrast and posterior/OLS summaries; e.g. a local discontinuity at a supplied threshold.

**Scientific restrictions.** Design-specific continuity, parallel-trend, donor or IV restrictions; prior and likelihood assumptions for Bayesian summaries.

**Proposed adapter behavior.** Treat RD, DiD, synthetic control and IV as separate operations. Pin sampler/runtime configuration; the inspected README warns optional nutpie changes sampling defaults. Do not infer unconditional frequentist coverage from an HDI.

**Proposed acceptance test.** For a specified RD, recover the population jump under continuity and expose manipulation/discontinuity confounding; replay with an explicit sampler selection and check numerical diagnostics.

**Inspected support.**

- `docs/literature/raw/readme_causalpy.md` lines 23--117, SHA-256 `3e150af37b3f84338767d1887aa342a7a6f25d6840e04901d5fcd30190ac3c32`: Quasi-experimental methods, Bayesian/OLS outputs, runtime notes and RD example. (primary_technical_text).

## linearmodels: Econometric baseline

Repository: `bashtage/linearmodels`. Observed package version: `7.0`. License observation: NCSA.
Source snapshot: [linearmodels.json](software/linearmodels.json), SHA-256 `3f59083b5729412c826af5468e7177a1253d3d08bd68dc3bb253cb43ae3a9255`.

**Mathematical input.** Panel or IV/system regression data with explicit formula, effects, instruments and covariance choice.

**Mathematical output.** Linear model coefficients, residuals and model-specific covariance/diagnostics.

**Scientific restrictions.** Strict exogeneity or stated IV moments; rank and dependence assumptions appropriate to each estimator.

**Proposed adapter behavior.** Keep fixed effects, instrument sets and covariance axes explicit. The panel label does not establish dynamic-panel GMM support or a modern staggered-adoption ATT.

**Proposed acceptance test.** Compare within and IV estimates to direct projections on a small full-rank design, then use a lagged-outcome short panel to expose invalid strict-exogeneity routing.

**Inspected support.**

- `docs/literature/raw/raw_readme_linearmodels.md` lines 1--140, SHA-256 `dee8dba087aa4ff0484a42ad9f28fed652d5c59f66380ee7a0ec5fedc08f3394`: PanelOLS, first differences, IV2SLS/LIML/GMM and systems feature/usage descriptions. (primary_technical_text).

## pyfixest: Python high-dimensional fixed-effect and panel candidate

Repository: `py-econometrics/pyfixest`. Observed package version: `0.60.0`. License observation: MIT.
Source snapshot: [pyfixest.json](software/pyfixest.json), SHA-256 `f6e14a56199d9cbb6afffce3deddc28a7f8d346cb0d7502500ef88b48886fd8e`.

**Mathematical input.** Formula-based outcomes, treatments, high-dimensional effects, weights, instruments and selected DiD/inference method.

**Mathematical output.** Selected regression or event-study effect and declared covariance.

**Scientific restrictions.** The chosen regression/DiD estimand is identified; weights and dependence model match the target.

**Proposed adapter behavior.** Do not convert a staggered-treatment request automatically into TWFE. Pin CPU/GPU backend and demeaning tolerances; declared speed/features are not this project's measured performance.

**Proposed acceptance test.** Recover a projection with explicit dummy variables; use heterogeneous cohort effects to distinguish TWFE from cohort ATT; compare weighted residualization and cluster covariance.

**Inspected support.**

- `docs/literature/raw/raw_readme_pyfixest.md` lines 1--145, SHA-256 `9d2cabe0c05e0e9534be97e55881609f40b091e7b77cc4992d7075e168bbe6c6`: FE/IV/GLM and DiD features, inference choices and backend declarations. (primary_technical_text).

## fixest: R fixed-effect/IV reference

Repository: `lrberge/fixest`. Observed package version: `0.14.2`. License observation: GPL-3.
Source snapshot: [fixest.json](software/fixest.json), SHA-256 `628096740cbcd4668d1965df73a9c3a48db6a504678b47d674c76dc1011ea8dc`.

**Mathematical input.** Formula, multiple effects, optional instruments, weights and covariance specification.

**Mathematical output.** Linear/GLM or IV coefficients with selected inference.

**Scientific restrictions.** Scientific regression/IV restrictions and weighting target are established outside formula parsing.

**Proposed adapter behavior.** Retain formula expansion, absorbed effects, observations dropped and inference defaults. Benchmark claims cannot be transferred across hardware or a different estimand.

**Proposed acceptance test.** Check explicit-dummy equivalence, treatment collinearity, singleton handling and same-target agreement with a Python reference.

**Inspected support.**

- `docs/literature/raw/raw_readme_fixest.md` lines 1--135, SHA-256 `d2b746c8f729fa0cb486318f8bf6c7651bacd515c7628c4062f1e878342edc22`: Multiway FE/IV/GLM features, inference and performance comparison caveats. (primary_technical_text).

## did: Group-time ATT reference

Repository: `bcallaway11/did`. Observed package version: `2.5.1.902`. License observation: GPL-3.
Source snapshot: [did.json](software/did.json), SHA-256 `7dbf80e7df492619310c0cb77e94231f18a6ae6a756b38a69c2cbc38eb8bc9df`.

Selected API commit: `74b88eb07f1faa644df1271055a0f77848f6550c` (2026-08-28T22:35:39Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Unit/time identifiers, outcome, first-adoption cohort, comparison group, covariates and weighting/sampling design.

**Mathematical output.** ATT(g,t), influence functions and selected pointwise/uniform inference; aggregation requires appropriate retained influence information.

**Scientific restrictions.** No anticipation, conditional group-specific parallel trends, comparison support and correct panel/repeated-cross-section interpretation.

**Proposed adapter behavior.** Pinned att_gt allows at most one additional coarser cluster beyond individual ID. Uniform bands require bootstrap. compute_inffunc=False disables inference/pretests/bands and prevents aggte. Inspect fixed-weight anchor rules before using unbalanced panels.

**Proposed acceptance test.** Reproduce known cohort effects and weighted aggregations; reject incompatible changing-treatment encodings and unsupported cluster layouts. Explicitly test the points-only path cannot be promoted to an interval.

**Inspected support.**

- `docs/literature/raw/r3g_api_did.txt` lines 1--145, SHA-256 `c36ea7217bfbd88ed5e316ca2a785aec39525dd1b7d9d62807b9a26cc73416f9`: att_gt design, weights, clustering, inference and aggregation controls. (primary_technical_text).

## honestdid: Parallel-trend sensitivity and confidence-set adapter

Repository: `asheshrambachan/HonestDiD`. Observed package version: `0.2.8`. License observation: MIT.
Source snapshot: [honestdid.json](software/honestdid.json), SHA-256 `2044e6f8723e2470eb114784f247295158d93f194f839a209a924eb1412f7a96`.

**Mathematical input.** Event-study contrast vector, its full covariance, pre/post ordering, contrast weights and a specified trend-violation class.

**Mathematical output.** Restriction-dependent identified/confidence sets and a sensitivity curve.

**Scientific restrictions.** The chosen restriction on post-treatment violations and the asymptotic approximation for input estimates hold.

**Proposed adapter behavior.** Keep relative-magnitude and smoothness restrictions distinct, including time units and baseline normalization. Do not treat the worst observed pretrend as a known population bound.

**Proposed acceptance test.** Use a finite trend polytope with independently solved extrema, and known-covariance simulations for coverage; vary preperiod precision while holding the restriction fixed.

**Inspected support.**

- `docs/literature/raw/raw_readme_honestdid.md` lines 1--90, SHA-256 `e4e6e8f1129d9d5967d7fa442f0bd65f1883bf2bfc5d934162056907f2cb179c`: Relative-magnitude/smoothness restrictions and inference accounting for pretrend estimation uncertainty. (primary_technical_text).

## synthdid: Block-adoption synthetic-DiD comparator

Repository: `synth-inference/synthdid`. Observed package version: `not established`. License observation: BSD-3-Clause.
Source snapshot: [synthdid.json](software/synthdid.json), SHA-256 `074b3a0b10917fbde1f15ab4bc965ca30d44fdf934ff6d82e64b0bbaed6b76c3`.

**Mathematical input.** An outcome panel with controls/treated rows and untreated/treated time blocks under simultaneous adoption.

**Mathematical output.** Synthetic-DiD treatment contrast with method-specific uncertainty.

**Scientific restrictions.** Block treatment layout, suitable donor/preperiod support and the method's outcome-model/design restrictions.

**Proposed adapter behavior.** Reject staggered adoption as direct input to the documented block interface. Pin beta API and define aggregation before preprocessing.

**Proposed acceptance test.** Reproduce a rank-one factor panel with a known common treatment effect; reject mixed adoption dates and inspect donor-weight concentration.

**Inspected support.**

- `docs/literature/raw/raw_readme_synthdid.md` lines 1--49, SHA-256 `a8063fbd00a42fb29952608cb9bad0a12f41c8405f464513b9744b189fb49b20`: Simultaneous/block adoption, estimator/variance usage and beta status. (primary_technical_text).

## gsynth: Interactive-factor counterfactual comparator; implementation deferred

Repository: `xuyiqing/gsynth`. Observed package version: `1.4.0`. License observation: MIT.
Source snapshot: [gsynth.json](software/gsynth.json), SHA-256 `f0d2c5f5f4a692d0047e6d86cbe23daa309ef912feaf11d021542d2f5e473f78`.

**Mathematical input.** Treated/control panel and an interactive-fixed-effect counterfactual model.

**Mathematical output.** Imputed untreated outcomes and their treatment contrasts.

**Scientific restrictions.** Stable low-rank factor structure, sufficient untreated overlap, no relevant spillovers and justified extrapolation.

**Proposed adapter behavior.** README states gsynth is now a fect wrapper maintained for backward compatibility. Qualify and pin fect separately before implementation. README 1.3.1 and DESCRIPTION 1.4.0 are distinct declarations, not interchangeable release evidence.

**Proposed acceptance test.** Use known low-rank factor panels and a treated-unit factor break; verify cross-validation excludes post-treatment leakage. Repeat against the actual pinned fect dependency.

**Inspected support.**

- `docs/literature/raw/raw_readme_gsynth.md` lines 13--76, SHA-256 `1e12ed36b97a4235a2bffe0021187bc1b7d1974154633b97b51f3a23b4c71d4e`: Interactive FE purpose, README version and fect/backward-compatibility notice. (primary_technical_text).

## d3rlpy: Policy-learning challenger

Repository: `takuseno/d3rlpy`. Observed package version: `2.8.1`. License observation: MIT.
Source snapshot: [d3rlpy.json](software/d3rlpy.json), SHA-256 `d85486b849fa2c8cb2e595e8903a8962b755850bf36a676f68dae2d9fa14038f`.

**Mathematical input.** Episode-indexed state/action/reward/terminal data and a selected offline-RL model.

**Mathematical output.** Learned policy and value approximations under the learning objective.

**Scientific restrictions.** Sufficient state/history, invariant reward/transition semantics, adequate behavior support and valid independent evaluation.

**Proposed adapter behavior.** Separate policy fitting from causal identification and OPE; retain terminal/truncation distinction. Pin v2 API and training configuration. Distributed training does not establish policy-value coverage.

**Proposed acceptance test.** Train on a small known MDP, evaluate on independent trajectories, then remove an action from logging support; report unsupported policy choices instead of certifying them from Q-values.

**Inspected support.**

- `docs/literature/raw/readme_d3rlpy.md` lines 14--132, SHA-256 `3b44807ebbb0f716d44b9f44f6b39cfbe1311a10c719c6cdcaa72df5fea63b0f`: Offline/online APIs, v2 breaking changes, declared distributed training and supported algorithm table. (primary_technical_text).

## scope_rl: Off-policy value/distribution comparator

Repository: `hakuhodo-technologies/scope-rl`. Observed package version: `0.2.1`. License observation: Apache-2.0.
Source snapshot: [scope_rl.json](software/scope_rl.json), SHA-256 `f2905347c580b5b9f6d419f763ea06ea280d092af60dfe9d8efcd618e4a23a9c`.

**Mathematical input.** Logged trajectories, behavior/target probabilities, horizon/discount and optional Q/occupancy nuisance estimates.

**Mathematical output.** Estimator-specific expected return, return distribution or policy-selection criterion with selected uncertainty routine.

**Scientific restrictions.** Exchangeability/sufficient information, support, nuisance and sampling conditions for the chosen trajectory or marginal estimator.

**Proposed adapter behavior.** Retain trajectory versus occupancy ratios and return-distribution versus mean targets. Interval-method availability does not establish coverage under hidden logging or arbitrary dependence.

**Proposed acceptance test.** Compare trajectory enumeration, IS and DR on a finite MDP; introduce a private logger and rare informative paths; assess bias and interval coverage by regime.

**Inspected support.**

- `docs/literature/raw/raw_readme_scope_rl.md` lines 42--150, SHA-256 `16bc3bcb41e9a0129afd3c33e873cb0206c78465cc270539a52e229d9bbb1849`: Offline-RL workflow, trajectory/marginal/DR estimators, confidence routines and selection criteria. (primary_technical_text).

## obp: One-step bandit evaluation reference

Repository: `st-tech/zr-obp`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [obp.json](software/obp.json), SHA-256 `7aeec96400084847e54e715025e8707b6d07b982620bf1018160ee0643695b78`.

**Mathematical input.** Context, logged action/reward, logging probability and target action distribution, including declared slate/position semantics.

**Mathematical output.** One-step policy value or contextual-bandit policy.

**Scientific restrictions.** Bandit exchangeability/support and correct logging probabilities; slate models need their own reward/propensity factorization.

**Proposed adapter behavior.** Do not route multi-period banking carryover to a contextual-bandit value. Preserve action/position conventions and evaluate learned policies on independent or appropriately split data.

**Proposed acceptance test.** Recover a one-step finite contextual value, then build a two-step carryover example showing that one-step reward can reverse the preferred policy.

**Inspected support.**

- `docs/literature/raw/raw_readme_obp.md` lines 67--155, SHA-256 `42047d3b5f697e440751dc7a13e83ccbb152737be6153042ec5dfeddd8cdaedd`: Bandit modules and supported standard/slate/continuous-action OPE families. (primary_technical_text).

## pomdp_py: Small POMDP planning comparator

Repository: `h2r/pomdp-py`. Observed package version: `1.3.5.1`. License observation: MIT.
Source snapshot: [pomdp_py.json](software/pomdp_py.json), SHA-256 `87bae331ad4be07cdda7ff7f0c2089c841f36bef813a28262b0dd682874c6c6d`.

**Mathematical input.** Explicit transition/observation/reward model, initial belief and planner configuration.

**Mathematical output.** Model-conditional belief updates, simulated decisions and policy/planner outputs.

**Scientific restrictions.** The supplied controlled model is valid for the intervention and the agent's available history; planner approximation is a separate numerical issue.

**Proposed adapter behavior.** The inspected README qualifies a Python/Cython modeling/planning framework, not a causal parameter estimator. Inspect concrete planner and belief APIs before implementation; never pass smoothed future information as an online belief.

**Proposed acceptance test.** Compare a finite two-state belief update and short-horizon action values to exhaustive enumeration, then verify private logging changes observational filtering but not the intervention kernel.

**Inspected support.**

- `docs/literature/raw/readme_pomdp_py_rst.txt` lines 1--22, SHA-256 `5be368e8630b9b5d4d73b65b9dafcf802b40d613c55ac8d638da5b8f8a2955b2`: Framework to build and solve POMDPs; source-level role only. (primary_technical_text).

## pomdps: Julia POMDP interface and solver comparator

Repository: `JuliaPOMDP/POMDPs.jl`. Observed package version: `not established`. License observation: MIT.
Source snapshot: [pomdps.json](software/pomdps.json), SHA-256 `7f70bea707dc8197930434b14208ac78a89791055d1965d13ddddbec33f93feb`.

**Mathematical input.** State/action/observation spaces, initial law, transition, observation, reward and discount through the model interface.

**Mathematical output.** Solver-specific policy and model-conditional simulated/belief trajectories.

**Scientific restrictions.** Controlled causal model and information filtration are already justified; solver approximations/guarantees depend on the separately chosen package.

**Proposed adapter behavior.** Pin POMDPs.jl, POMDPTools, the solver and language bridge independently. The core interface does not itself implement all listed solvers. Keep pre/post-transition observation conventions explicit.

**Proposed acceptance test.** Use the same finite model across the project oracle and a pinned Julia solver; check observation indexing, discount timing and belief measurability.

**Inspected support.**

- `docs/literature/raw/raw_readme_pomdps.md` lines 10--125, SHA-256 `2bcf336150a2c71edf04927871465061a535dfaf9c9c61348aac5bb188f266b2`: Core interface, separate tools/solvers, Tiger transition-observation-reward example. (primary_technical_text).

## pymc: Bayesian generative-model inference candidate

Repository: `pymc-devs/pymc`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [pymc.json](software/pymc.json), SHA-256 `aa4c49295aef51cd1242facead05fdf0a25fcd2bf98ff9a5791aa89d24125bb6`.

**Mathematical input.** A specified likelihood/prior and observed/missing variables.

**Mathematical output.** Posterior draws or variational approximation and predictive quantities conditional on the model.

**Scientific restrictions.** A properly defined probabilistic target, computational convergence/approximation and separately justified causal semantics.

**Proposed adapter behavior.** Record likelihood factors and intervention transformation. pm.do/pm.observe syntax changes a supplied model; it does not establish that a bank's causal graph or latent mechanisms are identified.

**Proposed acceptance test.** Compare a conjugate posterior and a marginalized finite latent model to exact values; introduce observationally equivalent causal completions and verify prior sensitivity remains visible.

**Inspected support.**

- `docs/literature/raw/raw_readme_pymc.txt` lines 8--111, SHA-256 `6acf764dca0cff1c354c87086d5d8d3ca6b29ff03c77b789dcf52b6bdced6138`: MCMC/VI features and explicit do/observe example. (primary_technical_text).

## numpyro: JAX probabilistic inference candidate

Repository: `pyro-ppl/numpyro`. Observed package version: `0.22.0`. License observation: Apache-2.0.
Source snapshot: [numpyro.json](software/numpyro.json), SHA-256 `c71034811355c84c5c87bee011487a31f46813e2229961f926a7e54b53409498`.

**Mathematical input.** A probabilistic program, observations, PRNG keys and inference configuration.

**Mathematical output.** MCMC/VI approximation to a specified posterior and diagnostics.

**Scientific restrictions.** Target density and numerical conditions match the selected algorithm; latent marginalization or a valid mixed/discrete method is required where appropriate.

**Proposed adapter behavior.** Do not claim all discrete states must be marginalized: the README documents MixedHMC and discrete VI as alternatives. Pin algorithm, precision, compiler, device and randomness. Fast differentiation does not identify interventions.

**Proposed acceptance test.** Compare exact finite-state marginalization and a conjugate continuous posterior; verify reproducible PRNG splitting and diagnose a difficult posterior rather than accepting speed alone.

**Inspected support.**

- `docs/literature/raw/raw_readme_numpyro.md` lines 24--117, SHA-256 `7b276dfddc4ef9d2daf72fdbc2731b39a1276b66569431fba59527f3a957a9bc`: JAX substrate, HMC/NUTS, MixedHMC/discrete VI and divergence/reparameterization diagnostics. (primary_technical_text).

## dynamax: Conditional state-space likelihood comparator

Repository: `probml/dynamax`. Observed package version: `1.0.2`. License observation: MIT.
Source snapshot: [dynamax.json](software/dynamax.json), SHA-256 `8336ff75d1ace4aaf738562a849049d7c40bb2cf84cbc72c3a539dad0aa89fc6`.

Selected API commit: `5098927f2c377c0dd548cda750e6f1436220aac6` (2026-09-29T18:17:46Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Discrete-time emission sequences, optional external inputs and initial/transition/emission parameter components.

**Mathematical output.** Conditional emission log likelihood, filtering/smoothing distributions and parameter-fitting ingredients.

**Scientific restrictions.** The specified conditional-input SSM matches the observational experiment; treating adaptive actions as inputs requires a valid logger/conditioning argument.

**Proposed adapter behavior.** HMM marginal_log_prob builds initial, transition and emission factors only. A private action likelihood is not supplied automatically. Standard transition components may ignore inputs; qualify the actual subclass and index mapping. Keep filtering separate from smoothing.

**Proposed acceptance test.** Compare finite latent-path summation to filter likelihood; include an informative private logger and demonstrate failure of a transition/emission-only likelihood. Verify input and observation timing explicitly.

**Inspected support.**

- `docs/literature/raw/r3g_api_dynamax.txt` lines 524--659, SHA-256 `126b65cf1865ca91e9107bf329950142f6576f18fbb5487256bd501a7868e776`: HMM law, optional input components, marginal_log_prob, filter, smoother and E-step. (primary_technical_text).

## duckdb: Local relational execution reference

Repository: `duckdb/duckdb`. Observed package version: `1.5.6`. License observation: MIT.
Source snapshot: [duckdb.json](software/duckdb.json), SHA-256 `d3b2b5305346ea6d1fc64026f65484efa891efcade88ebb9b8b3f896f42723a6`.

**Mathematical input.** Versioned tables/files, explicit SQL and query configuration.

**Mathematical output.** Materialized histories/features or score sufficient-statistic reductions.

**Scientific restrictions.** Keys, joins, event/availability semantics and aggregation preserve the declared population and information set.

**Proposed adapter behavior.** Use SQL windows/nested types where useful but separately enforce time and cardinality contracts. No bank-scale throughput inferred from the README.

**Proposed acceptance test.** Backfill and duplicate-key adversaries; compare a materialized temporal join with exhaustive small-table enumeration and record peak memory/spill for the actual workload.

**Inspected support.**

- `docs/literature/raw/raw_readme_duckdb.md` lines 17--42, SHA-256 `907b44f4727089c4475a5f9342e76ed2cdb39cac5619feb4ed9c5c065f5cc559`: SQL windows/nested types, clients and CSV/Parquet input. (primary_technical_text).

## polars: Optional columnar/streaming execution adapter

Repository: `pola-rs/polars`. Observed package version: `not established`. License observation: MIT.
Source snapshot: [polars.json](software/polars.json), SHA-256 `6be95d7c55919476442d32cfc597081b69cba28f4be2a134f02810e755c17c6c`.

**Mathematical input.** Versioned frames/files and a lazy/eager expression plan with selected engine.

**Mathematical output.** Transformed data/aggregates under query semantics.

**Scientific restrictions.** Reordering, null handling, casts and time-zone/ordering semantics preserve the intended history and numerical result.

**Proposed adapter behavior.** Retain the engine and physical plan; larger-than-memory and GPU declarations are capabilities to qualify, not causal-estimation speed evidence. Distributed cloud is not assumed to be the OSS execution path.

**Proposed acceptance test.** Require batch/streaming equivalence for ordered histories and cluster score sums within a declared tolerance; profile peak memory and unsupported-operation fallback.

**Inspected support.**

- `docs/literature/raw/raw_readme_polars.md` lines 44--98, SHA-256 `34ae7397cdce21d11b86261faa8c792b4ab502afaff817f1af26a6c22baa1f9f`: Lazy/eager engine, streaming, GPU and Arrow-interoperability declarations. (primary_technical_text).

## ray: Optional distributed execution substrate

Repository: `ray-project/ray`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [ray.json](software/ray.json), SHA-256 `2f03d3abce5a0f4b9537890f50ab403d41760b5349ec64c46cdff63685dad0e5`.

**Mathematical input.** An immutable partitioned dataset, task graph, model artifacts and deterministic fold/seed map.

**Mathematical output.** Distributed task results, fitted nuisance objects and reductions.

**Scientific restrictions.** Statistical split boundaries and aggregation are invariant to scheduling, retries and worker count.

**Proposed adapter behavior.** Adopt only after profiling. Tasks/actors/objects do not determine independent sampling units; retain explicit cluster/time partitioning and avoid duplicated score contributions on retry.

**Proposed acceptance test.** Kill/retry a worker during a bounded benchmark, change partition count, and require exactly-once logical contributions and equal fold membership; compare covariance with the local reference.

**Inspected support.**

- `docs/literature/raw/raw_readme_ray.txt` lines 18--49, SHA-256 `94df2acbdfdc95f867ce205d63da33480db909359e6235d9bb3c912fb6a11e87`: Distributed runtime, AI libraries and task/actor/object abstractions. (primary_technical_text).

## datahub: Metadata and lineage integration option

Repository: `datahub-project/datahub`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [datahub.json](software/datahub.json), SHA-256 `dab11e4eb81e9fa8a3243bdac664065b48f4b9058045b6468766af0f2a69a924`.

**Mathematical input.** Catalog assets, ownership, schemas and lineage from bank systems.

**Mathematical output.** Searchable metadata graph and context for candidate data mappings.

**Scientific restrictions.** Metadata completeness and semantic correctness are separate from causal assumptions and actual feature availability.

**Proposed adapter behavior.** Use the existing enterprise catalog where possible. The README mixes OSS and Cloud capabilities: only its explicit OSS metadata-graph/lineage/governance/discovery declaration is relied on here. Human context proposals need evidence-backed field semantics.

**Proposed acceptance test.** Import a bounded synthetic asset graph, preserve stable IDs and source-version links, and ensure lineage edges cannot be promoted automatically to causal arrows.

**Inspected support.**

- `docs/literature/raw/raw_readme_datahub.md` lines 43--58, SHA-256 `9711dc90543bb6a6703e37e246244e4eb689ff68234d9bdfc081edef544fdd7a`: Explicit DataHub OSS versus Cloud capability distinction. (primary_technical_text).

## openmetadata: Alternative enterprise metadata integration

Repository: `open-metadata/OpenMetadata`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [openmetadata.json](software/openmetadata.json), SHA-256 `ec5045e01a87a210525013f6c2c6064e3d3d5ff92f77705cc595ef3041a03f19`.

**Mathematical input.** Technical/business metadata, quality, ownership and lineage with stable asset identifiers.

**Mathematical output.** A unified metadata graph and schema-based context.

**Scientific restrictions.** Catalog declarations may be incomplete or stale; technical lineage and business associations do not establish causal direction.

**Proposed adapter behavior.** Integrate the bank's chosen catalog instead of requiring a second one. Qualify selected OSS connectors/API behavior before implementation; broad README capability lists are not an end-to-end test.

**Proposed acceptance test.** Reconcile a schema/ownership change and trace affected analysis inputs; retain unresolved definitions and verify no inferred adjustment set follows solely from catalog links.

**Inspected support.**

- `docs/literature/raw/raw_readme_openmetadata.md` lines 9--11, SHA-256 `8c959198c89ffe2fac596c329619bc82b2b848ea1f18db8fb9ae90f9248349a2`: Metadata/quality/lineage/ownership/glossary/contracts graph declaration. (primary_technical_text).
- `docs/literature/raw/raw_readme_openmetadata.md` lines 85--111, SHA-256 `8c959198c89ffe2fac596c329619bc82b2b848ea1f18db8fb9ae90f9248349a2`: Schema-first collection/normalization architecture. (primary_technical_text).

## openlineage: Runtime provenance interchange

Repository: `OpenLineage/OpenLineage`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [openlineage.json](software/openlineage.json), SHA-256 `4f6db5e0ded069a5519875e137f0e087ff9d3b93ac36f5bea3307b4baf0ca2f7`.

**Mathematical input.** Job/run/dataset identifiers and versioned event/facet payloads.

**Mathematical output.** Lineage events and an extensible provenance graph.

**Scientific restrictions.** Emitted events are complete enough for replay and correspond to actual immutable data/model versions.

**Proposed adapter behavior.** Define separate causal-analysis facets for target, observation clock, graph/model, split plan and estimator. A successful job event does not certify identification or inference.

**Proposed acceptance test.** Replay reordered/duplicate events, correlate one analysis to exact dataset/model artifacts, and require unknown facet versions to remain visible.

**Inspected support.**

- `docs/literature/raw/raw_readme_openlineage.md` lines 12--51, SHA-256 `8e0a2f3645ac69e3158b73f90267066eaa9f13d6fad2d01afa66bdc07bea1537`: Run/job/dataset model, runtime events and custom facets. (primary_technical_text).

## feast: Historical feature retrieval integration

Repository: `feast-dev/feast`. Observed package version: `not established`. License observation: Apache-2.0.
Source snapshot: [feast.json](software/feast.json), SHA-256 `24ef93109c068b1815aafb5d90aa77a5ef9ae541e2e5b52eec6e7cb1d83351ee`.

**Mathematical input.** Entity/event rows, feature references, TTL and optional created-timestamp filtering.

**Mathematical output.** A historical retrieval job whose features depend on timestamp configuration.

**Scientific restrictions.** Configured event/creation timestamps represent the bank's actual decision information and source revision history.

**Proposed adapter behavior.** The inspected API defaults filter_by_created_timestamp=False. Enabling it excludes later-created values only for views with created_timestamp_column. Require that field where availability matters and verify its business meaning; do not claim all Feast retrieval ignores availability time.

**Proposed acceptance test.** Use a feature dated before a decision but created after it. Check both flag settings, a missing creation field, TTL boundaries and revision tie-breaking against the declared history.

**Inspected support.**

- `docs/literature/raw/api_feast.txt` lines 1988--2065, SHA-256 `77b7681a0608a7cbbb98d85cf6b4a388e491c198f47179abebe8a7a47fbaedb5`: Historical retrieval, event/TTL semantics, opt-in creation-time filter and unaffected views lacking the field. (primary_technical_text).

## splink: Entity-linkage candidate

Repository: `moj-analytical-services/splink`. Observed package version: `5.0.0`. License observation: MIT.
Source snapshot: [splink.json](software/splink.json), SHA-256 `c7506768d42969c7450b503c1a5c2cc88d6079bd0b1531044e805c2671229a21`.

**Mathematical input.** Record comparisons, blocking rules and a probabilistic linkage model.

**Mathematical output.** Pairwise match probabilities and thresholded/clustered candidate entity IDs.

**Scientific restrictions.** Comparison-model calibration, blocking recall and dependence among fields; linkage uncertainty may depend on treatment/outcome.

**Proposed adapter behavior.** Preserve match uncertainty and the linkage-data clock. A hard connected component is an estimated entity, not ground truth; avoid post-treatment features when defining baseline identities without justification.

**Proposed acceptance test.** Inject treatment-dependent false merges/splits and quantify their effect on the causal contrast; compare integration over candidate links with a hard-threshold analysis.

**Inspected support.**

- `docs/literature/raw/raw_readme_splink.md` lines 14--57, SHA-256 `0d8bfe2b7e6c63ee7048762f3b7206dd5a6a5b8502b75e4a6bec33816b360386`: Probabilistic linkage, Fellegi-Sunter basis, pair probabilities, clustering and highly correlated field limitation. (primary_technical_text).

## pandera: Data/schema validation substrate

Repository: `unionai-oss/pandera`. Observed package version: `0.34.1`. License observation: MIT.
Source snapshot: [pandera.json](software/pandera.json), SHA-256 `38c98a50713e2c52d994396914a5b7cac07340657ab187522c1ececcd898183a`.

**Mathematical input.** Dataframe/schema and explicit type/value/cross-field checks.

**Mathematical output.** Validation result or schema failure.

**Scientific restrictions.** The user-specified checks actually express the intended data contract; passing checks is not causal identification.

**Proposed adapter behavior.** Use engine-specific schemas and preserve coercion/validation choices. Add product checks for unit keys, chronology and information availability; keep substantive assumptions distinct from executable checks.

**Proposed acceptance test.** Reject duplicated episode keys, wrong currency units and outcomes timestamped as baseline; include a valid-looking but confounded dataset to demonstrate the limit of schema validation.

**Inspected support.**

- `docs/literature/raw/raw_readme_pandera.md` lines 33--147, SHA-256 `cbe2f43b6dba825ebf0bfee73e12d48f490b103da9c346c005d90e1010c53847`: Multiple dataframe engines, schema/model APIs, custom checks and pandas import migration. (primary_technical_text).

## lmtp: Modified/stochastic longitudinal policy estimator reference

Repository: `nt-williams/lmtp`. Observed package version: `1.5.4`. License observation: AGPL-3.0.
Source snapshot: [lmtp.json](software/lmtp.json), SHA-256 `0c37917cab7ae782a7a581402a5d444804420e3bdebb590eb9f896c59ec2c1a0`.

Selected API commit: `f04a2b47f46debc515ce4ae778e05ebfde922c44` (2026-05-06T17:02:45Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Wide ordered treatment/covariate/outcome histories, a shift rule or shifted data, censoring/competing events, folds, sampling weights and optional cluster ID.

**Mathematical output.** TMLE/SDR policy mean, noncumulative density-ratio estimates and sequential regression fits.

**Scientific restrictions.** Consistency, appropriate sequential exchangeability, support for the shifted law and adequate nuisance rates; finite memory k requires its own history-sufficiency argument.

**Proposed adapter behavior.** Reject missing treatment under the documented capability matrix. Distinguish risk-ratio ipsi from odds tilting: at e=P(A=1|H), ipsi(delta) gives delta*e for delta<=1 and 1-(1-e)/delta for delta>1. Preserve mtp, shifted-overrides-shift and exact event/censoring interpretation.

**Proposed acceptance test.** For e=.2, delta=.5 gives .1 and delta=2 gives .6, versus odds-tilt values 1/9 and 1/3. Compare the declared policy mean to finite trajectory integration, including competing events and sampling weights.

**Inspected support.**

- `docs/literature/raw/raw_readme_lmtp.md` lines 28--105, SHA-256 `4bb1eb51dc496e02bc25e8be73e55ad81c24863b3f68378e8623ba39356aedef`: TMLE/SDR, risk-ratio incremental policies, missing-treatment limitation and competing risks. (primary_technical_text).
- `docs/literature/raw/r3g_api_lmtp_estimators.txt` lines 1--144, SHA-256 `a6dd3ddbc8948f66669483d3f4b4d71c302466ba32270f24995b67302b1dd9d6`: Chronological inputs, MTP flag, finite history, clusters, weights, folds and returned ratios/fits. (primary_technical_text).
- `docs/literature/raw/r3g_api_lmtp_shift.txt` lines 113--148, SHA-256 `b34776357cacfcdbf3b796fadb73eeaec6845d71baead622e31940109cdeb38f`: ipsi factory and stochastic up/down transformations. (primary_technical_text).

## ltmle: Fixed/dynamic binary-regime longitudinal TMLE reference

Repository: `joshuaschwab/ltmle`. Observed package version: `1.3-0`. License observation: GPL-2.
Source snapshot: [ltmle.json](software/ltmle.json), SHA-256 `d3451f98a64c78baf20d3d04a73472308eb67f2aed33c41a2d2aa3fc0100239f`.

Selected API commit: `338c029dae9692ef20714125773da7037688993b` (2023-04-17T22:09:22Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Wide data whose column order is causal time, binary treatment and censoring/event nodes, regime/rule and nuisance specifications.

**Mathematical output.** Regime mean or MSM projection, TMLE/IPTW (or G-computation), influence values and bounded/unbounded cumulative probabilities.

**Scientific restrictions.** Sequential identification and censoring restrictions, regime support and estimator-specific regularity.

**Proposed adapter behavior.** Validate chronology independently of column positions before constructing the input. Binary Anodes only; absorbing event coding must be coherent. Record Yrange truncation, gbounds on cumulative probabilities, sampling weights and id. Robust variance variants exclude several outcome/options combinations.

**Proposed acceptance test.** Use finite-law g-formula/DR identities and a column permutation that would reverse chronology; require rejection before fitting. Show how outcome clipping and cumulative probability bounding change bias/target behavior.

**Inspected support.**

- `docs/literature/raw/r3g_api_ltmle.txt` lines 1--106, SHA-256 `624e936e1405f87c30f06440856d86819661ac62928cbdfefd07ea8af62e633a`: Column-order chronology, binary actions, absorbing survival events, outcome scaling/truncation and dynamic rules. (primary_technical_text).
- `docs/literature/raw/r3g_api_ltmle.txt` lines 162--254, SHA-256 `624e936e1405f87c30f06440856d86819661ac62928cbdfefd07ea8af62e633a`: Cumulative gbounds, observation weights, variance restrictions, id and returned influence/cumulative-probability objects. (primary_technical_text).

## gformula: Parametric trajectory-simulation reference

Repository: `CausalInference/gfoRmula`. Observed package version: `1.1.2`. License observation: GPL-3 (DESCRIPTION).
Source snapshot: [gformula.json](software/gformula.json), SHA-256 `17603af1a8f98a0e285932f08d0a41096383ad8cf821c9f0a31b6259da57f153`.

Selected API commit: `86653ca1315f24a96a41b0ef590af13228f90ab4` (2025-11-03T16:01:40Z). Inspected API files at this commit; not an assertion about all README bytes or the published package release.

**Mathematical input.** Person-period data with explicit time, conditional covariate/outcome models, intervention functions, competing events, histories and Monte Carlo size.

**Mathematical output.** Intervention risks or terminal means/probabilities with model and optional bootstrap/simulation diagnostics.

**Scientific restrictions.** Sequential g-formula identification, specified transition/outcome law and meaningful event/observation conventions.

**Proposed adapter behavior.** Pin current intervention syntax; preserve baselags, visitprocess, competing-event handling and sim_trunc. sim_trunc defaults TRUE for specified continuous covariate families and alters the simulated law. nsimul controls Monte Carlo precision; nsamples controls bootstrap uncertainty.

**Proposed acceptance test.** Compare full-distribution simulation with exact two-period integration and mean-path substitution; vary nsimul separately from observed sample size. Use a tail-sensitive cash-flow target to quantify simulation truncation.

**Inspected support.**

- `docs/literature/raw/r3g_api_gformula.txt` lines 1--86, SHA-256 `200d3d04326a444c005734c53ba1499021aafe9bd0e1456dba415c5becb1d4d8`: Outcome-specific targets, conditional models, intervention API and baseline/history variables. (primary_technical_text).
- `docs/literature/raw/r3g_api_gformula.txt` lines 104--172, SHA-256 `200d3d04326a444c005734c53ba1499021aafe9bd0e1456dba415c5becb1d4d8`: Visit process, competing events, lag convention, simulation/bootstrap controls and sim_trunc. (primary_technical_text).

## zepid: Python epidemiologic-method reference

Repository: `pzivich/zEpid`. Observed package version: `0.9.1`. License observation: MIT.
Source snapshot: [zepid.json](software/zepid.json), SHA-256 `3e51f3f8d2c8815cc53d2a24246a1ae3c185ff97af8a15e3bf3f5cde6166ce2b`.

**Mathematical input.** Method-specific treatment/outcome/covariate data and explicitly selected weighting, g-computation, targeting or transport model.

**Mathematical output.** A specified point/longitudinal/transport estimand with that method's diagnostics.

**Scientific restrictions.** Selected method's exchangeability, positivity, missingness and transport conditions.

**Proposed adapter behavior.** Qualify individual classes before adapter implementation. The README documents monotone missingness for IPMW and single-time-point SNMM g-estimation; do not advertise general longitudinal SNMM fitting from the umbrella name.

**Proposed acceptance test.** Compare a chosen AIPW/g-computation class with an exact finite oracle, reject a nonmonotone pattern on a monotone-only path and distinguish point-treatment from longitudinal inputs.

**Inspected support.**

- `docs/literature/raw/raw_readme_zepid.md` lines 15--91, SHA-256 `53e33688ff43bca02560f00705dcd365614371de0c336073b044784d28c8ee5f`: Specific g-method/transport features, monotone IPMW and single-time SNMM scope. (primary_technical_text).

## pydynpd: Dynamic-panel moment estimator comparator

Repository: `dazhwu/pydynpd`. Observed package version: `0.2.2`. License observation: MIT.
Source snapshot: [pydynpd.json](software/pydynpd.json), SHA-256 `b3af4ada24bada895a3f3d5758a36db325c5f8e22353c3a1c900ef6adcb08eda`.

**Mathematical input.** Short panel, outcome lags, predetermined/exogenous regressors and explicit GMM/IV lag sets.

**Mathematical output.** Difference/system GMM coefficients, corrected two-step uncertainty and AR/Hansen diagnostics.

**Scientific restrictions.** Lag orthogonality, serial-correlation and initial-condition restrictions; system moments require additional level restrictions.

**Proposed adapter behavior.** Require an instrument ledger with count/lag depth/collapse choices. Automated model search and a nonrejected Hansen test do not establish valid moments or sufficient strength.

**Proposed acceptance test.** Compare sample moments to an independently built instrument matrix; add serial correlation and instrument proliferation; report bias and coverage alongside AR/Hansen output.

**Inspected support.**

- `docs/literature/raw/raw_readme_pydynpd.md` lines 5--72, SHA-256 `7eb81605441254cff176602dfdd13368df43c58282b0911b6f5fc9c0aeb42a82`: Dynamic panel equation, GMM families, transformations, corrected SE, diagnostics and explicit command syntax. (primary_technical_text).

