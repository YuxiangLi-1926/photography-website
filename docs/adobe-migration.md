# Adobe Portfolio migration

Read-only source: Adobe Portfolio site edd5c75b-8d9c-4707-85af-e7fc3d94fbff.
Inventory captured on 2026-11-06 from its authenticated preview. Adobe content was
not edited or published. The inventory covers the 12 projects visible on Work,
not a claim that hidden/unlisted pages have been exported.

## Imported content

220 project photos and 12 separately cropped covers; original project order,
years, photo sequence and existing Cars & Campaign description are retained.
The source URLs and source dimensions are recorded in adobe-source.json.
Local images are web exports, resized to a maximum 1920px edge and saved as
JPEG quality 86. They are not camera originals. Actual output dimensions are
recorded in src/data/importedPhotos.json and projects.json.

The current site's Yuxiang Li brand is retained instead of the older Brien Lee
name. The London introduction and contact details come from the old site.
Category mapping is provisional: Jaguar and Cars & Campaign → cars; Grads and
Portrait → portrait; Food in Love → food; Campaigns → event; remaining projects
→ my-work. Dedicated project names remain intact regardless of category.
Alt text identifies the series and sequence; descriptive image-specific alt
text remains an editorial follow-up.

## Restore and preview

Large images remain outside Git, matching the existing repository policy.
The local files live at public/media/adobe/, including the original 269-file
backup and 232 currently active images. The 37 removed photos remain as backups.
Keep this folder until the R2 copy is verified. An independent checkout can
restore from Adobe while those recorded source URLs remain available:

    python -m pip install Pillow
    python scripts/import-adobe.py
    npm install
    npm run build
    python scripts/verify-portfolio.py
    npm run dev

The homepage and /work/ show the same project overview. Detail pages live at
/projects/<slug>/. Existing category URLs remain available.
Detail photos retain their order and proportions, with a native dialog for
enlargement, previous/next controls, arrow keys, Escape and focus restoration.
Mobile navigation uses a native disclosure; photos stack on small screens.
Contact uses a real mailto link and social handles, without an inactive form.

## R2 hosting

Official Wrangler OAuth authorization succeeded on 2026-11-06. The existing
bucket yuxiang-photography was confirmed to expose the configured public endpoint:
https://pub-c656b8808bc24676b509a61ef1050d6c.r2.dev

The original 257 photos and 12 covers were uploaded under adobe/. Every public image was
downloaded and verified: HTTP 200, image/jpeg and a matching SHA-256 hash against
the local export. The website now uses this R2 base URL by default. No bucket
access settings were changed. No GitHub push or production deployment occurred.
PUBLIC_PORTFOLIO_MEDIA_URL can override the base; /media uses local backups.

To repeat an upload after updating images:

1. Complete the official Wrangler login in the browser.
2. Run npx wrangler@4.158.0 r2 bucket list and select the existing portfolio bucket.
3. Run pwsh -File scripts/upload-r2.ps1 -Bucket <existing-bucket>.
4. Verify all 269 keys at the existing public R2 endpoint.
5. Run python scripts/verify-r2.py <public-base-url>, then rebuild.

## Latest Adobe synchronization (2026-11-06)

The 12 visible Work pages were read again after the owner's edits. Jaguar changed
from 49 to 15 photos (34 removed); Campaigns from 17 to 14 (3 removed). No added
photos, series changes, cover changes or relative reordering of retained photos
were observed. The current display contains 220 photos plus 12 covers. Contact
details were checked again and remain unchanged.

Removed photos were removed from the display manifest only; local backups and
R2 objects remain. Retained photos reuse their exact original R2 keys, so a
change in sequence cannot accidentally substitute a different cached photo.
The synchronization utility assigns source-derived keys to new/changed assets.
The detailed comparison is in adobe-sync-latest.json; the previous inventory and
manifests are backed up locally under output/adobe-sync-before/.

For a fresh complete browser capture (adobe-covers.json and adobe-project-N.json):

    python scripts/sync-adobe-inventory.py <capture-directory>
    python scripts/import-adobe.py

Then upload any new asset keys, verify R2, and build. This utility checks capture
titles, unique sources, project URLs and any videos before updating the inventory.

The upload script only puts manifest-listed objects under adobe/; it does not
delete objects or alter bucket public access. Code is kept separate from
account credentials. No production deployment is performed by these scripts.

## Verified during implementation

- npm run build: passed; 23 static pages generated.
- python scripts/verify-portfolio.py: passed, including all 232 active image
  dimensions and built internal link targets.
- Playwright: no horizontal overflow at 320, 390, 768 and 1440px on the homepage,
  Jaguar project and contact page.
- Playwright: mobile menu reaches Contact; dialog opens, advances with the right
  arrow key, and closes with Escape.
- Desktop homepage, desktop Jaguar gallery and mobile homepage screenshots
  inspected visually.
