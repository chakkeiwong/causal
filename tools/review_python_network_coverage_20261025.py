#!/usr/bin/env python3
"""Authenticate pinned originals and review Python network proposal evidence."""
import argparse,hashlib,json
from pathlib import Path
import python_network_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/python-network-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.networks_interference.Python'
read=lambda p:json.loads(p.read_text())
SPECS=read(BASE/'anchor-specifications.json')
LIMITS=['Bounded Python searches, selected originals and uninspected tails; no saturation or absence claim.',
 'No acquired code, native package, upstream test, simulator or neural training executed.',
 'Authored expression/helper witnesses are not observed fitted-package benchmark results.',
 'Complete dependencies, installed artifacts, rights and native scientific qualification remain open.',
 'Unknown graph/assignment truth and arbitrary hidden dependence require information or justified restrictions.',
 'No theorem imported from source comments; visual, independent, bank and final acceptance remain open.']
NEXT='Complete Python network search tails and primary delegates; qualify exact assignment and exposure laws, batch-order invariance, covariance aggregation, focal/target compatibility, support predicates, sample accounting, policy weights and empty-selection handling on frozen known-law public tasks before native admission.'
DECISIONS=['ANI: conditional adapter after local-kernel fallback, order-invariance and graph/support tests.',
 'GraphDML: conditional adapter after population compatibility, contrast-valid covariance aggregation and dependence-law qualification; preserve explicit cluster-summary option.',
 'Targeted interference: architecture reference; defer direct adoption pending target derivation,isolate/device behavior,heldout oracle governance and rights.',
 'CausalMotifs: conditional partition-learning reference after Boolean/support,assignment-law and dependent-uncertainty tests.',
 'CausalGraphCut: allocation-design reference; defer direct adoption pending graph arguments,integer/sample accounting,adaptive-design validation and rights.',
 'Causal-PIE: policy reference; defer direct adoption pending probability-law,empty-support,matching,horizon,trajectory and rights gates.']

def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'source-selection.json')+read(BASE/'delegate-selection.json');assert len(rows)==48
    originals=[];evidence=[]
    for x in rows:
        p=RAW/(x['id']+'.txt');data=p.read_bytes();rp=p.with_suffix('.receipt.json');r=read(rp)
        assert len(data)==x['bytes'] and r['status']=='saved' and core.sha(p)==r['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['git_blob']
        originals.append(dict(repository_path=x['path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'URL,date,hash')))
    for key in SPECS:
        c=read(RAW/f'exec25_pnet_{key}_commit.json');c=c[0] if isinstance(c,list) else c
        assert c['sha']==SPECS[key][2].split(';')[-1] and c['commit']['committer']['date'][:10]<='2026-10-07'
        assert read(RAW/f'exec25_pnet_{key}_tree.json')['truncated'] is False
        evidence.extend(ref(RAW/f'exec25_pnet_{key}_{kind}.json','Dated pin and complete selected tree') for kind in ['commit','tree'])
    write(BASE/'authenticated-originals.json',dict(status='pass',count=48,originals=originals,evidence=evidence))
    fragments=[];sources=[]
    for key,(title,repo,version,checks) in SPECS.items():
        evidence=[ref(RAW/f'exec25_pnet_{key}_commit.json','Revision and date')];anchors=[];claims=[]
        for suffix,lo,hi,tokens,finding in checks:
            p=RAW/f'exec25_pnet_{key}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));s='\n'.join(lines[lo-1:hi]);assert all(t in s for t in tokens),(p,lo,hi)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=key,source=binding,first_line=lo,last_line=hi,text=s))
        sources.append(dict(integrated_citation_key='exec25_pnet_'+key,kind='software',title=title,author=repo+' contributors',year=int(version.split(';')[1][:4]),source_identity='https://github.com/'+repo+'/tree/'+version.split(';')[-1],version_date=version,local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=len(fragments)))
    assert exact.calculate()==read(BASE/'exact-preflight.json');write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_pnet_search*.json')):
        if 'receipt' in p.name:continue
        d=read(p);rp=p.with_suffix('.receipt.json');assert core.sha(p)==read(rp)['sha256']
        for x in d['items']:leads.setdefault(x['full_name'],dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected'))
        queries.append(dict(query=read(rp)['url'],total=d['total_count'],returned=len(d['items']),incomplete_results=d['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(rp,'Query identity')))
    for repo in [x[1] for x in SPECS.values()]:
        if repo in leads:leads[repo]['status']='selected_primary_anchors_only'
    assert len(leads)==54 and len(fragments)==50
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),additional_named_candidates=[x[1] for x in SPECS.values()],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Original identities and exact anchors') for n in ['authenticated-originals.json','inspected-extracts.json']],groups=6,anchors=50,native_execution=False))
    checks=['ANI path-score variances -2/9 and2/9; fallback changes later contrast to1/9 depending on batch order.',
      'Three positive-definite covariance matrices with determinant1 have elementwise median determinant-3 and total quadratic-2.',
      'One-rule arithmetic illustrates addition-before-equality; native array/caller test remains open.',
      '4096 nodes yield256 unwrapped default clusters; signed8bit arithmetic wraps to0;7 requested samples yield5 in full batches.',
      'Own0/neighbor1 with p1/5 has true probability4/25,uniform traversal factor1/10 and MC-limit factor1/25.',
      'Identical zero embeddings fail strict relative match; empty-selection sentinel can contribute3/5 from hypothetical residual6/count10.',
      'Hypothetical cost denominators reproduce30,50,75.']
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored arithmetic'),ref(BASE/'exact-results.json','Exact replay')],checks=checks,native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Python exposure,assignment,population,uncertainty and policy contracts',selected=list(SPECS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'primary-review.json','Selected declarations'),*evidence],findings=['ANI has BSD3 original;GraphDML and CausalMotifs have MIT originals.','No license-named original occurs in the selected complete targeted_interference,CausalGraphCut or Causal-PIE trees; no rights grant inferred.','CUDA-specific allocations,scientific Python requirements and custom spectral delegate inspected;complete transitive and installed-artifact rights remain open.'],integration_allowed=False))
    tests=['Tiny exact assignment spaces and joint exposure probabilities','Integer labels,edge orientation,weights,isolates and exactly-two-hop operators','Batch-order invariant variance and actual fallback-kernel reporting','Positive-semidefinite repeated covariance and total contrasts','Focal/target compatibility and common-shock cluster summaries','Boolean support rules,zero empirical probability and population accounting','Frozen training/model selection and inaccessible final synthetic oracles','GraphCut integer ranges,batch remainders,return-path definitions and adaptive law','Policy own-action factors,weighted traversal,empty selection and zero embeddings','Trajectory/horizon separation,terminal handling and collapsed RKHS bandwidth','Complete artifacts,rights,requests,refusals and cost denominators']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,owners=['Scientific author','Adapter owner','Artifact/rights owner','Evaluation reviewer'],native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded search tails')],known_routes=['Inspect missing primary delegates and settle artifact provenance and distribution rights.','Freeze tiny known-law targets,assignment laws and evaluation oracles before native experiments.'],unknown_universal_repairs=['Unknown graph truth,unobserved confounding and arbitrary dependent uncertainty have no universal promised repair.'],next_action=NEXT))
    sources.append(dict(integrated_citation_key='exec25_pnet_choice',kind='project_evidence_not_scholarly_paper',title='Authored Python network source comparison and public qualification design',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October2026;cutoff7 October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json']],inspected_anchors=[dict(anchor='Assignment,exposure,uncertainty,population,policy and cost comparisons',inspection='Author inspection')],supported_claims=['48 selected original files and50anchors;54bounded search leads.','Exact authored arithmetic and conditional candidate decisions.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=7,new_scholarly_pdfs=0,evidence=[ref(BASE/'authenticated-originals.json','48authentic originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed evidence') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['48authenticated originals,50anchors,sixcollections plus authored comparison.','Custom spectral delegate and cluster-summary method preserve positive capabilities;avoid unsupported absence claims.','No optimizer selection from heldout truth inferred;no helper witness asserted as native fit.','Preserve prior citations and serialize publication after R delivery exit.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Six distinct targets and candidate-specific adoption routes.','Source expressions,authored examples and native/scientific qualification separated.','Rights,search,visual and final gates retained.'],visual_acceptance=False))
    names=['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md','anchor-specifications.json']
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Reviewed bounded comparison') for n in names]+[ref(Path(__file__),'Review logic')],findings=['48 authentic originals and50verified anchors;source/native distinction retained.','Exposure,assignment,uncertainty,population and policy contracts explicit.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=48,anchors=50,unique_leads=54,new_records=7,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'))
    graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected source review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Selected Python network candidates identified;search,delegate and native coverage incomplete.','Claims bind authentic dated bytes and anchors;no scholarly theorem imported.','Alternatives and public qualification routes retain numerical,rights and native limits.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Python network exposure,assignment,uncertainty,population and policy source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Python network inconclusive receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
