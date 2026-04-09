# MercadoLibre Product Ads / Advertising API

Sources:
- https://global-selling.mercadolibre.com/devsite/mercado-ads
- https://global-selling.mercadolibre.com/devsite/manage-sales-global-selling/new-product-ads

## Overview

Mercado Ads is MeLi's integrated advertising solution. Available in Brazil, Mexico, and Chile.
Products automatically become sponsored listings with a recommended daily budget.

## Key Concepts

- **Advertiser (advertiser_id)**: Entity that invests budget for ads
- **Campaign**: Groups ads with a budget and strategy
- **Ad**: Individual item being advertised
- **ROAS**: Return on Ad Spend (revenue/spend)
- **Strategy**: profitability, increase (growth), visibility

## Endpoints

All endpoints require header: `api-version: 2`

### Get Advertiser Info
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/advertisers
```

### Create Campaign
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/advertisers/$ADVERTISER_ID/product_ads/campaigns \
  -d '{
    "name": "Main Campaign",
    "status": "active",
    "budget": 950,
    "strategy": "profitability",
    "channel": "marketplace",
    "roas_target": 19
  }'
```

### Modify Campaign
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/product_ads/campaigns/$CAMPAIGN_ID \
  -d '{"budget": 990, "roas_target": 25}'
```

### Search All Ads
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/advertisers/$ADVERTISER_ID/product_ads/ads/search
```

### Get Ad Details
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/product_ads/ads/$ITEM_ID
```

### Modify Single Ad
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/product_ads/ads/$ITEM_ID?channel=marketplace \
  -d '{"status": "active", "campaign_id": 1234567}'
```

### Bulk Modify Ads (up to 10,000)
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/advertisers/$ADVERTISER_ID/product_ads/ads?channel=marketplace \
  -d '{
    "target": ["MLM123", "MLM456"],
    "payload": {"status": "active", "campaign_id": 352274800}
  }'
```

### Campaign Metrics
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' -H 'api-version: 2' \
  https://api.mercadolibre.com/marketplace/advertising/$SITE_ID/advertisers/$ADVERTISER_ID/product_ads/campaigns/search?date_from=2024-01-01&date_to=2024-02-28&metrics=clicks,prints,cost,roas
```

## Campaign Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| profitability | Fewer ads, higher conversion | Products with many sales |
| increase | Balance of reach/profitability | Products with good sales |
| visibility | Maximum reach | New listings |

## ROAS Target
- Range: 1x to 35x
- Low ROAS = more sales, lower profitability per sale
- High ROAS = higher profitability, fewer total sales

## Budget Rules
- Daily budget can consume up to 2x (100% extra) using unspent balance
- Monthly billing considers all active days
- Paused campaign months = no consumption

## Ad Statuses
| Status | Description |
|--------|-------------|
| active | Advertising active |
| paused | Manually paused |
| hold | Item paused/out of stock at marketplace level |
| idle | Available but not in any campaign |
| delegated | Loaned to another advertiser |
| revoked | Returned from delegated advertiser |

## Available Metrics
clicks, prints, ctr, cost, cpc, acos, roas, sov, cvr,
organic_units_quantity, organic_units_amount, organic_items_quantity,
direct_items_quantity, direct_units_quantity, direct_amount,
indirect_items_quantity, indirect_units_quantity, indirect_amount,
advertising_items_quantity, units_quantity, total_amount,
impression_share, top_impression_share,
lost_impression_share_by_budget, lost_impression_share_by_ad_rank

## Aggregation Types
- sum (default)
- DAILY (time series)
- campaign / item

Date range: max 90 days backward. Updated at 10:00 AM GMT-3.
