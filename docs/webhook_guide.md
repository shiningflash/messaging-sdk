# Webhook Guide

## Overview

This document serves as a comprehensive guide for understanding and using the webhook functionality in the `messaging-sdk`. The webhook is designed to handle message delivery notifications from the API server, verifying the authenticity of the events and processing them as needed.

---

# Table of Contents

1. [Key Concepts](#key-concepts)
   - [Webhooks in Messaging](#webhooks-in-messaging)
   - [Authorization and Security](#authorization-and-security)
2. [Setting Up the Webhook](#setting-up-the-webhook)
   - [Configuration](#configuration)
   - [Starting the Webhook Server](#starting-the-webhook-server)
3. [Validating the Signature](#validating-the-signature)
   - [Example Code](#example-code)
4. [How to Use](#how-to-use)
   - [Receiving Webhook Events](#receiving-webhook-events)
   - [Processing Webhook Payloads](#processing-webhook-payloads)
5. [Testing the Webhook](#testing-the-webhook)
   - [Unit Tests](#unit-tests)
   - [Integration Tests](#integration-tests)
   - [Common Errors and Troubleshooting](#common-errors-and-troubleshooting)
     - [401 Unauthorized](#error-401-unauthorized)
     - [422 Unprocessable Entity](#error-422-unprocessable-entity)
6. [Advanced Features](#advanced-features)
   - [Customizing the Webhook Server](#customizing-the-webhook-server)
7. [Additional Resources](#additional-resources)

---

## Key Concepts

### Webhooks in Messaging
When a message is sent, it is initially marked as `queued`. The API server simulates a sending queue and eventually updates the status to `delivered` or `failed`. This status update is communicated to your application through a webhook URL, configured as:

```
http://localhost:3010/webhooks
```

### Authorization and Security
Each webhook event includes an `Authorization` header containing an HMAC signature. The signature is generated using the payload and a secret key. Your application must validate the signature to ensure the event is authentic.

---

## Setting Up the Webhook

### Configuration

Ensure the environment variables are set in your `.env` file. Copy all from `.env.example` and paste them to newly created `.env`, and update the values accordingly.

### Starting the Webhook Server

The webhook server is implemented using `FastAPI`. To start the server:

```bash
uvicorn src.server.app:app --reload --port 3010
```

The server will run at `http://localhost:3010`.

---

## Validating the Signature

The SDK provides a `verify_signature` utility to validate the HMAC signature. Here's how it works:

1. The server extracts the raw payload and the `Authorization` header.
2. The `verify_signature` function compares the provided signature with a locally generated one.
3. If the signatures match, the payload is processed.

Example Code:

```python
from src.core.security import verify_signature

try:
    verify_signature(message=raw_payload, signature=auth_header, secret=WEBHOOK_SECRET)
    print("Signature validated successfully.")
except ValueError:
    print("Invalid signature.")
```

---

## How to Use

### Receiving Webhook Events

The endpoint `/webhooks` is used to receive events. Here’s an example payload:

```json
{
    "id": "msg123",
    "status": "delivered",
    "deliveredAt": "2024-12-01T12:00:00Z"
}
```

### Processing Webhook Payloads

The server processes payloads as follows:

1. **Signature Validation**:
   - Verifies the `Authorization` header using the `WEBHOOK_SECRET`.

2. **Payload Parsing**:
   - Converts the raw request body into a structured object using the `WebhookPayload` schema.

3. **Event Handling**:
   - Logs the payload and prints it to the console (as required by the assignment).

Example of processing in `app.py`:

```python
@app.post("/webhooks")
async def handle_webhook(
    payload: WebhookPayload,
    authorization: str = Header(...),
    request: Request
):
    try:
        raw_body = await request.body()
        verify_signature(raw_body, authorization, settings.WEBHOOK_SECRET)
        logger.info(f"Webhook received: {payload.model_dump()}")
        print(f"Processed webhook payload: {payload.model_dump()}")
        return {"message": "Webhook processed successfully."}
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
```

---

## Testing the Webhook

Test the webhook by sending a simulated payload to it:

```bash
curl -X POST http://localhost:3010/webhooks \
     -H "Authorization: Bearer <calculated-signature>" \
     -d '{"id": "msg123", "status": "delivered", "deliveredAt": "2024-11-30T12:00:00Z"}'
```

For example,

```bash
secret="mySecret"
payload='{"id": "msg123", "status": "delivered", "deliveredAt": "2024-11-30T12:00:00Z"}'
signature=$(echo -n $payload | openssl dgst -sha256 -hmac $secret | awk '{print $2}')

curl -X POST http://localhost:3010/webhooks \
     -H "Authorization: Bearer $signature" \
     -H "Content-Type: application/json" \
     -d "$payload"
```

The response should be look like this,

```
{"message":"Webhook processed successfully."}
```

### Unit Tests

Run unit tests to verify webhook functionality:

```bash
pytest tests/unit/test_server
```

### Integration Tests

Run integration tests to verify webhook functionality:

```bash
pytest tests/integration/test_webhook.py
```

### Common Errors and Troubleshooting

###### Error: `401 Unauthorized`
- Cause: Invalid signature in the `Authorization` header.
- Solution: Ensure the `WEBHOOK_SECRET` is correct and the payload is serialized properly.

###### Error: `422 Unprocessable Entity`
- Cause: Invalid payload structure.
- Solution: Validate the payload against the `WebhookPayload` schema.

---

## Advanced Features

### Customizing the Webhook Server

The webhook server is modular and can be extended for advanced use cases:
- **Custom Routes**: Add new endpoints for other event types.
- **Database Integration**: Store event payloads in a database for future analysis.
- **Retry Mechanism**: Implement logic to retry failed webhooks.

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HMAC Authentication](https://en.wikipedia.org/wiki/HMAC)
- [Pydantic Schema Validation](https://docs.pydantic.dev/)
