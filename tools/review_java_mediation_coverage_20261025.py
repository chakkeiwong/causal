#!/usr/bin/env python3
"""Audit Java mediation/SEM source contracts without executing downloaded code."""
import argparse,hashlib,json
from pathlib import Path
import java_mediation_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/java-mediation-coverage-v1';RAW=ROOT/'docs/literature/raw';OP='SW.CELL.mediation_sensitivity.Java';read=lambda p:json.loads(p.read_text())
LIMITS=['Six bounded repository queries do not establish absence or complete JVM coverage.','29authentic originals and selected delegates;no downloaded Java,Julia or R code executed.','Authored exact algebra and static control-flow witnesses are not native failure-rate measurements.','Named Onyx scholarly identity lacks a retained genuine PDF and is not cited as technical evidence.','Complete rights,installed artifacts,dependent uncertainty,public native trials and final acceptance remain open.','No fresh visual or independent acceptance;no authentic bank or operational adoption.']
NEXT='Complete JVM candidate and primary-paper routes;reconcile treatment-disturbance intervention,parameter restoration,zero-variance and bounded-path semantics;qualify RAM failure propagation and target-language export round trips with public exact-law fixtures,rights,complete failures and costs.'
DECISIONS=['Tetrad:conditional graph/SEM reuse;retain correlated-error and intervention restrictions,failed parent-set denominators and bounded-search incompleteness.','Tetrad total-effect helper:reject blanket interpretation under correlated treatment errors;require structural surgery,typed zero variance and fixed-parameter rollback tests.','Onyx:conditional graphical/RAM candidate;defer backend admission until singular-state failure propagation and export direction parity are qualified.','Onyx exports:compare exact graph and equations before runtime estimates;retain missingness defaults,definition-edge refusal and name mapping.','Equation-level port only after declared benefit and scientific equivalence;no native capability or umbrella rights admission.']
ANCHORS={
 'tetrad':[
 ('03',2860,2910,'getTotalEffect','Directed coefficient surgery retains error covariance;zero variance returns0;zeroing precedes protected restoration.'),
 ('03',779,796,'getFreeParameters','Selected setter rejects nonfree/nonmean parameters and invalidates covariance and standard-error caches.'),
 ('03',2492,2505,'return this.errCovar','Error covariance is retained by the implied covariance path.'),
 ('03',2671,2677,'MatrixUtils.impliedCovar','Transpose of edge coefficients and full error covariance feed the helper.'),
 ('13',478,516,'m3.times(errCovar)','Implied covariance uses inverse(I-B),error covariance,and transpose.'),
 ('05',399,429,'SemOptimizerPowell','Default optimizer separates fixed/cyclic/correlated,latent and local-regression cases.'),
 ('06',96,142,'covxx.inverse','Local regression optimizer fits parent coefficients and residual variance.'),
 ('03',2163,2226,'Double.NaN','Parameter standard errors have data,latent and dimension restrictions;not product uncertainty.'),
 ('07',166,203,'catch (Exception','IDA parent-set enumeration catches failed configurations before returning effects.'),
 ('08',204,247,'NO_PD_PATHS','Eligibility uses bounded potentially directed search;documentation directs zero after an empty search.'),
 ('14',847,879,'path.size() - 1 > maxLength','Path traversal enforces edge-count cutoff and avoids repeated nodes.')],
 'onyx':[
 ('01',9,64,'Apache 2.0','Graphical SEM,Java runtime,exports,Apache declaration and separate dependency licenses.'),
 ('04',39,50,'Sigma =','RAM covariance and matrix derivative definition.'),
 ('04',831,857,'Warning: Accelerating cycle','Failed inverse emits warning and evaluation continues with the buffer.'),
 ('07',626,667,'Matrix is singular','Inverse buffer initialized to identity;exact singular pivot throws.'),
 ('08',286,305,'isIndirectData','Indirect data flag concerns supplied distribution/summary data,not a mediated causal effect.'),
 ('14',105,165,'createEdgeString(edge, "ON"','Generic exporter dispatches observed and latent directed edges with explicit ON/BY branches.'),
 ('11',32,45,'missing=','Lavaan export uses fixed.xFALSE,FIML and definition-edge validity predicate.'),
 ('11',93,114,'tname + " ~ "','Lavaan ON branch retains target-on-source regression orientation.'),
 ('10',106,125,'tname + " →  "','Julia ON branch emits target-to-source arrow while BY emits source-to-target.'),
 ('15',163,197,'duplicateName','Shared sanitized-name mapping attempts collision resolution.')]
}

def prepare():
    assert not (BASE/'review.json').exists();pins={x['key']:x for x in read(BASE/'pins.json')};rows=read(BASE/'selected-originals.json')+read(BASE/'followup-originals.json');assert len(rows)==29
    originals=[];ids=[]
    for g,pin in pins.items():
        cp=RAW/('exec25_jmed_'+g+'_commit.json');tp=RAW/('exec25_jmed_'+g+'_tree.json')
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        assert read(cp)[0]['sha']==pin['commit'] and pin['date']<='2026-10-07T15:59:59Z';tree=read(tp);assert tree['sha']==pin['commit'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};ids.extend([ref(cp,'Pinned revision/date'),ref(tp,'Complete selected tree')])
        for row in [x for x in rows if x['group']==g]:
            p=ROOT/row['local_path'];r=read(ROOT/row['receipt']);data=p.read_bytes();assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==row['url'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']];originals.append(dict(group=g,upstream_path=row['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(ROOT/row['receipt'],'Bound retrieval'),git_blob=row['git_blob']))
    write(BASE/'authenticated-originals-final.json',dict(status='pass',count=29,originals=originals,evidence=ids))
    sources=[];fragments=[]
    for g,checks in ANCHORS.items():
        pin=pins[g];evidence=[ref(RAW/('exec25_jmed_'+g+'_commit.json'),'Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/('exec25_jmed_'+g+'_src'+suffix+'.txt');data=p.read_bytes();encoding='latin-1' if g=='onyx' and suffix=='07' else 'utf-8';lines=data.decode(encoding).splitlines();excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(g,suffix,lo,token)
            binding=ref(p,'Lines{}-{}:{}'.format(lo,min(hi,len(lines)),finding));evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding,inspection_decoding=encoding));claims.append(finding);fragments.append(dict(group=g,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=excerpt,inspection_decoding=encoding))
        for row in [x for x in rows if x['group']==g and x['upstream_path'] in ['LICENSE','pom.xml','apache20-preamble.txt']]:evidence.append(ref(ROOT/row['local_path'],'Selected rights/dependency text'))
        sources.append(dict(integrated_citation_key='exec25_jmed_'+g,kind='software',title=g+' pinned Java mediation,SEM and export source contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['commit'],version_date=pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));assert read(BASE/'exact-results.json')==exact.calculate()
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_jmed_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p);queries.append(dict(original=ref(p,'Discovery only'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==6
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-final.json','Selected authentic declarations')],findings=['Tetrad selected GPL3 license;Onyx Apache2 declaration with separately named LGPL,MIT andEPL dependencies.','Source snapshot is not installed-artifact or complete dependency clearance.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent finite algebra'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'inspected-extracts.json','Static delegate chain')],findings=['Positive-definite disturbance covariance determinant11/16;structural total11 versus retained-correlation ratio25/2.','Mediator-outcome correlation yields regression product9 rather than structural8 despite total11.','Indirect-product delta variance33/25 rather than1 when covariance retained.','Three-edge path has total24 despite a two-edge search finding no complete path.','Scalar singular inverse has no mathematical solution;continued buffer expressions1and2 are static,not native output.','Literal export direction differs across ON branches;target runtime parity remains unverified.','Hypothetical USD150000 overstatement reproduces;not bank data.'],native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Java mediation,structural covariance and portable diagram contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    tests=['Freeze structural graph,target,clock,contrast,error covariance and measured/latent variable identities.','Enumerate linear paths and correlated-disturbance intervention laws.','Inject fixed-parameter errors,zero assignment variance and verify full state rollback.','Compare bounded path enumeration with complete reachability;never turn truncation into causal zero.','Reject singular RAM models;test near-singular residuals,conditioning and cache invalidation.','Round-trip graph directions,means,fixed/shared parameters,correlated errors,definition edges and sanitized labels across target versions.','Qualify product covariance and graph uncertainty under each sampling law;retain all attempted and failed configurations.','Use public generated known-law systems,complete costs and rights before bank experiments.']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,independent_branches=True,native_execution=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Bounded query scope'),ref(BASE/'identity-omissions.json','Weka pre-cutoff identity empty'),ref(BASE/'paper-access-review.json','Onyx genuine PDF not retained'),ref(BASE/'dependency-license-review.json','Rights limits')],known_routes=tests,uninspected=['Other JVM implementations,negative-control/path-specific methods and full source delegates.','Onyx scholarly candidate and complete installed artifact chain.'],unknown_universal_repairs=['Covariance fit does not identify arbitrary hidden assignment or mediator-outcome truth.','Unrestricted nonlinear and dependent mediation needs additional assumptions and theory.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals-final.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_jmed_choice',kind='project_evidence_not_scholarly_paper',title='Authored Java intervention,path,uncertainty and export qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence,inspected_anchors=[dict(anchor='Java source choices and public qualification',inspection='Author inspection')],supported_claims=['29authentic source originals,two concrete Java component comparisons and exact independent witnesses.','Conditional reuse,refusal,port and public qualification routes;unavailable paper not cited technically.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=3,new_scholarly_pdfs=0,evidence=evidence,native_execution=False));write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Extend prior graph/IDA reuse with mediation-specific source delegates.','No scholarly claim based on metadata-only Onyx candidate.','Scientific restrictions and exact witnesses precede any native admission;independent work continues.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Explained equations,assumptions,state behavior,export alternatives and bank-value consequence.','Static findings and mathematical derivations kept distinct from native observation.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=29,scholarly_originals=0,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(review='pass_for_selected_work',originals=29,anchors=len(fragments),new_records=3,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']];findings=['Two concrete Java source comparisons inspected;bounded search and native coverage remain incomplete.','Dated authentic sources and exact authored witnesses support the technical claims;unavailable paper not admitted.','Conditional reuse,port and refusal routes retain scientific,rights,artifact and acceptance conditions.'];result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Java mediation and structural/export source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT);run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Java mediation coverage receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
