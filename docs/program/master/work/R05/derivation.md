# R05: one sparse learner under declared temporal separation

The learner is a sparse linear nuisance family. A p-dimensional stationary
Gaussian control vector has geometric coordinate dependence, and the three
nuisances are action, outcome and encouragement regressions. Each block is
standardized using training data. A fixed penalty grid is selected on a
held-out half of the training block; the selected lasso is refit on that
block. Two evaluation blocks are separated by a frozen gap, so no fitted
prediction uses nearby observations across the declared mixing boundary.

For the residualized IV score, let Z be the encouragement residual, A the
action residual and Y the outcome residual. The target is
theta=E[ZY]/E[ZA]. Orthogonality removes first-order nuisance errors. A
prespecified sparse approximation with support s and bounded coordinates
requires lasso prediction error O_p(s log(p)/n_train) and the product of
action/outcome errors o_p(n_eval^-1/2). The block gap g must grow so the
geometric mixing remainder is o(n^-1/2); the score covariance uses a
Bartlett window b tending to infinity with b/n tending to zero. Positive
nuisance Gram eigenvalues and a fixed nonzero E[ZA] are required.

The dense challenger uses the same blocks and direct least squares. It is an
algebra/numerical reference, not an oracle. A prediction improvement cannot
qualify the inferential ratio: report bias, interval coverage, SE/SD,
denominator separation, selected penalties, nonzero counts and covariance
workload together. Weak instrument, misspecified sparsity and changing
persistence are refusal/adverse regimes.

The fixture compares sparse and dense cross-fitting and exercises the exact
zero-response selection boundary. The registered study varies p, support,
gap and persistence, and retains a dense independent implementation. This
supports only the declared sparse family and mixing law. Arbitrary learners,
nonstationary bank panels and finite uniform coverage remain open.
