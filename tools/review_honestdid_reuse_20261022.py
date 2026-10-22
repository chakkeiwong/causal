#!/usr/bin/env python3
"""Review immutable source and a bounded sensitivity reference; admit no runtime."""
import hashlib
import json
from pathlib import Path

import honestdid_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
ROOT=run.core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-22/honestdid-reuse-v1'
OP='SW.DECISION.inherited_honestdid'
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Selected immutable original-source inspection; no downloaded R code or upstream tests executed.',
    'Repository revision declares 0.2.8; equivalence to release-tag, CRAN or installed binary bytes is unverified.',
    'Full top-level MIT terms inspected; solver, transitive dependency, redistribution and deployment review remains open.',
    'No complete inspection of all conditional inversion, CVXR, sign/shape, parallel or solver-status branches.',
    'Gaussian projection is an authored conservative oracle under a stipulated known covariance, not the package algorithm or empirical coverage.',
    'A sensitivity restriction does not validate causal assignment, no anticipation, covariance or restriction selection.',
    'Rendered review, mandatory repair acceptance, independent review and bank qualification remain open.']


def main():
    state=run.core.read(ROOT,run.core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    selection=read(BASE/'source-selection.json');acquisition=read(BASE/'acquisition-review.json')
    verify_bindings(acquisition);verify_bindings(read(BASE/'plan-review.json'))
    commit=selection['commit'];repo=selection['repository']
    assert commit=='6813f02ed38f0b63bdca6915604b2eac90491303'
    commit_path=ROOT/'docs/literature/raw/exec22_honestdid_cutoff_commit.json'
    identity=read(commit_path)[0];assert identity['sha']==commit
    date=identity['commit']['committer']['date'];assert date<'2026-10-07T15:59:59Z'
    originals={x['path']:x for x in acquisition['files']}
    for s in selection['files']:
        body=(BASE/'sources'/s['path']).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==s['blob']
    specs=[
        ('DESCRIPTION',1,44,'Version 0.2.8; R>=3.6; CVXR>=1.8, ECOSolveR, Rglpk and other imports; MIT + file LICENSE.'),
        ('LICENSE',1,2,'Holder/year notice; full grant is separately saved in LICENSE.md.'),
        ('LICENSE.md',1,21,'Complete MIT grant, copyright/notice retention and warranty disclaimer.'),
        ('NEWS.md',1,14,'CVXR interface compatibility repairs in 0.2.7/0.2.8 and options-test addition; no support SLA.'),
        ('R/sensitivityresults.R',12,57,'Smoothness interface defaults FLCI and first post-period; data-dependent default M grid uses hardcoded .05 for multi-preperiod calibration.'),
        ('R/sensitivityresults.R',62,137,'Selected serial and parallel conditional smoothness paths reduce accepted grid to min/max endpoints.'),
        ('R/sensitivityresults.R',150,163,'FLCI warns that the requested sign restriction is unused.'),
        ('R/sensitivityresults.R',268,277,'FLCI warns that the requested shape restriction is unused.'),
        ('R/sensitivityresults.R',412,488,'Relative-magnitude interface defaults C-LF, ten Mbar values on[0,2], 1000 inference grid points; serial path reduces accepted grid to endpoints.'),
        ('R/sensitivityresults.R',721,735,'Original interval uses requested post-period contrast and its covariance, without robust trend adjustment.'),
        ('R/utilities.R',49,96,'Nonconformability refuses; asymmetry and negative covariance eigenvalues warn without a corrective projection.'),
        ('R/deltasd.R',15,58,'Second differences and removal of normalized baseline construct smoothness restrictions.'),
        ('R/deltasd.R',61,127,'LP target extrema; both nonzero statuses yield unadjusted point target with warning; one-failure branch not separately guarded here.'),
        ('R/deltarm.R',12,55,'First-difference relative-magnitude restrictions indexed by maximum preperiod direction and sign.'),
        ('R/deltarm.R',75,180,'Component LP extrema; both failed statuses yield point target without local warning; outer bounds use global min/max; comment assumes nonnegative target weights.'),
        ('R/deltarm.R',184,246,'Single-post conditional path delegates to no-nuisance inversion; multi-post path to nuisance inversion. Delegates not fully reviewed.'),
        ('R/deltarm.R',249,322,'Low-level default1000; grid bounds +/-20 post-target SE around zero; union membership retained across signed components.'),
        ('R/honest_did.R',1,113,'Dynamic/universal-baseline AGGTE guard, influence-product covariance, consecutive times/reference removal; wrapper100 grid points forwards only to relative magnitude.'),
        ('R/honest_sunab.R',1,38,'Selected fixest internal-field aggregation and transformed covariance; exact compatibility and dependence remain unqualified.')]
    extracts=[]
    for name,lo,hi,finding in specs:
        p=BASE/'sources'/name
        a=p.read_bytes().decode('utf-8').split('\n')
        assert 1<=lo<=hi<=len(a),(name,len(a),hi)
        excerpt='\n'.join(a[lo-1:hi])
        extracts.append(dict(source=ref(p,'Unmodified pinned original'),lines=[lo,hi],finding=finding,
            excerpt=excerpt,excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest()))
    write(BASE/'inspected-extracts.json',dict(anchors=extracts,native_execution=False))
    paper=ROOT/'docs/papers/A More Credible Approach to Parallel Trends Rambachan(2023).pdf'
    assert ref(paper,'Original')['sha256']=='2ef3448e51bb946478ad323b8e00fc5de80fcc1b274ec26aa01dfaa9e458b7dc'
    text=ROOT/'docs/literature/text/rambachan2023.txt';lines=text.read_text().split('\n')
    parts=[]
    for lo,hi,finding in [
        (392,580,'Population identified sets, relative magnitude versus absolute smoothness, and linear differential trend at M=0.'),
        (627,683,'Known Gaussian inferential goal and union of confidence sets for union restrictions; not a generic finite-sample bank result.'),
        (901,988,'Uniform CLT, positive eigenvalue bounds, uniformly consistent covariance and restriction regularity for Proposition3.1.'),
        (1306,1370,'FLCI bias/variance tradeoff, scoped convex/centrosymmetric near-optimality, and failure to exploit sign/shape; RM can require infinite FLCI.')]:
        excerpt='\n'.join(lines[lo-1:hi]);parts.append(dict(lines=[lo,hi],finding=finding,excerpt=excerpt))
    write(BASE/'paper-inspection.json',dict(citation_key='rambachan2023',paper=ref(paper,'Genuine published original'),
        text=ref(text,'Derived text; newline anchors preserve formfeeds'),inspected_anchors=parts,
        source_identity='https://doi.org/10.1093/restud/rdad018',version_date='Published2023; inherited local original',
        limitations=['Existing citation/audit preserved unchanged. No theorem from its cited literature is separately claimed.']))
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'identity-review.json',dict(repository=repo,commit=commit,commit_date=date,declared_version='0.2.8',
        metadata=[ref(commit_path,'Cutoff commit identity'),ref(ROOT/'docs/literature/raw/exec22_honestdid_cutoff_tree.json','Complete Git tree'),
            ref(ROOT/'docs/literature/raw/exec22_honestdid_releases.json','Release identities; tag equality unverified')],
        evidence=[ref(BASE/'acquisition-review.json','15 originals and Git-blob verification'),ref(BASE/'inspected-extracts.json','Technical and rights anchors')],
        license='Full repository MIT terms inspected; dependency and solver rights remain open.',
        maintenance='Pinned NEWS records CVXR compatibility changes; no demonstrated runtime/support commitment.',
        alias_boundary='R engine, Stata implementation and any third-party ports are distinct interfaces; no inherited runtime equivalence.'))
    claims=[
        'RM and SD use first and second differences with different tuning units and different zero-tuning assumptions.',
        'Defaults and retained numerical information differ between high-level, low-level and did bridge entrypoints.',
        'Warnings, accepted-grid membership and solver status must accompany any sensitivity result.',
        'Failed LP status can reach a point-target fallback; source reachability is not an observed package failure.',
        'Bridge conversion must preserve normalized ordering, aggregation and the supplied full covariance.']
    records=[]
    for key,title,bridge in [('exec22_honestdid_engine','HonestDiD 0.2.8 pinned sensitivity and numerical contracts',False),
                             ('exec22_honestdid_bridges','HonestDiD 0.2.8 did and fixest event-study conversion paths',True)]:
        selected=[e for e in extracts if (e['source']['path'].endswith(('R/honest_did.R','R/honest_sunab.R')))==bridge]
        names={e['source']['path'] for e in selected}
        records.append(dict(integrated_citation_key=key,kind='software_primary_source',title=title,
            author='Ashesh Rambachan, Jonathan Roth and contributors',year=2026,cutoff='2026-10-07',
            source_identity=f'https://github.com/{repo}/tree/{commit}',version_date='0.2.8; revision '+commit+'; '+date,
            local_copy=ref(BASE/'identity-review.json','Identity and source originals'),
            primary_sources=[v for v in originals.values() if v['local_copy']['path'] in names],
            inspected_anchors=[dict(anchor=e['source']['path']+' newline lines '+str(e['lines']),finding=e['finding'],
                evidence=ref(BASE/'inspected-extracts.json','Verbatim primary extract')) for e in selected],
            supported_claims=claims[4:] if bridge else claims[:4],limitations=LIMITS))
    records.append(dict(integrated_citation_key='exec22_honestdid_reference',kind='project_derivation',
        title='Three-period trend-restriction and Gaussian projection reference',author='Causal banking proposal project',year=2026,
        version_date='22 October 2026',source_identity='tools/honestdid_reference_20261022.py',
        local_copy=ref(ROOT/'tools/honestdid_reference_20261022.py','Independent authored oracle'),
        inspected_anchors=[ref(BASE/'exact-results.json','Exact targets, analytic extrema witnesses and grid counterexamples')],
        supported_claims=['Zero RM gives4 while zero SD gives2 at x=-2,y=4.',
            'Known Gaussian joint-ellipse projection gives analytic RM bounds preserving full covariance.',
            'A coarse empty accepted grid need not imply an empty continuous set; a hull can fill rejected gaps.'],limitations=LIMITS[4:]))
    write(BASE/'source-audit.json',dict(cutoff='2026-10-07',sources=records))
    contract=dict(status='proposed_not_implemented',integration_allowed=False,
        inputs=['Immutable R engine and R/dependency/solver lock; sampling design and covariance provenance.',
            'Ordered pre/post contrasts, explicit omitted baseline and equal-time calendar; no anticipation assumption.',
            'Target weights, units/horizon, full transformed covariance and declared retained population.',
            'Fixed restriction family, units, tuning values, alpha, method, seed, grid extent/resolution and sign/shape policy.'],
        outputs=['Requested and executed method, restriction and target; all default expansion made explicit.',
            'Population bounds versus confidence set; full accepted grid/components with hull separately labeled.',
            'Solver status, tolerances, warnings, retries, boundary contact and numerical/unavailable status.',
            'Ordinary reference interval separate from sensitivity result; alpha scope and non-simultaneous tuning selection explicit.'],
        failures=['Refuse malformed/nonfinite inputs, nonconformable order, invalid covariance or unexplained singularity under initial profile.',
            'Do not silently project a covariance to PSD or count a warning as repaired sampling validity.',
            'Failed, infeasible, unbounded and unknown solver results are distinct; never accept fallback point target as certified bounds.',
            'No accepted nodes means unresolved numerical set until an independently justified search rule; never report default infinity sentinels as confidence endpoints.',
            'Accepted boundaries require expansion or an external bound certificate; preserve disconnected nodes without asserting continuous topology.',
            'Ignored sign/shape restrictions and unforwarded wrapper grid options require explicit refusal or qualified fallback.',
            'A future status adapter may need a pinned patch or lower-level instrumentation; stdout warnings alone are insufficient.'],
        behavioral_oracle=ref(BASE/'exact-results.json','Independent population/known-law examples, not algorithm equivalence'),
        qualification=['Freeze an isolated R/solver environment and review dependency rights before execution.',
            'Compare direct engine and bridges on known ordered contrasts and full covariance; exercise option forwarding.',
            'Inject grid clipping, sparse-grid gaps, empty acceptance and each solver termination; require refusal contract.',
            'Register known-law experiments, failed-request denominator and computational budget before coverage or value claims.',
            'Compare ordinary DID, prespecified SD/RM and conservative projection under matched target, law and loss.'])
    write(BASE/'conversion-contract.json',contract)
    omissions=[
        ('Numerical delegates and upstream tests','Research/prototype author','Inspect remaining no-nuisance, nuisance, FLCI, parallel and solver wrappers; tests are not yet acquired or run.'),
        ('R and solver environment','Build and distribution owner','Freeze R/CVXR/GLPK/ECOS and transitive versions/rights; measure total conversion and inference cost.'),
        ('Runtime conformance','Prototype owner','Implement status-preserving adapter only after source and law-specific behavioral qualification.'),
        ('Alternative interfaces','Research author','Pin and inspect Stata/ports separately before compatibility or licensing claims.'),
        ('Restriction choice and data validity','Method/data owner','Justify no anticipation, target calendar, preperiod law and full covariance; distinguish selection from fixed tuning.'),
        ('Empirical precision and economics','Sponsor and method reviewer','Use preregistered public/generated panels before any costly bank study; stipulated dollars are not ROI.'),
        ('Rendered acceptance','Fresh visual session','Inspect added and shifted rendered pages under renewed image allowance.')]
    write(BASE/'omissions-register.json',dict(global_blocker=None,items=[dict(item=n,owner=o,next_action=a,status='open') for n,o,a in omissions]))
    evidence=[ref(BASE/n,'Scoped reuse evidence') for n in ['identity-review.json','source-audit.json','inspected-extracts.json',
        'paper-inspection.json','exact-results.json','conversion-contract.json','omissions-register.json','plan-review.json']]
    decision=dict(operation=OP,status='pass',decision='reference',capabilities=[],integration_allowed=False,
        scope='Retain pinned R HonestDiD as the sensitivity-method reference; defer native admission until numerical and environment contracts qualify.',
        source=dict(repository=repo,commit=commit,declared_version='0.2.8',distinct_engine_lineages=1),
        alternatives=[
            dict(choice='isolated_R_worker',disposition='preferred_future_candidate',reason='Reuses the published method implementation; must retain status/grid/covariance semantics and qualify pinned solvers.'),
            dict(choice='direct_generic_adoption',disposition='not_selected',reason='Generic endpoint pass-through loses warnings, failure status and grid information; no runtime evidence.'),
            dict(choice='port_to_Python_or_Cxx',disposition='not_selected_initially',reason='Conditional inversion, optimization and distributional details require parity evidence; no demonstrated cost benefit.'),
            dict(choice='Stata_or_third_party_port',disposition='separate_candidate',reason='No claim of API, license, result or default equivalence from shared method names.'),
            dict(choice='ordinary_DID_or_known_law_projection',disposition='matched_comparators',reason='Ordinary DID adds stronger trend assumptions; conservative projection is transparent but can lose precision.'),
            dict(choice='reject_method_family',disposition='not_selected',reason='Inspected paper/source supply a useful bounded sensitivity design; source concerns require contracts, not blanket rejection.')],
        costs='No native runtime or price measured. Account for event-study fitting, covariance, conversion, repeated inversions, solver licences, failure review and maintenance.',
        owner_obligations=[dict(owner=o,obligation=a) for _,o,a in omissions],
        revisit_trigger='Prototype build decision, source/solver update, new target/calendar/covariance or restriction-selection policy.',
        limitations=LIMITS,evidence=evidence)
    output=ROOT/'docs/program/comprehensive-v14/work'/OP/'decision.json'
    output.parent.mkdir(parents=True,exist_ok=True);write(output,decision)
    write(BASE/'review.json',dict(status='pass',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        findings=claims,evidence=evidence+[ref(output,'Reference-only decision')],limitations=LIMITS,native_execution=False,visual_acceptance=False))
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
    findings=['Bind cutoff commit, declared version, full top-level MIT terms, imports and maintenance limits; no alias equivalence.',
        'Explain restrictions, full covariance, uncertainty, alternatives, costs and owners using source, genuine paper and reproduced authored reference.',
        'A reasoned reference-only proposal decision passes; proposed conversion/failure contract admits no native integration.']
    receipt.update(outcome='pass',execution='performed',scope=decision['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),
        limitations=LIMITS,original_gap_qualification=False,capabilities=[],outputs=[ref(output,'Required HonestDiD disposition')],
        nonexecution_reason='',revisit_trigger=decision['revisit_trigger'],
        criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence+[ref(BASE/'review.json','Author review'),ref(Path(__file__),'Reproducible review')]) for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);verify_bindings(read(BASE/'source-audit.json'));verify_bindings(read(BASE/'review.json'))
    print(json.dumps(dict(decision='reference',outcome='pass',integration_allowed=False,originals=15,anchors=len(extracts))))


if __name__=='__main__':main()
