# What sensitivity and IV engines must preserve

A branch-offer estimate can look attractive because a noisy pretrend has been
treated as known. A causal proposal must instead connect the substantive trend
restriction, the joint sampling uncertainty and the offer's monetary target.
HonestDiD supplies a valuable R reference for sensitivity to departures from
parallel trends, supported by Rambachan and Roth's identification and inference
arguments. The proposed reuse choice is to retain that reference and consider
an isolated R worker after qualification. It does not yet admit a native engine.
The selected repository revision declares version 0.2.8; equality to a particular
distributed release, solver behavior and transitive dependency rights remain
unqualified. A new port would add statistical and numerical parity obligations
without a demonstrated benefit \citep{rambachan2023,exec22_honestdid_engine}.

The economic distinction is concrete. In a three-period example, normalize the
untreated group difference in the reference period to zero and call its earlier
value \(x\). Let the postperiod contrast be \(y=\tau+\delta_1\), where
\(\tau\) is the target offer effect. Bounding the next untreated first difference
by a multiplier \(m\) gives effects in \([y-m|x|,y+m|x|]\). Bounding the change
in that first difference by an absolute amount \(M\) instead gives
\([y+x-M,y+x+M]\). At \(x=-2,y=4\), setting the respective tuning values to
zero gives effects 4 and 2: a flat differential trend and continuation of a
linear differential trend are different assumptions. The multiplier is
dimensionless, while the smoothness bound has outcome units on a specified
calendar \citep{rambachan2023,exec22_honestdid_reference}.

An authored known-Gaussian experiment then illustrates the value of retaining
covariance. With estimated pretrend 0, postperiod contrast 4, multiplier 1,
variances 1 and 4 and covariance 1.5, projecting a joint 95% confidence ellipse
through the relative-magnitude restriction gives approximately
\([-2.9233,10.9233]\). A stipulated offer cost of USD 1 per exposure changes
this to net bounds of approximately \([-3.9233,9.9233]\). The corresponding
stipulated population example has effect 4 and net value 3, but a confidently
positive investment conclusion does not follow from this interval. These are
reproducible mathematical examples under a declared law, not measured bank
returns or an execution of HonestDiD's optimized procedures
\citep{exec22_honestdid_reference}.

An adapter must retain more than endpoints. The inspected R paths differ in
default methods, tuning grids and forwarding of options. Selected paths reduce
accepted grid nodes to their minimum and maximum; that hull can conceal gaps or
unresolved search extent. Some inspected population-bound failure branches can
return the unadjusted target as both endpoints. These source paths are not
observed runtime failures, but they make solver status, grid membership, warnings
and the executed restriction necessary parts of the interface. Conversion from
event-study engines must preserve coefficient ordering, reference removal,
target aggregation and full covariance \citep{exec22_honestdid_engine,exec22_honestdid_bridges}.

Instrumental-variable engines require a parallel discipline. Separate full ranks
of the action design and the instrument matrix do not establish a full-rank
projected design or a valid exclusion restriction. An exact four-row witness
has projected Gram \(4\varepsilon^2\) and IV ratio
\(2+1/(100\varepsilon)\): a stipulated small direct instrument effect changes
the fitted ratio from 3 to 12 as relevance shrinks. This motivates generated
comparisons that vary instrument strength and exclusion separately. The inspected
Python paths also differ in weighting, column removal and covariance defaults;
heteroskedastic-robust covariance does not automatically address calendar
dependence \citep{exec22_pyiv_kernels_linearmodels,exec22_pyiv_kernels_pyfixest,exec22_pyiv_reference}.

Diagnostic names must preserve their actual null and reference distribution.
A selected first-stage helper can display a Wald quadratic divided by its
restriction count while returning a chi-square p-value. For quadratic 8 and
two restrictions the displayed value is 4; chi-square-two and an F distribution
with 2 and 20 degrees of freedom give p-values about 0.0183 and 0.0346. Likewise,
an inspected Anderson--Rubin overidentification property is not a coefficient-null
confidence-set inversion. The library, CLI and MCP should therefore retain the
restriction, distribution, degrees of freedom, covariance and numerical status
instead of unifying similarly named fields into a generic interval
\citep{exec22_pyiv_kernels_pyfixest,exec22_pyiv_diagnostics_linearmodels,exec22_pyiv_reference}.

The next investment is a bounded public prototype: frozen model conversions,
known-law panels, prespecified restrictions, malformed-input and solver-status
cases, and matched decision comparisons that retain failures in the denominator.
Its full cost includes fitting, covariance construction, repeated inversions,
environment support and investigation of refused results. Python regression
discontinuity and CausalPy IV still require their own primary review. These
specific remaining tasks can establish whether native integration merits a
later costly bank experiment.
