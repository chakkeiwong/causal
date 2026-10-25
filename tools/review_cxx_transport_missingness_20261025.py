#!/usr/bin/env python3
"""Authenticate pinned C++ originals and review authored laws, without native execution."""
import argparse,hashlib,json
from pathlib import Path
import cxx_transport_missingness_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/cxx-transport-missingness-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.transport_missingness.Cxx'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Four bounded discovery queries do not establish saturation or absence; broad transport query mostly retrieved unrelated software.', '32 authentic originals across three collections; selected libDAI is a historical mirror, not a current supported-edition claim.', 'Static source and exact authored examples do not establish native failure rates or runtime compatibility.', 'Compiler, OpenMP, Armadillo/Bandicoot, inference backend, model and artifact identities require qualification.', 'Complete dependencies, native behavior, distribution rights and public-prototype full costs remain open.', 'Package-mentioned scholarly works remain discovery leads without newly retained original PDFs.', 'No visual, independent, bank or final acceptance; mandatory repairs and Q1/Q5 remain open.']
NEXT='Complete C++ transport/missingness candidates and current official library routes; qualify sentinel and sparse semantics, completion/deletion targets, compiler branches, evidence versus intervention, EM stopping and missing-aware prediction with public fixtures and complete rights/costs.'
DECISIONS=['mlpack: conditional numerical preprocessing baseline; preserve mask, orientation, sentinel, row identity and compiler-specific qualification.', 'libDAI: conditional inference/EM comparison or adaptation after model semantics and exact backend qualification; reject equating evidence clamping with intervention.', 'XGBoost: conditional nuisance-prediction engine after missing/sparse schema, split, calibration and selection assumptions; reject transport identification from missing support alone.']
ANCHORS={'libdai': [('src01', 1, 21, 'Redistribution', 'Selected BSD-style license; full dependencies and current edition remain separate.'),
            ('src05',
             38,
             77,
             'skip if missing observation',
             'Tabular parser validates variable identity, field counts and integer states; empty fields omitted from evidence.'),
            ('src04',
             37,
             76,
             'pseudo_count = 1',
             'Conditional probability estimator adds configurable pseudocounts, normalizes blocks and resets statistics.'),
            ('src04',
             166,
             190,
             'perm.convertLinearIndex',
             'Expected sufficient statistics and factor replacement preserve explicit variable permutations.'),
            ('src04',
             216,
             260,
             'diff < 0',
             'Default30iterations/0.01relative tolerance; likelihood decrease prints an error and also terminates.'),
            ('src04',
             265,
             307,
             'clamped->clamp',
             'Each sample clones inference, conditions on observed variables, and accumulates expectations before maximization.'),
            ('src09', 221, 231, 'Kronecker delta', 'Clamp is conditioning by a delta factor; cavity operation has separate semantics.'),
            ('src10',
             356,
             364,
             'factor(I) * mask',
             'Clamping multiplies incident factors by a mask; it does not remove a treatment assignment mechanism.'),
            ('src06', 30, 50, 'JTREE', 'Example chooses junction-tree backend; generic EM receives an arbitrary inference algorithm.'),
            ('src11',
             89,
             115,
             'memneeded',
             'Junction-tree construction estimates memory and can enforce a cap; whole runtime costs remain unmeasured.')],
 'mlpack': [('src01', 1, 20, 'BSD', 'Selected three-clause BSD declaration; dependencies separate.'),
            ('src03', 38, 71, 'columnMajor', 'In-place completion with orientation-aware dimension bounds.'),
            ('src04', 33, 56, 'customValue', 'Sentinel replacement mutates selected coordinates.'),
            ('src05',
             35,
             59,
             'shed_cols',
             'Listwise strategy removes observations with selected missing entries; row identity must survive externally.'),
            ('src06',
             35,
             104,
             '#pragma omp parallel for',
             'Pre-Armadillo14.6 branch increments shared count and sum in parallel loops without an explicit reduction clause.'),
            ('src06',
             106,
             143,
             'no non-missing',
             'Older branch explicitly refuses empty observed set; newer branch delegates to Armadillo reductions.'),
            ('src06', 159, 196, 'IsSparse', 'Generic backend branch disallows sparse input and delegates selected means.'),
            ('src07', 43, 124, 'tmp.is_empty', 'Median path differs across Armadillo versions; older branch refuses empty observed set.'),
            ('src08',
             69,
             100,
             'std::move',
             'Binding extracts input, sentinel, strategy and dimension; unspecified dimension covers all features.'),
            ('src08', 116, 141, 'ListwiseDeletion', 'CLI dispatches four strategies over selected dimensions.'),
            ('src09',
             27,
             67,
             'mappedValue = 0.0',
             'Upstream test demonstrates sentinel zero and alternate matrix orientations; not a local execution result.')],
 'xgboost': [('src01', 1, 12, 'Apache License', 'Selected Apache2 license declaration; dependency rights separate.'),
             ('src02',
              59,
              78,
              'branch directions',
              'Primary documentation distinguishes learned missing branches, linear-booster zero treatment and sparse/dense representation.'),
             ('src04', 64, 106, 'missing_left_chg', 'Categorical one-hot split evaluates missing mass on either side.'),
             ('src04', 236, 265, 'd_step == -1', 'Numerical histogram scan associates candidate gains with default direction.'),
             ('src04',
              319,
              326,
              'SplitContainsMissingValues',
              'Reverse numerical scan is selected when feature statistics indicate missing values.'),
             ('src10',
              15,
              46,
              'tree.DefaultChild',
              'Prediction dispatches NaN to default child when missing-aware specialization is enabled; sentinel conversion is a loader '
              'precondition.'),
             ('src05', 60, 74, 'GetNextNode', 'CPU traversal calls selected next-node helper.'),
             ('src06', 131, 159, 'quiet_NaN', 'Sparse feature access starts absent coordinates as NaN and resolves observed bins separately.')]}
def prepare():
    assert not (BASE/'review.json').exists()
    pins=read(BASE/'pins.json');selected=read(BASE/'selected-paths.json')+read(BASE/'delegate-paths.json')
    assert len(selected)==32;rows=[];identities=[];originals=[]
    for group,pin in pins.items():
        cp=ROOT/pin['commit_original']['path'];tp=ROOT/pin['tree_original']['path']
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp);commit=commit[0] if isinstance(commit,list) else commit;assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha'] in {pin['sha'],pin['tree_sha']} and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for item in [x for x in selected if x['group']==group]:
            p=RAW/(item['id']+'.txt');rp=p.with_suffix('.receipt.json');r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p)
            expected='https://raw.githubusercontent.com/'+pin['repository']+'/'+pin['sha']+'/'+item['upstream_path']
            assert r['url']==expected
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==blobs[item['upstream_path']]
            rows.append(dict(group=group,upstream_path=item['upstream_path'],local_path=str(p.relative_to(ROOT)),receipt=str(rp.relative_to(ROOT)),sha256=core.sha(p),git_blob=blob,url=expected))
            originals.append(dict(group=group,upstream_path=item['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Public receipt'),git_blob=blob))
    write(BASE/'selected-originals.json',rows);write(BASE/'authenticated-originals.json',dict(count=32,groups=3,originals=originals,identities=identities,native_execution=False))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[pin['commit_original']];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_ctm_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_ctm_'+group,kind='software',title=group+' pinned C++ missingness and numerical-completion contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_ctm_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only; creation-date filter is not historical search reconstruction'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results'],lexical_mismatch=p.stem.endswith('_transport')))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==4
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Selected declarations')],findings=['mlpack three-clause BSD; selected libDAI BSD-style; XGBoost Apache2.','Transitive dependencies, compiler and installed-artifact rights remain unqualified; mirror identity is not current-edition assurance.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored exact laws'),ref(BASE/'exact-results.json','Reproducible arithmetic'),ref(BASE/'inspected-extracts.json','Primary implementation contracts')],findings=['Mean completion has square1 versus expected square2.','Outcome-dependent observation changes mean1/2to3/4.','Pseudocount smoothing changes2/2to3/4; zero counts and zero prior leave zero mass.','Conditioning in U->A,U->Y law gives1 versus intervention1/2.','Likelihood decrease terminates selected EM without establishing convergence.','Hypothetical stump routes observed zero to0.1 and missing to0.9; population discrepancy yieldsUSD80000.'],native_execution=False))
    tests=['Freeze target population, causal estimand, observation law and analysis unit.','Qualify NaN/sentinel/schema conversion, sparse zero and row identity before and after mutation.','Test empty observed sets, orientation, all-dimension deletion, compiler branches, thread counts and backend versions.','Test nonlinear moments and held-out completion separately from causal targets.','Distinguish observational evidence from causal graph surgery; enumerate known latent laws.','Verify factor permutations, pseudocount blocks, zero probability and EM termination reasons with exact inference fixtures.','Separate exact from approximate E-steps and record convergence/memory costs.','Test learned missing routes, omitted sparse coordinates and held-out calibration under observation shifts.','Resolve exact artifact/dependency rights before distribution.','Replay typed CLI/MCP contracts and total public-prototype costs; expensive bank trials remain later.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='C++ completion, latent conditioning, prediction and transport contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Prototype implementation owner to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Query mismatch and candidate tail'),ref(BASE/'dependency-license-review.json','Unresolved artifact rights')],known_routes=tests,uninspected=['Uninspected returned repositories including statistical and domain-specific imputation candidates.','Complete numerical/dependency implementations and native qualification.','Current official libDAI and package-referenced scholarly originals.'],unknown_universal_repairs=['Unrestricted MNAR is not recovered by numerical completion.','Hidden assignment and unsupported target strata need new information or defended restrictions.','Arbitrary dependence and learner uncertainty have no universal correction.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_ctm_choice',kind='project_evidence_not_scholarly_paper',title='Authored C++ completion, evidence-conditioning and transport qualification decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff7 October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Finite laws, source contracts and comparison decisions',inspection='Author inspection')],supported_claims=['32 authentic originals ground three bounded component comparisons.','Exact laws distinguish completion, evidence conditioning, prediction and target population.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=4,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Imputation is distinct from population transport and causal identification.','Authored witnesses do not imply measured native failures.','Independent public qualification can proceed before bank trials; historical mirror limits do not block independent work.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Population target through completion, latent conditioning, prediction, alternatives and implementation contracts.','Three source collections and authored witnesses cited with limits.','No scholarly citation admitted without original; no native or visual acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=32,scholarly_originals=0,limitations=LIMITS,native_execution=False));print(json.dumps(dict(review='pass',outcome='inconclusive',originals=32,anchors=len(fragments))))

def receipt():
    review=read(BASE/'review.json');verify_bindings(review);assert exact.calculate()==read(BASE/'exact-results.json')
    state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);output=ROOT/node['outputs'][0]
    write(output,read(BASE/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Three source collections inspected; ecosystem, current-edition and native coverage remain incomplete.','Pinned originals and exact authored laws support claims; scholarly metadata is discovery only.','Conditional adoption, port, defer and reject routes retain scientific and rights conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='C++ transport and missingness primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('C++ transport/missingness coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
