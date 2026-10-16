#!/usr/bin/env python3
"""Review and record the bounded graph/set proposal requirement."""
import json
from pathlib import Path

import master_control as core
import run_program as run
import review_topology_v2_20261016 as work
from publish_latent_r_review_v2_20261013 import ref,transition,verify_bindings,write

ROOT,BASE,OP,OUTPUT=work.ROOT,work.BASE,work.OP,work.OUTPUT


def contract():
    return {
      'status':'proposed; not implemented by this review','version_date':'2026-10-16',
      'acceptance_scope':'Public/generated proposal prototype before authentic bank trials',
      'requirements':[
       {'id':'G1','meaning':'Graph family, endpoint marks and background restrictions',
        'proposed_fields':['representation_version','claimed_graph_family','node_identity_map','endpoint_marks','background_restriction_refs'],
        'local_acceptance':['Three-node exhaustive graph enumeration and chain class membership','Invalid family marks and cycles rejected by a declared class recognizer','PAG circle/arrow/tail and all supported mixed edges survive each native conversion'],
        'refusal':'unsupported_graph_family or invalid_graph_class; no silently selected DAG',
        'remaining':'Select and inspect a complete recognizer for each supported family; finite enumeration does not prove general completeness.'},
       {'id':'G2','meaning':'Graph-set members are scientific alternatives',
        'proposed_fields':['member_artifacts','member_node_maps','recognizer_identity','recognition_input_digest','recognition_scope'],
        'local_acceptance':['Resolve every member and verify exact bytes/schema','Missing/corrupt/duplicated members and mismatched variables','Union-of-edges and first-member substitutions fail the chain and equal-law references'],
        'refusal':'unavailable_member, incompatible_member or unsupported_identification; preserve original class',
        'remaining':'Actual member resolution and native library conversion acceptance; syntax counts are insufficient.'},
       {'id':'C1','meaning':'Coordinates bind target and transformations',
        'proposed_fields':['coordinate_id','outcome','contrast','population','horizon','statistic','unit','ordered_coordinate_ids','transformation_id'],
        'local_acceptance':['Same-unit reversed order is rejected or explicitly reindexed','Duplicate/missing coordinates refused','Permute estimate,covariance,joint constraints and financial weights together','Use unequal sentinel values; verify proposed retail/corporate net25 versus misread-5USD'],
        'refusal':'coordinate_mismatch or undeclared_transform',
        'remaining':'A successor schema and all adapter implementations; IDs do not certify the truth of an attached value.'},
       {'id':'S1','meaning':'Topology and set semantics survive mappings',
        'proposed_fields':['set_state','topology','interval_components','endpoint_inclusion','coordinate_ids','geometry','approximation_relation','uncertainty_kind','construction_evidence'],
        'local_acceptance':['Unknown,empty,whole-line,singleton and disconnected cases','Negative affine map reverses endpoints and component order','Nonlinear mappings use proved images or labelled outer bounds','Joint line versus rectangular projection net-value reference','Unknown member is never dropped as empty'],
        'refusal':'unsupported_set_geometry or uncomputed_constituent',
        'remaining':'Supported joint-region representation, certified arithmetic for declared domain, and statistical construction review; coordinate boxes alone lose relations.'},
       {'id':'N1','meaning':'Shared numeric and canonical context encoding',
        'proposed_fields':['numeric_codec_version','exact_integer_domain','decimal_scale','rounding_rule','canonical_context_bytes','context_digest'],
        'local_acceptance':['Exact large identifiers remain strings','2^53+1 singleton rejected or preserved in an explicit exact representation','Integral float12.0 and integer12 follow declared canonical equivalence rule','Actual changed context remains rejected','Unbounded endpoints remain explicit; no NaN or finite sentinel substitution'],
        'refusal':'numeric_domain_exceeded, unsupported_codec or context_mismatch',
        'remaining':'Shared encoding implementation and Python/R/Java/C++/Node byte and numeric fixtures; changing numeric schema requires a versioned successor.'},
       {'id':'V1','meaning':'Scientific validity remains separate from successful transport',
        'proposed_fields':['declaration_review','graph_recognition','identification_disposition','sampling_regime','joint_construction','approximation_error','qualification_evidence'],
        'local_acceptance':['Supplied-DAG back-door failure retains its limited scope','Unsupported graph classes publish no numeric effect','Pointwise coverage not relabelled simultaneous','All failed/unavailable/native cases remain in denominator','Generated equal observed laws retain different intervention effects'],
        'refusal':'unsupported_method or unresolved_identification; do not claim general nonidentification without a certificate',
        'remaining':'Regime-specific causal/uncertainty research; universal latent temporal recovery is not promised.'},
      ],
      'prototype_sequence':['Implement one graph-family recognizer and typed coordinate/codec successor','Execute exact/adverse cases at every actually implemented native boundary','Match library,CLI and MCP outputs plus refusal/error behavior','Run registered generated truth and suitable documented public examples','Use the resulting comparison to justify or reject later costly bank trials'],
      'owner_inputs_later':{'scientific_owner':['Variable meanings','Feasible interventions','Background restrictions and clock evidence','Sampling and latent-variable assumptions'],
        'consumer_platform_owner':['Accepted encodings and version migration','Actual language/runtime versions','Resource/deadline and recovery requirements'],
        'decision_owner':['Population and horizon','Losses,precision thresholds and real costs'],'independent_reviewer':['Graph/identification and joint-coverage review in the declared regime']},
      'known_routes':['Stable coordinate binding and explicit reindexing','Typed set and member handling','Shared exact/canonical codec','Generated adversarial acceptance cases for chosen native routes'],
      'unresolved_science':['Additional information distinguishing observationally equivalent causal models','General latent/temporal graph retention and effect-set calibration','Decision-useful precision for a chosen dependent regime'],
      'limits':work.LIMITS,
    }


def main():
    state=core.read(ROOT,core.STATE)
    assert state['execution_runtime']['active']['operation']==OP
    exact=json.loads((BASE/'exact-results.json').read_text());assert exact==work.exact()
    probes=json.loads((BASE/'runtime-probes.json').read_text())
    codec=json.loads((BASE/'node-roundtrip.json').read_text())
    assert len(probes['results'])==12 and codec['unsafe_integer']['both_validated']
    assert not codec['integral_float_context']['response_validation']['accepted']
    for path in ['runtime-probes.json','node-roundtrip.json','harness-repair.json','baseline-tests.json']:
        verify_bindings(json.loads((BASE/path).read_text()))
    source_paths={
      'src/causalbank/operation_contract_v12.py':'validate_context,validate_set,validate_response: graph scope,topology,units/counts and digest',
      'src/causalbank/operation_service_v12.py':'validate_request,invoke,_graph,_identify,_estimate: actual syntax and bounded identification scope',
      'src/causalbank/problem_contract_v12.py':'review_problem: allowed marks,duplicate edges,directed cycles,event order and delegated recognition',
      'src/causalbank/linkage_sets.py':'merge_intervals,weighted_sum: signed union arithmetic; Cartesian-product input semantics',
      'src/causalbank/discovery_sets.py':'module scope,covariance_region,dag_class: three-variable IID Gaussian causally sufficient outer construction',
      'src/causalbank/causal_workflow.py':'adjustment_expression: selected sufficient back-door criterion and rejection boundary',
      'docs/program/repair-v12/work/IN02/request-schema.json':'scientific_context units,graph marks and generic scientific target',
      'docs/program/repair-v12/work/IN02/response-schema.json':'typed result,coordinate_sets,units and unrestricted payload',
    }
    write(BASE/'primary-review.json',{'status':'pass','reviewer':work.REVIEWER,'version_date':'2026-10-16;source bytes unchanged from Git1533afc3',
      'sources':[ref(ROOT/p,a) for p,a in source_paths.items()],
      'observations':['Graph syntax and formal class recognition have different explicit scopes.',
        'Unit/count checks do not bind a coordinate-ID order vector;generic payload can carry a conflicting order.',
        'Unknown and empty states differ;weighted interval arithmetic computes a product image and cannot restore lost joint restrictions.',
        'Selected identification deliberately declines graph families and unsupported adjustments.',
        'Exact context bytes are bound under current Python serialization;cross-language number normalization needs an explicit contract.'],
      'limits':work.LIMITS})
    write(BASE/'proposed-acceptance-contract.json',contract())
    specs=[
      ('exec16_topology_runtime','Observed graph and coordinate semantic boundaries','project_implementation','runtime-probes.json',
       'Twelve bounded local service/validator case families',
       ['Actual syntax-only admissions,correct DAG/topology refusals,missing-member count,same-unit order mismatch and limited back-door result.']),
      ('exec16_topology_exact','Exact graph,coordinate and set-image banking references','project_derivation','exact-results.json',
       '25 DAGs,11 skeleton/collider groups;equal Gaussian laws;coordinate net25/-5;joint net-2 versus rectangle[-12,8];signed set images',
       ['Finite enumerations,explicit equal-law SCMs and stipulated monetary/set calculations;no fitted statistical performance.']),
      ('exec16_topology_codec','Observed Python and Node JSON topology and number round trips','project_implementation','node-roundtrip.json',
       'structural,unsafe_integer and integral_float_context observations',
       ['Tested topology/strings survive;2^53+1 singleton rounds down;12.0 context becomes12 and causes digest rejection.']),
      ('exec16_topology_source','Inspected local graph and set implementation scopes','project_implementation','primary-review.json',
       'Eight original implementation/schema artifacts and recorded anchors',
       ['Selected declaration checks,syntax-only operation,limited identification,product-set arithmetic and three-variable Gaussian outer construction.']),
      ('exec16_topology_contract','Proposed graph,set,coordinate and codec acceptance contract','project_design','proposed-acceptance-contract.json',
       'G1,G2,C1,S1,N1,V1;prototype sequence;later owner inputs;known routes and unresolved science',
       ['Proposed typed fields,refusals,exact/adverse cases,native and transport qualification sequence;not an implemented successor.']),
    ]
    sources=[]
    for key,title,kind,name,anchor,claims in specs:
        sources.append({'integrated_citation_key':key,'title':title,'kind':kind,'author':'Causal banking research project','year':2026,
          'source_identity':str((BASE/name).relative_to(ROOT)),'version_date':'2026-10-16;authored local proposal evidence',
          'local_copy':ref(BASE/name,anchor),'inspected_anchors':[anchor],'supported_claims':claims,
          'primary_artifacts':[ref(BASE/'development.tex','Connected derivation and proposal scope'),
            ref(ROOT/'tools/review_topology_20261016.py','Preserved initial exact/Node driver and failed runtime-root setup'),
            ref(ROOT/'tools/review_topology_v2_20261016.py','Successor runtime driver;only temporary-root location corrected')],
          'limits':work.LIMITS})
    write(BASE/'source-audit.json',{'cutoff':'2026-10-07','sources':sources,'new_scholarly_papers':0,'visual_acceptance':False})
    evidence=[ref(BASE/p,p) for p in ['plan.md','baseline-tests.json','runtime-probes.json','exact-results.json',
        'node-roundtrip.json','harness-repair.json','primary-review.json','proposed-acceptance-contract.json','source-audit.json','development.tex']]
    findings=[
      'Bound eight unchanged implementation/schema artifacts and twelve actual case families;distinguished syntax,recognition,identification and set meaning. Proposed six contract groups specify local acceptance and later owner inputs.',
      'Existing62 tests pass;actual Python/Node fixtures reproduce coordinate-order and numeric/digest boundaries. Exact finite graph,Gaussian,monetary,joint-set and signed-image references reproduce. Failure/refusal modes and no-native/no-bank limits are explicit.'
    ]
    write(OUTPUT,{'operation':OP,'status':'pass','scope':'Proposal requirement development and author review;no product qualification',
      'reviewer':work.REVIEWER,'criteria_findings':findings,'evidence':evidence,'remaining':work.LIMITS,
      'known_routes':contract()['known_routes'],'unresolved_science':contract()['unresolved_science'],
      'next_action':'Integrate and inspect preserving monograph successor;then continue eligible operation.'})
    write(BASE/'author-review.json',{'status':'pass','issues':[],'reviewer':work.REVIEWER,'findings':findings,
      'evidence':evidence+[ref(OUTPUT,'Contracted scoped requirement output')],
      'limitations':work.LIMITS,'scope':'Author source/math/proposal review;visual review pending;no capability qualified'})
    graph,_,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP);receipt=run.ledger.receipt_template(node)
    receipt.update(outcome='pass',execution='performed',scope='Proposal requirement only',reviewer=work.REVIEWER,
      limitations=work.LIMITS,outputs=[ref(OUTPUT,'Reviewed requirement')],nonexecution_reason='',revisit_trigger='',capabilities=[],
      criteria=[{'index':i,'verdict':'pass','finding':f,'evidence':evidence} for i,f in enumerate(findings)])
    write(BASE/'operation-receipt.json',receipt);transition('record',OP,BASE/'operation-receipt.json')
    print(json.dumps({'requirement':'pass','local_case_families':12,'new_citations':5,'product_qualified':False}))


if __name__=='__main__':main()
