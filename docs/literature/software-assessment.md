# Open-source assessment

Observed 7 October 2026. Source inspection, not runtime qualification. Full hashes, package versions and limitations are in `software-assessment.json`.

The table retains the 44-project document assessment. A separate scope
qualification executed **DoubleML 0.11.4 IRM** with matched folds/nuisances and
**Tigramite 5.2.10.1 PCMCI+/LPCMCI** with retained graph marks. The installed
source, metadata, release records and licenses are preserved in `runtime-scope/`
and registered as `runtime_doubleml_scope` / `runtime_tigramite_scope`.
The former agrees with the independent AIPW coefficient and standard error;
the latter supplies exploratory graph outputs, with conditioning caps and
conditional-effect/refusal semantics. This does not qualify all methods in
those packages or promote the historical records to runtime acceptance.
DoubleML declares BSD licensing; Tigramite metadata declares GPLv3 or later.
Its installed distribution omitted a standalone full license file, and the
historical primary license snapshot remains separate evidence. Details and
executions are in `../studies/scope-public-results.json`,
`../studies/scope-discovery-results.json` and `../studies/scope-graph-effect-results.json`.

| Project | Role | License observed | Last repository push | Recommendation and boundary |
|---|---|---|---|---|
| [py-why/dowhy](https://github.com/py-why/dowhy) | Model, identify, estimate and refute; graphical causal mechanisms | MIT | 2026-10-06 | Wrap identification and refutation; require explicit estimand and graph version. Refutation failure is informative; passing refutations does not verify unmeasured-confounding assumptions |
| [py-why/EconML](https://github.com/py-why/EconML) | DML, forests, heterogeneous effects and IV; panel DynamicDML | MIT | 2026-10-06 | Primary Python heterogeneous-effect adapter. Estimator-specific exchangeability, IV and panel restrictions; preserve groups in fitting |
| [DoubleML/doubleml-for-py](https://github.com/DoubleML/doubleml-for-py) | Orthogonal scores, cross-fitting, inference and cluster data | BSD-3-Clause | 2026-09-23 | Primary transparent score/inference adapter. A supported cluster layout is not arbitrary temporal dependence |
| [uber/causalml](https://github.com/uber/causalml) | Meta-learners, trees and uplift evaluation | Apache-2.0 | 2026-10-05 | Marketing challenger. Uplift fit and predictive ranking alone do not establish identification |
| [grf-labs/grf](https://github.com/grf-labs/grf) | Honest causal, instrumental, survival and multi-arm forests | GPL-3.0 | 2026-04-30 | R benchmark and optional governed adapter. Copyleft review and dependence assumptions precede distribution |
| [jakobrunge/tigramite](https://github.com/jakobrunge/tigramite) | PCMCI, PCMCI+, LPCMCI, regime and multi-dataset variants | GPL-3.0 | 2026-01-14 | Primary temporal discovery research adapter. Stationarity, graph semantics, CI-test assumptions and copyleft require explicit review |
| [py-why/causal-learn](https://github.com/py-why/causal-learn) | Constraint, score and functional discovery plus CI tests | MIT | 2026-09-04 | Primary static discovery adapter. CPDAG/PAG endpoints cannot be silently converted to a DAG |
| [quantumblacklabs/causalnex](https://github.com/quantumblacklabs/causalnex) | PyPI package metadata available; official GitHub endpoint unavailable | Unverified in this audit | unavailabl | Defer new dependency. 404/rate-limited access does not establish archive status or current support |
| [microsoft/causica](https://github.com/microsoft/causica) | DECI joint graph and additive-noise structural-model inference | MIT | 2026-10-06 | Research comparator. Joint discovery/estimation does not remove structural assumptions |
| [huawei-noah/trustworthyAI](https://github.com/huawei-noah/trustworthyAI) | Causal discovery toolbox within trustworthyAI monorepo | Apache-2.0 | 2026-09-21 | Research comparator. Monorepo activity is not evidence of submodule maintenance |
| [kevinsbello/dagma](https://github.com/kevinsbello/dagma) | Linear/nonlinear DAG search with log-determinant acyclicity | Apache-2.0 | 2024-01-14 | Small benchmark comparator. Nonconvex optimization, causal sufficiency and functional assumptions remain |
| [xunzheng/notears](https://github.com/xunzheng/notears) | Continuous optimization under exact acyclicity constraint | Apache-2.0 | 2026-05-26 | Reference algorithm. Acyclicity is not causal identification; inspect numerical thresholding |
| [cmu-phil/tetrad](https://github.com/cmu-phil/tetrad) | Java causal discovery library and GUI | GPL-3.0 | 2026-10-06 | Cross-language benchmark. Deployment and licensing cost; graph semantics must survive serialization |
| [google/CausalImpact](https://github.com/google/CausalImpact) | Bayesian structural time-series intervention analysis | Apache-2.0 | 2026-03-31 | Aggregate campaign comparator. Untreated covariates and stable counterfactual relationship are essential |
| [pymc-labs/CausalPy](https://github.com/pymc-labs/CausalPy) | DiD, synthetic controls, RD, interrupted series and IV | Apache-2.0 | 2026-10-06 | Bayesian challenger. Posterior uncertainty is conditional on design and model assumptions |
| [bashtage/linearmodels](https://github.com/bashtage/linearmodels) | Panel, IV, system regression and covariance estimators | NCSA | 2026-10-06 | Econometric baseline adapter. Do not infer dynamic-panel GMM support from the panel-regression label |
| [py-econometrics/pyfixest](https://github.com/py-econometrics/pyfixest) | High-dimensional fixed effects, IV, event studies and robust covariance | MIT | 2026-10-07 | Primary Python panel adapter. Fast TWFE remains inappropriate for some heterogeneous staggered effects |
| [lrberge/fixest](https://github.com/lrberge/fixest) | Multiway fixed effects, IV, GLM and inference | GPL-3 | 2026-06-26 | R reference adapter. GPL review; specify the estimand before the regression formula |
| [bcallaway11/did](https://github.com/bcallaway11/did) | Group-time ATT with att_gt and aggregation | GPL-3 | 2026-08-28 | R reference for modern DiD. No anticipation, group-specific parallel trends and comparison support |
| [asheshrambachan/HonestDiD](https://github.com/asheshrambachan/HonestDiD) | Robust confidence sets under restricted trend violations | MIT | 2026-04-12 | Sensitivity adapter. Sensitivity restriction is substantive, not learned truth |
| [synth-inference/synthdid](https://github.com/synth-inference/synthdid) | Synthetic difference-in-differences estimator | BSD-3-Clause | 2024-01-15 | Optional comparator. Documented block treatment/simultaneous adoption and beta API |
| [xuyiqing/gsynth](https://github.com/xuyiqing/gsynth) | Counterfactual imputation using interactive fixed effects | MIT | 2026-09-30 | Optional factor-model comparator. Latent-factor extrapolation and support require validation |
| [takuseno/d3rlpy](https://github.com/takuseno/d3rlpy) | Offline/online RL and distributed training | MIT | 2025-09-10 | Policy challenger after evaluation design. Logged support and causal information set are separate from learner capability |
| [hakuhodo-technologies/scope-rl](https://github.com/hakuhodo-technologies/scope-rl) | OPE, policy selection and distributional evaluation | Apache-2.0 | 2024-03-18 | OPE comparator. Snapshot last push in 2024; no generic hidden-confounding guarantee |
| [st-tech/zr-obp](https://github.com/st-tech/zr-obp) | Bandit OPE/learning and logged bandit data tools | Apache-2.0 | 2024-06-03 | One-step policy comparator. Contextual bandits do not represent multi-period banking carryover |
| [h2r/pomdp-py](https://github.com/h2r/pomdp-py) | POMDP modeling, belief updating, planning and simulation | MIT | 2025-10-28 | Small reference planner. Planning interface is not a causal parameter estimator |
| [JuliaPOMDP/POMDPs.jl](https://github.com/JuliaPOMDP/POMDPs.jl) | Julia model interface, tools, solvers and simulators | MIT | 2026-10-04 | Julia reference planner. Solver ecosystem versions/licenses must be pinned separately |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | MCMC and variational Bayesian modeling | Apache-2.0 | 2026-10-06 | Hierarchical-model comparator. Convergence and posterior fit do not identify interventions |
| [pyro-ppl/numpyro](https://github.com/pyro-ppl/numpyro) | JAX probabilistic programming and HMC | Apache-2.0 | 2026-10-05 | Accelerated inference adapter candidate. Discrete states often need marginalization; hardware speed unmeasured here |
| [probml/dynamax](https://github.com/probml/dynamax) | JAX state-space filtering and parameter learning | MIT | 2026-10-01 | First latent-dynamics comparator. Statistical state models need separate controlled causal identification |
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | Embedded SQL analytics with window/nested queries | MIT | 2026-10-07 | Default local reference execution. Measure spill, memory and point-in-time correctness on bank workloads |
| [pola-rs/polars](https://github.com/pola-rs/polars) | Lazy/streaming analytical DataFrames; optional GPU | MIT | 2026-10-07 | Optional columnar adapter. Capability does not establish distributed causal estimation |
| [ray-project/ray](https://github.com/ray-project/ray) | Distributed task execution and ML tools | Apache-2.0 | 2026-10-07 | Add only when single-node profiling warrants. Fault recovery, deterministic folds and aggregation are product responsibilities |
| [datahub-project/datahub](https://github.com/datahub-project/datahub) | Metadata graph, ownership, column lineage and discovery | Apache-2.0 | 2026-10-07 | Integrate the bank's existing catalog. Semantic context and lineage are not causal knowledge |
| [open-metadata/OpenMetadata](https://github.com/open-metadata/OpenMetadata) | Metadata, data quality, lineage, ownership and contracts | Apache-2.0 | 2026-10-07 | Alternative catalog integration. Avoid operating a duplicate enterprise catalog |
| [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) | Open standard for runtime job/dataset lineage | Apache-2.0 | 2026-10-06 | Adopt run and dataset lineage events. Add causal estimands and assumptions as explicit custom facets |
| [feast-dev/feast](https://github.com/feast-dev/feast) | Offline/online feature access and point-in-time retrieval | Apache-2.0 | 2026-10-07 | Integrate existing feature store. Event-time joins must additionally enforce actual availability time |
| [moj-analytical-services/splink](https://github.com/moj-analytical-services/splink) | Probabilistic record linkage and match diagnostics | MIT | 2026-10-06 | Optional entity-resolution adapter. Propagate uncertain links; false merges can induce causal bias |
| [unionai-oss/pandera](https://github.com/unionai-oss/pandera) | Typed dataframe validation across engines | MIT | 2026-10-07 | Contract-validation adapter. Schema validity does not establish causal semantics |
| [nt-williams/lmtp](https://github.com/nt-williams/lmtp) | Longitudinal modified treatment policies, TMLE and sequential DR; competing risks | AGPL-3.0 | 2026-07-01 | Qualified R longitudinal comparator. DESCRIPTION and license text specify AGPL-3, despite GPL-3 README badge; support and causal restrictions remain |
| [joshuaschwab/ltmle](https://github.com/joshuaschwab/ltmle) | Longitudinal TMLE of treatment/censoring-specific means and marginal structural models | GPL-2 | 2026-06-03 | R reference implementation. Censoring, intervention support and chronological node semantics need explicit checks |
| [CausalInference/gfoRmula](https://github.com/CausalInference/gfoRmula) | Parametric g-formula with time-varying treatments, failure times and competing events | GPL-3 (DESCRIPTION) | 2025-11-03 | R g-computation comparator. Model specification and intervention semantics are substantive; full license text not separately retrieved |
| [pzivich/zEpid](https://github.com/pzivich/zEpid) | IPTW/IPCW, AIPW, g-formula, TMLE and transportability tools | MIT | 2023-05-07 | Python g-method reference comparator. Observed last push May 2023; qualify dependency compatibility and exact longitudinal method scope |
| [dazhwu/pydynpd](https://github.com/dazhwu/pydynpd) | Difference/system GMM, corrected two-step errors, AR and Hansen diagnostics, collapsed instruments | MIT | 2025-12-15 | Dynamic-panel GMM comparator. Moment restrictions and instrument proliferation are scientific choices; package model search cannot validate them |
