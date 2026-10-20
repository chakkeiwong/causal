"""Source-grounded commercial mediation comparison; no vendor execution."""
import argparse
import json
from pathlib import Path
import mediation_reference_20261020 as exact
import run_program_reviews_v2 as extension
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

run = extension.base
core = run.core
ROOT = core.ROOT
BASE = ROOT/'docs/program/execution/2026-10-20/mediation-commercial-v1'
OP = 'SW.CELL.mediation_sensitivity.commercial'
COMPARE = 'SW.COMM.mediation_sensitivity'
REVIEWER = dict(name='Codex author/coordinator', kind='author')
read = lambda p: json.loads(p.read_text())
LIMITS = [
    'Five named candidate families and selected technical originals are a bounded survey, not complete commercial coverage.',
    'Post-cutoff acquisitions and PDF metadata do not authenticate exact cutoff-era bytes, licensed editions or current entitlements.',
    'StataNow two-mediator availability is distinct from one-mediator Stata; Mplus selected chapter metadata is March2017.',
    'SAS incomplete PDFs and generic Help Center shells, PROCESS TLS failure and IBM404 do not support absence claims.',
    'Linked scholarly references are uninspected leads; no theorem claim is borrowed without genuine inspected originals.',
    'No vendor engine, downloaded package, live model or sibling repository was executed.',
    'Exact authored examples are not measured native defects, calibration, costs or bank value.',
    'Mandatory repairs, Q1/Q5, rendered review and final proposal acceptance remain open.']


def source(key, original, text, title, author, url, version, ranges, claims, receipt=None):
    body=text.read_text(); lines=body.splitlines(keepends=True)
    anchors=[]
    for lo,hi in ranges:
        assert 1 <= lo <= hi <= len(lines)
        anchors.append(dict(anchor=f'extracted lines {lo}-{hi}',
            physical_page=''.join(lines[:lo-1]).count(chr(12))+1 if original.suffix=='.pdf' else None,
            inspected_text=''.join(lines[lo-1:hi])))
    result=dict(integrated_citation_key=key,kind='official_documentation',title=title,author=author,
        year=2017 if 'March2017' in version else 2026,source_identity=url,version_date=version,
        cutoff='2026-10-07',local_copy=ref(original,'Authentic original; no historical-byte inference'),
        text_copy=ref(text,'Inert extracted primary text'),inspected_anchors=anchors,
        supported_claims=claims,limitations=LIMITS)
    if receipt:
        r=read(receipt)
        assert r['returncode']==0 and r['sha256']==core.sha(original)
        result['receipt']=ref(receipt,'Fixed HTTPS acquisition')
    return result


def make_receipt(operation, output, evidence, findings, scope, trigger):
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==operation
    graph,_,_=run.combined(ROOT,state)
    receipt=run.ledger.receipt_template(run.ledger.operation(graph,operation))
    receipt.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=REVIEWER,
        capabilities=[],outputs=[ref(output,'Bounded proposal review')],limitations=LIMITS,
        nonexecution_reason='',revisit_trigger=trigger,
        criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)])
    return receipt


def coverage():
    assert not (BASE/'source-audit.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    old=ROOT/'docs/program/execution/2026-10-13/commercial-identification'
    previous=read(old/'source-audit.json')
    inherited=next(s for s in previous['sources'] if s['integrated_citation_key']=='exec13_ci_stata_mediate')
    verify_bindings(inherited)
    a=BASE/'acquisition/network';t=BASE/'text'
    sources=[source('exec20_med_stata_one', ROOT/inherited['local_copy']['path'],old/'stata_mediate.txt',
        'Stata mediate: one-mediator targets, interactions and identifying assumptions','StataCorp',
        inherited['source_identity'],inherited['version_date'],
        [(9,17),(61,81),(136,141),(175,177),(296,365),(391,405),(574,668)],
        ['One-mediator models support selected continuous/binary/count outcome and mediator combinations; some links cannot be combined.',
         'Treatment-mediator interaction is included by default; natural total/pure direct and indirect contrasts differ under interaction.',
         'The displayed mediation integral requires treatment and mediator ignorability, overlap and no treatment-induced mediator-outcome confounder.',
         'Robust, cluster, bootstrap and jackknife variance options are documented; actual dependent-law calibration is not established here.'])]
    specs=[
        ('stata_intro','Introduction to causal mediation analysis','StataCorp',
         'Official manual; metadata28July2026; specific licensed edition and cutoff bytes unresolved',
         [(7,18),(118,148)],
         ['Defines the workflow from question and decomposition to assumptions, estimation and interpretation.',
          'Linear no-interaction models provide a limited correspondence with classical coefficient-product effects.']),
        ('stata_post','Stata mediate postestimation: controlled effects and scale','StataCorp',
         'Official manual; metadata28July2026; licensed edition unresolved',
         [(154,162),(269,298),(303,308)],
         ['Controlled effects require explicit mediator values; default covariate averaging differs from atmeans.',
          'Proportion mediated normally refuses conflicting effect signs; force overrides the refusal, not its interpretive problem.',
          'Odds/risk/incidence-rate scales use potential-outcome means and may trigger model refitting.']),
        ('stata_multiple','StataNow mediate multiple: two-mediator models','StataCorp',
         'Explicit StataNow feature; metadata28July2026; historical entitlement and update date unresolved',
         [(1,20),(25,38),(64,74),(128,154),(407,422),(648,656)],
         ['Selected two-mediator syntax restricts outcomes and both mediators to continuous variables and treatment to binary/continuous.',
          'Parallel and sequential models, interaction switches and multiple decompositions are documented.',
          'The displayed model assumes independent zero-mean errors and no unmeasured confounding across the mediator/outcome system.']),
        ('mplus_ch17','Mplus User Guide Chapter17: conventional and counterfactual mediation','Muthen and Muthen',
         'Selected official chapter; metadata25March2017, printedpp759-766; current licensed version unresolved',
         [(2226,2277),(2363,2439),(2517,2530)],
         ['MODEL INDIRECT distinguishes conventional coefficient products from counterfactually defined effects.',
          'Conventional effects for categorical variables use latent response variables; multiple mediators are documented for that branch.',
          'The counterfactual branch documents one mediator and IND/MOD syntax, treatment-mediator moderation and controlled effects.',
          'Delta standard errors are default, with bootstrap/interval options; MOD covariates are evaluated at zero or means after centering.',
          'Selected command is unavailable with TYPE=RANDOM, VARIABLE CONSTRAINT and TYPE=EFA.'])]
    for name,title,author,version,ranges,claims in specs:
        sources.append(source('exec20_med_'+name,a/(name+'.pdf'),t/(name+'.txt'),
            title,author,read(a/(name+'.receipt.json'))['url'],version,ranges,claims,a/(name+'.receipt.json')))
    f=BASE/'followups/acquisition/network'
    sources.append(source('exec20_med_process_lead',f/'hayes_book.html',f/'hayes_book.txt',
        'PROCESS author website: supported hosts and documentation leads','Andrew F. Hayes',
        read(f/'hayes_book.receipt.json')['url'],
        'Mutable author website acquired20October2026; no frozen software version',
        [(39,43),(55,72)],
        ['Author website identifies PROCESS for SPSS,SAS and R and version-sensitive documentation.',
         'This establishes a separate extension candidate; it supplies no inspected current numerical algorithm or host entitlement.'],
        f/'hayes_book.receipt.json'))
    sources.append(dict(integrated_citation_key='exec20_med_reference',kind='project_derivation',
        title='Exact mediation decomposition, nonidentification and sensitivity references',
        author='Causal banking proposal project',year=2026,
        source_identity='tools/mediation_reference_20261020.py',version_date='20October2026',
        local_copy=ref(ROOT/'tools/mediation_reference_20261020.py','Independent finite-law and rational calculations'),
        inspected_anchors=[ref(BASE/'exact-results.json','All exact constructions')],
        supported_claims=['Interaction example total15 decomposes as6+9 or9+6; controlled effects4,6,9.',
            'Two randomized-treatment worlds have identical observed distributions and total effect1 but opposite natural decompositions.',
            'Independent mediator-only interventions have zero effect in the explicit worlds; assumed margins80/-20 compare different actions.',
            'Average-versus-mean-covariate effects1/5 and1/10 yield assumed margins5/-5.',
            'Inconsistent mediation gives proportion-2; residual-correlation scenarios give indirect-effect set[4,8], not a probability interval.'],
        limitations=exact.calculate()['limits']))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',limitations=LIMITS))
    write(BASE/'inspected-extracts.json',dict(sources=[dict(key=s['integrated_citation_key'],anchors=s['inspected_anchors']) for s in sources]))
    candidates=[
        dict(family='Stata',profile='One-mediator mediate plus separate StataNow two-mediator manual',
             status='selected_primary_methods_inspected',next_action='Bind exact licensed edition and historical StataNow availability; complete sensitivity/negative-control search and rights.'),
        dict(family='Mplus',profile='Selected March2017 Chapter17 MODEL INDIRECT',
             status='selected_primary_methods_inspected',next_action='Bind exact edition, technical derivations, sensitivity options and licensed deployment; do not infer current absence from historical single-mediator scope.'),
        dict(family='SAS',profile='SAS/STAT15.1 CAUSALMED candidate',
             status='essential_original_incomplete',next_action='Acquire complete official manual; timeout partial and generic15.2 Help Center shells support no estimator claim.'),
        dict(family='IBM SPSS/AMOS',profile='Standalone AMOS and SPSS-hosted extensions are separate candidates',
             status='exact_edition_not_inspected',next_action='Use authentic public23.0 directory or supported current documentation; guessed29.0 manual route404 does not establish absence.'),
        dict(family='PROCESS',profile='Independent extension for SPSS,SAS,R; commercial host is not extension supplier',
             status='author_identity_lead_only',next_action='Acquire versioned original documentation/code and terms via valid TLS route; book page is a lead, not inspected technical text.')]
    write(BASE/'candidate-register.json',dict(candidates=candidates,cutoff='2026-10-07',
        market_census_complete=False,stopping_rule='Bounded five-family inherited-lead and primary-route review; complementary discovery, sensitivity/negative controls and three technical originals remain unresolved.'))
    failures=[]
    for p in sorted(BASE.glob('**/*.receipt.json')):
        r=read(p)
        if r.get('returncode')!=0 or r.get('id') in ['sas_overview','sas_details']:
            failures.append(ref(p,'Failed acquisition or generic shell; no capability/absence proof'))
    write(BASE/'omissions-register.json',dict(global_blocker=False,candidates=candidates,failures=failures,
        additional=['Complete cross-family and negative-control/sensitivity discovery.',
            'Exact pre-cutoff editions, licenses, distribution/embedding rights and prices.',
            'Native numerical/uncertainty comparison on generated public mechanisms.',
            'Genuine linked scholarly originals before importing their technical claims.']))
    write(BASE/'search-review.json',dict(status='bounded_incomplete',cutoff='2026-10-07',
        evidence=[ref(BASE/'inherited-source-inventory.json','Failed inherited query and original inventory'),
            ref(BASE/'omissions-register.json','Observed acquisition limits')],
        finding='Source-specific navigation recovers Stata and Mplus technical text; SAS generic HTML is not a successful methods acquisition. No exhaustive search or absence claim.'))
    write(BASE/'plan-review.json',dict(status='pass',reviewer=REVIEWER,
        evidence=[ref(BASE/'plan.md','Reviewed question and scope'),ref(BASE/'search-review.json','Bounded discovery review')],
        findings=['Inspect effect definitions and assumptions before comparing labels.',
            'Keep StataNow, historical Mplus and independent PROCESS identities separate.',
            'Use exact examples to expose interaction, cross-world assumptions, covariate population and scenario uncertainty.',
            'Retain missing originals and no native admission; continue other eligible work.']))
    write(BASE/'conversion-contract.json',dict(status='proposed_not_implemented',integration_allowed=False,
        inputs=['Exposure/mediator/outcome clocks and approved graph with latent-confounding limitations',
            'Natural,controlled,interventional or path-specific target, exposure values and mediator reference',
            'Outcome scale, link, interaction structure, target covariate population and support',
            'Dependence/resampling unit, numerical settings and source/version identity',
            'Sensitivity parameter definition, range and whether identified, assumed or externally supplied'],
        outputs=['Typed decomposition and potential-outcome means; no incompatible pair summation',
            'Uncertainty type, full covariance, errors, unsupported status and refusal reasons',
            'Proportion-mediated denominator/sign diagnostics; no automatic force override',
            'Separate sensitivity range and statistical interval; identical meaning through library/CLI/MCP'],
        public_experiments=['Interaction exact means and decomposition parity',
            'Identical-law nonidentification and mediator-only interventions',
            'Covariate averaging versus atmeans and effect-scale conversions',
            'Sparse support, inconsistent mediation, failed fits and shared-calendar dependence',
            'Native validation only after edition, environment and rights qualification']))
    evidence=[ref(BASE/n,'Reviewed mediation evidence') for n in ['source-audit.json','inspected-extracts.json',
        'exact-results.json','candidate-register.json','omissions-register.json','search-review.json','plan-review.json','conversion-contract.json']]
    evidence.append(ref(Path(__file__),'Exact author review'))
    findings=[('inconclusive','Five families and aliases are explicit; complete search, exact editions and three essential technical originals remain open.'),
        ('pass','Five selected authentic technical manuals, one author-host identity page and exact authored references have hashes and inspected anchors.'),
        ('pass','Alternatives, failed downloads, generic shells, TLS/403/404 results and omissions are explicit without absence or source waivers.')]
    output=ROOT/f'docs/program/comprehensive-v14/work/{OP}/coverage-review.json'
    scope='Commercial mediation proposal coverage; bounded original-source comparison'
    trigger='Recover missing originals and version/rights details; extend sensitivity and negative-control searches before claiming coverage.'
    write(output,dict(operation_id=OP,status='inconclusive',scope=scope,reviewer=REVIEWER,
        evidence=evidence,limitations=LIMITS,candidates=candidates,capabilities=[],integration_allowed=False,
        criteria=[dict(index=i,verdict=v,finding=f) for i,(v,f) in enumerate(findings)]))
    write(BASE/'review.json',dict(status='inconclusive',scope=scope,evidence=evidence,
        output=ref(output,'Bounded coverage'),limitations=LIMITS))
    write(BASE/'operation-receipt.json',make_receipt(OP,output,evidence,findings,scope,trigger))
    verify_bindings(read(BASE/'source-audit.json'))
    print(json.dumps(dict(operation=OP,outcome='inconclusive',sources=len(sources),technical_manuals=5)))


def compare():
    sources=read(BASE/'source-audit.json');verify_bindings(sources)
    candidates=read(BASE/'candidate-register.json')['candidates']
    facts={
        'Stata':('Documented parametric natural and controlled effects, interaction, potential-outcome means and multiple variance methods; separate continuous two-mediator StataNow models.',
            'Our exact references and proposed typed semantics do not match its documented estimation surface; no working vendor adapter or parity trial exists.'),
        'Mplus':('Documented conventional and counterfactual branches, latent-variable modeling, IND/MOD, controlled effects and delta/bootstrap intervals.',
            'Our proposal must distinguish latent-response coefficient products, nested means, covariate reference points and missing identification; current native capability is untested.')}
    rows=[]
    for c in candidates:
        strength,gap=facts.get(c['family'],('Not technically evaluated for a matched edition.',c['next_action']))
        rows.append(dict(**c,documented_strength=strength,observed_current='Exact authored references only; no vendor execution',
            proposed='Typed target,clock,scale,assumptions,uncertainty and sensitivity through library/CLI/MCP',
            remaining_gap=gap,deployment_rights='Unverified for concrete product/edition and embedding use',
            price=dict(status='unavailable',amount=None,quote_obtained=False),absence_claim=False,runtime_executed=False))
    evidence=[ref(BASE/n,'Bounded vendor comparison basis') for n in ['source-audit.json','review.json',
        'candidate-register.json','omissions-register.json','conversion-contract.json','exact-results.json']]
    evidence.append(ref(Path(__file__),'Author vendor comparison'))
    findings=[('inconclusive','Two families have selected technical profiles; three families, licensed editions and full sensitivity coverage remain unresolved.'),
        ('pass','Documented strengths, actual local references, proposed capability, unavailable prices and untested rights/runtime are distinguished for every candidate.')]
    scope='Five-family commercial mediation comparison with two inspected technical profiles'
    trigger='Complete family-specific original and edition research, then design matched public/generated prototype comparisons.'
    output=ROOT/f'docs/program/comprehensive-v14/work/{COMPARE}/vendor-comparison.json'
    item=dict(operation_id=COMPARE,status='inconclusive',scope=scope,reviewer=REVIEWER,vendors=rows,
        evidence=evidence,limitations=LIMITS,capabilities=[],integration_allowed=False,purchases=False,vendor_contacts=False)
    write(output,item)
    write(BASE/'comparison-review.json',dict(status='inconclusive',evidence=evidence,
        output=ref(output,scope),limitations=LIMITS))
    write(BASE/'comparison-receipt.json',make_receipt(COMPARE,output,evidence,findings,scope,trigger))
    print(json.dumps(dict(operation=COMPARE,outcome='inconclusive',families=len(rows))))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['coverage','compare'])
    {'coverage':coverage,'compare':compare}[parser.parse_args().command]()
