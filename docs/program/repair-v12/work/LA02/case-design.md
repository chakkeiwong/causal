# Synthetic case definitions and analytical oracles

These four cases are project constructions. Names evoke banking decisions, but
no case describes verified bank data, process ownership or assignment truth.
All times are offsets in days from a declared decision origin. Observed and
derived variables have event and availability times; latent variables have no
observed availability time. Equal timestamps do not establish causal direction.

**Funding.** “Should we increase the deposit offer?” has at least two targets:
the balance response to a 25-basis-point increase, and the net funding-cost
change over thirty days. Customer risk and market conditions may confound offer
assignment. A sufficient DAG is a hypothesis; an ADMG with an unmeasured common
cause remains an alternative. Selecting one target requires a decision owner.
We keep both targets and do not turn their common business wording into a
single numerical query.

**Servicing.** A contact at day zero changes an intermediate account state L1,
which affects the day-eleven contact and the final outcome. The intermediate
state occurs at day ten and becomes available at day eleven. A dynamic rule can
use it at eleven but not at ten. L1 is a mediator of the first contact and a
confounder of the later contact-outcome relation. Treating it as an ordinary
baseline adjustment variable changes the first-contact total-effect problem.
The proposed policy depends only on permitted history. Its causal value still
requires sequential exchangeability, consistency, positivity and a suitable
statistical procedure; the schema cannot verify those premises.

**Discovery.** A deliberately simple binary offer A and customer response Y are
recorded at the same coarse event time. Under model F, A is Bernoulli(1/2) and
Y equals A with probability 0.9. Under model R, Y is Bernoulli(1/2) and A equals
Y with probability 0.9. These two structural constructions induce the same
joint table: p00=p11=0.45 and p01=p10=0.05. Intervention on A changes E[Y] by
0.8 under F and by zero under R. Thus the CPDAG A--Y, interpreted with these
two admissible models, retains the effect set {0, 0.8}. A language suggestion
favoring F cannot remove R without a new justified restriction. This is a
finite synthetic example, not a calibrated graph confidence set or a universal
identified-set calculation.

**Observation.** An analysis of a servicing action and repayment includes only
records that were successfully linked. Both action and outcome can affect
selection S. A latent ownership/identity variable may confound the causal
relation; a record-link score is an observed proxy, not ownership truth.
Population effects and effects restricted to linked records differ. The graph
therefore records the selection node and the latent alternative, and the
question remains ambiguous. Conditioning on the selection collider may open a
path even if the unselected population relation were unconfounded.

**Target-weight oracle.** Let X take two values with equal probability,
e(0)=0.2, e(1)=0.5, tau(0)=0 and tau(1)=10. Trimming to 0.1<=e(X)<=0.9 keeps
both strata, giving a trimmed-population ATE of 5. Conventional overlap weights
give (0.16*0+0.25*10)/(0.16+0.25)=250/41, approximately 6.09756. This exact
calculation illustrates why the OCI notebook's target label cannot be mapped
to conventional overlap ATO without checking the weighting rule. It is not an
evaluation of that downloaded notebook and supplies no estimated-trimming
coverage guarantee.

**IV oracle.** Let half of subjects comply with a randomized binary instrument
Z, and half never take treatment. Set treatment T=Z for compliers and T=0 for
never-takers. Let Y(0)=0, Y(1)=1 for compliers, and Y(1)=3 for never-takers.
The exclusion, randomization and monotonicity conditions hold. The Wald ratio
is (0.5)/(0.5)=1, while the population ATE is (1+3)/2=2. Altering the
never-takers' unobserved treated outcome changes the population ATE without
changing the observed law. This counterexample explains the extra-assumption
review required before treating an unrestricted IV ratio as population ATE.
It is not a finding that every CLadder-generated IV item uses this mechanism.
