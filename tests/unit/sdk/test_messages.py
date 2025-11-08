import pytest
from src.core.exceptions import ApiError


def test_send_message_success(messages, mock_api_client):
    """Test successfully sending a message."""
    # Mock API response
    mock_api_client.request.return_value = {
        "id": "msg123",
        "from": "+123456789",
        "to": {"id": "contact123", "name": "John Doe", "phone": "+987654321"},
        "content": "Hello, World!",
        "status": "queued",
        "createdAt": "2024-11-28T10:00:00Z"
    }

    # Corrected payload
    payload = {
        "to": {"id": "contact123"},  # The `to` field must be a dictionary with a valid contact ID
        "content": "Hello, World!",
        "from": "+123456789"  # Use `from` field (aliased to `from_sender` in the schema)
    }

    # Call the send_message method
    response = messages.send_message(payload=payload)

    # Assertions
    mock_api_client.request.assert_called_once_with("POST", "/messages", json=payload)
    assert response["id"] == "msg123"
    assert response["status"] == "queued"
    assert response["content"] == "Hello, World!"
    assert response["to"] == {"id": "contact123", "name": "John Doe", "phone": "+987654321"}


def test_send_message_validation_error(messages):
    """Test validation error when payload is invalid."""
    payload = {"to": "+987654321"}  # Missing 'content' and 'sender'
    with pytest.raises(ValueError, match="Invalid payload"):
        messages.send_message(payload=payload)


def test_send_message_api_error(messages, mock_api_client):
    """Test API error during message sending."""
    # Mock API error
    mock_api_client.request.side_effect = ApiError("Unhandled API Error")

    # Corrected payload
    payload = {
        "to": {"id": "contact123"},  # Use correct dictionary structure for `to`
        "content": "Hello, World!",
        "from": "+123456789"  # Use `from` field (aliased to `from_sender`)
    }

    # Ensure the error is raised as expected
    with pytest.raises(ApiError, match="Unhandled API Error"):
        messages.send_message(payload=payload)

    # Validate that the request was called with the correct parameters
    mock_api_client.request.assert_called_once_with("POST", "/messages", json=payload)


def test_list_messages_success(messages, mock_api_client):
    """Test successfully listing messages."""
    # Mock response
    mock_response = {
        "messages": [
            {
                "id": "msg123",
                "from": "+123456789",
                "to": "+987654321",
                "content": "Hello, World!",
                "status": "queued",
                "createdAt": "2024-11-28T10:00:00Z"
            }
        ],
        "page": 1,
        "quantityPerPage": 10
    }
    mock_api_client.request.return_value = mock_response

    # Call method
    response = messages.list_messages(page=1, limit=10)

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", "/messages", params={"page": 1, "limit": 10})
    assert len(response["messages"]) == 1
    assert response["messages"][0]["id"] == "msg123"


def test_get_message_success(messages, mock_api_client):
    """Test successfully retrieving a specific message."""
    # Mock response
    mock_response = {
        "id": "msg123",
        "from": "+123456789",
        "to": "+987654321",
        "content": "Hello, World!",
        "status": "queued",
        "createdAt": "2024-11-28T10:00:00Z"
    }
    mock_api_client.request.return_value = mock_response

    # Call method
    response = messages.get_message(message_id="msg123")

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", "/messages/msg123")
    assert response["id"] == "msg123"
    assert response["content"] == "Hello, World!"
