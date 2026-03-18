from __future__ import annotations

from collections.abc import Mapping, Sequence

from image_creator.config import Settings
from image_creator.contracts import GeneratedImageResult, ProviderImage
from image_creator.image_io import load_local_image, load_reference_images
from image_creator.image_profiles import list_profiles, resolve_image_selection
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
    profile: str,
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
        profile=profile,
    )


def list_image_profiles() -> dict[str, list[dict[str, object]]]:
    return {"profiles": list_profiles()}


def _validate_feature_compatibility(
    *,
    provider: str,
    model: str | None,
    background_mode: str | None,
    output_format: str | None,
    quality_level: str | None,
) -> None:
    normalized_model = (model or "").strip()
    normalized_background_mode = (background_mode or "").strip().lower()
    normalized_output_format = (output_format or "").strip().lower()
    normalized_quality_level = (quality_level or "").strip().lower()

    is_gemini_family = provider == "gemini" or normalized_model.startswith("google/gemini") or normalized_model.startswith("gemini-")
    is_openai_gpt_image = normalized_model.startswith("openai/gpt-5-image")

    if normalized_background_mode == "transparent":
        if not is_openai_gpt_image:
            raise ValueError(
                "Transparent background is not supported on the current Gemini image paths. "
                "Use the `transparent_bg` profile or an OpenAI GPT image model."
            )
        if normalized_output_format and normalized_output_format not in {"png", "webp"}:
            raise ValueError(
                "Transparent background requires `output_format` to be `png` or `webp`."
            )

    if normalized_output_format and not is_openai_gpt_image:
        raise ValueError(
            "`output_format` is currently only supported on the OpenAI GPT image route."
        )

    if normalized_quality_level and not is_openai_gpt_image:
        raise ValueError(
            "`quality_level` is currently only supported on the OpenAI GPT image route."
        )


async def generate_image_artifact(
    *,
    prompt: str,
    provider: str = "openrouter",
    model: str | None = None,
    profile: str | None = None,
    out_dir: str | None = None,
    aspect_ratio: str | None = "1:1",
    image_size: str | None = None,
    negative_prompt: str | None = None,
    reference_images: Sequence[Mapping[str, str]] | None = None,
    background_mode: str | None = None,
    output_format: str | None = None,
    quality_level: str | None = None,
    output_name: str | None = None,
    providers: Mapping[str, ImageProvider] | None = None,
    settings: Settings | None = None,
) -> GeneratedImageResult:
    settings = settings or Settings.from_env()
    providers = dict(providers or build_providers(settings))
    resolved_selection = resolve_image_selection(
        provider=provider,
        model=model,
        profile=profile,
        image_size=image_size,
        background_mode=background_mode,
        output_format=output_format,
        quality_level=quality_level,
    )
    loaded_reference_images = load_reference_images(reference_images, settings)
    _validate_feature_compatibility(
        provider=resolved_selection.provider,
        model=resolved_selection.model,
        background_mode=resolved_selection.background_mode,
        output_format=resolved_selection.output_format,
        quality_level=resolved_selection.quality_level,
    )

    chosen_provider, adapter = _select_provider(resolved_selection.provider, providers)
    provider_image = await adapter.generate(
        prompt=prompt,
        model=resolved_selection.model,
        aspect_ratio=aspect_ratio or None,
        image_size=resolved_selection.image_size,
        negative_prompt=negative_prompt or None,
        reference_images=loaded_reference_images,
        background_mode=resolved_selection.background_mode,
        output_format=resolved_selection.output_format,
        quality_level=resolved_selection.quality_level,
    )
    return _persist_result(
        provider_image=provider_image,
        chosen_provider=chosen_provider,
        profile=resolved_selection.profile,
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
    profile: str | None = None,
    out_dir: str | None = None,
    aspect_ratio: str | None = "1:1",
    image_size: str | None = None,
    negative_prompt: str | None = None,
    reference_images: Sequence[Mapping[str, str]] | None = None,
    background_mode: str | None = None,
    output_format: str | None = None,
    quality_level: str | None = None,
    output_name: str | None = None,
    providers: Mapping[str, ImageProvider] | None = None,
    settings: Settings | None = None,
) -> GeneratedImageResult:
    settings = settings or Settings.from_env()
    providers = dict(providers or build_providers(settings))
    resolved_selection = resolve_image_selection(
        provider=provider,
        model=model,
        profile=profile,
        image_size=image_size,
        background_mode=background_mode,
        output_format=output_format,
        quality_level=quality_level,
    )
    loaded_reference_images = load_reference_images(reference_images, settings)
    _validate_feature_compatibility(
        provider=resolved_selection.provider,
        model=resolved_selection.model,
        background_mode=resolved_selection.background_mode,
        output_format=resolved_selection.output_format,
        quality_level=resolved_selection.quality_level,
    )

    chosen_provider, adapter = _select_provider(resolved_selection.provider, providers)
    source_image = load_local_image(input_path, settings)
    provider_image = await adapter.edit(
        source_image=source_image,
        prompt=prompt,
        model=resolved_selection.model,
        aspect_ratio=aspect_ratio or None,
        image_size=resolved_selection.image_size,
        negative_prompt=negative_prompt or None,
        reference_images=loaded_reference_images,
        background_mode=resolved_selection.background_mode,
        output_format=resolved_selection.output_format,
        quality_level=resolved_selection.quality_level,
    )
    return _persist_result(
        provider_image=provider_image,
        chosen_provider=chosen_provider,
        profile=resolved_selection.profile,
        out_dir=out_dir,
        output_name=output_name,
        settings=settings,
    )
