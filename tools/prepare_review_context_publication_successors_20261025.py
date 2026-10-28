#!/usr/bin/env python3
"""Preserve bound executors and opt reviewed successors into narrow context copying."""
import ast,json
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'
BASE=ROOT/'docs/program/execution/2026-10-25'
def main():
    repair=BASE/'review-context-repair-v1/review.json';verify_bindings(json.loads(repair.read_text()))
    log=BASE/'review-context-repair-v1/execute-verification.log';assert not log.exists();log.write_bytes(Path('/tmp/causal-review-context-verification.log').read_bytes())
    profile=BASE/'validation-profile-v1/execute-profile.log';assert not profile.exists();profile.write_bytes(Path('/tmp/causal-validation-profile.log').read_bytes())
    for stem,unit in [('agent_evaluation_surveys','agent-evaluation-surveys-v1'),('benchmark_oracles','benchmark-oracles-v1')]:
        original=TOOLS/('execute_'+stem+'_publication_20261025.py')
        successor=TOOLS/('execute_'+stem+'_publication_v2_20261025.py');assert not successor.exists()
        text=original.read_text();assert text.count('tools/run_with_verified_hash_cache_20261025.py')==1
        text=text.replace('tools/run_with_verified_hash_cache_20261025.py','tools/run_with_review_context_cache_20261025.py').replace('publication-plan-review.json','publication-plan-review-v2.json')
        ast.parse(text);successor.write_text(text)
        delivery=TOOLS/('deliver_'+stem+'_publication_20261025.py');newdelivery=TOOLS/('deliver_'+stem+'_publication_v2_20261025.py');assert not newdelivery.exists()
        text=delivery.read_text().replace('from execute_'+stem+'_publication_20261025','from execute_'+stem+'_publication_v2_20261025')
        marker="'tools/run_with_verified_hash_cache_20261025.py'";assert marker in text
        text=text.replace(marker,marker+",'tools/run_with_review_context_cache_20261025.py','tools/verify_review_context_repair_20261025.py','tools/profile_publication_validation_20261025.py','tools/prepare_review_context_publication_successors_20261025.py','docs/program/execution/2026-10-25/review-context-repair-v1','docs/program/execution/2026-10-25/validation-profile-v1'")
        ast.parse(text);newdelivery.write_text(text)
        old=BASE/unit/'publication-plan-review.json';prior=json.loads(old.read_text());verify_bindings(prior)
        plan=dict(status='pass_for_serial_publication_after_consumed_predecessor',supersedes=ref(old,'Preserved reviewed original plan;executor not used'),evidence=prior['evidence']+[ref(successor,'Only process-local wrapper and successor-plan selection changed'),ref(newdelivery,'Scoped delivery plus exact repair evidence'),ref(repair,'Measured equivalence and adverse tests'),ref(TOOLS/'run_with_review_context_cache_20261025.py','Source-guarded review context copying'),ref(Path(__file__),'Successor preparation')],steps=prior['steps'],expected=prior['expected'],checks=prior['checks']+['Read-only full-state comparison:53.337soriginal versus17.485ssuccessor;17valid/adverse bindings agree and captured state unchanged.','Every condition and evidence hash retained; only three private context dictionaries copied.','Final full controller checks remain unmodified and unwrapped.'],global_blocker=None,phase_boundaries_are_stopping_points=False)
        verify_bindings(plan);write(BASE/unit/'publication-plan-review-v2.json',plan)
    print('Both pending publications now have reviewed faster successors; live data publication remains unchanged.')
if __name__=='__main__':main()
