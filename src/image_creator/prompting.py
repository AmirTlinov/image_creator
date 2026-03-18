from __future__ import annotations

from collections.abc import Sequence

from image_creator.image_io import ReferenceImageInput


def compose_image_instruction(
    *,
    prompt: str,
    negative_prompt: str | None,
    reference_images: Sequence[ReferenceImageInput],
    include_editable_base_image: bool,
) -> str:
    sections = [prompt.strip()]

    if include_editable_base_image:
        sections.append(
            "Editable base image: Image 1. Modify this image directly and treat any later images only as references."
        )

    if reference_images:
        start_index = 2 if include_editable_base_image else 1
        reference_lines = ["Reference images:"]
        for index, reference in enumerate(reference_images, start=start_index):
            reference_lines.append(f"- Image {index}: role={reference.role}")
        sections.append("\n".join(reference_lines))

    if negative_prompt and negative_prompt.strip():
        sections.append(f"Negative constraints: {negative_prompt.strip()}")

    return "\n\n".join(section for section in sections if section.strip())
