from __future__ import annotations

import base64
import mimetypes
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from image_creator.config import Settings

VALID_REFERENCE_ROLES = frozenset({"style", "subject", "object", "character", "layout"})
MAX_TOTAL_REFERENCE_IMAGES = 14
MAX_CHARACTER_REFERENCES = 4
MAX_NON_CHARACTER_REFERENCES = 10


@dataclass(frozen=True)
class LocalImageInput:
    path: Path
    mime_type: str
    data: bytes

    def to_data_url(self) -> str:
        encoded = base64.b64encode(self.data).decode("ascii")
        return f"data:{self.mime_type};base64,{encoded}"

    def to_gemini_inline_data(self) -> dict[str, str]:
        encoded = base64.b64encode(self.data).decode("ascii")
        return {
            "mime_type": self.mime_type,
            "data": encoded,
        }


@dataclass(frozen=True)
class ReferenceImageInput:
    image: LocalImageInput
    role: str

    def to_data_url(self) -> str:
        return self.image.to_data_url()

    def to_gemini_inline_data(self) -> dict[str, str]:
        return self.image.to_gemini_inline_data()


def resolve_repo_path(path_value: str, settings: Settings) -> Path:
    candidate = Path(path_value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (settings.repo_root / candidate).resolve()


def load_local_image(path_value: str, settings: Settings) -> LocalImageInput:
    path = resolve_repo_path(path_value, settings)
    if not path.exists():
        raise FileNotFoundError(f"Input image does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input image path is not a file: {path}")

    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Could not infer an image MIME type from: {path.name}")

    return LocalImageInput(
        path=path,
        mime_type=mime_type,
        data=path.read_bytes(),
    )


def load_reference_images(
    reference_images: Sequence[Mapping[str, str]] | None,
    settings: Settings,
) -> list[ReferenceImageInput]:
    if not reference_images:
        return []

    loaded: list[ReferenceImageInput] = []
    character_count = 0
    non_character_count = 0

    for raw_reference in reference_images:
        path_value = raw_reference.get("path", "").strip()
        role = raw_reference.get("role", "").strip().lower()

        if not path_value:
            raise ValueError("Each reference image must include a non-empty 'path'.")
        if role not in VALID_REFERENCE_ROLES:
            supported = ", ".join(sorted(VALID_REFERENCE_ROLES))
            raise ValueError(
                f"Unsupported reference image role '{raw_reference.get('role', '')}'. Expected one of: {supported}."
            )

        if role == "character":
            character_count += 1
        else:
            non_character_count += 1

        loaded.append(ReferenceImageInput(image=load_local_image(path_value, settings), role=role))

    if len(loaded) > MAX_TOTAL_REFERENCE_IMAGES:
        raise ValueError(
            f"Too many reference images: {len(loaded)}. Current Gemini-family limit is {MAX_TOTAL_REFERENCE_IMAGES}."
        )
    if character_count > MAX_CHARACTER_REFERENCES:
        raise ValueError(
            f"Too many character references: {character_count}. Current Gemini-family limit is {MAX_CHARACTER_REFERENCES}."
        )
    if non_character_count > MAX_NON_CHARACTER_REFERENCES:
        raise ValueError(
            f"Too many non-character references: {non_character_count}. Current Gemini-family limit is {MAX_NON_CHARACTER_REFERENCES}."
        )

    return loaded
