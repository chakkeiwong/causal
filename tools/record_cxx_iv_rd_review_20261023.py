#!/usr/bin/env python3
"""Bind the inspected, cutoff-pinned C++ IV/RD source disposition."""
import hashlib
import json
from pathlib import Path

import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-23/cxx-iv-rd-v1'
OUT = ROOT / 'docs/program/comprehensive-v14/work/SW.CELL.iv_rd_design.Cxx/coverage-review.json'
read = lambda p: json.loads(p.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not OUT.exists()
    repo_rdd = read(ROOT / 'docs/literature/raw/exec23_cxxiv_rddsigma_repo.json')
    commit_rdd = read(ROOT / 'docs/literature/raw/exec23_cxxiv_rddsigma_commit.json')
    tree_rdd = read(ROOT / 'docs/literature/raw/exec23_cxxiv_rddsigma_tree.json')
    repo_sys = read(ROOT / 'docs/literature/raw/exec23_cxxiv_academic_iv_repo.json')
    commit_sys = read(ROOT / 'docs/literature/raw/exec23_cxxiv_academic_iv_commit.json')
    tree_sys = read(ROOT / 'docs/literature/raw/exec23_cxxiv_academic_iv_tree.json')
    repo_rdd = repo_rdd[0] if isinstance(repo_rdd, list) else repo_rdd
    repo_sys = repo_sys[0] if isinstance(repo_sys, list) else repo_sys
    commit_rdd = commit_rdd[0] if isinstance(commit_rdd, list) else commit_rdd
    commit_sys = commit_sys[0] if isinstance(commit_sys, list) else commit_sys
    assert commit_rdd['sha'] == '2d1cdaaa34a593892bb729df1ae4cccd21ec3022'
    assert commit_sys['sha'] == 'f75d83efeca93b5f376b94e7d7d1e06ff564a72d'
    assert not tree_rdd['truncated'] and not tree_sys['truncated']

    rdd_files = [
        ('exec23_cxxiv_rddsigma_file_0.txt', 'DESCRIPTION', 'Package identity,0.2.0,MIT+file declaration,C++11/RcppArmadillo linkage.'),
        ('exec23_cxxiv_rddsigma_file_1.txt', 'LICENSE', 'Only YEAR and COPYRIGHT HOLDER template fields; not the full MIT grant.'),
        ('exec23_cxxiv_rddsigma_file_2.txt', 'README.md', 'Methods estimate running-variable measurement error, not an outcome treatment effect.'),
        ('exec23_cxxiv_rddsigma_file_3.txt', 'R/estimate_sigma.R', 'Inputs, paired missing-row deletion, random initializer path and dispatch.'),
        ('exec23_cxxiv_rddsigma_extra_0.txt', 'R/emparam.R', 'Gaussian latent variable; Gaussian/Laplace error, defaults and returned estimate object.'),
        ('exec23_cxxiv_rddsigma_file_4.txt', 'R/em_gauss_gauss.R', 'EM likelihood, NA filtering, criteria and returned convergence.'),
        ('exec23_cxxiv_rddsigma_file_5.txt', 'R/tsgauss.R', 'sd_w formula, random initialization, Brent bounds and convergence field.'),
        ('exec23_cxxiv_rddsigma_file_6.txt', 'R/gen_data.R', 'Synthetic data generator, not real causal evidence.'),
        ('exec23_cxxiv_rddsigma_file_7.txt', 'man/estimate_sigma.Rd', 'Documented estimand, distribution scope and defaults.'),
        ('exec23_cxxiv_rddsigma_file_8.txt', 'src/em-gauss-gauss.cpp', 'Native EM integration and result fields/convergence.'),
        ('exec23_cxxiv_rddsigma_extra_2.txt', 'src/em-gauss-lap.cpp', 'Native Gaussian/Laplace EM alternative and returned convergence.'),
        ('exec23_cxxiv_rddsigma_file_9.txt', 'src/integral.cpp', 'Adaptive quadrature implementation and termination paths.'),
        ('exec23_cxxiv_rddsigma_file_10.txt', 'src/integral.h', 'Integration algorithms, improper-integral transform and recursion failure statement.'),
        ('exec23_cxxiv_rddsigma_extra_1.txt', 'R/rddsigma-s3method.R', 'Summary reports convergence and parameterization.'),
        ('exec23_cxxiv_rddsigma_extra_3.txt', 'src/RcppExports.cpp', 'Rcpp exported helper boundary; not a standalone C++ API.'),
        ('exec23_cxxiv_rddsigma_file_11.txt', 'tests/testthat/test-estimate_sigma.R', 'Small interface test; no identified statistical or native qualification suite.'),
    ]
    sys_files = [
        ('exec23_cxxiv_academic_iv_file_0.txt', 'README.md', 'Project states recursive LS/IV dynamic transfer-function system identification; Doxygen TODO.'),
        ('exec23_cxxiv_academic_iv_header_2.txt', 'source/matrix_operations.hpp', 'USER_DATATYPE is long double.'),
        ('exec23_cxxiv_academic_iv_header_0.txt', 'source/system_identification.hpp', 'RLS/RIV method constants and public recursive interface.'),
        ('exec23_cxxiv_academic_iv_file_1.txt', 'source/system_identification.cpp', 'Lag buffers, RIV instruments, recursive updates and 0.0001 denominator substitution.'),
        ('exec23_cxxiv_academic_iv_header_1.txt', 'source/rank_identification.hpp', 'Fixed-capacity/default rank API and allocation parameters.'),
        ('exec23_cxxiv_academic_iv_file_2.txt', 'source/rank_identification.cpp', 'Default maximum rank/sample count, AIC-like selection and post-write overflow check.'),
        ('exec23_cxxiv_academic_iv_file_3.txt', 'source/matrix_operations.cpp', 'Manual allocation/indexing and arithmetic implementation.'),
    ]

    sources = []
    for fname, source_path, finding in rdd_files:
        path = ROOT / 'docs/literature/raw' / fname
        source = dict(product='rddsigma', source_identity=dict(repository=repo_rdd['html_url'],
            pinned_commit=commit_rdd['sha'], commit_date=commit_rdd['commit']['committer']['date'],
            path=source_path), version_date='Package 0.2.0; commit 2025-06-06; cutoff 2026-10-07',
            local_copy=dict(path=str(path.relative_to(ROOT)), sha256=sha(path), anchor=finding),
            role='inspected_pinned_primary_technical_text', supported_claims=[finding],
            scope_limit='Source inspection only; no build, run, statistical qualification or causal effect claim.')
        sources.append(source)
    for fname, source_path, finding in sys_files:
        path = ROOT / 'docs/literature/raw' / fname
        source = dict(product='academic dynamic-system identification project', source_identity=dict(
            repository=repo_sys['html_url'], pinned_commit=commit_sys['sha'],
            commit_date=commit_sys['commit']['committer']['date'], path=source_path),
            version_date='Commit 2016-10-15; cutoff 2026-10-07',
            local_copy=dict(path=str(path.relative_to(ROOT)), sha256=sha(path), anchor=finding),
            role='inspected_pinned_primary_technical_text', supported_claims=[finding],
            scope_limit='Adjacent dynamic-system code; no causal estimand, build, run or redistribution permission.')
        sources.append(source)

    identity_evidence = []
    for key in ['exec23_cxxiv_rddsigma_repo', 'exec23_cxxiv_rddsigma_commit', 'exec23_cxxiv_rddsigma_tree',
                'exec23_cxxiv_academic_iv_repo', 'exec23_cxxiv_academic_iv_commit', 'exec23_cxxiv_academic_iv_tree']:
        p = ROOT / 'docs/literature/raw' / f'{key}.json'
        identity_evidence.append(ref(p, 'Authenticated bounded repository identity or pinned complete tree'))
    searches = []
    query_manifest = read(BASE / 'search-manifest.json')['requests']
    for i in range(4):
        p = ROOT / 'docs/literature/raw' / f'exec23_cxxiv_search_{i}.json'
        data = read(p)
        searches.append(dict(query=query_manifest[i]['url'],
            total_count=data.get('total_count'), returned=len(data.get('items', [])),
            source=ref(p, f'Bounded GitHub metadata search {i}; discovery only')))
    assert [x['total_count'] for x in searches] == [1, 1, 0, 0]

    audit_path = BASE / 'source-audit.json'
    write(audit_path, dict(cutoff='2026-10-07T15:59:59Z', source_records=sources,
        search_scope=dict(route='GitHub repository metadata API only', max_results_per_query=30,
            four_queries=True, keywords=['instrumental variables C++', 'regression discontinuity C++',
                'two stage least squares C++', 'instrumental forest C++'],
            search_limit='Creation-date filter; repository descriptions may omit methods; no source-code registry, paper, non-English or universal search.'),
        candidates=[dict(id='rddsigma', disposition='retain_as_adjacent_R_Rcpp_measurement_error_component',
            not_causal_effect_estimator=True, runtime_executed=False),
            dict(id='academic_dynamic_iv', disposition='exclude_from_causal_IV_RD_estimators_retain_as_adjacent_system_identification',
                 license_unresolved=True, runtime_executed=False)],
        new_scholarly_works=0, all_technical_claims_have_local_originals=True))

    derivation = dict(status='static_source_algebra_only',
        sample_sd='sqrt(Q/(n-1))', code_sd='sqrt(Q/(n-1))*(n-1)/n',
        code_sd_squared='Q*(n-1)/n^2', gaussian_ml_sd='sqrt(Q/n)',
        code_to_ml_sd_ratio='sqrt((n-1)/n)',
        n2_example=dict(Q='1', sample_sd='1', code_sd='1/2', gaussian_ml_sd='1/sqrt(2)'),
        claim='The source expression differs from the Gaussian maximum-likelihood standard deviation described by its adjacent comment.',
        unmeasured_effect='No package output or downstream treatment-effect bias is asserted.')
    write(BASE / 'static-derivation.json', derivation)

    review = dict(schema_version='1.0', operation='SW.CELL.iv_rd_design.Cxx',
        status='pass_for_bounded_source_coverage_with_candidate_exclusions',
        reviewer=dict(name='Codex author/coordinator', kind='author'), cutoff='2026-10-07',
        search_results=searches, candidate_dispositions=[
            dict(candidate='kota7/rddsigma', revision=commit_rdd['sha'],
                disposition='adjacent R/Rcpp measurement-error parameter estimator; not a causal RD effect estimator',
                source_supported_features=['sharp threshold assignment with error in the running variable',
                    'two-step Gaussian and EM Gaussian/Gaussian or Gaussian/Laplace error models'],
                gaps=['no outcome input or RD discontinuity effect', 'no C++ standalone interface',
                    'R package removes paired missing rows and can draw random initial sigma',
                    'complete executable license grant is not present in the selected LICENSE template file',
                    'source formula for Gaussian ML sd_w requires independent numerical comparison']),
            dict(candidate='PatrykKot dynamic-system project', revision=commit_sys['sha'],
                disposition='exclude_as_causal_IV_RD_method; adjacent recursive system identification only',
                findings=['RIV instruments are lagged system inputs; no banking causal estimand or exclusion/monotonicity contract.',
                    'zero update denominator is replaced by 0.0001 in RLS and RIV.',
                    'rank buffer capacity check follows the write and permits an index equal to capacity.',
                    'metadata declares no license and the full tree contains no license file.'],
                native_execution=False)],
        source_audit=ref(audit_path, 'Sixteen rddsigma and seven system-project technical originals'),
        derived_check=ref(BASE / 'static-derivation.json', 'Formula comparison; no execution'),
        findings=['The two returned candidates have distinct, inspected primary source identities and date/revision pins.',
            'A relevant C++ Rcpp measurement-error component is not misclassified as an RD causal effect estimator.',
            'The academic RIV acronym is not treated as evidence of econometric causal IV functionality.',
            'Search coverage is bounded and stated; no market-wide absence inference is made.'],
        limitations=['No candidate compiled or executed; no native correctness, memory-safety or statistical qualification.',
            'The GitHub metadata search is not an exhaustive registry or full market census.',
            'No license distribution permission is inferred for either source; academic project has no license record.',
            'Commercial C++ and non-C++ IV/RD coverage are separate cells.'],
        integration_allowed=False, runtime_executed=False, distribution_cleared=False,
        revisit_trigger='A standalone causal IV/RD C++ package with an authenticated cutoff source, or a supported proposal for separately qualifying rddsigma as an auxiliary measurement-error module.')
    verify_bindings(review)
    write(BASE / 'coverage-review.json', review)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write(OUT, review)

    state = run.core.read(ROOT, run.core.STATE)
    graph, merged, _ = run.combined(ROOT, state)
    node = run.ledger.operation(graph, 'SW.CELL.iv_rd_design.Cxx')
    assert 'SW.CELL.iv_rd_design.Cxx' not in merged['execution_program']['results']
    assert not run.ledger.blockers(merged, node)
    evidence = [ref(BASE / 'coverage-review.json', 'Criterion-specific candidate source review'),
        ref(OUT, 'Required coverage review'), ref(audit_path, 'Pinned technical source audit'),
        ref(BASE / 'static-derivation.json', 'Reproducible static formula comparison'),
        ref(BASE / 'candidate-review.md', 'Connected source-grounded candidate dispositions'),
        ref(BASE / 'plan.md', 'Bounded search plan'), ref(Path(__file__), 'Coverage review and receipt validator')]
    evidence += identity_evidence + [q['source'] for q in searches]
    limitations = review['limitations']
    receipt = run.ledger.receipt_template(node)
    receipt.update(outcome='pass', execution='performed',
        scope='Bounded, cutoff-pinned C++ IV/RD candidate discovery and technical-source disposition. No native qualification.',
        reviewer=review['reviewer'], limitations=limitations,
        original_gap_qualification=False, capabilities=[], nonexecution_reason='',
        revisit_trigger=review['revisit_trigger'], outputs=[ref(OUT, 'Required source-coverage disposition')],
        criteria=[dict(index=i, verdict='pass', finding=review['findings'][i],
            evidence=evidence+[ref(BASE / 'coverage-review.json', 'Individual review')]) for i in range(3)])
    run.validate_receipt(ROOT, merged, node, receipt, len(state['execution_program']['turns']))
    write(BASE / 'operation-receipt.json', receipt)
    print(json.dumps(dict(operation=node['id'], source_records=len(sources), search_counts=[1, 1, 0, 0],
        candidates=2, runtime_executed=False, outcome='pass_for_bounded_coverage')))


if __name__ == '__main__':
    main()
