"""Refresh the executable master after the commercial mediation review."""
import refresh_gformula_program_20261020 as previous

source = previous.source
source = source.replace('program-refresh-gformula-v1', 'program-refresh-mediation-v1')
source = source.replace(
    "WORK=ROOT/'docs/program/execution/2026-10-20/gformula-reuse-v1/publication-v2'",
    "WORK=ROOT/'docs/program/execution/2026-10-20/mediation-commercial-v1'")
source = source.replace('sponsor-gformula-v1', 'sponsor-mediation-v1')
source = source.replace('causal_proposal_gformula_reviewed_v2', 'causal_proposal_mediation_reviewed')
source = source.replace('sponsor_proposal_gformula_reviewed', 'sponsor_proposal_mediation_reviewed')
source = source.replace("prior_git_commit='162962e5'", "prior_git_commit='b6818bee'")
source = source.replace('after the longitudinal gfoRmula reuse review.',
                        'after longitudinal reuse and commercial mediation reviews.')
a = source.index('        completed=[')
b = source.index('        remaining=', a)
source = source[:a] + '''        completed=['Completed the gfoRmula reference review and pushed its integrated reader/sponsor as b6818bee.',
            'Inspected five commercial mediation technical manuals and one PROCESS identity lead.',
            'Recorded commercial mediation coverage and vendor comparison as inconclusive with concrete omissions.',
            'Integrated exact interaction, nonidentification, covariate-population and sensitivity examples.',
            'Preserved Unicode-minus text-check failure and published the verified reader/sponsor with exact-reader Q2-Q4.',
            'Recovered candidate45 metadata but SSRN originals returned403; census remains54/59.'],
        evidence=[ref(WORK/n,'Reviewed continuation evidence') for n in ['source-audit.json','review.json',
            'comparison-review.json','release-source-review.json','working-release.json']],
''' + source[b:]
source = source.replace(
    "prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/mediation-commercial-v1/plan.md','Commercial mediation continuation')",
    "prepared_next=ref(ROOT/'docs/program/execution/2026-10-20/cxx-effects-v1/plan.md','C++ heterogeneous-effects continuation')")
a = source.index('## Substantive progress')
b = source.index('## Required standard and remaining routes', a)
source = source[:a] + '''## Substantive progress

The commercial mediation comparison occupies physical PDF pages {check['physical_pages'][0]}-{check['physical_pages'][1]}.
All {check['preserved_records']} earlier citation identities and contexts and
{check['unchanged_compiled_inputs']} compiled content inputs survive. Five official
technical manuals, one author software-identity page and an exact authored
reference add seven citations.

Stata's natural/controlled effects, interaction and covariate averaging are
distinguished from the separate StataNow two-mediator feature. The selected
Mplus chapter separates conventional latent-response products from counterfactual
effects and identifies its single-mediator branch and moderation reference points.
No native runtime, complete entitlement or superiority is established.

An exact interaction example gives total15 as6+9 or9+6. Two randomized-offer
worlds have identical observed data but opposite natural decompositions when
mediator ignorability fails. Offering the treatment versus changing only the
mediator gives assumed margins80/-20. Covariate averaging versus evaluation at
the mean gives assumed margins5/-5. A residual-correlation range4..8 is a
sensitivity scenario set, not a confidence interval or sharp identified set.

Coverage and commercial comparison are inconclusive: SAS, IBM/AMOS and PROCESS
still need matched technical originals; broader sensitivity/negative-control
discovery, editions, rights, prices and native parity remain open. Incomplete
SAS transfers, generic Help Center shells, PROCESS TLS failure and IBM404 are
preserved. Candidate45's identity is recovered, but two SSRN routes returned403;
its original remains unread and the54/59 census is unchanged.

The sponsor preserves181 earlier citation records and adds9, for190.
Both PDFs pass source and text-bounds checks. A failed ASCII-minus assertion
was repaired by explicitly normalizing the extracted mathematical minus; no
scientific value changed. Rendered visual and final acceptance remain open.

The [previous master view](2026-10-20/program-refresh-mediation-v1/prior-current-program.md)
preserves the gfoRmula and earlier findings.

''' + source[b:]
a = source.index('The [commercial mediation plan]')
b = source.index('Continue every eligible branch', a)
source = source[:a] + '''The [C++ effects plan](2026-10-20/cxx-effects-v1/plan.md)
preserves the earlier grf native/R boundary decision. Its selected April2026
commit has a recovered nontruncated root tree. Inspect causal targets, nuisance
fitting, honesty, weights and variance semantics, and compare alternative native
forest lineages without counting aliases as separate implementations.
Bounded repository discovery is a lead, not a capability or exhaustive search.

The [candidate45 recovery](2026-10-20/census-medical-agents-v1/acquisition-review.json)
records its original-source blocker. Other unread originals and complementary
searches remain independently eligible under the
[54/59 census](2026-10-20/census-hypothesis-v1/census-register.json).
''' + source[b:]
namespace = {'__name__': 'refresh_mediation_impl', '__file__': __file__}
exec(compile(source, __file__, 'exec'), namespace)
if __name__ == '__main__':
    namespace['main']()
