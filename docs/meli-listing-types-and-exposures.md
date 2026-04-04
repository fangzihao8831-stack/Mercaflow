URL: https://global-selling.mercadolibre.com/devsite/listing-types-and-exposures
Title: Developers

## Listing Types

Listing types determine the visibility and exposure of your products on Mercado Libre. Choosing the right type directly impacts your sales potential. Higher exposure types (Premium/gold\_pro) give your listings priority in search results and may appear on category home pages.

Depending on the level of exposure you want for your items, you can choose between different listing types. Each listing type has its own characteristics and fees. Let's see how to work with them correctly.

Note:

Availability varies by destination marketplace:

* **MLB, MLM, MCO, MLC:** gold\_special and gold\_pro available.
* **MLA:** gold\_special only (gold\_pro deprecated, use campaign\_tags for installments).
* **MLU:** gold\_special and free only (since November 2023).

 

### When to Choose Each Listing Type

Use this guide to select the right listing type for your needs:

| Listing Type | Best For | Key Characteristics |
| --- | --- | --- |
| **free** | Testing or low-volume sellers | Limited to 10 active listings. No selling fee, but lowest exposure. |
| **gold\_special** (Classic) | Standard visibility sellers | Unlimited listings. Pay only the selling fee. Good balance of cost vs exposure. |
| **gold\_pro** (Premium) | Maximum visibility + installments | Unlimited listings. Higher fees but best conversion. Offers buyer-friendly installments. |

Important:

Free listings have a limit of 10 active publications per user. Gold\_special and gold\_pro have **no quantity limits**. Check the `remaining_listings` field in the API response to know how many free listings you have left.

 

Important:

Currently, for MLU Marketplace, the Classic combo exists as listing\_type 'bronze' and Premium as 'gold\_special'. Starting November 15, 2023, we will unify both combos, and **only the listing\_type free and gold\_special (Premium) will be available for MLU**. [See MLU example](https://developers.mercadolibre.com.ar/es_ar/tipos-de-publicacion-y-actualizaciones-de-articulos?nocache=true#Tipos-de-publicaci%C3%B3n-por-site). 
Learn more [about the change in listings for MLU](https://www.mercadolibre.com.uy/ayuda/870).

Note:

\- Remember that the listing types or listing\_type available for Marketplace are free, gold\_special, gold\_pro (may vary depending on the site). 
\- Learn more about the [costs for selling](https://developers.mercadolibre.com.ar/es_ar/comision-por-vender) for a particular listing\_type by site, category, currency, logistics, and more. 

 

## Now Your Listings Are Differentiated by the Installments You Add

Important:

This functionality applies only to the Argentina site.

So you can identify more clearly what your listings offer, **we stop calling them Classic or Premium** (applies only at the frontend level, at the backend level we will continue using the listing\_type gold\_special and gold\_pro) and you can differentiate them as follows:

* **Listings where you choose not to add installments** 
 They apply to **gold\_special** listings; they only have installments with interest offered by banks. That's why you only pay the selling fee and, if applicable, the fixed cost.
* **Listings where you choose to add installments** 
 In **gold\_pro** listings, by offering more convenient installments to buyers, you pay the selling fee plus a cost for offering installments, and the fixed cost if applicable.

[Learn more about costs and commissions](https://www.mercadolibre.com.ar/ayuda/31519).

Take into account the **relationship between the listing\_type** (required attribute) **and campaign tags**. Learn more about [Installment Campaigns for Marketplace](https://developers.mercadolibre.com.ar/es_ar/campanas-con-cuotas-para-marketplace#:~:text=Mercado%20Libre%20.-,Comparaci%C3%B3n%20opciones%20de%20cuotas,-Publicaciones%20en%20las).

## Listing Types by Site

Find out about the different listing types **by Mercado Libre site**. To find the available IDs, execute the following call.

| Site | gold\_special (Classic) | gold\_pro (Premium) | free |
| --- | --- | --- | --- |
| **MLB** (Brazil) | Yes | Yes | Yes |
| **MLM** (Mexico) | Yes | Yes | Yes |
| **MCO** (Colombia) | Yes | Yes | Yes |
| **MLC** (Chile) | Yes | Yes | Yes |
| **MLA** (Argentina) | Yes | No | Yes |
| **MLU** (Uruguay) | Yes | No | Yes |

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/$SITE_ID/listing_types
```

Example site MLA:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/MLA/listing_types
```

Response:

```
[
 {
 "site_id": "MLA",
 "id": "gold_pro",
 "name": "Premium"
 },
 {
 "site_id": "MLA",
 "id": "gold_special",
 "name": "Clasica"
 },
 {
 "site_id": "MLA",
 "id": "free",
 "name": "Gratuita"
 }
]
```

Example site MLU:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/MLU/listing_types
```

Response:

* Starting November 15, 2023.

```
[
 {
 "site_id": "MLU",
 "id": "gold_special",
 "name": "Premium"
 },
 {
 "site_id": "MLU",
 "id": "free",
 "name": "Gratuita"
 }
]
```

 

## Listing Type Specification

If you want more information about a specific listing\_type by site, include the ID in the request:

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/$SITE_ID/listing_types/$LISTING_TYPE_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/MLA/listing_types/gold_special
```

Response:

```
{
 "id": "gold_special",
 "not_available_in_categories": [
 "MLA1743",
 "MLA1459",
 "MLA1540"
 ],
 "configuration": {
 "name": "Clasica",
 "listing_exposure": "highest",
 "requires_picture": true,
 "max_stock_per_item": 99999,
 "deduction_profile_id": null,
 "differential_pricing_id": null,
 "duration_days": {
 "buy_it_now": 7300,
 "auction": null,
 "classified": null
 },
 "immediate_payment": {
 "buy_it_now": false,
 "auction": false,
 "classified": false
 },
 "mercado_pago": "mandatory",
 "listing_fee_criteria": {
 "min_fee_amount": 0,
 "max_fee_amount": 0,
 "percentage_of_fee_amount": 0,
 "currency": "ARS"
 },
 "sale_fee_criteria": {
 "min_fee_amount": 0,
 "max_fee_amount": 750000,
 "percentage_of_fee_amount": 13,
 "currency": "ARS"
 }
 },
 "exceptions_by_category": []
}
```

Note:

Key fields to understand:

* **not\_available\_in\_categories:** Categories where this listing type cannot be used.
* **listing\_exposure:** The exposure level associated with this type (e.g., "highest").
* **duration\_days.buy\_it\_now:** Duration in days. Value 7300 means ~20 years (effectively unlimited).
* **requires\_picture:** If true, at least one picture is mandatory.

gold\_special and gold\_pro listings will have unlimited duration; you can check this in /items, filtering by the stop\_time attribute:

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID?attributes=stop_time
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1389403099?attributes=stop_time
```

Remember that listings will be paused if the stock is 0 and will be reactivated when you add a new quantity. Learn more about how to [Update the stock](https://developers.mercadolibre.com.ar/es_ar/producto-sincroniza-modifica-publicaciones#Actualiza-el-stock:~:text=Stock%20de%20%C3%ADtems-,Actualizar%20el%20stock,-Para%20actualizar%20el) of your listings.

 

## 
Available Listing Types

You can check the listing types available for a specific user and category.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/users/$USER_ID/available_listing_types?category_id=$CATEGORY_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/users/1234/available_listing_types?category_id=MLA1055
```

Response:

```
{
 "category_id": "MLA1055",
 "available": [
 {
 "site_id": "MLA",
 "id": "gold_pro",
 "name": "Premium",
 "remaining_listings": null
 },
 {
 "site_id": "MLA",
 "id": "gold_special",
 "name": "Clasica",
 "remaining_listings": null
 },
 {
 "site_id": "MLA",
 "id": "free",
 "name": "Gratuita",
 "remaining_listings": 10
 }
 ]
}
```

Note:

The `remaining_listings` field indicates how many listings of that type the user can still create:

* **null:** Unlimited listings available (gold\_special, gold\_pro).
* **Number (e.g., 10):** Remaining free listings before reaching the limit.

If you cannot create a listing in a certain listing type and want to know why it is not available for you, you can perform a GET request to find out the reason:

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/users/$USER_ID/available_listing_type/free?category_id=$CATEGORY_ID
```

Response:

```
{
 "available": false,
 "cause": "You have more than 5 transactions in the last year.",
 "code": "list.transactions.exceeded"
}
```

## 
Listing Exposures

You can check information about the exposure levels associated with all listing types on Mercado Libre by site.

Understanding exposure levels is crucial for maximizing your listing visibility:

| Exposure Level | priority\_in\_search | home\_page | category\_home\_page | Description |
| --- | --- | --- | --- | --- |
| **highest** | 0 (Best) | Yes | Yes | Maximum visibility. Appears first in search results and may appear on home pages. |
| **high** | 1 | No | Yes | High visibility. Good search priority, appears on category pages. |
| **mid** | 2 | No | Yes | Medium visibility. Moderate search priority. |
| **low** | 3 | No | No | Low visibility. Lower search priority. |
| **lowest** | 4 (Worst) | No | No | Minimum visibility. May show ads on listing page. |

Note:

* **priority\_in\_search:** Lower number = higher priority. 0 means your listing appears first.
* **home\_page:** If true, listing may appear on Mercado Libre home page.
* **category\_home\_page:** If true, listing may appear on category landing pages.
* **advertising\_on\_listing\_page:** If true, competitor ads may appear on your listing page.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/$SITE_ID/listing_exposures
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/MLA/listing_exposures
```

Response:

```
[
 {
 "id": "lowest",
 "name": "Ultima",
 "home_page": false,
 "category_home_page": false,
 "advertising_on_listing_page": true,
 "priority_in_search": 4
 },
 {
 "id": "low",
 "name": "Inferior",
 "home_page": false,
 "category_home_page": false,
 "advertising_on_listing_page": false,
 "priority_in_search": 3
 },
 {
 "id": "mid",
 "name": "Media",
 "home_page": false,
 "category_home_page": true,
 "advertising_on_listing_page": false,
 "priority_in_search": 2
 },
 {
 "id": "high",
 "name": "Alta",
 "home_page": false,
 "category_home_page": true,
 "advertising_on_listing_page": false,
 "priority_in_search": 1
 },
 {
 "id": "highest",
 "name": "Superior",
 "home_page": true,
 "category_home_page": true,
 "advertising_on_listing_page": false,
 "priority_in_search": 0
 }
]
```

You can also check each exposure level separately with its respective ID.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/$SITE_ID/listing_exposures/$EXPOSURE_LEVEL
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/sites/MLA/listing_exposures/high
```

Response:

```
{
 "id": "high",
 "name": "Alta",
 "home_page": false,
 "category_home_page": true,
 "advertising_on_listing_page": false,
 "priority_in_search": 1
}
```

 

## Available Transactions for a Listing

You can check the available listing\_type for a specific listing, which may vary by site.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/available_listing_types
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1389403099/available_listing_types
```

Response:

```
[
 {
 "site_id": "MLA",
 "id": "gold_pro",
 "name": "Premium"
 },
 {
 "site_id": "MLA",
 "id": "gold_premium",
 "name": "Oro Premium"
 }
]
```

 

## Available Upgrades for a Listing

You can perform an upgrade to a higher listing type. If you need to upgrade, you can see which listing types are available for your item, which may vary by site. If no upgrades are available, an empty list is returned.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/available_upgrades
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1389403099/available_upgrades
```

Response:

```
[
 {
 "site_id": "MLA",
 "id": "gold_pro",
 "name": "Premium"
 }
]
```

 

## Available Downgrades for a Listing

Downgrade is reducing the exposure of your listing by updating it to a lower type. It is available for some specific cases:

* Downgrades between gold\_pro to gold\_special and vice versa are allowed at any time (depending on the site).
* You can perform a downgrade on a listing with status PAYMENT\_REQUIRED. Furthermore, in MLA, you can also downgrade listings with status ACTIVE, NOT\_YET\_ACTIVE, UNDER\_REVIEW, and PAUSED.
* Downgrading a listing to free is not allowed.
* If no downgrades are available, an empty list is returned.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/available_downgrades
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1389403099/available_downgrades
```

Response:

```
[ ]
```

 

## Update Listing Type

Remember that you can **change between gold\_special and gold\_pro listing types** (depending on the site) whenever you want **without charge**. 
If you wish to update the listing\_type of a listing, you must perform a PUT request to the following resource:

Request:

```
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -H "Accept: application/json" -d
{
 "id": "gold_special"
}
https://api.mercadolibre.com/items/$ITEM_ID/listing_type
```

Example:

```
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -H "Accept: application/json" -d
{
 "id": "gold_special"
}
https://api.mercadolibre.com/items/MLA1389403099/listing_type
```

Response:

```
{
 "id": "MLA1389403099",
 "site_id": "MLA",
 "title": " Moto Z3 Play 64 Gb Indigo Oscuro 4 Gb Ram",
 "subtitle": null,
 "seller_id": 1160561786,
 "category_id": "MLA1055",
 "user_product_id": "MLAU10645855",
 "official_store_id": null,
 "price": 18008976,
 "base_price": 18008976,
 "original_price": null,
 "inventory_id": null,
 "currency_id": "ARS",
 "initial_quantity": 6,
 "available_quantity": 6,
 "sold_quantity": 0,
 "sale_terms": [],
 "buying_mode": "buy_it_now",
 "listing_type_id": "gold_special"
}
```

That's it! Now you're ready to access the correct exposure for your products and perform item updates. Since we know that sometimes you need more than one attempt to create your listing, we offer you the possibility to check if your listing turned out exactly how you wanted it before publishing it. Learn more about [the listing validator](https://developers.mercadolibre.com.ar/es_ar/validador-de-publicaciones).

 

## Best Practices

Pro Tips:

1. **Always check available\_listing\_types before creating a listing.** This prevents errors when the user or category doesn't support certain types.
2. **Monitor your listing exposure** with `GET /items/{id}` to verify the configuration is correct after creation.
3. **Use the Publication Validator** before going live to catch issues early.
4. **Consider the cost-benefit**: gold\_pro has higher fees but better conversion due to installments and exposure.
5. **Check site availability**: Not all listing types are available in all marketplaces. Always verify using `/sites/{site_id}/listing_types`.

**Learn more about:**

* [Installment Campaigns for Marketplace](https://developers.mercadolibre.com.ar/es_ar/campanas-con-cuotas-para-marketplace) (applies only to MLA).
* [Costs for Selling](https://developers.mercadolibre.com.ar/es_ar/comision-por-vender).
