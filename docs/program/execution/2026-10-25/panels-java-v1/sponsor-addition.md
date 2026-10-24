## A Java interface must preserve the panel estimand

The Java review inspects dated Smile and Apache Commons Math regression
paths, plus iMetrica's stated time-series scope. The first two offer useful
numerical components, but the inspected ordinary least-squares paths do not
establish staggered-treatment targets or cluster uncertainty. Apache's inspected
parameter-variance interface returns an unscaled inverse Gram matrix, while
its standard-error method separately applies residual variance. The adapter
must preserve this distinction. [@exec25_paneljava_smile; @exec25_paneljava_commons; @exec25_paneljava_imetrica]

An exact constructed two-group, three-period example has positive treatment
effects averaging 4 across treated cells but a two-way-effects coefficient of
-3.5. The discrepancy comes from the regression target's weights, not a
failed numerical solver. A second example gives variance 1/2 for two repeated
cluster shocks versus 1/4 for four independent rows. Public tests must check
the estimand, sampling law and unsupported horizons separately from numeric
agreement. Unknown counterfactual trends require additional assumptions or
information. [@exec25_paneljava_reference]

The proposed route is a narrow numerical delegate or a typed bridge to a
separately reviewed panel worker, preserving treatment history, control rules,
identities, weights and uncertainty. The selected Smile profile declares
Java 25 and core GPLv3/commercial terms; Apache is an inspected development
snapshot with legacy and dependency qualifications; iMetrica includes native
components. These declarations do not grant distribution rights, establish
support or quote prices. Direct panel admission and broad porting remain
deferred pending a qualified public profile. [@exec25_paneljava_smile; @exec25_paneljava_commons; @exec25_paneljava_imetrica]

An illustrative USD 2,400 total costs USD 24 across 100 submitted cases but
USD 40 across 60 usable results. Full costs and failures must accompany any
investment comparison. Bounded searches leave the wider Java and JVM panel
survey open. [@exec25_paneljava_reference]
