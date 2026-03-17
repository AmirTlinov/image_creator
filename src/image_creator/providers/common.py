from __future__ import annotations

import base64
import binascii
import json


class ProviderError(RuntimeError):
    """Provider-specific request or response failure."""


def decode_data_url(data_url: str) -> tuple[bytes, str]:
    if not data_url.startswith("data:"):
        raise ProviderError("Expected image data URL from provider response.")

    try:
        header, encoded = data_url.split(",", 1)
    except ValueError as exc:
        raise ProviderError("Malformed provider data URL.") from exc

    mime_type = header.removeprefix("data:").split(";", 1)[0] or "image/png"

    try:
        return base64.b64decode(encoded), mime_type
    except binascii.Error as exc:
        raise ProviderError("Failed to decode base64 image payload from provider.") from exc


def summarize_json(value: object, limit: int = 600) -> str:
    try:
        rendered = json.dumps(value, ensure_ascii=False)
    except TypeError:
        rendered = repr(value)
    return rendered[:limit]
