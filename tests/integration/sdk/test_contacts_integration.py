import pytest
from src.core.exceptions import NotFoundError


def test_create_contact_success(contacts, mock_api_client):
    """Test successfully creating a contact."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Test method
    payload = {"name": "John Doe", "phone": "+123456789"}
    response = contacts.create_contact(payload)

    # Assertions
    mock_api_client.request.assert_called_once_with("POST", "/contacts", json=payload)
    assert response["id"] == "123"
    assert response["name"] == "John Doe"
    assert response["phone"] == "+123456789"


def test_create_contact_invalid_response(contacts, mock_api_client):
    """Test handling of an invalid response from the API."""
    # Mock API response with missing required fields
    mock_api_client.request.return_value = {}

    # Input payload with all required fields
    payload = {"name": "John Doe", "phone": "+123456789"}

    # Ensure the method raises a validation error for the response payload
    with pytest.raises(ValueError, match="Invalid response"):
        contacts.create_contact(payload)


def test_create_contact_missing_fields(contacts, mock_api_client):
    """
    Test creating a contact with missing required fields.

    - The payload validation should fail.
    - The `request` method of the mocked client should never be called.
    """
    # Invalid payload (missing required 'phone')
    invalid_payload = {"name": "John Doe"}

    # Expect ValidationError when the payload is validated
    with pytest.raises(ValueError, match="Invalid payload"):
        contacts.create_contact(payload=invalid_payload)

    # Assert that no request was made
    mock_api_client.request.assert_not_called()


def test_list_contacts_success(contacts, mock_api_client):
    """Test successfully listing contacts."""
    # Mock API response
    mock_api_client.request.return_value = {
        "contactsList": [
            {"id": "123", "name": "John Doe", "phone": "+123456789"},
            {"id": "124", "name": "Jane Doe", "phone": "+987654321"}
        ],
        "pageNumber": 1,
        "pageSize": 2
    }

    # Test method
    response = contacts.list_contacts(page=1, max=2)

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", "/contacts", params={"pageIndex": 1, "max": 2})
    assert len(response["contactsList"]) == 2
    assert response["contactsList"][0]["id"] == "123"


def test_get_contact_success(contacts, mock_api_client):
    """Test successfully retrieving a specific contact."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Test method
    contact_id = "123"
    response = contacts.get_contact(contact_id)

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", f"/contacts/{contact_id}")
    assert response["id"] == "123"
    assert response["name"] == "John Doe"


def test_get_contact_not_found(contacts, mock_api_client):
    """Test retrieving a non-existent contact."""
    # Mock 404 error
    mock_api_client.request.side_effect = NotFoundError("Resource not found.")

    # Test method
    contact_id = "non-existent"
    with pytest.raises(NotFoundError, match="Resource not found."):
        contacts.get_contact(contact_id)


def test_update_contact_success(contacts, mock_api_client):
    """Test successfully updating a contact."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "Jane Doe", "phone": "+987654321"}

    # Test method
    contact_id = "123"
    payload = {"name": "Jane Doe", "phone": "+987654321"}
    response = contacts.update_contact(contact_id, payload)

    # Assertions
    mock_api_client.request.assert_called_once_with("PATCH", f"/contacts/{contact_id}", json=payload)
    assert response["id"] == "123"
    assert response["name"] == "Jane Doe"


def test_update_contact_not_found(contacts, mock_api_client):
    """Test updating a non-existent contact."""
    # Mock 404 error
    mock_api_client.request.side_effect = NotFoundError("Resource not found.")

    # Test method
    contact_id = "non-existent"
    payload = {"name": "Jane Doe", "phone": "+987654321"}

    with pytest.raises(NotFoundError, match="Resource not found."):
        contacts.update_contact(contact_id, payload)


def test_delete_contact_success(contacts, mock_api_client):
    """Test successfully deleting a contact."""
    # No response body expected for successful deletion
    mock_api_client.request.return_value = None

    # Test method
    contact_id = "123"
    contacts.delete_contact(contact_id)

    # Assertions
    mock_api_client.request.assert_called_once_with("DELETE", f"/contacts/{contact_id}")


def test_delete_contact_not_found(contacts, mock_api_client):
    """Test deleting a non-existent contact."""
    # Mock 404 error
    mock_api_client.request.side_effect = NotFoundError("Resource not found.")

    # Test method
    contact_id = "non-existent"
    with pytest.raises(NotFoundError, match="Resource not found."):
        contacts.delete_contact(contact_id)
