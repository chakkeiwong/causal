#!/usr/bin/env python3
"""Bounded Julia/JavaScript source review; never a general identification award."""
import hashlib
import json
from pathlib import Path

import other_identification_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
RAW = ROOT/'docs/literature/raw'
BASE = ROOT/'docs/program/execution/2026-10-19/other-identification-v1'
OP = 'SW.CELL.identification_counterfactual.other_relevant'
OUTPUT = ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())


def authenticate(identifier, upstream, project, repository, sections):
    commit_path = RAW/f'exec13_other_commit_{project}.json'
    tree_path = RAW/f'exec13_other_tree_{project}.json'
    commit, tree = read(commit_path)[0], read(tree_path)
    pin = commit['sha']
    assert tree['sha'] == pin and not tree['truncated']
    path = RAW/(identifier+'.txt')
    receipt_path = RAW/(identifier+'.receipt.json')
    receipt, data = read(receipt_path), path.read_bytes()
    url = f'https://raw.githubusercontent.com/{repository}/{pin}/{upstream}'
    assert receipt['status'] == 'saved' and receipt['url'] == url
    assert receipt['sha256'] == core.sha(path)
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    matches = [r for r in tree['tree'] if r['path'] == upstream and r['type'] == 'blob']
    assert len(matches) == 1 and matches[0]['sha'] == blob
    lines = data.decode().splitlines()
    assert all(1 <= a <= b <= len(lines) for a, b in sections)
    anchors = '; '.join(f'lines {a}-{b}' for a, b in sections)
    record = dict(role='inspected_primary_technical_text', source_identity=url,
        version_date=commit['commit']['committer']['date']+'; '+pin,
        local_copy=ref(path, anchors), receipt=ref(receipt_path, 'Primary acquisition and content hash'),
        identity_evidence=[ref(commit_path, 'Selected pre-cutoff commit'), ref(tree_path, 'Complete selected tree')],
        git_blob_sha1=blob, inspected_anchors=[anchors], executed=False)
    extract = dict(source=upstream, local_copy=record['local_copy'], sections=[dict(start=a,end=b,
        text='\n'.join(f'{i+1}: {lines[i]}' for i in range(a-1,b))) for a,b in sections])
    return record, extract


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    state = core.read(ROOT, core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    assert exact.calculate() == read(BASE/'exact-results.json')
    write(BASE/'execution-plan-review.json', dict(status='pass_to_execute', reviewer=REVIEWER,
        prior_plan=ref(BASE/'plan-review.json', 'Preserved prepared plan'),
        steps=['Authenticate selected files against receipts and pinned Git blobs.',
            'Separate graph editing, adjustment searches, identification and cross-world questions.',
            'Keep tests as inspected source; reproduce only the authored exact law.',
            'Record unresolved coverage and proofs; publish preserving reader and sponsor successors.',
            'Renew exact-reader reviews and continue independent ready work.'],
        challenge_findings=['A returned set is not a numerical effect or a universal identification result.',
            'Explicit observed-variable restrictions and search completion must survive conversion.',
            'Failed or empty results cannot silently become a zero effect.',
            'New PDF length does not close an existing substantive repair contract.'],
        native_execution=False, visual_acceptance=False))
    specs = [
        ('exec19_oid_julia_0','src/CausalInference.jl',[(1,62)]),
        ('exec19_oid_julia_1','src/do.jl',[(1,14)]),
        ('exec19_oid_julia_2','src/backdoor.jl',[(29,64),(76,127)]),
        ('exec19_oid_julia_3','src/recantingwitness.jl',[(1,70)]),
        ('exec19_oid_julia_4','docs/src/examples/backdoor_example.md',[(31,84)]),
        ('exec19_oid_julia_5','test/backdoor.jl',[(1,45)]),
        ('exec19_oid_julia_6','src/gensearch.jl',[(118,160),(187,247),(249,305),(307,392)]),
        ('exec19_oid_julia_tests','test/gensearch.jl',[(7,49),(51,98),(100,121)]),
        ('exec13_other_file_causalinference_1','LICENSE.md',[(1,22)]),
        ('exec13_other_file_causalinference_2','Project.toml',[(1,32),(46,80)])]
    julia, extracts = [], []
    for identifier, upstream, sections in specs:
        r, e = authenticate(identifier,upstream,'causalinference','mschauer/CausalInference.jl',sections)
        julia.append(r); extracts.append(e)
    dag, e = authenticate('exec13_other_file_dagitty_3','jslib/graph/GraphAnalyzer.js',
        'dagitty','jtextor/dagitty',[(384,443),(465,574),(1189,1210),(1593,1640)])
    extracts.append(e)
    inherited = ROOT/'docs/program/execution/2026-10-18/dagitty-reuse/source-audit.json'
    verify_bindings(read(inherited))
    write(BASE/'inspected-extracts.json',dict(records=extracts,native_execution=False))
    jclaims = [
        'The selected do! method removes incoming edges and returns the graph; it does not evaluate an intervention distribution.',
        'Adjustment and frontdoor methods expose mandatory I and allowed R sets; default R contains every nonendpoint vertex. The example explicitly removes unobserved vertices.',
        'Find methods return sets or false; iterator exhaustion is nothing and iterator size is unknown. Empty solution and no emitted solutions must stay distinct.',
        'find_backdoor_adjustment passes find_covariate_adjustment directly to setdiff without a local false guard; exact failure behavior remains a native conformance question.',
        'Selected frontdoor search is a graphical set search, not a general ID/IDC or counterfactual evaluator.',
        'The recanting-witness helper describes a path-specific question under complete observations. Its named proof is not inspected in this review.',
        'Inspected tests include explicit allowed-set exclusions, expected set enumeration, false results and selected invalid d-separation inputs. Tests were not executed.',
        'Project metadata declares version 0.19.4 with dependency ranges; the selected license declares MIT. Neither binds a fully resolved runtime distribution.']
    dclaims = [
        'The selected total-adjustment interface accepts dag/pdag/mag/pag tags; the direct-effect interface restricts to dag and rejects selection nodes.',
        'Missing source/target, failed adjustment conditions and selected selection failures can return false or empty lists on different interfaces.',
        'Total-adjustment enumeration carries latent and selection annotations and can impose max_nr; a result list alone does not certify exhaustive completion.',
        'Selected MAG/PAG validation branches retain TODOs for proper validation; passing these branches does not establish all scientific graph premises.']
    limits = ['Bounded Julia/JavaScript originals do not close other-language or complete package discovery.',
        'No installed Julia, JavaScript/browser, upstream tests or adapter execution occurred.',
        'Source comments identify proof leads but do not substitute for genuine inspected scholarly PDFs.',
        'Selected-function findings are not package-wide absence or completeness claims.',
        'No integration permission, runtime rights, scientific qualification or observed bank economics is granted.']
    sources=[]
    for key,title,author,identity,version,records,claims in [
        ('exec19_otherid_julia','CausalInference.jl selected graphical adjustment and frontdoor interfaces','CausalInference.jl contributors',
         'https://github.com/mschauer/CausalInference.jl','0.19.4; 459d654d765b5eadbc9071a1013b8e34346fc0be; 10 August 2026',julia,jclaims),
        ('exec19_otherid_dagitty','DAGitty selected adjustment and graph-validation interfaces','DAGitty contributors',
         'https://github.com/jtextor/dagitty','7a657776dc8f5e5ba4e323edb028e2c2aaf29327; 6 December 2024',[dag],dclaims)]:
        sources.append(dict(integrated_citation_key=key,kind='software_primary_sources',title=title,
            author=author,year=2026,source_identity=identity,version_date=version,local_copy=records[0]['local_copy'],
            records=records,inspected_anchors=[dict(anchor=c,inspection='Selected original source path') for c in claims],
            supported_claims=claims,limitations=limits))
    sources.append(dict(integrated_citation_key='exec19_otherid_reference',kind='project_authored_exact_reference',
        title='Exact positive-law frontdoor and lending-value reference',author='Causal banking proposal project',year=2026,
        source_identity='tools/other_identification_reference_20261019.py',version_date='19 October 2026',
        local_copy=ref(ROOT/'tools/other_identification_reference_20261019.py','calculate: exact rational enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Observed and intervention law enumeration')],
        supported_claims=['The stipulated law gives intervention and frontdoor risks 3/8 and 5/8.',
            'Observed and mediator-standardized contrasts are 3/8 and 1/8, versus intervention contrast 1/4.',
            'Assumed payoff100 and action cost20 yield net5,35/2,-15/2 respectively.'],
        limitations=['Exact identity for this stipulated law, not a general frontdoor proof or native execution.',
            'All payoff and cost amounts are assumed; no measured bank benefit.']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',records=julia+[dag],
        inherited_dagitty_audit=ref(inherited,'Previously reviewed JavaScript component scope'),
        supported_claims=jclaims+dclaims,native_execution=False))
    omissions=[dict(item=item,status=status,route=route) for item,status,route in [
        ('Additional language candidates','open','Continue primary discovery, distinguish bindings from independent algorithms and retain dated coverage limits.'),
        ('Adjustment and frontdoor proof originals','not_inspected_not_cited','Acquire genuine PDFs for source-linked arXiv1203.3515,1803.00116,2211.16468 and inspect exact graph/query assumptions.'),
        ('Path-specific proof and implementation correspondence','not_inspected','Acquire the genuine named path-specific original; check observation and cross-world premises, algorithm correspondence and adverse fixtures.'),
        ('Julia false-to-setdiff behavior','not_executed','Run separately admitted pinned runtime with impossible and inconsistent I/R cases; preserve error rather than assigning nonidentification.'),
        ('DAGitty graph validity and result truncation','not_fully_qualified','Validate scientific graph premises externally and track completion/budget with adverse graph fixtures.'),
        ('General ID/IDC, counterfactual and partial-identification coverage','not_established','Inspect actual matching algorithms and proof contracts; do not infer absence from selected adjustment files.'),
        ('Distribution rights and native environment','deferred','Resolve dependencies and notices for actual distribution before proposing an executable boundary.')]]
    write(BASE/'omissions-register.json',dict(items=omissions,global_blocker=None))
    write(BASE/'proof-discovery-check.json',dict(provider='built-in web',date='2026-10-19',
        queries=['site.arxiv.org/abs/1203.3515','site.arxiv.org/abs/1803.00116','site.arxiv.org/abs/2211.16468'],
        observation='Search and direct abstract open returned no usable text; no new source admitted.',
        local_filename_search='No matching filenames for validity of covariate, separators, frontdoor or path-specific; not a proof of absence under other names.',
        absence_claim=False,cutoff='2026-10-07'))
    contract=dict(status='proposed_not_implemented',integration_allowed=False,requirements=[
        'Preserve graph class, endpoint marks, latent/selected status, temporal order and observed-variable availability.',
        'Validate disjoint nonempty query sets and I subset R inside the permitted observed candidates before search.',
        'Separate graph editing, set validity, set enumeration, functional identification and numerical estimation.',
        'Represent one empty adjustment set separately from no emitted sets; preserve false, exceptions and cancellation.',
        'Return no_adjustment_route only for the declared criterion and a valid completed search, never universal not_identified.',
        'Record enumeration budget and completion independently; a cap reached is not proof that additional solutions exist or do not exist.',
        'Require a reviewed applicable identification certificate for not_identified; otherwise unknown, unsupported, invalid_request or execution_error.',
        'Reject hidden-variable adjustment and unqualified graph classes; retain original result for diagnosis.',
        'No default numerical zero, graph coercion, dropped uncertainty or automatic path-specific permission.'])
    write(BASE/'conversion-contract.json',contract)
    evidence=[ref(BASE/n,'Inspected source, semantic or omission evidence') for n in [
        'plan-review.json','execution-plan-review.json','search-review.json','proof-discovery-check.json',
        'source-audit.json','inspected-extracts.json','exact-results.json','omissions-register.json','conversion-contract.json']]
    evidence += [ref(Path(__file__),'Exact review construction')]
    criteria=[dict(index=0,verdict='inconclusive',finding='Two inherited candidates are inspected; complete other-language and algorithm coverage remains unresolved.'),
        dict(index=1,verdict='pass',finding='Eleven selected original files match acquisition hashes and pinned Git blobs; exact authored law reproduces without upstream execution.'),
        dict(index=2,verdict='pass',finding='Alternative routes, proof/runtime gaps and discovery omissions are explicit; no essential original is waived.')]
    trigger='Acquire and inspect matched adjustment/frontdoor/path-specific originals; extend other-language discovery and qualify explicit query, latent-variable, failure and completion contracts in a separately admitted prototype.'
    output=dict(operation_id=OP,status='inconclusive',scope='Julia and JavaScript graphical adjustment and identification boundaries',
        reviewer=REVIEWER,cutoff='2026-10-07',candidate_ids=['inherited:causalinference','inherited:dagitty'],
        documented_findings=jclaims+dclaims,alternatives=['General ID engines have distinct proof and graph contracts.',
            'Use an exact declared-law reference before native conformance; do not turn failed adjustment into universal nonidentification.'],
        evidence=evidence,limitations=limits,criteria=criteria,revisit_trigger=trigger,
        integration_allowed=False,capabilities=[],coverage_complete=False,bank_inputs_required=False)
    write(OUTPUT,output)
    write(BASE/'primary-review.json',dict(status='pass_for_bounded_source_claims',reviewer=REVIEWER,evidence=evidence,
        primary_files=11,upstream_tests='inspected_not_run',exact_reference='reproduced',limitations=limits))
    write(BASE/'review.json',dict(status='inconclusive_for_coverage',reviewer=REVIEWER,
        reviewed_output=ref(OUTPUT,'Bounded coverage disposition'),findings=criteria,evidence=evidence,limitations=limits))
    graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=output['scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted coverage review')],limitations=limits,
        nonexecution_reason='',revisit_trigger=trigger,criteria=[dict(c,evidence=evidence+[ref(BASE/'review.json','Author review')]) for c in criteria])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings([output,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',primary_files=11,exact_reference='pass',native_execution=False)))


if __name__ == '__main__':
    main()
