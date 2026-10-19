## R effect estimation: agree on the decision before comparing packages

The new R comparison distinguishes individual conditional effects, population
and treated-group averages, pooled slopes and continuous dose curves. The
inspected R DoubleML implementation has explicit ATE/ATTE score paths and
cluster-aware splitting and variance calculations. Its multiplier bootstrap
rejects clustered data; the proposed service must preserve that refusal when
joint uncertainty is requested. The grf averaging routes have their own target
and uncertainty restrictions. A Python implementation with the same name does
not establish the behavior of the R version.
\citep{exec20_rfx_doubleml_r,exec13_grf_rpath}

The tmle documentation's broad missing-treatment wording is narrowed by its
actual argument guard: the selected function rejects missing treatment labels.
Its null-treatment input selects a mean-outcome path, not a recovery of unknown
assignments. An exact generated example has identical observed data but effects
of USD 100 and USD 0 at a stipulated outcome scale. The example deliberately
lacks observation support for the group with erased labels; it motivates a
truthful label or additional-assumption requirement rather than a claim that
all missing-data analysis is impossible. \citep{exec20_rfx_tmle,exec20_rfx_reference}

Continuous-exposure engines also require unit and target checks. In an authored
credit example, a USD 1,000 increase has a stipulated margin contrast of USD 15;
using a pooled slope instead would give USD 35. CausalGPS weighting and causaldrf
dose prediction expose different transformation and uncertainty obligations.
The proposed public prototype should test conditional scales, exposure units,
counterfactual-dose scores, zero weights and full-stage resampling before any
bank experiment. These examples are not measured returns or native R tests.
\citep{exec20_rfx_reference,exec20_rfx_causalgps,exec20_rfx_causaldrf}

The adoption proposal is to wrap supported grf, R DoubleML and observed-treatment
tmle paths conditionally, while deferring native ports and unqualified continuous
exposure paths. BART-based alternatives, causalweight, further ecosystem aliases,
complete distribution rights and native conformance remain open. This successor
retains the preceding commercial dynamic-panel comparison and Feast proposal.
\citep{sp19dyn_reader,sp19dyn_progress}

