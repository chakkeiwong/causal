"""JSON-normalized successor; preserve exact authored calculations unchanged."""
import json
import data_workflow_wave_reference_20261025 as original

def calculate():
    return json.loads(json.dumps(original.calculate()))
