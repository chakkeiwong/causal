#!/usr/bin/env python3
"""Inspect downloaded data as data; never import or execute StatsPAI code."""
import ast
import hashlib
from fractions import Fraction
from importlib.metadata import version
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'docs/literature/raw'

def calculate():
    schema_path=RAW/'exec23_statspai_blob_2.txt'
    schema=json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    cases=[('method_only',{'method':'iv'},True),
           ('invalid_semantics',{'method':'iv','ci':[2,1],'se':-1,'pvalue':2,'alpha':-1,'n_obs':0.5},True),
           ('empty_interval',{'method':'iv','ci':[]},True),
           ('wrong_method_type',{'method':1},False)]
    results=[]
    for name,payload,expected in cases:
        accepted=validator.is_valid(payload)
        assert accepted==expected
        results.append(dict(name=name,payload=payload,schema_accepts=accepted))
    tree=ast.parse((RAW/'exec23_statspai_blob_6.txt').read_text())
    node=next(n for n in tree.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=='_RESULT_OUTPUT_SCHEMA_COMPACT')
    fields={ast.literal_eval(k):v for k,v in zip(node.value.keys,node.value.values)}
    compact={k:ast.literal_eval(fields[k]) for k in ['type','additionalProperties']}
    assert set(fields)=={'type','additionalProperties','description'}
    assert Draft202012Validator(compact).is_valid({})
    tree=ast.parse((RAW/'exec23_statspai_blob_4.txt').read_text())
    node=next(n for n in tree.body if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=='PYTHON_REFERENCE_ROWS')
    refs=ast.literal_eval(node.value)
    assert len(refs)==8
    customer=(10*4+10*(-4))/20
    observation=Fraction(10*3*4+10*(-4),10*3+10)
    assert customer==0 and observation==2
    return dict(kind='project_authored_static_contract_and_exact_arithmetic_witnesses',
      schema_sha256=hashlib.sha256(schema_path.read_bytes()).hexdigest(),jsonschema_version=version('jsonschema'),
      schema_cases=results,compact_schema_accepts_empty_object=True,
      python_reference_rows=refs,python_reference_count=len(refs),
      financial_example=dict(cohorts=[dict(customers=10,post_periods=3,effect_usd=4),dict(customers=10,post_periods=1,effect_usd=-4)],
        customer_weighted_effect_usd=0,treated_observation_weighted_effect_usd=2,
        stipulated_cost_per_customer_usd=1,customer_net_usd=-1,observation_value_minus_cost_usd=1,
        interpretation='The latter subtracts a per-customer cost from a different weighting target; it is not the same customer decision.'),
      duplicated_json_example=dict(structured_bytes=262144,two_payload_copies_bytes=524288,wire_bytes='strictly greater after envelope and escaping; image bytes additional'),
      downloaded_code_executed=False,native_qualification=False)
if __name__=='__main__': print(json.dumps(calculate(),indent=2))
