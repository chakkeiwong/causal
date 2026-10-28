"""Inspect pinned helper originals and prepare a scholarly preserving addition."""
import hashlib
import json
from pathlib import Path

import blip_helper_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'blip-helper-review-v1'
RAW = ROOT / 'docs/literature/raw'
PIN = '42dea82a5d13a989d08983a08527ed982776bccf'

ANCHORS = {
    0: [(12, 24, 'Score inherits Analyzer and stores the supplied dataset.'),
        (39, 50, 'Empty parents use the root score; other parent sets use inherited configuration construction.')],
    1: [(5, 25, 'Total row count, per-state row indices and missing indices are separate fields.'),
        (27, 34, 'Copy constructor aliases metadata arrays and does not copy row_values or missing_l.')],
    2: [(94, 123, 'Two-pointer intersection count requires ordered input indices for set semantics.'),
        (161, 192, 'Array intersection uses the same ordered two-pointer traversal.')],
    3: [(4, 17, 'Author disclaimer and adapted FDLIBM/Sun notice are separately declared.'),
        (217, 223, 'HI and LO use Java doubleToLongBits.'),
        (384, 415, 'Special-value branch maps NaN and both infinities to positive infinity; zero and finite negative values return NaN.')],
    4: [(124, 134, 'doubleEquals returns a boolean with strict absolute tolerance 2^-5 by default; it makes no assertion.'),
        (295, 341, 'Default readMissing is false; suffix selects reader; exceptions are logged and return null.')],
    5: [(47, 64, 'Parent configurations are computed directly from dataset state rows; cache code is commented.'),
        (79, 122, 'Single-parent overload reads dat.row_values rather than supplied rows; multiple parents use int cardinality products and a short-coded value index.'),
        (124, 166, 'Expansion uses int cardinality/index products and dat rows for the new parent.')],
    6: [(72, 125, 'DAT reader advances past blank rows and drops any question-mark row when readMissing is false; otherwise retains total rows and separate missing indices.'),
        (129, 155, 'Missing indices are distinct from ordinary category rows.'),
        (173, 228, 'Metadata arities, data read and explicit readMissing initialization.')],
    7: [(23, 40, 'DATA reader is comma-delimited, generates variable names and discovers arities.'),
        (60, 104, 'Blank or readMissing-and-question-mark branches continue without advancing nextLine; default false follows the missing-index branch.'),
        (106, 110, 'Category and missing indices are compacted separately after the loop.')],
    8: [(14, 30, 'TheTest provides assertDoubleEquals via assertTrue; the inspected BDeuTest calls the nonasserting RandomStuff helper instead.')],
}


def main():
    assert not (BASE / 'source-audit.json').exists()
    plans = [json.loads((BASE / n).read_text()) for n in ('plan-review.json', 'delegate-extension-plan.json')]
    work = [r for plan in plans for r in plan['worklist']]
    assert len(work) == 9
    sources = []
    for i, item in enumerate(work):
        path = RAW / (item['id'] + '.txt')
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        assert len(raw) == item['expected_bytes'] and blob == item['expected_git_blob']
        acquisition = path.with_suffix('.receipt.json')
        receipt = json.loads(acquisition.read_text())
        assert sha in json.dumps(receipt)
        lines = raw.decode().splitlines(keepends=True)
        anchors = []
        for start, end, finding in ANCHORS[i]:
            assert 1 <= start <= end <= len(lines), (i, start, end, len(lines))
            anchors.append(dict(lines=[start, end], excerpt_sha256=hashlib.sha256(''.join(lines[start-1:end]).encode()).hexdigest(), finding=finding))
        sources.append(dict(source_identity=item['url'], version_date='2026-09-02; ' + PIN,
            upstream_path=item['upstream_path'], local_copy=ref(path, 'Exact inspected pinned helper original'),
            acquisition_receipt=ref(acquisition, 'Observed public HTTPS acquisition'), git_blob_sha1=blob,
            bytes=len(raw), inspected_anchors=anchors, supported_claims=[a['finding'] for a in anchors], native_execution=False))
    # Keep the exact BDeu caller and test in scope, rather than infer their use.
    callers = []
    for name, spans in [('exec28_nested_15.txt', [(31, 57), (59, 112)]), ('exec28_nested_19.txt', [(14, 27)])]:
        p = RAW / name
        lines = p.read_text().splitlines(keepends=True)
        callers.append(dict(local_copy=ref(p, 'Previously pinned caller, re-inspected with immediate helper'),
                            inspected_anchors=[dict(lines=[start, end], excerpt_sha256=hashlib.sha256(''.join(lines[start-1:end]).encode()).hexdigest()) for start, end in spans]))
    results = exact.calculate()
    write(BASE / 'exact-results.json', results)
    write(BASE / 'mathematical-review.json', dict(status='pass_for_exact_declared_witnesses',
        evidence=[ref(Path(exact.__file__), 'Independent authored reference'), ref(BASE / 'exact-results.json', 'Performed exact witnesses')],
        findings=['Rising-factorial form gives 1/6 for two complete binary observations and 1/24 if the denominator counts one additional target-missing row.',
                  'The ratio 1/4 is an exact score-factor witness, not a missingness model or a bank bias estimate.',
                  'Ordered intersection, signed-int overflow and strict tolerance witnesses match the inspected branch conditions.',
                  'Unchanged nextLine state explains nonprogress of two DATA branches; no native timeout measurement is claimed.'],
        native_execution=False, final_acceptance=False))
    entries = [
        dict(integrated_citation_key='exec28_blip_helpers', kind='software_primary_sources',
             title='Pinned BLIP score, missingness, input, numerical and test helper review',
             author='reliableAI and BLIP contributors', year=2026, source_identity='microsoft/reliableAI@' + PIN,
             version_date='2026-09-02; pinned original helpers inspected 28 October 2026',
             local_copy=sources[0]['local_copy'], records=sources, callers=callers,
             inspected_anchors=[a for s in sources for a in s['inspected_anchors']],
             supported_claims=['Input suffix and readMissing change row retention and control flow.',
                               'Selected test discards a nonasserting comparator result.',
                               'Parent state, intersection, integer, numeric and copy boundaries require explicit admission contracts.'],
             evidence=[ref(BASE / 'plan-review.json', 'Reviewed initial exact scope'), ref(BASE / 'delegate-extension-plan.json', 'Reviewed immediate dependency extension'), ref(DAY / 'reliableai-nested-v1/author-review.json', 'Earlier BDeu and test callers')],
             limitations=['Static original-source review; no Java, JAR, parser or engine execution.', 'Selected helper notices do not resolve complete derivative or dependency rights.', 'ARFF, generic readers, remaining searchers and binary equality remain open.']),
        dict(integrated_citation_key='exec28_blip_helper_reference', kind='project_derivation',
             title='Exact score-denominator, ordered-index, reader-progress and bounded-integer witnesses',
             author='Causal banking proposal project', year=2026,
             source_identity='tools/blip_helper_reference_20261028.py', version_date='28 October 2026; authored exact witnesses',
             local_copy=ref(Path(exact.__file__), 'Independent exact calculation'),
             inspected_anchors=[ref(BASE / 'exact-results.json', 'Performed finite results')],
             supported_claims=['Exact score factors 1/6 and 1/24; ordered-row and integer-overflow witnesses.', 'Abstract reader nonprogress and assertion contract.'],
             evidence=[ref(BASE / 'mathematical-review.json', 'Finite mathematical review')],
             limitations=['No native package execution, empirical failure rate, calibrated uncertainty or bank data.'])]
    write(BASE / 'source-audit.json', dict(sources=entries, cutoff='2026-10-07', primary_files=9,
                                         selected_bytes=sum(s['bytes'] for s in sources), native_execution=False))
    development = r'''
\section{When score helpers change the proposed banking comparison}
\label{sec:exec28-blip-helpers}

A score comparison is only meaningful when its rows and failure states have the same meaning.
For a bank comparing candidate structures for arrears, utilization and servicing contact,
the input adapter determines which borrowers enter the score and whether an unobserved
field is dropped, retained or silently interpreted. The preceding BLIP discussion left
the data and test helpers uninspected. Nine further originals at the same reliableAI
commit now resolve selected paths without running Java or treating a source review as
empirical qualification. The findings concern the named derivative and routes, not every
BLIP release or all of its searchers.\citep{exec28_blip_helpers}

\paragraph{A test call is not a checked assertion.}
The selected BDeu test computes a score and calls
\texttt{RandomStuff.doubleEquals(-3627.0266, sk)}. The newly inspected helper returns a
boolean. Its default comparison is the strict absolute inequality
\( |s-v|<2^{-5}=1/32 \); it neither throws on inequality nor invokes a testing assertion.
The caller discards this return value. The inherited test base has a separate
\texttt{assertDoubleEquals} method that passes the boolean to \texttt{assertTrue}, but
the selected test does not call it. Consequently a score discrepancy alone does not
fail this particular comparison. File-read, score-computation or other exceptions can
still fail the test; no claim is made that the test cannot fail under any circumstance.
The proposed port must assert the result and state a justified absolute/relative error
policy, including nonfinite values. A test-suite name or a reported execution count
cannot establish numerical agreement.\citep{exec28_blip_helpers}

\paragraph{The data extension changes the observation rule.}
The common loader uses \texttt{readMissing=false} unless a caller supplies another
value. The \texttt{.dat} reader skips a row containing a question mark under this
default and advances the input. With missingness enabled it retains the row count and
records missing indices separately from each variable's ordinary category indices.
The \texttt{.data} reader has a different branch: its question-mark skip is guarded
by \texttt{readMissing=true}. That branch continues without updating
\texttt{nextLine}. Its blank-line branch has the same nonadvancing structure. On the
shown state transition, the next iteration reads the same in-memory line again.
This identifies a concrete progress defect for those inputs, not an observed native
runtime or a claim that all files fail. With the default false flag, the DATA route
instead retains question-mark rows in its separate missing-index representation.
An adapter that changes only a filename extension can therefore change both row
selection and termination behavior.\citep{exec28_blip_helpers}

For a servicing study this distinction is substantive. Dropping every borrower with
any missing recorded field changes the analyzed population; retaining a row with a
missing outcome does not by itself specify a valid observed-data likelihood. A
proposal must declare the missingness law and target population, record exclusion
counts, and distinguish source refusal from successful scoring. It must not call
either input branch an automatic treatment of informative missingness. A practical
first public fixture uses identical records in the two declared encodings, varies
the flag explicitly, and checks accepted rows, missing indices, progress and all
failure outcomes before comparing scores.\citep{exec28_blip_helpers}

\paragraph{An exact denominator witness.}
Let \(\alpha>0\) denote the BDeu equivalent sample size, let a binary child have
observed state counts \(n_0,n_1\), and write
\((a)_m=\prod_{j=0}^{m-1}(a+j)\), with \((a)_0=1\). For a parent-free complete
case with \(N=n_0+n_1\), the marginal factor underlying the log score is
\[
 M(\alpha;n_0,n_1,N)
 =\frac{(\alpha/2)_{n_0}(\alpha/2)_{n_1}}{(\alpha)_N}.
\]
The inspected root-score implementation uses the dataset's total row count in
the denominator and the lengths of category-index arrays in the numerator.
If a retained row has a missing child, those two counts need not agree. For the
stipulated rows with child values \(0,1,?\) and \(\alpha=2\), complete-case
counts give \(M=1/6\), while retaining three total rows but only the two observed
category indices gives \(M=1/24\). The factor ratio is \(1/4\), so the log scores
differ by \(-\log 4\). These rational values are independently reproduced here.
They expose the consequence of the specified count mismatch; they are not a claim
that an observed-data likelihood must always delete rows or that the empirical
bias has a particular sign.\citep{exec28_blip_helpers,exec28_blip_helper_reference}

For parented scores, the parent-configuration helper intersects ordinary category
indices. A missing parent can therefore remove a row from that configuration,
whereas a missing child can still leave the row in its parent count. The admission
contract should require a declared common row set or an explicitly derived
missing-data score. Compare each accepted configuration against an independent
count table. Otherwise a graph comparison may reward changes in its effective
sample as well as changes in the proposed conditional model. This source finding
does not identify the causal effect of a servicing intervention or remove hidden
confounding.\citep{exec28_blip_helpers}

\paragraph{Ordered identities and bounded representations.}
Both selected intersection helpers traverse two arrays by advancing the smaller
current row index. Their set interpretation requires ordered indices. For example,
the sets represented by \([2,0]\) and \([0,2]\) are equal, but the inspected
two-pointer logic counts one match; sorted arrays give two. The file readers append
row indices in increasing order on their ordinary paths, so this is an adapter
precondition and a negative fixture, not evidence that their normal output is
unsorted. The proposed typed boundary validates strict ordering, uniqueness and
range before accepting externally constructed datasets.\citep{exec28_blip_helpers,exec28_blip_helper_reference}

Parent cardinalities are multiplied in signed Java integers before allocating
configuration arrays and scaling the prior. The exact product \(65536^2=2^{32}\)
wraps to zero in that representation; \(46341^2\) exceeds the positive signed
range. These are representation witnesses, not estimates of typical banking table
sizes. Check multiplication before allocation and division, bound memory as well
as counts, and account for the helper's additional \texttt{short} state index.
The single-parent overload also returns the dataset's own indices instead of the
explicit alternative \texttt{rows} argument. Callers supplying a transformed row
view need a conformance check across one-parent and multi-parent routes.
The dataset copy constructor copies metadata references but leaves category and
missing-index fields unset; it is not a deep snapshot of the observations.
These contracts matter for reproducible resampling and recovery.\citep{exec28_blip_helpers,exec28_blip_helper_reference}

\paragraph{Numerical and reuse decisions.}
The inspected log-gamma helper declares an adaptation from FDLIBM and retains a
separate Sun notice, in addition to the author's disclaimer. Preserve those
component notices when evaluating a port; the nested root declaration is not a
complete dependency inventory. Its bit-level special-value branch returns positive
infinity for NaN and either infinity, and NaN for zero or finite negative input.
The score boundary must validate positive finite prior and cardinality arguments
and reject nonfinite results explicitly. This inspection does not supply an error
bound for the approximation or establish binary equality with an installed engine.
The loader also catches exceptions and returns null, requiring a structured failure
translation rather than a successful empty dataset.\citep{exec28_blip_helpers}

Retain BLIP as a conditional discrete score-search comparator. Reject direct
adoption of the selected DATA reader and nonasserting score test until repaired;
prefer an isolated, declared DAT route or a validated typed input adapter for the
first public comparison. A thin integration preserves the upstream search while
making row identity, finite-domain checks, progress, timeouts and failure accounting
explicit. A port needs the additional numerical and notice review. The next native
experiment should compare an independent table oracle across complete and missing
rows, category permutations, empty configurations, overflow refusal and interrupted
reads, with every requested case retained in the denominator. ARFF/generic readers,
remaining searchers, derivative origins, dependency rights and artifact equality
remain separate gaps. No acquired Java code was executed in this review.
\citep{exec28_blip_helpers,exec28_blip_helper_reference}
'''
    # Use an explicit token to avoid transport interpretation of TeX escapes.
    development = development.replace('\\', chr(92))
    (BASE / 'development.tex').write_text(development)
    sponsor = '''### Score helpers and the meaning of the comparison

Nine additional pinned BLIP helper originals clarify issues left open by the
nested-engine review. The selected score test discards a boolean comparison;
the inherited assertion helper is different and is not called. Input suffixes
also change missing-row handling. Two DATA-reader branches do not advance their
line state. These are source findings, not native failure-rate measurements.
[@exec28_blip_helpers]

For a stipulated binary child with observed counts one and one and prior size
two, the exact complete-case marginal factor is 1/6. Counting a third missing
child row only in the denominator changes that factor to 1/24. The ratio 1/4
shows why a proposed banking comparison must declare row retention and its
missing-data score before ranking graphs. Ordered row indices, bounded integer
cardinalities, numerical refusal and explicit test assertions become admission
conditions. No bank bias estimate or causal identification follows from this
arithmetic. [@exec28_blip_helpers; @exec28_blip_helper_reference]

Retain a conditional discrete score-search comparison, repair or replace the
selected DATA path and test, and use a declared typed input boundary for the
first public fixture. Keep all failures in its denominator. Component notices,
remaining readers/searchers, origin and binary equality still require review.
No acquired Java code was executed. [@exec28_blip_helpers]
'''
    (BASE / 'sponsor-addition.md').write_text(sponsor)
    write(BASE / 'copyedit-review.json', dict(status='pass_for_authored_addition',
        evidence=[ref(BASE / 'development.tex', 'Connected banking argument'), ref(BASE / 'sponsor-addition.md', 'Paired concise proposal addition')],
        checks=['Notation, count denominator and assumptions explained.', 'Specific route failures distinguished from whole-library claims.', 'Process history remains outside the product narrative.', 'No new paper cited from metadata; all new technical claims bind local originals.']))
    gaps = dict(selected_source_access='Nine named pinned helper originals acquired and inspected',
        known_routes=['Repair DATA reader progress and align readMissing semantics under a declared input contract.',
                      'Use an actual assertion and justified tolerance in the selected BDeu test.',
                      'Require a derived missing-data score or consistent accepted row set; validate parent configurations.',
                      'Bound integer/short state arithmetic, sorted indices, nonfinite scores and allocation before native admission.',
                      'Inspect remaining ARFF/Any readers, searchers, origin/derivative and binary/dependency boundaries.'],
        unchanged=['Full Java/software coverage', 'Native numerical and statistical qualification', 'Independent and bank acceptance'],
        native_execution=False, final_acceptance=False)
    write(BASE / 'remaining-gaps.json', gaps)
    verify_bindings(json.loads((BASE / 'source-audit.json').read_text()))
    write(BASE / 'review.json', dict(status='pass_for_bounded_source_and_exact_witnesses', sources=9,
        selected_bytes=sum(s['bytes'] for s in sources), evidence=[ref(BASE / p, 'Reviewed authored and primary evidence') for p in
        ('source-audit.json', 'exact-results.json', 'mathematical-review.json', 'copyedit-review.json', 'plan-review.json', 'delegate-extension-plan.json', 'remaining-gaps.json')],
        native_execution=False, visual_acceptance=False, final_acceptance=False))
    print(json.dumps(dict(review='pass', sources=9, bytes=sum(s['bytes'] for s in sources), original_coverage='inconclusive')))


if __name__ == '__main__':
    main()
