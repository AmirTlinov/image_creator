# image_creator

AI-first repository for a thin MCP image-generation server.

Goal: expose one stable MCP tool that lets an agent send a prompt to a provider API and get back a file path on disk. The provider can be Gemini, OpenRouter, OpenAI, or another adapter later. The contract stays the same.

## Current status

- root routing docs and skill-native memory are in place
- real OpenRouter generate and edit paths work and write image files to disk
- Gemini adapter is implemented but not live-smoked here because no `GEMINI_API_KEY` is configured
- `generate_image` and `edit_image` contracts are documented

## Quick start

```bash
cp .env.example .env
make bootstrap
make check
make smoke-live
make smoke-edit-live
```

`make check` is intentionally small but real: lint + typecheck + tests + import smoke.

## Repo map

- `AGENTS.md` — fast routing for future agents
- `ARCHITECTURE.md` — current system map and invariants
- `docs/contracts/generate-image.md` — tool contract
- `.agents/skills/` — repo-wide intent and routing
- `src/image_creator/` — owning domain for server, adapters, storage

## First implementation slice

1. live-smoked OpenRouter generate path is done
2. live-smoked OpenRouter edit path is done
3. Gemini live smoke still waits on `GEMINI_API_KEY`

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
