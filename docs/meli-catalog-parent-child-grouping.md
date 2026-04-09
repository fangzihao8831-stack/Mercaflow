# MeLi Catalog: Parent-Child Product Grouping

## Source
- https://developers.mercadolibre.com.ar/en_us/products-search
- https://developers.mercadolibre.com.ar/en_us/domains-and-products
- https://developers.mercadolibre.com.hn/en_us/items-and-searches/user-products

## Key Concepts

### Catalog Products (Old System)
- Products have a **parent-child hierarchy** controlled entirely by MeLi
- **Parent products** = generic (e.g., "Apple iPhone 13") — NOT purchasable
  - Have `children_ids` array with specific product IDs
  - `parent_id` = null
  - Status is never "active"
- **Child products** = specific variants (e.g., "Apple iPhone 13 128GB RED") — purchasable
  - Have `parent_id` pointing to parent
  - `children_ids` = empty array
  - Can have `status: "active"`

### Can Sellers Control Parent-Child Grouping?
**NO.** MeLi controls this entirely. There is NO seller API to:
- Create parent products
- Force child products to be grouped under a specific parent
- Modify the parent-child relationship

### How Grouping Works
Attributes with `hierarchy: "PARENT_PK"` determine grouping:
- **BRAND** — must match
- **MODEL** — must match
- **Domain** — must match

Attributes with `hierarchy: "CHILD_PK"` create variants:
- **COLOR** — can differ
- **INTERNAL_MEMORY** — can differ
- **SIZE** — can differ

### Pickers
Child products under the same parent appear as **pickers** on the product page:
```json
"pickers": [
  {
    "picker_id": "INTERNAL_MEMORY",
    "picker_name": "Memoria interna",
    "products": [
      {"product_id": "MLA18500852", "picker_label": "128 GB"},
      {"product_id": "MLA18500853", "picker_label": "256 GB"}
    ]
  },
  {
    "picker_id": "COLOR",
    "picker_name": "Color",
    "products": [
      {"product_id": "MLA18500852", "picker_label": "(Product)Red"},
      {"product_id": "MLA18500846", "picker_label": "Azul"}
    ]
  }
]
```

## User Products (New System — Replacing Catalog for Sellers)

### What Are User Products (UP)?
A new model being rolled out to all sellers (target: 100% by end of 2025):
- Each UP represents a physical product at the variation level
- UPs are grouped into **families** (auto-generated)
- Items in the same family appear as different **pickers** in the User Products Page (UPP)

### Family Grouping Rules
To group UPs into a family, these fields are considered:
1. **Name** (family_name has priority over name)
2. **Domain_id**
3. **User_id**
4. **Attributes:**
   - PARENT_PK — values must match across family
   - CHILD_PK — only id and name contribute (values can vary)
   - Custom Attributes — only id and name contribute
   - Item Condition
   - Note: read_only attributes are NOT considered

### Key Differences from Old Catalog
- UP allows **different prices per variant**
- UP allows **different shipping methods per variant**
- UP allows **specific promotions per variant**
- Seller controls the `family_name`
- Seller tag: `user_product_seller`

### API Endpoints for User Products
```
GET /items/{item_id}                          → get user_product_id
GET /user-products/{user_product_id}          → get family_id
GET /sites/{site_id}/user-products-families/{family_id}  → all UPs in family
GET /users/{seller_id}/items/search?user_product_id={id} → all items for UP
```

### Detection
- Seller enabled: check for `user_product_seller` tag in `/users` API
- Item in new model: `family_name` is not null
- Catalog items do NOT get `user_product_listing = true` tag

## Strategy for MercaFlow
1. Search for existing catalog product using `/products/search?q=...&site_id=MLM`
2. If found active child product → use its `catalog_product_id` to create catalog listing
3. If only parent found → search among `children_ids` for exact match
4. If no match → publish as marketplace item, wait for MeLi to create product
5. Submit multiple items with same PARENT_PK, different CHILD_PK → hope MeLi groups them
6. For User Products model: set same `family_name` + matching PARENT_PK attributes
