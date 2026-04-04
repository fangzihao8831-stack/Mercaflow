# MercadoLibre API Research: Automated Listing Pipeline

**Research Date:** 2026-04-01
**Target Market:** Mexico (MLM)
**Base API URL:** `https://api.mercadolibre.com`

---

## Table of Contents

1. [API Basics & Developer Portal](#1-api-basics--developer-portal)
2. [OAuth Authentication Flow](#2-oauth-authentication-flow)
3. [Rate Limits & Listing Limits](#3-rate-limits--listing-limits)
4. [SDKs & Libraries](#4-sdks--libraries)
5. [Item/Listing Creation API](#5-itemlisting-creation-api)
6. [Category System](#6-category-system)
7. [Category Predictor API](#7-category-predictor-api)
8. [Catalog System (Catalogo) — CRITICAL](#8-catalog-system-catálogo--critical)
9. [Product Descriptions](#9-product-descriptions)
10. [Image Upload API](#10-image-upload-api)
11. [Listing Types & Pricing](#11-listing-types--pricing)
12. [Shipping (Mercado Envios)](#12-shipping-mercado-envios)
13. [User Products — New Model](#13-user-products--new-model)
14. [Webhooks & Notifications](#14-webhooks--notifications)
15. [Bulk Operations](#15-bulk-operations)
16. [Key API Endpoints Reference](#16-key-api-endpoints-reference)
17. [Automated Pipeline Architecture](#17-automated-pipeline-architecture)

---

## 1. API Basics & Developer Portal

### Developer Portals

| Portal | URL | Notes |
|--------|-----|-------|
| Mexico | https://developers.mercadolibre.com.mx | MLM-specific docs |
| Argentina | https://developers.mercadolibre.com.ar | Most complete docs (en_us available) |
| Global Selling | https://global-selling.mercadolibre.com/devsite | Cross-border trade (CBT) |
| Application Manager | https://developers.mercadolibre.com/application-manager/ | Create/manage apps |

### API Architecture

- **REST API** — standard HTTP methods (GET, POST, PUT, DELETE)
- **Base URL:** `https://api.mercadolibre.com`
- **Response format:** JSON
- **Authentication:** OAuth 2.0 Bearer tokens in headers
- **Site ID for Mexico:** `MLM`
- **Currency for Mexico:** `MXN`

### Key Concepts

- **Items** = Listings (products for sale on the marketplace)
- **Site** = Country marketplace (MLM = Mexico, MLA = Argentina, MLB = Brazil, etc.)
- **Catalog Product** = MeLi's curated product page (shared among sellers)
- **User Product (UP)** = New concept: a physical product a seller owns (being rolled out 2024-2025)

---

## 2. OAuth Authentication Flow

### Overview

MeLi uses **OAuth 2.0 Authorization Code Grant Type** (server-side flow).

### Step-by-Step Flow

```
1. Redirect user to MeLi auth page
2. User logs in and authorizes your app
3. MeLi redirects back with authorization code
4. Exchange code for access_token + refresh_token
5. Use access_token in API requests
6. Refresh token when expired
```

### Step 1: Authorization URL (Mexico)

```
https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=$APP_ID&redirect_uri=$YOUR_URL
```

**Country-specific auth URLs:**
- Mexico: `https://auth.mercadolibre.com.mx`
- Argentina: `https://auth.mercadolibre.com.ar`
- Brazil: `https://auth.mercadolivre.com.br`
- Colombia: `https://auth.mercadolibre.com.co`

Optional PKCE parameters (recommended):
- `code_challenge` — SHA-256 hashed verification code
- `code_challenge_method` — `S256` or `plain`

### Step 2: Exchange Code for Token

```bash
curl -X POST \
  -H 'accept: application/json' \
  -H 'content-type: application/x-www-form-urlencoded' \
  'https://api.mercadolibre.com/oauth/token' \
  -d 'grant_type=authorization_code' \
  -d 'client_id=$APP_ID' \
  -d 'client_secret=$CLIENT_SECRET' \
  -d 'code=$AUTH_CODE' \
  -d 'redirect_uri=$REDIRECT_URI'
```

**Response:**
```json
{
  "access_token": "APP_USR-12345678-031820-X-12345678",
  "token_type": "Bearer",
  "expires_in": 21600,
  "scope": "offline_access read write",
  "user_id": 123456789,
  "refresh_token": "TG-..."
}
```

- `access_token` expires in **6 hours** (21600 seconds)
- `refresh_token` must be saved to renew access

### Step 3: Refresh Token

```bash
curl -X POST \
  -H 'accept: application/json' \
  -H 'content-type: application/x-www-form-urlencoded' \
  'https://api.mercadolibre.com/oauth/token' \
  -d 'grant_type=refresh_token' \
  -d 'client_id=$APP_ID' \
  -d 'client_secret=$CLIENT_SECRET' \
  -d 'refresh_token=$REFRESH_TOKEN'
```

### Using the Token

Always send via header (NOT query parameter):

```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/users/me
```

### Token Invalidation Events

- User changes password
- Application refreshes App Secret
- User revokes app permissions
- No API request made for 4 months

### Security Best Practices

- Send token params in POST body, not query string
- Use `state` parameter with secure random value to prevent CSRF
- Implement PKCE flow for added security
- Store refresh_token securely (encrypted at rest)

---

## 3. Rate Limits & Listing Limits

### API Rate Limits

| Limit | Value |
|-------|-------|
| Requests per minute per seller | **1,500 RPM** |
| Exceeded response | HTTP 429 (empty body) |
| Image upload endpoint | Separate RPM quota per app_id |
| Listing creation quota (Global Selling) | 10,000 requests per day per site |

### Listing Limits (Active Listings by Reputation)

| Reputation Level | Max Active Listings |
|-----------------|-------------------|
| Green Platinum / Green Gold | 50,000 |
| Green Silver | 20,000 |
| Green / Light Green | 10,000 |
| Yellow | 3,000 |
| Orange / Red / Newbie | 1,000 |

### Check Your Listing Limit

```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/marketplace/users/cap
```

Response includes `quota` (limit) and `total_items` (current count) per site.

---

## 4. SDKs & Libraries

### Official Python SDK — DEPRECATED

> **WARNING:** Official SDK at `github.com/mercadolibre/python-sdk` was deprecated in April 2021. Dependencies are not updated. DO NOT USE for new development.

The old SDK (`pip install meli`) used auto-generated OpenAPI code. It is non-functional.

### Recommended Approach

**Build a thin REST client using `requests` or `httpx`:**

```python
import requests

class MercadoLibreClient:
    BASE_URL = "https://api.mercadolibre.com"

    def __init__(self, access_token):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def get(self, path, params=None):
        return self.session.get(f"{self.BASE_URL}{path}", params=params)

    def post(self, path, json=None):
        return self.session.post(f"{self.BASE_URL}{path}", json=json)

    def put(self, path, json=None):
        return self.session.put(f"{self.BASE_URL}{path}", json=json)

    def delete(self, path):
        return self.session.delete(f"{self.BASE_URL}{path}")
```

### Third-Party Libraries

| Library | Language | Link | Status |
|---------|----------|------|--------|
| `mercadolibre/python-sdk` | Python | github.com/mercadolibre/python-sdk | **DEPRECATED** |
| `mercadolibre/php-sdk` | PHP | github.com/mercadolibre/php-sdk | **DEPRECATED** |
| `zephia/mercadolibre` | PHP | github.com/zephia/mercadolibre | Third-party, active |
| MCP Server | Various | global-selling.mercadolibre.com/devsite/mcp-server-from-mercado-libre | New (2025+) |

### MCP Server (New)

MeLi now offers an **MCP (Model Context Protocol) Server** for AI-powered integrations. See:
https://global-selling.mercadolibre.com/devsite/mcp-server-from-mercado-libre

---

## 5. Item/Listing Creation API

### Creating a New Listing

**Endpoint:** `POST https://api.mercadolibre.com/items`

### Minimum Required Fields

```json
{
  "title": "Product Title Here",
  "category_id": "MLM1234",
  "price": 999.99,
  "currency_id": "MXN",
  "available_quantity": 10,
  "buying_mode": "buy_it_now",
  "listing_type_id": "gold_special",
  "condition": "new",
  "pictures": [
    {"source": "https://example.com/image1.jpg"}
  ],
  "attributes": [
    {
      "id": "BRAND",
      "value_name": "MyBrand"
    },
    {
      "id": "ITEM_CONDITION",
      "value_id": "2230284",
      "value_name": "Nuevo"
    }
  ]
}
```

### Complete POST /items Example

```bash
curl -X POST \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Samsung Galaxy S23 128 Gb Negro 8 Gb Ram",
    "site_id": "MLM",
    "category_id": "MLM1055",
    "price": 15999,
    "currency_id": "MXN",
    "available_quantity": 5,
    "buying_mode": "buy_it_now",
    "listing_type_id": "gold_special",
    "pictures": [
      {"source": "https://example.com/front.jpg"},
      {"source": "https://example.com/back.jpg"}
    ],
    "attributes": [
      {"id": "BRAND", "value_name": "Samsung"},
      {"id": "MODEL", "value_name": "Galaxy S23"},
      {"id": "ITEM_CONDITION", "value_id": "2230284", "value_name": "Nuevo"},
      {"id": "INTERNAL_MEMORY", "value_name": "128 GB"},
      {"id": "COLOR", "value_name": "Negro"}
    ],
    "sale_terms": [
      {
        "id": "WARRANTY_TYPE",
        "value_name": "Garantía del vendedor"
      },
      {
        "id": "WARRANTY_TIME",
        "value_name": "90 días"
      }
    ],
    "shipping": {
      "mode": "me2",
      "local_pick_up": false,
      "free_shipping": false
    }
  }' \
  https://api.mercadolibre.com/items
```

### Response (Success)

Returns the created item object with:
- `id` — The item ID (e.g., "MLM1136716168")
- `permalink` — URL to the live listing
- `status` — Should be "active"
- All fields echoed back

### Validate Before Posting

```bash
POST https://api.mercadolibre.com/items/validate
```

Same body as POST /items. Returns validation errors without creating the listing.

### Update an Item

```bash
PUT https://api.mercadolibre.com/items/$ITEM_ID
```

### Get Item Details

```bash
GET https://api.mercadolibre.com/items/$ITEM_ID
```

### Key Field Notes

| Field | Details |
|-------|---------|
| `title` | Max length determined by category (`max_title_length` field in category details). Typically ~60 chars. |
| `category_id` | Must be a leaf category (no sub-categories). Use category predictor. |
| `condition` | `"new"` or `"used"`. Being replaced by `ITEM_CONDITION` attribute. |
| `buying_mode` | Almost always `"buy_it_now"` for fixed price. Also `"auction"`. |
| `listing_type_id` | See Listing Types section. `gold_special` (Classic) or `gold_pro` (Premium). |
| `currency_id` | `"MXN"` for Mexico, `"ARS"` for Argentina, `"BRL"` for Brazil. |
| `pictures` | Array of objects. Either `{"source": "URL"}` or `{"id": "picture_id"}`. |
| `attributes` | Category-specific. Check `/categories/{id}/attributes` for required ones. |
| `sale_terms` | Warranty info. Check `/categories/{id}/sale_terms` for available terms. |
| `channels` | Array to set publication channels. Replaces deprecated `exclusive_channel`. |
| `shipping` | Shipping configuration object. |

### Warranty (sale_terms)

```bash
# Get available sale terms for a category
GET https://api.mercadolibre.com/categories/$CATEGORY_ID/sale_terms
```

Common warranty attributes:
- `WARRANTY_TYPE`: "Garantía del vendedor", "Garantía de fábrica"
- `WARRANTY_TIME`: "90 días", "1 año", "6 meses"

---

## 6. Category System

### Browse Top-Level Categories (Mexico)

```bash
GET https://api.mercadolibre.com/sites/MLM/categories
```

Returns array of top-level categories:
```json
[
  {"id": "MLM1747", "name": "Accesorios para Vehículos"},
  {"id": "MLM1051", "name": "Celulares y Smartphones"},
  {"id": "MLM1648", "name": "Computación"},
  ...
]
```

### Get Category Details

```bash
GET https://api.mercadolibre.com/categories/$CATEGORY_ID
```

Returns:
- `id`, `name`
- `children_categories` — sub-categories
- `path_from_root` — full breadcrumb path
- `settings.max_title_length` — max chars for title
- `settings.listing_allowed` — whether listings can be created here

### Get Category-Specific Attributes

```bash
GET https://api.mercadolibre.com/categories/$CATEGORY_ID/attributes
```

**This is critical for listing creation.** Returns all attributes with:

```json
[
  {
    "id": "BRAND",
    "name": "Marca",
    "tags": {
      "required": true,
      "catalog_required": true
    },
    "hierarchy": "PARENT_PK",
    "relevance": 1,
    "value_type": "string",
    "value_max_length": 255,
    "values": [
      {"id": "206", "name": "Samsung"},
      {"id": "9344", "name": "Apple"}
    ]
  }
]
```

### Attribute Tags to Watch

| Tag | Meaning |
|-----|---------|
| `required` | Must be provided when creating a listing |
| `catalog_required` | Required for catalog participation |
| `read_only` | Auto-filled by MeLi, do not send |
| `hidden` | Not visible to buyers |
| `allow_variations` | Can have different values per variation |
| `defines_picture` | Variation attribute linked to pictures |

### Hierarchy Values

| Hierarchy | Meaning |
|-----------|---------|
| `PARENT_PK` | Main product identifier (e.g., Brand, Model). Same across family. |
| `CHILD_PK` | Variation identifier (e.g., Color, Size). Can vary. |

### Dump All Categories (Flat)

To get a flat list of all leaf categories:
```bash
GET https://api.mercadolibre.com/sites/MLM/categories/all
```

Returns a compressed file with all categories.

---

## 7. Category Predictor API

### Predict Category from Title

```bash
GET https://api.mercadolibre.com/sites/MLM/category_predictor/predict?title=Samsung+Galaxy+S23+128GB
```

### Response

```json
{
  "id": "MLM1055",
  "name": "Celulares y Smartphones",
  "prediction_class": "PREDICTED",
  "path_from_root": [
    {"id": "MLM1051", "name": "Celulares y Teléfonos"},
    {"id": "MLM1055", "name": "Celulares y Smartphones"}
  ]
}
```

### Enhanced Prediction with Domain & Attributes

For Global Selling / enhanced prediction:
```bash
GET https://api.mercadolibre.com/sites/MLM/category_predictor/predict?title=...
```

Response also includes:
- `domain_id` — Product domain (e.g., "MLM-CELLPHONES")
- `domain_name`
- `category_id`, `category_name`
- `attributes` — List of expected attributes

### Best Practice

1. Run the category predictor with the product title
2. Fetch attributes for the predicted category: `GET /categories/{id}/attributes`
3. Fill in all `required` and `catalog_required` attributes
4. Validate with `POST /items/validate`
5. Create listing with `POST /items`

---

## 8. Catalog System (Catálogo) — CRITICAL

### What is MeLi's Catalog?

The **catálogo** (catalog) is MeLi's **product-centric** listing system. Instead of each seller having their own product page, **multiple sellers compete on a single, curated product page**.

Think of it like **Amazon's product detail page + Buy Box system**.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Catalog Product** | A curated product page owned by MeLi (e.g., "iPhone 15 128GB Black") |
| **catalog_product_id** | Unique ID for a catalog product (e.g., "MLM15996654") |
| **Catalog Listing** | A seller's listing attached to a catalog product |
| **Buy Box** | The winning seller who gets the "Add to Cart" button on the product page |
| **Marketplace Listing** | Traditional individual listing (NOT in catalog) |
| **Product Page** | The unified page showing all sellers for one product |

### Catalog vs Traditional Listings

| Feature | Catalog Listing | Traditional Listing |
|---------|----------------|-------------------|
| Product page | Shared with other sellers | Unique per seller |
| Title | Set by MeLi (from product datasheet) | Set by seller |
| Images | Set by MeLi (from product datasheet) | Set by seller |
| Description | Provided by MeLi | Written by seller |
| Search visibility | **Higher** — appears in unified product page | Lower — individual listing |
| Competition | Buy Box algorithm | Individual listing ranking |
| Attributes | Auto-filled from catalog datasheet | Manually filled by seller |
| Requirements | Must match exact product | Flexible |

### Why Catalog Matters

1. **Massive visibility boost** — Catalog listings appear on unified product pages
2. **Buy Box winner** gets the primary "Buy" button
3. **Higher trust** — Buyers see standardized product info
4. **Expanding requirement** — More categories are making catalog **mandatory** (`catalog_required`)

### Listing Strategies per Category

Some categories have a `listing_strategy` field:

| Strategy | Meaning |
|----------|---------|
| `catalog_required` | MUST publish via catalog. Traditional listings rejected. |
| `catalog_optional` | Can publish either way. Catalog recommended. |
| (none) | Traditional listings only. |

### How to Check if Catalog is Required

```bash
GET https://api.mercadolibre.com/categories/$CATEGORY_ID
```

Look for `settings.catalog_product_id_required` or check the product search response for `listing_strategy`.

### Three Ways to Publish in Catalog

#### Method 1: Direct Catalog Listing (Preferred for Automation)

Post directly with `catalog_product_id` and `catalog_listing: true`:

```bash
curl -X POST \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "site_id": "MLM",
    "title": "Any title (will be overridden by catalog)",
    "category_id": "MLM1055",
    "price": 15999,
    "currency_id": "MXN",
    "available_quantity": 5,
    "buying_mode": "buy_it_now",
    "listing_type_id": "gold_special",
    "pictures": [],
    "attributes": [
      {"id": "ITEM_CONDITION", "value_id": "2230284", "value_name": "Nuevo"}
    ],
    "catalog_product_id": "MLM15996654",
    "catalog_listing": true
  }' \
  https://api.mercadolibre.com/items
```

**Key points:**
- `pictures` can be empty — catalog provides them
- `title` will be overridden by catalog product name
- Only need to send attributes not covered by catalog
- The `catalog_product_id` must be for an **active** catalog product
- **Seller is responsible** for ensuring their physical product matches the catalog datasheet

#### Method 2: Opt-in from Existing Marketplace Listing

Convert an existing listing to catalog:

```bash
curl -X POST \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "item_id": "MLM1477978125",
    "catalog_product_id": "MLM15996654"
  }' \
  https://api.mercadolibre.com/items/catalog_listings
```

For items with variations, include `variation_id`:
```json
{
  "item_id": "MLM1477978125",
  "variation_id": 174997747229,
  "catalog_product_id": "MLM15996654"
}
```

#### Method 3: Automatic Opt-in (Auto-optin)

MeLi may automatically associate your listing with a catalog product if your attributes match closely enough.

### Finding Catalog Products

#### Search by Keywords

```bash
GET https://api.mercadolibre.com/products/search?site_id=MLM&status=active&q=Samsung Galaxy S23 128GB Negro
```

Response:
```json
{
  "keywords": "Samsung Galaxy S23 128GB Negro",
  "paging": {"total": 3, "limit": 10, "offset": 0},
  "results": [
    {
      "id": "MLM15996654",
      "status": "active",
      "domain_id": "MLM-CELLPHONES",
      "settings": {"listing_strategy": "catalog_required"},
      "name": "Samsung Galaxy S23 128 Gb Negro 8 Gb Ram",
      "attributes": [...],
      "pictures": [...]
    }
  ]
}
```

#### Search by Product Identifier (GTIN/EAN/UPC)

```bash
GET https://api.mercadolibre.com/products/search?site_id=MLM&product_identifier=8806094967128
```

### Parameters for Product Search

| Parameter | Required | Description |
|-----------|----------|-------------|
| `site_id` | Yes | Country code (MLM) |
| `q` | Yes (if no product_identifier) | Search keywords — be specific! |
| `product_identifier` | Yes (if no q) | GTIN/EAN/UPC/ISBN |
| `status` | No | `active` or `inactive` (default: all) |
| `domain_id` | No | Filter by domain (e.g., MLM-CELLPHONES) |
| `offset` | No | Pagination offset |
| `limit` | No | Results per page |

### Catalog Eligibility

#### Check if an Item is Eligible for Catalog

```bash
GET https://api.mercadolibre.com/items/$ITEM_ID/catalog_listing_eligibility
```

#### Find All Eligible Items for a Seller

```bash
GET https://api.mercadolibre.com/users/$USER_ID/items/search?tags=catalog_listing_eligible
```

#### Filter Catalog vs Non-Catalog Items

```bash
# Catalog items only
GET https://api.mercadolibre.com/users/$USER_ID/items/search?catalog_listing=true

# Traditional items only
GET https://api.mercadolibre.com/users/$USER_ID/items/search?catalog_listing=false
```

### Eligibility Requirements

To participate in catalog, a listing generally must:
1. Condition: **new** (used items cannot be in catalog)
2. Match an existing **active** catalog product
3. Have correct attributes matching the catalog product's datasheet
4. Meet quality standards (good images, etc.)
5. For CELLPHONES domain: phone must be "released" (not pre-release)

### Catalog Competition (Buy Box)

#### How the Buy Box Works

An algorithm determines the winner based on:
1. **Price** — Lower is better
2. **Interest-free installments** — Offering cuotas sin interes helps
3. **Fulfillment (Full) shipping** — MeLi warehouse = strong boost
4. **Free shipping** — Significant advantage
5. **Same-day shipping** — Additional boost
6. **Seller reputation** — Better reputation = advantage

#### Check Competition Status

```bash
GET https://api.mercadolibre.com/items/$ITEM_ID/price_to_win?siteId=MLM&version=v2
```

Response:
```json
{
  "item_id": "MLM901414479",
  "current_price": 12999,
  "currency_id": "MXN",
  "price_to_win": 11500,
  "boosts": [
    {"id": "same_day_shipping", "status": "boosted"},
    {"id": "fulfillment", "status": "opportunity"},
    {"id": "free_installments", "status": "opportunity"},
    {"id": "free_shipping", "status": "not_apply"},
    {"id": "shipping_collect", "status": "boosted"}
  ],
  "status": "competing",
  "visit_share": "minimum",
  "reason": [],
  "catalog_product_id": "MLM16107499",
  "winner": {
    "item_id": "MLM884484295",
    "price": 13499,
    "currency_id": "MXN",
    "boosts": [...]
  }
}
```

#### Competition Statuses

| Status | Meaning |
|--------|---------|
| `winning` | You have the Buy Box |
| `sharing_first_place` | Sharing the Buy Box with similar-condition sellers |
| `competing` | Active in competition but not winning |
| `listed` | In catalog but NOT competing (has `reason` for why) |

#### Boost Statuses

| Status | Meaning |
|--------|---------|
| `boosted` | You have this advantage active |
| `opportunity` | You could activate this for competitive advantage |
| `not_apply` | Not applicable to your listing |

#### Reasons for Not Competing

The `reason` array explains why a listing isn't competing. Common reasons:
- Low reputation
- Price too high
- Missing shipping options
- Quality issues

#### Subscribe to Competition Notifications

Use the **Item competition** webhook topic to receive real-time updates when your competition status changes.

### Catalog Product Details

```bash
GET https://api.mercadolibre.com/products/$PRODUCT_ID
```

Response includes:
- Complete product datasheet
- Official images
- `buy_box_winner` field showing current winning listing

---

## 9. Product Descriptions

### Format: PLAIN TEXT ONLY

**MeLi only accepts plain text descriptions.** No HTML, no rich formatting, no emojis.

- No bold, italic, or font changes
- **Line breaks:** Use `\n`
- No HTML tags (will cause validation error)
- No emojis (will cause validation error)
- Priority: If both HTML `text` and `plain_text` are provided, `plain_text` takes precedence

### Upload Description (After Item Creation)

Descriptions are uploaded **separately** from the item, as a POST to the item's description endpoint:

```bash
curl -X POST \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "plain_text": "Descripcion del producto aqui.\n\nCaracteristicas principales:\n- Material: Acero inoxidable\n- Peso: 500g\n- Garantia: 1 ano"
  }' \
  https://api.mercadolibre.com/items/$ITEM_ID/description
```

### Update Description

```bash
curl -X PUT \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "plain_text": "Updated description here"
  }' \
  https://api.mercadolibre.com/items/$ITEM_ID/description?api_version=2
```

Note: Must use `api_version=2` for PUT to get detailed error messages.

### Get Description

```bash
GET https://api.mercadolibre.com/items/$ITEM_ID/description
```

### Benefits of Plain Text

- Better search results ranking
- 5x faster page load
- Proper display on all devices (mobile, tablet, desktop)

### Best Practices for Spanish-Language Descriptions (Mexico)

1. **Lead with technical specs** — Put the most important data in the attributes (datasheet), not description
2. **Don't repeat datasheet info** — Description should supplement, not duplicate
3. **Organize hierarchically** — Use uppercase, hyphens, spacing, line breaks
4. **Be concise** — Read your own description for length
5. **Include differentiators** — What makes your product stand out vs competition
6. **No contact info** — MeLi prohibits sharing external contact methods
7. **Use Mexican Spanish** — Avoid Spain-specific or Argentinian terms if targeting Mexico

### For Catalog Listings

**Catalog listings use MeLi's description from the product datasheet.** The seller's description is secondary. The datasheet (attributes) is the primary source of product information.

### Title Optimization for MeLi Search

- Max title length varies by category (check `max_title_length` in category settings)
- Include: Brand + Model + Key Spec + Color/Size
- Example: "Samsung Galaxy S23 128 Gb Negro 8 Gb Ram"
- Don't use ALL CAPS
- Don't use special characters or symbols excessively
- Don't include words like "oferta", "promo", "envio gratis" in title

---

## 10. Image Upload API

### Method 1: Upload by Source URL (Simplest)

When creating an item, include image URLs directly:

```json
{
  "pictures": [
    {"source": "https://example.com/product-front.jpg"},
    {"source": "https://example.com/product-back.jpg"},
    {"source": "https://example.com/product-detail.jpg"}
  ]
}
```

MeLi will download and process the images.

### Method 2: Upload Binary First, Then Link (Recommended for Reliability)

**Step 1: Upload image**

```bash
curl -X POST \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'content-type: multipart/form-data' \
  -F 'file=@/path/to/product-image.jpg' \
  'https://api.mercadolibre.com/pictures/items/upload'
```

Response:
```json
{
  "id": "123-MLM456_112021",
  "variations": [
    {"size": "1920x1076", "url": "...F.jpg"},
    {"size": "500x280", "url": "...O.jpg"},
    {"size": "400x400", "url": "...C.jpg"}
  ]
}
```

**Step 2: Link to item** (when creating)

```json
{
  "pictures": [
    {"id": "123-MLM456_112021"},
    {"id": "456-MLM789_112021"}
  ]
}
```

Or link to existing item:
```bash
POST https://api.mercadolibre.com/items/$ITEM_ID/pictures
{
  "id": "123-MLM456_112021"
}
```

### Image Specifications

| Spec | Value |
|------|-------|
| **Max file size** | 10 MB |
| **Supported formats** | JPG, JPEG, PNG |
| **Minimum resolution** | 500 x 500 px |
| **Maximum resolution** | 1920 x 1920 px (F version). Larger images are resized down. |
| **Recommended** | 1200 x 1200 px (enables zoom widget) |
| **Color space** | RGB (recommended over CMYK) |
| **Zoom activation** | Images wider than 800px enable zoom on hover |
| **Max images per item** | Varies by category |

### Image Processing by MeLi

MeLi automatically:
- Generates multiple size versions (F=full, O=original, C=crop, I=thumbnail)
- Applies **smart crop** — removes excess white background, keeping 10% margin
- Rejects images below minimum size after smart crop processing
- Returns HTTP 400 with detailed message if image is invalid

### Replacing Pictures

```bash
curl -X PUT \
  -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "pictures": [
      {"id": "new-picture-id-1"},
      {"id": "new-picture-id-2"}
    ]
  }' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

**Important:** To remove an image, simply omit its ID from the pictures array in the PUT.

### Image Order

The order of images in the `pictures` array determines display order. First image = main/thumbnail image.

### Rate Limits for Images

The `/pictures/items/upload` endpoint has a **separate RPM quota per app_id**. HTTP 429 means you've exceeded the quota.

---

## 11. Listing Types & Pricing

### Listing Types Available for Mexico (MLM)

| ID | Name | Description |
|----|------|-------------|
| `gold_pro` | **Premium** | Highest exposure. Buyer-friendly installments. Higher fees but best conversion. |
| `gold_special` | **Classic** | Standard visibility. Pay only selling fee. Good cost/exposure balance. |
| `free` | **Free** | No selling fee. **Limited to 10 active listings.** Lowest exposure. |

### Check Available Listing Types

```bash
GET https://api.mercadolibre.com/sites/MLM/listing_types
```

### Listing Type Comparison

| Feature | `free` | `gold_special` (Classic) | `gold_pro` (Premium) |
|---------|--------|-------------------------|---------------------|
| Selling fee | None | Commission only | Commission + installment cost |
| Active listing limit | 10 | **Unlimited** | **Unlimited** |
| Search exposure | Lowest | High (`highest`) | Highest |
| Requires pictures | No | Yes | Yes |
| Max stock per item | 99,999 | 99,999 | 99,999 |
| Duration | 60 days (auto-renew) | ~20 years | ~20 years |
| Payment | MercadoPago mandatory | MercadoPago mandatory | MercadoPago mandatory |
| Installments | Bank interest only | Bank interest only | Seller-funded interest-free |

### Commission Structure (Comisiones)

#### Check Selling Fees

```bash
GET https://api.mercadolibre.com/sites/MLM/listing_prices?price=$PRICE&listing_type_id=$TYPE&category_id=$CAT
```

Or get listing type configuration:
```bash
GET https://api.mercadolibre.com/sites/MLM/listing_types/gold_special
```

Response includes:
```json
{
  "id": "gold_special",
  "configuration": {
    "name": "Clásica",
    "listing_exposure": "highest",
    "requires_picture": true,
    "max_stock_per_item": 99999,
    "sale_fee_criteria": {
      "percentage_of_fee_amount": 13,
      "currency": "MXN"
    }
  }
}
```

#### Typical Commission Ranges (Mexico)

- **Classic (`gold_special`):** ~13-17.5% selling fee (varies by category)
- **Premium (`gold_pro`):** Selling fee + installment subsidization cost
- **Free:** No fee (limited listings)

**Note:** Exact commissions vary by:
- Category
- Listing type
- Product price
- Shipping method (Fulfillment sellers may get different rates)
- Seller reputation level

For current fees: https://www.mercadolibre.com.mx/ayuda/Costos-de-vender-un-producto_870

### Competitive Pricing

#### Price to Win (Catalog)

```bash
GET https://api.mercadolibre.com/items/$ITEM_ID/price_to_win?siteId=MLM&version=v2
```

Returns `price_to_win` — the price you need to beat the current winner.

#### Automated Pricing Campaigns

MeLi offers automated co-participation and competitive pricing campaigns:
- https://global-selling.mercadolibre.com/devsite/automated-co-participation-and-competitive-pricing-campaign
- Price discount campaigns
- Volume discount campaigns

---

## 12. Shipping (Mercado Envios)

### Shipping Modes

| Mode | Description |
|------|-------------|
| `me2` | **Mercado Envios 2** — MeLi manages shipping logistics |
| `me1` | Legacy mode (seller manages carrier directly) |
| `not_specified` | No shipping specified |
| `custom` | Custom shipping arrangement |

### Logistic Types (within ME2)

| Type | Code | Description |
|------|------|-------------|
| Drop-off | `drop_off` | Seller prints label, drops at post office |
| Colecta | `cross_docking` | MeLi picks up from seller |
| Places | `xd_drop_off` | Seller drops at MeLi collection point |
| Flex | `self_service` | Seller delivers locally |
| **Fulfillment (Full)** | `fulfillment` | **MeLi warehouses & ships** — Best for Buy Box! |

### Setting Shipping on a Listing

```json
{
  "shipping": {
    "mode": "me2",
    "local_pick_up": false,
    "free_shipping": false,
    "free_methods": []
  }
}
```

For free shipping:
```json
{
  "shipping": {
    "mode": "me2",
    "local_pick_up": false,
    "free_shipping": true
  }
}
```

### Package Dimensions

Dimensions are **stipulated by MeLi based on category** and cannot be manually set by sellers.

Check category shipping preferences:
```bash
GET https://api.mercadolibre.com/categories/$CATEGORY_ID/shipping_preferences
```

### Shipping Preferences

```bash
GET https://api.mercadolibre.com/users/$USER_ID/shipping_preferences
```

Returns what shipping modes and logistic types are available for the seller.

### Fulfillment (Mercado Envios Full)

Using Fulfillment gives **massive advantages** for the Buy Box. Available in MLM (Mexico).

Requires:
1. Seller must be approved for Fulfillment
2. Ship inventory to MeLi warehouses
3. MeLi handles storage, picking, packing, shipping

---

## 13. User Products — New Model

### What Are User Products (UP)?

**User Products** is MeLi's new publishing model being rolled out starting October 2024 (Argentina, Mexico first). This is the future of how listings work.

### Problem It Solves

Old model limitations:
- Cannot set different prices per variation
- Cannot configure different shipping per variation
- Cannot apply promotions to specific variations

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Item** | A listing visible to buyers. Contains sales conditions (price, installments). |
| **User Product (UP)** | A physical product at the most specific level (variation level). Has `user_product_id`. |
| **Family** | Auto-generated grouping of UPs with same main attributes. Like a parent listing. |
| **UPP** | User Products Page — the display of a family with all its variations and conditions. |

### How It Works

- A **User Product** (e.g., "Red iPhone 15 128GB") can be associated with **multiple items** (different sales conditions)
- UPs in the same family share `PARENT_PK` attributes (Brand, Model)
- `CHILD_PK` attributes (Color, Size) can vary between UPs
- Changes to one item's UP attributes sync to ALL items sharing that UP

### Synchronized Fields

When you modify an item, these fields sync across all items sharing the same UP:
- title, family_name, attributes, pictures, domain_id, catalog_product_id, condition, available_quantity

### Impact on Pipeline

For new integrations, you should be aware of the UP model. However, the traditional `POST /items` flow still works. MeLi creates UPs automatically behind the scenes.

---

## 14. Webhooks & Notifications

### Available Webhook Topics

| Topic | Description |
|-------|-------------|
| `items` | Changes to published items |
| `questions` | Questions asked or answered |
| `payments` | Payment creation and status changes |
| `messages` | New messages received |
| `orders_v2` | Creation/changes to confirmed sales |
| `shipments` | Shipping creation and changes |
| `orders_feedback` | Feedback creation/changes |
| `claims` | Sales claims |
| `item_competition` | **Catalog competition status changes** |
| `public_offers` | Offer status changes |
| `stock_locations` | Stock location modifications |
| `catalog_suggestions` | Catalog product suggestion status changes |
| `stock_fulfillment` | Fulfillment stock operations |
| `items_prices` | Price creation/update/deletion |

### Key Topics for Listing Pipeline

- **`item_competition`** — Know when you win/lose the Buy Box
- **`items`** — Track listing status changes
- **`items_prices`** — Monitor price changes
- **`catalog_suggestions`** — Track catalog association suggestions

### Notification Format

Webhooks are sent as HTTP POST requests to your configured endpoint. MeLi uses a **secret signature** for validation.

### Notification Simulator

MeLi provides a notifications simulator for testing webhook handling.

---

## 15. Bulk Operations

### No Official Bulk Create API

MeLi does **not provide** a single endpoint to create multiple listings at once. Each listing requires an individual `POST /items` call.

### Strategies for Bulk Listing

1. **Sequential API calls** with rate limiting (stay under 1,500 RPM)
2. **Parallel requests** with concurrency control (recommend 5-10 concurrent)
3. **Queue-based system** — Push items to a queue, process at controlled rate
4. **Validate first** — Use `POST /items/validate` to catch errors before creating

### Spreadsheet/CSV Upload

MeLi's seller dashboard provides spreadsheet upload for bulk listing, but this is a **frontend feature**, not an API.

### Bulk Image Upload

No bulk endpoint. Upload images individually via `POST /pictures/items/upload` then reference by ID.

### Practical Rate Plan

```
1,500 RPM limit
= 25 requests/second
= ~1,500 items per minute (if 1 request per item with pre-uploaded images)
= ~90,000 items per hour (theoretical max)
```

Realistic with validation + description + images:
- ~3-5 API calls per listing (validate, create, upload desc, upload images)
- ~300-500 complete listings per minute
- ~18,000-30,000 per hour

---

## 16. Key API Endpoints Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/oauth/token` | Get/refresh access token |

### Items (Listings)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items` | Create a new listing |
| POST | `/items/validate` | Validate listing data without creating |
| GET | `/items/{item_id}` | Get item details |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete/close an item |
| POST | `/items/{item_id}/description` | Add description to item |
| PUT | `/items/{item_id}/description?api_version=2` | Update description |
| GET | `/items/{item_id}/description` | Get item description |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/MLM/categories` | Get top-level categories (Mexico) |
| GET | `/categories/{category_id}` | Get category details |
| GET | `/categories/{category_id}/attributes` | Get category attributes |
| GET | `/categories/{category_id}/sale_terms` | Get available sale terms |
| GET | `/categories/{category_id}/shipping_preferences` | Get shipping config |
| GET | `/sites/MLM/category_predictor/predict?title=...` | Predict category |
| GET | `/sites/MLM/categories/all` | Dump all categories |

### Catalog

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/search?site_id=MLM&q=...` | Search catalog products |
| GET | `/products/search?site_id=MLM&product_identifier=...` | Search by GTIN/EAN |
| GET | `/products/{product_id}` | Get catalog product details |
| POST | `/items/catalog_listings` | Opt-in existing item to catalog |
| GET | `/items/{item_id}/catalog_listing_eligibility` | Check catalog eligibility |
| GET | `/users/{user_id}/items/search?catalog_listing=true` | List catalog items |
| GET | `/users/{user_id}/items/search?tags=catalog_listing_eligible` | Find eligible items |

### Competition

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items/{item_id}/price_to_win?siteId=MLM&version=v2` | Get competition details |

### Images

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/pictures/items/upload` | Upload image (multipart) |
| POST | `/items/{item_id}/pictures` | Link picture to item |

### Users & Limits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user info |
| GET | `/marketplace/users/cap` | Get listing limits |
| GET | `/users/{user_id}/shipping_preferences` | Get shipping preferences |

### Listing Types & Pricing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/MLM/listing_types` | Get available listing types |
| GET | `/sites/MLM/listing_types/{type_id}` | Get listing type details |
| GET | `/sites/MLM/listing_prices?price=...` | Get pricing/fees |

---

## 17. Automated Pipeline Architecture

### Recommended Flow for Creating a Listing

```
1. AUTHENTICATE
   └── POST /oauth/token (or refresh existing token)

2. DETERMINE CATEGORY
   ├── Option A: GET /sites/MLM/category_predictor/predict?title=...
   └── Option B: Use pre-mapped category from your database

3. GET REQUIRED ATTRIBUTES
   └── GET /categories/{category_id}/attributes
       └── Filter for tags.required = true

4. SEARCH CATALOG (if applicable)
   ├── GET /products/search?site_id=MLM&q=... (by name)
   └── GET /products/search?site_id=MLM&product_identifier=... (by GTIN)
       └── If catalog product found → use catalog_product_id

5. UPLOAD IMAGES
   ├── POST /pictures/items/upload (for each image)
   └── Collect picture IDs

6. VALIDATE
   └── POST /items/validate (with full item body)
       └── Fix any validation errors

7. CREATE LISTING
   ├── Option A (Catalog): POST /items with catalog_product_id + catalog_listing=true
   └── Option B (Traditional): POST /items with all fields

8. ADD DESCRIPTION
   └── POST /items/{item_id}/description

9. VERIFY
   └── GET /items/{item_id} (confirm listing is active)

10. MONITOR COMPETITION (for catalog)
    └── GET /items/{item_id}/price_to_win?siteId=MLM&version=v2
```

### Catalog-First Strategy

For products that exist in MeLi's catalog:

```python
# Pseudocode for catalog-first listing pipeline
def create_listing(product):
    # 1. Search catalog by GTIN first
    if product.gtin:
        catalog = search_catalog(product_identifier=product.gtin)
    else:
        catalog = search_catalog(q=product.full_name)

    if catalog.results:
        # Direct catalog listing
        item = post_item(
            catalog_product_id=catalog.results[0].id,
            catalog_listing=True,
            price=product.price,
            available_quantity=product.stock,
            listing_type_id="gold_special"
        )
    else:
        # Traditional listing with full attributes
        category = predict_category(product.title)
        attributes = get_required_attributes(category.id)
        images = upload_images(product.images)
        item = post_item(
            title=product.title,
            category_id=category.id,
            price=product.price,
            pictures=images,
            attributes=fill_attributes(attributes, product),
            ...
        )

    # Add description
    add_description(item.id, product.description)

    return item
```

### Error Handling

Common validation errors:
- `item.category_id.invalid` — Wrong/non-leaf category
- `item.title.max_length` — Title too long for category
- `item.pictures.min` — Not enough pictures for listing type
- `item.description.type.invalid` — HTML or emoji in description
- `item.attribute.missing` — Required attribute not provided
- `item.attribute.invalid_value` — Attribute value not in allowed list

---

## Source URLs

### Official Documentation
- https://developers.mercadolibre.com.mx (Mexico developer portal)
- https://developers.mercadolibre.com.ar/en_us (Argentina — most complete, English)
- https://global-selling.mercadolibre.com/devsite (Global Selling / CBT)

### Specific Guides
- Authentication: https://developers.mercadolibre.com.ar/en_us/authentication-and-authorization
- List Products: https://developers.mercadolibre.com.ar/en_us/list-products
- Categories & Attributes: https://developers.mercadolibre.com.ar/en_us/categories-attributes
- Item Description: https://developers.mercadolibre.com.ar/en_us/item-description-2
- Catalog Listing: https://developers.mercadolibre.com.ar/en_us/catalog-listing
- Catalog Eligibility: https://developers.mercadolibre.com.ar/en_us/catalog-eligibility
- Product Search: https://developers.mercadolibre.com.ar/en_us/products-search
- Catalog Competition: https://developers.mercadolibre.com.ar/en_us/catalog-competition
- Image Upload: https://global-selling.mercadolibre.com/devsite/pictures
- Mercado Envios 2: https://developers.mercadolibre.com.ar/en_us/mercadoenvios-mode-2
- Listing Types: https://global-selling.mercadolibre.com/devsite/listing-types-and-exposures
- User Products: https://developers.mercadolibre.com.ar/en_us/user-products
- Token Best Practices: https://global-selling.mercadolibre.com/devsite/authorization-and-token-best-practices

### Community / GitHub
- Official GitHub: https://github.com/mercadolibre
- Python SDK (deprecated): https://github.com/mercadolibre/python-sdk
- MCP Server: https://global-selling.mercadolibre.com/devsite/mcp-server-from-mercado-libre
