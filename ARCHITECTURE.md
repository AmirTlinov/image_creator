# Architecture

## Goal

Turn multiple image APIs into one stable MCP tool:

`prompt -> provider API -> image bytes -> saved file -> absolute path returned to agent`

## Current component map

- `src/image_creator/server.py`
  - MCP entrypoint
  - owns tool registration and profile-discovery surface
- `src/image_creator/providers/`
  - one adapter per external API
  - owns request/response mapping and provider-specific parsing
- `src/image_creator/image_profiles.py`
  - owns curated model-selection profiles and provider/model compatibility checks
- `src/image_creator/prompting.py`
  - owns deterministic prompt assembly for reference images and negative constraints
- `src/image_creator/storage.py`
  - owns file naming, extension mapping, safe write-to-disk behavior
- `src/image_creator/contracts.py`
  - shared result payload shape returned by the tool
- `docs/contracts/generate-image.md`
  - canonical tool contract

## Invariants

1. The agent-facing tool contract stays provider-agnostic and profile-first.
2. Provider payload shapes do not leak outside `providers/`.
3. The MCP tools return structured result objects, not JSON string wrappers.
4. The tools return absolute paths, not only base64 or transient URLs.
5. File writes are centralized in `storage.py` and must allocate collision-safe sibling names instead of overwriting by default.
6. Provider HTTP retries and timeout handling stay inside `providers/common.py`.
7. `generate_image` and `edit_image` stay separate tools; `edit_image` owns the editable base image semantics.
8. Transparent background generation is a GPT-image-only path in the current repo truth; Gemini-family image paths must fail early for this request instead of silently producing opaque images.

## Planned slices

1. Close Gemini live proof once `GEMINI_API_KEY` is available in this environment
2. Optional `OpenAIProvider` follow-up if it adds real value over OpenRouter + Gemini direct
3. Revisit video only as a separate layer rather than overloading the image surface
