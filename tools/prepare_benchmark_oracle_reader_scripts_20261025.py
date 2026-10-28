#!/usr/bin/env python3
"""Prepare a scoped preserving successor; inspect generated code before binding."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'

def swap(text,old,new):
    assert old in text,old
    return text.replace(old,new)

def main():
    s=(TOOLS/'build_agent_evaluation_surveys_reader_v2_20261025.py').read_text()
    s=swap(s,'agent_evaluation_survey_reference','benchmark_oracle_reference')
    s=swap(s,'agent-evaluation-surveys-reader-v2','benchmark-oracles-reader-v1')
    s=swap(s,'census-observation-workflow-v1','benchmark-oracles-v1')
    s=swap(s,'data-workflow-wave-reader-v1','agent-evaluation-surveys-reader-v2')
    s=swap(s,'causal_proposal_data_workflow_wave_reviewed_v1_2026-10-25','causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25')
    s=swap(s,'causal_proposal_agent_evaluation_surveys_reviewed_v2_2026-10-25\';DRIVER','causal_proposal_benchmark_oracles_reviewed_v1_2026-10-25\';DRIVER')
    s=swap(s,'sec:exec25-cow','sec:exec25-bor')
    s=swap(s,'development-v2.tex','development.tex')
    s=swap(s,",SOURCE/'layout-repair.json'",'')
    s=swap(s,"SOURCE/'layout-repair.json',",'')
    s=swap(s,'prior_count==1387 and added==3','prior_count==1390 and added==2')
    start=s.index("        (BASE/name).write_bytes")
    end=s.index(chr(10),start)
    s=s[:start]+"        (BASE/name).write_bytes((SOURCE/name).read_bytes())"+s[end:]
    s=swap(s,'section[Agent evaluation beyond workflow completion]{','section[Independent causal and scoring oracles]{')
    s=swap(s,'Preserve all1387 prior source records,citation contexts and content inputs. Add two genuine independently identified survey preprints and exact semantic-target,proxy,judge,label,test and cost witnesses; preserve all inherited comparisons.','Preserve all1390 prior source records,citation contexts and content inputs. Add pinned benchmark branch inspection and independent IV,identification-state,interval and capped-loss witnesses; preserve all inherited comparisons.')
    s=swap(s,'Original agent-evaluation survey software source and authored comparison records','Pinned benchmark source and independent authored oracle records')
    s=swap(s,'agent-evaluation survey component comparison','independent causal and scoring oracle argument')
    target=TOOLS/'build_benchmark_oracles_reader_20261025.py';assert not target.exists();ast.parse(s);target.write_text(s)
    s=(TOOLS/'publish_agent_evaluation_surveys_reader_v2_20261025.py').read_text()
    s=swap(s,'build_agent_evaluation_surveys_reader_v2','build_benchmark_oracles_reader')
    s=swap(s,'1390','NEWCOUNT');s=swap(s,'1387','1390');s=s.replace('NEWCOUNT','1392')
    s=swap(s,"{'exec25_cow_'+k for k in ['chemistry','vulnerability','reference']}","{'exec25_bor_'+k for k in ['sources','reference']}")
    s=swap(s,'added_citation_records=3','added_citation_records=2')
    s=swap(s,'An agent that completes a tool workflow has not necessarily answered the scientific question.','A public benchmark can justify a prototype only if its reference answer represents the scientific decision we intend to test.')
    s=swap(s,'Modular tools make the process inspectable; scientific acceptance still depends on the target, evidence and validation law.','the proposed product must obtain information, narrow assumptions or return the unresolved set.')
    s=swap(s,"['Ramos','Zhou','USD30','58','CLI/MCP']","['CLadder','CausalDS','250,000','quarantine','overflow']")
    s=swap(s,'Two authentic preprints support their own frameworks and syntheses;one authored exact-reference record separates proposal examples from empirical performance.','Pinned source branches are inspected; independent finite witnesses remain distinct from native benchmark results.')
    s=swap(s,'two genuine preprints and one authored reference record','two additional pinned-source and independent-project records')
    s=swap(s,'semantic-target,proxy-regret,correlated-judge,label,test and cost witnesses','IV-compatible-world,three-state-identification,finite-interval and capped-loss witnesses')
    s=s.replace('agent-evaluation survey','independent benchmark-oracle').replace('agent_evaluation_surveys','benchmark_oracles')
    target=TOOLS/'publish_benchmark_oracles_reader_20261025.py';assert not target.exists();ast.parse(s);target.write_text(s)
    print('Prepared preserving benchmark reader and exact-byte reviewer.')

if __name__=='__main__':main()
