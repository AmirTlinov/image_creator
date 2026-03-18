# Codex MCP usage

## Add the server to `~/.codex/config.toml`

```bash
codex mcp add image_creator -- \
  /home/amir/.local/bin/uv \
  --directory /media/amir/documents/projects/mcp/image_creator \
  run image-creator-mcp
```

This keeps the server tied to the repo checkout, so it can read `.env`, write into `outputs/`, and use the local source tree directly.

## Verify config state

```bash
codex mcp list
codex mcp get image_creator
```

## Real smoke from the repo

```bash
make smoke-live
make smoke-edit-live
make smoke-transparent-live
make verify-model-catalog
```

Expected result: JSON with `path`, `mime_type`, `provider`, and `model`, and a real file created under `outputs/`.
For the MCP tool itself, the result is a structured object with those same fields.

## Example tool call

Before choosing a model manually, ask the repo for curated defaults:

```json
{}
```

Tool: `list_image_profiles`

Use tool `generate_image` with arguments like:

```json
{
  "prompt": "Simple flat illustration of a banana on a white background",
  "profile": "draft",
  "out_dir": "outputs/codex_exec",
  "output_name": "codex-exec-smoke"
}
```

Higher-quality final pass:

```json
{
  "prompt": "Premium skincare jar on a clean white studio background",
  "profile": "quality",
  "aspect_ratio": "4:5",
  "output_name": "jar-final"
}
```

Transparent background / cutout:

```json
{
  "prompt": "Clean isolated product cutout of a red sneaker",
  "profile": "transparent_bg",
  "output_name": "sneaker-cutout"
}
```

Example edit call:

```json
{
  "input_path": "outputs/source.png",
  "prompt": "Add black sunglasses and keep the white background",
  "profile": "edit",
  "out_dir": "outputs/codex_exec",
  "output_name": "codex-edit-smoke"
}
```

Reference-aware style transfer:

```json
{
  "input_path": "outputs/source.png",
  "prompt": "Keep the composition. Render it as a tactile 3D illustration.",
  "profile": "style_transfer",
  "reference_images": [
    {"path": "refs/style.png", "role": "style"}
  ],
  "output_name": "source-restyled"
}
```

## Notes

- Current default provider is `openrouter`.
- Current proven OpenRouter default model is `google/gemini-3.1-flash-image-preview`.
- Transparent background generation is intentionally routed to `openai/gpt-5-image` through OpenRouter.
- In the current repo truth, Gemini-family image paths do not support true transparent-background generation.
- Old preview aliases like `google/gemini-2.5-flash-image-preview` are normalized to the working stable model.
- Profiles are the preferred default; explicit `model` override is for exceptional cases.
- `make check` runs lint + typecheck + tests + import smoke without adding a heavy CI layer.
- `make verify-model-catalog` is the drift check for curated OpenRouter image models.
- Gemini code path is implemented, but still not live-proven on this machine until `GEMINI_API_KEY` is set.
- If you change `~/.codex/config.toml` while a Codex chat is already running, restart that session before expecting the new MCP server to appear.
