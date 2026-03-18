# image_creator

Thin MCP server for image generation. Core contract: `generate_image` should always end by returning a real file path on disk.

## Start here by task

- Tool contract and file-output semantics -> `docs/contracts/generate-image.md`
- Edit tool contract -> `docs/contracts/edit-image.md`
- Image profiles and model-choice UX -> `docs/usage/codex-mcp.md`
- Codex MCP hookup and local smoke -> `docs/usage/codex-mcp.md`
- Repo-wide intent and guardrails -> `.agents/skills/repo-intent/SKILL.md`
- Server / adapter / storage implementation -> `src/image_creator/AGENTS.md`
- Current bootstrap slice -> `docs/changes/CHG-2026-03-18-ai-first-harness-bootstrap/change.md`

## Repo map

- `ARCHITECTURE.md` — current component map
- `.agents/skills/SKILLS.md` — root skill registry
- `src/image_creator/.agents/skills/SKILLS.md` — owning domain registry
- `Makefile` — bootstrap / test / smoke entrypoints
- `make smoke-transparent-live` — proof path for transparent-background generation via GPT image
- `make smoke-transparent-fast-live` / `make smoke-cutout-live` — proof paths for fast vs premium transparent asset workflows

## Verify

- `make bootstrap`
- `make test`
- `make smoke`
- `make check`
- `make verify-model-catalog`

Keep durable findings in the owning skill package, not only in chat.
