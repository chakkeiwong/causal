"""Prepare immutable successors using the verified preserving publication path."""
import json
from pathlib import Path
from prepare_openai_publication_20261028 import replace, save, ref

ROOT=Path(__file__).resolve().parents[1]
T=ROOT/'tools'
DAY=ROOT/'docs/program/execution/2026-10-28'


def main():
    source=DAY/'l6-delegate-review-v1'
    assert json.loads((source/'inspection-review.json').read_text())['inventory_only_files_remaining_in_this_worklist']==0
    targets=['development.tex','sponsor-addition.md','source-audit.json','exact-results.json','mathematical-review.json']
    for name,body in [
        ('copyedit-review.json',dict(status='pass',findings=['Connected collections example distinguishes source observations from proposed contracts.','Partial source paths, warning propagation, backend configuration and README-only limits are explicit.','All numbers are exact authored constructions with stipulated prices; no runtime merit asserted.'],evidence=[ref(source/n,'Reviewed input') for n in ['development.tex','sponsor-addition.md','exact-results.json']])),
        ('review.json',dict(status='pass',issues=[],scope='Finite29 acquired delegates,selected branches and precise qualification implications; not complete L6 acceptance',evidence=[ref(source/n,'Reviewed finite work') for n in ['plan-review.json','input-register.json','inspection-review.json','source-audit.json','mathematical-review.json','development.tex','sponsor-addition.md']],visual_acceptance=False,final_acceptance=False,native_execution=False))]:
        p=source/name;assert not p.exists();p.write_text(json.dumps(body,indent=2)+chr(10))
    target=DAY/'delegate-contract-review-v1';assert not target.exists();target.mkdir()
    for n in targets+['copyedit-review.json','review.json']:(target/n).write_bytes((source/n).read_bytes())
    plan=dict(status='pass',scope='Preserve all1403reader and1054sponsor records; add12selected-source/author records and exact reader pairing.',
        evidence=[ref(source/n,'Finite source and argument review') for n in ['plan-review.json','review.json','inspection-review.json']],
        checks=['All29originals verified by SHA256,Git blob and cutoff identity.','23technical files and6scope documents remain distinct.','Relevant material findings integrate in one preserving wave; no whole-repository or native claim.','Historical omissions are preserved; successor narrows only this finite worklist.','Both unchanged full controllers must pass; no fresh visual acceptance.'])
    (target/'plan-review.json').write_text(json.dumps(plan,indent=2)+chr(10))
    mapping={
        'openai_contract_reference_20261028':'delegate_contract_reference_20261028',
        'openai_contract':'delegate_contract','openai-contract-reader-v1':'delegate-contract-reader-v1',
        'openai-contract-review-v1':'delegate-contract-review-v1','sponsor-openai-contract-v1':'sponsor-delegate-contract-v1',
        'followup-causal-reader-v1':'openai-contract-reader-v1','sponsor-followup-causal-v1':'sponsor-openai-contract-v1',
        'causal_proposal_followup_causal_reviewed_v1_2026-10-28':'causal_proposal_openai_contract_reviewed_v1_2026-10-28',
        'sponsor_proposal_followup_causal_reviewed_2026-10-28':'sponsor_proposal_openai_contract_reviewed_2026-10-28',
        '1400':'1403','1403':'1415','1049':'1054','1054':'1068','exec28_oa_':'exec28_dl_',
        'sec:exec28-oa':'sec:exec28-dl','sp28oa_':'sp28dl_','sp28fr_':'sp28oa_',
        'provider response-state and scientific-admission':'framework-delegate and scientific-completion',
        'Structured outputs and scientific admission':'Framework delegates and scientific completion',
    }
    text=replace((T/'build_openai_contract_reader_20261028.py').read_text(),mapping)
    text=text.replace('added==3','added==12').replace('Add pinned official OpenAI cookbook/SDK contracts and exact scientific-admission/nested-retry witnesses','Add29inspected delegate originals and exact schema weakening,selective retry and completion witnesses')
    save('build_delegate_contract_reader_20261028.py',text)
    names="['langchain','semantic_kernel','dspy','llama_index','haystack','workflows','anthropic','google','ollama','vllm','llamacpp','reference']"
    text=replace((T/'publish_openai_contract_reader_20261028.py').read_text(),mapping)
    text=text.replace("['cookbook','sdk','reference']",names).replace('added_citation_records=3','added_citation_records=12')
    text=text.replace('A structured banking answer must preserve both the scientific target and the state of the computation.','A causal workflow can finish its control flow without producing an admissible causal answer.')
    text=text.replace('The banking decision remains admissible only when its scientific meaning survives the complete request lifecycle.','The causal answer is trustworthy only when its meaning survives validation, scheduling, stopping and recovery.')
    text=text.replace("['1.50','33','schema','reminder','refusal']","['1.25','2.25','schema','reminder','compaction']")
    text=text.replace('Official pinned client and notebook contracts are inspected; authored admission and budget witnesses remain distinct from native behavior.','Selected framework/backend delegates are inspected; exact witnesses remain distinct from native behavior.')
    text=text.replace('Pinned provider parsing,refusal,incomplete/phase and retry contracts with exact authored admission and budget witnesses','Selected framework validation,terminal states,selective retries,schema conversion and recovery contracts with exact authored witnesses')
    text=text.replace('three additional official-software and independent-project records','twelve additional selected-software and independent-project records')
    text=text.replace('Exact finite examples retain one admitted effect among four states,six nested attempts,stipulated1.50USD and33seconds','Exact finite examples retain one admitted effect among four states,five versus nine attempts,stipulated1.25versus2.25USD and strict schema-set inclusion')
    save('publish_delegate_contract_reader_20261028.py',text)
    text=replace((T/'build_openai_contract_sponsor_20261028.py').read_text(),mapping)
    text=text.replace('The program has 350 recorded outcomes of 376','The program has 351 recorded outcomes of 376')
    save('build_delegate_contract_sponsor_20261028.py',text)
    text=replace((T/'publish_openai_contract_sponsor_20261028.py').read_text(),mapping)
    text=text.replace("['cookbook','sdk','reference']",names).replace('Preserve scientific meaning across provider responses','Require scientific completion across framework boundaries')
    save('publish_delegate_contract_sponsor_20261028.py',text)
    print('Prepared reviewed finite-delegate source package and four preserving publication successors.')


if __name__=='__main__':main()
