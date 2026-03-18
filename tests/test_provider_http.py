from __future__ import annotations

import base64
import json

import httpx
import pytest

from image_creator.providers.common import ProviderError
from image_creator.providers.gemini import GeminiProvider
from image_creator.providers.openrouter import OpenRouterProvider


@pytest.mark.anyio
async def test_openrouter_retries_transient_429_and_then_succeeds() -> None:
    attempts = {"count": 0}
    encoded = base64.b64encode(b"png-bytes").decode()

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(429, json={"error": {"message": "rate limited"}})
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": f"data:image/png;base64,{encoded}",
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
        )

    provider = OpenRouterProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        retry_delay_sec=0.0,
    )

    result = await provider.generate(
        prompt="banana",
        model=None,
        aspect_ratio="1:1",
        image_size=None,
    )

    assert attempts["count"] == 2
    assert result.data == b"png-bytes"


@pytest.mark.anyio
async def test_gemini_raises_after_timeout_budget_is_exhausted() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    provider = GeminiProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        max_attempts=2,
        retry_delay_sec=0.0,
    )

    with pytest.raises(ProviderError, match="timed out"):
        await provider.generate(
            prompt="banana",
            model=None,
            aspect_ratio="1:1",
            image_size=None,
        )


@pytest.mark.anyio
async def test_openrouter_rejects_non_json_response_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text="not-json",
            headers={"content-type": "text/plain"},
        )

    provider = OpenRouterProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        retry_delay_sec=0.0,
    )

    with pytest.raises(ProviderError, match="non-JSON"):
        await provider.generate(
            prompt="banana",
            model=None,
            aspect_ratio="1:1",
            image_size=None,
        )


@pytest.mark.anyio
async def test_openrouter_edit_sends_input_image_as_data_url() -> None:
    encoded = base64.b64encode(b"edited").decode()

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        content = payload["messages"][0]["content"]
        assert content[0]["type"] == "text"
        assert content[1]["type"] == "image_url"
        assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": f"data:image/png;base64,{encoded}",
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
        )

    provider = OpenRouterProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        retry_delay_sec=0.0,
    )

    from image_creator.image_io import LocalImageInput

    result = await provider.edit(
        source_image=LocalImageInput(
            path=__import__("pathlib").Path("/tmp/source.png"),
            mime_type="image/png",
            data=b"source-image",
        ),
        prompt="add sunglasses",
        model=None,
        aspect_ratio="1:1",
        image_size=None,
    )

    assert result.data == b"edited"


@pytest.mark.anyio
async def test_openrouter_generate_sends_reference_images_after_text_part() -> None:
    encoded = base64.b64encode(b"png-bytes").decode()

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        content = payload["messages"][0]["content"]
        assert content[0]["type"] == "text"
        assert "Reference images:" in content[0]["text"]
        assert content[1]["type"] == "image_url"
        assert content[2]["type"] == "image_url"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": f"data:image/png;base64,{encoded}",
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
        )

    from image_creator.image_io import ReferenceImageInput, LocalImageInput

    provider = OpenRouterProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        retry_delay_sec=0.0,
    )

    result = await provider.generate(
        prompt="restyle this",
        model=None,
        aspect_ratio="1:1",
        image_size=None,
        negative_prompt="no watermark",
        reference_images=[
            ReferenceImageInput(
                image=LocalImageInput(
                    path=__import__("pathlib").Path("/tmp/style.png"),
                    mime_type="image/png",
                    data=b"style-image",
                ),
                role="style",
            ),
            ReferenceImageInput(
                image=LocalImageInput(
                    path=__import__("pathlib").Path("/tmp/object.png"),
                    mime_type="image/png",
                    data=b"object-image",
                ),
                role="object",
            ),
        ],
    )

    assert result.data == b"png-bytes"


@pytest.mark.anyio
async def test_gemini_edit_sends_text_base_then_references() -> None:
    encoded = base64.b64encode(b"edited").decode()

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        parts = payload["contents"][0]["parts"]
        assert "Editable base image" in parts[0]["text"]
        assert "Reference images:" in parts[0]["text"]
        assert "inline_data" in parts[1]
        assert "inline_data" in parts[2]
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "inlineData": {
                                        "mimeType": "image/png",
                                        "data": encoded,
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
        )

    from image_creator.image_io import ReferenceImageInput, LocalImageInput

    provider = GeminiProvider(
        api_key="test-key",
        transport=httpx.MockTransport(handler),
        retry_delay_sec=0.0,
    )

    result = await provider.edit(
        source_image=LocalImageInput(
            path=__import__("pathlib").Path("/tmp/base.png"),
            mime_type="image/png",
            data=b"base-image",
        ),
        prompt="add glasses",
        model=None,
        aspect_ratio="1:1",
        image_size=None,
        negative_prompt="no text",
        reference_images=[
            ReferenceImageInput(
                image=LocalImageInput(
                    path=__import__("pathlib").Path("/tmp/style.png"),
                    mime_type="image/png",
                    data=b"style-image",
                ),
                role="style",
            )
        ],
    )

    assert result.data == b"edited"
