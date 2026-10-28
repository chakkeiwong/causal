"""Review a finite RL/CORL source and primary-paper worklist with exact limits."""
import hashlib,json
from pathlib import Path
import rl_discovery_boundary_reference_20261028 as exact
from run_followup_program_20261028 import ROOT,append,load,bound
from run_followup_program_v2_20261028 import selected
from prepare_followup_program_20261028 import ref,write

def main():
    base=selected();key='PYTHON.RLTAIL';assert load(ROOT,base)['active']==key
    inputs=[ref(base/n,'Reviewed finite acquisition') for n in ['source-acquisition-plan.json','corl-delegate-plan.json','paper-acquisition-plan.json','paper-custody.json']]
    bound(ROOT,ref(base/'rl-tail-start.json','Preserved active packet start'))
    plans=[json.loads((base/n).read_text()) for n in ['source-acquisition-plan.json','corl-delegate-plan.json']]
    requests=[r for plan in plans for r in plan['requests'] if 'git_blob_sha1' in r and ('rl_tail' in r['id'] or 'corl_delegate' in r['id'])]
    spans={
      'exec28_rl_tail_0':[(149,175,'Defaults select TransformerEncoder,BIC and LR'),(236,258,'Learn binds data and output column labels'),(411,456,'Penalty updates,best sampled graph,LR/QR pruning and final transpose')],
      'exec28_rl_tail_1':[(28,50,'Supported score/regressor types and l1_graph_reg initialization'),(78,93,'Linear normal equations and median-scaled Gaussian process without shown degeneracy guards'),(143,166,'BIC penalties,cycle threshold1e-5 and misspelled positive-l1 attribute l1_grapha_reg'),(172,185,'Score normalization and re-ranking of cached graph scores')],
      'exec28_rl_tail_2':[(188,220,'dag_mask documentation versus getattr on kwargs mapping'),(375,394,'Best ordering conversion,LR/QR pruning and output transpose')],
      'exec28_rl_tail_3':[(205,240,'Cached ordering scores; both BIC branches have edge-count penalties commented out')],
      'exec28_rl_tail_4':[(90,122,'Transformer repeatedly applies attention and feedforward modules'),(145,213,'Q/K/V score construction,softmax dim1,functional dropout without training argument,weighted values and residual')],
      'exec28_rl_tail_5':[(23,110,'LSTM and MLP decode sequential actions via PointerDecoder; masks reset after forward')],
      'exec28_corl_delegate_0':[(113,194,'Categorical pointer action with selected-node mask penalties and one-hot updates')],
      'exec28_corl_delegate_1':[(22,66,'Order-to-graph constructs earlier-row to later-column entries and multiplies an optional binary mask'),(77,115,'Linear pruning regresses variable i on columns selected by row i with default coefficient threshold0.3')],
    }
    records=[]
    for req in requests:
        p=ROOT/'docs/literature/raw'/(req['id']+'.txt');rp=p.with_suffix('.receipt.json');r=json.loads(rp.read_text());data=p.read_bytes()
        assert r['status']=='saved' and r['url']==req['url'] and r['sha256']==hashlib.sha256(data).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==req['git_blob_sha1']
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,f in spans[req['id']]:
            assert hi<=len(lines);anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest(),finding=f))
        records.append(dict(source_identity=req['url'],version_date='2026-05-29;fd8a04f3b57a0f00930406257d5c30dcb91da0a5',upstream_path=req['upstream_path'],local_copy=ref(p,'Exact inspected original'),acquisition_receipt=ref(rp,'Fixed collector receipt'),git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],native_execution=False))
    paperplan=json.loads((base/'paper-acquisition-plan.json').read_text());papers=[]
    specs=[[(3,'Independent additive noises,causal minimality,IID data and additional identifiability restrictions'),(5,'BIC equal-variance variant and Proposition1 penalty condition'),(14,'AppendixB first proof direction'),(15,'AppendixB reverse argument and penalty/search distinction')],[(2,'Additive SEM,causal minimality and ordering framework'),(4,'Masked ordering,pruning and consistency proposition require identifiable SEM; local optimization caveat')]]
    for req,anchors in zip(paperplan['requests'],specs,strict=True):
        p=ROOT/'docs/papers'/(req['title']+' '+req['author']+'('+str(req['year'])+').pdf');text=base/(req['id']+'.txt');pages=text.read_text().split('\f');rp=ROOT/'docs/literature/raw'/(req['id']+'.receipt.json');receipt=json.loads(rp.read_text());assert receipt['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        papers.append(dict(title=req['title'],author=req['author'],year=req['year'],source_identity=req['url'],version_date=req['edition'],local_copy=ref(p,'Genuine original preprint edition'),acquisition_receipt=ref(rp,'Original PDF receipt'),text=ref(text,'Extracted primary text'),inspected_anchors=[dict(physical_page=page,excerpt_sha256=hashlib.sha256(pages[page-1].encode()).hexdigest(),finding=f) for page,f in anchors],supported_claims=[f for _,f in anchors],limitations=['Selected model,method and theorem anchors only; no native replication or complete literature search.']))
    witness=base/'rl-exact-results.json';write(witness,exact.calculate())
    out=base/'python-rl-tail.json'
    findings=['RL is a search over scored graphs; CORL searches orderings and prunes. Neither policy-search success nor attention weights supply identification or graph/effect confidence.','The Zhu Proposition1 non-strict penalty inequality can preserve a cyclic tied minimizer. The authored four-graph score witness satisfies the displayed bounds with lambda1=1,lambda2=0. Optimal values and an optimal DAG may still agree; strict domination excludes this tie. This is a project qualification of the general stated condition,not a claimed defect of BIC experiments.','CORL reads kwargs via getattr rather than mapping lookup in the selected learn method; the ordinary kwargs mapping does not supply the documented dag_mask through that expression. Native fixtures and transitive mask/orientation tracing remain necessary.','RL positive-l1 branch references l1_grapha_reg while initialization stores l1_graph_reg; under the ordinary constructor path without injected attribute this needs correction/testing before enablement.','The order-to-graph/pruning/output transpose path needs an explicit endpoint convention fixture. The CORL score omits an edge-count term on selected complete-order candidates; this alone does not prove ranking error because candidate edge count is fixed.','Selected Transformer attention normalizes dim1 and calls functional dropout without a training argument. Compare intended normalization and evaluation repeatability under a pinned torch version before adoption; do not infer a native outcome here.']
    write(out,dict(status='performed_bounded_primary_review',source_records=records,papers=papers,findings=findings,authored_witness=ref(witness,'Exact equality and kwargs witness'),reference=ref(Path(exact.__file__),'Independent calculation'),preserved_prior=['ENCO reviewed intervention-specific scope','gCastle PC/NOTEARS selected-source review'],remaining=['Independent attention-based discovery families beyond this architecture; finite complementary search not exhausted.','Selected decoder/score/regression/dependency closure and exact native failure/conversion trials.','No wholesale code adoption; root notice does not settle transitive dependency rights.','No latent,dependent-panel or graph-confidence guarantee from these IID/additive-model papers.'],reuse_decision='Conditional isolated public-data research adapter after mask,penalty,orientation and evaluation fixtures; defer port and native activation.',full_python_cell='inconclusive',evidence=inputs+[ref(Path(__file__),'Exact source/paper review')],native_execution=False))
    receipt=base/'rl-tail-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Eight source originals,two primary papers and precise limits')],evidence=inputs,criteria=[dict(index=0,verdict='pass',finding='Existing ENCO and gCastle PC/NOTEARS preserved; only distinct RL/CORL originals selected.'),dict(index=1,verdict='pass',finding='Eight exact code originals and two genuine primary PDFs inspected; source issues,theorem boundary and remaining attention coverage explicit.')],next_action='Review independent CDT dependency packet,then integrate RL/CORL argument and exact theorem boundary into a preserving successor.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,base);print(json.dumps(dict(source_files=len(records),primary_papers=len(papers),full_cell='inconclusive',next=load(ROOT,base)['next'])))

if __name__=='__main__':main()
