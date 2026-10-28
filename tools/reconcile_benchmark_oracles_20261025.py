#!/usr/bin/env python3
"""Record independent oracle progress while native qualification stays open."""
import json
from collections import Counter
from pathlib import Path
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings, transition
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'
BASE=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-v1'
READER=ROOT/'docs/program/execution/2026-10-25/benchmark-oracles-reader-v1'
read=lambda p:json.loads(p.read_text())

def main():
    run=controller.base;core=run.core;state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active'] is None
    for p in [SOURCE/'review.json',SOURCE/'qualification-design.json',SOURCE/'census-register.json',READER/'release-source-review.json']:
        verify_bindings(read(p))
    counts=Counter(x['disposition'] for x in read(SOURCE/'census-register.json')['items'])
    assert counts['inspected_primary_retained_with_limits']==82 and counts['open_original_not_inspected']==31
    note=dict(finding='Independent finite IV worlds and scoring-contract fixtures are integrated. The compatible observed laws have population effects-1/2and1/4; unknown identification,invalid responses,nonfinite arithmetic and clipped losses remain distinct. Census remains82/31plus4crosscutting; native qualification is open.',
        next_action='Continue LA01-runtime-licenses by inspecting exact retained LLM-CD,LLM-and-SCD and LCM artifact,weight and dependency identities. Preserve the benchmark qualification design: full native item/generator/parser/scorer conformance and rights remain open; do not repeat the completed finite-oracle derivation. Continue distinct permitted routes for31unread originals.',
        yield_reason='Finite oracle review and integration complete; independent rights and source obligations remain eligible.',
        evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(SOURCE/'census-register.json','Unchanged dispositions'),ref(SOURCE/'qualification-design.json','Native scientific qualification contract'),ref(SOURCE/'review.json','Independent source and project review'),ref(READER/'working-release.json','Preserving integrated monograph'),ref(Path(__file__),'Serial durable continuation')])
    write(BASE/'integrated-progress.json',note)
    before=core.sha(ROOT/core.STATE)
    event=run.apply(ROOT,state,'start','LL.CENSUS',reason='Record integrated finite-oracle qualification requirements without closing native obligations.')
    run.commit(ROOT,before,state,event)
    transition('yield','LL.CENSUS',BASE/'integrated-progress.json')
    state=core.read(ROOT,core.STATE);_,merged,_=run.combined(ROOT,state)
    saved=merged['execution_program']['progress']['LL.CENSUS'][-1]
    assert saved['path']==str((BASE/'integrated-progress.json').relative_to(ROOT))
    verify_bindings(saved);assert state['execution_runtime']['active'] is None
    write(BASE/'census-reconciliation.json',dict(status='pass',counts=dict(counts),originals_closed=0,independent_oracle_contracts=4,evidence=[saved,ref(SOURCE/'review.json','Reviewed source delta')],next_action=note['next_action']))
    print(json.dumps(dict(census_inspected=82,unread=31,crosscutting=4,new_original_dispositions=0)))

if __name__=='__main__':main()
