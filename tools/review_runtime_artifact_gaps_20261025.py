#!/usr/bin/env python3
"""Reconcile exact retained component/weight gaps without granting adoption rights."""
from copy import deepcopy
from collections import Counter
import base64,json,re
from pathlib import Path
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-25/runtime-artifact-gaps-v1'
RAW=ROOT/'docs/literature/raw'
read=lambda p:json.loads(p.read_text())

def main():
    assert not BASE.exists();BASE.mkdir()
    inherited=read(ROOT/'docs/program/repair-v12/work/LA01/source-audit.json');verify_bindings(inherited)
    selected=[x for x in inherited['sources'] if x.get('id') in ['v12_la_package_llm_cd','v12_la_package_llm_scd','v12_la_package_lcm']]
    assert len(selected)==3
    receipts=[]
    names=['v12_la_llm_cd_tree','v12_la_llm_scd_tree','v12_la_lcm_tree','v12_la_llm_cd_source_1','v12_la_llm_cd_source_2','v12_la_lcm_source_1','v12_la_lcm_license','exec15_latent_lcm_1','exec15_latent_lcm_8']
    import hashlib
    for name in names:
        receipt=RAW/(name+'.receipt.json');d=read(receipt);assert d['status']=='saved'
        paths=[p for p in RAW.glob(name+'.*') if not p.name.endswith('.receipt.json')];assert len(paths)==1
        p=paths[0];assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']
        receipts.append(dict(source_identity=d['url'],original=ref(p,'Retained exact primary bytes'),receipt=ref(receipt,'Historical fixed-collector retrieval')))
    trees={k:read(RAW/('v12_la_'+k+'_tree.json')) for k in ['llm_cd','llm_scd','lcm']}
    assert all(t['truncated'] is False for t in trees.values())
    inventory={}
    for k,t in trees.items():
        blobs=[x for x in t['tree'] if x['type']=='blob']
        notices=[x for x in blobs if any(w in Path(x['path']).name.lower() for w in ['license','copying'])]
        inventory[k]=dict(tree_entries=len(t['tree']),files=len(blobs),notice_paths=[x['path'] for x in notices],root_notice_paths=[x['path'] for x in notices if '/' not in x['path']],artifacts=[dict(path=x['path'],git_blob_identity=x['sha'],size=x.get('size')) for x in blobs if x['path'].endswith(('.jar','.class','.ckpt','.pkl','.pt','.pth','.ipynb'))],git_identity_is_not_local_sha256=True)
    assert inventory['llm_cd']['root_notice_paths']==[] and 'BI-CaMML/LICENSE.txt' in inventory['llm_cd']['notice_paths']
    assert inventory['llm_scd']['root_notice_paths']==[]
    notice=(RAW/'v12_la_llm_cd_source_2.txt').read_text();assert 'Redistribution and use in source and binary forms' in notice
    req=(RAW/'v12_la_llm_cd_source_1.txt').read_text();assert 'gurobipy==10.0.2' in req and 'pygobnilp==1.0' in req
    manifest=(RAW/'v12_la_lcm_source_1.txt').read_text();assert 'pytorch-lightning==2.0.8' in manifest and '"torch"' in manifest
    loader=(RAW/'exec15_latent_lcm_8.txt').read_text();assert 'weights_only=False' in loader and 'return None' in loader
    readme=(RAW/'exec15_latent_lcm_1.txt').read_text();links=re.findall(r'https://drive.google.com/[^)\s]+',readme)
    assert len(links)>=7
    write(BASE/'primary-source-records.json',dict(sources=selected,additional_primary_records=receipts,tree_inventory=inventory,external_checkpoint_links=links,cutoff='2026-10-07T15:59:59Z',new_network_requests=0,downloaded_code_executed=False))
    items=[
        dict(component='LLM-CD',commit='8ea28948affdab88bee91a8b7858e89dc9424ffe',disposition='defer_runtime_adoption',observed=['Complete pinned tree lacks a root notice; historical root-license endpoint returned404.','Nested BI-CaMML notice states source/binary redistribution conditions,notice retention and nonendorsement.','Pinned requirements include gurobipy10.0.2,pygobnilp1.0 and compiled/runtime dependencies; file is not an installed dependency lock.','Numerous retained tree entries are compiled artifacts; listing identity does not establish corresponding source-build provenance.'],unknown=['Project-wide source permission and exact component boundaries.','Transitive installed artifacts,commercial solver entitlement and complete distribution conditions.','Compiled artifact-to-source/build mapping.'],next_action='Acquire a project-authoritative root/component permission statement or choose a separately reviewed implementation;bind every required Java/Python/native artifact and solver entitlement before runtime adoption.',prototype_alternative='Use the inspected scientific idea as a design lead; qualify a separately authorized implementation against independent public fixtures without copying unresolved components.'),
        dict(component='LLM-and-SCD',commit='5aaeaea89e71e2cff443289e473c06d2f79172c5',disposition='defer_runtime_adoption',observed=['Complete retained tree lacks root license,README and environment manifest.','Notebook/data paths exist; their existence alone is not source-paper or execution reproducibility.','Historical README/license API routes returned404; this is not a global absence claim.'],unknown=['Authoritative source/data permissions.','Notebook execution order,full model/service identities and dependency environment.','Exact alignment of outputs to the inspected paper version.'],next_action='Obtain authoritative permissions and a reproducible environment/source-paper map or reject direct runtime reuse while retaining the scientific literature separately.',prototype_alternative='Draft the scientific contract and independent evaluation fixtures; do not label an unrun notebook as an integrated capability.'),
        dict(component='LCM',commit='b6d386913bb63e16b79439204ce06fd215baafd6',disposition='defer_exact_checkpoint_runtime_adoption',observed=['Root code notice is Apache2.0; this is a code-notice observation,not complete component or checkpoint rights clearance.','Four named pretrained model links and three experiment-folder links point to external Drive artifacts.','Pinned manifest leaves multiple dependency versions open and distinguishes optional baseline/notebook dependencies.','Pinned loader uses load_from_checkpoint with weights_onlyFalse and returnsNone for missing or exceptional loads.','Vendored benchmark/causalnex paths and a baseline transformer checkpoint are distinct from the four advertised LCM weights.'],unknown=['Exact downloaded weight bytes,SHA256,version,training/provenance records and applicable terms.','Full resolved dependency and vendored-component rights inventory.','Artifact loading,shape/clock/causal-assumption and error-result conformance.'],next_action='Acquire the named model artifacts through an authorized retained-original route,bind bytes and terms,and qualify loader and output contracts in an admitted environment;do not substitute the in-tree baseline checkpoint for the advertised LCM model.',prototype_alternative='Specify the architecture and finite synthetic tests without loading unaudited weights;consider a separately scoped public-data prototype after its inputs and runtime are reviewed.')]
    for item in items:item['evidence']=ref(BASE/'primary-source-records.json','Exact pinned component inventory and inspected originals')
    write(BASE/'remaining-artifact-register.json',dict(status='precise_local_deferments_not_global_blocker',items=items,legal_clearance=False,native_admission=False,source_cutoff='2026-10-07T15:59:59Z',new_network_requests=0))
    prior=BASE.parent/'benchmark-oracles-v1/census-register.json';reg=deepcopy(read(prior));row=next(x for x in reg['items'] if x['id']=='LA01-runtime-licenses')
    row.update(effect_on_claims='Three pinned artifact inventories and exact unresolved permission,weight,dependency and loader requirements are now recorded;runtime adoption remains unqualified.',source_followup=ref(BASE/'remaining-artifact-register.json','Concrete component-specific admission gaps'),next_action='Resolve the exact component permissions,weight bytes/provenance and dependency identities in the artifact register;where external originals are unavailable,use a separately scoped authorized prototype path. Do not repeat unchanged404or blocked artifact routes.')
    assert Counter(x['disposition'] for x in reg['items'])==Counter(x['disposition'] for x in read(prior)['items'])
    reg.update(supersedes=ref(prior,'Preserved census and finite-oracle progress'),changes=['Runtime-rights obligation now has three exact component/artifact admission registers;no disposition closed.'],closure=False)
    write(BASE/'census-register.json',reg)
    write(BASE/'review.json',dict(status='pass_for_precise_source_inventory_not_rights_clearance',evidence=[ref(BASE/'primary-source-records.json','Originals and exact inventory'),ref(BASE/'remaining-artifact-register.json','Observed,unknown and continuation separately'),ref(BASE/'census-register.json','Unchanged dispositions'),ref(Path(__file__),'Bounded source reviewer')],findings=['All claims limited to historical pinned originals and explicitly inspected paths.','Nested notices are not promoted to blanket repository permission.','External weights are not replaced by in-tree baseline artifacts.','No installed runtime,legal clearance or native conformance inferred.'],global_blocker=False,publication_pending=True))
    verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(review='pass',components=3,rights_clearance=False,native_admission=False,census_dispositions_changed=0)))
if __name__=='__main__':main()
