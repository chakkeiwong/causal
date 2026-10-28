#!/usr/bin/env python3
"""Prepare serial publication preserving predecessor and source boundaries."""
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'
def save(name,s):
    p=TOOLS/(name+'_20261025.py');assert not p.exists();ast.parse(s);p.write_text(s)
def common(s):
    s=s.replace('agent_evaluation_surveys_reader_v2','benchmark_oracles_reader').replace('agent_evaluation_surveys','benchmark_oracles')
    s=s.replace('agent-evaluation-surveys-reader-v2','benchmark-oracles-reader-v1').replace('agent-evaluation-surveys-v1','benchmark-oracles-v1').replace('census-observation-workflow-v1','benchmark-oracles-v1')
    return s
def main():
    s=common((TOOLS/'reconcile_agent_evaluation_surveys_20261025.py').read_text())
    s=s.replace("SOURCE/'route-review.json'","SOURCE/'qualification-design.json'")
    start=s.index('    note=dict(');end=s.index("    write(BASE/'integrated-progress.json'",start)
    s=s[:start]+'''    note=dict(finding='Independent finite IV worlds and scoring-contract fixtures are integrated. The compatible observed laws have population effects-1/2and1/4; unknown identification,invalid responses,nonfinite arithmetic and clipped losses remain distinct. Census remains82/31plus4crosscutting; native qualification is open.',
        next_action='Continue LA01-runtime-licenses by inspecting exact retained LLM-CD,LLM-and-SCD and LCM artifact,weight and dependency identities. Preserve the benchmark qualification design: full native item/generator/parser/scorer conformance and rights remain open; do not repeat the completed finite-oracle derivation. Continue distinct permitted routes for31unread originals.',
        yield_reason='Finite oracle review and integration complete; independent rights and source obligations remain eligible.',
        evidence=[state['execution_program']['progress']['LL.CENSUS'][-1],ref(SOURCE/'census-register.json','Unchanged dispositions'),ref(SOURCE/'qualification-design.json','Native scientific qualification contract'),ref(SOURCE/'review.json','Independent source and project review'),ref(READER/'working-release.json','Preserving integrated monograph'),ref(Path(__file__),'Serial durable continuation')])
'''+s[end:]
    s=s.replace('Record the integrated related-preprint and route review without closing original obligations.','Record integrated finite-oracle qualification requirements without closing native obligations.')
    s=s.replace('related_preprints_inspected=2','independent_oracle_contracts=4')
    s=s.replace('Record related-preprint progress without closing distinct original obligations.','Record independent oracle progress while native qualification stays open.')
    save('reconcile_benchmark_oracles',s)
    s=(TOOLS/'execute_agent_evaluation_surveys_publication_20261025.py').read_text()
    s=s.replace('data-workflow-wave-v1','PREDECESSOR_WAVE').replace('causal_proposal_data_workflow_wave_reviewed_v1_2026-10-25.pdf','PREDECESSOR_PDF')
    s=common(s).replace('PREDECESSOR_WAVE','agent-evaluation-surveys-v1').replace('PREDECESSOR_PDF','causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25.pdf')
    s=s.replace('related_preprints_inspected=2','independent_oracle_contracts=4')
    s=s.replace('then continue independent benchmark-oracle qualification.','then continue independent runtime-rights and source obligations.')
    s=s.replace('Agent evaluation survey publication','Independent benchmark oracle publication')
    save('execute_benchmark_oracles_publication',s)
    s=(TOOLS/'deliver_agent_evaluation_surveys_publication_20261025.py').read_text()
    s=s.replace('data-workflow-wave-v1','PREDECESSOR_WAVE')
    s=common(s).replace('PREDECESSOR_WAVE','agent-evaluation-surveys-v1')
    s=s.replace("'tools/*agent_evaluation*20261025.py'","'tools/*benchmark_oracle*20261025.py'")
    s=s.replace("'docs/program/execution/2026-10-25/*agent-evaluation*'","'docs/program/execution/2026-10-25/*benchmark-oracles*'")
    s=s.replace(",'docs/literature/raw/exec25_cow*'",'')
    s=s.replace('Integrate primary agent-evaluation surveys and preserve unresolved census obligations','Integrate independent causal and scoring oracles with bounded public qualification')
    save('deliver_benchmark_oracles_publication',s)
    print('Prepared benchmark census checkpoint,serial executor and scoped delivery.')
if __name__=='__main__':main()
