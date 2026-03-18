from __future__ import annotations

import argparse
import asyncio

from image_creator.service import edit_image_artifact, generate_image_artifact


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one real image and save it to disk.")
    parser.add_argument("--mode", choices=["generate", "edit"], default="generate")
    parser.add_argument("--provider", default="openrouter")
    parser.add_argument("--model", default="")
    parser.add_argument("--prompt", default="Minimal flat illustration of a banana on a white background")
    parser.add_argument("--aspect-ratio", default="1:1")
    parser.add_argument("--image-size", default="")
    parser.add_argument("--output-name", default="smoke-image")
    parser.add_argument("--out-dir", default="outputs/smoke")
    parser.add_argument("--input-path", default="")
    return parser.parse_args()


async def _main() -> None:
    args = parse_args()
    if args.mode == "generate":
        result = await generate_image_artifact(
            prompt=args.prompt,
            provider=args.provider,
            model=args.model or None,
            out_dir=args.out_dir,
            aspect_ratio=args.aspect_ratio or None,
            image_size=args.image_size or None,
            output_name=args.output_name or None,
        )
    else:
        if not args.input_path:
            raise ValueError("--input-path is required for --mode edit")
        result = await edit_image_artifact(
            input_path=args.input_path,
            prompt=args.prompt,
            provider=args.provider,
            model=args.model or None,
            out_dir=args.out_dir,
            aspect_ratio=args.aspect_ratio or None,
            image_size=args.image_size or None,
            output_name=args.output_name or None,
        )
    print(result.to_json())


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
