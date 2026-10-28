"""Create preserving publication successors for the RL discovery comparison."""
from prepare_openai_publication_20261028 import T,replace,save

def main():
    mapping={
      'boundary_profile_reference_20261028':'rl_discovery_boundary_reference_20261028',
      'boundary_profile_reader_v2_20261028':'rl_discovery_reader_20261028',
      'boundary_profile_sponsor_v2_20261028':'rl_discovery_sponsor_20261028',
      'boundary-profile-review-v2':'rl-discovery-review-v1','boundary-profile-reader-v2':'rl-discovery-reader-v1','sponsor-boundary-profile-v2':'sponsor-rl-discovery-v1',
      'delegate-contract-reader-v1':'boundary-profile-reader-v2','sponsor-delegate-contract-v1':'sponsor-boundary-profile-v2',
      'causal_proposal_boundary_profile_reviewed_v2_2026-10-28':'causal_proposal_rl_discovery_reviewed_v1_2026-10-28',
      'causal_proposal_delegate_contract_reviewed_v1_2026-10-28':'causal_proposal_boundary_profile_reviewed_v2_2026-10-28',
      'sponsor_proposal_boundary_profile_reviewed_v2_2026-10-28':'sponsor_proposal_rl_discovery_reviewed_2026-10-28',
      '1415':'1418','1418':'1423','1068':'1073','1073':'1080','271':'273',
      'exec28_bp_':'exec28_rl_','sec:exec28-bp':'sec:exec28-rl','sp28bp_':'sp28rl_','sp28dl_':'sp28bp_',
      'discovery-delegate and server-boundary':'reinforcement-discovery and dependency-contract',
      'Discovery delegates and local model boundaries':'Reinforcement search and discovery contracts',
    }
    for kind in ['build','publish']:
      for doc in ['reader','sponsor']:
        text=replace((T/f'{kind}_boundary_profile_{doc}_v2_20261028.py').read_text(),mapping)
        text=text.replace("['cdt','ollama','reference']","['zhu','wang','gcastle','cdt','reference']").replace('added==3','added==5').replace('added_citation_records=3','added_citation_records=5')
        text=text.replace('Add inspected CDT delegates and Ollama server originals with exact variable-order and stream-admission witnesses','Add two primary discovery papers,selected RL/CORL source and CDT dependency profiles with exact penalty/keyword witnesses')
        text=text.replace('A banking proposal must preserve variable identity across discovery and execution boundaries.','Reinforcement learning can search for a causal graph without establishing that the graph is identified.')
        text=text.replace('Variable identity and execution identity must survive every boundary before a causal result is admitted.','A discovery optimizer is useful only when its search result preserves the declared causal target and assumptions.')
        text=text.replace("['HTTP','Gaussian','schema','reminder','unload']","['penalty','mask','score','reminder','ordering']")
        text=text.replace('Selected CDT and Ollama server paths are inspected; exact witnesses remain distinct from native behavior.','Two original discovery papers and selected RL/CORL/CDT paths are inspected; exact project qualifications remain distinct from native behavior.')
        text=text.replace('Selected CDT score,order and launcher paths and Ollama routing,streaming and residency contracts with exact authored witnesses','Primary RL discovery assumptions and penalty boundary; selected mask,order,attention and dependency contracts with exact authored witnesses')
        text=text.replace('three additional selected-software and independent-project records','five additional primary-paper,software and independent-project records')
        text=text.replace('Exact finite examples show a label-only permutation reversing the named edge and one admitted result among six stipulated HTTP200 traces','Exact four-graph witness preserves a cyclic tie at the non-strict penalty boundary; strict domination excludes it,and kwargs key/attribute lookup differs')
        text=text.replace('Bind discovery and model execution boundaries','Qualify reinforcement discovery before reuse')
        if kind=='build' and doc=='sponsor':
            text=text.replace("assert text.count('273 genuine scholarly PDFs')==1","assert text.count('271 genuine scholarly PDFs')==1").replace("text=text.replace('273 genuine scholarly PDFs','273 genuine scholarly PDFs')","text=text.replace('271 genuine scholarly PDFs','273 genuine scholarly PDFs')")
        save(f'{kind}_rl_discovery_{doc}_20261028.py',text)
    print('Prepared four preserving RL discovery publication successors.')

if __name__=='__main__':main()
