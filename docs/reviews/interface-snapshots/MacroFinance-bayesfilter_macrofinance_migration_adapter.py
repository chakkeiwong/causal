"""MacroFinance client facade for BayesFilter HMC/filtering primitives.

This module is intentionally a thin compatibility layer. MacroFinance keeps
ownership of model construction, priors, data payloads, parameterization, and
the existing HMC runner. The facade records the BayesFilter import contract and
routes no-HMC compatibility checks through BayesFilter primitives first.
"""

from __future__ import annotations

import importlib
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from mixed_frequency_tfp_generated_data_affine_reparameterized_adapter import (
    build_phase4_macro_model_error_matched_dgp_repaired_truth_center,
)
from bayesfilter_macrofinance_matched_dgp_contract import (
    classify_matched_hmc_screen_failure,
    hmc_config_payload,
    matched_hmc_config,
    validate_matched_initialization_artifact,
)


BAYESFILTER_ROOT_ENV = "PYTHONPATH"
BAYESFILTER_EXPECTED_ROOT = "/home/ubuntu/python/BayesFilter"
BAYESFILTER_MODULE = "bayesfilter.inference"
BAYESFILTER_RUNTIME_MODULE = "bayesfilter.runtime"
MIGRATION_SCOPE = "no_hmc_macrofinance_client_compatibility"
MATCHED_INITIALIZATION_ARTIFACT = (
    "results/hmc/mixed_frequency_tfp_phase4_matched_dgp_hessian_scaled_initialization_gate.json"
)


@dataclass(frozen=True)
class BayesFilterImportContract:
    """Recorded import-path contract for MacroFinance client compatibility."""

    module_name: str
    runtime_module_name: str
    expected_root: str
    pythonpath: tuple[str, ...]
    root_present: bool
    module_imported: bool
    runtime_module_imported: bool
    primitive_names: tuple[str, ...]
    primitive_modules: Mapping[str, str]
    scope: str = MIGRATION_SCOPE
    nonclaims: tuple[str, ...] = (
        "MacroFinance client facade only",
        "no MacroFinance HMC runner replacement claim",
        "no posterior convergence claim",
        "no GPU/XLA readiness claim",
    )

    def payload(self) -> Mapping[str, Any]:
        return {
            "module_name": self.module_name,
            "runtime_module_name": self.runtime_module_name,
            "expected_root": self.expected_root,
            "pythonpath": self.pythonpath,
            "root_present": self.root_present,
            "module_imported": self.module_imported,
            "runtime_module_imported": self.runtime_module_imported,
            "primitive_names": self.primitive_names,
            "primitive_modules": dict(self.primitive_modules),
            "scope": self.scope,
            "nonclaims": self.nonclaims,
        }


@dataclass(frozen=True)
class MacroFinanceBayesFilterFacadeResult:
    """No-HMC compatibility result for the MacroFinance migration facade."""

    import_contract: BayesFilterImportContract
    initialization_artifact_path: str
    initialization_artifact_valid: bool
    transform_value_parity_max_abs: float
    transform_score_parity_max_abs: float
    fixed_screen_failure_class: str
    fixed_screen_veto: str | None
    manifest_hash: str
    existing_hmc_runner_reference: str = "inference.hmc.sample_posterior_with_hmc"
    runner_replaced: bool = False
    model_payload_changed: bool = False
    nonclaims: tuple[str, ...] = (
        "no HMC execution launched",
        "no MacroFinance model/data/prior/parameterization change",
        "no runtime replacement claim",
        "no posterior convergence claim",
    )

    def payload(self) -> Mapping[str, Any]:
        return {
            "import_contract": self.import_contract.payload(),
            "initialization_artifact_path": self.initialization_artifact_path,
            "initialization_artifact_valid": self.initialization_artifact_valid,
            "transform_value_parity_max_abs": self.transform_value_parity_max_abs,
            "transform_score_parity_max_abs": self.transform_score_parity_max_abs,
            "fixed_screen_failure_class": self.fixed_screen_failure_class,
            "fixed_screen_veto": self.fixed_screen_veto,
            "manifest_hash": self.manifest_hash,
            "existing_hmc_runner_reference": self.existing_hmc_runner_reference,
            "runner_replaced": self.runner_replaced,
            "model_payload_changed": self.model_payload_changed,
            "nonclaims": self.nonclaims,
        }


def bayesfilter_import_contract(
    *,
    expected_root: str = BAYESFILTER_EXPECTED_ROOT,
) -> BayesFilterImportContract:
    inference_module = importlib.import_module(BAYESFILTER_MODULE)
    runtime_module = importlib.import_module(BAYESFILTER_RUNTIME_MODULE)
    inference_primitives = (
        "LatentAffineHMCTransform",
        "PrecomputedMassArtifact",
        "TargetFailurePolicy",
        "BackendParityGate",
        "HMCTuningPolicy",
        "classify_fixed_kernel_screen_with_tuning_policy",
        "screen_hmc_diagnostics",
        "stable_adapter_signature",
    )
    runtime_primitives = ("EvidenceManifest",)
    missing = tuple(
        name for name in inference_primitives if not hasattr(inference_module, name)
    )
    missing += tuple(name for name in runtime_primitives if not hasattr(runtime_module, name))
    if missing:
        raise ValueError("BayesFilter missing required primitives: " + ", ".join(missing))
    pythonpath = tuple(os.environ.get(BAYESFILTER_ROOT_ENV, "").split(os.pathsep))
    primitive_modules = {
        **{name: BAYESFILTER_MODULE for name in inference_primitives},
        **{name: BAYESFILTER_RUNTIME_MODULE for name in runtime_primitives},
    }
    return BayesFilterImportContract(
        module_name=BAYESFILTER_MODULE,
        runtime_module_name=BAYESFILTER_RUNTIME_MODULE,
        expected_root=str(expected_root),
        pythonpath=pythonpath,
        root_present=str(expected_root) in pythonpath,
        module_imported=True,
        runtime_module_imported=True,
        primitive_names=tuple(primitive_modules),
        primitive_modules=primitive_modules,
    )


def load_matched_initialization_artifact(
    path: str = MATCHED_INITIALIZATION_ARTIFACT,
) -> Mapping[str, Any]:
    initialization = json.loads(Path(path).read_text(encoding="utf-8"))
    validation = validate_matched_initialization_artifact(initialization, path=path)
    if not validation["passed"]:
        raise ValueError(
            "matched-DGP initialization artifact failed freshness checks: "
            + ", ".join(validation["reasons"])
        )
    return initialization


def matched_dgp_transform_parity_via_bayesfilter(
    *,
    initialization: Mapping[str, Any] | None = None,
) -> Mapping[str, float]:
    inference_module = importlib.import_module(BAYESFILTER_MODULE)
    initialization = initialization or load_matched_initialization_artifact()
    _payload, adapter, phi_c = build_phase4_macro_model_error_matched_dgp_repaired_truth_center(
        backend="tf_svd_derived"
    )
    factor = np.asarray(initialization["covariance"]["L"], dtype=np.float64)
    selected_epsilon = float(initialization["selected_epsilon"])
    z_rows = [np.zeros_like(phi_c)]
    z_rows.extend(
        selected_epsilon * np.asarray(row, dtype=np.float64)
        for row in initialization["standardized_latent_directions"][:2]
    )
    z_batch = np.asarray(z_rows, dtype=np.float64)
    transform = inference_module.LatentAffineHMCTransform(
        center=phi_c,
        factor=factor,
        covariance_provenance="matched_dgp_hessian_scaled_initialization_gate",
    )

    bayesfilter_theta = transform.latent_to_position(z_batch)

    def direct_value_and_grad(theta_batch: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        values = []
        gradients = []
        for theta in np.asarray(theta_batch, dtype=np.float64):
            value, gradient = adapter.log_prob_and_grad(
                tf.convert_to_tensor(theta, dtype=tf.float64)
            )
            values.append(float(value.numpy()))
            gradients.append(np.asarray(gradient.numpy(), dtype=np.float64))
        return (
            np.asarray(values, dtype=np.float64),
            np.asarray(gradients, dtype=np.float64),
        )

    helper_values, helper_latent_grad = inference_module.latent_value_and_score(
        z_batch,
        phi_c,
        factor,
        direct_value_and_grad,
    )
    direct_values = []
    direct_theta_grad = []
    for theta in bayesfilter_theta:
        value, gradient = adapter.log_prob_and_grad(
            tf.convert_to_tensor(theta, dtype=tf.float64)
        )
        direct_values.append(float(value.numpy()))
        direct_theta_grad.append(np.asarray(gradient.numpy(), dtype=np.float64))
    direct_latent_grad = transform.theta_score_to_latent_score(
        np.asarray(direct_theta_grad, dtype=np.float64)
    )
    direct_values_np = np.asarray(direct_values, dtype=np.float64)
    return {
        "position_self_consistency_max_abs": float(
            np.max(
                np.abs(
                    bayesfilter_theta
                    - inference_module.latent_to_position(z_batch, phi_c, factor)
                )
            )
        ),
        "value_parity_max_abs": float(
            np.max(np.abs(np.asarray(helper_values, dtype=np.float64) - direct_values_np))
        ),
        "score_parity_max_abs": float(
            np.max(
                np.abs(
                    np.asarray(helper_latent_grad, dtype=np.float64)
                    - direct_latent_grad
                )
            )
        ),
        "value_finite": bool(np.all(np.isfinite(helper_values))),
        "score_finite": bool(np.all(np.isfinite(helper_latent_grad))),
        "value_range": float(np.max(direct_values_np) - np.min(direct_values_np)),
        "latent_score_max_abs": float(np.max(np.abs(helper_latent_grad))),
    }


def matched_dgp_mass_artifact_via_bayesfilter(
    *,
    initialization: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    inference_module = importlib.import_module(BAYESFILTER_MODULE)
    initialization = initialization or load_matched_initialization_artifact()
    _payload, adapter, phi_c = build_phase4_macro_model_error_matched_dgp_repaired_truth_center(
        backend="tf_svd_derived"
    )
    covariance_payload = initialization["covariance"]
    covariance = np.asarray(covariance_payload["Sigma_phi_reg"], dtype=np.float64)
    factor = np.asarray(covariance_payload["L"], dtype=np.float64)
    artifact = inference_module.PrecomputedMassArtifact(
        position=phi_c,
        covariance=covariance,
        factor=factor,
        adapter_signature=inference_module.stable_adapter_signature(adapter),
        position_role="diagnostic_center_not_map",
        covariance_source=covariance_payload["covariance_source"],
        matrix_used_for_square_root=covariance_payload["matrix_used_for_square_root"],
        factor_orientation="row_right_transpose",
        source="macrofinance_matched_dgp_initialization_gate",
        nonclaims=(
            "matched-DGP initialization artifact only",
            "no production MAP quality claim",
            "no sampler convergence claim",
        ),
    )
    position, represented_covariance, represented_factor = artifact.validate_for_adapter(
        adapter,
        expected_dim=int(adapter.parameter_dim),
    )
    return {
        "position_parity_max_abs": float(np.max(np.abs(position - phi_c))),
        "covariance_parity_max_abs": float(np.max(np.abs(represented_covariance - covariance))),
        "factor_reconstruction_max_abs": float(
            np.max(np.abs(represented_factor @ represented_factor.T - covariance))
        ),
        "position_role": artifact.position_role,
        "nonclaims": artifact.nonclaims,
    }


def fixed_kernel_classification_via_bayesfilter() -> Mapping[str, Any]:
    inference_module = importlib.import_module(BAYESFILTER_MODULE)
    config = matched_hmc_config()
    acceptance = [1.0, 1.0, 1.0, 1.0]
    max_abs_log_accept = 7.5e-10
    screen = inference_module.screen_hmc_diagnostics(
        sample_chain_returned=True,
        hmc_error_absent=True,
        required_arrays_finite=True,
        log_accept_ratio=[0.0, max_abs_log_accept],
        acceptance_rate_by_chain=acceptance,
        fixed_kernel_used=True,
        num_adaptation_steps_zero=True,
        latent_initial_scale_zero=True,
        use_xla_false=True,
        compile_chain_with_xla_false=True,
    )
    bayesfilter_classification = (
        inference_module.classify_fixed_kernel_screen_with_tuning_policy(
            inference_module.HMCTuningPolicy.fixed_kernel_screen(),
            screen,
            acceptance_rate_by_chain=acceptance,
            step_size=config.step_size,
            num_leapfrog_steps=config.num_leapfrog_steps,
            max_abs_log_accept_ratio=max_abs_log_accept,
        )
    )
    macro_classification = classify_matched_hmc_screen_failure(
        hmc_error=None,
        screen={
            "passed": False,
            "checks": {
                "sample_chain_returned": True,
                "hmc_error_absent": True,
                "required_arrays_finite": True,
                "zero_divergences": True,
                "log_accept_nonfinite_count_zero": True,
                "acceptance_rate_by_chain_finite": True,
                "acceptance_rate_by_chain_strictly_between_0_05_and_0_99": False,
                "fixed_kernel_used": True,
                "num_adaptation_steps_zero": True,
                "latent_initial_scale_zero": True,
                "use_xla_false": True,
                "compile_chain_with_xla_false": True,
            },
        },
        diagnostics={
            "acceptance_rate_by_chain": acceptance,
            "max_abs_log_accept_ratio": max_abs_log_accept,
        },
        config=config,
    )
    return {
        "bayesfilter_failure_class": bayesfilter_classification.failure_class,
        "macrofinance_failure_class": macro_classification["failure_class"],
        "bayesfilter_screen_veto": bayesfilter_classification.screen_veto,
        "macrofinance_screen_veto": macro_classification["screen_veto"],
        "bayesfilter_diagnostic_role": bayesfilter_classification.diagnostic_role,
        "macrofinance_interpretation": macro_classification["interpretation"],
        "hmc_config": hmc_config_payload(config),
    }


def evidence_manifest_via_bayesfilter(
    *,
    initialization_path: str = MATCHED_INITIALIZATION_ARTIFACT,
) -> Mapping[str, Any]:
    runtime_module = importlib.import_module("bayesfilter.runtime")
    initialization = load_matched_initialization_artifact(initialization_path)
    manifest = runtime_module.EvidenceManifest(
        run_scope="no_hmc_parity",
        git_state={"status_short": "not_captured_by_facade"},
        command=(
            "python",
            "-m",
            "pytest",
            "tests/test_bayesfilter_macrofinance_migration_adapter.py",
        ),
        environment={"PYTHONPATH": BAYESFILTER_EXPECTED_ROOT, "CUDA_VISIBLE_DEVICES": "-1"},
        cpu_gpu_status="CPU-only no-HMC compatibility facade",
        data_hash=str(initialization.get("artifact_hash", "matched-dgp-initialization")),
        target_scope="mixed_frequency_tfp_phase4_matched_dgp",
        backend="tf_svd_derived",
        transform_signature={"factor_orientation": "row_right_transpose"},
        map_covariance_source=str(initialization["covariance"]["covariance_source"]),
        tuning_policy="fixed_kernel_screen",
        diagnostic_policy="macrofinance_migration_facade_no_hmc",
        result_paths={
            "result_note": "docs/plans/bayesfilter_macrofinance_phase_8_macrofinance_migration_adapter_compatibility_result_2026_06_09.md",
            "test": "tests/test_bayesfilter_macrofinance_migration_adapter.py",
        },
        nonclaims=(
            "manifest from MacroFinance client facade only",
            "no HMC execution launched",
            "no posterior convergence claim",
            "no runtime replacement claim",
        ),
    )
    return {"manifest_hash": manifest.manifest_hash, "payload": manifest.payload()}


def evaluate_migration_facade() -> MacroFinanceBayesFilterFacadeResult:
    contract = bayesfilter_import_contract()
    initialization = load_matched_initialization_artifact()
    transform = matched_dgp_transform_parity_via_bayesfilter(initialization=initialization)
    _mass = matched_dgp_mass_artifact_via_bayesfilter(initialization=initialization)
    classification = fixed_kernel_classification_via_bayesfilter()
    manifest = evidence_manifest_via_bayesfilter()
    return MacroFinanceBayesFilterFacadeResult(
        import_contract=contract,
        initialization_artifact_path=MATCHED_INITIALIZATION_ARTIFACT,
        initialization_artifact_valid=True,
        transform_value_parity_max_abs=transform["value_parity_max_abs"],
        transform_score_parity_max_abs=transform["score_parity_max_abs"],
        fixed_screen_failure_class=str(classification["bayesfilter_failure_class"]),
        fixed_screen_veto=classification["bayesfilter_screen_veto"],
        manifest_hash=str(manifest["manifest_hash"]),
    )
