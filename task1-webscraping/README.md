# Multi Site Web Scraping Pipeline

Extracts structured marketing data from list pages and product pages across three e-commerce sites (Olipop, Poppi, Coca Cola Simply Pop), each built on a different underlying platform with a different rendering strategy, normalized into one shared schema.

## What this demonstrates

Real world scraping rarely means one script working across every target. These three sites required three distinct approaches: a lightweight request based method for Shopify backed storefronts, and a headless rendering fallback for a JS heavy enterprise site with bot protection. The interesting part isn't any single scrape, it's the normalization layer that reconciles inconsistent gallery structures, ingredient formatting, and nutrition label layouts into one clean output.

## Output

`output/products.csv`, one row per page scraped, columns: URL, page type, product name, price, discounted price, position, photo count, flavor, ingredients, nutrition facts.

## Method

- Ran as three separate extraction jobs rather than one generalized scraper, since a single approach became brittle against the schema differences across sites
- Used Apify actors with proxy rotation and headless rendering fallback for sites that blocked plain requests
- Defined a consistent counting rule for product photos across three different gallery implementations, documented so the method is reproducible
- Missing values are left blank and noted, never fabricated. Coca Cola's Simply Pop line has a narrower catalog than the other two brands, reflected honestly in the row count rather than padded

## Limitations, stated plainly

Coca Cola's product page structure exposed fewer of the requested fields than the two Shopify based sites. Documented in the output rather than worked around.
