# MercadoLibre Promotions API

Source: https://developers.mercadolibre.com.ar/en_us/manage-promotion

## Overview

The `/seller-promotions` resource centralizes all promotion types. Max discount: 80%.

## Promotion Types

| Campaign | Type Code | Price Definition | MeLi Bonus | Approval Required |
|----------|-----------|-----------------|------------|-------------------|
| Traditional | DEAL | User defines | No | Yes |
| Co-funded | MARKETPLACE_CAMPAIGN | User accepts | Yes | No |
| Volume discount | VOLUME | User accepts | Yes | No |
| Deal of the day | DOD | User defines (suggested) | No | No |
| Flash deal | LIGHTNING | User defines (suggested) | No | No |
| Pre-negotiated | PRE_NEGOTIATED | User accepts | Yes | No |
| Seller campaign | SELLER_CAMPAIGN | User defines | No | No |
| Auto co-funded | SMART | User accepts | Yes | No |
| Competitive pricing | PRICE_MATCHING | User accepts | Yes | No |
| Stock clearance | UNHEALTHY_STOCK | User accepts | Yes | No |
| Seller coupon | SELLER_COUPON_CAMPAIGN | User defines | No | No (MLB only) |

All types available for: MLA, MLB, MLM, MCO, MLC, MLU, MPE

## Key Endpoints

### List All Promotions for User
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/users/$USER_ID?app_version=v2
```

### List All Promotions for an Item
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/items/$ITEM_ID?app_version=v2
```

### Get Candidate Details
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/candidates/$CANDIDATE_ID?app_version=v2
```

### Get Offer Details
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/offers/$OFFERS_ID?app_version=v2
```

### Get Promotion Items
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/promotions/$PROMOTION_ID/items?promotion_type=$TYPE&app_version=v2
```

### Create Price Discount
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{
    "deal_price": $DEAL_PRICE,
    "top_deal_price": $TOP_DEAL_PRICE,
    "start_date": "$START_DATE",
    "finish_date": "$FINISH_DATE",
    "promotion_type": "PRICE_DISCOUNT"
  }' \
  https://api.mercadolibre.com/seller-promotions/items/$ITEM_ID?app_version=v2
```

### Bulk Delete All Offers on Item
```bash
curl -X DELETE -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/items/$ITEM_ID?app_version=v2
```

## Filters for Item Queries

| Parameter | Values |
|-----------|--------|
| **item_id** | Filter by specific item |
| **status** | started, pending, candidate |
| **status_item** | active, paused |

## Pagination

Use `search_after` parameter (not offset). Max limit: 50 per page.
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/seller-promotions/promotions/$ID/items?promotion_type=$TYPE&app_version=v2&limit=50&search_after=$SEARCH_AFTER'
```

Notes:
- search_after returned on all pages except last
- Has TTL of 5 minutes
- No backward pagination

## Response Fields

| Field | Description |
|-------|-------------|
| id | Promotion identifier |
| type | Promotion type code |
| status | candidate, started, pending |
| start_date | Promotion start |
| finish_date | Promotion end |
| deadline_date | Deadline to accept invitation |
| original_price | Price without discount |
| price | Discounted price |
| meli_percentage | MeLi discount contribution |
| seller_percentage | Seller discount contribution |
| min_discounted_price | Min allowed price |
| max_discounted_price | Max allowed price |
| suggested_discounted_price | Suggested price |

## Exclusion List Management

### Check if Seller is Excluded
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/exclusion-list/seller?app_version=v2
```

### Exclude/Include Seller
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"exclusion_status": "true"}' \
  https://api.mercadolibre.com/seller-promotions/exclusion-list/seller?app_version=v2
```

### Check if Item is Excluded
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/seller-promotions/exclusion-list/seller/$ITEM_ID?app_version=v2
```

### Exclude/Include Item
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"item_id": "$ITEM_ID", "exclusion_status": "true"}' \
  https://api.mercadolibre.com/seller-promotions/exclusion-list/item?app_version=v2
```
