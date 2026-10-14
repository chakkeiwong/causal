#!/usr/bin/env python3
"""Bind authentic vendor originals, inspected claims and exact proposal examples."""
import json
from pathlib import Path
import commercial_survival_examples_20261014 as exact
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-14/commercial-survival/v2'
REVIEWER={'name':'Codex author/coordinator','kind':'author'}
LIMITS=[
 'Official documentation and exact project constructions; no vendor runtime, actual bank sample or live-model trial.',
 'Cutoff is 2026-10-07 Asia/Shanghai. Later mutable downloads do not establish exact cutoff-era bytes.',
 'Named editions are separated from installed versions; Minitab, NCSS and Mplus exact edition/date remain unresolved.',
 'MATLAB originals returned HTTP403; missing sources establish no capability absence.',
 'Prices, entitlement, unattended execution, redistribution and benchmark-publication rights remain unverified.',
 'Nine-family bounded survey is not exhaustive market coverage; optional plugins and additional families remain omissions.',
 'Author review only; manuscript-wide depth, sponsor reconciliation and visual acceptance stay open.',
]


def main():
    completions={}
    for p in sorted(BASE.glob('acquisition-completion-*.json')):
        for row in json.loads(p.read_text()):
            assert row['status']=='fulfilled'
            completions[row['value']['session']]=row['value']
    acquired=[]
    for p in sorted(BASE.glob('acquisition-0[1-7].json')):
        for row in json.loads(p.read_text()):
            assert row['status']=='fulfilled'
            value=row['value']; result=completions[value['session_id']] if 'session_id' in value else value
            entry={k:value[k] for k in ['id','url','extension']}
            entry.update(exit_code=result['exit_code'],status='saved' if result['exit_code']==0 else 'unavailable',
                         command_record=ref(p,'Exact bounded public acquisition and outcome'),
                         headers=ref(BASE/(entry['id']+'.headers'),'Unmodified response headers'))
            raw=BASE/(entry['id']+'.'+entry['extension'])
            if raw.exists():
                entry['local_copy']=ref(raw,'Original bytes; usable only if acquisition succeeded')
                entry['bytes']=raw.stat().st_size
            if entry['status']=='saved':
                assert raw.is_file()
                if entry['extension']=='pdf':assert raw.read_bytes().startswith(b'%PDF-')
                entry['text_copy']=ref(BASE/(entry['id']+'.txt'),'Normalized extraction; originals unchanged')
            entry['observed_result']=result['output']
            acquired.append(entry)
    write(BASE/'acquisition-review.json',{'access_date':'2026-10-14','cutoff':'2026-10-07 Asia/Shanghai',
        'requests':acquired,'scope':'Public HTTPS originals; no uploads or downloaded execution.',
        'preserved_prior_failure':ref(BASE.parent/'acquisition-failure.json','Fixed collector rejected domains before HTTP'),
        'repair':'Existing approved bounded curl route; collector and permission settings unchanged. Required escalated same-URL retry recovered two SAS pages after sandbox network timeouts.',
        'search_tool_limit':'Built-in web calls returned no inspectable result payload; guessed official paths required direct byte validation.',
        'initial_preparation_failures':'Two string syntax errors preceded execution; duplicate-directory guard protected earlier evidence. Successor folder retains new work.'})
    by={r['id']:r for r in acquired}
    specs=[
      ('stata','StataCorp','Stata survival-time treatment effects and diagnostics',2026,
       'Stata 19 example route r19 in mutable official manuals; retrieved 2026-10-14, exact cutoff bytes and installed update unverified',
       [('stata_intro','physical pp1-2,11-16; targets, time-varying/delayed-entry exclusion, exchangeability, overlap and censoring'),
        ('stata_ipwra','physical pp3-6; covariance, overlap-error rule, LAC/WAC algorithms and censoring restrictions'),
        ('stata_post','physical pp1-4; propensity/censor-survival/conditional-mean exports and default treatment levels')],
       ['ATE, ATET and potential mean survival times have documented RA/IPW/IPWRA/WRA paths.',
        'The inspected stteffects family explicitly excludes delayed entry, time-varying covariates and multiple-record data.',
        'Weighted censoring variants require random, correctly modeled censoring that does not vary by treatment level in the inspected implementation.',
        'Overlap checking can return an error and flag offending observations; diagnostic plots do not prove exchangeability.']),
      ('stata_competing','StataCorp','Stata stcrreg competing-risks regression',2026,
       'Mutable official stcrreg manual retrieved 2026-10-14; installed edition/update and exact cutoff bytes unresolved',
       [('stata_stcrreg','physical pp1-4; subhazard target, competing-event coding, multiple records versus failures, covariance and time interactions')],
       ['Documented subhazard model permits single or multiple records, not multiple failures per subject.',
        'Competing-event definitions, cluster covariance and time interaction settings must survive conversion; no dynamic regime effect is inferred.']),
      ('sas','SAS Institute','SAS/STAT 14.1 PHREG counting-process and competing-risk methods',2015,
       'Explicit SAS/STAT 14.1 edition; acquired 2026-10-14; 15.1 PDF exceeded local transfer cap and is excluded',
       [('sas_overview','Overview body, Cox formulation, time-dependent covariates and listed model families'),
        ('sas_counting_retry','lines16-76; (T1,T2] intervals, recurrent-event example and delayed-entry code'),
        ('sas_competing_retry','Proportional Subdistribution Hazards section; EVENTCODE, retained competing-event risk sets, covariance, ignored options and pointwise CIF intervals')],
       ['PHREG counting-process input preserves subject intervals and within-interval covariates, including supplied recurrent-event and delayed-entry models.',
        'EVENTCODE selects a subdistribution-hazard model with modified risk sets; ASSESS/BAYES/RANDOM and named options are ignored in this edition.',
        'Cluster ID and covariance controls, CIF exports and inference settings are separate from causal regime identification.',
        'Image-only equations in HTML were not reconstructed as evidence.']),
      ('ibm','IBM','SPSS Statistics 30 computing time-dependent covariates',2025,
       'Documentation route 30.0.0; raw HTML copyright2025; accessed2026-10-14, exact historical update unknown',
       [('ibm_time','Complete procedure body; T_ interactions, segmented weekly measurements and interval boundary expressions')],
       ['T_ supports explicit time interactions and piecewise measured covariates for Cox models.',
        'Documented expression syntax does not establish longitudinal policy estimation, calibrated causal effects or a fitted adapter.']),
      ('jmp','JMP Statistical Discovery','JMP 18.1 Survival Analysis and Competing Causes',2024,
       'Help18.1 publication date2024-06-27; retrieved2026-10-14',
       [('jmp_overview','Survival platform scope and pointer to explanatory survival platforms'),
        ('jmp_competing','Complete Competing Causes body; independent-cause premise, other events censored, Omit Causes and saved coordinates')],
       ['The inspected competing-cause display treats other event times as censored and states independence for cause-wise survival interpretation.',
        'Omit Causes recalculates estimates as an illustrated removal scenario; it does not establish a bank intervention that removes prepayment.']),
      ('minitab','Minitab','Counting-process Cox method table',2026,
       'Mutable official help, copyright2026; acquired2026-10-14; exact edition/update and cutoff availability unresolved',
       [('minitab_counting','Complete Method table; repeated/time-dependent data, coding, ties, covariance, strata, PH tests and Rows unused')],
       ['Counting-process form is specified for time-dependent predictors or repeated measurements.',
        'Method settings distinguish tie rules, covariance, strata and residual-time transformation.',
        'Missing or nonpositive response rows can be excluded; entry after exit yields an error. Audit denominators accordingly.']),
      ('ncss','NCSS LLC','NCSS Chapter565 Cox Regression',2026,
       'Undated chapter565, no exact software edition; acquired2026-10-14;2026 is access year only',
       [('ncss_cox','printed565-1,565-20; procedure scope and convergence/row summary; extracted1-25,1094-1146')],
       ['Documented Cox fitting reports processed/used rows, iterations, achieved convergence and completion status.',
        'The displayed relative coefficient-change stopping statistic must accompany a result; a finite coefficient does not certify convergence or causal identification.',
        'Garbled extracted mathematical glyphs are excluded from claims.']),
      ('statistica','Cloud Software Group','Spotfire Statistica14.2 Cox regression input forms',2024,
       'Explicit14.2.0 documentation, copyright through2024; acquired2026-10-14',
       [('statistica_cox','Quick tab input types, time-function covariates, counting-process start/stop and event/censor codes')],
       ['Separate input types distinguish survival-time, explicit time-function and counting-process representations.',
        'Start/stop records specify entry/removal from the risk set; event and censor codes require explicit mapping.']),
      ('mplus','Muthen and Muthen','Mplus User Guide Chapter6 survival examples',2026,
       'Mutable undated official chapter; exact edition/date unresolved;2026 is access year only',
       [('mplus_ch6','printed149-154, examples6.19-6.22; post-event missingness, censor coding, baseline bins and latent-factor integration')],
       ['Examples distinguish discrete-time, Cox, parametric baseline and latent-factor survival specifications.',
        'Post-event and dropout missing values share a code in an example; preserve their distinct scientific reasons in an adapter.',
        'The latent-factor example uses numerical integration; supplied measurement restrictions are not automatically authenticated confounding control.']),
    ]
    sources=[]
    for ident,author,title,year,version,anchors,claims in specs:
        entries=[]
        for name,anchor in anchors:
            a=by[name];assert a['status']=='saved'
            entries.append({'source_identity':a['url'],'local_copy':ref(ROOT/a['local_copy']['path'],anchor),
                            'text_copy':ref(BASE/(name+'.txt'),anchor),'inspected_anchor':anchor})
        sources.append({'integrated_citation_key':'exec14_survival_'+ident,'kind':'software_primary_sources',
            'author':author,'title':title,'year':year,'source_identity':entries[0]['source_identity'],
            'version_date':version,'local_copy':entries[0]['local_copy'],'additional_sources':entries,
            'inspected_anchors':[a for _,a in anchors],'supported_claims':claims,'limitations':LIMITS})
    write(BASE/'primary-review.json',{'reviewer':REVIEWER,'status':'pass_bounded_primary_review',
        'source_records':sources,'cutoff':'2026-10-07 Asia/Shanghai','limitations':LIMITS,
        'scope_extension':'Retain inherited Mplus candidate as ninth family, avoiding loss of a prior unresolved lead; acquired its single official chapter.',
        'source_integrity':'All originals remain byte-identical; only separate plain-text derivatives were created.'})
    results=exact.calculate();write(BASE/'exact-results.json',results)
    write(BASE/'derivation-review.json',{'status':'pass','reviewer':REVIEWER,
        'evidence':[ref(BASE/'exact-results.json','Five authored constructions'),ref(ROOT/'tools/commercial_survival_examples_20261014.py','Rational arithmetic and independent full-law enumeration')],
        'findings':['Competing-event recursion and independent categorical path enumeration agree; net-risk removal needs unchanged cause hazard as an extra premise.',
         'Future-defined exposure creates a spurious25-point risk difference in stipulated counts; survivor landmark changes the target.',
         'Sixteen-state law gives observed late-treatment risks .18/.37 but fixed-regime risks .42/.13; full joint IPW agrees with the g-formula.',
         'Complete-case .20 versus full-cohort .35 follows known conditional observation probabilities; inverse weights recover .35 only under stated premises.',
         'Rare-path absence in an eight-subject bootstrap has exact probability (7/8)^8; dropping failures changes the replication law.'],
        'claims_not_made':'No fitted Cox bias estimate, vendor runtime failure rate, empirical bank effect or package performance superiority.'})
    candidates=[{'candidate':s['author'],'source_record':s['integrated_citation_key'],'disposition':'bounded primary comparison; licensed runtime and cutoff identity limitations retained'} for s in sources if s['integrated_citation_key']!='exec14_survival_stata_competing']
    candidates.append({'candidate':'MATLAB / fitcox / coxphfit','disposition':'HTTP403 for both originals; unknown_not_absent'})
    omissions=[
        {'candidate':'MATLAB','gap':'Both official method routes returned403; no technical capability finding.','next':'Obtain an accessible version-specific original through an authorized route.'},
        {'candidate':'Exact historical and installed editions','gap':'Mutable manuals plus undated NCSS/Mplus and unversioned Minitab cannot certify exact cutoff bytes.','next':'Acquire dated archived versions or retain strictly access-date-bounded claims.'},
        {'candidate':'SAS15.1 full PHREG manual','gap':'Exceeds12MiB bound; excluded. Two14.1 pages timed out and succeeded on required escalated retry.','next':'14.1 is the documented comparison; qualify later edition only when needed.'},
        {'candidate':'Wider families and extensions','gap':'LIMDEP, SYSTAT, BMDP, nQuery and vendor/community dynamic-regime macros were not systematically inspected.','next':'Separate candidate/alias search and original-method/rights reviews; no absence claim.'},
        {'candidate':'Licensed execution and economics','gap':'No installed vendor runs, matched price quote, unattended/embedding rights or benchmark-publication terms.','next':'After public/generated prototype merit, select edition, acquire intended entitlement and run a frozen matched comparison.'},
        {'candidate':'Scholarly works referenced by manuals','gap':'Not newly cited or treated as theorem originals.','next':'Acquire genuine correctly named PDFs before new scholarly attributions.'},
    ]
    write(BASE/'candidate-register.json',{'candidates':candidates,'families':9,'families_with_primary':8,
        'bounded_scope':'Earlier six families retained; Minitab, NCSS and Statistica added; no market census completion.',
        'plan':ref(BASE/'plan-review.md','Reviewed scope; inherited Mplus addition explicitly retained'),
        'search':ref(BASE/'search-ledger.json','Discovery limits'),
        'acquisition':ref(BASE/'acquisition-review.json','Every attempted source and failure')})
    write(BASE/'omissions-register.json',{'items':omissions,'status':'coverage_inconclusive','essential_source_waiver':False})
    for key,kind,title,path,anchor,claims in [
        ('exact','project_derivation','Exact longitudinal and competing-event banking comparisons',BASE/'exact-results.json','Five exact construction families',
         ['Competing events and value','Time-zero and future-defined exposure','Sequential confounding and full-law weighting','Conditional censoring correction','Rare-path bootstrap omission']),
        ('survey','project_design','Bounded commercial survival comparison and qualification design',BASE/'candidate-register.json','Nine-family dispositions and all acquisition outcomes',
         ['Bounded alternatives and omissions','Documented versus local prototype capability','Proposed target-preserving adapters and later qualification'])]:
        sources.append({'integrated_citation_key':'exec14_survival_'+key,'kind':kind,'author':'Causal banking proposal',
            'title':title,'year':2026,'version_date':'Project2026-10-14; exact bytes bound by SHA-256',
            'source_identity':'Project-authored '+kind,'local_copy':ref(path,anchor),'inspected_anchors':[anchor],
            'supported_claims':claims,'records':[{'local_copy':ref(p,'Author-reviewed supporting artifact')} for p in
             [BASE/'derivation-review.json',BASE/'primary-review.json',BASE/'omissions-register.json',
              ROOT/'src/causalbank/operation_service_v12.py',Path(__file__).resolve()]],'limitations':LIMITS})
    write(BASE/'source-audit.json',{'sources':sources,'cutoff':'2026-10-07 Asia/Shanghai','limitations':LIMITS})
    verify_bindings(json.loads((BASE/'source-audit.json').read_text()))
    print(json.dumps({'saved_acquisitions':sum(r['status']=='saved' for r in acquired),'attempts':len(acquired),
                      'primary_records':len(specs),'new_citation_records':len(sources),'families':9,'math':'pass','coverage':'inconclusive'}))


if __name__=='__main__':main()
