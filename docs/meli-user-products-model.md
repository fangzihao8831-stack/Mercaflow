# MercadoLibre User Products (UP) Model API

Source: https://developers.mercadolibre.com.ar/en_us/user-products

## Overview

User Product (UP) is MeLi's new listing model that allows different sales conditions per variant of the same product (different prices, shipping methods, promotions per variant).

## Why User Products?

Old model limitations:
- Cannot set different prices per variant
- Cannot configure different shipping per variant
- Cannot apply specific promotions to one variant

UP model solves this by decoupling sales conditions from variants.

## Key Concepts

### Item
- Representation of a product listing buyers see
- Contains sales conditions (price, installments)
- Has unique item_id

### User Product (UP)
- Represents a physical product the seller owns
- Describes product at the most specific level (variation level)
- Has unique user_product_id (auto-assigned)
- Can be associated with 1 or more items
- Example: Red iPhone (UP) can have item1 with 3 installments and item2 with different price

### Family
- Auto-generated based on product info
- Groups several UPs together
- Items in same family share family_name
- Grouped by PARENT_PK attributes (must match)
- CHILD_PK and custom attributes allow varying values

### Family Fields
- Name (family_name if exists, otherwise name)
- Domain_id
- User_id
- Attributes: PARENT_PK, CHILD_PK, Custom, Item Condition

## Key Endpoints

### Get User Product Details
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/user-products/$USER_PRODUCT_ID
```

### Get Family Members
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/sites/$SITE_ID/user-products-families/$FAMILY_ID
```

### Get Items for a User Product
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/users/$SELLER_ID/items/search?user_product_id=$UP_ID
```
Can send multiple: `user_product_id=MLAU1234,MLAU12345`

### Check if Seller is UP-enabled
Look for `"user_product_seller"` tag in `/users` API response.

### Check if Item is in UP Model
Validate if item has `family_name != null`.

## UPtin (Migration to UP)

When seller gets "user_product_seller" tag:
1. Single-variant and non-variant items auto-migrate
2. Multi-variant items need explicit migration via UPtin

### Check UPtin Eligibility
Use eligibility endpoint to validate if item can be migrated.

### UPtin Migration Results
- Old item gets status: closed
- New items get tag: "variations_migration_uptin"
- Notification sent for each new item via items topic
- sold_quantity reflects variant's sales
- Old orders remain with old item_id

## Synchronized Fields

When modifying a UP item via PUT /items, these fields sync to all items of same UP:
- title
- family_name
- attributes
- pictures
- domain_id
- catalog_product_id
- condition
- available_quantity

## Important Rules

- After seller activation, CANNOT publish with old model (variations array)
- family_name max length = domain's max_title_length
- family_name updatable only when NO items of the UP have sales
- Catalog items do NOT get user_product_listing tag
- Custom attributes supported in new model

## Initiatives

1. **Price per Variation** — Different prices per variant
2. **Distributed Stock** — Stock across locations
3. **Multi-origin Stock** — Multiple warehouse origins

## Timeline

- October 2024: Progressive seller enablement
- 2025: 100% of sellers enabled
- Test form: https://docs.google.com/forms/d/e/1FAIpQLSfC3RVMKKDrTU0vVVOC_TsbidG_ImvKMLggkB3004hrr0eMqw/viewform
