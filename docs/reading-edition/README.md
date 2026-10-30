# Causal inference for banking — reading edition

Open [the integrated PDF](../causal_banking_reading_edition_2026-10-29.pdf).
The [LaTeX root](../causal_banking_reading_edition_2026-10-29.tex) compiles the
complete manuscript in nine thematic parts. The [review](editorial-review.md)
states what changed, what was checked and what still needs human or visual review.

The active research programme is [the live master](../program/master-live.md).
Its scientific priorities are independent of the historical dependency queue.

Build from the repository root:

    python3 tools/build_reading_edition.py prepare
    python3 tools/build_reading_edition.py build
    python3 tools/check_reading_edition.py

The source map retains the original paths and hashes. Reading copies can be
regenerated; make repeatable contextual edits in the builder or the authored
opening and conclusion files. Do not edit protected historical sources to make
the new edition appear older or to alter prior results.
