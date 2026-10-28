"""Compare a historical Python tail with the current audited evidence."""
import json
from pathlib import Path
from run_followup_program_20261028 import ROOT,append,load,bound
from run_followup_program_v2_20261028 import selected
from prepare_followup_program_20261028 import ref,write


def main():
    base=selected();key='PYTHON.DELTA';node=load(ROOT,base)['nodes'][key]
    auditpath=ROOT/'docs/program/execution/2026-10-28/delegate-contract-reader-v1/reader/source-audit.json'
    old=ROOT/'docs/program/execution/2026-10-13/python-discovery/omissions-register.json'
    treepath=ROOT/'docs/literature/raw/v12_exec13_pydisc_cdt_tree.json'
    evidence=[ref(old,'Original finite omissions'),ref(auditpath,'Current integrated evidence'),ref(treepath,'Selected CDT tree')]
    start=base/'python-delta-start.json';write(start,dict(task=key,awards_acceptance=False,next_action=node['action'],evidence=evidence));append('start',key,str(start.relative_to(ROOT)),ROOT,base)
    audit={s['integrated_citation_key']:s for s in json.loads(auditpath.read_text())['sources']}
    keys=['exec14_pt_enco','exec14_pt_paper_enco','exec20_gcastle_source','exec13_pydisc_cdt']
    existing=[]
    for k in keys:
        s=audit[k];bound(ROOT,s['local_copy']);existing.append(dict(key=k,title=s['title'],local_copy=s['local_copy'],claims=s.get('supported_claims',s.get('claims')),limits=s.get('limitations',s.get('limits'))))
    originals=json.loads(old.read_text())['omissions'];rows=[]
    for item in originals:
        if item['id']=='PY-CENSUS':
            decision='ENCO source and genuine paper are already integrated under temporal/interventional scope; do not reacquire. Its informative-intervention assumptions do not make it an observational-IID substitute. Reinforcement/attention candidate search and full finite-tail closure remain unresolved.'
        elif item['id']=='CDT-DELEGATES':
            decision='Current selected CDT audit covers wrappers and terms but does not contain the exact pc.R,ges.R and launcher originals; saved tree supplies exact blob candidates. Acquire only these three first.'
        elif item['id']=='CAUSALLEARN-LICENSE-PIN':
            decision='Later causal-learn license files exist at separate acquired pins. Do not silently transfer those terms to the old technical pin; retain exact old-pin license check before distribution.'
        else:
            decision='Retain original scoped omission. This bounded delta does not settle wider nonlinear,missingness,latent,temporal or native qualification.'
        rows.append(dict(original=item,reviewed_delta=decision,full_cell_closed=False))
    tree={x['path']:x for x in json.loads(treepath.read_text())['tree']}
    targets=['cdt/causality/graph/R_templates/pc.R','cdt/causality/graph/R_templates/ges.R','cdt/utils/R.py'];missing=[]
    allreceipts=[]
    for p in (ROOT/'docs/literature/raw').glob('*cdt*.receipt.json'):
        r=json.loads(p.read_text())
        if r.get('status')=='saved':allreceipts.append(r)
    for i,path in enumerate(targets):
        url='https://raw.githubusercontent.com/FenTechSolutions/CausalDiscoveryToolbox/ff46dbca3d91f2dba30e6ae54986eea30c9b331f/'+path
        admitted=[r for r in allreceipts if r.get('url')==url]
        assert not admitted
        missing.append(dict(id='exec28_cdt_delegate_'+str(i),url=url,extension='txt',upstream_path=path,git_blob_sha1=tree[path]['sha'],scope='Selected missing original,not a runtime permission'))
    out=base/'python-delta.json';write(out,dict(status='performed_bounded_delta',omissions=rows,existing_evidence=existing,missing_selected_originals=missing,evidence=evidence+[ref(Path(__file__),'Exact delta and receipt scan')],search_limit='Checks the current integrated audit and matching saved collector receipts; no global source absence claim.',full_python_cell='inconclusive'))
    receipt=base/'python-delta-receipt.json';write(receipt,dict(task=key,awards_acceptance=False,execution='performed',outcome='pass',outputs=[ref(out,'Current evidence and exact missing delegates')],evidence=evidence,criteria=[dict(index=0,verdict='pass',finding='Every original omission dispositioned; ENCO/gCastle existing work retained and target limits explicit.'),dict(index=1,verdict='pass',finding='Only three exact saved-tree delegates selected for acquisition; no blanket repeat of prior review.')],next_action='Acquire exact three CDT delegates through unchanged fixed collector,then inspect without execution.'))
    append('record',key,str(receipt.relative_to(ROOT)),ROOT,base);print(json.dumps(dict(existing_records=4,selected_missing_originals=3,next=load(ROOT,base)['next'])))


if __name__=='__main__':main()
