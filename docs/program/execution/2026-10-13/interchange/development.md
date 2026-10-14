## When a conversion preserves the question

The interchange obligation can be stated as a commutation requirement. Let \(F_Q(D)\) be a scientific calculation on observations \(D\) for context \(Q\). Let \(E\) encode the observations and question for an engine, \(M\) denote that engine's computation, and \(R\) decode its result. If \(T\) is a declared change of coordinates, an exact adapter should satisfy

\[
 R\{M(E(D,Q))\}=T\{F_Q(D)\}.
\]

The right side specifies what the answer means before serialization. The left side describes the proposed software path. This equality is an obligation on the admitted domain, not a theorem established by two programs returning parseable JSON. It includes a negative scientific answer or a set with several components whenever that is the defined output of \(F_Q\). A method that changes the target while improving numerical stability has changed \(Q\); it has not merely implemented \(E\).

There are three useful levels of equivalence. Exact structural equivalence preserves a graph, variable map or expression tree up to declared renaming. Numerical equivalence permits a quantified error in the requested coordinates. Scientific equivalence additionally requires the same population, intervention, sampling law and uncertainty interpretation. A fixture showing agreement of two printed means addresses only a small part of the second level. The design should state which level it establishes and where further evidence is required.

An adapter also needs an explicit domain. Write \(\mathcal D_M\) for the queries and inputs admitted by engine \(M\). If \((D,Q)\notin\mathcal D_M\), the proper response is a typed unsupported result that preserves the original request. Automatically dropping weights, selecting one graph, clipping an interval or replacing a temporal sample with independent rows does not extend the domain honestly. A proposed approximation can still be useful, but its transformed question and additional assumptions must be disclosed as a different operation.

This view explains why a generic language bridge is insufficient. A Python-to-R array conversion can preserve all floating-point values while losing the fact that columns represent treatment arms in a specific order. A Java graph object can preserve adjacency while reversing an endpoint mark. A C++ routine can accurately optimize an objective for a different weighting measure. The mathematical interface must bind these meanings alongside the numeric payload, and its review must include examples for which apparently harmless changes lead to materially different bank decisions.

## Population measures and rate coordinates

Consider a bank's effect target

\[
 \tau_\mu=\int\{m_1(x)-m_0(x)\}\,d\mu(x),
\]

where \(m_a(x)\) is a conditional mean potential outcome under action \(a\), and \(\mu\) is the declared distribution of customers or exposures. The same response functions can imply different targets under different measures. In an assumed two-segment example, the customer shares are \(3/4\) and \(1/4\), the segment effects are USD 20 and USD -40 per account, and relative balances are one and nine. The customer-average effect is

\[
 \tfrac34(20)+\tfrac14(-40)=5.
\]

Balance weighting gives masses \(1/4\) and \(3/4\), and hence an effect of USD -25. The sign reverses even though no within-segment estimate changed. The example is stipulated arithmetic, not evidence about the distribution of any bank's customers. Its purpose is to make the weighting measure an indispensable part of the requested estimand. \citep{exec13_interchange_examples}

A caller may intentionally prefer the balance-weighted target for a treasury decision. That choice should create a new target identity and explain which decision it serves. It cannot be inferred from a column named `weight`, because a supplied weight might instead describe unequal sampling probabilities, treatment assignment, transport to another population or a numerical objective. These roles have different identification and variance implications. Multiplying several weights without preserving their definitions can conceal that distinction.

Treatment coordinates require similar care. Let \(r\) be a decimal interest rate, so a basis-point change is \(10^{-4}\). If a linear response derivative is \(\beta=\partial E(Y)/\partial r\), then the derivative per basis point is \(10^{-4}\beta\). A hypothetical estimate of USD 2 million per unit decimal rate becomes USD 200 per basis point; an interval of USD 1--3 million becomes USD 100--300. Reporting the original number under the new label would create a factor-of-10,000 error. The exact calculation is reproducible. It does not assert that a constant derivative is an appropriate response model over an arbitrary offer range. \citep{exec13_interchange_examples}

For a finite nonlinear rate change, the target is instead \(E\{Y(r_1)-Y(r_0)\}\); rescaling a local derivative does not identify that contrast. Nor does a per-month response become an annual causal response by changing its unit label. Timing, compounding, feedback and the intervention path may matter. Units should therefore describe the mathematical coordinate actually estimated, while the horizon and intervention path remain separate fields. A conversion that requires new structural assumptions belongs in a scientific transformation, not a formatting function.

## Joint uncertainty across coordinates

Suppose an admitted calculation returns \(\widehat\theta\) and covariance \(\widehat\Sigma\) in the declared coordinates. Under a fixed linear map \(\phi=L\theta+c\), the corresponding estimate and covariance are

\[
 \widehat\phi=L\widehat\theta+c,
 \qquad \widehat\Sigma_\phi=L\widehat\Sigma L^\top.
\]

This covariance identity follows by expanding the centered vector \(L(\widehat\theta-E\widehat\theta)\). It preserves whatever justification the original covariance actually has; it supplies no new consistency, normal approximation or finite-sample coverage argument. If \(L\) is estimated, choosing to hold it fixed is a conditional analysis and must be labeled. Joint estimation error cannot be eliminated by storing the fitted \(L\) as a configuration value.

For an exact arithmetic illustration, let the first coordinate be a gross revenue effect in USD and the second an operating-cost effect in thousands of USD. Suppose the supplied covariance is

\[
 \Sigma=\begin{pmatrix}40000&20\\20&1/4\end{pmatrix},
 \qquad L=\begin{pmatrix}1/1000&0\\0&-1\end{pmatrix}.
\]

The new coordinates are gross benefit and negative operating cost, both in thousands of USD. Their covariance is

\[
 L\Sigma L^\top=
 \begin{pmatrix}1/25&-1/50\\-1/50&1/4\end{pmatrix}.
\]

The negative cross-covariance matters when adding the two coordinates to obtain net value: its variance is \(1/4\), whereas dropping that covariance gives \(29/100\). A column-order error or a failure to reverse the covariance sign changes the uncertainty even if both marginal standard errors look reasonable. The matrices here are assumed, positive definite reference objects whose conversion is checked by exact arithmetic. They are not fitted bank uncertainty estimates. \citep{exec13_interchange_examples}

Marginal intervals cannot substitute for a joint region. If \(C_1,C_2\) each cover their own fixed coordinate with probability at least \(.95\), the union bound gives only

\[
 P\{(\theta_1,\theta_2)\in C_1\times C_2\}\geq .90.
\]

Even with independent coverage events and exact marginal coverage, the joint probability is \(.95^2=.9025\). A simultaneous 95% statement needs a construction that supports it; a transport cannot supply that construction by changing the uncertainty label. The same issue arises if an agent inspects several analyses and reports only the most favorable one. Coverage for each fixed query is not automatically coverage for the selected query. Preserving the full query-selection rule and any simultaneous or selective argument is part of the workflow's scientific identity.

These distinctions already appear in the local semantic validator: confidence, posterior credibility and sensitivity have separate meanings, a joint-confidence declaration requires construction evidence, and the declared sampling law must match the context. Those checks constrain what can be serialized. They do not independently prove the submitted construction or establish Bayesian calibration. \citep{exec13_interchange_runtime}

## A confidence set is not a pair of convenient endpoints

Weak identification supplies a practical reason to retain topology. For a ratio target \(\theta=\mu_Y/\mu_X\), one can invert a test of \(\mu_Y-\theta\mu_X=0\). With supplied approximately Gaussian mean errors, write their variances as \(s_{YY},s_{XX}\) and covariance as \(s_{XY}\). A residual-test set takes the form

\[
 (\bar Y-\theta\bar X)^2
 \leq c^2(s_{YY}-2\theta s_{XY}+\theta^2s_{XX}).
\]

Its interpretation depends on the stated Gaussian approximation, covariance and critical value; algebraic inversion alone is not a finite-sample theorem for an arbitrary dependent sample. Collecting terms gives

\[
 a\theta^2+b\theta+d\leq0,
\]

where

\[
 a=\bar X^2-c^2s_{XX},\quad
 b=-2\bar X\bar Y+2c^2s_{XY},\quad
 d=\bar Y^2-c^2s_{YY}.
\]

When the denominator is weak, \(a\) may be negative. With two real roots the solution then consists of exterior rays; with other coefficients it may be the whole line or another topology. The point ratio can fail to exist while the test-inversion set still has a precise meaning. For the stipulated values \(\bar Y=2,\bar X=0,c=2,s_{YY}=s_{XY}=0,s_{XX}=1/4\), the inequality is \(4\leq\theta^2\), giving

\[
 (-\infty,-2]\cup[2,\infty).
\]

This degenerate but positive-semidefinite reference covariance makes the algebra transparent. It does not validate that covariance for a data-generating process. It shows why a response object must allow a valid set without a finite point ratio. The existing local supplied-moment operation retains these distinctions under its declared approximation. \citep{exec13_interchange_examples,exec13_interchange_runtime}

Unknown, empty, whole-line and disconnected results answer different questions. Unknown says that no set has been computed. Empty may signal incompatible restrictions in a particular construction, and does not mean an effect of zero. Whole-line uncertainty means every real value remains allowed by that construction. An exterior-ray set excludes a middle region despite being unbounded. A graph-class result may instead be a set of distinct functionals whose numerical evaluation is not yet available. None can be reduced to a nullable scalar without losing information that could change a decision.

Nonlinear monetary transformations make the loss visible. Take the assumed effect set \([-3,-2]\cup[2,3]\) and value map \(V(\theta)=100(\theta^2-1)\). Its image is \([300,800]\). Applying the same map to the convex hull \([-3,3]\) gives \([-100,800]\). Both are outer possibilities for different retained information, but the latter invents a negative-value possibility that the original set excludes. A hull may be a disclosed conservative approximation; it must not be described as exact interchange. The reverse mistake, returning only transformed outer endpoints without considering interior extrema, can omit valid values and lose coverage. \citep{exec13_interchange_examples}

## Combining statistical, measurement and numerical uncertainty

Suppose an effect set \(C\) contains the fixed target \(\theta\) with probability at least \(1-\alpha_C\), and a set \(H\) contains a needed valuation parameter \(\eta\) with probability at least \(1-\alpha_H\). For a declared value function \(v\), the projection

\[
 W=\{v(t,h):t\in C,h\in H\}
\]

contains \(v(\theta,\eta)\) whenever both input events hold. Thus the union bound yields coverage at least \(1-\alpha_C-\alpha_H\), without independence. A valid joint region can be projected instead and may be narrower because it retains dependence between \(\theta\) and \(\eta\). Independently varying marginal ranges is generally an outer approximation to that joint region. Fixing \(\eta\) at an estimate has no such unconditional guarantee without an additional argument.

Numerical containment is a third obligation. Let \(\widetilde W\) be an approximate computed set. If a certificate establishes

\[
 W\subseteq\widetilde W\oplus[-\varepsilon,\varepsilon],
\]

where \(\oplus\) denotes addition of sets, then the enlarged computed set preserves the preceding coverage event. If the numerical certificate itself can fail with probability \(\delta\), the resulting guarantee is at least \(1-\alpha_C-\alpha_H-\delta\). Budgets of \(.02,.02,.01\) give a 95% lower guarantee. This arithmetic does not prove that a particular optimizer supplies the assumed certificate; its error bound must come from the numerical method. \citep{exec13_interchange_examples}

A grid of feasible points usually supplies an inner sample, not the required outer enclosure. Missing a disconnected component or an unbounded tail is therefore a scientific failure, even if all sampled points satisfy the constraints. An optimizer's small objective change also need not certify the set boundary. For a nonlinear map, a Lipschitz constant can propagate an input approximation error only over a region where the constant is valid; a bound obtained on a clipped plotting window does not control unbounded tails outside it.

The currency of the numerical error should be the currency of the decision. If a statistical lower value is USD 30 but an admitted numerical approximation has error up to USD 40, the certified lower value is USD -10. Reporting only the statistical endpoint can reverse a claimed robust recommendation. Conversely, a deliberately coarse computation may be adequate when its certified error cannot change the decision. This makes numerical precision an explicit investment tradeoff rather than an unexamined default tolerance.

## Sampling declarations and partial scientific answers

A shared data format does not create shared sampling assumptions. Consider the generated one-date account model \(Y_i=\theta+C+E_i\), where independent centered Gaussian components have \(\operatorname{Var}(C)=.09\), \(\operatorname{Var}(E_i)=1\), and \(C\) is shared by every account. Then

\[
 \operatorname{Var}(\bar Y)=.09+1/N.
\]

At \(N=10{,}000\), the correct variance is \(.0901\). Treating the rows as independent with their individual variance \(1.09\) gives \(.000109\), understating variance by \(90100/109\), or about 827 times. The number of rows was preserved exactly; the scientific information was not. This exact generated calculation illustrates why a panel or calendar declaration must survive conversion and why an iid-only method must reject it. It makes no claim about an observed bank covariance. \citep{exec13_interchange_examples}

The same problem occurs with persistent linkage errors, cluster treatment assignment and policies that condition on shared history. A consumer that sees only row count and a floating-point estimate cannot reconstruct the lost sampling unit. The local bounded back-door reference explicitly restricts its sampling regime, while the proposed symbolic identification adapter preserves the declaration without supplying estimation uncertainty. Those are different services with different obligations. \citep{exec13_interchange_runtime,exec13_y0_contract}

Finally, the response should identify what has actually been established. A source-inspected method may support a proposal decision. An executed adapter may establish that particular conversions work. A statistical region may be valid under declared scientific assumptions. A banking action may still be undecided because its loss function or information is insufficient. Preserving a partial answer makes the next step precise: obtain a needed assumption, improve information, choose another method or refine numerical containment. Automatically converting every partial answer into a confident recommendation would obscure the very gap the product is meant to explain.
