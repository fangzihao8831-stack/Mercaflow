URL: https://developers.mercadolibre.com.ar/en_us/catalog-eligibility
Title: Developers

## Catalog eligibility

## Identify an eligible publication for catalogue

Before publishing to catalog, you must recognize which publications are eligible or can be published to catalog by recognizing **the catalog\_listing\_eligible** tag from the item API or optin for the single **publication eligibility** or **multiget** resources to check multiple publications.

Note:

Only publications that comply with some requirements such as condition: new or for CELLPHONES domain that the phone is released can participate in catalog.

## Filtering of items per seller

This filter will allow you to distinguish catalog publications from traditional ones. You must send in **the catalog\_listing parameters** with the value true or false. First, we identify all catalog items of a seller. Note that you must pass the corresponding status parameter in case you want to add a filter, such as **status=active**.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/$USER_ID/items/search?catalog_listing=true
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/123456789/items/search?catalog_listing=true
```

Catalog items short response:

```
{
 "seller_id": "123456789",
 "query": null,
 "paging": {
 "limit": 50,
 "offset": 0,
 "total": 8
 },
 "results": [
 "MLA123456789",
 "MLA234567890",
 "MLA345678912",
 "MLA456789123",
 "MLA567891234",
 "MLA678912345",
 "MLA789123456",
 "MLA891234567"
 ],
 "orders": [...],
 
 "available_orders": [...]
}
```

You can use the same filter to identify all non-catalog items of a seller.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/$USER_ID/items/search?catalog_listing=false
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/123456789/items/search?catalog_listing=false
```

marketplace item's short response:

```
{
 "seller_id": "123456789",
 "query": null,
 "paging": {
 "limit": 50,
 "offset": 0,
 "total": 2902
 },
 "results": [
 "MLA987654321",
 "MLA123789456",
 "MLA456789123",
 "MLA132465798",
 "MLA978645312",
 "MLA312645978",
 "MLA654987321",
 "MLA123789654",
 ],

 "orders": [...],
 "available_orders": [...]
}
```

## Eligibility tag for items

The fact that an item is eligible means that it can be published in the catalog. Through the search resource, you will be able to identify all the items of a seller that are eligible for catalog with the tag **catalog\_listing\_eligible** and that are not yet participating in the catalog.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/$USER_ID/items/search?tags=catalog_listing_eligible
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'
https://api.mercadolibre.com/users/123456789/items/search?tags=catalog_listing_eligible
```

The search response displays all items from the seller with the **catalog\_listing\_eligible** tag.

Short response:

```
{
 "seller_id":"658869707",
 "query":null,
 "paging":{
 "limit":50,
 "offset":0,
 "total":0
 },
 "results":[
 "MLA123789456",
 "MLA456789123",
 "MLA132465798"
 ],
 "orders":[...
 ],
 "available_orders":[...
 ]
}
```

Eligible item example:

```
{
 "id": "MLA123789456",
 "site_id": "MLA",
 "title": "Item De Testeo, Por Favor No Ofertar --kc:off",
 "subtitle": null,
 "seller_id": 123456987,
 "category_id": "MLA3530",
 "official_store_id": null,
 "price": 50,
 "base_price": 50,
 "original_price": null,
 "currency_id": "ARS",
 "initial_quantity": 1,
 "available_quantity": 1,
 "sold_quantity": 0,
 "sale_terms": [
 ],
 "buying_mode": "buy_it_now",
 "listing_type_id": "free",
 "start_time": "2020-02-17T16:30:39.000Z",
 "stop_time": "2020-04-17T04:00:00.000Z",
 "condition": "used",
 "permalink": "https://articulo.mercadolibre.com.ar/MLA-839616438-item-de-testeo-por-favor-no-ofertar-kcoff-_JM",
 "thumbnail": "http://mla-s1-p.mlstatic.com/951410-MLA40807113659_022020-I.jpg",
 "secure_thumbnail": "https://mla-s1-p.mlstatic.com/951410-MLA40807113659_022020-I.jpg",
 "pictures": [],
 "video_id": null,
 "descriptions": [
 ],
 "accepts_mercadopago": true,
 "non_mercado_pago_payment_methods": [
 ],
 "shipping": {},
 "international_delivery_mode": "none",
 "seller_address": {},
 "seller_contact": null,
 "location": {
 },
 "geolocation": {},
 "coverage_areas": [
 ],
 "attributes": [],
 "warnings": [
 ],
 "listing_source": "",
 "variations": [
 ],
 "status": "active",
 "sub_status": [
 ],
 "tags": [
 "catalog_listing_eligible",
 "good_quality_picture",
 "test_item",
 "immediate_payment"
 ],
 "warranty": null,
 "catalog_product_id": null,
 "domain_id": "MLA-UNCLASSIFIED_PRODUCTS",
 "parent_item_id": null,
 "differential_pricing": null,
 "deal_ids": [
 ],
 "automatic_relist": false,
 "date_created": "2020-02-17T16:30:40.000Z",
 "last_updated": "2020-02-17T16:34:12.000Z",
 "health": 0.4,
 "catalog_listing": false
}
```

## Publication eligibility with **catalog\_product\_id**

Validates the eligibility of an existing publication, once you have published the item, Mercado Libre automatically tries to associate the best catalog product with which to link the publication, through the **catalog\_product\_id** attribute.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/catalog_listing_eligibility
```

Example of a publication with variations:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA123456789/catalog_listing_eligibility
```

Response:

```
{
 "id": "MLA123456789",
 "site_id": "MLA",
 "domain_id": "MLA-CELLPHONES",
 "status": null,
 "buy_box_eligible": null,
 "reason": null,
 "status": null,
 "variations": [
 {
 "id": 1312323,
 "status": "READY_FOR_OPTIN",
 "buy_box_eligible": true
 },
 {
 "id": 1312444,
 "status": "READY_FOR_OPTIN",
 "buy_box_eligible": true
 }
 ],
 "site_items": []
}
```

Example of a publication without variations:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLB1234/catalog_listing_eligibility 
```

Response:

```
{
 "id": "MLB1234",
 "site_id": "MLB",
 "domain_id": "MLB-MICROWAVES",
 "buy_box_eligible": true,
 "reason": null,
 "status": "READY_FOR_OPTIN",
 "variations": [],
 "site_items": []
}
```

### Considerations

* If the item does not have variations, the eligibility will be expressed through the first level **buy\_box\_eligible** field in the json of the response and the variations section will be empty.
* If the item has variations, the eligibility of each of them will be expressed within the variations section, which will contain an array per variation with a **buy\_box\_eligible** field for each of them.

### Description of fields

**id**: ID of the publication we are consulting. 
**site\_id**: ID of the site to which the item belongs. 
**domain\_id**: ID of the domain to which the item belongs. 
**buy\_box\_eligible**: indicates whether the item/variation is enabled or not to participate in the catalog. 
**variations**: are all the variations that an item has. Each one will have associated a status and a value for the **buy\_box\_eligible** field. 
**status**: defines the situation of the traditional item with respect to the catalog. The different states may be: 

* **READY\_FOR\_OPTIN**: the publication is eligible and can be opted into the catalog.
* **ALREADY\_OPTED\_IN**: the publication already has an associated catalog item.
* **CLOSED**: the publication is in a status that prevents it from continuing to be sold.
* **PRODUCT\_INACTIVE**: the publication is associated with a product that has not yet been enabled for catalog or the item does not yet have **catalog\_product\_id** assigned.
* **NOT\_ELIGIBLE**: there is a business rule that prevents the item from being catalog-enabled (e.g., a used product, an unlocked cell phone).
* **COMPETING**: the consulted catalog item is in competition.

 

## Check multiple eligible publications

To check if multiple publications are eligible for catalog, make a single request. You must incorporate the ids parameter in the url, in addition to request the multiget resource, as follows:

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/multiget/catalog_listing_eligibility?ids=$ITEM_ID,$ITEM_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN'https://api.mercadolibre.com/multiget/catalog_listing_eligibility?ids=MLA818878419,MLA820167922
```

Response with multiget:

```
[
 {
 "id": "MLA820167922",
 "site_id": "MLA",
 "domain_id": "MLA-CELLPHONES",
 "buy_box_eligible": null,
 "reason": null,
 "status": null,
 "variations": [
 {
 "id": 44931385066,
 "status": "READY_FOR_OPTIN",
 "buy_box_eligible": true
 {
 "id": 44931385069,
 "status": "ALREADY_OPTED_IN",
 "buy_box_eligible": true
 }
 ],
 "site_items": []
 },
 {
 "id": "MLA818878419",
 "site_id": "MLA",
 "domain_id": "MLA-CELLPHONES",
 "buy_box_eligible": null,
 "reason": null,
 "status": null,
 "variations": [
 {
 "id": 44612657634,
 "status": "NOT_ELIGIBLE",
 "buy_box_eligible": false,
 "reason": "status_not_active_nor_paused_by_stock_nor_under_review_by_buy_box"
 },
 {
 "id": 44890704657,
 "status": "NOT_ELIGIBLE",
 "buy_box_eligible": false,
 "reason": "status_not_active_nor_paused_by_stock_nor_under_review_by_buy_box"
 }
 ],
 "site_items": []
 }
 ]
```

**Next**: [Product search](https://global-selling.mercadolibre.com/devsite/products-search-gs).
