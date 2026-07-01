# Task 1: Webscraping

Snapshot date: 2026-07-01. Scrape covers Olipop, Poppi, and Coca-Cola Simply Pop, first 10 products per list page (fewer where fewer exist), plus each linked product page.

## Method per site

**Apify was evaluated first per the master plan and was not used.** All three sites returned complete, well-structured content through direct HTTP fetch (no JS rendering or proxy rotation needed), so running a paid Apify actor would have added cost and an extra layer of schema translation without improving data quality. Specifically:

- **Olipop (drinkolipop.com, Shopify).** List page fetched directly. Product pages fetched two ways: the rendered HTML page (for description, ingredients, nutrition facts, and the visible photo gallery) and the store's public `/products/<handle>.json` endpoint (for authoritative price and compare-at price). Olipop is mid-promotion at scrape time (a "4th of July, 25% off 12-packs" banner), so 3 of the 10 sampled products show a discounted price and 7 don't — this is a real, live pricing state, not a scraping inconsistency.
- **Poppi (drinkpoppi.com, Shopify).** Same two-fetch approach. Note: Poppi's Shopify product JSON endpoint only returns one image per product (the front-can shot), while the live page renders a separate 7-9 image gallery through a different app/section not reflected in that JSON. Photo counts in the CSV use the page-rendered gallery, not the JSON, for this reason (see "Photo count" below).
- **Coca-Cola Simply Pop (coca-cola.com).** Fetched directly with no bot-blocking encountered, so no headless/proxy actor was required. This site is a brand marketing page, not a storefront — see Limitations.

No Apify run was executed against any of the three domains. Total requests were roughly 65 lightweight GETs spread across three domains over one session — well below anything that risks rate-limiting or IP blocking, so this proceeded without a mid-task pause.

## How "number of photos" was defined

Rule: count distinct image URLs inside the product's own gallery/carousel component on its product page, in the order rendered, excluding: thumbnails of other flavors shown in "you may also like" or flavor-picker widgets, site chrome (logos, icons, badges), and background/lifestyle images outside the gallery block.

- Olipop: images under the page's "Product gallery carousel" heading, up to the point the flavor-picker (other products) begins.
- Poppi: the numbered image sequence (`...PDP-01.jpg` through `...PDP-0N.jpg`) shown at the top of the product page, before the customer-review and variety-pack sections.
- Coca-Cola: each Simply Pop flavor gets exactly one product shot on the shared `/products/pop` page; there is no per-flavor gallery.

## Limitations (not fabricated, flagged instead)

CSV cells always hold a clean value only (a number, or the literal string `NOT AVAILABLE`) — no inline explanations. The reasoning for every non-obvious or missing value is recorded here instead.

- **Olipop — Cherry Cola and Peaches & Cream:** the live page fetch for these two products did not render the gallery-carousel or nutrition-facts widgets (likely a different product-template variant lazy-loading that content client-side). Photo count for these two falls back to the Shopify JSON `images[]` array count (9 for both — a real count, just sourced from JSON instead of the rendered carousel like the other 8 Olipop products). Nutrition facts for these two could not be recovered from either the page or the JSON endpoint, so that cell reads `NOT AVAILABLE`.
- **Poppi — Doc Pop:** the product page fetch did not return the image gallery section at all (unlike the other 9 Poppi products, which all rendered a numbered `PDP-01.jpg` … `PDP-0N.jpg` sequence). Rather than assume the same 7-9 image pattern seen elsewhere on the site, the photo count cell reads `NOT AVAILABLE`.
- **Coca-Cola Simply Pop:** the list page has only 5 products, not 10 — Simply Pop launched with five flavors and the site does not list more. This is a real product-catalog limit, not a scrape failure. Coca-Cola also has no dedicated URL per flavor: all five flavors live on one shared page (`/products/pop`), so all 5 product rows share that URL, and each gets a photo count of 1 (one product shot per flavor on that shared page — see "How number of photos was defined" above). No price or discounted price is shown anywhere on the site for these products — Simply Pop is sold through Amazon and retail, not direct-to-consumer, so the brand page carries no checkout or pricing UI. Both fields are left blank rather than invented.
- **Olipop promotional pricing:** 3 of 10 sampled Olipop products (Classic Root Beer, Vintage Cola, Strawberry Vanilla) show a 25%-off sale price captured mid-scrape; the other 7 do not. Both states were real at the moment of their respective fetches.

## Output

`output/products.csv` — 50 rows (10 list-page rows + 10 product-page rows per site x 3 sites... Coca-Cola contributes 5 + 5 = 10). Columns: URL, list/product page, product name, price, discounted price, position, number of photos, flavor, ingredients, nutrition facts. List rows populate name/price/discounted price/position; product rows populate name/photos/flavor/ingredients/nutrition facts, per the task's acceptance criteria.
