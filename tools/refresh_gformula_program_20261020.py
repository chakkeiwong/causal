"""Refresh the executable program after the gfoRmula proposal review."""
import refresh_hypothesis_program_20261020 as previous

source = previous.source
source = source.replace('program-refresh-hypothesis-v1', 'program-refresh-gformula-v1')
source = source.replace(
    "WORK=ROOT/'docs/program/execution/2026-10-20/census-hypothesis-v1'",
    "WORK=ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1/publication-v2'")
source = source.replace('sponsor-hypothesis-v1', 'sponsor-gformula-v1')
source = source.replace('causal_proposal_hypothesis_generation_reviewed',
                        'causal_proposal_gformula_reviewed_v2')
source = source.replace('sponsor_proposal_hypothesis_generation_reviewed',
                        'sponsor_proposal_gformula_reviewed')
source = source.replace("prior_git_commit='7ea99d30'", "prior_git_commit='162962e5'")
source = source.replace('after Java effects and hypothesis-generation reviews.',
                        'after the longitudinal gfoRmula reuse review.')
a = source.index('        completed=[')
b = source.index('        remaining=', a)
source = source[:a] + '''        completed=['Authenticated17 original gfoRmula source blobs and resolved same-project aliases.',
            'Completed the reference disposition; no native runtime or distribution approval.',
            'Integrated intervention histories, competing events, clipping and failed-bootstrap semantics.',
            'Reproduced exact policy margins9.50/3.50 and competing-event loss difference50.40.',
            'Preserved equation-overflow failure; published corrected reader and paired sponsor with exact-reader Q2-Q4.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'release-source-review.json','working-release.json']],
''' + source[b:]
source = source.replace(
    "prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1/plan.md','Reviewed gfoRmula continuation')",
    "prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/mediation-commercial-v1/plan.md','Commercial mediation continuation')")
a = source.index('## Substantive progress')
b = source.index('## Required standard and remaining routes', a)
source = source[:a] + '''## Substantive progress

The gfoRmula discussion occupies physical PDF pages {check['physical_pages'][0]}-{check['physical_pages'][1]}.
All {check['preserved_records']} prior citation identities and contexts, and
{check['unchanged_compiled_inputs']} compiled content inputs survive. Seventeen
original source blobs are authenticated to the selected November 2025 tree.
The source declares1.1.2 while its release date is TBD.

The bounded reuse decision is reference. A proposed original R worker must
preserve target types, covariate/intervention order, history conventions,
competing-event priority, clipping, person-level resampling and failed replicate
counts. A port or direct adoption remains unqualified; complete rights,
dependencies, native behavior and broader dependence require later work.

An exact two-period law gives beneficial-outcome probabilities13/100,3/5,17/40
for never, always and dynamic policies. Substituting a mean history before the
dynamic decision gives73/200. At assumed value100 and fixed incremental cost20,
proper versus shortcut margins are9.50/3.50. Competing-event retention versus
elimination gives.3096/.36 and loss difference50.40 at assumed loss1000.
Separate clipping and selective-bootstrap examples expose scientific semantics
without asserting a measured native defect or bank result.

A two-column equation overflow was preserved and repaired in publication-v2.
The sponsor preserves177 earlier citation records and adds4, for181.
Both PDFs pass source and text-bounds checks; rendered acceptance remains open.
The previous hypothesis and Java findings remain integrated.

The [previous master view](2026-10-20/program-refresh-gformula-v1/prior-current-program.md)
preserves the earlier substantive findings and remaining limits.

''' + source[b:]
a = source.index('The [gfoRmula reuse plan]')
b = source.index('Continue every eligible branch', a)
source = source[:a] + '''The [commercial mediation plan](2026-10-20/mediation-commercial-v1/plan.md)
starts from the failed inherited query and genuine saved Stata original.
An inherited SAS PDF fails trailer/page validation; it supports no technical
claim. Inspect complete vendor originals and distinguish natural, controlled
and interventional effects, interaction and sensitivity assumptions. The
candidate list includes Stata, SAS, Mplus, IBM and the separate PROCESS extension;
no family receives coverage from another vendor's source.

The independent [candidate45 recovery](2026-10-20/census-medical-agents-v1/plan.md)
has matched OpenAlex and Crossref identity records. Its genuine original and
version remain to be inspected. Metadata is not technical evidence. The
[54/59 census](2026-10-20/census-hypothesis-v1/census-register.json) is unchanged.
''' + source[b:]
namespace = {'__name__': 'refresh_gformula_impl', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
if __name__ == '__main__':
    namespace['main']()
