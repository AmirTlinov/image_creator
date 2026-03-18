# Tool surface

This skill uses the local MCP server `image_creator`.

## Discovery

### `list_image_profiles`

Use first when you need to choose the right profile cheaply.

Output includes:
- `id`
- `provider`
- `model`
- `best_for`
- `supports_references`
- `recommended_aspect_ratio_behavior`
- `recommended_image_size_behavior`
- `notes`
- profile defaults for transparency / output format / quality when relevant

## Generation

### `generate_image`

Main inputs:
- `prompt`
- `profile`
- `provider`
- `model`
- `aspect_ratio`
- `image_size`
- `negative_prompt`
- `background_mode`
- `output_format`
- `quality_level`
- `reference_images`
- `out_dir`
- `output_name`

Returns a structured object:
- `path`
- `mime_type`
- `provider`
- `model`
- `profile`

## Editing

### `edit_image`

Same shape as `generate_image`, plus:
- `input_path` = editable base image

Important:
- `input_path` is the thing you edit
- `reference_images` are not extra editable bases

## Practical defaults

- current default provider = `openrouter`
- current default image model = `google/gemini-3.1-flash-image-preview`
- current higher-fidelity quality profile = `google/gemini-3-pro-image-preview`
- current balanced transparent-background profile = `openai/gpt-5-image`
- current fast transparent-background profile = `openai/gpt-5-image-mini`
- current premium cutout profile = `openai/gpt-5-image`
- Gemini direct code path exists, but is not live-proven in this environment until `GEMINI_API_KEY` exists

## Transparent background rule

In the current repo truth:
- Gemini-family image routes are not the transparent-background path
- transparent background / alpha channel / cutout tasks should use `transparent_bg`, `transparent_bg_fast`, or `cutout`

## Output contract

The real deliverable is always the saved file on disk.
When you answer the user, include the resulting file path whenever it matters.
