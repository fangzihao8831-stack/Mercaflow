# MercadoLibre Seller Reputation API

Source: https://global-selling.mercadolibre.com/devsite/seller-reputation-global-selling

## Overview

Reputation reflects seller performance quality. Displayed as a color thermometer. Calculated from fulfilled orders in last 3 months + current month (or full history if < 40 fulfilled orders).

## Check Reputation

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  https://api.mercadolibre.com/global/users/seller_reputation
```

Returns reputation for all marketplaces (MLM, MLB, MLC, MCO, etc.)

## Response Fields

| Field | Description |
|-------|-------------|
| level_id | Reputation level (e.g., "5_green") |
| power_seller_status | Mercado Lider medal (silver, gold, platinum) |
| real_level | Actual level during protection period |
| protection_end_date | End date of protection |

### Transactions
| Field | Description |
|-------|-------------|
| canceled | Number cancelled |
| completed | Number completed |
| period | "historic" or "60 days" / "365 days" |
| ratings.negative/neutral/positive | Rating ratios |
| total | Total transactions |

### Metrics
| Metric | Description |
|--------|-------------|
| sales.completed | Completed sales in period |
| claims.rate | Claims rate (claims/total sales) |
| claims.value | Number of claims |
| delayed_handling_time.rate | Late shipping rate |
| delayed_handling_time.value | Number of late shipments |
| cancellations.rate | Cancellation rate |
| cancellations.value | Number of cancellations |

## Evaluation Period

### Mexico (MLM)
| Condition | Period |
|-----------|--------|
| >= 40 sales in 60 days | Past 60 days |
| < 40 sales | Full history (365 days) |

### Brazil (MLB) / Colombia (MCO)
| Condition | Period |
|-----------|--------|
| >= 60 sales in 60 days | Past 60 days |
| < 60 sales | Full history (365 days) |

### Chile (MLC)
| Condition | Period |
|-----------|--------|
| >= 40 sales in 60 days | Past 60 days |
| < 40 sales | Full history (365 days) |

## Reputation Levels (Thermometer Colors)

### Claims Rate — Mexico (MLM)
| Color | Claims Rate |
|-------|-------------|
| light_green & up | <= 2% |
| yellow | 2% - 4% |
| orange | 4% - 7% |
| red | > 7% |

### Claims Rate — Brazil (MLB)
| Color | Claims Rate |
|-------|-------------|
| light_green & up | <= 3% |
| yellow | 3% - 7% |
| orange | 7% - 12% |
| red | > 12% |

### Claims Rate — Colombia (MCO) / Chile (MLC)
| Color | Claims Rate |
|-------|-------------|
| light_green & up | <= 5% |
| yellow | 5% - 7% |
| orange | 7% - 10% |
| red | > 10% |

## Handling Time

Policy: keep <= 3 days handling time per order.
- Green: delayed handling <= 15% of orders
- Yellow: delayed handling <= 20%
- Orange: delayed handling <= 30%
- Dispatch to carrier within 96 hours of order creation

## Cancellations

- Mexico: rate should be < 4%
- Brazil: rate should be < 3%

Formula: cancellations_rate = seller cancellations / total sales

## Claims Formula

claims_rate = sales with claims / total sales

Minimum 3 claims needed to impact reputation. Seller must have > 10 sales in history.

## Errors

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Malformed access_token | Verify token format |
| 401 | Invalid caller.id | Include valid Bearer token |
