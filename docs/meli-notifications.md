# MercadoLibre Notifications / Webhooks API

Source: https://global-selling.mercadolibre.com/devsite/receive-notifications

## Overview

Receiving notifications enables you to have a real-time feed of changes on different API resources. Events trigger HTTP POST notifications to your configured callback URL.

## Setup

1. Go to application manager: https://global-selling.mercadolibre.com/devcenter/
2. Configure **Notifications Callback URL**: public URL where system sends notifications via HTTP POST
3. Select **Topics** to subscribe to

## Available Topics

| Topic | Description |
|-------|-------------|
| **items** | Changes on parent items you published |
| **marketplace items** | Changes to any of your marketplace items |
| **marketplace orders** | Recently created sales orders |
| **marketplace questions** | Questions asked or answered |
| **marketplace messages** | New messages with your user_id as receiver |
| **marketplace shipments** | Creation and shipping changes to confirmed sales |
| **marketplace claims** | Sales claims |
| **marketplace fbm stock** | Fulfillment stock notifications |
| **marketplace item competition** | Competing catalog listings status changes (available in Mexico) |
| **marketplace pricing suggestion** | Pricing suggestions for items |
| **public offers** | Offer on item created or status change |
| **public candidates** | Item invited to participate in promotion |

## Important Requirements

- Return HTTP 200 within **500 milliseconds** or topics will be disabled
- Messages sent at exponential intervals, delivery attempts at 1-hour intervals
- After 1 hour, unaccepted messages are excluded
- Use queues: confirm receipt immediately (HTTP 200), then query the API

## Notification Format

All notifications follow this structure:
```json
{
  "_id": "5da8a1b24be30a49eb66c52a",
  "resource": "/items/CBT123456789",
  "user_id": 123456789,
  "topic": "items",
  "application_id": 2069392825111111,
  "attempts": 1,
  "sent": "2020-01-09T13:44:33.006Z",
  "received": "2020-01-09T13:44:32.984Z"
}
```

## Getting Details After Notification

### items
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/items/$ITEM_ID
```

### marketplace items
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/items/$ITEM_ID
```

### marketplace orders
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/orders/$ORDER_ID
```

### marketplace questions
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/questions/$QUESTION_ID
```

### marketplace messages
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/messages/$RESOURCE
```

### marketplace shipments
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/shipments/$RESOURCE
```

### marketplace claims
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/claims/$RESOURCE
```

### marketplace fbm stock
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/$RESOURCE
```

### marketplace item competition
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/$RESOURCE
```

### marketplace pricing suggestion
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/marketplace/benchmarks/items/$ITEM_ID/details
```

### public offers
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/marketplace/seller-promotions/promotions/offer/$OFFER_ID/$USER_ID
```

### public candidates
```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/marketplace/seller-promotions/promotions/candidate/$CANDIDATE_ID/$USER_ID
```

## Feed History (Missed Notifications)

```bash
curl -X GET -H 'Authorization: Bearer $ACCESS_TOKEN' https://api.mercadolibre.com/missed_feeds?app_id=$APP_ID
```

### Filter by topic
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/myfeeds?app_id=$APP_ID&topic=$TOPIC
```

### Pagination
```bash
curl -H 'Authorization: Bearer $ACCESS_TOKEN' -X GET https://api.mercadolibre.com/myfeeds?app_id=$APP_ID&offset=1&limit=5
```

## IP Addresses for Filtering
- 54.88.218.97
- 18.215.140.160
- 18.213.114.129
- 18.206.34.84

## Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | (callback URL) | MeLi sends notification to your URL |
| GET | /missed_feeds?app_id=$APP_ID | Get missed notifications |
| GET | /myfeeds?app_id=$APP_ID&topic=$TOPIC | Filter missed notifications by topic |
