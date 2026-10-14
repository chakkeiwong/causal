#!/usr/bin/env python3
"""Bind the inspected Java-discovery sources and finite candidate census."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/java-discovery'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return {'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2) + '\n')


def fetched(stem, anchor, inspected=True):
    p = RAW / ('v12_exec13_java_' + stem + '.receipt.json')
    r = json.loads(p.read_text())
    assert r['status'] == 'saved'
    bound = ref(r['path'], anchor)
    assert bound['sha256'] == r['sha256']
    return {'local_copy': bound, 'source_identity': r['url'], 'accessed_utc': r['accessed_utc'],
            'receipt': ref(p, 'Collector HTTP status, identity and byte hash'),
            'role': 'inspected_primary_technical_text' if inspected else 'identity_or_navigation_only'}


def main():
    # Descriptions below name actually read branches. Downloaded-only files never
    # become technical support merely by appearing in a repository tree.
    groups = [
        ('tetrad', 'Tetrad Java discovery source and configuration', 'cmu-phil/tetrad',
         'b89afaf952a4fd647df0d85b08102250106c6764; 2026-09-22; 7.6.11-SNAPSHOT', 2026,
         [('tetrad_fisherz', 'lines137-198 missing policies; 362-383 singularity; 429-465 df and test'),
          ('tetrad_fas', 'lines280-410 complete skeleton, depth and stable branch'),
          ('tetrad_testpc', 'lines59-95 oracle fixtures; 150-154 regression caveat; 165-192 MsepTest'),
          ('tetrad_fisherz_test', 'lines50-116 seeded500-row chain/collider assertions'),
          ('tetrad_fges', 'lines185-203 thread initialization; 229-262 search; 1193-1196 setter'),
          ('tetrad_sembic', 'lines53-55 IID linear Gaussian BIC; 123-127 penalty default'),
          ('tetrad_edges', 'lines57-68 directedEdge tail at source and arrow at target'),
          ('tetrad_endpoint', 'Endpoint enum distinguishes tail, arrow and circle'),
          ('tetrad_directlingam', 'lines94-104 score constructor; 119-147 entropy ingredient; 164-196 search'),
          ('tetrad_dagma', 'lines125-150 covariance and defaults; 542-566 threshold, orientation and CPDAG')],
         ['PC and CI configuration are distinct from graph truth or calibration.',
          'checkIndependence converts singular-matrix failure to dependent with p=0; getResult propagates the exception.',
          'DirectLingam helper uses a standardized second moment and an odd moment; project diagnostic is narrower than whole-algorithm parity.',
          'Dagma toGraph maps W[i,j] to i->j, thresholds abs weights and optionally returns CPDAG.',
          'FGES field/constructor initially uses one worker, although its comment says all processors.'],
         ['No compiled Java, dependency-resolution, throughput or statistical calibration run.',
          'Root compiler21 and bridge README25+ remain a real environment question.',
          'GPL distribution obligations require a scoped integration review.']),
        ('weka', 'Weka Bayesian classifier and structure-search sources from the discontinued mirror', 'Waikato/weka-3.8',
         '04804ccd6dff03534cbf3f2a71a35c73eef24fe8; 2022-08-10; 3.8.7-SNAPSHOT mirror', 2022,
         [('weka_bayesnet', 'lines52-53 filter imports; 158 K2 default; 197-276 data preparation'),
          ('weka_search', 'lines55-68 parent/initialization defaults; 317-330 class arrows and correction'),
          ('weka_ci', 'lines75-108 local score comparison with/without parent'),
          ('weka_ics', 'line98 max cardinality2; skeleton search and optional classifier correction'),
          ('weka_localscore', 'line107 BAYES score default; calcNodeScore dispatch'),
          ('weka_test', 'lines35-49 generic classifier-test inheritance and default instance'),
          ('weka_pom', 'line8 snapshot; lines90-100 Java8 profile; GPL license declaration'),
          ('weka_license', 'GNU GPL version3 full license text')],
         ['Default BayesNet uses K2, supervised discretization, replacement of missing values and removal of missing-class rows.',
          'Naive-Bayes initialization points class to other attributes; this is a classifier factorization.',
          'The inspected CI method is a score comparison, not a Fisher-Z alpha test.',
          'The mirrored source and generic classifier tests do not establish current2026 causal capability.'],
         ['Official mirror README directs readers to the Waikato Git service; current official release not acquired.',
          'No Java build or causal calibration run; no unrestricted relicensing inferred.']),
        ('aitiotita', 'Aitiotita Java PC source, configuration and license', 'jdellert/aitiotita',
         '8a8e566a87186de4935e644cec0fa80e6d456fd7; 2023-09-09; version1.0', 2023,
         [('aitiotita_readme', 'Java PC/FCI purpose and interface description'),
          ('aitiotita_pc', 'lines34-43 configuration; 69-115 all-neighbour shortcut; 120-214 subset search'),
          ('aitiotita_pom', 'lines7-18 version1.0, Java8, JUnit3.8.1'),
          ('aitiotita_license', 'Apache License version2.0 full text')],
         ['Separate correlation/arrow components and graph constraints are constructor inputs.',
          'At depth>2, dependence given all neighbours marks a link undeletable before smaller subsets are tested.',
          'Exact Gaussian derivation disproves conditioning-monotonicity as a general justification for that shortcut.'],
         ['Delegated PartialCorrelation, orientation implementation and test bodies were not acquired in this round.',
          'No compiled end-to-end failure or full correctness result is asserted.']),
        ('banjo', 'Banjo derivative: greedy-search source, restrictive notice and application description', 'daniel-315/slingshot-modified-banjo',
         '0c42b02ac2b452fc782ea8cff4c92f1cd11f8e6b; 2026-08-13; derivative, not an official release', 2026,
         [('banjo_readme', 'lines1-48 application, gold-standard-selected genes, pseudotime, lag1 and limits'),
          ('banjo_greedy', 'lines1-17 rights notice; 63-153 time/iteration/restart termination')],
         ['The selected derivative describes a gene-network application using inferred pseudotime; no banking result is inferred.',
          'Source notice says non-commercial use may be licensed and commercial use requires contact with Duke/Hartemink.',
          'Pinned source contains greedy-search termination controls.'],
         ['Original official Banjo release/full terms and derivative differences remain unverified.',
          'Settings.java is acquired but does not establish a fully inspected evaluator/cycle-check/test path.',
          'Public repository visibility does not authorize commercial reuse.'])]
    sources = []
    for key, title, owner, version, year, files, claims, limits in groups:
        records = [fetched(stem, anchor) for stem, anchor in files]
        s = {'integrated_citation_key': 'exec13_java_' + key, 'kind': 'software_primary_sources',
             'title': title, 'author': owner, 'year': year, 'source_identity': 'https://github.com/' + owner,
             'version_date': version + '; accessed2026-10-13 Asia/Shanghai',
             'local_copy': records[0]['local_copy'], 'records': records,
             'inspected_anchors': [r['local_copy']['anchor'] for r in records],
             'supported_claims': claims, 'limits': limits}
        if key == 'tetrad':
            inherited = json.loads((ROOT / 'docs/program/repair-v12/work/SW01/tetrad-review.json').read_text())
            s['inherited_primary_records'] = inherited['records']
            s['inherited_review'] = ref('docs/program/repair-v12/work/SW01/tetrad-review.json', 'Pinned PC assumptions, endpoints, compiler and license source review')
        if key == 'weka':
            s['official_mirror_notice'] = ref('docs/program/repair-v12/work/SW01/extracted/pinned-weka-README.md', 'lines1-9 mirror discontinued and official host')
            s['mirror_notice_receipt'] = ref('docs/literature/raw/v12_sw_pinned_readme_weka.receipt.json', 'Pinned mirror README acquisition identity')
            s['commit_identity'] = ref('docs/literature/raw/v12_sw_cutoff_commit_weka.json', 'Cutoff commit identity/date only')
        sources.append(s)

    observations = []
    selected = {}
    for stem in ['search_causal', 'search_banjo', 'search_banjo_author', 'search_banjo_name', 'search_banjo_readme']:
        record = fetched(stem, 'total_count, incomplete_results, bounded items and repository identities', False)
        d = json.loads((ROOT / record['local_copy']['path']).read_text())
        observations.append({'query': stem, 'total_count': d['total_count'], 'returned': len(d['items']),
                             'incomplete_results': d.get('incomplete_results'), 'evidence': record})
        for item in d['items']:
            selected[item['full_name']] = {k: item.get(k) for k in ['full_name', 'description', 'created_at', 'html_url']}
    dispositions = []
    core_candidates = {
        'cmu-phil/tetrad': ('primary_source_inspected', 'Preferred Java bridge candidate for PC/FGES; all graph/error/configuration conformance remains proposed.'),
        'Waikato/weka-3.8': ('stale_primary_mirror_inspected', 'Retain predictive baseline; reject automatic causal interpretation; acquire current official release.'),
        'jdellert/aitiotita': ('partial_primary_source_inspected', 'Hold direct adoption pending shortcut and delegated implementation review.'),
        'daniel-315/slingshot-modified-banjo': ('restricted_derivative_inspected', 'Hold reuse pending official release, license and derivative comparison.'),
        'microsoft/reliableAI': ('umbrella_candidate_unresolved', 'README/tree navigation identifies Java blip and Spot paths; inspect nested engine and license next.'),
        'kvb2univpitt/causal-experiment': ('experiment_collection', 'Do not count a collection README as an independent engine.'),
        'tyler-lovelace1/tetrad-censored': ('derivative_unresolved', 'Empty pinned README does not establish changes or lack of capability.'),
        'bd2kccd/tetrad': ('historical_lineage_candidate', 'Historical Tetrad description; avoid double counting pending lineage check.')}
    for name in sorted(set(selected) | set(core_candidates)):
        item = selected.get(name, {'full_name': name})
        if name in core_candidates:
            status, decision = core_candidates[name]
        elif item.get('created_at', '') > '2026-10-07T15:59:59Z':
            status, decision = 'excluded_after_cutoff', 'Created after cutoff; excluded from historical corpus without inferring prior absence.'
        else:
            status, decision = 'name_collision_or_unresolved_metadata', 'Banjo name-only result: no causal-engine claim; bounded README-focused search is not exhaustive.'
        dispositions.append({**item, 'status': status, 'decision': decision})
    reports = sorted((ROOT / 'docs/program/repair-v12/source-collection').glob('java-20261013-batch*/report.json'))
    all_receipts = [r for p in reports for r in json.loads(p.read_text())['receipts']]
    acquisition = {'requests': sum(json.loads(p.read_text())['requests'] for p in reports),
                   'saved': sum(r['status'] == 'saved' for r in all_receipts),
                   'failed': [r for r in all_receipts if r['status'] != 'saved'],
                   'reports': [ref(p, 'Completed bounded batch and restored collector manifest') for p in reports]}
    assert acquisition['requests'] == 48 and acquisition['saved'] == 47 and len(acquisition['failed']) == 1
    write('candidate-register.json', {'cutoff': '2026-10-07', 'queries': observations,
          'candidates': dispositions, 'acquisition': acquisition,
          'coverage_limit': 'Five metadata queries, at most12 returned per query and48 GETs; metadata only discovers identities. The33-hit Banjo-name query returned12. No ecosystem-completeness or absence claim.'})
    write('omissions-register.json', {'essential_gaps': [
        {'id': 'JAVA01', 'candidate': 'Weka', 'gap': 'Current official Waikato release and complete causal-use configuration/tests', 'next_action': 'Acquire an official pre-cutoff source archive and compare BayesNet, search, filters and tests to this stale mirror; if inaccessible, retain a release-scoped comparison only.'},
        {'id': 'JAVA02', 'candidate': 'Banjo', 'gap': 'Official original release, full license, scoring/cycle-check/test implementation and derivative diff', 'next_action': 'Find original Duke distribution/license through a new bounded primary-source protocol; compare pinned derivative; exclude redistribution until rights are established.'},
        {'id': 'JAVA03', 'candidate': 'Aitiotita', 'gap': 'PartialCorrelation, arrow rules, graph mutators and actual test bodies', 'next_action': 'Acquire delegated sources and compare oracle execution with the six-node conditioning counterexample; isolate the shortcut or restrict the supported graph class.'},
        {'id': 'JAVA04', 'candidate': 'reliableAI nested blip/Spot; Tetrad variants', 'gap': 'Nested engine identity/rights and derivative alias resolution', 'next_action': 'Inspect nested license, algorithm and tests at pinned commits; compare Tetrad lineage rather than double count.'}],
        'later_prototype_work': ['Java dependency/build qualification', 'Graph endpoint and signed-coefficient roundtrip', 'CI calibration, singularity and missingness trials', 'DirectLingam helper/reference parity and standardized-unit sensitivity', 'Measured scaling with declared hardware and failure counts'],
        'scholarly_limit': 'No new DirectLiNGAM scholarly original acquired in this bounded round; software source supports only implementation observations, not a fresh literature survey.',
        'global_blocker': False})
    # Verify local raw blobs against navigation entries. Comparing an API tree
    # response sha directly to a commit object's tree sha was an inherited error:
    # the saved response identifies the supplied revision. Do not invent a later
    # tree merely from that mismatch. Preserve the distinction and blob evidence.
    blobs = []
    for stem in ['banjo', 'aitiotita', 'weka', 'reliableai']:
        treefile = RAW / ('v12_exec13_java_' + stem + '_tree.json')
        tree = json.loads(treefile.read_text()); bypath = {e['path']: e for e in tree['tree']}
        for p in sorted(RAW.glob('v12_exec13_java_' + stem + '_*.receipt.json')):
            r = json.loads(p.read_text())
            if r['status'] != 'saved' or 'raw.githubusercontent.com' not in r['url']:
                continue
            path = r['url'].split('/', 6)[6]; body = (ROOT / r['path']).read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            blobs.append({'file': r['path'], 'tree_path': path, 'git_blob_sha1': blob,
                          'matches_saved_entry': blob == bypath.get(path, {}).get('sha')})
    assert all(b['matches_saved_entry'] for b in blobs)
    write('identity-review.json', {'status': 'pass_for_selected_pinned_bytes', 'blob_checks': blobs,
          'correction': 'The inherited summary called Banjo HEAD navigation a later mismatched tree. Saved response sha equals the selected cutoff commit, and all three pinned raw-file blob identities match saved entries. A commit tree-object sha is a different identity; that comparison alone cannot establish a later tree. Keep metadata as navigation and make claims from exact pinned technical URLs.',
          'evidence': [ref(RAW / 'v12_exec13_java_banjo_tree.json', 'Saved navigation sha and file blob entries'),
                       ref(RAW / 'v12_exec13_java_banjo_commit.json', 'Selected cutoff commit and tree-object identities')]})
    sources.append({'integrated_citation_key': 'exec13_java_examples', 'kind': 'project_derivation',
                    'title': 'Exact funding-orientation, conditioning and symmetric-moment diagnostics',
                    'author': 'Causal banking research project', 'year': 2026,
                    'source_identity': 'tools/java_discovery_examples_20261013.py',
                    'version_date': '2026-10-13; exact project derivations; zero random draws',
                    'local_copy': ref('tools/java_discovery_examples_20261013.py', 'funding, conditioning, symmetric_moments'),
                    'executed_results': ref(BASE / 'exact-results.json', 'Three executed project diagnostics'),
                    'inspected_anchors': ['funding: surgical intervention and transposed graph', 'conditioning:11 smaller subsets plus separator and collider', 'symmetric_moments: second/odd moments versus fourth moments'],
                    'supported_claims': ['Correct funding response cost=-3/50; transposed cost=0; absolute coefficients cost=13/50.', 'Conditional covariance givenZ1,Z2,Z3 is0; addingC gives-1/3 and partial correlation-1/2.', 'Two symmetric samples have equal helper ingredients despite different fourth moments.'],
                    'limits': ['Stipulated model units, no bank estimates, package execution, parity or runtime claims.']})
    write('source-audit.json', {'cutoff': '2026-10-07', 'sources': sources,
          'candidate_register': ref(BASE / 'candidate-register.json', 'Finite query results and individual dispositions'),
          'omissions': ref(BASE / 'omissions-register.json', 'Essential coverage gaps and exact continuation'),
          'identity_review': ref(BASE / 'identity-review.json', 'Selected byte identities and recovery correction')})
    print(json.dumps({'status': 'written', 'source_groups': len(sources), 'candidate_dispositions': len(dispositions),
                      'requests': 48, 'coverage_complete': False}))


if __name__ == '__main__':
    main()
