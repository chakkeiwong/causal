#!/usr/bin/env python3
"""Bind a pinned compatibility-wrapper review without admitting an adapter."""
import hashlib
import json
from pathlib import Path

import gsynth_reference_20261021 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
ROOT = run.core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-21/gsynth-reuse-v1'
OP = 'SW.DECISION.inherited_gsynth'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Selected original source inspection, not native R/C++ execution, a full dependency audit or measured coverage.',
    'Pinned gsynth 1.4.0 delegates to fect; selected fect 2.4.5 is a reviewed dependency candidate, not an installed lock.',
    'MIT + file LICENSE declarations and holder/year files are inspected; full standard template and dependency rights remain unreviewed.',
    'No genuine local Xu 2017 original was recovered for this review; package comments are not a substitute for a scholarly paper.',
    'Rank-two examples are authored deterministic counterexamples outside full pre-factor-rank qualification, not qualified-engine failures.',
    'No universal missingness, dependence, factor selection, bootstrap or economic validity is established.',
    'Rendered visual review, mandatory repairs and final proposal acceptance remain open.']


def main():
    assert not (BASE/'source-audit.json').exists()
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    selection = read(BASE/'version-selection.json')
    archives = read(BASE/'archive-inspection.json')
    verify_bindings(selection); verify_bindings(archives)
    selected = {r['name']: r for r in selection['entries']}
    archived = {r['name']: r for r in archives['records']}
    assert all(selected[k]['commit'] == v['commit'] for k,v in archived.items())
    equal = []
    for name in ['R/default.R','man/gsynth.Rd','LICENSE','NEWS.md']:
        up, cr = [BASE/'sources'/k/name for k in ['gsynth_upstream','gsynth_cran']]
        assert up.read_bytes() == cr.read_bytes()
        equal.append(dict(path=name,upstream=ref(up,'Pinned upstream'),cran=ref(cr,'Identical CRAN text')))
    write(BASE/'plan-review-v2.json',dict(status='pass',evidence=[ref(BASE/'plan.md','Reviewed proposal scope')],checks=[
        'Bind wrapper and selected engine separately; recover failed historical identity without overwriting it.',
        'Read complete wrapper and selected engine paths before assigning option or inference claims.',
        'Compare weighting, calendar aggregation and counterfactual rank using exact independently authored arithmetic.',
        'Reference-only disposition can complete the proposal decision without declaring a runtime integration.',
        'Record omissions and integrate substantive argument into the preserving reader and paired sponsor.']))
    specs = [
        ('gsynth_cran','DESCRIPTION',1,39,'Version 1.4.0; MIT declaration; no wrapper compilation; R >=2.10 and fect >=2.0.0 imports.'),
        ('gsynth_cran','LICENSE',1,2,'Year and holder only; full MIT template and dependency terms are not reproduced here.'),
        ('gsynth_cran','NEWS.md',1,19,'Estimator routing changed in 1.4.0; 1.3.0 merged functionality into fect and retained compatibility wrapper.'),
        ('gsynth_upstream','README.md',72,76,'Maintainers explicitly describe backward-compatibility-only maintenance.'),
        ('gsynth_cran','R/default.R',24,95,'Complete wrapper: weight is declared but unused; dispatch, inference remapping, defaults, original-data storage and class relabeling.'),
        ('gsynth_cran','man/gsynth.Rd',20,37,'Manual advertises weight as weighted average effect and cluster support only for nonparametric bootstrap.'),
        ('gsynth_cran','tests/testthat/test-gsynth.R',1,177,'Inspected tests cover routing, result shape, seed and options; skip_on_cran; no weight assertion in these ranges. Tests not run.'),
        ('fect_cran','DESCRIPTION',1,43,'Version 2.4.5; MIT declaration; compiled engine requires R >=4.1, Rcpp, RcppArmadillo and listed imports.'),
        ('fect_cran','LICENSE',1,2,'Year and holder only, not complete license-template evidence.'),
        ('fect_cran','R/default.R',310,360,'Direct engine defaults differ; weight roles, fixed effects, resampling and tolerance are explicit.'),
        ('fect_cran','R/default.R',380,394,'Default unconstrained loading and one-standard-error CV rule; rule validation.'),
        ('fect_cran','R/default.R',560,652,'Jackknife ignores cluster with warning; W fills both roles, distinct role columns refused, zero weights drop rows.'),
        ('fect_cran','R/default.R',708,755,'gsynth forces never-treated donor pool and em FALSE; pre-period count and CV defaults depend on method.'),
        ('fect_cran','R/default.R',1880,1938,'Donor/count gates and automatic unit removals; sample retention must accompany target.'),
        ('fect_cran','R/default.R',2090,2148,'Reversals refused for gsynth; parametric inference requires isolated never-treated pool; empirical/wild errors require complete panel.'),
        ('fect_cran','R/default.R',2630,2664,'Inspected no-CV gsynth path delegates to fect_nevertreated with weights, masks and rank.'),
        ('fect_cran','R/default.R',3380,3436,'Aggregation-weight outputs enter canonical slots; fitting-only weights do not; EM iteration-limit warning.'),
        ('fect_cran','R/fect_nevertreated.R',247,280,'Selected balanced/unbalanced control-fit dispatch; not a full C++ implementation audit.'),
        ('fect_cran','R/fect_nevertreated.R',330,345,'Rank versus count guards can reset rank or refuse CV; counts do not prove matrix rank.'),
        ('fect_cran','R/fect_nevertreated.R',631,701,'Selected parallel CV aggregation and legacy rank-update path; serial path distinct.'),
        ('fect_cran','R/fect_nevertreated.R',1010,1048,'Final CV rule can override intermediate selection using minimum, 1SE or legacy 1pct; sentinels removed from selection.'),
        ('fect_cran','R/fect_nevertreated.R',1210,1245,'Selected unbounded loading solve uses pre-factor Gram inverse; solve failure returns NA ATT fields.'),
        ('fect_cran','R/fect_nevertreated.R',2636,2672,'Treated-cell average, weighted counterpart and within-unit then across-unit average have distinct denominators.'),
        ('fect_cran','R/boot.R',812,835,'Parametric auto mode resolves to AR with missing cells, empirical otherwise.'),
        ('fect_cran','R/boot.R',1210,1289,'Selected case bootstrap resamples units or cluster IDs; support-conditioned retries appear in unit branch.'),
        ('fect_cran','R/boot.R',4115,4152,'Average SE uses sd with na.rm; normal CI default versus basic pivot; failed draws require explicit accounting.')]
    extracts, sources = [], {}
    for family,name,lo,hi,finding in specs:
        path = BASE/'sources'/family/name
        original = next(f['local_copy'] for f in archived[family]['files'] if f['local_copy']['path']==str(path.relative_to(ROOT)))
        assert ref(path,'Source')['sha256'] == original['sha256']
        lines=path.read_text().splitlines(keepends=True)
        assert 1 <= lo <= hi <= len(lines),(name,lo,hi,len(lines))
        excerpt=''.join(lines[lo-1:hi])
        extracts.append(dict(family=family,source=ref(path,name),lines=[lo,hi],finding=finding,
            excerpt=excerpt,excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
        sources[(family,name)]=dict(source_identity='https://github.com/'+selected[family]['repo']+'/blob/'+selected[family]['commit']+'/'+name,
            local_copy=ref(path,'Unmodified archive member'),archive=archived[family]['archive'],acquisition=archived[family]['receipt'])
    wrapper=(BASE/'sources/gsynth_cran/R/default.R').read_text()
    assert wrapper.count('weight')==1 and 'weight = NULL' in wrapper
    write(BASE/'inspected-extracts.json',dict(anchors=extracts,native_execution=False))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'identity-review.json',dict(selection=ref(BASE/'version-selection.json','Pre-cutoff revisions'),
        archives=ref(BASE/'archive-inspection.json','Bounded inert extraction'),identical_wrapper_files=equal,
        wrapper_version='1.4.0',selected_engine_version='2.4.5',engine_lineage='fect; gsynth compatibility surface',
        dependency_selection='Permitted by declared lower bound, but not an installed or tested environment.',
        license='Both declare MIT + file LICENSE; saved files identify year/holder only. Full template and transitive review remain open.',
        deployment='Wrapper compilation flag no does not erase fect compilation or its R >=4.1 requirement.',
        maintenance='Pinned NEWS and README identify compatibility maintenance; no runtime/support SLA claim.',
        historical_failures=[ref(ROOT/'docs/literature/raw/head_gsynth.receipt.json','Historical HTTP403 identity failure')],
        evidence=[ref(BASE/'inspected-extracts.json','Inspected source anchors')]))
    claims=[
        'gsynth 1.4.0 is a compatibility wrapper; selected fect 2.4.5 supplies estimation and inference.',
        'The complete selected wrapper declares weight but neither reads nor forwards it; the manual promises a weighted effect.',
        'Method, inference, force, CV, tolerance and output class cannot be inferred from wrapper name alone.',
        'fect distinguishes fit and aggregation weights, rejects different columns in selected source and changes canonical aggregation slots.',
        'Treated-cell and unit averages differ; missingness and removals require explicit denominators.',
        'Counts, predictive rank selection and a finite loading solve do not establish counterfactual stability.',
        'Never-treated donor, reversal and inference gates have explicit source behavior; no universal bootstrap claim.']
    records=[]
    for family,key,title in [('gsynth','exec21_gsynth_wrapper','gsynth 1.4.0 compatibility wrapper and documented weight contract'),
                             ('fect','exec21_gsynth_engine','fect 2.4.5 selected panel estimation, weighting and inference paths')]:
        matches=[e for e in extracts if e['family'].startswith(family)]
        selected_name=family+'_cran'
        records.append(dict(integrated_citation_key=key,kind='software_primary_source',title=title,
            author='Yiqing Xu and package contributors',year=2026,cutoff='2026-10-07',
            source_identity='https://github.com/'+selected[selected_name]['repo']+'/tree/'+selected[selected_name]['commit'],
            version_date=('1.4.0; 27 March 2026' if family=='gsynth' else '2.4.5; 29 May 2026, CRAN revision 30 May 2026'),
            local_copy=ref(BASE/'identity-review.json','Selected identity and dependency boundary'),
            primary_sources=[v for (f,_),v in sources.items() if f.startswith(family)],
            inspected_anchors=[dict(anchor=e['source']['path']+' lines '+str(e['lines']),finding=e['finding'],
                evidence=ref(BASE/'inspected-extracts.json','Verbatim primary anchors')) for e in matches],
            supported_claims=claims[:3] if family=='gsynth' else claims[3:],limitations=LIMITS))
    records.append(dict(integrated_citation_key='exec21_gsynth_reference',kind='project_derivation',
        title='Exact panel weighting, exposure-duration and factor-rank counterexamples',
        author='Causal banking proposal project',year=2026,version_date='21 October 2026',
        source_identity='tools/gsynth_reference_20261021.py',local_copy=ref(ROOT/'tools/gsynth_reference_20261021.py','Independent exact rational examples'),
        inspected_anchors=[ref(BASE/'exact-results.json','Three exact witnesses and padded count example')],
        supported_claims=['Effects -6 and 10 yield equal2 and weights9:1 yield -22/5.',
            'Unit effects10 over3 periods and -6 over1 yield cell6 and unit2.',
            'Rank-two models have the same observed panel and effects6 or2; six pre-period rows still span only one factor direction.'],limitations=LIMITS[4:]))
    write(BASE/'source-audit.json',dict(sources=records,cutoff='2026-10-07'))
    contract=dict(status='proposed_not_implemented',integration_allowed=False,
        initial_profile='Selected continuous-outcome panel, irreversible binary adoption, never-treated donors and explicit pre-action covariates; no generic fect family admission.',
        inputs=['Pinned wrapper and engine identities, R/compiler/dependency lock, seed, thread and resource limits.',
            'Unique unit/time keys, complete calendar, outcome units, treatment meaning/timing, never-treated donor list and masks.',
            'Requested target population, treated-cell versus unit average, horizon and weights with separate fit/aggregation roles.',
            'Explicit method, fixed effects, rank grid and CV rule, tolerance, missingness policy and declared sampling/error law.'],
        outputs=['Actual estimator/options and original request hash; no silent wrapper or default equivalence.',
            'Requested and retained populations, rows/units dropped with reasons, weights and all effect denominators.',
            'Rank/conditioning, fit/convergence and source warnings; individual contrasts and named aggregates.',
            'Uncertainty type, resampling unit, attempted/valid/failed draws and selection behavior; unavailable remains unavailable.'],
        failures=['Refuse weighted gsynth wrapper request: selected source does not forward weight.',
            'Reject duplicate/colliding keys, malformed timing, undefined target or nonfinite input/weights under initial contract.',
            'Reject unsupported distinct weight columns, treatment reversals, missing never-treated donors or insufficient support.',
            'Preserve NA/singular solves, rank resets, selected subsets, bootstrap retries and convergence warnings.',
            'Do not treat ordinary jackknife with cl as cluster-aware; do not silently substitute parametric and case bootstrap.',
            'Timeout, process failure or insufficient valid replications yields unavailable inference under a prespecified rule.'],
        prototype_oracles=[ref(BASE/'exact-results.json','Exact independent targets and rank ambiguity')],
        qualification=['First reproduce ignored weight with native wrapper and matched direct engine on a frozen small panel.',
            'Verify cell/unit denominators, aggregation-only versus fitting-only roles and returned canonical fields.',
            'Exercise missing cells, reversals, donor count, rank failures, method remapping, cluster warnings and timeout.',
            'Register known-law factor panels including weak support, drift, unequal treatment durations and dependence; count every failed request.',
            'Freeze CV/rank/regularization and complete refit/resampling behavior before coverage/value comparisons.'])
    write(BASE/'conversion-contract.json',contract)
    omissions=[
        ('Method originals','Research author','Acquire and inspect genuine Xu 2017 and relevant fect method PDFs before scholarly theorem claims.'),
        ('Full rights and environment','Future distribution/build owner','Inspect full standard MIT template, per-file and dependency terms; freeze R/compiler/runtime versions.'),
        ('Runtime conformance','Prototype owner','Execute registered wrapper/direct-engine parity and failure contracts in an isolated environment.'),
        ('Inference and selection','Method reviewer','Inspect remaining bootstrap/CV/native branches and register law-specific calibration and failure-denominator studies.'),
        ('Wider panel comparison','Research author','Compare concrete DID, classic synthetic control, matrix completion and state-space targets without declaring universal superiority.'),
        ('Costs and acceptance','Sponsor/operator and reviewer','Measure matched public-workflow total costs; later independent and bank evaluation require actual owners.'),
        ('Rendered pages','Fresh visual session','Inspect new and shifted pages under the separate image allowance; text bounds alone do not grant acceptance.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=n,owner=o,next_action=a,status='open') for n,o,a in omissions]))
    evidence=[ref(BASE/n,'Bounded proposal reuse evidence') for n in ['identity-review.json','source-audit.json','inspected-extracts.json',
        'exact-results.json','conversion-contract.json','omissions-register.json']]
    decision=dict(operation=OP,status='pass',decision='reference',capabilities=[],integration_allowed=False,
        scope='Retain pinned gsynth as a compatibility/source comparison; favor a future direct fect worker after separate qualification.',
        engine=dict(wrapper=selected['gsynth_cran'],dependency=selected['fect_cran'],distinct_estimation_lineages=1),
        alternatives=[
            dict(choice='adopt_gsynth_wrapper',disposition='reject_initial_production_route',reason='Ignored weight and remapped/default options make generic pass-through unsafe; compatibility has no demonstrated new-client benefit.'),
            dict(choice='direct_fect_worker',disposition='future_candidate',reason='Explicit weight and inference contracts avoid this wrapper defect; engine/dependency rights, numerical and runtime qualification still required.'),
            dict(choice='port_to_Python_or_Cxx',disposition='not_selected',reason='Would duplicate panel conversion, CV, native routines and inference without measured benefit or a behavioral parity baseline.'),
            dict(choice='DID_classic_synthetic_control_or_state_space',disposition='separate_comparators',reason='Different donor restrictions, extrapolation and targets require matched assumptions; none universally resolves rank or confounding.'),
            dict(choice='reject_entire_lineage',disposition='not_selected',reason='Pinned source supplies useful panel methods and transparent failure conditions for a bounded public comparison.')],
        costs='No native timing, engineering price or bank ROI observed. Measure conversion, validation, rank search, fits, bootstrap, serialization, review and support together.',
        owner_obligations=[dict(owner=o,obligation=a) for _,o,a in omissions],
        revisit_trigger='Wrapper fix, dependency/version change, target/weight/sampling-law change or decision to build the prototype.',
        limitations=LIMITS,evidence=evidence)
    output=ROOT/'docs/program/comprehensive-v14/work/SW.DECISION.inherited_gsynth/decision.json'
    output.parent.mkdir(parents=True,exist_ok=True);write(output,decision)
    write(BASE/'review.json',dict(status='pass',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,evidence=evidence+[ref(output,'Reference decision')],limitations=LIMITS,native_execution=False,visual_acceptance=False))
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
    findings=['Pin wrapper, selected engine and matching upstream bytes; bind rights declarations, dependencies and maintenance limits.',
        'Explain target, uncertainty, alternatives, costs and owners using inspected source and exact weighted/temporal/rank examples.',
        'Complete a reference-only disposition with conversion and failure contracts; runtime admission remains false.']
    ev=evidence+[ref(BASE/'plan-review-v2.json','Reviewed successor plan'),ref(BASE/'review.json','Author review'),ref(Path(__file__),'Exact review construction')]
    receipt.update(outcome='pass',execution='performed',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        limitations=LIMITS,original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Required gsynth decision')],
        nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i,verdict='pass',finding=f,evidence=ev) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(decision='reference',proposal_review='pass',integration_allowed=False,sources=len(sources),anchors=len(extracts))))


if __name__=='__main__':main()
