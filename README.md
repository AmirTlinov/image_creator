# image_creator

`image_creator` is a practical MCP server for agents that need to **generate or edit images and get real files on disk**, not just blobs in chat.

It is built around one simple idea:

> choose the right profile, send the prompt, save the artifact, keep iterating.

## What it can do

- generate new images
- edit existing local images
- remove the background from an existing local image through a deterministic cutout path
- use role-tagged reference images (`style`, `object`, `character`, etc.)
- switch between fast draft, high-fidelity, text-heavy, style-transfer, and character-consistency workflows
- generate **transparent PNG assets** through the GPT-image path when Gemini is the wrong tool for the job

## Why it is useful

Most image tooling makes agents think in raw model ids and provider quirks.
This repo gives them a cheaper mental model:

- ask `list_image_profiles`
- choose a profile like `draft`, `quality`, `edit`, `style_transfer`, `transparent_bg`
- use `generate_image` or `edit_image`
- use `remove_background` when the task is actually cutout / alpha extraction
- get back a saved file path

That keeps the surface small while still letting advanced users override `provider` and `model` when they really need to.

## Profiles at a glance

- `draft` — fast first-pass composition
- `quality` — higher-fidelity final pass
- `text_heavy` — assets with meaningful text inside
- `edit` — narrow corrections to an existing image
- `style_transfer` — same composition, new rendering style
- `character_consistency` — identity-preserving variants
- `transparent_bg` — balanced transparent-background generation
- `transparent_bg_fast` — cheaper/faster transparent draft path
- `cutout` — higher-fidelity isolated transparent asset path
- `remove_background` — deterministic background removal for an already existing image

## Quick start

```bash
cp .env.example .env
make bootstrap
make check
make smoke-live
make smoke-edit-live
make smoke-transparent-live
make smoke-transparent-fast-live
make smoke-cutout-live
make smoke-remove-bg-live
make verify-model-catalog
```

`make check` stays intentionally compact: lint + typecheck + tests + import smoke.

## For agents

- start with `AGENTS.md`
- reusable distributable skill lives in `skills/image-generation/`
- contracts live in `docs/contracts/`
- current MCP usage examples live in `docs/usage/codex-mcp.md`

If you are wiring this into Codex locally:

```bash
codex mcp add image_creator -- \
  /home/amir/.local/bin/uv \
  --directory /media/amir/documents/projects/mcp/image_creator \
  run image-creator-mcp
```

Then verify:

```bash
codex mcp list
codex mcp get image_creator
```

Active Codex chats usually need restart to see the new server.
