#!/usr/bin/env python3
"""Authored local-schema and arithmetic witnesses; no upstream service or client."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'docs/literature/raw'


def calculate():
    files=[RAW/f'exec24_openmetadata_source_{k}.txt' for k in ['03','04','05']]
    files.append(RAW/'exec24_openmetadata_extra_00.txt')
    docs=[json.loads(p.read_text()) for p in files]
    def refuse(uri):
        raise NoSuchResource(uri)
    registry=Registry(retrieve=refuse).with_resources(
        (d['$id'],Resource.from_contents(d)) for d in docs)
    # The acquired basic schema has Java-specific regex in an unused entityLink
    # definition. Preserve it; do not silently translate or claim full conformance.
    for d in docs[:3]:Draft202012Validator.check_schema(d)
    Draft202012Validator.check_schema(docs[3]['definitions']['uuid'])
    assert docs[3]['definitions']['entityLink']['pattern'].startswith('(?U)')
    validator=Draft202012Validator(docs[0],registry=registry,format_checker=FormatChecker())
    a={'id':'00000000-0000-4000-8000-000000000001','type':'table'}
    b={'id':'00000000-0000-4000-8000-000000000002','type':'table'}
    minimal={'edge':{'fromEntity':a,'toEntity':b}}
    claim=deepcopy(minimal);claim['edge']['lineageDetails']={'causalEffect':100,'identified':True}
    bad=deepcopy(minimal);bad['edge']['fromEntity']['id']='not-a-uuid'
    extra=deepcopy(minimal);extra['accepted']=True
    reverse={'edge':{'fromEntity':b,'toEntity':a}}
    results={k:validator.is_valid(x) for k,x in [('minimal_without_details',minimal),
        ('unregistered_causal_fields_in_details',claim),('invalid_uuid',bad),
        ('extra_top_level_field',extra),('reverse_edge',reverse)]}
    assert results==dict(minimal_without_details=True,unregistered_causal_fields_in_details=True,
        invalid_uuid=False,extra_top_level_field=False,reverse_edge=True)
    # Abstract filtering rule from the inspected selected method, not its execution.
    from_columns={'balance','status'};to_columns={'score'}
    submitted=[{'from':['balance','ghost'],'to':'score'}, {'from':['status'],'to':'missing'}]
    retained=[]
    for edge in submitted:
        if edge['to'] not in to_columns:continue
        valid=[c for c in edge['from'] if c in from_columns]
        if valid:retained.append({'from':valid,'to':edge['to']})
    assert retained==[{'from':['balance'],'to':'score'}]
    return dict(validator=dict(package='jsonschema',version=version('jsonschema'),format_checking=True,
        network_resolution=False,schemas=[dict(path=str(p.relative_to(ROOT)),sha256=sha256(p.read_bytes()).hexdigest()) for p in files],
        scope='Only references traversed by these fixtures; this is not every API schema or server validation.',
        full_basic_schema_compatibility='Unqualified: unused entityLink (?U) regex fails Python metaschema format validation; raw bytes preserved.'),
        validation=results,fixtures=dict(minimal=minimal,claim=claim,bad_uuid=bad,extra=extra,reverse=reverse),
        graph=dict(individually_valid_opposite_edges=2,document_schema_proves_acyclicity=False,server_behavior_tested=False),
        column_filter=dict(submitted=submitted,retained=retained,full_server_executed=False),
        identity=dict(same_entity=a,distinct_payload_hashes=[sha256(x).hexdigest() for x in [b'loan-snapshot-A',b'loan-snapshot-B']],reference_alone_binds_content=False),
        retry=dict(stipulated_sequence=[503,503,503,200],configured_retries=3,attempts=4,
            sleep_seconds=[30,60,90],total_sleep_seconds=180,network_time_included=False,
            scope='Abstract configured HTTP-retry trace, not wall-clock or delivery measurement'),
        designed_cost=dict(stipulated_total_usd=60,submitted_edges=4,persisted_edges_assumed=3,
            accepted_causal_artifacts_assumed=1,per_submission_usd=str(F(60,4)),
            per_persisted_edge_usd=str(F(60,3)),per_accepted_artifact_usd=str(F(60,1))),
        scope='Authored declarative fixtures and arithmetic; no upstream client/server/test execution, observed vulnerability, actual pricing or bank evidence.')


if __name__=='__main__':print(json.dumps(calculate(),indent=2))
