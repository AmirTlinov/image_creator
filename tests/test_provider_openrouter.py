import base64

import pytest

from image_creator.providers.common import ProviderError, decode_data_url
from image_creator.providers.openrouter import OpenRouterProvider


def test_decode_data_url_returns_bytes_and_mime():
    encoded = base64.b64encode(b"jpeg-bytes").decode()

    data, mime_type = decode_data_url(f"data:image/jpeg;base64,{encoded}")

    assert data == b"jpeg-bytes"
    assert mime_type == "image/jpeg"


def test_parse_chat_response_extracts_first_image():
    encoded = base64.b64encode(b"png-bytes").decode()
    payload = {
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
    }

    result = OpenRouterProvider.parse_chat_response(payload, "google/gemini-3.1-flash-image-preview")

    assert result.data == b"png-bytes"
    assert result.mime_type == "image/png"
    assert result.model == "google/gemini-3.1-flash-image-preview"


def test_parse_chat_response_requires_images():
    payload = {"choices": [{"message": {"content": "no image"}}]}

    with pytest.raises(ProviderError):
        OpenRouterProvider.parse_chat_response(payload, "google/gemini-3.1-flash-image-preview")


def test_normalize_model_maps_old_preview_alias_to_working_model():
    assert (
        OpenRouterProvider.normalize_model("google/gemini-3.1-flash-preview-image")
        == "google/gemini-3.1-flash-image-preview"
    )


def test_normalize_model_keeps_old_2_5_alias_on_stable_2_5_model():
    assert (
        OpenRouterProvider.normalize_model("google/gemini-2.5-flash-image-preview")
        == "google/gemini-2.5-flash-image"
    )
