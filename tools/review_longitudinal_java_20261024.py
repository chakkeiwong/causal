#!/usr/bin/env python3
"""Review pinned primary text; never execute upstream code or its tests."""
import argparse, hashlib, json
from pathlib import Path
import longitudinal_java_reference_20261024 as exact
import run_program_checkpoint_v3 as controller
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings
run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/longitudinal-java-v1'
RAW=ROOT/'docs/literature/raw'; OP='SW.CELL.longitudinal_survival.Java'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static inspected primary source and exact authored laws only; no upstream package, test, backend or secure protocol executed.',
 'Four bounded candidates do not establish exhaustive Java longitudinal/survival coverage.',
 'Start-stop prediction, weighted fitting, cluster covariance, confidential execution and causal identification are distinct.',
 'Native conformance, full helper/environment/rights review, numerical calibration and costs remain open.',
 'No visual, independent, bank or final acceptance; integration_allowed remains false.']

# Every span was inspected in bounded text reads. Unlisted acquired blobs are not technical evidence.
CLAIMS={
 'exec24_longjava_h2o_00':([(1,23),(32,83),(145,221)],'Documented hazard/timing/tie/weight contracts, weighted no-tie versus Breslow formula discrepancy, and convergence prose.'),
 'exec24_longjava_h2o_01':([(54,92),(168,200),(424,480),(505,600),(664,727),(835,890)],'Numeric time and per-row interval validation; inverse-Hessian covariance; separate baseline paths; weighted likelihood, event recoding and convergence iteration.'),
 'exec24_longjava_h2o_02':([(320,415)],'Ordinary scoring output is centered lp; exclusions, zero weights and unknown strata have explicit branches.'),
 'exec24_longjava_h2o_03':([(1,40)],'Common task skips bad and zero-weight rows before processRow.'),
 'exec24_longjava_h2o_04':([(10,34),(50,69)],'Efron update and tie denominator; local reduction-order comment is not full distributed reproducibility proof.'),
 'exec24_longjava_h2o_05':([(1,74)],'Public Cox schema exposes timing, strata, weights, offsets, ties and iteration controls.'),
 'exec24_longjava_h2o_06':([(52,92)],'MOJO returns centered linear predictor plus offset, not an absolute survival probability.'),
 'exec24_longjava_h2o_07':([(1,94)],'MOJO reader loads coefficient/mean/strata/interaction data; selected reader has no horizon baseline payload.'),
 'exec24_longjava_h2o_08':([(30,78),(498,550),(606,642)],'Tests specify optional-column parity and a scoped Efron Java11-plus concern; source tests not run.'),
 'exec24_longjava_h2o_09':([(1,51)],'R bridge returns ordinary covariance and used.robust=FALSE.'),
 'exec20_javaeffects_h2o_source_00':([(1,9)],'Root direct license identifies Apache2.0; full distribution/transitive clearance not inferred.'),
 'exec20_javaeffects_h2o_source_01':([(1,28)],'Build declares3.47.0 and bleeding_edge; not a supported-release assertion.'),
 'exec24_longjava_biojava_00':([(1,11)],'Root direct license is LGPL2.1; applicable notices and distribution remain review obligations.'),
 'exec24_longjava_biojava_01':([(1,38)],'Parent7.3.1-SNAPSHOT, Java11 property, LGPLv2 label and2.1 link.'),
 'exec24_longjava_biojava_02':([(1,50)],'Survival module version/license and direct dependencies; no solved environment.'),
 'exec24_longjava_biojava_03':([(27,146)],'Single-time helper, weight filtering, cluster dispatch, exception-to-null boundary.'),
 'exec24_longjava_biojava_05':([(30,165),(267,305),(770,930)],'Partial R port, controls, terminal-row strata, conjunction guard and robust cleanup state-restoration branches.'),
 'exec24_longjava_biojava_07':([(55,163)],'Score/dfbeta weighting, cluster rowsums and column-map reset precede covariance cross-product.'),
 'exec24_longjava_biojava_08':([(34,82),(237,253)],'Single time/status object and time/status comparator; ordinary strata labels are not automatically converted.'),
 'exec24_longjava_fresco_00':([(1,21)],'MIT notice, retention condition and no warranty; no transitive clearance.'),
 'exec24_longjava_fresco_01':([(20,34),(92,105)],'Secure-statistics purpose and explicit overflow warning; security theorem not independently verified.'),
 'exec24_longjava_fresco_02':([(1,30),(51,105)],'0.6-SNAPSHOT, FRESCO1.3.3, Java9 and direct dependency declarations.'),
 'exec24_longjava_fresco_03':([(1,75)],'Secret covariates, one time and field named censored.'),
 'exec24_longjava_fresco_04':([(35,60)],'Sorter returns tied groups as public BigInteger values.'),
 'exec24_longjava_fresco_05':([(64,155)],'Risk accumulations adjust tied groups and multiply final contributions by event-status bit.'),
 'exec24_longjava_fresco_07':([(18,90)],'Fixed-iteration scaled Hessian-pseudoinverse update; no further convergence check in this loop.'),
 'exec24_longjava_fresco_08':([(23,130)],'Comment says gradient descent while delegate uses Hessian; result exposes coefficients/errors/test but no convergence flag.'),
 'exec24_longjava_fresco_09':([(30,82)],'Source example uses observed-event status1 and distinguishes simulated tie identity from MiMC mechanism; not executed.'),
 'exec24_longjava_fresco_extra_00':([(1,44)],'Fresh shared MiMC key; ciphertexts opened, making equality classes public, not proving raw-time recovery.'),
 'exec24_longjava_jlinalg_00':([(1,8)],'Root text identifies GPL2; selected source headers specify GPL2-or-later.'),
 'exec24_longjava_jlinalg_02':([(1,95),(150,257)],'Documented CLI/API distinction, model boundaries and reported timings/tests; those reports are not reproduced or independently accepted.'),
 'exec24_longjava_jlinalg_extra_00':([(1,22),(119,174)],'0.3.6 build, declared dependencies and checksum-pinned JDistlib0.10.2 download logic; not a solved transitive environment.'),
 'exec24_longjava_jlinalg_extra_01':([(1,208)],'Prepared backend lifecycle, predictor scaling, step halving, convergence/status output, model covariance and absence of case-weight input in this signature.'),
 'exec24_longjava_jlinalg_extra_02':([(1,35)],'Explicit iteration, tolerance, ridge and confidence-level controls.'),
 'exec24_longjava_jlinalg_extra_03':([(1,61)],'Finite nonempty interval validation with0<=start<stop, strata and at least one event.'),
 'exec24_longjava_jlinalg_extra_04':([(1,69)],'Prepared per-stratum entry/exit ordering for counting-process risk sets.'),
 'exec24_longjava_jlinalg_extra_05':([(1,83)],'Ordinary standard errors, covariance, baseline, convergence message and backend provenance remain separate result fields.'),
 'exec24_longjava_jlinalg_extra_06':([(18,75),(88,165),(233,249)],'Separate diagnostics computes cluster-summed score sandwich, not automatic replacement of fit standard errors.'),
 'exec24_longjava_jlinalg_extra_07':([(419,462)],'Counting-process baseline updates entrants/exits and tie-specific increments.'),
}

def audit():
    assert not (BASE/'review.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    selections={x['id']:x for f in ['source-selection-h2o.json','source-selection-expanded.json','source-selection-delegates.json'] for x in read(BASE/f)}
    hcommit=read(RAW/'exec20_javaeffects_h2o_cutoff.json')[0]
    htree={x['path']:x for x in read(RAW/'exec20_javaeffects_h2o_tree.json')['tree']}
    for key,path in [('exec20_javaeffects_h2o_source_00','LICENSE'),('exec20_javaeffects_h2o_source_01','gradle.properties')]:
        selections[key]=dict(id=key,repository='h2oai/h2o-3',commit=hcommit['sha'],date=hcommit['commit']['committer']['date'],path=path,blob=htree[path]['sha'])
    profiles={x['slug']:x for x in read(BASE/'selected-repository-identities.json')}
    profiles['h2o']=dict(repo='h2oai/h2o-3',commit=hcommit['sha'],date=hcommit['commit']['committer']['date'])
    names=dict(h2o='H2O-3',biojava='BioJava survival',fresco='FRESCO-stat',jlinalg='robbyjo/JLinAlg')
    versions=dict(h2o='3.47.0 bleeding_edge',biojava='7.3.1-SNAPSHOT',fresco='0.6-SNAPSHOT',jlinalg='0.3.6')
    sources=[]
    for slug,p in profiles.items():
        records=[]
        for key,(spans,finding) in CLAIMS.items():
            x=selections[key]
            if x['repository']!=p['repo']:continue
            f=RAW/(key+'.txt');data=f.read_bytes();receipt=read(f.with_suffix('.receipt.json'))
            assert receipt['status']=='saved' and receipt['sha256']==core.sha(f)
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==x['blob']
            assert '/'+x['commit']+'/' in receipt['url']; lines=f.read_text().splitlines();anchors=[]
            for a,b in spans:
                assert 1<=a<=b<=len(lines),(key,a,b,len(lines))
                anchors.append(dict(lines=[a,b],text=chr(10).join(lines[a-1:b]),finding=finding))
            records.append(dict(source_identity=receipt['url'],version_date=f"{versions[slug]};{p['commit']};{p['date']}",upstream_path=x['path'],local_copy=ref(f,finding),receipt=ref(f.with_suffix('.receipt.json'),'Bounded public acquisition'),git_blob_sha1=x['blob'],inspected_anchors=anchors,supported_claims=[finding],executed=False))
        cutoff=RAW/('exec20_javaeffects_h2o_cutoff.json' if slug=='h2o' else f'exec24_longjava_{slug}_cutoff.json')
        tree=RAW/('exec20_javaeffects_h2o_tree.json' if slug=='h2o' else f'exec24_longjava_{slug}_tree.json')
        assert not read(tree)['truncated'] and p['date']<'2026-10-08'
        sources.append(dict(integrated_citation_key='exec24_longjava_'+slug,kind='software_primary_sources',title=names[slug]+' pinned survival contracts and integration limits',author=names[slug]+' contributors',year=2026,source_identity=f"https://github.com/{p['repo']}/tree/{p['commit']}",version_date=f"{versions[slug]};{p['commit']};{p['date']}",local_copy=records[-1]['local_copy'],records=records,identity_evidence=[ref(cutoff,'Selected default-branch cutoff commit; not all releases'),ref(tree,'Complete immutable tree')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[r['supported_claims'][0] for r in records],limitations=LIMITS))
    sources.append(dict(integrated_citation_key='exec24_longjava_reference',kind='project_evidence_not_scholarly_paper',title='Exact authored Java survival clock, score, weight, coding and covariance witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/longitudinal_java_reference_20261024.py',version_date='24 October 2026; exact finite laws and abstract traces',local_copy=ref(Path(exact.__file__),'Independent Fraction reference'),inspected_anchors=[ref(BASE/'exact-results.json','Exact outcomes and explicit scope')],supported_claims=['Delayed entry increments1/2 versus1/3; Efron5/6 versus Breslow2/3 under unit risk.','Weighted displayed no-tie1/4 versus Breslow1/16; score derivatives-1/2 and-1.','Same relative score permits risks3/4 and7/16, stipulated margins-150 and162.5USD.','Event collapse changes designed default fraction1/10 to1/2.','Specified score sandwich yields row1/4 versus cluster1/2.','Abstract BioJava index/guard traces and public tie-partition distinction are not native package runs.'],limitations=LIMITS))
    write(BASE/'source-audit.json',dict(sources=sources,cutoff='2026-10-07',authenticated_new_blobs=42,inspected_cited_blobs=len(CLAIMS),native_execution=False))
    queries=[];observed={}
    for name in ['survival','cox','causal']:
        f=RAW/f'exec24_longjava_search_{name}.json';d=read(f);queries.append(dict(source=ref(f,'Creation-date-filtered repository discovery only'),total=d['total_count'],returned=len(d['items']),incomplete=d['incomplete_results']))
        for x in d['items']:observed[x['full_name']]=dict(repository=x['full_name'],description=x.get('description'),disposition='metadata_lead_only_not_technical_evidence')
    for name in ['fresco','javastat','biojava']:
        f=RAW/f'exec24_longjava_discovery_{name}.json';d=read(f);queries.append(dict(source=ref(f,'Alias discovery only; unrelated hits and unreturned tail retained'),total=d['total_count'],returned=len(d['items']),incomplete=d['incomplete_results']))
        for x in d['items']:observed[x['full_name']]=dict(repository=x['full_name'],description=x.get('description'),disposition='metadata_lead_only_not_technical_evidence')
    for p in profiles.values():observed[p['repo']]=dict(repository=p['repo'],disposition='selected_bounded_primary_source_review',commit=p['commit'])
    write(BASE/'search-screening.json',dict(status='partial_not_exhaustive',cutoff='2026-10-07',inherited_zero_query=ref(RAW/'v12_sw_cell_longitudinal_survival_java.json','Zero compound OpenAlex matches prove no software absence'),queries=queries,items=list(observed.values()),aliases={'H2O':['h2oai/h2o-3','CoxPH','MOJO'],'BioJava':['biojava/biojava','biojava-survival','CoxR'],'FRESCO':['alexandrainst/fresco-stat','secure Cox'],'JLinAlg':['robbyjo/JLinAlg','0.3.6 distinct repository']},stopping_rule='Four contrastive primary profiles sufficient for bounded proposal comparison; no exhaustive status until targeted leads and search tails are resolved.',metadata_is_technical_evidence=False))
    omissions=[('coverage','Resolve relevant retained discovery leads, distinguish similarly named JavaStat/JLinAlg projects and expand targeted Java longitudinal/causal inventory; search tails do not prove absence.'),('h2o','Register weighted no-tie, named baseline/delayed-entry/tie and centered-score fixtures; inspect remaining runtime delegates and scoped Java11 Efron issue.'),('biojava','Resolve strata conversion, null/empty guard and robust unclustered state restoration with a reviewed successor and independent native fixture; inspect remaining score/martingale/numeric delegates.'),('fresco','Bind threat model, protocol suite, public tie partition, status coding, precision/modulus, pseudoinverse delegates and convergence criteria; independent security/numeric review.'),('jlinalg','Inspect backend and CoxMath/CoxRiskMoments delegates, CLI conversion and broader APIs; freeze distribution; no throughput or frailty acceptance from vignette.'),('qualification','Register generated/public-data environments and failure-complete trials after prototype justification; preserve target and sampling-unit distinctions.'),('rights_cost','Resolve direct declaration discrepancies and transitive rights; full costs and matched request denominators.'),('visual','Fresh permitted visual review, Q1/Q5 and mandatory coverage/depth remain open.')]
    write(BASE/'omissions-register.json',dict(status='open',items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in omissions],limitations=LIMITS))
    write(BASE/'conversion-contract.json',dict(status='proposal_only',integration_allowed=False,preferred_route='Conditional original Java workers with separate targets; reference use now',alternatives=['H2O service plus distinct MOJO scorer','BioJava worker after branch and strata qualification','FRESCO worker for an explicit custodian/security need','JLinAlg fixed-effect worker with separate diagnostics','R/Python longitudinal worker for sequential policies','Independent finite-law oracle'],rejected=['Whole-library port without demonstrated need and parity','Causal meaning inferred from survival label','Null/failed result converted to successful zero','Relative score silently converted to absolute risk'],inputs=['population/time-zero/availability','event dictionary and clock','treatment/observation/competing-event target','IDs/exclusions/weights/clusters','locked environment/RNG/backend/security contract'],outputs=['request/artifact identity','retained/rejected row IDs','resolved options/convergence/failure','selected covariance/cluster count','log score/baseline/horizon/centering','warnings and full costs'],owners=['Method owner: target/identification/sampling','Adapter owner: typed conversion and failures','Rights owner: distribution and artifacts','Evaluation owner: generated/public trials and full costs'],native_execution=False))
    write(BASE/'plan-review-v2.json',dict(status='pass_for_bounded_comparison_and_integration',evidence=[ref(BASE/'plan-review.json','Preserved acquisition plan'),ref(BASE/'development.tex','Connected scoped manuscript'),ref(BASE/'source-audit.json','Every technical citation bound'),ref(BASE/'omissions-register.json','Independent follow-ups')],checks=['Four contrastive source profiles, not exhaustive closure.','Check delegates before judging preliminary validation or covariance loops.','Source branches, exact authored traces, public reports and native execution clearly separated.','Preserve1034 prior citation records and236 genuine scholarly PDFs; add five records.','Publish only after exact source/context/arithmetic/all-page text checks, then pair sponsor and reconcile.'],preserved_prewrite_failure='Initial large manuscript tool submission failed on JavaScript backtick parsing before apply_patch; corrected submission succeeded.',visual_acceptance=False))
    write(BASE/'mathematical-review.json',dict(status='pass_for_exact_authored_laws',evidence=[ref(Path(exact.__file__),'Fraction laws and scoped branch traces'),ref(BASE/'exact-results.json','Recomputed outputs'),ref(BASE/'development.tex','Notation, assumptions and consequences')],findings=['Direct rational calculation confirms all risk, margin, weighted likelihood, entry/tie and covariance examples.','Native reachability and empirical calibration remain explicitly untested.','BioJava cluster rowsum clears its map per column; no false accumulation bug claimed.']))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected manuscript'),ref(BASE/'sponsor-addition.md','Sponsor consequences')],findings=['Proposal and later prototype evidence distinguished.','No scholarly original cited from vendor bibliographies; software claims use primary local bytes.','Source finding is not reported as a deployment observation.','No blanket Java absence or universal causal capability claim.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed bounded Java comparison') for n in ['plan-review-v2.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','development.tex','sponsor-addition.md','mathematical-review.json','copyedit-review.json','exact-results.json']]+[ref(Path(__file__),'Audit logic')]
    review=dict(status='pass_for_bounded_comparison',evidence=evidence,findings=['Four cutoff primary profiles with contrasting event, covariance, output and security contracts.','Broad coverage remains inconclusive; no implementation or native performance admitted.'],limitations=LIMITS)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(audited_sources=5,cited_inspected_blobs=len(CLAIMS),new_authenticated_blobs=42,coverage='inconclusive')))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));g,merged,_=run.combined(ROOT,state);node=run.ledger.operation(g,OP)
    evidence=[ref(BASE/n,'Scoped Java evidence') for n in ['review.json','source-audit.json','search-screening.json','omissions-register.json','conversion-contract.json','mathematical-review.json','development.tex']]
    scope='Four pinned Java survival lineages; bounded source comparison, not exhaustive longitudinal coverage'
    nxt='Resolve Java discovery aliases/tails and inspect named runtime delegates; preregister candidate-specific clock, weight, baseline, cluster, failure and secure-disclosure fixtures after prototype justification. Preserve original worker options and R/Python sequential-policy alternatives.'
    out=ROOT/node['outputs'][0];write(out,dict(operation=OP,status='inconclusive',scope=scope,candidates=['h2oai/h2o-3','biojava/biojava','alexandrainst/fresco-stat','robbyjo/JLinAlg'],evidence=evidence,limitations=LIMITS,next_action=nxt,integration_allowed=False))
    findings=[('inconclusive','Four cutoff candidates and observed discovery leads identified; alias resolution, targeted longitudinal inventory and query tails remain.'),('pass','Technical claims bind authentic local bytes, cutoff commit, version, hash and inspected spans; five audited records and no new metadata-only scholarly citation.'),('pass','Candidate-specific alternatives, rejections, omissions, owners and continuation routes explicit; no absence inference or unavailable-source waiver.')]
    r=run.ledger.receipt_template(node);r.update(outcome='inconclusive',execution='performed',scope=scope,reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(out,'Bounded Java coverage disposition')],criteria=[dict(index=i,verdict=v,finding=f,evidence=evidence) for i,(v,f) in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=nxt)
    run.validate_receipt(ROOT,merged,node,r,len(state['execution_program']['turns']));verify_bindings(r);write(BASE/'operation-receipt.json',r);print('Java coverage receipt prepared: inconclusive.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['audit','receipt']);globals()[p.parse_args().command]()
