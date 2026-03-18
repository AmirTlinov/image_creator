---
name: image-pipeline
description: Owns MCP tool registration, provider adapters, profile-first model selection, storage, and local planning for image generation/editing.
---

# image pipeline

## Owns

- MCP tool registration
- provider adapter boundaries
- curated profile-first model selection
- file naming and persistence contract
- local implementation planning for `generate_image` and `edit_image`

## Invariants

- `server.py` should stay thin and provider-agnostic
- curated profiles should be the default UX; raw `model` ids are override-only
- `storage.py` owns final path creation and atomic-ish writes
- adapter modules own provider HTTP payloads and response parsing
- successful tool results are structured objects with `path`, `mime_type`, `provider`, `model`, and `profile`

## Current local tasks

1. keep curated profiles aligned with live provider reality
2. keep reference-image semantics deterministic and role-based
3. close Gemini live proof once `GEMINI_API_KEY` is available

## Safe change order

1. update the contract if the agent-facing shape changes
2. update one provider adapter
3. keep storage behavior centralized
4. prove with tests and smoke
