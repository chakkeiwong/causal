#!/usr/bin/env python3
"""Review selected commercial dynamic-panel originals without claiming parity."""
import json
from pathlib import Path

import dynamic_panel_reference_20261019 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-19/dynamic-commercial-v1'
PRIOR = ROOT / 'docs/program/execution/2026-10-13/commercial-temporal'
OP = 'SW.CELL.dynamic_panel_timeseries.commercial'
OUTPUT = ROOT / f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())


def source(name, title, author, ranges, claims, extension='pdf'):
    original = BASE / 'acquisition' / (name + '.' + extension)
    receipt_path = BASE / 'acquisition' / (name + '.receipt.json')
    receipt = read(receipt_path)
    assert receipt['returncode'] == 0 and core.sha(original) == receipt['sha256']
    text = BASE / (name + '.txt')
    # Keep splitlines and form-feed page tracking separate; extracted originals
    # remain authoritative for character and equation-layout ambiguities.
    body = text.read_text(); lines = body.splitlines(keepends=True)
    anchors = []
    for lo, hi in ranges:
        assert 1 <= lo <= hi <= len(lines), (name, lo, hi)
        anchors.append(dict(anchor=f'extracted lines {lo}-{hi}',
            physical_page=body[:sum(len(s) for s in lines[:lo-1])].count(chr(12))+1 if extension=='pdf' else None,
            inspected_text=''.join(lines[lo-1:hi])))
    version = ('Official Stata manual; PDF metadata 28 July 2026; retrieved 19 October 2026' if extension=='pdf'
        else 'EViews help displays 12 March 2025 update; exact edition unresolved; retrieved 19 October 2026')
    record = dict(integrated_citation_key='exec19_dynamic_'+name, kind='official_documentation',
        title=title, author=author, year=2026 if extension=='pdf' else 2025,
        source_identity=receipt['url'], version_date=version, cutoff='2026-10-07',
        accessed_utc=receipt['finished_at'], local_copy=ref(original, 'Authentic official technical bytes'),
        text_copy=ref(text, 'Inert text extraction; original authoritative'),
        acquisition_receipt=ref(receipt_path, 'Fixed public HTTPS request and preserved outcome'),
        headers=ref(BASE / 'acquisition' / (name+'.headers'), 'Original response headers'),
        inspected_anchors=anchors, supported_claims=claims,
        limitations=['Post-cutoff retrieval and embedded/displayed dates do not authenticate exact cutoff-era bytes.',
            'No paid engine, exact entitlement, licensed runtime, release-wide support or bank performance verified.'])
    if extension=='pdf':
        record['pdf_metadata']=ref(BASE/(name+'-pdfinfo.txt'),'Observed metadata, not historical byte proof')
    return record


def main():
    assert not OUTPUT.exists() and not (BASE/'source-audit.json').exists()
    verify_bindings(read(BASE/'plan-review.json'))
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    new=[source('stata_ab','Stata xtabond: Arellano-Bond linear dynamic panel-data estimation','StataCorp',
        [(8,14),(70,82),(104,114),(239,249),(634,654)],
        ['Designed for many panels and few dates with no idiosyncratic autocorrelation; covariate timing classes determine instrument lags.',
         'Robust one-step and Windmeijer-corrected two-step variance are distinct; Sargan use has homoskedasticity limitations.',
         'Instrument counts grow quadratically in time; excessive moments can perform poorly in small samples.']),
        source('stata_system','Stata xtdpdsys: Arellano-Bover/Blundell-Bond dynamic panel-data estimation','StataCorp',
            [(8,15),(104,116),(136,169)],
            ['System estimation adds lagged-difference instruments for level equations, conditional on an initial-condition orthogonality restriction.',
             'Persistence motivates the extra moments but does not establish their validity; many-panel/few-date and error restrictions remain.']),
        source('stata_lp','Stata lpirf: Local-projection impulse-response functions','StataCorp',
            [(8,25),(36,90),(108,145)],
            ['Joint multistep local projections and exogenous dynamic multipliers have explicit horizon and lag controls.',
             'OLS, robust and HAC variance options differ; dfk and small change finite-sample presentation, not identification.',
             'Trailing horizons reduce usable observations; local projection flexibility is not an instrument or structural restriction.']),
        source('eviews_panel','EViews Help: Estimating a Panel Equation','EViews',
            [(99,121),(157,222),(314,316)],
            ['Panel GMM exposes differences, orthogonal deviations, dynamically expanding instruments and lag restrictions.',
             'Selected panel covariance labels distinguish period, individual and two-way clustering; transformation choices restrict some GMM weights.',
             '@DYN with20dates is described as171instruments for one series; @LEV preserves a level instrument in a transformed equation.'], extension='html')]
    inherited_audit=read(PRIOR/'source-audit.json');verify_bindings(inherited_audit)
    keys=['exec13_ct_stata_svar','exec13_ct_stata_ivsvar','exec13_ct_sas_causal',
        'exec13_ct_sas_structural','exec13_ct_ibm_tcm','exec13_ct_mplus81']
    inherited=[s for s in inherited_audit['sources'] if s['integrated_citation_key'] in keys]
    assert len(inherited)==6
    reference=dict(integrated_citation_key='exec19_dynamic_reference',kind='project_authored_exact_reference',
        title='Exact initial-condition and common-calendar examples for dynamic banking panels',
        author='Causal banking proposal project',year=2026,source_identity='tools/dynamic_panel_reference_20261019.py',
        version_date='19 October 2026',local_copy=ref(ROOT/'tools/dynamic_panel_reference_20261019.py','calculate: complete finite laws and moment/variance identities'),
        inspected_anchors=[dict(anchor='calculate()',inspection='Rational enumeration of16initial-condition states and256common-calendar states')],
        supported_claims=['Selected level-equation instrument moment is1/2under one initialization and0under the declared mean-stationary initialization.',
            'Common-date law has variance1/T+1/(NT); treating rows as independent gives2/(NT). For100panels25dates ratio is101/2.',
            'At stipulated10000USDscale, actual standard deviation is approximately2010USD versus283USDunder false row independence.',
            'All period-specific lag-level instruments for one series yield(T-1)(T-2)/2, hence171atT20.'],
        limitations=['Authored synthetic laws, not commercial runtime, general GMM qualification, confidence coverage or observed bank outcomes.'])
    write(BASE/'exact-results.json',exact.calculate())
    write(BASE/'source-audit.json',dict(sources=new+[reference],inherited_sources=inherited,cutoff='2026-10-07',
        prior_audit=ref(PRIOR/'source-audit.json','Unchanged original technical identities'),
        sources_executed=False,complete_coverage=False))
    extracts=[]
    for s in new+inherited:
        extracts.append(dict(identity=s['source_identity'],local_copy=s['local_copy'],
            anchors=s['inspected_anchors'],supported_claims=s['supported_claims']))
    write(BASE/'inspected-extracts.json',dict(sources=extracts,inspection='Selected primary passages; no native execution'))
    findings={
        'Stata':('selected_technical_originals','Difference/system GMM and local projections now have inspected manuals; existing SVAR and IV-SVAR originals retain structural and instrument premises.',
            'Verify exact licensed edition, command availability, full postestimation specification and operating/embedding terms before a native comparison.'),
        'EViews':('selected_technical_original','Panel GMM transformations, instruments and covariance labels are documented; system-GMM or every setting combination is not inferred.',
            'Acquire edition-matched full algorithms and command/export contracts; resolve the printed GMM-weight label ambiguity against an exact version.'),
        'SAS':('partial_inherited_originals','VARMAX Granger and lower-triangular dynamic-representation prose is inspected; dynamic-panel procedure and equation-image details remain unreviewed.',
            'Obtain exact SAS PANEL/dynamic-GMM originals, full equations and the selected product entitlement.'),
        'MathWorks':('essential_primary_unavailable','The selected official varm.irf route returned403; preserved failure is not an absence finding.',
            'Acquire authentic release-matched Econometrics Toolbox VAR/IRF and dynamic-panel documentation through an authorized alternative or supplied original.'),
        'IBM':('partial_inherited_original','TCM overview explicitly uses predictive Granger meaning; detailed settings and a dynamic-panel causal estimator are not established.',
            'Inspect actual edition-specific build/covariance and dynamic-panel implementation text.'),
        'Mplus':('partial_inherited_original','DSEM/RDSEM supplied-model syntax and missing-covariate restrictions are documented; complete dynamic-panel/GMM equivalence is not established.',
            'Bind selected model, estimator and inferential target to edition-specific technical documentation; distinguish supplied latent model from causal discovery.'),
        'OxMetrics':('essential_primary_unavailable','Earlier PcGive official routes failed; no dynamic-panel estimator or absence claim follows.',
            'Find an authentic PcGive dynamic-panel/Autometrics manual and selected edition rights.'),
        'Commercial hosted open-source frontends':('concrete_candidate_unresolved','No named service edition and numerical backend is established for this cell.',
            'Identify vendor, edition, backend revision and target-preserving export before comparing features or prices.')}
    candidates=[]
    for c in read(BASE/'plan.json')['candidates']:
        status,claim,action=findings[c['family']]
        candidates.append(dict(**c,status=status,documented_scope=claim,next_public_evidence=action,
            runtime_executed=False,price=None,entitlement_verified=False,absence_claim=False))
    write(BASE/'candidate-register.json',dict(cutoff='2026-10-07',candidates=candidates,
        scope='Eight named families/leads; no exhaustive market census',stopping_rule=read(BASE/'plan.json')['stopping_rule']))
    omissions=[dict(family=c['family'],gap=c['next_public_evidence'],trigger='Authentic selected source/version and independently reviewed claim; native trial later') for c in candidates]
    omissions += [dict(family='All comparisons',gap='Matched prices, rights, native runtime, exact cutoff bytes and complete long/short panel coverage remain unresolved.',
        trigger='Authenticated scope-specific originals and later prototype protocol; public source work proceeds now')]
    write(BASE/'omissions-register.json',dict(items=omissions,market_wide_absence_claim=False,bank_inputs_required_for_next_public_work=False))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',requirements=[
        'Bind target as predictive lag test, supplied structural shock, dynamic multiplier or policy intervention; preserve units and shock normalization.',
        'Declare N,T, actual common calendar, missing dates, panel keys and information availability before selecting an asymptotic regime.',
        'Record each regressor timing class, exact instrument columns and lags, rank/count, transformations, one/two-step weights and initial-condition assumptions.',
        'Keep moment validity, covariance estimation, diagnostic nonrejection and optimizer convergence distinct.',
        'Record horizon-specific sample sizes, HAC kernel/bandwidth or cluster unit and effective cluster count; distinguish pointwise and joint uncertainty.',
        'Preserve unsupported settings, weak/invalid moments, singular matrices, nonconvergence and missing output; do not turn them into zero effects.',
        'Compare complete public/generated cases under the same target, sample, normalization and cost accounting before proposing a licensed bank experiment.'],
        integration_allowed=False))
    limits=['Four new official originals and six inherited technical records support selected scope, not an exhaustive commercial census.',
        'Historical metadata does not prove exact cutoff bytes; prices, rights, support and licensed runtime remain unverified.',
        'MathWorks403 and earlier source failures are preserved as acquisition gaps, never product absence.',
        'Exact project moments and variance identities do not establish arbitrary dependence or commercial finite-sample performance.',
        'Proposal manuscript integration and final/visual acceptance remain separate; no executable capability is granted.']
    evidence=[ref(BASE/n,'Reviewed commercial dynamic-panel evidence') for n in
        ['plan.json','plan-review.json','source-audit.json','inspected-extracts.json','candidate-register.json',
         'omissions-register.json','conversion-contract.json','exact-results.json']]
    evidence += [ref(BASE/'acquisition/matlab_irf.receipt.json','Preserved403original route'),
        ref(Path(__file__),'Exact criterion review and output construction')]
    criteria=[dict(index=0,verdict='inconclusive',finding='Eight families/leads, aliases, cutoff and stopping rule are explicit; exact editions and complete candidate discovery remain unresolved.'),
        dict(index=1,verdict='pass',finding='Four new authentic technical originals and unchanged selected inherited identities support narrowly stated claims; all new sources have hashes, date limits and inspected anchors.'),
        dict(index=2,verdict='pass',finding='Alternatives and every known source/rights/runtime omission have public-evidence routes; no unavailable original is waived as proof of absence.')]
    coverage=dict(operation_id=OP,status='inconclusive',reviewer=REVIEWER,scope='Commercial dynamic-panel/time-series coverage with bounded public originals',
        cutoff='2026-10-07',candidates=candidates,evidence=evidence,criteria=criteria,limitations=limits,
        revisit_trigger='Execute the per-family public routes in omissions-register.json; native licensed trials and bank validation are later gates.',
        capabilities=[],integration_allowed=False,original_gap_qualification=False)
    write(OUTPUT,coverage)
    write(BASE/'review.json',dict(status='inconclusive',reviewer=REVIEWER,criteria=criteria,
        output=ref(OUTPUT,'Scoped dynamic-panel/time-series coverage'),evidence=evidence,limitations=limits))
    graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,OP))
    receipt.update(outcome='inconclusive',execution='performed',scope=coverage['scope'],reviewer=REVIEWER,
        capabilities=[],outputs=[ref(OUTPUT,'Contracted coverage result')],limitations=limits,nonexecution_reason='',
        revisit_trigger=coverage['revisit_trigger'],criteria=[dict(**c,evidence=evidence) for c in criteria])
    write(BASE/'operation-receipt.json',receipt)
    verify_bindings([coverage,receipt,read(BASE/'source-audit.json')])
    print(json.dumps(dict(operation=OP,outcome='inconclusive',new_originals=4,inherited_originals=6,candidates=8)))


if __name__=='__main__':
    main()
