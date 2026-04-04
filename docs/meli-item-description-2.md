URL: https://developers.mercadolibre.com.ar/en_us/item-description-2
Title: Developers

## Item description

The description of item contains information about the product and serves to complement what is detailed in the data sheet. Remember that this will allow the buyer to quickly find all the specifications that characterize the products. What kind of information should the description include? It should include the technical characteristics and the differentiators against competition. You can check all [the details on how to describe a product](https://ayuda.mercadolibre.com.ar/ayuda/completar_datos_productos_3147).

 

## Tips for describing a post

* First load the important data in the data sheet, that is to say all the specifications without forgetting the universal product code.
* Verify that the data that you are going to write in the description are the details that are not in the data sheet.
* Nests the information so that it is well organized. Use uppercase, hyphens, spacing, etc.
* Be brief and read your own description to check its length.

 

## Get item description

Request:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/$ITEM_ID/description
```

Example:

```
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/items/MLA935110000/description
```

Response:

```
{
 "text": "",
 "plain_text": "Compendio de Anatomía y Disección. H. Rouviere. 1986. Salvat Editores SA. Sin uso.",
 "last_updated": "2021-08-20T02:07:27.000Z",
 "date_created": "2021-08-20T02:07:27.000Z",
 "snapshot": {...}
}
```

 

## Uploading item description

Once the item is created, you can load its description by performing the following POST. Remember that they must contain plain text and you will not be able to change the fonts, sizes or mark texts in bold. You can only perform line breaks as follows: \\n.

```
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -d
{
 "plain_text":"Descripción con Texto Plano \n"
}
https://api.mercadolibre.com/items/$ITEM_ID/description
```

When trying to POST with description on a publication that already has it, you will receive a bad request error and you have [edit the item description](https://developers.mercadolibre.com.ar/en_us/item-description-2#Replacing).

 

## Benefits of using plain text

* They will have better results in searches.
* Descriptions can be downloaded 5 times faster.
* They will be properly displayed in all devices (mobile, tablets, computer).
* Besides, you will be able to upload up to 10 item pictures and/or a link with a YouTube video.

Find below an example of the best practice to prepare a description:

**Item:**“Babolat Pure Control 3 Racket” \[su\_custom\_gallery source="media: 10252" limit="1" link="lightbox" width="870" height="890"\]

Notes:

\- Bear in mind that you can add any payment and shipping method that you wish to the VIP. 
\- If you want your listing to show all item variations, even differential stock for each of them, we encourage you to [use customized variations](https://developers.mercadolibre.com.ar/en_us/variations#Customized-variation). 
\- Bear in mind that if you list using html and plain text, the priority will be given to the latter.

 

## Replacing an existing description

To make modifications to the existing descriptions, you will have to carry out the following PUT.

Example:

```
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -d
{
 "plain_text":"Los mejores Rayban Wayfarer. Test."
}
https://api.mercadolibre.com/items/$ITEM_ID/description?api_version=2
```

 

## Errors

### Listing description

In the event that you POST items by creating a post with a description that contains some unacceptable character, the response will contain more information about the error, such as the position of the wrong character.

Example:

```
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -d
{
 "plain_text":"Texto < br > 😀"
}
https://api.mercadolibre.com/items/$ITEM_ID/description
```

In the response you can identify that the errors are in position 12:

```
{
 "message":"Validation error",
 "error":"validation_error",
 "status":400,
 "cause":[
 {
 "department":"items",
 "cause_id":398,
 "type":"error",
 "code":"item.description.type.invalid",
 "references":[
 "plain_text[12]"
 ],
 "message":"The description must be in plain text"
 }
 ]
}
```

### Modifying an existing description

```
curl -X PUT -H 'Authorization: Bearer $ACCESS_TOKEN' -H "Content-Type: application/json" -d
{
 "plain_text":"< br > 😀"
}
https://api.mercadolibre.com/items/$ITEM_ID/description?api_version=2
```

For the response to return the position of the character that generates error, you must add the parameter api\_version=2.

The error will be:

```
{
 "message": "Validation error",
 "error": "validation_error",
 "status": 400,
 "cause": [
 {
 "department": "items",
 "cause_id": 398,
 "type": "error",
 "code": "item.description.type.invalid",
 "references": [
 "plain_text[7]"
 ],
 "message": "The description must be in plain text"
 }
 ]
}
```

In the references array you can get the exact location of the character that generates the error. In this case 7.
