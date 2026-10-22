## Instruments and credit thresholds require different decision targets

The R comparison now distinguishes six pinned packages: AER and ivreg for
separate regression interfaces; ivmodel for model-specific weak-instrument and
sensitivity procedures; rdrobust for continuity-based threshold inference;
rddensity for density diagnostics; and rdlocrand for local randomization.
The selected rdrobust version is 4.0.0: the 4.1.1 CRAN publication timestamp falls
after the exact client cutoff despite its 7 October package date.
\citep{exec22_riv_aer,exec22_riv_ivreg,exec22_riv_ivmodel,exec22_riv_rdrobust,exec22_riv_rddensity,exec22_riv_rdlocrand}

An exact hypothetical credit example gives a USD 150 loss reduction among
compliers and USD 70 across the full population. With a USD 100 treatment cost,
these imply margins of USD 50 and USD -30 respectively. A separate encouragement
policy has margin USD 10 after incremental take-up and encouragement costs.
The complier effect cannot be substituted for the effect of treating everyone.
Another exact example shows that two continuous loss models agree at all observed
integer scores while implying threshold effects of USD -20 and zero. A declared
slope bound yields a net-margin set of USD -10 to USD 30 rather than a uniformly
profitable action. These are authored laws, not measured bank returns.
\citep{exec22_riv_reference}

The proposed interfaces must preserve disconnected and unbounded confidence
sets, distinguish an empty finite search grid from a globally empty set, and
separate density diagnostics from evidence for the causal design. Inspection of
ivmodel's pinned CLR source found numerical-error branches that substitute zero;
native integration needs an explicit way to detect or repair those paths before
treating their outputs as valid inference. The five reuse dispositions are
reference-only; no R adapter or package benchmark has been executed.
\citep{exec22_riv_ivmodel,exec22_riv_reference}

Original R workers are preferred candidates for a bounded prototype because
porting adds numerical and maintenance obligations. The actual distribution
still needs dependency and rights review: inspected package-level license texts,
including ivmodel's MIT alternative, do not clear every dependency or packaging
choice. Public/generated conformance cases and prospectively specified calibration
studies can address these questions before a costly bank experiment.
\citep{exec22_riv_gpl2,exec22_riv_gpl3,exec22_riv_ivmodel}

