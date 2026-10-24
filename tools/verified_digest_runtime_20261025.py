#!/usr/bin/env python3
"""Explicit process-local SHA-256 reuse for stable files; canonical state bypasses it."""
import hashlib,json,os,runpy,stat,sys,time
from pathlib import Path

class StableDigest:
    def __init__(self,root):
        self.root=Path(root).resolve();self.cache={};self.hits=0;self.hashes=0;self.bytes=0
        self.canonical=self.root/'docs/program/state.json'
    @staticmethod
    def identity(s):
        return s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns
    @staticmethod
    def digest(stream):return hashlib.file_digest(stream,'sha256').hexdigest()
    def __call__(self,path):
        path=Path(path).absolute()
        with path.open('rb') as stream:
            before=os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):raise ValueError('Digest requires a regular file: '+str(path))
            identity=self.identity(before)
            if self.identity(path.stat())!=identity:raise ValueError('File replaced before digest: '+str(path))
            key=(str(path),identity)
            cacheable=path.resolve()!=self.canonical
            cached=self.cache.get(key) if cacheable else None
            if cached is None:
                digest=self.digest(stream);self.hashes+=1;self.bytes+=before.st_size
            else:
                digest=cached;self.hits+=1
            if self.identity(os.fstat(stream.fileno()))!=identity or self.identity(path.stat())!=identity:
                raise ValueError('File changed while verifying digest: '+str(path))
            if cacheable and cached is None:self.cache[key]=digest
            return digest
    def statistics(self):return dict(full_byte_hashes=self.hashes,stable_file_hits=self.hits,bytes_hashed=self.bytes,persistent_cache=False,canonical_state_cached=False)

def main():
    if len(sys.argv)<2:raise SystemExit('usage: verified_digest_runtime_20261025.py tools/TARGET.py [args]')
    root=Path(__file__).resolve().parents[1];target=(root/sys.argv[1]).resolve()
    if target.parent!=root/'tools' or target.suffix!='.py' or target==Path(__file__).resolve():raise SystemExit('Target must be one repository tools Python script.')
    if not target.is_file():raise SystemExit('Target does not exist.')
    cache=StableDigest(root)
    import master_control as core
    import build_integrated_monograph_v12 as shared
    core.sha=cache;shared.sha=cache
    sys.argv=[str(target),*sys.argv[2:]];started=time.monotonic()
    try:runpy.run_path(str(target),run_name='__main__')
    finally:print(json.dumps(dict(digest_runtime=cache.statistics(),elapsed_seconds=round(time.monotonic()-started,3))),file=sys.stderr,flush=True)
if __name__=='__main__':main()
