"""Bind seven pinned originals to a bounded delegate-level adoption argument."""
import hashlib
import json
from pathlib import Path

import aitiotita_delegate_reference_20261028 as exact
from prepare_aitiotita_delegate_review_20261028 import ROOT, BASE, RAW, PIN
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write


ANCHORS = [
    [(17, 31, 'Abstract correlation, partial-correlation and test callbacks; default collider-test methods return false.')],
    [(367, 440, 'Overlap counts and unexplained linguistic cognate flow, rather than a Gaussian covariance oracle.'),
     (443, 449, 'Independence is the unexplained-count comparison against a pair-specific threshold.'),
     (452, 496, 'The optional collider test fixes pValue=0.2 and compares it to 0.10; capability flag returns true.')],
    [(30, 50, 'Caller-supplied separating sets are appended to the pair registry.'),
     (53, 107, 'Conservative, stable and first-set rules differ; the stable comparison includes exact half votes.'),
     (112, 126, 'The default arrow finder invokes propagation rules 1, 2 and 3.')],
    [(69, 95, 'Rule 3 requires the same endpoint to be both arrow and circle before mutation.')],
    [(35, 37, 'Circle, line and arrow are distinct endpoint constants 0, 1 and 2.'),
     (143, 167, 'Link removal and endpoint setter inspect preset flags but proceed with mutation.'),
     (189, 205, 'Arrow setter warns about preset arrows but writes and may change the reverse endpoint.'),
     (384, 409, 'Unshielded triples use outer, outer, middle order; neighbor getter returns the stored set.'),
     (489, 548, 'Path helper reads graph adjacency into local search containers; no endpoint mutation before the contradictory check.')],
    [(24, 38, 'The only test method in this acquired test file asserts true.')],
    [(7, 13, 'The acquired main method prints Hello World, without a causal CLI.')],
]


def read(path):
    return json.loads(path.read_text())


def main():
    assert not (BASE / 'author-review.json').exists()
    plan = read(BASE / 'plan-review.json')
    verify_bindings(plan)
    commits = read(RAW / 'v12_exec13_java_aitiotita_commit.json')
    commit = commits[0] if isinstance(commits, list) else commits
    date = commit['commit']['committer']['date']
    assert commit['sha'] == PIN and date < '2026-10-07T15:59:59Z'
    sources = []
    for index, item in enumerate(plan['worklist']):
        path = RAW / (item['id'] + '.txt')
        data = path.read_bytes()
        receipt_path = RAW / (item['id'] + '.receipt.json')
        receipt = read(receipt_path)
        sha = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert receipt['status'] == 'saved' and receipt['sha256'] == sha
        assert receipt['bytes'] == len(data) == item['expected_bytes']
        assert receipt['url'] == item['url'] and blob == item['expected_git_blob']
        lines = data.decode().splitlines(keepends=True)
        anchors = []
        for start, end, finding in ANCHORS[index]:
            assert 0 < start <= end <= len(lines)
            anchors.append(dict(lines=[start, end], finding=finding,
                                excerpt_sha256=hashlib.sha256(''.join(lines[start-1:end]).encode()).hexdigest()))
        sources.append(dict(source_identity=item['url'], upstream_path=item['upstream_path'],
                            version=PIN, version_date=date, local_copy=ref(path, 'Exact upstream bytes'),
                            acquisition_receipt=ref(receipt_path, 'Fixed collector receipt'),
                            accessed_utc=receipt['accessed_utc'], git_blob_sha1=blob,
                            inspected_anchors=anchors, supported_claims=[a['finding'] for a in anchors],
                            native_execution=False))
    assert len(sources) == 7
    # Preserve the exact six-variable argument and its earlier review as inherited project evidence.
    prior = ROOT / 'docs/program/execution/2026-10-13/java-discovery'
    evidence = [ref(BASE / 'plan-review.json', 'Reviewed seven-file scope'),
                ref(prior / 'reproduction-review.json', 'Earlier exact Gaussian witness, not a Java run'),
                ref(prior / 'omissions-register.json', 'Historical JAVA03 gap retained'),
                ref(RAW / 'v12_exec13_java_aitiotita_pc.txt', 'Inspected generic callback and arrow-finder call site'),
                ref(RAW / 'v12_exec13_java_aitiotita_license.txt', 'Inspected root Apache-2.0 text; dependency rights separate'),
                ref(RAW / 'v12_exec13_java_aitiotita_pom.txt', 'Java 8 and JUnit 3.8.1 declarations'),
                ref(Path(exact.__file__), 'Source-free logical witnesses'), ref(Path(__file__), 'Source audit logic')]
    audit = dict(cutoff='2026-10-07', commit=PIN, version_date=date,
                 sources=sources, evidence=evidence, native_execution=False)
    write(BASE / 'source-audit.json', audit)
    results = exact.calculate()
    write(BASE / 'exact-results.json', results)
    narrative = '''# Aitiotita: separate the oracle, orientation and graph boundary

An adapter for a bank must preserve the statistical question before it preserves
the Java method signature. The pinned Aitiotita revision of 9 September 2023
accepts abstract correlation, conditional-correlation and independence callbacks.
The inspected bundled discrete implementation counts linguistic cognate overlaps
and subtracts flow explained through other languages. Its result is compared to
a pair-specific threshold. The class name therefore does not establish a
Gaussian partial-correlation test, a calibrated p-value, or a model for repeated
customer records.

This distinction narrows the earlier six-variable Gaussian counterexample.
Conditioning on three independent baseline factors separates a rate concession
and a balance response, while adding their common consequence reopens dependence.
That exact project calculation refutes a general monotonicity justification for
the skeleton shortcut. It is not an observed failure of the bundled linguistic
flow oracle. A port supporting banking covariance tests would need to remove the
shortcut or prove it valid for an explicitly restricted oracle and graph family.

The orientation interface introduces a second choice. For an unshielded triple,
let m be the number of registered separating sets and k the number containing
the middle variable. The default arrow finder's conservative branch orients
when k=0; its stable branch uses k<=floor(m/2); its remaining branch uses the
first set. With two sets, one containing the middle and one excluding it, the
stable rule orients even at an exact half vote, the conservative rule does not,
and reversing the registry order can change the first-set result. This finite
logical witness is derived from the inspected conditions. It supplies neither
a probability that a collider is true nor a general orientation theorem.

Two further literal-source limitations affect reuse. The optional collider test
in the bundled flow class fixes pValue=0.2 with the distribution calculation
commented out; every invocation reaching the 0.10 comparison returns false.
That callback is separate from the registered-separating-set arrow finder, so
it does not imply that all algorithm paths refuse every collider. In propagation
rule 3, the same endpoint must first equal ARROW_END and subsequently equal
CIRCLE_END before the assignment. The constants are 2 and 0. The inspected
intervening path helper reads adjacency without mutating endpoint state, so
the branch is contradictory under ordinary unchanged single-threaded reads.
Other orientation rules and concurrent mutation are outside that claim.

Preset graph knowledge also requires an explicit boundary. The low-level link,
endpoint and arrow mutators inspect preset flags but continue writing. Some
callers guard writes, but those local guards do not make every low-level method
an enforcing constraint interface. A bank rule forbidding a later collections
action from causing an earlier balance must either be enforced by an adapter
before each mutation or checked and refused before a result is released. The
adapter must preserve each endpoint, distinguish absent edges from circles,
and copy neighbor collections rather than expose the live stored set.

The root license is Apache-2.0; this is a source identity observation, with
transitive artifact and redistribution rights still to review. The acquired
POM declares Java 8 and test-only JUnit 3.8.1. The acquired test method merely
asserts true, and the acquired main prints Hello World. These files supply no
substantive causal test evidence or usable discovery command contract.

The proposal decision is to retain the revision as a transparent comparison
and a conditional component candidate. Direct adoption as a qualified bank
discovery engine is unsupported. A port would need a declared oracle domain,
the conditioning-shortcut disposition, an explicit tie policy, a repaired and
independently checked orientation specification, enforcing knowledge semantics,
and endpoint-preserving serialization. Native build, graph roundtrip, numerical
failure, calibration, scale and dependency qualification remain later prototype
work. Seven inspected delegates close this precise source-access omission;
they do not close the Java software cell, the full Java census or bank validity.
'''
    (BASE / 'delegate-comparison.md').write_text(narrative)
    write(BASE / 'remaining-gaps.json', dict(
        historical_gap='JAVA03', source_access='Seven named delegate originals acquired and inspected',
        broad_qualification='inconclusive', global_blocker=False,
        remaining=[
            dict(gap='Oracle domain and conditioning shortcut', route='Specify banking oracle; remove shortcut or prove a restricted validity result; then compare exact skeletons.'),
            dict(gap='Orientation and prior knowledge', route='Specify tie and conflict policies; independently derive rule 3; enforce presets and verify endpoint roundtrips.'),
            dict(gap='Build, dependencies and rights', route='Review transitive utilities and artifact rights, then run an approved native prototype with frozen dependencies.'),
            dict(gap='Statistical and operating qualification', route='Predeclare singularity, missingness, calibration and scaling trials; retain all failed requests.')],
        other_historical_gaps='Weka, Banjo, nested engines and Tetrad lineages retain their later dated evidence; do not reset already inspected work.'))
    write(BASE / 'author-review.json', dict(
        status='pass_for_bounded_static_review', issues=[], sources=7,
        evidence=[ref(BASE / n, 'Bounded completed review') for n in
                  ('source-audit.json', 'exact-results.json', 'delegate-comparison.md', 'remaining-gaps.json')] + evidence,
        findings=['All seven originals match exact pinned Git blobs, byte counts and collector SHA-256.',
                  'Generic Gaussian counterexample is separated from the bundled linguistic oracle.',
                  'Half-vote, contradictory-endpoint and literal-p-value findings are source-derived logical claims.',
                  'Conditional adoption and remaining prototype routes are explicit.'],
        limitations=['Selected anchors, not every implementation path or dependency.',
                     'No Java build or downloaded code executed; no empirical package failure or bank validity claim.',
                     'The prose is a reviewed source packet pending preserving integration into the paired reader and sponsor.'],
        native_execution=False, visual_acceptance=False, final_acceptance=False,
        awards_acceptance=False))
    verify_bindings(read(BASE / 'author-review.json'))
    print(json.dumps(dict(status='pass_for_bounded_static_review', originals=7,
                          witnesses=['three endpoint states', '27 vote states', 'two-set order'],
                          native_execution=False, integration='pending')))


if __name__ == '__main__':
    main()
