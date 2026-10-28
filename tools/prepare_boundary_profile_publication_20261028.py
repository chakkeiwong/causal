"""Create immutable successor scripts using the verified preserving builders."""
from prepare_openai_publication_20261028 import T,replace,save

def main():
    mapping={
      'delegate_contract_reference_20261028':'boundary_profile_reference_20261028',
      'delegate_contract':'boundary_profile','delegate-contract-reader-v1':'boundary-profile-reader-v1',
      'delegate-contract-review-v1':'boundary-profile-review-v1','sponsor-delegate-contract-v1':'sponsor-boundary-profile-v1',
      'openai-contract-reader-v1':'delegate-contract-reader-v1','sponsor-openai-contract-v1':'sponsor-delegate-contract-v1',
      'causal_proposal_openai_contract_reviewed_v1_2026-10-28':'causal_proposal_delegate_contract_reviewed_v1_2026-10-28',
      'sponsor_proposal_openai_contract_reviewed_2026-10-28':'sponsor_proposal_delegate_contract_reviewed_2026-10-28',
      '1403':'1415','1415':'1418','1054':'1068','1068':'1073','exec28_dl_':'exec28_bp_',
      'sec:exec28-dl':'sec:exec28-bp','sp28dl_':'sp28bp_','sp28oa_':'sp28dl_',
      'framework-delegate and scientific-completion':'discovery-delegate and server-boundary',
      'Framework delegates and scientific completion':'Discovery delegates and local model boundaries',
    }
    names="['langchain','semantic_kernel','dspy','llama_index','haystack','workflows','anthropic','google','ollama','vllm','llamacpp','reference']"
    for kind in ['build','publish']:
      for doc in ['reader','sponsor']:
        text=replace((T/f'{kind}_delegate_contract_{doc}_20261028.py').read_text(),mapping)
        text=text.replace(names,"['cdt','ollama','reference']")
        text=text.replace('added==12','added==3').replace('added_citation_records=12','added_citation_records=3')
        text=text.replace('Add29inspected delegate originals and exact schema weakening,selective retry and completion witnesses','Add inspected CDT delegates and Ollama server originals with exact variable-order and stream-admission witnesses')
        text=text.replace('A causal workflow can finish its control flow without producing an admissible causal answer.','A banking proposal must preserve variable identity across discovery and execution boundaries.')
        text=text.replace('The causal answer is trustworthy only when its meaning survives validation, scheduling, stopping and recovery.','Variable identity and execution identity must survive every boundary before a causal result is admitted.')
        text=text.replace("['1.25','2.25','schema','reminder','compaction']","['HTTP','Gaussian','schema','reminder','unload']")
        text=text.replace('Selected framework/backend delegates are inspected; exact witnesses remain distinct from native behavior.','Selected CDT and Ollama server paths are inspected; exact witnesses remain distinct from native behavior.')
        text=text.replace('Selected framework validation,terminal states,selective retries,schema conversion and recovery contracts with exact authored witnesses','Selected CDT score,order and launcher paths and Ollama routing,streaming and residency contracts with exact authored witnesses')
        text=text.replace('twelve additional selected-software and independent-project records','three additional selected-software and independent-project records')
        text=text.replace('Exact finite examples retain one admitted effect among four states,five versus nine attempts,stipulated1.25versus2.25USD and strict schema-set inclusion','Exact finite examples show a label-only permutation reversing the named edge and one admitted result among six stipulated HTTP200 traces')
        text=text.replace('Require scientific completion across framework boundaries','Bind discovery and model execution boundaries')
        save(f'{kind}_boundary_profile_{doc}_20261028.py',text)
    print('Prepared four preserving boundary-profile successors.')

if __name__=='__main__':main()
