#!/usr/bin/env python3
"""Compare original and successor validators on one fixed state and adverse bindings."""
import copy,hashlib,inspect,json,time
from pathlib import Path
import run_program_checkpoint_v3 as controller
import run_with_review_context_cache_20261025 as repair
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=repair.ROOT;BASE=repair.BASE;run=controller.base;core=run.core

def main():
    assert not BASE.exists();BASE.mkdir()
    deps={'review':run.validate_review_binding,'receipt':run.validate_receipt,'ledger_receipt':run.ledger.validate_operation_receipt,'blockers':run.ledger.blockers,'dependency_blockers':run.ledger.dependency_blockers,'protocol':run.ledger.validate_protocol}
    contract=dict(functions={k:hashlib.sha256(inspect.getsource(f).encode()).hexdigest() for k,f in deps.items()},assumption='Called validators read state and receipts; only the private context results dictionary is assigned.',evidence=[ref(ROOT/'tools/run_program.py','Historical review replay'),ref(ROOT/'tools/run_program_reviews_v2.py','Historical receipt delegate'),ref(ROOT/'tools/causal_program_v14.py','Read-only prerequisite and receipt validation')])
    write(BASE/'source-contract.json',contract)
    (BASE/'original-review-function.py.txt').write_text(inspect.getsource(run.validate_review_binding))
    (BASE/'successor-review-function.py.txt').write_text(repair.adapted_source(run.validate_review_binding))
    state=core.read(ROOT,core.STATE);write(BASE/'captured-state.json',state);before=core.digest_object(state)
    start=time.monotonic();old_issues=run.validate_state(ROOT,state);old_time=time.monotonic()-start
    assert core.digest_object(state)==before and not old_issues,old_issues
    original=repair.install(run)
    start=time.monotonic();new_issues=run.validate_state(ROOT,state);new_time=time.monotonic()-start
    assert old_issues==new_issues and core.digest_object(state)==before
    graph,merged,_=run.combined(ROOT,state);merged_before=core.digest_object(merged)
    bindings=[]
    for key,records in state['execution_runtime']['review_history'].items():
        if key.startswith('PROPOSAL.') and records:bindings.append((key,records[-1]['result']))
    assert bindings
    def verdict(function,key,binding):
        try:function(ROOT,merged,graph,key,binding);return dict(status='pass')
        except Exception as e:return dict(status='rejected',type=type(e).__name__,message=str(e))
    tests=[]
    for key,binding in bindings:
        candidates=[('valid',binding)]
        wrong=copy.deepcopy(binding);wrong['outcome']='negative' if binding['outcome']=='pass' else 'pass';candidates.append(('outcome_mismatch',wrong))
        wrong=copy.deepcopy(binding);wrong['capabilities']=['invented_capability'];candidates.append(('capability_mismatch',wrong))
        wrong=copy.deepcopy(binding);wrong['sha256']='0'*64;candidates.append(('changed_evidence',wrong))
        wrong=copy.deepcopy(binding);wrong.setdefault('prerequisites',{})['NOT.DECLARED']=dict(binding);candidates.append(('undeclared_prerequisite',wrong))
        if binding.get('prerequisites'):
            wrong=copy.deepcopy(binding);first=next(iter(wrong['prerequisites']));wrong['prerequisites'][first]['outcome']='invalid';candidates.append(('saved_prerequisite_mismatch',wrong))
        for name,value in candidates:
            a=verdict(original,key,value);b=verdict(run.validate_review_binding,key,value)
            assert a==b,(key,name,a,b);assert core.digest_object(merged)==merged_before
            assert (name=='valid')==(b['status']=='pass'),(name,b)
            tests.append(dict(operation=key,case=name,verdict=b))
    write(BASE/'verification.json',dict(status='pass',original_full_validation_seconds=old_time,successor_full_validation_seconds=new_time,full_validation_issues=new_issues,state_unchanged=True,adverse_tests=tests,evidence=[ref(BASE/'captured-state.json','Identical state for full comparison'),ref(BASE/'source-contract.json','Exact read-only dependency functions'),ref(BASE/'original-review-function.py.txt','Preserved original'),ref(BASE/'successor-review-function.py.txt','Only private context copy changed'),ref(Path(__file__),'Equivalence and mutation checks')]))
    review=dict(status='pass_for_narrow_process_local_performance_repair',evidence=[ref(BASE/'verification.json','Full old/new and adverse equivalence'),ref(Path(repair.__file__),'Guarded process-local wrapper'),ref(ROOT/'docs/program/execution/2026-10-25/validation-profile-v1/profile-review.json','Observed full-state deepcopy bottleneck')],findings=['Every original validation condition and evidence binding retained.','Only top-level,execution-program and results maps copied; mutation isolation verified.','Original validator source remains unchanged; guarded source digest rejects changed delegates.','No persistent hash or acceptance-result trust; final publication controllers remain unmodified.'],limitations=['Future validator mutation requires a new review and guard update.'])
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(status='pass',original_seconds=round(old_time,3),successor_seconds=round(new_time,3),equivalence_tests=len(tests))))
if __name__=='__main__':main()
