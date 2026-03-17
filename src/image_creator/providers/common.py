from __future__ import annotations

import asyncio
import base64
import binascii
import json
from typing import Any

import httpx


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


TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


async def post_json_with_retries(
    *,
    url: str,
    headers: dict[str, str],
    payload: dict[str, object],
    transport: httpx.AsyncBaseTransport | None = None,
    timeout_sec: float = 180.0,
    max_attempts: int = 3,
    retry_delay_sec: float = 0.5,
) -> dict[str, Any]:
    last_error: ProviderError | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout_sec, transport=transport) as client:
                response = await client.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            last_error = ProviderError(
                f"Provider request timed out after attempt {attempt}/{max_attempts}."
            )
            if attempt == max_attempts:
                raise last_error from exc
            await asyncio.sleep(retry_delay_sec * attempt)
            continue

        if response.status_code in TRANSIENT_STATUS_CODES and attempt < max_attempts:
            await asyncio.sleep(retry_delay_sec * attempt)
            continue

        if response.is_error:
            raise ProviderError(
                f"Provider request failed with HTTP {response.status_code}: {response.text[:400]}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise ProviderError(
                f"Provider returned a non-JSON response body: {response.text[:400]}"
            ) from exc

        if not isinstance(body, dict):
            raise ProviderError(f"Provider returned unexpected JSON shape: {summarize_json(body)}")

        return body

    raise last_error or ProviderError("Provider request failed before a response was returned.")
