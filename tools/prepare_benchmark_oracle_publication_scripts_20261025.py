#!/usr/bin/env python3
"""Generate preserving sponsor and reconciliation for the reviewed oracle wave."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'
def swap(s,a,b):
    assert a in s,a
    return s.replace(a,b)
def save(name,s):
    p=TOOLS/(name+'_20261025.py');assert not p.exists();ast.parse(s);p.write_text(s)
def common(s):
    s=s.replace('agent_evaluation_surveys_reader_v2','benchmark_oracles_reader')
    s=s.replace('agent_evaluation_surveys','benchmark_oracles')
    s=s.replace('agent-evaluation-surveys-reader-v2','benchmark-oracles-reader-v1')
    s=s.replace('agent-evaluation-surveys-v1','benchmark-oracles-v1')
    s=s.replace('sp25aes','sp25bor').replace('exec25_cow','exec25_bor')
    s=s.replace('1031','NEWSP').replace('1026','1031').replace('NEWSP','1035')
    s=s.replace('1390','NEWC').replace('1387','1390').replace('NEWC','1392')
    s=s.replace('agent-evaluation survey','independent benchmark-oracle')
    return s
def main():
    s=(TOOLS/'build_agent_evaluation_surveys_sponsor_20261025.py').read_text()
    s=s.replace('sponsor-data-workflow-wave-v1','OLDSP').replace('data-workflow-wave-reader-v1','OLDREADER').replace('sp25dww','OLDCITE')
    s=common(s).replace('OLDSP','sponsor-agent-evaluation-surveys-v1').replace('OLDREADER','agent-evaluation-surveys-reader-v2').replace('OLDCITE','sp25aes')
    s=swap(s,"assert text.count('265 genuine scholarly PDFs')==1","assert text.count('267 genuine scholarly PDFs')==1")
    s=swap(s,"text.replace('265 genuine scholarly PDFs','267 genuine scholarly PDFs')","text.replace('267 genuine scholarly PDFs','267 genuine scholarly PDFs')")
    s=swap(s,'census-observation-workflow-v1/census-register.json','benchmark-oracles-v1/census-register.json')
    s=swap(s,"'exec25_bor_chemistry','exec25_bor_vulnerability'","'exec25_cow_chemistry','exec25_cow_vulnerability'")
    save('build_benchmark_oracles_sponsor',s)
    s=common((TOOLS/'publish_agent_evaluation_surveys_sponsor_20261025.py').read_text())
    s=swap(s,"['chemistry','vulnerability','reference']","['sources','reference']")
    s=swap(s,'Evaluate scientific answers separately from completed agent workflows','Qualify the scientific oracle before funding the agent trial')
    save('publish_benchmark_oracles_sponsor',s)
    s=(TOOLS/'refresh_agent_evaluation_surveys_program_20261025.py').read_text().replace('program-refresh-data-workflow-wave-v1','OLDREFRESH')
    s=common(s).replace('OLDREFRESH','program-refresh-agent-evaluation-surveys-v1')
    s=swap(s,'census-observation-workflow-v1','benchmark-oracles-v1')
    s=swap(s,"read(SOURCE/'plan-review-v2.json')","read(SOURCE/'plan-review.json')")
    s=swap(s,"ref(SOURCE/'route-review.json','Preserved routes and related-source limits')","ref(SOURCE/'qualification-design.json','Explicit native qualification requirements')")
    s=s.replace('1,390','NEWFMT').replace('1,387','1,390').replace('NEWFMT','1,392')
    s=swap(s,'Two genuine related preprints add three citation records;no additional completed operation or native capability inferred.','Two pinned-source and independent-project records added;no completed operation or native capability inferred.')
    s=swap(s,'Two genuine preprints and finite project examples support semantic-target,proxy,judge,label,test and cost evaluation;separate journal obligations remain open.','Independent binary IV worlds,three-state identification,finite interval and clipped-loss fixtures specify public qualification;native obligations remain open.')
    old='The preserving successor integrates Ramos and colleagues chemistry-agent preprint and Zhou and colleagues vulnerability-repair preprint, plus exact project examples of semantic target loss, proxy regret, correlated judges, noisy labels, incomplete tests and complete evaluation denominators. Two genuine version3 originals are independently cited; exact journal equivalence is not established.'
    new='The preserving successor reinspects pinned CLadder and CausalDS branches and adds independent exact causal and scoring witnesses. Two binary IV worlds have identical observations and ratio1 but opposite population effects; unknown oracle states, malformed answers,nonfinite arithmetic and clipped loss remain distinct. The full native item/generator/scorer path and artifact rights require separate qualification.'
    s=swap(s,old,new)
    s=swap(s,'seventeen newly reviewed identity/route records preserve uninspected originals and two related-preprint/journal boundaries','prior source-route and preprint/journal boundaries remain; finite oracle witnesses do not establish native benchmark conformance')
    s=swap(s,'Agent evaluation primary survey comparison','Independent causal and scoring oracle review')
    s=swap(s,'twelve recorded source/identity limits retained without changing dispositions','all recorded source/identity limits retained without changing dispositions')
    s=swap(s,'5. Public prototypes: preregister task/version splits, scientific and refusal\n   oracles, native environment, fault tests and full costs before expensive bank work.','5. Public prototypes: the benchmark-oracle design now specifies independent IV,\n   identification-state, finite-interval and loss-aggregation fixtures. Qualify the\n   full native generator/scorer path,task versions,rights and complete costs before\n   expensive bank work; oracle-unknown tasks remain a separate denominator.')
    save('refresh_benchmark_oracles_program',s)
    print('Prepared benchmark sponsor,publisher and complete reconciliation for inspection.')
if __name__=='__main__':main()
