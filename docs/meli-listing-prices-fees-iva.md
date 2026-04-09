# MeLi Listing Prices API & IVA/Taxes

## Source
- https://developers.mercadolivre.com.br/en_us/fees-for-listing
- https://developers.mercadolibre.com.ar/en_us/billing-reports
- https://www.mercadolibre.com.mx/ayuda/Costos-de-vender-un-producto_870

## listing_prices API

### Endpoint
```
GET https://api.mercadolibre.com/sites/{SITE_ID}/listing_prices?price={PRICE}
```

### Parameters
- `price` — product price
- `listing_type_id` — gold_pro (Premium), gold_special (Classic), free
- `category_id` — category affects commission percentage
- `currency_id` — currency code
- `quantity` — number of items
- `logistic_type` — shipping logistics type
- `tags` — installment campaign tags (MLA only)
- `channel` — marketplace or mshops (default: marketplace)

### Response Fields
| Field | Description |
|-------|-------------|
| `sale_fee_amount` | Total fee amount for selling |
| `sale_fee_details.percentage_fee` | Total commission percentage |
| `sale_fee_details.meli_percentage_fee` | MeLi platform fee percentage |
| `sale_fee_details.financing_add_on_fee` | Installment financing add-on (Premium) |
| `sale_fee_details.fixed_fee` | Fixed fee per unit (low-price items) |
| `sale_fee_details.gross_amount` | Gross commission (without discounts) |
| `listing_fee_amount` | Publishing fee (always 0, listing is free) |

## Does listing_prices Include IVA/Taxes?

### Answer: IT DEPENDS ON THE SITE

**Mexico (MLM):**
- The commission percentages shown by MeLi "include IVA" per official help pages
- The Codefy calculator mentions: "comision estandar del 3.5% mas el IVA del 16% sobre la comision"
- MeLi Mexico applies **16% IVA on the commission** (not on the product price)
- Additionally: **2.5% ISR retention** on each sale (for sellers with RFC)
- The `sale_fee_amount` from the API likely returns the BASE fee BEFORE IVA
- You must add 16% IVA on top of the commission to get actual cost

**Argentina (MLA):**
- IVA and Ganancias retentions were eliminated on payments (2024)
- IVA perception on invoices remains (1-8% depending on tax status)
- Billing API shows: "Percepcion IVA Regimen General" as separate charge

### Mexico Taxes on Sales
1. **Commission IVA**: 16% on top of MeLi's selling fee
2. **ISR Retention**: 2.5% of sale price (if RFC registered)
3. **IVA Retention**: Varies by seller tax status
4. These are SEPARATE from the listing_prices API response

### How to Calculate Actual Cost for MLM
```
sale_price = 500 MXN
commission_rate = 16% (Classic, example category)
commission = 500 * 0.16 = 80 MXN
iva_on_commission = 80 * 0.16 = 12.80 MXN
total_commission = 80 + 12.80 = 92.80 MXN
isr_retention = 500 * 0.025 = 12.50 MXN
total_deductions = 92.80 + 12.50 = 105.30 MXN
you_receive = 500 - 105.30 = 394.70 MXN
```

### Fixed Fee by Price Range (MLM)
| Price Range | Fixed Fee per Unit |
|-------------|-------------------|
| < $99 MXN | $25 MXN |
| $99 - $149 MXN | $30 MXN |
| $149 - $299 MXN | $37 MXN |
| >= $299 MXN | $0 |

## Billing API
Separate endpoint for actual invoiced charges:
```
GET /billing/integration/monthly/periods?group=ML
GET /billing/integration/periods/key/{KEY}/documents
GET /billing/integration/periods/key/{KEY}/summary
GET /billing/integration/periods/key/{KEY}/details
```
For MLM, use `expiration_date` as the key (not first-of-month).

## Important Notes
- Commission varies 8-16% (Classic) and 12.5-20.5% (Premium) by category
- Use the API with `category_id` for accurate per-category rates
- Minimum product price: $35 MXN
- Free listing: 5 new items/year or 20 used items/year, max 10 active, 1 unit each
- Supermercado (Market) products have different cost structure
