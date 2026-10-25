#!/usr/bin/env python3
"""Authenticate C++ source comparisons; execute only the authored exact reference."""
import argparse,hashlib,json
from pathlib import Path
import cxx_mediation_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/cxx-mediation-coverage-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.mediation_sensitivity.Cxx'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Four bounded queries and selected primary delegates do not establish saturation or absence.','No downloaded code executed;static and exact-law witnesses are not native failure rates.','R-facing C++ engines and generated Stan models are not independent standalone mediation products.','Complete downstream delegate propagation,installed artifacts,dependency rights and native qualification remain open.','No new scholarly work is cited without its original PDF;software metadata references are not admitted papers.','No visual,independent,bank or final acceptance;Q1/Q5 and mandatory depth/coverage remain open.']
NEXT='Complete remaining C++ candidates and downstream guards;qualify joint bootstrap identities,status denominators,dense/sparse failure,derivative parity,path-order invariance,cyclic density normalization,prior-scale/schema,posterior sign mapping and zero/missing translation with public exact-law fixtures,rights and full costs.'
DECISIONS=['OpenMx:conditional RAM/algebra reuse with causal restrictions,joint sampling,complete status counts,artifact identity and numerical failure propagation.','Stan Math:conditional direct adoption of maintained numerical primitives;not a mediation or sensitivity estimator.','bsem:defer direct admission;consider equation-level reuse after named-path,prior,cycle,missingness and posterior-sign qualification.','gwsem:reject direct genetic-loader port for bank records;separately consider checkpoint/workflow abstractions after rights and semantic review.','No blanket integration,port or capability approval;retain explicit owners and public qualification gates.']
ANCHORS={
 'openmx':[
 ('01',45,60,'Apache License','Apache2 declaration and native dependencies are initial rights inputs.'),
 ('06',1,16,'Licensed under','Authentic source-header license despite no LICENSE-named tree file.'),
 ('21',171,229,'FullPivLU','Polynomial/dense LU/sparse guarded inverse branches;no blanket package failure inferred.'),
 ('07',4224,4246,'origCumSum','Frequency-aware dataset contexts initialized separately.'),
 ('07',4280,4337,'statusCode','Raw seeds,fit,parameters,statuses and prior dimension checks.'),
 ('07',4330,4401,'implement parallel TODO','Per-context resampling,seed replay,fit status capture and normal-path restoration.'),
 ('30',371,410,'unsafe','Public entry rejects detected dependent data unless unsafe override;passes parallel flag.'),
 ('30',412,448,'mask <-','Fresh-model and dimension checks;acceptable-status filtering with denominator warning.'),
 ('31',458,495,'omxSetParameters','Algebra evaluated after substitution of complete retained parameter vector.'),
 ('34',824,842,'2*z0','Type1 quantiles and bias correction without acceleration.'),
 ('23',63,95,'independence assumption','Documented independent-row restriction and retained replication output.')],
 'stanmath':[
 ('01',1,14,'BSD 3-Clause','Pinned source BSD3 declaration;not full compiled dependency clearance.'),
 ('03',19,39,'lu()','General arithmetic solve checks dimensions and delegates LU.'),
 ('04',31,61,'check_pos_definite','SPD solve checks symmetry,non-NaN and LLT positivity.'),
 ('05',29,87,'householderQr','Reverse solve uses QR and input adjoint callbacks.'),
 ('07',11,47,'ldlt.isPositive','Inverse checks positivity despite broader opening description.')],
 'bsem':[
 ('20',22,45,'GPL-3','R/rstan generated compilation and dependency declarations.'),
 ('24',1,32,'stanc_builder','R modules bind generated Stan model family.'),
 ('30',18,25,'Stan version 2.21.0','Retained generated code is not the separately pinned2026StanMath tree.'),
 ('22',151,177,'X[idna]','Observed/missing indices and temporary row-mean working values.'),
 ('23',1,43,'par2_beta','Coefficient-prior parser values forwarded without square root.'),
 ('31',5,11,'return(c(dist, val))','Literal prior-string parser preserves supplied parameters.'),
 ('23',226,265,'e$signals','Signals choose initial values;not hard posterior constraints.'),
 ('23',270,340,'e$standata$idy','Targets in block order and parents in path-list order;no cycle validation in selected handler.'),
 ('25',19,73,'sqrt(s[i])','Nonnegative prior locations,unrestricted coefficients,Gaussian regression product and square-root scale.'),
 ('27',25,61,'Xna[i]','Missing entries are separate unknowns under measurement density;no missingness-indicator model.'),
 ('22',438,520,'permuted = FALSE','Chain-preserving extraction then posterior sign handler before summaries.'),
 ('23',425,467,'handler6','Post-extraction sign transformation needs separate semantic parity qualification.')],
 'gwsem':[
 ('20',38,65,'GPL','Genetic-domain OpenMx interface and GPL>=3 dependency declaration.'),
 ('22',25,46,'Unrecognized file extension','Explicit genetic-file suffix dispatch.'),
 ('22',137,202,'mxComputeTryCatch','Variant loading,reset,optimization,checkpoint covariance and sample-size plan.'),
 ('22',279,298,'statistically identified','Caller identification responsibility and per-variant reporting.'),
 ('26',9,55,'dosage == 0.0','Numeric zero dosage maps to missing;explicit MissingValue callback throws.'),
 ('26',94,128,'read_genotype_data_block','BGEN row/type checks and actual callback delegation.'),
 ('26',246,270,'NA_REAL','Separate PGEN lookup distinguishes0,1,2 and missing;no universal loader claim.')]
}
def prepare():
    assert not (BASE/'review.json').exists()
    rows=read(BASE/'selected-originals-final.json')+read(BASE/'selected-originals-parser.json');assert len(rows)==47
    pins={x['key']:x for x in read(BASE/'pins.json')};originals=[];identities=[]
    for g,pin in pins.items():
        cp=RAW/f'exec25_cmed_{g}_commit.json';tp=RAW/f'exec25_cmed_{g}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        assert read(cp)[0]['sha']==pin['commit'] and pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['commit'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for row in [x for x in rows if x['group']==g]:
            p=ROOT/row['local_path'];rp=ROOT/row['receipt'];r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p) and r['url']==row['url']
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob']==blobs[row['upstream_path']]
            originals.append(dict(group=g,upstream_path=row['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Bound receipt'),git_blob=row['git_blob']))
    write(BASE/'authenticated-originals-v2.json',dict(status='pass',count=47,originals=originals,evidence=identities,predecessor=ref(BASE/'authenticated-originals-final.json','Preserved initial46original audit')))
    sources=[];fragments=[]
    for g,checks in ANCHORS.items():
        pin=pins[g];evidence=[ref(RAW/f'exec25_cmed_{g}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_cmed_{g}_src{suffix}.txt';lines=p.read_text().splitlines();excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(g,suffix,lo,token)
            binding=ref(p,f'Lines{lo}-{min(hi,len(lines))}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding));claims.append(finding);fragments.append(dict(group=g,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_cmed_'+g,kind='software',title=g+' pinned C++ mediation computation and translation contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['commit'],version_date=pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));assert exact.calculate()==read(BASE/'exact-results.json')
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_cmed_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results']))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    for pin in pins.values():
        if pin['repository'] in leads:leads[pin['repository']]['status']='selected_primary_anchors'
    if 'cran/BayesGmed' in leads:leads['cran/BayesGmed']['status']='earlier_R_component_review_preserved'
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals-v2.json','Selected original declarations')],findings=['OpenMx Apache2 declared in DESCRIPTION and source header;no LICENSE-named path in selected complete tree.','StanMath BSD3;bsem GPL3;gwsem GPL>=3 and multiple third-party components.','Source identity does not establish installed dependency or optimizer rights.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored exact finite arithmetic'),ref(BASE/'exact-results.json','Replayed exact laws'),ref(BASE/'inspected-extracts.json','Selected delegate chains')],findings=['Linear direct3,indirect8,total11;paired product10 versus independent8.','Near-singular response1000 and derivative1000000.','Reversed path-list order produces self-edge M<-M and Y<-A;intended chain product3/8.','Simultaneous Gaussian residual product integrates4/3;Jacobian factor3/4 required.','Prior second parameter4 gives selected SD2;negative prior location conflicts with selected data constraint.','Numeric callback zero/missing witness changes retained dosage mean1to3/2;not native behavior.','Hypothetical value difference USD200000 reproduces.'],native_execution=False))
    tests=['Freeze named graph,target,units,contrast,disturbance law and data-clock identities.','Compare joint parameter draws against independent recombination and complete status denominators.','Test same-record versus linked-table sampling;independent,cluster and time-series laws remain separate.','Verify bootstrap cache identity,seed replay,interrupt restoration,zero accepted fits and ties.','Compare dense/sparse singular and near-singular outputs,conditioning and propagated refusal.','Qualify arithmetic/autodiff solve parity with independent derivatives and residual bounds.','Permute named path inputs;reject duplicate,self and unsupported cyclic graphs.','For admitted cyclic models include and test determinant normalization.','Verify prior location/scale schema,missingness and posterior sign mapping with known equations.','Distinguish legitimate zero from missing at parser,callback and output layers.','Round-trip identical CLI/MCP requests and bounded artifact references.','Review compiler/dependency rights and report all attempts,failures,resource and economic costs before bank trials.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='C++ mediation computation,translation and sensitivity qualification',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Proposal implementation owner to be appointed for native trials',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Explicit query tail'),ref(BASE/'dependency-license-review.json','Unresolved complete rights')],known_routes=tests,uninspected=['Five other SEM search leads and dedicated C++ methods beyond bounded discovery.','Complete external library/parser propagation,installed artifact versions and native failure denominators.','Scholarly references mentioned in package metadata remain unadmitted without genuine original PDFs.'],unknown_universal_repairs=['Numerical solves do not identify unrestricted hidden causal assignment or mediation truth.','Arbitrary dependent-data mediation uncertainty needs justified assumptions and theory.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed source comparison') for n in ['authenticated-originals-v2.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_cmed_choice',kind='project_evidence_not_scholarly_paper',title='Authored C++ mediation translation and numerical qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence,inspected_anchors=[dict(anchor='Source choices and exact public qualification',inspection='Author inspection')],supported_claims=['47authentic originals,four component roles and exact authored arithmetic.','Conditional adoption,port,defer and reject decisions with scientific and artifact limits.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=5,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Four component roles compared;none admitted as complete mediation product.','Declared public fixtures precede expensive bank trials.','Keep successful source work separate from incomplete coverage and native qualification.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Bank decision through structural equations,derivatives,joint uncertainty,translation,alternatives and economic consequence.','Conditional source findings do not assert native failures or universal causal identification.','Prior parser and posterior sign handler inspected;sign semantic parity remains a named qualification.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    review=dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=47,scholarly_originals=0,limitations=LIMITS,native_execution=False);verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass_for_selected_work',originals=47,anchors=len(fragments),new_records=5,outcome='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP;verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);value=read(BASE/'comparison-review.json');value['evidence']=[ref(BASE/'review.json','Selected review')];output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Four component roles inspected;bounded search and native coverage remain incomplete.','Pinned authentic originals and exact authored witnesses support claims;no scholarly metadata admitted as technical paper evidence.','Conditional adoption,port,defer and reject routes retain scientific,rights,artifact and acceptance conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='C++ mediation computation and translation source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('C++ coverage receipt prepared.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
