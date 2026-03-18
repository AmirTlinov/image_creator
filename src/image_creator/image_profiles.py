from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageProfile:
    id: str
    provider: str
    model: str
    best_for: tuple[str, ...]
    supports_references: bool
    recommended_aspect_ratio_behavior: str
    recommended_image_size_behavior: str
    notes: str
    default_image_size: str | None = None
    default_background_mode: str | None = None
    default_output_format: str | None = None
    default_quality_level: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "provider": self.provider,
            "model": self.model,
            "best_for": list(self.best_for),
            "supports_references": self.supports_references,
            "recommended_aspect_ratio_behavior": self.recommended_aspect_ratio_behavior,
            "recommended_image_size_behavior": self.recommended_image_size_behavior,
            "notes": self.notes,
            "default_background_mode": self.default_background_mode,
            "default_output_format": self.default_output_format,
            "default_quality_level": self.default_quality_level,
        }


IMAGE_PROFILES: dict[str, ImageProfile] = {
    "draft": ImageProfile(
        id="draft",
        provider="openrouter",
        model="google/gemini-3.1-flash-image-preview",
        best_for=("fast iteration", "composition drafts", "high-volume exploration"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Set explicitly for the target surface; default 1:1 is only a safe fallback.",
        recommended_image_size_behavior="Leave unset for cheap drafts unless detail matters.",
        notes="Fastest default profile for first-pass generation and iterative edits.",
    ),
    "quality": ImageProfile(
        id="quality",
        provider="openrouter",
        model="google/gemini-3-pro-image-preview",
        best_for=("highest fidelity", "final passes", "brand-facing assets"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Always set explicitly based on final output format.",
        recommended_image_size_behavior='Prefer "2K" when output detail matters.',
        notes="Use when the draft is already correct and quality is the priority.",
        default_image_size="2K",
    ),
    "text_heavy": ImageProfile(
        id="text_heavy",
        provider="openrouter",
        model="google/gemini-3-pro-image-preview",
        best_for=("in-image text", "logos", "marketing copy", "layout-critical typography"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Set explicitly to the final canvas ratio before generating.",
        recommended_image_size_behavior='Prefer "2K" for text clarity.',
        notes="Best default when text accuracy is more important than generation speed.",
        default_image_size="2K",
    ),
    "edit": ImageProfile(
        id="edit",
        provider="openrouter",
        model="google/gemini-3.1-flash-image-preview",
        best_for=("surgical edits", "small changes", "quick correction loops"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Keep the base image ratio unless a deliberate resize is needed.",
        recommended_image_size_behavior="Match the base image unless a higher detail pass is needed.",
        notes="Default profile for changing details while preserving the original asset.",
    ),
    "character_consistency": ImageProfile(
        id="character_consistency",
        provider="openrouter",
        model="google/gemini-3.1-flash-image-preview",
        best_for=("recurring characters", "identity preservation", "style-consistent variations"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Set explicitly for the target shot format.",
        recommended_image_size_behavior='Use "2K" when faces or costume details matter.',
        notes="Use character references and keep prompts narrow and incremental.",
        default_image_size="2K",
    ),
    "style_transfer": ImageProfile(
        id="style_transfer",
        provider="openrouter",
        model="google/gemini-3.1-flash-image-preview",
        best_for=("restyling", "look development", "same composition with a new rendering style"),
        supports_references=True,
        recommended_aspect_ratio_behavior="Preserve the original ratio unless the style task requires reframing.",
        recommended_image_size_behavior='Use "2K" when texture or surface detail matters.',
        notes="Best when one image establishes composition and another establishes rendering style.",
        default_image_size="2K",
    ),
    "transparent_bg": ImageProfile(
        id="transparent_bg",
        provider="openrouter",
        model="openai/gpt-5-image",
        best_for=("transparent background", "clean cutouts", "isolated assets"),
        supports_references=False,
        recommended_aspect_ratio_behavior="Set explicitly to the target asset ratio before generating.",
        recommended_image_size_behavior='Use "2K" only if the cutout needs extra detail; otherwise rely on the GPT image quality dial.',
        notes="Use when alpha channel matters. Avoid Gemini-family models for this workflow.",
        default_background_mode="transparent",
        default_output_format="png",
        default_quality_level="medium",
    ),
}


OPENROUTER_CATALOG_MODELS = sorted(
    {profile.model for profile in IMAGE_PROFILES.values() if profile.provider == "openrouter"}
)


def list_profiles() -> list[dict[str, object]]:
    return [profile.to_dict() for profile in IMAGE_PROFILES.values()]


def get_profile(profile_id: str) -> ImageProfile:
    normalized = profile_id.strip().lower()
    if not normalized:
        raise ValueError("Profile id must not be empty.")
    try:
        return IMAGE_PROFILES[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(IMAGE_PROFILES))
        raise ValueError(f"Unsupported profile '{profile_id}'. Expected one of: {supported}") from exc


def validate_provider_model_compatibility(*, provider: str, model: str) -> None:
    normalized_provider = provider.strip().lower()
    normalized_model = model.strip()
    if not normalized_model:
        return

    if normalized_provider == "openrouter":
        if "/" not in normalized_model:
            raise ValueError(
                f"Model '{model}' does not look like an OpenRouter model id; expected '<vendor>/<model>'."
            )
        return

    if normalized_provider == "gemini":
        if "/" in normalized_model or not normalized_model.startswith("gemini-"):
            raise ValueError(
                f"Model '{model}' is incompatible with provider 'gemini'; expected a direct Gemini model id."
            )
        return

    raise ValueError(f"Unsupported provider '{provider}'.")


@dataclass(frozen=True)
class ResolvedImageSelection:
    provider: str
    model: str | None
    profile: str
    image_size: str | None
    background_mode: str | None
    output_format: str | None
    quality_level: str | None


def resolve_image_selection(
    *,
    provider: str,
    model: str | None,
    profile: str | None,
    image_size: str | None,
    background_mode: str | None,
    output_format: str | None,
    quality_level: str | None,
) -> ResolvedImageSelection:
    requested_provider = provider.strip().lower()
    requested_model = model.strip() if model else ""
    requested_profile = profile.strip().lower() if profile else ""
    requested_image_size = image_size.strip() if image_size else ""
    requested_background_mode = background_mode.strip().lower() if background_mode else ""
    requested_output_format = output_format.strip().lower() if output_format else ""
    requested_quality_level = quality_level.strip().lower() if quality_level else ""

    if requested_profile:
        chosen_profile = get_profile(requested_profile)
        if requested_provider and requested_provider != chosen_profile.provider:
            raise ValueError(
                f"Profile '{requested_profile}' requires provider '{chosen_profile.provider}', not '{provider}'."
            )
        resolved_provider = chosen_profile.provider
        resolved_model = requested_model or chosen_profile.model
        validate_provider_model_compatibility(provider=resolved_provider, model=resolved_model)
        return ResolvedImageSelection(
            provider=resolved_provider,
            model=resolved_model,
            profile=chosen_profile.id,
            image_size=requested_image_size or chosen_profile.default_image_size,
            background_mode=requested_background_mode or chosen_profile.default_background_mode,
            output_format=requested_output_format or chosen_profile.default_output_format,
            quality_level=requested_quality_level or chosen_profile.default_quality_level,
        )

    validate_provider_model_compatibility(provider=requested_provider, model=requested_model)
    return ResolvedImageSelection(
        provider=requested_provider,
        model=requested_model or None,
        profile="",
        image_size=requested_image_size or None,
        background_mode=requested_background_mode or None,
        output_format=requested_output_format or None,
        quality_level=requested_quality_level or None,
    )
