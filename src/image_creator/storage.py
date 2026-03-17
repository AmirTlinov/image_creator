from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import uuid


MIME_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
}


def _normalize_output_name(output_name: str | None, suffix: str) -> str:
    if not output_name:
        return f"img-{uuid.uuid4().hex[:12]}{suffix}"

    stem = Path(output_name).name
    if not stem:
        return f"img-{uuid.uuid4().hex[:12]}{suffix}"
    if Path(stem).suffix:
        return stem
    return f"{stem}{suffix}"


def _reserve_output_path(root: Path, filename: str) -> Path:
    stem = Path(filename).stem
    suffix = Path(filename).suffix

    attempt = 1
    while True:
        candidate_name = filename if attempt == 1 else f"{stem}-{attempt}{suffix}"
        candidate_path = root / candidate_name
        try:
            fd = os.open(candidate_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            attempt += 1
            continue
        os.close(fd)
        return candidate_path


def save_image_bytes(
    data: bytes,
    mime_type: str,
    out_dir: str | Path,
    output_name: str | None = None,
) -> Path:
    suffix = MIME_EXTENSIONS.get(mime_type, ".bin")
    root = Path(out_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    filename = _normalize_output_name(output_name, suffix)
    final_path = _reserve_output_path(root, filename)

    with NamedTemporaryFile(dir=root, prefix="tmp-", suffix=".part", delete=False) as handle:
        handle.write(data)
        temp_path = Path(handle.name)

    temp_path.replace(final_path)
    return final_path
