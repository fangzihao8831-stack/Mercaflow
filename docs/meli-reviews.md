# MercadoLibre Product Reviews API

Source: https://global-selling.mercadolibre.com/devsite/product-reviews

## Overview

Buyers can leave star ratings and comments after product delivery. Reviews display under the listing title on MeLi.

## Get Item Reviews

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/reviews/item/$ITEM_ID
```

### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | Integer | 5 | Max reviews to return (max 10000) |
| offset | Integer | 0 | Skip N reviews (max 1000000) |
| catalog_product_id | String | - | Filter for catalog items |

### Response
```json
{
  "paging": {
    "total": 3,
    "limit": 5,
    "offset": 0,
    "reviews_with_comment": 3
  },
  "reviews": [
    {
      "id": 60934080,
      "reviewable_object": {"id": "MLM769281453", "type": "product"},
      "date_created": "2020-05-02T13:18:21Z",
      "status": "published",
      "title": "Excellent product!",
      "content": "Good quality, works correctly.",
      "rate": 5,
      "likes": 0,
      "dislikes": 0,
      "reviewer_id": 0,
      "buying_date": "2020-04-16T04:00:00Z",
      "relevance": 10
    }
  ],
  "rating_average": 5,
  "stars": 5,
  "rating_levels": {
    "one_star": 0,
    "two_star": 0,
    "three_star": 0,
    "four_star": 0,
    "five_star": 3
  }
}
```

## Catalog Item Reviews

Aggregated reviews from all items linked to the same catalog product:

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/reviews/item/$ITEM_ID?catalog_product_id=$CATALOG_PRODUCT_ID
```

## Response Fields

### Review Object
| Field | Description |
|-------|-------------|
| id | Unique review identifier |
| reviewable_object.id | Item/product ID being reviewed |
| date_created | Review creation date (ISO 8601) |
| status | "published" or "pending" |
| title | Review title |
| content | Full review text |
| rate | Star rating (1-5) |
| likes/dislikes | Helpfulness votes |
| reviewer_id | Always 0 (privacy) |
| buying_date | Purchase date |
| relevance | Relevance ranking score |

### Aggregate Fields
| Field | Description |
|-------|-------------|
| rating_average | Average stars (1.0-5.0) |
| stars | Overall displayed stars |
| rating_levels | Breakdown by star count |

## Errors

| Status | Error | Description |
|--------|-------|-------------|
| 400 | unauthorized | Invalid item ID format |
| 400 | bad_request | Invalid limit or offset |
| 403 | forbidden | Invalid/expired access token |
