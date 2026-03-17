# image_creator domain

Owns the MCP server, provider adapters, shared contracts, and file-output semantics.

## Start here

- local skill registry -> `.agents/skills/SKILLS.md`
- tool contract -> `../../docs/contracts/generate-image.md`
- component map -> `../../ARCHITECTURE.md`

## Local map

- `server.py` -> tool registration and provider routing
- `providers/` -> provider-specific HTTP + parsing
- `storage.py` -> output path policy and safe writes
- `contracts.py` -> shared result payloads

## Verify

- `uv run pytest tests/test_storage.py tests/test_server.py`
