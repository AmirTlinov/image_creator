from __future__ import annotations

from collections.abc import Sequence

import httpx

from image_creator.contracts import ProviderImage
from image_creator.image_io import LocalImageInput, ReferenceImageInput
from image_creator.prompting import compose_image_instruction
from image_creator.providers.common import (
    ProviderError,
    decode_data_url,
    post_json_with_retries,
    summarize_json,
)


class OpenRouterProvider:
    name = "openrouter"
    default_model = "google/gemini-3.1-flash-image-preview"
    base_url = "https://openrouter.ai/api/v1"
    model_aliases = {
        "google/gemini-3.1-flash-preview-image": "google/gemini-3.1-flash-image-preview",
        "google/gemini-2.5-flash-image-preview": "google/gemini-2.5-flash-image",
        "google/gemini-2.5-flash-preview-image": "google/gemini-2.5-flash-image",
        "nano-banana": "google/gemini-2.5-flash-image",
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
    def parse_chat_response(body: dict[str, object], model: str) -> ProviderImage:
        choices = body.get("choices") or []
        if not choices:
            raise ProviderError(f"OpenRouter response has no choices: {summarize_json(body)}")
        if not isinstance(choices, list) or not isinstance(choices[0], dict):
            raise ProviderError(f"OpenRouter response has invalid choices payload: {summarize_json(body)}")

        message = choices[0].get("message") or {}
        if not isinstance(message, dict):
            raise ProviderError(f"OpenRouter response has invalid message payload: {summarize_json(body)}")
        images = message.get("images") or []
        if not isinstance(images, list) or not images:
            raise ProviderError(f"OpenRouter response has no images: {summarize_json(body)}")
        if not isinstance(images[0], dict):
            raise ProviderError(f"OpenRouter response has invalid image payload: {summarize_json(body)}")

        image = images[0]
        image_url = image.get("image_url") or image.get("imageUrl") or {}
        if not isinstance(image_url, dict):
            raise ProviderError(f"OpenRouter image payload is invalid: {summarize_json(body)}")
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
        negative_prompt: str | None = None,
        reference_images: Sequence[ReferenceImageInput] = (),
        background_mode: str | None = None,
        output_format: str | None = None,
        quality_level: str | None = None,
    ) -> ProviderImage:
        if not self.api_key:
            raise ProviderError("OPENROUTER_API_KEY is not configured.")

        chosen_model = self.normalize_model(model)
        composed_prompt = compose_image_instruction(
            prompt=prompt,
            negative_prompt=negative_prompt,
            reference_images=reference_images,
            include_editable_base_image=False,
        )

        if reference_images:
            content_parts: list[dict[str, object]] = [{"type": "text", "text": composed_prompt}]
            content_parts.extend(
                {
                    "type": "image_url",
                    "image_url": {"url": reference_image.to_data_url()},
                }
                for reference_image in reference_images
            )
            content: str | list[dict[str, object]] = content_parts
        else:
            content = composed_prompt

        payload: dict[str, object] = {
            "model": chosen_model,
            "messages": [{"role": "user", "content": content}],
            "modalities": ["image", "text"],
            "stream": False,
        }

        if chosen_model.startswith("openai/gpt-5-image"):
            if background_mode:
                payload["background"] = background_mode
            if output_format:
                payload["output_format"] = output_format
            if quality_level:
                payload["quality"] = quality_level

        image_config: dict[str, str] = {}
        if aspect_ratio:
            image_config["aspect_ratio"] = aspect_ratio
        if image_size:
            image_config["image_size"] = image_size
        if image_config:
            payload["image_config"] = image_config

        body = await post_json_with_retries(
            url=f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            transport=self.transport,
            max_attempts=self.max_attempts,
            retry_delay_sec=self.retry_delay_sec,
        )
        return self.parse_chat_response(body, chosen_model)

    async def edit(
        self,
        *,
        source_image: LocalImageInput,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
        negative_prompt: str | None = None,
        reference_images: Sequence[ReferenceImageInput] = (),
        background_mode: str | None = None,
        output_format: str | None = None,
        quality_level: str | None = None,
    ) -> ProviderImage:
        if not self.api_key:
            raise ProviderError("OPENROUTER_API_KEY is not configured.")

        chosen_model = self.normalize_model(model)
        content: list[dict[str, object]] = [
            {
                "type": "text",
                "text": compose_image_instruction(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    reference_images=reference_images,
                    include_editable_base_image=True,
                ),
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": source_image.to_data_url(),
                },
            },
        ]
        content.extend(
            {
                "type": "image_url",
                "image_url": {
                    "url": reference_image.to_data_url(),
                },
            }
            for reference_image in reference_images
        )
        payload: dict[str, object] = {
            "model": chosen_model,
            "messages": [
                {
                    "role": "user",
                    "content": content,
                }
            ],
            "modalities": ["image", "text"],
            "stream": False,
        }

        if chosen_model.startswith("openai/gpt-5-image"):
            if background_mode:
                payload["background"] = background_mode
            if output_format:
                payload["output_format"] = output_format
            if quality_level:
                payload["quality"] = quality_level

        image_config: dict[str, str] = {}
        if aspect_ratio:
            image_config["aspect_ratio"] = aspect_ratio
        if image_size:
            image_config["image_size"] = image_size
        if image_config:
            payload["image_config"] = image_config

        body = await post_json_with_retries(
            url=f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            transport=self.transport,
            max_attempts=self.max_attempts,
            retry_delay_sec=self.retry_delay_sec,
        )
        return self.parse_chat_response(body, chosen_model)
