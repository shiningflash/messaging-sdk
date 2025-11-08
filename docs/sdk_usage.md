# SDK Usage Guide

Welcome to the **messaging-sdk** SDK Usage Guide. This document provides detailed instructions for installing, configuring, and utilizing the SDK, including advanced features and best practices.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
    - [Sending Messages](#sending-messages)
    - [Managing Contacts](#managing-contacts)
5. [Advanced Usage](#advanced-usage)
    - [Pagination](#pagination)
    - [Retry Mechanism](#retry-mechanism)
6. [Error Handling](#error-handling)
7. [Testing](#testing)
8. [Logging](#logging)
9. [Complete Functionalities](#complete-functionalities)

---

## Introduction

The `messaging-sdk` is a Python library designed for seamless integration with messaging and contacts APIs. It provides:

- Simplified API interactions with minimal setup.
- Robust error handling and retry mechanisms.
- Logging for debugging and monitoring.
- Easy-to-use methods for sending messages and managing contacts.

---

## Installation

To install the SDK locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/shiningflash/messaging-sdk.git
    cd messaging-sdk
    ```

2. Install additional dependencies if required:

    ```bash
    pip install -r requirements.txt
    ```

---

## Configuration

1. Copy the `.env.example` file and rename it to `.env`:

    ```bash
    cp .env.example .env
    ```

2. Open `.env` and configure the following variables:

    - `BASE_URL`: Base URL for the API (e.g., `http://localhost:3000`).
    - `API_KEY`: Your API key for authentication.
    - `WEBHOOK_SECRET`: Secret key for validating webhooks.

Install the SDK using pip in editable mode:

```bash
pip install -e .
```

---

## Basic Usage

### Sending Messages

The SDK allows you to send messages easily:

```python
from sdk.client import ApiClient
from sdk.features.messages import Messages

client = ApiClient()
messages = Messages(client)

# Prepare the payload
payload = {
    "to": {"id": "contact-id"},  # Contact ID
    "content": "Hello, world!",
    "from": "+9876543210"  # Sender's phone number
}

# Send the message
response = messages.send_message(payload=payload)
print(response)
```

### Managing Contacts

You can create, list, and delete contacts:

```python
from sdk.features.contacts import Contacts

contacts = Contacts(client)

# Create a new contact
new_contact = {
    "name": "John Doe",
    "phone": "+1234567890"
}
response = contacts.create_contact(new_contact)

# List all contacts
contacts_list = contacts.list_contacts(page=1, max=5)
print(contacts_list)

# Delete a contact
contacts.delete_contact(contact_id="contact-id")
```

---

## Advanced Usage

### Pagination

The SDK supports pagination for listing messages and contacts:

```python
# Retrieve paginated messages
messages_list = messages.list_messages(page=1, limit=10)
print(messages_list)

# Retrieve paginated contacts
contacts_list = contacts.list_contacts(page=1, max=5)
print(contacts_list)
```

### Retry Mechanism

The SDK automatically retries requests for transient errors (e.g., HTTP 503). The retry logic is located in `src/core/retry.py` and can be customized.

---

## Error Handling

The SDK provides built-in exceptions for various scenarios:

- `UnauthorizedError`: Raised for authentication errors (`401 Unauthorized`).
- `NotFoundError`: Raised when a resource is not found (`404 Not Found`).
- `ServerError`: Raised for server-side errors (`500 Internal Server Error`).
- `ContactNotFoundError`: Raised for missing contacts.
- `MessageNotFoundError`: Raised for missing messages.
- `ApiError`: Raised for other API-related issues.

Example:

```python
try:
    messages.get_message("invalid-id")
except MessageNotFoundError as e:
    print(f"Message not found: {e}")
except ApiError as e:
    print(f"API Error: {e}")
```

---

## Testing

Run tests using `pytest`:

```bash
pytest
```

To check code coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

---

## Logging

Logs provide detailed insights into SDK operations:

- **Console Logs**: Informational logs for debugging.
- **File Logs**: Errors and warnings logged to `logs/app.log`.

Example:

```python
from sdk.core.logger import logger

logger.info("Starting application...")
```

---

## Complete Functionalities

### Messages

- **Send Message**: `send_message(payload)`
- **List Messages**: `list_messages(page, limit)`
- **Get Message by ID**: `get_message(message_id)`

### Contacts

- **Create Contact**: `create_contact(contact_payload)`
- **List Contacts**: `list_contacts(page, max)`
- **Delete Contact**: `delete_contact(contact_id)`
