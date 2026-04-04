URL: https://developers.mercadolibre.com.ar/en_us/products-search
Title: Developers

## Product search

Before publishing to the catalog on a product page, it is important to confirm that the catalog product is the most appropriate one based on the datasheet of your marketplace publication, and additional characteristics such as item status, price, and so on. The catalog product finder allows you to identify which products you can publish directly in the catalog and/or by associated marketplace publications

Note:

Sellers can **get the Mercado Libre products catalog** ([MLA](https://www.mercadolibre.com.ar/catalogo/explorar#from=dev_site), [MLB](https://www.mercadolivre.com.br/catalogo/explorar#from=dev_site), [MLM](https://www.mercadolibre.com.mx/catalogo/explorar#from=dev_site), [MLC](https://www.mercadolibre.cl/catalogo/explorar#from=dev_site), [MCO](https://www.mercadolibre.com.co/catalogo/explorar#from=dev_site), [MLU](https://www.mercadolibre.com.uy/catalogo/explorar#from=dev_site)) from the front end and, using the product id, publish them through the integration or from the front end itself.

### Parameters

**site\_id**: string that represents the country (required). 
**status**: if you don't send this parameter, by default it will bring all results, both active and inactive.

* **status=active**: returns catalog products with active status, so they can be elected to associate with a marketplace publication.
* **status=inactive**: returns products that are not yet eligible to associate with a marketplace publication, because they are inactive.

**product\_identifier**: string with the universal product code. Example: GTIN that encompasses the different PLs (EAN, UPC, ISBN, etc). Mandatory if you do not send a keyword string in parameter q. 
**q**: string with search keywords, it is important to consider that this field can send details of the attributes of your publication as needed, this way in the response you will get more assertive searches and avoid possible moderations by incorrect productization of marketplace publications. Example: Samsung Galaxy S8 Black 64 GB dual sim phone. This parameter is mandatory if you do not send the **product\_identifier** in the request. 
**domain\_id**: string with the domain where you want to publish (optional). 
**offset**: position that returns the results of the search (optional). 
**limit**: amount of results that returns the search (optional). 

Request with **q** parameter:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search?status=$STATUS_ID&site_id=$SITE_ID&q={q}
```

Example with **q** parameter:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search?status=active&site_id=MLA&q=Samsung 20 Galaxy S8 64 GB rosa'
```

Response with **q** parameter:

```
{
 "keywords": "Samsung 20 Galaxy S8 64 GB rosa",
 "paging": {
 "total": 1,
 "limit": 10,
 "offset": 0
 },
 "results": [
 {
 "id": "MLA16240160",
 "status": "active",
 "domain_id": "MLA-CELLPHONES",
 "settings": {
 "listing_strategy": "catalog_required"
 },
 "name": "Samsung Galaxy S8 64 GB rosa 4 GB RAM",
 "main_features": [],
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "206",
 "value_name": "Samsung"
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "249991",
 "value_name": "Galaxy S"
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "8030",
 "value_name": "S8"
 },
 {
 "id": "IS_DUAL_SIM",
 "name": "Es Dual SIM",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "COLOR",
 "name": "Color",
 "value_id": "51994",
 "value_name": "Rosa"
 },
 {
 "id": "INTERNAL_MEMORY",
 "name": "Memoria interna",
 "value_id": "59726",
 "value_name": "64 GB"
 },
 {
 "id": "RAM",
 "name": "Memoria RAM",
 "value_id": "98852",
 "value_name": "4 GB"
 },
 {
 "id": "MAIN_COLOR",
 "name": "Color principal",
 "value_id": "2450312",
 "value_name": "Rosa"
 },
 {
 "id": "GTIN",
 "name": "Código universal de producto",
 "value_id": "11069790",
 "value_name": "08801643066918"
 },
 {
 "id": "OPERATING_SYSTEM_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "7403813",
 "value_name": "Android"
 },
 {
 "id": "OS_ORIGINAL_VERSION",
 "name": "Versión original del sistema operativo",
 "value_id": "7199644",
 "value_name": "7.0 Nougat"
 },
 {
 "id": "OS_LAST_COMPATIBLE_VERSION",
 "name": "Última versión compatible del sistema operativo",
 "value_id": "9123308",
 "value_name": "10"
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "6927988",
 "value_name": "5.8 \""
 },
 {
 "id": "DISPLAY_RESOLUTION",
 "name": "Resolución de la pantalla",
 "value_id": "7222492",
 "value_name": "1440 px x 2960 px"
 },
 {
 "id": "MAIN_REAR_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara trasera principal",
 "value_id": "7199628",
 "value_name": "12 Mpx"
 },
 {
 "id": "REAR_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara trasera",
 "value_id": "7199630",
 "value_name": "3840 px x 2160 px"
 },
 {
 "id": "MAIN_FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal principal",
 "value_id": "7207052",
 "value_name": "8 Mpx"
 },
 {
 "id": "BATTERY_CAPACITY",
 "name": "Capacidad de la batería",
 "value_id": "98435",
 "value_name": "3000 mAh"
 },
 {
 "id": "WITH_FINGERPRINT_READER",
 "name": "Con lector de huella digital",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "SIM_CARD_SLOTS_NUMBER",
 "name": "Cantidad de ranuras para tarjeta SIM",
 "value_id": "2087812",
 "value_name": "1"
 },
 {
 "id": "COMPATIBLE_SIM_CARD_SIZES",
 "name": "Tamaños de tarjeta SIM compatibles",
 "value_id": "80453",
 "value_name": "Nano-SIM"
 },
 {
 "id": "WITH_ESIM",
 "name": "Con eSIM",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "OS_PERSONALIZATION_LAST_COMPATIBLE_SHELL",
 "name": "Última capa compatible de personalización del sistema operativo",
 "value_id": "11091675",
 "value_name": "One UI 2.0"
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "6845",
 "value_name": "155 g"
 },
 {
 "id": "HEIGHT",
 "name": "Altura",
 "value_id": "6954305",
 "value_name": "148.9 mm"
 },
 {
 "id": "WIDTH",
 "name": "Ancho",
 "value_id": "6954310",
 "value_name": "68.1 mm"
 },
 {
 "id": "DEPTH",
 "name": "Profundidad",
 "value_id": "4604272",
 "value_name": "8 mm"
 },
 {
 "id": "DISPLAY_TECHNOLOGY",
 "name": "Tecnología de la pantalla",
 "value_id": "80493",
 "value_name": "Super AMOLED"
 },
 {
 "id": "DISPLAY_PIXELS_PER_INCH",
 "name": "Píxeles por pulgada de la pantalla",
 "value_id": "7075863",
 "value_name": "570 ppi"
 },
 {
 "id": "WITH_TOUCHSCREEN_DISPLAY",
 "name": "Con pantalla táctil",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_PHYSICAL_QWERTY_KEYBOARD",
 "name": "Con teclado QWERTY físico",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_CAMERA",
 "name": "Con cámara",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477198",
 "value_name": "1"
 },
 {
 "id": "REAR_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara trasera",
 "value_id": "7444371",
 "value_name": "f 1.7"
 },
 {
 "id": "FRONT_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras frontales",
 "value_id": "7477216",
 "value_name": "1"
 },
 {
 "id": "FRONT_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara frontal",
 "value_id": "7222493",
 "value_name": "2560 px x 1440 px"
 },
 {
 "id": "WITH_FRONT_CAMERA_FLASH",
 "name": "Con flash en la cámara frontal",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "MOBILE_NETWORK",
 "name": "Red",
 "value_id": "367876",
 "value_name": "4G/LTE"
 },
 {
 "id": "MEMORY_CARD_TYPES",
 "name": "Tipos de tarjeta de memoria",
 "value_id": "7199655",
 "value_name": "Micro-SD"
 },
 {
 "id": "MEMORY_CARD_MAX_CAPACITY",
 "name": "Capacidad máxima de la tarjeta de memoria",
 "value_id": "6901713",
 "value_name": "512 GB"
 },
 {
 "id": "PROCESSOR_CORES_NUMBER",
 "name": "Cantidad de núcleos del procesador",
 "value_id": "7206961",
 "value_name": "8"
 },
 {
 "id": "WITH_USB_CONNECTOR",
 "name": "Con conector USB",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_WIFI",
 "name": "Con Wi-Fi",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_BLUETOOTH",
 "name": "Con Bluetooth",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_MINI_HDMI",
 "name": "Con mini HDMI",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_RADIO",
 "name": "Con radio",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_TV_TUNER",
 "name": "Con sintonizador de TV",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_ACCELEROMETER",
 "name": "Con acelerómetro",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_PROXIMITY_SENSOR",
 "name": "Con sensor de proximidad",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_GYROSCOPE",
 "name": "Con giroscopio",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "IS_WATERPROOF",
 "name": "Es a prueba de agua",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "BATTERY_TYPE",
 "name": "Tipo de batería",
 "value_id": "95013",
 "value_name": "Ion de litio"
 },
 {
 "id": "WITH_REMOVABLE_BATTERY",
 "name": "Con batería removible",
 "value_id": "242084",
 "value_name": "No"
 }
 ],
 "pictures": [
 {
 "id": "839840-MLA44098967985_112020",
 "url": "https://mla-s2-p.mlstatic.com/839840-MLA44098967985_112020-F.jpg"
 },
 {
 "id": "691918-MLA44099561087_112020",
 "url": "https://mla-s2-p.mlstatic.com/691918-MLA44099561087_112020-F.jpg"
 },
 {
 "id": "740790-MLA44098967958_112020",
 "url": "https://mla-s1-p.mlstatic.com/740790-MLA44098967958_112020-F.jpg"
 },
 {
 "id": "821696-MLA44098967963_112020",
 "url": "https://mla-s2-p.mlstatic.com/821696-MLA44098967963_112020-F.jpg"
 },
 {
 "id": "626553-MLA44098967962_112020",
 "url": "https://mla-s2-p.mlstatic.com/626553-MLA44098967962_112020-F.jpg"
 }
 ],
 "parent_id": "MLA6408697",
 "children_ids": []
 }
 ]
}
```

Request with **q** and **domain\_id parameters**:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search?status=$STATUS_ID&site_id=$SITE_ID&q={q}&domain_id=$DOMAIN_ID
```

Example with **q** and **domain\_id parameters**:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com//products/search?status=active&site_id=MLA&q=Samsung Series 8 QN55Q8CAMGXZS&domain_id=MLA-TELEVISIONS
```

Response with **q** and **domain\_id parameters**:

```
{
 "keywords": "Samsung Series 8 QN55Q8CAMGXZS",
 "domain_id": "MLA-TELEVISIONS",
 "paging": {
 "total": 1,
 "limit": 10,
 "offset": 0
 },
 "results": [
 {
 "id": "MLA10043973",
 "status": "active",
 "domain_id": "MLA-TELEVISIONS",
 "settings": {
 "listing_strategy": "catalog_required"
 },
 "name": "Smart TV Samsung Series 8 QN55Q8CAMGXZS QLED curvo 4K 55\"",
 "main_features": [],
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "206",
 "value_name": "Samsung"
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "106912",
 "value_name": "Series 8"
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "3380256",
 "value_name": "QN55Q8C"
 },
 {
 "id": "ALPHANUMERIC_MODEL",
 "name": "Modelo alfanumérico",
 "value_id": "7651078",
 "value_name": "QN55Q8CAMGXZS"
 },
 {
 "id": "DISPLAY_TYPE",
 "name": "Tipo de pantalla",
 "value_id": "3575905",
 "value_name": "QLED"
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "2538310",
 "value_name": "55 \""
 },
 {
 "id": "RESOLUTION_TYPE",
 "name": "Tipo de resolución",
 "value_id": "2685890",
 "value_name": "4K"
 },
 {
 "id": "IS_SMART",
 "name": "Es smart",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "IS_CURVED",
 "name": "Es curvo",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_HDR",
 "name": "Con HDR",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_USB",
 "name": "Con USB",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_HDMI",
 "name": "Con HDMI",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "MAX_RESOLUTION",
 "name": "Resolución máxima",
 "value_id": "7165730",
 "value_name": "3840 px - 2160 px"
 },
 {
 "id": "ASPECT_RATIO",
 "name": "Relación de aspecto",
 "value_id": "493284",
 "value_name": "16:9"
 },
 {
 "id": "HDMI_PORTS_NUMBER",
 "name": "Cantidad de puertos HDMI",
 "value_id": "1160534",
 "value_name": "4"
 },
 {
 "id": "USB_PORTS_NUMBER",
 "name": "Cantidad de puertos USB",
 "value_id": "972678",
 "value_name": "3"
 },
 {
 "id": "WITH_WI_FI",
 "name": "Con Wi-Fi",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_BLUETOOTH",
 "name": "Con Bluetooth",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_ETHERNET",
 "name": "Con ethernet",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WIDTH",
 "name": "Ancho",
 "value_id": "8109538",
 "value_name": "122.33 cm"
 },
 {
 "id": "DEPTH",
 "name": "Profundidad",
 "value_id": "8109539",
 "value_name": "9.08 cm"
 },
 {
 "id": "HEIGHT",
 "name": "Altura",
 "value_id": "8109537",
 "value_name": "70.4 cm"
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "203370",
 "value_name": "20 kg"
 },
 {
 "id": "PROCESSOR_CORES_NUMBER",
 "name": "Cantidad de núcleos del procesador",
 "value_id": "7206949",
 "value_name": "4"
 },
 {
 "id": "SPEAKERS_NUMBER",
 "name": "Cantidad de parlantes",
 "value_id": "8019559",
 "value_name": "6"
 },
 {
 "id": "MAX_SPEAKERS_POWER",
 "name": "Potencia máxima de los parlantes",
 "value_id": "7861486",
 "value_name": "60 W"
 },
 {
 "id": "SOUND_MODES",
 "name": "Modos de sonido",
 "value_id": "9872544",
 "value_name": "Dolby Digital Plus"
 },
 {
 "id": "WITH_AUTO_POWER_OFF",
 "name": "Con apagado automático",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_SCREEN_SHARE_FUNCTION",
 "name": "Con función screen share",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_INTEGRATED_VOICE_COMMAND",
 "name": "Con comando de voz integrado",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "ACCESSORIES_INCLUDED",
 "name": "Accesorios incluidos",
 "value_name": "Control remoto, Baterías, Cable de alimentación"
 },
 {
 "id": "INTEGRATED_APPS",
 "name": "Apps integradas",
 "value_name": "YouTube, Netflix, Web browser"
 }
 ],
 "pictures": [
 {
 "id": "678632-MLA41117772725_032020",
 "url": "https://mla-s2-p.mlstatic.com/678632-MLA41117772725_032020-F.jpg"
 },
 {
 "id": "612086-MLA41083915326_032020",
 "url": "https://mla-s1-p.mlstatic.com/612086-MLA41083915326_032020-F.jpg"
 },
 {
 "id": "987608-MLA41083724576_032020",
 "url": "https://mla-s1-p.mlstatic.com/987608-MLA41083724576_032020-F.jpg"
 },
 {
 "id": "944355-MLA41083915348_032020",

 "url": "https://mla-s2-p.mlstatic.com/944355-MLA41083915348_032020-F.jpg"
 }
 ],
 "children_ids": []
 }
 ]
}
```

Request with **product\_identifier** parameter:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search?status=$STATUS_ID&site_id=$SITE_ID&product_identifier=$PRODUCT_IDENTIFIER
```

Example with **product\_identifier** parameter:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search?status=active&site_id=MLA&product_identifier=0123456789
```

Response with **product\_identifier** parameter:

```
{ 
 "product_identifier": "0123456789", 
 "paging": {
 "total": 10, 
 "offset": 0, 
 "limit": 10 
 }, 
 "results": [ 
{
 "id": "MLA14719808",
 "status": "active",
 "domain_id": "MLA-TABLETS",
 "settings": {
 "listing_strategy": "catalog_required"
 },
 "name": "iPad Apple 6th generation 2018 A1954 9.7\" con red móvil 32GB gold y 2GB de memoria RAM",
 "main_features": [],
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "9344",
 "value_name": "Apple"
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "107662",
 "value_name": "iPad"
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "10351421",
 "value_name": "6th generation"
 },
 {
 "id": "VERSION",
 "name": "Versión",
 "value_id": "3640650",
 "value_name": "2018"
 },
 {
 "id": "ALPHANUMERIC_MODEL",
 "name": "Modelo alfanumérico",
 "value_id": "7657201",
 "value_name": "A1954"
 },
 {
 "id": "WITH_MOBILE_NETWORK",
 "name": "Con red móvil",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "COLOR",
 "name": "Color",
 "value_id": "59628",
 "value_name": "Gold"
 },
{
 "id": "GTIN",
 "name": "Código universal de producto",
 "value_id": null,
 "value_name": "0123456789",
 },

 {
 "id": "RAM_MEMORY",
 "name": "Memoria RAM",
 "value_id": "445970",
 "value_name": "2 GB"
 },
 {
 "id": "CAPACITY",
 "name": "Capacidad",
 "value_id": "18621",
 "value_name": "32 GB"
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "3912629",
 "value_name": "9.7 \""
 },
 {
 "id": "MAIN_COLOR",
 "name": "Color principal",
 "value_id": "2450289",
 "value_name": "Dorado"
 },
 {
 "id": "OS_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "4743193",
 "value_name": "iOS"
 },
 {
 "id": "OS_VERSION",
 "name": "Versión del sistema operativo",
 "value_id": "12909372",
 "value_name": "12.0"
 },
 {
 "id": "CONNECTIVITY",
 "name": "Conectividad",
 "value_name": "Bluetooth, Conector lightning, Smart connector, Wi-Fi"
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477198",
 "value_name": "1"
 },
 {
 "id": "BLUETOOTH_VERSION",
 "name": "Versión bluetooth",
 "value_id": "12008875",
 "value_name": "4.2"
 },
 {
 "id": "SIM_CARD_READERS",
 "name": "Lectores de tarjetas SIM",
 "value_id": "82830",
 "value_name": "Nano SIM"
 },
 {
 "id": "SENSORS",
 "name": "Sensores",
 "value_name": "Acelerómetro, Barómetro, Sensor de huella digital, Sensor de luz ambiente"
 },
 {
 "id": "CHIPSET",
 "name": "Chipset",
 "value_id": "7657199",
 "value_name": "Apple A10 Fusion"
 },
 {
 "id": "IS_MULTI_TOUCH",
 "name": "Es multi-touch",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_FLASH",
 "name": "Con flash",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_HEADPHONES_OUTPUT",
 "name": "Con salida para auriculares",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "PROCESSOR_SPEED",
 "name": "Velocidad del procesador",
 "value_id": "6877633",
 "value_name": "2.34 GHz"
 },
 {
 "id": "BATTERY_CAPACITY",
 "name": "Capacidad de la batería",
 "value_id": "7185348",
 "value_name": "8827 mAh"
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "1188",
 "value_name": "480 g"
 },
 {
 "id": "PIXELS_PER_INCH",
 "name": "Píxeles por pulgada",
 "value_id": "7749453",
 "value_name": "264 ppi"
 },
 {
 "id": "TABLET_REAR_CAMERAS_RESOLUTIONS",
 "name": "Resoluciones de las cámaras traseras",
 "value_id": "902414",
 "value_name": "8 Mpx"
 },
 {
 "id": "FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal",
 "value_id": "902404",
 "value_name": "1.2 Mpx"
 },
 {
 "id": "MAX_SCREEN_RESOLUTION",
 "name": "Máxima resolución de pantalla",
 "value_id": "1151117",
 "value_name": "2048 px x 1536 px"
 },
 {
 "id": "CORES_NUMBER",
 "name": "Cantidad de núcleos",
 "value_id": "6838527",
 "value_name": "4"
 }
 ],
 "pictures": [
 {
 "id": "777713-MLA32660788040_102019",
 "url": "https://mla-s2-p.mlstatic.com/777713-MLA32660788040_102019-F.jpg"
 },
 {
 "id": "611193-MLA32649508843_102019",
 "url": "https://mla-s1-p.mlstatic.com/611193-MLA32649508843_102019-F.jpg"
 },
 {
 "id": "748220-MLA32660542682_102019",
 "url": "https://mla-s1-p.mlstatic.com/748220-MLA32660542682_102019-F.jpg"
 }
 ],
 "parent_id": "MLA9592536",
 "children_ids": []
 }

 ] 
 }
```

Example with catalog attributes:

```
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/search
{
 "domain_id":"MLA-CELLPHONES",
 "site_id":"MLA",
 "status":"active",
 "attributes": [
 {
 "id": "BRAND",
 "value_id": "206"
 },
 {
 "id": "LINE",
 "value_name": "Galaxy"
 },
 {
 "id": "IS_DUAL_SIM",
 "value_name": "Si"
 }
 ]
}
```

Short response with catalog attributes:

```
{
 "domain_id": "MLA-CELLPHONES",
 "paging": {
 "total": 9,
 "limit": 10,
 "offset": 0
 },
 "results": [
 {
 "id": "MLA13316403",
 "status": "active",
 "domain_id": "MLA-CELLPHONES",
 "settings": {
 "listing_strategy": "open"
 },
 "name": "Samsung Galaxy Folder 2 Dual SIM 16 GB Negro 2 GB RAM",
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "206",
 "value_name": "Samsung"
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "43675",
 "value_name": "Galaxy"
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "8212554",
 "value_name": "Folder 2 Duos"
 },
 {
 "id": "IS_DUAL_SIM",
 "name": "Es Dual SIM",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "COLOR",
 "name": "Color",
 "value_id": "52049",
 "value_name": "Negro"
 },
 {
 "id": "INTERNAL_MEMORY",
 "name": "Memoria interna",
 "value_id": "59561",
 "value_name": "16 GB"
 },
 {
 "id": "RAM",
 "name": "Memoria RAM",
 "value_id": "445970",
 "value_name": "2 GB"
 },
 {
 "id": "MAIN_COLOR",
 "name": "Color principal",
 "value_id": "2450295",
 "value_name": "Negro"
 },
 {
 "id": "OPERATING_SYSTEM_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "7403813",
 "value_name": "Android"
 },
 {
 "id": "OPERATING_SYSTEM_VERSION",
 "name": "Versión del sistema operativo",
 "value_id": "7206970",
 "value_name": "6.0 Marshmallow"
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "7762087",
 "value_name": "3.8 \""
 },
 {
 "id": "DISPLAY_RESOLUTION",
 "name": "Resolución de la pantalla",
 "value_id": "7222488",
 "value_name": "480 px x 800 px"
 },
 {
 "id": "MAIN_REAR_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara trasera principal",
 "value_id": "7199614",
 "value_name": "8 Mpx"
 },
 {
 "id": "REAR_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara trasera",
 "value_id": "7199621",
 "value_name": "1920 px x 1080 px"
 },
 {
 "id": "MAIN_FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal principal",
 "value_id": "7199627",
 "value_name": "5 Mpx"
 },
 {
 "id": "WITH_FINGERPRINT_READER",
 "name": "Con lector de huella digital",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "BATTERY_CAPACITY",
 "name": "Capacidad de la batería",
 "value_id": "8212557",
 "value_name": "1950 mAh"
 },
 {
 "id": "NUMBER_OF_SIM_CARD_SLOTS",
 "name": "Cantidad de ranuras para tarjeta SIM",
 "value_id": "2087802",
 "value_name": "2"
 },
 {
 "id": "SIM_SIZES",
 "name": "Tamaños de tarjeta SIM compatibles",
 "value_id": "80453",
 "value_name": "Nano-SIM"
 },
 {
 "id": "WITH_ESIM",
 "name": "Con eSIM",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "2087854",
 "value_name": "165 g"
 },
 {
 "id": "HEIGHT",
 "name": "Altura",
 "value_id": "4369069",
 "value_name": "122 mm"
 },
 {
 "id": "WIDTH",
 "name": "Ancho",
 "value_id": "7936922",
 "value_name": "60.2 mm"
 },
 {
 "id": "DEPTH",
 "name": "Profundidad",
 "value_id": "8212558",
 "value_name": "16.1 mm"
 },
 {
 "id": "PIXELS_PER_INCH",
 "name": "Píxeles por pulgada",
 "value_id": "8212555",
 "value_name": "246 ppi"
 },
 {
 "id": "SCREEN_TECHNOLOGY",
 "name": "Tecnología de pantalla",
 "value_id": "80489",
 "value_name": "TFT"
 },
 {
 "id": "WITH_TOUCH_SCREEN",
 "name": "Con pantalla táctil",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_PHYSICAL_QWERTY_KEYBOARD",
 "name": "Con teclado QWERTY físico",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_CAMERA",
 "name": "Con cámara",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477198",
 "value_name": "1"
 },
 {
 "id": "REAR_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara trasera",
 "value_id": "7441410",
 "value_name": "f 1.9"
 },
 {
 "id": "FRONT_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras frontales",
 "value_id": "7477216",
 "value_name": "1"
 },
 {
 "id": "FRONT_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara frontal",
 "value_id": "7180687",
 "value_name": "1280 px x 720 px"
 },
 {
 "id": "FRONT_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara frontal",
 "value_id": "7439050",
 "value_name": "f 1.9"
 },
 {
 "id": "WITH_FRONT_CAMERA_FLASH",
 "name": "Con flash en la cámara frontal",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "MOBILE_NETWORK",
 "name": "Red",
 "value_id": "367876",
 "value_name": "4G/LTE"
 },
 {
 "id": "MEMORY_CARD_TYPES",
 "name": "Tipos de tarjeta de memoria",
 "value_id": "7199655",
 "value_name": "MicroSD"
 },
 {
 "id": "MAX_MEMORY_CARD_CAPACITY",
 "name": "Capacidad máxima de la tarjeta de memoria",
 "value_id": "2087792",
 "value_name": "256 GB"
 },
 {
 "id": "PROCESSOR_MODEL",
 "name": "Modelo del procesador",
 "value_id": "2087879",
 "value_name": "Snapdragon 425"
 },
 {
 "id": "CPU_MODELS",
 "name": "Modelos de CPU",
 "value_id": "7657686",
 "value_name": "4x1.4 GHz Cortex-A53"
 },
 {
 "id": "PROCESSOR_CORES_NUMBER",
 "name": "Cantidad de núcleos del procesador",
 "value_id": "7206949",
 "value_name": "4"
 },
 {
 "id": "PROCESSOR_SPEED",
 "name": "Velocidad del procesador",
 "value_id": "1151166",
 "value_name": "1.4 GHz"
 },
 {
 "id": "GPU_MODEL",
 "name": "Modelo de GPU",
 "value_id": "7531831",
 "value_name": "Adreno 308"
 },
 {
 "id": "WITH_USB_CONNECTOR",
 "name": "Con conector USB",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_WIFI",
 "name": "Con Wi-Fi",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_BLUETOOTH",
 "name": "Con Bluetooth",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_MINI_HDMI",
 "name": "Con mini HDMI",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_RADIO",
 "name": "Con radio",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_TV_TUNER",
 "name": "Con sintonizador de TV",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "WITH_ACCELEROMETER",
 "name": "Con acelerómetro",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_PROXIMITY_SENSOR",
 "name": "Con sensor de proximidad",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "WITH_GYROSCOPE",
 "name": "Con giroscopio",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "IS_SPLASH_RESISTANT",
 "name": "Es resistente a salpicaduras",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "IS_WATER_RESISTANT",
 "name": "Es resistente al agua",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "IS_WATERPROOF",
 "name": "Es a prueba de agua",
 "value_id": "242084",
 "value_name": "No"
 },
 {
 "id": "BATTERY_TYPE",
 "name": "Tipo de batería",
 "value_id": "95013",
 "value_name": "Ion de litio"
 },
 {
 "id": "WITH_REMOVABLE_BATTERY",
 "name": "Con batería removible",
 "value_id": "242085",
 "value_name": "Sí"
 },
 {
 "id": "STANDBY_TIME",
 "name": "Duración de la batería en espera",
 "value_id": "7835954",
 "value_name": "318 h"
 }
 ],
 "pictures": [
 {
 "id": "636253-MLA41570339037_042020",
 "url": "https://mla-s2-p.mlstatic.com/636253-MLA41570339037_042020-F.jpg"
 },
 {
 "id": "819635-MLA41570339038_042020",
 "url": "https://mla-s2-p.mlstatic.com/819635-MLA41570339038_042020-F.jpg"
 },
 {
 "id": "690923-MLA41569811814_042020",
 "url": "https://mla-s2-p.mlstatic.com/690923-MLA41569811814_042020-F.jpg"
 },
 {
 "id": "976286-MLA41569811805_042020",
 "url": "https://mla-s1-p.mlstatic.com/976286-MLA41569811805_042020-F.jpg"
 }
 ]
 }
}
```

Notes:

\- The **site\_id** parameter is mandatory. 
\- Depending on the parameters used for the search, you will get one or several products as a suggestion. 
\- If you use a **product\_identifier** as parameter, you will get only one product in the answer. 
\- If you use as parameter a keyword in **q**, either with or without a domain, you can. 
\- If you use a POST with attributes, the search is more specific, you may get one or several results. 
\*You must enter at least 3 different attributes in the attributes field of the body for the attribute search. 
\*All attributes in the attributes field, must have an **id** (attribute id) and a **value\_id** (attribute value id) or **value\_name** (attribute value).

 

## Catalog product

In order for an item to be published in the catalog and buyer, it must be associated with a catalog product or also known as a product page (PDP). Catalog products are created by Mercado Libre, where we ensure that they are specific enough (complete datasheet) so that the buyer knows precisely what he is buying (products with status=**active** in **/products/{product\_id}**).

## Product detail

Once you have identified a catalog product, you can learn about its main characteristics with the **/products/$PRODUCT\_ID** feature. In this way, you will be able to create a better quality item.

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/$PRODUCT_ID
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/MLA14719808
```

Response:

```
{
 "id": "MLA14719808",
 "status": "active",
 "sold_quantity": 6,
 "domain_id": "MLA-TABLETS",
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-32gb-gold-y-2gb-de-memoria-ram/p/MLA14719808",
 "name": "iPad Apple 6th generation 2018 A1954 9.7\" con red móvil 32GB gold y 2GB de memoria RAM",
 "family_name": "Apple iPad 6th generation 2018 A1954 (Incluye: Con red móvil)",
 "buy_box_winner": null,
 "buy_box_winner_price_range": null,
 "pickers": [
 {
 "picker_id": "COLOR",
 "picker_name": "Color",
 "products": [
 {
 "product_id": "MLA14719808",
 "picker_label": "Gold",
 "picture_id": "611193-MLA32649508843_102019",
 "thumbnail": "https://mla-s1-p.mlstatic.com/611193-MLA32649508843_102019-I.jpg",
 "tags": [
 "selected"
 ],
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-32gb-gold-y-2gb-de-memoria-ram/p/MLA14719808"
 },
 {
 "product_id": "MLA15061140",
 "picker_label": "Silver",
 "picture_id": "924731-MLA32649932035_102019",
 "thumbnail": "https://mla-s2-p.mlstatic.com/924731-MLA32649932035_102019-I.jpg",
 "tags": [
 "disabled"
 ],
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-32gb-silver-y-2gb-de-memoria-ram/p/MLA15061140"
 },
 {
 "product_id": "MLA15061142",
 "picker_label": "Space gray",
 "picture_id": "998164-MLA32654533791_102019",
 "thumbnail": "https://mla-s1-p.mlstatic.com/998164-MLA32654533791_102019-I.jpg",
 "tags": [
 "disabled"
 ],
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-32gb-space-gray-y-2gb-de-memoria-ram/p/MLA15061142"
 }
 ],
 "tags": null,
 "attributes": [
 {
 "attribute_id": "COLOR",
 "template": ""
 }
 ]
 },
 {
 "picker_id": "CAPACITY",
 "picker_name": "Capacidad",
 "products": [
 {
 "product_id": "MLA14719808",
 "picker_label": "32 GB",
 "picture_id": "",
 "thumbnail": "",
 "tags": [
 "selected"
 ],
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-32gb-gold-y-2gb-de-memoria-ram/p/MLA14719808"
 },
 {
 "product_id": "MLA9592537",
 "picker_label": "128 GB",
 "picture_id": "",
 "thumbnail": "",
 "tags": [
 "disabled"
 ],
 "permalink": "https://www.mercadolibre.com.ar/ipad-apple-6th-generation-2018-a1954-97-con-red-movil-128gb-gold-y-2gb-de-memoria-ram/p/MLA9592537"
 }
 ],
 "tags": null,
 "attributes": [
 {
 "attribute_id": "CAPACITY",
 "template": ""
 }
 ]
 }
 ],
 "pictures": [
 {
 "id": "777713-MLA32660788040_102019",
 "url": "https://mla-s2-p.mlstatic.com/777713-MLA32660788040_102019-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1051,
 "max_height": 1478
 },
 {
 "id": "611193-MLA32649508843_102019",
 "url": "https://mla-s1-p.mlstatic.com/611193-MLA32649508843_102019-F.jpg",
 "suggested_for_picker": [
 "COLOR"
 ],
 "max_width": 773,
 "max_height": 1092
 },
 {
 "id": "748220-MLA32660542682_102019",
 "url": "https://mla-s1-p.mlstatic.com/748220-MLA32660542682_102019-F.jpg",
 "suggested_for_picker": [],
 "max_width": 936,
 "max_height": 1074
 }
 ],
 "main_features": [
 {
 "text": "Sistema operativo: iOS 12.0. ",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Resolución de pantalla de 2048px x 1536px. ",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Cuenta con GPS. ",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Diseñado para llevar a todas partes. ",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Pesa tan solo 480g. ",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 }
 ],
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "9344",
 "value_name": "Apple",
 "values": [
 {
 "id": "9344",
 "name": "Apple"
 }
 ]
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "107662",
 "value_name": "iPad",
 "values": [
 {
 "id": "107662",
 "name": "iPad"
 }
 ]
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "10351421",
 "value_name": "6th generation",
 "values": [
 {
 "id": "10351421",
 "name": "6th generation"
 }
 ]
 },
 {
 "id": "VERSION",
 "name": "Versión",
 "value_id": "3640650",
 "value_name": "2018",
 "values": [
 {
 "id": "3640650",
 "name": "2018"
 }
 ]
 },
 {
 "id": "ALPHANUMERIC_MODEL",
 "name": "Modelo alfanumérico",
 "value_id": "7657201",
 "value_name": "A1954",
 "values": [
 {
 "id": "7657201",
 "name": "A1954"
 }
 ]
 },
 {
 "id": "WITH_MOBILE_NETWORK",
 "name": "Con red móvil",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "COLOR",
 "name": "Color",
 "value_id": "59628",
 "value_name": "Gold",
 "values": [
 {
 "id": "59628",
 "name": "Gold"
 }
 ]
 },
 {
 "id": "RAM_MEMORY",
 "name": "Memoria RAM",
 "value_id": "445970",
 "value_name": "2 GB",
 "values": [
 {
 "id": "445970",
 "name": "2 GB"
 }
 ]
 },
 {
 "id": "CAPACITY",
 "name": "Capacidad",
 "value_id": "18621",
 "value_name": "32 GB",
 "values": [
 {
 "id": "18621",
 "name": "32 GB"
 }
 ]
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "3912629",
 "value_name": "9.7 \"",
 "values": [
 {
 "id": "3912629",
 "name": "9.7 \""
 }
 ]
 },
 {
 "id": "MAIN_COLOR",
 "name": "Color principal",
 "value_id": "2450289",
 "value_name": "Dorado",
 "values": [
 {
 "id": "2450289",
 "name": "Dorado",
 "meta": {
 "rgb": "FFD700"
 }
 }
 ],
 "meta": {
 "rgb": "FFD700"
 }
 },
 {
 "id": "OS_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "4743193",
 "value_name": "iOS",
 "values": [
 {
 "id": "4743193",
 "name": "iOS"
 }
 ]
 },
 {
 "id": "OS_VERSION",
 "name": "Versión del sistema operativo",
 "value_id": "12909372",
 "value_name": "12.0",
 "values": [
 {
 "id": "12909372",
 "name": "12.0"
 }
 ]
 },
 {
 "id": "CONNECTIVITY",
 "name": "Conectividad",
 "value_id": null,
 "value_name": "Bluetooth, Conector lightning, Smart connector, Wi-Fi",
 "values": [
 {
 "id": "81950",
 "name": "Bluetooth"
 },
 {
 "id": "7599855",
 "name": "Conector lightning"
 },
 {
 "id": "7600284",
 "name": "Smart connector"
 },
 {
 "id": "2511537",
 "name": "Wi-Fi"
 }
 ]
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477198",
 "value_name": "1",
 "values": [
 {
 "id": "7477198",
 "name": "1"
 }
 ]
 },
 {
 "id": "BLUETOOTH_VERSION",
 "name": "Versión bluetooth",
 "value_id": "12008875",
 "value_name": "4.2",
 "values": [
 {
 "id": "12008875",
 "name": "4.2"
 }
 ]
 },
 {
 "id": "SIM_CARD_READERS",
 "name": "Lectores de tarjetas SIM",
 "value_id": "82830",
 "value_name": "Nano SIM",
 "values": [
 {
 "id": "82830",
 "name": "Nano SIM"
 }
 ]
 },
 {
 "id": "SENSORS",
 "name": "Sensores",
 "value_id": null,
 "value_name": "Acelerómetro, Barómetro, Sensor de huella digital, Sensor de luz ambiente",
 "values": [
 {
 "id": "82823",
 "name": "Acelerómetro"
 },
 {
 "id": "7176142",
 "name": "Barómetro"
 },
 {
 "id": "7511951",
 "name": "Sensor de huella digital"
 },
 {
 "id": "82817",
 "name": "Sensor de luz ambiente"
 }
 ]
 },
 {
 "id": "CHIPSET",
 "name": "Chipset",
 "value_id": "7657199",
 "value_name": "Apple A10 Fusion",
 "values": [
 {
 "id": "7657199",
 "name": "Apple A10 Fusion"
 }
 ]
 },
 {
 "id": "IS_MULTI_TOUCH",
 "name": "Es multi-touch",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_FLASH",
 "name": "Con flash",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_HEADPHONES_OUTPUT",
 "name": "Con salida para auriculares",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "PROCESSOR_SPEED",
 "name": "Velocidad del procesador",
 "value_id": "6877633",
 "value_name": "2.34 GHz",
 "values": [
 {
 "id": "6877633",
 "name": "2.34 GHz"
 }
 ]
 },
 {
 "id": "BATTERY_CAPACITY",
 "name": "Capacidad de la batería",
 "value_id": "7185348",
 "value_name": "8827 mAh",
 "values": [
 {
 "id": "7185348",
 "name": "8827 mAh"
 }
 ]
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "1188",
 "value_name": "480 g",
 "values": [
 {
 "id": "1188",
 "name": "480 g"
 }
 ]
 },
 {
 "id": "PIXELS_PER_INCH",
 "name": "Píxeles por pulgada",
 "value_id": "7749453",
 "value_name": "264 ppi",
 "values": [
 {
 "id": "7749453",
 "name": "264 ppi"
 }
 ]
 },
 {
 "id": "TABLET_REAR_CAMERAS_RESOLUTIONS",
 "name": "Resoluciones de las cámaras traseras",
 "value_id": "902414",
 "value_name": "8 Mpx",
 "values": [
 {
 "id": "902414",
 "name": "8 Mpx"
 }
 ]
 },
 {
 "id": "FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal",
 "value_id": "902404",
 "value_name": "1.2 Mpx",
 "values": [
 {
 "id": "902404",
 "name": "1.2 Mpx"
 }
 ]
 },
 {
 "id": "MAX_SCREEN_RESOLUTION",
 "name": "Máxima resolución de pantalla",
 "value_id": "1151117",
 "value_name": "2048 px x 1536 px",
 "values": [
 {
 "id": "1151117",
 "name": "2048 px x 1536 px"
 }
 ]
 },
 {
 "id": "CORES_NUMBER",
 "name": "Cantidad de núcleos",
 "value_id": "6838527",
 "value_name": "4",
 "values": [
 {
 "id": "6838527",
 "name": "4"
 }
 ]
 }
 ],
 "short_description": {
 "type": "plaintext",
 "content": "Este producto combina la potencia y la capacidad de una computadora con la versatilidad y facilidad de uso que solo un iPad puede brindar. Realizar varias tareas a la vez, como editar documentos mientras buscás información en internet o sacarte una selfie, es sumamente sencillo. Como si esto fuera poco, también ofrece la posibilidad de descargar desde la App Store cientos de aplicaciones creadas para pintar, dibujar, escuchar música y ¡mucho más!\n\nGracias a su cámara principal de 8 Mpx y frontal de 1.2 Mpx, podrás hacer videollamadas o sacarte fotos en cualquier momento y lugar, con una excelente calidad de imagen. Nitidez, brillo y colores vibrantes harán que tus experiencias se reflejen de manera óptima."
 },
 "parent_id": "MLA9592536",
 "children_ids": [],
 "settings": {
 "listing_strategy": "catalog_required",
 "has_rich_description": false
 },
 "buy_box_activation_date": "2019-11-11T14:59:19Z",
 "authority_types": [
 "INTERNAL"
 ],
 "date_created": "2019-06-04T18:43:31Z"
}
```

### Special behaviors

* When the product has status: inactive some fields like pictures, pickers and **main\_features** among others will be null. And the **short\_description** and permalink fields come empty.

Example of response for an inactive catalog product:

```
{
 "id": "MLA1002411",
 "status": "inactive",
 "sold_quantity": 0,
 "domain_id": "MLA-CELLPHONES",
 "permalink": "",
 "name": "Samsung Solstice ll SGH-A817",
 "family_name": "Samsung Solstice ll SGH-A817",
 "buy_box_winner": null,
 "buy_box_winner_price_range": null,
 "pickers": null,
 "pictures": null,
 "main_features": null,
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "206",
 "value_name": "Samsung",
 "values": [
 {
 "id": "206",
 "name": "Samsung"
 }
 ]
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "6410206",
 "value_name": "Solstice ll SGH-A817",
 "values": [
 {
 "id": "6410206",
 "name": "Solstice ll SGH-A817"
 }
 ]
 }
 ],
 "short_description": {
 "type": "",
 "content": ""
 },
 "parent_id": null,
 "children_ids": [],
 "settings": {
 "listing_strategy": "open",
 "has_rich_description": false
 },
 "authority_types": [
 "INTERNAL"
 ],
 "date_created": "2010-01-01T00:00:00Z"
}
```

Catalog products or product pages (PDP), in general, consist of several associated products that compete with each other. The **buy\_box\_winner** field indicates which of the products is currently winning by offering better selling conditions. When there is no catalog product competing, this field comes as null.

Example of the **buy\_box\_winner** field:

```
"buy_box_winner": {
 "item_id": "MLA1109016617",
 "category_id": "MLA1055",
 "seller_id": 123456,
 "price": 362999,
 "currency_id": "ARS",
 "sold_quantity": 63,
 "available_quantity": 3,
 "shipping": {
 "mode": "me2",
 "tags": [
 "self_service_in",
 "mandatory_free_shipping"
 ],
 "free_shipping": true,
 "logistic_type": "xd_drop_off",
 "store_pick_up": false
 },
 "warranty": "Garantía de fábrica: 12 meses",
 "condition": "new",
 "sale_terms": [
 {
 "id": "WARRANTY_TYPE",
 "name": "Tipo de garantía",
 "value_id": "2230279",
 "value_name": "Garantía de fábrica",
 "value_struct": null
 },
 {
 "id": "INVOICE",
 "name": "Facturación",
 "value_id": "6891885",
 "value_name": "Factura A",
 "value_struct": null
 },
 {
 "id": "WARRANTY_TIME",
 "name": "Tiempo de garantía",
 "value_id": null,
 "value_name": "12 meses",
 "value_struct": {
 "number": 12,
 "unit": "meses"
 }
 }
 ],
 "official_store_id": null,
 "original_price": null,
 "listing_type_id": "gold_special",
 "accepts_mercadopago": true,
 "seller_address": {
 "city": {
 "name": "Palermo"
 },
 "state": {
 "name": "Capital Federal"
 }
 },
 "international_delivery_mode": "none",
 "tags": [
 "good_quality_thumbnail",
 "extended_warranty_eligible",
 "immediate_payment",
 "cart_eligible",
 "good_quality_picture"
 ],
 "item_override_attributes": [],
 "seller": {
 "reputation_level_id": "GREEN",
 "tags": []
 },
 "deal_ids": [
 "MLA6500"
 ],
 "tier": "candidate",
 "inventory_id": "",
 "product_id": "MLA18500844",
 "site_id": "MLA"
 }
```

Nota:

The content of the catalog posting is provided by Mercado Livre. Therefore, the seller is responsible for confirming that the product to be associated matches the specific characteristics presented on the platform. 
If there is a difference between what the user bought and the associated product, it is possible to generate complaints and/or cancellations that negatively impact the reputation and as a consequence the inability to publish in the catalog, eventually leading to the suspension of the account. 

## Parents and children products

**Higher-level products (parents)** group together several specific catalog products and are not eligible to be purchased. Example: Motorola Moto G6. This one does not have the capacity or color specified. 
**Terminal level products (son or children)** catalog products that are sufficiently specified, i.e. with their complete technical data sheet, and are therefore eligible for purchase. Example: Motorola G6 32 GB dark indigo. 

Example of a parent/child product (not specific and not purchasable):

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/MLA18500843
```

Response:

```
{
 "id": "MLA9652753",
 "status": "inactive",
 "domain_id": "MLA-CELLPHONES",
 "permalink": "https://www.mercadolibre.com.ar/p/MLA9652753",
 "name": "Motorola Moto G6",
 "buy_box_winner": null,
 "pickers": null,
 "pictures": null,
 "main_features": null,
 "attributes": [],
 "short_description": {},
 "parent_id": "",
 "children_ids": [
 "MLA9652754",
 "MLA9652755",
 "MLA9652756",
 "MLA9652757",
 "MLA9707910",
 "MLA9707911",
 "MLA9707912",
 "MLA9707913"
 ]
} 

{
 "id": "MLA18500843",
 "status": "inactive",
 "sold_quantity": 4,
 "domain_id": "MLA-CELLPHONES",
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13/p/MLA18500843",
 "name": "Apple iPhone 13",
 "family_name": "Apple iPhone 13",
 "buy_box_winner": null,
 "buy_box_winner_price_range": null,
 "pickers": null,
 "pictures": null,
 "main_features": null,
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "9344",
 "value_name": "Apple",
 "values": [
 {
 "id": "9344",
 "name": "Apple"
 }
 ]
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "58993",
 "value_name": "iPhone",
 "values": [
 {
 "id": "58993",
 "name": "iPhone"
 }
 ]
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "11159139",
 "value_name": "iPhone 13",
 "values": [
 {
 "id": "11159139",
 "name": "iPhone 13"
 }
 ]
 },
 {
 "id": "IS_DUAL_SIM",
 "name": "Es Dual SIM",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "OPERATING_SYSTEM_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "7404961",
 "value_name": "iOS",
 "values": [
 {
 "id": "7404961",
 "name": "iOS"
 }
 ]
 },
 {
 "id": "OS_ORIGINAL_VERSION",
 "name": "Versión original del sistema operativo",
 "value_id": "11151771",
 "value_name": "15",
 "values": [
 {
 "id": "11151771",
 "name": "15"
 }
 ]
 },
 {
 "id": "OS_LAST_COMPATIBLE_VERSION",
 "name": "Última versión compatible del sistema operativo",
 "value_id": "12281407",
 "value_name": "16",
 "values": [
 {
 "id": "12281407",
 "name": "16"
 }
 ]
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "6892143",
 "value_name": "6.1 \"",
 "values": [
 {
 "id": "6892143",
 "name": "6.1 \""
 }
 ]
 },
 {
 "id": "DISPLAY_RESOLUTION",
 "name": "Resolución de la pantalla",
 "value_id": "9095646",
 "value_name": "1170 px x 2532 px",
 "values": [
 {
 "id": "9095646",
 "name": "1170 px x 2532 px"
 }
 ]
 },
 {
 "id": "MAIN_REAR_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara trasera principal",
 "value_id": "7199628",
 "value_name": "12 Mpx",
 "values": [
 {
 "id": "7199628",
 "name": "12 Mpx"
 }
 ]
 },
 {
 "id": "REAR_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara trasera",
 "value_id": "7199630",
 "value_name": "3840 px x 2160 px",
 "values": [
 {
 "id": "7199630",
 "name": "3840 px x 2160 px"
 }
 ]
 },
 {
 "id": "MAIN_FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal principal",
 "value_id": "7207109",
 "value_name": "12 Mpx",
 "values": [
 {
 "id": "7207109",
 "name": "12 Mpx"
 }
 ]
 },
 {
 "id": "WITH_FACIAL_RECOGNITION",
 "name": "Con reconocimiento facial",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "SIM_CARD_SLOTS_NUMBER",
 "name": "Cantidad de ranuras para tarjeta SIM",
 "value_id": "2087812",
 "value_name": "1",
 "values": [
 {
 "id": "2087812",
 "name": "1"
 }
 ]
 },
 {
 "id": "COMPATIBLE_SIM_CARD_SIZES",
 "name": "Tamaños de tarjeta SIM compatibles",
 "value_id": "80453",
 "value_name": "Nano-SIM",
 "values": [
 {
 "id": "80453",
 "name": "Nano-SIM"
 }
 ]
 },
 {
 "id": "WITH_ESIM",
 "name": "Con eSIM",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "ESIMS_NUMBER",
 "name": "Cantidad de eSIMs",
 "value_id": "11151772",
 "value_name": "2",
 "values": [
 {
 "id": "11151772",
 "name": "2"
 }
 ]
 },
 {
 "id": "RELEASE_MONTH",
 "name": "Mes de lanzamiento",
 "value_id": "8275348",
 "value_name": "Septiembre",
 "values": [
 {
 "id": "8275348",
 "name": "Septiembre"
 }
 ]
 },
 {
 "id": "RELEASE_YEAR",
 "name": "Año de lanzamiento",
 "value_id": "9676768",
 "value_name": "2021",
 "values": [
 {
 "id": "9676768",
 "name": "2021"
 }
 ]
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "462013",
 "value_name": "173 g",
 "values": [
 {
 "id": "462013",
 "name": "173 g"
 }
 ]
 },
 {
 "id": "HEIGHT",
 "name": "Altura",
 "value_id": "9095649",
 "value_name": "146.7 mm",
 "values": [
 {
 "id": "9095649",
 "name": "146.7 mm"
 }
 ]
 },
 {
 "id": "WIDTH",
 "name": "Ancho",
 "value_id": "5835158",
 "value_name": "71.5 mm",
 "values": [
 {
 "id": "5835158",
 "name": "71.5 mm"
 }
 ]
 },
 {
 "id": "DEPTH",
 "name": "Profundidad",
 "value_id": "7970551",
 "value_name": "7.65 mm",
 "values": [
 {
 "id": "7970551",
 "name": "7.65 mm"
 }
 ]
 },
 {
 "id": "DISPLAY_TECHNOLOGY",
 "name": "Tecnología de la pantalla",
 "value_id": "80491",
 "value_name": "OLED",
 "values": [
 {
 "id": "80491",
 "name": "OLED"
 }
 ]
 },
 {
 "id": "DISPLAY_TYPE",
 "name": "Tipo de pantalla",
 "value_id": "9785211",
 "value_name": "Super Retina XDR",
 "values": [
 {
 "id": "9785211",
 "name": "Super Retina XDR"
 }
 ]
 },
 {
 "id": "DISPLAY_ASPECT_RATIO",
 "name": "Relación de aspecto de la pantalla",
 "value_id": "11331351",
 "value_name": "19.5:9",
 "values": [
 {
 "id": "11331351",
 "name": "19.5:9"
 }
 ]
 },
 {
 "id": "DISPLAY_PIXELS_PER_INCH",
 "name": "Píxeles por pulgada de la pantalla",
 "value_id": "9095650",
 "value_name": "460 ppi",
 "values": [
 {
 "id": "9095650",
 "name": "460 ppi"
 }
 ]
 },
 {
 "id": "MAX_DISPLAY_BRIGHTNESS",
 "name": "Brillo máximo de la pantalla",
 "value_id": "7741025",
 "value_name": "1200 cd/m²",
 "values": [
 {
 "id": "7741025",
 "name": "1200 cd/m²"
 }
 ]
 },
 {
 "id": "WITH_TOUCHSCREEN_DISPLAY",
 "name": "Con pantalla táctil",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_PHYSICAL_QWERTY_KEYBOARD",
 "name": "Con teclado QWERTY físico",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_CAMERA",
 "name": "Con cámara",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "CAMERAS_MAIN_FEATURES",
 "name": "Características principales de las cámaras",
 "value_id": null,
 "value_name": "Bokeh, Modo noche, Deep fusion, HDR, Modo ráfaga",
 "values": [
 {
 "id": "9727052",
 "name": "Bokeh"
 },
 {
 "id": "9788716",
 "name": "Modo noche"
 },
 {
 "id": "11159138",
 "name": "Deep fusion"
 },
 {
 "id": "11625617",
 "name": "HDR"
 },
 {
 "id": "11151773",
 "name": "Modo ráfaga"
 }
 ]
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477262",
 "value_name": "2",
 "values": [
 {
 "id": "7477262",
 "name": "2"
 }
 ]
 },
 {
 "id": "REAR_CAMERAS_RESOLUTION",
 "name": "Resolución de las cámaras traseras",
 "value_id": "7405025",
 "value_name": "12 Mpx/12 Mpx",
 "values": [
 {
 "id": "7405025",
 "name": "12 Mpx/12 Mpx"
 }
 ]
 },
 {
 "id": "REAR_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara trasera",
 "value_id": "11159135",
 "value_name": "f 1.6/f 2.4",
 "values": [
 {
 "id": "11159135",
 "name": "f 1.6/f 2.4"
 }
 ]
 },
 {
 "id": "FRONT_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras frontales",
 "value_id": "7477216",
 "value_name": "1",
 "values": [
 {
 "id": "7477216",
 "name": "1"
 }
 ]
 },
 {
 "id": "FRONT_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara frontal",
 "value_id": "7207112",
 "value_name": "3840 px x 2160 px",
 "values": [
 {
 "id": "7207112",
 "name": "3840 px x 2160 px"
 }
 ]
 },
 {
 "id": "FRONT_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara frontal",
 "value_id": "7408595",
 "value_name": "f 2.2",
 "values": [
 {
 "id": "7408595",
 "name": "f 2.2"
 }
 ]
 },
 {
 "id": "OPTICAL_ZOOM",
 "name": "Zoom óptico",
 "value_id": "1344",
 "value_name": "2x",
 "values": [
 {
 "id": "1344",
 "name": "2x"
 }
 ]
 },
 {
 "id": "DIGITAL_ZOOM",
 "name": "Zoom digital",
 "value_id": "7199631",
 "value_name": "5x",
 "values": [
 {
 "id": "7199631",
 "name": "5x"
 }
 ]
 },
 {
 "id": "MOBILE_NETWORK",
 "name": "Red",
 "value_id": "7472027",
 "value_name": "5G",
 "values": [
 {
 "id": "7472027",
 "name": "5G"
 }
 ]
 },
 {
 "id": "WITH_MEMORY_CARD_SLOT",
 "name": "Con ranura para tarjeta de memoria",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "PROCESSOR_MODEL",
 "name": "Modelo del procesador",
 "value_id": "11151775",
 "value_name": "Apple A15 Bionic",
 "values": [
 {
 "id": "11151775",
 "name": "Apple A15 Bionic"
 }
 ]
 },
 {
 "id": "PROCESSOR_CORES_NUMBER",
 "name": "Cantidad de núcleos del procesador",
 "value_id": "7199636",
 "value_name": "6",
 "values": [
 {
 "id": "7199636",
 "name": "6"
 }
 ]
 },
 {
 "id": "PROCESSOR_SPEED",
 "name": "Velocidad del procesador",
 "value_id": "11159137",
 "value_name": "3.22 GHz",
 "values": [
 {
 "id": "11159137",
 "name": "3.22 GHz"
 }
 ]
 },
 {
 "id": "GPU_MODEL",
 "name": "Modelo de GPU",
 "value_id": "7741027",
 "value_name": "Apple GPU",
 "values": [
 {
 "id": "7741027",
 "name": "Apple GPU"
 }
 ]
 },
 {
 "id": "CHARGE_CONNECTOR_TYPE",
 "name": "Tipo de conector de carga",
 "value_id": "8275368",
 "value_name": "Lightning",
 "values": [
 {
 "id": "8275368",
 "name": "Lightning"
 }
 ]
 },
 {
 "id": "WITH_USB_CONNECTOR",
 "name": "Con conector USB",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_3_5_MM_JACK_CONNECTOR",
 "name": "Con conector jack 3.5 mm",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_WIFI",
 "name": "Con Wi-Fi",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_BLUETOOTH",
 "name": "Con Bluetooth",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_NFC",
 "name": "Con NFC",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_RADIO",
 "name": "Con radio",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_ACCELEROMETER",
 "name": "Con acelerómetro",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_PROXIMITY_SENSOR",
 "name": "Con sensor de proximidad",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_GYROSCOPE",
 "name": "Con giroscopio",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_COMPASS",
 "name": "Con brújula",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_BAROMETER",
 "name": "Con barómetro",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IS_WATER_RESISTANT",
 "name": "Es resistente al agua",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IS_DUST_RESISTANT",
 "name": "Es resistente al polvo",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IP_RATING",
 "name": "Clasificación IP",
 "value_id": "8275373",
 "value_name": "IP68",
 "values": [
 {
 "id": "8275373",
 "name": "IP68"
 }
 ]
 },
 {
 "id": "BATTERY_TYPE",
 "name": "Tipo de batería",
 "value_id": "95013",
 "value_name": "Ion de litio",
 "values": [
 {
 "id": "95013",
 "name": "Ion de litio"
 }
 ]
 },
 {
 "id": "WITH_FAST_CHARGING",
 "name": "Con carga rápida",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_WIRELESS_CHARGING",
 "name": "Con carga inalámbrica",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_REMOVABLE_BATTERY",
 "name": "Con batería removible",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 }
 ],
 "short_description": {
 "type": "",
 "content": ""
 },
 "parent_id": null,
 "children_ids": [
 "MLA18500844",
 "MLA18500845",
 "MLA18500846",
 "MLA18500847",
 "MLA18500848",
 "MLA18500849",
 "MLA18500850",
 "MLA18500851",
 "MLA18500852",
 "MLA18500853",
 "MLA18500854",
 "MLA18500855",
 "MLA18500856",
 "MLA18500857",
 "MLA18500858",
 "MLA18969310",
 "MLA18969311",
 "MLA18969312"
 ],
 "settings": {
 "listing_strategy": "catalog_required",
 "has_rich_description": false
 },
 "authority_types": [
 "INTERNAL"
 ],
 "date_created": "2021-09-28T18:23:35Z"
}
```

Example of a son product (with its complete datasheet you can publish if it is active):

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/products/MLA18500852
```

Response:

```
{
 "id": "MLA18500852",
 "status": "active",
 "sold_quantity": 15,
 "domain_id": "MLA-CELLPHONES",
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-productred/p/MLA18500852",
 "name": "Apple iPhone 13 (128 GB) - (PRODUCT)RED",
 "family_name": "Apple iPhone 13",
 "buy_box_winner": {
 "item_id": "MLA1109011009",
 "category_id": "MLA1055",
 "seller_id": 393731981,
 "price": 363999,
 "currency_id": "ARS",
 "sold_quantity": 8,
 "available_quantity": 4,
 "shipping": {
 "mode": "me2",
 "tags": [
 "self_service_in",
 "mandatory_free_shipping"
 ],
 "free_shipping": true,
 "logistic_type": "xd_drop_off",
 "store_pick_up": false
 },
 "warranty": "Garantía de fábrica: 12 meses",
 "condition": "new",
 "sale_terms": [
 {
 "id": "INVOICE",
 "name": "Facturación",
 "value_id": "6891885",
 "value_name": "Factura A",
 "value_struct": null
 },
 {
 "id": "WARRANTY_TIME",
 "name": "Tiempo de garantía",
 "value_id": null,
 "value_name": "12 meses",
 "value_struct": {
 "number": 12,
 "unit": "meses"
 }
 },
 {
 "id": "WARRANTY_TYPE",
 "name": "Tipo de garantía",
 "value_id": "2230279",
 "value_name": "Garantía de fábrica",
 "value_struct": null
 }
 ],
 "official_store_id": null,
 "original_price": null,
 "listing_type_id": "gold_special",
 "accepts_mercadopago": true,
 "seller_address": {
 "city": {
 "name": "Palermo"
 },
 "state": {
 "name": "Capital Federal"
 }
 },
 "international_delivery_mode": "none",
 "tags": [
 "good_quality_thumbnail",
 "extended_warranty_eligible",
 "immediate_payment",
 "loyalty_discount_eligible",
 "cart_eligible",
 "good_quality_picture"
 ],
 "item_override_attributes": [],
 "seller": {
 "reputation_level_id": "GREEN",
 "tags": []
 },
 "deal_ids": [],
 "tier": "candidate",
 "inventory_id": "",
 "product_id": "MLA18500852",
 "site_id": "MLA"
 },
 "buy_box_winner_price_range": {
 "min": {
 "price": 330158,
 "currency_id": "ARS"
 },
 "max": {
 "price": 437999,
 "currency_id": "ARS"
 }
 },
 "pickers": [
 {
 "picker_id": "INTERNAL_MEMORY",
 "picker_name": "Memoria interna",
 "products": [
 {
 "product_id": "MLA18500852",
 "picker_label": "128 GB",
 "picture_id": "",
 "thumbnail": "",
 "tags": [
 "selected"
 ],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-productred/p/MLA18500852"
 },
 {
 "product_id": "MLA18500853",
 "picker_label": "256 GB",
 "picture_id": "",
 "thumbnail": "",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-256-gb-productred/p/MLA18500853"
 },
 {
 "product_id": "MLA18500854",
 "picker_label": "512 GB",
 "picture_id": "",
 "thumbnail": "",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-512-gb-productred/p/MLA18500854"
 }
 ],
 "tags": null,
 "attributes": [
 {
 "attribute_id": "INTERNAL_MEMORY",
 "template": ""
 }
 ]
 },
 {
 "picker_id": "COLOR",
 "picker_name": "Color",
 "products": [
 {
 "product_id": "MLA18500852",
 "picker_label": "(Product)Red",
 "picture_id": "834059-MLA47781378504_102021",
 "thumbnail": "https://mla-s2-p.mlstatic.com/834059-MLA47781378504_102021-I.jpg",
 "tags": [
 "selected"
 ],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-productred/p/MLA18500852"
 },
 {
 "product_id": "MLA18500846",
 "picker_label": "Azul",
 "picture_id": "619667-MLA47781882790_102021",
 "thumbnail": "https://mla-s1-p.mlstatic.com/619667-MLA47781882790_102021-I.jpg",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-azul/p/MLA18500846"
 },
 {
 "product_id": "MLA18500844",
 "picker_label": "Azul medianoche",
 "picture_id": "973345-MLA47781591382_102021",
 "thumbnail": "https://mla-s1-p.mlstatic.com/973345-MLA47781591382_102021-I.jpg",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-azul-medianoche/p/MLA18500844"
 },
 {
 "product_id": "MLA18500855",
 "picker_label": "Blanco estelar",
 "picture_id": "736168-MLA47781742030_102021",
 "thumbnail": "https://mla-s1-p.mlstatic.com/736168-MLA47781742030_102021-I.jpg",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-blanco-estelar/p/MLA18500855"
 },
 {
 "product_id": "MLA18500849",
 "picker_label": "Rosa",
 "picture_id": "654080-MLA47781882564_102021",
 "thumbnail": "https://mla-s2-p.mlstatic.com/654080-MLA47781882564_102021-I.jpg",
 "tags": [],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-rosa/p/MLA18500849"
 },
 {
 "product_id": "MLA18969310",
 "picker_label": "Verde",
 "picture_id": "736376-MLA49590060561_042022",
 "thumbnail": "https://http2.mlstatic.com/D_NQ_NP_736376-MLA49590060561_042022-I.jpg",
 "tags": [
 "disabled"
 ],
 "permalink": "https://www.mercadolibre.com.ar/apple-iphone-13-128-gb-verde/p/MLA18969310"
 }
 ],
 "tags": null,
 "attributes": [
 {
 "attribute_id": "COLOR",
 "template": ""
 }
 ]
 }
 ],
 "pictures": [
 {
 "id": "834059-MLA47781378504_102021",
 "url": "https://mla-s2-p.mlstatic.com/834059-MLA47781378504_102021-F.jpg",
 "suggested_for_picker": [
 "COLOR"
 ],
 "max_width": 574,
 "max_height": 779
 },
 {
 "id": "936944-MLA47781322922_102021",
 "url": "https://mla-s1-p.mlstatic.com/936944-MLA47781322922_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "908320-MLA47781322923_102021",
 "url": "https://mla-s1-p.mlstatic.com/908320-MLA47781322923_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "672203-MLA47781327798_102021",
 "url": "https://mla-s2-p.mlstatic.com/672203-MLA47781327798_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "991770-MLA47781322924_102021",
 "url": "https://mla-s1-p.mlstatic.com/991770-MLA47781322924_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "789738-MLA47781378506_102021",
 "url": "https://mla-s1-p.mlstatic.com/789738-MLA47781378506_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "809168-MLA47781327802_102021",
 "url": "https://mla-s2-p.mlstatic.com/809168-MLA47781327802_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "908638-MLA47781322926_102021",
 "url": "https://mla-s2-p.mlstatic.com/908638-MLA47781322926_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 },
 {
 "id": "787863-MLA47781322928_102021",
 "url": "https://mla-s1-p.mlstatic.com/787863-MLA47781322928_102021-F.jpg",
 "suggested_for_picker": [],
 "max_width": 1100,
 "max_height": 1100
 }
 ],
 "main_features": [
 {
 "text": "Pantalla Super Retina XDR de 6.1 pulgadas.(1)",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Modo Cine con baja profundidad de campo y cambios de enfoque automáticos en tus videos.",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Sistema avanzado de dos cámaras de 12 MP (gran angular y ultra gran angular) con Estilos Fotográficos, HDR Inteligente 4, modo Noche y grabación de video 4K HDR en Dolby Vision.",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Cámara frontal TrueDepth de 12 MP con modo Noche y grabación de video 4K HDR en Dolby Vision.",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Chip A15 Bionic para un rendimiento fuera de serie.",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Hasta 19 horas de reproducción de video.(2)",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Diseño resistente con Ceramic Shield.",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Resistencia al agua IP68, líder en la industria.(3)",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "iOS 15 con nuevas funcionalidades para aprovechar tu iPhone al máximo.(4)",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 },
 {
 "text": "Compatibilidad con accesorios MagSafe, que se acoplan fácilmente a tu iPhone y permiten una carga inalámbrica más rápida.(5)",
 "type": "key_value",
 "metadata": {
 "key": "",
 "value": ""
 }
 }
 ],
 "attributes": [
 {
 "id": "BRAND",
 "name": "Marca",
 "value_id": "9344",
 "value_name": "Apple",
 "values": [
 {
 "id": "9344",
 "name": "Apple"
 }
 ]
 },
 {
 "id": "LINE",
 "name": "Línea",
 "value_id": "58993",
 "value_name": "iPhone",
 "values": [
 {
 "id": "58993",
 "name": "iPhone"
 }
 ]
 },
 {
 "id": "MODEL",
 "name": "Modelo",
 "value_id": "11159139",
 "value_name": "iPhone 13",
 "values": [
 {
 "id": "11159139",
 "name": "iPhone 13"
 }
 ]
 },
 {
 "id": "IS_DUAL_SIM",
 "name": "Es Dual SIM",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "COLOR",
 "name": "Color",
 "value_id": "7139195",
 "value_name": "(Product)Red",
 "values": [
 {
 "id": "7139195",
 "name": "(Product)Red"
 }
 ]
 },
 {
 "id": "INTERNAL_MEMORY",
 "name": "Memoria interna",
 "value_id": "84611",
 "value_name": "128 GB",
 "values": [
 {
 "id": "84611",
 "name": "128 GB"
 }
 ]
 },
 {
 "id": "RAM",
 "name": "Memoria RAM",
 "value_id": "98852",
 "value_name": "4 GB",
 "values": [
 {
 "id": "98852",
 "name": "4 GB"
 }
 ]
 },
 {
 "id": "MAIN_COLOR",
 "name": "Color principal",
 "value_id": "2450307",
 "value_name": "Rojo",
 "values": [
 {
 "id": "2450307",
 "name": "Rojo",
 "meta": {
 "rgb": "FF0000"
 }
 }
 ],
 "meta": {
 "rgb": "FF0000"
 }
 },
 {
 "id": "OPERATING_SYSTEM_NAME",
 "name": "Nombre del sistema operativo",
 "value_id": "7404961",
 "value_name": "iOS",
 "values": [
 {
 "id": "7404961",
 "name": "iOS"
 }
 ]
 },
 {
 "id": "OS_ORIGINAL_VERSION",
 "name": "Versión original del sistema operativo",
 "value_id": "11151771",
 "value_name": "15",
 "values": [
 {
 "id": "11151771",
 "name": "15"
 }
 ]
 },
 {
 "id": "OS_LAST_COMPATIBLE_VERSION",
 "name": "Última versión compatible del sistema operativo",
 "value_id": "12281407",
 "value_name": "16",
 "values": [
 {
 "id": "12281407",
 "name": "16"
 }
 ]
 },
 {
 "id": "DISPLAY_SIZE",
 "name": "Tamaño de la pantalla",
 "value_id": "6892143",
 "value_name": "6.1 \"",
 "values": [
 {
 "id": "6892143",
 "name": "6.1 \""
 }
 ]
 },
 {
 "id": "DISPLAY_RESOLUTION",
 "name": "Resolución de la pantalla",
 "value_id": "9095646",
 "value_name": "1170 px x 2532 px",
 "values": [
 {
 "id": "9095646",
 "name": "1170 px x 2532 px"
 }
 ]
 },
 {
 "id": "MAIN_REAR_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara trasera principal",
 "value_id": "7199628",
 "value_name": "12 Mpx",
 "values": [
 {
 "id": "7199628",
 "name": "12 Mpx"
 }
 ]
 },
 {
 "id": "REAR_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara trasera",
 "value_id": "7199630",
 "value_name": "3840 px x 2160 px",
 "values": [
 {
 "id": "7199630",
 "name": "3840 px x 2160 px"
 }
 ]
 },
 {
 "id": "MAIN_FRONT_CAMERA_RESOLUTION",
 "name": "Resolución de la cámara frontal principal",
 "value_id": "7207109",
 "value_name": "12 Mpx",
 "values": [
 {
 "id": "7207109",
 "name": "12 Mpx"
 }
 ]
 },
 {
 "id": "WITH_FACIAL_RECOGNITION",
 "name": "Con reconocimiento facial",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "SIM_CARD_SLOTS_NUMBER",
 "name": "Cantidad de ranuras para tarjeta SIM",
 "value_id": "2087812",
 "value_name": "1",
 "values": [
 {
 "id": "2087812",
 "name": "1"
 }
 ]
 },
 {
 "id": "COMPATIBLE_SIM_CARD_SIZES",
 "name": "Tamaños de tarjeta SIM compatibles",
 "value_id": "80453",
 "value_name": "Nano-SIM",
 "values": [
 {
 "id": "80453",
 "name": "Nano-SIM"
 }
 ]
 },
 {
 "id": "WITH_ESIM",
 "name": "Con eSIM",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "ESIMS_NUMBER",
 "name": "Cantidad de eSIMs",
 "value_id": "11151772",
 "value_name": "2",
 "values": [
 {
 "id": "11151772",
 "name": "2"
 }
 ]
 },
 {
 "id": "RELEASE_MONTH",
 "name": "Mes de lanzamiento",
 "value_id": "8275348",
 "value_name": "Septiembre",
 "values": [
 {
 "id": "8275348",
 "name": "Septiembre"
 }
 ]
 },
 {
 "id": "RELEASE_YEAR",
 "name": "Año de lanzamiento",
 "value_id": "9676768",
 "value_name": "2021",
 "values": [
 {
 "id": "9676768",
 "name": "2021"
 }
 ]
 },
 {
 "id": "WEIGHT",
 "name": "Peso",
 "value_id": "462013",
 "value_name": "173 g",
 "values": [
 {
 "id": "462013",
 "name": "173 g"
 }
 ]
 },
 {
 "id": "HEIGHT",
 "name": "Altura",
 "value_id": "9095649",
 "value_name": "146.7 mm",
 "values": [
 {
 "id": "9095649",
 "name": "146.7 mm"
 }
 ]
 },
 {
 "id": "WIDTH",
 "name": "Ancho",
 "value_id": "5835158",
 "value_name": "71.5 mm",
 "values": [
 {
 "id": "5835158",
 "name": "71.5 mm"
 }
 ]
 },
 {
 "id": "DEPTH",
 "name": "Profundidad",
 "value_id": "7970551",
 "value_name": "7.65 mm",
 "values": [
 {
 "id": "7970551",
 "name": "7.65 mm"
 }
 ]
 },
 {
 "id": "DISPLAY_TECHNOLOGY",
 "name": "Tecnología de la pantalla",
 "value_id": "80491",
 "value_name": "OLED",
 "values": [
 {
 "id": "80491",
 "name": "OLED"
 }
 ]
 },
 {
 "id": "DISPLAY_TYPE",
 "name": "Tipo de pantalla",
 "value_id": "9785211",
 "value_name": "Super Retina XDR",
 "values": [
 {
 "id": "9785211",
 "name": "Super Retina XDR"
 }
 ]
 },
 {
 "id": "DISPLAY_ASPECT_RATIO",
 "name": "Relación de aspecto de la pantalla",
 "value_id": "11331351",
 "value_name": "19.5:9",
 "values": [
 {
 "id": "11331351",
 "name": "19.5:9"
 }
 ]
 },
 {
 "id": "DISPLAY_PIXELS_PER_INCH",
 "name": "Píxeles por pulgada de la pantalla",
 "value_id": "9095650",
 "value_name": "460 ppi",
 "values": [
 {
 "id": "9095650",
 "name": "460 ppi"
 }
 ]
 },
 {
 "id": "MAX_DISPLAY_BRIGHTNESS",
 "name": "Brillo máximo de la pantalla",
 "value_id": "7741025",
 "value_name": "1200 cd/m²",
 "values": [
 {
 "id": "7741025",
 "name": "1200 cd/m²"
 }
 ]
 },
 {
 "id": "WITH_TOUCHSCREEN_DISPLAY",
 "name": "Con pantalla táctil",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_PHYSICAL_QWERTY_KEYBOARD",
 "name": "Con teclado QWERTY físico",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_CAMERA",
 "name": "Con cámara",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "CAMERAS_MAIN_FEATURES",
 "name": "Características principales de las cámaras",
 "value_id": null,
 "value_name": "Bokeh, Modo noche, Deep fusion, HDR, Modo ráfaga",
 "values": [
 {
 "id": "9727052",
 "name": "Bokeh"
 },
 {
 "id": "9788716",
 "name": "Modo noche"
 },
 {
 "id": "11159138",
 "name": "Deep fusion"
 },
 {
 "id": "11625617",
 "name": "HDR"
 },
 {
 "id": "11151773",
 "name": "Modo ráfaga"
 }
 ]
 },
 {
 "id": "REAR_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras traseras",
 "value_id": "7477262",
 "value_name": "2",
 "values": [
 {
 "id": "7477262",
 "name": "2"
 }
 ]
 },
 {
 "id": "REAR_CAMERAS_RESOLUTION",
 "name": "Resolución de las cámaras traseras",
 "value_id": "7405025",
 "value_name": "12 Mpx/12 Mpx",
 "values": [
 {
 "id": "7405025",
 "name": "12 Mpx/12 Mpx"
 }
 ]
 },
 {
 "id": "REAR_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara trasera",
 "value_id": "11159135",
 "value_name": "f 1.6/f 2.4",
 "values": [
 {
 "id": "11159135",
 "name": "f 1.6/f 2.4"
 }
 ]
 },
 {
 "id": "FRONT_CAMERAS_NUMBER",
 "name": "Cantidad de cámaras frontales",
 "value_id": "7477216",
 "value_name": "1",
 "values": [
 {
 "id": "7477216",
 "name": "1"
 }
 ]
 },
 {
 "id": "FRONT_CAMERA_RECORDING_RESOLUTION",
 "name": "Resolución de video de la cámara frontal",
 "value_id": "7207112",
 "value_name": "3840 px x 2160 px",
 "values": [
 {
 "id": "7207112",
 "name": "3840 px x 2160 px"
 }
 ]
 },
 {
 "id": "FRONT_CAMERA_APERTURE",
 "name": "Apertura del diafragma de la cámara frontal",
 "value_id": "7408595",
 "value_name": "f 2.2",
 "values": [
 {
 "id": "7408595",
 "name": "f 2.2"
 }
 ]
 },
 {
 "id": "OPTICAL_ZOOM",
 "name": "Zoom óptico",
 "value_id": "1344",
 "value_name": "2x",
 "values": [
 {
 "id": "1344",
 "name": "2x"
 }
 ]
 },
 {
 "id": "DIGITAL_ZOOM",
 "name": "Zoom digital",
 "value_id": "7199631",
 "value_name": "5x",
 "values": [
 {
 "id": "7199631",
 "name": "5x"
 }
 ]
 },
 {
 "id": "MOBILE_NETWORK",
 "name": "Red",
 "value_id": "7472027",
 "value_name": "5G",
 "values": [
 {
 "id": "7472027",
 "name": "5G"
 }
 ]
 },
 {
 "id": "WITH_MEMORY_CARD_SLOT",
 "name": "Con ranura para tarjeta de memoria",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "PROCESSOR_MODEL",
 "name": "Modelo del procesador",
 "value_id": "11151775",
 "value_name": "Apple A15 Bionic",
 "values": [
 {
 "id": "11151775",
 "name": "Apple A15 Bionic"
 }
 ]
 },
 {
 "id": "PROCESSOR_CORES_NUMBER",
 "name": "Cantidad de núcleos del procesador",
 "value_id": "7199636",
 "value_name": "6",
 "values": [
 {
 "id": "7199636",
 "name": "6"
 }
 ]
 },
 {
 "id": "PROCESSOR_SPEED",
 "name": "Velocidad del procesador",
 "value_id": "11159137",
 "value_name": "3.22 GHz",
 "values": [
 {
 "id": "11159137",
 "name": "3.22 GHz"
 }
 ]
 },
 {
 "id": "GPU_MODEL",
 "name": "Modelo de GPU",
 "value_id": "7741027",
 "value_name": "Apple GPU",
 "values": [
 {
 "id": "7741027",
 "name": "Apple GPU"
 }
 ]
 },
 {
 "id": "CHARGE_CONNECTOR_TYPE",
 "name": "Tipo de conector de carga",
 "value_id": "8275368",
 "value_name": "Lightning",
 "values": [
 {
 "id": "8275368",
 "name": "Lightning"
 }
 ]
 },
 {
 "id": "WITH_USB_CONNECTOR",
 "name": "Con conector USB",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_3_5_MM_JACK_CONNECTOR",
 "name": "Con conector jack 3.5 mm",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_WIFI",
 "name": "Con Wi-Fi",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_GPS",
 "name": "Con GPS",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_BLUETOOTH",
 "name": "Con Bluetooth",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_NFC",
 "name": "Con NFC",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_RADIO",
 "name": "Con radio",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "WITH_ACCELEROMETER",
 "name": "Con acelerómetro",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_PROXIMITY_SENSOR",
 "name": "Con sensor de proximidad",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_GYROSCOPE",
 "name": "Con giroscopio",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_COMPASS",
 "name": "Con brújula",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_BAROMETER",
 "name": "Con barómetro",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IS_WATER_RESISTANT",
 "name": "Es resistente al agua",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IS_DUST_RESISTANT",
 "name": "Es resistente al polvo",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "IP_RATING",
 "name": "Clasificación IP",
 "value_id": "8275373",
 "value_name": "IP68",
 "values": [
 {
 "id": "8275373",
 "name": "IP68"
 }
 ]
 },
 {
 "id": "BATTERY_TYPE",
 "name": "Tipo de batería",
 "value_id": "95013",
 "value_name": "Ion de litio",
 "values": [
 {
 "id": "95013",
 "name": "Ion de litio"
 }
 ]
 },
 {
 "id": "WITH_FAST_CHARGING",
 "name": "Con carga rápida",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_WIRELESS_CHARGING",
 "name": "Con carga inalámbrica",
 "value_id": "242085",
 "value_name": "Sí",
 "values": [
 {
 "id": "242085",
 "name": "Sí",
 "meta": {
 "value": true
 }
 }
 ],
 "meta": {
 "value": true
 }
 },
 {
 "id": "WITH_REMOVABLE_BATTERY",
 "name": "Con batería removible",
 "value_id": "242084",
 "value_name": "No",
 "values": [
 {
 "id": "242084",
 "name": "No",
 "meta": {
 "value": false
 }
 }
 ],
 "meta": {
 "value": false
 }
 },
 {
 "id": "MPN",
 "name": "MPN",
 "value_id": "11159158",
 "value_name": "MLNF3E/A",
 "values": [
 {
 "id": "11159158",
 "name": "MLNF3E/A"
 }
 ]
 }
 ],
 "short_description": {
 "type": "plaintext",
 "content": "iPhone 13. El sistema de dos cámaras más avanzado en un iPhone. El superrápido chip A15 Bionic. Un gran\nsalto en duración de batería. Un diseño resistente. Y una pantalla Super Retina XDR más brillante.\n\nAvisos Legales\n(1)La pantalla tiene esquinas redondeadas que siguen el elegante diseño curvo del teléfono, y las esquinas se encuentran dentro de un rectángulo estándar. Si se mide en forma de rectángulo estándar, la pantalla tiene 6.06 pulgadas en diagonal. El área real de visualización es menor.\n(2)La duración de la batería varía según el uso y la configuración.\n(3)El iPhone 13 es resistente a los derrames, a las salpicaduras y al polvo, y fue probado en condiciones de laboratorio controladas, con una clasificación IP68 según la norma IEC 60529. La resistencia a los derrames, a las salpicaduras y al polvo no es una condición permanente, y podría disminuir como consecuencia del uso normal. No intentes cargar un iPhone mojado; consulta el manual del usuario para ver las instrucciones de limpieza y secado. La garantía no cubre daños producidos por líquidos.\n(4)Algunas funcionalidades podrían no estar disponibles en todos los países o áreas.\n(5)Los accesorios se venden por separado."
 },
 "parent_id": "MLA18500843",
 "children_ids": [],
 "settings": {
 "listing_strategy": "catalog_required",
 "has_rich_description": false
 },
 "buy_box_activation_date": "2022-04-22T15:20:31Z",
 "authority_types": [
 "INTERNAL"
 ],
 "date_created": "2021-09-28T18:23:39Z"
}
```

When publishing to catalog products, you should consider that.

<

**The **children\_ids** field from the previous answer:**

* If the field is empty, it is because it is a **child** product, which is specific enough to publish.
* If this field contains IDs of other products, it means that the current **catalog\_product\_id** corresponds to a **parent** product (not fully specified). To publish to the catalog we must search for a specific product among its **child\_ids**.

**The status field from the previous answer:**

* To create a catalog publication, the product must have the status=active.
* Parent" products will never have status=active because they cannot be bought.

 

## Choose a product to list

Marketplace publication and/or their catalog eligible variations have a **catalog\_product\_id** field that must be checked before publishing to catalog, as this field tells you which catalog product is suitable for publishing to the /products/$CATALOG\_PRODUCT\_ID resource.

Example to get the **catalog\_product\_id** information in a marketplace publication:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA1150086340
```

Short response:

```
{
 "id": "MLA1150086340",
 "site_id": "MLA",
 "title": "Apple iPad Air De 10.9 Wi-fi 256gb Oro Rosa (4ª Generación)",
 "subtitle": null,
 "seller_id": 123456,
 "category_id": "MLA82085",
 "official_store_id": null,
 "price": 190000,
 "base_price": 190000,
 "original_price": null,
 "inventory_id": "PFQC17442",
 "currency_id": "ARS",
 "initial_quantity": 4,
 "available_quantity": 1,
 "sold_quantity": 3,
 "sale_terms": [... 
 ],
 "pictures": [... ],
 "video_id": null,
 "attributes": [...
 ],

 "warranty": "Garantía de fábrica: 12 meses",
 "catalog_product_id": "MLA16242935",
 "domain_id": "MLA-TABLETS",
 "channels": [
 "marketplace",
 "mshops"
 ],
 "bundle": null
}
```

When creating a catalog post from an eligible marketplace post, you will need to check with our product resource **/products/$CATALOG\_PRODUCT\_ID**:

* If the field **catalog\_product\_id** corresponds to a product with active status, if so it is ready to publish to catalog using this **catalog\_product\_id**.
* If the field **catalog\_product\_id** corresponds to a product with status inactive, you will have to inform Mercado Livre to make your marketplace publication again, since if you try to publish in catalog you will get an error.
* If the array **children\_ids** is empty, it means that the publication or variation is already associated to the most specific product we have and it is not ready to publish in the catalog yet, until the product is edited by Mercado Libre.
* If the array **children\_ids** is not empty, you should search among the children products for the one that exactly matches (comparing the datasheets) the one you are selling.
* If you find an active **catalog\_product\_id** child that matches exactly with what you want to sell, you can use it in the next step to create your catalog publication.
* If among the child **catalog\_product\_id** you can't find your exact product, you can publish normally and will have to wait for Mercado Livre to create the appropriate product for your datasheet.

**Next**: [Catalog listing](https://developers.mercadolibre.com.ar/en_us/catalog-listing).
