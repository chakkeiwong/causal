"""Refresh the hypothesis-generation master view from canonical receipts."""
from pathlib import Path
import refresh_java_effects_program_20261020 as java
source=java.source
source=source.replace('program-refresh-java-effects-v1','program-refresh-hypothesis-v1')
source=source.replace("WORK=ROOT/'docs/program/execution/2026-10-20/java-effects-v1'","WORK=ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1'")
source=source.replace('sponsor-java-effects-v2','sponsor-hypothesis-v1')
source=source.replace('causal_proposal_java_effects_reviewed','causal_proposal_hypothesis_generation_reviewed')
source=source.replace('sponsor_proposal_java_effects_reviewed_v2','sponsor_proposal_hypothesis_generation_reviewed')
source=source.replace('census-expert-averaging-v1','census-hypothesis-v1')
source=source.replace('53 inspected and 60 unread','54 inspected and 59 unread')
source=source.replace('53 inspected and 60 unread out of113','54 inspected and 59 unread out of113')
source=source.replace('after the Java effects source and proposal review.','after Java effects and hypothesis-generation reviews.')
a=source.index('        completed=[');b=source.index('        remaining=',a)
source=source[:a]+'''        completed=['Integrated Java source review and corrected sponsor citation syntax.',
            'Acquired and inspected the authentic14-page July2024 Tong article; publisher challenge and earlier58-page version preserved.',
            'Reconciled one census entry to54 inspected/59 unread while preserving116 others and14 tasks.',
            'Integrated label denominators, comparator limits, printed ANOVA discrepancies and causal graph witness.',
            'Published paired reader/sponsor and renewed exact-reader Q2-Q4.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'release-source-review.json','working-release.json','census-register.json','task-map.json']],
'''+source[b:]
source=source.replace("prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1/plan.md','Reviewed hypothesis census continuation')","prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1/plan.md','Reviewed gfoRmula continuation')")
a=source.index('## Substantive progress');b=source.index('## Required standard and remaining routes',a)
source=source[:a]+'''## Substantive progress

The hypothesis-generation discussion occupies physical PDF pages {check['physical_pages'][0]}-{check['physical_pages'][1]}.
All {check['preserved_records']} preceding citation identities/contexts and
{check['unchanged_compiled_inputs']} compiled content inputs survive. The authentic
July2024 article supplies the literature-based hypothesis design; publisher challenge
responses and the older preprint remain distinct evidence.

The argument separates literature claims, predicted links, novelty ratings and
identified interventions. Of238 model-labelled causal pairs,156 received matching
human causal labels;207 were recognized as relationships. Unequal comparator
selection, reviewer disagreement and a novelty-versus-usefulness distinction limit
transfer. A printed F/p pair and F/R2 pair do not reconcile under ordinary stated
ANOVA; the revised supplement and raw analysis remain open.

An exact graph witness has Jaccard similarity1 but zero causal effect. At assumed
value100 and cost20, treating similarity as success suggests80 while the stipulated
incremental margin is-20. Public experiments should test extraction, operational
business translation, blinded hypothesis quality and known-mechanism interventions
separately. A library/CLI/MCP contract must preserve those evidence types.

The Java review remains integrated:28 authenticated H2O/Tetrad source blobs,
confounding and smoothing references, metric-population and signed-effect limits,
and native reconciliation obligations. Its coverage outcome remains inconclusive.

The current sponsor preserves all173 earlier citations and adds4, for177 records.
Both PDFs pass source/text checks; rendered visual acceptance remains open.
The [previous master view](2026-10-20/program-refresh-hypothesis-v1/prior-current-program.md)
preserves earlier findings and limitations.

'''+source[b:]
a=source.index('The [hypothesis census plan]');b=source.index('Continue every eligible branch',a)
source=source[:a]+'''The [gfoRmula reuse plan](2026-10-20/gformula-reuse-v1/plan.md) resolves the inherited
gformula/gfoRmula aliases at commit86653ca1315f24a96a41b0ef590af13228f90ab4.
Seventeen source blobs are authenticated against the explicit root tree; technical
inspection, complete rights, decision and integration remain outstanding. Trace
intervention clocks, competing events, censoring, truncation, histories, bootstrap
unit and failure semantics before choosing a reuse disposition.

The [54/59 census](2026-10-20/census-hypothesis-v1/census-register.json) retains
candidate45 and the other unread originals. Complementary searches and citation
chaining remain eligible; do not repeat candidate42's completed primary review.
'''+source[b:]
namespace={'__name__':'refresh_hypothesis_impl','__file__':__file__}
exec(compile(source,__file__,'exec'),namespace)
if __name__=='__main__':namespace['main']()

