# Local portfolio update — 2026-11-06

The owner requested additions from D:\照片\网站素材, explicitly choosing to
retain existing photos and append folder contents. All original files are
read-only inputs. Existing covers and retained R2 keys remain unchanged.

| Folder / series | Existing | Added | Current |
| --- | ---: | ---: | ---: |
| Campaign | 14 | 9 | 23 |
| London | 23 | 1 | 24 |
| Portrait | 26 | 18 | 44 |
| Grads | 15 | 16 | 31 |
| Food in Love | 15 | 29 | 44 |
| Edi | 0 | 7 | 7 |
| Night in London | 0 | 36 | 36 |
| The White Cliff | 0 | 10 | 10 |

All 126 local photos were added. No matches met the conservative duplicate
threshold within their destination series: matching aspect ratio and maximum
per-channel RMS difference of at most 1 on 64px thumbnails. This check is not
a claim that every near-identical composition or differently edited version
has been eliminated.

Within each folder, filenames use natural sorting (1, 2, …, 10). New photos
follow existing photos. New series use the first naturally sorted photo as
their cover; existing series keep their covers. EXIF capture years are used
for new photos and new series. The original series start years are retained.

## Display order

Grads → Campaign → Food in Love → Portrait → London → Night in London →
Cars & Campaign → Jaguar → Real Estate → The White Cliff → Edi → Spain →
Switzerland → Netherland → DOGGY & KITTY.

The final nine entries follow the owner's exact requested order. Other
existing series keep their relative order at the front; Night in London
follows them. The 15 project pages and their recommendations use this catalog.

## Files and hosting

- docs/portfolio-source.json is now the canonical combined inventory, including
  both Adobe web exports and local file references with original SHA-256 hashes.
- docs/adobe-source.json remains the earlier Adobe-only snapshot. Do not use it
  to overwrite the combined inventory after a subsequent Adobe edit.
- docs/local-import-latest.json records counts, ordering and new upload keys.
- Existing photos remain under adobe/ in R2; new local exports use portfolio/.
  Content-based filenames prevent replacements from serving stale cached images.
- Exports are JPEG quality 86, maximum 1920px edge. All 126 local files were
  confirmed to have sRGB profiles. Originals are neither resized nor rewritten.
- The three new cover references reuse their first photo: 346 photo references
  plus 15 covers correspond to 358 distinct R2 objects.
- The previous manifests are backed up under output/before-local-import/.

## Repeatable workflow

    python scripts/import-local.py <source-folder>
    python scripts/import-adobe.py
    pwsh -File scripts/upload-r2.ps1 -Bucket yuxiang-photography -ChangesFile docs/local-import-latest.json
    python scripts/verify-r2.py https://pub-c656b8808bc24676b509a61ef1050d6c.r2.dev
    npm run build
    python scripts/verify-portfolio.py

The source-folder contents are appended. Updating an existing original's bytes
at the same path requires an explicit replacement workflow; this importer
does not silently replace a previously imported photo.

## Verification

- All 126 new objects uploaded successfully; all 358 distinct active R2 files
  returned HTTP 200 with JPEG content type and matching local SHA-256 hashes.
- npm run build passed: 26 static pages.
- verify-portfolio.py passed: counts, inventory order, dimensions and internal links.
- All 220 previous photo keys remain in the current manifest; the final nine
  catalog positions exactly match the requested order.
- All 126 source-file SHA-256 hashes still match, confirming originals unchanged.
- Playwright confirmed all eight updated/new series counts, first/last image
  decoding, 15 homepage cards in the requested order, and no mobile overflow.
- New series lightbox opens, advances and closes with Escape. Desktop and mobile
  screenshots of The White Cliff were visually checked.
- Changes are local; no GitHub push or production site deployment was performed.
