# R02: one joint pair/calendar/gold experiment

The inherited iid-pair/mixing-calendar construction adds row and date
variances and gold-label delta variance. This can count the pair-date
interaction twice; it does not make persistent audit noise diagonal over
time. Here we specify an entire experiment and retain that distinction.

## Sampling law and identification

There are N iid persistent pairs. Their signed focal and companion responses
are F_it = beta + U_i + C_t + E_it and D_it = delta + V_i + C_t + J_it.
Their difference cancels the common calendar. U,V are independent zero-mean Gaussian pair
effects with variance sigma_p^2; E,J are independent Gaussian cell errors
with variance sigma_e^2. C is an independent stationary Gaussian AR(1)
calendar with variance sigma_c^2 and fixed |rho|<1. A_it is an independent
randomized sign, and stored outcomes equal A_it times these responses.
Candidate ordering is fixed for each pair and exogenous. R_i is one
Bernoulli(q) audit per whole pair history; it is not redrawn per date.

An audited ordering label has independent symmetric flip probability e<1/2.
An independent representative gold sample of M labels gives e_hat. When its
exact binomial upper limit reaches 1/2 the procedure refuses rank-dependent
inference. The gold study must concern the same error mechanism. An independent
population of gold labels does not establish that scientific premise itself.

After multiplying stored outcomes by their actions, the adjusted pair-date
score is Z_it = B_it + R_i L_i Ddiff_it/[2q(1-2e_hat)], where L=+1/-1
is the observed audited ordering and B is the candidate average. Unobserved
labels remain absent. At the true e, the random multiplier W_i = R_i xi_i /
[q(1-2e)] has E[W]=1 and E[W^2]=1/[q(1-2e)^2], regardless of the candidate
ordering probability. This proves E[Z]=beta without inversion of identity
counts. Unknown/endogenous inclusion, unknown asymmetric error or endogenous
maps are outside the experiment. Explicit unsupported declarations refuse;
a lying declaration can still produce misleading estimates.

## Projection and all covariance terms

Let d=(beta-delta)/2 and a=E[W^2]. The score separates into

    Z_it = beta + P_i + C_t + H_it,
    P_i = (U_i+V_i)/2 + W_i(U_i-V_i)/2 + d(W_i-1),
    H_it = (E_it+J_it)/2 + W_i(E_it-J_it)/2.

P and H are uncorrelated; H has zero cross-date and cross-pair covariance
although its conditional variance depends on W. Then

    Var(P) = sigma_p^2(1+a)/2 + d^2(a-1),
    Var(H) = sigma_e^2(1+a)/2,
    Var(mean C) = sigma_c^2 [T + 2 sum_{k=1}^{T-1}(T-k)rho^k]/T^2.

The finite known-e variance is Var(P)/N + Var(mean C) + Var(H)/(NT).
The estimated-error expansion adds g^2 e(1-e)/M, with
g=(beta-delta)/(1-2e). Its cross products with pair/calendar sampling are
zero at first order because the gold sample is independent. Remainders
include O_p(M^-1) curvature and O_p((MN)^-1/2) random derivative error;
their constants diverge as e approaches 1/2. A fixed boundary margin,
nondegenerate projections and comparable N,T,M growth control them.

Persistent audits contribute to Var(P), so their repeated-date covariance
does not vanish as T grows. Independent origin audits instead contribute a
cell component: only their conditional lag-zero variance remains. With q=1,
e=0 the score equals the full focal response and these formulas reduce to
sigma_p^2/N + Var(mean C) + sigma_e^2/(NT). Exact audit/flip enumeration and
Gaussian covariance-matrix sums provide independent references for both limits.

## Feasible covariance and finite limitations

Row-mean sample variance/N estimates the pair term plus the interaction.
Bartlett covariance of column means/T estimates the calendar term plus the
same interaction. Subtract the double-demeaned cell mean-square/(NT) once,
then add estimated gold variance. Refuse a nonpositive total. This subtraction
is motivated by the specified additive experiment, not arbitrary multiway
dependence. The inherited method is retained as a paired challenger.

Fixed |rho|<1 gives geometric mixing and finite moments. With bandwidth b
tending to infinity and b/T tending to zero (the chosen b=floor(T^(1/3))),
calendar HAC is consistent. Independent pair and gold CLTs and the calendar
CLT yield the first-order normal interval under comparable growth. A 99%
critical is prespecified for a min95 selected-grid screen. High persistence
and small samples can still make the finite window biased, while weak gold
rank invalidates a first-order approximation. An analytical variance using
the true constants is an oracle diagnostic, not deployable information.

The study varies pair/date/gold ratios, q, identity rank, persistence and
window. Shared audits across pairs, wrong q and state-dependent label errors
are retained as adverse laws. All requests, including rank refusals, remain
in the coverage denominator. Earlier V10 finite undercoverage remains
historical evidence in the original reliability study. No general dependent
identity theorem or bank validation follows from this selected experiment.
