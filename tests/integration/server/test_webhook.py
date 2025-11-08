import json
from fastapi.testclient import TestClient
from src.core.config import settings
from src.server.app import app
from src.core.security import generate_signature

client = TestClient(app)


def test_integration_webhook_processing():
    """
    Integration test for webhook processing.
    Verifies the full request-response lifecycle.
    """
    # Arrange: Prepare payload and signature
    payload = {
        "id": "msg123",
        "status": "delivered",
        "deliveredAt": "2024-12-01T12:00:00Z",
    }
    # Generate a valid signature
    signature = generate_signature(payload, settings.WEBHOOK_SECRET)

    # Act: Make the POST request to the webhook endpoint
    response = client.post(
        "/webhooks",
        json=payload,  # Send payload as JSON
        headers={"Authorization": f"Bearer {signature}"}
    )

    # Assert: Validate the response
    assert response.status_code == 200
    assert response.json() == {"message": "Webhook processed successfully."}
