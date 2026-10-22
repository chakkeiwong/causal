#!/usr/bin/env python3
"""Inspect pinned source evidence and record scoped proposal decisions."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import r_iv_rd_reference_20261022 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-22/r-iv-rd-v1'
RAW=ROOT/'docs/literature/raw'
OP='SW.CELL.iv_rd_design.R'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Proposal source review and exact authored reference only; no R package, vendor engine, downloaded code or live model was executed.',
    'Client cutoff 2026-10-07T15:59:59Z; current task-view discovery and license retrieval are later snapshots.',
    'Six pinned packages plus inherited grf/fixest are not an exhaustive R IV/RD census; complementary leads remain uninspected.',
    'Direct dependency declarations and applicable license texts are inspected; transitive dependency/build/distribution clearance remains open.',
    'No native conformance, empirical coverage, performance superiority or measured bank return is established.',
    'Rendered visual review awaits a fresh image allowance; Q1/Q5 and all mandatory repairs remain open.']


def fields(path):
    result={};key=None
    for line in path.read_text().split('\n'):
        if line.startswith((' ','\t')) and key:result[key]+=' '+line.strip()
        elif re.match(r'^[A-Za-z][^:]*:',line):
            key,value=line.split(':',1);result[key]=value.strip()
    return result


def inspected(stem,ranges,tree=None):
    p=RAW/(stem+'.txt');receipt=p.with_suffix('.receipt.json');r=read(receipt)
    assert r['status']=='saved' and core.sha(p)==r['sha256']
    raw=p.read_bytes();lines=p.read_text().split('\n');anchors=[]
    blob=None
    if tree is not None:
        # raw.githubusercontent.com/{owner}/{repo}/{revision}/{relative-path}
        rel=r['url'].split('/',6)[6]
        expected=next(x['sha'] for x in tree['tree'] if x['path']==rel)
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert expected==blob,(stem,rel)
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines),(stem,lo,hi,len(lines))
        anchors.append(dict(anchor=f'newline-delimited lines {lo}-{hi}',
            line_start=lo,line_end=hi,inspected_text='\n'.join(lines[lo-1:hi])))
    return dict(local_copy=ref(p,'Inspected authentic original'),acquisition=ref(receipt,'URL/date/hash'),
        source_url=r['url'],git_blob_sha1=blob,inspected_anchors=anchors)


def package(name,version,commit,tree_path,description,records,claims):
    t=read(tree_path);assert not t.get('truncated',False)
    details=fields(RAW/(description+'.txt'))
    assert details['Version']==version
    meta=inspected(description,[(1,len((RAW/(description+'.txt')).read_text().split('\n'))-1)],t)
    originals=[inspected(stem,ranges,t) for stem,ranges in records]
    return dict(integrated_citation_key='exec22_riv_'+name.lower(),kind='software_documentation',
        title=f'{name} {version}: pinned technical, source and reuse review',author=name+' package contributors',year=2026,
        source_identity='https://github.com/cran/'+name,version_date=version+'; commit '+commit,
        local_copy=originals[0]['local_copy'],records=originals,
        inspected_anchors=[dict(source=r['local_copy'],anchors=r['inspected_anchors']) for r in originals],
        tree=ref(tree_path,'Pinned tree; selected raw-file Git blob identities verified'),
        description=meta,declared_license=details['License'],
        direct_dependencies={k:details.get(k,'') for k in ['Depends','Imports','LinkingTo','Suggests','NeedsCompilation']},
        maintenance=dict(publication=details.get('Date/Publication'),packaged=details.get('Packaged'),
            limitation='Snapshot and selected changelog evidence only; no promised support or issue-resolution SLA.'),
        supported_claims=claims,limitations=LIMITS)


def prepare():
    assert not (BASE/'source-audit.json').exists()
    inherited=read(ROOT/'docs/program/repair-v12/work/SW01/source-audit.json')
    pins={s['id'].split(':')[-1]:s for s in inherited['entries'] if s['id'].startswith('v12:pinned-package:')}
    specs={
      'ivreg':([
          ('v12_sw2_manual_ivreg_1',[(45,109),(112,151)]),
          ('exec22_riv_ivreg_0',[(45,71),(87,89)]),
          ('exec22_riv_ivreg_1',[(18,41),(43,95)]),
          ('exec22_riv_ivreg_2',[(1,38)])],
          ['Exogenous regressors belong in the instrument matrix; two/three-part formulas have distinct roles.',
           'OLS mode uses 2SLS; M/MM are robust regressions, not a weak-IV confidence-set guarantee.',
           'Wald covariance overrides must be functions for auxiliary diagnostic fits; preserve aliased coefficients and both stage ranks.']),
      'ivmodel':([
          ('exec22_riv_ivmodel_1',[(1,40),(42,65)]),
          ('v12_sw2_manual_ivmodel_1',[(1,21)]),
          ('v12_sw2_manual_ivmodel_2',[(1,20)]),
          ('exec22_riv_ivmodel_2',[(1,22)]),
          ('exec22_riv_ivmodel_ar_source',[(3,84)]),
          ('exec22_riv_ivmodel_clr_source',[(10,25),(33,86)]),
          ('exec22_riv_ivmodel_0',[(1,21)])],
          ['One endogenous variable and continuous-outcome linear IV model; CLR adds a first-stage linear model.',
           'AR/CLR return interval-component matrices, including unbounded and disconnected sets.',
           'Pinned AR computes an F ratio from projections; pinned CLR forms residual cross-product covariance. Generic heteroSE/clusterID options do not establish robust AR/CLR inference.',
           'CLR source catches conditional-p-value and root-search errors and substitutes zero; native trigger behavior is untested.',
           'DESCRIPTION offers GPL-2 or file LICENSE; the pinned file contains MIT terms. Dependency and distribution scope still require review.']),
      'rdrobust':([
          ('v12_sw2_manual_rdrobust_1',[(5,14),(17,47),(49,118),(121,154)])],
          ['Sharp/fuzzy/kink, separate estimation/bias bandwidths, conventional/bias-corrected estimates and distinct standard errors must be preserved.',
           'Mass-point adjustments count/enlarge local support; they do not supply missing identification assumptions.',
           'Version 4.0.0 is the selected cutoff pin; 4.1.1 CRAN publication is later than the exact cutoff.']),
      'rddensity':([
          ('v12_sw2_manual_rddensity_1',[(31,95),(112,151)])],
          ['Local-polynomial density estimates and manipulation tests are separate diagnostics; preserve bandwidths, support and variance method.',
           'Nonrejection does not establish continuity of potential outcomes or absence of competing interventions.']),
      'rdlocrand':([
          ('v12_sw2_manual_rdlocrand_1',[(47,84),(88,120),(122,152)]),
          ('exec22_riv_rdwinselect',[(85,109)])],
          ['Local-randomization inference requires an explicit window and assignment law; p>0 uses asymptotic inference for documented contrasts.',
           'Requested/effective polynomial degrees and inference methods can differ; retain warnings and method switches.',
           'Finite confidence-set grids can truncate; selected windows depend on covariate balance tests and need provenance.',
           'The package imports AER and sandwich; AER is an actual dependency, not just a legacy alias.'])}
    sources=[]
    aer_commit=read(RAW/'exec22_riv_aer_cutoff.json')[0]['sha']
    aer=package('AER','1.2-17',aer_commit,RAW/'exec22_riv_aer_tree.json','exec22_riv_aer_description',[
        ('exec22_riv_aer_0',[(5,34),(38,81)]),('exec22_riv_aer_1',[(1,53)]),
        ('exec22_riv_aer_2',[(21,51)]),('exec22_riv_aer_4',[(1,49)])],
        ['AER contains a separate 2SLS implementation and ivreg-class methods; it is not identical to the ivreg package.',
         'Its summary diagnostics default to FALSE and cover first-stage F, Wu-Hausman and overidentification diagnostics.',
         'Formula roles, weights, missingness, rank and covariance must be explicit; diagnostic tests do not prove exclusion or monotonicity.'])
    aer['cutoff_evidence']=ref(RAW/'exec22_riv_aer_cutoff.json','Cutoff-filtered commit query')
    sources.append(aer)
    for pkg,(records,claims) in specs.items():
        old=pins[pkg];verify_bindings(old)
        s=package(pkg,old['observed_version'],old['commit'],RAW/f'v12_sw2_tree_{pkg}.json',
            f'v12_sw2_description_{pkg}',records,claims)
        s['cutoff_evidence']=old['cutoff_evidence'];sources.append(s)
    # Resolve CRAN 4.1.1 rather than broadening the before-cutoff capability claim.
    rd411=inspected('exec22_riv_rd411_description',[(1,6),(28,40)],read(RAW/'exec22_riv_rd411_tree.json'))
    publication=fields(RAW/'exec22_riv_rd411_description.txt')['Date/Publication']
    assert publication=='2026-10-07 23:20:02 UTC'
    assert datetime.fromisoformat(publication.replace(' UTC','+00:00'))>datetime.fromisoformat('2026-10-07T15:59:59+00:00')
    sources[3]['later_cran_revision']=rd411
    write(BASE/'version-review.json',dict(status='resolved_for_CRAN_distribution',
        cutoff_utc='2026-10-07T15:59:59Z',rdrobust_selected='4.0.0',rdrobust_4_1_1_publication=publication,
        evidence=[ref(RAW/'exec22_riv_rdrobust_history.json','Observed commit history'),
            ref(RAW/'exec22_riv_rd411_tree.json','Exact later distribution tree'),rd411['local_copy']],
        finding='Package Date 2026-10-07 alone is insufficient: packaging22:01:16 and publication23:20:02 UTC follow the client cutoff. No claim about every upstream channel.'))
    for num,spans in [(2,[(61,102),(134,169)]),(3,[(95,101),(156,175),(198,228),(246,254)])]:
        r=inspected('exec22_riv_gpl'+str(num),spans)
        sources.append(dict(integrated_citation_key='exec22_riv_gpl'+str(num),kind='official_license_text',
            title='GNU General Public License version '+str(num),author='Free Software Foundation',year=1991 if num==2 else 2007,
            source_identity=r['source_url'],version_date=f'GPL-{num}; acquired22October2026 from CRAN license index',
            local_copy=r['local_copy'],acquisition=r['acquisition'],inspected_anchors=r['inspected_anchors'],
            supported_claims=['Running, copying, modification, notices and corresponding-source conditions are distinct; a process boundary is not a blanket license clearance.'],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec22_riv_reference',kind='project_authored_exact_reference',
        title='Exact credit encouragement, weak-ratio sets and threshold references',author='Causal banking proposal project',year=2026,
        source_identity='tools/r_iv_rd_reference_20261022.py',version_date='22October2026; declared finite laws and known-covariance Gaussian reference',
        local_copy=ref(ROOT/'tools/r_iv_rd_reference_20261022.py','calculate(): complete exact laws'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Finite population sums, quadratic roots and complete enumeration of20 assignments')],
        supported_claims=['LATE-150, ATE-70 and encouragement ITT-60 give different assumed margins50,-30,10USD.',
            'Exclusion/monotonicity violations give ratios-200/-250USD in explicit alternative laws.',
            'Gaussian inversion can give two rays, one bounded interval or the whole line; a narrow grid misses a nonempty set.',
            'Two continuous potential-mean laws agree on integer-score observations but imply cutoff effects-20/0USD.',
            'With slope bound10 and one-unit support gaps, effect bounds are[-40,0]USD and net margins[-10,30]USD.',
            'A sharp-null randomization reference over20 equally likely allocations gives two-sided p=1/10.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'exact-results.json',exact.calculate())
    discovery=RAW/'exec22_riv_econometrics_view.html'
    lines=discovery.read_text().split('\n')
    excerpts=[dict(line=i,text=line) for i,line in enumerate(lines,1) if 73<=i<=83]
    leads=['sem','LARF','lfe','plm','REndo','SteinIV','rdmulti','rdpower','RATest']
    write(BASE/'search-review.json',dict(status='bounded_search_incomplete',
        stop_rule='Inspect the seeded five packages and AER, one CRAN Task View IV/RD section, named grf/fixest prior decisions and30 DESCRIPTION-history entries; stop this source batch after23 registered public requests.',
        search_date='2026-10-22',cutoff='2026-10-07T15:59:59Z',
        source=ref(discovery,'Current CRAN Econometrics Task View, discovery only'),inspected_anchors=excerpts,
        leads=leads,limitation='Current list is not cutoff membership or technical evidence. Trace eligible versions, aliases and rights independently before accepting capabilities; no exhaustive search claim.'))
    prior_paths=[ROOT/'docs/program/execution/2026-10-21/grf-reuse-v1/conversion-contract.json',
                 ROOT/'docs/program/execution/2026-10-20/fixest-reuse-v1/conversion-contract.json']
    write(BASE/'inherited-source-review.json',dict(evidence=[ref(p,'Reinspected existing reuse boundary') for p in prior_paths],
        findings=['grf initial AIPW binary-iid profile explicitly excludes IV/LATE; do not borrow its runtime admission.',
            'fixest worker proposal preserves row masks, covariance and formula semantics; IV inference requires a separate target/design review.']))
    write(BASE/'omissions-register.json',dict(status='open',items=[
        dict(id='complementary_candidates',candidates=leads,next_action='Recover cutoff commits and primary manuals; resolve panel aliases and investigate multicutoff, power, alternative IV and randomization-test scope.',blocker_scope='R IV/RD census only'),
        dict(id='distribution_rights',next_action='Choose exact R worker distribution; freeze all direct/transitive dependency versions and third-party notices; review original and modified distribution obligations.',blocker_scope='Runtime admission only'),
        dict(id='native_trials',next_action='Prepare a pinned R environment and prospectively register the conformance/calibration studies in conversion-contract.json before native execution.',blocker_scope='Native implementation and performance claims only'),
        dict(id='ivmodel_failure_path',next_action='Exercise CLR numerical integration/root-search failure cases in a controlled native harness; qualify failure detection or patch/audit a distinct pinned fork.',blocker_scope='CLR runtime profile only'),
        dict(id='visual',next_action='Fresh visual session under inherited preview limit; inspect changed pages and full-document navigation.',blocker_scope='Rendered acceptance only')],
        resolved=[dict(id='rdrobust_4_1_1_cutoff',disposition='CRAN distribution after cutoff; retain4.0.0',evidence=ref(BASE/'version-review.json','Exact timestamps'))],global_blocker=None))
    contract=dict(status='proposal_only',integration_allowed=False,
        inputs=['Immutable data/row IDs, score units, eligibility rule and timing, outcome horizon/units, assignment/treatment coding, target population.',
            'Separate exogenous/endogenous/instrument matrices; explicit intercept, contrasts, weights, missingness and allowed formula AST. No arbitrary agent-authored R evaluation.',
            'Chosen IV model or continuity/local-randomization design, assumptions and known support limits. No automatic LATE-to-ATE or fuzzy-to-sharp substitution.',
            'All variance options, alpha/critical law, effective rank, cluster units, bandwidths, kernels, degrees, randomization law, seeds and window selection provenance.'],
        outputs=['Target, full row mask and warnings; coefficient names with complete covariance and degrees of freedom; separate reduced form and first stage.',
            'Set as ordered interval components with open/closed endpoints, explicit +/-infinity, empty/unknown distinction, inversion grid, search bounds and truncation status.',
            'Conventional, bias-corrected and robust RD rows remain distinct; retain h/b, N/N_h/N_b, unique support and requested/effective options.',
            'Density diagnostics and balance tests never become automatic validity or exclusion/monotonicity certifications.'],
        failure_contract=['Uninstalled/unqualified engine returns unavailable; unsupported model remains unsupported, not not_identified.',
            'Numerical integration/root failures and CLR swallowed-error branches must be detected or the route refused; zero p-value is not proof of successful computation.',
            'A finite inversion grid returning no accepted values means empty_on_grid, not globally_empty. Boundary contact means global bounds unresolved.',
            'Missing target, rank loss, collinearity, mass points, too few clusters, warnings and degree downgrades are preserved; resource/time failure returns no partial success.'],
        owners=['Research owner specifies target/design and inference regime.','R adapter owner verifies native conversion and failure paths.',
            'Distribution owner freezes dependency rights and notices.','Evaluation owner preregisters public/generated conformance and coverage studies.'],
        proposed_studies=[
            dict(id='IV-CONFORMANCE',target='Pinned AER and ivreg ordinary2SLS',law='Fixed public/generated full-rank and rank-deficient matrices; explicit weights/categorical design/missingness',oracle='Independent projection normal equations; preserve all masks and covariance conventions',acceptance='Targets and rows identical; numeric tolerance declared after scale profiling, before final fixtures; unsupported targets refused'),
            dict(id='WEAK-SET',target='Selected ivmodel AR/CLR and local-randomization fuzzy inference',law='Freeze one-endogenous continuous-outcome Gaussian iid model; distinct heteroskedastic and clustered stress regimes',oracle='Independent inversion and current exact topology witnesses; native numerical faults injected',acceptance='All interval components and infinities survive; no numerical error converted to significance; no cluster claim without a separately justified method'),
            dict(id='RD-CONTINUITY',target='rdrobust4.0.0',law='Known smooth potential-mean functions and specified sharp/fuzzy treatment jump; discrete-support and tiny-first-stage stress cases',oracle='Declared cutoff effect; native output and serialized output agree on every estimate/SE/bandwidth/support field',acceptance='Prospective Monte Carlo budget/seeds and coverage intervals; keep failures in denominator; unresolved discrete support does not produce a false identified estimate'),
            dict(id='RD-RANDOMIZATION',target='rdlocrand3.0',law='Fixed window before outcomes; uniform3-of6 exact reference, then larger frozen assignments and separate selected-window studies',oracle='Enumerate20 assignments: two-sided sharp-null p=.1; preserve requested/effective p and window provenance',acceptance='Exact-law result preserved; asymptotic switches explicitly labeled; no unconditional coverage claim after unreviewed window selection')],
        cost_comparison='Worker retains upstream semantics but needs R/dependency operations and serialization; port adds numerical/maintenance/rights burden. Measure both only on a declared prototype; no invented runtime or prices.',
        exact_reference=ref(BASE/'exact-results.json','Authored semantic references; not package-conformance results'),limitations=LIMITS)
    write(BASE/'conversion-contract.json',contract)
    write(BASE/'review.json',dict(status='pass_for_scoped_review_coverage_inconclusive',reviewer=REVIEWER,
        findings=['AER1.2-17 resolved as a distinct cutoff package; current ivreg0.6-8 is not a transparent alias.',
            'rdrobust4.1.1 CRAN timestamp resolves the selected distribution question; upstream history remains outside that finding.',
            'Six package trees and inspected file hashes verified; actual local MIT alternative in ivmodel replaces metadata-only uncertainty.',
            'Scientific scope, set topology, numerical failure and target/economic mismatch are explicit.',
            'Five reference-only reuse decisions can be completed without granting runtime integration; census remains inconclusive.'],
        evidence=[ref(BASE/n,'Reviewed substantive evidence') for n in ['source-audit.json','exact-results.json','version-review.json','search-review.json','inherited-source-review.json','conversion-contract.json','omissions-register.json','plan-review.json']],
        limitations=LIMITS,independent_review=False,rendered_review=False))
    print(json.dumps(dict(sources=len(sources),packages=6,coverage='inconclusive',rd411='CRAN after cutoff',native_execution=False)))


def record(identifier):
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==identifier
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,identifier)
    evidence=[ref(BASE/n,'Reviewed source, scientific and disposition evidence') for n in
        ['source-audit.json','exact-results.json','version-review.json','search-review.json','inherited-source-review.json','conversion-contract.json','omissions-register.json','plan-review.json','review.json']]
    evidence.append(ref(Path(__file__),'Exact review and disposition construction'))
    for r in evidence:core.bound(ROOT,r)
    output=ROOT/node['outputs'][0]
    if identifier==OP:
        outcome='inconclusive';scope='Six pinned R IV/RD packages and inherited grf/fixest boundaries; bounded proposal survey'
        value=dict(operation=identifier,status=outcome,scope=scope,evidence=evidence,
            candidates=['AER1.2-17','ivreg0.6-8','ivmodel1.9.1','rdrobust4.0.0','rddensity3.0','rdlocrand3.0','inherited:grf','inherited:fixest'],
            incomplete='Nine complementary leads need cutoff/version/technical review; no exhaustive coverage or runtime claim.',
            limitations=LIMITS,next_action='Inspect complementary leads and finish scoped R census; native qualification and distribution rights remain separate prototype tasks.')
        findings=[('inconclusive','Seeded family and AER are resolved, but nine complementary leads and cutoff history remain outside inspected scope.'),
            ('pass','Authentic technical bytes, commit trees, Git blob/SHA-256 checks, exact newline anchors and supported claims are bound.'),
            ('pass','Omissions, post-cutoff distribution and failure contracts are explicit; no unavailable original is waived or replaced.')]
        receipt_path=BASE/'operation-receipt.json'
    else:
        group=identifier.rsplit('_',1)[-1]
        choices={
          '050':('AER1.2-17 and ivreg0.6-8','Prefer the dedicated ivreg worker for a future plain2SLS profile; retain AER as a separate comparison and rdlocrand dependency. Do not alias their S3 defaults or port before native parity.',
              'Choose between ordinary2SLS and robust-regression profiles explicitly; compare covariance/diagnostic defaults and loaded namespace behavior.'),
          '051':('ivmodel1.9.1','Retain as a weak-IV and sensitivity reference; defer runtime admission until CLR numerical failure paths and the exact inference law are qualified. No generic cluster/heteroskedastic AR/CLR promise.',
              'Qualify source-audited error detection or a separately reviewed fork; compare an independent inversion implementation.'),
          '052':('rdrobust4.0.0','Prefer preserving the original R implementation for a future continuity-based RD worker; retain exact bandwidth/variance/support outputs. Do not port or upgrade to4.1.1 in the cutoff comparison.',
              'Freeze target and density/support assumptions, then qualify sharp/fuzzy/kink and discrete-score refusal paths.'),
          '053':('rddensity3.0','Retain as a supplementary manipulation diagnostic; never an automatic causal-design approval. Native integration can follow an explicit support/diagnostic contract.',
              'Qualify bandwidth, mass-point and density outputs; compare covariate/design evidence independently.'),
          '054':('rdlocrand3.0','Retain for an explicitly local-randomization design with fixed-window reference; do not silently substitute continuity or asymptotic inference. AER and sandwich remain genuine dependencies.',
              'Qualify assignment law, selected-window provenance, requested/effective polynomial degree and confidence-grid topology.')}
        name,reason,revisit=choices[group]
        outcome='pass';scope='Completed reference-only proposal reuse disposition; runtime capability denied'
        value=dict(operation=identifier,status='pass',decision='reference',candidate=name,scope=scope,
            integration_allowed=False,reason=reason,alternatives=['Original pinned R worker after qualification','Port after demonstrated need and separate rights/numerical review','Independent reference implementation and scoped commercial comparison'],
            costs=read(BASE/'conversion-contract.json')['cost_comparison'],owners=read(BASE/'conversion-contract.json')['owners'],
            revisit_trigger=revisit,evidence=evidence,limitations=LIMITS)
        findings=[('pass','Pinned primary source, declared dependencies, license texts and maintenance limits support a reference-only disposition; no full distribution clearance.'),
            ('pass',reason+' Costs, alternatives, owners and exact revisit triggers are recorded.'),
            ('pass','integration_allowed=false; original-worker preference is conditional, with semantic oracles and conversion/failure contracts, not runtime authorization.')]
        receipt_path=BASE/'decisions'/group/'operation-receipt.json'
    write(output,value)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome=outcome,execution='performed',scope=scope,reviewer=REVIEWER,capabilities=[],
        outputs=[ref(output,'Reviewed coverage or reuse disposition')],limitations=LIMITS,nonexecution_reason='',
        revisit_trigger=value.get('revisit_trigger',value.get('next_action','')),
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    write(receipt_path,receipt)
    print(json.dumps(dict(operation=identifier,outcome=outcome,receipt=str(receipt_path.relative_to(ROOT)))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);p.add_argument('operation',nargs='?')
    a=p.parse_args();prepare() if a.command=='prepare' else record(a.operation)
