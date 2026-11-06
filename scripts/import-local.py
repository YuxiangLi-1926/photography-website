"""Append curated local folders without changing originals or existing R2 keys."""
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
folder = Path(sys.argv[1]).resolve()
inventory_path = ROOT / 'docs/portfolio-source.json'
if not inventory_path.exists():
    inventory_path = ROOT / 'docs/adobe-source.json'
projects = json.loads(inventory_path.read_text(encoding='utf-8'))
mapping = {
    'Campaign': ('campaigns', 'Campaign', 'event'),
    'London': ('london', 'London', 'my-work'),
    'Portrait': ('portrait', 'Portrait', 'portrait'),
    'Grads': ('grads', 'Grads', 'portrait'),
    'Food in Love': ('food-in-love', 'Food in Love', 'food'),
    'Edi': ('edi', 'Edi', 'my-work'),
    'Night in London': ('night-in-london', 'Night in London', 'nightlife'),
    'The White Cliff': ('the-white-cliff', 'The White Cliff', 'my-work'),
}
tail = ['cars-campaign', 'jaguar', 'real-estate', 'the-white-cliff', 'edi', 'spain', 'switzerland', 'netherland', 'doggy-kitty']
catalog = {p['slug']: p for p in projects}
report, upload_keys = [], []


def natural_key(path):
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r'(\d+)', path.name)]


def signature(path):
    with Image.open(path) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        return image.width / image.height, image.resize((64, 64), Image.Resampling.LANCZOS)


for name, (slug, title, category) in mapping.items():
    files = sorted((folder / name).glob('*.jpg'), key=natural_key)
    assert files, f'No JPEG photos: {name}'
    project = catalog.get(slug)
    existing = project['images'] if project else []
    signatures = [(image['key'], signature(ROOT / 'public/media' / image['key'])) for image in existing]
    known_sources = {image['src'] for image in existing}
    additions, skipped = [], []
    for file in files:
        ratio, thumbnail = signature(file)
        duplicate = None
        for key, (old_ratio, old_thumbnail) in signatures:
            if abs(ratio / old_ratio - 1) < .002:
                rms = max(ImageStat.Stat(ImageChops.difference(thumbnail, old_thumbnail)).rms)
                if rms <= 1:
                    duplicate = key
                    break
        if duplicate or file.as_uri() in known_sources:
            skipped.append({'file': file.name, 'matches': duplicate})
            continue
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        key = f'portfolio/{slug}/{digest[:20]}.jpg'
        with Image.open(file) as image:
            raw_date = str(image.getexif().get_ifd(34665).get(36867, ''))
            year = int(raw_date[:4]) if re.match(r'^\d{4}:', raw_date) else None
        additions.append({'src': file.as_uri(), 'key': key, 'sourceName': file.name, 'sourceSha256': digest, 'year': year})
        upload_keys.append(key)
        signatures.append((key, (ratio, thumbnail)))
    if not project:
        assert additions, f'New project has no photos: {slug}'
        first = additions[0]
        project = dict(slug=slug, title=title, year=min(image['year'] for image in additions if image['year']),
                       category=category, description='', sourceKind='local',
                       coverUrl=first['src'], coverKey=first['key'], images=[])
        projects.append(project)
        catalog[slug] = project
    else:
        project['title'] = title
    before = len(project['images'])
    project['images'].extend(additions)
    report.append(dict(folder=name, slug=slug, files=len(files), before=before, added=len(additions),
                       duplicates=skipped, after=len(project['images'])))

ordered = [p for p in projects if p['slug'] not in tail] + [catalog[slug] for slug in tail]
assert len({p['slug'] for p in ordered}) == len(ordered)
backup = ROOT / 'output/before-local-import'
backup.mkdir(parents=True, exist_ok=True)
for relative in [str(inventory_path.relative_to(ROOT)), 'src/data/projects.json', 'src/data/importedPhotos.json']:
    (backup / Path(relative).name).write_bytes((ROOT / relative).read_bytes())
(ROOT / 'docs/portfolio-source.json').write_text(json.dumps(ordered, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(ROOT / 'docs/local-import-latest.json').write_text(json.dumps(dict(folders=report, order=[p['slug'] for p in ordered], uploadKeys=upload_keys), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for row in report:
    print(f"{row['folder']}: {row['before']} + {row['added']} ({len(row['duplicates'])} duplicates skipped) = {row['after']}", flush=True)
