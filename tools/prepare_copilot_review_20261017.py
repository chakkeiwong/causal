#!/usr/bin/env python3
"""Preserve genuine Copilot bytes and bounded primary/static/exact reviews."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

import copilot_reference_20261017 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'docs/literature/raw'
RECOVERY = ROOT/'docs/program/execution/2026-10-17/census-recovery'
BASE = RECOVERY/'copilot-v1'
COMMIT = 'a31aa7cab277d7e19478bc326dbec154525969cc'
TREE = '586f930d10eda074bca396e6f55c3684eb4f338d'
FILES = {
    'license': (9, 'LICENSE'), 'readme': (9, 'README.md'),
    'pyproject': (9, 'pyproject.toml'), 'requirements': (9, 'requirements_cpu.txt'),
    'main': (9, 'main.py'), 'judge': (9, 'postprocess/judge.py'),
    'judge_functions': (9, 'postprocess/judge_functions.py'),
    'evaluator': (9, 'causal_discovery/evaluation/evaluator.py'),
    'benchmark': (9, 'causal_discovery/evaluation/benchmarking_integrated.py'),
    'config': (9, 'causal_discovery/evaluation/benchmarking_integrated_config.py'),
    'causallearn_license': (9, 'externals/causal-learn/LICENSE'),
    'prompt': (10, 'postprocess/context/pruning_prompt.txt'),
    'program': (10, 'causal_discovery/program.py'),
    'filter': (10, 'causal_discovery/filter.py'), 'state': (10, 'global_setting/state.py')}
PAGES = {
    1: 'Title, thirteen authors, exact arXiv v2 date and code repository identity.',
    4: 'Natural-language objective/constraint parsing and user revisions; preprocessing scope.',
    5: 'Diagnostics and filtering are author-described workflow components, not certificates of causal assumptions.',
    6: 'Ranking, configuration, execution-error revision and bootstrap edge confidence.',
    7: 'Explicit no-override claim for high-confidence bootstrap decisions; PDF report generation.',
    16: 'Web interface is author-described; no present deployment trial established.',
    29: 'Section5.2 explicitly generates synthetic scenarios with known ground truth.',
    30: 'Table2 default/sparse countercomparisons; simulated financial scenario50 nodes/three domains, F1 .650 plus/minus .130.',
    31: 'Linear stationary temporal Table3; default .673 vs .695/.733; n5000 table .668 but prose .649; very-large table p100 but prose p1000.',
    33: 'Conclusion describes automated selection/configuration/execution; proposed future extensions.',
    46: 'Temporal simulation is stationary linear; preliminary design settings are scoped.',
    47: 'Runtime cap20min; best-DAG conversion for tabular graphs; temporal summary-graph evaluation and excluded diagonals.'}
RANGES = {
    'evaluator': [(9,54,'Edge tags, receiver/source convention, default sample=False and asymmetric-tag requirement.'),
        (154,215,'Default helper consults true_graph when orienting ambiguous predicted edge tags.'),
        (266,327,'Default helper invocation and minimum-SHD selection; sampling mode also selects against truth.'),
        (330,365,'Ordered off-diagonal binary metrics; autoregressive diagonals omitted.')],
    'benchmark': [(108,119,'Default GraphEvaluator construction.'),
        (234,246,'Benchmark replaces missing values with zero; this is a preprocessing choice.'),
        (318,347,'Timer covers Programming.forward; temporal branch uses direct binary scoring, tabular branch compute_metrics.')],
    'judge_functions': [(15,55,'IID row branch; temporal block_size10 and block starts sampled without replacement.'),
        (221,265,'High/low thresholds and low directed entries included in middle_prob_edges.'),
        (310,338,'Middle ordered entries combined and deduplicated as unordered pairs.'),
        (435,461,'Accepted A/B responses direct an edge; accepted C creates a forbid entry.')],
    'judge': [(58,128,'Reachable quality_judge passes ts=False; fixed_pairs=[] permits later LLM edits; KCI/cycle steps follow.'),
        (133,153,'Judge.forward reaches quality_judge.')],
    'main': [(280,300,'Main execution path reaches Judge.forward.')],
    'filter': [(15,40,'User selection bypasses filtering; otherwise LLM selects candidates at temperature0.'),
        (65,90,'Prompt uses query, statistics, knowledge, resources and requested CPDAG/DAG output.')],
    'program': [(9,78,'Wrapper invocation, optional correlated-feature removal/restoration and returned lag-matrix storage.')],
    'state': [(20,48,'accept_CPDAG=True and boot_num=20 defaults.'),
        (80,106,'Distinct raw/revised/lagged fields do not alone establish semantic compatibility.')],
    'pyproject': [(1,24,'Default pytest excludes integration/LLM/LaTeX categories; tests are declared, not absent.')],
    'requirements': [(1,38,'Pinned requirements coexist with unpinned huggingface-hub; not a complete environment lock.')],
    'prompt': [(1,200,'Inspect full prompt: A/B direction, C no relationship and D unknown remain distinct.')],
    'license': [(1,22,'Root MIT, copyright2026 contributors; preserve notice and warranty disclaimer.')],
    'causallearn_license': [(1,22,'Vendored causal-learn MIT, copyright2022cmu-phil; not every dependency license.')],
    'readme': [(1,25,'Repository title, description and historical presentation only.')],
    'config': [(1,55,'Declared benchmark configuration is source context, not proof of executed experiments.')]}
LIMITS = [
    'Author review of paper and static historical source only; no downloaded code, model, paid engine or bank workflow executed.',
    'The2026-05-15 source snapshot is not established as the2025 paper experiment code.',
    'Conditional witnesses stipulate inputs and accepted responses; they do not observe an upstream failure or source experiment.',
    'Root MIT and one vendored MIT notice do not close all dependency, asset, data, provider or deployment rights.',
    'Original113-candidate census remains37 inspected/76 unread; citation-chain lead is separately tracked.',
    'No exclusive depth, full repair, visual or final proposal acceptance awarded.']


def read(path):
    return json.loads(path.read_text())


def main():
    assert not BASE.exists()
    BASE.mkdir()
    commit_file=RAW/'exec17_census_search7_copilot_cutoff_commit.json'
    tree_file=RAW/'exec17_census_search8_copilot_tree.json'
    commit=read(commit_file)[0]
    tree=read(tree_file)
    assert commit['sha']==COMMIT and commit['commit']['tree']['sha']==TREE
    assert commit['commit']['committer']['date']=='2026-05-15T14:43:14Z'
    assert tree['sha']==TREE and tree['truncated'] is False and len(tree['tree'])==1540
    members={r['path']:r for r in tree['tree']}
    checked=[]
    anchors=[]
    for key,(search,original_path) in FILES.items():
        local=RAW/f'exec17_census_search{search}_copilot_{key}.txt'
        receipt=local.with_suffix('.receipt.json')
        entry=read(receipt)
        data=local.read_bytes()
        assert entry['status']=='saved' and entry['http_status']==200
        assert entry['path']==str(local.relative_to(ROOT)) and entry['bytes']==len(data)
        assert entry['sha256']==hashlib.sha256(data).hexdigest()
        assert entry['url']==f'https://raw.githubusercontent.com/Lancelot39/Causal-Copilot/{COMMIT}/{original_path}'
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert members[original_path]['type']=='blob' and members[original_path]['sha']==blob
        assert members[original_path]['size']==len(data)
        checked.append(dict(original_path=original_path,git_blob_sha1=blob,
            local_copy=ref(local,'Pinned authentic upstream file'),receipt=ref(receipt,'Bounded HTTPS retrieval')))
        lines=data.decode().splitlines()
        for lo,hi,finding in RANGES[key]:
            end=min(hi,len(lines))
            excerpt=BASE/f'{key}-lines-{lo}-{end}.txt'
            excerpt.write_text(''.join(f'{i}: {lines[i-1]}\n' for i in range(lo,end+1)))
            anchors.append(dict(file=original_path,anchor=f'Lines{lo}–{end}',finding=finding,
                extracted_text=ref(excerpt,'Inspected pinned primary source lines')))
    write(BASE/'git-byte-validation.json',dict(status='pass',repository='Lancelot39/Causal-Copilot',
        cutoff='2026-10-07',cutoff_instant='2026-10-07T15:59:59Z',commit=COMMIT,
        commit_date=commit['commit']['committer']['date'],tree=TREE,tree_truncated=False,
        tree_entries=1540,validated_files=checked,
        evidence=[ref(commit_file,'Historical commit query'),ref(tree_file,'Complete selected Git tree')],
        execution=False,limits=LIMITS))
    original=RAW/'exec17_census_search6_copilot_v2.pdf'
    paper_receipt=read(original.with_suffix('.receipt.json'))
    assert paper_receipt['status']=='saved'
    assert hashlib.sha256(original.read_bytes()).hexdigest()==paper_receipt['sha256']=='af514a45ed019fd6d38e7902d5ad945a6d34fc227c0f5f3d4e615f911d6ed083'
    dest=ROOT/'docs/papers/Causal-Copilot An Autonomous Causal Analysis Agent Wang(2025).pdf'
    assert not dest.exists()
    dest.write_bytes(original.read_bytes())
    full=BASE/'copilot-full.txt'
    subprocess.run(['pdftotext','-layout',str(dest),str(full)],check=True,timeout=20)
    pages=full.read_text().split(chr(12))
    assert len([p for p in pages if p.strip()])==61
    paper_anchors=[]
    for page,finding in PAGES.items():
        excerpt=BASE/f'paper-page-{page}.txt'
        excerpt.write_text(pages[page-1])
        paper_anchors.append(dict(anchor=f'Physical PDF page{page}',finding=finding,
            extracted_text=ref(excerpt,'Inspected genuine exact-version primary page')))
    paper=dict(integrated_citation_key='exec17_copilot_paper',kind='paper',
        title='Causal-Copilot: An Autonomous Causal Analysis Agent',
        filename_title='Causal-Copilot An Autonomous Causal Analysis Agent',first_author='Wang',
        author='Xinyue Wang and Kun Zhou and Wenyi Wu and Har Simrat Singh and Fang Nan and Songyao Jin and Aryan Philip and Saloni Patnaik and Hou Zhu and Shivam Singh and Parjanya Prashant and Qian Shen and Biwei Huang',
        year=2025,source_identity='https://arxiv.org/pdf/2504.13263v2',
        version_date='arXiv2504.13263v2,2025-04-21; acquired2026-10-17',cutoff='2026-10-07',
        local_copy=ref(dest,'Authentic61-page arXiv v2; no summary substitution'),
        local_path=str(dest.relative_to(ROOT)),sha256=paper_receipt['sha256'],
        inspected_anchors=paper_anchors,related_primary_bytes=[
            ref(original,'Retrieved v2'),ref(original.with_suffix('.receipt.json'),'Successful acquisition receipt'),
            ref(RAW/'exec17_census_search5_copilot_v1.pdf','Preserved distinct earlier version')],
        supported_claims=[
            'The described pipeline separates natural-language interaction, preparation, selection, execution, graph refinement and reporting.',
            'Paper p7 explicitly states LLM suggestions cannot override high-confidence bootstrap decisions.',
            'Table2 includes default/sparse countercomparisons; the financial scenario is generated, not bank validation.',
            'Table3 is linear stationary and does not establish universal superiority; its p100/p1000 and .668/.649 discrepancies are retained.',
            'AppendixD reports best-DAG conversion and temporal summary-graph metrics excluding diagonals; no lag-specific or autoregressive qualification follows.'],
        unresolved_source_issues=['Temporal table/prose discrepancies remain unresolved.',
            'No established binding between this2025 paper experiment and the selected2026 source snapshot.'],limitations=LIMITS)
    code=dict(integrated_citation_key='exec17_copilot_code',kind='software',
        title='Causal-Copilot historical selection, execution, judging and evaluation source',
        author='Causal-Copilot contributors',year=2026,
        source_identity=f'https://github.com/Lancelot39/Causal-Copilot/tree/{COMMIT}',
        version_date='Git commit'+COMMIT+',2026-05-15T14:43:14Z; retrieved2026-10-17',
        local_copy=ref(BASE/'git-byte-validation.json','Fifteen byte-validated files from complete historical tree'),
        inspected_anchors=[a for a in anchors if a['file'] not in ['LICENSE','externals/causal-learn/LICENSE']],
        supported_claims=[
            'Default tabular benchmark compute_metrics invokes a truth-assisted orientation helper; sampling mode also chooses against truth. This concerns evaluation, not observed live-discovery truth leakage.',
            'The selected main/Judge call path passes ts=False despite an available temporal block branch.',
            'Low ordered reverse entries can return a high-confidence unordered pair to the LLM; fixed_pairs=[] does not enforce the paper no-override promise.',
            'A conditional accepted C response can erase the stipulated high-confidence edge before later KCI/cycle operations.',
            'User-selected algorithms bypass filtering; a DAG preference does not supply identifying orientation evidence.',
            'Lag matrices can be retained when returned, but summary scoring and state fields alone do not establish temporal semantics.',
            'Default tests exclude three marked categories, and at least one requirement is unpinned; no absence-of-tests claim.'],
        limitations=LIMITS)
    rights=dict(integrated_citation_key='exec17_copilot_rights',kind='software_documentation',
        title='Causal-Copilot and vendored causal-learn bounded MIT notices',
        author='Causal-Copilot contributors and cmu-phil',year=2026,
        source_identity=f'https://github.com/Lancelot39/Causal-Copilot/blob/{COMMIT}/LICENSE',
        version_date='Pinned2026-05-15 source; root copyright2026, vendored copyright2022',
        local_copy=ref(RAW/'exec17_census_search9_copilot_license.txt','Root MIT license'),
        related_primary_bytes=[ref(RAW/'exec17_census_search9_copilot_causallearn_license.txt','Vendored MIT notice'),
            ref(BASE/'git-byte-validation.json','Historical byte bindings')],
        inspected_anchors=[a for a in anchors if a['file'] in ['LICENSE','externals/causal-learn/LICENSE']],
        supported_claims=['Both inspected notices grant MIT permissions subject to notice inclusion and disclaim warranty.',
            'These two notices do not establish complete transitive dependency, asset, data, provider or deployment rights.'],limitations=LIMITS)
    write(BASE/'exact-results.json',exact.serial(exact.calculate()))
    derivation=dict(integrated_citation_key='exec17_copilot_exact',kind='project_derivation',
        title='Observational equivalence, bootstrap stability and conditional graph-edit references',
        author='Causal banking proposal',year=2026,version_date='2026-10-17',
        source_identity='Project-authored two-world structural laws and finite static witnesses',
        local_copy=ref(BASE/'exact-results.json','Fraction arithmetic and independent finite enumerations'),
        inspected_anchors=['Two structural worlds and observational/interventional enumeration',
            '6^6 bootstrap sequence and4^6 stipulated dataset enumerations',
            'Two opposite two-node DAG truths and fixed/assisted F1',
            'Stipulated19/20 vs1/20 bootstrap collection; accepted-C mutation and proposed unordered guard'],
        supported_claims=['Same positive observational law supports the two specified effects .8 and0 and hypothetical USD50/−30 incremental values.',
            'Conditional positive-covariance bootstrap probability is31/32, distinct from causal identification and algorithm edge selection.',
            'Truth-assisted two-node orientation scores1 in both worlds; a fixed direction scores1and0.',
            'Conditional graph-deletion reference reproduces inspected recommendation/pair/empty-guard expressions, stopping before later pruning.'],
        records=[ref(ROOT/'tools/copilot_reference_20261017.py','Authored independently enumerated reference; no upstream imports')],limitations=LIMITS)
    sources=[paper,code,rights,derivation]
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=sources,
        prior=ref(RECOVERY/'benchmark-v1/reader/source-audit.json','738 predecessor records')))
    verify_bindings(read(BASE/'source-audit.json'))
    write(BASE/'primary-review.json',dict(status='pass',issues=[],scope='Bounded author primary and static source review',
        reviewer=dict(name='Codex author/coordinator',kind='author'),sources=sources,
        source_limits=paper['unresolved_source_issues'],evidence=[
            ref(BASE/'git-byte-validation.json','All15 files match selected Git blobs'),
            ref(BASE/'exact-results.json','Reviewed authored exact examples'),
            ref(RECOVERY/'copilot-plan.md','Reviewed continuation plan'),
            ref(Path(__file__),'Audits and inspected anchors')],limitations=LIMITS,final_acceptance=False))
    prior=read(RECOVERY/'benchmark-v1/census-register.json')
    assert prior['counts']['inspected_primary_retained_with_limits']==37
    assert prior['counts']['open_original_not_inspected']==76
    write(BASE/'citation-chain-register.json',dict(original_census=ref(RECOVERY/'benchmark-v1/census-register.json',
        'Unchanged113 original candidates plus4 cross-cutting records'),original_inspected=37,original_unread=76,
        additional_leads=[dict(id='citation-chain-copilot-2504.13263',title=paper['title'],
            disposition='inspected_primary_retained_with_limits',source_keys=[s['integrated_citation_key'] for s in sources],
            primary_review=ref(BASE/'primary-review.json','Paper, static code and bounded rights review'),
            tasks=['business_translation','expert_evidence','diagram_construction','iid_discovery',
                'temporal_discovery','identification','reporting_monitoring','evaluation_cost'],
            next_action='Qualify protected graph semantics, matched scoring, temporal resampling and full environment/rights before runtime reuse.')],
        denominator_policy='One inspected citation-chain lead; no addition to or reclassification within original113 candidates.',closure=False))
    write(BASE/'omissions.json',dict(cutoff='2026-10-07',items=[
        dict(id='LA01-candidate-27',title='Agent-guided Causal Discovery with a Small Language Model',
            doi='10.1109/FLLM67465.2025.11391103',original_unavailable_in_attempts=True,
            finding='No genuine PDF supplied by recorded DOI/author/arXiv/metadata routes; technical claims withheld. No global unavailability assertion.',
            evidence=[ref(RECOVERY/'search-v8/search-v7-observations.json','Scoped unsuccessful acquisition routes')],
            next_action='Resume a distinct public author or publisher route if located; keep original unread.'),
        dict(id='copilot-runtime-and-rights',finding='No upstream run or full transitive rights/environment qualification; proposals remain conditional.',
            next_action='Freeze complete dependencies/assets and define semantic and matched scoring fixtures before controlled trial.'),
        dict(id='copilot-paper-experiment-binding',finding='Later code bytes are not established as the paper experiment code.',
            next_action='Locate an exact experiment release/configuration/raw result binding; do not attribute static findings to2025 experiments.')],
        global_blocker=False))
    write(BASE/'recovery-review.json',dict(status='pass',scope='Crash recovery and revised continuation plan review',
        controller_checks=[read(Path('/tmp/causal-run-check-20261017-recovery7.json'))['status'],
            read(Path('/tmp/causal-legacy-check-20261017-recovery7.json'))['status']],
        prior_reader=ref(ROOT/'docs/causal_proposal_benchmark_sources_reviewed_2026-10-17.pdf','Preserved1025-page reader'),
        plan=ref(RECOVERY/'copilot-plan.md','Reviewed crash continuation'),
        repair='Unbound exact witness changed .99/.01 to .95/.05 to match a stipulated20-result collection; no acquired evidence changed.',
        reference=ref(ROOT/'tools/copilot_reference_20261017.py','Reviewed finite reference'),
        evidence=[ref(BASE/'primary-review.json','Reviewed claim boundaries')],visual_acceptance=False))
    print(json.dumps(dict(validated_git_files=15,added_sources=4,additional_inspected_leads=1,
        original_inspected=37,original_unread=76,scholarly_paper_added=True,upstream_execution=False)))


if __name__=='__main__':
    main()
