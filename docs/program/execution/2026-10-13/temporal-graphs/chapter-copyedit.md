\chapter{Continuous temporal uncertainty and an informative intervention}
\label{exec13:temporal-region}

## The banking question and the observation law

A bank can observe a stable association between an offer and a subsequent outcome yet remain unable to price the effect of changing the offer. The missing information can persist even with an exactly known observational distribution. This chapter develops a restricted temporal confidence construction and shows what an additional direct intervention would contribute. The mathematical construction and exact calculations are project derivations, not a fitted bank result. \cite{exec13_temporal_argument,exec13_temporal_exact}

In the preserved temporal graph study, all valid cells covered and retained their declared
true graph in 512 of 512 requests. Weak relevance and unrestricted latent
observation each produced 512 whole-line sets. The persistent cell produced
507 finite sets and five whole-line sets. Under false exclusion, the true
graph was retained zero times despite numerical effect coverage. These findings distinguish numerical coverage from informative effects and from a valid causal restriction. \cite{exec13_temporal_predecessor}

Let \(X_t=(Z_t,A_t,Y_t)'\) satisfy
\[
 X_t=\rho X_{t-1}+\varepsilon_t,\quad
 \varepsilon_t\mathrel{\mathop\sim^{\rm iid}}N_3(0,\Sigma),\quad
 \Sigma\succ0,\quad \rho\in I\subset(-1,1).
\]
Here \(I\) is a declared closed interval, not an estimated selected lag.
Initial observations have the invariant distribution
\(N_3(0,\Sigma/(1-\rho^2))\), independently of future innovations. We observe
\(X_0,\ldots,X_n\), with \(n\ge2\). The scalar lag common to all coordinates
and the Gaussian independent innovations are substantive restrictions. A
general lag matrix, unknown lag order, nonstationarity, hidden temporal state,
selection and measurement errors are outside this law.

A structural innovation model is
\[
 \varepsilon_Z=E_Z,\qquad
 \varepsilon_A=k\varepsilon_Z+U,\qquad
 \varepsilon_Y=\tau\varepsilon_A+c\varepsilon_Z+V,
\]
where \(E_Z\) is independent of the jointly Gaussian pair \((U,V)\). Dependence
between \(U\) and \(V\) represents latent action/outcome confounding.
The target \(\tau\) is the contemporaneous response to changing \(A_t\)
while holding the past fixed. In observed-coordinate structural equations,
the lag matrix is \(\rho(I-B)\), where \(B\) contains the contemporaneous
coefficients. It is not permissible to change that lag matrix to
\(\rho I\) in the structural equations and claim the same target/law.

The declared graph family may include the exclusion model \(c=0\) and a
broad latent model with unrestricted \(c\). In the former,
\(\Sigma_{ZY}=\tau\Sigma_{ZA}\). In the latter that equality need not hold.
An exclusion is a scientific restriction, not a conclusion from fitting a
favorable covariance. The construction below accommodates a finite declared
family through a union over graph/parameter pairs; it does not claim an
exhaustive search over unrestricted causal structures.

## A feasible region with continuous unknown lag

For every candidate \(r\in I\), form residuals
\(E_t(r)=X_t-rX_{t-1}\). Use the nine fixed directions
\[
 \mathcal V=\{e_1,e_2,e_3,e_1+e_2,e_1-e_2,
 e_1+e_3,e_1-e_3,e_2+e_3,e_2-e_3\},\quad K=9.
\]
For each direction, let \(S_v(r)\) be the ordinary sample variance of
\(v'E_t(r)\), with divisor \(\nu=n-1\). At the true lag only,
\(\nu S_v(\rho)/(v'\Sigma v)\) is the sum of squares of \(\nu\) independent
standard normal variables. To see this, scale the vector of independent
normal residuals by its population standard deviation and apply an
orthogonal matrix whose first row is the normalized all-ones vector. The
remaining \(\nu\) coordinates are independent standard normals, and their
squared norm is the centered sum of squares. Consequently
\[
 E[S_v(\rho)]=v'\Sigma v,\qquad
 \operatorname{Var}(S_v(\rho))=2(v'\Sigma v)^2/\nu.
\]
For a declared rational tolerance \(0<t<1\), Markov's inequality applied to
the squared relative error gives
\[
 P\{|S_v(\rho)/(v'\Sigma v)-1|>t\}\le\frac{2}{\nu t^2}.
\]
If \(2K/(\nu t^2)\le\alpha_O\), the union bound supplies simultaneous
coverage at least \(1-\alpha_O\) for
\[
 L_v(r)=\frac{S_v(r)}{1+t}\le v'\Sigma v
 \le \frac{S_v(r)}{1-t}=U_v(r),\qquad v\in\mathcal V,
\]
evaluated at \(r=\rho\). Dependence between the nine directions is harmless
for this bound. Residuals at an incorrect lag need not be independent.

Define \(\mathcal C_O\) to contain every tuple \((r,G,\lambda,\Sigma)\) for
which \(r\in I\), \(G\) is in the declared family, its parameters \(\lambda\)
generate \(\Sigma\succ0\) under the stated innovation law, and all nine
inequalities hold. All nuisance coefficients and the continuous lag remain
in the region. Let
\[
 \mathcal S_O=\{\tau(G,\lambda):(r,G,\lambda,\Sigma)\in\mathcal C_O\}.
\]
On simultaneous variance inclusion, the true tuple belongs to
\(\mathcal C_O\); hence its effect belongs to \(\mathcal S_O\). Thus
\(P(\tau_0\in\mathcal S_O)\ge1-\alpha_O\), provided the declared family
contains the true structural model. No multiple-testing penalty over the
continuum of candidate lags is required: this proof uses a single coverage
event at the fixed true lag, and the union includes that lag. It does not
declare every wrong-lag confidence calculation valid or justify discarding
the true lag by a separate selector.

The construction is deliberately conservative. With \(t=1/4\), \(K=9\)
and \(\alpha_O=.02\), it needs \(\nu\ge14{,}400\). The predecessor used
240 transitions; this particular finite bound cannot give it the displayed
two-sided relative band. At smaller sample size this profile returns the
whole line and a bound-insufficient disposition, rather than inserting an
invalid finite interval. The exact chi-square pivot above offers a sharper
candidate using suitably certified quantiles, but its numerical implementation
would need separate validation. No improvement in cost or useful width is
claimed from replacing a lag grid with this conservative continuum argument.

## Numerical outer bounds that cannot lose a lag or a component

Let \(u_t=v'X_t\) and \(w_t=v'X_{t-1}\). Center each series over the same
\(n\) transitions. Direct expansion gives
\[
 \begin{aligned}
 S_v(r)&=a_vr^2+b_vr+d_v,\\
 a_v&=\nu^{-1}\sum_t(w_t-\bar w)^2,\\
 b_v&=-2\nu^{-1}\sum_t(u_t-\bar u)(w_t-\bar w),\\
 d_v&=\nu^{-1}\sum_t(u_t-\bar u)^2.
 \end{aligned}
\]
For a closed lag cell \(J=[r_L,r_U]\), its maximum is at an endpoint because
\(a_v\ge0\); its minimum is at an endpoint or at \(-b_v/(2a_v)\) if that
vertex lies in the cell. The constant case is handled separately. Rational
coefficients and cell endpoints therefore give exact bounds
\([s^-_v(J),s^+_v(J)]\). A finite partition covering all of \(I\), with
shared endpoints retained, is a continuum enclosure, not an evaluation grid.
Refining cells can reduce excess width; stopping early preserves validity.

For exact supplied numbers, a conservative directional variance interval
over the cell is
\([s^-_v/(1+t),s^+_v/(1-t)]\). Polarization gives an entrywise covariance
box. For \(i\ne j\), use
\[
 \Sigma_{ij}\in\frac14
 [L_{e_i+e_j}(J)-U_{e_i-e_j}(J),
  U_{e_i+e_j}(J)-L_{e_i-e_j}(J)].
\]
Dropping positive-definiteness and shared-parameter consistency enlarges this
box. It can make results much wider, but cannot remove the true covariance.
Positive-definiteness or graph constraints may narrow a later implementation
only through certified feasibility exclusion, not by failure of an optimizer.

Exact arithmetic on decimal data alone does not enclose unknown rounding.
Suppose every coordinate of the ideal input is enclosed within absolute
error \(\eta\) of the supplied value, and let
\(h=\|v\|_1\eta(1+\max_{r\in J}|r|)\). Residual error is at most \(h\)
and its centered error at most \(2h\). Cauchy--Schwarz then bounds the change
in sample variance by
\[
 B_v(J)=4h\sqrt{n/\nu}\sqrt{s^+_v(J)}+4nh^2/\nu.
\]
Use rational upward bounds for the square roots and replace the variance
enclosure by \([\max(0,s^-_v-B_v),s^+_v+B_v]\) before dividing by
\(1\pm t\). This is an input-conversion certificate conditional on a valid
input enclosure. Undocumented measurement error, noisy proxies or incorrect
entity matches are changes to the observation law, not floating-point errors
that this formula repairs.

In an exclusion cell, write the resulting intervals as \(N_J\) for
\(\Sigma_{ZY}\) and \(D_J\) for \(\Sigma_{ZA}\). Retain the full set
\[
 \mathcal T_J=\{\theta:\exists (N,D)\in N_J\times D_J,
                      \ N-\theta D=0\}.
\]
When \(0\notin D_J\), its endpoints are the extreme corner ratios.
When the denominator straddles zero and the numerator excludes zero,
two rays can result. For \(N_J=[1,2]\) and \(D_J=[-1,1]\), the set is
\(( -\infty,-1]\cup[1,\infty)\). When both intervals include zero, their
rectangle contains \((0,0)\), so every \(\theta\) is feasible. When
\(D_J=\{0\}\) and \(0\notin N_J\), the moment set is empty. That is a
constraint inconsistency, not evidence for a zero effect.

Union these components over every lag cell and every retained graph. The
broad latent graph below contributes the whole line whenever its observational
law is admitted. Keep disconnected components unless they overlap; never
replace a pair of rays by a finite interval. The exact reference checks ratio
sets against the independent criterion that \(N_J\) intersects
\(\theta D_J\), including zero denominators and exact endpoints. Bounds
include every continuous lag by the quadratic proof; sampled checks alone
are not the certificate. The reference is not a general graph feasibility
solver and supplies no bank-data result.

## An equal-law witness and what an exclusion actually buys

Let \(Z,U,E\) be independent standard Gaussian innovations and set
\[
 \varepsilon_Z=Z,\quad \varepsilon_A=Z+U,\quad
 \varepsilon_Y=\tau\varepsilon_A+(2-\tau)Z+(1-\tau)U+E.
\]
For every real \(\tau\), the observed innovation is exactly
\((Z,Z+U,2Z+U+E)'\), with covariance
\[
 \Sigma=\begin{pmatrix}1&1&2\\1&2&3\\2&3&6\end{pmatrix},
 \qquad\det\Sigma=1.
\]
The confounded disturbance has variance \(1+(1-\tau)^2\) and covariance
\(1-\tau\) with \(U\); its conditional noise variance is always one.
Every world is a coherent positive-definite Gaussian law. Attaching the same
scalar lag and invariant initialization makes the entire observed temporal
law identical for every \(\tau\), while a contemporaneous intervention on
\(A\) changes \(Y\) at slope \(\tau\). The equality is algebraic for all
real effects, not merely an equality across the finite checked examples.

The restriction \(c=0\) reduces this family to \(\tau=2\); strong observed
relevance \(\Sigma_{ZA}=1\) then gives the familiar ratio. But relevance
alone does not establish exclusion: all other worlds have the same strong
observed correlation with \(Z\). Merely observing more of this law, using a
different discovery optimizer or asking an LLM to orient an edge cannot
choose among these effects. No theorem here rules out all additional
measurements; it states exactly what the declared observational law omits.

At zero relevance, even exclusion can leave every effect feasible. Take
\(\varepsilon_A=U\) and
\(\varepsilon_Y=\tau\varepsilon_A+(1-\tau)U+E=U+E\), with \(Z\)
independent. Now \(c=0\), \(\Sigma_{ZA}=\Sigma_{ZY}=0\), and the effect
is still arbitrary. A weak-instrument ratio that quietly deletes zero cannot
solve this information problem.

## A direct intervention that separates effects without identifying every edge

Consider independent experimental episodes at a common fixed pre-action
history. Replace the action equation by
\(A=a_0+\delta R\), where \(\delta>0\) is known and \(R\in\{-1,1\}\)
is assigned with \(m\) episodes per arm independently of innovation roots.
Keep the other structural equations unchanged. Under the restricted linear
Gaussian model and an invariant \(\tau\), the outcome has the form
\[
 Y=\mu+\tau\delta R+\xi,\quad
 \xi\mathrel{\mathop\sim^{\rm iid}}N(0,\sigma_I^2),\qquad \sigma_I^2>0.
\]
The unknown \(\mu\) absorbs the fixed history and baseline action; the
unknown variance absorbs the remaining contemporaneous causes. The episodes
must be independent; taking adjacent dates from one continuing customer
trajectory does not satisfy this experiment. Identical variance in the two
arms and a common transported effect are additional model assumptions.

Let \(\widehat\tau_I=(\bar Y_+-\bar Y_-)/(2\delta)\), and let \(S_p^2\)
be the usual pooled within-arm variance with \(\nu_I=2m-2\) degrees of
freedom. Orthogonal Gaussian projections within each arm make its sample
mean independent of its centered residuals. Hence
\[
 T=\frac{\widehat\tau_I-\tau}{S_p/(\delta\sqrt{2m})}
   =\frac{Z_0}{\sqrt{Q/\nu_I}},\qquad
 Z_0\sim N(0,1),\quad Q\sim\chi^2_{\nu_I},\quad Z_0\perp Q.
\]
For \(m>2\), integrating the chi-square density gives
\(E[Q^{-1}]=1/(\nu_I-2)\), so \(E[T^2]=\nu_I/(\nu_I-2)\).
Choose any rational \(b^2\ge\nu_I/((\nu_I-2)\alpha_I)\).
Markov's inequality proves finite coverage at least \(1-\alpha_I\) for
\[
 \mathcal S_I=\left[\widehat\tau_I-
  \sqrt{\frac{b^2S_p^2}{2m\delta^2}},\quad
  \widehat\tau_I+\sqrt{\frac{b^2S_p^2}{2m\delta^2}}\right].
\]
This conservative alternative avoids unverified numerical tail quantiles.
A sharper Student pivot interval is possible with certified quantiles.
Nonpositive pooled variance or insufficient degrees of freedom produces a
refusal/whole-line result under the declared algorithm, never zero-width
certainty. A nonnormal outcome model needs another uncertainty argument.
If input numbers are enclosed rather than exact, enclose the arm means and
pooled variance as well before projecting these endpoints.

Under a common effect parameter, report
\(\mathcal S=\mathcal S_O\cap\mathcal S_I\). The two component coverage
events need not be independent: the union bound gives at least
\(1-\alpha_O-\alpha_I\). Using outer numerical supersets preserves this
inclusion proof. An empty intersection is a retained inconsistency/failure
event, not an invitation to change the error budget or delete a graph after
seeing the result. If no observational restriction is defensible, use
\(\mathcal S_I\) alone under its own experiment and target assumptions.

In the equal-law family, intervention changes the arm mean difference to
\(2\delta\tau\). Distinct effects are now distinguishable, although
several graphs can remain compatible. Identifying the decision-relevant
effect does not require identifying every edge. Randomizing a variable that
merely encourages the action is a different experiment: exclusion,
compliance and relevance then need their own argument.

## Precision, costs and the exact remaining scope

For a binary offer, take \(a_0=\delta=1/2\). A planning illustration with
\(m=200\) per arm, \(\alpha_I=.03\), a reported effect of twenty dollars
and \(S_p^2=100\) dollars squared gives
\(b^2=9950/297\) and half-width
\(\sqrt{9950/297}\), approximately 5.788 dollars. The exact reference
uses a rational upward square-root enclosure. These are supplied planning
summaries, not observations from a completed trial.

For 3,000 eligible customers and fifteen dollars incremental implementation
cost per offer, the point scenario has fifteen thousand dollars net benefit.
Its conservative interval still includes a small loss. Scaling an effect by
population does not remove uncertainty, and changing the intervention or
customer population may invalidate transport. A genuine next-experiment
proposal should ask whether resolving this decision is worth the experiment's
cost, compare a cheaper operational alternative, and include delayed outcomes,
noncompliance and treatment costs in the estimand. No measured bank ROI is
inferred from this illustration.

What is resolved is the mathematical route for one continuous scalar-lag
Gaussian family, a certified enclosure strategy, exact information
counterexamples and a separating intervention with an explicit finite bound.
What remains is a resource-profiled implementation and prospectively registered
study, tighter useful uncertainty, justified input and model assumptions,
actual interventions/measurements if the proposal advances, and the general
unknown-lag-matrix/latent-state/non-Gaussian/heterogeneous-effect problem.
This argument establishes no general temporal-graph capability, bank validation or independent acceptance. The computational and information routes are
concrete enough to design the next bounded public/generated experiment.

\label{exec13:temporal-region-end}
