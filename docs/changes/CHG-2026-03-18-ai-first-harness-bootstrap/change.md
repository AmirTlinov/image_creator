# CHG-2026-03-18-ai-first-harness-bootstrap-and-implementation

Status: active
Owner: main-agent

## intent

Bootstrap an AI-first repository for the MCP image creator so future implementation happens against stable routing docs, skill-native memory, a documented tool contract, and a minimal runnable Python skeleton.

## done_criteria

- root routing docs exist
- root and domain-local skill registries exist
- `generate_image` contract is written down as canonical repo truth
- Python package skeleton and deterministic verify commands exist
- basic tests and import smoke pass

## non_goals

        - `edit_image` tool
        - packaging or release automation

## rollback

Revert this bootstrap change as one commit, or remove the added docs, skills, and Python scaffold if the repo direction changes.

## evidence

Executed on 2026-03-18:

- `make test` -> pass
- `make smoke` -> pass
- `make smoke-live` -> pass via OpenRouter, file written to `outputs/smoke/smoke-openrouter-default.png`
- `compas validate mode=ratchet` -> pass
- `compas gate kind=ci_fast` -> pass
- `codex mcp add image_creator` + `codex mcp list` + `codex mcp get image_creator` -> pass
- `codex exec ...` using MCP tool `generate_image` -> pass, file written to `outputs/codex_exec/codex-exec-smoke.png`
