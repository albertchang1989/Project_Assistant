import base64
import hashlib
import hmac
import urllib.parse

from work_assistant.dingtalk.security import verify_dingtalk_signature


def build_signature(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
    return urllib.parse.quote_plus(base64.b64encode(digest))


def build_decoded_signature(timestamp: str, secret: str) -> str:
    return urllib.parse.unquote_plus(build_signature(timestamp, secret))


def test_verify_dingtalk_signature_accepts_valid_signature():
    timestamp = "1710000000000"
    secret = "test-secret"
    sign = build_decoded_signature(timestamp, secret)

    assert verify_dingtalk_signature(timestamp, sign, secret, now_ms=1710000001000) is True


def test_verify_dingtalk_signature_rejects_invalid_signature():
    assert (
        verify_dingtalk_signature(
            "1710000000000", "bad-sign", "test-secret", now_ms=1710000001000
        )
        is False
    )


def test_verify_dingtalk_signature_allows_empty_secret():
    assert verify_dingtalk_signature("", "", "") is True


def test_verify_dingtalk_signature_rejects_stale_timestamp():
    timestamp = "1710000000000"
    secret = "test-secret"
    sign = build_decoded_signature(timestamp, secret)

    assert verify_dingtalk_signature(timestamp, sign, secret, now_ms=1710007200001) is False
