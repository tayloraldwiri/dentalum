# Dentalum redesign

A complete buildless, responsive Swedish website. Original source: https://dentalum.com. Audited 18 October 2026.

## Run

```sh
npm start
```

Open http://localhost:4173. No npm dependencies or build step are needed. Deploy `dist/` to any static host that serves directory `index.html` files. The original Dentalum domain has not been modified.

## Coverage

223 preserved page routes plus a new searchable `/sidkarta/`. The original navigation, footer, robots file, sitemap index, all child sitemaps, and recursively discovered internal HTML links were crawled. Aliases, financial documents, news categories and Cision tags were included rather than silently discarded.

- 35 clinic profiles, a clinic index and 14 regional pages
- 30 treatment routes, including regional guides and original URL aliases
- 4 news articles, news archives and category alias
- 104 individual press releases, 5 archive pages and 10 tag archives
- About, team, careers, partnerships, sustainability, patient safety, contact, pricing, policies and investor pages
- Existing root/author/about aliases preserved with the content returned by the source

Detailed source URL and implementation coverage: `audit/page-inventory.json`. Full request statuses and redirects: `audit/crawl.json`. Local image mapping and original URLs: `audit/assets.json`.

## Design and interactions

Warm ivory and forest-green light theme; complete dark theme. System preference initializes before rendering; manual choice persists. Shared responsive menus, mobile navigation, booking selector, clinic search/region filters/reset/empty state, treatment selector and validation, team name/role filters, FAQ accordions and expand/collapse controls, keyboard-operable image galleries, page contents links, larger-text control, searchable sitemap and back-to-top control. Entrance/reveal animations and interactive feedback respect reduced-motion preferences. Content remains available without JavaScript; menus and enhancement controls need JavaScript.

Original people photos are reused byte-for-byte, with natural aspect ratios and no generated replacements, edits, retouching or object-fit cropping. Original hero background photos are displayed as normal images so people remain fully visible. Reviewer photos stay alongside their original reviews. Downloadable assets and new typography are served locally where available. Review content and rating counts are labeled as a dated source snapshot, rather than implying a live integration.

## External functionality and source limitations

- Booking uses Dentalum's existing clinic pages and booking service, opened in a new tab. Choose **Boka tid** on the original clinic page. This recreation does not submit bookings itself.
- Original contact, registration and patient-feedback forms depend on the original backend. Their replacements clearly explain this and link to the original page; no simulated submission or false confirmation is shown.
- `https://dentalum.com/cdn-cgi/l/email-protection` returned **404**. Encoded addresses were decoded from the source and converted to working `mailto:` links.
- The direct-marketing policy PDF returned **429** on repeated download attempts. Its original external link is retained: `https://dentalum.com/wp-content/uploads/2025/12/Riktlinjer-for-direktmarknadsforing.pdf`.
- One legacy original photo returned **500**: `https://kungsf29.mydental.host/wp-content/uploads/2022/11/tandlakare-kvinna-2000px.webp`. Every affected location explicitly identifies the unavailable original and links to it. It has not been replaced or regenerated.
- External booking/form submissions, phone/email apps, external career systems, third-party document downloads and live review updates cannot be tested as transactions locally. No real patient request was submitted.
- Publication was not completed: the Sites source-workflow helpers were absent from the environment, and the skill package became unavailable during execution. A complete static deployment artifact is provided instead.

## Verification

See `audit/verification.json` for route-by-route results and interaction checks. `audit/coverage-gaps.json` compares source main-content headings and image references; remaining differences are the original rating widget's decorative star/platform icons, which were redesigned. Browser testing uses Chromium through Playwright. Representative screenshots are included in `audit/`.

The prebuilt site is ready to serve. To regenerate source extraction, install `requirements.txt` and run `python build.py`. `crawl.py` and `assets.py` document the original acquisition. These scripts are retained for provenance; existing audit snapshots and local assets allow generation without another source crawl.
