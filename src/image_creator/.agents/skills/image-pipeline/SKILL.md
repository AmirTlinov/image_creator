---
name: image-pipeline
description: Owns MCP tool registration, provider adapters, storage, and local planning for generate_image.
---

# image pipeline

## Owns

- MCP tool registration
- provider adapter boundaries
- file naming and persistence contract
- local implementation planning for `generate_image`

## Invariants

- `server.py` should stay thin and provider-agnostic
- `storage.py` owns final path creation and atomic-ish writes
- adapter modules own provider HTTP payloads and response parsing
- the first successful tool result is always a JSON string with `path`, `mime_type`, `provider`, `model`

## Current local tasks

1. implement `GeminiProvider.generate()` using `generateContent` and `inlineData`
2. implement `OpenRouterProvider.generate()` using chat completions and data-URL decoding
3. add tests for response parsing and one real smoke path to `outputs/`

## Safe change order

1. update the contract if the agent-facing shape changes
2. update one provider adapter
3. keep storage behavior centralized
4. prove with tests and smoke
