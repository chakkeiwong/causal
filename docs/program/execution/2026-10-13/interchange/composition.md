## Numerical equivalence must survive composition

Even an adapter that preserves the exact mathematical expression can fail when independently acceptable numerical errors accumulate through a workflow. Conditional identification provides a concrete example. Suppose a returned functional is \(f=N/D\), with a strictly positive denominator, and a downstream evaluator computes \(\widetilde N,\widetilde D\). Assume certificates give

\[
 |N-\widetilde N|\leq\varepsilon_N,\qquad
 |D-\widetilde D|\leq\varepsilon_D,
 \qquad |N|\leq B,\quad D\geq d_0>\varepsilon_D.
\]

By writing the difference over a common denominator and using
\(|\widetilde D|\geq d_0-\varepsilon_D\), one obtains

\[
 \left|\frac{\widetilde N}{\widetilde D}-\frac ND\right|
 \leq\frac{\varepsilon_N}{d_0-\varepsilon_D}
 +\frac{B\varepsilon_D}{d_0(d_0-\varepsilon_D)}.
\]

Thus an absolute tolerance on probability calculations has no fixed interpretation for the conditional answer as the denominator approaches zero. The mathematical statement that a conditional probability exists at a positive coordinate is weaker than a uniform numerical stability claim. A service that promises a useful numeric answer needs either an adequate support margin or a certified set that reflects the weak denominator.

For a reproducible assumed example, let \(\widetilde N=.004\), \(\widetilde D=.010\), with bounds \(\varepsilon_N=.001\) and \(\varepsilon_D=.004\). Independent interval division gives

\[
 \frac ND\in\left[\frac{.003}{.014},\frac{.005}{.006}\right]
 =\left[\frac3{14},\frac56\right],
\]

while the point ratio is \(.4\). All numerator/denominator corners here obey \(0\leq N\leq D\), so intersecting with the probability range does not narrow the interval. A valid dependence relation between their errors might narrow it, but it must be supplied and retained as joint information. The broad result is produced by bounded deterministic error alone; it is not a statistical confidence interval. \citep{exec13_interchange_composition}

If an uncertainty region includes \(D=0\), the service should preserve the unresolved support condition. Clipping the denominator to a positive constant silently changes the functional and generally supplies no error certificate. If only strictly positive but arbitrarily small denominators are allowed, a ratio may be highly sensitive even though the target is defined at every admitted point. The response should distinguish a model-relative identification result, a supported numeric coordinate and a finite-precision certificate. These objects answer different questions and may become available at different times.

Composition also requires the correct order of nonlinear operations. Suppose two equally weighted customer groups have success probabilities \(1/5\) and \(1/2\). Their population probability is \(7/20\), with odds \(7/13\). Averaging their odds instead gives \((1/4+1)/2=5/8\), which transforms back to probability \(5/13\). Neither number arose from a floating-point error. Averaging and the nonlinear odds map do not commute. An interface that substitutes an average log-odds, odds or probability because each is called a “risk” has changed the target. In a causal contrast the error can affect both action-specific means before they are differenced. \citep{exec13_interchange_composition}

These examples motivate a transformation graph accompanying the result. Its nodes should identify the scientific object and coordinates, and its arrows should identify an exact map, a conditional approximation or a certified outer enclosure. A population aggregation followed by valuation is one path; conversion to a subgroup score followed by averaging is another. The workflow should be able to explain why the selected path answers the declared question. A chain of individually sensible package defaults is insufficient evidence that the composed path does.

Cross-language comparison can test these properties without pretending to qualify every estimator. For an exact finite reference table, an admitted identification expression should agree with a separately computed intervention distribution; variable renaming and category-order changes should preserve that answer after inverse mapping. A sign reversal should reverse an effect and reorder interval endpoints. A probability marginal should normalize on its declared support. These are necessary checks on the concrete path, not sufficient evidence of universal scientific correctness. The front-door and collider examples provide particularly useful references because a superficially plausible formula can return a different probability.

The same testing discipline should retain expected refusals. An unsupported graph class must not become an empty graph. A normalization failure must not become an estimated zero effect. A numerical timeout must not be cached as a scientific negative answer for an unrelated context. Matching those dispositions across library, CLI and MCP is part of semantic equivalence. The preserved local transport trial demonstrates selected comparisons for the existing bounded operations; the proposed y0 path still requires its own actual engine and conversion evidence. \citep{exec13_interchange_runtime}

For investment planning, the practical question is whether the information and computation are adequate for the decision. A numerically precise conditional effect on a vanishingly small subgroup may be irrelevant to the bank's target population. A broad but valid effect set may establish that a costly expansion cannot be justified yet. A slightly more expensive evaluator may be valuable if certified containment resolves a decision that uncontrolled approximations cannot. The proposed product should expose these consequences through the scientific result, its restrictions and its value calculation, rather than hiding them behind a generic success flag.
\label{exec13:interchange-complete-end}
