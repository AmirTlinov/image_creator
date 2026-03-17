from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import dotenv_values


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "outputs"


def _load_repo_dotenv() -> dict[str, str]:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return {}

    loaded = dotenv_values(env_path)
    return {key: value for key, value in loaded.items() if key and value is not None}


def _getenv(name: str, fallback: str | None = None) -> str | None:
    if name in os.environ:
        return os.environ[name]
    return _load_repo_dotenv().get(name, fallback)


def _resolve_output_dir(value: str | None) -> Path:
    if not value:
        return DEFAULT_OUTPUT_DIR.resolve()

    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (REPO_ROOT / candidate).resolve()


@dataclass(frozen=True)
class Settings:
    repo_root: Path
    default_output_dir: Path
    gemini_api_key: str | None
    openrouter_api_key: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            repo_root=REPO_ROOT,
            default_output_dir=_resolve_output_dir(_getenv("IMAGE_OUTPUT_DIR")),
            gemini_api_key=_getenv("GEMINI_API_KEY"),
            openrouter_api_key=_getenv("OPENROUTER_API_KEY"),
        )
