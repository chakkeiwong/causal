#!/usr/bin/env python3
"""Avoid copying unrelated history when replaying a read-only review context.

All validation and source hashes remain. Only the three dictionaries on the
modified results path are copied. This is not a validation-result cache.
Historical controllers stay untouched; final publication checks stay unwrapped.
"""
import hashlib,inspect,json,runpy,sys,time
from pathlib import Path
from run_with_verified_hash_cache_20261025 import VerifiedHashCache
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/review-context-repair-v1'

def adapted_source(original):
    source=inspect.getsource(original)
    old='        context = copy.deepcopy(state)'
    new="        context = dict(state)\n        context['execution_program'] = dict(state['execution_program'])\n        context['execution_program']['results'] = dict(state['execution_program']['results'])"
    assert source.count(old)==1
    return source.replace(old,new)

def install(run):
    contract=json.loads((BASE/'source-contract.json').read_text())
    dependencies={'review':run.validate_review_binding,'receipt':run.validate_receipt,'ledger_receipt':run.ledger.validate_operation_receipt,'blockers':run.ledger.blockers,'dependency_blockers':run.ledger.dependency_blockers,'protocol':run.ledger.validate_protocol}
    for name,function in dependencies.items():
        digest=hashlib.sha256(inspect.getsource(function).encode()).hexdigest()
        assert digest==contract['functions'][name],('Historical validator source changed',name)
    source=adapted_source(run.validate_review_binding)
    namespace={};exec(compile(source,str(Path(__file__))+'::review-context','exec'),run.validate_review_binding.__globals__,namespace)
    previous=run.validate_review_binding;run.validate_review_binding=namespace['validate_review_binding']
    return previous

def main():
    if len(sys.argv)<2:raise SystemExit('Expected repository-local tool')
    target=Path(sys.argv[1]).resolve();assert target.is_relative_to(ROOT/'tools') and target.suffix=='.py'
    import run_program_checkpoint_v3 as controller
    import build_integrated_monograph_v12 as shared
    cache=VerifiedHashCache();controller.base.core.sha=cache.sha;shared.sha=cache.sha
    install(controller.base);sys.argv=[str(target),*sys.argv[2:]];start=time.monotonic()
    try:runpy.run_path(str(target),run_name='__main__')
    finally:print(json.dumps(dict(review_context='three private dictionaries;all validators retained',hash_verification=cache.summary(),elapsed_seconds=round(time.monotonic()-start,3))),file=sys.stderr)
if __name__=='__main__':main()
