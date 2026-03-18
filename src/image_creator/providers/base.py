from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from image_creator.contracts import ProviderImage
from image_creator.image_io import LocalImageInput, ReferenceImageInput


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
        negative_prompt: str | None = None,
        reference_images: Sequence[ReferenceImageInput] = (),
        background_mode: str | None = None,
        output_format: str | None = None,
        quality_level: str | None = None,
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
        negative_prompt: str | None = None,
        reference_images: Sequence[ReferenceImageInput] = (),
        background_mode: str | None = None,
        output_format: str | None = None,
        quality_level: str | None = None,
    ) -> ProviderImage:
        ...
