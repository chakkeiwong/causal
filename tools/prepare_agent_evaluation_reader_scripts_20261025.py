#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'

def save(name,s):
    p=TOOLS/(name+'_20261025.py');assert not p.exists();p.write_text(s)

def main():
    s=(TOOLS/'build_data_workflow_wave_reader_v2_20261025.py').read_text()
    s=s.replace('bayesian-state-wave-reader-v1','PREVIOUS_READER').replace('causal_proposal_bayesian_state_wave_reviewed_v1','PREVIOUS_PDF')
    s=s.replace('data_workflow_wave_reference_v2','agent_evaluation_survey_reference').replace('data-workflow-wave-reader-v1','agent-evaluation-surveys-reader-v1').replace('data-workflow-wave-v1','census-observation-workflow-v1').replace('causal_proposal_data_workflow_wave_reviewed_v1','causal_proposal_agent_evaluation_surveys_reviewed_v1')
    s=s.replace('PREVIOUS_READER','data-workflow-wave-reader-v1').replace('PREVIOUS_PDF','causal_proposal_data_workflow_wave_reviewed_v1')
    s=s.replace('exec25-dww','exec25-cow').replace('1377','1387').replace('added==10','added==3').replace('expected_scholarly_pdfs=265','expected_scholarly_pdfs=267')
    s=s.replace('Observation data and computation workflows','Agent evaluation beyond workflow completion').replace('observation-data and computation-workflow','agent-evaluation survey')
    s=s.replace('Add five-language observation identity,cardinality,clocks,linkage,task,retry,effect,numeric and cost contracts','Add two genuine independently identified survey preprints and exact semantic-target,proxy,judge,label,test and cost witnesses')
    save('build_agent_evaluation_surveys_reader',s)
    s=(TOOLS/'publish_data_workflow_wave_reader_v2_20261025.py').read_text()
    s=s.replace('build_data_workflow_wave_reader_v2','build_agent_evaluation_surveys_reader').replace('data_workflow_wave','agent_evaluation_surveys').replace('1387','NEW_COUNT').replace('1377','1387').replace('NEW_COUNT','1390').replace('265','267')
    s=s.replace('added_citation_records=10','added_citation_records=3').replace('exec25_dww','exec25_cow')
    s=s.replace("['datatable','targets','dask','snakemake','beam','arrow','taskflow','dataframes','dagger','choice']","['chemistry','vulnerability','reference']")
    s=s.replace('A bank selecting an observation-data engine or computation workflow must preserve','An agent that completes a tool workflow has not necessarily answered the scientific question.')
    s=s.replace('The available engines can move and schedule evidence efficiently; the proposed product must retain its scientific meaning through every transformation and attempt.','Modular tools make the process inspectable; scientific acceptance still depends on the target, evidence and validation law.')
    s=s.replace("['data.table','Dask','Snakemake','Taskflow','Dagger','USD1.8 million']","['Ramos','Zhou','USD30','58','CLI/MCP']")
    s=s.replace('ten-cell observation-data and computation-workflow','agent-evaluation survey')
    s=s.replace('83 authentic originals and17unchanged prior records support five bounded language comparisons.','Two authentic preprints support their own frameworks and syntheses;one authored exact-reference record separates proposal examples from empirical performance.')
    s=s.replace('nine source collections and one authored comparison record','two genuine preprints and one authored reference record')
    s=s.replace('Exact join,linkage,time,retry/effect,replicate,numeric and cost witnesses','Exact semantic-target,proxy-regret,correlated-judge,label,test and cost witnesses')
    s=s.replace('Proposed data/workflow contracts preserve units,cardinality,clocks,linkage,logical tasks,attempts,effects,errors,artifacts and full costs','Proposed evaluation contracts preserve scientific targets,graph ambiguity,independent oracles,refusals,attempts and full costs')
    save('publish_agent_evaluation_surveys_reader',s)
    print('Prepared survey reader and preserving reviewer')

if __name__=='__main__':main()
