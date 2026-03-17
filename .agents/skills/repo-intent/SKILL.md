---
name: repo-intent
description: Repo-wide mission, guardrails, and next slices for the image_creator MCP server.
---

# Repo intent

## Mission

Build a thin MCP server that turns image-generation APIs into one stable local artifact contract: prompt in, file path out.

## Global constraints

- prefer one MCP tool with a small explicit API over many clever helper tools
- keep provider-specific request and response logic inside adapter modules
- the agent-facing success payload must stay provider-agnostic
- the file path on disk is the primary artifact; inline base64 is only an internal transport detail
- avoid orchestration theater, fake docs, and broad speculative scaffolding

## Current repo state

- bootstrap docs and skill-native memory are installed
- Python package skeleton exists
- Gemini and OpenRouter adapters are intentionally scaffolded, not implemented

## Next slices

1. implement Gemini adapter end-to-end
2. implement OpenRouter adapter end-to-end
3. add real smoke proof for one generated image written to disk
4. only then decide whether `edit_image` deserves a second tool

## Update rule

Update this skill when repo-wide intent, provider policy, or the top-level tool contract changes.
