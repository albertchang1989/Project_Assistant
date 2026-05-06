import base64
import hashlib
import hmac
import time


def verify_dingtalk_signature(
    timestamp: str,
    sign: str,
    secret: str,
    *,
    now_ms: int | None = None,
    max_age_ms: int = 60 * 60 * 1000,
) -> bool:
    if not secret:
        return True

    try:
        timestamp_ms = int(timestamp)
    except ValueError:
        return False

    current_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    if abs(current_ms - timestamp_ms) > max_age_ms:
        return False

    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(expected, sign)
