"""Verify migrated metadata, real image dimensions, and built internal links."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
photos = json.loads((ROOT / 'src/data/importedPhotos.json').read_text(encoding='utf-8'))
projects = json.loads((ROOT / 'src/data/projects.json').read_text(encoding='utf-8'))
source_path = ROOT / 'docs/portfolio-source.json'
if not source_path.exists():
    source_path = ROOT / 'docs/adobe-source.json'
source = json.loads(source_path.read_text(encoding='utf-8'))
assert len({p['id'] for p in photos}) == len(photos)
assert len({p['key'] for p in photos}) == len(photos)
assert len({p['slug'] for p in projects}) == len(projects)
assert [p['slug'] for p in projects] == [p['slug'] for p in source]
categories = {'event', 'nightlife', 'food', 'portrait', 'cars', 'her', 'my-work'}
for project, original in zip(projects, source):
    series = [p for p in photos if p['project'] == project['slug']]
    assert len(series) == project['photoCount'] == len(original['images'])
    if all('key' in image for image in original['images']):
        assert [p['key'] for p in series] == [image['key'] for image in original['images']], project['slug']
    assert [p['order'] for p in series] == sorted(p['order'] for p in series)
    assert all(p['category'] in categories for p in series)
    for entry, width, height in [(p['key'], p['width'], p['height']) for p in series] + [(project['coverKey'], project['coverWidth'], project['coverHeight'])]:
        with Image.open(ROOT / 'public/media' / entry) as image:
            assert image.size == (width, height), entry
            assert width > 1 and height > 1, entry


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('href', 'src') and value:
                parsed = urlsplit(value)
                path = unquote(parsed.path)
                if not parsed.scheme and not parsed.netloc and path.startswith('/'):
                    target = ROOT / 'dist' / path.lstrip('/')
                    if path.endswith('/'):
                        target /= 'index.html'
                    assert target.is_file(), f'{self.page}: missing {path}'


pages = list((ROOT / 'dist').rglob('*.html'))
assert pages, 'Run npm run build first'
for page in pages:
    parser = Links()
    parser.page = page.relative_to(ROOT)
    parser.feed(page.read_text(encoding='utf-8'))
print(f'PASS: {len(projects)} series, {len(photos)} photos, {len(photos) + len(projects)} image dimensions, {len(pages)} built pages and their internal links.')
