# MercadoLibre Questions & Answers API

Source: https://global-selling.mercadolibre.com/devsite/manage-questions-answers-global-selling

## Overview

Questions are how buyers communicate with sellers before a transaction. This API allows searching, answering, and deleting questions.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /marketplace/questions/search | Search questions by seller, item, or user |
| GET | /marketplace/questions/{QUESTION_ID} | Get specific question |
| POST | /marketplace/answers | Post an answer |
| DELETE | /marketplace/questions/{QUESTION_ID} | Delete a question |

## Search Questions

### By Seller
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/search?seller_id=$SELLER_ID'
```

### By Item
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/search?item=$ITEM_ID'
```

### By User on Item
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/search?item=$ITEM_ID&from=$USER_ID'
```

### With Sorting
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/search?seller_id=$SELLER_ID&sort_fields=date_created&sort_types=DESC'
```

Sort fields: item_id, seller_id, from_id, date_created
Sort types: ASC, DESC

## Question Status Values

| Status | Description |
|--------|-------------|
| UNANSWERED | Not answered yet |
| ANSWERED | Has been answered |
| CLOSED_UNANSWERED | Item closed, never answered |
| UNDER_REVIEW | Under review |
| BANNED | Policy violation |
| DELETED | Deleted |
| DISABLED | Disabled |

## Get Question by ID

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/$QUESTION_ID'
```

Response includes:
- id, seller_id, text, text_translated, status
- item_id (CBT), marketplace_item_id (MLM)
- answer.text, answer.text_translated, answer.status

## Answer a Question

Max 2000 characters.

```bash
curl -X POST -H 'Authorization: Bearer $ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  'https://api.mercadolibre.com/marketplace/answers' \
  -d '{
    "question_id": $QUESTION_ID,
    "text": "Answer text",
    "text_translated": "Translated answer (optional)"
  }'
```

## Delete a Question

```bash
curl -X DELETE -H 'Authorization: Bearer $ACCESS_TOKEN' \
  'https://api.mercadolibre.com/marketplace/questions/$QUESTION_ID'
```

## Receive Notifications

1. Configure callback URL in Application Manager
2. Subscribe to **marketplace_questions** topic
3. Notification payload:
```json
{
  "user_id": 1234,
  "resource": "/marketplace/questions/139876",
  "topic": "marketplace_questions",
  "received": "2011-10-19T16:38:34.425Z",
  "sent": "2011-10-19T16:40:34.425Z"
}
```
4. Return HTTP 200 OK to acknowledge

## Available Filters

- item: Filter by item ID
- from: Filter by buyer user ID
- status: Filter by question status
- Offset max: 1000

## Errors

| Error Code | Message | Solution |
|------------|---------|----------|
| invalid_question | Question is invalid | Verify question_id is valid |
| invalid_post_body | Invalid JSON | Check required params: question_id, text |
