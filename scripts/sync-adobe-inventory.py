"""Apply a complete read-only browser capture, preserving existing asset keys."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
capture = Path(sys.argv[1])
load = lambda path: json.loads(path.read_text(encoding='utf-8-sig'))
old = load(ROOT / 'docs/adobe-source.json')
photos = load(ROOT / 'src/data/importedPhotos.json')
catalog = {p['slug']: p for p in load(ROOT / 'src/data/projects.json')}
covers = load(capture / 'adobe-covers.json')
by_path = {p['sourcePath']: p for p in old}
updated, changes, upload_keys = [], [], []

for index, cover in enumerate(covers, 1):
    detail = load(capture / f'adobe-project-{index}.json')
    title, year = cover['title'].rsplit('\n', 1)
    assert detail['title'].strip() == title.strip(), f'Wrong capture for {title}'
    assert not detail['videos'], f'Video migration needs review: {title}'
    previous = by_path.get(cover['href'])
    slug = previous['slug'] if previous else re.sub('[^a-z0-9]+', '-', title.lower()).strip('-')
    assert slug, f'Cannot derive project URL: {title}'
    previous_photos = sorted([p for p in photos if p['project'] == slug], key=lambda p: p['order'])
    previous_images = previous['images'] if previous else []
    assert len(previous_images) == len(previous_photos), f'Old inventory mismatch: {slug}'
    known = {i['src']: p['key'] for i, p in zip(previous_images, previous_photos)}
    before = [i['src'] for i in previous_images]
    after = [i['src'] for i in detail['images']]
    assert len(set(after)) == len(after), f'Duplicate photo source: {slug}'
    for image in detail['images']:
        key = known.get(image['src'])
        if not key:
            key = f"adobe/{slug}/{hashlib.sha256(image['src'].encode()).hexdigest()[:20]}.jpg"
            upload_keys.append(key)
        image['key'] = key
    cover_changed = not previous or previous['coverUrl'] != cover['cover']
    cover_key = (f"adobe/{slug}/cover-{hashlib.sha256(cover['cover'].encode()).hexdigest()[:20]}.jpg"
                 if cover_changed else catalog[slug]['coverKey'])
    if cover_changed:
        upload_keys.append(cover_key)
    updated.append(dict(slug=slug, title=title, year=int(year),
                        category=previous['category'] if previous else 'my-work',
                        sourcePath=cover['href'], coverUrl=cover['cover'], coverKey=cover_key,
                        description=detail['text'].strip(), images=detail['images']))
    changes.append(dict(slug=slug, before=len(before), after=len(after),
                        added=sum(u not in before for u in after), removed=sum(u not in after for u in before),
                        reordered=[u for u in before if u in after] != [u for u in after if u in before],
                        coverChanged=cover_changed))

assert len({p['slug'] for p in updated}) == len(updated), 'Duplicate project URLs'
backup = ROOT / 'output/adobe-sync-before'
backup.mkdir(parents=True, exist_ok=True)
for path in ['docs/adobe-source.json', 'src/data/importedPhotos.json', 'src/data/projects.json']:
    (backup / Path(path).name).write_bytes((ROOT / path).read_bytes())
removed_projects = [p['slug'] for p in old if p['sourcePath'] not in {c['href'] for c in covers}]
report = dict(projects=changes, removedProjects=removed_projects, uploadKeys=upload_keys,
              beforePhotos=sum(len(p['images']) for p in old), afterPhotos=sum(len(p['images']) for p in updated))
(ROOT / 'docs/adobe-sync-latest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(ROOT / 'docs/adobe-source.json').write_text(json.dumps(updated, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
