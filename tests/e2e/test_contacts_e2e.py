import pytest


@pytest.mark.e2e
def test_create_and_retrieve_contact(mock_api_client, contacts):
    """
    E2E Test: Create a contact and then retrieve it to verify it was saved correctly.
    """
    # Mock the API response for creating a contact
    create_response = {
        "id": "contact123",
        "name": "John Doe",
        "phone": "+123456789",
    }
    mock_api_client.request.return_value = create_response

    # Step 1: Create a contact
    contact_payload = {"name": "John Doe", "phone": "+123456789"}
    created_contact = contacts.create_contact(contact_payload)
    assert created_contact == create_response, "Failed to create contact."

    # Mock the API response for retrieving the contact
    retrieve_response = {
        "id": "contact123",
        "name": "John Doe",
        "phone": "+123456789",
    }
    mock_api_client.request.return_value = retrieve_response

    # Step 2: Retrieve the contact
    retrieved_contact = contacts.get_contact(contact_id="contact123")
    assert retrieved_contact == retrieve_response, "Failed to retrieve contact."

    # Ensure API calls were made as expected
    mock_api_client.request.assert_any_call("POST", "/contacts", json=contact_payload)
    mock_api_client.request.assert_any_call("GET", "/contacts/contact123")


@pytest.mark.e2e
def test_update_contact_and_verify(mock_api_client, contacts):
    """
    E2E Test: Update a contact and verify the updated details.
    """
    # Mock the API response for updating the contact
    update_response = {
        "id": "contact123",
        "name": "Johnathan Doe",
        "phone": "+987654321",
    }
    mock_api_client.request.return_value = update_response

    # Step 1: Update the contact
    update_payload = {"name": "Johnathan Doe", "phone": "+987654321"}
    updated_contact = contacts.update_contact(contact_id="contact123", payload=update_payload)
    assert updated_contact == update_response, "Failed to update contact."

    # Mock the API response for retrieving the updated contact
    retrieve_response = {
        "id": "contact123",
        "name": "Johnathan Doe",
        "phone": "+987654321",
    }
    mock_api_client.request.return_value = retrieve_response

    # Step 2: Retrieve the updated contact
    retrieved_contact = contacts.get_contact(contact_id="contact123")
    assert retrieved_contact == retrieve_response, "Failed to verify updated contact."

    # Ensure API calls were made as expected
    mock_api_client.request.assert_any_call("PATCH", "/contacts/contact123", json=update_payload)
    mock_api_client.request.assert_any_call("GET", "/contacts/contact123")


@pytest.mark.e2e
def test_delete_contact_and_handle_absence(mock_api_client, contacts):
    """
    E2E Test: Delete a contact and verify it cannot be retrieved afterward.
    """
    # Mock the API response for deleting the contact
    mock_api_client.request.return_value = {"success": True}

    # Step 1: Delete the contact
    contact_id = "contact123"
    delete_response = contacts.delete_contact(contact_id=contact_id)
    assert delete_response == None

    # Mock the API response for attempting to retrieve the deleted contact
    mock_api_client.request.side_effect = RuntimeError("Contact not found")

    # Step 2: Attempt to retrieve the deleted contact
    with pytest.raises(RuntimeError, match="Contact not found"):
        contacts.get_contact(contact_id=contact_id)

    # Ensure API calls were made as expected
    mock_api_client.request.assert_any_call("DELETE", f"/contacts/{contact_id}")
    mock_api_client.request.assert_any_call("GET", f"/contacts/{contact_id}")


@pytest.mark.e2e
def test_list_contacts_with_pagination(mock_api_client, contacts):
    """
    E2E Test: List contacts with pagination and verify the correct data is returned.
    """
    # Mock the API response for listing contacts
    list_response = {
        "contactsList": [
            {"id": "contact1", "name": "Alice", "phone": "+111111111"},
            {"id": "contact2", "name": "Bob", "phone": "+222222222"},
        ],
        "pageNumber": 1,
        "pageSize": 2,
        "total": 5,
    }
    mock_api_client.request.return_value = list_response

    # Step 1: Call the list_contacts method with page and max arguments
    contacts_list = contacts.list_contacts(page=1, max=2)

    # Validate the response
    assert contacts_list == list_response, "Failed to list contacts with pagination."

    # Ensure the API call was made with the correct arguments
    mock_api_client.request.assert_called_once_with(
        "GET",
        "/contacts",
        params={"pageIndex": 1, "max": 2},
    )


@pytest.mark.e2e
def test_create_duplicate_contact_error(mock_api_client, contacts):
    """
    E2E Test: Attempt to create a duplicate contact and verify the correct error is raised.
    """
    # Mock the API response for attempting to create a duplicate contact
    mock_api_client.request.side_effect = RuntimeError("Contact already exists")

    # Step 1: Attempt to create a duplicate contact
    contact_payload = {"name": "John Doe", "phone": "+123456789"}
    with pytest.raises(RuntimeError, match="Contact already exists"):
        contacts.create_contact(contact_payload)

    # Ensure the API call was made as expected
    mock_api_client.request.assert_called_once_with("POST", "/contacts", json=contact_payload)
