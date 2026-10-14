#!/usr/bin/env python3
"""Replay inspected proposal calculations into fresh Q3 evidence, never originals."""
import argparse
import contextlib
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib
import io
import json
import math
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-13/prototype-review'
OLD = ROOT / 'docs/program/execution/2026-10-13'


def ref(path):
    return {'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def normalize(value):
    return json.loads(json.dumps(value, default=lambda x: str(x) if isinstance(x, Fraction) else x))


def compare(actual, expected, path='root'):
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and actual.keys() == expected.keys(), path + ': keys'
        for key, value in expected.items():
            compare(actual[key], value, path + '/' + key)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), path + ': length'
        for i, (a, b) in enumerate(zip(actual, expected)):
            compare(a, b, path + '/' + str(i))
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert isinstance(actual, (int, float)) and math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-8), path + ': numeric'
    else:
        assert actual == expected, path + ': value'


def captured_main(module):
    text = io.StringIO()
    with contextlib.redirect_stdout(text):
        module.main()
    return json.loads(text.getvalue())


def run(group, destination):
    destination.mkdir(parents=True, exist_ok=False)
    os.environ['MPLCONFIGDIR'] = str(destination / 'matplotlib-cache')
    records = []

    def perform(name, original, code, action):
        before = ref(original)
        row = {'family': name, 'frozen_result': before, 'code': [ref(ROOT / 'tools' / (m + '.py')) for m in code]}
        try:
            actual = normalize(action())
            computed = destination / (name + '.json')
            computed.write_text(json.dumps(actual, indent=2) + '\n')
            row['recomputed_result'] = ref(computed)
            compare(actual, json.loads(original.read_text()))
            row['status'] = 'pass'
        except Exception as exc:
            row.update(status='fail', error=type(exc).__name__ + ': ' + str(exc))
            (destination / (name + '.failure.txt')).write_text(traceback.format_exc())
        row['original_unchanged'] = ref(original) == before
        if not row['original_unchanged']:
            row['status'] = 'fail'
        records.append(row)
        (destination / 'receipt.json').write_text(json.dumps({
            'scope': 'Fresh numerical replay of frozen demonstrations; no new qualification study',
            'executed_at': datetime.now(timezone.utc).isoformat(),
            'harness': ref(Path(__file__)), 'python': sys.version,
            'comparison': {'absolute_tolerance': 1e-8, 'relative_tolerance': 1e-8,
                           'rational_strings_and_discrete_fields': 'exact'},
            'records': records,
            'status': 'pass' if all(r['status'] == 'pass' for r in records) else 'fail',
        }, indent=2) + '\n')
        print(json.dumps({'family': name, 'status': row['status'], 'original_unchanged': row['original_unchanged'],
                          **({'error': row['error']} if 'error' in row else {})}), flush=True)

    if group == 'foundation':
        import numpy as np
        import run_examples as examples
        frozen = ROOT / 'docs/examples/results.json'
        seed = json.loads(frozen.read_text())['seed']
        rng = np.random.default_rng(seed)

        def foundation():
            result = json.loads(frozen.read_text())
            # Original shared RNG order is part of the frozen experiment.
            result.update(static=examples.static_aipw(rng), longitudinal=examples.longitudinal(),
                          staggered=examples.staggered(), pomdp=examples.pomdp(rng),
                          hmm_recovery=examples.hmm_recovery(rng), economics=examples.economics())
            return result
        perform('six-foundational-families', frozen, ['run_examples'], foundation)

    elif group == 'exact':
        pure = [
            ('software-contract', 'proposal_contract_examples_20261013', 'exact-examples.json'),
            ('formulation-targets', 'formulation_target_examples_20261013', 'formulation-targets.json'),
            ('persistent-region', 'persistent_region_examples_20261013', 'research/persistent-region-examples.json'),
            ('servicing', 'servicing_observed_examples_20261013', 'servicing/exact-results.json'),
            ('python-discovery', 'python_discovery_examples_20261013', 'python-discovery/oracle-results.json'),
            ('survey-comparison', 'survey_comparison_examples_20261013', 'survey-comparison.json'),
            ('commercial-latent', 'commercial_latent_examples_20261013', 'commercial-latent/exact-results.json'),
        ]
        for name, module, source in pure:
            perform(name, OLD / source, [module], importlib.import_module(module).calculate)
        stdout = [
            ('diagrams', 'diagram_examples_20261013', 'diagrams/exact-results.json'),
            ('restrictions', 'diagram_restrictions_20261013', 'diagrams/restriction-results.json'),
            ('ontology', 'ontology_examples_20261013', 'diagrams/ontology-results.json'),
            ('interchange', 'interchange_examples_20261013', 'interchange/example-results.json'),
            ('composition', 'interchange_composition_examples_20261013', 'interchange/composition-results.json'),
            ('python-identification', 'python_identification_oracles_20261013', 'python-integration/oracle-results.json'),
        ]
        for name, module, source in stdout:
            perform(name, OLD / source, [module], lambda m=module: captured_main(importlib.import_module(m)))
        redirected = [
            ('semantic-v131', 'gap_semantic_examples_v13_1', ROOT / 'docs/program/gap-execution-v13_1/semantic-examples.json', 'file'),
            ('design-v13', 'gap_design_checks_v13', ROOT / 'docs/program/gap-repair-v13/work/RG1/design-checks.json', 'directory'),
            ('llm-census', 'llm_census_examples_20261013', OLD / 'llm-census/exact-examples.json', 'file'),
        ]
        for name, module, original, mode in redirected:
            def action(m=module, n=name, style=mode):
                imported = importlib.import_module(m)
                target = destination / (n + '-raw.json')
                if style == 'directory':
                    imported.OUT = destination / n
                    target = imported.OUT / 'design-checks.json'
                else:
                    imported.OUT = target
                with contextlib.redirect_stdout(io.StringIO()):
                    imported.main()
                return json.loads(target.read_text())
            perform(name, original, [module], action)
        for name, module, original in [
            ('java-discovery', 'java_discovery_examples_20261013', OLD / 'java-discovery/exact-results.json'),
            ('java-adapter', 'java_adapter_oracles_20261013', OLD / 'java-integration/oracle-results.json'),
        ]:
            def action(m=module, n=name):
                target = destination / (n + '-raw.json')
                previous = sys.argv
                try:
                    sys.argv = [m, '--output', str(target)]
                    with contextlib.redirect_stdout(io.StringIO()):
                        importlib.import_module(m).main()
                finally:
                    sys.argv = previous
                return json.loads(target.read_text())
            perform(name, original, [module], action)

    elif group == 'native-temporal':
        import run_grf_boundary_oracle_20261013 as native
        native.BASE = destination / 'native'
        native.BASE.mkdir()

        def native_action():
            with contextlib.redirect_stdout(io.StringIO()):
                native.main()
            return json.loads((native.BASE / 'oracle-results.json').read_text())
        perform('native-arithmetic', OLD / 'grf-cxx/oracle-results.json', ['run_grf_boundary_oracle_20261013'], native_action)
        import temporal_graph_oracles_20261013 as temporal
        import review_temporal_graph_oracles_20261013 as reviewer
        temporal.BASE = reviewer.BASE = destination / 'temporal'

        def temporal_action():
            with contextlib.redirect_stdout(io.StringIO()):
                temporal.main()
                reviewer.main()
            return json.loads((temporal.BASE / 'oracle-results.json').read_text())
        perform('temporal-arithmetic', OLD / 'temporal-graphs/oracle-results.json',
                ['temporal_graph_oracles_20261013', 'review_temporal_graph_oracles_20261013'], temporal_action)
    return 0 if records and all(r['status'] == 'pass' for r in records) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('group', choices=['foundation', 'exact', 'native-temporal'])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.group, args.output.resolve()))
