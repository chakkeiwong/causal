"""Review and execute bounded, authored contract tests with durable receipts."""
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import public_attention_contract_v2_20261028 as fixture
from publish_latent_r_review_v2_20261013 import ref, write

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/public-attention-contract-v2'


def main():
    assert not BASE.exists(), 'Preserve execution evidence; use a successor on failure.'
    BASE.mkdir()
    code = ROOT / 'tools/public_attention_contract_v2_20261028.py'
    tests = ROOT / 'tests/test_public_attention_contract_v2_20261028.py'
    original = ROOT / 'tools/public_attention_contract_fixture_20261028.py'
    inputs = [ref(original, 'Observed truth-bearing case objects, partial split overlap and None-only filter'),
              ref(code, 'Proposal-owned stricter contract successor'),
              ref(tests, 'Adversarial, exact-outcome contract tests'),
              ref(Path(__file__), 'Bounded execution and actual exit recording')]
    write(BASE / 'plan-review.json', dict(
        status='pass_for_bounded_authored_fixture', evidence=inputs,
        problem='The previous selected examples do not enforce all split identities or finite denominators.',
        actions=['Preserve the original implementation and its historical receipts.',
                 'Use immutable truth-free identities and one fingerprinted three-split registry.',
                 'Reject repeated case, graph-instance and data identities across or within splits.',
                 'Restrict selection inputs to exact validation identities and declare deterministic ties.',
                 'Retain missing/nonfinite requests, report finite availability and conditional means.',
                 'Exercise adversarial overlap, truth access, scoring-universe and invalid-input cases.'],
        review_findings=['Case identity is not authenticated scientific truth.',
                         'The local trusted-call API does not enforce process-level information isolation.',
                         'Dataset digest and graph identity declarations are caller supplied; no empirical model is qualified.',
                         'Partial-valid performance is conditional; total request and failure counts are mandatory.',
                         'Exact empty/empty F1 and threshold tie conventions are declared before the fixture runs.'],
        acceptance=['Every adversarial contract test passes with actual process exit zero.',
                    'The exact example retains two evaluation requests, one failure and availability one half.',
                    'None, NaN and both infinities yield unavailable when no finite value remains.'],
        awards_acceptance=False, native_execution=False))
    command = [sys.executable, '-m', 'pytest', '-q', str(tests.relative_to(ROOT)),
               '--junitxml=' + str(BASE / 'pytest-results.xml')]
    with (BASE / 'pytest.log').open('x') as out:
        result = subprocess.run(command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, timeout=90)
    write(BASE / 'test-exit.json', dict(command=command, actual_exit_code=result.returncode,
                                       evidence=[ref(BASE / 'pytest.log', 'Actual test output')]))
    if result.returncode:
        print(json.dumps(dict(status='failed',actual_exit_code=result.returncode,
                              log=str((BASE / 'pytest.log').relative_to(ROOT)))))
        raise SystemExit(result.returncode)
    suites = ET.parse(BASE / 'pytest-results.xml').getroot().findall('testsuite')
    totals = {key: sum(int(s.get(key, 0)) for s in suites)
              for key in ('tests', 'failures', 'errors', 'skipped')}
    assert totals['tests'] >= 50 and not any(totals[k] for k in ('failures', 'errors', 'skipped'))
    example = fixture.json_safe(fixture.example())
    assert example['evaluation']['macro_f1']['requested'] == 2
    assert example['evaluation']['macro_f1']['valid'] == 1
    assert example['evaluation']['macro_f1']['availability'] == '1/2'
    assert example['all_invalid']['valid'] == 0 and example['all_invalid']['value'] is None
    # Forbid nonstandard JSON numbers in persisted evidence.
    json.dumps(example, allow_nan=False)
    write(BASE / 'exact-example.json', example)
    write(BASE / 'author-review.json', dict(
        status='pass_for_declared_fixture_only', actual_exit_code=result.returncode,
        tests=totals, evidence=inputs + [ref(BASE / n, 'Performed exact/adversarial checks')
                                       for n in ('plan-review.json', 'test-exit.json', 'pytest-results.xml', 'exact-example.json')],
        findings=['Every split pair and repeated evaluation identity is tested.',
                  'Held-out truth cannot be supplied through the validation-truth parameter.',
                  'Candidate ties are invariant to insertion order.',
                  'Missing and nonfinite outcomes remain in the request denominator.',
                  'The source-derived temporal and threshold witnesses remain separate historical evidence.'],
        limitations=['Trusted local interfaces, not an adversarial information-flow sandbox.',
                     'No native external runtime, bank data, calibration, complete coverage or proposal acceptance.'],
        awards_acceptance=False, native_execution=False, final_acceptance=False))
    print(json.dumps(dict(status='pass_for_declared_fixture_only', tests=totals,
                          actual_exit_code=result.returncode, native_execution=False)))


if __name__ == '__main__':
    main()
