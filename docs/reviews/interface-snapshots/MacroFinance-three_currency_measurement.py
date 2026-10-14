"""Measurement equations for the USD/EUR/JPY synthetic block.

This module keeps quote mapping and observed-versus-derived row semantics out
of the provider.  The formulas are the monograph's directed convention:

``rho^{i/j}(tau) = (f^{i/j}(tau) - s^{i/j}) / tau``
``chi^{i/j}(tau) = (r^j(tau) - rho^{i/j}(tau)) - r^i(tau)``
``x_m^{i/j}(tau) = -chi^{i/j}(tau)``
``Phi^{i/j,G}(tau) = (lambda^i(tau) - lambda^j(tau)) + chi^{i/j}(tau)``

For USD-source edges, positive ``chi`` is the model sign for dollar scarcity.
The full-triangle residual ``kappa_obs`` is an observed diagnostic residual, not
automatically a structural cycle wedge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from three_currency_graph import (
    CurrencyCode,
    DEFAULT_MEASUREMENT_NOISE_STD,
    ThreeCurrencyGraph,
    ThreeCurrencyObservationRow,
    canonical_three_currency_graph,
    edge_row_metadata,
    triangle_diagnostic,
    zero_cycle_implied_cross_edge,
)


ObservationMode = Literal["usd_star", "full_triangle"]
COUNTRY_YIELD_GROUP = "country_yield"
EDGE_WEDGE_GROUP = "edge_wedge"
TRIANGLE_DIAGNOSTIC_GROUP = "triangle_diagnostic"


@dataclass(frozen=True)
class DirectedPairMeasurement:
    """Formula output for one directed pair and maturity."""

    source: CurrencyCode
    target: CurrencyCode
    maturity: float
    rho: np.ndarray | float
    chi: np.ndarray | float
    market_residual: np.ndarray | float
    government_bond_wedge: np.ndarray | float


@dataclass(frozen=True)
class ObservationContract:
    """Rows and diagnostics exposed for one observation mode."""

    mode: ObservationMode
    observed_edge_rows: tuple[ThreeCurrencyObservationRow, ...]
    derived_edge_rows: tuple[ThreeCurrencyObservationRow, ...]
    diagnostic_rows: tuple[ThreeCurrencyObservationRow, ...]
    measurement_noise_std: float
    identification_notes: tuple[str, ...]


def _as_output(value: np.ndarray) -> np.ndarray | float:
    if value.ndim == 0:
        return float(value)
    return value


def forward_premium(
    spot_log: np.ndarray | float,
    forward_log: np.ndarray | float,
    maturity: float,
) -> np.ndarray | float:
    """Return annualized directed forward premium ``rho``."""

    if maturity <= 0.0:
        raise ValueError("maturity must be strictly positive.")
    value = (np.asarray(forward_log, dtype=np.float64) - np.asarray(spot_log, dtype=np.float64)) / float(maturity)
    return _as_output(value)


def model_wedge_chi(
    source_yield: np.ndarray | float,
    target_yield: np.ndarray | float,
    rho: np.ndarray | float,
) -> np.ndarray | float:
    """Return ``chi^{i/j} = (r^j-rho^{i/j})-r^i``."""

    value = (
        np.asarray(target_yield, dtype=np.float64)
        - np.asarray(rho, dtype=np.float64)
        - np.asarray(source_yield, dtype=np.float64)
    )
    return _as_output(value)


def market_residual_basis(chi: np.ndarray | float) -> np.ndarray | float:
    """Return market residual ``x_m=-chi``."""

    return _as_output(-np.asarray(chi, dtype=np.float64))


def government_bond_wedge(
    source_convenience_yield: np.ndarray | float,
    target_convenience_yield: np.ndarray | float,
    chi: np.ndarray | float,
) -> np.ndarray | float:
    """Return ``Phi^{i/j,G}=(lambda^i-lambda^j)+chi^{i/j}``."""

    value = (
        np.asarray(source_convenience_yield, dtype=np.float64)
        - np.asarray(target_convenience_yield, dtype=np.float64)
        + np.asarray(chi, dtype=np.float64)
    )
    return _as_output(value)


def directed_pair_measurement(
    *,
    source: CurrencyCode,
    target: CurrencyCode,
    maturity: float,
    spot_log: np.ndarray | float,
    forward_log: np.ndarray | float,
    source_yield: np.ndarray | float,
    target_yield: np.ndarray | float,
    source_convenience_yield: np.ndarray | float = 0.0,
    target_convenience_yield: np.ndarray | float = 0.0,
) -> DirectedPairMeasurement:
    """Evaluate all deterministic formulas for one directed pair."""

    rho = forward_premium(spot_log, forward_log, maturity)
    chi = model_wedge_chi(source_yield, target_yield, rho)
    market_residual = market_residual_basis(chi)
    phi = government_bond_wedge(source_convenience_yield, target_convenience_yield, chi)
    return DirectedPairMeasurement(
        source=source,
        target=target,
        maturity=float(maturity),
        rho=rho,
        chi=chi,
        market_residual=market_residual,
        government_bond_wedge=phi,
    )


def reverse_directed_pair_measurement(measurement: DirectedPairMeasurement) -> DirectedPairMeasurement:
    """Return the reciprocal-pair measurement when yields are held fixed."""

    return DirectedPairMeasurement(
        source=measurement.target,
        target=measurement.source,
        maturity=measurement.maturity,
        rho=_as_output(-np.asarray(measurement.rho, dtype=np.float64)),
        chi=_as_output(-np.asarray(measurement.chi, dtype=np.float64)),
        market_residual=_as_output(-np.asarray(measurement.market_residual, dtype=np.float64)),
        government_bond_wedge=_as_output(-np.asarray(measurement.government_bond_wedge, dtype=np.float64)),
    )


def country_yield_row(currency: CurrencyCode, maturity: float) -> ThreeCurrencyObservationRow:
    """Return row metadata for one country-yield observation."""

    return ThreeCurrencyObservationRow(
        row_id=f"country_yield:{currency}:{float(maturity):.8g}:observed",
        row_kind="country_yield",
        source=currency,
        target=None,
        maturity=float(maturity),
        observed=True,
        quote_convention=f"{currency} yield",
        model_sign_convention="positive continuously compounded annualized yield",
        measurement_error_group=COUNTRY_YIELD_GROUP,
        identification_status="Identified",
    )


def triangle_diagnostic_row(maturity: float, *, observed: bool) -> ThreeCurrencyObservationRow:
    """Return row metadata for the full-triangle observed diagnostic."""

    status = "Identified" if observed else "Untrusted"
    return ThreeCurrencyObservationRow(
        row_id=f"triangle_diagnostic:kappa:{float(maturity):.8g}:{'observed' if observed else 'derived'}",
        row_kind="triangle_diagnostic",
        source=None,
        target=None,
        maturity=float(maturity),
        observed=observed,
        quote_convention="kappa=w01-w02+w12",
        model_sign_convention="observed residual; structural interpretation requires measurement-error separation",
        measurement_error_group=TRIANGLE_DIAGNOSTIC_GROUP,
        identification_status=status,
        notes=("Full-triangle residual is observed but not automatically structural.",)
        if observed
        else ("USD-star missing cross edge, so kappa is not data-identified.",),
    )


def edge_rows_for_mode(
    mode: ObservationMode,
    maturities: np.ndarray,
    graph: ThreeCurrencyGraph | None = None,
) -> tuple[tuple[ThreeCurrencyObservationRow, ...], tuple[ThreeCurrencyObservationRow, ...], tuple[ThreeCurrencyObservationRow, ...]]:
    """Return observed, derived, and diagnostic rows for an edge observation mode."""

    graph = canonical_three_currency_graph() if graph is None else graph
    maturities = np.asarray(maturities, dtype=np.float64)
    if maturities.ndim != 1 or np.any(maturities <= 0.0):
        raise ValueError("maturities must be a one-dimensional positive array.")

    observed_rows: list[ThreeCurrencyObservationRow] = []
    derived_rows: list[ThreeCurrencyObservationRow] = []
    diagnostic_rows: list[ThreeCurrencyObservationRow] = []
    if mode == "usd_star":
        observed_pairs: tuple[tuple[CurrencyCode, CurrencyCode], ...] = (("USD", "EUR"), ("USD", "JPY"))
        for maturity in maturities:
            for source, target in observed_pairs:
                graph.edge_index_ignoring_orientation(source, target)
                observed_rows.append(edge_row_metadata(source, target, maturity=float(maturity), observed=True))
            derived_rows.append(zero_cycle_implied_cross_edge(0.0, 0.0, maturity=float(maturity)).row)
            diagnostic_rows.append(triangle_diagnostic_row(float(maturity), observed=False))
        return tuple(observed_rows), tuple(derived_rows), tuple(diagnostic_rows)
    if mode == "full_triangle":
        for maturity in maturities:
            for edge in graph.edges:
                observed_rows.append(edge_row_metadata(edge.source, edge.target, maturity=float(maturity), observed=True))
            diagnostic_rows.append(triangle_diagnostic_row(float(maturity), observed=True))
        return tuple(observed_rows), tuple(derived_rows), tuple(diagnostic_rows)
    raise ValueError(f"unsupported observation mode {mode!r}")


def observation_contract(
    mode: ObservationMode,
    maturities: np.ndarray,
    *,
    measurement_noise_std: float = DEFAULT_MEASUREMENT_NOISE_STD,
    graph: ThreeCurrencyGraph | None = None,
) -> ObservationContract:
    """Return the deterministic observed/derived row contract for a mode."""

    if measurement_noise_std <= 0.0:
        raise ValueError("measurement_noise_std must be strictly positive.")
    observed, derived, diagnostics = edge_rows_for_mode(mode, maturities, graph)
    if mode == "usd_star":
        notes = (
            "Observed edge rows are w01 and w02 only.",
            "EUR/JPY is a derived zero-cycle implication and is Not data-identified.",
            "USD-star kappa is Untrusted because the cross edge is missing.",
        )
    else:
        notes = (
            "All three directed edge rows are observed.",
            "kappa_obs is an observed residual, not automatically a structural cycle wedge.",
        )
    return ObservationContract(
        mode=mode,
        observed_edge_rows=observed,
        derived_edge_rows=derived,
        diagnostic_rows=diagnostics,
        measurement_noise_std=float(measurement_noise_std),
        identification_notes=notes,
    )


def triangle_observed_residual(edge_wedges: np.ndarray, graph: ThreeCurrencyGraph | None = None) -> np.ndarray | float:
    """Return observed full-triangle residual from observed edge rows."""

    return triangle_diagnostic(edge_wedges, graph)
