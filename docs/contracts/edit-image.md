# `edit_image` contract

Second MCP tool for this repo.

## Intent

Take an existing local image file, send it to a provider together with an edit prompt, save the edited result to disk, and return a structured result object.

## Input

- `input_path: str` — required local path to the source image, absolute or repo-relative
- `prompt: str` — required edit instruction
- `profile: str` — optional curated profile such as `edit`, `quality`, `text_heavy`, `style_transfer`, `character_consistency`
- `provider: str` — optional; defaults to `openrouter`
- `model: str` — optional provider-specific override
- `out_dir: str` — optional output directory; defaults to `IMAGE_OUTPUT_DIR` or `./outputs`
- `aspect_ratio: str` — optional provider-supported ratio such as `1:1`, `16:9`, `9:16`
- `image_size: str` — optional provider-supported size such as `1K`, `2K`, `4K`
- `negative_prompt: str` — optional explicit constraints for things that must not appear
- `reference_images: list[{path, role}]` — optional non-editable references with roles `style`, `subject`, `object`, `character`, `layout`
- `output_name: str` — optional preferred filename stem; collisions are resolved by sibling suffixes

## Success output

The MCP tool returns a structured object:

```json
{
  "path": "/abs/path/to/outputs/banana-with-glasses.png",
  "mime_type": "image/png",
  "provider": "openrouter",
  "model": "google/gemini-3.1-flash-image-preview",
  "profile": "edit"
}
```

## Behavioral invariants

- resolve repo-relative input paths against the repo root
- reject missing or non-image files early
- keep the source image unchanged
- return an absolute path to the edited file
- do not overwrite an existing output path; allocate a collision-safe sibling name instead
- `input_path` is always the editable base image
- `reference_images` are guidance-only and must not be treated as extra editable bases

## Provider mapping notes

### OpenRouter

- endpoint: `/api/v1/chat/completions`
- editing request uses a `messages[0].content` array with text + `image_url`
- local source files are sent as base64 data URLs
- current proven default model: `google/gemini-3.1-flash-image-preview`

### Gemini

- endpoint family: `models/{model}:generateContent`
- editing request sends both text and `inline_data` parts in the same `contents` item
- code path exists, but live proof in this environment still depends on `GEMINI_API_KEY`
