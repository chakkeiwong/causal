#!/usr/bin/env python3
"""Record related-preprint progress without closing distinct original obligations."""
import json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings, transition
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/program/execution/2026-10-25/census-observation-workflow-v1'
BASE=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-v1'
READER=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-reader-v2'
read=lambda p:json.loads(p.read_text())

def main():
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    for p in [SOURCE/'review.json',SOURCE/'route-review.json',SOURCE/'census-register.json',READER/'release-source-review.json']:
        verify_bindings(read(p))
    counts=Counter(x['disposition'] for x in read(SOURCE/'census-register.json')['items'])
    assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    note=dict(finding='Two authentic related preprints inspected and integrated with exact project examples; their distinct journal-original obligations remain open. Seventeen candidate identity/route records preserve original access, edition and cutoff limits. Census remains82 inspected/31 unread plus four crosscutting tasks.',
        next_action='Continue LA01-benchmark-oracles using independent finite causal/scoring fixtures for the pinned CLadder IV and CausalDS unknown-ID/nonfinite branches. Preserve the 31 unread-original and four crosscutting obligations; related preprints do not close journal originals. Seek distinct permitted routes only, without retrying unchanged provider or policy failures.',
        yield_reason='This integrated source delta is complete; independent benchmark qualification and remaining proposal obligations continue.',
        evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(SOURCE/'census-register.json','Unchanged original dispositions'),ref(SOURCE/'route-review.json','Seventeen preserved route findings'),ref(SOURCE/'review.json','Two independently audited preprints'),ref(READER/'working-release.json','Preserving integrated monograph'),ref(Path(__file__),'Serial durable continuation')])
    write(BASE/'integrated-progress.json',note)
    before=core.sha(ROOT/core.STATE)
    event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record the integrated related-preprint and route review without closing original obligations.')
    run.commit(ROOT,before,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state)
    saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT))
    verify_bindings(saved);assert state['execution_runtime']['active'] is None
    write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(counts),originals_closed=0,related_preprints_inspected=2,evidence=[saved,ref(SOURCE/'review.json','Reviewed source delta')],next_action=note['next_action']))
    print(json.dumps(dict(census_inspected=82,unread=31,crosscutting=4,new_original_dispositions=0)))

if __name__=='__main__':main()
