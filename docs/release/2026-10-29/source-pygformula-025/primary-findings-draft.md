# Selected pygformula fitting contracts

The investigation uses commit e66f787fcef2d6a9092b88135147c6b13785795c (1.2.1, 22 May 2026). Eight new source/doc originals and two retained caller/simulator originals match the selected Git tree. No downloaded Python implementation is executed.

## Consequential findings

1. The documented restriction schema is a list of lists, each beginning with a covariate string. Deterministic knowledge.rst:14–40 says to fit only histories on which the outcome is not deterministic. fit.py:106–135 instead builds repeated copies of the whole first restriction, then asks whether a string covariate belongs to that list. The documented input does not enter the filtering branch. simulate.py:371–386 does extract names and enforces the deterministic values. The constructor stores restrictions without transformation and forwards them directly (parametric_gformula.py:316,500–504). error_catch has no restriction transformation. This supports a static fitting-population mismatch, not a measured runtime claim.
2. fit_ymodel:315–339 selects nonmissing outcomes; explicit competing events further require current competing event zero. No censor-name parameter is passed to it. Input data.rst:37–66 defines covariates at k and outcomes at k+1 and qualifies the choice of NA or zero on survival censor rows by fine time intervals. Censoring event.rst:6–26 assigns the censor model to the observed IPW comparator. The same censor label does not choose outcome likelihood rows for the user.
3. fit_compevent_model and simulate.py:405–469 preserve a coherent competing-first ordering. Default is conditional on no current competing event, and current competing survival multiplies its hazard. This is a valid conditional probability factorization, not a defect.

## Proposed exact constructions

Use a full-rank binary predictor X with equal cell counts. For each X, ten eligible records contain eight completions and two failures; ten ineligible records have deterministic zero. The correctly restricted logistic score gives q=4/5 for both X cells, while unrestricted pooled fitting gives 2/5. At half eligibility, the simulated portfolio completion mean becomes 2/5 or1/5. A stipulated USD100 contingent receipt and USD30 per-account cost produces USD10 or -10. These are analytical model traces, not executed package outputs, bank data, or causal service effects.

For a coarse interval with100 accounts,20 missing outcomes after censoring,8 observed defaults and72 observed nondefaults, a constant outcome likelihood gives1/10 on observed outcomes or2/25 after coding unknown outcomes zero. At USD10,000 loss and USD900 premium the illustrative margin is USD100 or -100. Without an assumption about the missing outcomes, the finite-population default proportion ranges from2/25 to7/25, so neither encoding identifies it automatically. Independent censoring and a common modeled history are explicit additional assumptions for interpreting the observed1/10 as a target risk.

For competing events,20 prepayments,8 defaults and72 other outcomes give q=1/5 and p=1/10 conditional on no prepayment. (1-q)p=2/25 matches the actual one-step frequency. A marginal8/100 inserted as the conditional default hazard would double-count prepayment survival and return8/125. Preserve the existing two-period86/625 and19/100 comparison.

## Deliberate scope limits

Other inspected parser, category-mapping and baseline-validation questions are not folded into this treatment without their own developed consequence. The package's referenced scholarly works remain discovery leads unless already independently admitted. No empirical coverage, fitted-package execution, full dependency qualification or bank validity is claimed.

## Tooling observations

The inherited summary mentioned a pygformula pin.json that does not exist; the selected pin is established by plan.json and the retained authenticated Git tree/receipt identities. A broad initial state read was truncated; subsequent reads are bounded. A malformed executor string was corrected before any write.
