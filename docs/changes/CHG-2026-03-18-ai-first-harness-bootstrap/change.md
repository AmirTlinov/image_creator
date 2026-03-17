# CHG-2026-03-18-ai-first-harness-bootstrap-and-implementation

Status: active
Owner: main-agent

## intent

Bootstrap and complete the first flagship implementation of the MCP image creator so future work happens against stable routing docs, skill-native memory, a documented tool contract, and a small but real verification loop.

## done_criteria

- root routing docs exist
- root and domain-local skill registries exist
- `generate_image` contract is written down as canonical repo truth
- OpenRouter path is implemented and live-proven
- deterministic verify commands exist
- lint, typecheck, tests, import smoke, and ci_fast gate pass

## non_goals

- `edit_image` tool
- packaging or release automation
- pretending Gemini is live-proven without a real `GEMINI_API_KEY`

## rollback

Revert this bootstrap change as one commit, or remove the added docs, skills, and Python scaffold if the repo direction changes.

## evidence

Executed on 2026-03-18:

- `make check` -> pass
- `make test` -> pass
- `make smoke` -> pass
- `make smoke-live` -> pass via OpenRouter, file written to `outputs/smoke/smoke-openrouter-default.png`
- `compas validate mode=ratchet` -> pass
- `compas gate kind=ci_fast` -> pass
- `codex mcp add image_creator` + `codex mcp list` + `codex mcp get image_creator` -> pass
- `codex exec ...` using MCP tool `generate_image` -> pass, structured MCP result proven, file written to `outputs/codex_exec/codex-exec-structured.png`

## known_gap

- Gemini implementation is code-complete and test-covered, but still lacks live proof in this environment because `GEMINI_API_KEY` is unset as of 2026-03-18.
