import pytest


@pytest.mark.e2e
def test_send_message_and_verify(mock_api_client, messages):
    """
    E2E Test: Send a message and verify it is successfully sent.
    """
    # Step 1: Mock the API response for sending a message
    send_response = {
        "id": "msg123",
        "to": {
            "id": "contact123",
            "name": "John Doe",
            "phone": "+123456789"
        },
        "from": "+987654321",
        "content": "Hello, World!",
        "status": "delivered",
        "createdAt": "2024-12-01T00:00:00Z",
    }
    mock_api_client.request.return_value = send_response

    # Step 2: Send the message
    send_payload = {
        "to": {"id": "contact123"},  # Match the expected schema
        "content": "Hello, World!",
        "from": "+987654321"  # Use the correct field name
    }
    sent_message = messages.send_message(payload=send_payload)
    assert sent_message == send_response, "Failed to send message."

    # Step 3: Mock the API response for retrieving the message
    retrieve_response = {
        "id": "msg123",
        "to": {
            "id": "contact123",
            "name": "John Doe",
            "phone": "+123456789"
        },
        "from": "+987654321",
        "content": "Hello, World!",
        "status": "delivered",
        "createdAt": "2024-12-01T00:00:00Z",
    }
    mock_api_client.request.return_value = retrieve_response

    # Step 4: Retrieve the message and verify its details
    retrieved_message = messages.get_message(message_id="msg123")
    assert retrieved_message == retrieve_response, "Failed to retrieve the sent message."

    # Ensure the API calls were made as expected
    mock_api_client.request.assert_any_call("POST", "/messages", json=send_payload)
    mock_api_client.request.assert_any_call("GET", "/messages/msg123")


@pytest.mark.e2e
def test_list_messages_with_pagination(mock_api_client, messages):
    """
    E2E Test: List messages with pagination and verify the correct data is returned.
    """
    # Step 1: Mock the API response for listing messages
    list_response = {
        "messages": [
            {
                "id": "msg123",
                "to": "+123456789",
                "from": "+987654321",
                "content": "Hello, World!",
                "status": "delivered",
                "createdAt": "2024-12-01T00:00:00Z",
            },
            {
                "id": "msg124",
                "to": "+987654321",
                "from": "+123456789",
                "content": "Hi there!",
                "status": "delivered",
                "createdAt": "2024-12-01T00:05:00Z",
            },
        ],
        "page": 1,
        "quantityPerPage": 2,
    }
    mock_api_client.request.return_value = list_response

    # Step 2: List messages
    messages_list = messages.list_messages(page=1, limit=2)
    assert messages_list == list_response, "Failed to list messages with pagination."

    # Ensure the API call was made as expected
    mock_api_client.request.assert_called_once_with(
        "GET", "/messages", params={"page": 1, "limit": 2}
    )


@pytest.mark.e2e
def test_resend_failed_message(mock_api_client, messages):
    """
    E2E Test: Simulate resending a failed message using send_message.
    """
    # Step 1: Mock the API response for retrieving a failed message
    retrieve_response = {
        "id": "msg123",
        "to": {
            "id": "contact123",
            "name": "John Doe",
            "phone": "+123456789"
        },
        "from": "+987654321",
        "content": "Hello, World!",
        "status": "failed",
        "createdAt": "2024-12-01T00:00:00Z",
    }
    mock_api_client.request.return_value = retrieve_response

    # Step 2: Retrieve the failed message
    failed_message = messages.get_message(message_id="msg123")
    assert failed_message == retrieve_response, "Failed to retrieve the failed message."

    # Step 3: Mock the API response for resending the message
    resend_payload = {
        "to": {"id": "contact123"},  # Match the expected schema
        "content": "Hello, World!",
        "from": "+987654321"  # Use the correct field
    }
    resend_response = {
        "id": "msg123",
        "to": {
            "id": "contact123",
            "name": "John Doe",
            "phone": "+123456789"
        },
        "from": "+987654321",
        "content": "Hello, World!",
        "status": "delivered",
        "createdAt": "2024-12-01T00:00:00Z",
    }
    mock_api_client.request.return_value = resend_response

    # Step 4: Resend the message
    resent_message = messages.send_message(payload=resend_payload)
    assert resent_message == resend_response, "Failed to resend the failed message."

    # Ensure the API calls were made as expected
    mock_api_client.request.assert_any_call("GET", "/messages/msg123")
    mock_api_client.request.assert_any_call("POST", "/messages", json=resend_payload)
