# Exact-result serialization repair

Reader preparation stopped before creating its output directory because the
original calculator represents binary potential-outcome pairs as Python
tuples, while the reviewed JSON represents the same pairs as arrays. Every
numeric value and every other field matched. Full JSON round-trip comparison
confirmed equality.

The original calculator, exact-results JSON, source review and failed
reader-prepare.log are retained unchanged. The v2 calculator wraps the
original in a JSON round trip so in-memory comparisons use the same domain
as stored evidence. This changes representation only, not mathematics,
examples, claims or source identity. The builder binds this successor.
