# MercadoLibre Fulfillment / Mercado Envios Full API

Source: https://developers.mercadolibre.com.ar/en_us/fulfillment

## Overview

With Fulfillment (Mercado Envios Full), seller products are stored in MeLi warehouses and all logistics are handled by MeLi. Inbounding is done via Seller Center (frontend). APIs allow querying stock and operations.

Available in: Argentina, Brazil, Mexico, Chile, Colombia.

## Get inventory_id

The inventory_id identifies the item in fulfillment. Get it from /items:

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

Response includes `"inventory_id": "LCQI05831"`. When item has variations, each variation has its own inventory_id.

## Check Fulfillment Stock

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/inventories/$INVENTORY_ID/stock/fulfillment
```

Response:
```json
{
  "inventory_id": "LCQI05831",
  "total": 20,
  "available_quantity": 5,
  "not_available_quantity": 15,
  "not_available_detail": [
    {"status": "damage", "quantity": 2},
    {"status": "lost", "quantity": 1},
    {"status": "noFiscalCoverage", "quantity": 5},
    {"status": "withdrawal", "quantity": 5},
    {"status": "internal_process", "quantity": 1},
    {"status": "transfer", "quantity": 1}
  ],
  "external_references": [
    {"type": "item", "id": "MLB1557246024", "variation_id": 4742223403}
  ]
}
```

### Stock Status Types
| Status | Description |
|--------|-------------|
| damaged | Damaged items (seller, meli, carrier) |
| lost | Lost and not found |
| withdrawal | Reserved for seller pickup |
| internal_process | Reserved by warehouse quality |
| transfer | Reserved for warehouse transfer |
| noFiscalCoverage | No tax coverage (Brazil) |
| not_supported | Unidentifiable/unprocessable items |

## Fulfillment Stock Notifications

Subscribe to `fbm_stock` topic in app settings.

## Consult Operations

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/stock/fulfillment/operations/search?seller_id=$SELLER_ID&inventory_id=$INVENTORY_ID&date_from=2020-06-01&date_to=2020-06-30
```

### Filter Parameters
| Parameter | Description |
|-----------|-------------|
| seller_id | Seller identifier (required) |
| inventory_id | Comma-separated list |
| date_from | Search start date (default: 15 days ago) |
| date_to | Search end date (default: today) |
| type | Operation type (inbound_reception, sale_confirmation, etc.) |
| external_references.shipment_id | Shipment ID |
| limit | Results per page (max 1000) |

### Operation Types

**Inbound:**
- inbound_reception — Stock reception
- fiscal_coverage_adjustment — Tax coverage adjustment (Brazil)

**Outbound:**
- sale_confirmation — Reserve units for sale
- sale_cancelation — Cancel sale reservation
- sale_delivery_cancelation — Undelivered order
- sale_return — Buyer return

**Withdrawal:**
- withdrawal_reservation — Reserve for pickup
- withdrawal_cancelation — Cancel pickup
- withdrawal_delivery — Physical pickup
- withdrawal_discarded — Seller-requested removal

**Transfer:**
- transfer_reservation — Multi-warehouse transfer
- transfer_adjustment — Quality inspection restock
- transfer_delivery — Transfer receipt

**Quarantine:**
- quarantine_reservation — Quality inspection
- quarantine_restock — Restock after inspection
- lost_refund — Permanent lost cancellation

**Stock Adjustments:**
- adjustment — Internal adjustments
- identification_problem_remove/add — SKU correction

## Pagination

Uses scroll-based pagination:
- scroll_id expires in 5 minutes
- Default limit: 1000 (max 1000)
- scroll = null means no more results

## Key Errors

| Status | Error | Description |
|--------|-------|-------------|
| 404 | seller_product_not_found | Product not found |
| 400 | validation_error | Invalid parameter |
| 403 | forbidden | Not authorized |
| 429 | too_many_request | Rate limit exceeded |

## Important Notes

- Only last 12 months of data available
- Stock lookup returns data up to day-1
- Sending products to warehouse is done via Seller Center (not API)
- For creating fulfillment listings, set `available_quantity: 0` to create paused with out_of_stock
