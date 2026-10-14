#!/usr/bin/env python3
"""Bind inspected grf originals and the scoped proposal contract; no engine execution."""
import copy
import hashlib
import json
from pathlib import Path
import sys

import jsonschema
import build_integrated_monograph_v12 as shared
import master_control as core

ROOT = core.ROOT
BASE = ROOT / 'docs/program/execution/2026-10-13/grf-cxx'
DEST = ROOT / 'docs/program/comprehensive-v14/work/IN.DESIGN.Cxx/adapter-contract.json'
RAW = ROOT / 'docs/literature/raw'
COMMIT = '5bee99b51471f76cb2d63acbc8a9b0ffec408ba0'
ref = shared.ref
sys.path.insert(0, str(ROOT / 'src'))
from causalbank.operation_contract_v12 import context_digest, validate_response


def artifact(path, identifier, role, schema):
    raw = path.read_bytes()
    return dict(artifact_id=identifier, sha256=hashlib.sha256(raw).hexdigest(),
                media_type='application/json', schema_version=schema, role=role,
                bytes=len(raw), custody='local_project_reference')


def original(identifier, anchor):
    p = RAW / (identifier + '.receipt.json')
    r = json.loads(p.read_text())
    local = ROOT / r['path']
    assert r['status'] == 'saved' and core.sha(local) == r['sha256']
    assert COMMIT in r['url']
    return dict(source_identity=r['url'], local_copy=ref(local, anchor),
                acquisition=ref(p, 'Original collector receipt'), accessed_utc=r['accessed_utc'])


def main():
    contract = {
        'schema_version': 'causalbank.grf-adapter-design/1.0.0',
        'operation_id': 'IN.DESIGN.Cxx', 'date': '2026-10-13',
        'status': 'reviewed_proposal_design_not_runtime_admission',
        'engine': {'name': 'grf', 'commit': COMMIT, 'commit_date': '2026-04-30',
                   'package_version': '2.6.1', 'cutoff': '2026-10-07', 'runtime_admitted': False},
        'choice': {'initial': 'Pinned isolated R process invoking the maintained native C++ core.',
                   'direct_native': 'Deferred until ownership, preprocessing, aggregation, serialization and environment parity are qualified.',
                   'port': 'Reject for the initial scope: transfers forest and statistical maintenance without a measured workload benefit.'},
        'scope': {
            'operation': 'estimate.effect', 'engine_id': 'grf-r-native-2.6.1',
            'estimator_id': 'binary-iid-aipw-all-v1',
            'target': 'E[Y(1)-Y(0)] in the declared customer population, estimated by all-sample AIPW scores; not mean fitted CATE.',
            'law': 'Complete independent customer rows; one binary action, one fixed scalar outcome and horizon.',
            'identification': ['Consistency', 'No interference', 'Conditional exchangeability or declared randomization', 'Positivity'],
            'assumption_status': 'Declared premises; neither syntax nor fitting verifies them.',
            'initial_options': {'honesty': True, 'tune.parameters': 'none', 'num.trees': 2000,
                                'ci.group.size': 2, 'sample.fraction': 0.5, 'min.node.size': 5,
                                'honesty.fraction': 0.5, 'honesty.prune.leaves': True,
                                'alpha': 0.05, 'imbalance.penalty': 0, 'stabilize.splits': True,
                                'compute.oob.predictions': True, 'num.threads': 1,
                                'sample.weights': None, 'clusters': None, 'equalize.cluster.weights': False,
                                'mtry': 'min(ceil(sqrt(p)+20),p), realized value recorded',
                                'seed': 'Required integer, recorded; no default random draw'},
            'nuisance': 'Retain R OOB nuisance path; optional declared known randomized propensity only. Supplied fitted nuisances need a separately qualified provenance/split profile.',
            'excluded': ['Continuous treatment/dose derivative', 'IV/LATE', 'Repeated actions and policy value',
                         'Panel/calendar dependence', 'Weights or clusters in initial profile', 'Post-treatment features',
                         'Missing or nonfinite data', 'Unresolved graph-class identification',
                         'External fitted nuisance vectors in initial profile', 'Automatic overlap-target substitution'],
            'extension': 'Independent-cluster all-sample AIPW design retains cluster units and target weights; no current admission or few-cluster coverage.'},
        'request': {
            'shared_contract': ref(ROOT/'docs/program/repair-v12/work/IN02/operation-contract.json', 'Preserved request/result/uncertainty contract'),
            'parameters': {'engine_id': 'grf-r-native-2.6.1', 'estimator_id': 'binary-iid-aipw-all-v1'},
            'configuration': 'Versioned immutable engine_configuration ArtifactRef: source, options, roles, units, target, seed and numerical policy. Detailed options are not added to generic parameters.',
            'data': 'Authorized local immutable handles only; verify bytes, schema and hash. Preserve row IDs and ordered feature names; no caller executable or network locator.',
            'identity': 'Context digest plus full request digest including all data/configuration/environment identities; never cache by scientific context alone.',
            'graph': 'Preserve graph and set topology and all endpoint marks; no arbitrary representative DAG. Require an applicable target-identification argument before estimation.'},
        'conversion': {
            'R_boundary': 'Original X,Y,W sent to R; R residualizes Y and W before native call. Record nuisance vectors and provenance.',
            'native_boundary': 'Borrowed column-major double buffer [X,Y_residual,W_residual,...]; own memory for full call/thread lifetime; checked size multiplication and role indices.',
            'roles': 'Outcome/treatment/instrument/weight setters exclude role columns from splitting; causal binding sets instrument index to treatment index.',
            'units': 'No silent scaling. Output unit equals Y unit for binary 1-minus-0 contrast; variances have squared units, SEs original units.',
            'query_coordinates': 'Conditional prediction artifact retains query-row IDs, feature order and out-of-bag versus newdata distinction; not individual counterfactual effects.',
            'serialization': 'RcppUtilities::serialize_forest consumes tree unique_ptrs; do not reuse original. Deserialize into new object. Bind nuisance/training/feature/option/environment identities alongside model; no stable native ABI claim.'},
        'statistics': {
            'score': 'tau+(W-e)/(e*(1-e))*(Y-m-tau*(W-e))',
            'ATE': 'Weighted average of scores for an explicitly named population; initial q_i=1.',
            'variance': 'ATE std.err is already square-rooted; conditional variance.estimates is a variance. Neither excess.error nor mean CATE variances supplies ATE variance.',
            'cluster_extension': 'G/(G-1) sum_g[sum_i_in_g q_i(Gamma_i-theta)]^2 / (sum_i q_i)^2; G positive-weight clusters. Independent-cluster law and nuisance conditions required.',
            'weak_support': 'Reject boundary/invalid propensities and nonfinite scores; declared profile alarms never silently trim or retarget. Native denominator diagnostics required before a direct-native route.',
            'qualification': 'After engineering admission only execution_only with no confidence object. Conditional/asymptotic uncertainty needs its own construction evidence; no simultaneous or uniform guarantee inferred.'},
        'responses': {
            'unavailable': 'Current state: engine/dependency/admission receipt absent; no numeric result.',
            'unsupported': 'Recognized query outside profile; explain sampling/target mismatch and reviewed alternative.',
            'refused': 'Support or identification prerequisites fail under declared profile; retain diagnostics and target.',
            'not_identified': 'Only with an audited identification failure; inability of adapter is not proof.',
            'failed': 'Nonfinite result, corrupt model, subprocess error, timeout or resource failure; no partial numeric estimate.',
            'computed': 'Only admitted runtime result with original context and units, scalar AIPW target, provenance; uncertainty no stronger than bound evidence.',
            'sets': 'Preserve unknown/empty/disconnected/unbounded sets from applicable methods; this forest route cannot fabricate a finite interval for them.'},
        'deployment': {
            'declared_build': 'R >=3.5.0; C++17; GNU make; LinkingTo Rcpp/RcppEigen; imports DiceKriging,lmtest,Matrix,methods,Rcpp,sandwich; versions locked at admission.',
            'native_build': 'Inspected CMake builds an executable with src and test sources; shared-library ABI remains unqualified.',
            'environment': 'Record source/binary/compiler/flags/R/dependency/thread/RNG/global-option hashes and versions; declarations do not prove installed compatibility.',
            'rights': 'DESCRIPTION GPL-3; inspected source headers GPL-3-or-later; preserve file and dependency terms, review distribution obligations before release.',
            'isolation': 'One worker per local R process; native global runtime_context writes require separate shared-embedding concurrency review.',
            'faults': 'Parent-enforced wall/memory/output budget, bounded logs, atomic complete publication. No mid-tree resume; immutable replay only. Cross-environment bitwise equality unclaimed.'},
        'admission_sequence': [
            'Freeze complete source/dependencies/rights and a local runtime environment.',
            'Implement profile validator and request/result conversions with unavailable/unsupported/refusal/fault paths.',
            'Compare actual R execution with exact fixtures and source-correct AIPW/variance oracle; validate serialization/reload, coordinates and units.',
            'If needed implement native route and match R preprocessing, options, predictions and aggregation; include lifetime and failure trials.',
            'Profile full workflow; prospectively register generated-data study for any coverage/performance claim.',
            'Run registered study retaining failed requests; report scoped results and conditional next experiment.'],
        'reference_evidence': ref(BASE/'reproduction-review.json', 'Ten exact arithmetic comparisons; five reference rejections; no grf execution'),
        'limits': ['Proposal design only', 'No grf/core or transport execution', 'No source completeness/ABI or statistical qualification', 'No bank validation or product acceptance']}
    core.write(DEST, contract)

    groups = [
        ('memory', 'grf borrowed data views and consuming Rcpp serialization', [
            ('v12_exec13_grfcxx_1', 'Data.h lines32-51 and188-190: ownership and offset'),
            ('v12_exec13_grfcxx_2', 'Data.cpp lines31-82: borrowed constructor and role exclusion'),
            ('v12_exec13_grfcxx_3', 'RcppUtilities.h lines35-46: destructive serialization contract'),
            ('v12_exec13_grfcxx_4', 'RcppUtilities.cpp lines74-130: move trees, saved fields and borrowed matrix')],
         ['Column-major views borrow storage; host must preserve lifetime and coordinates.', 'Serialization consumes trees; a consumed native object is not reusable.']),
        ('runtime', 'grf source build and package dependency declarations', [
            ('v12_exec13_grfcxx_5', 'DESCRIPTION: Version, Depends, LinkingTo, Imports, License, SystemRequirements'),
            ('v12_exec13_grfcxx_6', 'CMakeLists lines7-9,25-26,48: C++17, test/source collection, executable'),
            ('v12_gap3_grf_license', 'COPYING GPL version3 terms; source headers retained separately')],
         ['Source identifies package2.6.1 and declared build/dependency requirements.', 'CMake executable is not evidence of a production shared-library ABI.', 'GPL terms are documented; distribution/dependency clearance is not awarded.']),
        ('rpath', 'grf residualization, causal scores and average effects', [
            ('v12_gap3_grf_technical', 'causal_forest.R lines30-38,153-252,301-339,390-436: weights, nuisance path, residualization and prediction variance'),
            ('v12_gap4_grf_scores', 'get_scores.R lines47-106: binary scores and two-regression identity'),
            ('v12_gap4_grf_average', 'average_treatment_effect.R lines125-172,202-250: target, weights, cluster correction and SE')],
         ['Residualization occurs in R before native training.', 'Binary AIPW differs from averaging fitted CATE.', 'Target weights and cluster variance preserve distinct meanings; CATE variance and ATE SE differ.']),
        ('native', 'grf causal binding and instrumental local prediction strategy', [
            ('v12_gap4_grf_binding_body', 'CausalForestBindings.cpp lines30-105: trainer, treatment as instrument, options, prediction and runtime_context'),
            ('v12_gap4_grf_instrumental_native', 'InstrumentalPredictionStrategy.cpp lines41-88,128-151: local moment ratio and variance'),
            ('v12_exec13_grfcxx_4', 'RcppUtilities.cpp lines157-180: variance values copied without square root')],
         ['Causal binding uses instrumental strategy with treatment as instrument.', 'Native ratio needs treatment variation; grouped-tree conditional variance is not the ATE variance.', 'Global context and finite outputs require explicit host controls.'])]
    sources = []
    for key, title, specs, claims in groups:
        originals = [original(i,a) for i,a in specs]
        sources.append(dict(integrated_citation_key='exec13_grf_'+key, kind='software_primary_sources',
                            title=title, author='GRF contributors', year=2026,
                            source_identity='https://github.com/grf-labs/grf/tree/'+COMMIT,
                            version_date=COMMIT+';2026-04-30;acquired2026-10-12;cutoff2026-10-07',
                            local_copy=originals[0]['local_copy'], originals=originals,
                            identity_evidence=ref(RAW/'v12_sw2_cutoff_grf.json', 'Commit date and identity only'),
                            inspected_anchors=[a for _,a in specs], supported_claims=claims,
                            limits=['Static source inspection; no downloaded engine execution or full runtime/ABI qualification.']))
    for key, title, p, anchors, claims in [
        ('design','Restricted grf R/native adapter design',DEST,
         ['scope/request/conversion/statistics/responses/deployment/admission_sequence'],
         ['Concrete proposed binary IID AIPW path with semantic, native ownership, failure and admission contracts.']),
        ('oracle','Exact native-boundary arithmetic and independent rational references',BASE/'reproduction-review.json',
         ['exact_expected and inference_limits; C++ score/moment/layout functions and Python independent AIPW expansion'],
         ['Ten scalar comparisons pass; five invalid reference cases reject.', 'Customer and equal-cluster means30/25; variances40,1600/9,225; AIPW mean5/2; slope3; layout20 versus3.'])]:
        sources.append(dict(integrated_citation_key='exec13_grf_'+key, kind='project_design' if key=='design' else 'project_derivation',
                            title=title, author='Causal banking research project', year=2026,
                            source_identity=str(p.relative_to(ROOT)), version_date='2026-10-13;project evidence;not grf execution',
                            local_copy=ref(p, '; '.join(anchors)), inspected_anchors=anchors, supported_claims=claims,
                            limits=['No statistical coverage, runtime admission, bank or independent acceptance.']))
    sources[-1]['implementation'] = [ref(ROOT/'tools/grf_boundary_oracle_20261013.cpp','Project arithmetic'),
                                      ref(ROOT/'tools/run_grf_boundary_oracle_20261013.py','Independent rational reference and compiler invocation')]
    audit = {'cutoff':'2026-10-07','sources':sources,
             'scope':'New software/source and project records only; inherited scholarly grf2018 record retains its real PDF and prior inspected anchors.'}
    shared.verify_refs(audit)
    core.write(BASE/'source-audit.json',audit)

    # Structural examples use the current schemas. They are not engine outputs.
    context = {'target': {'kind':'ATE','outcome':'Y','treatment':'W','contrast':'offer1-minus-no-offer0'},
               'population':{'definition':'Eligible customers in the declared sampling frame','unit':'customer'},
               'variables':[{'id':v,'role':r,'unit':u} for v,r,u in [('X','covariate','standardized'),('W','action','binary'),('Y','outcome','USD')]],
               'intervention':{'kind':'fixed_action','value':'W=1 versus W=0'},
               'horizon':{'value':12,'unit':'months'},'units':['USD'],'sign_convention':'offer-minus-no-offer',
               'observation_clock':{'event_time':'event_at','available_time':'available_at','decision_time':'decision_at',
                                    'rule':'strict_before_decision','alternative_justification':None},
               'sampling':{'law':'iid_customers','unit':'customer','fold_unit':'customer'},
               'assumptions':[{'id':a,'statement':a,'status':'unverified','evidence':[]} for a in ['consistency','no_interference','exchangeability','positivity']],
               'graph':None,'source_evidence':[]}
    fixture = {'kind':'deterministic_wire_fixture_not_fitted_data','columns':['Y','W','m','e','tau'],
               'rows':[[0,0,1,.25,2],[1,0,1,.5,2],[3,1,2,.5,2],[5,1,2,.75,2]],
               'warning':'Oracle inputs, including supplied nuisance numbers, are not admitted training data for the initial profile.'}
    core.write(BASE/'wire-input.json',fixture)
    config = {'schema_version':'causalbank.grf-config/1.0.0','engine_commit':COMMIT,
              'adapter_version':'proposal-1','profile':'binary-iid-aipw-all-v1',
              'target':'all_customer_ATE','seed':20261013,'num.threads':1,'runtime_admitted':False,
              'options':contract['scope']['initial_options']}
    config['options'] = copy.deepcopy(config['options']);config['options']['seed']=20261013
    core.write(BASE/'wire-configuration.json',config)
    req = {'schema_version':'causalbank.request/1.0.0','request_id':'grf-design-only',
           'operation':'estimate.effect','artifact_inputs':[
               artifact(BASE/'wire-input.json','grf-wire-fixture','data','project-wire-fixture/1'),
               artifact(BASE/'wire-configuration.json','grf-wire-config','engine_configuration','causalbank.grf-config/1.0.0')],
           'budget':{'wall_seconds':20,'memory_bytes':1073741824,'max_output_bytes':1000000,'model_calls':0},
           'parameters':contract['request']['parameters'],'scientific_context':context,'idempotency_key':'grf-design-only'}
    rsp = {'schema_version':'causalbank.response/1.0.0','request_id':req['request_id'],'operation':req['operation'],
           'status':'completed','disposition':'unavailable','context_sha256':context_digest(context),
           'result':None,'error':None,'evidence':[],'qualification':{'level':'none','evidence':[]}}
    cases=[{'label':'Design runtime unavailable; no engine attempt','request':req,'response':rsp}]
    q,r=copy.deepcopy(req),copy.deepcopy(rsp)
    q['scientific_context']['sampling']['law']='repeated_customer_calendar'
    r.update(disposition='unsupported',context_sha256=context_digest(q['scientific_context']))
    cases.append({'label':'Illustrative dependent-data profile rejection','request':q,'response':r})
    q,r=copy.deepcopy(req),copy.deepcopy(rsp)
    r.update(status='failed',error={'code':'NONFINITE_SCORE','message':'Hypothetical native nonfinite output; no engine was run.','retryable':False})
    cases.append({'label':'Illustrative numerical failure without estimate','request':q,'response':r})
    q,r=copy.deepcopy(req),copy.deepcopy(rsp)
    r.update(disposition='computed',result={'kind':'effect','estimate':[2.5],'coordinate_sets':None,'units':['USD'],
                                          'uncertainty':None,'payload':{'source':'Independent project score oracle; no fitted engine result'}})
    cases.append({'label':'Response-shape illustration using exact supplied-score reference only','request':q,'response':r})
    schemas=ROOT/'docs/program/repair-v12/work/IN02'
    for c in cases:
        jsonschema.validate(c['request'],json.loads((schemas/'request-schema.json').read_text()))
        jsonschema.validate(c['response'],json.loads((schemas/'response-schema.json').read_text()))
        validate_response(c['request'],c['response'])
    changed=copy.deepcopy(req);changed['scientific_context']['population']['unit']='branch'
    try:
        validate_response(changed,rsp)
    except ValueError as exc:
        rejection=str(exc)
    else:
        raise AssertionError('Stale population context accepted')
    core.write(BASE/'wire-examples.json',{'status':'pass','kind':'schema_and_reference_semantics_only',
                'engine_executed':False,'cases':cases,'stale_context_rejection':rejection,
                'limits':['No dispatcher, transport or admission validator executed.','Example data are supplied-score fixtures and do not meet the initial training profile.']})
    print(json.dumps({'contract':str(DEST.relative_to(ROOT)),'source_groups':len(sources),'wire_examples':len(cases),'engine_executed':False}))


if __name__ == '__main__':
    main()
