## Encoding algorithm settings without changing the shared schema

The existing discovery request schema permits only an algorithm identifier and
algorithm version in its parameter object. The proposed Java profile therefore
places the detailed settings in a separate immutable configuration artifact.
The request supplies its opaque handle, hash, media type, schema version and
role, alongside the data artifact. Resolving that artifact recovers the test
level, conditioning depth, missingness policy, numerical controls and
background-knowledge choice. The full request identity includes its hash, so
changing a setting creates a different request even when the downstream
scientific context remains identical. This preserves compatibility with the
shared schema while retaining the scientifically relevant settings.
\citep{exec13_java_adapter_contract}

The adapter's admission check must require exactly one configuration artifact
of the reviewed version, verify its bytes and recognized fields, and check
that the declared algorithm version admits that profile. Generic schema
validation alone cannot establish those conditions. The worked wire records
separately represent an unavailable runtime, an unsupported sampling regime,
a failed invocation and a graph response from an independent population
reference. Their data fixture is deterministic, and their graph is not a
fitted result. These records make the proposed response contract concrete
without treating a valid message as evidence of an executed engine.
\label{exec13:java-wire-end}
