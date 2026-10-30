# Causal banking monograph: reproducible candidate package

Frozen from verified batch 065, 29 October 2026. This is a release
candidate, not a record of independent acceptance or bank qualification. The
reader has 1,939 pages; the aligned sponsor has
4 pages. The literature cutoff is 7 October 2026;
individual later retrievals retain their recorded coverage limits.

## Build

Prerequisites: Python 3, pdfLaTeX, BibTeX and the TeX packages/fonts recorded in
manifest.json. No network requests or downloaded executable dependencies occur.
Run from any directory with this extracted folder intact:

    python3 /absolute/path/to/package/build.py --output /absolute/path/to/new-build

The output directory must not exist. The script verifies all 478 source files,
compiles both documents with shell escape disabled, records actual compiler
inputs, checks warnings and compares both PDF hashes with this candidate.
It records changed or missing system inputs instead of silently claiming
cross-platform reproducibility. The exact system packages and fonts may be
needed for byte identity. The audit does not certify visual readability.

## Read and audit

pdf/ contains the candidate and sponsor. source/ contains all manuscript text,
bibliography, six figure PDFs and two inherited bibliography-style files.
Their existing copyright and licence notices remain intact. This local review
package makes no new grant of rights over third-party material.

evidence/full-deletion-ledger.md records each exact replacement and substantive
destination. evidence/deletion-audit.json binds the unchanged baseline, compiled
input order, mathematics, labels, citation keys and final candidate sources.
The preserved/ tree contains the exact release-stage baseline and declared
additions, so the reader can replay every replacement outside the checkout:

    python3 /absolute/path/to/package/check_preservation.py --output /path/to/new-audit

This checks exact before/after anchors and final bytes for every source. It
also verifies the packaged mathematical-addition reviews and their bound
witness/audit identities, disallows mathematical removal, and checks the
archived original behind the declared protected-inventory relocation. It
retains each reason and substantive destination for editorial assessment. The
earlier 505-edit baseline remains a separately scoped historical review; this
runner does not pretend to redo that earlier rewrite or judge scientific prose.

evidence/source-verification.json maps every citation to inspected original
anchors, supported claims, version/date and local hashes. Its repository-relative
original-source paths refer to the retained research workspace; genuine papers
and vendor documents are not redistributed in this build-only package. Numerical
receipts identify retained input data and independently reconstructed results;
the underlying research data/code remain in that same workspace. The separate
numerical reconstruction package declares its retained arithmetic groups and
requires five hash-checked external inputs through separate intake: two public
experimental subsets and three saved benchmark tables. A manuscript
build alone does not rerun or independently validate those studies.

Visual inspection of these exact candidate bytes and actual independent
editorial findings remain outstanding. No native vendor run, live language-model
benefit, bank-data validation or adoption is asserted by this package.
