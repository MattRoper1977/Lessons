#!/usr/bin/env python3
"""Regenerate the exact RSH-3 pack checksum entry sets."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PACKS={
 'Science_Teesside/Grow/Autumn2_W7_2026-27':'SHA256SUMS.txt',
 'LAUNCH_ASDAN/W13-W14_2026-27':'SHA256SUMS.txt',
 'Science_Teesside/Launch/W14-W15_2026-27':'SHA256SUMS.txt',
}
for rel,name in PACKS.items():
 pack=ROOT/rel;files=sorted(list(pack.rglob('*.html'))+[pack/'manifest.json'],key=lambda p:str(p.relative_to(pack)))
 text=''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(pack)}\n' for path in files)
 (pack/name).write_text(text,encoding='ascii');print(rel,name,len(files))
