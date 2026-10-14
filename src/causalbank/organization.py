"""Finite observation-plan search. Evidence scores are not probabilities.

The caller supplies a grammar and scientific constraints. Acceptance refers
to this finite request/view, never universal recovery of economic semantics.
"""
from dataclasses import asdict, dataclass
from itertools import product
import hashlib
import json
import math


@dataclass(frozen=True)
class Candidate:
    event_clock: str
    available_clock: str
    revision: str
    aggregation: str
    unit: str
    record_key: str = "entity_record"


def candidates(grammar):
    return [Candidate(*clocks, revision, aggregation, unit, key)
            for clocks,revision,aggregation,unit,key in product(
                grammar["clock_pairs"],grammar["revisions"],
                grammar["aggregations"],grammar["units"],grammar.get("record_keys",["entity_record"]))]


def materialize(records,decisions,candidate,*,links=None,begin=-math.inf):
    """Strict availability; choose revisions before filtering [begin,decision).

    A stock returns its last economic observation; a flow sums distinct events.
    Links are supplied candidate maps, not inferred posterior entity matches.
    Missing is None, not zero. Records have one currency per request.
    """
    links=links or {}
    entity=lambda key: links.get(key,key) if candidate.unit=="household" else key
    index={}
    for row in records:
        index.setdefault(entity(row["entity"]),[]).append(row)
    result=[]
    for decision in decisions:
        end=decision["at"]; available=[r for r in index.get(entity(decision["entity"]),[])
                                      if r[candidate.available_clock]<end]
        if candidate.revision=="latest_available":
            latest={}
            for row in available:
                key=(row["source"],row["entity"] if candidate.record_key=="entity_record" else "",row["record_id"])
                if key not in latest or row["version"]>latest[key]["version"]:
                    latest[key]=row
            available=list(latest.values())
        selected=[r for r in available if begin<=r[candidate.event_clock]<end and not r.get("void",False)]
        if candidate.aggregation=="stock" and selected:
            latest_time=max(r[candidate.event_clock] for r in selected)
            selected=[r for r in selected if r[candidate.event_clock]==latest_time]
            if len({r["entity"] for r in selected})!=len(selected):
                raise ValueError("multiple_stock_records_for_same_entity_instant")
            # Several household accounts at that instant are additive stocks.
        result.append({"decision_id":decision["decision_id"],"unit_id":entity(decision["entity"]),
                       "value":math.fsum(r["value"] for r in selected) if selected else None,
                       "lineage":sorted([r["source"],r["entity"],r["record_id"],r["version"]] for r in selected)})
    return result


def organize(records,decisions,grammar,constraints,*,links=None):
    identities=[(r["source"],r["entity"],r["record_id"],r["version"]) for r in records]
    decision_ids=[d["decision_id"] for d in decisions]
    if len(set(identities))!=len(identities) or len(set(decision_ids))!=len(decision_ids):
        raise ValueError("duplicate revision or decision identity")
    if any(not math.isfinite(r["value"]) for r in records):
        raise ValueError("nonfinite value")
    if len({r["currency"] for r in records})!=1:
        raise ValueError("explicit currency conversion required")
    survivors=[]; rejected=[]
    for candidate in candidates(grammar):
        reasons=[]; declaration=asdict(candidate)
        if candidate.record_key=="record":
            keys=[(r["source"],r["record_id"],r["version"]) for r in records]
            if len(set(keys))!=len(keys):
                reasons.append("nonunique_candidate_key")
        for name,value in constraints.get("declared",{}).items():
            if declaration.get(name)!=value:
                reasons.append("declared_"+name)
        if constraints.get("event_precedes_availability") and any(
            r[candidate.event_clock]>r[candidate.available_clock] for r in records):
            reasons.append("chronology")
        # The finite grammar's version relation includes monotone publication.
        groups={}
        for row in records:
            groups.setdefault((row["source"],row["entity"],row["record_id"]),[]).append(row)
        if constraints.get("monotone_revision_publication") and any(
            a[candidate.available_clock]>b[candidate.available_clock]
            for group in groups.values() for a,b in zip(sorted(group,key=lambda r:r["version"]),
                                                        sorted(group,key=lambda r:r["version"])[1:])):
            reasons.append("revision_publication")
        if reasons:
            rejected.append({"candidate":declaration,"reasons":reasons}); continue
        try:
            view=materialize(records,decisions,candidate,links=links,begin=constraints.get("begin",-math.inf))
        except ValueError as error:
            rejected.append({"candidate":declaration,"reasons":[str(error)]}); continue
        if any(row["value"] is None or abs(row["value"]-constraints["reconciliation"][row["decision_id"]])>1e-9
               for row in view if row["decision_id"] in constraints.get("reconciliation",{})):
            rejected.append({"candidate":declaration,"reasons":["declared_accounting_identity"]}); continue
        # Rank for inspection only. No top-score threshold can certify semantics.
        score=sum(constraints.get("hints",{}).get(k)==v for k,v in declaration.items())
        signature={"aggregation":candidate.aggregation,"unit":candidate.unit,"rows":view}
        digest=hashlib.sha256(json.dumps(signature,sort_keys=True).encode()).hexdigest()
        survivors.append({"candidate":declaration,"evidence_score":score,"view":view,"view_sha256":digest})
    survivors.sort(key=lambda x:(-x["evidence_score"],json.dumps(x["candidate"],sort_keys=True)))
    groups={r["view_sha256"] for r in survivors}
    return {"status":"incompatible" if not survivors else "accepted_view" if len(groups)==1 else "abstain",
            "survivors":survivors,"rejected":rejected,"material_views":len(groups),
            "scope":"Conditional on the declared finite grammar/constraints; scores only order inspection. Accepted view applies to these decisions."}
