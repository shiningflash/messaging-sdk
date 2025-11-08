import os
import sys
from random import randint

# Ensure SDK is in the Python path
sys.path.append(os.path.join(os.path.curdir, "../messaging-sdk"))

from sdk.features.messages import Messages
from sdk.features.contacts import Contacts
from sdk.client import ApiClient
from core.logger import logger

def send_message_example(messages):
    """Send a message and handle the response."""
    payload = {
        "to": {"id": "f5469d44-c405-4de4-ac4c-d8ef26a22bee"},  # Give a proper Contact ID
        "content": "Hello, world!",  # Message content
        "from": "+9876543210"  # Sender's phone number
    }
    try:
        logger.info("Attempting to send a message...")
        response = messages.send_message(payload=payload)
        logger.info(f"Message sent successfully: {response}")
        print("Message sent successfully:")
        print(response)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

def manage_contacts_example(contacts):
    """Demonstrate creating, listing, and deleting a contact."""
    try:
        # Create a new contact
        new_contact = {
            "name": 'Contact Name',  # Give the contact name
            "phone": f"+{randint(10**9, 10**10-1)}"
        }
        logger.info("Creating a new contact...")
        response = contacts.create_contact(new_contact)
        logger.info(f"Contact created successfully: {response}")
        print("Contact created successfully:")
        print(response)

        # List all contacts
        logger.info("Listing all contacts...")
        contacts_list = contacts.list_contacts()
        logger.info(f"Retrieved contacts: {contacts_list}")
        print("Contacts list:")
        print(contacts_list)

        # Delete the created contact
        contact_id = response["id"]
        logger.info(f"Deleting contact with ID: {contact_id}")
        contacts.delete_contact(contact_id)
        logger.info(f"Contact with ID {contact_id} deleted successfully.")
        print(f"Contact with ID {contact_id} deleted successfully.")

    except Exception as e:
        logger.error(f"An error occurred while managing contacts: {e}")


def main():
    # Initialize API client and SDK components
    client = ApiClient()
    messages = Messages(client=client)
    contacts = Contacts(client=client)

    try:
        # Send a message example
        send_message_example(messages)

        # List, create, and delete contacts example
        manage_contacts_example(contacts)

    except Exception as e:
        logger.error(f"An error occurred during the main workflow: {e}")

if __name__ == "__main__":
    main()
