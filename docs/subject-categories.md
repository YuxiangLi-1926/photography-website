# Current portfolio subjects

The public filters are People, Moments, Food, Places and Sweetie.

| Subject | Series | Photos |
| --- | ---: | ---: |
| People | 2 | 75 |
| Moments | 3 | 88 |
| Food | 1 | 44 |
| Places | 8 | 109 |
| Sweetie | 1 | 30 |

Moments contains Events (previously Campaign), Night in London, and
Cars & Campaign. Places includes Jaguar and the previous Personal series,
except DOGGY & KITTY, which is now the only Sweetie series.

The original 15-series display order, photo order, IDs, cover keys and all
346 photo keys are unchanged. The Events series retains /projects/campaigns/
so existing project links remain valid.

The source inventory, generated catalog and photo metadata agree on category
membership. Internal keys event and my-work are retained for Moments and Places;
the new Sweetie key is sweetie. New local Night in London imports use event,
and the Campaign folder retains the public Events title.

Canonical subject pages are /moments/, /places/ and /sweetie/. Legacy /event/
and /nightlife/ redirect to /moments/; /my-work/ to /places/; /cars/ to /work/.
Astro handles the local redirects and public/_redirects supplies production
HTTP redirects on Cloudflare Pages.

Verification: static build and inventory/image/link verification passed.
Browser checks confirmed exact filter membership, canonical page photo counts
and mobile layout. No photos were uploaded, deleted or moved in R2 for this change.
