import pytest

from image_creator.image_profiles import list_profiles, resolve_image_selection


def test_list_profiles_contains_quality_profile():
    profiles = list_profiles()

    assert any(profile["id"] == "quality" for profile in profiles)


def test_quality_profile_resolves_to_gemini_3_pro():
    resolved = resolve_image_selection(
        provider="openrouter",
        model=None,
        profile="quality",
        image_size=None,
        background_mode=None,
        output_format=None,
        quality_level=None,
    )

    assert resolved.provider == "openrouter"
    assert resolved.model == "google/gemini-3-pro-image-preview"
    assert resolved.profile == "quality"
    assert resolved.image_size == "2K"


def test_explicit_model_override_beats_profile_default_model():
    resolved = resolve_image_selection(
        provider="openrouter",
        model="google/gemini-3.1-flash-image-preview",
        profile="quality",
        image_size=None,
        background_mode=None,
        output_format=None,
        quality_level=None,
    )

    assert resolved.model == "google/gemini-3.1-flash-image-preview"
    assert resolved.profile == "quality"


def test_profile_provider_mismatch_fails():
    with pytest.raises(ValueError, match="requires provider"):
        resolve_image_selection(
            provider="gemini",
            model=None,
            profile="quality",
            image_size=None,
            background_mode=None,
            output_format=None,
            quality_level=None,
        )


def test_incompatible_provider_and_model_fails():
    with pytest.raises(ValueError, match="incompatible with provider"):
        resolve_image_selection(
            provider="gemini",
            model="google/gemini-3.1-flash-image-preview",
            profile=None,
            image_size=None,
            background_mode=None,
            output_format=None,
            quality_level=None,
        )


def test_transparent_bg_profile_resolves_to_openai_gpt_image():
    resolved = resolve_image_selection(
        provider="openrouter",
        model=None,
        profile="transparent_bg",
        image_size=None,
        background_mode=None,
        output_format=None,
        quality_level=None,
    )

    assert resolved.model == "openai/gpt-5-image"
    assert resolved.background_mode == "transparent"
    assert resolved.output_format == "png"
    assert resolved.quality_level == "medium"
