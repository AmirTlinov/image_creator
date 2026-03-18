import asyncio
from pathlib import Path

from image_creator.config import Settings
from image_creator.contracts import ProviderImage
from image_creator.image_io import LocalImageInput
from image_creator.service import edit_image_artifact, generate_image_artifact


class FakeProvider:
    name = "fake"
    default_model = "fake-model"

    async def generate(self, *, prompt, model, aspect_ratio, image_size, negative_prompt, reference_images):
        assert prompt == "hello"
        assert model is None
        assert aspect_ratio == "1:1"
        assert image_size is None
        assert negative_prompt is None
        assert reference_images == []
        return ProviderImage(data=b"png-bytes", mime_type="image/png", model=self.default_model)

    async def edit(self, *, source_image, prompt, model, aspect_ratio, image_size, negative_prompt, reference_images):
        assert isinstance(source_image, LocalImageInput)
        assert source_image.data == b"source"
        assert prompt == "edit this"
        assert model is None
        assert aspect_ratio == "1:1"
        assert image_size is None
        assert negative_prompt is None
        assert reference_images == []
        return ProviderImage(data=b"edited-bytes", mime_type="image/png", model=self.default_model)


def test_generate_image_artifact_writes_file(tmp_path):
    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "out",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    result = asyncio.run(
        generate_image_artifact(
            prompt="hello",
            provider="fake",
            settings=settings,
            providers={"fake": FakeProvider()},
        )
    )

    assert result.provider == "fake"
    assert result.model == "fake-model"
    assert result.mime_type == "image/png"
    assert result.profile == ""
    assert Path(result.path).exists()
    assert Path(result.path).read_bytes() == b"png-bytes"


def test_edit_image_artifact_reads_input_and_writes_output(tmp_path):
    source = tmp_path / "source.png"
    source.write_bytes(b"source")

    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "out",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    result = asyncio.run(
        edit_image_artifact(
            input_path="source.png",
            prompt="edit this",
            provider="fake",
            settings=settings,
            providers={"fake": FakeProvider()},
        )
    )

    assert Path(result.path).exists()
    assert Path(result.path).read_bytes() == b"edited-bytes"


def test_generate_image_artifact_applies_profile_defaults(tmp_path):
    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "out",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    class ProfileAwareFakeProvider(FakeProvider):
        async def generate(self, *, prompt, model, aspect_ratio, image_size, negative_prompt, reference_images):
            assert model == "google/gemini-3-pro-image-preview"
            assert image_size == "2K"
            return await super().generate(
                prompt=prompt,
                model=None,
                aspect_ratio=aspect_ratio,
                image_size=None,
                negative_prompt=negative_prompt,
                reference_images=reference_images,
            )

    result = asyncio.run(
        generate_image_artifact(
            prompt="hello",
            provider="openrouter",
            profile="quality",
            settings=settings,
            providers={"openrouter": ProfileAwareFakeProvider()},
        )
    )

    assert result.profile == "quality"
