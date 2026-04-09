# MercadoLibre Orders API

Source: https://global-selling.mercadolibre.com/devsite/manage-orders-cbt

## Overview

An order is a request made by a customer on a listed item with purchase conditions. Orders contain product info, payment, shipping, and buyer/seller details.

## Order Statuses

| Status | Description |
|--------|-------------|
| **payment_required** | Payment should be confirmed to display user info |
| **payment_in_process** | Payment exists but not yet credited |
| **partially_paid** | Credited payment but not enough |
| **paid** | Payment credited |
| **cancelled** | Order not fulfilled |
| **invalid** | Invalidated (malicious buyer) |

## Key Endpoints

### Search All Orders
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/orders/search
```
Rate limit: 100 requests/minute

### Search Orders by Seller
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/orders/search?seller.id=$SELLER_ID
```

### Get Single Order
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/orders/$ORDER_ID
```

### Get Order Invoice (Proforma for customs)
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/orders/$ORDER_ID/invoice
```

### Get Payment Methods (by site)
```bash
curl -X GET https://api.mercadolibre.com/sites/$SITE_ID/payment_methods
```

### Get Specific Payment Method
```bash
curl -X GET https://api.mercadolibre.com/sites/$SITE_ID/payment_methods/$PAYMENT_ID
```

## Search Filters

| Parameter | Description |
|-----------|-------------|
| **buyer** | Search by buyer ID |
| **seller.id** | Search by seller ID |
| **order.status** | Filter by status (paid, cancelled, payment_required) |
| **site** | Filter by country (MLM, MLB, MLC) |
| **limit** | Max results per page (max 1000, default 50) |
| **offset** | Offset for pagination |
| **date_created.from/to** | Filter by creation date |
| **last_updated.from/to** | Filter by update date |
| **date_closed.from/to** | Filter by close date |

## Sort Options

| Sort | Description |
|------|-------------|
| date_asc | Date ascending |
| date_desc | Date descending |
| updated_asc | Last updated ascending |
| updated_desc | Last updated descending |
| closed_asc | Close date ascending |
| closed_desc | Close date descending |

## Order Response Fields

| Field | Description |
|-------|-------------|
| **id** | Unique order identifier |
| **date_created** | Order creation date |
| **date_closed** | Confirmation date (status first changes to paid) |
| **expiration_date** | Deadline for user to qualify |
| **status** | Order status |
| **currency_id** | Currency (USD for CBT) |
| **buyer** | Buyer info (id, nickname, first_name, last_name) |
| **seller** | Seller info |
| **order_items** | List of items in order |
| **payments** | Payment details |
| **shipping** | Shipping config (shipment ID) |
| **tags** | Seller-selected tags (delivered, paid) |
| **taxes** | Tax amounts |
| **gross_price** | Original amount without discounts |

## Order Item Fields

Each order_item contains:
- **item.id** — MLM item ID
- **item.title** — Item title
- **item.category_id** — Category
- **item.variation_id** — Variation if applicable
- **item.seller_sku** — Seller SKU
- **item.parent_item_id** — Parent CBT item ID
- **quantity** — Units purchased
- **unit_price** — Price per unit
- **currency_id** — Currency
- **sale_fee** — MeLi commission
- **base_exchange_rate** — Exchange rate used

## Payment Fields

- **id** — Payment ID
- **payment_method_id** — Method (visa, amex, oxxo, etc.)
- **installments** — Number of installments
- **status** — Payment status (approved, etc.)
- **transaction_amount** — Total amount
- **date_approved** — Approval date

## gross_price Calculation

```
gross_price = (unit_price + discounts.full) x quantity
```

Example: unit_price=440, discount=341, qty=2 → gross_price = (440+341)*2 = 1562

## Fraud Alerts

Orders tagged with **"fraud_risk_detected"** should NOT be shipped. Cancel the order immediately.

## Mexico Payment Methods

- Visa (credit_card)
- American Express (credit_card)
- Mastercard (credit_card)
- Mastercard Debito (debit_card)
- Visa Debito (debit_card)
- Tarjeta MercadoPago (prepaid_card)
- Santander/ATM
- OXXO (ticket/cash)
- Dinero en cuenta MercadoPago (account_money)
- BBVA Bancomer (ATM)
- Citibanamex (ATM)
- Mercado Credito (digital_currency)

## Errors

| HTTP Code | Error | Message |
|-----------|-------|---------|
| 403 | forbidden | Invalid caller.id |
| 404 | not_found | Resource not found |
| 500 | internal_server_error | Something went wrong |
| 401 | not_found | invalid_token |
| 400 | bad_request | Malformed access_token |
| 451 | unavailable | User not available for legal reasons |
