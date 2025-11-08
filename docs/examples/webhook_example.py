import hmac
import hashlib
import os
import json
from core.logger import logger

"""
Run with: uvicorn src.server.app:app --reload --port 3010
"""

def generate_hmac_signature(payload: str, secret: str) -> str:
    """
    Generate HMAC signature for the payload using the given secret.
    Args:
        payload (str): JSON string of the payload.
        secret (str): Webhook secret key.
    Returns:
        str: Generated HMAC signature as a hexadecimal string.
    """
    logger.info("Generating HMAC signature...")
    try:
        message = payload.encode("utf-8")
        secret_key = secret.encode("utf-8")
        hmac_instance = hmac.new(secret_key, message, hashlib.sha256)
        return hmac_instance.hexdigest()
    except Exception as e:
        logger.error(f"Error generating HMAC signature: {e}")
        raise

def trigger_webhook_example():
    """
    Simulate sending a webhook POST request with a valid HMAC signature.
    """
    try:
        # Define secret and payload
        secret = "mySecret"
        payload = {
            "id": "msg123",
            "status": "delivered",
            "deliveredAt": "2024-11-30T12:00:00Z"
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload, separators=(",", ":"))

        # Generate HMAC signature
        signature = generate_hmac_signature(payload_json, secret)

        # Prepare the cURL command
        command = (
            f'curl -X POST http://localhost:3010/webhooks '
            f'-H "Authorization: Bearer {signature}" '
            f'-H "Content-Type: application/json" '
            f'-d \'{payload_json}\''
        )

        # Simulate the webhook
        logger.info("Simulating webhook request...")
        response = os.popen(command).read()
        logger.info(f"Webhook response: {response}")
        print("Webhook response:")
        print(response)

    except Exception as e:
        logger.error(f"An error occurred while triggering the webhook: {e}")

if __name__ == "__main__":
    trigger_webhook_example()
