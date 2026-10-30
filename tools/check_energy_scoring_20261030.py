"""Static external-source review and authored-only execution witness."""
from pathlib import Path
import ast, hashlib, json
R=Path(__file__).resolve().parents[1]
RAW=R/'docs/literature/raw'
O=R/'docs/twelve-hour-closure/2026-10-29'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    out=O/'energy-scoring-review.json';assert not out.exists()
    data=RAW/'closure30_edge_humaneval_data.txt'
    rows=[json.loads(x)for x in data.read_text().splitlines()]
    structures=[]
    for row in rows:
        tree=ast.parse(row['test'])
        assert all(isinstance(x,(ast.Assign,ast.FunctionDef))for x in tree.body)
        checks=[x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='check']
        assert len(checks)==1
        assert not any(isinstance(x,ast.Expr)and isinstance(x.value,ast.Call)for x in tree.body)
        assert row['entry_point'].isidentifier()
        structures.append(dict(task=row['task_id'],entry_point=row['entry_point'],top_level_test_call=False))
    assert len(rows)==164
    for a,b in [('closure30_edge_paperera_evaluation.txt','closure30_edge_src_evaluate_HumanEval_py.txt'),
                ('closure30_edge_paperera_data.txt','closure30_edge_humaneval_data.txt')]:
        assert (RAW/a).read_bytes()==(RAW/b).read_bytes()
    # Only these authored literals execute; external files are parsed as data.
    good='def charge(principal, rate):\n    return principal * rate\n'
    bad='def charge(principal, rate):\n    return 0\n'
    definitions='def check(candidate):\n    assert candidate(100, 0.05) == 5\n    assert candidate(200, 0.10) == 20\n'
    def outcome(text):
        try:exec(compile(text,'authored-energy-witness','exec'),{})
        except AssertionError:return 'failed assertion'
        return 'passed execution'
    results={}
    for name,program in [('correct',good),('wrong',bad)]:
        results[name]=dict(definition_only=outcome(program+definitions),
                           invoked=outcome(program+definitions+'check(charge)\n'))
    assert results['wrong']['definition_only']=='passed execution'
    assert results['wrong']['invoked']=='failed assertion'
    assert results['correct']['invoked']=='passed execution'
    selected=['closure30_edge_src_evaluate_HumanEval_py.txt','closure30_edge_humaneval_data.txt',
              'closure30_hf_code_eval_py.txt','closure30_hf_execute_py.txt',
              'closure30_edge_paperera_evaluation.txt','closure30_edge_paperera_data.txt']
    out.write_text(json.dumps(dict(status='verified_static_defect_with_publication_limit',
       classification='IMPLEMENTATION_EVIDENCE_AND_PROJECT_COUNTEREXAMPLE',
       artifacts=[dict(path=str(RAW/n),sha256=sha(RAW/n))for n in selected],
       repository_commit='c11fe134709bd41a6a35344a988b9edc8d03016e',
       publication_era_commit='a130cb8583bed65e76c8190e3b6c3435bd79b07e',
       metric_commit='c447fc8eda9c62af501bfdc6988919571050d950',
       source_chain=['Evaluator supplies indata.test directly and never loads entry_point.',
         'All164 supplied tests define check(candidate) without invoking it.',
         'Metric concatenates candidate and reference; executor reports success on normal termination.',
         'An authored wrong function passes definition-only execution and fails when check is invoked.'],
       structures=structures,authored_witness=results,
       additional_concerns=['model_performance repeats the pooled pass_at_k for every model; row-level evaluation may still be regrouped downstream.',
         'Separate unused baseline helper has a column-name and unit mismatch; the principal postprocessor correctly multiplies idle watts by duration.',
         'RepositoryREADME sampling100kHz differs from paper2MHz; exact experimental configuration requires reconciliation.'],
       disposition='Quarantine comparator accuracy and joint accuracy-energy rankings pending reconstruction; do not use source as positive comparative support.',
       limitations=['No downloaded code or generated candidate was executed.',
         'Static history establishes the defect existed before preprint publication, not that every published number used that exact executable path.',
         'Actual model outputs, experimental dependency versions and manually repaired tests were not reconstructed.',
         'No claim of author intent or universal invalidity of separate energy measurements.'],
       remedy=['Append an explicit call to check(entry_point) in each reference under a controlled execution environment.',
         'Include deliberately incorrect,correct,syntax-failing andtimed-out controls in native qualification.',
         'Recompute per-task/per-model pass rates and paired energy ratios from the exact preserved outputs.',
         'Keep sensor failures, incomplete requests and failed tasks in denominator/accounting; report missing measurements explicitly.']),indent=2)+'\n')
    print(json.dumps(dict(status='pass',static_test_definitions=164,authored_witness=results)))
if __name__=='__main__':main()
