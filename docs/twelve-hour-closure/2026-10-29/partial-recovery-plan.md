# When a follow-up invitation does not recover the outcome

Question: what causal conclusions remain justified when routine missingness is informative and randomized invitations produce selective successful recovery? Continue the completed recovery study without silently assuming every invitation succeeds.

Inspect Coppock,Gerber,Green,Kern(2017) and the cutoff-pinned attrition R package. The package appeared on CRAN in September2026, within the7October cutoff. Obtain its genuine paper, inspect identification, confidence and stability assumptions, and audit the implementation rather than inheriting the DESCRIPTION claims. Do not execute downloaded code. Check overlap with the separate release agent before expanding.

Proposed authored study, subject to primary-text review:
- Use a bounded binary endpoint and randomized single treatment. Do not impose finite bounds on the previous Gaussian servicing reward, which is unbounded.
- Derive worst-case mean and effect bounds under arbitrary routine missingness and selective completed recovery, with randomized invitation and stable historical outcome.
- Prove which part of identification width depends on completion and which part of estimation precision depends on invitation probability. A larger invitation fraction alone need not shrink the population identified set.
- Exact finite-type enumeration supplies population truth and attainable extremal completions. Compare complete-case and falsely representative recovery point estimates with honest bounds.
- Inspect whether monotone-response/Lee bounds answer a different target and require additional assumptions; do not treat them as an automatic substitute.
- Only after definitions and target are fixed, run finite-sample comparisons, report uncertainty and decision consequences, and retain a deliberately violated outcome-stability case if it discriminates the assumptions.

Review priorities: no conditioning on post-treatment response without acknowledging target change; no point identification from random invitation alone; no sharpness claim beyond the declared model; no bank-data or native-package qualification. A successful negative finding can close the proposal question without claiming all missingness problems solved.

Publication will preserve energy revision2/scientific v15, with sources, reproducible calculations, checked mathematics, compact economic prose, figures and rendered review. Independent acceptance and genuine bank recovery remain later.

## Fixed design after primary reading

Coppock2017 Sections2.1–2.5 identify the full experimental-population ATE with bounded outcomes, random invitation and outcome stability, retaining arbitrary follow-up nonresponse. Equations11–16 imply the planned bounds. Section2.7's delta is a mixture restriction on follow-up nonresponders; it does not relax outcome stability. The package DESCRIPTION calls it stability sensitivity, but its actual function documentation and gen_mean implement the former. Preserve this distinction.

Use IID customers with binary historical outcomes, treatment-arm means0.55 and0.45 (true benefit0.10). An optional joint potential-outcome construction has masses0.35,0.20,0.10,0.35 for(0,0),(0,1),(1,0),(1,1). Routine observation probabilities are control(0.8,0.4)andtreated(0.4,0.8),indexed by outcome0,1. Completed recovery probabilities among invited routine nonresponders are:
- Standard: control(0.1,0.9),treated(0.9,0.2).
- Intensive: control(0.8,0.98),treated(0.98,0.8).
- Complete:(1,1)botharms.
- Unstable:complete recovery,but half the originally unsuccessful missing treated customers are recorded as successful at follow-up. This deliberately changes the endpoint and violates stability.

Known independent invitation q=0.1,0.25,0.5,1,shared uniforms within replication. 500replications per regime,2000IIDcustomers per arm;new seed202610300517. Four regimes yield2000independent datasets and8000regime-rate cells. Retain first/middle/last diagnostic datasets and all replicate summaries.

Use authored Horvitz–Thompson endpoint means under Bernoulli invitations,not pretend to execute the package's ratio estimator orfixed-size design. ForYin[0,1],theper-person lower score is RY+(1-R)BSY/q andupper score RY+(1-R)[1-BS(1-Y)/q]. Each score's range is1/q. Derive a finite-sample outward confidence band withHoeffding using an included proof from bounded tiltedvariance: t=sqrt(0.5*(1/(n1*q1^2)+1/(n0*q0^2))*log(2/alpha)). This covers the entire population identified interval with probability at least1-alpha under the declared IIDanddesign assumptions. Also report approximate normal endpoint bands separately;do nottransferguarantees.

Verify exact rational bounds,widths,naive limit,attainableextremalcompletionsandobserved-lawpreservation before simulation. Verify unseen-data poisoning. Report truthcoverage,whole-setcoverage,width,positive/negative conclusions,invitationsandcompletedrecoveries. Theunstablescenarioisexpectedtoinvalidatebothbandsforthehistoricaltarget;illustrate a separately declared boundgamma onmeanoutcome change amongrecoveredcases,not package delta. Noquantitativebankcostclaim.
