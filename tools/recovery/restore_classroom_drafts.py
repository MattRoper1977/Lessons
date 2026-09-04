#!/usr/bin/env python3
"""Restore the chat-transfer drafts to a new directory, checking every byte."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile

def restore(destination):
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'CLASSROOM_DRAFTS_20260905.json').read_text())
    raw = base64.b64decode((here/'CLASSROOM_DRAFTS_20260905.tar.gz.b64').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == manifest['gzipSha256'], 'Archive digest mismatch'
    destination = Path(destination).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Choose a new or empty directory; existing work is never overwritten')
    expected = {r['path']:r for r in manifest['files']}
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
        members = archive.getmembers()
        assert len(members) == len(expected) == manifest['fileCount']
        assert {m.name for m in members} == set(expected)
        for member in members:
            name = PurePosixPath(member.name)
            assert member.isfile() and not name.is_absolute() and '..' not in name.parts
            data = archive.extractfile(member).read()
            assert len(data) == expected[member.name]['bytes']
            assert hashlib.sha256(data).hexdigest() == expected[member.name]['sha256']
            file = destination/member.name
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(data)
    print(json.dumps({'restored':len(expected),'destination':str(destination),'verified':True}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--destination',required=True)
    restore(parser.parse_args().destination)
