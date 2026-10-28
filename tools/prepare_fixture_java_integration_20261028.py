"""Review source identities and connected prose before a preserving paired build."""
import json
from pathlib import Path

import recovery_fixture_java_reference_20261028 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'docs/program/execution/2026-10-28'
BASE = DAY / 'fixture-java-review-v1'
JAVA = DAY / 'aitiotita-delegates-v1'
FIXTURE = DAY / 'public-attention-contract-v2'


DEVELOPMENT = r'''\section[Enforcing a public discovery evaluation contract]{Enforcing a public discovery evaluation contract}
\label{sec:exec28-fj-fixture}
A public discovery comparison needs an information contract that can fail visibly.
The preceding small fixture illustrates a split-and-score design. Its case objects
still carry graph truth, and its checks do not enforce every duplicate identity or
nonfinite denominator boundary. The stronger proposal-owned successor separates
case identity from labels and checks these conditions explicitly. Its demonstrated
scope is a trusted local interface, with no external discovery engine execution.
\citep{exec28_fj_contract}

\subsection{Declared identity and permitted truth access}
A case reference contains an identifier, graph-instance identifier, exact data
SHA-256 and one of training, validation or evaluation. It contains no graph
truth. A frozen registry binds the node universe and all case references to a
deterministic digest. The registry rejects repeated case identifiers, graph-instance
identifiers and data hashes across every declared split, including repeated
evaluation requests. This is a policy on supplied identities and exact bytes;
it does not prove that two differently encoded mechanisms are independent.
\citep{exec28_fj_contract}

Validation labels must match exactly the validation case identifiers. The threshold
selector checks both this split role and the registry digest; an evaluation truth
view is refused. A selected threshold is then carried into a separate evaluation
call that checks the evaluation labels and retains every requested case. Neither
a digest nor a frozen Python object prevents a malicious caller from fabricating
a new validation label view or obtaining labels elsewhere. A later native
experiment therefore also needs a separately operated truth store, declared
access paths and a recorded selection freeze. These local checks specify a
reviewable boundary before that more costly experiment.
\citep{exec28_fj_contract}

The graph universe is directed off-diagonal edges over the frozen node set.
Unknown nodes, self edges and mutable edge sets are refused. For a predicted
edge set $E$ and truth $T$, the fixture computes
\[
 F_1(E,T)=\frac{2|E\cap T|}{|E|+|T|}
\]
when the denominator is positive and explicitly assigns one to an empty/empty
pair. That convention is part of this comparison, rather than an inferred
property of a third-party scorer. Threshold candidates use exact rational
numbers in $[0,1]$. Equal validation macro scores select the smallest threshold,
so reversing candidate insertion order cannot resolve a scientific choice
differently. A future score-to-edge adapter must additionally freeze its strict
or inclusive comparison and record the predictions associated with each
candidate; this fixture accepts those candidate graphs as inputs.
\citep{exec28_fj_contract}

\subsection{Availability changes the interpretation of an average}
Let $m>0$ be the requested graph count, $v$ the finite valid count and $s$ the sum
of valid scores. The reported conditional mean is $s/v$ when $v>0$ and the declared
minimum valid count is met. Availability is $v/m$. Missing results, NaN and
either infinity remain in the requested count and have separate reason counts.
When no valid result remains, the mean is unavailable. Increasing a minimum
valid count can also make the mean unavailable even when a finite score exists.
These are accounting and interface rules, not statistical calibration results.
\citep{exec28_fj_contract}

The exact example retains two evaluation requests: one perfectly reconstructed
graph and one unavailable prediction. Its conditional mean is one and its
availability is $1/2$. If a score for every unavailable request is known only
to lie in $[0,1]$, the mean over all requested graphs lies in
\[
 \left[\frac{s}{m},\frac{s+m-v}{m}\right]=[1/2,1].
\]
This is an elementary bound on missing scores, not a confidence interval.
A bank comparing workflows should preserve both the conditional quality and
availability before assigning value to returned graphs. Reporting only the
conditional score of one would conceal the unresolved request.
\citep{exec28_fj_reference}

The performed suite contains 48 adversarial cases with no failures, errors or
skips. It covers duplicate identities, split-role confusion, graph-universe
errors, invalid thresholds, deterministic ties, missing/nonfinite denominators
and retained failed evaluation requests. It establishes these selected local
behaviors. It does not establish authentic graph labels, process isolation,
general calibration, an implemented third-party adapter or bank performance.
A causal comparison is credible only when the missing results and permitted
information remain part of the reported question.\citep{exec28_fj_contract}

\section[Java delegates and conditional adoption]{Java delegates and conditional adoption}
\label{sec:exec28-fj-java}
A banking discovery adapter must preserve the oracle as well as the graph.
The seven newly inspected Aitiotita delegates at the pinned 9 September 2023
revision clarify the earlier source-access limit. Their abstract interface
accepts correlation, conditional-correlation and independence callbacks. The
bundled discrete implementation instead counts linguistic cognate overlaps
and subtracts flow explained through other languages. Its unexplained count
is compared to a pair-specific threshold. The class name alone supplies no
Gaussian partial-correlation test or calibrated banking p-value.
\citep{exec28_fj_java}

\subsection{The earlier conditioning witness has a precise scope}
The earlier exact six-variable Gaussian construction separates a concession
$X$ and response $Y$ after three independent baseline factors are held fixed.
Adding their common consequence opens dependence again: conditional covariance
changes from zero to $-1/3$, with residual variances $2/3$ and correlation
$-1/2$. It refutes a general argument that dependence given every neighbor
rules out all smaller separators. Because the generic algorithm accepts a
supplied oracle, a proposed covariance-based port must address this objection.
It is not an empirical failure of the bundled linguistic-flow oracle. Retain
that domain distinction when deciding whether to remove the shortcut or prove
validity in a narrower graph and oracle family.
\citep{exec13_java_examples,exec13_java_aitiotita,exec28_fj_java}

\subsection{Three separating-set policies need different interpretations}
For an unshielded triple, let $m$ be the number of registered separating sets
and $k$ the number containing the middle variable. The inspected default
arrow finder orients in its conservative branch when $k=0$, in its stable
branch when $k\leq\lfloor m/2\rfloor$, and in its remaining branch when the
first set excludes the middle. Thus an exact half vote is included by the
stable comparison. With two sets, one containing the middle and one excluding
it, that branch orients and the conservative branch refuses; reversing the
set order can alter the first-set result. The authored finite truth table
checks all 27 $(m,k)$ states for $1\leq m\leq6$. The differences from a strict
minority occur at $(2,1)$, $(4,2)$ and $(6,3)$. None of these policies supplies
a probability that the proposed collider is true.\citep{exec28_fj_java,exec28_fj_reference}

The optional collider callback in the discrete-flow class makes a separate
literal-source choice: it sets $p=0.2$, leaves the distribution calculation
commented, and compares $p<0.10$. Every invocation reaching that comparison
returns false. The registered-separating-set arrow finder is a different
path, so this observation does not imply that every algorithm configuration
refuses every collider. Reuse requires tracing the selected call path rather
than inferring global behavior from a method name.\citep{exec28_fj_java}

\subsection{Propagation and prior knowledge need enforcement}
In the inspected propagation rule 3, an outer condition requires an endpoint
to equal the arrow constant two; an inner condition requires the same endpoint
to equal the circle constant zero before the assignment. The intervening path
helper reads adjacency without changing endpoint state. Under unchanged
single-threaded graph reads these requirements are contradictory. The
three-state authored truth table confirms this local logical obstruction;
it does not prove the behavior of every other rule or concurrent execution.
A port needs an independently derived intended rule and graph-level witnesses,
rather than an unreviewed textual replacement of one index.
\citep{exec28_fj_java,exec28_fj_reference}

The low-level graph methods also differ from an enforcing knowledge boundary.
Link removal and endpoint/arrow setters inspect preset flags but proceed with
mutation. Some callers guard particular writes. Such guards do not make every
method safe for an arbitrary caller with an earlier-time causal restriction.
For example, a prohibition on a later collections action causing an earlier
balance must be enforced at the adapter boundary and checked before release.
Serialization should preserve both endpoint marks and edge existence; the
neighbor getter exposes a live stored set, so a consumer should use a copy.
\citep{exec28_fj_java}

The acquired root text is Apache-2.0. Dependency and redistributed-artifact
rights still require their own review. The POM declares Java 8 and test-only
JUnit 3.8.1; the acquired test method only asserts true, while the main method
prints Hello World. These files provide no substantive causal test evidence
or usable discovery CLI contract. Native builds and external tests were not
run here.\citep{exec28_fj_java}

The proposal should retain this revision as a transparent comparison and a
conditional component candidate. A banking port would need a declared oracle,
the conditioning-shortcut disposition, an explicit tie policy, independently
checked propagation, enforcing knowledge semantics and endpoint-preserving
roundtrips. Native numerical failure, missingness, calibration, scale and
dependency qualification remain prototype work. Seven inspected delegates
close this particular source-access omission, while the broad Java survey and
qualified banking discovery remain open. Conditional reuse follows the
declared oracle, the graph semantics and the evidence supporting each boundary.
'''

SPONSOR = r'''# Availability and graph constraints are part of discovery quality

A stronger proposal-owned evaluation interface now separates immutable case identities from graph labels, rejects repeated declared case/graph/data identities, permits validation labels only in threshold selection, and retains unavailable held-out requests. All 48 adversarial cases passed. These are trusted local contracts, not process isolation, authentic labels or an executed external discovery adapter. [@exec28_fj_contract]

In its exact example, one of two requested graphs is perfectly reconstructed and one prediction is unavailable. The conditional F1 is one, availability is one half, and the mean across all requests is bounded by one half and one if the missing score can be anywhere in [0,1]. The proposal must report quality and availability together before valuing a workflow. This accounting bound is not statistical calibration. [@exec28_fj_reference]

Seven pinned Aitiotita delegates clarify its conditional reuse case. Its bundled oracle counts linguistic flow rather than Gaussian covariance; the earlier Gaussian conditioning counterexample therefore addresses the generic shortcut, not an observed failure of that bundled oracle. Half-vote orientation, a locally contradictory rule-3 condition, and low-level preset mutations require explicit policies and independently checked repairs before a banking port. The acquired placeholder test and Hello World main supply no substantive causal qualification or CLI. Retain the revision as a comparison and conditional component candidate; native, dependency, rights and statistical qualification remain later prototype work. [@exec28_fj_java; @exec28_fj_reference]
'''


def main():
    assert not BASE.exists()
    java = json.loads((JAVA / 'source-audit.json').read_text())
    for packet in (JAVA, FIXTURE):
        verify_bindings(json.loads((packet / 'author-review.json').read_text()))
    prior = DAY / 'attention-protocol-reader-v2'
    prior_audit = json.loads((prior / 'reader/source-audit.json').read_text())
    assert len(prior_audit['sources']) == 1433
    sources = [dict(
        integrated_citation_key='exec28_fj_java', kind='software_primary_sources',
        title='Aitiotita pinned oracle, orientation, graph, test and entrypoint delegates',
        author='jdellert/aitiotita contributors', year=2023,
        source_identity=java['sources'][0]['source_identity'],
        version_date=java['version_date'] + '; commit ' + java['commit'],
        local_copy=java['sources'][0]['local_copy'], records=java['sources'],
        inspected_anchors=[anchor for item in java['sources'] for anchor in item['inspected_anchors']],
        supported_claims=[claim for item in java['sources'] for claim in item['supported_claims']],
        evidence=[ref(JAVA / n, 'Bounded source review') for n in ('source-audit.json', 'author-review.json', 'remaining-gaps.json')],
        limitations=['Selected exact delegates and literal-source findings; no Java/native execution.',
                     'Generic Gaussian witness and bundled linguistic oracle are distinct domains.']),
        dict(integrated_citation_key='exec28_fj_contract', kind='project_implementation_and_adversarial_tests',
        title='Proposal-owned public graph evaluation contract version 2 and 48-case execution',
        author='Causal banking proposal project', year=2026,
        source_identity='tools/public_attention_contract_v2_20261028.py',
        version_date='28 October 2026; exact local fixture and performed tests',
        local_copy=ref(ROOT / 'tools/public_attention_contract_v2_20261028.py', 'Inspected authored API'),
        inspected_anchors=[ref(FIXTURE / n, 'Performed finite fixture evidence') for n in
                           ('author-review.json', 'test-exit.json', 'pytest-results.xml', 'exact-example.json')],
        supported_claims=['Truth-free declared identities, validation-role checks, exact ties and finite denominators.',
                          'All 48 selected adversarial cases passed; no external model or native engine.'],
        evidence=[ref(ROOT / 'tests/test_public_attention_contract_v2_20261028.py', 'Exact adversarial suite'),
                  ref(FIXTURE / 'harness-failure.json', 'Preserved wrapper-count error and evidence repair')],
        limitations=['Trusted local callers; no process isolation, authentic-label verification or empirical calibration.']),
        dict(integrated_citation_key='exec28_fj_reference', kind='project_derivation_and_exact_reference',
        title='Exact logical orientation witnesses and full-request missing-score accounting bounds',
        author='Causal banking proposal project', year=2026,
        source_identity='tools/recovery_fixture_java_reference_20261028.py',
        version_date='28 October 2026; exact authored calculations',
        local_copy=ref(Path(exact.__file__), 'Independent source-free exact reference'),
        inspected_anchors=[ref(ROOT / 'tools/aitiotita_delegate_reference_20261028.py', 'Three endpoint and 27 vote states')],
        supported_claims=['Stable half-vote differences and contradictory endpoint literal are finite logical witnesses.',
                          'With one valid perfect score in two requests, the full-request mean is bounded by [1/2,1].'],
        limitations=['Accounting and logic, not confidence coverage, native performance or universal algorithm correctness.'])]
    assert not {s['integrated_citation_key'] for s in sources} & {s['integrated_citation_key'] for s in prior_audit['sources']}
    BASE.mkdir()
    write(BASE / 'source-audit.json', dict(sources=sources, cutoff='2026-10-07', native_execution=False,
          evidence=[ref(JAVA / 'author-review.json', 'Completed delegate review'), ref(FIXTURE / 'author-review.json', 'Completed fixture review')]))
    write(BASE / 'exact-results.json', exact.calculate())
    (BASE / 'development.tex').write_text(DEVELOPMENT)
    (BASE / 'sponsor-addition.md').write_text(SPONSOR)
    evidence = [ref(BASE / n, 'Reviewed integration input') for n in
                ('source-audit.json', 'exact-results.json', 'development.tex', 'sponsor-addition.md')]
    evidence += [ref(Path(__file__), 'Source identities and authored argument')]
    write(BASE / 'plan-review.json', dict(status='pass', evidence=evidence,
        checks=['Preserve all 1433 reader and 1094 sponsor source identities and compiled content inputs.',
                'Three additions are software/project records; no new scholarly PDF is implied.',
                'Local checks, exact logic, native qualification and banking acceptance remain distinct.',
                'Compile paired documents and inspect all-page text/bounds; retain visual acceptance open.']))
    write(BASE / 'mathematical-review.json', dict(status='pass_for_declared_exact_arguments', issues=[], evidence=evidence,
        findings=['The full-request score bound follows from 0<=unavailable score<=1; conditional score and availability are different quantities.',
                  'All 27 finite vote states and the three distinct endpoint states reproduce.',
                  'No Gaussian theorem is transferred to the linguistic flow oracle.',
                  'The exact example is consistent with the previously executed 48-case fixture suite.']))
    write(BASE / 'copyedit-review.json', dict(status='pass', evidence=evidence,
        findings=['Connects graph uncertainty and failure accounting to a banking adapter decision.',
                  'Defines all displayed notation and numerical inputs.',
                  'Distinguishes source facts, authored proofs, performed fixture tests and future prototype work.',
                  'Wrapper failures and execution governance remain outside the product narrative.']))
    write(BASE / 'review.json', dict(status='pass', issues=[], evidence=evidence + [ref(BASE / n, 'Pre-build review') for n in
        ('plan-review.json', 'mathematical-review.json', 'copyedit-review.json')],
        native_execution=False, visual_acceptance=False, final_acceptance=False))
    verify_bindings(json.loads((BASE / 'review.json').read_text()))
    print(json.dumps(dict(status='pass_for_preserving_build', added_records=3,
                          expected_reader_records=1436, expected_sponsor_records=1099)))


if __name__ == '__main__':
    main()
