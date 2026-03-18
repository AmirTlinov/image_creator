from __future__ import annotations

from typing import Protocol

from image_creator.contracts import ProviderImage
from image_creator.image_io import LocalImageInput


class ImageProvider(Protocol):
    name: str
    default_model: str

    async def generate(
        self,
        *,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
    ) -> ProviderImage:
        ...

    async def edit(
        self,
        *,
        source_image: LocalImageInput,
        prompt: str,
        model: str | None,
        aspect_ratio: str | None,
        image_size: str | None,
    ) -> ProviderImage:
        ...
