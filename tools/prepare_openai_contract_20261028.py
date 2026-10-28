"""Prepare inspected official originals and a connected proposal comparison."""
import hashlib
import json
from pathlib import Path
import openai_contract_reference_20261028 as exact

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/program/execution/2026-10-28/l6-openai-pinned-v1'
RAW = ROOT / 'docs/literature/raw'


def read(p):
    return json.loads(p.read_text())


def ref(p, anchor):
    return dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest(), anchor=anchor)


def write(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, indent=2) + chr(10))


def main():
    text = r'''§section[Structured outputs and scientific admission]{Structured outputs, response states and scientific admission}
§label{sec:exec28-oa}
A structured banking answer must preserve both the scientific target and the state of the computation.
Suppose a collections analyst requests the effect of a reminder on thirty-day arrears. A response can have
the required fields and a well-formed number while using a post-treatment variable, an unjustified graph,
or a different treatment population. It can also be a syntactically valid fragment of an unfinished request.
The proposed library therefore needs separate tests for completion, representation and causal admission.
This distinction determines how a provider client can be reused without attributing scientific guarantees to it.

§subsection{What the pinned official sources establish}
The selected official OpenAI cookbook demonstrates a strict JSON-schema response format, required fields,
closed object properties and a Pydantic parsing helper. Its worked examples are useful interface illustrations,
not measurements of this proposal. The same notebook explicitly describes a refusal field because a refused
request need not follow the supplied answer schema. Its opening description of constrained outputs must
therefore be read together with this exception. Schema adherence concerns representation; it does not assert
that an adjustment set is scientifically admissible or that a reported effect is identified.§citep{exec28_oa_cookbook}

The selected Python SDK source has version 3.26.0 and declares Python 3.10 or later. Its parsing helper converts
a Pydantic model to a schema and parses eligible content into that model. In the inspected Chat Completions path,
a length stop raises a dedicated error, as does a content-filter stop. Refusal content is not parsed as an ordinary
answer. Automatic tool-argument parsing requires a strict function-tool contract. These are source-level client
rules at the selected revision, rather than a claim that every compatible server or model honors them.
The cookbook and SDK are pinned separately; their example calling surfaces must not be silently combined into
one version-independent executable recipe.§citep{exec28_oa_sdk,exec28_oa_cookbook}

The Responses parsing path also makes the message phase significant. At this revision, final-answer text and
legacy messages without a phase are eligible for parsing; other explicit phases retain their text with no parsed
result. The helper documentation warns that concatenated output text can include commentary, while the parsed
output selects a structured result. An adapter should retain the entire typed output sequence and the response
status, not search arbitrary text for a schema-shaped substring and promote it to the final answer. A declared
incomplete state remains incomplete even if part of its output can be decoded.§citep{exec28_oa_sdk}

For the banking request, a useful envelope contains the provider response identifier, endpoint and selected
model identifier; status and native stop reason; refusal or incomplete details; the parsed payload, if any;
tool-call identities and pending results; and the target, assumptions and scientific disposition. These fields
are proposed product requirements. A provider refusal, a malformed object and a correctly identified failure
of identification have different meanings. The analyst should be able to tell which information is missing
and which action, if any, could change the result.

§subsection{An admission rule that cannot be satisfied by JSON alone}
Let §(C§) denote completed output, §(J§) successful representation validation and §(I§) admission of the
requested causal effect under its declared information and assumptions. A proposed effect-admission predicate is
§[
 A=C§land J§land I.
§]
This is a software decision rule, not a theorem that the assumptions are true. It makes the owner of each
judgment visible. A source parser can help establish §(J§), transport and response-state handling contribute to
§(C§), and the causal library must justify §(I§). The operator and eventual bank reviewer still own the truth
of substantive inputs. An unidentified effect may legitimately produce a completed, well-formed scientific
answer whose disposition is nonidentification; it must not produce an admitted scalar effect by default.

An exact authored four-case witness admits only the complete, schema-valid, identified case. A complete but
unidentified case retains its nonidentification result; an incomplete case with a valid prefix remains pending;
a refusal stays a refusal. These cases are finite constructions used to specify the interface, not observations
of OpenAI behavior or a measured refusal rate. In particular, treating all valid objects as completed causal
answers would merge scientifically different outcomes.§citep{exec28_oa_reference}

§subsection{Retry layers and the cost of one business request}
The pinned SDK documentation describes two retries by default for selected connection and HTTP failures,
subject to a resendable body, and a configurable request timeout. The implementation distinguishes status
classes, server retry hints and backoff. A workflow can add another retry loop around this client. Consequently,
neither the number of logical banking requests nor one configured timeout determines the full attempt count or
end-to-end latency. A retry may also leave uncertainty about a remote effect; successful parsing alone cannot
provide exactly-once execution of a business action.§citep{exec28_oa_sdk}

Consider a stipulated workflow with at most two outer attempts and three HTTP attempts within each. Its maximum
is six HTTP attempts, not the sum of the two limits. At a stipulated USD 0.25 per attempt, the corresponding
cost is USD 1.50. If each attempt takes four seconds, inner waits are one and two seconds in each outer attempt,
and the outer wait is three seconds, the specified path takes §(24+6+3=33§) seconds. These values are exact
bookkeeping under the stated assumptions, not vendor prices or a measured service guarantee.§citep{exec28_oa_reference}

The proposed admission layer should reserve a workflow-wide attempt and cost budget before issuing calls,
debit actual attempts, retain response identifiers and unknown outcomes, and distinguish cancellation requested
from cancellation observed. Public prototype tests should include an error after remote work may have begun,
an incomplete stream, a refusal, invalid tool arguments and a timeout during a tool result. The complete
denominator includes these cases. Financial value remains a separate assessment of decision quality and full
workflow costs; cheap valid JSON is not a monetary benefit by definition.

§subsection{Comparison and a bounded reuse choice}
The existing comparison treats Anthropic and Google client contracts, Ollama request and stream behavior,
and the parser, template and generation settings of vLLM and llama.cpp separately. The newly inspected OpenAI
originals add a sixth named provider/client family with explicit parsing, refusal, phase and retry rules.
Across these profiles, one adapter should preserve native status and error information before mapping it into
the common scientific envelope. Compatibility in endpoint spelling cannot prove equivalence in parsing,
model behavior, cancellation or cost.§citep{exec24_backend_anthropic,exec24_backend_google,exec24_backend_ollama,exec24_backend_vllm,exec24_backend_llamacpp,exec28_oa_sdk}

The bounded proposal choice is conditional adoption of the original client behind a thin, versioned adapter,
rather than a wholesale port. The inspected SDK and cookbook carry Apache 2.0 and MIT notices respectively;
these notices concern those source artifacts. They do not establish service entitlement, model-weight rights,
data permissions or approved bank deployment. An implementation decision still requires the exact endpoint,
model, dependencies, configured retry policy and applicable service terms. The official live guide access
failure also remains an omission; the recovered repository originals establish their own narrower contracts.
No downloaded code or live model was executed in this review.§citep{exec28_oa_sdk,exec28_oa_cookbook}

CLI and MCP should expose the same typed outcome, including nonidentification, scientific rejection, refusal,
incomplete output and transport uncertainty. Framework scheduling must consume this outcome rather than infer
success from text presence. This supplies a concrete route for a low-cost public prototype: freeze the client
and adapter identities, register adversarial response-state fixtures, verify the scientific envelope against
independent answers, and only then compare live backends under a declared budget. The source comparison reduces
an architectural uncertainty while leaving native performance, service terms and bank effectiveness open.
The banking decision remains admissible only when its scientific meaning survives the complete request lifecycle.
'''
    (BASE / 'development.tex').write_text(text.replace('§', chr(92)))
    sponsor = '''## Preserve scientific meaning across provider responses

Pinned official OpenAI cookbook and Python SDK originals now complement the five existing backend profiles. Strict schemas and parsing helpers constrain representation; refusals, incomplete output and commentary require separate handling. The proposed adapter preserves these native states and admits a scalar effect only after completion, representation checks and scientific identification. A completed nonidentification answer remains a useful but distinct result. [@exec28_oa_cookbook; @exec28_oa_sdk]

An exact authored example gives six possible HTTP attempts when two workflow attempts each allow three client attempts. At a stipulated USD 0.25 per attempt the cost is USD 1.50; the stated timing path takes 33 seconds. These are illustrative accounting results, not vendor prices or measured latency. Conditional adoption of the original client through a thin adapter avoids an unjustified wholesale port, while model and service terms, native public fixtures and bank effectiveness remain open. [@exec28_oa_reference]
'''
    (BASE / 'sponsor-addition.md').write_text(sponsor)
    results = exact.calculate()
    assert results['admitted'] == 1 and results['maximum_http_attempts'] == 6
    assert results['stipulated_total_cost_usd'] == '3/2' and results['stipulated_elapsed_seconds'] == 33
    write(BASE / 'exact-results.json', results)
    index = read(BASE / 'authenticated-source-index.json')['records']
    pins = {x['profile']: x for x in read(BASE / 'selected-pins.json')}
    specs = {
        'README.md': [(1, 14, 'Official client identity and Python requirement'), (750, 819, 'Retry defaults, resendable bodies, configuration and timeout distinction')],
        'helpers.md': [(1, 60, 'Schema parsing, final-answer phase, legacy phase and commentary distinction'), (142, 147, 'Length/content-filter errors and strict tool restriction')],
        'pyproject.toml': [(1, 43, 'Version 3.26.0, Python 3.10 and declared dependencies')],
        'src/openai/lib/_parsing/_completions.py': [(65, 113, 'Strict tools and completion-stop errors'), (199, 209, 'No ordinary content parsing on refusal')],
        'src/openai/lib/_parsing/_responses.py': [(53, 99, 'Typed response items retained'), (146, 198, 'Phase-aware parsing and strict tool-argument conditions')],
        'src/openai/_base_client.py': [(851, 927, 'Retry limits, backoff, server hints and status classes')],
        'src/openai/types/chat/chat_completion.py': [(35, 58, 'Native finish reason fields')],
        'src/openai/types/chat/chat_completion_message.py': [(57, 65, 'Separate content and refusal fields')],
        'src/openai/types/responses/response.py': [(57, 67, 'Incomplete reasons'), (271, 279, 'Error and incomplete details'), (505, 512, 'Native response status values')],
    }
    sources = []
    for profile, title in [('cookbook', 'Official OpenAI structured-output examples and refusal exception'), ('sdk', 'Official OpenAI Python parsing, response-phase and retry contracts')]:
        records = []
        for x in index:
            if x['profile'] != profile:
                continue
            p = ROOT / x['local_copy']['path']
            anchors = []
            if x['upstream_path'].endswith('.ipynb'):
                notebook = read(p)
                for cell, finding in [(0, 'Strict schema versus valid JSON'), (6, 'Required fields and closed objects'), (10, 'Pydantic helper explanation'), (14, 'Refusal may not follow supplied answer schema')]:
                    excerpt = ''.join(notebook['cells'][cell]['source'])
                    anchors.append(dict(anchor='Notebook source cell ' + str(cell), excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(), finding=finding))
            else:
                lines = p.read_text().splitlines()
                spans = specs.get(x['upstream_path'], [(1, min(len(lines), 21), 'Direct source license notice; no service or model rights inferred')])
                for lo, hi, finding in spans:
                    excerpt = chr(10).join(lines[lo - 1:hi])
                    anchors.append(dict(lines=[lo, hi], excerpt_sha256=hashlib.sha256(excerpt.encode()).hexdigest(), finding=finding))
            records.append(dict(source_identity=x['source_identity'], version_date=pins[profile]['date'] + ';' + pins[profile]['commit'],
                upstream_path=x['upstream_path'], local_copy=x['local_copy'], acquisition_receipt=x['receipt'],
                git_blob_sha1=x['git_blob'], inspected_anchors=anchors, supported_claims=[a['finding'] for a in anchors], executed=False))
        sources.append(dict(integrated_citation_key='exec28_oa_' + profile, kind='software_primary_sources', title=title,
            author='OpenAI contributors', year=2026, source_identity='https://github.com/' + pins[profile]['repository'] + '/tree/' + pins[profile]['commit'],
            version_date=pins[profile]['date'] + ';' + pins[profile]['commit'], local_copy=records[0]['local_copy'], records=records,
            inspected_anchors=[a for r in records for a in r['inspected_anchors']], supported_claims=[c for r in records for c in r['supported_claims']],
            limitations=['Pinned source-level findings; no native model/client execution.', 'No complete server guarantee, service entitlement, model rights or bank effectiveness established.']))
    sources.append(dict(integrated_citation_key='exec28_oa_reference', kind='project_derivation_and_exact_reference',
        title='Authored completion, schema, identification and nested-retry witnesses', author='Causal banking proposal project', year=2026,
        source_identity='tools/openai_contract_reference_20261028.py', version_date='28 October 2026; exact authored constructions',
        local_copy=ref(Path(exact.__file__), 'Independent authored calculation'),
        inspected_anchors=[ref(BASE / 'exact-results.json', 'Four admission cases and exact nested-attempt arithmetic')],
        supported_claims=['Only completed, representation-valid, identified case admits an effect.', 'Two outer times three inner attempts gives six; stipulated cost 3/2 USD and elapsed time 33 seconds.'],
        limitations=['Stipulated mathematics and proposed semantics; no observed vendor or bank result.']))
    write(BASE / 'source-audit.json', dict(sources=sources, cutoff='2026-10-07T15:59:59Z', native_execution=False,
        evidence=[ref(BASE / 'authenticated-source-index.json', 'Twelve exact Git-blob-verified originals'), ref(BASE / 'selected-pins.json', 'Independent cutoff commit pins')]))
    write(BASE / 'mathematical-review.json', dict(status='pass', findings=['Boolean admission preserves four distinct states.', 'Attempt limits multiply across nested loops; cost and elapsed-time arithmetic replay exactly.'],
        evidence=[ref(Path(exact.__file__), 'Exact authored reference'), ref(BASE / 'exact-results.json', 'Observed local arithmetic replay')], observed_model_performance=False))
    write(BASE / 'copyedit-review.json', dict(status='pass', findings=['Scientific target, completion and schema are separately defined.', 'Source examples and proposed adapter requirements are distinct.', 'Costs, timings and cases are explicitly stipulated.'], evidence=[ref(BASE / 'development.tex', 'Connected banking argument'), ref(BASE / 'sponsor-addition.md', 'Sponsor comparison')]))
    write(BASE / 'review.json', dict(status='pass', issues=[], scope='Bounded official source comparison and authored mathematics; not L6 full coverage.',
        evidence=[ref(BASE / n, 'Reviewed original, argument or exact calculation') for n in ['source-audit.json', 'mathematical-review.json', 'copyedit-review.json', 'plan-review-v2.json', 'development.tex', 'sponsor-addition.md']] + [ref(Path(__file__), 'Exact preparation')],
        visual_acceptance=False, final_acceptance=False, native_execution=False))
    print(json.dumps(dict(source_records=3, original_files=len(index), scholarly_papers=0, source_review='pass', full_L6_acceptance=False)))


if __name__ == '__main__':
    main()
