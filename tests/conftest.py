import pytest
from src.sdk.client import ApiClient
from src.sdk.features.contacts import Contacts
from src.sdk.features.messages import Messages
from unittest.mock import patch


@pytest.fixture
def mock_api_client():
    """
    Fixture to provide a customizable mocked ApiClient.

    Returns:
        MagicMock: A fully customized mocked ApiClient instance.
    """
    with patch("src.sdk.client.ApiClient") as MockApiClient:
        mock_client = MockApiClient.return_value
        mock_client.request.return_value = {"success": True}  # Default response
        yield mock_client


@pytest.fixture
def mock_client(mocker):
    """
    Fixture to provide an ApiClient instance with the 'request' method patched.

    Args:
        mocker: Pytest-mock fixture for patching.

    Returns:
        ApiClient: A real ApiClient instance with 'request' method mocked.
    """
    client = ApiClient()
    mocker.patch.object(client, "request")
    return client


@pytest.fixture
def contacts(mock_api_client):
    """
    Fixture to provide a Contacts instance with a mocked ApiClient.

    Args:
        mock_api_client (MagicMock): Mocked ApiClient instance.

    Returns:
        Contacts: A Contacts instance using the mocked ApiClient.
    """
    return Contacts(client=mock_api_client)


@pytest.fixture
def messages(mock_api_client):
    """
    Fixture to provide a Messages instance with a mocked ApiClient.

    Args:
        mock_api_client (MagicMock): Mocked ApiClient instance.

    Returns:
        Messages: A Messages instance using the mocked ApiClient.
    """
    return Messages(client=mock_api_client)
