import pytest
import hmac
import hashlib
import json

from src.core.config import settings
from src.core.security import verify_signature
from src.core.security import generate_signature
from src.schemas.errors import UnauthorizedError


def test_valid_signature():
    payload = {"id": "msg123", "status": "delivered"}
    serialized_payload = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = generate_signature(payload, settings.WEBHOOK_SECRET)
    assert verify_signature(serialized_payload, signature, settings.WEBHOOK_SECRET) is True

def test_invalid_signature():
    payload = {"id": "msg123", "status": "delivered"}
    serialized_payload = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    invalid_signature = "invalidsignature"

    with pytest.raises(UnauthorizedError, match="Unauthorized: Signature validation failed."):
        verify_signature(serialized_payload, invalid_signature, settings.WEBHOOK_SECRET)

def test_empty_signature():
    payload = {"id": "msg123", "status": "delivered"}
    serialized_payload = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    empty_signature = ""

    with pytest.raises(UnauthorizedError, match="Unauthorized: Signature validation failed."):
        verify_signature(serialized_payload, empty_signature, settings.WEBHOOK_SECRET)

