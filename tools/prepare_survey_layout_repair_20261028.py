#!/usr/bin/env python3
"""Preserve failed sponsor and correct whitespace in its newly added prose."""
from pathlib import Path
import ast,json,re
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'
BASE=ROOT/'docs/program/execution/2026-10-28/crash-recovery-v1'
WAVE=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-v1'
OLD=ROOT/'docs/program/execution/2026-10-25/sponsor-agent-evaluation-surveys-v1'

def save(name,text):
    p=TOOLS/(name+'_20261028.py');assert not p.exists();ast.parse(text);p.write_text(text);return p

def main():
    source=(TOOLS/'build_agent_evaluation_surveys_sponsor_20261025.py').read_text()
    source=source.replace('sponsor-agent-evaluation-surveys-v1','sponsor-agent-evaluation-surveys-v2')
    marker="    addition=(READER_BASE/'sponsor-addition.md').read_text()"
    assert source.count(marker)==1
    source=source.replace(marker,marker+chr(10)+"    addition=re.sub(r'(?<=[A-Za-z])[,;](?=[A-Za-z])',lambda m:m.group(0)+' ',addition)")
    builder=save('build_agent_evaluation_surveys_sponsor_v2',source)
    source=(TOOLS/'publish_agent_evaluation_surveys_sponsor_20261025.py').read_text().replace('build_agent_evaluation_surveys_sponsor_20261025','build_agent_evaluation_surveys_sponsor_v2_20261028')
    publisher=save('publish_agent_evaluation_surveys_sponsor_v2',source)
    source=(TOOLS/'refresh_agent_evaluation_surveys_program_20261025.py').read_text().replace('sponsor-agent-evaluation-surveys-v1','sponsor-agent-evaluation-surveys-v2').replace('Updated 25 October 2026','Updated 28 October 2026')
    refresher=save('refresh_agent_evaluation_surveys_program_v2',source)
    import build_agent_evaluation_surveys_sponsor_v2_20261028 as new
    expected=new.manuscript(1719);original=(OLD/'proposal.md').read_text()
    assert ''.join(expected.split())==''.join(original.split()) and expected!=original
    (BASE/'expected-repaired-sponsor.md').write_text(expected)
    report=dict(status='reviewed_whitespace_only_successor',failure='Sponsor build rejected11.00363pt overfull line in newly added CLI/MCP paragraph;missing spaces after punctuation.',evidence=[ref(OLD/'reader/sponsor-proposal.log','Preserved failed rendered layout'),ref(OLD/'proposal.md','Preserved failed manuscript'),ref(WAVE/'sponsor-build.log','Exit1 retained'),ref(BASE/'expected-repaired-sponsor.md','Whitespace-only corrected manuscript'),ref(builder,'Corrected preserving builder'),ref(publisher,'Exact sponsor review and publication'),ref(refresher,'Current program references corrected sponsor'),ref(Path(__file__),'Whitespace equivalence and plan review')],checks=['All nonwhitespace manuscript characters identical.','All1031citation records retained;expected reader pairing1719pages.','Failed original source and render retained.','Full rendering,source,economics,snapshot and exact-byte checks required before publication.'],visual_acceptance=False,final_acceptance=False)
    verify_bindings(report);write(BASE/'sponsor-layout-repair.json',report)
    print('Prepared and reviewed whitespace-only sponsor successor.')
if __name__=='__main__':main()
