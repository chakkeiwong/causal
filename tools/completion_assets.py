#!/usr/bin/env python3
"""Generate manuscript tables from preserved scientific results."""
import hashlib
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[1]


def main():
    response_path=ROOT/"docs/studies/a-results.json"; response=json.loads(response_path.read_text())
    lines=[r"\begin{tabular}{lrrrrrr}",r"\toprule",r"Case & Iid & HAC & Joint & Max & IV set & VAR\\",r"\midrule"]
    labels=["Strong, white","Strong, persistent","Persistent, long","Weak, persistent","Near unit","Invalid IV"]
    methods=["iid_pointwise","hac_pointwise","hac_bonferroni","hac_gaussian_max","weakiv_bonferroni","proxy_var_bonferroni"]
    for label,row in zip(labels,response["results"]):
        lines.append(label+" & "+" & ".join(f"{row['metrics'][name]['whole_curve_coverage']:.3f}" for name in methods)+r"\\")
    lines+=[r"\bottomrule",r"\end{tabular}"]
    response_table=ROOT/"docs/derivations/scientific_response_results.tex"; response_table.write_text("\n".join(lines)+"\n")
    path=ROOT/"docs/studies/workflow-results.json"; workflow=json.loads(path.read_text()); summary=[]
    lines=[r"\begin{tabular}{lrrr}",r"\toprule",r"Workload & Raw rows & Seconds & Peak MiB\\",r"\midrule"]
    names=["Response, small","Response, medium","Response, large","Learning, small","Learning, large","Latent, small","Latent, large","Temporal graph, small","Temporal graph, large"]
    for name,case in zip(names,workflow["spec"]["cases"]):
        runs=[r for r in workflow["results"] if r["case"]==case["id"]]
        details=[json.loads((ROOT/r["path"]).read_text()) for r in runs if r["exit_code"]==0]
        if len(details)!=workflow["spec"]["repeats"]: raise ValueError("Failed process must be accounted for before publishing summary")
        row={"case":case["id"],"raw_records":details[0]["raw_records"],"median_seconds":statistics.median(r["process_seconds"] for r in runs),
             "median_peak_mib":statistics.median(r["peak_rss_mib"] for r in details),"max_reference_error":max(r.get("fit_max_reference_error",r.get("reconstruction_max_error",0)) for r in details),
             "median_stages":{k:statistics.median(r["stages"][k] for r in details) for k in details[0]["stages"]},
             "max_parquet_bytes":max(r["parquet_bytes"] for r in details),"process_failures":len(runs)-len(details)}
        if case["kind"]=="latent":
            diagnostics=[r["fit"]["diagnostics"] for r in details]+[b["diagnostics"] for r in details for b in r["bootstrap"]]
            row.update(total_fits=len(diagnostics),optimizer_failures=sum(not d["optimizer_success"] for d in diagnostics),boundary_fits=sum(d["on_boundary"] for d in diagnostics),em_starts_at_cap=sum(s["em_cap"] for d in diagnostics for s in d["starts"]),max_average_score=max(d["score_mean_max"] for d in diagnostics))
        summary.append(row)
        lines.append(f"{name} & {row['raw_records']:,} & {row['median_seconds']:.2f} & {row['median_peak_mib']:.1f}"+r"\\")
    lines+=[r"\bottomrule",r"\end{tabular}"]
    workflow_table=ROOT/"docs/derivations/scientific_workflow_results.tex"; workflow_table.write_text("\n".join(lines)+"\n")
    (ROOT/"docs/studies/workflow-summary.json").write_text(json.dumps({"host":workflow["host"],"results":summary},indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__=="__main__": main()
