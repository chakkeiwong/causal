#!/usr/bin/env python3
"""Connected Java panel comparison; source inspection is not native qualification."""
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-25/panels-java-v1'
TEXT=r'''
\section{Java regression components and the missing panel contract}
\label{sec:exec25-panels-java}
A bank standardizing its services on Java still needs to decide which causal
panel problem each numerical component solves. A branch identifier, a time
column and an ordinary regression interface do not specify a staggered-policy
estimand. We compare two dated Java regression implementations, Haifeng Li's
Statistical Machine Intelligence and Learning Engine (Smile) and Apache
Commons Math, with the distinct econometrics-oriented iMetrica candidate.
Smile here is not BayesFusion's SMILE Bayesian-network engine. The selected
source commits precede the research cutoff; they are source profiles, not
claims that a current binary release or a bank deployment has been tested.
\citep{exec25_paneljava_smile,exec25_paneljava_commons,exec25_paneljava_imetrica}

\subsection{Useful numerical machinery, different scientific obligations}
The selected Smile source declares version 6.3.0. Its ordinary least-squares
path expands a formula into a design matrix and rejects a system with no more
rows than columns. It selects QR or singular-value decomposition (SVD), and
the QR path catches a runtime exception before attempting SVD. If standard
errors or recursive updating are requested, the subsequent path still constructs
an inverse through a Cholesky route. Thus an SVD coefficient fallback should
not be advertised as proof that every rank-deficient uncertainty calculation
will succeed. This is a source-path qualification question, not an observed
execution failure. The reported coefficient standard error is the residual
scale times the square root of a diagonal inverse-Gram entry. The linear-model
constructor calculates the residual scale using residual sum of squares divided
by $n-p$. The inspected path does not consume cluster identifiers or calculate
a cluster sandwich.\citep{exec25_paneljava_smile}

The Apache profile is a 4.0-SNAPSHOT source tree, not a stable 4.0 release
claim. Its legacy-module descriptor explicitly describes code that is unsupported
or not yet modularized. The inspected OLS implementation solves by QR, with
an intercept included by default. Its public parameter-variance method returns
the inverse Gram matrix; the standard-error method separately multiplies its
diagonal by the estimated residual variance before taking square roots. This
distinction matters to an adapter that expects a fully scaled covariance matrix.
Selected upstream tests cover numerical examples and residual or standard-error
comparisons, but their presence is not a locally observed test pass.
\citep{exec25_paneljava_commons}

For full-rank design matrix $X$, the conventional formulas can be expressed
as $B=(X^\mathsf{T}X)^{-1}$ and $\widehat V=\widehat\sigma^2 B$, with
$\widehat\sigma^2=\mathrm{RSS}/(n-p)$. In an authored one-parameter
example, $X^\mathsf{T}X=2$ and $\widehat\sigma^2=9$ give $B=1/2$ and
$\widehat V=9/2$. Treating the unscaled return as covariance loses a factor
of nine. Conversely, multiplying an already scaled matrix again is also wrong.
The integration contract must specify the returned object's scale, residual
degrees of freedom, intercept convention and rank handling, and test them
against an independent oracle. Matching method names is insufficient.
\citep{exec25_paneljava_reference}

The inspected iMetrica README describes interactive multivariate time-series
modeling, real-time filtering and signal extraction, with computational
libraries written in Fortran or C and a Java interface. It lists native
dependencies and a Linux-oriented build. This makes it relevant to an
econometrics survey, but the inspected README and root license do not
establish a staggered-adoption or cluster-inference implementation. We defer
it as a panel delegate while retaining its stated time-series role. This is
a bounded scope decision, not an ecosystem-wide claim that Java has no
panel-data software.\citep{exec25_paneljava_imetrica}

\subsection{An exact staggered-policy counterexample}
Let $D_{gt}$ indicate an absorbing branch policy for group $g$ and period $t$.
Consider two equally weighted groups over three periods, with treatment rows
$(0,1,1)$ and $(0,0,1)$. Stipulate untreated outcomes of zero, and positive
treatment effects producing observed outcomes $(0,1,10)$ and $(0,0,1)$.
These are exact constructed outcomes, not bank observations. The equal-weight
average across the three treated cells is $(1+10+1)/3=4$.
\citep{exec25_paneljava_reference}

Now fit a constant treatment coefficient with group and period effects. In
this balanced example, subtracting row and column means and adding the grand
mean gives the residualized treatment
\[
\widetilde D=
\begin{pmatrix}-1/6&1/3&-1/6\\1/6&-1/3&1/6\end{pmatrix},
\qquad \sum_{g,t}\widetilde D_{gt}^2=1/3.
\]
The treatment coefficient is $\sum\widetilde D_{gt}Y_{gt}/
\sum\widetilde D_{gt}^2$. The three treated-cell contributions have weights
$1,-1/2,1/2$, so the coefficient equals
$1-10/2+1/2=-7/2$. Every stipulated treatment effect is positive, but the
constant-coefficient regression is negative. The numerical regression can
solve the supplied least-squares problem exactly while answering a different
question from the average treated-cell effect. No defect in QR or SVD is
required for this discrepancy.\citep{exec25_paneljava_reference}

At the last period, both groups are treated. There is no untreated comparison
group in these observed cells. Our construction knows the untreated outcomes
because it stipulated them; an analyst of ordinary observational data would
need assumptions or additional controls to know them. The public test should
therefore check the declared target, supported comparisons and unsupported
horizons, rather than insist that every package returns the oracle value 4.
It should retain cohort and event-time heterogeneity, anticipation windows,
treatment reversals and the control rule as explicit input contracts.
A routine designed for absorbing treatment must refuse or separately model
a reversed policy path; an ordinary design matrix does not decide that rule.
\citep{exec25_paneljava_reference}

\subsection{Sampling dependence and unidentified trends}
Suppose four observed rows consist of two copies from each of two independent
groups, with each group's shock independently equal to $-1$ or $1$ with
probability one half. The mean is $(Z_1+Z_2)/2$ and has variance $1/2$.
Four independent row shocks instead give variance $1/4$. Enumerating the
four group-shock assignments and sixteen independent-row assignments verifies
the distinction exactly. The example concerns two different known sampling
laws; it is not an empirical coverage estimate or an endorsement of a
two-cluster asymptotic confidence interval. A worker must preserve cluster
identity and the justified sampling law, and disclose when too few independent
units prevent its proposed uncertainty procedure.
\citep{exec25_paneljava_reference}

Under an explicitly justified independent-cluster asymptotic regime, a proposed
uncorrected sandwich would use $B[\sum_g X_g^\mathsf{T}\widehat u_g
\widehat u_g^\mathsf{T}X_g]B$, where $X_g$ and $\widehat u_g$ collect
group $g$'s rows. This is a different object from $\widehat\sigma^2B$.
Implementing that expression would still leave finite-cluster correction,
degrees of freedom, resampling, high-dimensional effects and the scientific
sampling assumptions to justify. Neither inspected OLS path establishes
those panel guarantees merely by returning coefficient tests.
\citep{exec25_paneljava_reference,exec25_paneljava_smile,exec25_paneljava_commons}

There is a separate identification limit that better covariance code cannot
repair. Suppose a treated branch's outcome moves from 10 to 15 while a control
branch moves from 10 to 12. The observed difference in differences is 3.
One compatible world has untreated treated-branch outcome 12 and effect 3;
another has untreated outcome 15 and effect 0. Both produce the same four
observed cells. A parallel-trends restriction or additional evidence is needed
to distinguish them. More accurate optimization, an agent-generated narrative
or a small standard error cannot supply the missing counterfactual information.
\citep{exec25_paneljava_reference}

\subsection{Reuse, rights and the public prototype route}
For a Java service, our proposed architecture first separates an estimand
contract from numerical execution. A narrow Java numerical delegate could
serve a justified regression subproblem, while a separately reviewed R or
Python panel worker retains its own group-time, control and uncertainty
semantics. The earlier differences and csdid inspections provide concrete
comparison routes, with their own unresolved normalization, dependency and
failure concerns. Delegation must preserve row IDs, panel keys, treatment
history, weights, missingness, cohort/time support and the exact returned
uncertainty type. A cross-language call is not evidence of statistical parity.
\citep{exec24_panelpy_differences,exec24_panelpy_csdid,exec25_paneljava_reference}

The selected Smile build declares Java 25 with preview features, and its
root notice distinguishes core-library GPLv3/commercial terms from separate
server and studio terms. These are inspected declarations, not a legal
clearance or a quoted commercial price. Apache's selected tree declares
Apache-2.0 material and third-party notices, a Java 8 compilation target
and multiple component dependencies. iMetrica includes root GPLv3 text and
native library requirements. A final choice needs the exact distribution,
transitive dependencies, intended deployment, rights review, maintenance
commitments and measured full costs. We do not transfer one module's terms
to another or infer a supported runtime from a build file alone.
\citep{exec25_paneljava_smile,exec25_paneljava_commons,exec25_paneljava_imetrica}

The immediate proposal decision is to retain Smile and Commons Math as
numerical references, and to defer direct panel admission and whole-library
porting. The public qualification route is concrete: freeze a source and
runtime profile; compare coefficients, covariance scaling, intercept and
rank-failure behavior on known linear problems; then test the declared causal
panel target on staggered, reversed, anticipated, unbalanced and dependent
fixtures with known intervention answers or required refusals. Test data
conversion and every error path, including missing groups and unsupported
post-treatment horizons. Keep numerical parity, scientific correctness and
operating acceptance as separate reported outcomes.
\citep{exec25_paneljava_reference}

Complete costs also need distinct denominators. An illustrative USD 2,400
experiment costs USD 24 per submitted case for 100 submissions, or USD 40
per scientifically usable case if only 60 qualify. Neither ratio is a
measured price or an ROI result. Report engineering, expert adjudication,
dependency and entitlement work, failed attempts and runtime in the numerator.
The bounded repository search and selected source paths leave further Java
and JVM panel, synthetic-control and bridge candidates to inspect. This
comparison narrows the implementation route while preserving the remaining
coverage and causal-identification obligations.\citep{exec25_paneljava_reference}
'''
SPONSOR='''## A Java interface must preserve the panel estimand

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
'''

def main():
    for name,text in [('development.tex',TEXT),('sponsor-addition.md',SPONSOR)]:
        p=BASE/name;assert not p.exists();p.write_text(text)
    print('Prepared connected panel argument and sponsor comparison.')

if __name__=='__main__':main()
