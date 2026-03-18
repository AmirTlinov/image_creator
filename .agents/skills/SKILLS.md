# Root skill registry

## Project-wide skills

- `repo-intent` -> repo-wide mission, guardrails, and next slices
- `skills/image-generation/SKILL.md` -> reusable visible skill package for external agents using the repo MCP surface

## Domain entrypoints

- `src/image_creator/.agents/skills/SKILLS.md` -> owning domain for MCP server, adapters, storage, and tool contract implementation

## Read order

1. `repo-intent`
2. owning domain skill for the code you will touch
