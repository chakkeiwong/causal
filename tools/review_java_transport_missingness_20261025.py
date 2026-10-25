#!/usr/bin/env python3
"""Authenticate pinned Java originals and review authored laws, without native execution."""
import argparse,hashlib,json
from pathlib import Path
import java_transport_missingness_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref,write as fresh_write,verify_bindings
run=controller.base;core=run.core;ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-25/java-transport-missingness-v1'
RAW=ROOT/'docs/literature/raw';OP='SW.CELL.transport_missingness.Java'
read=lambda p:json.loads(p.read_text())
def write(p,value):
    if p.exists():assert read(p)==value,'Existing evidence differs: '+str(p)
    else:fresh_write(p,value)
LIMITS=['Six bounded discovery queries do not establish ecosystem saturation or absence; the broad selection query mostly returned unrelated transport software.',
 '36 authentic originals across three source collections; archived Weka mirror is not the current supported edition.',
 'Exact authored laws and source findings do not establish native package failure frequencies or calibrated uncertainty.',
 'Current Weka repository is outside the fixed collector allowlist; authentic current-edition acquisition remains open without relaxing policy.',
 'Complete delegates, graph legality, learner uncertainty, runtime and artifact/dependency rights remain unqualified.',
 'Package-mentioned scholarly works are discovery leads until original PDFs and technical anchors are retained.',
 'No visual, independent, bank or final acceptance; mandatory repairs and Q1/Q5 remain open.']
NEXT='Complete Java candidate and current Weka primary-source routes; qualify EM convergence and information counts, conditional versus parameter draws, graph consensus legality, donor support, row identity, weights, low-rank refusal and rights with public fixtures before native admission.'
DECISIONS=['Tetrad: conditionally reuse missingness audits and typed policies; adapt imputation and graph aggregation only after convergence, uncertainty and legality qualification.',
 'Smile: consider numerical completion baselines with retained missingness masks; reject treating deterministic completion as multiple imputation or transport identification; resolve exact component licensing.',
 'Weka: preserve archived filters as historical comparators; seek current official edition and qualify weights, class/row semantics and uncertainty before adoption.']
ANCHORS={
 'tetrad':[
 ('src01',65,105,'createGraphWithHighProbabilityEdges','Selected imputation search chooses an imputer, searches completed datasets and calls per-pair graph aggregation.'),
 ('src10',76,106,'estimator.estimate','EM fitted once before completed datasets; selected wrapper does not inspect convergence flag.'),
 ('src10',118,153,'condCov','Conditional Gaussian means and covariance; entirely missing rows use marginal draws.'),
 ('src10',169,201,'Math.max(cov[a][a]','Cholesky exception falls back to independent diagonal draws; no jitter is added in the selected catch block.'),
 ('src19',167,177,'converged','EM exposes convergence status to callers.'),
 ('src19',389,413,'patterns.isEmpty','All-missing rows excluded from fitting and all-empty data refused.'),
 ('src19',448,462,'cholSolveMatrix','EM conditional-block calculation includes conditional covariance.'),
 ('src19',539,580,'ridge * meanDiagonal','M-step covariance and optional diagonal ridge.'),
 ('src02',324,341,'has no observed values','Missingness mask retained; entirely unobserved columns refused.'),
 ('src02',384,419,'rand.nextInt','Seeded donor initialization, chained sweeps, copies and logged events.'),
 ('src02',449,453,'hotDeck','Insufficient observed rows trigger marginal hot-deck fallback.'),
 ('src02',545,568,'regression could not be solved','Numerical fallback and ridge-dependence events are logged.'),
 ('src02',626,683,'best[rand.nextInt(k)]','Randomized tied candidate order and donor choice preserve observed-value support.'),
 ('src11',57,105,'double total = within + inflated','Scalar pooling combines within and finite-imputation between variance with degrees-of-freedom adjustment.'),
 ('src12',143,175,'candidateRows.size()','Cache treats full-length candidate list as all rows; input uniqueness/identity needs an adapter contract.'),
 ('src12',189,222,'guaranteed positive definite','Pairwise covariance is a screening object, not guaranteed positive definite.'),
 ('src20',113,155,'createEdge','Per-pair frequency aggregation constructs a composite graph.'),
 ('src20',158,180,'selectMedianEnsembleGraph','Alternative member-graph selection preserves underlying member legality conditions.'),
 ('src20',180,253,'Graph winner = members.get(bestIndex)','Member-selection implementation scores members and copies the winning member endpoints.'),
 ('src20',336,386,'graphs.size()','Highest-frequency state and empirical counts are aggregation semantics, not posterior calibration.'),
 ('src14',1,5,'Version 3','Selected GPLv3 license text; whole-artifact rights require separate review.')],
 'smile':[
 ('src02',78,117,'vector.length == 0 ? null','Neighbor imputation takes available-value mode/mean and can retain null.'),
 ('src03',50,110,'qr.solve','SVD completion initializes from means and solves per-row rank-k regressions; rank/conditioning needs qualification.'),
 ('src04',304,355,'The whole row','Matrix means reject wholly missing rows/columns; observed entries are preserved.'),
 ('src06',1,33,'GPLv3 / Commercial','Selected core declaration is dual GPLv3/commercial; commercial route is not a price or rights clearance.'),
 ('src06',35,50,'AGPLv3','Serve has a distinct declared license; do not transfer its terms to core.')],
 'weka':[
 ('src01',1,14,'version 3','Selected source declares GPLv3-or-later.'),
 ('src01',416,475,'isFirstBatchDone','Numeric and sample-size checks; fit first batch, reuse model, retain pattern-sorted alignment.'),
 ('src01',1013,1068,'theta_kj * y_ik','Selected output uses conditional means without conditional random draws.'),
 ('src02',152,205,'inst.weight()','Weighted numeric mean and nominal counts; zero observed-weight denominator leaves initialized numeric zero.'),
 ('src05',1,9,'no longer being updated','Archived mirror directs readers to official current repository.'),
 ('src06',1,5,'Version 3','Archived distribution includes GPLv3 text.'),
 ('src07',1,36,'3rd-party','Third-party license ledger demonstrates component-specific rights.')]}

def prepare():
    assert not (BASE/'review.json').exists()
    pins=read(BASE/'pins.json');selected=read(BASE/'selected-paths.json')+read(BASE/'delegate-paths.json')
    assert len(selected)==36;rows=[];identities=[];originals=[]
    for group,pin in pins.items():
        cp=RAW/f'exec25_jtm_{group}_commit.json';tp=RAW/f'exec25_jtm_{group}_tree.json'
        for p in [cp,tp]:assert core.sha(p)==read(p.with_suffix('.receipt.json'))['sha256']
        commit=read(cp)[0];assert commit['sha']==pin['sha'] and commit['commit']['committer']['date']==pin['date']<='2026-10-07T15:59:59Z'
        tree=read(tp);assert tree['sha']==pin['sha'] and not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
        identities.extend([ref(cp,'Pinned identity'),ref(tp,'Complete selected tree')])
        for item in [x for x in selected if x['group']==group]:
            p=RAW/(item['id']+'.txt');rp=p.with_suffix('.receipt.json');r=read(rp);data=p.read_bytes()
            assert r['status']=='saved' and r['sha256']==core.sha(p)
            expected='https://raw.githubusercontent.com/'+pin['repository']+'/'+pin['sha']+'/'+item['upstream_path']
            assert r['url']==expected
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest();assert blob==blobs[item['upstream_path']]
            rows.append(dict(group=group,upstream_path=item['upstream_path'],local_path=str(p.relative_to(ROOT)),receipt=str(rp.relative_to(ROOT)),sha256=core.sha(p),git_blob=blob,url=expected))
            originals.append(dict(group=group,upstream_path=item['upstream_path'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'Public receipt'),git_blob=blob))
    write(BASE/'selected-originals.json',rows);write(BASE/'authenticated-originals.json',dict(count=36,groups=3,originals=originals,identities=identities,native_execution=False))
    sources=[];fragments=[]
    for group,checks in ANCHORS.items():
        pin=pins[group];evidence=[ref(RAW/f'exec25_jtm_{group}_commit.json','Pinned identity')];anchors=[];claims=[]
        for suffix,lo,hi,token,finding in checks:
            p=RAW/f'exec25_jtm_{group}_{suffix}.txt';lines=p.read_text().splitlines();hi=min(hi,len(lines));excerpt=chr(10).join(lines[lo-1:hi]);assert token in excerpt,(group,suffix,lo,token)
            binding=ref(p,f'Lines {lo}-{hi}: {finding}');evidence.append(binding);anchors.append(dict(path=binding['path'],line_spans=[[lo,hi]],finding=finding));claims.append(finding);fragments.append(dict(group=group,source=binding,first_line=lo,last_line=hi,text=excerpt))
        sources.append(dict(integrated_citation_key='exec25_jtm_'+group,kind='software',title=group+' pinned Java missingness and numerical-completion contracts',author=pin['repository']+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+pin['repository']+'/tree/'+pin['sha'],version_date=pin['date']+';'+pin['sha'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    write(BASE/'inspected-extracts.json',dict(count=len(fragments),anchors=fragments));write(BASE/'exact-results.json',exact.calculate())
    queries=[];leads={}
    for p in sorted(RAW.glob('exec25_jtm_search_*.json')):
        if p.name.endswith('.receipt.json'):continue
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='saved' and core.sha(p)==r['sha256'];d=read(p)
        queries.append(dict(original=ref(p,'Discovery only; creation-date filter is not historical search reconstruction'),total=d['total_count'],returned=len(d['items']),unreturned=max(0,d['total_count']-len(d['items'])),incomplete=d['incomplete_results'],lexical_mismatch=p.stem.endswith('_selection')))
        for x in d['items']:leads[x['full_name']]=dict(repository=x['full_name'],status='uninspected_discovery')
    assert len(queries)==6
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',queries=queries,unique_leads=len(leads),leads=list(leads.values()),absence_claim=False,saturation_claim=False))
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','Selected declarations')],findings=['Tetrad GPLv3 text; Weka selected source GPLv3-or-later and third-party declarations.','Smile selected core GPLv3/commercial and distinct Serve AGPLv3/commercial declarations; no quoted commercial price or distribution clearance.','No installed artifacts, transitive dependency resolution or current Weka edition inspected.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Authored arithmetic'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'inspected-extracts.json','Source semantics')],findings=['Three acyclic directed paths have a cyclic per-pair majority.','Pairwise covariance has negative quadratic form -8.','Parameter mixing adds variance1/4; diagonal fallback changes contrast variance0to2.','Scalar pooling gives19/3; weighted completion gives3/2versus1.','Target/source means1and1/5 differ despite complete data; hypothetical discrepancyUSD80000.'],native_execution=False))
    tests=['Freeze population, estimand, observation mask and assignment assumptions before selecting a component.','Compare EM means, covariance, likelihood trace, ridge effects, convergence and actual information counts against analytic Gaussian fixtures.','Check conditional draws separately from parameter uncertainty; expose all numerical fallbacks.','Test donor support, seed scope, ties, substantive-model compatibility and imputation diagnostics.','Preserve graph ensemble members; test majority cycles, equivalence-class validity and member-selection semantics.','Test pooled within/between variance and full covariance where needed.','Test row identifiers, class semantics, case weights, empty strata, cache invalidation and candidate-row uniqueness.','Qualify SVD rank/conditioning and neighbor empty-set behavior.','Acquire current Weka sources through an approved route and resolve exact component rights/prices.','Replay typed CLI/MCP fixtures and total public-prototype costs without requiring bank trials now.']
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Java missingness, transport separation and uncertainty contracts',selected=list(ANCHORS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',owner='Prototype implementation owner to be appointed',tests=tests,independent_branches=True,native_execution=False,bank_trials_required_now=False))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Candidate and query limits'),ref(BASE/'dependency-license-review.json','Rights limits'),ref(ROOT/'tools/public_sources.py','Fixed collector host policy'),ref(RAW/'exec25_jtm_weka_src05.txt','Official current source route')],known_routes=tests,uninspected=['EvoImp and EnsembleImputation discovery candidates.','Remaining returned candidates and complete technical delegates.','Current official Weka edition; host outside fixed collector policy.','Package-referenced scholarly originals not admitted here.'],unknown_universal_repairs=['Unrestricted MNAR and hidden causal assignment are not identified by imputation.','Unsupported target populations require data or justified restrictions.','Arbitrary dependence and learner uncertainty have no universal correction.'],next_action=NEXT))
    evidence=[ref(BASE/n,'Reviewed comparison') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','dependency-license-review.json','mathematical-review.json','comparison-review.json','qualification-plan.json','omissions-register.json']]
    sources.append(dict(integrated_citation_key='exec25_jtm_choice',kind='project_evidence_not_scholarly_paper',title='Authored Java missingness, graph aggregation and transport qualification decisions',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25 October 2026; cutoff7 October2026; no native execution',local_copy=ref(BASE/'mathematical-review.json','Exact witnesses'),evidence=evidence+[ref(Path(exact.__file__),'Authored reference')],inspected_anchors=[dict(anchor='Finite laws, source contracts and comparison decisions',inspection='Author inspection')],supported_claims=['36 authentic originals ground three bounded component comparisons.','Exact laws distinguish graph aggregation, uncertainty, weighting and target population.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=4,new_scholarly_pdfs=0,evidence=evidence,native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=evidence+[ref(BASE/'plan.md','Initial plan')],checks=['Imputation is distinct from population transport and causal identification.','Authored witnesses do not imply measured native failures.','Independent public qualification can proceed before bank trials; current Weka route does not block other work.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Connected banking argument'),ref(BASE/'sponsor-addition.md','Investment case')],findings=['Population target through missingness, numerical law, graphs, alternatives and implementation contracts.','Three source collections and authored witnesses cited with limits.','No scholarly citation admitted without original; no native or visual acceptance.'],visual_acceptance=False))
    evidence += [ref(BASE/n,'Reviewed integration') for n in ['source-audit.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md']]+[ref(Path(__file__),'Reviewer')]
    verify_bindings(dict(evidence=evidence));write(BASE/'review.json',dict(status='pass_for_bounded_source_work',operation_outcome='inconclusive',evidence=evidence,technical_anchors=len(fragments),originals=36,scholarly_originals=0,limitations=LIMITS,native_execution=False));print(json.dumps(dict(review='pass',outcome='inconclusive',originals=36,anchors=len(fragments))))

def receipt():
    review=read(BASE/'review.json');verify_bindings(review);assert exact.calculate()==read(BASE/'exact-results.json')
    state=core.read(ROOT,core.STATE);graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);output=ROOT/node['outputs'][0]
    write(output,read(BASE/'comparison-review.json'))
    evidence=[ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings=['Three source collections inspected; ecosystem, current-edition and native coverage remain incomplete.','Pinned originals and exact authored laws support claims; scholarly metadata is discovery only.','Conditional adoption, port, defer and reject routes retain scientific and rights conditions.']
    result=run.ledger.receipt_template(node);result.update(outcome='inconclusive',execution='performed',scope='Java transport and missingness primary-source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('Java transport/missingness coverage receipt prepared.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
