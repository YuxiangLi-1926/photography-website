"""Package the static build for Pages; photography is served from R2."""
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
build = ROOT / 'dist'
assert (build / 'index.html').is_file(), 'Run npm run build first'
assert '.r2.dev/' in (build / 'index.html').read_text(encoding='utf-8'), 'Build must use R2 image URLs'
(ROOT / 'output').mkdir(exist_ok=True)
destination = Path(tempfile.mkdtemp(prefix='pages-release-', dir=ROOT / 'output'))
files = 0
for source in build.rglob('*'):
    relative = source.relative_to(build)
    if not source.is_file() or relative.parts[0] == 'media':
        continue
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    files += 1
print(json.dumps({'directory': str(destination), 'files': files}))
