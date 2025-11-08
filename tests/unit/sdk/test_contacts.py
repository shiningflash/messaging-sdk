import pytest
from src.core.exceptions import ApiError, ContactNotFoundError


def test_create_contact_success(contacts, mock_api_client):
    """Test creating a contact successfully."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Input payload
    payload = {"name": "John Doe", "phone": "+123456789"}

    # Call method
    response = contacts.create_contact(payload=payload)

    # Assertions
    mock_api_client.request.assert_called_once_with("POST", "/contacts", json=payload)
    assert response["id"] == "123"
    assert response["name"] == "John Doe"
    assert response["phone"] == "+123456789"


def test_create_contact_validation_error(contacts):
    """Test validation error when creating a contact with invalid data."""
    # Missing 'phone' in payload
    payload = {"name": "John Doe"}

    # Assertions
    with pytest.raises(ValueError, match="Invalid payload"):
        contacts.create_contact(payload=payload)


def test_create_contact_api_error(contacts, mock_api_client):
    """Test API error during contact creation."""
    # Mock API error
    mock_api_client.request.side_effect = ApiError("Unhandled API Error")

    # Input payload
    payload = {"name": "John Doe", "phone": "+123456789"}

    # Assertions
    with pytest.raises(ApiError, match="Unhandled API Error"):
        contacts.create_contact(payload=payload)


def test_list_contacts_success(contacts, mock_api_client):
    """Test listing contacts successfully with pagination."""
    # Mock API response
    mock_api_client.request.return_value = {
        "contactsList": [{"id": "123", "name": "John Doe", "phone": "+123456789"}],
        "pageNumber": 1,
        "pageSize": 10,
    }

    # Call method
    response = contacts.list_contacts(page=1, max=10)

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", "/contacts", params={"pageIndex": 1, "max": 10})
    assert response["pageNumber"] == 1
    assert len(response["contactsList"]) == 1
    assert response["contactsList"][0]["id"] == "123"
    assert response["contactsList"][0]["name"] == "John Doe"


def test_get_contact_success(contacts, mock_api_client):
    """Test retrieving a contact successfully by ID."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Call method
    response = contacts.get_contact(contact_id="123")

    # Assertions
    mock_api_client.request.assert_called_once_with("GET", "/contacts/123")
    assert response["id"] == "123"
    assert response["name"] == "John Doe"
    assert response["phone"] == "+123456789"


def test_update_contact_success(contacts, mock_api_client):
    """Test updating a contact successfully."""
    # Mock API response
    mock_api_client.request.return_value = {"id": "123", "name": "Jane Doe", "phone": "+987654321"}

    # Input payload
    payload = {"name": "Jane Doe", "phone": "+987654321"}

    # Call method
    response = contacts.update_contact(contact_id="123", payload=payload)

    # Assertions
    mock_api_client.request.assert_called_once_with("PATCH", "/contacts/123", json=payload)
    assert response["id"] == "123"
    assert response["name"] == "Jane Doe"
    assert response["phone"] == "+987654321"


def test_delete_contact_success(contacts, mock_api_client):
    """Test deleting a contact successfully."""
    # Call method
    contacts.delete_contact(contact_id="123")

    # Assertions
    mock_api_client.request.assert_called_once_with("DELETE", "/contacts/123")


def test_get_contact_not_found(contacts, mock_api_client):
    """Test retrieving a contact that does not exist."""
    # Mock API 404 error response with ContactNotFoundError
    mock_api_client.request.side_effect = ContactNotFoundError(
        id="non-existent",
        message="Contact not found."
    )

    # Assertions
    with pytest.raises(ContactNotFoundError, match="Contact not found."):
        contacts.get_contact(contact_id="non-existent")


def test_delete_contact_not_found(contacts, mock_api_client):
    """Test deleting a contact that does not exist."""
    # Mock API 404 error response with ContactNotFoundError
    mock_api_client.request.side_effect = ContactNotFoundError(
        id="non-existent",
        message="Contact not found."
    )

    # Assertions
    with pytest.raises(ContactNotFoundError, match="Contact not found."):
        contacts.delete_contact(contact_id="non-existent")
