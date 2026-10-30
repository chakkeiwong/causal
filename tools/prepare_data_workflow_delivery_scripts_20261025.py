#!/usr/bin/env python3
"""Generate unbound successor publication scripts for review before use."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TOOLS=ROOT/'tools'

def transform(s):
    s=s.replace('bayesian_state_wave','data_workflow_wave').replace('bayesian-state-wave','data-workflow-wave')
    s=s.replace('exec25_bsw','exec25_dww').replace('sp25bsw','sp25dww')
    s=s.replace('1377','NEW_RECORD_COUNT').replace('1371','1377').replace('NEW_RECORD_COUNT','1387')
    s=s.replace('1014','NEW_SPONSOR_COUNT').replace('1006','1014').replace('NEW_SPONSOR_COUNT','1026')
    s=s.replace('340','NEW_OPERATION_COUNT').replace('335','340').replace('NEW_OPERATION_COUNT','350')
    s=s.replace('88','NEW_INCONCLUSIVE_COUNT').replace('83','88').replace('NEW_INCONCLUSIVE_COUNT','98')
    s=s.replace('11 open','1 open').replace('16 open','11 open')
    s=s.replace("['open']==11","['open']==1").replace("['open']==16","['open']==11")
    s=s.replace('software3/88/11','software3/98/1').replace('3/98/11','3/98/1')
    s=s.replace('three pass / 98 inconclusive / 11 open','three pass / 98 inconclusive / 1 open')
    s=s.replace('Software: 11 open and 98','Software: 1 open and 98')
    s=s.replace('five-language Bayesian SCM and hidden-state','ten-cell observation-data and computation-workflow')
    s=s.replace('Five-language Bayesian and state','Observation-data and computation-workflow')
    return s

def save(stem,s):
    p=TOOLS/(stem+'_20261025.py');assert not p.exists();p.write_text(s)

def main():
    s=(TOOLS/'build_bayesian_state_wave_sponsor_20261025.py').read_text()
    s=s.replace('sponsor-transport-missingness-wave-v1','PRIOR_SPONSOR_MARKER').replace('other-transport-missingness-reader-v1','PRIOR_READER_MARKER').replace('sp25tmwave','PRIOR_CITE_MARKER')
    s=transform(s).replace('PRIOR_SPONSOR_MARKER','sponsor-bayesian-state-wave-v1').replace('PRIOR_READER_MARKER','bayesian-state-wave-reader-v1').replace('PRIOR_CITE_MARKER','sp25bsw')
    s=s.replace('import build_data_workflow_wave_reader_20261025 as reader','import build_data_workflow_wave_reader_v2_20261025 as reader')
    save('build_data_workflow_wave_sponsor',s)
    s=transform((TOOLS/'publish_bayesian_state_wave_sponsor_20261025.py').read_text())
    s=s.replace("['stan','rstan','nimble','keanu','turing','choice']","['datatable','targets','dask','snakemake','beam','arrow','taskflow','dataframes','dagger','choice']")
    s=s.replace('Bayesian and hidden-state workers across five language families','Observation data and workflow execution as a scientific contract')
    save('publish_data_workflow_wave_sponsor',s)
    s=(TOOLS/'refresh_bayesian_state_wave_program_20261025.py').read_text()
    s=s.replace('program-refresh-transport-missingness-wave-v1','PRIOR_REFRESH_MARKER')
    s=transform(s).replace('PRIOR_REFRESH_MARKER','program-refresh-bayesian-state-wave-v1')
    s=s.replace("[ref(SOURCE/language/'operation-receipt.json','Separate language comparison') for language in ['R','Python','Java','Cxx','other_relevant']]","[ref(SOURCE/family/language/'operation-receipt.json','Separate family/language comparison') for family in ['observations_data','computation_workflow'] for language in ['R','Python','Java','Cxx','other_relevant']]")
    s=s.replace('The five Bayesian/state language cells record five inconclusive outcomes','The ten observation/workflow cells record ten inconclusive outcomes')
    s=s.replace('57 authentic originals and46technical anchors plus24unchanged prior citation records support five bounded language cells.','83 authentic originals and50technical anchors plus17unchanged prior citation records support ten bounded language/family cells.')
    s=s.replace('five-language Bayesian source comparison','ten-cell observation/workflow source comparison')
    old='The preserving successor compares Stan, RStan, NIMBLE, historical Keanu and Turing with existing PyMC, NumPyro, bnlearn, Dynamax and graphical/state-space audits. 57 authentic originals and24preserved source records ground Bayesian identification limits, information clocks, posterior uncertainty, diagnostic formulas, empty/partial outputs, adaptation and restart qualification.'
    new='The preserving successor compares data.table, targets, Dask, Snakemake, Beam, Arrow, Taskflow, DataFrames.jl and Dagger.jl with prior DuckDB, Polars, Feast, Pandera, Splink, OpenLineage, Ray, Spark and historical SAS evidence. 83 authentic originals and17preserved source records ground identity, cardinality, information clocks, linkage uncertainty, task/cache identity, retry/effect semantics, numeric reductions and complete cost accounting.'
    assert old in s;s=s.replace(old,new)
    s=s.replace('1,371','PRIOR_COUNT').replace('1,377','1,387').replace('PRIOR_COUNT','1,377').replace('four successful bounded queries','five successful bounded queries')
    save('refresh_data_workflow_wave_program',s)
    s=(TOOLS/'execute_bayesian_state_wave_publication_20261025.py').read_text()
    s=s.replace('transport-missingness-wave-v1','PRIOR_WAVE_MARKER').replace('causal_proposal_other_transport_missingness_reviewed_v1','PRIOR_PDF_MARKER')
    s=transform(s).replace('PRIOR_WAVE_MARKER','bayesian-state-wave-v1').replace('PRIOR_PDF_MARKER','causal_proposal_bayesian_state_wave_reviewed_v1')
    a=s.index("    for language in ['R','Python','Java','Cxx','other_relevant']:")
    z=s.index('    for name,stem,verb in [',a)
    s=s[:a]+'''    for family in ['observations_data','computation_workflow']:
        for language in ['R','Python','Java','Cxx','other_relevant']:
            operation='SW.CELL.'+family+'.'+language
            label=family+'-'+language
            step(label+'-start',['python3','tools/run_program_checkpoint_v3.py','start',operation,'--reason','Record reviewed source comparison; coverage and native admission remain inconclusive.'])
            step(label+'-receipt',['python3','tools/review_data_workflow_wave_v2_20261025.py','receipt',family,language])
            transition('record',operation,BASE/family/language/'operation-receipt.json')
''' +s[z:]
    s=s.replace("'publish_data_workflow_wave_reader'","'publish_data_workflow_wave_reader_v2'")
    s=s.replace('source_files_authenticated=57,source_retrievals_authenticated=57','source_files_authenticated=83,source_retrievals_authenticated=83')
    s=s.replace('assert predecessor[\'status\']==\'pass\'','assert predecessor[\'status\']==\'pass\'\n    assert json.loads((BASE/\'predecessor-delivery-consumed.json\').read_text())[\'exit_code\']==0')
    save('execute_data_workflow_wave_publication',s)
    s=(TOOLS/'deliver_bayesian_state_wave_publication_20261025.py').read_text().replace('transport-missingness-wave-v1','PRIOR_WAVE_MARKER')
    s=transform(s).replace('PRIOR_WAVE_MARKER','bayesian-state-wave-v1')
    old="    for language in ['R','Python','Java','Cxx','other_relevant']:\n        paths.add('docs/program/comprehensive-v14/work/SW.CELL.bayesian_scm_state.'+language)"
    new="    for family in ['observations_data','computation_workflow']:\n        for language in ['R','Python','Java','Cxx','other_relevant']:\n            paths.add('docs/program/comprehensive-v14/work/SW.CELL.'+family+'.'+language)"
    assert old in s;s=s.replace(old,new)
    s=s.replace('Integrate five-language Bayesian and hidden-state worker comparisons','Integrate observation-data and workflow comparisons across five language ecosystems')
    save('deliver_data_workflow_wave_publication',s)
    print('Prepared successor sponsor, refresh, execution and delivery scripts for review')

if __name__=='__main__':main()
