"""Explicit identification, mature observations and group-safe analysis inputs."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields, replace
from datetime import timedelta

from finmarketing.core.types import canonical, digest, instant, number, require, text
from finmarketing.toolkit import Target, parse_record


def exact(cls, value):
    require(type(value) is dict and set(value) == {f.name for f in fields(cls)}, "invalid_causal_fields")
    return dict(value)


def sha(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


@dataclass(frozen=True)
class Identification:
    assignment: str
    exchangeability: str
    consistency: bool
    interference: str
    sampling: str
    basis: str

    def __post_init__(self):
        require(self.assignment in {"independent_bernoulli", "observational", "constrained", "unknown"}, "invalid_causal_assignment")
        require(self.exchangeability in {"randomized", "conditional", "unknown"}
                and type(self.consistency) is bool, "invalid_identification_assumptions")
        require(self.interference in {"none", "within_group", "unknown"}
                and self.sampling in {"independent_groups", "unknown"} and text(self.basis), "invalid_identification_basis")
        require((self.assignment == "independent_bernoulli") == (self.exchangeability == "randomized"),
                "inconsistent_randomization_assumption")

    def require_identified(self):
        require(self.consistency and self.interference != "unknown"
                and self.exchangeability != "unknown", "causal_identification_not_established")
        require(self.sampling == "independent_groups" and self.assignment in {"independent_bernoulli", "observational"},
                "unsupported_causal_dependence_law")

    @property
    def identification_id(self):
        return "identification-" + digest(asdict(self))


@dataclass(frozen=True)
class CausalData:
    target: Target
    permission_id: str
    identification: Identification
    columns: tuple[str, ...]
    feature_roles: tuple[str, ...]
    matrix: tuple[tuple[float, ...], ...]
    treatment: tuple[int, ...]
    outcomes: tuple[float, ...]
    row_ids: tuple[str, ...]
    groups: tuple[str, ...]
    feature_available: tuple[str, ...]
    assigned_at: tuple[str, ...]
    outcome_available: tuple[str, ...]
    horizon_days: int
    as_of: str
    partition: str
    source_digest: str
    transform_digest: str
    known_propensity: tuple[float, ...] | None = None

    def __post_init__(self):
        require(type(self.target) is Target and self.target.kind == "causal_effect", "causal_target_required")
        require(type(self.identification) is Identification and text(self.permission_id)
                and sha(self.source_digest) and sha(self.transform_digest), "invalid_causal_lineage")
        require(type(self.columns) is tuple and bool(self.columns) and len(set(self.columns)) == len(self.columns)
                and all(text(c) for c in self.columns), "invalid_causal_columns")
        require(type(self.feature_roles) is tuple and len(self.feature_roles) == len(self.columns)
                and all(r == "pretreatment" for r in self.feature_roles), "post_treatment_adjustment_forbidden")
        require(type(self.matrix) is tuple and bool(self.matrix) and all(type(r) is tuple and len(r) == len(self.columns)
                and all(number(x) for x in r) for r in self.matrix), "invalid_causal_matrix")
        n = len(self.matrix)
        for values in (self.row_ids, self.groups, self.feature_available, self.assigned_at, self.outcome_available):
            require(type(values) is tuple and len(values) == n and all(text(v) for v in values), "invalid_causal_rows")
        require(len(set(self.row_ids)) == n, "duplicate_causal_row")
        require(type(self.treatment) is tuple and len(self.treatment) == n
                and all(type(a) is int and a in (0, 1) for a in self.treatment), "binary_assigned_action_required")
        require(type(self.outcomes) is tuple and len(self.outcomes) == n
                and all(number(y) for y in self.outcomes), "complete_mature_outcomes_required")
        require(type(self.horizon_days) is int and self.horizon_days >= 0
                and self.target.economic.horizon == f"{self.horizon_days}d", "causal_horizon_mismatch")
        require(self.partition in {"train", "validation", "test"}, "invalid_causal_partition")
        cutoff = instant(self.as_of)
        for f, a, y in zip(self.feature_available, self.assigned_at, self.outcome_available, strict=True):
            require(instant(f) < instant(a) and instant(a)+timedelta(days=self.horizon_days) <= instant(y) <= cutoff,
                    "causal_temporal_leakage_or_immaturity")
        require(self.known_propensity is None or type(self.known_propensity) is tuple and len(self.known_propensity) == n
                and all(number(p) and 0 <= p <= 1 for p in self.known_propensity), "invalid_known_propensity")
        if self.identification.assignment == "independent_bernoulli":
            require(self.known_propensity is not None, "randomized_probabilities_required")
            # A declared randomized group is one draw, including repeated members.
            grouped = {}
            for g, a, p in zip(self.groups, self.treatment, self.known_propensity, strict=True):
                require(g not in grouped or grouped[g] == (a, p), "inconsistent_group_randomization")
                grouped[g] = a, p
        if self.identification.interference == "within_group":
            grouped = {}
            for group, action in zip(self.groups, self.treatment, strict=True):
                require(group not in grouped or grouped[group] == action,
                        "mixed_group_exposure_not_supported")
                grouped[group] = action

    def to_record(self):
        value = asdict(self)
        value["target"] = self.target.to_record()
        return json.loads(canonical({"version": "causal-data.v1", "payload": value}))

    @classmethod
    def from_record(cls, record):
        require(type(record) is dict and set(record) == {"version", "payload"}
                and record["version"] == "causal-data.v1", "unsupported_causal_data")
        value = exact(cls, record["payload"])
        value["target"] = parse_record(value["target"])
        value["identification"] = Identification(**exact(Identification, value["identification"]))
        for name in ("columns", "feature_roles", "treatment", "outcomes", "row_ids", "groups",
                     "feature_available", "assigned_at", "outcome_available", "known_propensity"):
            if value[name] is not None:
                require(type(value[name]) is list, "causal_array_required")
                value[name] = tuple(value[name])
        require(type(value["matrix"]) is list and all(type(r) is list for r in value["matrix"]), "causal_array_required")
        value["matrix"] = tuple(tuple(r) for r in value["matrix"])
        return cls(**value)

    @property
    def content_digest(self):
        return digest(self.to_record())

    @property
    def schema_digest(self):
        return digest({"columns": self.columns, "roles": self.feature_roles, "target": self.target.to_record(),
                       "transform": self.transform_digest, "permission": self.permission_id,
                       "identification": {k: v for k, v in asdict(self.identification).items() if k != "basis"}})

    def subset(self, indices):
        indices = tuple(indices)
        require(bool(indices) and all(type(i) is int and 0 <= i < len(self.matrix) for i in indices)
                and len(set(indices)) == len(indices), "invalid_causal_subset")
        values = {name: tuple(getattr(self, name)[i] for i in indices) for name in
                  ("matrix", "treatment", "outcomes", "row_ids", "groups", "feature_available", "assigned_at", "outcome_available")}
        values["known_propensity"] = None if self.known_propensity is None else tuple(self.known_propensity[i] for i in indices)
        return replace(self, **values)

    def require_after(self, training):
        require(type(training) is CausalData and training.schema_digest == self.schema_digest, "incompatible_causal_schema")
        require(not set(training.row_ids) & set(self.row_ids) and not set(training.groups) & set(self.groups),
                "causal_evaluation_group_overlap")
        require(max(map(instant, training.outcome_available)) < min(map(instant, self.assigned_at)),
                "causal_evaluation_future_leakage")


@dataclass(frozen=True)
class CausalConfig:
    folds: int = 5
    seed: int = 20261004
    overlap_floor: float = .02
    confidence_level: float = .95
    minimum_groups: int = 20
    singular_ratio_min: float = 1e-10

    def __post_init__(self):
        require(type(self.folds) is int and 2 <= self.folds <= 20
                and type(self.seed) is int and 0 <= self.seed < 2**63, "invalid_causal_folds")
        require(number(self.overlap_floor) and 0 < self.overlap_floor < .5
                and number(self.confidence_level) and 0 < self.confidence_level < 1, "invalid_causal_precision")
        require(type(self.minimum_groups) is int and self.minimum_groups >= 2
                and number(self.singular_ratio_min) and 0 < self.singular_ratio_min < 1, "invalid_causal_numeric_bound")


DEFAULT_CONFIG = CausalConfig()
