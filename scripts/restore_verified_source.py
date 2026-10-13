#!/usr/bin/env python3
"""Restore the five reviewed source files from a checksummed transport bundle.

The bundle contains only project-authored text and extracted numeric estimates,
not fonts, third-party article full text, credentials, or executable archives.
"""
from pathlib import Path
import base64
import hashlib
import json
import lzma

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = '76ac0a59d68f7204d253afda70ff9d7243ecd8035cc0432aa494b518693dc789'
ALLOWED = {
    'manuscript/seminar.fa.md',
    'scripts/build_seminar.py',
    'scripts/content_assets.py',
    'scripts/update_indexes.py',
    'research/data/effect_estimates.csv',
}
parts = [ROOT / f'.delivery/v2/source.{i:02d}.b64' for i in range(7)]
encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in parts)
if len(encoded) != 38908:
    raise ValueError(f'Incomplete source transport: {len(encoded)} characters')
compressed = base64.b64decode(encoded, validate=True)
actual_hash = hashlib.sha256(compressed).hexdigest()
if actual_hash != EXPECTED_SHA256:
    raise ValueError(f'Source checksum mismatch: {actual_hash}')
files = json.loads(lzma.decompress(compressed))
if set(files) != ALLOWED or not all(isinstance(v, str) for v in files.values()):
    raise ValueError('Unexpected source files or invalid contents')
report = {'transport_sha256': actual_hash, 'transport_verified': True, 'files': {}}
for name, text in files.items():
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    report['files'][name] = {'bytes': len(path.read_bytes()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
(ROOT / 'qa').mkdir(exist_ok=True)
(ROOT / 'qa/SOURCE_TRANSPORT_QA.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
