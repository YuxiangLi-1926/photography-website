"""Compare every public R2 image with its local migration export."""
import concurrent.futures
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = sys.argv[1].rstrip('/')
if not base.startswith('https://'):
    raise ValueError('An HTTPS public media base URL is required')
photos = json.loads((ROOT / 'src/data/importedPhotos.json').read_text(encoding='utf-8'))
projects = json.loads((ROOT / 'src/data/projects.json').read_text(encoding='utf-8'))
keys = list(dict.fromkeys([p['key'] for p in photos] + [p['coverKey'] for p in projects]))


def verify(key):
    expected = hashlib.sha256((ROOT / 'public/media' / key).read_bytes()).digest()
    for attempt in range(3):
        try:
            request = urllib.request.Request(base + '/' + key, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=60) as response:
                assert response.status == 200, key
                assert response.headers.get_content_type() == 'image/jpeg', key
                actual = hashlib.sha256(response.read()).digest()
            assert actual == expected, 'Content mismatch: ' + key
            return key
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for index, key in enumerate(pool.map(verify, keys), 1):
        if index % 30 == 0:
            print(f'Verified {index}/{len(keys)} public images', flush=True)
print(f'PASS: {len(keys)} public R2 images returned HTTP 200, JPEG content type and matching SHA-256 hashes.')
