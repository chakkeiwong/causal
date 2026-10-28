"""Exact, proposal-owned graph-evaluation contracts; no external model execution.

These interfaces constrain trusted local callers. They are not a process sandbox
and cannot establish authentic labels or prevent a malicious caller from leaking
information outside the interfaces. Reported means condition on valid requests.
"""
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
import re

SPLITS = frozenset({'training', 'validation', 'evaluation'})


@dataclass(frozen=True)
class CaseRef:
    case_id: str
    graph_instance_id: str
    data_sha256: str
    split: str


@dataclass(frozen=True)
class Registry:
    cases: tuple[CaseRef, ...]
    nodes: frozenset[str]
    sha256: str

    def ids(self, split):
        if split not in SPLITS:
            raise ValueError('Unknown split')
        return frozenset(c.case_id for c in self.cases if c.split == split)


def registry(cases, nodes):
    cases, nodes = tuple(cases), frozenset(nodes)
    if not cases or len(nodes) < 2 or any(not isinstance(n, str) or not n for n in nodes):
        raise ValueError('Nonempty cases and at least two named nodes required')
    for c in cases:
        if not isinstance(c, CaseRef) or c.split not in SPLITS:
            raise ValueError('Invalid case identity or split')
        if not all(isinstance(v, str) and v for v in (c.case_id, c.graph_instance_id)):
            raise ValueError('Empty case or graph identity')
        if not isinstance(c.data_sha256, str) or not re.fullmatch('[0-9a-f]{64}', c.data_sha256):
            raise ValueError('Exact data SHA-256 required')
    for field in ('case_id', 'graph_instance_id', 'data_sha256'):
        if len({getattr(c, field) for c in cases}) != len(cases):
            raise ValueError('Repeated case, graph instance or data bytes: ' + field)
    if {c.split for c in cases} != SPLITS:
        raise ValueError('Declare all three splits')
    payload = dict(nodes=sorted(nodes), cases=[vars(c) for c in sorted(cases, key=lambda c: c.case_id)])
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return Registry(cases, nodes, digest)


def graph(edges, reg):
    if not isinstance(edges, frozenset):
        raise ValueError('Use an immutable edge set')
    for edge in edges:
        if (not isinstance(edge, tuple) or len(edge) != 2 or
                any(n not in reg.nodes for n in edge) or edge[0] == edge[1]):
            raise ValueError('Scoring universe is directed, known-node, off-diagonal edges')
    return edges


@dataclass(frozen=True)
class TruthView:
    registry_sha256: str
    split: str
    labels: tuple


def truth_view(reg, split, labels):
    if split not in ('validation', 'evaluation') or set(labels) != reg.ids(split):
        raise ValueError('Truth must exactly match its declared split')
    return TruthView(reg.sha256, split,
                     tuple((key, graph(labels[key], reg)) for key in sorted(labels)))


def labels_for(reg, view, split):
    if (not isinstance(view, TruthView) or view.registry_sha256 != reg.sha256 or
            view.split != split):
        raise ValueError('Wrong truth access or registry identity')
    labels = dict(view.labels)
    if len(labels) != len(view.labels) or set(labels) != reg.ids(split):
        raise ValueError('Duplicate, missing or additional truth identity')
    return {key: graph(value, reg) for key, value in labels.items()}


def exact_threshold(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError('Thresholds use finite exact rational numbers')
    value = Fraction(value)
    if not 0 <= value <= 1:
        raise ValueError('Threshold outside [0,1]')
    return value


def f1(prediction, truth):
    denominator = len(prediction) + len(truth)
    # The empty/empty convention is declared, rather than inherited silently.
    return Fraction(2 * len(prediction & truth), denominator) if denominator else Fraction(1)


@dataclass(frozen=True)
class Selection:
    registry_sha256: str
    threshold: Fraction
    validation_macro_f1: Fraction
    validation_cases: int
    tie_rule: str = 'smallest exact threshold among equal macro F1 values'


def choose_threshold(reg, validation_truth, candidates):
    """Accept validation labels only; case references contain no truth."""
    labels = labels_for(reg, validation_truth, 'validation')
    if not candidates:
        raise ValueError('At least one frozen candidate required')
    scored = []
    for threshold, predictions in candidates.items():
        threshold = exact_threshold(threshold)
        if set(predictions) != reg.ids('validation'):
            raise ValueError('Candidate predictions must exactly match validation identities')
        score = sum((f1(graph(predictions[key], reg), labels[key]) for key in sorted(labels)), Fraction()) / len(labels)
        scored.append((score, threshold))
    best_score = max(score for score, _ in scored)
    threshold = min(t for score, t in scored if score == best_score)
    return Selection(reg.sha256, threshold, best_score, len(labels))


def valid_mean(values, minimum_valid=1):
    if isinstance(minimum_valid, bool) or not isinstance(minimum_valid, int) or minimum_valid < 1:
        raise ValueError('Minimum valid denominator must be a positive integer')
    requested, missing, nonfinite, finite = 0, 0, 0, []
    for value in values:
        requested += 1
        if value is None:
            missing += 1
        elif isinstance(value, bool) or not isinstance(value, (int, Fraction, float)):
            raise ValueError('Metrics must be numeric values or explicit missing values')
        elif isinstance(value, float) and not math.isfinite(value):
            nonfinite += 1
        else:
            finite.append(Fraction(value))
    valid = len(finite)
    available = valid >= minimum_valid
    return dict(status='available' if available else 'unavailable', requested=requested,
                valid=valid, missing=missing, nonfinite=nonfinite, minimum_valid=minimum_valid,
                availability=Fraction(valid, requested) if requested else None,
                value=sum(finite, Fraction()) / valid if available else None,
                estimand='mean conditional on finite valid requests')


def evaluate(reg, selection, heldout_truth, predictions, minimum_valid=1):
    if not isinstance(selection, Selection) or selection.registry_sha256 != reg.sha256:
        raise ValueError('Selection registry mismatch')
    exact_threshold(selection.threshold)
    labels = labels_for(reg, heldout_truth, 'evaluation')
    if set(predictions) != reg.ids('evaluation'):
        raise ValueError('Retain every evaluation request; use None for failed predictions')
    scores, exact, rows = [], [], {}
    for key in sorted(labels):
        prediction = predictions[key]
        if prediction is None:
            score, match = None, None
        else:
            prediction = graph(prediction, reg)
            score, match = f1(prediction, labels[key]), int(prediction == labels[key])
        scores.append(score)
        exact.append(match)
        rows[key] = dict(status='unavailable' if score is None else 'available',
                         f1=score, exact_match=match)
    return dict(threshold=selection.threshold, requests=rows,
                macro_f1=valid_mean(scores, minimum_valid),
                exact_match_rate=valid_mean(exact, minimum_valid),
                native_execution=False)


def json_safe(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(val) for val in value]
    return value


def example():
    cases = [CaseRef(key, 'graph-' + key, hashlib.sha256(key.encode()).hexdigest(), split)
             for key, split in [('t', 'training'), ('v', 'validation'),
                                ('e1', 'evaluation'), ('e2', 'evaluation')]]
    reg = registry(cases, {'a', 'b'})
    edge = frozenset({('a', 'b')})
    valid = truth_view(reg, 'validation', {'v': edge})
    selection = choose_threshold(reg, valid, {Fraction(3, 4): {'v': edge}, Fraction(1, 2): {'v': edge}})
    heldout = truth_view(reg, 'evaluation', {'e1': edge, 'e2': frozenset({('b', 'a')})})
    result = evaluate(reg, selection, heldout, {'e1': edge, 'e2': None})
    return dict(evidence_type='authored public exact contract fixture',
                registry_sha256=reg.sha256, selected_threshold=selection.threshold,
                tie_rule=selection.tie_rule, evaluation=result,
                all_invalid=valid_mean([None, float('nan'), float('inf'), -float('inf')]),
                limitations=['No external package, model, bank data or empirical calibration.',
                            'Trusted interface contract; no process-level isolation or authentic-label proof.',
                            'Partial-valid averages are conditional and must retain availability.'])


if __name__ == '__main__':
    print(json.dumps(json_safe(example()), indent=2, allow_nan=False))
