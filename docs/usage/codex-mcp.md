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
```

Expected result: JSON with `path`, `mime_type`, `provider`, and `model`, and a real file created under `outputs/`.
For the MCP tool itself, the result is a structured object with those same fields.

## Example tool call

Use tool `generate_image` with arguments like:

```json
{
  "prompt": "Simple flat illustration of a banana on a white background",
  "provider": "openrouter",
  "out_dir": "outputs/codex_exec",
  "output_name": "codex-exec-smoke"
}
```

Example edit call:

```json
{
  "input_path": "outputs/smoke/smoke-openrouter-default.png",
  "prompt": "Add black sunglasses and keep the white background",
  "provider": "openrouter",
  "out_dir": "outputs/codex_exec",
  "output_name": "codex-edit-smoke"
}
```

## Notes

- Current default provider is `openrouter`.
- Current proven OpenRouter default model is `google/gemini-3.1-flash-image-preview`.
- Old preview aliases like `google/gemini-2.5-flash-image-preview` are normalized to the working stable model.
- `make check` runs lint + typecheck + tests + import smoke without adding a heavy CI layer.
- Gemini code path is implemented, but still not live-proven on this machine until `GEMINI_API_KEY` is set.
- If you change `~/.codex/config.toml` while a Codex chat is already running, restart that session before expecting the new MCP server to appear.
