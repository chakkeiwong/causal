# R05 pre-evaluation author review

The sparse learner is fixed before evaluation: standardize the control block,
select one lasso penalty from a finite grid on the held-out training half,
refit, and cross-fit across two blocks separated by a declared gap. The
residualized IV ratio uses the encouragement residual as score instrument.
The derivation requires sparse approximation and product rates, positive
Gram/effective IV separation and geometric-mixing gap/HAC rates. A dense
cross-fit implementation is an algebra reference, not an oracle.

The fixture gives sparse/dense estimate difference 0.00209 and passes the
zero-response selection boundary. Weak instrument, misspecification and
persistence are retained; prediction/fit output is never sufficient for
inference qualification. Freeze eight cells and 512 requests each. The
learner remains a family-specific result with no arbitrary-learner claim.
