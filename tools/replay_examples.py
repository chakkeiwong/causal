#!/usr/bin/env python3
"""Recompute the frozen scientific outputs without changing their artifact hashes."""
import json
from pathlib import Path
import numpy as np
import run_examples as examples

ROOT = Path(__file__).resolve().parents[1]


def compare(actual, expected, path):
    if isinstance(expected, dict):
        assert set(actual) == set(expected), "Key mismatch: " + path
        for k, value in expected.items():
            compare(actual[k], value, path + "/" + str(k))
    elif isinstance(expected, list):
        assert len(actual) == len(expected), "Length mismatch: " + path
        for i, value in enumerate(expected):
            compare(actual[i], value, path + "/" + str(i))
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert np.isclose(actual, expected, atol=1e-8, rtol=1e-8), "Numerical mismatch: " + path
    else:
        assert actual == expected, "Mismatch: " + path


def main():
    frozen = json.loads((ROOT / "docs/examples/results.json").read_text())
    rng = np.random.default_rng(frozen["seed"])
    computed = {
        "static": examples.static_aipw(rng),
        "longitudinal": examples.longitudinal(),
        "staggered": examples.staggered(),
        "pomdp": examples.pomdp(rng),
        "hmm_recovery": examples.hmm_recovery(rng),
        "economics": examples.economics(),
    }
    # JSON normalization makes the saved integer dictionary keys comparable.
    computed = json.loads(json.dumps(computed))
    for key, result in computed.items():
        compare(result, frozen[key], key)
    output = {"status": "pass", "seed": frozen["seed"], "families": list(computed),
              "relative_tolerance": 1e-8, "absolute_tolerance": 1e-8,
              "scope": "Replay of frozen synthetic calculations; not coverage, scale, package or bank validation."}
    (ROOT / "docs/examples/replay-check.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
