from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from image_creator.background_removal import _assert_real_transparency, remove_background_artifact
from image_creator.config import Settings


def _png_bytes(mode: str, color) -> bytes:
    image = Image.new(mode, (4, 4), color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _partially_transparent_png_bytes() -> bytes:
    image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
    image.putpixel((0, 0), (255, 0, 0, 0))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_assert_real_transparency_accepts_rgba_with_transparent_pixels():
    payload = _partially_transparent_png_bytes()

    _assert_real_transparency(payload)


def test_assert_real_transparency_rejects_opaque_png():
    payload = _png_bytes("RGB", (255, 0, 0))

    with pytest.raises(ValueError, match="opaque"):
        _assert_real_transparency(payload)


def test_remove_background_artifact_writes_png(monkeypatch, tmp_path):
    source = tmp_path / "source.jpg"
    source.write_bytes(b"fake-jpeg")
    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "out",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    transparent_png = _partially_transparent_png_bytes()

    monkeypatch.setattr(
        "image_creator.background_removal._remove_background_bytes",
        lambda image_bytes, engine: transparent_png,
    )

    result = remove_background_artifact(
        input_path="source.jpg",
        out_dir=str(tmp_path / "out"),
        output_name="removed-bg",
        settings=settings,
    )

    assert result.provider == "local"
    assert result.model == "rembg:u2net"
    assert result.profile == "remove_background"
    assert result.mime_type == "image/png"
    assert Path(result.path).exists()
