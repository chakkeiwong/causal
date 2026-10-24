#!/usr/bin/env python3
"""Adversarial change/invalidation checks for the explicit digest wrapper."""
import hashlib,json,os,tempfile
from pathlib import Path
from verified_digest_runtime_20261025 import StableDigest

def main():
    tests=[]
    with tempfile.TemporaryDirectory(prefix='causal-digest-test-') as folder:
        root=Path(folder);p=root/'evidence';p.write_bytes(b'alpha');cache=StableDigest(root)
        expected=hashlib.sha256(b'alpha').hexdigest();assert cache(p)==expected and cache.hashes==1
        assert cache(p)==expected and cache.hits==1;tests.append('First full-byte hash and unchanged hit')
        old=p.stat();p.write_bytes(b'bravo');os.utime(p,ns=(old.st_atime_ns,old.st_mtime_ns));assert cache(p)==hashlib.sha256(b'bravo').hexdigest() and cache.hashes==2;tests.append('Same-size edit with restored mtime invalidates through ctime')
        q=root/'replacement';q.write_bytes(b'gamma');q.replace(p);assert cache(p)==hashlib.sha256(b'gamma').hexdigest();tests.append('Atomic inode replacement invalidates')
        p.unlink()
        try:cache(p)
        except FileNotFoundError:tests.append('Deletion is rejected')
        else:raise AssertionError('Deleted file accepted')
        a=root/'a';b=root/'b';a.write_bytes(b'one');b.write_bytes(b'two');p.symlink_to(a);x=cache(p);p.unlink();p.symlink_to(b);assert cache(p)!=x;tests.append('Symlink retarget invalidates')
        state=root/'docs/program/state.json';state.parent.mkdir(parents=True);state.write_bytes(b'{}');before=cache.hashes;cache(state);cache(state);assert cache.hashes==before+2;tests.append('Canonical state never cached')
        victim=root/'victim';victim.write_bytes(b'old');changing=StableDigest(root)
        def mutate(stream):
            value=hashlib.file_digest(stream,'sha256').hexdigest();victim.write_bytes(b'new');return value
        changing.digest=mutate
        try:changing(victim)
        except ValueError:tests.append('Mutation during hash rejected')
        else:raise AssertionError('Changed file accepted')
        fresh=StableDigest(root);fresh(a);assert fresh.hashes==1 and not fresh.hits;tests.append('Fresh instance begins untrusted')
    print(json.dumps(dict(status='pass',tests=tests,scope='Ordinary local filesystem metadata; no hostile privileged-filesystem guarantee'),indent=2))
if __name__=='__main__':main()
