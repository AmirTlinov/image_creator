from __future__ import annotations

from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Any, cast

from PIL import Image

from image_creator.config import Settings
from image_creator.contracts import GeneratedImageResult
from image_creator.image_io import load_local_image
from image_creator.storage import save_image_bytes


def _assert_real_transparency(image_bytes: bytes) -> None:
    with Image.open(BytesIO(image_bytes)) as image:
        if image.mode not in {"RGBA", "LA"}:
            raise ValueError(
                "Background removal did not produce an alpha channel. "
                "The output is still opaque."
            )

        alpha_channel = image.getchannel("A")
        minimum_alpha, maximum_alpha = alpha_channel.getextrema()
        if minimum_alpha == 255:
            raise ValueError(
                "Background removal output is fully opaque. "
                "No transparent pixels were produced."
            )
        if maximum_alpha == 0:
            raise ValueError("Background removal output is fully transparent and unusable.")


@lru_cache(maxsize=4)
def _get_session(model_name: str) -> Any:
    from rembg import new_session  # type: ignore[import-untyped]

    return new_session(model_name)


def _remove_background_bytes(image_bytes: bytes, engine: str) -> bytes:
    from rembg import remove

    session = _get_session(engine)
    return cast(bytes, remove(image_bytes, session=session, force_return_bytes=True))


def remove_background_artifact(
    *,
    input_path: str,
    out_dir: str | None = None,
    output_name: str | None = None,
    engine: str = "u2net",
    settings: Settings | None = None,
) -> GeneratedImageResult:
    settings = settings or Settings.from_env()
    source_image = load_local_image(input_path, settings)
    removed_background = _remove_background_bytes(source_image.data, engine)
    _assert_real_transparency(removed_background)

    final_path = save_image_bytes(
        removed_background,
        "image/png",
        out_dir or settings.default_output_dir,
        output_name or None,
    )
    return GeneratedImageResult(
        path=str(final_path),
        mime_type="image/png",
        provider="local",
        model=f"rembg:{engine}",
        profile="remove_background",
    )
