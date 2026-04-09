# MeLi Mexico (MLM) — Complete Cost Breakdown 2025/2026

## Sources
- https://www.mercadolibre.com.mx/ayuda/Costos-de-vender-un-producto_870
- https://www.mercadolibre.com.mx/ayuda/costos-envios-gratis_3287
- https://www.mercadolibre.com.mx/ayuda/40538
- https://www.mercadolibre.com.mx/ayuda/44007
- https://academia.nubimetrics.com/cambios-mercado-libre-mexico

---

## LAYER 1: Sales Commission (% of sale price)

Charged ONLY when a sale is completed. Varies by category and listing type.

| Listing Type | Commission Range | Exposure | Duration | MSI (Meses Sin Intereses) |
|-------------|-----------------|----------|----------|---------------------------|
| **Gratuita** | 0% | Baja | 60 days | No |
| **Clásica** (gold_special) | 8% - 16% | Alta | Unlimited | No |
| **Premium** (gold_pro) | 12.5% - 20.5% | Máxima | Unlimited | Yes (up to 12 months) |

**Premium vs Clásica difference** = ~4.5% extra. That extra covers MSI financing cost that MeLi absorbs.

### Commission by Category (Examples for MLM)
Use `GET /sites/MLM/listing_prices?price=X&category_id=Y&listing_type_id=Z` for exact rates.

Typical ranges:
- Electronics/Tech: 8% (Clásica) / 12.5% (Premium)
- Fashion/Clothing: 16% (Clásica) / 20.5% (Premium)
- Home/Garden: ~13% (Clásica) / ~17% (Premium)
- Stationery/Office (OUR PRODUCTS): likely 11-14% (Clásica)

---

## LAYER 2: Fixed Fee Per Unit (low-price products)

Additional flat charge per unit sold, based on product price:

| Product Price | Fixed Fee Per Unit | Notes |
|--------------|-------------------|-------|
| < $99 MXN | **$25 MXN** | Kills margin on cheap items |
| $99 - $149 MXN | **$30 MXN** | Still painful |
| $149 - $299 MXN | **$37 MXN** | Worst absolute amount |
| ≥ $299 MXN | **$0** | No fixed fee |

**Kit exception:** If selling a kit (bundle) under $299, only ONE fixed fee per kit (not per unit).

**CRITICAL INSIGHT:** This is why $299 MXN is the magic price threshold. Below it, you're paying fixed fees that eat margin. Above it, no fixed fee + mandatory free shipping (which MeLi subsidizes).

---

## LAYER 3: Shipping Costs (when offering envío gratis)

Shipping cost is charged to the SELLER when they offer free shipping. Calculated from 4 variables:
1. **Weight** (greater of physical weight vs volumetric weight)
2. **Product price** (determines discount tier)
3. **Seller reputation** (determines discount percentage)
4. **Quantity of units** (cost multiplied per unit)

### Volumetric Weight Formula
```
Volumetric weight (kg) = (Length × Width × Height in cm) / 5000
Use whichever is GREATER: physical weight or volumetric weight
```

### Base Shipping Cost by Weight (MXN per unit)

| Weight Range | Base Cost (used products / no reputation) |
|-------------|------------------------------------------|
| Up to 300g | $131 |
| 300g - 500g | $140 |
| 500g - 1kg | $149 |
| 1kg - 2kg | $169 |
| 2kg - 3kg | $190 |
| 3kg - 4kg | $206 |
| 4kg - 5kg | $220 |
| 5kg - 7kg | $245 |
| 7kg - 9kg | $279 |
| 9kg - 12kg | $323 |
| 12kg - 15kg | $380 |
| 15kg - 20kg | $445 |
| 20kg - 30kg | $563 |
| 30kg - 40kg | $698 |
| 40kg - 50kg | $903 |

### Shipping Discounts by Price Tier + Reputation

MeLi gives you a discount on shipping costs based on your product price and reputation:

| Product Price | MercadoLíder | Green Reputation | Yellow | No Reputation |
|--------------|-------------|-------------------|--------|---------------|
| ≥ $499 MXN | ~50% discount | ~50% discount | ~50% discount | ~50% discount |
| $299 - $498.99 | ~60% discount | ~60% discount | ~60% discount | ~60% discount |
| < $299 MXN (new) | ~30% discount | ~30% discount | ~30% discount | ~30% discount |

**NOTE:** Products ≥ $299 MUST offer free shipping (mandatory). Products < $299 can optionally offer free shipping.

### Shipping Cost Example (Our Products)
Typical AOSHIDA stationery product: ~500g, priced at ~$350 MXN
```
Base shipping cost for 500g-1kg: $149 MXN
Price tier: $299-$498.99 → 60% discount
Your shipping cost: $149 × 0.40 = $59.60 MXN
```

---

## LAYER 4: Taxes (IVA + ISR Retention)

### IVA on Commission
- MeLi charges **16% IVA on top of their commission**
- This is Mexican federal tax, not optional
- Applied to the commission amount, NOT the product price

### ISR Retention
- **2.5% of sale price** retained by MeLi
- Only if seller has RFC (tax ID) registered
- If NO RFC registered, MeLi applies MAXIMUM tax rates by law

### IVA Retention
- Additional IVA retention may apply depending on seller's tax status (régimen fiscal)
- Varies by Constancia de Situación Fiscal uploaded to MeLi

### How Taxes Work with "Lo Que Recibes"
MeLi's "what you receive" estimate already includes:
- Sales commission
- Shipping cost (if free shipping offered)
- Tax retentions (ISR, IVA)

It does NOT include:
- Advertising costs (Mercado Ads)
- Fulfillment storage fees
- "Mi Página" subscription ($437/month)

---

## LAYER 5: Complete Cost Formula

```
SALE PRICE = $500 MXN
Category commission (Clásica, 14%): $500 × 14% = $70.00

LAYER 1 - Commission:                    $70.00
LAYER 2 - Fixed fee (≥$299, so $0):       $0.00
LAYER 3 - Shipping (1kg, 60% discount):  $59.60
LAYER 4a - IVA on commission (16%):      $11.20
LAYER 4b - ISR retention (2.5%):         $12.50
─────────────────────────────────────────────────
TOTAL DEDUCTIONS:                       $153.30
YOU RECEIVE:                            $346.70 (69.3% of sale price)
```

### Another Example: Cheap Product ($150 MXN)
```
SALE PRICE = $150 MXN
Category commission (Clásica, 14%): $150 × 14% = $21.00

LAYER 1 - Commission:                    $21.00
LAYER 2 - Fixed fee ($149-$299):          $37.00  ← THIS KILLS YOU
LAYER 3 - Shipping (300g, 30% disc):      $91.70  ← only 30% discount under $299
LAYER 4a - IVA on commission (16%):        $3.36
LAYER 4b - ISR retention (2.5%):           $3.75
─────────────────────────────────────────────────
TOTAL DEDUCTIONS:                        $156.81
YOU RECEIVE:                              -$6.81  ← YOU LOSE MONEY
```

**This is why products under $299 are almost impossible to sell profitably on MeLi unless you bundle them.**

---

## LAYER 6: Optional Costs

### Mercado Ads (Product Ads)
- CPC (cost per click) model
- Varies by keyword competition
- Typical: $1-5 MXN per click
- No minimum spend

### Fulfillment (Mercado Envíos Full)
Daily storage fees:
| Size | Daily Fee/Unit |
|------|---------------|
| Small (≤12×15×25cm, <18kg) | US$0.0005 |
| Medium (≤25×33×48cm, <18kg) | US$0.0018 |
| Large (≤50×60×60cm, <18kg) | US$0.0037 |
| Extra large (>50×60×60cm or >18kg) | US$0.0240 |

Long-term storage penalties after 120 days.

### Mi Página (replaces Mercado Shops)
- 3 months free trial
- Then $437 MXN/month

### MSI (Meses Sin Intereses) — Premium only
- The extra ~4.5% commission on Premium already includes MSI cost
- Buyers can pay in up to 12 monthly installments
- Seller receives full amount upfront (MeLi fronts the financing)

---

## PRICING STRATEGY FOR AOSHIDA PRODUCTS

### The $299 Rule
**ALWAYS price at or above $299 MXN.** Below this threshold you face:
- Fixed fee per unit ($25-$37)
- Lower shipping discount (30% vs 60%)
- Mandatory free shipping doesn't apply (but buyers expect it)

### Optimal Price Range
**$350 - $999 MXN** is the sweet spot:
- No fixed fee
- 60% shipping discount
- Premium listing viable (MSI attracts buyers)
- Enough margin to absorb 14-17% total commission + taxes

### Bundle Strategy for Cheap Items
If AOSHIDA product costs $80 MXN:
- DON'T list at $150 → you lose money
- Bundle 3-pack at $399 → no fixed fee, good shipping discount, viable margin

---

## API Endpoints for Cost Calculation

```bash
# Exact commission for a product
GET /sites/MLM/listing_prices?price=500&category_id=MLM1234&listing_type_id=gold_special

# Shipping cost estimate
GET /items/{ITEM_ID}/shipping_options?zip_code=06600

# Price reference with TAXES + COSTS breakdown (BEST ENDPOINT)
GET /marketplace/benchmarks/items/{ITEM_ID}/details
# Returns:
#   estimated_taxes: { amount: 1009.27, usd_amount: ... }
#   costs: { selling_fees: 1672.50, shipping_fees: 74.50 }
#   suggested_price, current_price, lowest_price

# Get all items with price references for a seller
GET /marketplace/benchmarks/user/{USER_ID}/items

# Official cost simulator (browser)
https://www.mercadolibre.com.mx/simulador-de-costos
https://www.mercadolibre.com.mx/landing/costos-de-venta
```

---

## Key Rules Summary

1. **Minimum price: $35 MXN** (can't list below this)
2. **Free shipping mandatory for products ≥ $299 MXN (new)**
3. **Free listings: 5 new/year, 20 used/year, max 10 active, 1 unit stock**
4. **MercadoLíder or Pro MercadoPago users CANNOT use free listings**
5. **Kit sales under $299: ONE fixed fee per kit, not per unit**
6. **No RFC = maximum tax retention (register RFC ASAP)**
7. **Weight = max(physical, volumetric) — volumetric = L×W×H/5000**
8. **Commission includes IVA in official MeLi pages, but API returns base amount**
