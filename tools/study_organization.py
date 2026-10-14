#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.special import expit
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from causalbank.organization import Candidate,materialize,organize


def fixture(rng,n,case):
    x,w=rng.normal(size=(2,n)); action=rng.binomial(1,expit(.7*x))
    y=20*action+30*x+rng.normal(scale=5,size=n)
    records=[]; decisions=[]; links={}
    for i in range(n):
        entity=str(i); links[entity]=str(i//2)
        decisions.append({"decision_id":entity,"entity":entity,"at":10})
        def record(record_id,version,event,available,value):
            return {"source":"ledger","record_id":record_id,"entity":entity,"version":version,
                    "clock_a":event,"clock_b":available,"value":float(value),"currency":"USD"}
        records.append(record("latest",1,5,6,x[i]))
        records.append(record("latest",2,5,12,x[i]+2*action[i]))
        if case=="ambiguous_aggregation":
            records.append(record("earlier",1,3,4,w[i]))
        if case=="accounting_resolves_flow":
            records[-2]["value"]=float(x[i]-w[i])
            records.append(record("earlier",1,3,4,w[i]))
    grammar={"clock_pairs":[["clock_a","clock_b"],["clock_b","clock_a"]],
             "revisions":["latest_available","append"],"aggregations":["stock","flow"],"units":["account","household"],
             "record_keys":["entity_record","record"]}
    declared={"event_clock":"clock_a","available_clock":"clock_b","revision":"latest_available","aggregation":"stock","unit":"account"}
    constraints={"declared":declared,"event_precedes_availability":True,"monotone_revision_publication":True,
                 "hints":{"aggregation":"flow","unit":"household"}}
    if case=="clock_order":
        del declared["event_clock"]; del declared["available_clock"]
    if case in ("ambiguous_aggregation","accounting_resolves_flow"):
        del declared["aggregation"]
    if case=="ambiguous_household":
        del declared["unit"]
    if case=="accounting_resolves_flow":
        constraints["reconciliation"]={str(i):float(x[i]) for i in range(n)}
    oracle=Candidate("clock_a","clock_b","latest_available","flow" if case=="accounting_resolves_flow" else "stock","account")
    return records,decisions,links,grammar,constraints,oracle,x,action,y


def effect(x,a,y):
    return float(np.linalg.lstsq(np.column_stack((np.ones(len(a)),a,x)),y,rcond=None)[0][1])


def main():
    spec_path=ROOT/"docs/studies/d-experiment-v1.json"; spec=json.loads(spec_path.read_text()); results=[]
    with threadpool_limits(limits=1):
        for ci,case in enumerate(spec["cases"]):
            rows=[]; start=time.perf_counter()
            for rep in range(spec["repetitions"]):
                rng=np.random.default_rng(np.random.SeedSequence([spec["seed"],ci,rep]))
                raw,decisions,links,grammar,constraints,oracle,x,a,y=fixture(rng,spec["entities"],case)
                result=organize(raw,decisions,grammar,constraints,links=links)
                oracle_view=materialize(raw,decisions,oracle,links=links)
                values=np.array([r["value"] for r in oracle_view])
                fits=[effect(np.array([r["value"] for r in candidate["view"]]),a,y) for candidate in result["survivors"]]
                accepted=result["status"]=="accepted_view"
                rows.append({"status":result["status"],"accepted_wrong":accepted and result["survivors"][0]["view"]!=oracle_view,
                             "oracle_retained":any(r["view"]==oracle_view for r in result["survivors"]),
                             "oracle_error":effect(values,a,y)-spec["effect"],"top_error":fits[0]-spec["effect"],
                             "retrospective_error":effect(x+2*a,a,y)-spec["effect"],
                             "estimate_range":max(fits)-min(fits),"material_views":result["material_views"]})
            result={"case":case,"seconds":time.perf_counter()-start,
                    "accepted_view_fraction":float(np.mean([r["status"]=="accepted_view" for r in rows])),
                    "accepted_wrong_view_fraction":float(np.mean([r["accepted_wrong"] for r in rows])),
                    "oracle_survival_fraction":float(np.mean([r["oracle_retained"] for r in rows])),
                    "abstention_fraction":float(np.mean([r["status"]=="abstain" for r in rows])),
                    "oracle_ols_rmse":float(np.sqrt(np.mean([r["oracle_error"]**2 for r in rows]))),
                    "forced_top_view_ols_rmse":float(np.sqrt(np.mean([r["top_error"]**2 for r in rows]))),
                    "retrospective_revision_ols_rmse":float(np.sqrt(np.mean([r["retrospective_error"]**2 for r in rows]))),
                    "mean_range_of_alternative_estimates":float(np.mean([r["estimate_range"] for r in rows])),"records":rows}
            results.append(result); print(json.dumps({k:v for k,v in result.items() if k!="records"}),flush=True)
    files=[spec_path,Path(__file__),ROOT/"src/causalbank/organization.py"]
    (ROOT/"docs/studies/d-results.json").write_text(json.dumps({"spec":spec,"results":results,
        "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+"\n")


if __name__=="__main__":
    main()
