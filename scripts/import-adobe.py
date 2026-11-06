"""Restore recorded web exports from Adobe or local sources; originals are read-only."""
import concurrent.futures
import io
import json
import time
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
source_path = ROOT / 'docs/portfolio-source.json'
if not source_path.exists():
    source_path = ROOT / 'docs/adobe-source.json'
projects = json.loads(source_path.read_text(encoding='utf-8'))


def restore(task):
    key, url = task
    destination = ROOT / 'public/media' / key
    if not destination.exists():
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={'User-Agent': 'PhotographyPortfolioMigration/1.0'})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                with Image.open(io.BytesIO(data)) as source:
                    image = ImageOps.exif_transpose(source).convert('RGB')
                    image.thumbnail((1920, 1920))
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    temporary = destination.with_suffix('.tmp')
                    image.save(temporary, format='JPEG', quality=86, optimize=True)
                    temporary.replace(destination)
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)
    with Image.open(destination) as image:
        image.verify()
    with Image.open(destination) as image:
        return key, image.size


tasks = []
for project in projects:
    prefix = f"adobe/{project['slug']}"
    tasks.append((project.get('coverKey', f'{prefix}/cover.jpg'), project['coverUrl']))
    for index, image in enumerate(project['images'], 1):
        tasks.append((image.get('key', f'{prefix}/{index:03}.jpg'), image['src']))

# New projects may use their first photo as the cover. Restore each key once.
tasks = list(dict(tasks).items())
dimensions = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for index, (key, size) in enumerate(pool.map(restore, tasks), 1):
        dimensions[key] = size
        if index % 30 == 0:
            print(f'Restored {index}/{len(tasks)} images', flush=True)

photos, catalog = [], []
for project in projects:
    prefix = f"adobe/{project['slug']}"
    cover_key = project.get('coverKey', f'{prefix}/cover.jpg')
    cover_width, cover_height = dimensions[cover_key]
    catalog.append({
        'slug': project['slug'], 'title': project['title'], 'year': project['year'],
        'category': project['category'], 'description': project['description'],
        'coverKey': cover_key, 'coverWidth': cover_width, 'coverHeight': cover_height,
        'photoCount': len(project['images']),
    })
    for index, image in enumerate(project['images'], 1):
        key = image.get('key', f'{prefix}/{index:03}.jpg')
        width, height = dimensions[key]
        photos.append({
            'id': f"{project['slug']}-{Path(key).stem}", 'key': key,
            'category': project['category'], 'project': project['slug'],
            'year': image.get('year') or project['year'], 'width': width, 'height': height,
            'altEn': f"{project['title']} — photograph {index}",
            'altZh': f"{project['title']} · 第 {index} 张作品",
            'featured': index == 1, 'order': len(photos) + 1,
        })

(ROOT / 'src/data/importedPhotos.json').write_text(json.dumps(photos, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(ROOT / 'src/data/projects.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f"Restored {len(photos)} photos and {len(catalog)} covers. Dimensions verified.", flush=True)
