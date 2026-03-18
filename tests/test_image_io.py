from pathlib import Path

import pytest

from image_creator.config import Settings
from image_creator.image_io import load_local_image


def test_load_local_image_resolves_relative_repo_path(tmp_path):
    image_path = tmp_path / "cat.png"
    image_path.write_bytes(b"png-bytes")
    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "outputs",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    image = load_local_image("cat.png", settings)

    assert image.path == image_path.resolve()
    assert image.mime_type == "image/png"
    assert image.data == b"png-bytes"


def test_load_local_image_rejects_missing_file(tmp_path):
    settings = Settings(
        repo_root=tmp_path,
        default_output_dir=tmp_path / "outputs",
        gemini_api_key=None,
        openrouter_api_key=None,
    )

    with pytest.raises(FileNotFoundError):
        load_local_image("missing.png", settings)
