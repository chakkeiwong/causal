#!/usr/bin/env python3
"""Recover saved public documentation; independently review exact target arithmetic."""
import hashlib
import json
from pathlib import Path
import re
from fractions import Fraction as F
from itertools import product
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-13/commercial-heterogeneity'
ref=shared.ref

def save(name,value):
    path=BASE/name
    assert not path.exists(), f'Preserve {path}'
    core.write(path,value)

def main():
    protocol=json.loads((BASE/'search-protocol.json').read_text())
    requests={r['id']:r for r in protocol['requests']}
    for stem,tail in [('jmp_models','causal-treatment-models'),('jmp_estimands','statistical-details-for-causal-estimands-and-estimators'),('jmp_assumptions','statistical-details-for-causal-assumptions'),('jmp_continuous','statistical-details-for-continuous-treatment-methods')]:
        requests[stem]={'id':stem,'vendor':'JMP','url':'https://www.jmp.com/support/help/en/19.2/jmp/'+tail+'.shtml','extension':'html','provenance':'URL recovered from linked primary documentation and saved headers'}
    requests['datarobot_target']={'id':'datarobot_target','vendor':'DataRobot','url':'https://docs.datarobot.com/en/docs/api/dev-learning/accelerators/model-building-tuning/causal-ai.html','extension':'html','provenance':'Saved redirect target'}
    requests['sas_html']={'id':'sas_html','vendor':'SAS','url':None,'extension':'html','provenance':'Legacy SAS CAUSALTRT overview request in saved continuation; exact failed route not retained in this directory'}
    attempts=[]
    for stem,r in requests.items():
        header=BASE/(stem+'.headers')
        if not header.exists():
            assert stem=='stata_teffects'
            continue
        h=header.read_text(errors='replace')
        codes=re.findall(r'HTTP/\S+ (\d+)',h)
        lengths=re.findall(r'(?mi)^content-length:\s*(\d+)',h)
        raw=BASE/(stem+'.'+r['extension'])
        size=raw.stat().st_size if raw.exists() else 0
        status='complete_document'
        reason=''
        if not raw.exists():
            status='unavailable';reason='HTTP '+codes[-1] if codes else 'Saved continuation reports TLS hostname mismatch; headers contain no HTTP response'
        elif lengths and size!=int(lengths[-1]):
            status='partial_excluded';reason='Saved bytes differ from declared Content-Length; continuation reports transfer timeout'
        elif stem=='datarobot_causal':
            status='redirect_document_only';reason='HTML redirect, not methodological text'
        rec=dict(r,status=status,reason=reason,saved_bytes=size,http_status=codes[-1] if codes else None,
                 declared_content_length=int(lengths[-1]) if lengths else None,headers=ref(header,'Saved HTTP metadata, including failures'),
                 request_started_at=None,exit_code=None,
                 reconstruction_limit='Recovered after interruption; request timestamp and process exit code were not preserved here. HTTP server date is not a request start timestamp.')
        rec['server_dates']=re.findall(r'(?mi)^date:\s*(.+)$',h)
        rec['last_modified']=re.findall(r'(?mi)^last-modified:\s*(.+)$',h)
        if raw.exists():rec['raw']=ref(raw,'Authentic acquired bytes; status controls admissibility')
        text=BASE/(stem+'.txt')
        if text.exists():rec['extracted_text']=ref(text,'Saved text extraction; formula images are not transcribed')
        attempts.append(rec)
    assert len(attempts)==16 and sum(r['status']=='complete_document' for r in attempts)==10
    save('acquisition-review.json',{'status':'recovered_with_explicit_metadata_limits','cutoff':'2026-10-07','acquisition_date':'2026-10-13','new_GETs_in_this_continuation':0,'saved_attempts':16,'cap':20,'attempts':attempts,'skipped':[{'id':'stata_teffects','reason':'Already-local predecessor source; no new header/body in this acquisition directory'}],'claim_limit':'Current saved bytes are not authenticated exact-cutoff snapshots. No HTTP failure supports absence of a feature.'})

    # Deterministic population representation, separate from the original grouped expectation implementation.
    accounts=[]
    for i in range(40):
        low=i<30;d=int(i<3 or 30<=i<38);e=F(1,10) if low else F(4,5)
        y0=8 if low else 4;effect=2 if low else 10;cost=1 if low else 12
        accounts.append(dict(low=low,d=d,e=e,y0=y0,effect=effect,cost=cost,y=y0+d*effect))
    ate=F(sum(a['effect'] for a in accounts),40)
    att=F(sum(a['d']*a['effect'] for a in accounts),sum(a['d'] for a in accounts))
    numerator=sum((a['d']-a['e'])*(a['y']-a['y0']-a['e']*a['effect']) for a in accounts)
    denominator=sum((a['d']-a['e'])**2 for a in accounts)
    aipw=sum(a['effect']+a['d']*(a['y']-a['y0']-a['effect'])/a['e']-(1-a['d'])*(a['y']-a['y0'])/(1-a['e']) for a in accounts)/40
    policy={str(bits):str(sum((bits[0] if a['low'] else bits[1])*(a['effect']-a['cost']) for a in accounts)/F(40)) for bits in product([0,1],repeat=2)}
    original=json.loads((BASE/'exact-results.json').read_text())
    assert str(ate)==original['targets']['ATE']=='4'
    assert str(att)==original['targets']['ATET']=='86/11'
    assert str(numerator/denominator)==original['targets']['po_constant_target']=='214/43'
    assert str(aipw)=='4' and policy==original['policy_net_USD_per_eligible_account']
    # A 20-member exact population has one treated member, y1=10, y0=0.
    clipped=sum(F(10,1)/F(1,10) if i==0 else 0 for i in range(20))/20
    assert clipped==5
    independent_eval=[(a,b,c,d) for a,b,c,d in product([-1,1],repeat=4)]
    evaluation=sum(c if a>=b else d for a,b,c,d in independent_eval)/F(16)
    assert evaluation==0 and sum(max(a,b) for a,b in product([-1,1],repeat=2))/F(4)==F(1,2)
    save('exact-review.json',{'status':'pass','reviewer_kind':'author_using_separate_finite_population_representation','accounts':40,'treated_accounts':11,'ATE':str(ate),'ATET':str(att),'residual_slope':str(numerator/denominator),'AIPW_mean':str(aipw),'policies':policy,'clipped_unnormalized_IPW':str(clipped),'fresh_evaluation_selection_error':str(evaluation),'random_draws':0,'vendor_calls':0,'evidence':[ref(BASE/'exact-results.json','Original rational expectations'),ref(ROOT/'tools/commercial_heterogeneity_examples_20261013.py','Original implementation'),ref(Path(__file__),'Separate 40-account and 20-account reviews')],'limits':['Independent calculation, not an independent reviewer.','Generated finite population represents the stipulated law exactly; not observed financial outcomes or a causal-method performance experiment.']})

    # Finite literal alias census: no generated chapters and no claim of market completeness.
    roots=[ROOT/'docs/program/execution/2026-10-13'/s for s in ['commercial','commercial-latent','commercial-temporal','commercial-identification','commercial-heterogeneity']]
    corpus=[p for r in roots for p in r.glob('*.txt') if p.stat().st_size<5_000_000]
    texts={str(p.relative_to(ROOT)):p.read_text(errors='replace').casefold() for p in corpus}
    families=[]
    for family in protocol['candidate_universe']:
        hits={alias:[p for p,t in texts.items() if alias.casefold() in t] for alias in [family['vendor']]+family['aliases']}
        vendor=family['vendor']
        disposition={'StataCorp':'Detailed CATE/postestimation technical comparison; entitlement and runtime unverified.','JMP':'Detailed Uplift and Causal Treatment comparison with separate version scopes; runtime and rights unverified.','DataRobot':'Official propensity/IPTW accelerator overview only; pinned notebook and license not inspected.','SAS':'New partial PDF and failed routes excluded; essential estimator/heterogeneity and entitlement evidence remains missing.','MathWorks':'Requested page denied access; it cannot establish causal heterogeneity support or absence.','causaLens':'TLS request failure retained; no disabled certificate validation or feature-absence conclusion.'}.get(vendor,'Prior-area source/alias leads only; no fresh matched heterogeneity method, edition, API and rights determination.')
        families.append(dict(family,literal_local_hits=hits,disposition=disposition,closed=False))
    save('candidate-register.json',{'cutoff':'2026-10-07','scope':'17 declared families; bounded local literal searches and previously saved public reads','corpus':[ref(p,'Finite local alias search corpus') for p in corpus],'families':families,'limit':'A literal match may be navigation or an unrelated method; zero local matches is not feature absence. Earlier web searches returned no usable results; no global query coverage is claimed.'})
    save('omissions-register.json',{'operation':'SW.CELL.effects_heterogeneity.commercial','essential_coverage_open':True,'items':[{'vendor':f['vendor'],'gap':f['disposition'],'next_action':'Acquire versioned primary method and inferential documentation, exact edition/runtime API and authorized-use terms; compare under the same target and sampling law.','revisit_trigger':'Authentic complete technical/rights bytes become available within a declared successor search scope.'} for f in families if f['vendor'] not in ['StataCorp','JMP']]+[{'vendor':'StataCorp and JMP','gap':'Exact-cutoff bytes, server/automation/redistribution entitlement, matched executable reproduction and dependent-unit inference are not qualified.','next_action':'Pin edition-specific terms and supported API, then design a matched generated comparison if licensed runtime becomes available.','revisit_trigger':'Complete version/rights record; runtime needed only for an empirical implementation claim.'}],'not_claimed':['Complete commercial market coverage','Unavailable feature inferred from failed request','Licensed integration or comparative measured performance'],'sources':[ref(BASE/'acquisition-review.json','Incomplete and failed sources'),ref(BASE/'candidate-register.json','All family dispositions')]})

    sources=[]
    def source(key,title,author,year,version,records,claims,limits,kind='official_technical_documentation'):
        loc=[];anchors=[]
        for stem,anchor in records:
            p=BASE/stem;loc.append(ref(p,anchor));anchors.append(anchor)
        row={'id':key,'integrated_citation_key':key,'kind':kind,'title':title,'author':author,'year':year,'version_date':version,'source_identity':title+'; authenticated local saved bytes and acquisition metadata','local_records':loc,'inspected_anchors':anchors,'supported_claims':claims,'limits':limits}
        row['urls']=[r['url'] for r in attempts if any(Path(stem).stem==r['id'] for stem,_ in records) and r['url']]
        sources.append(row)
    source('exec13_ch_stata','Stata: cate and cate postestimation','StataCorp',2025,'Copyright 1985–2025; r19 context; HTTP modification 2026-07-29; acquired 2026-10-13; exact-cutoff byte identity unverified',[('stata_cate.pdf','PDF pp.1–7 description/options; p.10 conditional effect definitions; pp.46–48 residualization and folds; pp.52–61 AIPW, forest and missingness'),('stata_post.pdf','PDF pp.1–4 prediction and prespecified policy evaluation; methods pp.16–18'),('stata_cate.txt','Saved layout extraction for inspected PDF pages'),('stata_post.txt','Saved postestimation extraction'),('stata_cate.headers','HTTP date, length and modification metadata')],['IATE is a covariate-conditional average; GATE and GATES use prespecified and learned groupings.','PO/AIPW nuisance learning, random-observation cross-fitting, default honest forest and documented option restrictions.','Prediction uncertainty and prespecified policy evaluation are documented.'],['No vendor execution, entitlement, arbitrary sampling-law validity or observed individual causal truth.'])
    source('exec13_ch_jmp_uplift','JMP Uplift platform: overview and Consumer Research guide','JMP',2025,'JMP 19.0 overview dated 2025-07-15; JMP 16 guide separately scoped; acquisition 2026-10-13',[('jmp_uplift.html','Overview: treatment-by-split interaction, predictor multiplicity adjustment'),('jmp_uplift.txt','Full substantive prose'),('jmp_consumer16.pdf','Chapter 6, PDF pp.169–179; pp.174–175 treatment ordering, pooling and validation; pp.176–178 reports'),('jmp_consumer16.txt','Chapter 6 extracted text'),('jmp_uplift.headers','Saved acquisition metadata')],['Partition splits target treatment differences, with linear/logistic interaction and Monte Carlo multiplicity adjustment.','JMP16 guide documents first versus remaining levels and validation-driven split selection.'],['Older-guide details are not automatically verified for JMP19; no postselection validity or vendor performance assertion.'])
    records=[]
    for stem in ['jmp_models','jmp_estimands','jmp_assumptions','jmp_continuous','jmp_causal']:
        records.extend([(stem+'.html','Named page substantive prose, publication 2026-01-13'),(stem+'.txt','Extracted prose; equation images excluded')])
    source('exec13_ch_jmp_causal','JMP Pro Causal Treatment models: targets, assumptions and estimators','JMP',2026,'Help 19.2 pages dated 2026-01-13; acquisition 2026-10-13; exact-cutoff bytes unverified',records,['JMP Pro personality supports binary/continuous treatment and outcome; ATE/ATET and continuous potential-outcome means.','Binary IPWR/REGADJ/AIPW use documented logistic propensity and linear/logistic response models.','Continuous treatment documentation specifies a normal conditional density, stabilized MSM and GPS methods.'],['Only prose is used; image-only equations not visually reviewed. No native CATE forest, cluster-valid inference or license/API entitlement inferred.'])
    source('exec13_ch_datarobot','DataRobot Causal AI for readmission accelerator overview','DataRobot',2026,'Displayed update 2026-09-21; acquired 2026-10-13; exact-cutoff bytes unverified',[('datarobot_target.html','Causal AI for readmission: propensity fitting, inverse propensity weights, weighted comparison; update footer'),('datarobot_target.txt','Substantive prose after navigation'),('datarobot_target.headers','Complete 183158-byte response')],['Official page describes propensity modeling with DataRobot followed by IPTW.'],['Notebook code and license were not inspected; not proof of native CATE engine, calibrated inference or integrated execution.'])
    source('exec13_ch_exact','Servicing: exact estimand and policy contrasts','Causal banking research project',2026,'Project construction and review 2026-10-13',[('exact-results.json','Generated targets, clipping and policy values'),('exact-review.json','Separate finite-population review')],['ATE 4, ATET 86/11 and residualized constant slope 214/43 differ under the generated law.','Treating the lower-risk group alone has net scenario value 3/4 USD per eligible account.','Specified clipping and policy-selection constructions change the stated targets.'],['Generated truth and assumed costs, not bank ROI or vendor performance.'],kind='project_derivation_and_exact_examples')
    source('exec13_ch_scope','Bounded commercial heterogeneous-effects coverage','Causal banking research project',2026,'Recovered acquisition/corpus review 2026-10-13; literature cutoff 2026-10-07',[('search-protocol.json','Declared universe and 20-read maximum'),('acquisition-review.json','Sixteen saved attempts with metadata limitations and exclusions'),('candidate-register.json','All seventeen family and alias dispositions'),('omissions-register.json','Essential remaining source and rights gaps')],['Bounded corpus, failed acquisitions, scope limits and conditional integration recommendations are explicit.'],['No exhaustive market, exact-cutoff or feature-absence conclusion.'],kind='project_evidence')
    temporal=ROOT/'docs/program/execution/2026-10-13/temporal-design'
    sources.append({'id':'exec13_temporal_design','integrated_citation_key':'exec13_temporal_design','kind':'project_derivation_and_review','title':'Temporal graph-to-effect study: feasibility, count interpretation and screen power','author':'Causal banking research project','year':2026,'version_date':'13 October 2026 project review','source_identity':'Preserved temporal-design author review and exact calculations','local_records':[ref(temporal/p,a) for p,a in [('design-review.md','Restricted argument, count clarification and repair routes'),('calculations.json','507/512 raw fraction; variance bound; exact binomial tails; scenario widths'),('operation-receipt.json','Negative final-study design outcome')]]+[ref(ROOT/'tools/review_temporal_design_20261013.py','Preserved independent calculations')],'inspected_anchors':['Persistent raw fraction passes .99; distinct coverage lower-bound screen','14401 transitions under specified Chebyshev bound','500/512 coverage screen and stated per-cell powers'],'supported_claims':['The persistent cell passes its original raw finite-availability rule; weak and broad-latent cells do not.','Sharper certified variance pivots, resource-profiled executable and useful-width/power design remain required before a final study.'],'limits':['No new final random data, certified ordinary quantiles, arbitrary temporal graph confidence or bank trial recommendation.']})
    audit={'cutoff':'2026-10-07','acquisition_date':'2026-10-13','sources':sources,'scholarly_originals_added':0,'visual_acceptance':False}
    shared.verify_refs(audit);save('source-audit.json',audit)
    print(json.dumps({'saved_attempts':16,'complete_documents':10,'families':17,'source_records':len(sources),'exact_review':'pass','coverage':'inconclusive'}))

if __name__=='__main__': main()
