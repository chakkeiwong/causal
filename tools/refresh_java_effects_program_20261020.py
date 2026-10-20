"""Refresh the Java-effects master from canonical receipts, preserving history."""
import json
from pathlib import Path
import refresh_network_commercial_program_20261020 as prior

ROOT=prior.ROOT
source=(ROOT/'tools/refresh_network_commercial_program_20261020.py').read_text()
source=source.replace('network-commercial-v1','java-effects-v1').replace('sponsor-java-effects-v1','sponsor-java-effects-v2')
source=source.replace('causal_proposal_network_commercial_reviewed','causal_proposal_java_effects_reviewed').replace('sponsor_proposal_network_commercial_reviewed','sponsor_proposal_java_effects_reviewed_v2')
source=source.replace("prior_git_commit='1d046622'","prior_git_commit='7ea99d30'")
a=source.index('        completed=[');b=source.index('        remaining=',a)
source=source[:a]+'''        completed=['Authenticated28 Java source blobs and reviewed H2O/Tetrad effect semantics.',
            'Reproduced confounding, smoothing, score-population, ranking, KL-expression and signed-effect witnesses.',
            'Recorded Java effects coverage as inconclusive; full search, native reconciliation and rights stay open.',
            'Preserved fraction-check mismatch and bare sponsor citations; corrected sponsor v2 cites173 records.',
            'Published paired reader and sponsor and renewed exact-reader Q2-Q4.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'release-source-review.json','working-release.json']],
'''+source[b:]
source=source.replace("prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/java-effects-v1/plan.md','Reviewed Java effects continuation')","prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1/plan.md','Reviewed hypothesis census continuation')")
source=source.replace('Updated 20 October 2026 after gCastle reuse and commercial network/interference\ncomparisons.','Updated 20 October 2026 after the Java effects source and proposal review.')
a=source.index('## Substantive progress');b=source.index('## Required standard and remaining routes',a)
source=source[:a]+'''## Substantive progress

The Java discussion occupies physical PDF pages {check['physical_pages'][0]}-{check['physical_pages'][1]}.
All {check['preserved_records']} prior citation identities/contexts and
{check['unchanged_compiled_inputs']} compiled content inputs survive. The review
binds 28 original H2O-3 and Tetrad source blobs to pre-cutoff revisions.

The argument distinguishes conditional causal effects, response predictions,
retained-row averages, uplift ranking, signed graph-compatible slopes and minimum
absolute effects. Selected H2O training rejects weights and built-in cross-validation.
Tetrad stability selection and rank cutoffs do not provide calibrated effect intervals.

Exact authored examples give confounded observed contrast 9/25 despite zero causal
effect; assumed margins are 16 versus -20. Smoothing changes 3/5 to 1/2 without
providing missing support. Rescaling preserves rank while changing predicted means.
A literal equal-probability KL expression gives -1 versus documented 0; native
behavior remains untested. Signed slopes -2 and -1/2 give assumed margins -220/-70,
while treating magnitude as benefit gives 30. No native defect or bank result is claimed.

The proposed Java worker preserves event/treatment coding, sample selection,
missing-support behavior, numerical failure, archive roundtrips and typed outputs
through library, CLI and MCP. Full rights, remaining candidates and native
qualification stay open. The operation is inconclusive.

A fraction-check mismatch and sponsor v1 bare citation syntax were preserved.
The corrected 32-page sponsor v2 cites 173 audited records. Both current PDFs pass
source/text checks; rendered acceptance remains open. The next paper's publisher
routes returned a browser challenge; a matching pre-cutoff arXiv revision was acquired.

Earlier gCastle, network, fixed-effect, Python and LLM evidence remains integrated.
The [previous master view](2026-10-20/program-refresh-java-effects-v1/prior-current-program.md)
preserves those findings and limitations.

'''+source[b:]
a=source.index('The [Java effects plan]');b=source.index('Continue every eligible branch',a)
source=source[:a]+'''The [hypothesis census plan](2026-10-20/census-hypothesis-v1/plan.md) selects candidate 42.
Inspect the authentic July 2024 revision and distinguish literature claims, graph
links and novelty ratings from validated causal mechanisms. The
[53/60 register](2026-10-20/census-expert-averaging-v1/census-register.json) remains
unchanged until primary inspection and reconciliation are recorded.
'''+source[b:]
namespace={'__name__':'refresh_java_impl','__file__':__file__}
exec(compile(source,__file__,'exec'),namespace)
if __name__=='__main__':namespace['main']()

