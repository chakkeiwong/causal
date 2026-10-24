#!/usr/bin/env python3
"""Selected historical Weka source and reference disposition; no acquired code run."""
import argparse,hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
import weka_reuse_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as write_new,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/weka-reuse-v1';RAW=ROOT/'docs/literature/raw'
PIN='04804ccd6dff03534cbf3f2a71a35c73eef24fe8';OP='SW.DECISION.seed_078';read=lambda p:json.loads(p.read_text())
LIMITS=['Pinned2022discontinued mirror only;official2026cutoff identity unresolved.',
 'No Weka or downloaded code executed;examples and static deductions are authored.',
 'Predictive factorization,score and smoothing do not establish intervention identification.',
 'Complete rights,dependencies,native behavior,support and costs remain unqualified.',
 'Reference only;no native,causal,independent,visual,bank or final acceptance.']
SPECS={
 'exec24_weka_source_0':[(1,20,'GPL source header'),(75,145,'CPT construction and weighted updates'),(148,223,'Class conditioning,log scale and zero-vector fallback')],
 'exec24_weka_source_1':[(55,70,'Half-count prior default'),(145,202,'Prior option and setters')],
 'exec24_weka_source_2':[(57,111,'Per-category prior,weighted counts and probabilities')],
 'exec24_weka_source_3':[(40,140,'Version resource parsing and fallback identity')],
 'exec24_weka_source_4':[(1,27,'Snapshot and GPL declarations'),(86,127,'Java8/9plus profiles'),(383,471,'Fourteen declared dependency entries')],
 'exec24_weka_source_5':[(1,9,'Discontinued mirror and official successor')],
 'exec24_weka_source_6':[(100,140,'Fit state and buffering'),(145,210,'Weighted modes/means and all-missing defaults'),(228,280,'Class exclusion and replacement')],
 'exec24_weka_source_7':[(324,390,'Training filter fit boundary'),(801,840,'Cutpoint fitting and missingness'),(958,1025,'Class-weighted entropy selection')],
 'exec24_weka_source_8':[(1267,1309,'First maximum on tied counts'),(1374,1407,'Zero/NaN normalization refusal')],
 'exec24_weka_source_9':[(1,1,'3-8-7-snapshot resource')],
 'v12_exec13_java_weka_bayesnet':[(18,106,'Classifier target and weighted interface'),(150,278,'K2/simple defaults,label deletion and filters'),(355,383,'Prediction and update normalization')],
 'v12_exec13_java_weka_search':[(48,80,'One-parent and naive-Bayes defaults'),(289,333,'Name/index import and class-parent initialization')],
 'v12_exec13_java_weka_k2':[(115,125,'Fixed-order default'),(164,234,'Class-first ordering,unseeded optional randomization and parent bound')],
 'v12_exec13_java_weka_ci':[(75,108,'Score-comparison independence predicate')],
 'v12_exec13_java_weka_localscore':[(93,110,'Separate score prior and BAYES default'),(236,272,'Plain unweighted integer counts'),(285,395,'Score and penalty dispatch')],
 'v12_exec13_java_weka_bif':[(190,240,'Named graph and CPT import'),(635,651,'Node lookup')],
 'v12_exec13_java_weka_test':[(30,52,'Generic classifier-test inheritance;no causal oracle')],
 'v12_exec13_java_weka_license':[(1,17,'GPLv3 identity'),(155,172,'Basic permissions'),(201,255,'Conveying modified and nonsource forms')]
}

def write(path,value):
    if path.exists():
        assert read(path)==value, 'Preserve different existing evidence: '+str(path)
    else:write_new(path,value)

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'v12_exec13_java_weka_tree.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={x['path']:x for x in tree['tree']};cutoff=read(RAW/'v12_sw_cutoff_commit_weka.json')[0]
    assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']=='2022-08-10T01:25:51Z'
    records=[]
    for key,specs in SPECS.items():
        p=RAW/(key+'.txt');data=p.read_bytes();r=read(RAW/(key+'.receipt.json'));path=r['url'].split('/'+PIN+'/')[1]
        digest=hashlib.sha256(data).hexdigest();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert digest==r['sha256'] and lookup[path]['sha']==blob
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,f in specs:
            assert 1<=lo<=hi<=len(lines),(key,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],finding=f,excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
        records.append(dict(source_identity=r['url'],repository_path=path,git_blob=blob,version_date='10August2022;3.8.7-SNAPSHOT;'+PIN,
            local_copy=ref(p,'Authenticated historical original'),acquisition=ref(RAW/(key+'.receipt.json'),'Acquisition receipt'),
            inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    assert len(records)==18 and (RAW/'exec24_weka_source_9.txt').read_text().strip()=='3-8-7-snapshot'
    write(BASE/'identity-review.json',dict(status='pass_for_selected_historical_sources',records=records,commit=PIN,date='2022-08-10',version='3.8.7-SNAPSHOT',
        evidence=[ref(RAW/'v12_exec13_java_weka_tree.json','Complete mirror tree'),ref(RAW/'v12_sw_cutoff_commit_weka.json','Mirror cutoff'),
                  ref(BASE/'official-access-limit.json','Official source identity still unresolved'),ref(BASE/'path-preflight-repair.json','Resolved delegate path'),ref(BASE/'version-path-preflight-repair.json','Resolved resource path')],
        official_current_identity=False,native_execution=False))
    search=(RAW/'v12_exec13_java_weka_search.txt').read_text();score=(RAW/'v12_exec13_java_weka_localscore.txt').read_text()
    assert 'protected int m_nMaxNrOfParents = 1;' in search and 'protected boolean m_bInitAsNaiveBayes = true;' in search
    assert 'initialNet.getNode(bayesNet.getNodeName(iAttribute))' in search and 'initialNet.getNrOfParents(iAttribute)' in search and 'initialNet.getParent(iNode,' in search
    plain=score.split('private double calcNodeScorePlain(int nNode)',1)[1].split('} // CalcNodeScore',1)[0]
    assert 'instance.weight()' not in plain and 'nCounts[numValues * ((int) iCPT) + (int) instance.value(nNode)]++;' in plain
    simple=(RAW/'exec24_weka_source_0.txt').read_text();assert 'instance.value(iAttribute), instance.weight()' in simple and 'return new double[nNumClasses]' in simple
    write(BASE/'control-flow-review.json',dict(status='pass_for_bounded_static_findings',
        findings=['Default class parent fills selected one-parent K2 budget.','Plain local structure score counts rows;CPT estimator adds instance weights.',
            'Initial BIF uses dataset-index parent count with name-mapped parent retrieval.','Normalization refusal becomes all-zero missing prediction.'],
        evidence=[ref(RAW/(k+'.txt'),'Selected source') for k in ['v12_exec13_java_weka_search','v12_exec13_java_weka_localscore','exec24_weka_source_0','exec24_weka_source_8']]+[ref(Path(__file__),'Bounded source assertions')],native_execution=False))
    write(BASE/'exact-results-v2.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',
        findings=['Confounded observational contrast3/5 versus causal0;net50000versus-10000USD.',
            'Half-count prior gives1/4versus1/22for scaled counts;empty row1/2does not create support.',
            'Plain counts1,1versusweighted1,9giveillustrative1/2versus3/22first-category probabilities.',
            'Label selection changes population1/2toobserved4/5.','Permuted BIF node order uses incorrect parent count.',
            'Zero vector is not a probability distribution;7200USD denominators20,24,30.'],
        evidence=[ref(Path(exact.__file__),'Independent rational oracle'),ref(BASE/'exact-results-v2.json','Exact outputs'),ref(BASE/'development.tex','Connected argument')],native_execution=False))
    xml=ET.fromstring((RAW/'exec24_weka_source_4.txt').read_text());ns={'m':'http://maven.apache.org/POM/4.0.0'}
    dependencies=[{k:n.findtext('m:'+k,default='',namespaces=ns) for k in ['groupId','artifactId','version','scope','optional']} for n in xml.findall('m:dependencies/m:dependency',ns)]
    assert len(dependencies)==14
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_not_clearance',declared_dependencies=dependencies,
        evidence=[ref(RAW/'exec24_weka_source_4.txt','Pinned POM'),ref(RAW/'v12_exec13_java_weka_license.txt','GPL original'),ref(BASE/'official-access-limit.json','Successor access boundary')],
        license='GPLv3 root;selected headers v3or later',version='3.8.7-SNAPSHOT',unresolved=['Official successor cutoff identity','Built artifact and complete transitive notices',
            'Runtime/platform and XML import behavior','Support,maintenance and service costs'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Prediction versus intervention target,population and label clock','Typed nominal categories,ordered names and weight meaning',
            'Training-only preprocessing,missing masks,cutpoints and fit generation','Algorithm,prior,ordering,parent bound and graph import identity','Exact artifact,rights and worker'],
        outputs=['Class-labelled probability simplex or explicit refusal','Fitted preprocessing and separate selection/support diagnostics',
            'Graph class without automatic causal interpretation','Complete submitted/completed/qualified/failure counts and costs'],
        refusals=['Unknown official artifact','Causal target without identification','Missing-category or graph mapping loss','Unqualified weights/dependence',
            'Zero/NaN/invalid probabilities','Leaked evaluation labels','Unsupported observed-label extrapolation'],integration_allowed=False))
    next_action='Retain historical Weka reference and predictive comparator. Obtain permitted authentic official cutoff source;reconcile binary/rights,inspect remaining delegates and preregister classifier-versus-intervention,preprocessing-split,selection,weight,prior,empty-row,BIF-permutation and probability-refusal fixtures with all costs. Do not repeat the selected mirror inspection.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Approved official-source collection','Complete binary,dependency and rights inventory','Generated confounding/selection and conversion fixtures','Matched predictive evaluation'],
        remaining=['Official source identity outside collector allowlist','Other search/ADTree/estimator paths','Native error and graph import behavior','Independent implementation/coverage and service costs'],
        unavailable_scholarly_candidates=['No Weka/K2 original paper newly cited;software bibliographic metadata is not a substituted technical original.'],
        unknown_without_information=['Actual bank assignment and confounding','Unobserved label mechanism','Unique causal graph from predictive fit']))
    choice=dict(candidate='Weka Bayesian-network methods',canonical_candidate='Waikato/weka-3.8 historical mirror;official successor unresolved',decision='reference',
        selected_revision=PIN,selected_version='3.8.7-SNAPSHOT;historical2022',alias_boundary='Selected BayesNet classifier and search;not general causal identification or all Weka packages',
        reason='Concrete predictive reference exposes required conversion,target and failure contracts;current official and native qualification unestablished.',
        alternatives=[dict(route='adopt',decision='defer',reason='Current artifact and full surface unqualified'),
            dict(route='integrate',decision='conditional_predictive_comparator',reason='Typed isolated worker after identity,rights and native fixtures'),
            dict(route='port',decision='defer',reason='No measured benefit for new search,probability and maintenance burden'),
            dict(route='reference',decision='retain',reason='Authenticated historical classifier and exact scientific counterexamples'),
            dict(route='reject',decision='restricted',reason='Reject causal interpretation of classifier arrows and missing predictions as zero risk')],
        owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,label selection,support and information clock'),('Adapter','Types,preprocessing,imports,weights,output simplex and refusal'),
            ('Rights/platform','Official artifact,notices,runtime and maintenance'),('Evaluation','Matched public fixtures,all failures and costs')]],
        costs=dict(prices='Unmeasured;7200USD authored illustration',categories=['source and rights','environment','conversion','all fits','failures','review','maintenance']),
        maintenance='Discontinued mirror;current official support not verified',revisit_trigger=next_action,integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    source=dict(integrated_citation_key='exec24_weka_source',kind='software_primary_sources',title='Historical Weka Bayesian classifier,search,preprocessing and probability contracts',
        author='University of Waikato contributors',year=2022,source_identity='https://github.com/Waikato/weka-3.8/tree/'+PIN,version_date='10August2022;3.8.7-SNAPSHOT;'+PIN,
        local_copy=ref(RAW/'v12_exec13_java_weka_bayesnet.txt','Primary classifier'),records=records,identity_evidence=[ref(BASE/'identity-review.json','Full-byte/tree identity')],
        inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_weka_choice',kind='project_evidence_not_scholarly_paper',title='Authored Weka conditioning,selection,smoothing,weights,import and cost witnesses',
        author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native execution',
        local_copy=ref(BASE/'mathematical-review.json','Exact independent witnesses'),inspected_anchors=[ref(BASE/n,'Bounded choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','omissions-register.json']],
        supported_claims=['Exact conditioning/intervention and selection counterexamples','Priors,weights and index witnesses','Bounded alternatives,owners,all costs and unresolved questions'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,authored],new_records=2,new_scholarly_pdfs=0,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',evidence=[ref(BASE/n,'Plan and evidence') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],
        findings=['Preserve historical mirror boundary and official access limit.','Use classifier task as comparator distinct from causal identification.',
            'Explicit known routes for public fixtures,rights and environment;no invented missing scholarly original.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',evidence=[ref(BASE/'development.tex','Technical argument'),ref(BASE/'sponsor-addition.md','Sponsor addition')],
        findings=['Notation,banking target and exact monetary consequences explained.','Primitive and end-to-end behavior separated.','Static source findings do not assert native benchmark failure.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','source-audit.json','control-flow-review.json','dependency-license-review.json','conversion-contract.json',
            'omissions-register.json','choice.json','exact-results-v2.json','mathematical-review.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Review logic')],
        findings=['Eighteen selected originals authenticate to historical pinned tree.','Exact authored scientific and interface witnesses reproduce.',
            'Historical reference decision grants no native or causal capability.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=18,decision='reference',new_records=2,official_successor_identity=False,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed historical Weka proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value);evidence=[ref(BASE/n,'Reviewed choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results-v2.json']]
    findings=['Pinned identity,alias,rights,dependencies and maintenance limits explicit.','Target,conversion,alternatives,owners,costs and revisit conditions reviewed.',
        'Reference only;no native,causal or current-release qualification.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,
        capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Weka reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
