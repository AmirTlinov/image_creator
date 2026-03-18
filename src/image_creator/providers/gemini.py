from __future__ import annotations

import base64

import httpx

from image_creator.contracts import ProviderImage
from image_creator.image_io import LocalImageInput
from image_creator.providers.common import ProviderError, post_json_with_retries, summarize_json


class GeminiProvider:
    name = "gemini"
    default_model = "gemini-2.5-flash-image"
    base_url = "https://generativelanguage.googleapis.com/v1beta"
    model_aliases = {
        "gemini-2.5-flash-image-preview": "gemini-2.5-flash-image",
        "nano-banana": "gemini-2.5-flash-image",
    }

    def __init__(
        self,
        api_key: str | None,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
        max_attempts: int = 3,
        retry_delay_sec: float = 0.5,
    ) -> None:
        self.api_key = api_key
        self.transport = transport
        self.max_attempts = max_attempts
        self.retry_delay_sec = retry_delay_sec

    @classmethod
    def normalize_model(cls, model: str | None) -> str:
        if not model:
            return cls.default_model
        return cls.model_aliases.get(model.strip(), model.strip())

    @staticmethod
    def parse_generate_content_response(body: dict[str, object], model: str) -> ProviderImage:
        candidates = body.get("candidates") or []
        if not isinstance(candidates, list) or not candidates:
            raise ProviderError(f"Gemini response has no candidates: {summarize_json(body)}")
        if not isinstance(candidates[0], dict):
            raise ProviderError(f"Gemini response has invalid candidate payload: {summarize_json(body)}")

        parts = ((candidates[0].get("content") or {}).get("parts")) or []
        if not isinstance(parts, list):
            raise ProviderError(f"Gemini response has invalid parts payload: {summarize_json(body)}")
        for part in parts:
            if not isinstance(part, dict):
                continue
            inline_data = part.get("inlineData") or part.get("inline_data")
            if isinstance(inline_data, dict) and inline_data.get("data"):
                mime_type = inline_data.get("mimeType") or inline_data.get("mime_type") or "image/png"
                return ProviderImage(
                    data=base64.b64decode(inline_data["data"]),
                    mime_type=mime_type,
                    model=model,
                )

        raise ProviderError(f"Gemini response does not contain image bytes: {summarize_json(body)}")

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
    ) -> ProviderImage:
        if not self.api_key:
            raise ProviderError("GEMINI_API_KEY is not configured.")

        chosen_model = self.normalize_model(model)
        generation_config: dict[str, object] = {"responseModalities": ["Image"]}

        image_config: dict[str, str] = {}
        if aspect_ratio:
            image_config["aspectRatio"] = aspect_ratio
        if image_size:
            image_config["imageSize"] = image_size
        if image_config:
            generation_config["imageConfig"] = image_config

        payload: dict[str, object] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }

        body = await post_json_with_retries(
            url=f"{self.base_url}/models/{chosen_model}:generateContent",
            headers={
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
            },
            payload=payload,
            transport=self.transport,
            max_attempts=self.max_attempts,
            retry_delay_sec=self.retry_delay_sec,
        )
        return self.parse_generate_content_response(body, chosen_model)

    async def edit(
        self,
        *,
        source_image: LocalImageInput,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
    ) -> ProviderImage:
        if not self.api_key:
            raise ProviderError("GEMINI_API_KEY is not configured.")

        chosen_model = self.normalize_model(model)
        generation_config: dict[str, object] = {"responseModalities": ["Image"]}

        image_config: dict[str, str] = {}
        if aspect_ratio:
            image_config["aspectRatio"] = aspect_ratio
        if image_size:
            image_config["imageSize"] = image_size
        if image_config:
            generation_config["imageConfig"] = image_config

        payload: dict[str, object] = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {"inline_data": source_image.to_gemini_inline_data()},
                    ]
                }
            ],
            "generationConfig": generation_config,
        }

        body = await post_json_with_retries(
            url=f"{self.base_url}/models/{chosen_model}:generateContent",
            headers={
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
            },
            payload=payload,
            transport=self.transport,
            max_attempts=self.max_attempts,
            retry_delay_sec=self.retry_delay_sec,
        )
        return self.parse_generate_content_response(body, chosen_model)
