#!/usr/bin/env python3
"""Read public CSV/JSON and Python AST as data; never execute upstream code."""
import ast,csv,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'docs/literature/raw'
def calculate():
    rows=list(csv.DictReader((RAW/'exec23_gist_file_9.txt').open()))
    summary=list(csv.DictReader((RAW/'exec23_gist_file_10.txt').open()))
    tasks=json.loads((RAW/'exec23_gist_file_7.json').read_text())
    tools=json.loads((RAW/'exec23_gist_file_8.json').read_text())
    assert len(rows)==5040 and len(tasks)==120 and len(tools)==32
    assert len({(r['model'],r['method'],r['task_id']) for r in rows})==5040
    assert all(int(r['tokens'])>0 and int(r['tokens'])==int(r['input_tokens'])+int(r['output_tokens']) for r in rows)
    taskids={t['task_id']:t for t in tasks}
    assert all(r['task_id'] in taskids and r['request_type']==taskids[r['task_id']]['request_type'] for r in rows)
    methods={}
    for item in summary:
        name=item['method'];group=[r for r in rows if r['method']==name];assert len(group)==int(item['n'])==840
        for field in ['success','wrong_goal_execution','avg_tools_exposed','wrong_tools','clarification_count','unnecessary_clarification','input_tokens','output_tokens','tokens']:
            mean=sum(float(r[field]) for r in group)/len(group)
            assert math.isclose(mean,float(item[field]),rel_tol=1e-12,abs_tol=1e-10),(name,field)
        methods[name]=dict(rows=len(group),success_count=sum(int(r['success']) for r in group),wrong_goal_count=sum(int(r['wrong_goal_execution']) for r in group),mean_tokens=str(F(sum(int(r['tokens']) for r in group),len(group))))
    assert methods['gist_cmtf']['success_count']==815 and methods['gist_cmtf']['wrong_goal_count']==21
    assert methods['top_goal_cmtf']['success_count']==673 and methods['top_goal_cmtf']['wrong_goal_count']==163
    assert methods['semantic_goal_cmtf']['success_count']==696
    errors=Counter(r['error'] for r in rows)
    assert errors==Counter({r['error']:int(r['count']) for r in csv.DictReader((RAW/'exec23_gist_file_11.txt').open())})
    source=(RAW/'exec23_gist_file_5.txt').read_text();tree=ast.parse(source);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    init=functions['initial_goal_for_method'];run=functions['run_one'];main=functions['main']
    assert 'rt in {"ambiguous_goal", "missing_variable", "clarification_required"}' in ast.get_source_segment(source,init)
    assert 'selected_goal = true_goal' in ast.get_source_segment(source,run)
    assert 'task.get("gold_path", [])' in ast.get_source_segment(source,run)
    assert all('gold_path' not in t and 'gold_chains' in t for t in tasks)
    fieldnames=next(ast.literal_eval(n.value) for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fieldnames' for t in n.targets))
    csv_fields=list(rows[0]);mismatches=[r for r in rows if r['method']=='gist_cmtf' and r['request_type']!='explicit_goal' and int(r['clarification_count'])==0]
    assert len(mismatches)==53
    total_wrong=sum(int(r['wrong_tools']) for r in rows);assert total_wrong==3520
    default_models=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DEFAULT_MODELS' for t in n.targets))
    delta_success=F(815-673,840);extra_tokens=F(methods['gist_cmtf']['mean_tokens'])-F(methods['top_goal_cmtf']['mean_tokens'])
    extra_clar=F(sum(int(r['clarification_count']) for r in rows if r['method']=='gist_cmtf')-sum(int(r['clarification_count']) for r in rows if r['method']=='top_goal_cmtf'),840)
    benefit=10*delta_success;token_charge=F(1,1000)*extra_tokens;net_low=benefit-token_charge-2*extra_clar;net_high=benefit-token_charge-6*extra_clar
    assert net_low>0 and net_high<0
    return dict(kind='independent_data_and_static_source_review',native_execution=False,rows=5040,tasks=120,tools=32,unique_run_keys=5040,zero_token_rows=0,task_types=dict(Counter(t['request_type'] for t in tasks)),methods=methods,errors=dict(errors),
      source_data_gaps=dict(cutoff_runner_uses_annotated_request_type=True,clarification_substitutes_intended_goal=True,nonexplicit_gist_rows_without_clarification=53,nonexplicit_gist_denominator=560,all_tasks_lack_runner_gold_path=True,all_tasks_supply_gold_chains=True,reported_wrong_tool_total=total_wrong,csv_only_fields=sorted(set(csv_fields)-set(fieldnames)),runner_only_fields=sorted(set(fieldnames)-set(csv_fields)),default_models_not_in_saved_data=sorted(set(default_models)-{r['model'] for r in rows}),saved_models_not_in_defaults=sorted({r['model'] for r in rows}-set(default_models))),
      illustrative_economics=dict(extra_success_per_task=str(delta_success),extra_tokens_per_task=str(extra_tokens),extra_clarifications_per_task=str(extra_clar),stipulated_value_per_success='10',stipulated_cost_per_token='1/1000',net_with_clarification_cost2=str(net_low),net_with_clarification_cost6=str(net_high)),
      limits=['Saved final-data aggregation is reproducible; actual model calls, logs, cleaning and exact generating runner are not independently reproduced.','Static incompatibilities establish a provenance/replay gap, not fabricated results or observed native failures.','Stipulated economics uses descriptive averages, no causal superiority, confidence interval or measured cost claim.'])
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
