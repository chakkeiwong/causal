# Card NPV

This repository contains the supported Card NPV admission and mathematical
contract layer, active TensorFlow Probability/XLA qualification code, and a
large archive of research campaigns. The whole tree is an evidence store; it is
not all one production package. The release manifest is
[RELEASE_MANIFEST.md](RELEASE_MANIFEST.md).

## Supported Boundary

Colleagues should begin with these modules:

| Responsibility | Module |
| --- | --- |
| actual-data manifest and privacy-safe profile | `poc.card_end_to_end.actual_data_readiness` |
| mathematical and modeling decisions | `poc.card_end_to_end.modeling_math_readiness` |
| unambiguous target value | `poc.card_end_to_end.target_contract` |
| current issuer contribution | `poc.valuation.issuer_contribution` |
| promotion V2 gate | `tools.validate_card_scientific_promotion` |
| active qualification likelihood | `poc.card_end_to_end.joint_likelihood_*` |
| active TFP/XLA qualification | `poc.card_end_to_end.synthetic_structural_tfp*` |

The package-level `poc.card_end_to_end` import exposes only supported admission,
readiness, and target interfaces. The old four-route campaign is available only
through `poc.card_end_to_end.negative_controls` and cannot authorize a Card
claim.

The governing target is

```text
historical_value - perfect_execution_value
```

with sign ID `V_G0_MINUS_V_GH`. Historical NumPy and Torch modules retain their
opposite-sign numbers under the explicit name `perfect_minus_historical`.

## Install

Use Python 3.11. From any directory:

```bash
python -m pip install -e '/path/to/cardnpv[core,test]'
```

For active inference qualification:

```bash
python -m pip install -e '/path/to/cardnpv[core,test,tfp]'
```

Torch is historical only:

```bash
python -m pip install -e '/path/to/cardnpv[core,test,historical-torch]'
```

Equivalent constrained inputs live under `requirements/`.

The 2026-08-03 local parity run used a custom TensorFlow
`2.20.0-dev` build with TFP `0.25.0` and `tf-keras 2.19.0`. The portable
profile uses stable TensorFlow `2.19.1`; CI is the governing compatibility
check for that profile. A passing local custom build is not represented as a
reproducible wheel lock.

## Release Candidate Quickstart

For a colleague who wants the shortest path from clone to verification:

1. Read [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md) first.
2. Install the supported boundary with `python -m pip install -e '/path/to/cardnpv[core,test]'`.
3. Build a wheel and smoke-test it from a clean directory:

   ```bash
   python -m pip install build
   python -m build
   python -m venv /tmp/cardnpv-release-smoke
   /tmp/cardnpv-release-smoke/bin/python -m pip install --upgrade pip
   /tmp/cardnpv-release-smoke/bin/python -m pip install dist/*.whl -r requirements/core.txt
   /tmp/cardnpv-release-smoke/bin/python -m pip check
   mkdir -p /tmp/cardnpv-release-smoke-work
   cd /tmp/cardnpv-release-smoke-work
   /tmp/cardnpv-release-smoke/bin/python -c 'import poc, program_h_policy, tools'
   ```
4. Run `pytest -q` for the supported delivery gate.
5. Run the CPU-only TFP gate only when working on that surface:

   ```bash
   CUDA_VISIBLE_DEVICES=-1 pytest -q \
     poc/tests/test_actual_data_readiness.py \
     poc/tests/test_joint_likelihood_backbone.py \
     poc/tests/test_joint_likelihood_card_lite.py \
     poc/tests/test_synthetic_structural_tfp_contract.py \
     poc/tests/test_synthetic_structural_tfp_parity.py
   ```

Program H remains qualification-only: its tests depend on frozen design artifacts and are not part of the default release gate.

## Test Profiles

The default command is dependency-light and is the delivery gate:

```bash
pytest -q
```

It covers strict ADR/MMR/promotion inputs, canonical target sign, and finance
invariants. It does not claim posterior convergence or actual-data validity.

Collect every test available in the current environment:

```bash
pytest -q --collect-only poc/tests tests
```

Run the active TensorFlow/TFP admission and qualification checks deliberately on
CPU by hiding GPU devices before framework import:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  poc/tests/test_actual_data_readiness.py \
  poc/tests/test_joint_likelihood_backbone.py \
  poc/tests/test_joint_likelihood_card_lite.py \
  poc/tests/test_synthetic_structural_tfp_contract.py \
  poc/tests/test_synthetic_structural_tfp_parity.py
```

Historical Torch tests are collected only when Torch is installed. Program H
tests additionally require their frozen design artifacts under
`artifacts/program_h_policy_endogeneity/design/`; they are qualification replay,
not the default Card NPV suite.

## Evidence And Promotion

Promotion manifests use `CARD_NPV_PROMOTION_MANIFEST_V2`. Each of the fifteen
evidence roles must be a distinct, hash-bound JSON packet with matching target,
likelihood, estimator, implementation, and governing-sign bindings. Actual-data
claims also require a distinct data file, dictionary, lineage file, and an ADR
final-admission report whose source hash names that data.

A Git commit is not evidence that a dirty or untracked source file was present.
Claim-bearing runners must use the common provenance utilities and run from a
clean commit. Diagnostic runs may record dirty state but cannot be promoted.

## Repository Tiers

The final release-tree disposition is in
`docs/reviews/card-npv-code-handover-final-file-inventory.csv`. The original
pre-repair inventory remains preserved beside it as review evidence.

- `handover_candidate_repair_first`: supported boundary repaired for handover.
- `qualification_evidence_freeze`: active qualification code preserved with its
  evidence; it is not automatically a production default.
- `historical_research_archive`: old campaigns and opposite-sign backends kept
  for replay, not supported use.
- `separate_tooling_package`: manuscript, literature, and governance tooling.
- `test_classify_with_subject`: follows the environment and tier of its subject.
- `manual_boundary_decision`: shared code whose owner must be chosen before
  further productization.

Generated PDFs, raw samples, experiment outputs, and local review sessions are
not part of the supported Python package.

## Handover Records

- Initial audit: `docs/reviews/card-npv-code-handover-review-2026-08-03.md`
- Repair program: `docs/plans/card-npv-colleague-handover-repair-master-program.md`
- Pre-repair inventory: `docs/reviews/card-npv-code-handover-file-inventory.csv`
- Final inventory: `docs/reviews/card-npv-code-handover-final-file-inventory.csv`
- Final audit: `docs/reviews/card-npv-colleague-handover-final-audit-2026-08-03.md`
