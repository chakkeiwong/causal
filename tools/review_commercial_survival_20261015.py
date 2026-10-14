#!/usr/bin/env python3
"""Record bounded commercial-survival claims without granting census closure."""
import json
from pathlib import Path
import sys
import build_commercial_survival_v3_20261015 as build
import commercial_survival_examples_20261014 as exact
import prepare_commercial_survival_20261014 as work
import master_control as core
import run_program as run
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write

ROOT,BASE,OUT=build.ROOT,build.BASE,build.OUT
WORK=work.BASE
OP='SW.CELL.longitudinal_survival.commercial'
OUTPUT=ROOT/('docs/program/comprehensive-v14/work/'+OP+'/coverage-review.json')
REVIEWER=work.REVIEWER
LIMITS=work.LIMITS


def main():
    report=json.loads((OUT/'build-report.json').read_text())
    audit=json.loads((OUT/'source-audit.json').read_text())
    prior=json.loads(build.PRIOR.read_text())
    trace=json.loads((BASE/'traceability-review.json').read_text())
    for obj in [report,audit,prior,trace,json.loads((BASE/'prepared-inputs.json').read_text()),
                json.loads((WORK/'primary-review.json').read_text()),json.loads((WORK/'derivation-review.json').read_text())]:
        verify_bindings(obj)
    assert trace['status']=='pass' and not trace['issues'] and trace['scholarly_pdfs']==172
    assert json.loads((OUT/'text-layout-review.json').read_text())['status']=='pass'
    assert not [w for w in report['warnings'] if 'Underfull' not in w]
    old={s['integrated_citation_key']:s for s in prior['sources']}
    new={s['integrated_citation_key']:s for s in audit['sources']}
    assert len(old)==603 and len(new)==614 and all(new[k]==v for k,v in old.items())
    files={r['path']:r for r in audit['tex_files']}
    kept=[r for r in prior['tex_files'] if r['path']!=str(build.OLD.relative_to(ROOT))]
    assert all(files[r['path']]['sha256']==r['sha256'] for r in kept)
    prior_trace=json.loads((build.PRIOR.parent.parent/'traceability-review.json').read_text())
    contexts={r['citation_key']:r['citation_contexts'] for r in trace['records']}
    count=0
    for row in prior_trace['records']:
        for c in row['citation_contexts']:
            assert c in contexts[row['citation_key']],row['citation_key']
            count+=1
    assert exact.calculate()==json.loads((WORK/'exact-results.json').read_text())
    assert (BASE/'comparison.tex').read_text()==build.corrected((WORK/'comparison.tex').read_text())
    sys.path.insert(0,str(ROOT/'src'))
    from causalbank.operation_service_v12 import SUPPORTED
    assert SUPPORTED=={'capabilities.describe':'exact_runtime_manifest','graph.review':'declared_graph_syntax_only',
        'identify.effect':'supplied_DAG_backdoor_independent_units','estimate.effect':'supplied_moment_Gaussian_residual_inversion',
        'sensitivity.evaluate':'deterministic_quadratic_sublevel','audit.observation':'declared_strict_before_decision_clock'}
    text=' '.join((OUT/'reader.txt').read_text().split())
    for phrase in ['Commercial survival software and repeated banking interventions',
                   'eight families','minus 25 percentage points','sixteen-state law',
                   '34.36%','LAC-IPWRA','WAC-IPWRA','Omit Causes','EVENTCODE',
                   'unrestricted mean default time','proprietary']:
        assert phrase.lower() in text.lower(),phrase
    evidence=[ref(p,a) for p,a in [
        (OUT/'build-report.json','Exact integrated survival reader'),
        (OUT/'source-audit.json','614 records preserving all603 earlier identities'),
        (BASE/'traceability-review.json','Complete claim/source index and172 genuine scholarly PDFs'),
        (OUT/'text-layout-review.json','Every-page text bounds'),
        (OUT/'reader.txt','Author inspected added pages and equations'),
        (WORK/'primary-review.json','Fourteen original documents and specific supported claims'),
        (WORK/'acquisition-review.json','Every successful, denied, oversized and timed-out transfer'),
        (WORK/'candidate-register.json','Nine vendor families with explicit dispositions'),
        (WORK/'omissions-register.json','Unresolved originals, dates, rights and broader families'),
        (WORK/'exact-results.json','Five exact banking constructions'),
        (WORK/'derivation-review.json','Independent path and joint-law checks'),
        (BASE/'repair-review.json','Preserved candidate and two wording corrections'),
        (BASE/'comparison.tex','Connected source-grounded banking comparison'),
        (BASE/'prepared-inputs.json','Frozen preserving input identities'),
        (ROOT/'tools/commercial_survival_examples_20261014.py','Rational reproduction'),
        (ROOT/'src/causalbank/operation_service_v12.py','Observed six-operation local reference'),
        (Path(__file__).resolve(),'Exact author review and scope limits'),
    ]]
    findings=[
        'Fourteen successful official originals support eight commercial families; MATLAB remains unresolved after two403 responses.',
        'Stata survival treatment-effect targets are separated from its explicit multiple-record/time-varying/delayed-entry exclusions and censoring-adjustment limits.',
        'SAS subdistribution risk sets and effective options, JMP independent-cause removal displays, and IBM/Statistica/Minitab record clocks are distinguished.',
        'NCSS convergence/row accounting and Mplus censoring/latent-model examples support specific proposed conversion checks, not qualified runtime.',
        'Five exact constructions reproduce: competing-event risk/value, future exposure, sequential confounding, informative observation and rare-path bootstrap.',
        'All603 earlier citation records and uses remain;11 additions bind official text and project examples without adding scholarly original claims.',
        'Coverage is inconclusive: exact editions/cutoff bytes, one essential vendor source, wider families and licensing/runtime comparisons remain unqualified.',
    ]
    write(BASE/'release-source-review.json',{'status':'pass','issues':[],'reviewer':REVIEWER,
        'scope':'Author source/claim/mathematics delta, not census completeness or visual acceptance',
        'reviewed_reader':report['pdf'],'evidence':evidence,'findings':findings,
        'preserved_source_records':603,'new_source_records':11,'preserved_citation_uses':count,
        'unchanged_compiled_sources':len(kept),'limitations':LIMITS,'visual_acceptance':False})
    routes=[
        {'vendor':'Stata','proposal':'Licensed fixed-treatment survival comparator and separate subdistribution case; preserve estimand, labels, sample, overlap refusal and uncertainty.','not_awarded':'Repeated-regime estimator or installed adapter.'},
        {'vendor':'SAS/STAT','proposal':'Version14.1 interval and EVENTCODE comparator with cluster ID, effective options, CIF and pointwise uncertainty.','not_awarded':'Arbitrary sequential causal identification or later-edition equivalence.'},
        {'vendor':'IBM SPSS','proposal':'Time-expression and measured-covariate conversion reference; freeze availability/interval conventions.','not_awarded':'Causal policy effect from a time-dependent coefficient.'},
        {'vendor':'JMP','proposal':'Cause-specific/cause-removal display comparator with explicit independence and event-removal premises.','not_awarded':'Observed cumulative incidence or causal removal from an Omit Causes control.'},
        {'vendor':'Minitab','proposal':'Counting-process, excluded-row, tie/covariance and diagnostic export comparison.','not_awarded':'Exact edition, runtime or identification acceptance.'},
        {'vendor':'NCSS','proposal':'Convergence and processed/used-row reporting comparator.','not_awarded':'Undated release identity, calibrated inference or causal target.'},
        {'vendor':'Statistica','proposal':'Separate fixed, time-function and start/stop input conversions.','not_awarded':'Sequential regime semantics from risk-set representation alone.'},
        {'vendor':'Mplus','proposal':'Separate discrete-time, Cox, parametric and latent-measurement survival reference paths.','not_awarded':'Authenticated hidden-confounding control, exact edition or numerical runtime.'},
        {'vendor':'MATLAB','proposal':'Obtain accessible essential original, then review fitted operation and intended license.','not_awarded':'Any absence or performance finding.'},
    ]
    revisit='Acquire MATLAB originals and dated edition snapshots; inspect remaining candidate families and any relevant dynamic-regime extensions. Following prototype merit, settle deployment rights and run a frozen licensed target/conversion comparison.'
    write(OUTPUT,{'operation_id':OP,'status':'inconclusive','scope':'Bounded nine-family primary comparison; eight have inspected originals',
        'cutoff':'2026-10-07 Asia/Shanghai','reviewed_on':'2026-10-15 Asia/Shanghai','reviewer':REVIEWER,
        'reviewed_reader':report['pdf'],'source_audit':ref(BASE/'source-audit.json','All original identities, hashes, dates and claims'),
        'findings':findings,'routes':routes,'evidence':evidence,'limitations':LIMITS,
        'exhaustive_census':False,'vendor_runtime_executed':False,'paid_trial':False,
        'prices':'Unknown, not zero','original_gap_qualification':False,'revisit_trigger':revisit,
        'prototype_acceptance':[
            'Target, horizon, event/censor codes, risk-set intervals and subject IDs survive serialization.',
            'Fixed-treatment target never receives an implicit repeated-policy interpretation.',
            'Cumulative incidence and cause-removal outputs remain distinct on the .15/.18/.19 example.',
            'Future-defined exposure is refused; landmark target change is explicit.',
            'Full-law sequential reference reproduces .42/.13 and observed .18/.37 under declared assumptions.',
            'Excluded rows, nonconvergence and undefined bootstrap replicates remain in original denominators.',
            'Matched runtime comparison waits for actual version, intended rights and useful prototype evidence.']})
    graph,_,_=run.combined(ROOT,core.read(ROOT,core.STATE));node=run.ledger.operation(graph,OP)
    receipt=run.ledger.receipt_template(node)
    criteria=[('inconclusive','All nine bounded family dispositions are explicit, but global aliases, exact historical editions and wider coverage remain incomplete.'),
              ('pass','Every added technical claim binds authentic original bytes, identity/date limits and inspected anchors; project constructions reproduce. No new scholarly work is cited without an original.'),
              ('pass','Alternatives and omissions remain explicit; unavailable MATLAB and unresolved rights receive no absence, zero-price or essential-source waiver.')]
    receipt.update(outcome='inconclusive',execution='performed',scope='Bounded commercial survival proposal comparison',
        reviewer=REVIEWER,limitations=LIMITS,outputs=[ref(OUTPUT,'Scoped coverage review and concrete qualification routes')],
        nonexecution_reason='',revisit_trigger=revisit,
        criteria=[{'index':i,'verdict':v,'finding':f,'evidence':evidence+[ref(OUTPUT,'Reviewed outcomes')]} for i,(v,f) in enumerate(criteria)])
    write(BASE/'operation-receipt.json',receipt)
    print(json.dumps({'coverage':'inconclusive','source_math_review':'pass','families_with_primary':8,
                      'new_records':11,'preserved_contexts':count,'reader_pages':report['pages']}))


if __name__=='__main__':main()
