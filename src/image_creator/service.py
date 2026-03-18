from __future__ import annotations

from collections.abc import Mapping

from image_creator.config import Settings
from image_creator.contracts import GeneratedImageResult, ProviderImage
from image_creator.image_io import load_local_image
from image_creator.providers import GeminiProvider, OpenRouterProvider
from image_creator.providers.base import ImageProvider
from image_creator.storage import save_image_bytes


def build_providers(settings: Settings) -> dict[str, ImageProvider]:
    return {
        GeminiProvider.name: GeminiProvider(api_key=settings.gemini_api_key),
        OpenRouterProvider.name: OpenRouterProvider(api_key=settings.openrouter_api_key),
    }


def _select_provider(
    provider: str,
    providers: Mapping[str, ImageProvider],
) -> tuple[str, ImageProvider]:
    chosen_provider = provider.strip().lower()
    if chosen_provider not in providers:
        supported = ", ".join(sorted(providers))
        raise ValueError(f"Unsupported provider '{provider}'. Expected one of: {supported}")
    return chosen_provider, providers[chosen_provider]


def _persist_result(
    *,
    provider_image: ProviderImage,
    chosen_provider: str,
    out_dir: str | None,
    output_name: str | None,
    settings: Settings,
) -> GeneratedImageResult:
    final_path = save_image_bytes(
        provider_image.data,
        provider_image.mime_type,
        out_dir or settings.default_output_dir,
        output_name or None,
    )
    return GeneratedImageResult(
        path=str(final_path),
        mime_type=provider_image.mime_type,
        provider=chosen_provider,
        model=provider_image.model,
    )


async def generate_image_artifact(
    *,
    prompt: str,
    provider: str = "openrouter",
    model: str | None = None,
    out_dir: str | None = None,
    aspect_ratio: str | None = "1:1",
    image_size: str | None = None,
    output_name: str | None = None,
    providers: Mapping[str, ImageProvider] | None = None,
    settings: Settings | None = None,
) -> GeneratedImageResult:
    settings = settings or Settings.from_env()
    providers = dict(providers or build_providers(settings))

    chosen_provider, adapter = _select_provider(provider, providers)
    provider_image = await adapter.generate(
        prompt=prompt,
        model=model or None,
        aspect_ratio=aspect_ratio or None,
        image_size=image_size or None,
    )
    return _persist_result(
        provider_image=provider_image,
        chosen_provider=chosen_provider,
        out_dir=out_dir,
        output_name=output_name,
        settings=settings,
    )


async def edit_image_artifact(
    *,
    input_path: str,
    prompt: str,
    provider: str = "openrouter",
    model: str | None = None,
    out_dir: str | None = None,
    aspect_ratio: str | None = "1:1",
    image_size: str | None = None,
    output_name: str | None = None,
    providers: Mapping[str, ImageProvider] | None = None,
    settings: Settings | None = None,
) -> GeneratedImageResult:
    settings = settings or Settings.from_env()
    providers = dict(providers or build_providers(settings))

    chosen_provider, adapter = _select_provider(provider, providers)
    source_image = load_local_image(input_path, settings)
    provider_image = await adapter.edit(
        source_image=source_image,
        prompt=prompt,
        model=model or None,
        aspect_ratio=aspect_ratio or None,
        image_size=image_size or None,
    )
    return _persist_result(
        provider_image=provider_image,
        chosen_provider=chosen_provider,
        out_dir=out_dir,
        output_name=output_name,
        settings=settings,
    )
