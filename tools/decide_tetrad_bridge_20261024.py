#!/usr/bin/env python3
"""Authenticate selected bridge originals and record a reference-only proposal choice."""
import argparse,ast,hashlib,json
from pathlib import Path
import tetrad_bridge_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/tetrad-bridge-reuse-v1'
RAW=ROOT/'docs/literature/raw';PIN='3a1217630a6d368e878e064e39fe24774bfe00bf'
OP='SW.DECISION.seed_077';read=lambda p:json.loads(p.read_text())
INHERITED=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_tetrad/decision.json'
PAPER=ROOT/'docs/papers/Py-Tetrad and RPy-Tetrad A New Python Interface with R Support for Tetrad Causal Search Ramsey(2023).pdf'
LIMITS=['Selected source identity does not establish bundled binary or installed distribution equality.',
 'No acquired Python,R,Java or JAR code executed; exact and base-R witnesses are authored.',
 'Static observations are conditional code findings,not measured native failure rates.',
 'Dependency rights,worker qualification,graph truth,calibration and actual costs remain open.',
 'Reference only;no native,independent,visual,bank or final acceptance.']
SPECS={
 0:('README.md',[(7,21,'Bridge architecture and adjusted bundled JAR'),(23,59,'JDK and Python requirements and historical paper identity')]),
 1:('LICENSE',[(1,21,'Root MIT grant,notice and disclaimer')]),
 2:('setup.py',[(1,31,'Version0.1.2,declared dependencies,resources and Python>=3.7')]),
 3:('pytetrad/tools/TetradSearch.py',[(1,38,'NetworkX and G-regression imports'),(121,157,'Mutable state and missing-policy parameters'),
     (181,186,'Discretize value not passed into setter'),(744,796,'PC/FCI result assignment after search'),
     (1090,1178,'Bootstrapping,data replacement and pooled datasets'),(1188,1247,'Result getters,explicit argument returns and bootstrap index')]),
 4:('pytetrad/tools/translate.py',[(1,17,'Import-time JVM and swallowed OSError'),(37,82,'Dtypes,first-order categories,stringification and missingness'),
     (85,115,'Continuous and discrete output conversion'),(117,182,'Endpoint matrix and binary adjacency mismatch'),
     (217,295,'Named endpoint conversion to causal-learn'),(297,375,'Inverse conversion and unknown endpoint refusal')]),
 5:('pytetrad/tools/__init__.py',[]),
 6:('pytetrad/tools/missing.py',[(1,58,'JVM lifecycle,class check,imputation and edge-frequency delegation')]),
 7:('pytetrad/R/TetradSearch.R',[(1,29,'Distinct direct-rJava temporary surface and referenced terms'),(112,130,'Knowledge-tier error handling'),
     (515,570,'Numeric-before-integer and factor/helper boundary')]),
 8:('pytetrad/R/tetrad_utils.R',[(1,40,'Moving JDK and version7.6.5 download declarations'),(57,110,'Unexecuted installer and error handling'),
     (129,150,'JAR download surface'),(180,220,'Direct-rJava startup path')]),
 9:('pytetrad/tools/gregression.py',[(1,59,'Delegated effects and distinct JVM flags;comments not independently verified'),
     (120,145,'Graph and data/covariance construction'),(156,212,'Fixed supplied graph,effect and bootstrap delegation')]),
 10:('pytetrad/R/README.md',[(1,12,'Reticulate and separate rJava alternatives')])}

def prepare():
    assert not (BASE/'review.json').exists()
    tree=read(RAW/'exec24_pytetrad_tree.json');assert tree['sha']==PIN and not tree['truncated']
    lookup={x['path']:x for x in tree['tree']};cutoff=read(RAW/'exec24_pytetrad_cutoff.json')[0]
    assert cutoff['sha']==PIN and cutoff['commit']['committer']['date']=='2026-10-07T11:51:35Z'
    records=[]
    for i,(path,specs) in SPECS.items():
        key=f'exec24_pytetrad_source_{i}';p=RAW/(key+'.txt');data=p.read_bytes();receipt=read(RAW/(key+'.receipt.json'))
        digest=hashlib.sha256(data).hexdigest();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
        assert receipt['sha256']==digest and lookup[path]['sha']==blob and '/'+PIN+'/' in receipt['url']
        lines=data.decode().splitlines();anchors=[]
        for lo,hi,finding in specs:
            assert 1<=lo<=hi<=len(lines),(path,lo,hi,len(lines))
            anchors.append(dict(lines=[lo,hi],finding=finding,excerpt_sha256=hashlib.sha256('\n'.join(lines[lo-1:hi]).encode()).hexdigest()))
        if not specs:
            assert data==b'';anchors=[dict(anchor='Complete empty original',finding='No initializer content',excerpt_sha256=digest)]
        records.append(dict(source_identity=receipt['url'],repository_path=path,git_blob=blob,version_date='7October2026;'+PIN,
            local_copy=ref(p,'Authenticated pinned original'),acquisition=ref(RAW/(key+'.receipt.json'),'Acquisition receipt'),
            inspected_anchors=anchors,supported_claims=[a['finding'] for a in anchors],executed=False))
    jar=lookup['pytetrad/resources/tetrad-current.jar'];assert jar['size']==56587560
    assert not any(x['path'].lower().endswith('license.txt') for x in tree['tree'])
    write(BASE/'identity-review.json',dict(status='pass_for_selected_sources',records=records,commit=PIN,
        date=cutoff['commit']['committer']['date'],declared_version='0.1.2',
        evidence=[ref(RAW/'exec24_pytetrad_tree.json','Complete cutoff tree'),ref(RAW/'exec24_pytetrad_cutoff.json','Commit identity'),ref(INHERITED,'Distinct inherited Java choice')],
        jar_metadata_only=jar,jar_acquired=False,jar_executed=False,installed_equivalence=False))
    t=ast.parse((RAW/'exec24_pytetrad_source_3.txt').read_text());c=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='TetradSearch')
    methods={n.name:n for n in c.body if isinstance(n,ast.FunctionDef)}
    missing_returns=[]
    for name in ['get_string','get_causal_learn','get_graph_to_matrix']:
        node=methods[name];branch=next(n for n in node.body if isinstance(n,ast.If))
        assert branch.orelse and not any(isinstance(n,ast.Return) for root in branch.orelse for n in ast.walk(root))
        missing_returns.append(name)
    m=methods['use_mixed_variable_polynomial'];calls=[n for n in ast.walk(m) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.params.set']
    bad=next(n for n in calls if n.args and ast.unparse(n.args[0])=='Params.DISCRETIZE');assert len(bad.args)==1
    writes=lambda n:[ast.unparse(a) for a in ast.walk(n) if isinstance(a,ast.Assign)]
    assert writes(methods['set_data'])==['self.data = tr.pandas_data_to_tetrad(data)']
    for method in ['run_pc','run_fci']:
        assigns=writes(methods[method]);assert sum(x.startswith('self.java = ') for x in assigns)==1
        assert any(x.startswith('self.java = alg.search(') for x in assigns)
    translate=ast.parse((RAW/'exec24_pytetrad_source_4.txt').read_text())
    converter=next(n for n in translate.body if isinstance(n,ast.FunctionDef) and n.name=='adj_matrix_to_graph')
    arc=next(n for n in ast.walk(converter) if isinstance(n,ast.Call) and ast.unparse(n.func)=='graph.addDirectedEdge')
    assert [ast.unparse(a) for a in arc.args]==['variables.get(i)','variables.get(j)']
    r=read(BASE/'r-type-witness.json');assert r['exit_code']==0 and 'integer_is_numeric=TRUE' in r['stdout'] and 'selected_branch=continuous' in r['stdout']
    write(BASE/'control-flow-review.json',dict(status='pass_for_selected_static_findings',explicit_graph_missing_returns=missing_returns,
        discretize_setter_arguments=1,set_data_invalidates_graph=False,adjacency_loop='i to j',
        evidence=[ref(RAW/'exec24_pytetrad_source_3.txt','Selected AST'),ref(RAW/'exec24_pytetrad_source_4.txt','Selected converter'),
                  ref(BASE/'r-type-witness.json','Authored base-R observation'),ref(BASE/'r-type-witness.R','No bridge code imported'),ref(Path(__file__),'AST-only verification')],native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_exact_witnesses',
        findings=['Binary convention reverses the requested edge;endpoint truthiness requests two directions.',
            'First-occurrence codes differ and stringified labels collide.',
            'Opposite Gaussian SEMs have identical covariance but effects1/2versus0 and net6000versus-4000USD.',
            'Failed right-hand assignment preserves earlier state;no native failure induced.',
            '6000USD over300,240,200requests gives20,25,30.'],
        evidence=[ref(Path(exact.__file__),'Independent rational oracle'),ref(BASE/'exact-results.json','Exact outputs'),ref(BASE/'development.tex','Connected derivation')],native_execution=False))
    write(BASE/'dependency-license-review.json',dict(status='selected_declarations_not_clearance',
        evidence=[ref(RAW/f'exec24_pytetrad_source_{i}.txt','Original declarations') for i in [0,1,2,3,7,8,9,10]]+[ref(INHERITED,'Separate Java decision')],
        root='MIT',R_header='MIT(SEI)-style references separate absent license.txt;terms unresolved',
        python_setup='>=3.7',python_readme='>=3.12',jdk_readme='>=21',setup_dependencies=['numpy','pandas','JPype1'],
        other_imports=['networkx','gregression','optional causal-learn'],
        unresolved=['Bundled JAR/source equality and full dependency notices','Separate R terms','Actual classpath and JVM flags',
                    'Pandas/missing-sentinel behavior','Java imputation,G-regression and pooling delegates','Native support,resources and costs'],integration_allowed=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_reference_only',
        inputs=['Scientific types,units,clock,sampling law and graph target','Bijections for variables and categories,missing masks and row IDs',
                'Distinct binary and endpoint graph schemas','Explicit test,score,knowledge,pooling,seed and resampling settings','JAR/JVM/dependency hashes and request generation'],
        outputs=['Typed graph and both endpoint marks','Effective inputs,settings and knowledge','Bound request identity and fresh result generation',
                 'Completed,qualified,refused,failed,cancelled and stale states','Complete task/failure/cost denominators'],
        refusals=['Unattested binary or rights','Colliding names or categories','Unmapped missingness','Endpoint loss or ambiguous adjacency direction',
                  'Stale result after changed data or failure','Unsupported graph-to-effect conversion','Unqualified dependence or uncertainty'],integration_allowed=False))
    next_action='Retain separate bridge reference decision and inherited Java choice. Reconcile exact bundled JAR/source/rights and Python/R routes; inspect imputation,G-regression,pooling and factor helpers; preregister typed category/missingness/endpoint round trips,explicit getters,failed second runs,knowledge and full-cost public fixtures. Do not repeat this bounded source review.'
    write(BASE/'omissions-register.json',dict(next_action=next_action,global_blocker=False,
        known_routes=['Binary/source and complete rights reconciliation','Locked isolated worker','Known-law public and negative fixtures','Selected delegate originals'],
        remaining=['Native behavior and cross-library conversion','Imputation and G-regression scholarly/delegate qualification','R terms and DataSetHelper coding',
                   'Separate r-tetrad repository','Actual support,prices and full costs','Mandatory coverage and final acceptance'],
        unknown_without_information=['Bank assignment and graph truth','Unique causal direction from observationally equivalent models','Universal hidden-state or dependent-data uncertainty']))
    choice=dict(candidate='Tetrad / py-tetrad bridge',canonical_candidate='cmu-phil/py-tetrad',decision='reference',
        alias_boundary='Python bridge plus selected R surfaces;not a new Java algorithm or inherited Java qualification',
        selected_revision=PIN,selected_version='0.1.2 declaration;bundled Java version unverified',
        reason='Useful primary interface design with explicit conversion and failure conditions;native scientific and artifact qualification remains open.',
        alternatives=[dict(route='adopt',decision='defer',reason='Unrestricted surface and bundled artifact unqualified'),
            dict(route='integrate',decision='conditional',reason='Isolated worker after scientific,rights,identity and native fixtures'),
            dict(route='port',decision='defer_algorithm;conditional_converters',reason='No measured engine-port benefit;converter rights and oracles required'),
            dict(route='reference',decision='retain',reason='Authenticated originals,historical paper and exact independent witnesses'),
            dict(route='reject',decision='restricted',reason='Reject lossy graph/type conversion,stale results and invented identification')],
        owners=[dict(role=r,responsibility=v) for r,v in [('Scientific','Target,measurement,graph assumptions and uncertainty'),
            ('Adapter','Bijections,missingness,request generations,parameters and refusal'),('Rights/platform','Exact binaries,notices,JVM and support'),
            ('Evaluation','Public known-law,negative cases and all-cost denominators')]],
        costs=dict(prices='Unmeasured;6000USD authored illustration',categories=['environment','adapter','rights','all searches','failures','review','maintenance']),
        maintenance='Community source;future service and upgrade costs unverified',revisit_trigger=next_action,
        inherited_decision=ref(INHERITED,'Preserved distinct Java decision'),integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    pbytes=PAPER.read_bytes();receipt=read(RAW/'exec24_pytetrad_paper.receipt.json');assert receipt['sha256']==hashlib.sha256(pbytes).hexdigest()
    assert pbytes==(RAW/'exec24_pytetrad_paper.pdf').read_bytes()
    pages=(BASE/'paper.txt').read_text().split(chr(12));assert len([p for p in pages if p.strip()])==12
    assert 'Ramsey' in pages[0] and 'Andrews' in pages[0] and 'reps = 10' in pages[4] and '100-fold' in pages[6]
    inspected=[(1,'Original identity and interface purpose'),(2,'JPype and Reticulate architecture and historical alternatives'),
        (3,'Data typing and endpoint conversion interfaces'),(4,'Knowledge tiers and bootstrap example'),(5,'Displayed ten-repetition Python example'),
        (6,'R/Reticulate path and required explicit variable types'),(7,'Table100fold description,knowledge and conditional type restrictions')]
    paper=dict(integrated_citation_key='exec24_pytetrad_paper',kind='paper',
        title='Py-Tetrad and RPy-Tetrad: A New Python Interface with R Support for Tetrad Causal Search',
        filename_title=PAPER.name.rsplit(' Ramsey(2023).pdf',1)[0],first_author='Ramsey',author='Ramsey, Joseph and Andrews, Bryan',year=2023,
        source_identity=receipt['url'],version_date='PMLR223:40-51;20November2023;12page publisher original',
        local_path=str(PAPER.relative_to(ROOT)),sha256=receipt['sha256'],local_copy=ref(PAPER,'Genuine publisher PDF'),
        identity_evidence=[ref(RAW/'exec24_pytetrad_paper.receipt.json','Acquisition'),ref(RAW/'exec24_pytetrad_paper_identity.html','Publisher metadata')],
        inspected_anchors=[dict(anchor=f'Physical page{n};printed{39+n}',text_extract=ref(BASE/'paper.txt','Original text'),
            excerpt_sha256=hashlib.sha256(pages[n-1].encode()).hexdigest(),finding=f) for n,f in inspected],
        supported_claims=[f for _,f in inspected],limitations=['Historical architecture and selected examples;no2026binary equivalence or reproduced paper experiment.',
            'Tenrepetitions in displayed code versus100fold table description not resolved;no denominator or causal-truth claim.'])
    source=dict(integrated_citation_key='exec24_pytetrad_source',kind='software_primary_sources',
        title='Pinned Py-Tetrad and selected R bridge type,graph,state and artifact contracts',author='Tetrad contributors',year=2026,
        source_identity='https://github.com/cmu-phil/py-tetrad/tree/'+PIN,version_date='7October2026;'+PIN,
        local_copy=ref(RAW/'exec24_pytetrad_source_4.txt','Primary converter'),records=records,
        identity_evidence=[ref(BASE/'identity-review.json','Tree and full-byte authentication')],
        inspected_anchors=[r['local_copy'] for r in records],supported_claims=[f for r in records for f in r['supported_claims']],limitations=LIMITS)
    authored=dict(integrated_citation_key='exec24_pytetrad_choice',kind='project_evidence_not_scholarly_paper',
        title='Authored Tetrad bridge graph,type,state,economics and reuse witnesses',author='Causal banking proposal project',year=2026,
        source_identity=str(BASE.relative_to(ROOT)),version_date='24October2026;cutoff7October2026;no native Tetrad execution',
        local_copy=ref(BASE/'mathematical-review.json','Independent exact witnesses'),
        inspected_anchors=[ref(BASE/n,'Bounded reviewed choice') for n in ['choice.json','conversion-contract.json','control-flow-review.json','r-type-witness.json','omissions-register.json']],
        supported_claims=['Independent graph and Gaussian nonidentification examples','Base-R integer predicate witness','Bounded alternatives,owners,costs and revisit conditions'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[paper,source,authored],new_records=3,new_scholarly_pdfs=1,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_choice',
        evidence=[ref(BASE/n,'Reviewed plan') for n in ['plan.md','identity-review.json','choice.json','mathematical-review.json']],
        findings=['Inherited Java decision preserved;bridge reviewed separately.','Historical paper distinct from pinned2026source and unacquired binary.',
            'Typed conversions,failures,knowledge and uncertainty have explicit public fixtures.','Unsupported delegates and rights remain local followups.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_bounded_argument',
        evidence=[ref(BASE/'development.tex','Technical manuscript'),ref(BASE/'sponsor-addition.md','Sponsor addition')],
        findings=['Banking rationale,notation,scientific ambiguity and exact economic consequences explained.',
            'Selected static observations distinguished from native failures.','Historical and direct-R routes,rights,owners,costs and remaining limits explicit.'],visual_acceptance=False))
    review=dict(status='pass_for_reference_only_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=[ref(BASE/n,'Reviewed evidence') for n in ['identity-review.json','source-audit.json','control-flow-review.json','dependency-license-review.json',
            'conversion-contract.json','omissions-register.json','choice.json','exact-results.json','mathematical-review.json','plan-review-v2.json',
            'copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Verification logic')],
        findings=['Eleven selected originals authenticate to cutoff tree.','Genuine12page publisher paper locally saved and inspected.',
            'Authored exact and base-R witnesses verified;no acquired software run.','Reference choice admits no native or causal capability.'],limitations=LIMITS,integration_allowed=False)
    verify_bindings(review);write(BASE/'review.json',review)
    print(json.dumps(dict(authenticated=11,scholarly_pdfs=1,decision='reference',new_records=3,native_execution=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed bridge proposal reference choice;no native admission',evidence=[ref(BASE/'review.json','Author review')])
    output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed decision') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Identity,alias,version,license,dependencies and maintenance limits explicit.',
        'Conversion and failure semantics,alternatives,owners,costs and revisit conditions reviewed.',
        'Reference only;integration false and no native or scientific capability admission.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        outputs=[ref(output,'Reference disposition')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],
        limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result)
    print('Tetrad bridge reference receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
