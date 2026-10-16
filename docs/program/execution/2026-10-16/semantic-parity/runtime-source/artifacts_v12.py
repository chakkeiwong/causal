"""Local content-addressed JSON artifacts for one explicitly configured operator."""
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

from .operation_contract_v12 import finite_json, validate_artifact_ref

ROOT = Path(__file__).resolve().parents[2]
MAX_ARTIFACT = 8 * 1024 * 1024


def encode(value):
    finite_json(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def local_root(path):
    """Runtime roots are operator configuration, confined to this repo's .runtime."""
    path = Path(path).absolute()
    permitted = ROOT / ".runtime"
    if path != path.resolve() or not path.is_relative_to(permitted):
        raise ValueError("Runtime root must be a nonsymlink path inside causal/.runtime")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def atomic(path, value):
    if path.is_symlink() or path.parent != path.parent.resolve():
        raise ValueError("Symlink state path rejected")
    data = encode(value)
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def bounded_read(path, limit=MAX_ARTIFACT):
    if path.parent != path.parent.resolve():
        raise ValueError("Artifact directory symlink rejected")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError("Artifact is not a bounded regular file")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Artifact exceeds read budget")
    return data


class ArtifactStore:
    def __init__(self, root):
        self.root = local_root(root)
        self.folder = local_root(self.root / "artifacts")

    def put(self, value, schema_version, role, custody="local_operator"):
        data = encode(value)
        if len(data) > MAX_ARTIFACT:
            raise ValueError("Artifact exceeds store byte limit")
        descriptor = {"sha256": hashlib.sha256(data).hexdigest(),
                      "media_type": "application/json", "schema_version": schema_version,
                      "role": role, "bytes": len(data), "custody": custody}
        artifact_id = "a" + digest(descriptor)
        ref = {"artifact_id": artifact_id, **descriptor}
        # Byte and metadata publications are individually atomic and deterministic.
        content, metadata = self.folder / (artifact_id + ".json"), self.folder / (artifact_id + ".meta")
        if content.exists() or content.is_symlink():
            if bounded_read(content) != data:
                raise ValueError("Existing artifact identity has changed bytes")
        else:
            atomic(content, value)
        if metadata.exists() or metadata.is_symlink():
            if json.loads(bounded_read(metadata)) != ref:
                raise ValueError("Existing artifact identity has changed metadata")
        else:
            atomic(metadata, ref)
        return ref

    def reference(self, artifact_id):
        validate_artifact_ref({"artifact_id": artifact_id, "sha256": "0" * 64})
        return json.loads(bounded_read(self.folder / (artifact_id + ".meta"), 8192))

    def get(self, ref, limit=MAX_ARTIFACT):
        validate_artifact_ref(ref)
        recorded = self.reference(ref["artifact_id"])
        if ref != recorded:
            raise ValueError("Artifact metadata or custody mismatch")
        data = bounded_read(self.folder / (ref["artifact_id"] + ".json"), min(limit, MAX_ARTIFACT))
        if len(data) != ref["bytes"] or hashlib.sha256(data).hexdigest() != ref["sha256"]:
            raise ValueError("Artifact bytes changed from declared identity")
        value = json.loads(data)
        finite_json(value)
        return value

    def list_refs(self):
        return [self.reference(p.name[:-5]) for p in sorted(self.folder.glob("a*.meta"))]
