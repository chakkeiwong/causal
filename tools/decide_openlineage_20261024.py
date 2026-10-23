#!/usr/bin/env python3
"""Pinned lineage reference decision; acquired code is never executed."""
import argparse, hashlib, json, tomllib
from pathlib import Path
import run_program_checkpoint_v3 as controller
import openlineage_reference_20261024 as exact
from publish_latent_r_review_v2_20261013 import ref, write, verify_bindings

run=controller.base; core=run.core; ROOT=core.ROOT
BASE=ROOT/'docs/program/execution/2026-10-24/openlineage-reuse-v1'
RAW=ROOT/'docs/literature/raw'; OP='SW.DECISION.inherited_openlineage'
read=lambda p:json.loads(p.read_text())
LIMITS=['Static selected source and authored schema/arithmetic fixtures only; no upstream client, tests or receiver executed.',
 'Single-document validation does not qualify lifecycle completeness, persistence, exactly-once ingestion or scientific truth.',
 'Direct license/build declarations are not complete distribution rights, a solved environment or support commitment.',
 'Reference-only proposal decision; integration_allowed=false and capabilities empty.',
 'Visual, independent, bank and final acceptance remain open.']
CLAIMS={
 'source_00':([(1,201)],'Direct Apache2.0 terms; notice/change/attribution obligations and warranty limits, not transitive clearance.'),
 'source_01':([(1,97)],'Repository identity and lineage purpose; broad README ecosystem claims are not independently qualified.'),
 'source_02':([(1,63),(113,165),(230,304)],'Schema2.0.2: required run/job, optional event type and datasets, UUID, dataset naming and extensible base facets; no stream lifecycle validator.'),
 'source_03':([(1,115)],'Java8 source/target and Java17 toolchain; concrete dependency declarations, not a solved transitive lock.'),
 'source_04':([(65,106)],'Comment broader than guarded behavior: timer delegates emission, circuit breaker returns without emitting, duration passed to selected transport.'),
 'source_05':([(89,139),(330,400)],'Synchronous HTTP POST, default5000ms component timeouts, IOException wrapping and explicit400-599 response exception condition; no duration overload in selected file.'),
 'source_06':([(1,60)],'Python1.54.0, Python>=3.10, bounded uv_build and minimum runtime/optional dependency declarations.'),
 'source_07':([(175,225)],'Client adds facets and can reduce/filter/suppress; public emit discards transport response; debug serialization and close delegation.'),
 'source_08':([(403,443),(488,562)],'HTTP config5sec/TLSverifytrue; POST/close/status path, temporary HTTP debug suppression and urllib3 Retry configuration.'),
 'delegate_00':([(1,15)],'Default total/read/connect5,backoff0.3,status500/502/503/504,allowedHEAD/POST.'),
 'delegate_01':([(1,33)],'Default Duration overload delegates ordinary emit; bounded acknowledgement is transport-dependent.'),
 'delegate_02':([(1,77)],'HTTP timeout, authentication, compression, URL parameters and TLS configuration fields.'),
 'delegate_03':([(1,24)],'Response exception extends OpenLineageClientException and retains code/body; not universal no-throw behavior.')}

def prepare():
    assert not (BASE/'review.json').exists()
    assert exact.calculate()==read(BASE/'exact-results.json')
    inventories=read(BASE/'authenticated-source-inventory.json')+read(BASE/'authenticated-delegate-inventory.json')
    selected={x['id']:x for x in inventories}
    commit=read(RAW/'exec24_openlineage_cutoff.json')[0]
    tree=read(RAW/'exec24_openlineage_tree.json'); assert not tree['truncated']
    entries={x['path']:x for x in tree['tree']}
    assert commit['sha']=='87c977da7fe341780df678365d4073d4197f6ac6'
    assert commit['commit']['tree']['sha']==tree['sha']=='b5954df5c15f1a0e0b569d0700197ff9cf891403'
    assert commit['commit']['committer']['date']=='2026-10-07T13:24:25Z'
    records=[]
    for suffix,(spans,finding) in CLAIMS.items():
        key='exec24_openlineage_'+suffix;x=selected[key];p=ROOT/x['local_copy'];data=p.read_bytes();receipt=read(p.with_suffix('.receipt.json'))
        assert receipt['status']=='saved' and receipt['sha256']==hashlib.sha256(data).hexdigest()==x['sha256']
        assert x['commit']==commit['sha'] and '/'+commit['sha']+'/' in receipt['url']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==x['blob']==entries[x['path']]['sha']
        lines=data.decode().splitlines();anchors=[]
        for a,b in spans:
            assert 1<=a<=b<=len(lines)
            anchors.append(dict(lines=[a,b],text=chr(10).join(lines[a-1:b]),finding=finding))
        records.append(dict(source_identity=receipt['url'],version_date=commit['sha']+';7October2026',upstream_path=x['path'],local_copy=ref(p,finding),receipt=ref(p.with_suffix('.receipt.json'),'Bounded public acquisition'),git_blob_sha1=x['blob'],inspected_anchors=anchors,supported_claims=[finding],executed=False))
    assert len(records)==13
    source=dict(integrated_citation_key='exec24_openlineage_source',kind='software_primary_sources',title='OpenLineage pinned schema and Java/Python delivery contracts',author='OpenLineage contributors',year=2026,source_identity='https://github.com/OpenLineage/OpenLineage/tree/'+commit['sha'],version_date='7October2026 commit '+commit['sha']+';schema2.0.2;Python1.54.0',local_copy=records[2]['local_copy'],records=records,identity_evidence=[ref(RAW/'exec24_openlineage_cutoff.json','Default-branch cutoff selection'),ref(RAW/'exec24_openlineage_tree.json','Complete4317-entry immutable tree')],inspected_anchors=[r['local_copy'] for r in records],supported_claims=[r['supported_claims'][0] for r in records],limitations=LIMITS)
    reference=dict(integrated_citation_key='exec24_openlineage_reference',kind='project_evidence_not_scholarly_paper',title='Authored OpenLineage schema, lifecycle, immutable identity and cost witnesses',author='Causal banking proposal project',year=2026,source_identity='tools/openlineage_reference_20261024.py',version_date='24October2026;local declarative schema and exact arithmetic',local_copy=ref(Path(exact.__file__),'Authored fixtures; no upstream clients'),inspected_anchors=[ref(BASE/'exact-results.json','Explicit validator version, schema hash and outcomes')],supported_claims=['Selected schema accepts missing type, COMPLETE without datasets and arbitrary custom claim; rejects invalid UUID with format checking.','Two individually valid duplicate terminals do not prove complete lifecycle.','Dataset namespace/name does not distinguish two payload hashes.','Stipulated45USD over3 completed jobs versus1 accepted artifact gives15 versus45USD.'],limitations=LIMITS)
    write(BASE/'source-audit.json',dict(sources=[source,reference],cutoff='2026-10-07',authenticated_blobs=13,inspected_cited_blobs=13,native_execution=False))
    meta=tomllib.loads((RAW/'exec24_openlineage_source_06.txt').read_text())
    write(BASE/'dependency-license-review.json',dict(status='inspected_for_reference_choice',evidence=[ref(BASE/'source-audit.json','Exact original identities and inspected terms')],direct_license='Apache-2.0',observations=['Direct text requires license and applicable attribution retention and change notices.','Patent and trademark conditions and warranty/liability exclusions remain explicit.','Full transitive rights and distributed notices not cleared.'],python_build=meta['build-system'],python_runtime=meta['project']['dependencies'],python_requires=meta['project']['requires-python'],python_version=meta['project']['version'],java='DeclaredJava8source/target;Java17toolchain;HttpClient5.6.4 and other explicit coordinates',maintenance='Selected7October2026 commit; no inferred SLA, cost or support status.',resolved_environment=False))
    contract=dict(status='proposal_only',integration_allowed=False,
        input_fields=['request/attempt/run IDs','target/horizon/eligible population','data snapshot hash and availability clock','graph/model/assumptions and evidence hashes','nuisance/split/dependence/uncertainty specification','client/schema/receiver exact versions','authorized artifact references'],
        output_states=['estimate','identified set','sensitivity analysis','diagnostic','structured refusal'],
        delivery_states=['suppressed','attempted','acknowledged','persisted','reconciled'],
        separate_acceptance=['schema conformance','identification review','numerical qualification','artifact review','institutional approval'],
        failure_rules=['Do not convert missing eventType or a normal return into delivery success.','Reject unknown custom-facet versions and unresolved artifact identities.','Retain durable local record and explicit receiver acknowledgement/persistence contract.','Reconcile retries/duplicate/reordered events; UUID alone is not idempotency.','Timeout/cancel/requested deadline and causal refusal remain separate.','Record debug/logging and access policy without sending sensitive artifacts indiscriminately.'],
        behavioral_oracle=ref(BASE/'exact-results.json','Schema/identity/cost only; no transport oracle'),native_delivery_oracle='Not established; registered generated receiver/fault trials required.')
    write(BASE/'conversion-contract.json',contract)
    omissions=[('native_profile','Choose exact Java or Python client plus receiver and solved dependency/rights profile; no native code executed here.'),('custom_facet','Define approved causal-facet schema and bind scientific evidence separately from event validation.'),('delivery','Register missing/reordered/duplicate/suppressed events, custom-facet rejection, acknowledgement loss, receiver persistence, retries and cancellation.'),('consumer','Read-only consumer-specific requirements can be reviewed; no sibling adoption or modifications inferred.'),('cost','Measure full matched workflow denominators, refusal reasons, storage, retries, operations and support with actual prices.'),('source_scope','Selected HTTP paths only; other transports, remaining helpers and receiver semantics require their own pinned reviews.'),('historical_identity','Old mutable README is not attributed to failed historical HEAD acquisition; selected commit sources supersede identity uncertainty without rewriting history.')]
    write(BASE/'omissions-register.json',dict(items=[dict(gap=k,next_action=v,global_blocker=False) for k,v in omissions],native_execution=False))
    choice=dict(operation=OP,status='proposed_reference_decision',decision='reference',name='OpenLineage',selected_commit=commit['sha'],version='Schema2.0.2;Python1.54.0;Java commit-bound',canonical_aliases=['OpenLineage/OpenLineage','openlineage-python','io.openlineage client','OpenLineage.json'],target='Versioned run/job/dataset/facet protocol and selected Java/Python HTTP clients; no causal estimator.',reason='Retain lineage vocabulary and original-client references while requiring a separate causal evidence contract and receiver qualification.',source=ref(BASE/'source-audit.json','Pinned source and authored witnesses'),license=ref(BASE/'dependency-license-review.json','Direct terms/environment limits'),conversion_failure_contract=ref(BASE/'conversion-contract.json','Typed semantic and delivery boundaries'),
        uncertainty_contract=['Lineage carries a declared uncertainty object and sampling unit; it does not derive or validate it.','Identification/refusal, numerical status and bank acceptance are independent of COMPLETE and schema validity.'],
        alternatives=[dict(route='Original pinned Python or Java client',decision='preferred conditional prototype',reason='Preserve reviewed implementation; add causal facets and explicit receiver acknowledgement contract.'),dict(route='Direct schema-compatible emission from another language',decision='conditional alternative',reason='Avoid language runtime bridge but own validation, transport and compatibility maintenance.'),dict(route='Port whole integrations catalogue',decision='reject for present scope',reason='No demonstrated target or cost benefit justifies duplicate maintenance.'),dict(route='Local immutable file lineage',decision='retain comparator',reason='Small generated-data prototype can test artifact/target semantics before receiver deployment.'),dict(route='Treat lineage as causal certification',decision='reject',reason='Schema and job state cannot establish scientific truth.')],
        costs=dict(prices='Not supplied; authored45USD witness is not a measured quote',categories=['Schema/facet and receiver design','Source/dependency/rights review','Artifact storage and retention','Delivery/retry/reconciliation','Privacy/logging/access controls','Full failure-complete qualification and support']),
        owners=[dict(role='Method owner',obligation='Approve target/uncertainty/causal vocabulary and scientific review'),dict(role='Adapter owner',obligation='Freeze client/receiver and own conversion, lifecycle and failures'),dict(role='Rights owner',obligation='Resolve full distribution and transitive terms'),dict(role='Evaluation owner',obligation='Preregister generated/public trials and full cost denominators')],
        maintenance='Pinned cutoff source; no SLA or maintenance prediction.',revisit_trigger='Named receiver/profile, approved causal facet, solved environment/rights and registered semantic/delivery fault tests with matched total costs.',integration_allowed=False,capabilities=[],limitations=LIMITS)
    write(BASE/'choice.json',choice)
    write(BASE/'plan-review-v2.json',dict(status='pass_for_reference_decision_and_integration',evidence=[ref(BASE/'plan-review.json','Preserved acquisition plan'),ref(BASE/'source-audit.json','Authenticated primary evidence'),ref(BASE/'choice.json','Bounded choice')],checks=['Source comments checked against concrete delegates before claims.','Schema-only fixtures separated from client/backend experiments.','Preserve all1039 predecessor records and236 scholarly PDFs; add2 records.','Integrate manuscript and sponsor, verify exact sources/context/arithmetic/text bounds and renew exact-reader reviews.','No new scholarly paper, native admission or global blocker; continue independent work.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_schema_and_exact_accounting',evidence=[ref(Path(exact.__file__),'Inspected authored fixtures'),ref(BASE/'exact-results.json','Replayed exact results')],findings=['Internal references only; installed jsonschema4.26.0 with format checking.','UUID negative control fails while three scoped examples pass.','Duplicate terminal validation is individual, not server ingestion.','Stipulated cost denominators15 and45USD reproduce.'],native_execution=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(BASE/'development.tex','Connected product argument'),ref(BASE/'sponsor-addition.md','Sponsor consequences')],findings=['Schema and scientific claims, client comment and inspected behavior, prototype and bank evidence remain distinct.','No universal exception/async/timeout or exactly-once guarantee inferred.','No imported ecosystem citation substitutes for original evidence.'],visual_acceptance=False))
    evidence=[ref(BASE/n,'Reviewed reference choice') for n in ['source-audit.json','dependency-license-review.json','conversion-contract.json','omissions-register.json','choice.json','plan-review-v2.json','mathematical-review.json','copyedit-review.json','development.tex','sponsor-addition.md','exact-results.json']]+[ref(Path(__file__),'Decision logic')]
    review=dict(status='pass_for_reference_only_decision',evidence=evidence,findings=['Thirteen blobs authenticated against cutoff commit/tree and inspected.','Semantics, alternatives, direct rights, owner obligations, costs and revisit trigger explicit.','Reference-only proposal outcome; all runtime and scientific acceptance boundaries retained.'],integration_allowed=False,native_execution=False,limitations=LIMITS)
    verify_bindings(review);write(BASE/'review.json',review);print(json.dumps(dict(sources=2,blobs=13,decision='reference',integration_allowed=False)))

def receipt():
    state=core.read(ROOT,core.STATE);assert state['execution_runtime']['active']['operation']==OP
    verify_bindings(read(BASE/'review.json'));graph,merged,_=run.combined(ROOT,state);node=run.ledger.operation(graph,OP)
    value=read(BASE/'choice.json');value.update(status='pass',scope='Completed proposal reference disposition; no native admission',evidence=[ref(BASE/'review.json','Author review')]);output=ROOT/node['outputs'][0];write(output,value)
    evidence=[ref(BASE/n,'Reviewed pinned reference choice') for n in ['review.json','choice.json','dependency-license-review.json','conversion-contract.json','exact-results.json']]
    findings=['Pinned aliases/schema/client identity, direct license, build/dependency and maintenance evidence bound.','Target/uncertainty semantics, alternatives, costs, owners and revisit trigger explicit.','Reference-only; integration disallowed and capabilities empty; native delivery oracle remains required.']
    result=run.ledger.receipt_template(node);result.update(outcome='pass',execution='performed',scope=value['scope'],reviewer=dict(name='Codex author/coordinator',kind='author'),outputs=[ref(output,'Reference-only choice')],criteria=[dict(index=i,verdict='pass',finding=f,evidence=evidence) for i,f in enumerate(findings)],limitations=LIMITS,capabilities=[],nonexecution_reason='',revisit_trigger=value['revisit_trigger'])
    run.validate_receipt(ROOT,merged,node,result,len(state['execution_program']['turns']));verify_bindings(result);write(BASE/'operation-receipt.json',result);print('OpenLineage reference receipt prepared')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','receipt']);globals()[p.parse_args().command]()
