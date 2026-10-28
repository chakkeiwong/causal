#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'

def save(stem,s):
    p=TOOLS/(stem+'_20261025.py');assert not p.exists();p.write_text(s)

def common(s):
    s=s.replace('data_workflow_wave','agent_evaluation_surveys').replace('data-workflow-wave-reader-v1','agent-evaluation-surveys-reader-v2').replace('data-workflow-wave-v1','agent-evaluation-surveys-v1')
    s=s.replace('sp25dww','sp25aes').replace('exec25_dww','exec25_cow')
    s=s.replace('1387','NEW_RECORD').replace('1377','1387').replace('NEW_RECORD','1390')
    s=s.replace('1026','NEW_SPONSOR').replace('1014','1026').replace('NEW_SPONSOR','1031')
    s=s.replace('ten-cell observation-data and computation-workflow','agent-evaluation survey')
    return s

def main():
    s=(TOOLS/'build_data_workflow_wave_sponsor_20261025.py').read_text()
    s=s.replace('sponsor-bayesian-state-wave-v1','PRIOR_SPONSOR').replace('bayesian-state-wave-reader-v1','PRIOR_READER').replace('sp25bsw','PRIOR_CITE')
    s=common(s).replace('PRIOR_SPONSOR','sponsor-data-workflow-wave-v1').replace('PRIOR_READER','data-workflow-wave-reader-v1').replace('PRIOR_CITE','sp25dww')
    s=s.replace('sponsor-data-workflow-wave-v1','PRIOR_SPONSOR_SENTINEL').replace('sponsor-agent-evaluation-surveys-v1','sponsor-agent-evaluation-surveys-v1').replace('PRIOR_SPONSOR_SENTINEL','sponsor-data-workflow-wave-v1')
    s=s.replace("BASE=DOCS/'program/execution/2026-10-25/sponsor-data-workflow-wave-v1'","BASE=DOCS/'program/execution/2026-10-25/sponsor-agent-evaluation-surveys-v1'")
    s=s.replace("old='The program has 340 recorded outcomes of 376'","old='The program has 350 recorded outcomes of 376'")
    s=s.replace("old='Current software coverage is three passing, 88 inconclusive and 11 open cells'","old='Current software coverage is three passing, 98 inconclusive and 1 open cells'")
    s=s.replace("text=text.replace('265 genuine scholarly PDFs','265 genuine scholarly PDFs')","text=text.replace('265 genuine scholarly PDFs','267 genuine scholarly PDFs')")
    s=s.replace('census-route-followup-v1/census-register.json','census-observation-workflow-v1/census-register.json')
    s=s.replace("{'exec25_pymed_neural_paper'","{'exec25_cow_chemistry','exec25_cow_vulnerability','exec25_pymed_neural_paper'")
    save('build_agent_evaluation_surveys_sponsor',s)
    s=common((TOOLS/'publish_data_workflow_wave_sponsor_20261025.py').read_text())
    s=s.replace("['datatable','targets','dask','snakemake','beam','arrow','taskflow','dataframes','dagger','choice']","['chemistry','vulnerability','reference']")
    s=s.replace('265 genuine scholarly PDFs','267 genuine scholarly PDFs').replace('Observation data and workflow execution as a scientific contract','Evaluate scientific answers separately from completed agent workflows')
    save('publish_agent_evaluation_surveys_sponsor',s)
    s=(TOOLS/'refresh_data_workflow_wave_program_20261025.py').read_text().replace('program-refresh-bayesian-state-wave-v1','PRIOR_REFRESH')
    s=common(s).replace('PRIOR_REFRESH','program-refresh-data-workflow-wave-v1')
    s=s.replace("SOURCE=ROOT/'docs/program/execution/2026-10-25/agent-evaluation-surveys-v1'","SOURCE=ROOT/'docs/program/execution/2026-10-25/census-observation-workflow-v1'")
    s=s.replace("CENSUS=ROOT/'docs/program/execution/2026-10-25/census-route-followup-v1'","CENSUS=SOURCE")
    s=s.replace('+[ref(SOURCE/family/language/\'comparison-review.json\',\'Separate language/family comparison\') for family in [\'observations_data\',\'computation_workflow\'] for language in [\'R\',\'Python\',\'Java\',\'Cxx\',\'other_relevant\']]','+[ref(SOURCE/\'route-review.json\',\'Preserved routes and related-source limits\')]')
    s=s.replace('The ten observation/workflow cells record ten inconclusive outcomes;no native capability admitted.','Two genuine related preprints add three citation records;no additional completed operation or native capability inferred.')
    s=s.replace('83 authentic originals and50technical anchors plus17unchanged prior citation records support ten bounded language/family cells.','Two genuine preprints and finite project examples support semantic-target,proxy,judge,label,test and cost evaluation;separate journal obligations remain open.')
    s=s.replace('ten-cell observation/workflow source comparison','Agent evaluation primary survey comparison')
    old='The preserving successor compares data.table, targets, Dask, Snakemake, Beam, Arrow, Taskflow, DataFrames.jl and Dagger.jl with prior DuckDB, Polars, Feast, Pandera, Splink, OpenLineage, Ray, Spark and historical SAS evidence. 83 authentic originals and17preserved source records ground identity, cardinality, information clocks, linkage uncertainty, task/cache identity, retry/effect semantics, numeric reductions and complete cost accounting.'
    new='The preserving successor integrates Ramos and colleagues chemistry-agent preprint and Zhou and colleagues vulnerability-repair preprint, plus exact project examples of semantic target loss, proxy regret, correlated judges, noisy labels, incomplete tests and complete evaluation denominators. Two genuine version3 originals are independently cited; exact journal equivalence is not established.'
    assert old in s;s=s.replace(old,new)
    s=s.replace('1,377','PRIOR_COUNT').replace('1,387','1,390').replace('PRIOR_COUNT','1,387')
    s=s.replace('265 scholarly PDFs','267 scholarly PDFs').replace('265scholarly PDFs','267scholarly PDFs').replace('265 genuine scholarly PDFs','267 genuine scholarly PDFs')
    s=s.replace('five successful bounded queries retain unreturned and uninspected candidates plus broader ecosystem limits','seventeen newly reviewed identity/route records preserve uninspected originals and two related-preprint/journal boundaries')
    s=s.replace('Continue the 31 unread originals and four crosscutting tasks.','Continue the 31 unread originals and four crosscutting tasks; two related preprints do not close their distinct journal-original obligations.')
    save('refresh_agent_evaluation_surveys_program',s)
    print('Prepared sponsor and full reconciliation for review')

if __name__=='__main__':main()
