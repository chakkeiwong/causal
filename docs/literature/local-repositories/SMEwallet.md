# Model Card: SME Wallet Synthetic Prototype

Date: 2026-07-17  
Status: research artifact; no production or real-data approval

## Summary

This repository implements a deposit-only SME wallet prototype on synthetic
data. It defines a two-part total wallet, sparse multi-bank composition,
selected quotes, conserved origin-destination flows, finite randomized actions,
component-owned value, estimator/policy claim gates, and a safe artifact
boundary. The final Phase 12 audit established
`synthetic_prototype_mechanically_feasible` for the frozen local system.

No learned opening estimator or learned policy was promoted. The recommended
model is a gated reference architecture with abstention and a challenger
ladder, not an unconditional enhanced model.

## Intended Use

- Check mathematical identities, support, timing, masks, and stock-flow
  conservation.
- Exercise synthetic DGP scenarios and distinguish engineering, numerical, and
  scientific evidence.
- Compare estimator and policy candidates under predeclared synthetic regimes.
- Identify the external data, design, governance, and human authorization needed
  before any real claim.

## Prohibited Use

Do not use this artifact to infer a real SME's competitor balances, contact or
price a customer, allocate credit, make adverse-action decisions, claim causal
uplift or production NPV, forecast competitor equilibrium, release synthetic
records, or assert privacy, fairness, compliance, legal validity, commercial
benefit, or production readiness.

## Population, Inputs, and Outputs

The target is a declared SME population and an eligible bank-deposit boundary.
The prototype's bank set is `(b_f, b_c, b_r)`; nonbank liquidity is outside the
wallet. Synthetic inputs include pre-action covariates, bank quote primitives,
opening balances, masks/anchors, assignment/receipt, scenario state, and
declared valuation fixtures. Monetary units are synthetic currency units (SCU).

Outputs are typed and evidence-labeled:

- total and competitor wallet, with point/set/rank/not-identified or abstention
  status;
- model-conditional active-bank shares and structural primary;
- conserved movement, retention, expansion, cannibalization, and runoff;
- assignment ITT/CATE diagnostics only under their own gates;
- synthetic scenario policy value/regret; and
- component-owned scenario value and WTA derivative ratios.

## Architecture

1. Dynamic two-part incidence and positive wallet.
2. Structural-primary hurdle plus active-set logistic-normal composition.
3. Latent pre-assignment and potential-offer quote blocks with masks.
4. Target-constrained proportional-mixing reference flows, with origin-aware
   challengers on the same margins.
5. Randomized finite-action assignment and explicit receipt/interference
   challengers.
6. Assigned-path likelihood that marginalizes unassigned potential variables.
7. Pathwise value with one owner per cash-flow component and an explicit
   finite-horizon or modeled-terminal rule.

The proportional-mixing flow law is a synthetic reference hypothesis, not an
identified provenance claim. A logistic-normal reference change requires the
corresponding mean/covariance transformation and ALR Jacobian.

## Performance Evidence

Phase 7 passed 11,567 invariant checks for all 42 scenarios at a smoke tier.
Phase 9 completed 4,026 cells and 5,208,394 invariant checks; two
scenario-specific opening directions passed all ranking conjuncts, one was
coverage-vetoed, and 54 comparisons were primary non-rejections. Phase 10
completed 413 cells and 530,526 checks; five evaluable regimes showed a
descriptive balance/value objective conflict and no ranking was allowed.

Phase 12 completed 244 cells, 312,511 checks, 2,928 opening records, 1,220
policy records, 732 mechanism records, and 488 causal records. Three of six
opening comparisons and seven of eight policy comparisons were available. No
opening or policy candidate was promoted. Seven available policy comparisons
favored `always_a0` on synthetic value regret while balance regret moved in the
opposite direction. `always_a0` is a transparent comparator, not a default.

These results are synthetic, scenario-specific, and conditional on the frozen
generator and evidence contracts. They do not rank methods globally.

## Limitations and Risks

- Focal balance alone does not identify total wallet and focal share.
- Aggregate anchors do not identify individual wallets.
- Endpoint balances do not identify origin-destination movement.
- Competitor rates are not generic excluded instruments.
- Selected quotes, MNAR anchors, transport, receipt effects, and interference
  require separate assumptions and may force abstention.
- Synthetic value inputs are not institution-approved FTP/cost/loss inputs.
- Heavy tails and support failures can create typed unavailable cells.
- Synthetic data are not automatically private; no threat-model attack study was
  run.
- No fairness, legal, compliance, or model-risk review was performed.

## Data and Leakage Controls

Persistent research bundles are scalar-only or safe-observation artifacts. Truth
balances, potential outcomes, unassigned quotes, latent effects, copula draws,
and model objects are excluded. Safe writers reject oracle fields and
non-allowlisted filenames. Entity-level persistence is absent from the Phase 12
adjudication bundle.

## Change Control

Any real-data or production extension needs a new reviewed plan, source and
consent ledger, target-specific training protocol, baseline ladder, uncertainty
and downstream criterion, privacy/fairness assessment, and human authorization.
A repaired estimator or value-aligned policy is a new exploratory candidate on
fresh scenarios; it cannot reinterpret the frozen audit.

## Authority

The survey is a readable synthesis. Exact authority is in the Phase 2 source
and equation ledgers, Phase 3--6 specifications, tested math contract, Phase
7--12 raw artifacts and close records, the Phase 13 claim ledger and equation
crosswalk, and the final red-team report. The model card must be checked by
`scripts/check_phase13_document.sh` together with the survey and manifest.
