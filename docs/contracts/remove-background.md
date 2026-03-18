# `remove_background` contract

Deterministic cutout tool for existing local images.

## Intent

Take an existing image file, remove its background with a local background-removal engine, save a transparent PNG to disk, and return a structured result object.

## Input

- `input_path: str` — required local path to the source image
- `out_dir: str` — optional output directory; defaults to `IMAGE_OUTPUT_DIR` or `./outputs`
- `output_name: str` — optional filename stem
- `engine: str` — optional local cutout engine name; current default is `u2net`

## Success output

```json
{
  "path": "/abs/path/to/outputs/cutout.png",
  "mime_type": "image/png",
  "provider": "local",
  "model": "rembg:u2net",
  "profile": "remove_background"
}
```

## Behavioral invariants

- `input_path` is always the source image to cut out
- output is always written as PNG
- the tool fails if the result does not contain real transparency
- this tool is the preferred path for removing the background from an already existing image

## Why this tool exists

Background removal is not the same job as semantic image editing.
Use:
- `generate_image` for new assets
- `edit_image` for semantic changes
- `remove_background` for deterministic cutout / alpha extraction
