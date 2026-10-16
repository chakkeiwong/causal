#!/usr/bin/env python3
"""Clarify equal-arm pooled accuracy; preserve the original exact receipt."""
import json
from ontology_reference_20261017 import ROOT, BASE, calculate as original


def calculate():
    result=original()
    row=result['differential_measurement']
    row['pooled_accuracy_equal_arms']=row.pop('pooled_balanced_accuracy')
    return result


if __name__=='__main__':
    with (BASE/'exact-results-v2.json').open('x') as stream:
        json.dump(calculate(),stream,indent=2);stream.write('\n')
    print(json.dumps({'families':6,'repair':'Field name distinguishes equal-arm pooling from class-balanced accuracy; values unchanged.'}))
