#!/usr/bin/env python3
"""JSON-stable successor to the preserved 24 October exact witnesses."""
import json
import ecmo_graph_reference_20261024 as original

def calculate():
    return json.loads(json.dumps(original.calculate()))

if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
