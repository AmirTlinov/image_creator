from __future__ import annotations

import argparse
import asyncio

from image_creator.background_removal import remove_background_artifact
from image_creator.service import edit_image_artifact, generate_image_artifact


def _parse_reference_images(values: list[str]) -> list[dict[str, str]]:
    references: list[dict[str, str]] = []
    for value in values:
        try:
            role, path = value.split(":", 1)
        except ValueError as exc:
            raise ValueError(
                f"Invalid reference image '{value}'. Expected 'role:path'."
            ) from exc
        references.append({"role": role.strip(), "path": path.strip()})
    return references


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one real image and save it to disk.")
    parser.add_argument("--mode", choices=["generate", "edit", "remove_bg"], default="generate")
    parser.add_argument("--provider", default="openrouter")
    parser.add_argument("--model", default="")
    parser.add_argument("--profile", default="")
    parser.add_argument("--prompt", default="Minimal flat illustration of a banana on a white background")
    parser.add_argument("--aspect-ratio", default="1:1")
    parser.add_argument("--image-size", default="")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--background-mode", default="")
    parser.add_argument("--output-format", default="")
    parser.add_argument("--quality-level", default="")
    parser.add_argument("--reference-image", action="append", default=[])
    parser.add_argument("--output-name", default="smoke-image")
    parser.add_argument("--out-dir", default="outputs/smoke")
    parser.add_argument("--input-path", default="")
    parser.add_argument("--engine", default="u2net")
    return parser.parse_args()


async def _main() -> None:
    args = parse_args()
    reference_images = _parse_reference_images(args.reference_image)
    if args.mode == "generate":
        result = await generate_image_artifact(
            prompt=args.prompt,
            provider=args.provider,
            model=args.model or None,
            profile=args.profile or None,
            out_dir=args.out_dir,
            aspect_ratio=args.aspect_ratio or None,
            image_size=args.image_size or None,
            negative_prompt=args.negative_prompt or None,
            background_mode=args.background_mode or None,
            output_format=args.output_format or None,
            quality_level=args.quality_level or None,
            reference_images=reference_images,
            output_name=args.output_name or None,
        )
    elif args.mode == "edit":
        if not args.input_path:
            raise ValueError("--input-path is required for --mode edit")
        result = await edit_image_artifact(
            input_path=args.input_path,
            prompt=args.prompt,
            provider=args.provider,
            model=args.model or None,
            profile=args.profile or None,
            out_dir=args.out_dir,
            aspect_ratio=args.aspect_ratio or None,
            image_size=args.image_size or None,
            negative_prompt=args.negative_prompt or None,
            background_mode=args.background_mode or None,
            output_format=args.output_format or None,
            quality_level=args.quality_level or None,
            reference_images=reference_images,
            output_name=args.output_name or None,
        )
    else:
        if not args.input_path:
            raise ValueError("--input-path is required for --mode remove_bg")
        result = remove_background_artifact(
            input_path=args.input_path,
            out_dir=args.out_dir,
            output_name=args.output_name or None,
            engine=args.engine or "u2net",
        )
    print(result.to_json())


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
