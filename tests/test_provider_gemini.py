import base64

import pytest

from image_creator.providers.common import ProviderError
from image_creator.providers.gemini import GeminiProvider


def test_parse_generate_content_response_extracts_inline_data():
    payload = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": "done"},
                        {
                            "inlineData": {
                                "mimeType": "image/png",
                                "data": base64.b64encode(b"png-bytes").decode(),
                            }
                        },
                    ]
                }
            }
        ]
    }

    result = GeminiProvider.parse_generate_content_response(payload, "gemini-3.1-flash-image-preview")

    assert result.data == b"png-bytes"
    assert result.mime_type == "image/png"
    assert result.model == "gemini-3.1-flash-image-preview"


def test_parse_generate_content_response_requires_image():
    payload = {"candidates": [{"content": {"parts": [{"text": "only text"}]}}]}

    with pytest.raises(ProviderError):
        GeminiProvider.parse_generate_content_response(payload, "gemini-3.1-flash-image-preview")
