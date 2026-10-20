#!/usr/bin/env python3
"""Bounded commercial network coverage and explicit proposal comparison."""
import argparse
import json
from pathlib import Path

import network_interference_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run=extension.base
core=run.core
ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-20/network-commercial-v1'
OP='SW.CELL.networks_interference.commercial'
COMPARE='SW.COMM.networks_interference'
REVIEWER=dict(name='Codex author/coordinator',kind='author')
read=lambda p:json.loads(p.read_text())
LIMITS=[
    'Nine selected official originals and eight candidate families do not constitute an exhaustive commercial census.',
    'Post-cutoff acquisition, embedded metadata and legacy dates do not prove exact cutoff-era bytes or current entitlements.',
    'ArcGIS and Statsig image-only equations were not acquired or visually reviewed; claims use inspected primary prose only.',
    'No commercial engine, downloaded package, live experiment or sibling repository was executed.',
    'Exact authored network and assignment examples are not native conformance, bank data or empirical coverage findings.',
    'Unmatched editions, rights, prices, missing originals and broader search remain explicit; no absence finding is inferred.',
    'Mandatory repairs, Q1/Q5, rendered review and final proposal acceptance remain open.'
]


def source(name,folder,ext,title,author,version,year,ranges,claims):
    p=BASE/folder/(name+'.'+ext);receipt=p.with_suffix('.receipt.json')
    r=read(receipt);assert r['returncode']==0 and r['format_valid'] and r['sha256']==core.sha(p)
    body=(BASE/(name+'.txt')).read_text();lines=body.splitlines(keepends=True);anchors=[]
    for lo,hi in ranges:
        assert 1<=lo<=hi<=len(lines),(name,lo,hi)
        anchors.append(dict(anchor=f'extracted lines {lo}-{hi}',
            physical_page=body[:sum(len(s) for s in lines[:lo-1])].count(chr(12))+1 if ext=='pdf' else None,
            inspected_text=''.join(lines[lo-1:hi])))
    item=dict(integrated_citation_key='exec20_network_'+name,kind='official_documentation',
        title=title,author=author,year=year,source_identity=r['url'],version_date=version,
        accessed_utc=r['finished_at'],local_copy=ref(p,'Authentic selected official original'),
        text_copy=ref(BASE/(name+'.txt'),'Inert extraction; original authoritative'),
        acquisition_receipt=ref(receipt,'Fixed HTTPS acquisition and redirects'),
        headers=ref(BASE/folder/(name+'.headers'),'Original response headers'),
        inspected_anchors=anchors,supported_claims=claims,limitations=LIMITS)
    if ext=='pdf':item['pdf_metadata']=ref(BASE/(name+'-pdfinfo.txt'),'Observed metadata, not cutoff-byte proof')
    return item


def record(operation,output,evidence,findings,scope,trigger):
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==operation
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,operation)
    receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=REVIEWER,
        capabilities=[],outputs=[ref(output,'Bounded commercial proposal output')],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger=trigger,
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    return receipt


def coverage():
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    assert not output.exists() and not (BASE/'source-audit.json').exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    write(BASE/'plan-review.json',dict(status='pass',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed plan'),ref(BASE/'search-review.json','Bounded discovery limits')],
        checks=['Separate spatial association, structural equilibrium effects, exposure estimands and temporal assignment.',
            'Compare the documented quantity called impact before comparing feature names.',
            'Preserve incomplete/redirected downloads and edition uncertainty; inspect primary methods before claims.',
            'Complete a public proposal comparison now; costly licensed and bank trials remain later.',
            'Carry incomplete census, original and rights work forward without blocking other ready lanes.']))
    a='acquisition/network';f='followups/acquisition/network';s='switchback/acquisition/network'
    sources=[
        source('stata_spregress',a,'pdf','Stata spregress: spatial autoregressive models','StataCorp',
            'Official manual; PDF metadata 28 July 2026; exact licensed edition unresolved',2026,
            [(9,39),(122,145),(218,241),(270,334)],
            ['Cross-sectional SAR supports dependent-variable, covariate and error lags with GS2SLS or ML.',
             'ML robust variance addresses nonnormal iid errors; heteroskedastic GS2SLS still requires independent innovations.',
             'Row normalization changes the model; scalar spectral/minmax scaling can be absorbed in spatial coefficients.',
             'force bypasses sample/W mismatch refusal; manual warns that omitted units and normalization alter spillovers.']),
        source('stata_impacts',a,'pdf','Stata spregress postestimation: reduced-form impacts','StataCorp',
            'Official manual; PDF metadata 28 July 2026; exact licensed edition unresolved',2026,
            [(145,197),(201,242),(290,318)],
            ['estat impact averages own derivatives, off-diagonal derivatives and their sum for the reduced-form mean.',
             'Default delta variance conditions on regressors; unconditional option accounts for their sampling variation and is unavailable with if/in.',
             'Jacobians and covariance matrices are exposed; fitted impacts do not themselves establish causal interventions.']),
        source('stata_panel',a,'pdf','Stata spxtregress: spatial autoregressive panel models','StataCorp',
            'Official manual; PDF metadata 28 July 2026; exact licensed edition unresolved',2026,
            [(9,36),(193,264),(317,325)],
            ['Requires strongly balanced panels and fixed spatial matrices in the displayed model.',
             'FE conditions out panel effects and cannot fit time-invariant regressors; RE imposes panel-effect restrictions.',
             'Displayed innovations are iid across panels and time; selected spatial panels do not qualify arbitrary network/time dependence.']),
        source('arcgis_method',a,'html','ArcGIS Pro: how Spatial Autoregression works','Esri',
            'ArcGIS Pro3.5 path and meta version; meta last-modified2April2025',2025,
            [(12,41),(64,101)],
            ['Documents OLS, spatial lag, error and combined models, with optional LM-based selection and explicit cautions about fit.',
             'Documents simple impacts: the direct impact is the coefficient, unlike a full feedback-adjusted average own derivative.',
             'Documents robust lag-model errors and AK-triggered spatial HAC using a separate nearest-neighbor triangular-kernel matrix.',
             'Documents refusal at30percent connectivity; this is a tool rule, not a universal causal/statistical cutoff.']),
        source('arcgis_tool',a,'html','ArcGIS Pro: Spatial Autoregression tool and Python parameters','Esri',
            'ArcGIS Pro3.5 path and meta version; acquired20October2026',2025,
            [(12,25),(43,82),(98,137),(177,180)],
            ['arcpy.stats.SAR exposes model, neighborhood and weight choices; automatic neighborhood/bandwidth choices need recording.',
             'Weights are row standardized unless a matrix file is supplied; default nearest-neighbor count is8.',
             'Documentation lists Basic, Standard and Advanced availability; this is not deployment, redistribution or purchase entitlement.']),
        source('sas_latest_spatial',f,'pdf','SAS/ETS User Guide: The SPATIALREG Procedure','SAS Institute',
            'Title page2023.10; document dated15August2024; PDF metadata13August2024',2024,
            [(1,39),(105,166),(482,489),(899,925),(1055,1119),(1121,1138),(2215,2229)],
            ['Cross-sectional SAR, SLX, Durbin and spatial-error/moving-average families have supplied W and model-specific likelihoods.',
             'Default row normalization replaces missing weights by zero; NONORMALIZE refuses missing off-diagonal entries and keeps diagonal zero.',
             'SPATIALID aligns data and W; numeric noninteger identifiers are truncated for matching.',
             'SAR displayed likelihood assumes iid normal innovations; covariance choices Hessian, OP and QML are distinct, with Hessian default and approximation restrictions.']),
        source('statsig_types',f,'html','Statsig Warehouse Native: types of experiments','Statsig',
            'Legacy documentation; displayed update18September2025; acquired20October2026',2025,
            [(1,31)],
            ['Distinguishes analysis-only from assign-and-analyze experiments.',
             'Describes switchbacks for network effects and GeoLift-based geo testing; exact backend release is not established.']),
        source('statsig_units',f,'html','Statsig: cluster experiments across unit types','Statsig',
            'Legacy documentation; displayed update18September2025; acquired20October2026',2025,
            [(1,33)],
            ['Example assigns at organization level and targets user revenue using a one-to-many organization/user relation.',
             'Delta-method ratio inference accounts for numerator-denominator covariance; no arbitrary cross-cluster interference claim follows.']),
        source('statsig_switchback',s,'html','Statsig: switchback tests, attribution and resampling','Statsig',
            'Legacy documentation; displayed update18September2025; acquired20October2026',2025,
            [(4,31),(33,63)],
            ['Attributes events by exposure time/unit, attribution window and subsequent event timestamp; buckets combine time windows and grouping attributes.',
             'Resamples test buckets and control buckets separately10000times and uses percentile intervals.',
             'Documents schedule and burn-in/out controls and advanced randomized bucketing; burn-in/out discards exposures.',
             'Legacy page states no hourly Pulse initially, no time-series/dimension breakdown, and CUPED/sequential testing unavailable for this profile; current feature absence is not claimed.'])]
    reference=dict(integrated_citation_key='exec20_network_reference',kind='project_authored_exact_reference',
        title='Exact feedback, exposure-support and switchback references for bank networks',
        author='Causal banking proposal project',year=2026,
        source_identity='tools/network_interference_reference_20261020.py',version_date='20October2026',
        local_copy=ref(ROOT/'tools/network_interference_reference_20261020.py','calculate, inverse and response'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Rational matrix identities, assignment enumeration and explicit temporal laws')],
        supported_claims=['Feedback gives own40/3, spillover20/3 and total20; assumed cost12 gives coefficient margin-2, own4/3 and portfolio8.',
            'Removing one tie changes targeted portfolio margin to-2; row normalization changes responses while coordinated scalar rescaling preserves them.',
            'Illustrative full delta variance28 differs from20 after omitting covariance.',
            'Exactly-one-treated pair lacks two exposure cells; independent half-probability assignments give each cell1/4 and unbiased HT means5,8,7,10.',
            'Authored time trend yields observed102 versus immediate2; alternating carryover yields-2 versus immediate2 and sustained6.'],limitations=LIMITS)
    sources.append(reference)
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'inspected-extracts.json',dict(sources=[dict(key=r['integrated_citation_key'],anchors=r['inspected_anchors']) for r in sources],software_executed=False))
    write(BASE/'exact-results.json',exact.calculate())
    candidates=[]
    specs=[
        ('Stata','spregress, estat impact, spxtregress; SP manual profile','Selected technical originals',
         'Bind licensed edition, spivregress endogenous-treatment route and complete W/postestimation specification; measure native costs.'),
        ('SAS','SAS/ETS SPATIALREG; title-page2023.10','Selected technical original',
         'Bind exact licensed product, sparse-approximation settings, effect extraction and rights; recover historical15.1 only if comparing that version.'),
        ('Esri','ArcGIS Pro3.5 Spatial Autoregression; arcpy.stats.SAR','Selected technical originals',
         'Acquire equation/flowchart images in a fresh visual session, exact estimation/dependency algorithms and native simple-impact comparison; check deployment terms.'),
        ('Statsig','Warehouse Native switchbacks and cluster-unit analysis; legacy18September2025 docs','Selected technical originals',
         'Bind product tier/backend, complete ratio formulas and scheduling, attribution overlap and dependence/resampling law; verify pricing and current availability.'),
        ('Optimizely','Legacy Full Stack mutually-exclusive-experiments candidate','Essential original unavailable',
         'Follow an authentic product/version documentation route; acquired URL redirects to general homepage and supports no interference claim.'),
        ('EViews','Candidate spatial/network or user-programmed routes; no matched edition','Unresolved candidate',
         'Acquire exact spatial/treatment-exposure technical originals or record unresolved coverage; pooled-regression material is insufficient.'),
        ('IBM SPSS','Candidate spatial/network extensions; no matched edition','Unresolved candidate',
         'Resolve concrete procedure, extension, supplier and inferential target with authentic originals.'),
        ('Commercial probabilistic-network tools','HUGIN and GeNIe/SMILE candidate families; separate from exposure inference','Unresolved candidate for this cell',
         'Establish any treatment-interference procedure from primary technical text; a supplied Bayesian network alone is not evidence of that capability.')]
    for family,alias,status,action in specs:
        candidates.append(dict(family=family,aliases=alias,status=status,next_public_evidence=action,
            runtime_executed=False,price=None,entitlement_verified=False,absence_claim=False))
    write(BASE/'candidate-register.json',dict(cutoff='2026-10-07',candidates=candidates,
        stopping_rule='Eight-family bounded comparison with nine selected originals; failed inherited query and unresolved complementary search retained.',
        market_census_complete=False,search_evidence=ref(BASE/'search-review.json','Discovery attempts, not primary technical proof')))
    failures=[]
    for p in sorted(BASE.glob('**/*.receipt.json')):
        r=read(p)
        if r['returncode']!=0 or r['id']=='optimizely_exclusion':
            failures.append(ref(p,'Failed/incomplete acquisition or redirected homepage; no capability/absence finding'))
    write(BASE/'omissions-register.json',dict(candidates=[dict(family=c['family'],next_action=c['next_public_evidence']) for c in candidates],
        additional=['Complete market discovery and cutoff-specific byte/version evidence.',
            'Image-only equations/flowcharts, inherited bibliography leads and full vendor estimator specifications.',
            'Prices, contract rights, operating limits, reproducible vendor outputs and interface trial.',
            'Missing network ties, endogenous links, assignment support, arbitrary serial/cross-cluster dependence and decision-useful precision.'],
        failures=failures,bank_inputs_required_for_next_public_work=False))
    contract=dict(status='proposed_not_implemented',requirements=[
        'Declare target as conditional spatial derivative, structural equilibrium intervention, exposure-cell contrast or switchback policy contrast.',
        'Bind unit identity, receiver/source matrix convention, graph date, missing-tie policy, normalization and treatment/observation clock.',
        'Separate scalar weight reparameterization from row normalization; preserve all W changes and sample masks.',
        'Record identification assumptions: exogenous intervention and invariant equilibrium mechanism, or actual assignment/exposure law and positivity.',
        'Keep coefficient, average own derivative, indirect/total derivative and targeted portfolio sum as separately named outputs.',
        'Preserve full parameter covariance and derivative convention; distinguish conditional/unconditional uncertainty and dependence assumptions.',
        'For experiments bind randomized unit, exposure mapping, cluster linkage, outcome denominator and joint exposure probabilities.',
        'For switchbacks bind schedules, randomization, carryover horizon, attribution windows, overlap, burn-in/out and resampling unit.',
        'Reject or report unavailable unstable/singular feedback, missing labels, unsupported exposure cells, insufficient clusters and unqualified covariance.',
        'Use identical target/graph/clock/refusal schemas in library, CLI and MCP; model prose cannot manufacture missing ties or randomization.',
        'Compare exact public/generated cases and local computation first; measure native licensed cost before bank trials.'
    ],integration_allowed=False)
    write(BASE/'conversion-contract.json',contract)
    evidence=[ref(BASE/n,'Reviewed commercial network evidence') for n in ['plan.md','plan-review.json','search-review.json',
        'source-audit.json','inspected-extracts.json','exact-results.json','candidate-register.json','omissions-register.json','conversion-contract.json']]
    evidence.append(ref(Path(__file__),'Exact author review construction'))
    scope='Commercial network/interference proposal coverage; selected primary originals with explicit market/version limits'
    trigger='Complete per-family primary acquisition and complementary searches; resolve image-only formulas, editions and rights before native prototype comparison.'
    findings=[('inconclusive','Eight families/aliases and bounded stopping rule are recorded; complete candidate discovery and exact editions remain unresolved.'),
        ('pass','Nine authentic official originals support selected spatial, feedback, switchback and cluster-unit claims with hashes, dates and inspected anchors.'),
        ('pass','Alternatives, incomplete SAS downloads, Optimizely homepage redirect and unresolved formulas/rights are explicit; no absence or unavailable-source waiver.')]
    item=dict(operation_id=OP,status='inconclusive',scope=scope,reviewer=REVIEWER,cutoff='2026-10-07',
        candidates=candidates,evidence=evidence,criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)],
        limitations=LIMITS,revisit_trigger=trigger,capabilities=[],integration_allowed=False,original_gap_qualification=False)
    write(output,item)
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,output=ref(output,scope),
        criteria=item['criteria'],evidence=evidence,limitations=LIMITS))
    receipt=record(OP,output,evidence,findings,scope,trigger)
    write(BASE/'operation-receipt.json',receipt);verify_bindings([item,receipt])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',official_originals=9,candidate_families=8,native_execution=False)))


def compare():
    output=ROOT/f'docs/program/comprehensive-v14/work/{COMPARE}/vendor-comparison.json'
    assert not output.exists()
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==COMPARE
    sources=read(BASE/'source-audit.json');verify_bindings(sources)
    candidates=read(BASE/'candidate-register.json')['candidates']
    facts={
        'Stata':('Spatial SAR/GS2SLS/ML, balanced-panel models and full averaged reduced-form derivatives with covariance options.',
            'Commercial counterpart for explicit W, sample restrictions and derivative-based impact outputs; stronger documented native surface than our exact references.',
            'Our proposal adds explicit exposure/assignment and causal-target contracts; it has no matched executable implementation or superiority evidence.'),
        'SAS':('Supplied-W cross-sectional model catalog, normalization/ID policies and Hessian/OP/QML covariance choices.',
            'Relevant original engine comparator if the target is a selected spatial structural model; missing-weight and integer-ID rules need explicit guards.',
            'Public exact algebra is available; native model fitting, covariance, scaling and complete rights remain proposed.'),
        'Esri':('GIS neighborhood construction, spatial diagnostics, lag/error/combined fits, Python surface and simple impacts.',
            'Useful spatial workflow comparator; its documented simple direct impact differs from a full feedback derivative.',
            'Our target schema must preserve that distinction; no empirical accuracy, speed or integration advantage is established.'),
        'Statsig':('Assignment/analysis, switchback schedules and attribution, bucket bootstrap, and ratio inference across assignment-unit types.',
            'Concrete experimental alternative for marketplace spillovers; temporal/cross-bucket dependence and cluster boundary assumptions still require review.',
            'Our proposed contract covers explicit exposure support and temporal sensitivity, but lacks a live experiment/analysis engine and matched outcome trial.')}
    rows=[]
    for c in candidates:
        strength,comparison,gap=facts.get(c['family'],('Not evaluated for this precise network/exposure target.',
            'No capability, absence or parity finding follows from the current evidence.',c['next_public_evidence']))
        rows.append(dict(family=c['family'],selected_profile=c['aliases'],source_status=c['status'],
            documented_strength=strength,matched_proposal_comparison=comparison,observed_current_capability='Exact authored matrix, assignment and temporal references only; no vendor runtime.',
            proposed_capability='Typed target, graph/exposure, covariance and failure contract through library/CLI/MCP.',
            remaining_gap=gap,next_public_evidence=c['next_public_evidence'],
            deployment_rights='Unverified for selected distribution and use; API or availability labels are not a license grant.',
            price=dict(status='unavailable',amount=None,quote_obtained=False),runtime_executed=False,absence_claim=False))
    evidence=[ref(BASE/n,'Reviewed commercial comparison evidence') for n in ['source-audit.json','review.json','candidate-register.json',
        'omissions-register.json','exact-results.json','conversion-contract.json','plan-review.json']]
    evidence.append(ref(Path(__file__),'Candidate-specific comparison construction'))
    scope='Eight-family commercial network comparison with four documented profiles and four unresolved candidate families'
    trigger='Complete the explicit per-family acquisition/version and rights work, then design matched public/generated native comparisons before any expensive bank study.'
    item=dict(operation_id=COMPARE,status='inconclusive',reviewer=REVIEWER,scope=scope,vendors=rows,
        criteria=[dict(index=0,verdict='inconclusive',finding='Four technical profiles have primary support; exact licensed editions and four other candidate families remain unresolved.'),
            dict(index=1,verdict='pass',finding='Documented strengths, actual reference capability, proposed contract, unknown deployment rights/prices and nonexecution are distinct for every row.')],
        evidence=evidence,limitations=LIMITS,revisit_trigger=trigger,capabilities=[],integration_allowed=False,
        purchases=False,vendor_contacts=False,matched_runtime_trial=False)
    write(output,item)
    write(BASE/'comparison-review.json',dict(status='inconclusive',reviewer=REVIEWER,output=ref(output,scope),
        findings=item['criteria'],evidence=evidence,limitations=LIMITS))
    receipt=record(COMPARE,output,evidence,[(c['verdict'],c['finding']) for c in item['criteria']],scope,trigger)
    write(BASE/'comparison-receipt.json',receipt);verify_bindings([item,receipt])
    print(json.dumps(dict(operation=COMPARE,outcome='inconclusive',families=len(rows),documented_profiles=4,native_execution=False)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['coverage','compare'])
    {'coverage':coverage,'compare':compare}[p.parse_args().command]()
