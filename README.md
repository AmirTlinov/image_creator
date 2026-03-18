# image_creator

AI-first repository for a thin MCP image-generation server.

Goal: expose one stable MCP tool that lets an agent send a prompt to a provider API and get back a file path on disk. The provider can be Gemini, OpenRouter, OpenAI, or another adapter later. The contract stays the same.

## Current status

- root routing docs and skill-native memory are in place
- real OpenRouter generate and edit paths work and write image files to disk
- transparent background generation now routes to GPT-image via OpenRouter
- Gemini adapter is implemented but not live-smoked here because no `GEMINI_API_KEY` is configured
- `generate_image` and `edit_image` contracts are documented
- current default image model is `Gemini 3.1 Flash Image Preview`
- curated image profiles exist so the agent can choose task-specific defaults without guessing raw model ids

## Quick start

```bash
cp .env.example .env
make bootstrap
make check
make smoke-live
make smoke-edit-live
make smoke-transparent-live
make verify-model-catalog
```

`make check` is intentionally small but real: lint + typecheck + tests + import smoke.

## Repo map

- `AGENTS.md` — fast routing for future agents
- `ARCHITECTURE.md` — current system map and invariants
- `docs/contracts/generate-image.md` — tool contract
- `docs/contracts/edit-image.md` — edit contract
- `.agents/skills/` — repo-wide intent and routing
- `src/image_creator/` — owning domain for server, adapters, storage

## Current operating model

1. agent calls `list_image_profiles` to choose `draft`, `quality`, `text_heavy`, `edit`, `character_consistency`, or `style_transfer`
2. agent can still override `provider` and `model` explicitly for exceptional cases
3. `reference_images` let the agent send role-tagged refs like `style`, `object`, or `character`
4. `transparent_bg` chooses the GPT-image route because Gemini cannot produce true transparent backgrounds in this tool surface
5. Gemini live smoke still waits on `GEMINI_API_KEY`

## Codex MCP hookup

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
