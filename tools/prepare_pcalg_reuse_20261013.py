#!/usr/bin/env python3
"""Bind the inspected pcalg source, independent examples and successor design."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/pcalg-reuse'
RAW = ROOT / 'docs/literature/raw'


def ref(path, anchor):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'anchor': anchor}


def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    selection = json.loads((BASE / 'source-selection.json').read_text())
    verified = json.loads((BASE / 'blob-verification.json').read_text())
    files = {'description': 'DESCRIPTION', **json.loads((BASE / 'selected-files.json').read_text())}
    anchors = {
        'description': [(1, 16), (27, 36), (55, 57)],
        'implementation': [(114, 119), (280, 305), (339, 356), (1399, 1424),
                           (1608, 1660), (1673, 1675), (2113, 2124), (2161, 2166),
                           (2210, 2243), (2839, 2844), (2982, 3018), (3091, 3136), (3150, 3184)],
        'classes': [(36, 49)],
        'graph_validation': [(128, 190)],
        'namespace': [(1, 8), (28, 74), (91, 119)],
        'news': [(8, 13), (28, 32), (116, 121)],
        'pc_tests': [(17, 36), (38, 50), (183, 190)],
        'ida_tests': [(1, 42), (115, 160)],
        'makevars': [(1, 5)],
        'changelog': [(1, 9)],
    }
    records = []
    for key, upstream in files.items():
        path = RAW / f'exec13_pcalg_{key}.txt'
        lines = path.read_text().splitlines()
        ranges = [(a, min(b, len(lines))) for a, b in anchors[key]]
        assert all(a <= b for a, b in ranges), key
        proof = next(row for row in verified['files'] if row['upstream_path'] == upstream)
        receipt = path.with_suffix('.receipt.json')
        acquisition = json.loads(receipt.read_text())
        assert acquisition['sha256'] == ref(path, '')['sha256']
        records.append({'upstream_path': upstream,
            'source_identity': acquisition['url'], 'acquired_utc': acquisition['accessed_utc'],
            'local_copy': ref(path, '; '.join(f'lines {a}-{b}' for a, b in ranges)),
            'acquisition_receipt': ref(receipt, 'Bounded public read receipt'),
            'git_blob_sha1': proof['git_blob_sha1'], 'tree_identity_verified': True,
            'inspected_anchors': [{'lines': [a, b], 'text': '\n'.join(lines[a-1:b])} for a, b in ranges]})
    fields = {}
    for line in (RAW / 'exec13_pcalg_description.txt').read_text().splitlines():
        if line and not line[0].isspace():
            key, value = line.split(':', 1)
            fields[key] = value.strip()
        else:
            fields[key] += ' ' + line.strip()
    dependencies = {k: [v.strip() for v in fields[k].split(',')] for k in ['Depends', 'Imports', 'LinkingTo', 'Suggests']}
    assert len(dependencies['Imports']) == 17 and len(dependencies['LinkingTo']) == 3
    findings = [
        {'id': 'PC-CONFLICT', 'source': 'R/pcalg.R lines 1399-1424,1608-1640; manual121',
         'finding': 'solve.confl=false can overwrite incompatible directions. Use true with relaxed orientation, preserve 2/2 as an algorithmic conflict and refuse the effect stage. This does not license a latent-variable interpretation.'},
        {'id': 'CI-FALLBACK', 'source': 'R/pcalg.R lines 280-305,339-356,2839-2844; NAMESPACE29',
         'finding': 'pcorOrder uses corpcor pseudoinverse for larger conditioning sets, converts NA correlations to zero and clips; zStat converts NA to zero. Checking only returned p values or NAdelete=false cannot reveal an internally replaced value. Strict preflight excludes the illustrated singular/invalid-df inputs; no valid-input package failure claimed.'},
        {'id': 'MATRIX-DIRECTION', 'source': 'R/pcalg.R114-119; R/AllClasses.R40-48; manual12',
         'finding': 'pcAlgo matrix coercion uses wgtMatrix default transpose. amat.cpdag uses row endpoint: i->j is (0,1), whereas graph matrix uses (1,0). amat.pag uses the column endpoint and (2,3). Serialize the operation and convention explicitly.'},
        {'id': 'IDA-COERCION', 'source': 'R/pcalg.R3011-3017',
         'finding': 'ida converts every nonzero graph weight to1 before validation. Invalid type emits message() without an immediate stop. Reject conflict codes before binarization and enforce a separate strict CPDAG admission check.'},
        {'id': 'MULTISET', 'source': 'R/pcalg.R3091-3136,3150-3184; manual88-89; tests/test_ida.R115-160',
         'finding': 'Local parent-set and global DAG enumeration may have different multiplicities. Preserve raw results and method. Optimal adjustment can differ on sample covariance; do not impose identical finite-sample values across every method.'},
    ]
    primary = {'selection': selection, 'records': records, 'dependency_declarations': dependencies,
        'license': fields['License'], 'package_date': fields['Date'], 'needs_compilation': fields['NeedsCompilation'],
        'maintenance': {'mirror_history': 'Five selected mirror commits span 2.7-8 through2.7-12, latest2024-09-13.',
            'news': 'Inspected NEWS latest section is2.7-8; top of ChangeLog is2010. Neither is a complete2.7-12 changelog.',
            'tests': 'Source includes selected PC and IDA regression examples; some are gated by doExtras. No upstream or local package-test pass inferred.',
            'limits': 'No current upstream issue response, resolved dependency tree or support SLA measured.'},
        'findings': findings, 'scope': 'Pinned selected source review; not whole-package validation or runtime qualification'}
    write('primary-review.json', primary)
    # An independently written scalar expression trace, executed only with installed base R.
    proc = subprocess.run(['Rscript', '--vanilla', str(ROOT/'tools/pcalg_fallback_trace_20261013.R')],
                          capture_output=True, text=True, check=True, timeout=20)
    trace = json.loads(proc.stdout)
    trace['stderr'] = proc.stderr
    write('fallback-trace.json', trace)
    write('reproduction-review.json', {'status': 'pass',
        'exact_results': ref(BASE/'exact-results.json', 'Three equal-law SEMs, distinct multisets, units,54 independent roundtrips and36 transpose detection cases'),
        'exact_code': ref(ROOT/'tools/pcalg_reuse_examples_20261013.py', 'Exact rational reference, independent of pcalg'),
        'fallback_results': ref(BASE/'fallback-trace.json', 'Executed base-R scalar trace for explicitly invalid inputs'),
        'fallback_code': ref(ROOT/'tools/pcalg_fallback_trace_20261013.R', 'Project trace, no pcalg package load'),
        'limitations': ['No pcalg execution or real adapter roundtrip.', 'No empirical coverage, performance or live bank study.']})
    audit = {'cutoff': '2026-10-07', 'sources': [
        {'integrated_citation_key': 'exec13_pcalg_reuse_primary', 'kind': 'software_primary_sources',
         'title': 'pcalg 2.7-12 pinned PC, IDA and graph-conversion source',
         'author': 'pcalg contributors; CRAN source mirror', 'year': 2024,
         'source_identity': 'https://github.com/cran/pcalg',
         'version_date': f"2.7-12; package 2024-09-12; mirror commit {selection['revision']}; inspected 2026-10-13",
         'local_copy': ref(RAW/'exec13_pcalg_implementation.txt', 'Inspected PC/IDA, numerical and conversion passages'),
         'records': records,
         'revision_evidence': [ref(RAW/'exec13_pcalg_cutoff_commits.json', 'Cutoff-limited mirror history'),
                               ref(RAW/'exec13_pcalg_tree.json', 'Selected recursive Git tree'),
                               ref(RAW/'exec13_pcalg_repository.json', 'Mirror identity; current metadata not historical support evidence')],
         'source_review': ref(BASE/'primary-review.json', 'Dependencies, rights, maintenance and five source findings'),
         'inspected_anchors': [f["source"] for f in findings] + ['DESCRIPTION27-36; Makevars1-5; NEWS8-13; selected tests'],
         'supported_claims': [f['finding'] for f in findings] + ['Declared GPL>=2 and R>=3.5.0, seventeen imports, three LinkingTo dependencies and compiled BLAS/LAPACK route.'],
         'limits': ['Selected source inspection, not runtime behavior measurement.', 'Mirror recency is not a maintenance-quality measure.']},
        {'integrated_citation_key': 'exec13_pcalg_reuse_examples', 'kind': 'project_exact_example',
         'title': 'Exact graph, monetary-unit and numerical-boundary references for proposed R integration',
         'author': 'Causal proposal project', 'year': 2026,
         'source_identity': 'Project derivation and independently written scalar traces',
         'version_date': '2026-10-13; exact rational model and installed base-R arithmetic',
         'local_copy': ref(BASE/'exact-results.json', 'Exact model, multiplicity and encoding outputs'),
         'reproduction': ref(BASE/'reproduction-review.json', 'Executable code, outputs and claim limits'),
         'inspected_anchors': ['global_dag_multiset; local_parent_set_multiset; encoding cases; fallback trace'],
         'supported_claims': ['Three Gaussian SEMs share the stated covariance; effects0,0,12/25.',
                              'Local parent-set reference yields0,12/25; unit scaling gives4.8 currency/bp and120 currency/25bp.',
                              'Independent encoding fixtures detect transposes and show nonzero coercion erases conflict code.',
                              'Base-R scalar traces show invalid inputs can produce finite p=1 after the inspected fallbacks; positive-definite/df preflight rejects them.'],
         'limits': ['The package and its adapter were not executed.', 'These finite deterministic examples are not a sampling-law guarantee.']}
    ]}
    write('source-audit.json', audit)
    old = ROOT/'docs/program/comprehensive-v14/work/IN.DESIGN.R/adapter-contract.json'
    contract = copy.deepcopy(json.loads(old.read_text()))
    contract.update(contract_version='2.0-source-reviewed-proposal',
        supersedes=ref(old, 'Preserved accepted initial design; this successor corrects source-level assumptions'),
        source_evidence=ref(BASE/'source-audit.json', 'Pinned implementation and independent references'),
        pinned_revision=selection['revision'], status='reviewed_successor_design_not_implemented')
    pc = contract['request']['pc_gaussian']
    pc['configuration']['solve.confl'] = True
    pc['configuration']['indepTest'] = 'strict_gaussian_ci (project callback proposed; not yet implemented or engine-verified)'
    pc['configuration_note'] = ('Conservative relaxed PC with conflict-preserving orientation. Do not infer a CPDAG from the object class; conflicts and incomplete orientation require refusal of IDA. Stable.fast and its compiled CI route are excluded from this initial callback path.')
    pc['ci_wrapper'] = ('Compute conditional correlation and Fisher-Z from checked SPD submatrices with Cholesky solves. Reject rank loss, nonpositive residual variances, invalid df, nonfinite arithmetic, |r|>=1, or ill conditioning beyond a prospectively frozen tolerance. No pseudoinverse, NA-to-zero fallback, clipping, or silent regularization. Catch warnings and record diagnostics; require numeric scalar p in[0,1]. Compare to gaussCItest on well-conditioned fixtures before admission; deliberate failure behavior differs. This is a new project callback, not a claim that unmodified gaussCItest has these checks.')
    pc['constraints'] = ('Initial route excludes required/forbidden edges and background constraints. A separate provenance-bearing PDAG design must specify their compatibility, orientation closure and effect semantics before enabling them.')
    pc['validation'].append('Record condition-number/rank tolerances and check each used conditioning matrix. No claimed numerical equivalence from package documentation alone.')
    ida = contract['request']['ida_singleton']
    ida['method'] = 'Initial local singleton method, y.notparent=false, type=cpdag; global enumeration is a separately capped oracle. Optimal/multivariate/PDAG routes remain excluded until their separate finite-sample contracts are reviewed.'
    ida['admission'] = ('Inspect unmodified weighted graph matrix before any nonzero coercion. Require exact allowed codes, zero diagonal, named node alignment, matching covariance order and no2/2 conflict. Apply strict CPDAG and consistent-extension checks that abort on false/error, before calling ida. ida message() is not a refusal. Never repair by orienting unresolved edges or applying y.notparent=true.')
    contract['representation']['pc_graph'] = ('For as(pcAlgo,"matrix"), type=amat.cpdag, i->j is A[i,j]=0,A[j,i]=1. For as(pcAlgo@graph,"matrix"), the inspected implementation uses row-as-source graph adjacency, i->j=(1,0). wgtMatrix defaults to transpose=TRUE. Verify installed graph coercion on named fixtures and preserve pre-coercion weights; do not treat all nonzero entries as1. Reciprocal1/1 is undirected; reciprocal2/2 is a PC algorithmic conflict and requires refusal. Retain exact accessor and package revisions.')
    contract['representation']['validation'] += ' A PC conflict code2/2 and a PAG bidirected code2/2 have different scientific meanings; encode the origin, not just numbers.'
    contract['behavioral_oracles'] += [
        {'case': 'internal CI fallback', 'expected': 'Singular and invalid-df fixtures fail before numerical inference; returned finite p alone is insufficient. No regularized substitute.'},
        {'case': 'graph encoding and IDA coercion', 'expected': 'Named collider survives each accessor and all six node permutations. A transpose reverses directions and fails. Detect2/2 before ida normalizes nonzero weights.'},
        {'case': 'invalid graph message', 'expected': 'A non-CPDAG aborts before ida even if native function would merely emit a message.'},
        {'case': 'multiset multiplicity', 'expected': 'Three-DAG path gives global[0,0,.48], local[0,.48] in the exact model. Do not turn a2/3 zero frequency into a posterior probability.'}
    ]
    contract['executed_evidence'] = ref(BASE/'reproduction-review.json', 'Project references only; no R adapter')
    contract['design_review'] = {'reviewer': 'Codex author/coordinator', 'kind': 'author',
        'findings_resolved': [f['id'] for f in findings],
        'remaining_implementation_work': 'Local implementation is eligible under the pinned reuse decision. Pin and install a compatible R/dependency build; implement strict CI/conversion/admission; execute the full named, permutation, graph, numerical, unit and failure fixtures before claiming engine_executed or runtime qualification. Performance studies remain prospective.'}
    write('adapter-contract-v2.json', contract)
    print(json.dumps({'source_records': len(records), 'new_audited_citations': len(audit['sources']),
                      'successor_contract': '2.0-source-reviewed-proposal', 'runtime_executed': False}))


if __name__ == '__main__':
    main()
