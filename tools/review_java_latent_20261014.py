#!/usr/bin/env python3
"""Bounded static Java latent-discovery review; no downloaded code execution."""
import hashlib,json
from pathlib import Path
import master_control as core
import run_program as control
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-14/java-latent'
OUTPUT=ROOT/'docs/program/comprehensive-v14/work/SW.CELL.discovery_latent.Java/coverage-review.json'
RAW=ROOT/'docs/literature/raw'
PIN='b89afaf952a4fd647df0d85b08102250106c6764'
def ref(p,a):
 p=Path(p);return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':a}
def write(p,d):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def source(key,anchors,claims,tree):
 r=json.loads((RAW/(key+'.receipt.json')).read_text());p=RAW/(key+'.txt');b=p.read_bytes();assert r['status']=='saved' and r['sha256']==hashlib.sha256(b).hexdigest()
 path=r['url'].split(PIN+'/')[1];indexed={x['path']:x['sha'] for x in tree['tree']};blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==indexed[path]
 return {'source_identity':r['url'],'version_date':PIN+'; selected pre-cutoff commit 2026-09-22','original':ref(p,'; '.join(anchors)),'receipt':ref(RAW/(key+'.receipt.json'),'Acquisition and hash'),'git_blob_sha1':blob,'tree_match':True,'inspected_anchors':anchors,'supported_claims':claims}
def main():
 tree=json.loads((RAW/'v12_sw2_tetrad_tree.json').read_text());assert tree['sha']==PIN and not tree['truncated']
 specs=[('v12_sw2_tetrad_fci',['lines 34-43 class comment','lines 50-67 defaults','lines 330-430 FAS, possible-D-SEP and orientation branches','lines 788-795 selection flag'],['FCI path initializes circle endpoints and returns a graph described as PAG','Possible-D-SEP branch tests one complete candidate set per endpoint at path limit 3','Ordinary finalOrientation call is inside doPossibleDsep branch; guaranteePag is a separate optional step','Default excludeSelectionBias is false; completeRuleSetUsed true']),
 ('exec14_java_latent_rfci',['lines 37-45 RFCI-PAG scope','lines 142-220 search and orientation','lines 566-571 selection flag'],['RFCI is a distinct search route with RFCI-PAG output and selection control']),
 ('exec14_java_latent_orient',['lines 386-406 orient entry','lines 510-642 final orientation; R5-R7 selection restriction'],['Final orientation has a distinct callable path; excluding selection changes applicable rules']),
 ('exec14_java_latent_paths',['lines 1855-1940 possibleDsep traversal and path bound'],['possibleDsep enumerates candidate nodes by graph paths; the returned list is not a set of all subset tests']),
 ('v12_exec13_java_tetrad_endpoint',['lines 32-64 endpoint enum'],['Tail, arrow, circle, star and null are distinct endpoint values']),
 ('exec14_java_latent_edge',['lines 100-142 constructor and flip','lines 196-259 proximal endpoint access','lines 458-490 equality'],['Edge stores two endpoint marks tied to nodes; constructor may reverse node order and must be decoded by proximal endpoint'])]
 sources=[source(*row,tree) for row in specs]
 fci=(RAW/'v12_sw2_tetrad_fci.txt').read_text().splitlines()
 block='\n'.join(fci[329:430]);assert block.count('possibleDsep(')==2 and block.count('checkIndependence(x, y, d)')==2
 assert block.count('fciOrient.finalOrientation(pag, excludeSelectionBias)')==1
 assert block.index('if (this.doPossibleDsep)')<block.index('fciOrient.finalOrientation(pag, excludeSelectionBias)')<block.index('if (guaranteePag)')
 # Independent interchange fixture, not a Tetrad runtime result.
 edges=[('Offer','Recovery','tail','arrow'),('Risk','Offer','circle','arrow'),('Risk','Recovery','arrow','arrow'),('Policy','Offer','tail','tail')]
 valid={'tail','arrow','circle'}; encoded=[]
 for a,b,ma,mb in edges:
  assert ma in valid and mb in valid
  encoded.append({'left':a,'right':b,'left_mark':ma,'right_mark':mb})
 decoded=[(x['left'],x['right'],x['left_mark'],x['right_mark']) for x in encoded]
 assert decoded==edges and ('star' not in valid and 'null' not in valid)
 write(BASE/'endpoint-oracle.json',{'kind':'independent_interchange_fixture','package_execution':False,'input_edges':edges,
    'encoded':encoded,'roundtrip':decoded,'isolated_nodes':['Branch'],'unsupported_java_endpoint_marks':['star','null'],
    'interpretation':['tail-arrow is directed','circle-arrow retains uncertainty','arrow-arrow may encode latent common cause in a PAG','tail-tail can reflect selection in a PAG'],
    'limits':['No Java Edge object constructed','No PAG validity or graph-level distributional guarantee established']})
 paper=ROOT/'docs/papers/Learning high-dimensional directed acyclic graphs with latent and selection variables Colombo(2012).pdf'
 assert paper.read_bytes().startswith(b'%PDF-')
 prior=json.loads((ROOT/'docs/program/execution/2026-10-13/latent-r/source-audit-integrated.json').read_text());claim=next(x for x in prior['sources'] if x.get('id')=='exec13_latentr_colombo2012');assert hashlib.sha256(paper.read_bytes()).hexdigest()==claim['sha256']
 write(BASE/'primary-review.json',{'cutoff':'2026-10-07','source_pin':PIN,'source_tree':ref(RAW/'v12_sw2_tetrad_tree.json','Pinned complete tree and blob identities'),
    'sources':sources,'scholarly_original':{'title':claim['title'],'source_identity':claim['url'],'version_date':claim.get('version_date',claim.get('year')),'original':ref(paper,'Colombo et al. 2012 original; FCI/RFCI latent and selection regimes'),'prior_audit':ref(ROOT/'docs/program/execution/2026-10-13/latent-r/source-audit-integrated.json','Original paper anchors and claims')},
    'static_finding':'Pinned FCI search tests a full possibleDsep candidate set at each endpoint rather than enumerating its subsets in this block; doPossibleDsep=false skips the ordinary finalOrientation call in this source. This is static path evidence, not an executed correctness theorem.',
    'environment':{'java_runtime':'OpenJDK 11.0.32.1','javac':'not found','selected_build_target':'Java 21 in previously audited POM','qualified_execution':False},
    'limits':['No executable Tetrad FCI/RFCI trial','No full dependency tree or endpoint serialization test','No claim that every upstream release shares this behavior']})
 query=json.loads((RAW/'v12_sw_cell_discovery_latent_java.receipt.json').read_text());assert query['status']=='saved'
 review={'operation_id':'SW.CELL.discovery_latent.Java','outcome':'inconclusive','coverage_qualified':False,
    'candidates':[{'name':'Tetrad Java library','alias':'Tetrad GUI and Python/R bridges are surfaces, not independent Java engines','pin':PIN,'scope':'FCI, RFCI and distinct PC candidate'},
                  {'name':'pcalg R','scope':'separately reviewed FCI/RFCI comparator, not Java implementation'},
                  {'name':'causal-learn Python','scope':'separately reviewed PC/FCI comparator, not Java implementation'}],
    'search':{'cutoff':'2026-10-07','route':query['url'],'result_count':6,'stopping_rule':'One ranked OpenAlex page, maximum ten; no exhaustive or absence inference','local_copy':ref(RAW/'v12_sw_cell_discovery_latent_java.json','Discovery metadata only'),'receipt':ref(RAW/'v12_sw_cell_discovery_latent_java.receipt.json','Search request and acquired result')},
    'scientific_target':'PAG/RFCI-PAG under explicit latent and selection assumptions; never silently selected DAG or effect',
    'bank_example':'Unobserved borrower risk may cause both an offer and later recovery; selection into observed servicing records can further alter the graph. PC causal sufficiency is not warranted by table completeness.',
    'positive_findings':['Six pinned Tetrad source files agree with the complete revision tree.','PAG/RFCI-PAG, endpoint marks, selection flag and separate FCI/RFCI paths are present in source.','Independent endpoint fixture preserves marks and isolated nodes under the proposed interchange contract.'],
    'adverse_findings':['The pinned FCI possible-D-SEP path uses only a complete candidate set per endpoint in the inspected block; subset search behavior has not been established.','Disabling possible-D-SEP skips the ordinary finalOrientation call in the inspected search path.','Java 11 runtime and no javac do not meet the audited Java 21 build profile; engine behavior was not executed.'],
    'alternatives':[{'route':'Scoped Tetrad FCI in qualified Java 21 environment','status':'pending','reason':'Needs full dependency closure, endpoint roundtrip and graph-oracle/failure trials.'},
                    {'route':'R pcalg FCI/RFCI','status':'independent comparator','reason':'Source audited, distinct endpoint and search semantics.'},
                    {'route':'Python causal-learn FCI','status':'independent comparator','reason':'Separate pin and conversion contract; no parity assumed.'}],
    'next_action':'Acquire/build a pinned Java 21 dependency environment; run deterministic PAG endpoint, selection/no-selection, possible-D-SEP subset and interruption/numerical-failure fixtures. Resolve the static FCI path concern before any adapter admission. Keep independent R/Python comparators active.',
    'evidence':[ref(BASE/'primary-review.json','Pinned source, original paper and static branch inspection'),ref(BASE/'endpoint-oracle.json','Independent proposed interchange oracle'),ref(ROOT/'docs/program/execution/2026-10-13/java-discovery/exact-results.json','Existing independent nonmonotone conditioning fixture')],
    'limitations':['One-page discovery search is not comprehensive','No qualified Java execution or product capability granted']}
 write(OUTPUT,review)
 graph,_,_=control.combined(ROOT,core.read(ROOT,core.STATE));node=control.ledger.operation(graph,review['operation_id'])
 receipt=control.ledger.receipt_template(node)
 receipt.update(outcome='inconclusive',execution='performed',scope='Static source and interchange review; executable Java FCI/RFCI coverage not qualified',
    reviewer={'name':'Codex author/coordinator','kind':'author'},limitations=review['limitations'],capabilities=[],outputs=[ref(OUTPUT,'Reviewed Java latent-discovery cell')],
    revisit_trigger=review['next_action'])
 findings=['Candidate aliases and bounded pre-cutoff search are identified, but one ranked page does not close every possible Java candidate.',
           'Six genuine source copies match one pinned tree; a named scholarly original is hash checked; no Java execution is invented.',
           'R/Python alternatives and Java environment/algorithm omissions are explicit; no unavailable-source waiver or absence claim.']
 for i,f in enumerate(findings):receipt['criteria'][i].update(verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=review['evidence'])
 write(BASE/'operation-receipt.json',receipt)
 print(json.dumps({'outcome':'inconclusive','sources_verified':len(sources),'java_runtime':'11','javac':False,'qualified_execution':False,'source_branch_concern':True}))
if __name__=='__main__': main()
