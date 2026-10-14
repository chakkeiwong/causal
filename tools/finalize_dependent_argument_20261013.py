#!/usr/bin/env python3
"""Bind substantive argument review and primary/project claim evidence."""
import json
from pathlib import Path

import run_program as control
from dependent_learner_argument_20261013 import ROOT, BASE, ARGUMENT, ref, write


def main():
    results=json.loads((BASE/'exact-results.json').read_text())
    assert results['status']=='pass' and not results['issues']
    for evidence in results['evidence']:
        control.core.bound(ROOT,evidence)
    prior=ROOT/'docs/program/execution/2026-10-13/cxx-discovery/reader/source-audit.json'
    sources=json.loads(prior.read_text())['sources']
    dml=next(s for s in sources if s['integrated_citation_key']=='dml2018')
    assert ref(ROOT/dml['local_path'],'identity')['sha256']==dml['sha256']
    primary={'source_identity':dml['title'],'version':dml['version_status'],
             'pdf':ref(ROOT/dml['local_path'],'Section 4.2, equations (4.5)-(4.8), Assumption 4.2 and Theorem 4.2'),
             'text':ref(ROOT/dml['text_path'],'Lines 1703-1789: residualized PLIV score and actual rate and slope assumptions'),
             'supported_claim':'The source states the partially linear IV score and nuisance-product/nonzero-slope conditions.',
             'not_supported':'No inheritance of this independent-sample asymptotic theorem for arbitrary dependent rows or the new finite rectangle.'}
    write(BASE/'primary-reading.json',primary)
    checks=[
        ('Historical scope','The first-attempt leakage/scenario defects were already repaired. R05-v2 is the negative baseline and its 99% intervals, failed cells and 0/512 nonlinear result remain unchanged.'),
        ('Identification','The imposed PLIV conditional moment implies M=theta Q; causal exclusion is an unverified premise and Q=0 need not identify theta.'),
        ('Nuisance remainder','Independent-pilot expansion gives the two exact products, with a 16-world rational reference. The correct instrument-error factor remains present.'),
        ('Learner certificate','The basic inequality, cone norm bounds and empirical-to-population Gram transfer yield the stated norm rate, with approximation, numeric and certificate requirements explicit.'),
        ('Alternative information','Independent bounded calibration supplies a feasible risk upper bound; a zero lower noise bound is valid but can leave a nonshrinking floor.'),
        ('Dependence','Known d-dependence of the full vector makes residue classes independent internally. The 2q union bound and weighted class means yield a finite joint moment region; no claim for the old Gaussian AR law.'),
        ('Weak IV and numerics','Projecting the joint rectangle needs no estimated denominator division. Exact topology agrees with 18,685 direct intersection comparisons over 225 rectangles.'),
        ('Misspecification and usefulness','The omitted Gaussian quadratic produces the exact limiting shift 45/86; this is not a fitted bias estimate. Planning bounds can be very wide; width and action thresholds remain separate requirements.'),
        ('Acceptance boundary','This is an argument operation with exact references. No final study, production learner, original-gap qualification or independent acceptance is awarded.')]
    review={'status':'pass','issues':[], 'operation_id':'SCI.ARGUMENT.R05S',
            'reviewer':{'name':'Codex author','kind':'author'},
            'scope':'Reviewed restricted argument plus explicit excluded regimes and information requirements',
            'findings':[{'topic':k,'finding':v,'verdict':'pass'} for k,v in checks],
            'original_gap_qualification':False,'final_study_approved':False,
            'limits':['Unknown/unbounded dependence is outside the finite theorem.',
                      'Sparse cone, approximation and optimizer certificates remain mandatory inputs.',
                      'Finite validity does not establish useful precision; the new method has no repeated-sampling qualification.',
                      'Instrument truth and bank economic usefulness are unverified.'],
            'evidence':[ref(ARGUMENT,'Complete argument, proofs, exact counterexamples and remaining obligations'),
                        ref(BASE/'chapter.tex','Connected banking interpretation and mathematical development'),
                        ref(BASE/'exact-results.json','Exact and independent numerical references'),
                        ref(BASE/'primary-reading.json','Re-inspected primary source and non-inherited claims'),
                        ref(ROOT/'docs/program/master/work/R05-v2/review.md','Relevant preserved predecessor failures')]}
    write(BASE/'argument-review.json',review)
    state=control.core.read(ROOT,control.core.STATE);graph,_,_=control.combined(ROOT,state)
    node=control.ledger.operation(graph,review['operation_id'])
    receipt=control.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope=review['scope'],reviewer=review['reviewer'],
                   limitations=review['limits'],outputs=[ref(ARGUMENT,'Reviewed successor argument and counterexamples')])
    findings=[
        'The exact PLIV target, independent pilot, bounded finite-dependent evaluation law and confidence projection are developed, with a direct comparison to the unchanged R05-v2 failures.',
        'The lasso norm certificate and calibration alternative control the correct nuisance products; the finite dependent region and weak-IV projection are proved. Exact counterexamples and information requirements retain excluded regimes without capability closure.']
    for i,f in enumerate(findings):
        receipt['criteria'][i].update(verdict='pass',finding=f,evidence=[ref(ARGUMENT,'Proofs and scope'),
            ref(BASE/'argument-review.json','Substantive author review'),ref(BASE/'exact-results.json','Independent finite references')])
    write(BASE/'operation-receipt.json',receipt)
    journey=ROOT/'docs/program/execution/2026-10-13/discovery-journey'
    records=[]
    for key,title,files,claims,limits in [
        ('exec13_dependent_argument','Independent pilot PLIV learning with finite dependent evaluation',
         [(ARGUMENT,'Derivation: exact product, sparse certificate, calibration, finite dependence, projection and counterexamples'),
          (BASE/'exact-results.json','Sixteen exact worlds, orthogonal convex reference, 18,685 projection comparisons and planning bounds'),
          (ROOT/'tools/dependent_learner_argument_20261013.py','Reproducible deterministic references with no random qualification draws'),
          (BASE/'argument-review.json','Reviewed premise and claim boundaries'),
          (BASE/'primary-reading.json','Primary-score identity and inspected anchors'),
          (ROOT/'docs/program/master/work/R05-v2/results.json','Actual preserved predecessor outcomes'),
          (ROOT/'tools/master_r05_v2.py','Generator contains the omitted quadratic term')],
         ['The stated restricted model admits the derived finite joint region and projection when its premises and certificates hold.',
          'The exact project references reproduce the score products, selected lasso solution, projection topology and population nonlinear shift.',
          'Earlier calibration failures and useful-width restrictions remain open.'],
         review['limits']),
        ('exec13_discovery_journey','Registered discovery workflow boundary and restart exercise',
         [(journey/'local-review.json','All 98 expectations, scientific dispositions and restarted prefix identities'),
          (journey/'local-journal.json','Every request, response, failure, duration and completed prefix'),
          (ROOT/'docs/program/comprehensive-v14/work/IN.JOURNEY.LOCAL.discovery/local-results.json','All-request results and resource scope'),
          (ROOT/'docs/program/comprehensive-v14/work/IN.JOURNEY.DESIGN.discovery/workflow-protocol.json','Prospectively frozen design'),
          (ROOT/'tools/discovery_journey_20261013.py','Frozen fixture and trial runner'),
          (ROOT/'src/causalbank/operation_service_v12.py','Available method scope and unsupported graph.discover'),
          (journey/'plan-review.md','Independent path, inequality and clock references')],
         ['All 98 fixed invocation slots matched frozen expectations; unsupported and failed requests stayed in the denominator.',
          'Twenty-four semantic parity checks and restarted prefix identities passed.',
          'Elapsed invocation time measures only the declared local exercise.'],
         ['No statistical coverage or discovery-accuracy claim.','No live model, actual sibling, MCP transport or multi-host crash qualification.'])]:
        records.append({'id':key,'integrated_citation_key':key,'kind':'project_derivation_and_executed_examples',
                        'title':title,'author':'Causal banking research project','authors':['Causal banking research project'],
                        'year':2026,'version_date':'13 October 2026; new project evidence, not backdated literature',
                        'source_identity':'Local project derivation and exact registered or deterministic evidence',
                        'local_records':[ref(p,a) for p,a in files],
                        'inspected_anchors':[a for _,a in files], 'supported_claims':claims,'limits':limits})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','project_evidence_date':'2026-10-13',
                                  'sources':records,'inherited_primary_source':primary})
    print(json.dumps({'review':'pass','sources':len(records),'receipt':str((BASE/'operation-receipt.json').relative_to(ROOT))}))


if __name__=='__main__':
    main()
