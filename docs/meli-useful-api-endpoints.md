# MeLi Useful API Endpoints (Beyond Basic CRUD)

## Source: Multiple official developer pages + community research

---

## 1. Listing Quality / Performance Score
**NEW endpoint** (replaces deprecated /health):
```
GET https://api.mercadolibre.com/item/{ITEM_ID}/performance
```
Returns:
- `score`: 0-100 quality score
- `level`: "Bad", "Average", "Good"
- `level_wording`: localized ("Basica", "Estandar", "Profesional")
- `buckets`: CHARACTERISTICS (GTIN, PICTURES, TITLE, TECHNICAL_SPECS) and OFFER (FREE_SHIPPING, etc.)
- Each rule has `status`, `progress`, `mode` (OPPORTUNITY/WARNING), and action `link`

**Critical for SEO:** This score directly affects search ranking exposure.
Key quality factors:
- HAS_GTIN (universal product code)
- PICTURES_QUANTITY_MIN (minimum 3 photos)
- TITLE_LENGTH_MIN (at least 3 words)
- TS_MAIN_QUANTITY (technical specifications)
- HAS_FREE_SHIPPING

---

## 2. Trends (Top 50 Searches)
```
GET https://api.mercadolibre.com/trends/{SITE_ID}
GET https://api.mercadolibre.com/trends/{SITE_ID}/{CATEGORY_ID}
```
Returns array of 50 objects:
- First 10: highest growth searches
- Next 20: most wanted searches
- Last 20: most popular trends
- Each: `{keyword, url}`
- Updated weekly
- Available for: MLA, MLB, MLC, MLM, MCO, MLU, MPE

**Use case:** Identify hot products for MLM before listing.
Mexico trends: https://tendencias.mercadolibre.com.mx/

---

## 3. Item Visits
```
GET https://api.mercadolibre.com/items/{ITEM_ID}/visits
GET https://api.mercadolibre.com/users/{USER_ID}/items_visits?date_from=2024-01-01T00:00:00&date_to=2024-01-31T00:00:00
```
Returns visit counts per item or aggregated by seller.

---

## 4. Product Reviews
```
GET https://api.mercadolibre.com/reviews/item/{ITEM_ID}
GET https://api.mercadolibre.com/reviews/item/{ITEM_ID}?catalog_product_id={PRODUCT_ID}
```
Returns:
- Individual reviews with `rate`, `title`, `content`, `date_created`
- `rating_average`, `stars`
- `rating_levels` (breakdown by star count)
- Pagination: `limit` (max 10000), `offset`

---

## 5. Shipping Cost Calculator
```
GET https://api.mercadolibre.com/items/{ITEM_ID}/shipping_options?zip_code={ZIP_CODE}
```
Returns:
- Multiple shipping options with `list_cost` (before discounts) and `cost` (after free shipping)
- `estimated_delivery_time` with `shipping` and `handling` hours
- Discount details if free shipping applies

---

## 6. Listing Prices (Fee Calculator)
```
GET https://api.mercadolibre.com/sites/{SITE_ID}/listing_prices?price={PRICE}&category_id={CAT}&listing_type_id={TYPE}
```
Calculate exact fees before listing. Supports filters: price, category, listing_type, currency, quantity, logistic_type, tags, channel.

---

## 7. Category Predictor
```
GET https://api.mercadolibre.com/sites/{SITE_ID}/category_predictor/predict?title={TITLE}
```
Returns best matching category based on product title.

---

## 8. Products Search (Catalog)
```
GET https://api.mercadolibre.com/products/search?site_id={SITE}&q={QUERY}&status=active
GET https://api.mercadolibre.com/products/search?site_id={SITE}&product_identifier={GTIN}
GET https://api.mercadolibre.com/marketplace/products/search?q={QUERY}  (new GS endpoint)
```
Search catalog products by keyword or GTIN/EAN/UPC.

---

## 9. Domains by Country
```
GET https://api.mercadolibre.com/sites/{SITE_ID}/domains
GET https://api.mercadolibre.com/catalog_domains/{DOMAIN_ID}/products
```
List all product domains and their catalog products.

---

## 10. Seller Listing Capacity
```
GET https://api.mercadolibre.com/marketplace/users/cap
```
Returns listing limits by reputation level:
- Green Platinum/Gold: 50,000
- Green Silver: 20,000
- Green/Light Green: 10,000
- Yellow: 3,000
- Orange/Red/Newbie: 1,000

---

## 11. Billing Reports
```
GET /billing/integration/monthly/periods
GET /billing/integration/periods/key/{KEY}/documents
GET /billing/integration/periods/key/{KEY}/summary
GET /billing/integration/periods/key/{KEY}/details
```
Detailed billing with IVA perceptions, bonuses, charges broken down.

---

## 12. User Products Family
```
GET /user-products/{USER_PRODUCT_ID}             → get family_id
GET /sites/{SITE}/user-products-families/{FAMILY_ID}  → all UPs in family
GET /users/{SELLER}/items/search?user_product_id={ID}  → items for UP
```

---

## 13. Webhook Notification Topics
Subscribe to real-time updates:
- `items` — listing changes
- `orders_v2` — confirmed sales
- `questions` — Q&A
- `payments` — payment status
- `shipments` — shipping updates
- `messages` — buyer messages
- `item_competition` — catalog competition changes
- `catalog_suggestions` — catalog product suggestion status
- `items_prices` — price changes
- `stock_locations` — stock changes
- `stock_fulfillment` — FBM warehouse operations

---

## 14. Rate Limits
- 1500 requests per minute per seller
- 429 status code when exceeded
- Max search offset: 1000 (use `search_type=scan` + `scroll_id` for more)

---

## 15. MCP Server (NEW)
MeLi now offers an MCP (Model Context Protocol) server for AI integrations:
https://global-selling.mercadolibre.com/devsite/mcp-server-from-mercado-libre
