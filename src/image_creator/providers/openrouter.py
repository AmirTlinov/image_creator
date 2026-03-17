from __future__ import annotations

import httpx

from image_creator.contracts import ProviderImage
from image_creator.providers.common import ProviderError, decode_data_url, summarize_json


class OpenRouterProvider:
    name = "openrouter"
    default_model = "google/gemini-2.5-flash-image"
    base_url = "https://openrouter.ai/api/v1"
    model_aliases = {
        "google/gemini-2.5-flash-image-preview": "google/gemini-2.5-flash-image",
        "google/gemini-2.5-flash-preview-image": "google/gemini-2.5-flash-image",
        "nano-banana": "google/gemini-2.5-flash-image",
    }

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    @classmethod
    def normalize_model(cls, model: str | None) -> str:
        if not model:
            return cls.default_model
        return cls.model_aliases.get(model.strip(), model.strip())

    @staticmethod
    def parse_chat_response(body: dict, model: str) -> ProviderImage:
        choices = body.get("choices") or []
        if not choices:
            raise ProviderError(f"OpenRouter response has no choices: {summarize_json(body)}")

        message = choices[0].get("message") or {}
        images = message.get("images") or []
        if not images:
            raise ProviderError(f"OpenRouter response has no images: {summarize_json(body)}")

        image = images[0]
        image_url = image.get("image_url") or image.get("imageUrl") or {}
        url = image_url.get("url")
        if not url:
            raise ProviderError(f"OpenRouter image payload is missing url: {summarize_json(body)}")

        data, mime_type = decode_data_url(url)
        return ProviderImage(data=data, mime_type=mime_type, model=model)

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
    ) -> ProviderImage:
        if not self.api_key:
            raise ProviderError("OPENROUTER_API_KEY is not configured.")

        chosen_model = self.normalize_model(model)
        payload: dict[str, object] = {
            "model": chosen_model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "stream": False,
        }

        image_config: dict[str, str] = {}
        if aspect_ratio:
            image_config["aspect_ratio"] = aspect_ratio
        if image_size:
            image_config["image_size"] = image_size
        if image_config:
            payload["image_config"] = image_config

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        if response.is_error:
            raise ProviderError(
                f"OpenRouter request failed with HTTP {response.status_code}: {response.text[:400]}"
            )

        return self.parse_chat_response(response.json(), chosen_model)
