# Architecture

## Goal

Turn multiple image APIs into one stable MCP tool:

`prompt -> provider API -> image bytes -> saved file -> absolute path returned to agent`

## Current component map

- `src/image_creator/server.py`
  - MCP entrypoint
  - owns tool registration and provider selection
- `src/image_creator/providers/`
  - one adapter per external API
  - owns request/response mapping and provider-specific parsing
- `src/image_creator/storage.py`
  - owns file naming, extension mapping, safe write-to-disk behavior
- `src/image_creator/contracts.py`
  - shared result payload shape returned by the tool
- `docs/contracts/generate-image.md`
  - canonical tool contract

## Invariants

1. The agent-facing tool contract stays provider-agnostic.
2. Provider payload shapes do not leak outside `providers/`.
3. The tool returns an absolute path, not only base64 or a transient URL.
4. File writes are centralized in `storage.py` so later edits, retention, and naming policy stay deterministic.
5. `edit_image` should be a separate tool later, not a hidden mode that muddies the first contract.

## Planned slices

1. Gemini adapter: `generateContent` -> `inlineData`
2. OpenRouter adapter: `/chat/completions` -> `message.images[*].image_url.url`
3. Real smoke proof that writes one file into `outputs/`
4. Optional `OpenAIProvider` and `edit_image` follow-up
