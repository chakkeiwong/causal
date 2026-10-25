#!/usr/bin/env python3
"""Authenticate remaining-language network sources; no acquired code execution."""
import argparse
import hashlib
import json
from pathlib import Path
import other_network_coverage_reference_20261025 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write as write_new, verify_bindings

run = controller.base
core = run.core
ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-25/other-network-coverage-v1'
RAW = ROOT/'docs/literature/raw'
OP = 'SW.CELL.networks_interference.other_relevant'
read = lambda p: json.loads(p.read_text())
SPECS = read(BASE/'anchor-specifications.json')
LIMITS = [
    'Five successful bounded repository queries,six leads and three rate-limit failures;no saturation or absence claim.',
    'No acquired code,installed package,upstream test or native experiment executed.',
    'Selected2025authorpaper only;no independent theorem validation or later publisher certification.',
    'Static source expressions and authored examples do not establish observed native failure rates.',
    'Complete artifacts,dependency rights,scientific qualification and bank state sufficiency remain open.',
    'Visual,independent and final acceptance remain open;proposal is not an implemented product.'
]
NEXT = ('Complete bounded direct-candidate and language-query tails;resolve dml4ssi rights;'
        'reconcile assignment-history length,variance normalization,auxiliary independence and experiment bookkeeping;'
        'qualify graph identity,multiplicity,state ownership,scheduling and restart on frozen public known-law fixtures.')
DECISIONS = [
    'dml4ssi:conditional method reference;defer native adoption until rights,equation-to-source mapping and complete experiment qualification.',
    'Graphs.jl:conditional Julia substrate with persistent external identity,remapping,direction and weight validation.',
    'Agents.jl:conditional public simulation;declare position versus borrower unit,scheduler,clock and full restart envelope.',
    'NetworkDynamics.jl:conditional dynamical substrate;qualify component ordering,aliasing,counterfactual isolation and numerical settings.',
    'petgraph:conditional Rust graph backend;choose Graph,StableGraph or GraphMap under explicit identity and multiplicity contracts.',
    'Graphology:conditional analyst interface;canonical keys,immutable snapshots and reviewed causal-edge provenance.',
    'Ports require a declared target and measured workflow benefit;reject silent semantic changes and automatic causal qualification.'
]


def write(path, value):
    if path.exists():
        assert read(path) == value, 'Preserve differing evidence: '+str(path)
    else:
        write_new(path, value)


def authenticated(path):
    receipt = read(path.with_suffix('.receipt.json'))
    assert receipt['status'] == 'saved' and core.sha(path) == receipt['sha256']
    return read(path)


def prepare():
    assert not (BASE/'review.json').exists()
    pins = {x['key']: x for x in read(BASE/'pins.json')}
    for x in read(BASE/'lead-pins.json'):
        pins[x['id']] = dict(key=x['id'], repository=x['repository'], commit=x['sha'], date=x['date'])
    identity, trees = [], {}
    for group, x in pins.items():
        prefix = 'exec25_onet_'+('lead_' if group in ['dml','spillovers'] else '')+group
        cp, tp = RAW/(prefix+'_commit.json'), RAW/(prefix+'_tree.json')
        commits, tree = authenticated(cp), authenticated(tp)
        assert commits[0]['sha'] == x['commit'] and commits[0]['commit']['committer']['date'] == x['date']
        assert x['date'] <= '2026-10-07T15:59:59Z' and tree['sha'] == x['commit'] and not tree['truncated']
        trees[group] = {y['path']: y for y in tree['tree'] if y['type'] == 'blob'}
        identity.extend([ref(cp,'Pinned revision/date'),ref(tp,'Complete selected tree')])
    rows = read(BASE/'selected-originals.json')+read(BASE/'delegate-originals.json')
    assert len(rows) == 58
    originals = []
    for x in rows:
        p, rp = ROOT/x['local_path'], ROOT/x['receipt']
        data, receipt = p.read_bytes(), read(rp)
        assert receipt['status'] == 'saved' and core.sha(p) == receipt['sha256'] and receipt['url'] == x['url']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == x['git_blob']
        assert trees[x['group']][x['upstream_path']]['sha'] == x['git_blob']
        originals.append(dict(group=x['group'],upstream_path=x['upstream_path'],git_blob=x['git_blob'],local_copy=ref(p,'Authentic original'),retrieval=ref(rp,'URL,date,hash')))
    write(BASE/'authenticated-originals.json',dict(status='pass',count=58,originals=originals,evidence=identity))
    sources, fragments = [], []
    for group, (title, repo, version, checks) in SPECS.items():
        pin = pins[group]
        prefix = 'exec25_onet_'+('lead_' if group == 'dml' else '')+group
        evidence = [ref(RAW/(prefix+'_commit.json'),'Pinned revision/date')]
        anchors, claims = [], []
        for suffix, lo, hi, tokens, finding in checks:
            p = RAW/f'exec25_onet_{group}_{suffix}.txt'
            lines = p.read_text().splitlines()
            text = '\n'.join(lines[lo-1:hi])
            assert all(t in text for t in tokens), (group,suffix,lo)
            binding = ref(p,f'Lines{lo}-{min(hi,len(lines))}: '+finding)
            evidence.append(binding)
            anchors.append(dict(path=binding['path'],line_spans=[[lo,min(hi,len(lines))]],finding=finding))
            claims.append(finding)
            fragments.append(dict(group=group,source=binding,first_line=lo,last_line=min(hi,len(lines)),text=text))
        sources.append(dict(integrated_citation_key='exec25_onet_'+group,kind='software',title=title,author=repo+' contributors',year=int(pin['date'][:4]),source_identity='https://github.com/'+repo+'/tree/'+pin['commit'],version_date=version+';'+pin['date']+';'+pin['commit'],local_copy=evidence[1],evidence=evidence,inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS,native_execution=False))
    assert len(fragments) == 58
    write(BASE/'inspected-extracts.json',dict(anchors=fragments,count=58))
    assert exact.calculate() == read(BASE/'exact-preflight.json')
    write(BASE/'exact-results.json',exact.calculate())
    queries, leads, failed = [], {}, []
    for rp in sorted(RAW.glob('exec25_onet_search*.receipt.json')):
        receipt = read(rp)
        if receipt['status'] != 'saved':
            failed.append(dict(url=receipt['url'],reason=receipt['error'],receipt=ref(rp,'Preserved failed query')))
            continue
        p = rp.with_name(rp.name.replace('.receipt.json','.json'))
        data = authenticated(p)
        for x in data['items']:
            leads[x['full_name']] = dict(repository=x['full_name'],language=x.get('language'),status='discovery_only_uninspected')
        queries.append(dict(url=receipt['url'],total=data['total_count'],returned=len(data['items']),unreturned=max(0,data['total_count']-len(data['items'])),incomplete=data['incomplete_results'],original=ref(p,'Discovery only'),receipt=ref(rp,'Query identity')))
    assert len(queries) == 5 and len(leads) == 6 and len(failed) == 3
    leads['johnchrishays/dml4ssi']['status'] = 'selected_primary_technical_anchors'
    leads['YushengGuan/Spillovers']['status'] = 'screened_cost_to_equilibrium_replication_not_admitted_as_general_borrower_estimator'
    screening = [ref(RAW/f'exec25_onet_spillovers_src{i:02d}.txt','Authentic candidate-screening original') for i in [1,2,3]]
    write(BASE/'search-screening.json',dict(cutoff='2026-10-07',cutoff_utc='2026-10-07T15:59:59Z',queries=queries,failed_queries=failed,unique_leads=6,leads=list(leads.values()),candidate_screening=screening,screening_anchors=['README_zh lines1-24:revised cost decomposition and default archived-equilibrium workflow.','CITATION lines1-18:software title,authors,release2026.09.18;not inspected manuscript evidence.','RELEASE_NOTES lines1-10:archived versus newly solved equilibrium distinction.'],additional_named_components=[pins[k]['repository'] for k in ['graphs','agents','dynamics','petgraph','graphology']],saturation_claim=False,absence_claim=False))
    write(BASE/'primary-review.json',dict(status='pass_for_selected_anchors',evidence=[ref(BASE/n,'Exact source custody') for n in ['authenticated-originals.json','inspected-extracts.json','search-screening.json','paper-review.json']],groups=6,anchors=58,scholarly_originals=1,native_execution=False))
    assert not [p for p in trees['dml'] if any(w in p.lower() for w in ['license','licence','copying','copyright'])]
    assert len(trees['dml']) == 9
    write(BASE/'dependency-license-review.json',dict(status='not_complete_clearance',evidence=[ref(BASE/'authenticated-originals.json','License and configuration originals')],findings=['dml4ssi complete nine-file tree has no license-named original;rights not inferred.','Selected manifest identifiesJulia1.11.4;complete dependency artifacts remain uninspected.','GraphsBSD-style,AgentsMIT,NetworkDynamicsMIT,petgraphMIT-or-Apache2.0,GraphologyMIT declarations retained.','Selected petgraph workspace declaresedition2024 andRust1.91;no installed-artifact certification.'],integration_allowed=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_authored_witnesses',evidence=[ref(Path(exact.__file__),'Independent finite enumeration'),ref(BASE/'exact-results.json','Exact replay'),ref(BASE/'paper-review.json','Primary equation conventions')],checks=['Uniform-phase fair blocks enumerate7/16for2observations and3/8for3;first truncated event1/2.','Out-of-domain fixed formula-1/16versus exact10-window7/64;not an extension of the primary theorem.','IPW group normalization2versus population normalization1.','Lag1 versus inclusive lag2 expressions-1/2and1/2;clamp is not calibration.','Four-score once/twice scaling variances1and1/4.','Parallel-edge exposure10/11becomes1/2under last-edge retention.','Sequential update order and nested-attribute custody examples reproduce.','Hypothetical USD30000 cost denominators reproduce30,50,75.'],native_execution=False))
    tests = ['Independent auxiliary trajectories and declared state sufficiency','Paper-to-source score,history and dependence-index mapping','Exact assignment probability,initial boundary and positivity','Normalization,finite-lag and batch covariance,negative-variance refusal','Truth generation,all comparator callers and complete failed-request counts','Persistent keys,vertex remapping,slot reuse,multiplicity,direction and weights','Position-versus-agent semantics and location invariants','Schedule,random streams,counterfactual state isolation and complete restart','Immutable attributes and CLI/MCP schema roundtrips','Pinned native artifacts,rights,full costs and qualified result/refusal oracles']
    write(BASE/'qualification-plan.json',dict(status='proposed_not_executed',tests=tests,dependencies='Source/equation reconciliation precedes native estimator admission;independent graph fixtures remain eligible.',native_execution=False))
    write(BASE/'comparison-review.json',dict(operation=OP,status='inconclusive',target='Shared-state estimators and remaining-language network contracts',selected=list(SPECS),decisions=DECISIONS,limitations=LIMITS,next_action=NEXT))
    write(BASE/'omissions-register.json',dict(global_blocker=False,evidence=[ref(BASE/'search-screening.json','Failed queries and candidates'),ref(BASE/'dependency-license-review.json','Rights and artifact limits')],known_routes=['Complete distinct permitted discovery routes and candidate technical inspection.','Reconcile source and paper conventions,resolve rights,and run future approved native known-law fixtures.','Qualify graph conversion,clock,state isolation,restart and full costs.'],unknown_universal_repairs=['Unknown bank state sufficiency,hidden confounding,arbitrary persistence and general dependent-data uncertainty require information or justified restrictions.'],next_action=NEXT))
    paper = read(BASE/'paper-identity.json')
    pr = read(BASE/'paper-review.json')
    pa = read(BASE/'paper-inspected-extracts.json')
    pp = ROOT/paper['local_copy']['path']
    assert core.sha(pp) == paper['local_copy']['sha256'] and pa['source'] == paper['local_copy']
    anchors = [dict(physical_pages=x['pages'],anchor='Physical PDF pages '+','.join(map(str,x['pages'])),text_extract=ref(BASE/'paper.txt','Genuine PDF text'),excerpt_sha256=hashlib.sha256(x['text'].encode()).hexdigest(),finding=x['claim']) for x in pa['anchors']]
    sources.append(dict(integrated_citation_key='exec25_onet_paper',kind='paper',title=paper['title'],filename_title=paper['title'],first_author='Hays',author='Hays, Chris and Raghavan, Manish',year=2025,source_identity='https://arxiv.org/pdf/2504.08836v1',version_date=paper['version'],local_path=str(pp.relative_to(ROOT)),sha256=core.sha(pp),local_copy=paper['local_copy'],identity_evidence=[paper['identity'],paper['retrieval']],inspected_anchors=anchors,supported_claims=pr['supported_claims'],limitations=pr['limitations'],evidence=[ref(BASE/'paper-review.json','Bounded primary review')]))
    sources.append(dict(integrated_citation_key='exec25_onet_choice',kind='project_evidence_not_scholarly_paper',title='Authored shared-state and remaining-language network qualification comparison',author='Causal banking proposal project',year=2026,source_identity=str(BASE.relative_to(ROOT)),version_date='25October2026;cutoff7October2026;no native execution',local_copy=ref(BASE/'mathematical-review.json','Authored exact witnesses'),evidence=[ref(BASE/n,'Reviewed comparison') for n in ['comparison-review.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','primary-review.json']],inspected_anchors=[dict(anchor='Selected source comparison,exact examples and conditional adoption decisions',inspection='Author inspection')],supported_claims=['58software/screening originals,58technical anchors,sixsoftwarecollections and genuine48-pagepaper.','Explicit equations,graph identity,scheduling,state,restart,interface and public qualification routes.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,new_records=8,new_scholarly_pdfs=1,evidence=[ref(BASE/'authenticated-originals.json','58authenticated originals')],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_inconclusive_source_work',evidence=[ref(BASE/n,'Reviewed source work') for n in ['plan.md','plan-review.json','primary-review.json','mathematical-review.json','qualification-plan.json','omissions-register.json']],checks=['Direct causal implementation and genuine primary paper included beside graph substrates.','Bound active versus unused helper observations;no theorem refutation or native failure inferred.','Keep search,rights,artifact,visual and final gates open;serialize after C++ delivery.']))
    write(BASE/'copyedit-review.json',dict(status='pass_for_connected_argument',evidence=[ref(BASE/'development.tex','Banking argument'),ref(BASE/'sponsor-addition.md','Investment argument')],findings=['Explained direct/global targets,assumptions,window probabilities,variance and counterexamples.','Distinct direct-use,port and rejection decisions with public qualification sequence.','Process custody remains in audit records;no empirical bank or native claims.'],visual_acceptance=False))
    names = ['authenticated-originals.json','primary-review.json','mathematical-review.json','comparison-review.json','source-audit.json','search-screening.json','dependency-license-review.json','qualification-plan.json','omissions-register.json','plan-review-v2.json','copyedit-review.json','development.tex','sponsor-addition.md','anchor-specifications.json','paper-review.json','paper-identity.json']
    review = dict(status='pass_for_selected_source_work',operation_outcome='inconclusive',evidence=[ref(BASE/n,'Bounded reviewed comparison') for n in names]+[ref(Path(__file__),'Reviewer')],findings=['58authenticated originals,58technical anchors and genuine48-pageauthorpaper.','Paper guarantees,static source findings,authored examples and native qualification remain distinct.'],limitations=LIMITS,native_execution=False)
    verify_bindings(review)
    write(BASE/'review.json',review)
    print(json.dumps(dict(review='pass_for_selected_work',originals=58,anchors=58,new_records=8,outcome='inconclusive')))


def receipt():
    state = core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    verify_bindings(read(BASE/'review.json'))
    graph, merged, _ = run.combined(ROOT,state)
    node = run.ledger.operation(graph,OP)
    value = read(BASE/'comparison-review.json')
    value['evidence'] = [ref(BASE/'review.json','Selected review')]
    output = ROOT/node['outputs'][0]
    write(output,value)
    evidence = [ref(BASE/n,'Reviewed coverage') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json']]
    findings = ['Selected direct Julia causal implementation and graph/simulation/interface originals inspected;search/native coverage incomplete.','Claims bind authentic dated originals and primary paper;exact authored expressions reproduce.','Explicit integration,port and rejection routes retain scientific,rights,artifact and final acceptance limits.']
    result = run.ledger.receipt_template(node)
    result.update(outcome='inconclusive',execution='performed',scope='Shared-state and remaining-language network source comparison',reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Bounded coverage')],criteria=[dict(index=i,verdict='inconclusive' if i==0 else 'pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=NEXT)
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']))
    verify_bindings(result)
    write(BASE/'operation-receipt.json',result)
    print('Remaining-language network receipt prepared.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command',choices=['prepare','receipt'])
    globals()[p.parse_args().command]()
