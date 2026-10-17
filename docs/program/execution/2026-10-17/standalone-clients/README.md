# Standalone causal-client examples

These bounded proposal demonstrations run inside the causal repository. A notebook-friendly Python function and reproducible batch script preserve the full canonical response. No sibling repository, live model provider, MCP client or bank workflow changes.

From the repository root, using the installed environment:

    PYTHONPATH=src:tools .runtime/in04/bin/python tools/standalone_client_examples_20261017.py --output docs/program/execution/2026-10-17/standalone-clients/run-1

Use a new output directory name for a repeat. Earlier evidence remains preserved. The script creates an isolated store under .runtime, makes three library and three CLI invocations, and checks their complete responses. Expected classifications are conditional_expression, scientific_unsupported and scientific_refused. None supplies a fitted monetary estimate.

For a notebook or ordinary Python caller:

    from standalone_client_examples_20261017 import decode
    admitted = decode(request, response_json_text)
    print(admitted['interpretation'])
    response = admitted['response']

Add tools and src to the Python import path. The request must satisfy the existing canonical request schema and semantic validator. The decoder admits one bounded JSON object, validates the response schema and relation to the request, and returns every response field. It never replaces a missing estimate with zero.

Four saved set responses additionally check finite, empty, whole-line and disconnected interpretation without rerunning estimation. Five deliberately invalid copies check duplicate keys, missing schema version, changed request identity, nonfinite tokens and trailing bytes. The report labels stored-fixture and adverse-copy checks separately from actual calls.

Remaining qualification includes a real notebook-kernel installation, plotting/export, parser nesting/resource limits, asynchronous artifact retrieval, exact MCP compatibility, custody and launch-environment testing. Platform and consumer owners assess their actual workflows after prototype merit is shown. I2 develops these boundaries; this directory supplies the runnable standalone requirement evidence.
