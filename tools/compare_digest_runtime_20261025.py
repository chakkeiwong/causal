#!/usr/bin/env python3
"""Compare full-byte and stable-file-cached checks on one preserved state snapshot."""
import hashlib,json,time
from pathlib import Path
import run_program_checkpoint_v3 as controller
import master_control as core
import build_integrated_monograph_v12 as shared
from verified_digest_runtime_20261025 import StableDigest
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/program/execution/2026-10-25/digest-runtime-v1'

def main():
    snapshot=BASE/'comparison-state.json';assert not snapshot.exists();snapshot.write_bytes((ROOT/core.STATE).read_bytes());state=json.loads(snapshot.read_text())
    original_core,original_shared=core.sha,shared.sha
    started=time.monotonic();baseline=controller.base.validate_state(ROOT,state);baseline_seconds=time.monotonic()-started
    write(BASE/'baseline-result.json',dict(issues=baseline,seconds=baseline_seconds,state=ref(snapshot,'Exact comparison state')))
    print(json.dumps(dict(stage='baseline_complete',issues=len(baseline),seconds=round(baseline_seconds,3))),flush=True)
    cache=StableDigest(ROOT);core.sha=cache;shared.sha=cache
    started=time.monotonic();candidate=controller.base.validate_state(ROOT,state);candidate_seconds=time.monotonic()-started
    core.sha,shared.sha=original_core,original_shared
    assert baseline==candidate==[]
    write(BASE/'comparison-review.json',dict(status='pass',state=ref(snapshot,'Same immutable state for both checks'),baseline_seconds=baseline_seconds,candidate_seconds=candidate_seconds,identical_issues=baseline,statistics=cache.statistics(),evidence=[ref(BASE/'plan.md','Preserving performance plan'),ref(BASE/'unit-check.json','Invalidation and change-detection tests'),ref(BASE/'baseline-result.json','Uncached baseline'),ref(ROOT/'tools/verified_digest_runtime_20261025.py','Explicit process-local wrapper'),ref(ROOT/'tools/check_verified_digest_runtime_20261025.py','Change tests'),ref(Path(__file__),'Same-state comparison')],limitations=['Ordinary local filesystem metadata,not hostile privileged mutation detection','New process has empty cache; canonical state always full-byte hashed'],historical_controllers_changed=False))
    print(json.dumps(dict(status='pass',baseline_seconds=round(baseline_seconds,3),candidate_seconds=round(candidate_seconds,3),statistics=cache.statistics())),flush=True)
if __name__=='__main__':main()
