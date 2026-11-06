# Photography Website

Personal photography portfolio website built with Astro as a static site.

## Foundation

- Static Astro project
- Mobile-first layout and navigation
- Project-led homepage, Work overview, 15 project detail pages, and real contact information
- Original category routes retained alongside the project overview
- No CMS or database
- No photography assets stored in the repository

Production photography assets are hosted outside Git in Cloudflare R2.

## Adobe Portfolio migration

The Adobe preview and curated local folders are combined as 15 series and 346 photographs.
The original 220 displayed photos are retained, with 126 local photos appended.
Images are uploaded to the existing R2 bucket and their
public file contents have been verified against the local exports. The preview
and static build use R2 by default. Local backups at public/media/adobe/ are
ignored by Git. Source inventory, restoration commands,
R2 upload instructions and remaining editorial notes are in
[docs/adobe-migration.md](docs/adobe-migration.md).

PUBLIC_PORTFOLIO_MEDIA_URL can override the default public media base URL.
Set it to /media for a preview using the local image backups.

After building, run python scripts/verify-portfolio.py to verify the photo
metadata, actual dimensions and all built internal links.

The current combined source inventory is docs/portfolio-source.json. The earlier
Adobe-only inventory remains at docs/adobe-source.json. To append the same local
folder structure again, use python scripts/import-local.py <folder>, followed by
python scripts/import-adobe.py. Existing photo keys and originals are preserved.

## Commands

```sh
npm install
npm run dev
npm run build
```

## Navigation and publication

Project covers show a permanent subject badge, title, photo count and year.
Work and Contact remain directly visible on mobile. The Work page provides
subject filters with accessible pressed states, announced result counts and
the original series order within each selection.

To publish a tested build to the Cloudflare Pages project yuxiang-photography:

    npm run build
    python scripts/verify-portfolio.py
    python scripts/prepare-deployment.py
    npx wrangler@4.158.0 pages deploy <returned-directory> --project-name yuxiang-photography --branch main

The deployment packager excludes local photo backups; displayed photos come
from R2. The site source is maintained in the existing GitHub repository.
