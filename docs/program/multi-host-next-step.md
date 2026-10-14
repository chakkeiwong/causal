# Runnable multi-host qualification protocol

This is deferred execution, not a measured distributed service. Use immutable
source partitions from `write_partitions`, retaining one ordered manifest with
hash, fold and global offsets per partition. Transfer only approved study data
to approved hosts; the local research run has not made that transfer.

1. On each approved host install the locked research environment and preserve
   package versions, numeric thread limits and source identities. Run the same
   `tools/closure_workloads.py --worker ...` cases on staged sources. Record the
   full stdout JSON, host, process timing, peak memory, storage and network bytes.
2. Use one designated coordinator for the global mean and committed prefix.
   Workers submit immutable, idempotent moment summaries keyed by source/procedure
   identity. The coordinator rejects duplicate identities with differing content.
3. Broadcast the fixed global mean and same-fold chronological halos for the
   second pass. Assign each core score to one worker; lag products belong to the
   later origin's core. No cross-fold pair is permitted. Never average separately
   centered partition covariance matrices as the global covariance.
4. Commit coordinator summaries transactionally using the platform's documented
   semantics. Local `os.replace` is not assumed to be a remote object-store
   transaction. Inject worker loss, network timeout, duplicate delivery, old
   checkpoint, corrupt content and coordinator restart before asserting recovery.
5. Compare one, two and four hosts over identical total work and sources, twice
   in separate runs, including loading, fitting, uncertainty, reports, serialization,
   network and recovery. Assert matching public results and tolerance-equivalent
   numerical summaries to the serial reference. Concurrent requests need another
   measured service-level arm; a single-request speedup is insufficient.

The protocol can reuse the selected sufficient-statistic calculation; it does
not distribute arbitrary nuisance learners or change sampling units. Stop and
record platform nonresolution if exactly-once summaries or immutable-source
access cannot be established. No bank infrastructure access, uploads or remote
execution have been performed in this workspace.
