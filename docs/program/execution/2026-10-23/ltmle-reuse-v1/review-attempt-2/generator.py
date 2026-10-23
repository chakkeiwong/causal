#!/usr/bin/env python3
"""Review pinned ltmle semantics and an exact validated policy construction."""
import hashlib
import json
from pathlib import Path

import ltmle_policy_oracle_v2_20261023 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = controller.base
ROOT = run.core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-23/ltmle-reuse-v1'
RAW = ROOT / 'docs/literature/raw'
OP = 'SW.DECISION.inherited_ltmle'
PIN = '338c029dae9692ef20714125773da7037688993b'
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Source-level proposal reference; no downloaded R code, package tests or external dependency was executed.',
    'The cutoff-filtered default-branch query returns this 2023 commit. A June 2026 repository push is a separate observation; CRAN release equality and other branches are not established.',
    'GPL-2 package declaration and authentic standard license are inspected; transitive dependency compatibility and a specific distribution arrangement remain to be reviewed.',
    'Matrix, matrixStats, SuperLearner, R runtime and BLAS implementation versions are not locked or qualified.',
    'Native fit behavior, dynamic-rule correctness, nuisance assumptions, positivity, cluster sampling and calibration require future matched trials.',
    'Exact finite-law and covariance examples are authored mathematical references; they are not package execution, fitted influence values or bank returns.',
    'The decision does not close longitudinal software coverage, grant an integration capability or accept a product.',
]


def main():
    state = run.core.read(ROOT, run.core.STATE)
    assert state['execution_runtime']['active']['operation'] == OP
    commit = read(RAW / 'r3g_commit_ltmle.json')[0]
    cutoff = read(RAW / 'exec23_ltmle_cutoff_commit.json')[0]
    tree = read(RAW / 'exec23_ltmle_tree.json')
    assert commit['sha'] == cutoff['sha'] == PIN
    assert commit['commit']['committer']['date'] < '2026-10-07T15:59:59Z'
    assert tree['truncated'] is False
    entries = {x['path']: x for x in tree['tree']}
    proofs = []
    for directory in ['', 'R']:
        children = [x for x in tree['tree'] if str(Path(x['path']).parent) == (directory or '.')]
        children.sort(key=lambda x: (Path(x['path']).name + ('/' if x['type']=='tree' else '')).encode())
        body = b''.join(x['mode'].lstrip('0').encode()+b' '+Path(x['path']).name.encode()
            +b'\0'+bytes.fromhex(x['sha']) for x in children)
        oid = hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()
        expected = entries[directory]['sha'] if directory else commit['commit']['tree']['sha']
        assert oid == expected
        proofs.append(dict(directory=directory or '/', expected=expected, reconstructed=oid))
    mapping = {'R/ltmle.R':'r3g_api_ltmle.txt', 'DESCRIPTION':'exec23_ltmle_description.txt',
        'NAMESPACE':'exec23_ltmle_NAMESPACE.txt', 'NEWS':'exec23_ltmle_news.txt'}
    for name in ['GeneralUtilities', 'DeterministicFunctions', 'BinaryToCensoring', 'ltmle_sg', 'ltmle-package', 'zzz']:
        mapping['R/'+name+'.R'] = 'exec23_ltmle_'+name.replace('-','_')+'.txt'
    originals, paths = [], {}
    for repository_path, local in mapping.items():
        p = RAW / local
        body = p.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        assert (blob,len(body)) == (entries[repository_path]['sha'],entries[repository_path]['size'])
        receipt = p.with_suffix('.receipt.json')
        r = read(receipt)
        assert r['status']=='saved' and r['sha256']==run.core.sha(p)
        paths[repository_path] = p
        originals.append(dict(repository_path=repository_path, git_blob=blob,
            source_identity=f'https://raw.githubusercontent.com/joshuaschwab/ltmle/{PIN}/{repository_path}',
            local_copy=ref(p,'Authentic bytes matching pinned Git tree'), retrieval=ref(receipt,'Preserved successful acquisition')))
    paths['GPL-2'] = RAW / 'exec22_riv_gpl2.txt'
    lic = read(RAW / 'exec22_riv_gpl2.receipt.json')
    assert lic['sha256']==run.core.sha(paths['GPL-2']) and lic['status']=='saved'
    originals.append(dict(source_identity=lic['url'], local_copy=ref(paths['GPL-2'],'Authentic GPL version 2 text'),
        retrieval=ref(RAW / 'exec22_riv_gpl2.receipt.json','License acquisition')))
    specs = [
        ('DESCRIPTION',1,43,'Version 1.3-0, date 2023-4-13, R >=3.1.0, Matrix/matrixStats imports, optional SuperLearner and GPL-2 declaration.'),
        ('NAMESPACE',1,21,'Exports the simple and MSM entrypoints and censoring helpers; registers separate summary methods.'),
        ('NEWS',1,18,'Version 1.3-0 changed deterministic-Q ordering and replaced speedglm by glm; 1.1-0 documented small-sample t intervals.'),
        ('GPL-2',60,165,'Sections0-3 distinguish running from modifying/distributing, state notice/source requirements and distinguish independent works and aggregation.'),
        ('R/ltmle.R',1,106,'Documented column chronology, binary actions, censoring, absorbing events, outcome range and rule interface.'),
        ('R/ltmle.R',331,404,'Default glm, cumulative gbounds .01 to1, TMLE variance; simple entrypoint constructs one or two regimes in a working model.'),
        ('R/ltmle.R',406,460,'Single-regime output converts from logistic working parameters, preserves influence values/cumulative g diagnostics and rescales outcomes.'),
        ('R/ltmle.R',485,558,'Creates defaults and validates input; resets unavailable requested variance method to ic, including all no-action/censoring cases.'),
        ('R/ltmle.R',632,660,'Additional variance unavailable for nonbinary, deterministic-Q, gcomp, stratify and non-null id; warnings use selected positivity and rare-event conditions.'),
        ('R/ltmle.R',1025,1065,'HouseholdIC aggregates by sum and multiplies by household/record count; FinalizeIC calls it after weighting.'),
        ('R/ltmle.R',1067,1109,'Normalization uses record-level expectation matrix; near-zero rcond leads to missing matrix and a warning.'),
        ('R/ltmle.R',1337,1416,'Single mean takes maximum available variance; each paired contrast applies gradients to shared covariance and selects larger available standard deviation; nonbinary RR/OR removed and scales restored.'),
        ('R/ltmle.R',1442,1471,'P values switch between t with n-1 df and normal; MSM standard errors divide by number of influence rows.'),
        ('R/ltmle.R',1590,1618,'Summary propagates a full covariance via gradient and divides by influence-row count; t critical value is used for n<100 and normal otherwise.'),
        ('R/ltmle.R',1758,1835,'Fewer than two fitting observations stop; constant outcome skips fitting; learner calls receive weights and id; selected warnings are suppressed and some out-of-range predictions bounded.'),
        ('R/ltmle.R',2009,2013,'Cumulative products are computed first, then bounded; a floor on each incremental probability is a different calculation.'),
        ('R/ltmle.R',2174,2220,'Checks chronological index order and disjoint node roles and restricts CV options; accepts non-GLM library only if SuperLearner is present.'),
        ('R/ltmle.R',2264,2325,'Treatment binary checks, survival consistency, NA restrictions, weight and id validation; supplying a vector id is not a sampling-law proof.'),
        ('R/ltmle.R',2327,2405,'Outcome clipping/scaling and post-event/censoring cleaning; explicit range division motivates nondegeneracy validation.'),
        ('R/ltmle.R',2407,2445,'Default regressions include prior nodes with exclusions for censoring, events or treatment stratification.'),
        ('R/ltmle.R',2583,2621,'Numeric C=1 is uncensored; conversions precede helpers; suppresses extreme-probability/rank warnings and, in update steps, nonconvergence warning.'),
        ('R/ltmle.R',2635,2652,'GLM and glm.fit helpers set maxit=100; no native convergence qualification follows.'),
        ('R/GeneralUtilities.R',7,23,'Failed solve returns missing matrix and warning; successful return does not establish scientific identifiability.'),
        ('R/GeneralUtilities.R',73,80,'Warning suppression uses exact warning-message match and muffleWarning.'),
        ('R/BinaryToCensoring.R',24,37,'Named is.censored/is.uncensored arguments distinguish coding and return censoring factors.'),
        ('R/DeterministicFunctions.R',8,24,'Templates must be completed; factor/index conversion and absorbing-event behavior are documented.'),
        ('R/ltmle_sg.R',1,19,'Separate historical implementation is marked testing-only and subset scope; it is not independent qualification.'),
    ]
    anchors = []
    for name,lo,hi,finding in specs:
        lines = paths[name].read_text().splitlines()
        assert hi<=len(lines),(name,hi,len(lines))
        excerpt='\n'.join(lines[lo-1:hi])
        anchors.append(dict(source=ref(paths[name],'Inspected authentic original'),lines=[lo,hi],finding=finding,
            excerpt=excerpt,excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
    write(BASE/'inspected-extracts-v2.json',dict(anchors=anchors))
    write(BASE/'identity-review-v2.json',dict(status='pass_for_source_identity',repository='joshuaschwab/ltmle',
        commit=PIN,commit_date=commit['commit']['committer']['date'],declared_version='1.3-0',
        tree_proofs=proofs,originals=originals,license='GPL-2',
        dependencies=dict(R='>=3.1.0',imports=['Matrix','matrixStats'],conditional=['SuperLearner']),
        cutoff_query=ref(RAW/'exec23_ltmle_cutoff_commit.json','Fresh cutoff-filtered default-branch query returns same commit'),
        commit_object=ref(RAW/'r3g_commit_ltmle.json','Commit/tree identity'),tree=ref(RAW/'exec23_ltmle_tree.json','Complete tree'),
        maintenance=ref(RAW/'repo_ltmle_verified.json','June 2026 push observation; does not establish branch or package equality'),
        limitations=LIMITS))
    result=exact.calculate()
    assert result==read(BASE/'policy-oracle-results-v2.json')
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_reference_work',issues=[],
        evidence=[ref(BASE/'plan.md','Original bounded scope'),ref(BASE/'failed-draft-1/failure-review.json','Identified failures and precise repairs'),
            ref(BASE/'development-v2.tex','Scientific successor using new citation identities')],
        checks=['Authenticate actual Git blobs and trees, separating sort order from serialized names.',
            'Inspect effective variance, contrast and failure paths, not only user-facing defaults.',
            'Validate all binary histories and full mass; cross-check enumeration by independent moment identity.',
            'Preserve failed drafts and both frozen S5 inputs; new text is a successor pending integration.']))
    write(BASE/'mathematical-review-v2.json',dict(status='pass_for_exact_authored_argument',issues=[],
        evidence=[ref(Path(exact.__file__),'Exhaustive finite-law oracle and independent checks'),
            ref(BASE/'policy-oracle-results-v2.json','Replayed exact outputs'),ref(BASE/'development-v2.tex','Connected derivation')],
        findings=['All16 binary histories have probabilities in[1/100,2/5]; each policy joint mass is1.',
            'Enumeration and separate moment identity agree on risks13/60,17/100,7/75 and net0,130/3,340/3USD.',
            'Complete-case risks differ from target; the known-probability IPCW identity holds exactly.',
            'Paired covariance gives contrast variance1/3 versus7/3 after omitting covariance.',
            'Duplicate iid-row first-mean variance5/7 versus household5/3 has exact ratio7/3, not2.'],
        native_execution=False,empirical_coverage=False))
    source=dict(integrated_citation_key='exec23_ltmle_source',kind='software_primary_source',
        title='ltmle binary longitudinal regime and uncertainty implementation at the selected cutoff revision',
        author='Joshua Schwab and ltmle contributors',year=2023,
        source_identity=f'https://github.com/joshuaschwab/ltmle/tree/{PIN}',
        version_date=f'1.3-0 declared; {PIN}; 2023-04-17; cutoff default-branch query observed 23 October2026',
        local_copy=ref(BASE/'identity-review-v2.json','Identity and authentic source originals'),primary_sources=originals,
        inspected_anchors=[dict(anchor=x['source']['path']+' lines '+str(x['lines']),finding=x['finding'],
            evidence=ref(BASE/'inspected-extracts-v2.json','Verbatim anchors')) for x in anchors],
        supported_claims=[x['finding'] for x in anchors],limitations=LIMITS)
    math=dict(integrated_citation_key='exec23_ltmle_exact',kind='project_derivation',
        title='Exact dynamic servicing, censoring and household covariance constructions',
        author='Causal banking proposal authors',year=2026,
        source_identity='tools/ltmle_policy_oracle_v2_20261023.py',version_date='23 October2026; exact authored reference',
        local_copy=ref(Path(exact.__file__),'Authored calculation'),
        inspected_anchors=[dict(anchor='calculate(): full-support validation, enumeration, independent moments and covariance',
            finding='Exact stipulated risks, monetary contrasts, missingness selection and covariance distinctions.',
            evidence=ref(BASE/'mathematical-review-v2.json','Inspected mathematical argument and replay'))],
        supported_claims=['The explicit probability law and influence fixture imply the displayed exact values.'],limitations=LIMITS)
    write(BASE/'source-audit-v2.json',dict(cutoff='2026-10-07',sources=[source,math]))
    contract=dict(status='proposed_not_implemented',integration_allowed=False,
        input=['Declare population, time zero, observation clock, history and dynamic-rule information sets.',
            'Validate binary actions, event/censoring orientation, row and cluster maps, finite nonnegative weights and positive outcome-range width.',
            'Freeze cumulative floors, Q/g formulas and libraries, effective variance path and R/dependency identities.'],
        output=['Regime means and contrasts with reference regime, covariance, influence unit and cluster counts.',
            'Actual variance method, range clipping, bounded/unbounded cumulative probabilities, full fit diagnostics and warnings.',
            'Explicit unavailable uncertainty, unsupported history, invalid input, weak-support and failed-fit states.'],
        refusal=['Future-dependent rules, incoherent absorbing outcomes, nonfinite weights, missing IDs or unsupported continuous actions.',
            'Unannounced change from requested robust variance to influence-only variance.',
            'Unspecified outcome clipping, lost covariance or replacement of missing uncertainty by zero.'],
        oracle=ref(BASE/'policy-oracle-results-v2.json','Truth and covariance fixture; backend has not been run'),
        qualification='Future locked R trial with binary histories, rare outcomes, poor support, rank deficiency, unequal cluster sizes and constant-range cases; include all failures.')
    write(BASE/'conversion-contract-v2.json',contract)
    omissions=[dict(item='Native behavior and dependencies',owner='Prototype author',next_action='Lock a selected R distribution and package/dependency graph; review GPL-2 distribution compatibility; execute policy and covariance fixtures with all failed requests retained.'),
        dict(item='Scientific qualification',owner='Method reviewer',next_action='Choose a concrete sampling law and target; justify nuisance/positivity conditions, then register fresh coverage, availability and useful-width screens.'),
        dict(item='Current edition and branch coverage',owner='Source reviewer',next_action='Authenticate CRAN archive equality and any alternative branch needed by the prototype; a default-branch query is not an exhaustive release census.'),
        dict(item='Reader integration',owner='Monograph author',next_action='Insert development-v2 with new citations into a preserving paired release; the current delivered PDFs do not yet contain it.')]
    write(BASE/'omissions-register-v2.json',dict(items=omissions,global_blocker=None,
        acquisition_failure_resolved=ref(BASE/'acquisition-success.json','Successful retry after preserved DNS failure')))
    evidence=[ref(BASE/n,'Bounded source, mathematical and design review') for n in ['identity-review-v2.json','inspected-extracts-v2.json',
        'source-audit-v2.json','plan-review-v2.json','mathematical-review-v2.json','conversion-contract-v2.json',
        'omissions-register-v2.json','development-v2.tex','policy-oracle-results-v2.json']]
    evidence += [ref(Path(exact.__file__),'Exact authored reference'),ref(Path(__file__),'Review successor'),
        ref(BASE/'failed-draft-1/failure-review.json','Preserved errors and repairs')]
    decision=dict(operation=OP,status='pass',decision='reference',integration_allowed=False,capabilities=[],
        scope='Use pinned ltmle as a binary longitudinal regime/uncertainty reference and candidate future R comparator; no adapter admitted.',
        source=dict(repository='joshuaschwab/ltmle',commit=PIN,declared_version='1.3-0',distinct_engine_lineages=1),
        alternatives=[dict(choice='pinned_R_worker',disposition='future_candidate',reason='Preserve original estimator semantics after locking dependencies and testing effective variance, history conversion and failure diagnostics.'),
            dict(choice='immediate_native_adoption',disposition='not_selected',reason='Requested variance can change and warnings can be suppressed; no accepted profile or native trial establishes the intended uncertainty behavior.'),
            dict(choice='cross_language_port',disposition='not_selected_initially',reason='No demonstrated requirement offsets porting dynamic rules, cumulative floors, learner and covariance semantics; compare original R first.'),
            dict(choice='lmtp_or_gfoRmula',disposition='distinct_alternatives',reason='Modified treatment laws, simulation and uncertainty contracts differ; match requested regime before comparing.'),
            dict(choice='blanket_rejection',disposition='not_selected',reason='Inspected implementation is a useful technical reference despite remaining qualification needs.')],
        costs='No measured runtime or price. Include R/dependency management, GPL distribution review, history conversion, nuisance fitting, diagnostics, covariance, failure recovery and maintenance.',
        owner_obligations=omissions,revisit_trigger='A prototype selects binary longitudinal regimes, new source/dependency versions are needed, or target/clock/censoring/cluster law changes.',
        evidence=evidence,limitations=LIMITS)
    out=ROOT/'docs/program/comprehensive-v14/work'/OP/'decision.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    write(out,decision)
    review=dict(status='pass_for_bounded_reference_decision',reviewer=dict(name='Codex author/coordinator',kind='author'),
        evidence=evidence+[ref(out,'Canonical reference decision')],
        findings=['Eleven authentic originals establish selected code, license text and maintenance evidence.',
            'Effective variance fallback, warnings, shared covariance, ID aggregation and range behavior are traced to code.',
            'Probability-law and finite-sample covariance errors were preserved and corrected before any operation receipt.',
            'Comparison, costs and revisit obligations are explicit; no native capability or coverage acceptance is granted.'],
        limitations=LIMITS,native_execution=False,visual_acceptance=False)
    verify_bindings(review)
    write(BASE/'review-v2.json',review)
    graph,merged,_=run.combined(ROOT,state)
    node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    findings=['Pinned source, GPL-2, dependencies and observed maintenance bind to exact originals; lmtp/gfoRmula remain distinct.',
        'Target, clock, uncertainty, alternatives, cost components and owner/revisit obligations are developed with exact valid banking calculations.',
        'Reference-only choice; a proposed conversion/failure contract and exact oracle are retained without integration permission.']
    receipt.update(outcome='pass',execution='performed',scope=decision['scope'],reviewer=review['reviewer'],limitations=LIMITS,
        capabilities=[],original_gap_qualification=False,nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        outputs=[ref(out,'Required reuse decision')],criteria=[dict(index=i,verdict='pass',finding=f,
            evidence=evidence+[ref(BASE/'review-v2.json','Author review')]) for i,f in enumerate(findings)])
    run.validate_receipt(ROOT,merged,node,receipt,len(state['execution_program']['turns']))
    write(BASE/'operation-receipt-v2.json',receipt)
    print(json.dumps(dict(operation=OP,originals=len(originals),anchors=len(anchors),decision='reference',integration_allowed=False)))


if __name__=='__main__':
    main()
