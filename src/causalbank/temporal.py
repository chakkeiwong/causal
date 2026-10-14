"""Bitemporal revision selection. Semantic declarations remain caller-owned."""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import json
import math


def clock(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError('TIMEZONE_REQUIRED')
    return dt


@dataclass(frozen=True)
class Event:
    event_id: str
    entity_id: str
    occurred_at: str
    available_at: str
    revision: int
    amount: float
    currency: str
    void: bool = False


@dataclass(frozen=True)
class Decision:
    decision_id: str
    entity_id: str
    decision_at: str


def compile_snapshot(events, decisions, *, lookback_days, currency, feed_complete):
    """Sum valid events in (decision-lookback, decision], known by decision.

    Select latest available revision BEFORE filtering economic time. A correction
    moving an event outside the window must not resurrect its old revision.
    This reference implementation prioritizes inspectable semantics over scale.
    """
    events=tuple(events); decisions=tuple(decisions)
    if feed_complete is not True:
        raise ValueError('SOURCE_COMPLETENESS_REQUIRED')
    if lookback_days <= 0:
        raise ValueError('POSITIVE_LOOKBACK_REQUIRED')
    seen = set(); owners = {}; indexed = {}
    for event in events:
        if any(not isinstance(key, str) or not key.strip() for key in (event.event_id, event.entity_id)) or not isinstance(event.revision, int) or isinstance(event.revision, bool) or event.revision < 1:
            raise ValueError('INVALID_EVENT_IDENTITY')
        if not math.isfinite(event.amount):
            raise ValueError('FINITE_AMOUNT_REQUIRED')
        if event.currency != currency:
            raise ValueError('CURRENCY_MISMATCH')
        clock(event.occurred_at); clock(event.available_at)
        key = (event.event_id, event.revision)
        if key in seen:
            raise ValueError('DUPLICATE_EVENT_REVISION')
        seen.add(key)
        if event.event_id in owners and owners[event.event_id] != event.entity_id:
            raise ValueError('EVENT_OWNER_CHANGED')
        owners[event.event_id] = event.entity_id
        indexed.setdefault(event.entity_id, {}).setdefault(event.event_id, []).append(event)
    rows=[]; used_decisions=set()
    for decision in decisions:
        if any(not isinstance(key, str) or not key.strip() for key in (decision.decision_id, decision.entity_id)):
            raise ValueError('INVALID_DECISION_IDENTITY')
        if decision.decision_id in used_decisions:
            raise ValueError('DUPLICATE_DECISION')
        used_decisions.add(decision.decision_id)
        end=clock(decision.decision_at); begin=end-timedelta(days=lookback_days)
        selected=[]
        for versions in indexed.get(decision.entity_id, {}).values():
            available=[e for e in versions if clock(e.available_at)<=end]
            if not available: continue
            event=max(available,key=lambda e:e.revision)
            if begin<clock(event.occurred_at)<=end and not event.void:
                selected.append(event)
        selected.sort(key=lambda e:e.event_id)
        rows.append({'decision_id':decision.decision_id,'entity_id':decision.entity_id,
                     'decision_at':decision.decision_at,'amount':math.fsum(e.amount for e in selected),
                     'currency':currency,'source_versions':[[e.event_id,e.revision] for e in selected]})
    payload={'events':sorted([asdict(e) for e in events],key=lambda e:(e['event_id'],e['revision'])),
             'decisions':[asdict(d) for d in decisions],'lookback_days':lookback_days,'currency':currency,'feed_complete':feed_complete,
             'availability_convention':'inclusive, assumed known at recorded instant'}
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'snapshot_id':digest,'rows':rows,'semantics':payload['availability_convention']}
