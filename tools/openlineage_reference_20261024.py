#!/usr/bin/env python3
"""Authored fixtures validate local declarative JSON only; no upstream client runs."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/'docs/literature/raw/exec24_openlineage_source_02.txt'

def calculate():
    schema=json.loads(SCHEMA.read_text())
    def check_refs(x):
        if isinstance(x,dict):
            if '$ref' in x: assert x['$ref'].startswith('#'), 'No remote schema reads'
            for v in x.values():check_refs(v)
        elif isinstance(x,list):
            for v in x:check_refs(v)
    check_refs(schema);Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema,format_checker=FormatChecker())
    base={'eventTime':'2026-10-07T10:00:00Z','producer':'https://example.org/producer/v1',
          'schemaURL':schema['$id'],'run':{'runId':'f49755a5-e6a8-4b31-ae48-97ba57a0c640'},
          'job':{'namespace':'bank-proposal','name':'generated-analysis'}}
    missing_type=deepcopy(base);terminal=deepcopy(base);terminal['eventType']='COMPLETE'
    invented=deepcopy(terminal)
    invented['run']['facets']={'causalAssertion':{'_producer':'https://example.org/producer/v1',
        '_schemaURL':'https://example.org/causal-facet/1','identified':True,'unsupported_claim':True}}
    bad=deepcopy(base);bad['run']['runId']='not-a-uuid'
    outcomes={k:validator.is_valid(v) for k,v in [('missing_event_type',missing_type),
        ('complete_without_inputs_or_outputs',terminal),('arbitrary_custom_claim',invented),('invalid_uuid',bad)]}
    assert outcomes==dict(missing_event_type=True,complete_without_inputs_or_outputs=True,arbitrary_custom_claim=True,invalid_uuid=False)
    duplicate_stream=[terminal,deepcopy(terminal)]
    assert all(validator.is_valid(v) for v in duplicate_stream)
    payloads=[b'version-A',b'version-B'];assert sha256(payloads[0]).digest()!=sha256(payloads[1]).digest()
    return {'validator':{'package':'jsonschema','version':version('jsonschema'),'schema_sha256':sha256(SCHEMA.read_bytes()).hexdigest(),
                'network_resolution':False,'format_checking':True,'upstream_clients_executed':False},
        'single_event_validation':outcomes,'fixtures':dict(missing_type=missing_type,terminal=terminal,custom_claim=invented,bad_uuid=bad),
        'stream_validation':{'individually_valid_duplicate_COMPLETE_events':2,'distinct_run_ids':1,'START_events':0,
            'single_document_schema_proves_lifecycle':False,'server_ingestion_tested':False},
        'identity':{'same_namespace_name':['bank-proposal','loan-history'],
            'different_content_sha256':[sha256(x).hexdigest() for x in payloads],
            'name_alone_is_immutable_version':False},
        'designed_cost':{'completed_analysis_jobs':3,'causally_accepted_artifacts':1,'abstentions':2,
            'stipulated_total_usd':45,'per_completed_job_usd':str(F(45,3)),'per_accepted_artifact_usd':str(F(45,1))},
        'scope':'Authored schema and arithmetic witnesses; no client/backend delivery trial, causal validation, prices or bank evidence.'}

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
