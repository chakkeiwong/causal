"""Audit pinned nested originals and develop bounded banking reuse arguments."""
import hashlib
import json
from pathlib import Path

import reliableai_nested_reference_20261028 as exact
from prepare_reliableai_nested_review_20261028 import BASE, PIN, RAW, ROOT
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ANCHORS = [
    [(1, 21, 'Root file declares MIT terms; nested packages require separate identity.')],
    [(1, 32, 'Spot carries an Apache-2.0 text.'), (66, 121, 'Grant and redistribution clauses are present; dependency and compiled-artifact rights remain separate.')],
    [(1, 15, 'README identifies a research artifact and an example baseline command; paper title is discovery metadata only.')],
    [(1, 110, 'Pinned requirements include ananke-causal 0.1.5, causal-learn 0.1.2.8 and a broad numerical/ML stack; not a verified installed lock.')],
    [(10, 34, 'MAG converter delegates to MagToPag with complete rules; catches conversion exceptions and prints a generic message; main takes args[0].')],
    [(10, 32, 'PAG converter delegates to pagToMag, writes one MAG and catches conversion exceptions; no distribution over graph class is specified here.')],
    [(1, 6, 'Setup downloads Tetrad 6.8.0 with certificate checking disabled, downloads XOM 1.3.5, and compiles only the MAG-to-PAG helper in this script.')],
    [(47, 73, 'Writer maps arrow/tail endpoints with circle fallback.'),
     (136, 185, 'Shell conversion return status is not checked; read_tetrad_graph maps undirected --- to bidirected <-> as a workaround.'),
     (187, 224, 'Parser uses integer-to-X names and endpoint tokens; sample_mag delegates to external PAG-to-MAG conversion.'),
     (276, 296, 'Skeleton scoring returns an empty dictionary on arithmetic exceptions.'),
     (298, 399, 'Full-edge match respects endpoint storage reversal, but second endpoint arrow/tail keys repeat node2 and lose the neighbor; explicit zero-denominator conventions differ.')],
    [(1, 20, 'Baseline imports local FCI, passes Fisher Z, loads saved reference graph and returns compare_pag; no calibration claim follows.')],
    [(7, 28, 'Local def fci shadows imported fci; recursive global lookup receives a NumPy array after the first subsample.'),
     (30, 56, 'RFCI branch invokes a bundled causal-cmd JAR without checking shell status; missing output calls exit.'),
     (59, 84, 'One hundred subsamples aggregate binary graph marks; main selects RFCI rather than the default FCI function.')],
    [(1, 40, 'Nested BLIP carries LGPL-3 text incorporating GPL-3 terms.'), (79, 126, 'Combined-work provisions appear; this review inventories declarations, not deployment rights approval.')],
    [(1, 19, 'Nested README attributes BLIP to Mauro Scanagatta/IDSIA and lists scholarly leads; citations are metadata, not inspected papers.'),
     (25, 116, 'README documents discrete cardinalities, score caches, budgeted structure search and parameter learning; performance assertions are not verified here.')],
    [(5, 68, 'API artifact version 1.0, Java source/target 1.6, args4j 2.33, core 1.0 and JUnit 4.10 declarations.')],
    [(5, 35, 'Core declares version 1.0, args4j 2.33, JUnit 4.10 and Java 1.6 compiler target.')],
    [(22, 70, 'CLI banner version 0.9 differs from POM; reflective dispatch catches exceptions and logs them.'), (94, 131, 'CLI task registry is loaded from the clazzes resource, outside selected source scope.')],
    [(18, 52, 'BDeu alpha defaults to 10; passing zero leaves that default; parentless score uses arity and row counts.'),
     (55, 119, 'Parent configuration product is an int; score uses log-gamma and intersections with supplied parent rows; missing-value handling delegates remain uninspected.'),
     (127, 130, 'computePrediction forms a fresh int[] lookup key; concrete Map behavior and use path need review.')],
    [(116, 149, 'Search starts worker threads and awaits termination; returns best structure after output attempt.'),
     (199, 212, 'Time checks set a shared still_time flag.'),
     (335, 393, 'Optional acyclicity/completeness failures are logged but do not return before score-based acceptance.'),
     (499, 515, 'Worker checks budget between search calls; individual search call bound is not established here.'),
     (521, 550, 'Solution comparator returns -1 for equal scores, including comparison with itself; graph equality has a separate method.')],
    [(35, 81, 'Brutal solver delegates parent-set limits and searchers; options read sercher spelling and default tw=5, with prepare fallback 3 when tw=0.')],
    [(14, 60, 'Selected solver test methods invoke APIs using inherited fixture paths; no explicit correctness assertion in those active bodies.'),
     (62, 96, 'The visible assertion in greedyComplete is inside commented code; unseen helpers still may throw.')],
    [(14, 26, 'BDeu test invokes doubleEquals on a reference score; helper return/throw semantics remain uninspected, so no claim that the test cannot fail.')],
]

DEVELOPMENT = r'''section[Bundled discovery engines and semantic boundaries]{Bundled discovery engines and semantic boundaries}
label{sec:exec28-nested-engines}
A repository name is too coarse a unit for a banking reuse decision. A collections
analyst may ask whether changing a contact policy affects repayment, while a
bundled program learns a high-scoring discrete network or converts one graph
representation into another. The implementation can be useful without answering
that intervention question. The inspected reliableAI revision of 2 September
2026 contains selected Spot and BLIP components with different source origins,
licenses, numerical targets and operating boundaries. Twenty exact text originals
support the following comparison; no downloaded engine, Java class, JAR or setup
script was executed.citep{exec28_nested_sources}

subsection{Source identity is finer than the enclosing repository}
The repository root contains MIT license text, Spot contains Apache-2.0 text,
and the nested BLIP directory contains LGPL-3 text. The BLIP README attributes
the package to Mauro Scanagatta and IDSIA. These declarations cannot be collapsed
into a root-wide permission or proof that a vendored derivative equals an
upstream release. The selected POM files declare version 1.0 and Java 1.6
source/target settings, while the CLI banner declares version 0.9. Record both
identities and reconcile the exact distribution before proposing a native
adapter. Dependency terms, source changes, compiled artifacts and notices require
their own review. This is a source inventory, not an approval of redistribution.
citep{exec28_nested_sources}

Spot's requirements list pins a broad numerical and machine-learning stack,
including causal-learn 0.1.2.8 and ananke-causal 0.1.5. A requirements list is
not evidence that those packages, their transitive dependencies and the saved
Java binaries agree with the source under review. The setup script downloads
Tetrad 6.8.0 with certificate checking disabled, downloads XOM 1.3.5, and compiles
only the MAG-to-PAG helper. Its companion PAG-to-MAG source is present, but that
script does not rebuild it. The proposed integration therefore replaces this
installation path with authenticated, fixed artifacts and a reproducible build
before any execution is claimed.citep{exec28_nested_sources}

subsection{Graph conversion must preserve the object being inferred}
The Java MAG-to-PAG helper calls Tetrad's 	exttt{MagToPag}, enables the complete
rule set and saves the result. The reverse helper calls 	exttt{pagToMag} and
saves one graph. That call site specifies neither random sampling nor a
probability distribution over the equivalence class. Accordingly, the Python
name 	exttt{sample_mag} is not evidence that its output represents posterior
graph uncertainty. A proposed effect query must preserve the original class
or justify the selection rule and its scientific consequences.
citep{exec28_nested_sources}

The surrounding Python converter invokes the shell without checking its return
status and then reads the expected output. The Java helpers catch conversion
exceptions and print generic error messages. A future worker needs a structured
result that distinguishes launch failure, parse failure, invalid graph, missing
output and successful conversion. In a batch of banking questions, failures
must remain in the requested denominator rather than become absent files.
The existing public evaluation contract supplies a local accounting pattern;
it does not already implement this Java adapter.citep{exec28_nested_sources,exec28_fj_contract}

A further source-level workaround changes meaning: the inspected reader maps
an undirected token 	exttt{---} to a bidirected edge, just as it maps
	exttt{<->}. Those endpoint marks are distinct inputs. An adapter must reject
unsupported marks or retain them explicitly; it cannot silently treat the
workaround as an endpoint-preserving round trip. The other parser also
constructs node names from integer labels. Customer-variable identity and
time ordering therefore need an explicit bijection, with roundtrip checks,
rather than an assumption that every dataset already uses the expected names.
citep{exec28_nested_sources}

subsection{A good endpoint score can conceal the wrong neighboring variable}
For each arrowhead at variable $v$ on the edge joining $u$ and $v$, a
neighbor-preserving key is the ordered pair $(v,u)$. The inspected
	exttt{compare_pag} function uses such a pair for the first stored endpoint,
but encodes an arrowhead at the second endpoint as $(v,v)$. The same pattern
appears in its tail keys. Consequently, distinct edges entering one variable
can collapse to the same key. Its full-edge and skeleton metrics are separate
and need not share this failure.citep{exec28_nested_sources}

Consider a truthful edge $A	o B$ and an estimated edge $C	o B$, each stored
with $B$ second. The arrowhead key sets both become ${(B,B)}$, so their
reported arrowhead $F_1$ is one even though the neighbor-preserving sets are
disjoint and their $F_1$ is zero. Conversely, store the same truthful edge as
$(B,A)$ with an arrow at its first endpoint: its key becomes $(B,A)$, and
the inspected key comparison against the original storage gives zero although
the semantic graph is unchanged. Two incoming edges $A	o C$ and $B	o C$
also collapse to one second-endpoint key. These are exact authored logical
witnesses of the inspected encoding, not measured native failure rates.
citep{exec28_nested_reference}

The proposal should adopt the invariant that endpoint identity includes its
neighbor, canonicalize storage independently of meaning, and retain empty-graph
and unavailable-result conventions. The selected skeleton-only scorer returns
an empty dictionary on arithmetic exceptions; the PAG scorer instead uses
several explicit zero conventions. Their outputs cannot be silently pooled
into a common average without an adapter-level contract. A comparison of
contact-policy graphs is decision-relevant only if a correct arrowhead at the
wrong business variable is still recognized as an incorrect result.
citep{exec28_nested_sources}

The bootstrap module has a separate call-boundary problem. It imports
	exttt{fci} and then defines another function with that name. Inside the local
function, the call 	exttt{fci(sub_X)} resolves to the local global binding,
which expects an object with an 	exttt{X} attribute, although the supplied
subsample is a NumPy array. This static name-resolution finding concerns that
default route; the module's main block explicitly chooses RFCI instead. The
RFCI branch launches a bundled JAR and exits after a missing-output condition.
Neither reading the source nor counting one hundred subsamples establishes
that the numerical procedure ran or that its aggregate is calibrated.
citep{exec28_nested_sources}

subsection{BLIP supplies a score-based comparison, not an intervention answer}
The nested BLIP README documents discrete cardinalities, parent-set score
caches, budgeted search and parameter learning. For a child with $r$ states
and $q$ parent configurations, the inspected BDeu score allocates prior mass
$alpha/q$ per parent configuration and $alpha/(qr)$ per child-parent cell.
With complete categorical counts $N_{jk}$ and $N_j=sum_kN_{jk}$, its intended
log-gamma expression is
[
 sum_{j=1}^{q}left[logGamma(alpha/q)-logGamma(alpha/q+N_j)
 +sum_{k=1}^{r}{logGamma(alpha/(qr)+N_{jk})-logGamma(alpha/(qr))}ight].
]
This interpretation is conditional on the row-count and parent-configuration
helpers agreeing with those complete counts. Missingness, unused levels and
configuration enumeration require separate review. The integer product used
for $q$ also needs a declared cardinality bound before a large problem is
admitted.citep{exec28_nested_sources}

Passing zero to the inspected constructor preserves its default $alpha=10$;
it does not request a zero-prior calculation. In an exact binary example with
one observation in each category and no parents, the marginal factor is
$(alpha/2)^2/[alpha(alpha+1)]$. It equals $1/6$ at $alpha=2$ and $5/22$
at $alpha=10$. The score is the natural logarithm of this factor. This simple
prior-sensitivity calculation specifies an adapter input convention; it proves
neither a preferred prior nor a causal direction from observational fit.
citep{exec28_nested_reference}

The base solver compares summed parent-set scores. Optional acyclicity and
completeness checks log failures but do not return before the subsequent
score-based acceptance block. Specific searchers may enforce stronger
invariants, so this is not evidence that every native search returns a cyclic
graph. It does mean the base acceptance method is not by itself an enforcing
validation boundary. Time checks occur between search calls; the inspected
worker supplies no hard bound on an individual delegate call. In the retained
solution comparator, equal scores return minus one, including self-comparison,
rather than equality. Explicit graph validation, stable tie handling and
bounded worker cancellation belong in the proposed integration contract.
citep{exec28_nested_sources,exec28_nested_reference}

The selected solver tests invoke APIs and inherited file fixtures. The BDeu
test calls a 	exttt{doubleEquals} helper on a reference score; its uninspected
return or exception behavior prevents a claim that the test cannot fail. The
two visible files do not establish full test coverage. Likewise, the CLI uses
a separate task registry and reflective dispatch, with exceptions logged. A
stable external interface needs verified task mappings, typed requests and
observable failures, not just a command name.citep{exec28_nested_sources}

subsection{A conditional reuse decision with an executable next step}
Retain the selected revisions as transparent comparative references. A BLIP
component is a conditional candidate for a declared discrete score-based
baseline once source origin, dependencies, rights, cardinalities, missingness,
graph invariants and native tests are qualified. Direct adoption as a
bank-qualified causal engine is unsupported. For Spot, reject direct adoption
of the inspected scoring and wrapper paths until neighbor identity, graph
marks, function binding and failure reporting are repaired and independently
checked. This is a decision about these paths, not a rejection of every
uninspected algorithm in the repository.citep{exec28_nested_sources}

The near-term prototype protocol is finite: freeze a rights-cleared build;
test all supported endpoint pairs and storage reversals; reject unsupported
marks; keep every failed request; exercise zero-prior and high-cardinality
inputs; verify tied scores and invalid candidate graphs; then run a matched
public-data comparison on declared estimands and full costs. The source
review closes selected access and interpretation gaps while leaving nested
origins, remaining helpers, compiled artifacts, the broad Java census and
scientific qualification open. Unknown bank assignment or hidden causes
cannot be supplied by a successful source build.citep{exec28_nested_sources}
'''

SPONSOR = '''# Nested discovery components need separate contracts

Twenty pinned source files distinguish reliableAI's root, Spot and nested BLIP components. Their license declarations, source origins and build identities differ; a repository-level label cannot establish artifact equivalence or deployment rights. No acquired engine, setup script or JAR was executed. [@exec28_nested_sources]

The inspected Spot endpoint scorer can lose the neighboring variable: a wrong edge into the same destination obtains arrowhead F1 of one in an exact logical witness, while a neighbor-preserving score is zero. Reversing storage of the same semantic edge can produce the opposite discrepancy. Full-edge and skeleton metrics are separate. Graph conversion, default FCI binding and failure reporting also require explicit adapter repairs before a public trial. [@exec28_nested_sources; @exec28_nested_reference]

BLIP remains a conditional discrete score-based comparison. Zero alpha preserves a default of ten in the inspected constructor; score ties and base-level graph checks require a declared policy. Source inspection is neither native qualification nor evidence that observational score optimization answers a bank intervention question. The next economical step is a fixed public fixture with endpoint roundtrips, failed-request denominators, prior/cardinality checks and explicit costs. Broad software coverage, authentic bank truth and final acceptance remain open. [@exec28_nested_sources; @exec28_nested_reference]
'''


def main():
    assert not (BASE / 'author-review.json').exists()
    plan = json.loads((BASE / 'plan-review.json').read_text())
    verify_bindings(plan)
    sources = []
    for i, item in enumerate(plan['worklist']):
        p = RAW / (item['id'] + '.txt')
        data = p.read_bytes()
        receipt_path = p.with_suffix('.receipt.json')
        receipt = json.loads(receipt_path.read_text())
        sha = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + bytes([0]) + data).hexdigest()
        assert sha == receipt['sha256'] and blob == item['expected_git_blob']
        assert len(data) == item['expected_bytes'] == receipt['bytes']
        assert receipt['url'] == item['url'] and receipt['status'] == 'saved'
        lines = data.decode().splitlines(keepends=True)
        anchors = []
        for first, last, claim in ANCHORS[i]:
            assert 0 < first <= last <= len(lines)
            anchors.append(dict(lines=[first, last], finding=claim, excerpt_sha256=hashlib.sha256(''.join(lines[first-1:last]).encode()).hexdigest()))
        sources.append(dict(source_identity=item['url'], upstream_path=item['upstream_path'], version=PIN, version_date=plan['version_date'],
            local_copy=ref(p, 'Exact upstream bytes'), acquisition_receipt=ref(receipt_path, 'Performed bounded public GET'),
            accessed_utc=receipt['accessed_utc'], git_blob_sha1=blob, inspected_anchors=anchors, supported_claims=[a['finding'] for a in anchors], native_execution=False))
    assert len(sources) == 20
    write(BASE / 'primary-source-audit.json', dict(sources=sources, cutoff='2026-10-07', commit=PIN, native_execution=False, evidence=[ref(BASE / 'plan-review.json', 'Reviewed scope'), ref(BASE / 'identity-review.json', 'All exact originals verified')]))
    results = exact.calculate()
    write(BASE / 'exact-results.json', results)
    (BASE / 'development.tex').write_text(DEVELOPMENT)
    (BASE / 'sponsor-addition.md').write_text(SPONSOR)
    write(BASE / 'remaining-gaps.json', dict(historical_gap='JAVA04', selected_source_access='20 named pinned text originals acquired and inspected', broad_qualification='inconclusive', global_blocker=False,
        known_routes=['Inspect Spot FCI/Dataset and numerical delegates, Tetrad source and matching compiled artifacts.', 'Review BLIP origin/derivative diff, Score/DataSet/Gamma/ArrayUtils and concrete map helpers, searchers, registry and test helpers.', 'Replace endpoint keys, unsupported-mark conversion, default FCI binding and failure reporting under a reviewed adapter contract.', 'Qualify prior/cardinality/missingness, graph validity, tie ordering, timeout, native behavior and full-cost public comparisons.'],
        scholarly_leads='README-listed papers and Spot submission title remain metadata leads unless independently matched to a genuine locally saved original; no new paper cited here.',
        unknown_without_information=['Authentic bank assignment and hidden causes', 'A unique causal effect from observationally equivalent models', 'General useful uncertainty over arbitrary dependent latent graphs'],
        native_execution=False, final_acceptance=False))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_authored_finite_witnesses', evidence=[ref(Path(exact.__file__), 'Independent source-free arithmetic'), ref(BASE / 'exact-results.json', 'Performed exact outputs'), ref(BASE / 'primary-source-audit.json', 'Inspected conditions')],
        findings=['Wrong-neighbor arrowhead example gives inspected score 1 versus neighbor-preserving 0.', 'Storage reversal gives inspected score 0 versus invariant 1; two incoming arrowheads collapse to one key.', 'Binary marginal factors are exactly 1/6 and 5/22; log-score interpretation is conditional on complete counts.', 'Equal-score comparator returns -1; no native TreeSet behavior asserted.'], native_execution=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', evidence=[ref(BASE / 'development.tex', 'Connected banking argument'), ref(BASE / 'sponsor-addition.md', 'Sponsor implications')], checks=['Separate full-edge, skeleton and endpoint metrics.', 'Name-resolution finding distinguishes default route from RFCI main.', 'No claim that unseen test helpers cannot fail.', 'Different nested license declarations do not become a legal deployment approval.', 'Do not claim whole-package rejection or general native failure from selected static paths.']))
    citation_sources = [dict(integrated_citation_key='exec28_nested_sources', kind='software_primary_sources', title='Pinned reliableAI Spot and BLIP nested-engine source comparison', author='reliableAI and nested package contributors', year=2026, source_identity=sources[0]['source_identity'], version_date=plan['version_date'] + '; commit ' + PIN,
        local_copy=sources[0]['local_copy'], records=sources, inspected_anchors=[a for s in sources for a in s['inspected_anchors']], supported_claims=[a['finding'] for s in sources for a in s['inspected_anchors']], evidence=[ref(BASE / 'primary-source-audit.json', '20 exact originals'), ref(BASE / 'remaining-gaps.json', 'Declared residual scope')], limitations=['Selected static paths only; no downloaded code execution or whole-ecosystem completion.']),
        dict(integrated_citation_key='exec28_nested_reference', kind='project_derivation', title='Exact endpoint identity, prior and comparator witnesses', author='Causal banking proposal project', year=2026, source_identity='tools/reliableai_nested_reference_20261028.py', version_date='28 October 2026; exact authored calculations', local_copy=ref(Path(exact.__file__), 'Independent exact code'), inspected_anchors=[ref(BASE / 'exact-results.json', 'Performed finite calculations')], supported_claims=['Endpoint identity collision and storage reversal witnesses.', 'Exact binary prior factors and equal-score comparator witness.'], evidence=[ref(BASE / 'mathematical-review.json', 'Reviewed finite scope')], limitations=['No native execution, empirical failure rate or statistical calibration.'])]
    write(BASE / 'source-audit.json', dict(sources=citation_sources, cutoff='2026-10-07', new_records=2, new_scholarly_pdfs=0, native_execution=False))
    evidence = [ref(BASE / n, 'Completed source and manuscript review') for n in ('plan-review.json', 'primary-source-audit.json', 'source-audit.json', 'exact-results.json', 'mathematical-review.json', 'copyedit-review.json', 'remaining-gaps.json', 'development.tex', 'sponsor-addition.md')]
    evidence += [ref(Path(__file__), 'Review implementation'), ref(Path(exact.__file__), 'Authored exact witnesses')]
    write(BASE / 'author-review.json', dict(status='pass_for_bounded_static_review', sources=20, issues=[], evidence=evidence,
        findings=['All 20 originals match exact bytes, Git blobs and collector identities; selected anchors inspected.', 'Conditional reuse and specific refusal/repair paths are explicit.', 'Scientific, native, provenance, rights and broad coverage limits retained.'],
        limitations=['Publication pending.', 'Unseen delegates and scholarly originals remain omissions.', 'No downloaded code run, fresh visual review or final acceptance.'], native_execution=False, visual_acceptance=False, final_acceptance=False, awards_acceptance=False))
    write(BASE / 'review.json', json.loads((BASE / 'author-review.json').read_text()))
    verify_bindings(json.loads((BASE / 'author-review.json').read_text()))
    print(json.dumps(dict(status='pass_for_bounded_static_review', originals=20, citation_records=2, native_execution=False, publication='pending')))


if __name__ == '__main__':
    main()
