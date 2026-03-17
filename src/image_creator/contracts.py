from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class ProviderImage:
    data: bytes
    mime_type: str
    model: str


@dataclass(frozen=True)
class GeneratedImageResult:
    path: str
    mime_type: str
    provider: str
    model: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
