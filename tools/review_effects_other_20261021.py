#!/usr/bin/env python3
"""Inspect pinned Julia sources and retain bounded other-language discovery."""
import json
from pathlib import Path
import effects_other_reference_20261021 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-21/effects-other-v1'
OP = 'SW.CELL.effects_heterogeneity.other_relevant'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Four newly inspected Julia revisions plus matching CausalInference evidence do not complete all other-language coverage.',
    'Repository and registry queries are current metadata acquired21October2026; creation/commit filters do not authenticate historical descriptions or complete release histories.',
    'First20 search/registry results are bounded leads, not a census; Rust technical originals and wider language searches remain open.',
    'No Julia engine, vendor, live model, native adapter or bank data was executed; source analysis and exact authored algebra are distinct.',
    'The CausalForest archive exceeded the requested curl16MiB limit; actual bytes and failure of limit enforcement are preserved. Subsequent discovery uses streamed byte limits.',
    'MIT licenses were inspected for four archives; dependency rights, supported environments and deployment obligations still need review.',
    'Package manuscript Markdown and citations in source code are not admitted as scholarly PDFs.',
    'Visual acceptance awaits a fresh session allowance; Q1/Q5, mandatory repairs and final proposal acceptance remain open.'
]


def source(name, title, specs, claims):
    versions = {r['name']: r for r in read(BASE/'version-selection.json')['entries']}
    archives = {r['name']: r for r in read(BASE/'archive-inspection.json')['records']}
    identity, archive = versions[name], archives[name]
    verify_bindings(archive)
    records = []
    for filename, ranges in specs:
        p = BASE/'sources'/name/filename
        lines = p.read_text().splitlines(keepends=True)
        anchors = []
        for lo, hi in ranges:
            hi = len(lines) if hi is None else hi
            assert 1 <= lo <= hi <= len(lines), (name, filename, lo, hi, len(lines))
            anchors.append(dict(anchor=f'lines {lo}-{hi}', inspected_text=''.join(lines[lo-1:hi])))
        records.append(dict(source_identity=identity['repo'].removesuffix('.git')+'/blob/'+identity['commit']+'/'+filename,
            local_copy=ref(p, 'Unmodified pinned primary source'), inspected_anchors=anchors, executed=False))
    version = next(line.split('"')[1] for line in (BASE/'sources'/name/'Project.toml').read_text().splitlines() if line.startswith('version ='))
    return dict(integrated_citation_key='exec21_effects_'+name.lower(), kind='software_primary_sources',
        title=title, author=name+'.jl contributors', year=2026,
        year_meaning='Inspection year; revision and declared version stated separately',
        source_identity=identity['repo'], version_date=f'{version}; {identity["commit"]}; {identity["committer_date"]}',
        local_copy=archive['archive'], acquisition_receipt=archive['receipt'], records=records,
        identity_evidence=[ref(BASE/'version-selection.json', 'Selected pre-cutoff revisions')],
        inspected_anchors=[dict(anchor='Pinned technical files and license', inspection='See per-file exact inspected text')],
        supported_claims=claims, limitations=LIMITS)


def main():
    assert not (BASE/'source-audit.json').exists()
    verify_bindings(read(BASE/'archive-inspection.json'))
    write(BASE/'plan-review.json', dict(status='pass', reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md', 'Six-step continuation plan')],
        checks=['Separate identity discovery from technical inspection and native qualification.',
                'Review estimand, sampling unit, outcome units, assignment law, missingness and source/target population together.',
                'Use exact finite laws with independent probability enumeration; preserve source defects without editing upstream originals.',
                'Record bounded Rust leads and unavailable scholarly originals; incomplete census stays inconclusive.',
                'Integrate a preserving successor, renew exact-reader reviews and continue independently eligible work.']))
    receipt = read(BASE/'acquisition/sources-network/CausalForest.receipt.json')
    assert receipt['returncode'] == 0 and receipt['bytes'] == 17486799 > 16777216
    write(BASE/'acquisition-limit-review.json', dict(status='observed_limit_enforcement_failure',
        requested_bytes=16777216, observed_bytes=receipt['bytes'], excess_bytes=receipt['bytes']-16777216,
        evidence=[ref(BASE/'acquisition/sources-network/CausalForest.receipt.json', 'Actual returned bytes'),
                  ref(ROOT/'tools/acquire_transport_details_20261021.py', 'Inherited curl --max-filesize request'),
                  ref(ROOT/'tools/acquire_effects_other_discovery_20261021.py', 'Successor checks streamed byte count'),
                  ref(BASE/'archive-inspection.json', 'Bounded inert extraction')],
        cause='Not established; curl option did not bound this observed transfer.',
        disposition='Preserve actual complete archive/hash; do not assert16MiB enforcement. Extraction limits held. Future reads check streamed bytes.',
        downloaded_code_executed=False, global_blocker=False))
    common = [('Project.toml', [(1,None)]), ('LICENSE', [(1,None)])]
    sources = [
        source('CausalELM', 'CausalELM.jl effects, cross-fitting and uncertainty source', common+[
            ('Manifest.toml', [(1,5)]), ('src/estimators.jl',[(323,445)]),
            ('src/utilities.jl',[(187,208)]), ('src/metalearners.jl',[(435,472),(493,504)]),
            ('src/inference.jl',[(190,212),(300,333),(361,369)])], [
                'G-computation averages all covariates for ATE/ITT/CATE labels and restricts the other branch to treated rows; ITT requires the supplied T to represent assignment.',
                'Selected S/T learners return fitted individual contrasts; no uniform CATE band follows from returning a vector.',
                'DML averages foldwise residual least-squares coefficients; generate_folds uses contiguous row slices.',
                'Generic null construction draws uniform labels or uniform values over the treatment range rather than preserving actual treatment counts/assignment law.',
                'The source stderr expression is squared deviations/(n-1)/sqrt(n), hence has squared-outcome units and scales quadratically.',
                'The reported interval searches a grid using the same null tail comparisons; valid general inversion is not established by this code.',
                'Root Manifest declares Julia1.11.1; Project declares0.8.0 and a Julia compatibility expression, not a tested deployment here.']),
        source('CausalForest', 'CausalForest.jl tree honesty, centering and prediction source', common+[
            ('src/CausalForest.jl',[(1,None)]), ('src/causal/main.jl',[(1,16),(137,323),(325,419)]),
            ('src/causal_ols/main.jl',[(267,333)])], [
                'Selected forest interface distinguishes split and leaf samples when honest, with bootstrap/subsampling controls.',
                'Outcome-centering forest is fitted before the per-tree honest split, using the chosen treatment arm.',
                'Prediction normalizes within-leaf treated/control weights and returns centered-outcome contrasts.',
                'Inspected apply_forest/apply_forest_ols return point predictions; these paths provide no calibrated variance object.',
                'Tree honesty alone does not prove separation of nuisance fitting or establish parity with another forest library.',
                'DecisionTree0.10 and plotting/image dependencies appear in the declared environment; runtime reproduction remains unperformed.']),
        source('TMLE', 'TMLE.jl targeted estimation, influence scales, missingness and table extension', common+[
            ('src/counterfactual_mean_based/estimators.jl',[(1,182),(195,230)]),
            ('src/counterfactual_mean_based/gradient.jl',[(1,78)]),
            ('src/counterfactual_mean_based/estimates.jl',[(38,111)]),
            ('src/estimators.jl',[(64,85),(299,306),(360,366)]),
            ('src/testing.jl',[(1,5)]), ('src/utils.jl',[(31,82),(252,274)]),
            ('src/resampling.jl',[(1,None)]), ('docs/src/user_guide/missingness.md',[(1,None)]),
            ('ext/CausalTablesExt.jl',[(1,None)])], [
                'Tmle/Ose expose nuisance models, resampling and propensity truncation; default noncollaborative resampling is nothing.',
                'Tmle implementation has weighted=true although adjacent constructor prose says false; adapters must bind actual configuration.',
                'TMLEstimate stores std(IC) and n, and testing forwards both; std is the influence-function scale, not already the standard error.',
                'Joint estimates use covariance of stacked influence curves, requiring alignment of contributing units; author review requires explicit IDs.',
                'Relevant-variable incomplete rows are dropped; non-CV propensity fits can use additional observed treatment/confounder rows.',
                'Case-control mode accepts a prevalence Float64; external prevalence uncertainty is not an input to these inspected interfaces.',
                'CausalTables extension converts treatment columns to categorical data and identifies using supplied ct.causes; supplied graph truth is an assumption.']),
        source('CausalTables', 'CausalTables.jl supplied-SCM intervention and Monte Carlo references', common+[
            ('src/estimands.jl',[(1,13),(42,54),(73,78),(116,123),(161,170)]),
            ('docs/src/man/ground-truth.md',[(1,None)])], [
                'Interventions and draws use a supplied StructuralCausalModel, with summaries recomputed before conditional outcome draws.',
                'cfmean and cfdiff approximate supplied-model counterfactual means by Monte Carlo.',
                'Inspected return tuples contain only mu despite efficiency-bound wording in their documentation.',
                'Known simulator truth is useful for public comparisons but does not identify an unknown observational mechanism.',
                'Network conditional summaries are supported only for documented available closed forms; simulation summaries do not establish dependent-sample uncertainty.'])]
    searches = []
    candidates = []
    for name in ['rust_repos','rust_effect_repos','crates_causal','crates_treatment']:
        p=BASE/'acquisition/discovery-network'/(name+'.json')
        r=read(p.with_suffix('.receipt.json'));assert r['status']=='complete_metadata_only'
        d=read(p);items=d.get('items',d.get('crates',[]))
        total=d.get('total_count',d.get('meta',{}).get('total'))
        searches.append(dict(query=name, source_identity=r['url'], total_reported=total, inspected_records=len(items),
            incomplete_results=d.get('incomplete_results'), local_copy=ref(p,'Discovery metadata only'),
            receipt=ref(p.with_suffix('.receipt.json'),'Public read; current index; cutoff limits')))
        for item in items:
            date=item.get('created_at','')
            candidates.append(dict(search=name, name=item.get('full_name',item.get('name')),
                source_identity=item.get('html_url',item.get('repository')), description=item.get('description'),
                created_at=date, status='post_cutoff_identity_omitted' if date[:10]>'2026-10-07' else 'metadata_lead_technical_original_unread',
                next_action='Recover selected pre-cutoff release, Cargo/license and actual estimator code; disambiguate statistical effects from distributed/event causality.',
                capability_verified=False, absence_claim=False))
    write(BASE/'complementary-search-review.json',dict(searches=searches, candidates=candidates,
        stopping_rule='Four fixed first-page queries, at most20 results each; inspect all returned metadata, defer source claims.',
        cutoff='2026-10-07', coverage_complete=False,
        limitations=['GitHub created filter is not a source-version filter; current description may be later.',
            'Crates queries have no cutoff filter; post-cutoff identities are explicitly excluded.',
            'No pagination, dependent-package search or wider languages completed. Zero exact-phrase hits are not absence evidence.']))
    sources.append(dict(integrated_citation_key='exec21_effects_discovery',kind='official_registry_metadata',
        title='Bounded Rust repository and crate discovery for causal effects',author='GitHub and crates.io',year=2026,
        source_identity='Fixed official GitHub/crates.io search endpoints',version_date='21October2026 acquisition;7October cutoff with stated limits',
        local_copy=ref(BASE/'acquisition/discovery-network/rust_repos.json','Official discovery response'),
        records=searches, inspected_anchors=[dict(anchor='First returned pages',inspection='All returned names/descriptions inspected as leads')],
        supported_claims=['Current bounded queries return additional Rust candidate identities; no technical functionality or historical-description claim.'],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec21_effects_reference',kind='project_authored_exact_reference',
        title='Exact target, uncertainty-scale, response-selection and supplied-SCM witnesses',author='Causal banking proposal project',year=2026,
        source_identity='tools/effects_other_reference_20261021.py',version_date='21October2026 exact authored laws',
        local_copy=ref(ROOT/'tools/effects_other_reference_20261021.py','calculate(): rational finite-law enumeration'),
        inspected_anchors=[dict(anchor='calculate()',inspection='ATE/ATT/residual slopes, response weighting, dimensional and observed-law equality checks')],
        supported_claims=['ATE4, ATT-4/3 and residual slope4/17 differ; cost2 margins2 and-30/17.',
            'MAR response selection changes complete-case mean effect to-12/5; correct known-law response weighting recovers4.',
            'Outcome scale100 gives source-expression scale10000; four binary label draws preserve one-treatment design with probability1/4.',
            'Two SCMs have identical observed law and effects1/0; supplied truth does not settle which model generated bank data.',
            'Influence values(-3,-1,1,3) yield variance20/3 and mean variance5/3.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'exact-results.json',exact.calculate())
    rows=[dict(name=s['title'].split(' ')[0],status='pinned_primary_inspection',source=ref(BASE/'source-audit.json',s['integrated_citation_key'])) for s in sources[:4]]
    rows.append(dict(name='CausalInference.jl',status='matching_revision_graphical_scope_only',
        prior=ref(ROOT/'docs/program/execution/2026-10-19/other-identification-v1/source-audit.json','Same459d654d revision; reviewed graphical adjustment'),
        inspection=ref(ROOT/'docs/literature/raw/exec19_oid_julia_0.txt','Module exports and includes inspected; no heterogeneity qualification implied')))
    write(BASE/'candidate-register.json',dict(julia_candidates=rows,rust_leads=candidates,
        aliases=['CausalELM/CausalELM.jl','CausalForest/CausalForest.jl','TMLE/TMLE.jl','CausalTables/CausalTables.jl','CausalInference/CausalInference.jl'],
        coverage_complete=False,negative_absence_claims=[],broader_languages='unresolved'))
    write(BASE/'omissions-register.json',dict(global_blocker=False,
        source_gaps=['Inspect pinned Rust effect candidates including perpetual, causalkit, oxicuda-causal and propensity-score; exact technical scope/versions unknown.',
            'Complete pagination, alias searches, complementary registries and non-Julia/Rust language coverage.',
            'Recover genuine original PDFs for package papers before any scholarly citation; Markdown is not a PDF.',
            'Inspect full native environments, dependency rights, actual failure behavior, RNG and reproducibility.',
            'Qualify CATE uncertainty, dependent sampling, target support and optional prevalence uncertainty separately.'],
        evidence=[ref(BASE/'complementary-search-review.json','Bounded discovered leads'),ref(BASE/'acquisition-limit-review.json','Preserved collector failure')],
        native_execution=False,expensive_bank_experiment_required_for_next_work=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        requirements=['Use isolated Julia worker with pinned project/manifest/dependencies and explicit method/version.',
            'Declare treatment assignment versus receipt, contrast levels, source/target population, unit IDs, row order, missingness and sampling units.',
            'Carry ATE/ATT/CATE/residual-coefficient kind explicitly; preserve fold membership and actual nuisance training rows.',
            'Export influence values and corresponding unit IDs with n and covariance meaning; standard deviation is not standard error.',
            'Keep every failure, empty arm, missing overlap and unsupported uncertainty result visible; do not invent intervals.',
            'Preserve ct.causes provenance, categorical level order and exact graph-to-adjustment mapping through library/CLI/MCP.',
            'Use public fixed-law scalar/scale/assignment/missingness/graph witnesses before selecting expensive native or bank experiments.'],
        provisional_options={'CausalELM':'Retain point-estimation candidate; reject unqualified uncertainty reuse at this revision pending repair and fresh qualification.',
            'CausalForest':'Defer calibrated inference; compare exact prediction/nuisance semantics before claiming equivalence to grf.',
            'TMLE':'Prioritize bounded native worker design; preserve influence scale, missingness target and supplied graph assumptions.',
            'CausalTables':'Prioritize public reference-generation and typed-data design; retain SCM and Monte Carlo uncertainty.',
            'CausalInference':'Reuse graphical contract only; effect estimation needs an additional validated method.'},
        formal_reuse_operation_completed=False))
    evidence=[ref(BASE/n,'Reviewed other-language effects evidence') for n in ['plan.md','plan-review.json','source-audit.json',
        'candidate-register.json','complementary-search-review.json','omissions-register.json','conversion-contract.json','exact-results.json','acquisition-limit-review.json']]
    evidence.append(ref(Path(__file__),'Exact author review construction'))
    findings=[('inconclusive','Five Julia identities and bounded Rust leads are explicit; full complementary coverage remains open.'),
        ('pass','Pinned technical originals, versions, MIT text, exact inspected anchors and authored witnesses support the scoped claims.'),
        ('pass','Source gaps, inference defects, rights/runtime uncertainty and alternative targets remain explicit; no absence or native parity claim.')]
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    item=dict(operation_id=OP,status='inconclusive',scope='Selected Julia effects source review and bounded Rust metadata discovery',
        reviewer=REVIEWER,criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],
        evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False)
    write(output,item);write(BASE/'review.json',item);verify_bindings(item)
    state=run.core.read(ROOT,run.core.STATE);assert state['execution_runtime']['active']['operation']==OP
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope=item['scope'],reviewer=REVIEWER,
        outputs=[ref(output,'Selected source review; coverage incomplete')],capabilities=[],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger='Complete recorded source/census obligations and native target-specific public qualification.',
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps(dict(operation=OP,outcome='inconclusive',new_audited_sources=len(sources),rust_metadata_records=len(candidates))))


if __name__=='__main__':main()
