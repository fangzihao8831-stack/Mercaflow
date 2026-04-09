# MercadoLibre Prices API

Source: https://developers.mercadolibre.com.ar/en_us/price-apl

## Overview

Dedicated API for querying item prices across channels. MeLi is phasing out price, base_price, and original_price fields from /items API. Use /prices endpoints instead.

## Price Notifications

Subscribe to `items_prices` topic, then query /prices resource after notification.

## Get Current Sales Price

Returns the winning price shown to buyers, filterable by channel and loyalty level.

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items/$ITEM_ID/sale_price?context=$CHANNEL,$LOYALTY_LEVEL
```

### Context Parameters

**Channels:**
- channel_marketplace — Mercado Libre
- channel_proximity, mp_merchants, mp_links — MercadoPago channels (coming soon)

**Loyalty Levels** (not available in MLU, MPE):
- buyer_loyalty_3
- buyer_loyalty_4
- buyer_loyalty_5
- buyer_loyalty_6

### Response
```json
{
  "price_id": "1",
  "amount": 800,
  "regular_amount": null,
  "currency_id": "BRL",
  "reference_date": "2023-02-15T00:23:53Z"
}
```

Fields:
- **amount**: Current selling price
- **regular_amount**: Original price if promotional (strikethrough price)
- **promotion_id**: If active promotion, the promotion ID
- **promotion_type**: Type of promotion

## Get All Item Prices

Returns all price types across all channels:

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items/$ITEM_ID/prices
```

### Response
```json
{
  "id": "MLB3191390879",
  "prices": [
    {
      "id": "1",
      "type": "standard",
      "amount": 800,
      "regular_amount": null,
      "currency_id": "BRL",
      "last_updated": "2023-02-14T18:43:58Z",
      "conditions": {
        "context_restrictions": ["channel_marketplace"],
        "start_time": null,
        "end_time": null
      }
    },
    {
      "id": "2",
      "type": "standard",
      "amount": 650,
      "currency_id": "BRL",
      "conditions": {
        "context_restrictions": ["channel_mshops"]
      }
    }
  ]
}
```

## Price Types
- **standard**: Seller-defined price without promotions
- **promotion**: Promotional price (coming soon to API)

## Price Fields

| Field | Description |
|-------|-------------|
| id | Price ID |
| type | "standard" or "promotion" |
| amount | Price value |
| regular_amount | Original price (if promotional) |
| currency_id | Currency |
| last_updated | Last modification date |
| conditions.context_restrictions | Channel/loyalty restrictions |
| conditions.start_time/end_time | Price validity period |

## Promotion Price Behavior

When promotion is **active**:
- Lowering price below offer removes the promotion
- Lowering price but staying above promotion keeps it active

When promotion is **scheduled**:
- Price changes won't affect scheduled promotion
- DEALS price updates take effect at scheduled date

## Important Notes

- To CREATE or UPDATE prices, still use PUT /items API
- Separate price editing (outside /items) coming soon
- Only CUSTOM and PRICE_DISCOUNT offers reported as custom
- Subscribe to items_prices topic for real-time price changes
