#!/usr/bin/env python3
"""Prepare a successor using established preserving publication mechanics."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'

def save(stem,text):
    path=TOOLS/(stem+'_20261025.py')
    assert not path.exists(),path
    path.write_text(text)

def main():
    s=(TOOLS/'build_bayesian_state_wave_reader_20261025.py').read_text()
    s=s.replace('other-transport-missingness-reader-v1','PRIOR_READER_MARKER').replace('causal_proposal_other_transport_missingness_reviewed_v1','PRIOR_PDF_MARKER')
    s=s.replace('bayesian_state_wave','data_workflow_wave').replace('bayesian-state-wave','data-workflow-wave').replace('exec25-bsw','exec25-dww')
    s=s.replace('PRIOR_READER_MARKER','bayesian-state-wave-reader-v1').replace('PRIOR_PDF_MARKER','causal_proposal_bayesian_state_wave_reviewed_v1')
    s=s.replace('1371','1377').replace('added==6','added==10')
    s=s.replace('Bayesian SCM and hidden-state workers','Observation data and computation workflows')
    s=s.replace('Bayesian SCM and hidden-state','observation-data and computation-workflow')
    s=s.replace('Bayesian SCM,hidden-state,information-clock,posterior uncertainty,diagnostic and qualification contracts','observation identity,cardinality,clocks,linkage,task,retry,effect,numeric and cost contracts')
    save('build_data_workflow_wave_reader',s)
    s=(TOOLS/'publish_bayesian_state_wave_reader_20261025.py').read_text()
    s=s.replace('bayesian_state_wave','data_workflow_wave').replace('bayesian-state-wave','data-workflow-wave').replace('exec25_bsw','exec25_dww')
    s=s.replace('1377','COUNT_NEW').replace('1371','1377').replace('COUNT_NEW','1387').replace('added_citation_records=6','added_citation_records=10')
    s=s.replace('five source collections and one authored comparison record','nine source collections and one authored comparison record')
    s=s.replace("['stan','rstan','nimble','keanu','turing','choice']","['datatable','targets','dask','snakemake','beam','arrow','taskflow','dataframes','dagger','choice']")
    s=s.replace('A bank selecting a Bayesian or hidden-state worker must distinguish','A bank selecting an observation-data engine or computation workflow must preserve')
    s=s.replace('A well-computed posterior remains conditional on a defensible model and information set.','The available engines can move and schedule evidence efficiently; the proposed product must retain its scientific meaning through every transformation and attempt.')
    s=s.replace('start+12','start+24').replace("['RStan','NIMBLE','Keanu','Turing','USD250,000']","['data.table','Dask','Snakemake','Taskflow','Dagger','USD1.8 million']")
    s=s.replace('57 authentic originals and24unchanged prior records','83 authentic originals and17unchanged prior records')
    s=s.replace('five-language Bayesian SCM and hidden-state','ten-cell observation-data and computation-workflow')
    s=s.replace('Numerical parity, causal identification and uncertainty remain distinct','Scientific identity, numerical accuracy and workflow completion remain distinct')
    s=s.replace('Exact prior sensitivity,filtering/smoothing,predictive uncertainty,diagnostic and sample-accounting witnesses','Exact join,linkage,time,retry/effect,replicate,numeric and cost witnesses')
    s=s.replace('Proposed Bayesian/state contracts preserve model,intervention,information clocks,uncertainty,diagnostic formula,failures,retained draws,artifacts and full costs','Proposed data/workflow contracts preserve units,cardinality,clocks,linkage,logical tasks,attempts,effects,errors,artifacts and full costs')
    save('publish_data_workflow_wave_reader',s)
    print('Prepared preserving reader builder and reviewer')

if __name__=='__main__':main()
