from __future__ import annotations

import base64
import mimetypes
from dataclasses import dataclass
from pathlib import Path

from image_creator.config import Settings


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
