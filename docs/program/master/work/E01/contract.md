# E01 common result and recovery contract

Every journey emits `status`, set topology, assumptions, currency/units,
capability disposition, estimate and interval fields. `finite_interval`,
`finite_union`, `whole_line` and `unavailable` preserve refusal and
nonidentification semantics. A result with an interval is not automatically
qualified; the disposition remains attached.

The streamed linked implementation keeps at most the pilot fit plus one
bounded evaluation block of pseudo-outcomes. It retains chronological
covariance state and publishes requests atomically by immutable identity.
The dense implementation remains the fallback. Local crash recovery journals
completed request identities and never counts a replay as a new request.
