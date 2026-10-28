"""Inspect exact CDT delegates and retain package/version boundaries."""
import hashlib,json
from pathlib import Path
from run_followup_program_20261028 import ROOT,append,load,bound
from run_followup_program_v2_20261028 import selected
from prepare_followup_program_20261028 import ref,write


def main():
    base=selected();key='CDT.DELEGATES';assert load(ROOT,base)['active']==key
    plan=json.loads((base/'cdt-acquisition-plan.json').read_text());sources=[]
    specs=[[(1,23,'Selected MIT notice;no transitive-rights inference'),(25,59,'Loads pcalg,kpcalg,methods and RCIT;sets stable.fast/majority/conflict options;numCores appears in optionsList but not passed in shown pc call'),(61,102,'Matrix extraction,headerless data/fixed matrices,original positional order and CSV output')],[(1,24,'Selected MIT notice and pcalg dependency'),(26,40,'Reads headerless data;constructs selected score with data only;calls ges;extracts essential graph and writes CSV;numeric-index normalization retained for later fixture')],[(128,148,'Package availability probes do not establish version or rights'),(151,188,'UUID script directory,template copying and literal placeholder substitution'),(190,228,'No-callback branch returns process status;callback branch waits without checking return code then parses output;cleanup differs on errors and interrupt')]]
    for req,spans in zip(plan['requests'],specs):
        p=ROOT/'docs/literature/raw'/(req['id']+'.txt');r=p.with_suffix('.receipt.json');receipt=json.loads(r.read_text());data=p.read_bytes()
        assert receipt['status']=='saved' and receipt['url']==req['url'] and receipt['sha256']==hashlib.sha256(data).hexdigest()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==req['git_blob_sha1']
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,finding in spans:
            assert hi<=len(lines);anchors.append(dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest(),finding=finding))
        sources.append(dict(source_identity=req['url'],version_date='2025-10-13;ff46dbca3d91f2dba30e6ae54986eea30c9b331f',upstream_path=req['upstream_path'],local_copy=ref(p,'Exact inspected original'),acquisition_receipt=ref(r,'Collector receipt'),git_blob_sha1=blob,inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],native_execution=False))
    prior=json.loads((ROOT/'docs/program/execution/2026-10-13/python-discovery/source-audit.json').read_text())['sources']
    cdt=next(s for s in prior if s['integrated_citation_key']=='exec13_pydisc_cdt')
    extras=[('docs/literature/raw/v12_exec13_pydisc_cdt_source_3.txt',[(181,196,'PC conditional-test mapping'),(217,241,'Skeleton order and output labels sorted'),(270,311,'Unconstrained labels retain data order;input CSV is not reordered')]),('docs/literature/raw/v12_exec13_pydisc_cdt_source_4.txt',[(58,70,'Categorical label conflicts with listed Gaussian score names'),(107,146,'int maps to GaussL0penIntScore;constraint and output labels sorted'),(159,209,'Unconstrained labels retain input order;data written without reordering')])]
    for filename,spans in extras:
        p=ROOT/filename;old=next(r for r in cdt['records'] if r['local_copy']['path']==filename);bound(ROOT,old['local_copy']);lines=p.read_text().splitlines()
        sources.append(dict(source_identity=old['source_identity'],version_date=cdt['version_date'],local_copy=old['local_copy'],acquisition_receipt=old['receipt'],inspected_anchors=[dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest(),finding=f) for lo,hi,f in spans],supported_claims=[f for _,_,f in spans],native_execution=False))
    p=ROOT/'docs/literature/raw/exec13_pcalg_classes.txt'
    audit=json.loads((ROOT/'docs/program/execution/2026-10-28/delegate-contract-reader-v1/reader/source-audit.json').read_text())['sources'];pcalg=next(s for s in audit if s['integrated_citation_key']=='exec13_pcalg_reuse_primary');old=next(r for r in pcalg['records'] if r['upstream_path']=='R/AllClasses.R');bound(ROOT,old['local_copy'])
    lines=p.read_text().splitlines();spans=[(620,676,'DataScore target list,row index and ordering'),(697,748,'GaussL0penIntScore is Gaussian;defaults empty intervention target and all rows assigned index1;CDT does not pin this separately selected pcalg version')]
    comparator=dict(source_identity=old['source_identity'],version_date=pcalg['version_date'],local_copy=old['local_copy'],inspected_anchors=[dict(lines=[lo,hi],excerpt_sha256=hashlib.sha256(chr(10).join(lines[lo-1:hi]).encode()).hexdigest(),finding=f) for lo,hi,f in spans],supported_claims=[f for _,_,f in spans],native_execution=False,installed_dependency_equivalence=False)
    # Authored positional witness, not a run of CDT or R.
    labels=['z','a'];matrix=[[0,1],[0,0]]
    edges=lambda names:[(names[i],names[j]) for i,row in enumerate(matrix) for j,value in enumerate(row) if value]
    witness=dict(input_columns=labels,unchanged_matrix=matrix,correct_edges=edges(labels),sorted_labels_only_edges=edges(sorted(labels)),native_execution=False)
    assert witness['correct_edges']!=witness['sorted_labels_only_edges']
    out=base/'cdt-delegates.json'
    write(out,dict(status='performed_selected_source_review',sources=sources,pcalg_comparator=comparator,authored_position_witness=witness,findings=['Three selected missing originals now acquired and inspected.','The int score path selects a Gaussian interventional-score class name,not a categorical likelihood;separate pinned pcalg comparator exposes Gaussian/default-target semantics but is not the resolved CDT dependency.','Direct orientation paths combine sorted skeleton/output labels with original-order data;require explicit common ordering and permutation fixtures before integration.','Callback launcher does not condition output retrieval on process returncode;timeout,diagnostic/cancellation and stale/partial-output trials remain necessary.','Template declares core count without passing it in shown pc call;do not promise parallel scaling.'],remaining=['Exact resolved R,pcalg,kpcalg,RCIT and Python dependency versions and rights.','Native matrix endpoint/orientation,CSV,returncode,large-stderr and interrupted-child fixtures.','Remaining Python search-tail families and full coverage.'],reuse_decision='Conditional thin typed adapter or direct declared pcalg route;defer wholesale port/native enablement until versions,rights and conversion fixtures are satisfied.',evidence=[ref(base/'cdt-acquisition-plan.json','Reviewed acquisition'),ref(Path(__file__),'Exact branch review and independent witness')],full_python_cell='inconclusive',native_execution=False))
    receipt=base/'cdt-delegates-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Exact delegates and bounded comparison')],evidence=[ref(base/'cdt-acquisition-plan.json','Selected originals')],criteria=[dict(index=0,verdict='pass',finding='All three originals match selected Git blobs and receipt SHA256;technical anchors recorded without execution.'),dict(index=1,verdict='pass',finding='Score,label/order and launcher paths traced;separate pcalg comparator and unresolved versions/rights/native qualification explicit.')],next_action='Integrate the bounded source findings with other independent profiles in one preserving publication;continue L1 successor now.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,base);print(json.dumps(dict(originals=3,source_paths=5,comparator_paths=1,next=load(ROOT,base)['next'])))


if __name__=='__main__':main()
