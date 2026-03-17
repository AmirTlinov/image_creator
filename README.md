# image_creator

AI-first repository for a thin MCP image-generation server.

Goal: expose one stable MCP tool that lets an agent send a prompt to a provider API and get back a file path on disk. The provider can be Gemini, OpenRouter, OpenAI, or another adapter later. The contract stays the same.

## Current status

- root routing docs and skill-native memory are in place
- real OpenRouter adapter works and writes image files to disk
- Gemini adapter is implemented but not live-smoked here because no `GEMINI_API_KEY` is configured
- `generate_image` tool contract is documented

## Quick start

```bash
cp .env.example .env
make bootstrap
make check
make smoke-live
```

## Repo map

- `AGENTS.md` — fast routing for future agents
- `ARCHITECTURE.md` — current system map and invariants
- `docs/contracts/generate-image.md` — tool contract
- `.agents/skills/` — repo-wide intent and routing
- `src/image_creator/` — owning domain for server, adapters, storage

## First implementation slice

1. live-smoked OpenRouter path is done
2. next real follow-up is Gemini live smoke once `GEMINI_API_KEY` exists
3. after that, decide whether `edit_image` deserves a second tool

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
