# MeLi Mexico (MLM) Fee Structure — 2025/2026

## Sources
- https://www.mercadolibre.com.mx/ayuda/Costos-de-vender-un-producto_870
- https://www.tiendanube.com/blog/comision-mercado-libre-mexico/
- https://global-selling.mercadolibre.com/landing/pricing
- https://blog.brusmax.com/costos-y-comisiones-para-vender-en-mercadolibre/

---

## Listing Types Available for MLM
| Type | ID | Exposure | Duration | MSI |
|------|-----|----------|----------|-----|
| Gratuita | `free` | Baja | 60 days | No |
| Clasica | `gold_special` | Alta | Unlimited | No |
| Premium | `gold_pro` | Maxima | Unlimited | Yes |

---

## Commission Ranges by Listing Type
| Listing Type | Commission Range | Notes |
|-------------|-----------------|-------|
| Gratuita | 0% | Max 5 new/year, 20 used/year, 10 active, 1 unit |
| Clasica | 8% - 16% | Varies by category |
| Premium | 12.5% - 20.5% | Includes MSI financing cost |

---

## Fixed Fee per Unit (Additional to Commission)
| Product Price Range | Fixed Fee per Unit |
|--------------------|--------------------|
| < $99 MXN | $25 MXN |
| $99 - $149 MXN | $30 MXN |
| $149 - $299 MXN | $37 MXN |
| >= $299 MXN | $0 |

**Note:** Kit sales under $299 pay only ONE fixed fee per kit.

---

## Tax Implications (Mexico)
| Tax | Rate | Basis |
|-----|------|-------|
| IVA on commission | 16% | Applied on MeLi's commission |
| ISR retention | 2.5% | Applied on sale price (if RFC registered) |

### Example Calculation
Product price: $500 MXN, Category commission: 16% (Clasica)
```
Commission: $500 × 16% = $80.00
IVA on commission: $80 × 16% = $12.80
ISR retention: $500 × 2.5% = $12.50
Total deductions: $80 + $12.80 + $12.50 = $105.30
You receive: $500 - $105.30 = $394.70 (78.9% of sale price)
```

---

## Shipping Costs (Mexico)
- Free shipping threshold: **$299 MXN** (products above this MUST offer free shipping)
- Seller pays shipping cost, MeLi provides discount based on:
  - Product weight (physical or volumetric, whichever is higher)
  - Product price
  - Seller reputation
  - Number of units

### Shipping Discounts by Reputation
| Price Range | MercadoLider | Green Reputation | Standard |
|-------------|-------------|-----------------|----------|
| $299 - $499 | ~60% discount | ~50% discount | ~40% discount |
| >= $499 | Higher discounts | Higher discounts | Higher discounts |

---

## Full (Fulfillment) Fees — Mexico
### Daily Storage Fee
| Size | Daily Fee per Unit |
|------|-------------------|
| Small (≤12×15×25cm, <18kg) | US$0.0005 |
| Medium (≤25×33×48cm, <18kg) | US$0.0018 |
| Large (≤50×60×60cm, <18kg) | US$0.0037 |
| Extra large/heavy (>50×60×60cm or >18kg) | US$0.0240 |

### Long-term Storage (>120 days)
| Duration | Small | Medium | Large | Extra Large |
|----------|-------|--------|-------|-------------|
| Up to 4 months | $0 | $0 | $0 | $0 |
| 4-6 months | US$0.68 | US$1.02 | US$1.22 | US$3.22 |
| 6-12 months | US$2.15 | US$3.32 | US$4.15 | US$10.68 |
| >12 months | US$3.66 | US$4.98 | US$6.73 | US$22.39 |

---

## Minimum Listing Prices
| Logistics | Minimum Price |
|-----------|--------------|
| Direct-to-Consumer | US$3 |
| Full (Mexico) | US$4 |

---

## Key Rules
- Minimum product price: **$35 MXN**
- Free listings: 5 new/year, 20 used/year, max 10 active, 1 unit stock
- MercadoLider or Pro Mercado Pago users CANNOT use free listings
- Supermercado (Market) products have separate cost structure
- All published fees include IVA per official MeLi pages

---

## API to Check Exact Fees
```bash
# Get fees for a $500 product in a specific category on MLM
curl -X GET -H 'Authorization: Bearer $TOKEN' \
  'https://api.mercadolibre.com/sites/MLM/listing_prices?price=500&category_id=MLM1234&listing_type_id=gold_special'
```

## Revenue Calculator
Official tool: https://global-selling.mercadolibre.com/listings/cost-calculator
MeLi Mexico cost simulator: https://www.mercadolibre.com.mx/simulador-de-costos
