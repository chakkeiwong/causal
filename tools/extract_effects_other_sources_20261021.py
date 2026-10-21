#!/usr/bin/env python3
"""Extract only bounded inert source text from authenticated archives; no execution."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
from publish_latent_r_review_v2_20261013 import ref,write
from acquire_effects_other_sources_20261021 import REVISIONS

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/program/execution/2026-10-21/effects-other-v1'


def main():
    assert not (BASE/'archive-inspection.json').exists()
    records=[]
    for name,repo,commit in REVISIONS:
        archive=BASE/'acquisition/sources-network'/(name+'.tgz')
        receipt=archive.with_suffix('.receipt.json');attempt=json.loads(receipt.read_text())
        if attempt['returncode']!=0:
            records.append(dict(name=name,status='acquisition_failed',receipt=ref(receipt,'Preserved failure')));continue
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==attempt['sha256']
        output=BASE/'sources'/name;output.mkdir(parents=True,exist_ok=False)
        files=[];skipped=[];total=0
        with tarfile.open(archive,'r:gz') as tar:
            for member in tar:
                path=PurePosixPath(member.name)
                assert not path.is_absolute() and '..' not in path.parts
                assert path.parts[0].endswith(commit),path.parts[0]
                if not member.isfile():
                    if not member.isdir():skipped.append(dict(path=str(path),reason='Nonregular member not extracted'))
                    continue
                total+=member.size;assert total<=64*1024*1024
                if path.suffix.lower() not in ['.jl','.toml','.md','.rst','.txt','.yml','.yaml'] and path.name.lower() not in ['license','copying','notice']:
                    skipped.append(dict(path=str(path),reason='Not selected inert source text'));continue
                assert member.size<=2*1024*1024
                raw=tar.extractfile(member).read();raw.decode('utf-8')
                target=output/Path(*path.parts[1:]);target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as stream:stream.write(raw)
                files.append(dict(archive_member=str(path),bytes=len(raw),local_copy=ref(target,'Unmodified pinned source text')))
        records.append(dict(name=name,repo=repo,commit=commit,archive=ref(archive,'Pinned complete archive'),
            receipt=ref(receipt,'Bounded acquisition'),files=files,skipped=skipped,total_archive_member_bytes=total,
            status='inert_sources_extracted_not_qualified',code_executed=False))
        print(json.dumps(dict(name=name,files=len(files),skipped=len(skipped),bytes=total)))
    write(BASE/'archive-inspection.json',dict(records=records,code_executed=False,
        constraints='Reject absolute/traversing paths; skip nonregular and nontext members; bound total64MiB and individual text2MiB; retain original archive.'))


if __name__=='__main__':main()
