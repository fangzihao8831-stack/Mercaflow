# MercadoLibre Update/Modify Items API

Source: https://developers.mercadolibre.com.ar/en_us/products-sync-listings

## Overview

Update and modify active listings: stock, price, description, pictures, status, and more.

## What Can Be Updated

### When item is **active**:
- available_quantity (stock)
- price
- video
- pictures
- description
- shipping

### When item **has sales** (sold_quantity > 0), CANNOT change:
- title
- condition
- buying_mode

### When item **has NO sales** (sold_quantity = 0), CAN change:
- title

## Basic Update (PUT /items/{id})

```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your new title",
    "price": 1000
  }' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

## Update Stock

```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H "Content-Type: application/json" \
  -d '{"available_quantity": 6}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

**Auto-pause behavior** (MLB, MLA, MLM, MLC, MPE, MLV):
- PUT available_quantity = 0 → status changes to "paused" with out_of_stock sub-status
- PUT available_quantity > 0 when out_of_stock → status changes to "active"
- Item with available_quantity = 0 can only be paused when condition = new and listing_type != free

## Listing Status Flow

```
Active → Payment Required → Under Review → Paused → Closed → Inactive
```

### Status Values

| Status | Description |
|--------|-------------|
| **active** | Listing is active, receives bids/questions |
| **payment_required** | Debtor user listing, reactivated after payment |
| **under_review** | Under MeLi review (warning, waiting_for_patch, held, pending_documentation, forbidden) |
| **paused** | Auto (out_of_stock) or manual (paused_by_seller) |
| **closed** | Final status (expired, deleted, suspended, freezed) |
| **inactive** | Failed to correct under_review issues |

### Change Status

**Close listing** (permanent):
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"status":"closed"}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

**Pause listing**:
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"status":"paused"}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

**Reactivate paused listing**:
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"status":"active"}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

## Delete Listing (2-step)

1. Close first:
```bash
curl -X PUT -d '{"status": "closed"}' https://api.mercadolibre.com/items/$ITEM_ID
```

2. Then delete:
```bash
curl -X PUT -d '{"deleted":"true"}' https://api.mercadolibre.com/items/$ITEM_ID
```

Note: For items with status "under_review" and substatus "forbidden", only execute step 2.

## Manufacturing Time (MANUFACTURING_TIME sale_term)

Available in: Argentina, Brasil, Uruguay, Colombia, Mexico. Max 45 days.

### Check if category supports it:
```bash
curl -X GET https://api.mercadolibre.com/categories/$CATEGORY_ID/sale_terms
```

### Create item with manufacturing time:
```json
{
  "sale_terms": [{
    "id": "MANUFACTURING_TIME",
    "value_name": "20 dias"
  }]
}
```

### Update manufacturing time:
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"sale_terms": [{"id": "MANUFACTURING_TIME", "value_name": "30 dias"}]}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

### Delete manufacturing time:
```bash
curl -X PUT -d '{"sale_terms": [{"id": "MANUFACTURING_TIME", "value_id": null, "value_name": null}]}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

## Maximum Purchase Quantity

```bash
curl -X PUT -d '{"sale_terms": [{"id": "PURCHASE_MAX_QUANTITY", "value_name": "10"}]}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

## Sale Terms Available

| Sale Term | Description |
|-----------|-------------|
| INVOICE | Billing type (Factura A/B/C/No factura) |
| WARRANTY_TYPE | Warranty type (seller/factory/none) |
| WARRANTY_TIME | Warranty duration (days/months/years) |
| MANUFACTURING_TIME | Stock availability time (max 45 days) |
| PURCHASE_MAX_QUANTITY | Max units per purchase |
| SUBSCRIBABLE | Subscription enabled |
| PRICE_SUBSCRIPTION | Subscription price |
| LOYALTY_LEVEL_1-6 | Loyalty tier pricing |

## Key Endpoints Summary

| Method | Endpoint | Action |
|--------|----------|--------|
| PUT | /items/{id} | Update item fields |
| PUT | /items/{id} | Change status (active/paused/closed) |
| PUT | /items/{id} | Delete (set deleted: true) |
| GET | /categories/{id}/sale_terms | Get available sale terms |
