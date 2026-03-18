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
- OpenRouter generate and edit paths are implemented and live-proven in this environment
- default image model target is now `Gemini 3.1 Flash Image Preview`
- Gemini adapter is implemented, but still lacks live proof here because `GEMINI_API_KEY` is not configured
- repo truth must stay in sync with the actual code and verification evidence

## Next slices

1. keep docs and change notes aligned with real implementation state
2. close Gemini live proof once `GEMINI_API_KEY` is available
3. only then decide whether `OpenAIProvider` adds enough value to justify another adapter

## Update rule

Update this skill when repo-wide intent, provider policy, or the top-level tool contract changes.
