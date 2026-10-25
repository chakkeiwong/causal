#!/usr/bin/env python3
"""Run one local program with process-only SHA reuse for unchanged file identities.

The first encounter reads every byte. Every reuse rechecks device,inode,size,
mtime and ctime. Changes during a read fail closed. Nothing is persisted and
the historical controllers remain unchanged. This assumes the ordinary local
filesystem threat model; it does not protect against a privileged actor forging
filesystem metadata. Final publication checks still use unmodified controllers.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]

class VerifiedHashCache:
    def __init__(self):
        self.cache={}
        self.calls=0
        self.reads=0
        self.bytes_read=0

    @staticmethod
    def identity(stat):
        return (stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns)

    def sha(self,path):
        path=Path(path)
        self.calls+=1
        before=self.identity(path.stat())
        key=(str(path.absolute()),before)
        if key in self.cache:
            return self.cache[key]
        with path.open('rb') as stream:
            opened=self.identity(os.fstat(stream.fileno()))
            if opened!=before:raise RuntimeError('File changed before hashing: '+str(path))
            digest=hashlib.file_digest(stream,'sha256').hexdigest()
            after=self.identity(os.fstat(stream.fileno()))
        if opened!=after or self.identity(path.stat())!=after:
            raise RuntimeError('File changed while hashing: '+str(path))
        self.reads+=1
        self.bytes_read+=after[2]
        self.cache[key]=digest
        return digest

    def summary(self):
        return dict(calls=self.calls,full_byte_reads=self.reads,reuses=self.calls-self.reads,bytes_read=self.bytes_read,persistent_cache=False)

def selftest():
    cache=VerifiedHashCache()
    with tempfile.TemporaryDirectory(prefix='causal-hash-cache-') as directory:
        p=Path(directory)/'evidence';p.write_bytes(b'one')
        initial=p.stat();one=cache.sha(p);assert one==hashlib.sha256(b'one').hexdigest()
        assert cache.sha(p)==one and cache.reads==1
        time.sleep(.01);p.write_bytes(b'two');os.utime(p,ns=(initial.st_atime_ns,initial.st_mtime_ns))
        assert cache.sha(p)==hashlib.sha256(b'two').hexdigest() and cache.reads==2
        q=Path(directory)/'replacement';q.write_bytes(b'one');q.replace(p)
        assert cache.sha(p)==one and cache.reads==3
        p.unlink()
        try:cache.sha(p)
        except FileNotFoundError:pass
        else:raise AssertionError('Deleted evidence must fail')
    return dict(status='pass',tests=['First call hashes bytes','Unchanged repeated binding reuses digest','Same-size write with restored mtime invalidates through ctime','Atomic replacement invalidates through inode','Deleted evidence fails'],**cache.summary())

def main():
    if sys.argv[1:]==['--self-test']:
        print(json.dumps(selftest()));return
    if len(sys.argv)<2:raise SystemExit('Expected repository-local Python script')
    target=Path(sys.argv[1]).resolve()
    if not target.is_relative_to(ROOT/'tools') or target.suffix!='.py':
        raise SystemExit('Only repository-local tools are accepted')
    import master_control as core
    import build_integrated_monograph_v12 as shared
    cache=VerifiedHashCache();core.sha=cache.sha;shared.sha=cache.sha
    sys.argv=[str(target),*sys.argv[2:]]
    started=time.monotonic()
    try:runpy.run_path(str(target),run_name='__main__')
    finally:print(json.dumps(dict(hash_verification=cache.summary(),elapsed_seconds=round(time.monotonic()-started,3))),file=sys.stderr)

if __name__=='__main__':main()
