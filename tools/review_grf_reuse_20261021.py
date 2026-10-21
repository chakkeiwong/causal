"""Reconcile the inherited R package entry with the preserved native-route decision."""
import hashlib
import json
from pathlib import Path

import grf_reuse_reference_20261021 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-21/grf-reuse-v1'
PRIOR = ROOT/'docs/program/execution/2026-10-20/cxx-effects-v1'
RAW = ROOT/'docs/literature/raw'
OP = 'SW.DECISION.inherited_grf'
NATIVE = ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.seed_080/decision.json'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Selected source inspection is not a full distribution, dependency lock or rights audit.',
    'Pinned 30 April 2026 source declares 2.6.1; no current-release, support-SLA or installed-compatibility claim.',
    'The inherited R package and native core are one engine lineage with different integration routes.',
    'No upstream R/C++ code or upstream tests executed; fixed-law examples do not qualify runtime or coverage.',
    'General dependence, missing data, continuous treatment, IV, multiarm, survival and adaptive policies are excluded from the initial profile.',
    'Mandatory repairs, Q1/Q5, rendered visual review and final acceptance remain open.']


def main():
    assert not (BASE/'source-audit.json').exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    native = read(NATIVE)
    verify_bindings(native)
    assert native['integration_allowed'] is False
    identity = read(PRIOR/'identity-selection.json')
    authenticated = read(PRIOR/'grf-authenticated-sources.json')
    selection = read(PRIOR/'grf-source-selection.json')
    assert identity['commit'] == authenticated['commit'] == selection['commit'] == native['engine']['commit']
    write(BASE/'plan-review.json', dict(status='pass', evidence=[ref(BASE/'plan.md','Existing reviewed scope'),
        ref(NATIVE,'Preserved completed native-route decision')], checks=[
        'Resolve the inherited package as an alias of the native lineage without counting another engine.',
        'Inspect R target selection, score construction, OOB and supplied nuisance provenance, method restrictions and license.',
        'Derive conditional score bias and target-switch economics using exact independent enumeration.',
        'Choose a proposal reference disposition; bind future conversion, qualification, costs and owners.',
        'Integrate only new wrapper-specific argument and preserve the existing native analysis.']))
    specs = [
        (0, 155, 177, 'GPL section 2 distinguishes running/non-conveying from conveying; process isolation alone does not resolve distribution obligations.'),
        (0, 195, 215, 'Source conveyance preserves notices/license; modification notices and dates are required under stated terms.'),
        (1, 1, 46, 'Version, maintainer, tracker, R/C++ requirements, GPL-3, imports and optional dependencies.'),
        (7, 154, 235, 'Default arguments, nuisance regression calls, accepted supplied vectors and residualization; length checks cannot establish provenance.'),
        (7, 276, 298, 'Forest object retains original observations and nuisance predictions; data handling must cover serialized artifacts.'),
        (7, 300, 339, 'OOB versus new-data prediction, column order, CATE variance and error diagnostics have distinct meanings.'),
        (7, 378, 436, 'Cached OOB branch, explicit newdata/native prediction dispatch; local-linear sample weights unsupported.'),
        (8, 47, 106, 'Binary debiasing weights and reconstructed outcome regressions produce AIPW scores.'),
        (9, 1, 59, 'All/treated/control/overlap targets, cluster target weights and baseline-only subset warning.'),
        (9, 126, 170, 'TMLE rejects cluster/sample weights; subset must span more than one cluster.'),
        (9, 172, 201, 'Extreme-propensity guidance is a warning, not automatic rejection or target replacement.'),
        (9, 204, 250, 'All-sample AIPW aggregates scores and centered cluster sums.'),
        (9, 269, 312, 'Overlap branch uses residual regression and sandwich standard errors; method label is ignored there.'),
    ]
    extracts, records = [], {}
    for index, lo, hi, finding in specs:
        p = RAW/f'exec20_cxx_effects_grf_{index:02}.txt'
        source = next(s for s in authenticated['sources'] if s['local_path'] == str(p.relative_to(ROOT)))
        selected = next(s for s in selection['selected'] if s['index'] == index)
        b = p.read_bytes()
        assert hashlib.sha256(b).hexdigest() == source['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == source['git_blob_sha1'] == selected['git_blob_sha1']
        receipt = p.with_suffix('.receipt.json')
        acquisition = read(receipt)
        assert acquisition['status'] == 'saved' and acquisition['sha256'] == source['sha256']
        lines = p.read_text().splitlines(keepends=True)
        assert hi <= len(lines)
        text = ''.join(lines[lo-1:hi])
        extracts.append(dict(source=ref(p, selected['path']), lines=[lo, hi], finding=finding,
            excerpt=text, excerpt_sha256=hashlib.sha256(text.encode()).hexdigest()))
        records[index] = dict(source_identity=acquisition['url'], local_copy=ref(p, selected['path']),
            acquisition=ref(receipt,'Preserved acquisition'), git_blob_sha1=selected['git_blob_sha1'])
    write(BASE/'inspected-extracts.json', dict(anchors=extracts, native_execution=False))
    write(BASE/'exact-results.json', exact.calculate())
    write(BASE/'identity-review.json', dict(repository='grf-labs/grf',commit=identity['commit'],
        root_tree=identity['root_tree'], commit_date=identity['commit_date'], version='2.6.1',
        aliases=['inherited:grf','seed:080 native core'], distinct_engine_count=1,
        routes=['R package wrapper','native embedding/port'], previous_decision=ref(NATIVE,'Preserved native decision'),
        license_declaration='DESCRIPTION GPL-3; native headers may grant GPL-3-or-later; preserve per-file terms.',
        dependencies=dict(runtime='R >=3.5.0', build=['C++17','GNU make'], linking=['Rcpp','RcppEigen'],
            imports=['DiceKriging','lmtest','Matrix','methods','Rcpp >=0.12.15','sandwich >=2.4-0']),
        rights='Running the original and distributing a combined work are distinct questions; full source/dependency review remains.',
        maintenance='Dated commit, named maintainer and issue tracker; earlier build/test source inspection retained. No test execution or SLA.',
        evidence=[ref(PRIOR/'grf-authenticated-sources.json','Pinned source authentication'),
            ref(BASE/'inspected-extracts.json','Primary anchors')]))
    claims = [
        'Binary scores reconstruct both treatment-specific outcome regressions from m, e and tau; their DR interpretation is about these surfaces and propensity.',
        'The all, treated, control and overlap options define different target populations.',
        'The overlap branch fits residual OLS and ignores AIPW/TMLE selection; TMLE with clusters or sample weights is explicitly rejected earlier.',
        'Supplied nuisance vectors have length checks; provenance, split integrity and causal assumptions are not thereby verified.',
        'OOB prediction and newdata prediction follow distinct paths; CATE variance, R-loss and Monte Carlo error are different outputs.',
        'A pinned R worker remains a relevant reference candidate; source inspection does not grant runtime admission.']
    software = dict(integrated_citation_key='exec21_grf_reuse',kind='software_primary_source',
        title='grf R package target selection and nuisance semantics at the April 2026 revision',
        author='grf contributors',year=2026,source_identity='https://github.com/grf-labs/grf/tree/'+identity['commit'],
        version_date='2.6.1 declared; 30 April 2026 pinned commit',cutoff='2026-10-07',
        local_copy=ref(BASE/'identity-review.json','Pinned identity, aliases, rights and dependencies'),
        primary_sources=list(records.values()), inspected_anchors=[
            dict(anchor=f'{Path(x["source"]["path"]).name} lines {x["lines"][0]}-{x["lines"][1]}',
                finding=x['finding'],evidence=ref(BASE/'inspected-extracts.json','Verbatim inspected ranges')) for x in extracts],
        supported_claims=claims,limitations=LIMITS)
    project = dict(integrated_citation_key='exec21_grf_reference',kind='project_derivation',
        title='Exact binary forest score-bias and target-population witnesses',author='Causal banking proposal project',
        year=2026,source_identity='tools/grf_reuse_reference_20261021.py',version_date='21 October 2026',
        local_copy=ref(ROOT/'tools/grf_reuse_reference_20261021.py','Independent rational enumeration'),
        inspected_anchors=[ref(BASE/'exact-results.json','Four nuisance cases and four population targets')],
        supported_claims=['Correct marginal outcome mean and conditional effect with wrong propensity can yield 3/2 instead of true 2.',
            'Correct propensity or both correctly reconstructed outcome surfaces recover 2 in the stipulated law.',
            'Equal groups with propensities 1/2 and 1/10 and effects -4 and 12 have ATE 4, ATT -4/3, ATC 44/7 and overlap effect 4/17.',
            'Assumed cost 2 gives customer-population margin 2 and overlap-population margin -30/17.'],
        limitations=exact.calculate()['limits'])
    write(BASE/'source-audit.json',dict(sources=[software,project],cutoff='2026-10-07'))
    contract = dict(status='proposed_not_implemented',integration_allowed=False,
        initial_profile=native['target_and_exclusions'], inherited_boundary=ref(
            ROOT/'docs/program/comprehensive-v14/work/IN.DESIGN.Cxx/adapter-contract.json','Existing bounded worker contract'),
        inputs=['Immutable request identity, feature order, customer keys, action/outcome coding, units and fixed horizon.',
            'Explicit all-population AIPW target; no silent treated/control/overlap substitution.',
            'Nuisance origin, fold/time provenance, seed and thread configuration; external fitted vectors excluded initially.',
            'Dependency/compiler/RNG/source versions and process limits.'],
        outputs=['Target, population and actual estimator identifier, scalar score aggregate and separately labeled standard error.',
            'All warnings and support diagnostics, original request hash, completed status and provenance.',
            'CATE predictions, R-loss, Monte Carlo error and confidence statements remain separate typed fields.'],
        exclusions=native['target_and_exclusions']['excluded'],
        failures=native['failure_contract'], prototype_oracles=[
            ref(BASE/'exact-results.json','Fixed-law bias and target-change witnesses'),
            ref(ROOT/'docs/program/execution/2026-10-13/grf-cxx/oracle-results.json','Existing exact conversion and variance oracle')],
        qualification=['Run original R package on declared data only after environment preparation.',
            'Compare supplied fixed-score fixtures, actual predictions, aggregation, serialization and refusal/fault behavior.',
            'Test warnings, target/method combinations, OOB versus newdata, and time/fold leakage guards.',
            'Register separate public-data calibration and cost studies; retain failed fits in the denominator.'])
    write(BASE/'conversion-contract.json',contract)
    omissions = [
        ('Runtime and uncertainty','Future prototype owner','Freeze full environment and compare original R output with the exact and generated-law oracles.'),
        ('Rights and dependencies','Future distribution owner','Review complete source/dependency licenses and actual distribution architecture; isolation is not a license exemption.'),
        ('Dependence and extra methods','Method reviewer','Separate IV, multiarm, survival, repeated-action and dependent-data contracts and source reviews.'),
        ('Maintenance and costs','Prototype/operator owner','Inspect release changes and measure matched preprocessing, training, serialization, review and support costs.'),
        ('Independent and visual acceptance','Independent reviewer / fresh visual session','Review complete proposal and rendered pages without relabeling text bounds as visual inspection.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[
        dict(item=n,owner=o,next_action=a,status='open') for n,o,a in omissions]))
    evidence = [ref(BASE/n,'Reviewed scoped reuse evidence') for n in ['identity-review.json','source-audit.json',
        'inspected-extracts.json','exact-results.json','conversion-contract.json','omissions-register.json']]
    decision = dict(operation=OP,status='pass',decision='reference',capabilities=[],integration_allowed=False,
        scope='Retain pinned original grf R package as the binary independent-customer AIPW reference candidate; no executable admission.',
        canonical_aliases=['inherited:grf','seed:080'],distinct_engine_count=1,prior_native_decision=ref(NATIVE,'Preserved route decision'),
        alternatives=[
            dict(choice='integrate_original_R_worker',disposition='candidate_after_qualification',
                reason='Preserves wrapper nuisance and score/target semantics plus native code; process isolation still needs rights and full runtime qualification.'),
            dict(choice='direct_native_adoption_or_port',disposition='reject_initial_route',
                reason='Existing native decision remains: duplicate preprocessing/statistical/lifetime ownership without measured benefit.'),
            dict(choice='Bayesian_bcf_XBCF_flexBCF',disposition='separate_comparators',
                reason='Posterior targets, priors, scale restoration and uncertainty differ; source hazards and historical evidence require their own qualification.'),
            dict(choice='reject_entire_package',disposition='not_selected',
                reason='A source-grounded, scoped binary-effect method is relevant; limitations support comparison rather than wholesale rejection.')],
        costs='No observed comparative runtime, integration price or bank ROI. Measure data validation, nuisance fits, training, scoring, serialization, review and operational support jointly.',
        owner_obligations=[dict(owner=o,obligation=a) for _,o,a in omissions],
        revisit_trigger='Changed source, target, nuisance provenance, dependence law, distribution terms, or decision to build a prototype.',
        limitations=LIMITS,evidence=evidence)
    output=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_grf/decision.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    write(output,decision)
    write(BASE/'review.json',dict(status='pass',scope=decision['scope'],
        reviewer=dict(name='Codex author/coordinator',kind='author'),findings=claims,
        evidence=evidence+[ref(output,'Complete reference disposition')],limitations=LIMITS,
        native_execution=False,visual_acceptance=False))
    graph,_,_=run.combined(ROOT,state)
    node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    ev=evidence+[ref(BASE/'plan-review.json','Plan review'),ref(BASE/'review.json','Author review'),ref(Path(__file__),'Exact review construction')]
    findings=[
        'Resolve inherited R and native-core alias at one authenticated commit; bind target, dependencies, rights and maintenance limits.',
        'Compare worker, port and Bayesian alternatives with exact target/bias examples, uncertainty distinctions, costs and explicit owner obligations.',
        'Reference decision completes a proposal disposition while denying runtime capability; native decision and later qualification duties are preserved.']
    assert len(node['criteria'])==len(findings)
    receipt.update(outcome='pass',execution='performed',scope=decision['scope'],
        reviewer=dict(name='Codex author/coordinator',kind='author'),limitations=LIMITS,
        original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Contracted inherited grf decision')],
        nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i,verdict='pass',finding=f,evidence=ev) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings(read(BASE/'source-audit.json'))
    verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(decision='reference',proposal_review='pass',integration_allowed=False,
        inspected_sources=len(records),exact_checks=exact.calculate()['algebra_grid_checks'])))


if __name__=='__main__':
    main()
