#!/usr/bin/env python3
"""Bind completed study receipts and semantic checks; never assess scholarly sufficiency."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    studies=["a-results","a-extension-results","a-panel-results","b-latent-results","b-history-results","c-results","c-temporal-results","d-results","workflow-results"]
    receipts=["docs/studies/"+name+".json" for name in studies]+[
        "docs/reviews/scientific-completion-checks.json","docs/reviews/interface-qualification.json","docs/reviews/standalone-qualification.json"]
    issues=[]; inputs={}; verified=[]
    for name in receipts:
        path=ROOT/name; receipt=json.loads(path.read_text()); inputs[name]=digest(path)
        if receipt.get("status","pass")!="pass": issues.append("Nonpassing receipt: "+name)
        if not receipt.get("input_sha256"): issues.append("Missing input identity: "+name)
        for source,expected in receipt.get("input_sha256",{}).items():
            file=ROOT/source
            if not file.is_file() or digest(file)!=expected: issues.append("Stale input: "+name+" -> "+source)
            else: inputs[source]=expected
        verified.append({"path":name,"sha256":digest(path),"scope":receipt.get("scope","Synthetic experiment under its frozen model; adverse outcomes are evidence, not failed execution")})
    for name in ["docs/derivations/scientific_response_results.tex","docs/derivations/scientific_workflow_results.tex","docs/studies/workflow-summary.json","tools/completion_assets.py",str(Path(__file__).relative_to(ROOT))]:
        inputs[name]=digest(ROOT/name)
    result={"status":"pass" if not issues else "fail","issues":issues,"verified_receipts":verified,"input_sha256":inputs,
            "scope":"Current experiment/check/input byte closure. Passing includes adverse empirical findings and does not assert finite-sample coverage, general proof correctness or bank validity."}
    (ROOT/"docs/reviews/scientific-completion-verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"bound_inputs":len(inputs),"issues":issues},indent=2)); return bool(issues)


if __name__=="__main__": raise SystemExit(main())
