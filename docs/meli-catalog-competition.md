URL: https://developers.mercadolibre.com.ar/en_us/catalog-competition
Title: Developers

## Catalog competition

In catalog, publications compete for the sales of the product page and an algorithm determines who will be the winner of those sales based on characteristics of the publication and the seller itself, such as **Price**, **interest-free fees**, **full shipping**, **free shipping** or **in the same day**.

## Notification for status changes

With the **Item competition** topic you can subscribe and start [receive notifications](https://developers.mercadolibre.com.ar/en_us/products-receive-notifications) of the change of status of catalog items, and will allow you to recognize the item that modifies its competition status to winner.

 

## Competition detail

With the resource **/price\_to\_win?siteId=$SITE\_ID&version=v2** you recognize detail information about the status of the catalog publication: it may be winning, sharing first, losing or listed. When a publication has a listed status it means that it cannot win in the catalog because it does not comply with certain reasons that prevent it from competing, but it is still a publication that a buyer can purchase and view from Mercado Libre's main search engine.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/price_to_win?siteId=$SITE_ID&version=v2
```

Example of a request to a publication that is losing in the competition:

```

curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1234567/price_to_win?version=v2
```

Response with **status:competing**:

```
{
 "item_id": "MLA930793214",
 "current_price": 267999,
 "currency_id": "ARS",
 "price_to_win": 267999,
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ],
 "status": "winning",
 "consistent": true,
 "visit_share": "maximum",
 "competitors_sharing_first_place": 0,
 "reason": [],
 "catalog_product_id": "MLA16163648",
 "winner": {
 "item_id": "MLA930793214",
 "price": 267999,
 "currency_id": "ARS",
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ]
 }
}
```

Example of request for a publication that is winning in the competition:

```

curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA765432/price_to_win?version=v2
```

Response with status:winning:

```
{
 "item_id": "MLA930793214",
 "current_price": 267999,
 "currency_id": "ARS",
 "price_to_win": 267999,
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ],
 "status": "winning",
 "consistent": true,
 "visit_share": "maximum",
 "competitors_sharing_first_place": 0,
 "reason": [],
 "catalog_product_id": "MLA16163648",
 "winner": {
 "item_id": "MLA930793214",
 "price": 267999,
 "currency_id": "ARS",
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ]
 }
}
```

Example of a request for a publication that is sharing first place in the competition:

Nota:

The **status:sharing\_first\_place** identifies all sellers who according to the terms of the offer currently share the first place as the **winner**.

```

curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA9876543/price_to_win?version=v2
```

Response with **status: sharing\_first\_place**:

```
{
 "item_id": "MLA9876543",
 "current_price": 493000,
 "currency_id": "ARS",
 "price_to_win": 485109,
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ],
 "status": "sharing_first_place",
 "consistent": true,
 "visit_share": "medium",
 "competitors_sharing_first_place": 1,
 "reason": [],
 "catalog_product_id": "MLA15934914",
 "winner": {
 "item_id": "MLA765432",
 "price": 48150,
 "currency_id": "ARS",
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas al mismo precio que publicaste"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "opportunity",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ]
 }
}
```

Example of a request for a publication that is not in competition:

```

curl -X GET https://api.mercadolibre.com/items/MLA1146313673/price_to_win?access_token=$ACCESS_TOKEN
```

Response:

```
{
 "item_id": "MLA1146313673",
 "current_price": 239999,
 "currency_id": "ARS",
 "price_to_win": null,
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "opportunity",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ],
 "status": "listed",
 "consistent": true,
 "visit_share": "minimum",
 "competitors_sharing_first_place": null,
 "reason": [
 "reputation_below_threshold"
 ],
 "catalog_product_id": "MLA16163648",
 "winner": {
 "item_id": "MLA930793214",
 "price": 267999,
 "currency_id": "ARS",
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "boosted",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ]
 }
}
```

Example of a request for a publication that is not in competition:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA456789/price_to_win?version=v2
```

Response with **status: listed:**

```

{
 "item_id": "MLA456789",
 "current_price": 239999,
 "currency_id": "ARS",
 "price_to_win": null,
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas sin interés"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "opportunity",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ],
 "status": "listed",
 "consistent": true,
 "visit_share": "minimum",
 "competitors_sharing_first_place": null,
 "reason": [
 "reputation_below_threshold"
 ],
 "catalog_product_id": "MLA15934914",
 "winner": {
 "item_id": "MLA765432",
 "price": 48150,
 "currency_id": "ARS",
 "boosts": [
 {
 "id": "fulfillment",
 "status": "opportunity",
 "description": "Mercado Envíos Full"
 },
 {
 "id": "free_installments",
 "status": "opportunity",
 "description": "Cuotas al mismo precio que publicaste"
 },
 {
 "id": "free_shipping",
 "status": "boosted",
 "description": "Envíos gratis por Mercado Envíos"
 },
 {
 "id": "shipping_collect",
 "status": "boosted",
 "description": "Mercado Envíos Colecta"
 },
 {
 "id": "same_day_shipping",
 "status": "opportunity",
 "description": "Envíos en el día por Mercado Envíos"
 }
 ]
 }
}
```

### Response fields

**price\_to\_win**: indicates the price (in the current currency of the publication) so that you have a **more competitive publication**, that is, request PUT to the /items resource with the suggested price, your publication will have a **more competitive price** in the Catalog. 
**boosts**: characteristics of the publication that provide chances of winning, such as:

* **same\_day\_shipping**: shipping on day with Mercado Envíos.
* **fulfillment**: [Mercado Envíos Full](https://developers.mercadolibre.com.ar/es_ar/mercado-envios-full-fulfillment).
* **free\_installments**: interest-free fees.
* **free\_shipping**: [free Shipping](https://developers.mercadolibre.com.ar/es_ar/enviogratis) con Mercado Envios.
* **shipping\_quarantine**: shipping normally.
* **shipping\_collect**: [Mercado Envios Colecta](https://developers.mercadolibre.com.ar/es_ar/envios-colecta-cross-docking).

Now, you can recognize within the boost the state of these and draw a comparison table accordingly.

| **Boost status** | Detail |
| --- | --- |
| **boosted** | It has the condition of sale and currently applies the boost. |
| **not\_boosted** | It has the condition of sale but it is not a boost that improves the chances of winning. |
| **opportunity** | It does not have the condition of sale. If applied, it would improve the chances of winning. |
| **not\_apply** | The sales condition does not apply as a boost to the product where the item competes. |

**status**: the product is winning for the public or for minority segments, for example, as those who do not take advantage of same day shipping. When it is winning, the value is **winning**, otherwise it will be **competing** for the one who is losing, and a new value is added **sharing\_first\_place** for when the first place is shared with other publications of the product page. 
**visit\_share**: the level of visibility your publication has in the catalog. These values can vary depending on the state:

* **Winning**: always will be maximum.
* **Competing**: always will be minimum.
* **Sharing\_first\_place**: always will be medium.
**competitors\_sharing\_first\_place**: the amount of sellers sharing the first place. It will also depend on the state of the publications.

* **Winning**: will always be 0, since by winning, you will take all sales and visibility in the catalog.
* **Competing**: will always be null, since if you lose, you will have to improve the conditions to share the first place or win.
* **Listed**: will always be null, since if you lose, you will have to improve the conditions to share the first place or win.
* **Sharing\_first\_place**: will show the value of sellers that are competing for the first place.

**reason**: Mostrará información únicamente cuando la publicación no esté compitiendo, permitiendo identificar el motivo por el cual no lo está haciendo y así realizar acciones de mejora.

**catalog\_product\_id**: Indica el ID de la página de producto a la que pertenece la publicación.

 
**winner**: Indica el detalle del producto que está actualmente como ganador, permitiendo realizar una comparación rápida, con el item\_id de la publicación que estás consultando, mostrando campos como: **item\_id, price, currency\_id** y **boosts**.

## Reasons

There are different reasons why a publication is not competing within the catalog, below we list all the possible reasons that the [price\_to\_win](https://developers.mercadolibre.com.ar/en_us/catalog-competition?nocache=true#Competition-detail) endpoint will answer in the reason attribute, which will allow you to perform the different actions to improve your publication and enter it to the competition.

| Reason | Description |
| --- | --- |
| non\_trusted\_seller | The seller cannot compete because he is marked as unreliable seller. It appears at the bottom of the list. |
| reputation\_below\_threshold | The seller cannot compete because he does not achieve the reputation needed to win. Appears on the list. |
| item\_reputation\_below\_threshold | The publication cannot compete, as it does not reach the reputation required to win. It appears in the listings. |
| winner\_has\_better\_reputation | The seller has a reputation that could compete but there is a winner with a better reputation. At the moment, it only appears in the listings (yellow case with green winner). |
| manufacturing\_time | The publication has manufacturing team, appears only on the list, and cannot win because the winner has immediate stock. |
| temporarily\_winning\_manufacturing\_time | The publication has manufacturing team, is temporarily winning because there are no competitors at the same level of reputation without manufacturing team. |
| temporarily\_competing\_manufacturing\_time | The publication has a manufacturing team, it is competing temporarily because there are no competitors at the same level of reputation without a manufacturing team, the winner also has a manufacturing team. |
| temporarily\_winning\_best\_reputation\_available | The seller is not green but has a reputation that can win and is the best offer available. He is winning temporarily. If a better offer appears, stop winning. |
| temporarily\_competing\_best\_reputation\_available | The seller is not green, but has the best reputation available, he is competing temporarily. The winner is also of the same reputation. If a better seller comes along, it will go back to just being on the list. |
| item\_paused | The item is paused, it cannot be listed. |
| item\_not\_opted\_in | No optin was made from the publication, it cannot appear in the list, the item\_id call was used from a publication that is not from a catalog or is a test item, so it cannot enter the competition. |
| shipping\_mode | The seller is not competing because their shipping method is inferior to the winner. ME2 > ME1 > Custom Shipping > Not Specified. |
| newbie\_program\_seller | The seller has reached the sales limit defined by the startup dosage program. |

## Winning publication

Using the /products/{product\_id} feature, in addition to knowing the product's features and status, you can recognize by the **buy\_box\_winner** field which publication is winning on the product page. 
Example of a product page detail short answer:

```

 "id": "MLM12345",
 "status": "active",
 "sold_quantity": 391,
 "domain_id": "MLM-CELLPHONES",
 "permalink": "https://www.mercadolibre.com.mx/apple-iphone-13-pro-128-gb-grafito,
 "name": "Apple iPhone 13 Pro (128 GB) - Grafito",
 "family_name": "Apple iPhone 13 Pro",
 "buy_box_winner": {
 "item_id": "MLM987654321",
 "category_id": "MLM1055",
 "seller_id": 1234567,
 "price": 25219,
 "currency_id": "MXN",
 "sold_quantity": 362,
 "available_quantity": 110,
 "shipping": {
 "mode": "me2",
 "tags": [
 "mandatory_free_shipping"
 ],
 "free_shipping": true,
 "logistic_type": "fulfillment",
 "store_pick_up": false
 },
 "warranty": "Garantía de fábrica: 12 meses",
 "condition": "new",
 "sale_terms": [...],
 "official_store_id": 3953,
 "original_price": 25999,
 "listing_type_id": "gold_pro",
 "accepts_mercadopago": true,
 "seller_address": {...},
 "international_delivery_mode": "none",
 "tags": [...],
 "item_override_attributes": [],
 "seller": {
 "reputation_level_id": "GREEN",
 "tags": []
 },
 "deal_ids": [...],
 "tier": "candidate",
 "inventory_id": "DHEV26968",
 "product_id": "MLM18494248",
 "site_id": "MLM"
 },
 "buy_box_winner_price_range": {
 "min": {
 "price": 25219,
 "currency_id": "MXN"
 },
 "max": {
 "price": 38999,
 "currency_id": "MXN"
 }
 },
 "pickers": [... ],
 "pictures": [... ],
 "main_features": [... ],
 "attributes": [... ],
 "short_description": {... },
 "parent_id": "MLM18494246",
 "children_ids": [],
 "settings": {... },
 "buy_box_activation_date": "2022-04-22T15:20:15Z",
 "authority_types": [... ],
 "date_created": "2021-09-27T18:13:54Z"
}
```

## List of publications for a product page

Nota:

Starting 10/01/2025, the /products/$PRODUCT\_ID/items endpoint, which lists listings competing on a catalog product page, will be shut down. We recommend reviewing and adjusting your flows before that date to avoid disruptions. You can continue checking the Buy Box recommendation via: /items/$ITEM\_ID/price\_to\_win?SITE\_ID&version=v2. 

If you need to know which catalog publications (from all sellers) are competing for sales of a particular product page, make the following call:

 

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/$PRODUCT_ID/items
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/MLA18494233/items
```

Simplified response

```
{
 "paging": {
 "total": 41,
 "offset": 0,
 "limit": 100
 },
 "results": [
 {
 "item_id": "MLA1110011006",
 "site_id": "MLA",
 "seller_id": 1234567,
 "accepts_mercadopago": true,
 "sold_quantity": 25,
 "available_quantity": 1,
 "price": 492499,
 "category_id": "MLA1055",
 "currency_id": "ARS",
 "warranty": "Garantía de fábrica: 12 meses",
 "condition": "new",
 "listing_type_id": "gold_special",
 "international_delivery_mode": "none",
 "tier": "",
 "inventory_id": "",
 "tags": [
 "good_quality_picture",
 "good_quality_thumbnail",
 "extended_warranty_eligible",
 "immediate_payment",
 "cart_eligible"
 ],
 "deal_ids": [],
 "official_store_id": null,
 "original_price": null,
 "shipping": {
 "free_shipping": true,
 "store_pick_up": false,
 "mode": "me2",
 "logistic_type": "xd_drop_off",
 "tags": [
 "self_service_in",
 "mandatory_free_shipping"
 ]
 },
 "seller_address": {...
 },
 "sale_terms": [
 {
 "value_struct": null,
 "id": "INVOICE",
 "name": "Facturación",
 "value_name": "Factura A",
 "value_id": "6891885"
 },
 {
 "value_struct": {
 "number": 12,
 "unit": "meses"
 },
 "id": "WARRANTY_TIME",
 "name": "Tiempo de garantía",
 "value_name": "12 meses",
 "value_id": null
 },
 {
 "value_struct": null,
 "id": "WARRANTY_TYPE",
 "name": "Tipo de garantía",
 "value_name": "Garantía de fábrica",
 "value_id": "2230279"
 }
 ]
 },
 {
 "item_id": "MLA1150170600",
 "site_id": "MLA",
 "seller_id": 7654321,
 "accepts_mercadopago": true,
 "sold_quantity": 1,
 "available_quantity": 1,
 "price": 493000,
 "category_id": "MLA1055",
 "currency_id": "ARS",
 "warranty": "Garantía de fábrica: 12 meses",
 "condition": "new",
 "listing_type_id": "gold_special",
 "international_delivery_mode": "none",
 "tier": "",
 "inventory_id": "",
 "tags": [...
 ],
 "deal_ids": [],
 "official_store_id": null,
 "original_price": null,
 "shipping": {...
 },
 "seller_address": {...
 },
 "sale_terms": [...
 ]
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 },
 {...
 }
 ],
 "experiments": null
}
```

Consider that **results** will return all posts on the product page that are competing to win that product.

 

## Filters

Use filters to decrease the response in the resource **/products/$PRODUCT\_ID/items** This filter works the same as the Search **/sites/{site}/search** resource where you can use the values of **available\_filters** as a parameter in the URL. 
Currently, we offer the following filter options:

| Parameters | Value | Description |
| --- | --- | --- |
| official\_store | all | To show only products with winner of Official Stores. |
| official\_store\_id | id | To show the winner products of an Official Store. |
| discount | 10-100 | To show products with a winner with a discount greater than or equal to 10%. |
| price | 100-200 | For products with winner priced between 100 and 200. Depending on the local currency |
| shipping | fulfillment | For products with winner with Fulfillment. |
| shipping | mercadoenvios | For products with winner without Fulfillment. |
| shipping\_cost | free | For products with winner with free shipping. |
| shipping\_time | sameday/ nextday | It must be used together with the query param b.buyer\_zones which indicates in which areas the buyer is located. |
| seller\_id | id | Get the winner user\_id |

Example of request using filters:

```

curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/MLM123456789/items?shipping_cost=free
```

**Next**: [Brand Central.](https://developers.mercadolibre.com.ar/en_us/brand-central)
