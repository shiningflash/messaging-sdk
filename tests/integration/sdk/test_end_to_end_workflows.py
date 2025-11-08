import pytest


def test_send_and_check_message_workflow(messages, mock_api_client):
    """
    Test the end-to-end workflow of sending a message and verifying its status.
    """
    # Step 1: Send a message
    send_payload = {
        "to": {"id": "contact123"},  # Align with ContactID schema
        "content": "Hello, World!",
        "from": "+987654321"  # Use the correct field
    }
    sent_message_response = {
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
    mock_api_client.request.return_value = sent_message_response

    # Send the message
    sent_message = messages.send_message(payload=send_payload)
    assert sent_message == sent_message_response, "Message sending failed."

    # Step 2: Check the status of the message
    mock_api_client.request.return_value = sent_message_response
    retrieved_message = messages.get_message(message_id="msg123")
    assert retrieved_message == sent_message_response, "Failed to retrieve the sent message."

    # Ensure the API was called as expected
    mock_api_client.request.assert_any_call("POST", "/messages", json=send_payload)
    mock_api_client.request.assert_any_call("GET", "/messages/msg123")


def test_list_contacts_and_messages_workflow(contacts, messages, mock_api_client):
    """
    Test the workflow of listing contacts and messages.
    """
    # Step 1: Mock the response for listing contacts
    contacts_list_response = {
        "contactsList": [
            {"id": "contact1", "name": "Alice", "phone": "+111111111"},
            {"id": "contact2", "name": "Bob", "phone": "+222222222"},
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "total": 2,
    }
    mock_api_client.request.return_value = contacts_list_response

    # Call the list_contacts method
    contacts_list = contacts.list_contacts()
    assert contacts_list == contacts_list_response, "Failed to list contacts."

    # Assert the API call was made with correct parameters
    mock_api_client.request.assert_called_once_with(
        "GET", "/contacts", params={"pageIndex": 1, "max": 10}
    )

    # Step 2: Mock the response for listing messages
    messages_list_response = {
        "messages": [
            {
                "id": "msg123",
                "to": "+123456789",
                "from": "+987654321",
                "content": "Hello, World!",
                "status": "delivered",
                "createdAt": "2024-12-01T00:00:00Z",
            }
        ],
        "page": 1,
        "quantityPerPage": 10,
        "total": 1,
    }
    mock_api_client.request.return_value = messages_list_response

    # Call the list_messages method
    messages_list = messages.list_messages()
    assert messages_list == messages_list_response, "Failed to list messages."

    # Assert the API call was made with correct parameters
    mock_api_client.request.assert_called_with(
        "GET", "/messages", params={"page": 1, "limit": 10}
    )


def test_delete_contact_and_verify(contacts, mock_api_client):
    """
    Test the workflow of deleting a contact and verifying the deletion.
    """
    # Step 1: Mock the API response for deleting a contact
    contact_id = "contact123"
    mock_api_client.request.return_value = None  # Simulate DELETE response (typically no content)

    # Step 2: Call the delete_contact method
    contacts.delete_contact(contact_id=contact_id)

    # Step 3: Verify the API call was made with the correct parameters
    mock_api_client.request.assert_called_once_with("DELETE", f"/contacts/{contact_id}")
