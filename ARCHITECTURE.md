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
3. The MCP tool returns a structured result object, not a JSON string wrapper.
4. The tool returns an absolute path, not only base64 or a transient URL.
5. File writes are centralized in `storage.py` and must allocate collision-safe sibling names instead of overwriting by default.
6. Provider HTTP retries and timeout handling stay inside `providers/common.py`.
7. `edit_image` should be a separate tool later, not a hidden mode that muddies the first contract.

## Planned slices

1. Close Gemini live proof once `GEMINI_API_KEY` is available in this environment
2. Optional `OpenAIProvider` follow-up if it adds real value over OpenRouter + Gemini direct
3. Keep `edit_image` as a separate tool and avoid collapsing it back into hidden `generate_image` modes
