#!/usr/bin/env python3
"""JSON-stable successor to the preserved exact GCM witness calculator."""
import json
import gcm_reuse_reference_20261024 as original

def calculate():
    # JSON represents the original tuple-valued binary outcomes as lists.
    # Preserve all values and compare exactly in that same serialized domain.
    return json.loads(json.dumps(original.calculate()))

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
