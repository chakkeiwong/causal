"""Versioned scientific records. Validation establishes meaning, not authority."""
from __future__ import annotations

import json
import math
import types
from dataclasses import asdict, dataclass, fields, is_dataclass
from datetime import date
from typing import get_args, get_origin, get_type_hints

from finmarketing.core.types import (
    Rejected,
    canonical,
    digest,
    instant,
    number,
    require,
    text,
)
from finmarketing.core.types import Target as EconomicTarget

VERSION = "toolkit-contracts.v1"


def _decode(annotation, value, *, wire):
    origin, args = get_origin(annotation), get_args(annotation)
    if origin is types.UnionType:
        for item in args:
            try:
                return _decode(item, value, wire=wire)
            except Rejected:
                pass
        raise Rejected("invalid_field_type")
    if annotation is type(None):
        require(value is None, "invalid_field_type")
    elif annotation is str:
        require(type(value) is str and bool(value.strip()), "invalid_field_type")
    elif annotation is bool:
        require(type(value) is bool, "invalid_field_type")
    elif annotation is int:
        require(type(value) is int, "invalid_field_type")
    elif annotation is float:
        try:
            require(number(value), "invalid_field_type")
        except OverflowError:
            raise Rejected("invalid_field_type") from None
    elif origin is tuple:
        require(type(value) is (list if wire else tuple), "invalid_field_type")
        require(len(args) == 2 and args[1] is Ellipsis, "unsupported_contract_type")
        return tuple(_decode(args[0], item, wire=wire) for item in value)
    elif is_dataclass(annotation):
        if not wire:
            require(type(value) is annotation, "invalid_field_type")
            return value
        require(type(value) is dict, "invalid_field_type")
        hints = get_type_hints(annotation)
        require(set(value) == {f.name for f in fields(annotation)}, "invalid_record_fields")
        return annotation(**{k: _decode(hints[k], v, wire=True) for k, v in value.items()})
    else:
        raise Rejected("unsupported_contract_type")
    return value


def _typed(record):
    for key, hint in get_type_hints(type(record)).items():
        _decode(hint, getattr(record, key), wire=False)


def _unique(values, *, nonempty=True):
    require((not nonempty or bool(values)) and len(values) == len(set(values)), "invalid_unique_items")


def _date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise Rejected("invalid_date") from None


def _sha(value):
    require(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "invalid_digest")


def _probabilities(values):
    require(bool(values) and all(0 <= v <= 1 for v in values), "invalid_probability")
    require(math.isclose(math.fsum(values), 1, rel_tol=0, abs_tol=1e-12), "unnormalized_probabilities")


class Contract:
    def to_record(self):
        return json.loads(canonical({"schema_version": VERSION, "kind": type(self).__name__, "payload": asdict(self)}))

    @property
    def content_digest(self):
        return digest(self.to_record())


@dataclass(frozen=True)
class Entity(Contract):
    workspace: str
    entity_type: str
    entity_id: str

    def __post_init__(self):
        _typed(self)


@dataclass(frozen=True)
class Field(Contract):
    name: str
    dtype: str
    role: str
    unit: str
    nullable: bool

    def __post_init__(self):
        _typed(self)
        require(self.dtype in {"string", "number", "integer", "boolean", "timestamp"}, "unsupported_field_dtype")
        require(self.role in {"key", "feature", "outcome", "valid_time", "available_time", "control"}, "unsupported_field_role")


@dataclass(frozen=True)
class SourceBatch(Contract):
    batch_id: str
    workspace: str
    entity_type: str
    source_owner: str
    source_kind: str
    use_basis: str
    source_digest: str
    received_at: str
    schema: tuple[Field, ...]
    record_ids: tuple[str, ...]
    accepted_ids: tuple[str, ...]
    rejected_ids: tuple[str, ...]
    permission_id: str

    def __post_init__(self):
        _typed(self)
        require(self.source_kind in {"synthetic", "licensed_public"}, "unsupported_data_boundary")
        _sha(self.source_digest)
        instant(self.received_at)
        _unique(tuple(f.name for f in self.schema))
        for items in (self.record_ids, self.accepted_ids, self.rejected_ids):
            _unique(items, nonempty=False)
        require(not set(self.accepted_ids) & set(self.rejected_ids), "conflicting_batch_disposition")
        require(set(self.accepted_ids) | set(self.rejected_ids) == set(self.record_ids), "incomplete_batch_disposition")


@dataclass(frozen=True)
class FeatureSnapshot(Contract):
    snapshot_id: str
    batch_ids: tuple[str, ...]
    workspace: str
    entity_type: str
    entity_ids: tuple[str, ...]
    feature_names: tuple[str, ...]
    outcome_names: tuple[str, ...]
    cutoff: str
    cutoff_sequence: int
    decision_at: str
    decision_sequence: int
    max_available_at: str
    max_available_sequence: int
    transform_id: str
    fitted_transform_snapshot_id: str | None
    partition: str
    dependence_unit: str
    label_horizon_days: int
    content_sha256: str
    permission_id: str

    def __post_init__(self):
        _typed(self)
        for items in (self.batch_ids, self.entity_ids, self.feature_names):
            _unique(items)
        _unique(self.outcome_names, nonempty=False)
        require(not set(self.feature_names) & set(self.outcome_names), "outcome_leakage")
        require(min(self.cutoff_sequence, self.decision_sequence, self.max_available_sequence, self.label_horizon_days) >= 0, "invalid_time_order")
        cutoff = (instant(self.cutoff), self.cutoff_sequence)
        decision = (instant(self.decision_at), self.decision_sequence)
        available = (instant(self.max_available_at), self.max_available_sequence)
        require(available <= cutoff < decision, "information_unavailable_at_decision")
        require(self.partition in {"train", "validation", "test", "serving"}, "invalid_partition")
        if self.partition == "train":
            require(self.fitted_transform_snapshot_id in {None, self.snapshot_id}, "foreign_training_transform")
        else:
            require(text(self.fitted_transform_snapshot_id) and self.fitted_transform_snapshot_id != self.snapshot_id, "training_transform_required")
        _sha(self.content_sha256)


@dataclass(frozen=True)
class Target(Contract):
    economic: EconomicTarget
    workspace: str
    entity_type: str
    kind: str

    def __post_init__(self):
        _typed(self)
        require(self.kind in {"prediction", "causal_effect", "conditional_scenario", "realized_contribution", "client_objective"}, "unsupported_target_kind")
        if self.economic.unit == "probability":
            require(self.kind == "prediction" and self.economic.currency is None, "probability_is_not_financial_value")
        if self.economic.unit == "currency":
            require(self.economic.currency is not None, "missing_financial_currency")

    def comparable(self, other):
        require(type(other) is Target and self == other, "incompatible_scientific_target")


@dataclass(frozen=True)
class Estimate(Contract):
    estimate_id: str
    target: Target
    kind: str
    value: float | None
    lower: float | None
    upper: float | None
    reason: str | None
    distribution_id: str | None
    identification_id: str | None
    snapshot_id: str
    model_id: str
    method_id: str
    code_version: str
    assumptions: tuple[str, ...]
    diagnostic_ids: tuple[str, ...]
    uncertainty: str
    permission_id: str

    def __post_init__(self):
        _typed(self)
        _unique(self.assumptions)
        _unique(self.diagnostic_ids)
        require(self.uncertainty in {"not_quantified", "sampling", "parameter", "outcome", "identified_set", "procedure"}, "invalid_uncertainty_kind")
        allowed = {"prediction": "prediction", "causal_contrast": "causal_effect", "conditional_simulation": "conditional_scenario"}
        require(self.kind in {*allowed, "identified_set", "distribution", "abstention"}, "unsupported_estimate_kind")
        if self.kind in allowed:
            require(self.target.kind == allowed[self.kind], "estimate_target_mismatch")
            require(self.value is not None and self.reason is self.distribution_id is None, "invalid_point_estimate")
        elif self.kind == "identified_set":
            require(self.value is self.reason is self.distribution_id is None and self.lower is not None and self.upper is not None, "invalid_identified_set")
        elif self.kind == "distribution":
            require(self.distribution_id is not None and self.value is self.lower is self.upper is self.reason is None, "invalid_distribution")
        else:
            require(self.reason is not None and self.value is self.lower is self.upper is self.distribution_id is None, "invalid_abstention")
        require((self.lower is None) == (self.upper is None), "incomplete_interval")
        if self.lower is not None:
            require(self.lower <= self.upper, "reversed_interval")
        if self.target.kind == "causal_effect" and self.kind != "abstention":
            require(self.identification_id is not None, "identification_required")
        if self.target.economic.unit == "probability":
            require(all(v is None or 0 <= v <= 1 for v in (self.value, self.lower, self.upper)), "invalid_probability")


@dataclass(frozen=True)
class CashEntry(Contract):
    event_id: str
    account: str
    owner: str
    category: str
    amount: float
    currency: str
    cash_date: str
    basis: str
    included_in_value: bool

    def __post_init__(self):
        _typed(self)
        _date(self.cash_date)
        require(len(self.currency) == 3 and self.currency.isupper(), "invalid_currency")
        require(self.category in {"revenue", "cost", "principal", "liability", "internal_transfer", "continuation"}, "invalid_account_category")
        require(self.basis in {"realized", "conditional", "predicted"}, "invalid_cash_basis")
        if self.category == "cost":
            require(self.amount <= 0, "cost_sign_error")


@dataclass(frozen=True)
class Value(Contract):
    value_id: str
    target: Target
    estimate_id: str | None
    mapping_id: str | None
    entries: tuple[CashEntry, ...]
    valuation_date: str
    cash_horizon_end: str
    continuation_from: str | None
    assumptions: tuple[str, ...]
    uncertainty_id: str
    permission_id: str

    def __post_init__(self):
        _typed(self)
        _unique(self.assumptions)
        require(self.target.economic.unit == "currency" and self.target.kind != "prediction", "financial_value_target_required")
        require((self.estimate_id is None) == (self.mapping_id is None), "value_mapping_required")
        if self.target.kind == "realized_contribution":
            require(self.estimate_id is None, "prediction_is_not_realized_cash")
        require(_date(self.valuation_date) <= _date(self.cash_horizon_end), "invalid_value_horizon")
        require(self.valuation_date == self.target.economic.origin, "valuation_origin_mismatch")
        _unique(tuple((e.event_id, e.account) for e in self.entries))
        for entry in self.entries:
            require(entry.currency == self.target.economic.currency and entry.owner == self.target.economic.finance_owner, "incompatible_ledger_target")
            require(_date(self.valuation_date) <= _date(entry.cash_date) <= _date(self.cash_horizon_end), "cash_outside_value_horizon")
            if self.target.economic.measure == "net_contribution" and entry.category in {"principal", "liability", "internal_transfer"}:
                require(not entry.included_in_value, "balance_movement_is_not_income")
            if self.target.kind == "realized_contribution":
                require(entry.basis == "realized", "prediction_is_not_realized_cash")
        if any(e.category == "continuation" for e in self.entries):
            require(self.continuation_from is not None and _date(self.continuation_from) > _date(self.cash_horizon_end), "overlapping_continuation")
        else:
            require(self.continuation_from is None, "unexpected_continuation")


@dataclass(frozen=True)
class Resource(Contract):
    name: str
    amount: float

    def __post_init__(self):
        _typed(self)
        require(self.amount >= 0, "invalid_resource")


@dataclass(frozen=True)
class Policy(Contract):
    policy_id: str
    target: Target
    snapshot_id: str
    estimate_id: str
    value_id: str
    validation_id: str
    code_version: str
    objective: str
    assumptions: tuple[str, ...]
    action_ids: tuple[str, ...]
    no_action: str
    limits: tuple[Resource, ...]
    valid_from: str
    valid_until: str
    permission_id: str

    def __post_init__(self):
        _typed(self)
        _unique(self.assumptions)
        _unique(self.action_ids)
        _unique(tuple(r.name for r in self.limits), nonempty=False)
        require(self.no_action in self.action_ids, "missing_no_action")
        require(instant(self.valid_from) < instant(self.valid_until), "invalid_policy_window")


@dataclass(frozen=True)
class Exclusion(Contract):
    action_id: str
    reason: str

    def __post_init__(self):
        _typed(self)


@dataclass(frozen=True)
class Opportunity(Contract):
    opportunity_id: str
    entity: Entity
    trigger: str
    target: Target
    policy_id: str
    snapshot_id: str
    estimate_id: str
    value_id: str
    decision_at: str
    expires_at: str
    eligible_actions: tuple[str, ...]
    removed_actions: tuple[Exclusion, ...]
    selected_action: str | None
    demands: tuple[Resource, ...]
    reasons: tuple[str, ...]
    uncertainty_id: str
    route: str
    permission_id: str
    override_reference: str | None

    def __post_init__(self):
        _typed(self)
        require((self.entity.workspace, self.entity.entity_type) == (self.target.workspace, self.target.entity_type), "incompatible_entity_scope")
        _unique(self.eligible_actions)
        _unique(tuple(e.action_id for e in self.removed_actions), nonempty=False)
        require(not set(self.eligible_actions) & {e.action_id for e in self.removed_actions}, "conflicting_action_eligibility")
        _unique(tuple(d.name for d in self.demands), nonempty=False)
        _unique(self.reasons)
        require(self.selected_action is None or self.selected_action in self.eligible_actions, "ineligible_action")
        require(instant(self.decision_at) < instant(self.expires_at), "expired_opportunity")


@dataclass(frozen=True)
class Outcome(Contract):
    outcome_id: str
    entity: Entity
    opportunity_id: str
    assignment_id: str
    action_id: str
    assigned_at: str
    delivery_status: str
    exposed_at: str | None
    observed_at: str
    maturity_at: str
    status: str
    measure: str
    value: float | None
    correction_of: str | None

    def __post_init__(self):
        _typed(self)
        assigned, observed, mature = instant(self.assigned_at), instant(self.observed_at), instant(self.maturity_at)
        require(assigned <= observed and assigned <= mature, "invalid_outcome_chronology")
        require(self.delivery_status in {"not_attempted", "attempted", "delivered", "failed", "suppressed"}, "invalid_delivery_status")
        if self.exposed_at is not None:
            require(self.delivery_status == "delivered" and assigned <= instant(self.exposed_at) <= observed, "invalid_exposure")
        require(self.status in {"pending", "censored", "mature"}, "invalid_outcome_status")
        if self.status == "mature":
            require(observed >= mature and self.value is not None, "immature_outcome")
        else:
            require(self.value is None, "missingness_is_not_zero")
        require(self.correction_of != self.outcome_id, "self_correction")


@dataclass(frozen=True)
class AssignmentLog(Contract):
    assignment_id: str
    decision_id: str
    unit: Entity
    eligible_actions: tuple[str, ...]
    chosen_action: str
    propensity: float
    assigned_at: str
    policy_id: str
    design_id: str
    snapshot_id: str
    randomization_unit: str
    dependence_unit: str
    constraint_digest: str
    probability_kind: str
    joint_probability: float | None
    joint_design_id: str | None
    reward_horizon_days: int

    def __post_init__(self):
        _typed(self)
        _unique(self.eligible_actions)
        require(self.chosen_action in self.eligible_actions, "action_not_logged_as_eligible")
        require(0 < self.propensity <= 1, "invalid_propensity")
        require(self.probability_kind in {"marginal", "conditional", "joint"}, "invalid_probability_kind")
        instant(self.assigned_at)
        _sha(self.constraint_digest)
        require(self.reward_horizon_days >= 0, "invalid_reward_horizon")
        require((self.joint_probability is None) == (self.joint_design_id is None), "incomplete_joint_log")
        if self.joint_probability is not None:
            require(0 < self.joint_probability <= 1, "invalid_joint_probability")
        if self.probability_kind == "joint":
            require(self.joint_probability is not None, "joint_log_required")


@dataclass(frozen=True)
class JointScenario(Contract):
    scenario_id: str
    target: Target
    variables: tuple[str, ...]
    outcomes: tuple[tuple[float, ...], ...]
    weights: tuple[float, ...]
    law_kind: str
    dependence_assumption: str
    source_digest: str
    uncertainty_kind: str
    applicability: str

    def __post_init__(self):
        _typed(self)
        _unique(self.variables)
        require(len(self.outcomes) == len(self.weights) and all(len(row) == len(self.variables) for row in self.outcomes), "joint_law_dimension_mismatch")
        _probabilities(self.weights)
        _sha(self.source_digest)
        require(self.law_kind in {"synthetic", "empirical", "parametric"}, "invalid_law_kind")
        require(self.uncertainty_kind in {"sampling", "parameter", "outcome", "procedure"}, "invalid_uncertainty_kind")


@dataclass(frozen=True)
class ObservationModel(Contract):
    observation_model_id: str
    scenario_id: str
    observations: tuple[str, ...]
    likelihoods: tuple[tuple[float, ...], ...]
    subsequent_actions: tuple[str, ...]
    update_rule: str
    information_cost: float
    cost_currency: str
    available_at: str
    decision_at: str
    assumptions: tuple[str, ...]

    def __post_init__(self):
        _typed(self)
        _unique(self.observations)
        _unique(self.subsequent_actions)
        _unique(self.assumptions)
        require(bool(self.likelihoods), "missing_observation_law")
        for row in self.likelihoods:
            require(len(row) == len(self.observations), "observation_dimension_mismatch")
            _probabilities(row)
        require(self.information_cost >= 0, "invalid_information_cost")
        require(len(self.cost_currency) == 3 and self.cost_currency.isupper(), "invalid_currency")
        require(instant(self.available_at) < instant(self.decision_at), "observation_after_decision")


RECORD_TYPES = {cls.__name__: cls for cls in (
    Entity, Field, SourceBatch, FeatureSnapshot, Target, Estimate, CashEntry,
    Value, Resource, Policy, Exclusion, Opportunity, Outcome, AssignmentLog,
    JointScenario, ObservationModel,
)}


def parse_record(record):
    """Parse an exact-version wire object; never import code named by a record."""
    require(type(record) is dict and set(record) == {"schema_version", "kind", "payload"}, "invalid_envelope")
    require(record["schema_version"] == VERSION, "unsupported_contract_version")
    require(type(record["kind"]) is str and record["kind"] in RECORD_TYPES, "unsupported_contract_kind")
    return _decode(RECORD_TYPES[record["kind"]], record["payload"], wire=True)


def validate_journey(batch, snapshot, estimate, value, policy, opportunity, outcome=None, assignment=None):
    """Check connected schema meaning. Stored references still need runtime validation."""
    for obj, cls in ((batch, SourceBatch), (snapshot, FeatureSnapshot), (estimate, Estimate),
                     (value, Value), (policy, Policy), (opportunity, Opportunity)):
        require(type(obj) is cls, "invalid_journey_object")
    scope = (batch.workspace, batch.entity_type)
    require(scope == (snapshot.workspace, snapshot.entity_type) == (estimate.target.workspace, estimate.target.entity_type), "incompatible_source_scope")
    require(batch.batch_id in snapshot.batch_ids, "snapshot_source_mismatch")
    require(instant(batch.received_at) <= instant(snapshot.cutoff), "batch_unavailable_at_cutoff")
    allowed_features = {f.name for f in batch.schema if f.role == "feature"}
    allowed_outcomes = {f.name for f in batch.schema if f.role == "outcome"}
    require(set(snapshot.feature_names) <= allowed_features and set(snapshot.outcome_names) <= allowed_outcomes, "snapshot_field_role_mismatch")
    require(snapshot.snapshot_id == estimate.snapshot_id == policy.snapshot_id == opportunity.snapshot_id, "snapshot_reference_mismatch")
    require(estimate.estimate_id == policy.estimate_id == opportunity.estimate_id, "estimate_reference_mismatch")
    require(value.estimate_id in {None, estimate.estimate_id}, "value_estimate_reference_mismatch")
    if value.estimate_id is not None:
        # A unit/measure conversion still refers to the same economic decision.
        # Reaggregation across horizons, owners or populations needs a new target.
        for name in ("population", "action", "comparator", "origin", "horizon",
                     "finance_owner", "capital_convention"):
            require(getattr(estimate.target.economic, name) == getattr(value.target.economic, name),
                    "incompatible_estimate_value_target")
        require(estimate.kind != "abstention", "abstention_has_no_value_mapping")
    if value.target.kind == "causal_effect":
        require(estimate.target.kind == "causal_effect" and estimate.identification_id is not None, "prediction_is_not_causal_value")
    require(value.value_id == policy.value_id == opportunity.value_id, "value_reference_mismatch")
    value.target.comparable(policy.target)
    policy.target.comparable(opportunity.target)
    require(scope == (value.target.workspace, value.target.entity_type), "incompatible_value_scope")
    require(opportunity.policy_id == policy.policy_id, "policy_reference_mismatch")
    require(opportunity.entity.entity_id in snapshot.entity_ids, "entity_missing_from_snapshot")
    require(instant(snapshot.decision_at) <= instant(opportunity.decision_at), "opportunity_precedes_snapshot")
    require(instant(policy.valid_from) <= instant(opportunity.decision_at) < instant(opportunity.expires_at) <= instant(policy.valid_until), "policy_not_current")
    require(set(opportunity.eligible_actions) <= set(policy.action_ids), "unknown_policy_action")
    require(set(opportunity.eligible_actions) | {e.action_id for e in opportunity.removed_actions}
            == set(policy.action_ids), "incomplete_action_disposition")
    require(policy.no_action in opportunity.eligible_actions, "missing_no_action")
    limits = {r.name: r.amount for r in policy.limits}
    require(all(d.name in limits and d.amount <= limits[d.name] for d in opportunity.demands), "invalid_resource_demand")
    require(len({obj.permission_id for obj in (batch, snapshot, estimate, value, policy, opportunity)}) == 1, "permission_reference_mismatch")
    if assignment is not None:
        require(type(assignment) is AssignmentLog, "invalid_assignment")
        require(assignment.unit == opportunity.entity and assignment.decision_id == opportunity.opportunity_id, "assignment_scope_mismatch")
        require(assignment.policy_id == policy.policy_id and assignment.snapshot_id == snapshot.snapshot_id, "assignment_version_mismatch")
        require(assignment.eligible_actions == opportunity.eligible_actions and assignment.chosen_action == opportunity.selected_action, "assignment_action_mismatch")
        require(instant(opportunity.decision_at) <= instant(assignment.assigned_at) < instant(opportunity.expires_at), "assignment_after_expiry")
    if outcome is not None:
        require(type(outcome) is Outcome and assignment is not None, "assignment_required_for_outcome")
        require(outcome.entity == opportunity.entity and outcome.opportunity_id == opportunity.opportunity_id, "outcome_scope_mismatch")
        require(outcome.assignment_id == assignment.assignment_id and outcome.action_id == assignment.chosen_action and outcome.assigned_at == assignment.assigned_at, "outcome_assignment_mismatch")
    return {"schema_version": VERSION, "passed": True, "evidence_kind": "contract_compatibility_only",
            "limits": "No model approval, causal identification, numerical valuation or dispatch authority established."}


def validate_observation(scenarios, observation):
    require(type(scenarios) is JointScenario and type(observation) is ObservationModel, "invalid_information_objects")
    require(scenarios.scenario_id == observation.scenario_id and len(scenarios.outcomes) == len(observation.likelihoods), "observation_scenario_mismatch")
    require(scenarios.target.economic.currency == observation.cost_currency, "incompatible_information_currency")
    return True
