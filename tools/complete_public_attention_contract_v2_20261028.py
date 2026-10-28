"""Finish evidence review after the test-count expectation failed; no test rerun."""
import ast
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import public_attention_contract_v2_20261028 as fixture
from execute_public_attention_contract_v2_20261028 import ROOT, BASE
from publish_latent_r_review_v2_20261013 import ref, verify_bindings, write


def main():
    assert not (BASE / 'author-review.json').exists()
    plan = json.loads((BASE / 'plan-review.json').read_text())
    verify_bindings(plan)
    result = json.loads((BASE / 'test-exit.json').read_text())
    verify_bindings(result)
    assert result['actual_exit_code'] == 0
    tree = ET.parse(BASE / 'pytest-results.xml')
    suites = tree.getroot().findall('testsuite')
    totals = {key: sum(int(s.get(key, 0)) for s in suites)
              for key in ('tests', 'failures', 'errors', 'skipped')}
    cases = tree.findall('.//testcase')
    declared = {node.name for node in ast.parse((ROOT / 'tests/test_public_attention_contract_v2_20261028.py').read_text()).body
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
    performed = {case.get('name').split('[', 1)[0] for case in cases}
    assert declared == performed and totals['tests'] == len(cases) == 48
    assert not any(totals[k] for k in ('failures', 'errors', 'skipped'))
    write(BASE / 'harness-failure.json', dict(
        status='preserved_and_repaired', actual_harness_exit_code=1,
        actual_pytest_exit_code=0, tests=totals,
        cause='The wrapper assumed at least 50 tests, but the declared suite contains 48 passing parameterized cases.',
        repair='Validate every declared test function against actual JUnit cases; preserve the passing execution without rerunning.',
        evidence=[ref(ROOT / 'tools/execute_public_attention_contract_v2_20261028.py', 'Failed count assertion preserved'),
                  ref(BASE / 'test-exit.json', 'Actual successful test exit'),
                  ref(BASE / 'pytest-results.xml', 'Actual 48-case execution'),
                  ref(Path(__file__), 'Sequential evidence-review repair')]))
    example = fixture.json_safe(fixture.example())
    metric = example['evaluation']['macro_f1']
    assert (metric['requested'], metric['valid'], metric['availability']) == (2, 1, '1/2')
    assert example['all_invalid']['valid'] == 0 and example['all_invalid']['value'] is None
    json.dumps(example, allow_nan=False)
    write(BASE / 'exact-example.json', example)
    write(BASE / 'author-review.json', dict(
        status='pass_for_declared_fixture_only', actual_exit_code=0, tests=totals,
        declared_test_functions=sorted(declared),
        evidence=plan['evidence'] + [ref(BASE / n, 'Performed exact/adversarial checks') for n in
                                    ('plan-review.json', 'test-exit.json', 'pytest-results.xml', 'harness-failure.json', 'exact-example.json')],
        findings=['All 48 declared adversarial cases passed, with no failure, error or skip.',
                  'All split-pair duplicates and repeated evaluation identities are rejected.',
                  'Held-out truth is rejected by the validation-truth interface.',
                  'Ties are invariant to candidate insertion order.',
                  'Missing/nonfinite results remain in request counts and partial-valid averages are explicitly conditional.'],
        limitations=['Trusted local interfaces, not a process-level information-flow sandbox or authentic-label verification.',
                     'No external model, empirical calibration, native package or bank data.',
                     'This successor does not retroactively strengthen the original fixture or close broad proposal obligations.'],
        awards_acceptance=False, native_execution=False, final_acceptance=False))
    print(json.dumps(dict(status='pass_for_declared_fixture_only', tests=totals,
                          tests_rerun=False, harness_failure_preserved=True)))


if __name__ == '__main__':
    main()
