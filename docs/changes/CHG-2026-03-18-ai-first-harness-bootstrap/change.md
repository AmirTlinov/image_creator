# CHG-2026-03-18-ai-first-harness-bootstrap-and-implementation

Status: active
Owner: main-agent

## intent

Bootstrap and complete the first flagship implementation of the MCP image creator so future work happens against stable routing docs, skill-native memory, a documented tool contract, a profile-first model-selection layer, and a small but real verification loop.

## done_criteria

- root routing docs exist
- root and domain-local skill registries exist
- `generate_image` and `edit_image` contracts are written down as canonical repo truth
- `remove_background` contract is written down as canonical repo truth
- OpenRouter generate and edit paths are implemented and live-proven
- curated profile-first model selection exists with explicit raw model override
- `list_image_profiles` gives the agent a cheap discovery surface
- transparent-background generation is routed to a GPT-image profile instead of the Gemini path
- visible distributable skill package exists under `skills/image-generation/` for external agents
- deterministic background removal exists as a separate tool instead of being forced through `edit_image`
- deterministic verify commands exist
- lint, typecheck, tests, import smoke, and ci_fast gate pass

## non_goals

- packaging or release automation
- pretending Gemini is live-proven without a real `GEMINI_API_KEY`

## rollback

Revert this bootstrap change as one commit, or remove the added docs, skills, and Python scaffold if the repo direction changes.

## evidence

Executed on 2026-03-18:

- `make check` -> pass
- `make verify-model-catalog` -> pass, curated OpenRouter model ids present
- `make test` -> pass
- `make smoke` -> pass
- `make smoke-live` -> pass via OpenRouter, file written to `outputs/smoke/smoke-image-4.png`
- `make smoke-edit-live` -> pass via OpenRouter, file written to `outputs/smoke_edit_result/smoke-edit-result-3.png`
- `make smoke-transparent-live` -> pass via OpenRouter GPT-image route, file written to `outputs/transparent_proofs/smoke-transparent-proof.png` and detected as `RGBA`
- `make smoke-transparent-fast-live` -> pass via OpenRouter GPT-image-mini route, file written to `outputs/transparent_proofs/smoke-transparent-fast-proof.png` and detected as `RGBA`
- `make smoke-cutout-live` -> pass via OpenRouter GPT-image route, file written to `outputs/transparent_proofs/smoke-cutout-proof.png` and detected as `RGBA`
- `make smoke-remove-bg-live` -> pass via local `rembg:u2net` route, file written to `outputs/remove_bg_result/smoke-remove-bg-proof.png` and detected as `RGBA`
- `compas validate mode=ratchet` -> pass
- `compas gate kind=ci_fast` -> pass
- `codex mcp add image_creator` + `codex mcp list` + `codex mcp get image_creator` -> pass
- `codex exec ...` using MCP tool `generate_image` -> pass, structured MCP result proven, file written to `outputs/codex_exec/codex-exec-structured.png`
- `codex exec ...` using MCP tool `edit_image` -> pass, structured MCP result proven, file written to `outputs/codex_exec/codex-edit-structured.png`
- `uv run python -m image_creator.smoke --profile quality ...` -> pass, file written to `outputs/profile_proofs/profile-quality-proof.jpg`
- `uv run python -m image_creator.smoke --mode edit --profile style_transfer --reference-image style:...` -> pass, file written to `outputs/profile_proofs/style-transfer-proof.png`
- `codex exec ...` using `list_image_profiles` then `edit_image(profile=style_transfer, reference_images=[...])` -> pass, file written to `outputs/codex_exec/codex-style-transfer-proof.png`
- `codex exec ...` using `generate_image(profile=transparent_bg)` -> pass, file written to `outputs/codex_exec/codex-transparent-proof.png`
- default image model moved to `Gemini 3.1 Flash Image Preview`; current OpenRouter models API exposes `google/gemini-3.1-flash-image-preview`
- `skills/image-generation` -> copied into the repo as a visible distributable skill and validated with `quick_validate.py`

## known_gap

- Gemini implementation is code-complete and test-covered, but still lacks live proof in this environment because `GEMINI_API_KEY` is unset as of 2026-03-18.
