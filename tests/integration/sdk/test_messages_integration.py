import pytest
from src.core.exceptions import ApiError, UnauthorizedError, MessageNotFoundError

def test_send_message_success(messages, mock_api_client):
    """
    Test sending a message successfully.
    """
    mock_response = {
        "id": "msg123",
        "to": "+123456789",
        "from": "+987654321",
        "content": "Hello, World!",
        "sender": "Sender123",
        "status": "delivered",
        "createdAt": "2024-12-01T00:00:00Z"
    }
    mock_api_client.request.return_value = mock_response

    payload = {
        "to": "+123456789",
        "content": "Hello, World!",
        "sender": "Sender123"
    }

    result = messages.send_message(payload)

    mock_api_client.request.assert_called_once_with(
        "POST", "/messages", json=payload
    )
    assert result == mock_response


def test_send_message_validation_error(messages, mock_api_client):
    """
    Test sending a message with an invalid payload.

    - The payload validation should fail.
    - The `request` method of the mocked client should never be called.
    """
    # Invalid payload (missing required fields: `content`, `sender`)
    invalid_payload = {"to": "+123456789"}

    # Expect ValueError when the payload is validated
    with pytest.raises(ValueError, match="Invalid payload"):
        messages.send_message(payload=invalid_payload)

    # Assert that no request was made
    mock_api_client.request.assert_not_called()


def test_list_messages_success(messages, mock_api_client):
    """
    Test listing messages with pagination successfully.
    """
    mock_response = {
        "total": 1,
        "page": 1,
        "quantityPerPage": 10,
        "messages": [
            {
                "id": "msg123",
                "to": "+123456789",
                "from": "+987654321",
                "content": "Hello, World!",
                "sender": "Sender123",
                "status": "delivered",
                "createdAt": "2024-12-01T00:00:00Z"
            }
        ]
    }
    mock_api_client.request.return_value = mock_response

    result = messages.list_messages(page=1, limit=10)

    mock_api_client.request.assert_called_once_with(
        "GET", "/messages", params={"page": 1, "limit": 10}
    )
    assert result == mock_response


def test_list_messages_error(messages, mock_api_client):
    """
    Test error when listing messages.
    """
    mock_api_client.request.side_effect = ApiError("An error occurred.")

    with pytest.raises(ApiError, match="An error occurred."):
        messages.list_messages(page=1, limit=10)


def test_get_message_success(messages, mock_api_client):
    """
    Test retrieving a specific message successfully.
    """
    mock_response = {
        "id": "msg123",
        "to": "+123456789",
        "from": "+987654321",
        "content": "Hello, World!",
        "sender": "Sender123",
        "status": "delivered",
        "createdAt": "2024-12-01T00:00:00Z"
    }
    mock_api_client.request.return_value = mock_response

    result = messages.get_message("msg123")

    mock_api_client.request.assert_called_once_with(
        "GET", "/messages/msg123"
    )
    assert result == mock_response


def test_get_message_not_found(messages, mock_api_client):
    """Test retrieving a message that does not exist."""
    # Mock API 404 error response with MessageNotFoundError
    mock_api_client.request.side_effect = MessageNotFoundError(
        id="non-existent",
        message="Message not found."
    )

    # Assertions
    with pytest.raises(MessageNotFoundError, match="Message not found."):
        messages.get_message(message_id="non-existent")


def test_get_message_unauthorized(messages, mock_api_client):
    """
    Test unauthorized access when retrieving a message.
    """
    mock_api_client.request.side_effect = UnauthorizedError("Unauthorized access.")

    with pytest.raises(UnauthorizedError, match="Unauthorized access."):
        messages.get_message("msg123")
