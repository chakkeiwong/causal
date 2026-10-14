# Artifact and data custody: bounded proposal review

Operation: `IN.REQ.artifact_data_custody`.

Inspect the unchanged local artifact store, scientific-context validation,
runtime replay and report code against the preserved IN02/IN04 contracts.
Replay the existing local service/runtime tests, then exercise isolated
fixtures for byte changes, metadata changes, scientific-context changes,
symlinks, read limits and unexpected file types. Include a coherent rewrite
of content/descriptor under an old handle to distinguish agreement with a
supplied reference from verification of the handle derivation. All altered
files belong to temporary directories under this repository's `.runtime`.

No bank data, sibling edits, external credentials or network services are
required. A named-pipe read, if exercised, runs in a disposable subprocess
with a one-second deadline and explicit termination, so a discovered blocking
read cannot hang the research session. Unexpected outcomes are evidence;
preserve the original implementation and bind exact next repairs rather than
rewriting a previously qualified source snapshot.

The resulting requirement discussion should connect custody to the causal
target: identical data bytes used for a different population, horizon, graph
or information clock do not support the same effect claim. Hash agreement
establishes consistency with a reference, not the truth or authority of its
contents. Describe the known local repair, owner-supplied provenance, access,
retention and revocation requirements separately from observed local behavior.
Integrate substantive findings into the reader after reviewing the actual
trials, with actual/static/proposed labels.

Plan review: existing tests substantiate selected mutations and replay, but
do not justify multi-tenant custody or arbitrary-file availability claims.
Tests use genuine local implementation calls; generated accounts and declared
contexts remain synthetic. The hostile-local-writer scenario lies outside the
current single-operator trust scope and is a boundary probe, not a claim of a
remote exploit. Exact refusal behavior and limitations can satisfy this
proposal requirement without claiming an accepted security product.
