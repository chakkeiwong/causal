#!/usr/bin/env python3
"""Historical libDAI proposal reference review; no acquired code executed."""
import argparse,hashlib,json
from pathlib import Path
import libdai_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/libdai-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='6df66a8ce7eb6f669bae933ab6ec35bbba56182f';OP='SW.DECISION.seed_081';read=lambda p:json.loads(p.read_text())
TITLE='libDAI A Free and Open Source C++ Library for Discrete Approximate Inference in Graphical Models'
PAPER=ROOT/'docs/papers'/(TITLE+' Mooij(2010).pdf')
LIMITS=['Historical2012mirror only;official current provenance and complete dependencies unresolved.',
 'Paper describes0.2.7/GPL;selected mirror declares0.3.0/BSD;do not conflate versions.',
 'No downloaded code or build executed;finite witnesses and conditional static findings are authored.',
 'Inference requires a supplied probability model;convergence is not accuracy,causal identification or statistical uncertainty.',
 'Reference only;no native,independent,visual,bank or final acceptance;actual costs unmeasured.']
SPECS={
 'exec24_libdai_source_0':[(41,118,'Factor order and constructor permutation'),(495,523,'Slice and intersected-domain marginal')],
 'exec24_libdai_source_1':[(280,298,'Debug-only setter bounds'),(464,478,'Zero-norm refusal'),(516,532,'In-place normalization')],
 'exec24_libdai_source_2':[(44,113,'Numeric label identity and debug domain consistency')],
 'exec24_libdai_source_3':[(31,83,'Ascending labels,fast first axis and unspecified-state zero')],
 'exec24_libdai_source_4':[(145,178,'Missing-variable/factor lookup refusal'),(234,278,'Backup and restore API')],
 'exec24_libdai_source_5':[(222,228,'Cavity replaces every touching factor'),(356,365,'Clamp indicator and non-strict initial guard'),(399,441,'Backup,duplicate-backup refusal and restore')],
 'exec24_libdai_source_6':[(30,58,'Tolerance,updates,iterations,time and damping options'),(258,351,'Residual loop,limits,verbosity and no NaN guard'),(356,389,'Normalized variable and factor beliefs'),(445,460,'Damped update')],
 'exec24_libdai_source_7':[(25,57,'Documented message/belief definition'),(189,202,'Belief,residual and iteration API')],
 'exec24_libdai_source_8':[(20,42,'Junction-tree heuristic and memory options'),(74,113,'Elimination and heuristic memory estimate')],
 'exec24_libdai_source_9':[(25,40,'Exact clique inference description'),(107,134,'Construction,beliefs and fixed iteration API')],
 'exec24_libdai_source_10':[(68,114,'Full-joint product,normalization and MAP enumeration')],
 'exec24_libdai_source_11':[(54,68,'Always-on versus debug-only assertions')],
 'exec24_libdai_source_12':[(8,82,'Platform configuration,debug flags and selected algorithm builds')],
 'exec24_libdai_source_13':[(8,14,'Local template requirement'),(31,78,'Compiler,GMP,Boost and Python2.7 example')],
 'exec24_libdai_source_14':[(1,42,'Version0.3.0 and GPL/BSD transition'),(60,112,'Interfaces,tasks and inference-engine scope'),(158,174,'Build dependencies')],
 'exec24_libdai_source_15':[(1,21,'Two-clause BSD redistribution conditions')],
 'exec24_libdai_delegate_0':[(18,37,'Linear index and inverse implementation')],
 'exec24_libdai_delegate_1':[(148,210,'Domain permutation and index conversion')],
 'exec24_libdai_delegate_2':[(18,44,'Selected algorithms and debug default')]
}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'exec24_libdai_tree.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={v['path']:v for v in tree['tree']};commit=read(RAW/'v12_sw_cutoff_commit_libdai.json')[0]
    assert commit['sha']==PIN and commit['commit']['committer']['date']=='2012-05-16T13:50:19Z'
    records=[]
    for key,specs in SPECS.items():
        p=RAW/(key+'.txt');data=p.read_bytes();receipt=read(RAW/(key+'.receipt.json'));path=receipt['url'].split('/'+PIN+'/')[1]
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert hashlib.sha256(data).hexdigest()==receipt['sha256'] and lookup[path]['sha']==blob
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,f in specs:
            assert 1<=lo<=hi<=len(lines),(key,len(lines),hi)
            anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(source_identity=receipt['url'],repository_path=path,git_blob=blob,version_date='16May2012mirror;'+PIN,local_copy=ref(p,'Authenticated historical source'),acquisition=ref(RAW/(key+'.receipt.json'),'Original acquisition'),inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==19
    fail=read(RAW/'exec24_libdai_official.receipt.json');assert fail['status']=='failed' and 'allowlist' in fail['error']
    write(BASE/'official-access-limit.json',dict(status='local_host_policy_limit_not_server_failure',evidence=[ref(RAW/'exec24_libdai_official.receipt.json','Exact attempted route')],policy_changed=False))
    write(BASE/'identity-review.json',dict(status='pass_for_selected_historical_mirror',records=records,commit=PIN,date='2012-05-16',declared_version='0.3.0;12July2011',evidence=[ref(RAW/'exec24_libdai_tree.json','Complete mirror tree'),ref(RAW/'v12_sw_cutoff_commit_libdai.json','Cutoff identity'),ref(BASE/'official-access-limit.json','Local access boundary'),ref(BASE/'path-preflight-repair.json','Corrected concrete build path')],official_current_identity=False,native_execution=False))
    assert PAPER.read_bytes()==(RAW/'exec24_libdai_paper.pdf').read_bytes() and core.sha(PAPER)==read(RAW/'exec24_libdai_paper.receipt.json')['sha256']
    pages=(BASE/'paper.txt').read_text().split(chr(12));pages=[p for p in pages if p.strip()];assert len(pages)==5
    assert 'version 0.2.7' in pages[0] and 'GPL v2+' in pages[0] and 'Structure learning' in pages[2]
    findings=['Original identity,0.2.7andGPLscope','Factor law,inference queries,methods and limited bindings','Historical task comparison,build/support context','Acknowledgments and references;not separate technical evidence','References;not inherited as newly inspected works']
    anchors=[dict(anchor=f'Physical page{i+1};printed{2169+i}',text_extract=ref(BASE/'paper.txt','Primary text extraction'),excerpt_sha256=hashlib.sha256(p.encode()).hexdigest(),finding=findings[i]) for i,p in enumerate(pages)]
    write(BASE/'paper-review.json',dict(status='pass_for_original_identity_and_bounded_technical_claims',paper=ref(PAPER,'Genuine five-page publisher original'),identity=[ref(RAW/'exec24_libdai_paper.receipt.json','Acquisition'),ref(RAW/'exec24_libdai_publisher.html','Publisher identity')],anchors=anchors,limits=['Historical version and comparison;no reproduced performance','Cited references not promoted to inspected originals','No native evidence or independent acceptance']))
    fg=(RAW/'exec24_libdai_source_5.txt').read_text();bp=(RAW/'exec24_libdai_source_6.txt').read_text();pr=(RAW/'exec24_libdai_source_1.txt').read_text()
    assert 'DAI_ASSERT( x <= var(i).states() );' in fg and 'DAI_DEBASSERT( i < _p.size() );' in pr
    assert 'BP::run does not check for NANs' in bp and 'return maxDiff;' in bp
    write(BASE/'control-flow-review.json',dict(status='pass_for_bounded_static_findings',findings=['Clamp keeps neighboring mechanisms and adds an evidence indicator;not do replacement.','Cavity erases all touching factors.','Clamp equal-to-cardinality guard and debug-only setter require preflight refusal.','Residual is belief change;limits and no NaN loop guard require explicit worker validation.'],evidence=[ref(RAW/(k+'.txt'),'Primary implementation') for k in ['exec24_libdai_source_5','exec24_libdai_source_6','exec24_libdai_source_1','exec24_libdai_source_11']],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_and_numerical_witnesses',findings=['Factor order changes4/7to5/7.','Conditioning4/5versus intervention1/2;effect0.','Uniform BP fixed point:edge3/4versus exact5/6withZ72.','Binary64underflow versus exact1/5,4/5and log-scale recovery.','Thirty binary variables require8GiBdouble payload for full joint.','Error1/12at120000USDgives10000USD;12000USDover400/300/200gives30/40/60.'],evidence=[ref(Path(exact.__file__),'Independent mathematical code'),ref(BASE/'exact-results.json','Exact/numerical outputs'),ref(BASE/'development.tex','Explained argument')],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_grant_not_complete_binary_clearance',selected_source_license='Two-clause BSD',paper_version_license='0.2.7;GPLv2or later',selected_build_declarations=['GMP/GMPXX','Boost','Optional Matlab/SWIG/Octave interfaces','Linux example Python2.7headers;local config required','Debug default enabled;artifact flags must be bound'],evidence=[ref(RAW/(k+'.txt'),'Pinned declaration') for k in ['exec24_libdai_source_15','exec24_libdai_source_14','exec24_libdai_source_13','exec24_libdai_delegate_2']],unresolved=['Official provenance','Complete dependency and binding notices','Modern compiler/ABI and rights-cleared binary','Maintenance,support,security and costs'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',inputs=['Causal mechanism provenance and declared target','Unique labels,cardinalities,categories,axis ordering and exact query variables','Nonnegative finite factors,positive finite normalizer and explicit evidence','Algorithm,arithmetic,iteration/time/memory caps,seed and error budget','Exact source,binary,build flags,rights and worker'],outputs=['Typed beliefs and query identity','Algorithmic residual separate from approximation error and statistical uncertainty','Normalizer/scales,refusals,restoration state and complete request/cost counts'],refusals=['Missing identification','Conflicting domains or incomplete query','State outside0<=x<r','Zero/nonfinite mass or invalid factors','Unsupported approximation guarantee','Resource or recovery failure'],integration_allowed=False))
    next_action='Retain libDAI historical numerical reference;obtain official provenance and complete dependency rights,then preregister native factor-order/domain/query,conditioning/do/cavity,rollback,zero-mass/underflow,exact/junction-tree,loopy-fixed-point,truncation and resource fixtures. Bind exact artifact and full costs;do not repeat selected source or paper review.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,known_routes=['Official source and complete granted terms','Independent finite inference/query oracles','Rights-cleared isolated C++ worker and full request accounting'],remaining=['Official host outside collector scope','Other algorithms,bindings,learning and export delegates','Complete dependency/artifact and native qualification','Current support,price and maintenance evidence'],unknown_without_information=['Bank causal mechanisms and assignment truth','Universal loopy-inference error guarantee from residual','General latent identification or unrestricted dependent-data uncertainty']))
    choice=dict(candidate='libDAI',canonical_candidate='dbtsai/libDAI historical mirror',decision='reference',selected_revision=PIN,selected_version='README0.3.0;2012mirror',alias_boundary='Discrete numerical inference;not causal discovery/identification or whole-platform approval',reason='Concrete factor and inference reference;native,rights,official and error qualification remain explicit.',alternatives=[dict(route='adopt',decision='defer',reason='Whole causal platform and current binary unsupported'),dict(route='integrate',decision='conditional',reason='Isolated C++worker after identity,rights and native finite fixtures'),dict(route='port',decision='defer',reason='No measured benefit against new correctness/maintenance burden'),dict(route='reference',decision='retain',reason='Authenticated original/source and exact numerical/scientific witnesses'),dict(route='reject',decision='restricted',reason='Reject clamping as do,convergence as accuracy and silent conversion loss')],owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Mechanisms,identification,domains and target'),('Numerical','Exact oracles,approximation and resource error'),('Adapter','Axis identity,queries,refusal and restoration'),('Rights/platform','Official artifact,dependencies,build/support and costs')]],costs=dict(prices='Unmeasured;12000USD authored illustration',categories=['source/rights','build','conversion','all inference','failures','review','maintenance']),maintenance='Historical mirror;official current support unverified',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_libdai_source',kind='software_primary_sources',title='Historical libDAI factor,conditioning,inference and numerical contracts',author='libDAI authors and mirror contributors',year=2012,source_identity='https://github.com/dbtsai/libDAI/tree/'+PIN,version_date='16May2012mirror;README0.3.0;'+PIN,local_copy=ref(RAW/'exec24_libdai_source_0.txt','Primary factor representation'),records=records,identity_evidence=[ref(BASE/'identity-review.json','Full-byte/tree identity')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    paper=dict(integrated_citation_key='exec24_libdai_paper',kind='paper',title='libDAI: A Free and Open Source C++ Library for Discrete Approximate Inference in Graphical Models',filename_title=TITLE,first_author='Mooij',author='Mooij, Joris M.',year=2010,source_identity='https://www.jmlr.org/papers/volume11/mooij10a/mooij10a.pdf',version_date='JMLR11:2169-2173;August2010;five-page publisher original;version0.2.7',local_path=str(PAPER.relative_to(ROOT)),sha256=core.sha(PAPER),local_copy=ref(PAPER,'Genuine publisher original'),identity_evidence=[ref(RAW/'exec24_libdai_paper.receipt.json','Acquisition'),ref(RAW/'exec24_libdai_publisher.html','Publisher identity')],inspected_anchors=anchors,supported_claims=findings[:3],limitations=['Historical technical scope and version;not current comparison or reproduced benchmark','Other references require their own inspected originals'])
    authored=dict(integrated_citation_key='exec24_libdai_choice',kind='project_evidence_not_scholarly_paper',title='Authored libDAI factor-order,intervention,loopy-error,underflow and cost witnesses',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact/numerical review'),inspected_anchors=[ref(BASE/n,'Bounded choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','omissions-register.json']],supported_claims=['Exact factor and intervention witnesses','Zero-residual loopy error and numerical support failures','Bounded alternatives,owners,costs and public-fixture route'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,paper,authored],new_records=3,new_scholarly_pdfs=1,native_execution=False))
    write(BASE/'plan-review.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Plan and evidence') for n in ['plan.md','identity-review.json','paper-review.json','choice.json','mathematical-review.json']],findings=['Separate paper and mirror versions/rights.','Inspect exact delegates for conversion and numerical claims.','Independent mathematical witnesses do not become native benchmarks.','Official access and bank truth do not block independent proposal work.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Sponsor implications')],findings=['Factor notation,assumptions,numerical limits and monetary consequences explained.','Claim scope distinguishes source behavior,authored derivation and future native tests.','Genuine scholarly PDF retained;references not promoted without inspection.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','paper-review.json','source-audit.json','control-flow-review.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','exact-results.json','mathematical-review.json','plan-review.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],findings=['Nineteen selected originals authenticate;genuine JMLR paper identity and anchors verified.','Authored exact probabilities and numerical witnesses reproduce.','Reference decision admits no native or causal capability.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(authenticated=19,papers=1,decision='reference',records=3,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed historical libDAI numerical-reference proposal choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned mirror identity,alias,version-specific rights and maintenance limits explicit.','Target,conversion,alternatives,owners,costs and revisit conditions reviewed.','Reference only;no native,causal,current-release or full rights qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('libDAI reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
