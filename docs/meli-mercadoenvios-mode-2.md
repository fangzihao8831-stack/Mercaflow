URL: https://developers.mercadolibre.com.ar/en_us/mercadoenvios-mode-2
Title: Developers

## Mercado Envios 2

With these guides we will help you publish a product with Mercado Envíos 2 and manage the entire shipping process using our API resources. Remember that the dimensions of the packages are stipulated by Mercado Libre and cannot be manipulated by the user. If you want to activate Mercado Envíos 2, you can do it from each country ([Argentina](http://envios.mercadolibre.com.ar/), [Brasil](http://envios.mercadolivre.com.br/), [Colombia](http://envios.mercadolibre.com.co/), [México](http://envios.mercadolibre.com.mx/), [Chile](http://envios.mercadolibre.cl/), [Uruguay](https://envios.mercadolibre.com.uy/)).

## Logistic type

The different logistic types are:

* Mercado Envíos (drop\_off): seller [print the label](https://developers.mercadolibre.com.ar/en_us/mercadoenvios-mode-2#Print-shipping-labels) and make the shipment in the mail. Also, you need to consider the shipping status. About billing: it is not mandatory but in case the seller needs it, it is possible [upload invoices](https://developers.mercadolibre.com.ar/en_us/upload-invoices) or can use the Mercado Libre biller.
* [Mercado Envíos Places](https://developers.mercadolibre.com.ar/es_ar/places-xd-drop-off) (xd\_drop\_off): Only in MLA, MLB, MCO and MLM.
* [Mercado Envíos Coleta](https://developers.mercadolibre.com.ar/es_ar/envios-colecta-cross-docking) (cross\_docking): Solo en MLA, MLB, MLM and MLU.
* [Mercado Envíos Flex](https://developers.mercadolibre.com.ar/en_us/mercado-envios-flex) (self\_service): Only in MLA, MLB, MLC, MCO y MLU.
* [Mercado Envíos Full](https://developers.mercadolibre.com.ar/es_ar/mercado-envios-full-fulfillment) (fulfillment): Only in MLA, MLB, MLM, MLC and MCO.

 

## Offering ME2 on your products

Use POST to list. Be sure to inform [the mandatory attributes required by the category](https://developers.mercadolibre.com.ar/en_us/attributes#Mandatory-attributes) and the attributes required by the domain.

 

```
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -d 
 {
 "title": "Item de teste",
 "category_id": "MLA91727",
 "price": 1200,
 "currency_id": "ARS",
 "available_quantity": 2,
 "buying_mode": "buy_it_now",
 "listing_type_id": "bronze",
 "condition": "new",
 "description": "test",
 "pictures": [
 {
 "source": "http://upload.wikimedia.org/wikipedia/commons/f/fd/Ray_Ban_Original_Wayfarer.jpg"
 },
 {
 "source": "http://en.wikipedia.org/wiki/File:Teashades.gif"
 }
 ],
 "shipping": {
 "mode": "me2",
 "local_pick_up": false,
 "free_shipping": false,
 "free_methods": []
 }
 }
 https://api.mercadolibre.com/items
```

Remember that to publish in categories marked as Fragile, the user should also be flagged as "fragile," and will need to have a business agreement. In the following API calls you must validate the fields that are shown below:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/users/$USER_ID/shipping_preferences

 {
 "local_pick_up": false,
 "modes": [
 "custom",
 "not_specified",
 "me1",
 "me2"
 ],
 "trusted_user": true,
 "custom_calculator": false,
 "picking_type": "cross_docking",
 "thermal_printer": null,
 "option": "in",
 "tags": [
 ],
 "carrier_pickup": false,
 "items_combination": "enabled",
 "services": [
 311,
 591,
 671,
 801,
 881,
 1181,
 1191,
 136261
 ],
 "logistics": [
 { 
 "mode": "me1",
 "types": [
 {
 "type": "default",
 "carrier_pickup": [],
 "services": [
 21,
 23,
 22,
 11
 ],
 "default": true
 }
 ]
 },
 
 {"mode": "me2",
 "types": [
 {
 "type": "cross_docking",
 "carrier_pickup": [
 17501840
 ],
 "services": [
 311,
 591,
 671,
 801,
 881,
 1181,
 1191
 ],
 "default": false
 },
 {
 "type": "self_service",
 "carrier_pickup": [
 ],
 "services": [
 136261
 ],
 "default": false
 }
 ]
 },
 {
 "mode": "custom",
 "types": [
 {
 "type": "custom",
 "carrier_pickup": [
 ],
 "services": null,
 "default": true
 }
 ]
 },
 {
 "mode": "not_specified",
 "types": [
 {
 "type": "not_specified",
 "carrier_pickup": [
 ],
 "services": null,
 "default": true
 }
 ]
 }
 ],
 "content_declaration_disabled": false,
 "conciliation": {
 "type": null
 },
 "mandatory_invoice_data": false,
 "site_id": "MLA",
 "free_configurations": [
 {
 "condition": {
 "value": null,
 "type": "all"
 },
 "rule": {
 "default": true,
 "free_mode": "country",
 "value": null
 }
 }
 ],
 "mandatory_settings": {
 }
 }
```

"trusted\_user": true (API users)

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/categories/MCO7159/shipping_preferences
 {
 "category_id": "MCO7159",
 "dimensions": {
 "weight": 50000,
 "height": 20,
 "width": 60,
 "length": 130
 },
 "logistics": [
 {
 "types": [
 "default"
 ],
 "mode": "me1"
 },
 {
 "types": [
 "drop_off",
 "xd_drop_off",
 "cross_docking",
 "fulfillment"
 ],
 "mode": "me2"
 },
 {
 "types": [
 "not_specified"
 ],
 "mode": "not_specified"
 },
 {
 "types": [
 "custom"
 ],
 "mode": "custom"
 }
 ],
 "restricted": true
 }
```

## Required attributes by domain

You will have to validate which are the attributes that according to the domain will be required to be reported in order **to determine if the item is a candidate to be sent by me2 or not**.

Request:

```
curl -X GET 'Authorization: Bearer $ACCESS_TOKEN' http://api.mercadolibre.com/catalog_domains/$DOMAIN_ID/shipping_attributes
```

Request example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/catalog_domains/MLB-AUTOMOTIVE_TIRES/shipping_attributes
```

Response example:

```
{
 "domain_id": "MLB-AUTOMOTIVE_TIRES",
 "attributes": [
 {
 "id": "RIM_DIAMETER",
 "type": "NUMBER_UNIT",
 "unit": "\"",
 "index": 1,
 "ranges": null
 },
 {
 "id": "TIRES_NUMBER",
 "type": "INTEGER",
 "unit": "",
 "index": 2,
 "ranges": null
 },
 {
 "id": "SECTION_WIDTH",
 "type": "NUMBER_UNIT",
 "unit": "mm",
 "index": 3,
 "ranges": null
 }
 ],
 "client_id": 3536736322237473,
 "date_created": "2022-03-29T13:04:27.912-03:00",
 "last_modified": "2023-07-18T11:31:20.092-03:00"
}
```

### The fields will indicate:

* **domain\_id**: ID of the queried domain.
* **attributes**: Array containing the attributes that must be reported when creating or modifying an item and that will help determine if the item is a candidate to be sent by me2.

 

## Check product delivery date

Important:

It is available in México, Brazil, Argentina and Chile.

To avoid exceeding the capacity of the carriers and that buyers receive the products on time, check the shipment date of the products. Identify shipments of this type by performing a GET to /shipments, incorporating the header 'X-Format-New: true', checking the “buffering” node.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' 'X-Format-New: true' https://api.mercadolibre.com/shipments/$SHIPMENT_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' 'X-Format-New: true' https://api.mercadolibre.com/shipments/40173236996
```

Response:

```
{
 "id":40173236996,
 "external_reference":null,
 "status":"pending",
 "substatus":"buffered",
 "date_created":"2020-10-20T10:08:30.000-04:00",
 "last_updated":"2020-10-20T15:09:22.000-04:00",
 "declared_value":7000,
 "dimensions":{
 "height":14,
 "width":19,
 "length":38,
 "weight":950
 },
 "logistic":{
 "direction":"forward",
 "mode":"me2",
 "type":"xd_drop_off"
 },
 []
 "lead_time":{
 "option_id":3628548109,
 "shipping_method":{
 "id":510545,
 "name":"Express a domicilio",
 "type":"two_days",
 "deliver_to":"address"
 },
 "currency_id":"ARS",
 "cost":0,
 "list_cost":504.99,
 "cost_type":"free",
 "service_id":831,
 "delivery_type":"estimated",
 "estimated_schedule_limit":{
 "date":null
 },
 "buffering":{
 "date":"2020-10-21T20:18:26.000Z" ---> Fecha que podrá realizar el envío
 },
 "estimated_delivery_time":{
 "type":"known",
 "date":"2020-10-22T00:00:00.000-03:00",
 "unit":"hour",
 "offset":{
 "date":null,
 "shipping":null
 },
 "time_frame":{
 "from":null,
 "to":null
 },
 "pay_before":"2020-10-21T00:00:00.000-03:00",
 "shipping":24,
 "handling":24,
 "schedule":null
 },
 "estimated_delivery_limit":{
 "date":null,
 "offset":null
 },
 "estimated_delivery_final":{
 "date":null,
 "offset":null
 },
 "estimated_delivery_extended":{
 "date":null,
 "offset":null
 },
 "estimated_handling_limit":{
 "date":"2020-10-21T00:00:00.000-03:00"
 }
 },
 "tags":[
 "test_shipment"
 ]
}
```

In the buffering “date” field from “buffering” node will be the corresponding date that the package has to be dispatched and that same day we will make the label available for printing.

Note:

For **Drop Shipping**, **Cross Docking** and **Cross Docking Drop Off** order shipments, if the substatus is **“buffered”** you must check the "buffering" node and inform the seller that he will be able to print the label on the date mentioned in the "date" field.

 

## Print shipping labels

Important:

We recommend consulting up to 50 (fifty) shipment\_ids. If you exceed the maximum amount allowed, you will receive a 400 error.

In the sale process, when the buyer completes his purchase (checkout), the seller must print the prepaid label to make the shipment. This tag can be a PDF or ZPL file and you can **get it by consulting the shipment\_labels resource**. 
Make the following GET request with the list of shipping ID and an access token. When the status of the shipments is **ready\_to\_ship you will know that the payment has been processed and the prepaid tag is available**.

To get labels in PDF format, make the following request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/shipment_labels?shipment_ids=$SHIPPING_ID1,$SHIPPING_ID2&response_type=pdf
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/shipment_labels?shipment_ids=20178600648,20182100995&response_type=pdf
```

If you want the tags in ZPL format, change response\_type=pdf to response\_type=zpl2:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/shipment_labels?shipment_ids=$SHIPPING_ID&response_type=zpl2
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/shipment_labels?shipment_ids=20178600648&response_type=zpl2
```

This resource returns a ZIP file that includes a PDF with the PLP and a TXT file for a Zebra printer.

Note:

To reprint the label, perform the same GET.

 

## Considerations on label types by site

| Printing type | Printer | Availables sites | Response type | Output |
| --- | --- | --- | --- | --- |
| PDF | Common printer | Argentina (MLA), México (MLM), Brasil (MLB), Colombia (MCO), Chile (MLC) and Uruguay (MLU) | response\_type=pdf | PDF label |
| ZPL2 | Thermal printer | Argentina (MLA), México (MLM), Brasil (MLB), Chile (MLC), Uruguay (MLU), Colombia (MCO | response\_type=pdf | Zip file with the tag in txt format and print summary in pdf format. |

 

## Consult cart shipments

Important:

Shopping cart is available in Argentina, Brazil, Mexico, Chile and Colombia. Coming soon in Uruguay.

With the shopping cart, shoppers can take more advantage of shipping. When they are visiting your publications, we will recommend them your other products to add to the cart. If they buy multiple products from you, shoppers will be able to get free shipping or discounted shipping. 
With the current orders JSON structure, the shipping information is no longer available, only the ID will be available. Thus, you can get the additional information in [the /shipments resource](https://developers.mercadolibre.com.ar/en_us/shipment-handling). 
To work with the updated JSON, when doing the GET you will have to send the parameter "x-format-new: true". The rest of the resource structure will continue to work the same way, with some modifications that you will have to take into account.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/orders/$ORDER_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/orders/2053577644
```

Response:

```
{
 "id": 2053577644,
 "date_created": "2019-06-13T09:20:02.000-04:00",
 "date_closed": "2019-06-13T09:20:08.000-04:00",
 "last_updated": "2019-06-13T09:20:08.000-04:00",
 "manufacturing_ending_date": null,
 "feedback": {
 "sale": null,
 "purchase": null
 },
 "mediations": [],
 "comments": null,
 "pack_id": 2000000101334825,
 "pickup_id": null,
 "order_request": {
 "return": null,
 "change": null
 },
 "fulfilled": null,
 "total_amount": 9.99,
 "paid_amount": 9.99,
 "coupon": {
 "id": null,
 "amount": 0
 },
 "expiration_date": "2019-07-11T09:20:08.000-04:00",
 "order_items": [
 
 "item": {
 "id": "MLB1226730704",
 "title": "Produto Teste - Não Ofertar",
 "category_id": "MLB11742",
 "variation_id": null,
 "seller_custom_field": null,
 "variation_attributes": [],
 "warranty": "12 months",
 "condition": "new",
 "seller_sku": null
 },
 "quantity": 1,
 "unit_price": 9.99,
 "full_unit_price": 9.99,
 "currency_id": "BRL",
 "manufacturing_days": null
 
 ],
 "currency_id": "BRL",
 "payments": [
 
 "id": 4863317779,
 "order_id": 2053577644,
 "payer_id": 419067349,
 "collector": {
 "id": 419059118
 },
 "card_id": null,
 "site_id": "MLB",
 "reason": "Produto Teste - Não Ofertar",
 "payment_method_id": "account_money",
 "currency_id": "BRL",
 "installments": 1,
 "issuer_id": null,
 "atm_transfer_reference": {
 "company_id": null,
 "transaction_id": null
 },
 "coupon_id": null,
 "activation_uri": null,
 "operation_type": "regular_payment",
 "payment_type": "account_money",
 "available_actions": [
 "refund"
 ],
 "status": "approved",
 "status_code": null,
 "status_detail": "accredited",
 "transaction_amount": 9.99,
 "taxes_amount": 0,
 "shipping_cost": 0,
 "coupon_amount": 0,
 "overpaid_amount": 0,
 "total_paid_amount": 9.99,
 "installment_amount": null,
 "deferred_period": null,
 "date_approved": "2019-06-13T09:20:07.000-04:00",
 "authorization_code": null,
 "transaction_order_id": null,
 "date_created": "2019-06-13T09:20:07.000-04:00",
 "date_last_modified": "2019-06-13T09:20:07.000-04:00"
 
 ],
 "shipping": {
 "id": 27987243797
 },
 "status": "paid",
 "status_detail": null,
 "tags": [
 "test_order",
 "pack_order",
 "paid"
 ],
 "buyer": {
 "id": 419067349,
 "nickname": "TT763866",
 "email": "ttest.6hqmq6+2-ogiydkmzvg43tmobx@mail.mercadolivre.com", },
 "first_name": "Test",
 "last_name": "Test",
 "billing_info": {
 "doc_type": "CPF",
 "doc_number": "78525276200"
 
 },
 "seller": {
 "id": 419059118,
 "nickname": "TETE8288849",
 "email": "ttest.hpz2z6q+2-ogiydkmzvg43tmobs@mail.mercadolivre.com",
 "phone": {
 "area_code": "01",
 "extension": "",
 "number": "1111-1111",
 "verified": false
 },
 "alternative_phone": {
 "area_code": "",
 "extension": "",
 "number": ""
 },
 "first_name": "Test",
 "last_name": "Test"
 },
 "taxes": {
 "amount": null,
 "currency_id": null
 
 }
```

The response does not return the total\_amount\_with\_shipping field, which must be calculated. To understand what each of the parameters refers to make the following call:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/orders/$ORDER_ID?options
```

## Calculate total amount with shipping

With our orders resource you can calculate the total amount with shipping.

### Considerations

* The "pack\_order" tag is generated automatically to be able to discriminate if the order is associated with a cart and cannot be deleted by the buyer or the seller.
* The "pack\_id" field shows the cart number to which the order belongs.
* In case the order is not associated with a Shopping Cart and the transaction is under the "agree with seller" mode, you will no longer receive a status to be agreed but directly the shipping ID will be displayed as null. This will give you the indication that you will have to contact the buyer to coordinate the shipping method.
* You will only have the shipping ID, and then go to the new Shipping resources to find the information.
* There is a possibility that, even if there is an order, the shipment may take some time to be created. In such cases the ID will be null until it is created. When that happens, you will be notified.
* The tags "delivered/not delivered" will no longer be added automatically. The tag will only exist if the integrator performs a PUT with the defined tag.
* Orders in paid status will be canceled if the payment is rejected or returned. If this happens, you will receive a notification to let you know the change in the order status.

Important:

The Order will still display the "seller\_custom\_field" field, but will display the data loaded with the following criteria used to choose SKU information: 
1- SELLER\_SKU of variation attributes. 
2- seller\_custom\_field of variation 
3- SELLER\_SKU of item attributes 
4- seller\_custom\_field of item. 

### Possible errors

400: consistency validations:

* Required fields are incomplete.
* The format of the IDsids is incorrect.

401: invalid token. 
403: missing permissions. 
404: Bad Request - the specified item, products or domains do not exist.

Next: [Calculate shipping costs & handling time](https://developers.mercadolibre.com.ar/en_us/calculate-shipping-costs-handling-time).
