#!/usr/bin/env python3
"""Preserve a bounded Java latent-IV source inspection, without runtime admission."""
import hashlib
import json
from pathlib import Path

import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-22/java-iv-rd-preflight-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = 'b89afaf952a4fd647df0d85b08102250106c6764'
OP = 'SW.CELL.iv_rd_design.Java'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Static inspection of four pinned source files; no downloaded code, native package, caller or test was executed.',
    'Tetrad latent measurement-model fitting is not evidence of generic external-IV or regression-discontinuity coverage.',
    'Three zero-hit repository queries do not establish absence of Java/JVM alternatives or exhaustive coverage.',
    'The source-level axis mismatch is not an observed package failure; caller reachability and concrete DataSet behavior remain unverified.',
    'The local covariance array has no outward assignment in this method; this does not show that the entire library lacks uncertainty APIs.',
    'EJML singular/near-singular behavior, callers, complete dependency rights and runtime compatibility remain unqualified.',
    'The method paper named in source comments is not admitted as an inspected scholarly source; no new theorem claim is made.']


def main():
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    prior = ROOT / 'docs/program/execution/2026-10-13/tetrad-reuse/primary-review.json'
    verify_bindings(read(prior))
    identity = read(ROOT / 'docs/program/repair-v12/work/SW01/tetrad-review.json')
    assert identity['commit'] == PIN
    assert identity['commit_date'] < '2026-10-07T15:59:59Z'
    tree_path = RAW / 'v12_sw2_tetrad_tree.json'
    tree = read(tree_path)
    assert tree['truncated'] is False
    entries = {x['path']: x for x in tree['tree']}
    selected = [dict(read(BASE / 'source-selection.json'), artifact='docs/literature/raw/exec22_javaiv_tetrad_tsls.txt')]
    selected += read(BASE / 'delegate-selection.json') + [read(BASE / 'backend-selection.json')]
    originals, paths = [], {}
    for item in selected:
        p = ROOT / item['artifact']
        body = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        assert blob == item['git_blob'] == entries[item['path']]['sha']
        assert len(body) == item['bytes'] == entries[item['path']]['size']
        receipt_path = p.with_suffix('.receipt.json')
        receipt = read(receipt_path)
        url = f'https://raw.githubusercontent.com/cmu-phil/tetrad/{PIN}/{item["path"]}'
        assert receipt['status'] == 'saved' and receipt['http_status'] == 200
        assert receipt['sha256'] == hashlib.sha256(body).hexdigest() and receipt['url'] == url
        originals.append(dict(repository_path=item['path'], git_blob=blob,
            source_identity=url, local_copy=ref(p, 'Authentic pinned primary source'),
            retrieval=ref(receipt_path, 'Acquisition date, URL and byte digest')))
        paths[Path(item['path']).name] = p
    specs = [
        ('Tsls.java', 1, 18, 'This source header grants GPL version 3 or later; distribution and dependency review remain necessary.'),
        ('Tsls.java', 33, 58, 'The documented target is a supplied pure latent measurement model; the class is package-private.'),
        ('Tsls.java', 90, 107, 'estimate creates a SemIm, estimates coefficients and returns it; getEstimatedSem returns that object.'),
        ('Tsls.java', 110, 165, 'Default fixed-loading selection uses lexicographic indicator names; explicit fixed-loading names are another branch.'),
        ('Tsls.java', 259, 294, 'Other measurements of latent parents supply instrument columns; an empty instrument collection skips that latent iteration.'),
        ('Tsls.java', 341, 364, 'Projection uses two direct inverses; the covariance helper is called only for a matching selected nodeName.'),
        ('Tsls.java', 377, 418, 'Measurement iteration excludes the current and fixed indicator, then skips when no other measures remain.'),
        ('Tsls.java', 421, 430, 'C is populated with getDouble(colIndex, i), reversing the declared case/variable argument order.'),
        ('Tsls.java', 441, 468, 'Nearby V and outcome reads use row then column; a scalar inverse projected norm supplies the loading estimate.'),
        ('Tsls.java', 473, 485, 'A residual-variance-scaled inverse is computed into a local array in a void helper, with no return or field assignment.'),
        ('DataSet.java', 122, 130, 'getDouble specifies row as case and column as variable.'),
        ('MatrixUtils.java', 226, 234, 'The array inverse delegates to Matrix.inverse().'),
        ('Matrix.java', 343, 362, 'inverse checks square/zero dimensions then calls CommonOps_DDRM.invert; no explicit rank or post-inversion finiteness check appears here.'),
        ('Matrix.java', 369, 420, 'Pseudoinverse and regularized/NaN-checking chooseInverse are distinct paths; the inspected Tsls calls use direct inverse.')]
    anchors = []
    for name, lo, hi, finding in specs:
        lines = paths[name].read_text().splitlines()
        assert hi <= len(lines)
        excerpt = '\n'.join(lines[lo - 1:hi])
        anchors.append(dict(source=ref(paths[name], 'Inspected original'), lines=[lo, hi],
            finding=finding, excerpt=excerpt,
            excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
    write(BASE / 'inspected-extracts.json', dict(anchors=anchors))
    searches = []
    for name in ['iv', '2sls', 'rd']:
        p = RAW / f'exec22_javaiv_search_{name}.json'
        d = read(p)
        receipt = p.with_suffix('.receipt.json')
        r = read(receipt)
        assert r['status'] == 'saved' and r['sha256'] == run.core.sha(p)
        searches.append(dict(query=r['url'], accessed_utc=r['accessed_utc'],
            total_count=d['total_count'], incomplete_results=d['incomplete_results'],
            original=ref(p, 'Repository-discovery response only'), receipt=ref(receipt, 'Saved query identity')))
    write(BASE / 'search-review.json', dict(searches=searches,
        cutoff='2026-10-07', limitation='Current repository search with creation-date restriction; not a historical index, content search, Maven census or absence certificate.',
        complementary_followup=['Maven artifact documentation and source archives',
            'JVM/Scala and econometrics terminology', 'Named candidate technical manuals and APIs']))
    write(BASE / 'plan-review.json', dict(status='pass_for_partial_source_scope',
        evidence=[ref(BASE / 'plan.md', 'Scope and failure checks')],
        findings=['Inspected the data-access delegate before recording the axis mismatch.',
            'Inspected the direct inverse delegate; retained EJML behavior as unresolved.',
            'Kept source-level, library-wide, method-theorem and runtime claims separate.',
            'Did not infer absent software from zero repository hits.']))
    write(BASE / 'source-audit.json', dict(cutoff='2026-10-07', sources=[dict(
        integrated_citation_key='exec22_java_latent_iv_preflight', kind='software_primary_source',
        title='Tetrad latent measurement-model Tsls and its data/inverse delegates',
        author='Ricardo Silva and Tetrad contributors', year=2026,
        source_identity=f'https://github.com/cmu-phil/tetrad/tree/{PIN}',
        version_date=f'7.6.11-SNAPSHOT; {PIN}; {identity["commit_date"]}',
        local_copy=ref(BASE / 'inspected-extracts.json', 'Verbatim source anchors'),
        primary_sources=originals, identity_evidence=[ref(tree_path, 'Complete pinned tree'), ref(prior, 'Existing license/environment review')],
        inspected_anchors=[dict(anchor=x['source']['path'] + ' lines ' + str(x['lines']), finding=x['finding']) for x in anchors],
        supported_claims=[x['finding'] for x in anchors], limitations=LIMITS)]))
    contract = dict(status='proposed_not_implemented', integration_allowed=False,
        scope='Candidate latent-measurement coefficient reference only; no generic credit-threshold effect is admitted.',
        inputs=['Explicit supplied graph, continuous variable order, case IDs, units and measurement-error assumptions.',
            'Record fixed indicator and loading normalization; changing indicator names must not silently change the estimand.',
            'Preserve structural and measurement stages separately, including branches skipped for insufficient auxiliary measurements.'],
        outputs=['Coefficient target and scale, full variable/case map, stage and fitted status.',
            'Distinguish a computed coefficient from qualified uncertainty; the inspected helper is not an uncertainty output API.',
            'Preserve numerical and missing-estimate states rather than treating default SemIm values as certified fits.'],
        admission_work=['Inspect actual public callers, initialization and concrete DataSet implementation.',
            'Resolve the swapped-axis source finding on non-square data before enabling this path.',
            'Qualify EJML and projected rank/conditioning, finite output, empty instruments and zero projected norms.',
            'Use prospectively fixed known-law latent measurement examples with explicit normalizations and independent numerical references.',
            'Assess GPL and dependency terms for the chosen distribution/bridge; an isolated process alone grants no rights clearance.'],
        banking_boundary='A latent repayment-propensity loading has a chosen measurement scale. A credit-eligibility threshold requires an explicitly different intervention/assignment target and RD diagnostics. A shared 2SLS label does not establish interchangeability.')
    write(BASE / 'conversion-contract.json', contract)
    omissions = [
        dict(item='Bollen 1996 original named by code comments', status='original_not_acquired_or_inspected',
            title='An alternative two stage least squares (2SLS) estimator for latent variable equations',
            identity_limit='Title, author, venue, year and pages reported by source comment; scholarly identity not independently authenticated here.',
            next_action='Acquire and inspect the genuine original PDF before citing its theorem or method guarantees; save under the required title/author/year name.'),
        dict(item='Generic IV/RD coverage', status='open', next_action='Search Maven/JVM and econometrics sources, inspect matched primary APIs and rights; retain weak-IV and discrete-running-variable limits.'),
        dict(item='Caller and numerical qualification', status='open', next_action='Inspect public callers, concrete DataSet, initialization and EJML 0.44 delegates; use registered native fixtures before reporting observed behavior.'),
        dict(item='Editorial integration', status='open', next_action='Integrate the bounded latent-IV distinction with the next substantive software release; do not describe it as present in the current PDF.')]
    write(BASE / 'omissions-register.json', dict(items=omissions, global_blocker=None))
    next_action = ('Complete complementary Java/JVM and Maven IV/RD discovery, inspect generic-IV/RD candidates and their rights, '
        'and resolve Tetrad caller/initialization/DataSet/EJML questions before any native admission. Acquire the Bollen original '
        'only if method claims are needed. Four pinned files are already inspected; do not repeat their acquisition. '
        'Integrate this bounded distinction with the next substantive software release; the Java coverage cell remains open.')
    evidence = [ref(BASE / n, 'Partial Java source review') for n in [
        'plan-review.json', 'source-audit.json', 'inspected-extracts.json', 'search-review.json',
        'conversion-contract.json', 'omissions-register.json']]
    write(BASE / 'review.json', dict(status='partial_progress', reviewer=dict(name='Codex author/coordinator', kind='author'),
        findings=['Four authentic pinned originals verified against Git blobs and HTTP receipts.',
            'DataSet contract authenticates the source-level swapped-axis finding.',
            'Scale selection, skipped measurements, unreturned local covariance and direct inverse paths have explicit boundaries.'],
        evidence=evidence, next_action=next_action, limitations=LIMITS, capabilities=[],
        integration_allowed=False, native_execution=False, whole_cell_pass=False))
    write(BASE / 'progress.json', dict(operation=OP, finding='Pinned latent-IV source inspected with three bounded repository searches; generic Java IV/RD coverage and native behavior remain open.',
        evidence=evidence + [ref(BASE / 'review.json', 'Author review'), ref(Path(__file__), 'Review generator')],
        next_action=next_action, yield_reason='Preserve partial source work and continue the independent lmtp reuse decision; this is not a completion or global blocker.',
        native_execution=False, capabilities=[]))
    verify_bindings(read(BASE / 'progress.json'))
    print(json.dumps(dict(operation=OP, originals=len(originals), anchors=len(anchors), status='partial_progress', integration_allowed=False)))


if __name__ == '__main__':
    main()
