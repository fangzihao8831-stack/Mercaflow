# MercadoLibre Payments / MercadoPago Integration

Source: https://developers.mercadolibre.com.ar/en_us/payment-handling

## Overview

MercadoPago is MeLi's payment platform. For full payment integration, visit: https://www.mercadopago.com.br/developers/es/guides

MeLi marketplace payments are handled automatically — sellers don't need to implement payment processing.

## Payment Notifications

Subscribe to `payments` topic to receive payment notifications.

See: https://developers.mercadolibre.com.ar/en_us/products-receive-notifications#payments

## Cashback for Canceled Sales

Available for sellers in Mexico (and soon Argentina, Brazil).

When orders are cancelled, buyers with good reputation who paid with credit/debit card automatically receive a refund as MercadoPago account money.

### Order State Changes
- status = **paid** (not cancelled)
- New tag: **unfulfilled**
- Payment includes **refund_account_money** tag

Note: Order never gets status "cancelled" since the refund-to-account generates a completed payment flow.

## Mexico Payment Methods

Available at: `GET https://api.mercadolibre.com/sites/MLM/payment_methods`

| Method | Type |
|--------|------|
| Visa | credit_card |
| American Express | credit_card |
| Mastercard | credit_card |
| Mastercard Debito | debit_card |
| Visa Debito | debit_card |
| Tarjeta MercadoPago | prepaid_card |
| Santander | ATM |
| OXXO | ticket (cash) |
| Dinero en cuenta MP | account_money |
| BBVA Bancomer | ATM |
| Citibanamex | ATM |
| Mercado Credito | digital_currency |

## Payment in Orders

Order payments include:
- payment_method_id (visa, amex, oxxo, etc.)
- installments (number of installments)
- status (approved, etc.)
- transaction_amount
- date_approved

## Key Point for Sellers

MeLi handles all payment processing, collection, and disbursement. Sellers receive funds in their MercadoPago account after order completion. No direct MercadoPago API integration needed for basic selling.

For advanced payment features (installments, Cuota Simple), see meli-installments.md.

## Related Resources

- Payment methods: `GET /sites/$SITE_ID/payment_methods`
- Specific method: `GET /sites/$SITE_ID/payment_methods/$METHOD_ID`
- Payment notifications: Subscribe to `payments` topic
- Selling fees: `GET /sites/$SITE_ID/listing_prices`
