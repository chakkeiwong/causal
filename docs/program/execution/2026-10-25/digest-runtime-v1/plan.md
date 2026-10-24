# Reduce repeated evidence hashing without weakening content verification

The publication controller revalidates the growing immutable evidence graph on
many transitions, repeatedly hashing the same source bytes in one process.
Keep all historical controllers and their reviews unchanged. Add an explicit
invocation wrapper with a process-local digest cache, never a persistent cache.

Every first use hashes complete bytes. Cache keys include absolute path, device,
inode, mode, size, nanosecond mtime and ctime. Open and check the descriptor and
path before and after hashing/cache use; a changed object must raise. The live
canonical state always bypasses caching. A new process starts with no trusted
hashes. The mechanism assumes the same ordinary filesystem and non-adversarial
local execution model as the existing checks; it is not a hostile-filesystem
integrity mechanism.

Test changed same-size contents with restored mtime, atomic replacement,
deletion, symlink retargeting, canonical bypass, first-read byte hashing,
unchanged hits and mid-read mutation detection. Then compare full controller
check outcomes on the same state against the unwrapped checks. Record timing,
cache counters and the exact wrapper identity. Do not deploy the wrapper to a
canonical publication until these checks agree. Keep command output bounded.
