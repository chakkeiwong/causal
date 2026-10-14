# Source-to-question matrix

9 October 2026. Publication cutoff: 7 October 2026.

Question-led reconstruction map. A source ID points to a preserved PDF and reading notes. Inherited inspection records are distinguished from passages re-read in this reconstruction; none of these rows declares a domain complete.

Full source identity, preserved path and hashes: [source register](sources.json). Current claim/anchor trace: [reconstruction-source-trace.json](reconstruction-source-trace.json).

## 1. Causal semantics

What intervention and counterfactual does the scientific model define, and which joint counterfactual restrictions does it impose?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| pearl2009 | Sections 3.1--3.2, printed pp.103--115 | re_read |
| swig2013 | Sections 1--2, PDF pp.1--5: model classes, splitting and modularity | re_read |
| hernan2020 | Chapters 1--3; Chapter 21 Technical Point 21.1 | mixed_inherited_and_re_read |

**Draft anchors:** r3:graphs; r3:mediation-interventions; r3:interference

**Remaining scholarship:** Semantics were checked against the seven proposed operations. General path-specific identification and arbitrary network interference remain outside initial algorithm support; the supplied edge and randomized-mediator examples have explicit distinct targets.

## 2. Diagram construction

How are decision, observation, latent and selection mechanisms converted into a defensible graph?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| pearl2009 | Definition 1, Definition 3 and SCM discussion | re_read |
| peters2017 | Chapter 6, Proposition 6.41 and Example 6.46 | re_read |
| gerhardus2020 | Section 2: latent time-series graph, no selection, window dependence | re_read |
| zhang2008 | Section 3, Definitions 1--3; marginal ancestral graph construction | re_read |
| perkovic2018 | Section 2; visibility and definite-status paths | re_read |
| pearltransport2014 | Definitions 4--5, Theorem 2/Corollary 1; Examples 1--2 | re_read |

**Draft anchors:** r3:graph-construction; r3:latent-graphs; r3:selection-diagram

**Remaining scholarship:** Selection-domain and proxy shifts are explicit. Selection-inclusive discovery and general transport algorithms remain distinct from the proposed no-selection discovery and registered transport templates.

## 3. Identification logic

Which observable functional or identified set follows, and what certifies nonidentification?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| pearl2009 | Definition 2, Theorem 1, Corollary 1; Section 3.5 | re_read |
| id2006 | Sections 3--6, Figures 2--3, hedge and ID/IDC theorems | re_read |
| peters2017 | Section 6.7, Example 6.46 | re_read |
| perkovic2018 | Definitions 1--4, Theorems 5 and 7 | re_read |

**Draft anchors:** r3:id-algorithm; r3:general-adjustment; r3:graph-effects; r3:id-trace; r3:mediation-interventions

**Remaining scholarship:** Recursive ID/IDC and failure witnesses are worked through. Finite discrete kernel product, marginalization and intervention semantics now have local executed checks. General ID/PAG and path-specific engines, including executable hedge validation, remain implementation work.

## 4. Randomization and adaptive assignment

Which assignment mechanism identifies ITT, receipt effects and dynamic value under clusters, spillovers and optional stopping?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| angrist1996 | Assumptions 1--5, equation (9), Proposition 1 | re_read |
| hernan2020 | Chapters 2--3 and 21 | mixed_inherited_and_re_read |
| howard2021 | Definition 1, Lemma 2, Appendix A.3/Proposition 5 | re_read |

**Draft anchors:** r3:targets; r3:late; r3:adaptive-inference; r3:interference

**Remaining scholarship:** Known predictable assignment, a mixture boundary, repeated exact tests and exposure-map randomization are developed. Unknown propensities, selected delays, cross-cluster spillovers and adaptive policy optimization need distinct guarantees.

## 5. Instrumental variables

When does an IV graph identify a homogeneous coefficient, complier effect or nonlinear response?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| angrist1996 | Section 2 and Section 3, printed pp.445--448 | re_read |
| dml2018 | Section 4.2 equations (4.5)--(4.8) | re_read |
| pearl2009 | Section 3.5: graph, linear effect and nonidentification | re_read |
| staiger1994 | Printed pp.4--6, 15--17, equation (2.24), Theorem 3 | re_read |
| hall2005 | Sections 2 and 4.1--4.2, A.1--A.5 and Theorems 4.1--4.2 | re_read |
| imbens2002 | Assumptions 3.1--3.3, Theorems 1--2; Appendix A | re_read |
| casini2025 | Sections 2.1--2.2.1, pp.10--14: Assumptions 2.1--2.5, equation 2.4 and Proposition 2.1; shock versus policy and responsive-population weights; Section 2.2.2, pp.15 onward: deterministic complier status Assumption 2.6 and local comparison/smoothness 2.7--2.8 | primary_text_inspected_in_scope_revision |
| kleibergen2021 | Section 2, pp.2--9: population continuously updated criterion, pseudo-true parameter and structural interpretation; Section 3, pp.10--12: Assumptions 1--2, Theorems 2--4; joint moment/Jacobian CLT and covariance convergence | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:instruments; r3:inverse-functional; r3:inverse-rates; r3:control-function; s5:response-inference; s5:composition

**Remaining scholarship:** Dynamic LATE has responsive-population and source-specific local-smoothness restrictions. Misspecification-robust CUE targets a pseudo-true minimizer, which need not retain a causal interpretation. Original 1949 AR and Newey–Powell texts remain unavailable; the project residual-test inversion is explicitly derived.

## 6. Semiparametric statistics and causal ML

How does an identified functional determine a gradient, nuisance remainder, learning loss and valid inference?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| dml2018 | Section 5.1, score (5.3), Assumption 5.1, Theorem 5.1 | re_read |
| rlearner2020 | Sections 2 and 5: R-loss and kernel quasi-oracle analysis | re_read |
| drlearner2023 | Theorem 2 and Corollary 1, pp.12--13: stable smoother and local rates | re_read |
| grf2018 | Algorithm 1, Specification 1, condition (13), Theorem 5 | re_read |
| kunzel2019 | Meta-learner construction and imputed contrasts | re_read |
| policy2021 | Sections 2.1--2.3, Assumptions 1--4 and Theorem 1 | re_read |
| targeted2018 | Chapter 4, Sections 4.4--4.5, pp.40--46 | re_read |
| dynamicdml2021 | Section 2.1, Theorem 2: conditional blip moments and residual treatment-covariance identification; Section 2.2 and Algorithm 1: independent trajectories, fixed treatment dimension/horizon, recursive residualization and cross-fitting; Sections 2.3 onward: source separately develops rates, normality and extended blip/dependence regimes; no universal package-level inheritance | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| paneldml2024 | Sections 2–4, especially pp.6–7: early/late demeaning, correlated random effects and DML/panel comparison; Problem statement and simulation scope: comparison of point-estimator adaptations | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| bica2020 | Appendix B, Assumptions 1–3: consistency, positivity and sequential strong ignorability; Main-text Theorem 1 and Appendix proof: ideal treatment-adversarial optimum equalizes treatment-group representation distributions | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| causalpfn2026 | Sections 3.2–4.2, Definitions 3.1 and 4.2: practitioner-supplied identification and priors on SCM-induced observational/interventional pairs; Theorem 4.3: linear query, noncancellation condition within observational-equivalence classes and prior-consistency necessity; IV example: additive structural response, independence and completeness; not generic LATE | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| babii2020 | First page and Introduction: archive v4 12 December 2020 and internal date 15 December 2020, nowcasting/mixed-frequency motivation; Section 3.2, pp.10--13, Assumptions 3.1--3.4, Theorem 3.1, Corollary 3.1: product-process moments/mixing, restricted eigenvalue, tail/dependence penalty and approximation error | primary_technical_text_read_in_scientific_completion |
| ciganovic2026 | First page and Section 1: arXiv v1 11 March 2026, PLR target and capital-regulation application; Section 2.3, pp.6--8, Assumptions 2.1--2.5: oracle FCLT, smoothness, conditional plug-in stability and fixed folds; Section 2.4, Theorem 2.1 and Supplement S1 pp.S1--S2: fold-average asymptotic variance and stacked chronological HAC | primary_technical_text_read_in_scientific_completion |
| ran2026 | Sections 2.2--2.4, pp.4--5: observed-history intervention, censoring and future-history exchangeability; Definition 1; Section 5, pp.11--14: Assumptions 5--9, Theorems 1--6 and Corollary 1 | primary_text_inspected_in_scope_revision |
| runtime_doubleml_scope | doubleml-0.txt lines 271--370: external nuisance predictions, clipping and ATE score; doubleml-1.txt lines 1--46: fit external_predictions contract; doubleml-metadata.txt lines 1--49: version and BSD license | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:influence; r3:ml-remainder; r3:cate-rates; r3:recent-dynamic-dml; r3:balance-limit; r3:causal-fm; s4:dependent-learning; s5:history-censoring; s5:composition

**Remaining scholarship:** Continuous observed-history censoring has a telescoping remainder and explicit fixed-horizon nuisance-product conditions; selected boosting fits are not a general proof of those rates. Matched DoubleML score/SE checks use identical folds and predictions. General dependent CATE bands and increasing-horizon learning remain separate research.

## 7. Endogeneity, proxies, representations and transport

Which rank, completeness, measurement and environment restrictions survive learned representations?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| dml2018 | Section 4.2 partially linear IV score | re_read |
| miao2018 | Proxy conditional-independence and latent completeness identification argument | re_read |
| proximal2020 | Existing notes: bridge and completeness restrictions | inherited_only |
| ghassami2022 | Bridge functional, mixed bias and minimax conditional moments | re_read |
| hall2005 | Sections 2 and 4 | re_read |
| pearltransport2014 | Definitions 4--8, Theorem 2 and Corollary 1 | re_read |
| petersicp2016 | Assumption 1, Proposition 1 and Theorem 1 | re_read |
| ovb2022 | Assumptions 1--2, Lemma 1, Theorem 2/Corollary 2 and Appendix B.4 | re_read |
| imbens2002 | Theorems 1--2, rank and support | re_read |
| proximalfm2026 | Sections 2.1–2.2: latent exchangeability, proxy exclusions, positivity, completeness and bridge existence; equations (2)–(3); Section 3.1 and Appendix B.3.4: structural/noise inputs, propensity clipping, proxy dimension/cardinality heuristics and relevance diagnostics; arbitrary nonlinear completeness not guaranteed; Appendix A.1–A.4, Lemma A.3, Theorem A.4 and equations (18)–(19): oracle prior-almost-sure consistency at a fixed query, Monte Carlo labels and unproved neural approximation term | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| causalpfn2026 | Sections 3.2–4.2, Definitions 3.1 and 4.2: practitioner-supplied identification and priors on SCM-induced observational/interventional pairs; Theorem 4.3: linear query, noncancellation condition within observational-equivalence classes and prior-consistency necessity; IV example: additive structural response, independence and completeness; not generic LATE | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| zhangprox2024 | Sections 2--3: sequential proximal latent randomization and target dynamic-regime value; Assumption 2 and Theorem 1: time-varying bridge equations for joint counterfactual identification; Assumption 3 and Corollary 1: completeness/relevance and observable bridge characterization | primary_text_inspected_in_scope_revision |
| wei2026 | Sections 2--3: MNAR reward observation, no-future-dependence, concentrability and augmented-state assumptions; Assumptions 3.1--3.4 and Theorem 3.6: shadow next-state exclusion/relevance and completeness for bridge identification; Section 4: bridge estimation as an NPIV/conditional-moment problem and finite-sample value route | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:inverse-functional; r3:proximal-score; r3:proximal-fm; r3:causal-fm; r3:transport; s5:private-logger

**Remaining scholarship:** Bridge existence/range is separate from completeness/injectivity. Labelled measurement validation, observed-history exchangeability and sequential proxy assumptions identify different objects. No automatic unobserved exclusion, bridge existence or cross-bank invariance validation is claimed.

## 8. Longitudinal counterfactuals and g-methods

How do g-computation, weighting, MSMs, SNMMs and recursive augmentation estimate distinct dynamic targets?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| hernan2020 | Chapter 21, Technical Points 21.1 and 21.3 | re_read |
| snm2014 | Sections 3.2, 5, 6.1, equations (14), (24), (32)--(33) | re_read |
| jiang2016 | Section 4.1, equation (10) | mixed_inherited_and_re_read |
| sequentialdr2018 | Sequential robustness and augmented pseudo-outcome recursion | re_read |
| kennedy2019 | Theorem 1, Corollaries 1--2, Theorem 3 | re_read |
| targeted2018 | Chapter 4, Sections 4.4--4.5 | re_read |
| lmtp2023 | Assumptions 1--4, Theorems 1--2 and equation (3) | re_read |
| selective2025 | Sections 2.1--2.2, Assumptions 1--3 and eligible-treatment target | re_read |
| competing2026 | Sections 2.1--2.2, event order and equations (1)--(3) | re_read |
| roysland2024 | Definition 2, Proposition 1 | re_read |
| rytgaard2021 | Definitions 1--2 and Theorems 1--2 | re_read |
| ryalen2026 | Definition 3, Theorem 1/proof, Definition 5/Remark 2 | re_read |
| gnet2020 | Sections 3–4, assumptions 1–3, conditional g-formula, Algorithm 1 and equation (5): intervention simulation and conditional covariate factorization; Section 4 continuous-variable residual sampling from a holdout set; distributional simulation versus conditional-mean fitting | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| melnychuk2022 | Section 3: target conditional mean under a future treatment sequence and autoregressive prediction inputs; Appendix A, Assumptions A.1–A.3 and Corollary A.4: consistency, sequential overlap, ignorability and g-computation | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| dynamicdml2021 | Section 2.1, Theorem 2: conditional blip moments and residual treatment-covariance identification; Section 2.2 and Algorithm 1: independent trajectories, fixed treatment dimension/horizon, recursive residualization and cross-fitting; Sections 2.3 onward: source separately develops rates, normality and extended blip/dependence regimes; no universal package-level inheritance | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| ran2026 | Sections 2.2--2.4, pp.4--5: observed-history intervention, censoring and future-history exchangeability; Definition 1; Section 5, pp.11--14: Assumptions 5--9, Theorems 1--6 and Corollary 1 | primary_text_inspected_in_scope_revision |
| zhangprox2024 | Sections 2--3: sequential proximal latent randomization and target dynamic-regime value; Assumption 2 and Theorem 1: time-varying bridge equations for joint counterfactual identification; Assumption 3 and Corollary 1: completeness/relevance and observable bridge characterization | primary_text_inspected_in_scope_revision |
| wei2026 | Sections 2--3: MNAR reward observation, no-future-dependence, concentrability and augmented-state assumptions; Assumptions 3.1--3.4 and Theorem 3.6: shadow next-state exclusion/relevance and completeness for bridge identification; Section 4: bridge estimation as an NPIV/conditional-moment problem and finite-sample value route | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:g-formula; r3:msm-snm; r3:long-gradient-proof; r3:event-gradient; r3:neural-g; r3:recent-dynamic-dml; s4:fitted-history; s5:history-censoring

**Remaining scholarship:** Fitted continuous histories, monotone MAR censoring, separate policy training and trajectory contrast inference now have executed comparisons and exact stopping-path checks. MNAR failure is retained. Natural irregular-visit histories differ from changing visit intensity or using latent complete paths. Common-shock and increasing-horizon inference remain model-specific.

## 9. Longitudinal and state-space bridge

When does a controlled latent model reduce to history g-computation, and how does private logging change the filter?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| hernan2020 | Technical Point 21.1 | re_read |
| kaelbling1998 | Sections 3.2--3.4 | re_read |
| rabiner1989 | Existing notes: forward/backward and expected counts, printed pp.264--266 | inherited_only |
| tennenholtz2020 | Existing notes: partial-observation OPE information restrictions | inherited_only |
| sarkka2013 | Sections 4.3, 7.3 and 12.1 | re_read |
| bennettprox2023 | Section 4, Assumptions 1--2, Theorem 2 and Proposition 1 | re_read |
| sde2026 | Definitions 3--5 and Theorems 6, 11--12 | re_read |
| boeken2024 | Definitions 4--7 and Section 5 | re_read |
| zhangprox2024 | Sections 2--3: sequential proximal latent randomization and target dynamic-regime value; Assumption 2 and Theorem 1: time-varying bridge equations for joint counterfactual identification; Assumption 3 and Corollary 1: completeness/relevance and observable bridge characterization | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:state-bridge; r3:filtering; r3:controlled-estimation; r3:sequential-proxies; r3:marked-reward-identification; r3:continuous; s4:unknown-emission; s5:private-logger; s5:continuous-controlled

**Remaining scholarship:** A validated multistate private logger and a continuous Gaussian private logger now each have constructive identification, matched likelihood and value inference. The Gaussian route requires known noise/initial laws and calibrated scale. Its deterministic continuous policy is structurally identified, singular for ordinary density-ratio weighting. General nonlinear identification remains unestablished.

## 10. POMDP estimation and structural behavior

Which likelihood parameters and policy values are identified, including customer choice and equilibrium response?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| hmmident2016 | Section 2, A1--A3 and Theorem 1 | re_read |
| kaelbling1998 | Sections 3.2--3.4 and belief-MDP construction | re_read |
| bennett2021 | Existing notes: MDPUC information and assumptions | inherited_only |
| xu2023 | Existing notes: sequential IV exclusions and interaction restrictions | inherited_only |
| kalouptsidi2021 | Section 2, equations (1)--(6); Section 3.1 | re_read |
| imai2009 | Sections 2.2--2.3 and 3, Assumptions 1--8/Theorems 1--2 | re_read |
| sarkka2013 | Sections 4.3, 7.3 and 12.1 | re_read |
| sde2026 | Definitions 3--5 and Theorems 6, 11--12 | re_read |
| boeken2024 | Definitions 4--7 and Section 5 | re_read |
| opehard2026 | Sections 2.1–2.2: two hidden-lane models, common history-dependent logger, all-continue target and rare informative path; Definition 3.1 and Theorem 4.1: behavior-marginal revealing/coverage scope and exponential sample lower bound; Section 4.1 and Proposition 5.1: three-symbol experiment and trajectory KL; Theorem 5.2: optimal fair-tie test; Section 7: physical-state insufficiency for history-dependent logger continuation and rare state after memory augmentation | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| sharpdynamic2026 | Sections 2.1–2.2: finite observed state and contemporaneous stage-specific confounding; persistent latent customer characteristics excluded; Definition 3.1, Steps 1–4 and equations (7)–(9): default local feasible transition polytopes; Theorem 3.8: exact causal sharpness of the unmodified default family; Section 4.1, equations (12)–(14) and backward-induction proof: rectangular set value recursion | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| spectral2016 | Title page, archive v1 and Introduction: controlled spectral learning, memoryless policy benchmark and planning oracle; Sections 2--3, pp.8--9, Assumptions 1--4: ergodicity, full-column-rank emissions/transitions and policy set; Sections 3.1--3.2, pp.9--12, action-conditioned three views, Proposition 1, Lemma 1, equations (5)--(9), Theorem 1 and Algorithm 1 | primary_technical_text_read_in_scientific_completion |
| wei2026 | Sections 2--3: MNAR reward observation, no-future-dependence, concentrability and augmented-state assumptions; Assumptions 3.1--3.4 and Theorem 3.6: shadow next-state exclusion/relevance and completeness for bridge identification; Section 4: bridge estimation as an NPIV/conditional-moment problem and finite-sample value route | primary_text_inspected_in_scope_revision |
| zhangprox2024 | Sections 2--3: sequential proximal latent randomization and target dynamic-regime value; Assumption 2 and Theorem 1: time-varying bridge equations for joint counterfactual identification; Assumption 3 and Corollary 1: completeness/relevance and observable bridge characterization | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:controlled-identification; r3:customer-choice; r3:ope-hardness; r3:dynamic-bounds; s4:latent-inference; s4:pomdp-error; s5:private-logger; s5:continuous-controlled

**Remaining scholarship:** Three-state joint uncertainty undercovers and the 199-refit bootstrap withholds an interval after 17 failed/boundary fits. Exact Gaussian likelihood/score comparisons are more favorable within their own restrictions. Profile/boundary inference, general nonlinear state estimation and strategic equilibrium remain research; a routine calibrated finite-state interval is not released.

## 11. Econometric panels and dynamic systems

How do panel and shock moment restrictions relate to causal interventions, heterogeneity and dependent inference?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| arellano1991 | Section 2, equations (2)--(6); Section 3, equations (8)--(9) | re_read |
| callaway2021 | Section 2.3 assumptions 3--6; Section 2.4/Theorem 1 | re_read |
| stock2018 | Sections 2.2--2.5, Condition LP-IV/equation (8) | re_read |
| jorda2024 | Sections 6.1--6.3, equations (24)--(29) | re_read |
| cluster2021 | Assumptions 1--3/Theorems 1--2 | re_read |
| dechaisemartin2024 | Section 2.3 and Section 3.1/Lemma 1 | re_read |
| abadie2010 | Section 2.2 equations (1)--(4) | re_read |
| hyvarinen2010 | Sections 2.1--2.3 | re_read |
| rambachan2023 | Section 2.3/Lemma 2.1; Sections 2.4.1--2.4.4 and inference setup | re_read |
| bongers2022 | Definition 4.9, Theorems 4.11 and 4.18 | re_read |
| newey1986 | Scanned title page: NBER Technical Working Paper 55, April 1986, authors and title; Printed pp.2--4, equations (4)--(7) and Theorem 1: lag-covariance estimator, modified Bartlett weights and positive-semidefinite proof; Printed pp.5--6, Theorem 2: differentiability/envelopes, higher moments, mixing, root-T fitted parameters and bandwidth o(T^(1/4)) | primary_technical_text_read_in_scientific_completion |
| lpaug2020 | Title page and Introduction footnote 1: v1 identity, dates, focus on marginal rather than joint inference; Section 2, Assumption 1 and equations around lag-augmented AR example: innovations mean independent of all other dates; Sections 4.1--4.3, pp.20--23, Definition 1, Assumptions 2--3, Proposition 1: parameter space, moments/cumulants, scaled nonsingularity and horizon restrictions | primary_technical_text_read_in_scientific_completion |
| inoue2023 | First page, arXiv v1 and cover: exact title Significance Bands for Local Projections and three authors; Introduction and pp.3--5, equations (3)--(8): null score, long-run covariance and Bonferroni joint significance bands | primary_technical_text_read_in_scientific_completion |
| johansen2017 | Journal first page: Econometrics 2017, 5, 36, DOI, authors and publication date; Section 1 pp.1--2, equations (1)--(2): random-walk trend, observation law, likelihood and invertible trend-coordinate ambiguity; Section 4 pp.8--9, Theorems 1--2 and decomposition: identified trend components versus individually normalized trend estimates | primary_technical_text_read_in_scientific_completion |
| blundellbond2023 | Abstract and Section 1: dynamic panels with persistent economic series and motivation for system estimator; Section 2.3, pp.104--105: differenced moments, two-step weight and finite-sample variance correction; Section 2.4, p.106: weak instruments as persistence approaches unity and initial-condition alternatives; Sections 3.1--3.3, pp.107--109: E(delta y_i2 alpha_i)=0, decomposition around long-run mean, level instruments and weighting qualification | primary_text_inspected_in_scope_revision |
| kleibergen2021 | Section 2, pp.2--9: population continuously updated criterion, pseudo-true parameter and structural interpretation; Section 3, pp.10--12: Assumptions 1--2, Theorems 2--4; joint moment/Jacobian CLT and covariance convergence | primary_text_inspected_in_scope_revision |
| casini2025 | Sections 2.1--2.2.1, pp.10--14: Assumptions 2.1--2.5, equation 2.4 and Proposition 2.1; shock versus policy and responsive-population weights; Section 2.2.2, pp.15 onward: deterministic complier status Assumption 2.6 and local comparison/smoothness 2.7--2.8 | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:panels; r3:time-series; r3:trend-sensitivity; r3:equilibrium; s4:response-construction; s4:date-panel; s5:dynamic-panel; s5:response-inference

**Remaining scholarship:** System initial-law moments and one/two-step sandwiches are derived and compared; invalid initial/serial moments fail. The original Windmeijer correction is not implemented. Same-target covariance alternatives, separate lag-augmented joint bands and common-date comparisons form an explicit hierarchy. Unknown cointegration rank, breaks and heavy-tail mixed-frequency combinations need distinct qualification. V6 supplies decision-specific cohort influence, donor inference and calibrated linkage comparisons; see dynamic-decision-ledger.md for exact scope and unresolved generality.

## 12. Causal discovery

What graph equivalence object can be learned under temporal, functional, latent and selection assumptions?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| peters2017 | Definition 6.24, Lemma 6.25; Chapter 10 not yet re-read | mixed_inherited_and_re_read |
| gerhardus2020 | Sections 2.1--2.3 | re_read |
| notears2018 | Theorem 1 and Section 4 | re_read |
| runge2019 | Existing notes: PCMCI conditioning | inherited_only |
| hyvarinen2010 | Existing notes: structural non-Gaussian time-series model | inherited_only |
| zhang2008 | Section 3, Definitions 1--3 | re_read |
| perkovic2018 | Section 3, Theorem 5 | re_read |
| kalisch2007 | A1--A4, Theorems 1--2 | re_read |
| runge2020 | Assumptions 1/Theorems 1--2 | re_read |
| petersicp2016 | Assumption 1, Proposition 1 and Theorem 1/proof | re_read |
| sde2026 | Theorems 14--15, Definition 9 and Example 10 | re_read |
| itsy2026 | Section 3.1, equation (1) and Assumptions 1–3: linear first-order SVAR, contemporaneous DAG, sufficiency, stationarity and MCAR; Sections 3–4: underlying missing grid, reduced-form noise transformation and coupled imputation/graph-learning objective | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| lucid2026 | Section 4.1: VAR(1) residual spectrum and Marchenko–Pastur routing between sparse and pervasive regimes; Sections 4.2–4.3: post-double-selection branch, spectral trimming, persistence gate and contemporaneous recovery; Novel-versus-adopted-components paragraph: lag-zero orientation explicitly heuristic; router-separation proof referred to extended version | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| panelpfn2026 | Sections 3.2–3.6: temporal tokens, judgment head, mixed causal-regime priors and context selection; Section 3.6.2, equation (10): generic EIF correction followed by an assertion of double robustness and valid confidence intervals | Technical primary passages read; theorem boundaries reconstructed; no package/model replication. |
| rohekar2023 | Title/abstract and PMLR/arXiv identity: stationary SVAR with temporal and contemporaneous relations and latent confounders; Sections 2--3, definitions/algorithm: faithfulness, causal Markov, dynamic PAG and TS-ICD ordering; Theorem/completeness discussion: soundness/completeness is conditional on the stated oracle assumptions | primary_text_inspected_in_scope_revision |
| gerhardus2021 | Sections 2--4: temporal latent projection and stationarification definitions; Sections 4.5--4.6, pp.19--20: then-current LPCMCI/tsFCI/SVAR-FCI incompleteness under stronger time-series graph class; conceptual enumeration; Section 5.1, pp.21--22, Propositions 5.2--5.7: information gained by longer observed window | primary_text_inspected_in_scope_revision |
| runtime_tigramite_scope | pcmci-operation.txt lines 28--99: sufficiency, stages and endpoint semantics; lines 187--194 output matrices; lpcmci-operation.txt lines 1--32 and 147--158: conditioning caps, graph and p/value matrices; parcorr-operation.txt: linear partial correlation and analytic significance; tigramite-metadata.txt lines 1--14 and 172--180: version and GPLv3+ declaration | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:discovery; r3:recent-discovery; r3:causal-fm; s4:graph-confidence; s4:temporal-graph-confidence; s5:discovery

**Remaining scholarship:** PCMCI+/LPCMCI operations are version-bound executions; 20-repeat comparisons do not certify graphs. A bounded sufficient-graph adapter preserves collider restrictions and unresolved order through fresh-data effects. It refuses PAG endpoints and hidden-effect requests outside its model. Graph-selection uncertainty and general PAG effect confidence remain unresolved.

## 13. Observation and automatic data organization

How do measurement, sampling, aggregation, missingness and entity linkage change identification?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| hernan2020 | Existing missingness/selection discussion and reconstructed censoring identities | mixed_inherited_and_re_read |
| corrupt2022 | Sections 3.2--3.3 and 4.1 | re_read |
| gerhardus2020 | Section 2.3: time-window marginalization | re_read |
| tu2019 | Section 3, Assumptions 1--4 and Proposition 1 | re_read |
| roysland2024 | Sections 3.2--3.4 and 6 | re_read |
| rytgaard2021 | Definitions 1--2 | re_read |
| slawski2025 | Sections 2.1--2.2: consistency/SUTVA, mismatch indicators, unconfoundedness, audit sample and exchangeable linkage-error assumptions; Proposition 1 and subsequent estimators: mismatch attenuation and audit-based correction; Discussion: black-box linkage and dependence of causal validity on linkage assumptions | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:observation; r3:availability; r3:missingness; r3:measurement; r3:entity-uncertainty; r3:no-event-filter; s4:organization-algorithm; s5:observation-generation; s6:linked-histories; s61:linkage-sets

**Remaining scholarship:** Schema profiles generate finite candidates, trusted answers resolve material ambiguity, and an unsupported three-field key yields incompatibility. Automatic semantic truth is not established. Linkage audit variance and biased-audit failure are derived/executed under independent replacement; general probabilistic linkage needs a justified joint model and validation. V6 supplies decision-specific cohort influence, donor inference and calibrated linkage comparisons; see dynamic-decision-ledger.md for exact scope and unresolved generality. V6.1 connects paired linkage rank to projected financial confidence sets with explicit primitive approximation limits. Persistent/endogenous mappings and misclassified audits remain outside that construction; see linkage-decision-ledger.md.

## 14. Scientific computing and product design

What typed transformations, estimators and evidence states does the theory justify implementing?

| Source key | Inspected anchor | Current inspection status |
|---|---|---|
| id2006 | ID/IDC kernel transformations and failure witness | re_read |
| dml2018 | Scores, rank/rate and sampling requirements | re_read |
| kaelbling1998 | Belief update and planning contract | re_read |
| runtime_doubleml_scope | doubleml-0.txt lines 271--370: external nuisance predictions, clipping and ATE score; doubleml-1.txt lines 1--46: fit external_predictions contract; doubleml-metadata.txt lines 1--49: version and BSD license | primary_text_inspected_in_scope_revision |
| runtime_tigramite_scope | pcmci-operation.txt lines 28--99: sufficiency, stages and endpoint semantics; lines 187--194 output matrices; lpcmci-operation.txt lines 1--32 and 147--158: conditioning caps, graph and p/value matrices; parcorr-operation.txt: linear partial correlation and analytic significance; tigramite-metadata.txt lines 1--14 and 172--180: version and GPLv3+ declaration | primary_text_inspected_in_scope_revision |
| public401k | Stata bytes parsed: 9915 rows; net_tfa, e401, p401 and nine controls in scope-public-spec.json; no required-field row deletions; DML primary Section 6.2 cross-checks design and controls; extract has no PSU/stratum/weight fields | primary_text_inspected_in_scope_revision |

**Draft anchors:** r3:software-types; r3:software-composition; r3:operation-catalogue; r3:protocol; r3:adapter-inference; r3:inference-contract; r3:construction; r3:investment; s4:scientific-language; s4:sibling-mappings; s4:workflow-results; s5:composition; s5:dominant-workloads; s5:public-finance

**Remaining scholarship:** Seven selected installed-package records supplement, without promoting, 44 historical source/document qualifications. Static/public/history query compositions and graph-effect adapters execute; public causal truth is unknown and survey design fields absent. Eleven workloads in 22 fresh processes retain statistical dimensions, actual thread limits and numerical statuses. Distributed services, full workspaces and accepted sibling adoption remain construction work.
