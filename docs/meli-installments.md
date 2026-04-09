# MercadoLibre Installments / Cuotas sin Interes API

Source: https://developers.mercadolibre.com.ar/en_us/campaigns-with-installments-for-marketplace

## Overview

Configure installment payment options for listings. Available primarily in Argentina. Mexico has different installment structures managed by MeLi.

## Listing Types and Installments

### gold_special (no added installments)
- Bank-offered interest installments only
- **cuota-simple-paid-by-buyer** tag: Cuota Simple Program (buyer pays financing)
- **pcj-co-funded** tag: 3-12 installments with low interest (seller pays 4%)

### gold_pro (added installments)
- **3x_campaign** tag: 3 installments at listed price (selected categories)
- No tag needed: 6 installments at listed price (default for gold_pro)
- **cuota-simple-3** tag: 3 installments Cuota Simple Program
- **cuota-simple-6** tag: 6 installments Cuota Simple Program

## Key Endpoints

### Check if Seller Can Join Campaign
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/special_installments/3x_campaign/sellers/$SELLER_ID
```
Tags: cuota-simple-paid-by-buyer, pcj-co-funded, 3x_campaign, cuota-simple-3, cuota-simple-6

### Check if Category Supports Campaign
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/special_installments/$CAMPAIGN_TAG/categories/$CATEGORY_ID/enabled
```

### Check if Item is in Campaign
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items/$ITEM_ID
```
Look for the campaign tag in the `tags` array.

### View Selling Fees by Campaign
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/sites/$SITE/listing_prices?price=$PRICE&listing_type_id=$TYPE&tags=$CAMPAIGN_TAG&domain_id=$DOMAIN
```

### Enable Campaign on a Listing (PUT)
```bash
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -d '{"tags": ["3x_campaign", "immediate_payment"]}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```
Note: Include ALL existing tags plus the campaign tag.

### Disable Campaign on a Listing (PUT)
Send all tags EXCEPT the campaign tag:
```bash
curl -X PUT -d '{"tags": ["immediate_payment"]}' \
  https://api.mercadolibre.com/items/$ITEM_ID
```

### Create Item with Campaign
```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/items \
  -d '{
    "listing_type_id": "gold_pro",
    "condition": "new",
    "buying_mode": "buy_it_now",
    "tags": ["3x_campaign"],
    ...
  }'
```

## Fee Structure Example

For Notebooks domain with 3x_campaign:
- Selling fee: 12% (marketplace)
- Installment fee: 15%
- Total: 27%

For Cell phones with pcj-co-funded:
- Selling fee: 12%
- Installment fee: 4%
- Total: 16%

## Errors (HTTP 400)
- Category not enabled for installments
- Seller not qualified for Cuota Simple
- Product is used or reconditioned
- listing_type doesn't match campaign tag
- Brand/model not in campaign (Cuota Simple)
