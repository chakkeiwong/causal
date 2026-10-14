# MathDevMCP

MathDevMCP is an exploratory, high-standard, rigorous, agent-facing
mathematical development system. It searches broadly across assumptions,
derivations, counterexamples, formalizations, and specialist-tool routes while
remaining strict at the claim boundary: diagnostic exploration is not a proof,
publication decision, or scientific promotion. Release and private-corpus
controls remain available as operator capabilities, but they do not define the
academic mission.

Current distribution status: **controlled internal research beta** for trusted
local stdio use. It is intended for academic colleagues and designated
maintainers, not untrusted network or multi-tenant deployment.

The primary product document is:

- [Final release report](docs/mathdevmcp-release-report.tex)
- [Colleague quick start](docs/mathdevmcp-colleague-quick-start.md)
- [Maintained documentation index](docs/README.md)
- [Operator guide](docs/mathdevmcp-operator-guide.md)
- [Deployment guide](docs/mathdevmcp-deployment-guide.md)
- [Release policy](docs/mathdevmcp-release-policy.md)
- [Security and governance](docs/mathdevmcp-security-governance.md)
- [Private corpus manifest guide](docs/private-corpus-manifest-guide.md)
- [Maintainer guide](docs/mathdevmcp-maintainer-guide.md)
- [Support matrix](docs/mathdevmcp-support-matrix.md)
- [Versioning and compatibility policy](docs/mathdevmcp-versioning-policy.md)

Distribution is restricted to colleagues authorized by the project owner under
the controlled-internal [license](LICENSE). Do not upload this package or its
third-party document corpus to a public repository or package index.

## Install

Base development install:

```bash
python -m pip install -e ".[dev]"
```

MCP-facing install:

```bash
python -m pip install -e ".[dev,mcp]"
```

The base package intentionally has no required runtime dependencies. Use the
`[mcp]` extra for `mathdevmcp-mcp` and the FastMCP server runtime.

Optional symbolic/backend packages:

```bash
python -m pip install -e ".[dev,symbolic]"
scripts/setup_backend_env.sh
```

LeanDojo should remain in an isolated backend environment. The documented
bootstrap creates `mathdevmcp-backends`; an existing validated environment can
be selected with `MATHDEVMCP_BACKEND_CONDA_ENV`:

```bash
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean"
scripts/validate_backend_install.sh "$PWD"
```

Optional Lean-context integrations are version-controlled but not required by
the base package. `doctor` reports both the supported version and the installed
version/status:

```bash
python -m pip install -e ".[lean-search]"
# or let the isolated backend env install the supported LeanDojo + LeanExplore pins:
scripts/setup_backend_env.sh
PYTHONPATH=src python -m mathdevmcp.cli doctor
```

Current supported integration pins are recorded in
`src/mathdevmcp/integration_versions.py` and surfaced by `doctor`:

- `sympy==1.14.0`
- `mcp==1.27.0`
- `lean-dojo==4.20.0` with `leanprover/lean4:v4.20.0`
- `lean-explore==1.2.1`
- `pantograph==0.3.15` in a Python 3.11 Lean backend environment
- LeanSearch-v2 source/service commit `94f4888cbaf9`
- jixia source commit `755fde27a9cf` with `leanprover/lean4:v4.29.0`

LaTeXML is a system tool. Validate it with:

```bash
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
```

The supported install and validation modes are summarized in the
[support matrix](docs/mathdevmcp-support-matrix.md).

## MCP Interface

The MCP server uses a tiered interface. The preferred surface keeps
deterministic primitives, tested workflow tools, and operational release tools:

- primitives: `search_latex`, `latex_label_lookup`, `search_code_docs`,
  `check_equality`, `lean_check`;
- workflows: `audit_implementation_label`, `derive_label_step`,
  `derive_or_refute`, `prove_or_refute`, `localize_proof_gap`,
  `code_implements_equation`, `classify_math_claim`, `reconcile_notation`,
  `generate_math_tests`, `math_review_packet`, `math_change_impact`,
  `literature_local_audit`, `implementation_brief`,
  `audit_derivation_label`, `audit_derivation_v2_label`,
  `audit_kalman_recursion`, `typed_obligation_label`,
  `derive_from`, `prove_or_counterexample`, `assumptions_for`,
  `debug_derivation`, `audit_math_to_code`, `prepare_review_packet`,
  `propose_fix`, `audit_and_propose_fix`, `external_tool_first_plan`;
- operations: `doctor`, `benchmark_gate`, `run_benchmarks`,
  `high_level_workflow_quality`, `workbench_benchmark_quality`,
  `release_corpus_manifest`, `validate_release_corpus`, `release_readiness`,
  `release_profile_analysis`, `lean_readiness`;
- informational: `tool_matrix`/`get_tool_matrix`, `status_taxonomy`,
  `governance_policy`.

Compatibility aliases remain available for a migration cycle:
`extract_latex_context` and `extract_latex_neighborhood` map to
`latex_label_lookup`; `check_proof_obligation` maps to `check_equality`;
`compare_label_code` maps to `audit_implementation_label`.

See [mcp/README.md](mcp/README.md) for the full surface and migration table.

## Common Workflows

Question-centered mathematical debugging workflows:

```bash
PYTHONPATH=src python -m mathdevmcp.cli derive-from "a + b = b + a" \
  --given "a,b are scalars"
PYTHONPATH=src python -m mathdevmcp.cli prove-or-counterexample "A*B = B*A"
PYTHONPATH=src python -m mathdevmcp.cli assumptions-for "logdet(A)"
PYTHONPATH=src python -m mathdevmcp.cli debug-derivation \
  --step "logdet(A)" --step "trace(A)" --step "trace(A)"
PYTHONPATH=src python -m mathdevmcp.cli audit-math-to-code \
  "logdet(S)" "def f(S): return logdet(S)"
PYTHONPATH=src python -m mathdevmcp.cli prepare-review-packet \
  "Review derivation" --evidence '[{"status":"diagnostic_only"}]'
PYTHONPATH=src python -m mathdevmcp.cli derive-or-refute "a + b = b + a"
PYTHONPATH=src python -m mathdevmcp.cli prove-or-refute "(a+b)*(a-b) = a*a - b*b"
PYTHONPATH=src python -m mathdevmcp.cli localize-proof-gap \
  --step "a + b = b + a" --step "b + a = a - b"
PYTHONPATH=src python -m mathdevmcp.cli code-implements-equation \
  "logdet(S)" "def f(S): return logdet(S)"
PYTHONPATH=src python -m mathdevmcp.cli classify-math-claim \
  "Assume x > 0." --evidence '[{"metadata":{"contract":"claim_support_packet"},"claim_status":"model_assumption"}]'
PYTHONPATH=src python -m mathdevmcp.cli external-tool-first-plan \
  "a + b = b + a"
```

Extract a local PDF through the optional ResearchAssistant checkout:

```bash
PYTHONPATH=src python -m mathdevmcp.cli \
  extract-pdf-with-research-assistant /absolute/path/paper.pdf \
  --response-mode compact --output-json /tmp/paper-extraction.json
```

This experimental provider bridge binds the output to the PDF bytes and the
local ResearchAssistant checkout. It defaults to a compact response and keeps
parser failures, disagreements, and capability limits visible. PDF equations
and citations remain non-certifying; check material claims against rendered
pages or structured source. ResearchAssistant currently exposes PDF parsing
through its CLI rather than its MCP server.

Run the experimental general applied-mathematics audit over PDF/LaTeX sources,
with optional code/model and data paths:

```bash
PYTHONPATH=src python -m mathdevmcp.cli audit-applied-math-document \
  /absolute/path/paper.pdf --response-mode compact \
  --artifact-root /tmp/mathdevmcp-applied-audit
```

The compact response is backed by an immutable detailed JSON artifact. Resolve
one bounded collection by its exact artifact digest:

```bash
PYTHONPATH=src python -m mathdevmcp.cli page-applied-math-audit-records \
  /tmp/mathdevmcp-applied-audit/audit-<source-prefix>.json <artifact-sha256> findings
```

The audit preserves page/line/source evidence, explicit abstentions, optional
ResearchAssistant intake, and typed DynareMCP diagnostics. It does not certify
equations, code equivalence, causal validity, or scientific conclusions.
Detailed artifacts also expose pageable `equation_blocks`,
`semantic_profiles`, `relation_hypotheses`, and `semantic_checks`. These
records reconstruct candidate parser-text relations and diagnostic tensions;
they do not authenticate PDF transcription or prove that a displayed equation
is correct or wrong.

These tools are exploratory in search and rigorous at the claim boundary. Backend-certified scoped obligations can support
proof/refutation statuses; structural code matches, numeric diagnostics,
generated tests, and review packets remain diagnostic unless linked to a
certifying backend result.

The high-level commands return `high_level_workflow_result` envelopes with
explicit `evidence_classes`, `certification_source`, `veto_reasons`,
`assumptions`, `counterexamples`, `actions`, and `non_claims`. Free-form
`--given` context is not silently promoted to a formal assumption; pass formal
route assumptions with `--assumption`.

Check the runtime environment:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
scripts/backend_env_doctor.sh "$PWD"
```

Analyze all release profiles before answering what gaps remain:

```bash
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
```

Search a LaTeX corpus:

```bash
PYTHONPATH=src python -m mathdevmcp.cli search-latex "state space likelihood" \
  --root benchmarks/fixtures --limit 3
```

Audit a labeled equation against code:

```bash
PYTHONPATH=src python -m mathdevmcp.cli compare-label-code \
  eq:dept-state-space-likelihood \
  benchmarks/fixtures/doc_department_state_space_missing_solve.py \
  --root benchmarks/fixtures --required-terms logdet,solve --paragraph-context
```

Audit a derivation label:

```bash
PYTHONPATH=src python -m mathdevmcp.cli audit-derivation-v2-label \
  eq:dept-state-space-likelihood --root benchmarks/fixtures --summary-only
```

Run the release benchmark gate:

```bash
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
```

Run the seeded mathematical workbench quality report:

```bash
PYTHONPATH=src python -m mathdevmcp.cli workbench-benchmark-quality --root "$PWD"
```

Run the seeded high-level workflow quality report:

```bash
PYTHONPATH=src python -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"
```

This report measures seeded coverage and false-confidence resistance. It is
separate from external benchmark packs, release readiness, and leaderboard
claims.

## Private Corpus Validation

Private department documents and populated manifests stay outside git. Start
from `examples/private-corpus-manifest.template.json`, populate it externally,
then run:

```bash
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
scripts/validate_private_corpus.sh "$PWD"
```

For local sanitized release-gate validation without committing private files:

```bash
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json
scripts/validate_private_corpus.sh "$PWD"
```

Normal reports redact private paths.

For a strict full-profile review, configure backend, LaTeXML, and external
private-corpus evidence in the same shell:

```bash
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_REQUIRE_LATEXML=1
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

## Release Profiles

```text
base             public benchmarks, parser policy, governance, release corpus
backend          base + isolated LeanDojo backend env
latexml          base + strict LaTeXML validation
private-corpus   base + external private/sanitized manifest
full             all required release evidence
public           public industrial release product-surface gate
```

Run:

```bash
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --public
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

`full` is the strict internal/deployment profile. `public` adds CI,
packaging, MCP surface consistency, documentation synchronization, quality
gate, and redaction checks before a public industrial release claim.
`release-hypothesis-check --public` checks publication invariants and evidence
boundary language without requiring private secrets. Strict/full hypothesis
checks are opt-in because they require backend and private-corpus evidence.

## Build the Release Report

Regenerate report evidence, then build:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json \
scripts/generate_release_report_evidence.sh docs/generated/release_report

cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
```

`docs/proposal.tex` remains only as a compatibility wrapper for the release
report.

## Test

```bash
PYTHONPATH=src pytest -q
scripts/quality_gate.sh
scripts/release_smoke.sh "$PWD"
scripts/release_matrix.sh "$PWD"
```
